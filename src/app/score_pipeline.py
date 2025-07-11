import pandas as pd
import sqlite3
from math import radians, sin, cos, acos
from pathlib import Path
import yaml

from Formulation.scorers import (
    DamoovAccelerationScorer,
    DamoovDeccelerationScorer,
    DamoovCorneringScorer,
    SpeedingDetectorFixedLimit,
    PhoneUsageDetector
)

# Load config
def load_config():
    base_dir = Path(__file__).resolve().parent
    with open(base_dir / "config.yaml", "r") as f:
        return yaml.safe_load(f)

# Calculate spherical distance
def spherical_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    return R * acos(sin(lat1)*sin(lat2) + cos(lat1)*cos(lat2)*cos(lon2 - lon1))

# Calculate trip distances
def calculate_trip_distances(start_df, stop_df):
    start_df = start_df.rename(columns={'latitude': 'start_lat', 'longitude': 'start_lon'})
    stop_df = stop_df.rename(columns={'latitude': 'end_lat', 'longitude': 'end_lon'})

    start_min = start_df.groupby("UNIQUE_ID")["ID"].idxmin()
    stop_max = stop_df.groupby("UNIQUE_ID")["ID"].idxmax()

    start_points = start_df.loc[start_min].copy()
    end_points = stop_df.loc[stop_max].copy()

    merged = pd.merge(start_points, end_points[['UNIQUE_ID', 'end_lat', 'end_lon']], on='UNIQUE_ID')
    merged["distance_km"] = merged.apply(
        lambda row: spherical_distance(row["start_lat"], row["start_lon"], row["end_lat"], row["end_lon"]), axis=1
    )
    return merged[["UNIQUE_ID", "distance_km"]]

# Calculate driver aggregated scores
def calculate_driver_scores(main_df):
    """
    Calculate aggregated driver scores based on device_id
    This groups trips by device_id and calculates average scores
    """
    try:
        # Only include rows with valid scores and device_id
        valid_scores = main_df[
            (main_df['safe_score'].notna()) & 
            (main_df['device_id'].notna()) & 
            (main_df['device_id'] != '')
        ].copy()
        
        if valid_scores.empty:
            print("⚠️  No valid scores with device_id found for driver aggregation")
            return pd.DataFrame()
        
        # Group by device_id and calculate aggregated metrics
        driver_scores = valid_scores.groupby('device_id').agg({
            'safe_score': ['mean', 'count', 'std'],
            'risk_factor': 'mean',
            'total_penalty': 'mean',
            'star_rating': ['mean', lambda x: x.value_counts().to_dict()],
            'timestamp': 'max'  # Latest trip date
        }).reset_index()
        
        # Flatten column names
        driver_scores.columns = [
            'device_id', 'avg_safe_score', 'trip_count', 'score_std',
            'avg_risk_factor', 'avg_total_penalty', 'avg_star_rating', 
            'star_distribution', 'latest_trip_date'
        ]
        
        # Round the scores
        driver_scores['avg_safe_score'] = driver_scores['avg_safe_score'].round(2)
        driver_scores['avg_risk_factor'] = driver_scores['avg_risk_factor'].round(4)
        driver_scores['avg_total_penalty'] = driver_scores['avg_total_penalty'].round(4)
        driver_scores['avg_star_rating'] = driver_scores['avg_star_rating'].round(1)
        driver_scores['score_std'] = driver_scores['score_std'].round(2)
        
        print(f"✅ Calculated driver scores for {len(driver_scores)} drivers")
        return driver_scores
        
    except Exception as e:
        print(f"❌ Error calculating driver scores: {str(e)}")
        return pd.DataFrame()

