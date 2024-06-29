from flask import Flask, render_template
import paho.mqtt.client as mqtt
import json
import threading

app = Flask(__name__)

MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_TOPIC = 'test'  # Replace with your topic

mqtt_data={

    'suitable_slot': 'N/A',
    'slot_1': 'N/A',
    'slot_2': 'N/A',
    'slot_3': 'N/A',
    'vehicle_size': 'N/A'
}

@app.route('/')
def index():
    return render_template("index.html", **mqtt_data)

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    global mqtt_data
    payload = msg.payload.decode()
    print(f"Received message: {payload}")
    data = json.loads(payload)
    
    with threading.Lock():
        mqtt_data['vehicle_size'] = data.get('size', 'N/A')
        if mqtt_data['vehicle_size'] == 1:
            mqtt_data['suitable_slot'] = 'Slot 1'
            mqtt_data['slot_1'] = 'Occupied'
        elif mqtt_data['vehicle_size'] == 2:
            mqtt_data['suitable_slot'] = 'Slot 2'
            mqtt_data['slot_2'] = 'Available'
        else:
            mqtt_data['suitable_slot'] = 'Slot 3'
            mqtt_data['slot_3'] = 'Available'

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
