from typing import List, Sequence

from app.models import (
    Destination,
    NearbyExpansionRequest,
    NearbyExpansionResponse,
    NearbySuggestion,
)
from app.utils.haversine import haversine_km


def suggest_nearby_destinations(
    destinations: Sequence[Destination],
    request: NearbyExpansionRequest,
) -> NearbyExpansionResponse:
    origin = _find_destination(destinations, request.destination_id)
    origin_point = (origin.latitude, origin.longitude)
    suggestions: List[NearbySuggestion] = []

    for dest in destinations:
        if dest.id == origin.id:
            continue
        distance = haversine_km(origin_point, (dest.latitude, dest.longitude))
        if distance > request.radius_km:
            continue

        # Simple feasibility heuristic:
        # - If extra_days >= 1 and extra_budget >= 200, mark as feasible
        feasible = request.extra_days >= 1 and request.extra_budget >= 200
        note_parts = [f"{distance:.1f} km away"]
        if not feasible:
            note_parts.append("might need more days/budget")
        else:
            note_parts.append("doable with provided buffer")

        suggestions.append(
            NearbySuggestion(
                destination_id=dest.id,
                name=dest.name,
                country=dest.country,
                distance_km=round(distance, 1),
                feasible=feasible,
                notes="; ".join(note_parts),
            )
        )

    suggestions.sort(key=lambda s: s.distance_km)
    return NearbyExpansionResponse(
        origin_destination_id=origin.id, suggestions=suggestions
    )


def _find_destination(destinations: Sequence[Destination], dest_id: int) -> Destination:
    for d in destinations:
        if d.id == dest_id:
            return d
    raise ValueError(f"Destination id {dest_id} not found")


