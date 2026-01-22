import network
import time
import machine
import math
import ubinascii
from umqtt.simple import MQTTClient
import json

# ==========================================
# 1. WIFI & MQTT CONFIGURATION
# ==========================================
WIFI_SSID = "WIFI"    
WIFI_PASS = "PASS"   

MQTT_BROKER = "test.mosquitto.org"
MQTT_TOPIC = "schoolbus/bimbo/data"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())

# ==========================================
# 2. PIN CONFIGURATION
# ==========================================
I2C_SCL = 22  
I2C_SDA = 19  
GAS_PIN = 34  
LED_PIN = 23  
BUZZER_PIN = 18 
BUTTON_PIN = 4  

ALCOHOL_LIMIT = 2000    
CRASH_LIMIT = 2.0       

# ==========================================
# 3. MPU6050 CLASS (Driver)
# ==========================================
class MPU6050:
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        try:
            self.i2c.writeto(self.addr, bytearray([107, 0]))
        except:
            print("❌ MPU6050 Error")

    def get_values(self):
        try:
            raw = self.i2c.readfrom_mem(self.addr, 0x3B, 14)
            vals = {}
            vals['AcX'] = self.bytes_to_int(raw[0], raw[1])
            vals['AcY'] = self.bytes_to_int(raw[2], raw[3])
            vals['AcZ'] = self.bytes_to_int(raw[4], raw[5])
            return vals
        except:
            return {'AcX':0, 'AcY':0, 'AcZ':0}

    def bytes_to_int(self, first, second):
        val = (first << 8) | second
        if val & 0x8000: return val - 0x10000
        return val

# ==========================================
# 4. SETUP FUNCTIONS
# ==========================================
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            pass
    print('✅ WiFi Connected:', wlan.ifconfig())

def connect_mqtt():
    try:
        client = MQTTClient(CLIENT_ID, MQTT_BROKER)
        client.connect()
        print('✅ MQTT Connected')
        return client
    except Exception as e:
        print('❌ MQTT Connection Failed:', e)
        return None

# ==========================================
# 5. MAIN PROGRAM
# ==========================================
# Hardware Setup
i2c = machine.I2C(0, scl=machine.Pin(I2C_SCL), sda=machine.Pin(I2C_SDA))
mpu = MPU6050(i2c)
adc = machine.ADC(machine.Pin(GAS_PIN))
adc.atten(machine.ADC.ATTN_11DB)
led = machine.Pin(LED_PIN, machine.Pin.OUT)
buzzer = machine.Pin(BUZZER_PIN, machine.Pin.OUT)
button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

# Connect to Internet
connect_wifi()
mqtt_client = connect_mqtt()

alarm_active = False

print("--- SYSTEM READY ---")

while True:
    try:
        # Read Sensors
        alcohol_val = adc.read()
        data = mpu.get_values()
        total_g = math.sqrt((data['AcX']/16384)**2 + (data['AcY']/16384)**2 + (data['AcZ']/16384)**2)
        impact = abs(total_g - 1)

        # Logic
        accident_detected = impact > CRASH_LIMIT
        drunk_detected = alcohol_val > ALCOHOL_LIMIT
        
        if accident_detected or drunk_detected:
            alarm_active = True
            print(f"🚨 ALERT! Impact: {impact:.2f}G, Alcohol: {alcohol_val}")

        # Handle Alarm
        if alarm_active:
            led.value(1)
            buzzer.value(1)
            time.sleep(0.1)
            led.value(0)
            buzzer.value(0)
            time.sleep(0.1)
            
            if button.value() == 0: # Reset
                alarm_active = False
                print("✅ Alarm Reset")
                time.sleep(1)

        # Send Data to Backend via MQTT
        if mqtt_client:
            payload = json.dumps({
                "latitude": 38.0037,    
                "longitude": 23.6757,
                "speed": 0,             
                "accident": alarm_active,
                "alcohol": alcohol_val
            })
            mqtt_client.publish(MQTT_TOPIC, payload)
            print(".", end="") 

        time.sleep(0.5)

    except Exception as e:
        print("Error:", e)
        time.sleep(1)
        # Try to reconnect MQTT if failed
        if mqtt_client: 
            try: mqtt_client.connect()
            except: pass