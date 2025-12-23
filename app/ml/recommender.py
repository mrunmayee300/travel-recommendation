from functools import lru_cache
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from app.models import Destination, PreferenceRequest


# -----------------------------------------------------------------------------
# Feature encoding
# -----------------------------------------------------------------------------


def build_tag_vocab(destinations: Sequence[Destination]) -> Dict[str, int]:
    tags = set()
    for d in destinations:
        tags.update(t.lower() for t in d.tags)
    return {tag: idx for idx, tag in enumerate(sorted(tags))}


def encode_destination(
    destination: Destination,
    tag_index: Dict[str, int],
) -> np.ndarray:
    """Encode a destination into a numeric feature vector.

    Features include:
    - semantic tags (hill station, wildlife, spiritual, monsoon-friendly, etc.)
    - budget tier in INR (budget / mid / premium)
    - climate and crowd level
    - Indian region
    """
    tag_vec = np.zeros(len(tag_index), dtype=float)
    for tag in destination.tags:
        key = tag.lower()
        if key in tag_index:
            tag_vec[tag_index[key]] = 1.0

    budget_vec = one_hot(destination.budget_level, ["budget", "mid", "premium"])
    climate_vec = one_hot(destination.climate, ["cold", "moderate", "warm"])
    crowd_vec = one_hot(destination.crowd_level, ["low", "medium", "high"])
    region_vec = one_hot(destination.region, ["North", "South", "East", "West", "Northeast"])

    return np.concatenate([tag_vec, budget_vec, climate_vec, crowd_vec, region_vec])


def encode_preferences(
    prefs: PreferenceRequest,
    tag_index: Dict[str, int],
) -> np.ndarray:
    """Encode user preferences into a numeric feature vector."""
    tag_vec = np.zeros(len(tag_index), dtype=float)
    for tag in prefs.tags:
        key = tag.lower()
        if key in tag_index:
            tag_vec[tag_index[key]] = 1.0

    # Normalize historic level names if they appear
    level = None
    if prefs.budget_level:
        lowered = prefs.budget_level.lower()
        if lowered in {"low", "budget"}:
            level = "budget"
        elif lowered in {"mid", "medium"}:
            level = "mid"
        elif lowered in {"high", "premium"}:
            level = "premium"
        else:
            level = lowered

    budget_vec = one_hot(level, ["budget", "mid", "premium"])
    climate_vec = one_hot(prefs.climate, ["cold", "moderate", "warm"])
    crowd_vec = one_hot(prefs.crowd_level, ["low", "medium", "high"])

    # Region preference is not explicitly chosen yet, so we keep it neutral (zeros)
    region_vec = np.zeros(5, dtype=float)

    return np.concatenate([tag_vec, budget_vec, climate_vec, crowd_vec, region_vec])


def one_hot(value: str | None, allowed: Iterable[str]) -> np.ndarray:
    allowed_list = list(allowed)
    vec = np.zeros(len(allowed_list), dtype=float)
    if value is None:
        return vec
    value_lower = value.lower()
    if value_lower in allowed_list:
        vec[allowed_list.index(value_lower)] = 1.0
    return vec


# -----------------------------------------------------------------------------
# Recommender
# -----------------------------------------------------------------------------


@lru_cache()
def _tag_index_cached(destinations_key: Tuple[Tuple[int, str], ...]) -> Dict[str, int]:
    """Cache tag index keyed by destination ids/names to avoid rebuilds."""
    destinations = [Destination(id=did, name=name, country="", tags=[], budget_level="mid", climate="moderate", crowd_level="medium", latitude=0.0, longitude=0.0) for did, name in destinations_key]  # type: ignore[arg-type]
    return build_tag_vocab(destinations)


def recommend_destinations(
    destinations: Sequence[Destination],
    preferences: PreferenceRequest,
) -> List[Destination]:
    """
    Rank destinations using content-based filtering + cosine similarity.

    - Encodes destination attributes (tags + categorical signals)
    - Encodes user preferences into the same feature space
    - Uses cosine similarity to score and sort
    """
    if not destinations:
        return []

    tag_index = build_tag_vocab(destinations)

    dest_vectors = np.vstack([encode_destination(d, tag_index) for d in destinations])
    pref_vector = encode_preferences(preferences, tag_index).reshape(1, -1)

    scores = cosine_similarity(pref_vector, dest_vectors).flatten()
    ranked = sorted(zip(destinations, scores), key=lambda x: x[1], reverse=True)
    top_k = min(preferences.top_k, len(ranked))
    return [dest for dest, _ in ranked[:top_k]]


