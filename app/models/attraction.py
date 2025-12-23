from pydantic import BaseModel, Field


class Attraction(BaseModel):
    """Represents a point of interest within a destination."""

    id: int = Field(..., description="Unique identifier for the attraction")
    destination_id: int
    name: str
    category: str
    cost: float = Field(..., description="Estimated cost in INR")
    latitude: float
    longitude: float
    visit_duration: float = Field(..., description="Recommended visit duration in hours")


