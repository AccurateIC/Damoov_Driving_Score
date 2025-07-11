from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import sqlite3
import pandas as pd
import numpy as np
import json
import yaml
from datetime import datetime
import logging
import sys
import os

# Add src/app to the import path
sys.path.append(os.path.join(os.path.dirname(__file__), "src", "app"))

# Import your custom modules
from score_pipeline import run_score_pipeline
from drift_detector import ADWINDriftMonitoring, DriftConfig
from Formulation.scorers import (
    DamoovAccelerationScorer,
    DamoovDeccelerationScorer,
    DamoovCorneringScorer,
    SpeedingDetectorFixedLimit,
    PhoneUsageDetector
)

# ============ NUMPY SERIALIZATION UTILITY ============

def convert_numpy_types(obj):
    """Convert NumPy types to native Python types for JSON serialization"""
    if isinstance(obj, dict):
        return {k: convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif pd.isna(obj):
        return None
    return obj

def safe_to_dict(df):
    """Safely convert DataFrame to dict with NumPy type conversion"""
    records = df.to_dict('records')
    return convert_numpy_types(records)

# Initialize FastAPI app
app = FastAPI(title="Driving Score & Drift Detection API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

config = load_config()

# ============ PYDANTIC MODELS ============

class TripData(BaseModel):
    unique_id: str
    device_id: Optional[str] = None  # Add device_id field
    timestamp: float
    latitude: float
    longitude: float
    speed_kmh: float
    acceleration: float
    deceleration: float
    acceleration_y: float
    screen_on: int
    screen_blocked: int

class BatchTripData(BaseModel):
    trips: List[TripData]

class ScoreResponse(BaseModel):
    unique_id: str
    device_id: Optional[str] = None
    safe_score: float
    risk_factor: float
    total_penalty: float
    star_rating: int
    acceleration_score: float
    braking_score: float
    cornering_score: float
    speeding_score: float
    phone_usage_score: float

class DriverScoreResponse(BaseModel):
    device_id: str
    average_safe_score: float
    average_risk_factor: float
    average_star_rating: float
    total_trips: int
    score_distribution: Dict[str, int]  # star_rating -> count
    latest_trip_date: Optional[str] = None

class DriftCheckRequest(BaseModel):
    data: List[Dict[str, Any]]

class DriftResponse(BaseModel):
    drift_detected: bool
    overall_drift_score: float
    feature_drifts: Dict[str, float]
    timestamp: str

# ============ DATABASE UTILITIES ============

def get_db_connection():
    return sqlite3.connect(config['database']['sqlite_path'])

def execute_query(query: str, params=None):
    conn = get_db_connection()
    try:
        if params:
            result = pd.read_sql_query(query, conn, params=params)
        else:
            result = pd.read_sql_query(query, conn)
        return result
    finally:
        conn.close()

# ============ API ENDPOINTS ============

@app.get("/")
async def root():
    return {"message": "Driving Score & Drift Detection API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    try:
        # Test database connection
        conn = get_db_connection()
        conn.execute("SELECT 1")
        conn.close()
        return {"status": "healthy", "timestamp": datetime.now().isoformat()}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")

# ============ SCORING ENDPOINTS ============
from Formulation.distance_utils import calculate_trip_distance_from_points

@app.post("/calculate-score", response_model=ScoreResponse)
async def calculate_single_trip_score(trip_data: List[TripData]):
    """Calculate driving score for a single trip"""
    try:
        # Convert to DataFrame
        df = pd.DataFrame([t.dict() for t in trip_data])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        
        # Assume trip distance (you can calculate this from GPS coordinates)
        trip_distance = calculate_trip_distance_from_points(df) # Default value, should be calculated
        if trip_distance <= 0:
           trip_distance = 1.0

        weights = config['weights']
        
        # Calculate individual scores
        acc = DamoovAccelerationScorer(**config['acceleration'])
        acc.df = df
        acc.detect_events()
        acc.calculate_penalties()
        acc_score = acc.get_events()['penalty_acc'].sum() if not acc.get_events().empty else 0
        
        dec = DamoovDeccelerationScorer(**config['deceleration'])
        dec.df = df
        dec.detect_events()
        dec.calculate_penalties()
        dec_score = dec.get_events()['penalty_braking'].sum() if not dec.get_events().empty else 0
        
        cor = DamoovCorneringScorer(**config['cornering'])
        cor.df = df
        cor.detect_events()
        cor.calculate_penalties()
        cor_score = cor.get_events()['penalty_cornering'].sum() if not cor.get_events().empty else 0
        
        spd = SpeedingDetectorFixedLimit(**config['speeding'])
        spd.df = df
        spd.detect_speeding()
        spd.assign_penalties()
        spd_score = spd.get_events()['penalty_speeding'].sum() if not spd.get_events().empty else 0
        
        phone = PhoneUsageDetector(**config['phone_usage'])
        phone.df = df
        phone.detect_phone_usage()
        phone.assign_penalties()
        phone_score = phone.get_events()['penalty_phone'].sum() if not phone.get_events().empty else 0
        
        # Calculate total penalty and score
        total_penalty = (
            weights["acceleration_weight"] * acc_score +
            weights["braking_weight"] * dec_score +
            weights["cornering_weight"] * cor_score +
            weights["speeding_weight"] * spd_score +
            weights["phone_usage_weight"] * phone_score
        )
        
        risk_factor = total_penalty / trip_distance if trip_distance > 0 else 1
        safe_score = round(100 * (1 / (1 + risk_factor)), 2)
        star = 5 if safe_score == 100 else 4 if safe_score >= 90 else 3 if safe_score >= 80 else 2 if safe_score >= 70 else 1
        
        return ScoreResponse(
            unique_id=trip_data[0].unique_id,
            device_id=trip_data[0].device_id,
            safe_score=float(safe_score),
            risk_factor=float(round(risk_factor, 4)),
            total_penalty=float(round(total_penalty, 4)),
            star_rating=int(star),
            acceleration_score=float(round(acc_score, 4)),
            braking_score=float(round(dec_score, 4)),
            cornering_score=float(round(cor_score, 4)),
            speeding_score=float(round(spd_score, 4)),
            phone_usage_score=float(round(phone_score, 4))
        )
        
    except Exception as e:
        logger.error(f"Error calculating score: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error calculating score: {str(e)}")

@app.post("/batch-calculate-scores")
async def batch_calculate_scores(background_tasks: BackgroundTasks):
    """Run the full scoring pipeline on all trips in the database"""
    try:
        background_tasks.add_task(run_score_pipeline, config['database']['sqlite_path'], config)
        return {"message": "Batch scoring started in background", "status": "processing"}
    except Exception as e:
        logger.error(f"Error starting batch scoring: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error starting batch scoring: {str(e)}")

@app.get("/scores/{unique_id}")
async def get_trip_score(unique_id: str):
    """Get calculated score for a specific trip"""
    try:
        query = "SELECT * FROM SampleTable WHERE unique_id = ?"
        result = execute_query(query, params=(unique_id,))
        
        if result.empty:
            raise HTTPException(status_code=404, detail="Trip not found")
        
        trip_data = result.iloc[0].to_dict()
        return convert_numpy_types(trip_data)
        
    except Exception as e:
        logger.error(f"Error fetching trip score: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching trip score: {str(e)}")

@app.get("/scores")
async def get_all_scores(limit: int = 100, offset: int = 0):
    """Get all calculated scores with pagination"""
    try:
        query = f"SELECT * FROM SampleTable LIMIT {limit} OFFSET {offset}"
        result = execute_query(query)
        
        return {
            "total": int(len(result)),
            "limit": int(limit),
            "offset": int(offset),
            "data": safe_to_dict(result)
        }
        
    except Exception as e:
        logger.error(f"Error fetching scores: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching scores: {str(e)}")

# ============ NEW DRIVER SCORE ENDPOINTS ============

@app.get("/driver-score/{device_id}", response_model=DriverScoreResponse)
async def get_driver_score(device_id: str):
    """Get aggregated driving score for a specific device/driver"""
    try:
        # Query to get all trips for this device
        query = """
        SELECT unique_id, device_id, safe_score, risk_factor, star_rating, timestamp
        FROM SampleTable 
        WHERE device_id = ? AND safe_score IS NOT NULL
        """
        result = execute_query(query, params=(device_id,))
        
        if result.empty:
            raise HTTPException(status_code=404, detail="No trips found for this device ID")
        
        # Calculate aggregated metrics
        avg_safe_score = float(round(result['safe_score'].mean(), 2))
        avg_risk_factor = float(round(result['risk_factor'].mean(), 4))
        avg_star_rating = float(round(result['star_rating'].mean(), 1))
        total_trips = int(len(result))
        
        # Calculate score distribution
        score_distribution = result['star_rating'].value_counts().to_dict()
        score_distribution = {str(k): int(v) for k, v in score_distribution.items()}
        
        # Get latest trip date
        latest_trip = None
        if 'timestamp' in result.columns:
            latest_trip = result['timestamp'].max()
            if pd.notna(latest_trip):
                latest_trip = str(latest_trip)
        
        return DriverScoreResponse(
            device_id=device_id,
            average_safe_score=avg_safe_score,
            average_risk_factor=avg_risk_factor,
            average_star_rating=avg_star_rating,
            total_trips=total_trips,
            score_distribution=score_distribution,
            latest_trip_date=latest_trip
        )
        
    except Exception as e:
        logger.error(f"Error fetching driver score: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching driver score: {str(e)}")

@app.get("/driver-scores")
async def get_all_driver_scores(limit: int = 100, offset: int = 0):
    """Get aggregated scores for all drivers with pagination"""
    try:
        # Query to get all device IDs and their aggregated scores
        query = """
        SELECT 
            device_id,
            COUNT(*) as total_trips,
            ROUND(AVG(safe_score), 2) as avg_safe_score,
            ROUND(AVG(risk_factor), 4) as avg_risk_factor,
            ROUND(AVG(star_rating), 1) as avg_star_rating,
            MAX(timestamp) as latest_trip_date
        FROM SampleTable 
        WHERE device_id IS NOT NULL AND safe_score IS NOT NULL
        GROUP BY device_id
        ORDER BY avg_safe_score DESC
        LIMIT ? OFFSET ?
        """
        result = execute_query(query, params=(limit, offset))
        
        # Get total count for pagination
        count_query = """
        SELECT COUNT(DISTINCT device_id) as total_drivers
        FROM SampleTable 
        WHERE device_id IS NOT NULL AND safe_score IS NOT NULL
        """
        total_count = execute_query(count_query)
        total_drivers = int(total_count.iloc[0]['total_drivers']) if not total_count.empty else 0
        
        return {
            "total_drivers": total_drivers,
            "limit": int(limit),
            "offset": int(offset),
            "data": safe_to_dict(result)
        }
        
    except Exception as e:
        logger.error(f"Error fetching driver scores: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching driver scores: {str(e)}")

@app.get("/driver-trips/{device_id}")
async def get_driver_trips(device_id: str, limit: int = 50, offset: int = 0):
    """Get all trips for a specific driver with pagination"""
    try:
        query = """
        SELECT unique_id, device_id, safe_score, risk_factor, star_rating, timestamp
        FROM SampleTable 
        WHERE device_id = ? AND safe_score IS NOT NULL
        ORDER BY timestamp DESC
        LIMIT ? OFFSET ?
        """
        result = execute_query(query, params=(device_id, limit, offset))
        
        # Get total count for this driver
        count_query = """
        SELECT COUNT(*) as total_trips
        FROM SampleTable 
        WHERE device_id = ? AND safe_score IS NOT NULL
        """
        total_count = execute_query(count_query, params=(device_id,))
        total_trips = int(total_count.iloc[0]['total_trips']) if not total_count.empty else 0
        
        if result.empty:
            raise HTTPException(status_code=404, detail="No trips found for this device ID")
        
        return {
            "device_id": device_id,
            "total_trips": total_trips,
            "limit": int(limit),
            "offset": int(offset),
            "data": safe_to_dict(result)
        }
        
    except Exception as e:
        logger.error(f"Error fetching driver trips: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching driver trips: {str(e)}")

# ============ DRIFT DETECTION ENDPOINTS ============

@app.post("/check-drift", response_model=DriftResponse)
async def check_drift(request: List[Dict[str, Any]]):
    """Check for data drift using ADWINDriftMonitoring"""
    try:
        # Convert request JSON to DataFrame
        current_data = pd.DataFrame(request)

        # Initialize drift detection configuration
        drift_config = DriftConfig(
            drift_threshold=0.1,
            retraining_threshold=0.15,
            numerical_features=[
                'acceleration_x_original', 'acceleration_y_original', 'acceleration_z_original',
                'acceleration', 'deceleration', 'midSpeed'
            ],
            target_column='safe_score',
        )

        # Embed your DB & table into the config
        drift_config.reference_db_path = config['database']['sqlite_path']
        drift_config.current_db_path   = config['database']['sqlite_path']
        drift_config.table_name        = 'SampleTable'

        # Only pass the config now
        drift_system = ADWINDriftMonitoring(drift_config)
        result = drift_system.run()

        # If no drift detected, return zeros
        if not result.get("drift_detected", False):
            return DriftResponse(
                drift_detected=False,
                overall_drift_score=0.0,
                feature_drifts={},
                timestamp=datetime.now().isoformat()
            )

        # Otherwise unpack the real result with type conversion
        return DriftResponse(
            drift_detected      = bool(result["drift_detected"]),
            overall_drift_score = float(result["average_drift_score"]),
            feature_drifts      = convert_numpy_types(result["feature_drifts"]),
            timestamp           = datetime.now().isoformat()
        )

    except Exception as e:
        logger.error(f"Error in drift detection: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in drift detection: {str(e)}")

# ============ DATA MANAGEMENT ENDPOINTS ============

@app.post("/upload-trip-data")
async def upload_trip_data(trip_data: List[TripData]):
    """Upload new trip data to the database"""
    try:
        df = pd.DataFrame([t.dict() for t in trip_data])
        
        conn = get_db_connection()
        df.to_sql("SampleTable", conn, if_exists="append", index=False)
        conn.close()
        
        return {"message": f"Successfully uploaded {len(trip_data)} trip data points"}
        
    except Exception as e:
        logger.error(f"Error uploading trip data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error uploading trip data: {str(e)}")

@app.get("/database-stats")
async def get_database_stats():
    """Get database statistics"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get table info
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        stats = {"tables": {}}
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            stats["tables"][table] = {"row_count": int(count)}
        
        conn.close()
        
        return stats
        
    except Exception as e:
        logger.error(f"Error getting database stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting database stats: {str(e)}")

# ============ CONFIGURATION ENDPOINTS ============

@app.get("/config")
async def get_config():
    """Get current configuration"""
    return convert_numpy_types(config)

@app.put("/config")
async def update_config(new_config: dict):
    """Update configuration (be careful with this in production!)"""
    try:
        global config
        config.update(new_config)
        
        # Save to file
        with open("config.yaml", "w") as f:
            yaml.dump(config, f)
        
        return {"message": "Configuration updated successfully"}
        
    except Exception as e:
        logger.error(f"Error updating config: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating config: {str(e)}")

# ============ MONITORING ENDPOINTS ============

@app.get("/metrics")
async def get_metrics():
    """Get system metrics (could be enhanced with Prometheus metrics)"""
    try:
        conn = get_db_connection()
        
        # Get recent scores
        recent_scores = pd.read_sql_query(
            "SELECT AVG(safe_score) as avg_score, COUNT(*) as total_trips FROM SampleTable WHERE safe_score IS NOT NULL",
            conn
        )
        
        conn.close()
        
        avg_score = recent_scores.iloc[0]['avg_score'] if not recent_scores.empty else 0
        total_trips = recent_scores.iloc[0]['total_trips'] if not recent_scores.empty else 0
        
        return {
            "average_safety_score": float(avg_score) if avg_score is not None else 0.0,
            "total_trips_scored": int(total_trips),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting metrics: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

