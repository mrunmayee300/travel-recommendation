from typing import List

from pydantic import BaseModel, Field, confloat, conint


class NearbyExpansionRequest(BaseModel):
    destination_id: int
    extra_days: conint(ge=0) = Field(
        default=0, description="Number of additional days the traveler can extend"
    )
    extra_budget: confloat(ge=0) = Field(
        default=0, description="Additional budget in USD for nearby expansions"
    )
    radius_km: confloat(gt=0) = Field(
        default=350.0, description="Search radius for nearby destinations in kilometers"
    )


class NearbySuggestion(BaseModel):
    destination_id: int
    name: str
    country: str
    distance_km: float
    feasible: bool = Field(
        ..., description="Whether extra days/budget appear sufficient to visit"
    )
    notes: str


class NearbyExpansionResponse(BaseModel):
    origin_destination_id: int
    suggestions: List[NearbySuggestion]


