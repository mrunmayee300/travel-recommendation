from fastapi import APIRouter, HTTPException

from app.models import NearbyExpansionRequest, NearbyExpansionResponse
from app.services.nearby import suggest_nearby_destinations
from app.utils.data_loader import load_sample_data

router = APIRouter(tags=["nearby"])


@router.post("/nearby-expansions", response_model=NearbyExpansionResponse)
def nearby_expansions_route(payload: NearbyExpansionRequest) -> NearbyExpansionResponse:
    destinations, _ = load_sample_data()
    try:
        return suggest_nearby_destinations(destinations, payload)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


