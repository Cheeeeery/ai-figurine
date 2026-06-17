import paho.mqtt.client as mqtt
import time
import random
import sys

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
TOPIC_AUDIO_IN = "figurine/audio/in"
TOPIC_AUDIO_OUT = "figurine/audio/out"
TOPIC_STATUS = "figurine/status"

def create_mock_audio(text="你好"):
    import struct
    sample_rate = 16000
    duration = 2.0
    num_samples = int(sample_rate * duration)
    
    try:
        import numpy as np
        t = np.linspace(0, duration, num_samples, False)
        freq = 300 + random.random() * 200
        signal = np.sin(2 * np.pi * freq * t) * 0.3
        signal = (signal * 32767).astype(np.int16)
        return signal.tobytes()
    except ImportError:
        samples = []
        for i in range(num_samples):
            val = int(0.3 * 32767 * (1 if (i * 300 // sample_rate) % 2 == 0 else -1))
            samples.append(val)
        return struct.pack(f'<{len(samples)}h', *samples)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[MockDevice] Connected to MQTT broker")
        client.subscribe(TOPIC_AUDIO_OUT)
    else:
        print(f"[MockDevice] Connection failed: {rc}")

def on_message(client, userdata, msg):
    if msg.topic == TOPIC_AUDIO_OUT:
        if msg.payload == b'END':
            print("[MockDevice] Received END marker, playback complete")
        else:
            print(f"[MockDevice] Received audio chunk: {len(msg.payload)} bytes")

def main():
    client = mqtt.Client(client_id="figurine_device_mock")
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        
        time.sleep(2)
        
        print("\n[MockDevice] Simulating voice interaction...")
        print("[MockDevice] Recording...")
        time.sleep(1)
        
        audio_data = create_mock_audio()
        chunk_size = 4096
        
        for i in range(0, len(audio_data), chunk_size):
            chunk = audio_data[i:i+chunk_size]
            client.publish(TOPIC_AUDIO_IN, chunk)
        
        client.publish(TOPIC_AUDIO_IN, b'END')
        print(f"[MockDevice] Sent {len(audio_data)} bytes of audio")
        
        status = {
            "device": "figurine",
            "state": "waiting",
            "battery": 85,
            "rssi": -45,
            "uptime": 100
        }
        import json
        client.publish(TOPIC_STATUS, json.dumps(status))
        
        print("[MockDevice] Waiting for response...")
        time.sleep(10)
        
    except Exception as e:
        print(f"[MockDevice] Error: {e}")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == '__main__':
    main()
