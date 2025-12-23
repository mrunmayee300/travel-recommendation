from fastapi import APIRouter, HTTPException

from app.models import ItineraryRequest, ItineraryResponse
from app.services.itinerary import generate_itinerary
from app.utils.data_loader import load_sample_data

router = APIRouter(tags=["itinerary"])


@router.post("/generate-itinerary", response_model=ItineraryResponse)
def generate_itinerary_route(payload: ItineraryRequest) -> ItineraryResponse:
    destinations, attractions = load_sample_data()
    try:
        return generate_itinerary(destinations, attractions, payload)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


