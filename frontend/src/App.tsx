import { useEffect, useState } from "react";
import { BrowserRouter, Navigate, Route, Routes, useNavigate } from "react-router-dom";
import clsx from "clsx";
import { Stepper } from "./components/Stepper";
import { TripProvider, useTrip } from "./state/TripContext";
import { PreferencesPage } from "./pages/PreferencesPage";
import { RecommendationsPage } from "./pages/RecommendationsPage";
import { CustomizePage } from "./pages/CustomizePage";
import { ItineraryPage } from "./pages/ItineraryPage";

function AppShell() {
  const [theme, setTheme] = useState<"light" | "dark">("light");
  const navigate = useNavigate();
  const { resetTrip } = useTrip();

  useEffect(() => {
    document.documentElement.classList.toggle("dark", theme === "dark");
  }, [theme]);

  const handleRestart = () => {
    resetTrip();
    navigate("/preferences", { replace: true });
  };

  return (
    <div
      className={clsx(
        "min-h-screen pb-16 transition-colors",
        theme === "dark" ? "bg-olive text-white" : "bg-sand text-charcoal",
      )}
    >
      <header className="section flex items-center justify-between py-6">
        <div className="flex items-center gap-4">
          <button
            onClick={handleRestart}
            className="flex items-center justify-center w-10 h-10 rounded-full bg-forest/10 dark:bg-amber/10 hover:bg-forest/20 dark:hover:bg-amber/20 transition-colors cursor-pointer"
            title="Restart journey"
            type="button"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="w-6 h-6 text-forest dark:text-amber"
            >
              <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8" />
              <path d="M21 3v5h-5" />
              <path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16" />
              <path d="M3 21v-5h5" />
            </svg>
          </button>
          <div>
            <p className="text-sm uppercase tracking-[0.2em] text-forest dark:text-amber">
              Explorer's Journal 
            </p>
            <h1 className="font-heading text-3xl md:text-4xl mt-1">
              Craft your next travel story
            </h1>
          </div>
        </div>
        <div className="flex flex-col items-end gap-2">
          <Stepper />
          <button
            className="btn-ghost text-xs px-3 py-1"
            onClick={() => setTheme(theme === "light" ? "dark" : "light")}
          >
            {theme === "light" ? "Dark mode" : "Light mode"}
          </button>
        </div>
      </header>

      <main className="space-y-10 mt-2">
        <Routes>
          <Route path="/" element={<Navigate to="/preferences" replace />} />
          <Route path="/preferences" element={<PreferencesPage />} />
          <Route path="/recommendations" element={<RecommendationsPage />} />
          <Route path="/customize" element={<CustomizePage />} />
          <Route path="/itinerary" element={<ItineraryPage />} />
          <Route path="*" element={<Navigate to="/preferences" replace />} />
        </Routes>
      </main>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <TripProvider>
        <AppShell />
      </TripProvider>
    </BrowserRouter>
  );
}

export default App;


