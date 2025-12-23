import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useTrip, Destination } from "../state/TripContext";

const API_BASE = (import.meta as any).env?.VITE_API_BASE ?? "http://localhost:8000/api";

export function RecommendationsPage() {
  const navigate = useNavigate();
  const { preferences, setSelectedDestination } = useTrip();
  const [destinations, setDestinations] = useState<Destination[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!preferences) {
      navigate("/preferences", { replace: true });
      return;
    }

    const fetchRecommendations = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API_BASE}/recommend-destinations`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(preferences),
        });
        if (!res.ok) {
          throw new Error("API error");
        }
        const data = await res.json();
        setDestinations(data);
      } catch {
        setError("Could not reach API. Showing no destinations.");
      } finally {
        setLoading(false);
      }
    };

    fetchRecommendations();
  }, [preferences, navigate]);

  const handleSelect = (dest: Destination) => {
    setSelectedDestination(dest);
    navigate("/customize");
  };

  if (!preferences) return null;

  return (
    <div className="section animate-fade-in space-y-6">
      <header className="flex items-center justify-between">
        <div>
          <p className="uppercase text-xs tracking-[0.3em] text-forest dark:text-amber">
            Step 2 · Places
          </p>
          <h2 className="font-heading text-3xl md:text-4xl">
            Destinations that fit your travel mood
          </h2>
          <p className="text-sm text-black/70 dark:text-white/70 max-w-2xl">
            Pick one Indian destination to continue. You can always come back and explore other options.
          </p>
        </div>
        <button
          className="btn-ghost"
          type="button"
          onClick={() => navigate("/preferences")}
        >
          Edit preferences
        </button>
      </header>

      {loading && <p className="text-sm text-black/70 dark:text-white/70">Finding places that match your vibe…</p>}
      {error && <p className="text-sm text-terracotta dark:text-amber">{error}</p>}

      <div className="grid md:grid-cols-3 gap-4">
        {destinations.map((dest) => (
          <button
            key={dest.id}
            type="button"
            className="text-left card p-4 flex flex-col gap-3 hover:-translate-y-1 hover:shadow-soft transition-transform cursor-pointer"
            onClick={() => handleSelect(dest)}
          >
            <div>
              <h3 className="font-heading text-xl">{dest.name}</h3>
              <p className="text-sm text-black/70 dark:text-white/70">
                {dest.country}
              </p>
            </div>
            <div className="flex flex-wrap gap-2">
              {dest.tags.slice(0, 4).map((t) => (
                <span key={t} className="pill">
                  {t}
                </span>
              ))}
            </div>
          </button>
        ))}
        {!loading && destinations.length === 0 && !error && (
          <p className="text-sm text-black/70 dark:text-white/70">
            No destinations found. Try broadening your preferences.
          </p>
        )}
      </div>
    </div>
  );
}


