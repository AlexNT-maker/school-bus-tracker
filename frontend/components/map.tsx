"use client";   // Informs Next.js that this runs only on browser

import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet"; 
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import { useEffect } from "react";

// Fix for icon issues due to a known bug between Leaflet and React ----------------------------------
// Specifying external URLs for the marker images -------------------------------------------------------
const iconUrl = "https://unpkg.com/leaflet@1.9.3/dist/images/marker-icon.png";
const iconRetinaUrl = "https://unpkg.com/leaflet@1.9.3/dist/images/marker-icon-2x.png";
const shadowUrl = "https://unpkg.com/leaflet@1.9.3/dist/images/marker-shadow.png";

// Create the custom icon object ----------------------------------------------------
const defaultIcon = L.icon({
  iconUrl: iconUrl,
  iconRetinaUrl: iconRetinaUrl,
  shadowUrl: shadowUrl,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

// Define the Props interface for TypeScript ---------------------------------------
interface MapProps {
  lat: number;
  lng: number;
}

// Helper component to re-center the map when coordinates change
function Recenter({ lat, lng }: { lat: number; lng: number }) {
  const map = useMap(); 
  useEffect(() => {
    map.setView([lat, lng]); 
  }, [lat, lng, map]); 
  return null;
}


export default function Map({ lat, lng }: MapProps) {
  return (
    // Map Container with styling -----------------------------------------------------------
    <div className="h-full w-full rounded-lg overflow-hidden border-4 border-blue-500 shadow-xl">
      <MapContainer
        center={[lat, lng]}
        zoom={16} 
        scrollWheelZoom={true}
        className="h-full w-full"
        style={{ height: "100%", width: "100%" }}
      >
        {/* Use OpenStreetMap tiles */}
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        {/* Auto-recenter map on update */}
        <Recenter lat={lat} lng={lng} />

        <Marker position={[lat, lng]} icon={defaultIcon}>
          <Popup>
            Εδώ είναι το σχολικό! <br />
          </Popup>
        </Marker>
      </MapContainer>
    </div>
  );
}