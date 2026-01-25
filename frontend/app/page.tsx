"use client";
import { useState, useEffect } from "react";
import dynamic from "next/dynamic";

// Map Loading ------------------------------------------------------------------------------------------
const Map = dynamic(() => import("../components/map"), { 
  ssr: false, 
  loading: () => <p className="text-center p-10">Φόρτωση χάρτη...</p> 
});

export default function Home() {
  // Page State Management ------------------------------------------------------------------------------------
  const [busData, setBusData] = useState({
    latitude: 38.0037, // Αρχική θέση (ΠΑΔΑ)
    longitude: 23.6757,
    speed: 0,
    accident: false
  });

  // Data Fetching Interval (Polls Python Backend) -------------------------------------------
  useEffect(() => {
    const timer = setInterval(async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/bus-location");
        const data = await response.json();
        
        if (data.latitude !== 0) {
          setBusData(data);
        }
      } catch (error) {
        console.error("Backend is not responding:", error);
      }
    }, 1000); 

    return () => clearInterval(timer);
  }, []);

  // UI Rendering with Tailwind CSS ------------------------------------------------------------------------
  return (
    <main className="flex min-h-screen flex-col items-center p-4 bg-slate-50">
      
      {/* Header / Dashboard */}
      <div className="z-10 w-full max-w-5xl items-center justify-between font-mono text-sm lg:flex mb-6 bg-white p-6 rounded-xl shadow-sm border border-slate-200">
        <div>
          <h1 className="text-3xl font-bold text-blue-900 mb-2">
            Bus Tracker 
          </h1>
          <p className="text-slate-500">Παρακολουθήστε το σχολικό σε πραγματικό χρόνο.</p>
        </div>

        {/* Speed and Status Indicators */}
        <div className="flex gap-4 mt-4 lg:mt-0">
          <div className="bg-blue-50 p-3 rounded-lg text-center min-w-[100px]">
            <span className="block text-xs text-blue-500 font-bold uppercase">ΤΑΧΥΤΗΤΑ</span>
            <span className="text-2xl font-bold text-blue-800">{busData.speed} <span className="text-sm">km/h</span></span>
          </div>
          
          {/*Status Box, changes color on accident*/}
          <div className={`p-3 rounded-lg text-center min-w-[120px] ${busData.accident ? 'bg-red-100' : 'bg-green-100'}`}>
            <span className={`block text-xs font-bold uppercase ${busData.accident ? 'text-red-600' : 'text-green-600'}`}>ΚΑΤΑΣΤΑΣΗ</span>
            <span className={`text-xl font-bold ${busData.accident ? 'text-red-700 animate-pulse' : 'text-green-700'}`}>
              {busData.accident ? "SOS 🚨" : "ΟΚ ✅"}
            </span>
          </div>
        </div>
      </div>

      {/* Map Component */}
      <div className="w-full max-w-5xl h-[60vh] bg-white rounded-2xl shadow-xl overflow-hidden border-4 border-white">
        <Map lat={busData.latitude} lng={busData.longitude} />
      </div>

    </main>
  );
}