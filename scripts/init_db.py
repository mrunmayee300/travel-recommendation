"""Initialize database on first startup."""
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.database import init_database
from scripts.import_india_data import main as import_data


if __name__ == "__main__":
    print("🚀 Initializing database...")
    init_database()
    print("✅ Database initialized")
    
    print("🚀 Importing India travel data...")
    import_data()
    print("✅ Data import complete")

