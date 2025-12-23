from typing import Dict, List, Sequence, Tuple

from app.models import (
    Attraction,
    Destination,
    ItineraryActivity,
    ItineraryDay,
    ItineraryRequest,
    ItineraryResponse,
)
from app.utils.haversine import haversine_km


PACE_HOURS = {
    "relaxed": 6.0,
    "moderate": 8.0,
    "full": 10.0,
}


def generate_itinerary(
    destinations: Sequence[Destination],
    attractions: Sequence[Attraction],
    request: ItineraryRequest,
) -> ItineraryResponse:
    destination = _find_destination(destinations, request.destination_id)
    dest_center = (destination.latitude, destination.longitude)

    dest_attractions = [a for a in attractions if a.destination_id == destination.id]
    scored = _score_attractions(dest_attractions, request, dest_center)

    days = _distribute_into_days(scored, request, dest_center)
    return ItineraryResponse(
        destination_id=destination.id,
        destination_name=destination.name,
        days=days,
    )


def _find_destination(destinations: Sequence[Destination], dest_id: int) -> Destination:
    for d in destinations:
        if d.id == dest_id:
            return d
    raise ValueError(f"Destination id {dest_id} not found")


def _score_attractions(
    attractions: Sequence[Attraction],
    request: ItineraryRequest,
    dest_center: Tuple[float, float],
) -> List[Tuple[Attraction, float]]:
    per_day_budget = (request.budget / request.days) if request.days else 0
    interests_lower = {i.lower() for i in request.interests}

    scored: List[Tuple[Attraction, float]] = []
    for a in attractions:
        interest_score = 1.0 if a.category.lower() in interests_lower else 0.4
        cost_fit = (
            max(0.0, 1.0 - (a.cost / per_day_budget)) if per_day_budget > 0 else 0.8
        )
        distance = haversine_km(dest_center, (a.latitude, a.longitude))
        distance_efficiency = max(0.0, 1.0 - min(distance / 50, 1))  # prefer nearby

        score = (0.5 * interest_score) + (0.2 * cost_fit) + (0.2 * distance_efficiency) + 0.1
        scored.append((a, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored


def _distribute_into_days(
    scored: List[Tuple[Attraction, float]],
    request: ItineraryRequest,
    dest_center: Tuple[float, float],
) -> List[ItineraryDay]:
    max_hours = PACE_HOURS.get(request.pace, PACE_HOURS["moderate"])
    remaining = scored.copy()
    days: List[ItineraryDay] = []

    # Calculate target hours per day for more even distribution
    total_hours = sum(attr.visit_duration for attr, _ in scored)
    target_hours_per_day = total_hours / request.days if request.days > 0 else max_hours

    for day_num in range(1, request.days + 1):
        day_hours = 0.0
        activities: List[ItineraryActivity] = []
        last_point = dest_center

        # Try to fill up to target hours, but allow some flexibility
        # For the last day, use max_hours to fill remaining attractions
        if day_num == request.days:
            target_for_day = max_hours
        else:
            target_for_day = min(target_hours_per_day * 1.3, max_hours)  # Allow 30% over target

        # Greedy fill activities for the day by score and remaining time
        idx = 0
        while idx < len(remaining):
            attraction, _score = remaining[idx]
            
            # Check if adding this attraction would exceed max hours
            if day_hours + attraction.visit_duration > max_hours:
                idx += 1
                continue
            
            # If we've reached target for this day and there are more days to fill,
            # move to next day to distribute more evenly
            if day_hours >= target_for_day and day_num < request.days:
                break

            distance = haversine_km(last_point, (attraction.latitude, attraction.longitude))
            activities.append(
                ItineraryActivity(
                    attraction_id=attraction.id,
                    name=attraction.name,
                    category=attraction.category,
                    estimated_time_hours=attraction.visit_duration,
                    estimated_cost=attraction.cost,
                    latitude=attraction.latitude,
                    longitude=attraction.longitude,
                    distance_from_prev_km=distance,
                )
            )
            day_hours += attraction.visit_duration
            last_point = (attraction.latitude, attraction.longitude)
            remaining.pop(idx)
            # Don't increment idx since we popped the element
        
        day_cost = sum(a.estimated_cost for a in activities)
        days.append(
            ItineraryDay(day=day_num, activities=activities, estimated_day_cost=day_cost)
        )
        
        # Always continue to create all requested days, even if we run out of attractions

    return days


