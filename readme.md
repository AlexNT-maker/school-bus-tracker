# School Bus Tracker System

Ένα σύστημα παρακολούθησης σχολικού λεωφορείου σε πραγματικό χρόνο.

## 🛠️ Τεχνολογίες
* **Frontend:** Next.js, React, Tailwind CSS, React-Leaflet
* **Backend:** Python, FastAPI
* **IoT/Messaging:** MQTT (Mosquitto Broker), Paho-MQTT
* **Simulation:** Python Script

## Πώς να το τρέξετε

Θα χρειαστείτε 3 διαφορετικά τερματικά:

**1. Backend (Server)**
```bash
cd backend
.\env\Scripts\activate
python -m uvicorn main:app --reload

cd backend
.\env\Scripts\activate
python simulator.py

cd frontend
npm run dev



