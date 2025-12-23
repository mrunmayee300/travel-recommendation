# Travel Recommendation Web App (Backend API)

FastAPI backend for travel recommendations, itineraries, and nearby expansions. Aligned with the “Explorer’s Journal” experience.

## Stack
- FastAPI + Uvicorn
- scikit-learn (content-based similarity)
- Pydantic models
- Sample data via JSON (swap to DB later)

## Setup
```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Endpoints
- `GET /api/health` — health check
- `GET /api/meta` — app metadata
- `POST /api/recommend-destinations` — content-based destination ranking
- `POST /api/generate-itinerary` — itinerary generation (day-wise activities)
- `POST /api/nearby-expansions` — nearby destination suggestions

## Request Examples

### Recommend destinations
```json
{
  "tags": ["culture", "food"],
  "budget_level": "mid",
  "climate": "warm",
  "crowd_level": "medium",
  "top_k": 3
}
```

### Generate itinerary
```json
{
  "destination_id": 1,
  "days": 3,
  "budget": 600,
  "interests": ["culture", "food"],
  "pace": "moderate"
}
```

### Nearby expansions
```json
{
  "destination_id": 1,
  "extra_days": 2,
  "extra_budget": 500,
  "radius_km": 400
}
```

## Notes
- Sample data lives in `app/data/sample_data.json`.
- ML logic resides in `app/ml/recommender.py`; itinerary logic in `app/services/itinerary.py`; nearby suggestions in `app/services/nearby.py`.
- Future: replace JSON loader with DB models and persistence.


