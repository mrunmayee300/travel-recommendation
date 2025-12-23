from typing import List

from fastapi import APIRouter, HTTPException

from app.ml.recommender import recommend_destinations
from app.models import Destination, PreferenceRequest
from app.utils.data_loader import load_sample_data

router = APIRouter(tags=["recommendations"])


@router.post("/recommend-destinations", response_model=List[Destination])
def recommend_destinations_route(preferences: PreferenceRequest) -> List[Destination]:
    destinations, _ = load_sample_data()
    if not destinations:
        raise HTTPException(status_code=500, detail="No destination data available")

    ranked = recommend_destinations(destinations, preferences)
    return ranked