# The main pipeline
def run_score_pipeline(db_path, config):
    conn = sqlite3.connect(db_path)

    # Read main data
    main_df = pd.read_sql_query("SELECT * FROM SampleTable", conn)
    
    # Check if required tables exist
    try:
        start_df = pd.read_sql_query("SELECT * FROM EventsStartPointTable", conn)
        stop_df = pd.read_sql_query("SELECT * FROM EventsStopPointTable", conn)
        use_distance_tables = True
    except Exception as e:
        print(f"⚠️  Warning: Could not load distance tables: {str(e)}")
        print("    Using default distance values")
        use_distance_tables = False
    
    main_df['timestamp'] = pd.to_datetime(main_df['timestamp'])

    # Calculate trip distances if tables are available
    if use_distance_tables:
        try:
            trip_distances_df = calculate_trip_distances(start_df, stop_df)
            trip_distance_dict = dict(zip(trip_distances_df['UNIQUE_ID'], trip_distances_df['distance_km']))
        except Exception as e:
            print(f"⚠️  Warning: Could not calculate trip distances: {str(e)}")
            trip_distance_dict = {}
    else:
        trip_distance_dict = {}

    weights = config['weights']
    trip_scores = []

    print(f"📊 Processing {len(main_df['unique_id'].unique())} unique trips...")
    
    for uid in main_df['unique_id'].unique():
        trip_distance = trip_distance_dict.get(uid, 50.0)  # Default 50km if not found
        trip_df = main_df[main_df['unique_id'] == uid].copy()

        # Apply data cleaning
        trip_df = trip_df[(trip_df['speed_kmh'] >= 1.0) & (trip_df['speed_kmh'] <= 160.0)]

        if len(trip_df) < 10 or trip_distance <= 1.0:
            continue

        # Get device_id for this trip (take the first non-null value)
        device_id = None
        if 'device_id' in trip_df.columns:
            device_id = trip_df['device_id'].dropna().iloc[0] if not trip_df['device_id'].dropna().empty else None

        # Acceleration
        acc = DamoovAccelerationScorer(**config['acceleration'])
        acc.df = trip_df
        acc.detect_events()
        acc.calculate_penalties()
        acc_score = acc.get_events()['penalty_acc'].sum() if not acc.get_events().empty else 0

        # Deceleration
        dec = DamoovDeccelerationScorer(**config['deceleration'])
        dec.df = trip_df
        dec.detect_events()
        dec.calculate_penalties()
        dec_score = dec.get_events()['penalty_braking'].sum() if not dec.get_events().empty else 0

        # Cornering
        cor = DamoovCorneringScorer(**config['cornering'])
        cor.df = trip_df
        cor.detect_events()
        cor.calculate_penalties()
        cor_score = cor.get_events()['penalty_cornering'].sum() if not cor.get_events().empty else 0

        # Speeding
        spd = SpeedingDetectorFixedLimit(**config['speeding'])
        spd.df = trip_df
        spd.detect_speeding()
        spd.assign_penalties()
        spd_score = spd.get_events()['penalty_speeding'].sum() if not spd.get_events().empty else 0

        # Phone Usage
        phone = PhoneUsageDetector(**config['phone_usage'])
        phone.df = trip_df
        phone.detect_phone_usage()
        phone.assign_penalties()
        phone_score = phone.get_events()['penalty_phone'].sum() if not phone.get_events().empty else 0

        total_penalty = (
            weights["acceleration_weight"] * acc_score +
            weights["braking_weight"] * dec_score +
            weights["cornering_weight"] * cor_score +
            weights["speeding_weight"] * spd_score +
            weights["phone_usage_weight"] * phone_score
        )

        # Normalize penalty by trip distance
        penalty_per_km = total_penalty / trip_distance
        trip_scores.append({
            'unique_id': uid,
            'device_id': device_id,
            'penalty_per_km': penalty_per_km,
            'trip_distance': trip_distance,
            'total_penalty_raw': total_penalty
        })

    # Create dataframe for normalization step
    score_df = pd.DataFrame(trip_scores)
    
    if score_df.empty:
        print("⚠️  No valid trips found for scoring")
        conn.close()
        return

    # Apply Min-Max Normalization AFTER aggregation
    min_penalty = score_df['penalty_per_km'].min()
    max_penalty = score_df['penalty_per_km'].max()

    if max_penalty == min_penalty:
        score_df['safe_score'] = 100.0
    else:
        score_df['safe_score'] = 100 * (1 - (score_df['penalty_per_km'] - min_penalty) / (max_penalty - min_penalty))
        score_df['safe_score'] = score_df['safe_score'].round(2)

    score_df['risk_factor'] = score_df['penalty_per_km'].round(4)
    score_df['total_penalty'] = score_df['penalty_per_km'].round(4) * 1  # keep same for compatibility

    # Star Rating logic
    score_df['star_rating'] = score_df['safe_score'].apply(
        lambda s: 5 if s >= 95 else 4 if s >= 85 else 3 if s >= 75 else 2 if s >= 65 else 1
    )

    print(f"📈 Calculated scores for {len(score_df)} trips")
    print(score_df[['unique_id', 'device_id', 'safe_score', 'star_rating']].head())

    # Drop old scoring columns from main_df
    columns_to_drop = ['safe_score', 'risk_factor', 'total_penalty', 'star_rating']
    main_df = main_df.drop(columns=[col for col in columns_to_drop if col in main_df.columns], errors='ignore')

    # Merge scores back to main dataframe
    updated_df = pd.merge(main_df, score_df[['unique_id', 'safe_score', 'risk_factor', 'total_penalty', 'star_rating']], 
                         on='unique_id', how='left')
    
    # Update the main table
    updated_df.to_sql("SampleTable", conn, if_exists="replace", index=False)
    
    # Calculate and store driver aggregated scores
    driver_scores = calculate_driver_scores(updated_df)
    
    if not driver_scores.empty:
        try:
            # Create or update driver scores table
            driver_scores.to_sql("DriverScoresTable", conn, if_exists="replace", index=False)
            print(f"✅ Created/Updated DriverScoresTable with {len(driver_scores)} driver records")
        except Exception as e:
            print(f"⚠️  Warning: Could not create DriverScoresTable: {str(e)}")
    
    conn.close()
    print("✅ SQLite SampleTable updated with normalized scores.")
    print("✅ Driver aggregated scores calculated and stored.")


