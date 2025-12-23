from typing import List, Literal, Optional

from pydantic import BaseModel, Field, conint, confloat


class ItineraryActivity(BaseModel):
    attraction_id: int
    name: str
    category: str
    estimated_time_hours: float
    estimated_cost: float
    latitude: float = Field(..., description="Attraction latitude")
    longitude: float = Field(..., description="Attraction longitude")
    distance_from_prev_km: Optional[float] = Field(
        default=None, description="Travel distance from previous stop"
    )


class ItineraryDay(BaseModel):
    day: int
    activities: List[ItineraryActivity]
    estimated_day_cost: float


class ItineraryResponse(BaseModel):
    destination_id: int
    destination_name: str
    days: List[ItineraryDay]


class ItineraryRequest(BaseModel):
    destination_id: int
    days: conint(ge=1, le=30) = Field(..., description="Trip length in days")
    budget: confloat(ge=0) = Field(..., description="Total budget in INR")
    interests: List[str] = Field(default_factory=list, description="Preferred categories")
    pace: Literal["relaxed", "moderate", "full"] = Field(
        default="moderate", description="Controls daily hours and activity count"
    )


