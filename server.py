from flask import Flask, request
import paho.mqtt.client as mqtt
import json
import threading

app = Flask(__name__)

MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_TOPIC = 'test'  # Replace with your topic

@app.route('/')
def index():
    return "Pake MQTT Flask App"

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Received message: {payload}")
    data = json.loads(payload)
    vehicle_size = data.get('size')
    print(f"Vehicle Size: {vehicle_size}")
    
    # Print slot based on vehicle size
    if vehicle_size == 1:
        print("slot_1")
    elif vehicle_size == 2:
        print("slot_2")
    else:
        print("slot_3")

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

def start_mqtt():
    mqtt_client.loop_forever()

if __name__ == '__main__':
    mqtt_thread = threading.Thread(target=start_mqtt)
    mqtt_thread.start()
    app.run(debug=True)