# Additional utility function for manual driver score calculation
def calculate_driver_score_for_device(db_path, device_id):
    """
    Calculate aggregated score for a specific device ID
    This can be used for real-time driver score queries
    """
    conn = sqlite3.connect(db_path)
    
    try:
        query = """
        SELECT unique_id, device_id, safe_score, risk_factor, star_rating, timestamp, total_penalty
        FROM SampleTable 
        WHERE device_id = ? AND safe_score IS NOT NULL
        """
        
        df = pd.read_sql_query(query, conn, params=(device_id,))
        
        if df.empty:
            return None
        
        # Calculate aggregated metrics
        driver_score = {
            'device_id': device_id,
            'average_safe_score': round(df['safe_score'].mean(), 2),
            'average_risk_factor': round(df['risk_factor'].mean(), 4),
            'average_star_rating': round(df['star_rating'].mean(), 1),
            'total_trips': len(df),
            'score_std': round(df['safe_score'].std(), 2) if len(df) > 1 else 0.0,
            'star_distribution': df['star_rating'].value_counts().to_dict(),
            'latest_trip_date': df['timestamp'].max() if 'timestamp' in df.columns else None,
            'best_score': df['safe_score'].max(),
            'worst_score': df['safe_score'].min()
        }
        
        return driver_score
        
    except Exception as e:
        print(f"❌ Error calculating driver score for device {device_id}: {str(e)}")
        return None
    finally:
        conn.close()


# Function to get driver rankings
def get_driver_rankings(db_path, limit=10):
    """
    Get top drivers based on average safe score
    """
    conn = sqlite3.connect(db_path)
    
    try:
        query = """
        SELECT 
            device_id,
            COUNT(*) as total_trips,
            ROUND(AVG(safe_score), 2) as avg_safe_score,
            ROUND(AVG(risk_factor), 4) as avg_risk_factor,
            ROUND(AVG(star_rating), 1) as avg_star_rating,
            MAX(timestamp) as latest_trip_date,
            MAX(safe_score) as best_score,
            MIN(safe_score) as worst_score
        FROM SampleTable 
        WHERE device_id IS NOT NULL AND safe_score IS NOT NULL
        GROUP BY device_id
        HAVING COUNT(*) >= 5  -- Only drivers with at least 5 trips
        ORDER BY avg_safe_score DESC, total_trips DESC
        LIMIT ?
        """
        
        rankings = pd.read_sql_query(query, conn, params=(limit,))
        return rankings.to_dict('records')
        
    except Exception as e:
        print(f"❌ Error getting driver rankings: {str(e)}")
        return []
    finally:
        conn.close()


# Function to update driver scores incrementally
def update_driver_scores_incremental(db_path, device_ids=None):
    """
    Update driver scores for specific device IDs or all devices
    This is more efficient than recalculating everything
    """
    conn = sqlite3.connect(db_path)
    
    try:
        if device_ids is None:
            # Get all device IDs
            device_query = "SELECT DISTINCT device_id FROM SampleTable WHERE device_id IS NOT NULL"
            device_df = pd.read_sql_query(device_query, conn)
            device_ids = device_df['device_id'].tolist()
        
        if not isinstance(device_ids, list):
            device_ids = [device_ids]
        
        driver_scores = []
        
        for device_id in device_ids:
            driver_score = calculate_driver_score_for_device(db_path, device_id)
            if driver_score:
                driver_scores.append(driver_score)
        
        if driver_scores:
            # Convert to DataFrame and save
            driver_scores_df = pd.DataFrame(driver_scores)
            
            # Handle the star_distribution column (convert dict to string for SQLite)
            if 'star_distribution' in driver_scores_df.columns:
                driver_scores_df['star_distribution'] = driver_scores_df['star_distribution'].astype(str)
            
            driver_scores_df.to_sql("DriverScoresTable", conn, if_exists="replace", index=False)
            print(f"✅ Updated driver scores for {len(driver_scores)} drivers")
            
        return driver_scores
        
    except Exception as e:
        print(f"❌ Error updating driver scores: {str(e)}")
        return []
    finally:
        conn.close()