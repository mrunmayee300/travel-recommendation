import { useEffect, useRef } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

// Fix default marker icons (Leaflet issue with webpack/vite)
import icon from "leaflet/dist/images/marker-icon.png";
import iconShadow from "leaflet/dist/images/marker-shadow.png";

const DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

L.Marker.prototype.options.icon = DefaultIcon;

type Activity = {
  attraction_id: number;
  name: string;
  category: string;
  estimated_time_hours: number;
  estimated_cost: number;
  latitude: number;
  longitude: number;
  distance_from_prev_km?: number | null;
};

type Day = {
  day: number;
  activities: Activity[];
  estimated_day_cost: number;
};

type ItineraryMapProps = {
  destinationName: string;
  destinationLat: number;
  destinationLng: number;
  days: Day[];
};

// Day colors for markers
const DAY_COLORS = [
  "#2F5D46", // Forest green (Day 1)
  "#C16A4A", // Terracotta (Day 2)
  "#F59E0B", // Amber (Day 3)
  "#8B5CF6", // Purple (Day 4+)
];

function MapCenter({ lat, lng }: { lat: number; lng: number }) {
  const map = useMap();
  useEffect(() => {
    map.setView([lat, lng], 12);
  }, [map, lat, lng]);
  return null;
}

export function ItineraryMap({
  destinationName,
  destinationLat,
  destinationLng,
  days,
}: ItineraryMapProps) {
  // Create custom markers for each day
  const createDayIcon = (dayNum: number) => {
    const color = DAY_COLORS[(dayNum - 1) % DAY_COLORS.length];
    return L.divIcon({
      className: "custom-marker",
      html: `<div style="
        background-color: ${color};
        width: 24px;
        height: 24px;
        border-radius: 50%;
        border: 2px solid white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 11px;
      ">${dayNum}</div>`,
      iconSize: [24, 24],
      iconAnchor: [12, 12],
    });
  };

  // Collect all activities with coordinates
  const markers: Array<{
    lat: number;
    lng: number;
    day: number;
    activity: Activity;
  }> = [];

  days.forEach((day) => {
    day.activities.forEach((activity) => {
      if (activity.latitude && activity.longitude) {
        markers.push({
          lat: activity.latitude,
          lng: activity.longitude,
          day: day.day,
          activity,
        });
      }
    });
  });

  if (markers.length === 0) {
    // Fallback: show destination center if no attraction coords
    return (
      <div className="h-full w-full rounded-xl bg-gradient-to-br from-forest/15 via-terracotta/10 to-amber/20 dark:from-olive dark:via-slate dark:to-amber/20 flex items-center justify-center text-sm text-black/70 dark:text-white/70">
        <div className="text-center">
          <p className="font-semibold mb-2">Map View</p>
          <p className="text-xs">No attraction coordinates available.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full w-full rounded-xl overflow-hidden border border-black/10 dark:border-white/10">
      <MapContainer
        center={[destinationLat, destinationLng]}
        zoom={11}
        style={{ height: "100%", width: "100%" }}
        scrollWheelZoom={true}
      >
        <MapCenter lat={destinationLat} lng={destinationLng} />
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        {/* Destination center marker */}
        <Marker position={[destinationLat, destinationLng]}>
          <Popup>
            <div className="font-semibold text-forest dark:text-amber">{destinationName}</div>
            <div className="text-xs text-black/70 dark:text-white/70">Trip Destination</div>
          </Popup>
        </Marker>

        {/* Activity markers by day */}
        {markers.map((marker, idx) => (
          <Marker
            key={`${marker.day}-${marker.activity.attraction_id}-${idx}`}
            position={[marker.lat, marker.lng]}
            icon={createDayIcon(marker.day)}
          >
            <Popup>
              <div className="text-sm">
                <div className="font-semibold">{marker.activity.name}</div>
                <div className="text-xs text-black/70 dark:text-white/70 mt-1">
                  Day {marker.day} • {marker.activity.category}
                </div>
                <div className="text-xs text-black/60 dark:text-white/60 mt-1">
                  {marker.activity.estimated_time_hours}h • ₹{marker.activity.estimated_cost.toFixed(0)}
                </div>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}

