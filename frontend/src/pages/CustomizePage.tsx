import { FormEvent, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useTrip } from "../state/TripContext";

const indiaInterestOptions = [
  "Spiritual",
  "Wildlife",
  "Monsoon-friendly",
  "Hill station",
  "Beach",
  "Heritage & Forts",
  "Food & Street food",
];

export function CustomizePage() {
  const navigate = useNavigate();
  const { preferences, selectedDestination, customization, setCustomization } =
    useTrip();
  const [localInterests, setLocalInterests] = useState<string[]>(
    customization?.interests ?? [],
  );

  useEffect(() => {
    if (!preferences) {
      navigate("/preferences", { replace: true });
      return;
    }
    if (!selectedDestination) {
      navigate("/recommendations", { replace: true });
    }
  }, [preferences, selectedDestination, navigate]);

  if (!preferences || !selectedDestination) return null;

  const local = {
    days: customization?.days ?? 4,
    budgetPerDayInr: customization?.budgetPerDayInr ?? 12000,
    pace: customization?.pace ?? "moderate" as const,
  };

  const toggleInterest = (tag: string) => {
    setLocalInterests((prev) =>
      prev.includes(tag) ? prev.filter((t) => t !== tag) : [...prev, tag],
    );
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    setCustomization({
      days: local.days,
      budgetPerDayInr: local.budgetPerDayInr,
      pace: "moderate", // Default pace since removed from UI
      interests: localInterests,
    });
    navigate("/itinerary");
  };

  return (
    <div className="section animate-fade-in">
      <div className="card p-6 md:p-10 space-y-6">
        <header className="space-y-2">
          <p className="uppercase text-xs tracking-[0.3em] text-forest dark:text-amber">
            Step 3 · Customize
          </p>
          <h2 className="font-heading text-3xl md:text-4xl">
            Shape your time in {selectedDestination.name}
          </h2>
          <p className="text-sm text-black/70 dark:text-white/70 max-w-2xl">
            Balance days and budget. We will generate a practical itinerary for you.
          </p>
        </header>

        <form
          onSubmit={handleSubmit}
          className="grid md:grid-cols-3 gap-6 items-start"
        >
          <div className="card p-4 space-y-4">
            <label className="text-sm font-semibold flex items-center justify-between">
              Number of days
              <span className="text-xs text-black/60 dark:text-white/60">
                {local.days} days
              </span>
            </label>
            <input
              type="range"
              min={2}
              max={14}
              value={local.days}
              onChange={(e) =>
                setCustomization({
                  ...local,
                  days: Number(e.target.value),
                  interests: localInterests,
                })
              }
              className="w-full accent-forest"
            />

            <label className="text-sm font-semibold flex items-center justify-between">
              Budget per day (₹)
              <span className="text-xs text-black/60 dark:text-white/60">
                ₹{local.budgetPerDayInr.toLocaleString("en-IN")}
              </span>
            </label>
            <input
              type="range"
              min={5000}
              max={25000}
              step={1000}
              value={local.budgetPerDayInr}
              onChange={(e) =>
                setCustomization({
                  ...local,
                  budgetPerDayInr: Number(e.target.value),
                  interests: localInterests,
                })
              }
              className="w-full accent-forest"
            />
          </div>

          <div className="md:col-span-2 card p-4 space-y-3">
            <h3 className="font-semibold">Interests (India-specific)</h3>
            <p className="text-xs text-black/60 dark:text-white/60">
              Refine what you want to focus on in this trip.
            </p>
            <div className="flex flex-wrap gap-2 mt-2">
              {indiaInterestOptions.map((tag) => (
                <button
                  key={tag}
                  type="button"
                  onClick={() => toggleInterest(tag)}
                  className={`px-3 py-2 rounded-xl border text-sm ${
                    localInterests.includes(tag)
                      ? "bg-forest text-white border-forest"
                      : "border-black/10 dark:border-white/10 bg-white/80 dark:bg-olive"
                  }`}
                >
                  {tag}
                </button>
              ))}
            </div>
          </div>

          <div className="md:col-span-3 flex justify-between items-center">
            <button
              type="button"
              className="btn-ghost"
              onClick={() => navigate("/recommendations")}
            >
              Back to places
            </button>
            <button type="submit" className="btn-primary">
              See itinerary
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}


