from fastapi import FastAPI
import json
import asyncio
from contextlib import asynccontextmanager
import paho.mqtt.client as mqtt
from fastapi.middleware.cors import CORSMiddleware



BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "schoolbus/bimbo/data"

# Σε αυτό το dictionary θα αποθηκευτεί το τελευταίο στίγμα που λάβαμε
latest_data = {
    "latitude": 0,
    "longitude": 0,
    "speed": 0,
    "accident": False,
    "message": "Waiting for data..."
}

# Η συνάρτηση που τρέχει όταν λαμβάνουμε μήνυμα απο το MQTT
def on_message(client, userdata, msg):
    global latest_data
    try:
        # Αποκωδικοποίηση του μηνύματος από bytes σε string και μετά σε λεξικό (JSON)
        payload = msg.payload.decode ("utf-8")
        data = json.loads(payload)

        latest_data = data 
        print (f"New pinpoint {latest_data['speed']} km/h")

    except Exception as e:
        print(f"Error: {e}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message

# Εκκίνηση τερματισμός του MQTT μαζί με το FASTAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        client.connect(BROKER, PORT, 60)
        client.subscribe(TOPIC)
        client.loop_start()
        print(f"backend connect to {TOPIC}")
    except Exception as e:
        print(f"Connection problem with MQTT: {e}")

    yield

    client.loop_stop()
    client.disconnect()
    print("Backend MQTT disconnected")

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Online", "service": "School Bus Tracker Backend"}

@app.get("/api/bus-location")
def get_bus_location():
    """
    Επιστρέφει το τελευταίο γνωστό στίγμα του λεωφορείου
    """
    return latest_data