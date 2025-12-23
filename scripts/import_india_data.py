"""Import script to load Indian travel datasets into SQLite database."""
import json
import re
import sqlite3
from pathlib import Path

import pandas as pd

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "app" / "data"
DB_PATH = PROJECT_ROOT / "travel_india.db"

# CSV files
CITIES_CSV = DATA_DIR / "in.csv"
DESTINATIONS_CSV = DATA_DIR / "Expanded_Indian_Travel_Dataset.csv"
ATTRACTIONS_CSV = DATA_DIR / "Top Indian Places to Visit.csv"


def normalize_city_name(name: str) -> str:
    """Normalize city names for matching (remove diacritics, lowercase)."""
    # Remove common suffixes
    name = re.sub(r"\s+(City|Town|Village)$", "", name, flags=re.IGNORECASE)
    # Basic normalization
    return name.strip().lower()


def infer_budget_level(avg_cost: int) -> str:
    """Infer budget level from average daily cost in INR."""
    if avg_cost < 5000:
        return "budget"
    elif avg_cost < 15000:
        return "mid"
    else:
        return "premium"


def infer_climate_from_region(region: str) -> str:
    """Infer climate from region."""
    region_lower = region.lower()
    if "north" in region_lower and "east" not in region_lower:
        return "cold"  # Northern hill stations
    elif "south" in region_lower:
        return "warm"
    elif "east" in region_lower:
        return "moderate"
    elif "west" in region_lower:
        return "warm"
    else:
        return "moderate"


def infer_crowd_level(accessibility: str) -> str:
    """Infer crowd level from accessibility."""
    if not accessibility:
        return "medium"
    acc_lower = accessibility.lower()
    if "easy" in acc_lower:
        return "high"
    elif "difficult" in acc_lower:
        return "low"
    else:
        return "medium"


def category_to_tags(category: str, region: str) -> list[str]:
    """Convert category to tags list."""
    tags = []
    cat_lower = category.lower() if category else ""
    
    # Map categories to our tag system
    if "heritage" in cat_lower or "fort" in cat_lower:
        tags.append("Heritage & Forts")
    if "beach" in cat_lower:
        tags.append("Beach")
    if "nature" in cat_lower or "national park" in cat_lower:
        tags.append("Nature")
        tags.append("Wildlife")
    if "religious" in cat_lower or "spiritual" in cat_lower:
        tags.append("Spiritual")
    if "adventure" in cat_lower:
        tags.append("Adventure")
    if "hill" in cat_lower or any(x in region.lower() for x in ["himachal", "uttarakhand", "sikkim"]):
        tags.append("Hill station")
    
    # Add region-based tags
    if "north" in region.lower() and "east" not in region.lower():
        if "himachal" in region.lower() or "uttarakhand" in region.lower():
            tags.append("Hill station")
    
    return tags if tags else ["Nature"]


