from typing import List, Optional

from pydantic import BaseModel, Field, conint


class PreferenceRequest(BaseModel):
    """User travel preferences used for destination ranking (India-specific)."""

    tags: List[str] = Field(
        default_factory=list,
        description=(
            "Interests such as Spiritual, Wildlife, Monsoon-friendly, "
            "Hill station, Beach, Heritage & Forts, Food & Street food"
        ),
    )
    budget_level: Optional[str] = Field(
        default=None,
        description="budget | mid | premium preference (per-day INR tiers)",
    )
    climate: Optional[str] = Field(
        default=None, description="cold | moderate | warm preference"
    )
    crowd_level: Optional[str] = Field(
        default=None, description="low | medium | high preference"
    )
    top_k: conint(ge=1, le=20) = Field(
        default=5, description="Number of destinations to return"
    )


