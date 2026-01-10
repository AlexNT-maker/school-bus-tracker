import time     
import random 
import json
import paho.mqtt.client as mqtt

# Χρησιμοποιούμε ένα δημόσιο broker για δοκιμή (Ρυθμίσεις mqtt)
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "schoolbus/bimbo/data"


#Αρχικές συντεταγμένες ΠΑΔΑ σε μορφή dictionary
bus_data = {
    "latitude": 38.0037,
    "longitude": 23.6757,
    "speed": 0,
    "accident": False,
    "alcohol_detected": False
}

def on_connect(client, userdata, flags, rc, properties = None):
    """Η συνάρτηση που καλούμε μόλις συνδεθούμε
    Παραμέτροι :
    Η συνάρτηση είναι τυποποιημένη στο documentation του paho-mqtt
      """
    if rc == 0:
        print("Connected with MQTT Broker")
    else:
        print(f"Unsuccesful attempt, code: {rc}")

#Δημιουργία client 
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect

print("Attempt to connect at Broker...")


# Προσομοίωση κίνησης, ταχύτητας και ατυχήματος -------------------------------------------------------------------
try:
    client.connect(BROKER, PORT, 60)
    client.loop_start() #Ξεκινάμε τη λούπα

    while (True):                                               
        bus_data["latitude"] += random.uniform(-0.0001, 0.0001)
        bus_data["longitude"] += random.uniform(-0.0001, 0.0001)

        bus_data["speed"] = round(random.uniform(0 , 95), 1) 

        if random.randint(0,100) > 98 :
            bus_data["accident"] = True
            print ("SOS: Accident detected")
        else: 
            bus_data["accident"] = False

        # Μετατροπή σε αρχείο JSON 
        payload = json.dumps(bus_data)
        client.publish(TOPIC, payload)

        print(f"Sended {payload}")

        time.sleep(5)  #Αναμονή πέντε δευτερολέπτων πριν το επόμενο μήνυμα

except KeyboardInterrupt:
    print("\n Simulator has stopped")
    client.loop_stop()
    client.disconnect

except Exception as e:
    print(f"Connection error: {e}")


# python simulator.py στο terminal για τεστάρισμα. Επειδή η λούπα είναι φτιαγμένη να μην σταματάει διακοπή με ctrl+c