def import_destinations(conn: sqlite3.Connection):
    """Import destinations from Expanded_Indian_Travel_Dataset.csv."""
    print("📦 Loading destinations CSV...")
    df_dest = pd.read_csv(DESTINATIONS_CSV)
    
    print("📦 Loading cities CSV for coordinates...")
    df_cities = pd.read_csv(CITIES_CSV)
    
    # Create a lookup map: normalized city name -> (lat, lng)
    city_coords = {}
    for _, row in df_cities.iterrows():
        city_name = normalize_city_name(str(row.get("city", "")))
        lat = row.get("lat")
        lng = row.get("lng")
        if pd.notna(lat) and pd.notna(lng):
            city_coords[city_name] = (float(lat), float(lng))
    
    cursor = conn.cursor()
    imported = 0
    skipped = 0
    
    for _, row in df_dest.iterrows():
        dest_name = str(row.get("Destination Name", "")).strip()
        state = str(row.get("State", "")).strip()
        region = str(row.get("Region", "")).strip()
        category = str(row.get("Category", "")).strip()
        
        if not dest_name or not state:
            skipped += 1
            continue
        
        # Try to find coordinates
        lat, lng = None, None
        normalized_dest = normalize_city_name(dest_name)
        
        # Try exact match first
        if normalized_dest in city_coords:
            lat, lng = city_coords[normalized_dest]
        else:
            # Try matching by state + partial name
            for city_name, coords in city_coords.items():
                if normalized_dest in city_name or city_name in normalized_dest:
                    lat, lng = coords
                    break
        
        # Fallback: use state capital or approximate coordinates
        if lat is None or lng is None:
            # Approximate coordinates by state (very rough)
            state_coords = {
                "himachal pradesh": (31.1048, 77.1734),  # Shimla
                "rajasthan": (26.9124, 75.7873),  # Jaipur
                "goa": (15.2993, 74.1240),
                "kerala": (10.1632, 76.6413),  # Kochi
                "uttar pradesh": (26.8467, 80.9462),  # Lucknow
                "west bengal": (22.5726, 88.3639),  # Kolkata
                "punjab": (31.6340, 74.8723),  # Amritsar
                "tamil nadu": (13.0827, 80.2707),  # Chennai
                "assam": (26.1445, 91.7362),  # Guwahati
                "karnataka": (12.9716, 77.5946),  # Bangalore
                "uttarakhand": (30.3165, 78.0322),  # Dehradun
                "maharashtra": (19.0760, 72.8777),  # Mumbai
                "meghalaya": (25.5788, 91.8933),  # Shillong
                "andaman and nicobar": (11.6234, 92.7265),  # Port Blair
            }
            state_lower = state.lower()
            if state_lower in state_coords:
                lat, lng = state_coords[state_lower]
            else:
                lat, lng = 20.5937, 78.9629  # India center fallback
        
        # Build tags from category
        tags = category_to_tags(category, region)
        tags_json = json.dumps(tags)
        
        # Infer attributes
        budget_level = "mid"  # Default
        avg_daily_cost_inr = 10000  # Default mid-range
        climate = infer_climate_from_region(region)
        accessibility = str(row.get("Accessibility", "")).strip()
        crowd_level = infer_crowd_level(accessibility)
        
        # Adjust budget based on category/accessibility
        if "difficult" in accessibility.lower():
            budget_level = "premium"
            avg_daily_cost_inr = 20000
        elif "easy" in accessibility.lower() and "heritage" in category.lower():
            budget_level = "mid"
            avg_daily_cost_inr = 12000
        
        best_season = "Oct–Mar"  # Default for most Indian destinations
        travel_type = ["road", "train"]  # Default
        if row.get("Nearest Airport"):
            travel_type.append("flight")
        travel_type_json = json.dumps(travel_type)
        
        popular_attraction = str(row.get("Popular Attraction", "")).strip() or None
        nearest_airport = str(row.get("Nearest Airport", "")).strip() or None
        nearest_railway = str(row.get("Nearest Railway Station", "")).strip() or None
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO destinations (
                    name, state, region, latitude, longitude, tags, budget_level,
                    avg_daily_cost_inr, climate, crowd_level, best_season,
                    travel_type, category, popular_attraction, accessibility,
                    nearest_airport, nearest_railway
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                dest_name, state, region, lat, lng, tags_json, budget_level,
                avg_daily_cost_inr, climate, crowd_level, best_season,
                travel_type_json, category, popular_attraction, accessibility,
                nearest_airport, nearest_railway
            ))
            imported += 1
        except Exception as e:
            print(f"⚠️  Error importing {dest_name}: {e}")
            skipped += 1
    
    conn.commit()
    print(f"✅ Imported {imported} destinations, skipped {skipped}")
    return imported


