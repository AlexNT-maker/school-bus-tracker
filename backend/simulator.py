import time     
import random 
import json
import paho.mqtt.client as mqtt

# MQTT Broker Settings (Using a public broker for testing)
BROKER = "test.mosquitto.org"  #Χρήση δημόσιου server για επικοινωνία
PORT = 1883
TOPIC = "schoolbus/bimbo/data" # Unique topic for data publishing


# Initial Coordinates (University of West Attica - UNIWA)
bus_data = {
    "latitude": 38.0037,
    "longitude": 23.6757,
    "speed": 0,
    "accident": False,
    "alcohol_detected": False
}

def on_connect(client, userdata, flags, rc, properties = None):
    """Callback function triggered upon connection.
    rc=0 indicates a successful connection.
      """
    if rc == 0:
        print("Connected with MQTT Broker")
    else:
        print(f"Unsuccesful attempt, code: {rc}")

# Create MQTT Client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect

print("Attempt to connect at Broker...")


# Simulation Loop: Movement, Speed, and Accident Generation -------------------------------------------------------------------
try:
    client.connect(BROKER, PORT, 60) 
    client.loop_start() 

# Simulate small coordinate changes
    while (True):                                               
        bus_data["latitude"] += random.uniform(-0.0001, 0.0001)
        bus_data["longitude"] += random.uniform(-0.0001, 0.0001)

# Simulate speed
        bus_data["speed"] = round(random.uniform(0 , 95), 1) 

# Simulate accident (2% probability)
        if random.randint(0,100) > 98 :   
            bus_data["accident"] = True
            print ("SOS: Accident detected")
        else: 
            bus_data["accident"] = False

        # Convert to JSON format
        payload = json.dumps(bus_data)
        client.publish(TOPIC, payload)

        print(f"Sended {payload}")

        time.sleep(1)  # Wait 1 second before next update

except KeyboardInterrupt:
    print("\n Simulator has stopped")
    client.loop_stop()
    client.disconnect

except Exception as e:
    print(f"Connection error: {e}")


