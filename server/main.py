import yaml
import os
import sys
import signal
import time

from mqtt_handler import MQTTHandler
from asr_engine import ASREngine
from llm_engine import LLMEngine
from tts_engine import TTSEngine

class FigurineServer:
    def __init__(self, config_path='config.yaml'):
        self.config = self._load_config(config_path)
        self.mqtt = MQTTHandler(self.config['mqtt'])
        self.asr = ASREngine(self.config['asr'])
        self.llm = LLMEngine(self.config['llm'])
        self.tts = TTSEngine(self.config['tts'])
        
        self.is_processing = False
        self._setup_callbacks()
    
    def _load_config(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _setup_callbacks(self):
        self.mqtt.set_audio_callback(self._on_audio_received)
        self.mqtt.set_status_callback(self._on_status_received)
    
    def _on_audio_received(self, audio_data):
        if self.is_processing:
            print("[Server] Already processing, ignoring...")
            return
        
        self.is_processing = True
        
        try:
            print(f"[Server] Received audio: {len(audio_data)} bytes")
            
            self.mqtt.publish_status({"state": "processing", "device": "figurine"})
            
            print("[Server] Running ASR...")
            text = self.asr.recognize(audio_data)
            print(f"[Server] ASR result: {text}")
            
            if not text:
                print("[Server] No speech detected")
                self.is_processing = False
                return
            
            print("[Server] Generating LLM response...")
            response = self.llm.generate_response(text)
            print(f"[Server] LLM response: {response}")
            
            print("[Server] Generating speech...")
            audio_response = self.tts.generate(response)
            print(f"[Server] TTS generated: {len(audio_response)} bytes")
            
            print("[Server] Sending audio response...")
            self.mqtt.publish_audio(audio_response)
            
            print("[Server] Processing complete")
        
        except Exception as e:
            print(f"[Server] Error: {e}")
        
        finally:
            self.is_processing = False
    
    def _on_status_received(self, status):
        print(f"[Server] Device status: {status}")
    
    def start(self):
        print("=" * 50)
        print("  AI Figurine Server")
        print("=" * 50)
        print()
        
        if not self.mqtt.connect():
            print("Failed to connect to MQTT broker")
            return False
        
        print("[Server] Server started. Waiting for audio...")
        print("[Server] Press Ctrl+C to stop")
        
        return True
    
    def stop(self):
        print("\n[Server] Stopping...")
        self.mqtt.disconnect()
        print("[Server] Stopped")
    
    def run(self):
        if not self.start():
            return
        
        def signal_handler(sig, frame):
            self.stop()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

if __name__ == '__main__':
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    server = FigurineServer(config_path)
    server.run()
