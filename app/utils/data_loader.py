import json
from functools import lru_cache
from pathlib import Path
from typing import List, Tuple

from app.database import get_db_connection
from app.models import Attraction, Destination


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "sample_data.json"


def load_sample_data(path: Path = DATA_PATH) -> Tuple[List[Destination], List[Attraction]]:
    """
    Load destinations and attractions from SQLite database.
    
    Falls back to JSON if database is empty (for backward compatibility).
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if database has data
        cursor.execute("SELECT COUNT(*) FROM destinations")
        dest_count = cursor.fetchone()[0]
        
        if dest_count == 0:
            # Fallback to JSON if database is empty
            if path.exists():
                with path.open("r", encoding="utf-8") as f:
                    payload = json.load(f)
                destinations = [Destination(**item) for item in payload.get("destinations", [])]
                attractions = [Attraction(**item) for item in payload.get("attractions", [])]
                return destinations, attractions
            else:
                return [], []
        
        # Load destinations from database
        cursor.execute("""
            SELECT id, name, state, region, latitude, longitude, tags,
                   budget_level, avg_daily_cost_inr, climate, crowd_level,
                   best_season, travel_type
            FROM destinations
        """)
        dest_rows = cursor.fetchall()
        
        destinations = []
        for row in dest_rows:
            tags = json.loads(row["tags"]) if row["tags"] else []
            travel_type = json.loads(row["travel_type"]) if row["travel_type"] else []
            
            destinations.append(Destination(
                id=row["id"],
                name=row["name"],
                country="India",
                state=row["state"],
                region=row["region"],
                latitude=row["latitude"],
                longitude=row["longitude"],
                tags=tags,
                budget_level=row["budget_level"],
                avg_daily_cost_inr=row["avg_daily_cost_inr"],
                climate=row["climate"],
                crowd_level=row["crowd_level"],
                best_season=row["best_season"],
                travel_type=travel_type,
            ))
        
        # Load attractions from database
        cursor.execute("""
            SELECT id, destination_id, name, category, cost_inr as cost,
                   latitude, longitude, visit_duration_hours as visit_duration
            FROM attractions
        """)
        attr_rows = cursor.fetchall()
        
        attractions = []
        for row in attr_rows:
            attractions.append(Attraction(
                id=row["id"],
                destination_id=row["destination_id"],
                name=row["name"],
                category=row["category"],
                cost=row["cost"],
                latitude=row["latitude"],
                longitude=row["longitude"],
                visit_duration=row["visit_duration"],
            ))
        
        return destinations, attractions
        
    finally:
        conn.close()


