import clsx from "clsx";
import { useLocation } from "react-router-dom";

const steps = [
  { id: "preferences", label: "Preferences", path: "/preferences" },
  { id: "recommendations", label: "Places", path: "/recommendations" },
  { id: "customize", label: "Customize", path: "/customize" },
  { id: "itinerary", label: "Itinerary", path: "/itinerary" },
];

export function Stepper() {
  const location = useLocation();

  const activeIndex = steps.findIndex((step) =>
    location.pathname.startsWith(step.path),
  );

  return (
    <nav className="flex items-center gap-4 text-sm">
      {steps.map((step, index) => {
        const isActive = index === activeIndex;
        const isCompleted = index < activeIndex;

        return (
          <div key={step.id} className="flex items-center gap-2">
            <div
              className={clsx(
                "h-8 w-8 rounded-full flex items-center justify-center border text-xs font-semibold",
                isActive &&
                  "bg-forest text-white border-forest dark:bg-amber dark:text-slate",
                !isActive &&
                  !isCompleted &&
                  "bg-white/70 dark:bg-olive/60 border-black/10 dark:border-white/10 text-black/60 dark:text-white/60",
                isCompleted &&
                  "bg-forest/10 dark:bg-amber/20 border-forest/40 dark:border-amber/40 text-forest dark:text-amber",
              )}
            >
              {index + 1}
            </div>
            <span
              className={clsx(
                "uppercase tracking-[0.2em]",
                isActive && "text-forest dark:text-amber",
                !isActive && "text-black/50 dark:text-white/50",
              )}
            >
              {step.label}
            </span>
            {index < steps.length - 1 && (
              <div className="h-px w-8 bg-gradient-to-r from-black/10 to-black/5 dark:from-white/10 dark:to-white/5" />
            )}
          </div>
        );
      })}
    </nav>
  );
}