def import_attractions(conn: sqlite3.Connection):
    """Import attractions from Top Indian Places to Visit.csv."""
    print("📦 Loading attractions CSV...")
    df_attr = pd.read_csv(ATTRACTIONS_CSV)
    
    # Load destinations to match by city name
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, state FROM destinations")
    dest_rows = cursor.fetchall()
    
    # Create lookup: (city_normalized, state_normalized) -> destination_id
    dest_lookup = {}
    for dest_row in dest_rows:
        dest_id, dest_name, dest_state = dest_row
        dest_name_norm = normalize_city_name(dest_name)
        dest_state_norm = normalize_city_name(dest_state)
        dest_lookup[(dest_name_norm, dest_state_norm)] = dest_id
    
    imported = 0
    skipped = 0
    
    for _, row in df_attr.iterrows():
        city = str(row.get("City", "")).strip()
        state = str(row.get("State", "")).strip()
        attr_name = str(row.get("Name", "")).strip()
        
        if not city or not attr_name:
            skipped += 1
            continue
        
        # Try to match destination
        city_norm = normalize_city_name(city)
        state_norm = normalize_city_name(state) if state else ""
        
        destination_id = None
        
        # Try exact match
        if (city_norm, state_norm) in dest_lookup:
            destination_id = dest_lookup[(city_norm, state_norm)]
        else:
            # Try city name match only
            for (dest_city, dest_state), dest_id in dest_lookup.items():
                if city_norm == dest_city or city_norm in dest_city or dest_city in city_norm:
                    destination_id = dest_id
                    break
        
        if not destination_id:
            skipped += 1
            continue
        
        # Extract fields
        category = str(row.get("Type", "")).strip() or "Nature"
        cost_inr = float(row.get("Entrance Fee in INR", 0) or 0)
        duration_hours = float(row.get("time needed to visit in hrs", 2.0) or 2.0)
        
        # Try to get coordinates (if available in cities CSV)
        lat, lng = None, None
        df_cities = pd.read_csv(CITIES_CSV)
        for _, city_row in df_cities.iterrows():
            if normalize_city_name(str(city_row.get("city", ""))) == city_norm:
                lat = float(city_row.get("lat", 0))
                lng = float(city_row.get("lng", 0))
                break
        
        # Fallback: use destination coordinates
        if lat is None or lng is None:
            cursor.execute("SELECT latitude, longitude FROM destinations WHERE id = ?", (destination_id,))
            dest_coords = cursor.fetchone()
            if dest_coords:
                lat, lng = dest_coords
        
        if lat is None or lng is None:
            lat, lng = 20.5937, 78.9629  # India center fallback
        
        significance = str(row.get("Significance", "")).strip() or None
        rating = float(row.get("Google review rating", 0) or 0) if pd.notna(row.get("Google review rating")) else None
        best_time = str(row.get("Best Time to visit", "")).strip() or None
        
        try:
            cursor.execute("""
                INSERT INTO attractions (
                    destination_id, name, category, cost_inr, latitude, longitude,
                    visit_duration_hours, type, significance, rating, best_time_to_visit
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                destination_id, attr_name, category, cost_inr, lat, lng,
                duration_hours, category, significance, rating, best_time
            ))
            imported += 1
        except Exception as e:
            print(f"⚠️  Error importing attraction {attr_name}: {e}")
            skipped += 1
    
    conn.commit()
    print(f"✅ Imported {imported} attractions, skipped {skipped}")
    return imported


def main():
    """Main import function."""
    import sys
    sys.path.insert(0, str(PROJECT_ROOT))
    
    print("🚀 Starting India travel data import...")
    
    # Initialize database
    from app.database import init_database, clear_database
    
    init_database()
    print("✅ Database initialized")
    
    # Clear existing data
    clear_database()
    print("✅ Cleared existing data")
    
    # Connect to database
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    
    try:
        # Import destinations
        dest_count = import_destinations(conn)
        
        # Import attractions
        attr_count = import_attractions(conn)
        
        print(f"\n🎉 Import complete!")
        print(f"   Destinations: {dest_count}")
        print(f"   Attractions: {attr_count}")
        
    finally:
        conn.close()


if __name__ == "__main__":
    main()

