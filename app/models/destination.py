from typing import List, Literal

from pydantic import BaseModel, Field


class Destination(BaseModel):
    """Represents an Indian travel destination and its key attributes."""

    id: int = Field(..., description="Unique identifier for the destination")
    name: str
    country: str = Field("India", description="Country (restricted to India)")
    state: str = Field(..., description="Indian state or union territory")
    region: Literal["North", "South", "East", "West", "Northeast"]
    tags: List[str] = Field(
        default_factory=list,
        description="Descriptors like hill-station, beach, wildlife, spiritual, food",
    )
    budget_level: Literal["budget", "mid", "premium"] = Field(
        ..., description="Budget tiers in INR per day"
    )
    avg_daily_cost_inr: int = Field(
        ..., description="Typical average daily cost in INR"
    )
    climate: Literal["cold", "moderate", "warm"]
    crowd_level: Literal["low", "medium", "high"]
    best_season: str = Field(
        ..., description="Human-readable best season, e.g. 'Oct–Mar'"
    )
    travel_type: List[Literal["train", "road", "flight"]] = Field(
        default_factory=list,
        description="Common ways to reach (train, road, flight)",
    )
    latitude: float
    longitude: float


