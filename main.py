from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import sqlite3
import pandas as pd
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
    safe_score: float
    risk_factor: float
    total_penalty: float
    star_rating: int
    acceleration_score: float
    braking_score: float
    cornering_score: float
    speeding_score: float
    phone_usage_score: float

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
            safe_score=safe_score,
            risk_factor=round(risk_factor, 4),
            total_penalty=round(total_penalty, 4),
            star_rating=star,
            acceleration_score=round(acc_score, 4),
            braking_score=round(dec_score, 4),
            cornering_score=round(cor_score, 4),
            speeding_score=round(spd_score, 4),
            phone_usage_score=round(phone_score, 4)
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
        return trip_data
        
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
            "total": len(result),
            "limit": limit,
            "offset": offset,
            "data": result.to_dict('records')
        }
        
    except Exception as e:
        logger.error(f"Error fetching scores: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching scores: {str(e)}")

# ============ DRIFT DETECTION ENDPOINTS ============
"""
@app.post("/check-drift", response_model=DriftResponse)
async def check_drift(request: List[Dict[str, Any]]):
    
    try:
        # Convert to DataFrame
        current_data = pd.DataFrame(request)
        
        # Initialize drift detection config
        drift_config = DriftConfig(
            drift_threshold=0.1,
            retraining_threshold=0.15,
            numerical_features=[
            'acceleration_x_original', 'acceleration_y_original', 'acceleration_z_original',
            'acceleration', 'deceleration', 'midSpeed'
            ],
            target_column='safe_score',
            #data_path=config['database']['sqlite_path']
        )
        
        # Initialize drift monitoring system
        drift_system = ADWINDriftMonitoring(
            drift_config, 
            db_path=config['database']['sqlite_path'], 
            table_name='SampleTable'
        )
        
        # Run drift detection
        result = drift_system.run_cycle()
        
        if "drift" not in result:
            return DriftResponse(
                drift_detected=False,
                overall_drift_score=0.0,
                feature_drifts={},
                timestamp=datetime.now().isoformat()
            )
        
        drift_result = result["drift"]
        
        return DriftResponse(
            drift_detected=drift_result.get("drift_detected", False),
            overall_drift_score=drift_result.get("overall_drift_score", 0.0),
            feature_drifts=drift_result.get("feature_drifts", {}),
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error in drift detection: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in drift detection: {str(e)}")
""" 
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

        # Initialize drift monitoring system with reference DB
        drift_system = ADWINDriftMonitoring(
            config=drift_config,
            db_path=config['database']['sqlite_path'],
            table_name='SampleTable'
        )

        # Run the drift detection cycle
        result = drift_system.run_cycle()

        if "drift" not in result:
            return DriftResponse(
                drift_detected=False,
                overall_drift_score=0.0,
                feature_drifts={},
                timestamp=datetime.now().isoformat()
            )

        drift_result = result["drift"]

        return DriftResponse(
            drift_detected=drift_result.get("drift_detected", False),
            overall_drift_score=drift_result.get("overall_drift_score", 0.0),
            feature_drifts=drift_result.get("feature_drifts", {}),
            timestamp=datetime.now().isoformat()
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
            stats["tables"][table] = {"row_count": count}
        
        conn.close()
        
        return stats
        
    except Exception as e:
        logger.error(f"Error getting database stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting database stats: {str(e)}")

# ============ CONFIGURATION ENDPOINTS ============

@app.get("/config")
async def get_config():
    """Get current configuration"""
    return config

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
        
        return {
            "average_safety_score": float(recent_scores.iloc[0]['avg_score']) if not recent_scores.empty else 0,
            "total_trips_scored": int(recent_scores.iloc[0]['total_trips']) if not recent_scores.empty else 0,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting metrics: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 


