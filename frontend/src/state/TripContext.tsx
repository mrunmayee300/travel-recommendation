import {
  createContext,
  useContext,
  useState,
  ReactNode,
  useEffect,
} from "react";

export type PreferenceRequest = {
  tags: string[];
  budget_level?: string | null;
  climate?: string | null;
  crowd_level?: string | null;
  top_k: number;
};

export type Destination = {
  id: number;
  name: string;
  country: string;
  tags: string[];
  budget_level: string;
  climate: string;
  crowd_level: string;
  latitude: number;
  longitude: number;
};

export type Customization = {
  days: number;
  budgetPerDayInr: number;
  pace: "relaxed" | "moderate" | "full";
  interests: string[];
};

type TripState = {
  preferences: PreferenceRequest | null;
  setPreferences: (p: PreferenceRequest) => void;
  selectedDestination: Destination | null;
  setSelectedDestination: (d: Destination | null) => void;
  customization: Customization | null;
  setCustomization: (c: Customization) => void;
  resetTrip: () => void;
};

const TripContext = createContext<TripState | undefined>(undefined);

export function TripProvider({ children }: { children: ReactNode }) {
  const [preferences, setPreferencesState] = useState<PreferenceRequest | null>(
    null,
  );
  const [selectedDestination, setSelectedDestination] =
    useState<Destination | null>(null);
  const [customization, setCustomizationState] =
    useState<Customization | null>(null);

  // simple in-memory state for now; can extend to localStorage later
  useEffect(() => {
    // placeholder for potential persistence hook
  }, []);

  const resetTrip = () => {
    setPreferencesState(null);
    setSelectedDestination(null);
    setCustomizationState(null);
  };

  const value: TripState = {
    preferences,
    setPreferences: setPreferencesState,
    selectedDestination,
    setSelectedDestination,
    customization,
    setCustomization: setCustomizationState,
    resetTrip,
  };

  return <TripContext.Provider value={value}>{children}</TripContext.Provider>;
}

export function useTrip() {
  const ctx = useContext(TripContext);
  if (!ctx) {
    throw new Error("useTrip must be used within TripProvider");
  }
  return ctx;
}


