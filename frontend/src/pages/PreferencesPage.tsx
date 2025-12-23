import { FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import clsx from "clsx";
import { useTrip, PreferenceRequest } from "../state/TripContext";

const interestOptions = [
  "culture",
  "food",
  "nature",
  "adventure",
  "beach",
  "history",
  "scenic",
];

export function PreferencesPage() {
  const navigate = useNavigate();
  const { preferences, setPreferences, setSelectedDestination, setCustomization } =
    useTrip();

  const prefs: PreferenceRequest =
    preferences ?? {
      tags: ["culture", "food"],
      budget_level: "mid",
      climate: "warm",
      crowd_level: "medium",
      top_k: 6,
    };

  const toggleTag = (tag: string) => {
    const exists = prefs.tags.includes(tag);
    const next = {
      ...prefs,
      tags: exists ? prefs.tags.filter((t) => t !== tag) : [...prefs.tags, tag],
    };
    setPreferences(next);
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    setPreferences(prefs);
    // reset downstream state when starting over
    setSelectedDestination(null);
    setCustomization({
      days: 3,
      budgetPerDayInr: 12000,
      pace: "moderate",
      interests: prefs.tags,
    });
    navigate("/recommendations");
  };

  return (
    <div className="section animate-fade-in">
      <div className="card p-6 md:p-10 space-y-6">
        <header className="space-y-2">
          <p className="uppercase text-xs tracking-[0.3em] text-forest dark:text-amber">
            Step 1 · Preferences
          </p>
          <h2 className="font-heading text-3xl md:text-4xl">
            What kind of trip are you dreaming about?
          </h2>
          <p className="text-sm text-black/70 dark:text-white/70 max-w-2xl">
            Choose the moods and conditions that feel right. We will use these to
            find the best destinations that match your style.
          </p>
        </header>

        <form onSubmit={handleSubmit} className="grid md:grid-cols-3 gap-6">
          <div className="md:col-span-3 card p-4 space-y-3">
            <h3 className="font-semibold">Interests</h3>
            <div className="flex flex-wrap gap-2">
              {interestOptions.map((tag) => (
                <button
                  type="button"
                  key={tag}
                  onClick={() => toggleTag(tag)}
                  className={clsx(
                    "px-3 py-2 rounded-xl border text-sm transition",
                    prefs.tags.includes(tag)
                      ? "bg-forest text-white border-forest"
                      : "border-black/10 dark:border-white/10 hover:border-forest/40",
                  )}
                >
                  {tag}
                </button>
              ))}
            </div>
          </div>

          <DropdownCard
            label="Budget level"
            value={prefs.budget_level ?? ""}
            options={["low", "mid", "high"]}
            onChange={(v) => setPreferences({ ...prefs, budget_level: v })}
          />
          <DropdownCard
            label="Preferred climate"
            value={prefs.climate ?? ""}
            options={["cold", "moderate", "warm"]}
            onChange={(v) => setPreferences({ ...prefs, climate: v })}
          />

          <div className="card p-4 space-y-3 md:col-span-3 md:max-w-xs">
            <label className="flex items-center justify-between text-sm font-semibold">
              How many destinations?
              <input
                type="number"
                min={1}
                max={12}
                value={prefs.top_k}
                onChange={(e) =>
                  setPreferences({ ...prefs, top_k: Number(e.target.value) })
                }
                className="w-20 rounded-lg border border-black/10 bg-white/80 px-2 py-1 dark:border-white/10 dark:bg-olive"
              />
            </label>
            <p className="text-xs text-black/60 dark:text-white/60">
              We will rank the destinations using content-based similarity.
            </p>
          </div>

          <div className="md:col-span-3 flex justify-end">
            <button type="submit" className="btn-primary">
              Continue to places
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function DropdownCard({
  label,
  value,
  options,
  onChange,
}: {
  label: string;
  value: string;
  options: string[];
  onChange: (v: string) => void;
}) {
  return (
    <div className="card p-4 space-y-2">
      <label className="text-sm font-semibold">{label}</label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full rounded-xl border border-black/10 bg-white/80 px-3 py-2 text-sm dark:border-white/10 dark:bg-olive"
      >
        <option value="">Any</option>
        {options.map((opt) => (
          <option key={opt} value={opt}>
            {opt}
          </option>
        ))}
      </select>
    </div>
  );
}


