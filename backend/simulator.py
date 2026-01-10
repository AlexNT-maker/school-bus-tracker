import time     
import random 
import json
import paho.mqtt.client as mqtt

# Χρησιμοποιούμε ένα δημόσιο broker για δοκιμή (Ρυθμίσεις mqtt)
BROKER = "test.mosquitto.org"  #Χρήση δημόσιου server για επικοινωνία
PORT = 1883
TOPIC = "schoolbus/bimbo/data" #Μοναδικό topic για να δημοσιεύουμε τα δεδομένα


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
    Η συνάρτηση είναι τυποποιημένη στο documentation του paho-mqtt. rc=0 σημαίνει ότι η σύνδεση πέτυχε
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
    client.connect(BROKER, PORT, 60) #Σύνδεση στον server
    client.loop_start() 

#Ατέρμονος βρόχος για συνεχή συλλογή δεδομένων
    while (True):                                               
        bus_data["latitude"] += random.uniform(-0.0001, 0.0001)
        bus_data["longitude"] += random.uniform(-0.0001, 0.0001)

        bus_data["speed"] = round(random.uniform(0 , 95), 1) 

        if random.randint(0,100) > 98 :   #2% πιθανότητα ατυχήματος
            bus_data["accident"] = True
            print ("SOS: Accident detected")
        else: 
            bus_data["accident"] = False

        # Μετατροπή σε αρχείο JSON για να μπορεί να διαβαστεί απο παντού
        payload = json.dumps(bus_data)
        client.publish(TOPIC, payload)

        print(f"Sended {payload}")

        time.sleep(1)  #Αναμονή ένα δευτερόλεπτο πριν το επόμενο στίγμα

except KeyboardInterrupt:
    print("\n Simulator has stopped")
    client.loop_stop()
    client.disconnect

except Exception as e:
    print(f"Connection error: {e}")


# python simulator.py στο terminal για τεστάρισμα. Επειδή η λούπα είναι φτιαγμένη να μην σταματάει διακοπή με ctrl+c