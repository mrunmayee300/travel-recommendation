import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useTrip } from "../state/TripContext";
import { ItineraryMap } from "../components/ItineraryMap";

type ItineraryActivity = {
  attraction_id: number;
  name: string;
  category: string;
  estimated_time_hours: number;
  estimated_cost: number;
  latitude: number;
  longitude: number;
  distance_from_prev_km?: number | null;
};

type ItineraryDay = {
  day: number;
  activities: ItineraryActivity[];
  estimated_day_cost: number;
};

type ItineraryResponse = {
  destination_id: number;
  destination_name: string;
  days: ItineraryDay[];
};

type NearbySuggestion = {
  destination_id: number;
  name: string;
  country: string;
  distance_km: number;
  feasible: boolean;
  notes: string;
};

const API_BASE = (import.meta as any).env?.VITE_API_BASE ?? "http://localhost:8000/api";

export function ItineraryPage() {
  const navigate = useNavigate();
  const { preferences, selectedDestination, customization } = useTrip();
  const [itinerary, setItinerary] = useState<ItineraryResponse | null>(null);
  const [nearby, setNearby] = useState<NearbySuggestion[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!preferences) {
      navigate("/preferences", { replace: true });
      return;
    }
    if (!selectedDestination) {
      navigate("/recommendations", { replace: true });
      return;
    }
    if (!customization) {
      navigate("/customize", { replace: true });
      return;
    }

    const fetchItinerary = async () => {
      setLoading(true);
      setError(null);
      try {
        const payload = {
          destination_id: selectedDestination.id,
          days: customization.days,
          budget: customization.days * customization.budgetPerDayInr,
          interests: customization.interests.length
            ? customization.interests
            : preferences.tags,
          pace: "moderate", // Default pace since removed from UI
        };
        const res = await fetch(`${API_BASE}/generate-itinerary`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        if (!res.ok) throw new Error("API error");
        const data = (await res.json()) as ItineraryResponse;
        setItinerary(data);
      } catch {
        setError("Could not generate itinerary from API.");
      } finally {
        setLoading(false);
      }
    };

    const fetchNearby = async () => {
      try {
        const res = await fetch(`${API_BASE}/nearby-expansions`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            destination_id: selectedDestination.id,
            extra_days: 2,
            extra_budget: 2 * customization.budgetPerDayInr,
            radius_km: 600,
          }),
        });
        if (!res.ok) throw new Error("API error");
        const data = (await res.json()) as { suggestions: NearbySuggestion[] };
        setNearby(data.suggestions);
      } catch {
        // keep silent; optional
      }
    };

    fetchItinerary();
    fetchNearby();
  }, [preferences, selectedDestination, customization, navigate]);

  if (!preferences || !selectedDestination || !customization) return null;

  return (
    <div className="section animate-fade-in space-y-6">
      <header className="flex items-center justify-between">
        <div>
          <p className="uppercase text-xs tracking-[0.3em] text-forest dark:text-amber">
            Step 4 · Itinerary
          </p>
          <h2 className="font-heading text-3xl md:text-4xl">
            Your Explorer&apos;s Journal for {selectedDestination.name}
          </h2>
          <p className="text-sm text-black/70 dark:text-white/70 max-w-2xl">
            A soft, day-wise plan in INR, with nearby expansions for when the journey asks for a little more.
          </p>
        </div>
        <button
          className="btn-ghost"
          type="button"
          onClick={() => navigate("/customize")}
        >
          Adjust trip
        </button>
      </header>

      {loading && <p className="text-sm text-black/70 dark:text-white/70">Sketching your days…</p>}
      {error && <p className="text-sm text-terracotta dark:text-amber">{error}</p>}

      <section className="grid lg:grid-cols-[2fr,1.2fr] gap-6 items-start">
        <div className="card p-5 space-y-4">
          <h3 className="font-heading text-2xl">Itinerary timeline</h3>
          {itinerary ? (
            <div className="space-y-4">
              {itinerary.days.map((day) => (
                <div
                  key={day.day}
                  className="border-l-4 border-forest/70 dark:border-amber/70 pl-4"
                >
                  <p className="font-semibold text-forest dark:text-amber">
                    Day {day.day}
                  </p>
                  <ul className="space-y-2 mt-2">
                    {day.activities.map((act) => (
                      <li
                        key={act.attraction_id}
                        className="rounded-lg bg-white/70 dark:bg-olive/60 px-3 py-2"
                      >
                        <div className="flex items-center justify-between">
                          <span className="font-semibold">{act.name}</span>
                          <span className="text-sm text-black/60 dark:text-white/60">
                            {act.category}
                          </span>
                        </div>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-black/70 dark:text-white/70">
              We&apos;ll fill this timeline as soon as the API responds.
            </p>
          )}
        </div>

        <div className="card p-5 space-y-4">
          <h3 className="font-heading text-xl">Map & nearby ideas</h3>
          {itinerary && selectedDestination ? (
            <div className="h-96 rounded-xl overflow-hidden">
              <ItineraryMap
                destinationName={itinerary.destination_name}
                destinationLat={selectedDestination.latitude}
                destinationLng={selectedDestination.longitude}
                days={itinerary.days}
              />
            </div>
          ) : (
            <div className="h-48 rounded-xl bg-gradient-to-br from-forest/15 via-terracotta/10 to-amber/20 dark:from-olive dark:via-slate dark:to-amber/20 flex items-center justify-center text-sm text-black/70 dark:text-white/70">
              Map will appear once itinerary is generated.
            </div>
          )}
          <div className="space-y-2">
            {nearby.length === 0 && (
              <p className="text-sm text-black/60 dark:text-white/60">
                Nearby suggestions will appear here when available.
              </p>
            )}
            {nearby.map((s) => (
              <div
                key={s.destination_id}
                className="rounded-lg border border-black/5 dark:border-white/10 px-3 py-2"
              >
                <div className="flex items-center justify-between">
                  <p className="font-semibold">{s.name}</p>
                  <span className="pill">{s.distance_km} km</span>
                </div>
                <p className="text-sm text-black/70 dark:text-white/70">
                  {s.country}
                </p>
                <p className="text-xs mt-1 text-forest dark:text-amber">
                  {s.notes}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}


