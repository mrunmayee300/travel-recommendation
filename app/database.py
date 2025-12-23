"""Database schema and connection management for SQLite."""
import sqlite3
from pathlib import Path
from typing import Optional

DB_PATH = Path(__file__).resolve().parent.parent / "travel_india.db"


def get_db_connection() -> sqlite3.Connection:
    """Get a connection to the SQLite database."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row  # Enable dict-like row access
    return conn


def init_database():
    """Create database tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Destinations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS destinations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            state TEXT NOT NULL,
            region TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            tags TEXT NOT NULL,  -- JSON array as string
            budget_level TEXT NOT NULL,  -- budget, mid, premium
            avg_daily_cost_inr INTEGER NOT NULL,
            climate TEXT NOT NULL,  -- cold, moderate, warm
            crowd_level TEXT NOT NULL,  -- low, medium, high
            best_season TEXT,
            travel_type TEXT,  -- JSON array as string
            category TEXT,  -- Heritage, Beach, Nature, etc.
            popular_attraction TEXT,
            accessibility TEXT,
            nearest_airport TEXT,
            nearest_railway TEXT,
            UNIQUE(name, state)
        )
    """)

    # Attractions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attractions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            destination_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            cost_inr REAL NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            visit_duration_hours REAL NOT NULL,
            type TEXT,
            significance TEXT,
            rating REAL,
            best_time_to_visit TEXT,
            FOREIGN KEY (destination_id) REFERENCES destinations(id) ON DELETE CASCADE
        )
    """)

    # Create indexes for faster queries
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_destinations_region ON destinations(region)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_destinations_state ON destinations(state)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_attractions_destination ON attractions(destination_id)")

    conn.commit()
    conn.close()


def clear_database():
    """Clear all data from tables (useful for re-imports)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM attractions")
    cursor.execute("DELETE FROM destinations")
    conn.commit()
    conn.close()

