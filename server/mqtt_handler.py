import paho.mqtt.client as mqtt
import json
import time
import os
import hmac
import hashlib
import secrets

class MQTTHandler:
    def __init__(self, config):
        self.config = config
        self.aliyun_iot = config.get('aliyun_iot', {})
        
        # 根据配置选择连接方式
        if self.aliyun_iot.get('enabled', False):
            self._setup_aliyun_iot()
        else:
            self.client = mqtt.Client(client_id=config['client_id'])
            if config.get('username'):
                self.client.username_pw_set(config['username'], config['password'])
        
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        
        self.audio_callback = None
        self.status_callback = None
        
        self.connected = False
        self._audio_buffer = bytearray()
        self._receiving_audio = False
    
    def _setup_aliyun_iot(self):
        """设置阿里云物联网平台连接参数"""
        product_key = self.aliyun_iot['product_key']
        device_name = self.aliyun_iot['device_name']
        device_secret = self.aliyun_iot['device_secret']
        region = self.aliyun_iot.get('region', 'cn-shanghai')
        
        # 生成broker地址
        broker = f"{product_key}.iot-as-mqtt.{region}.aliyuncs.com"
        
        # 生成client_id（格式：clientId|securemode=2,signmethod=hmacsha256|）
        client_id = f"{device_name}|securemode=2,signmethod=hmacsha256|"
        
        # 生成username（格式：deviceName&productKey）
        username = f"{device_name}&{product_key}"
        
        # 生成password（使用HMAC-SHA256签名）
        timestamp = str(int(time.time() * 1000))
        sign_content = f"clientId{device_name}deviceName{device_name}productKey{product_key}timestamp{timestamp}"
        password = hmac.new(
            device_secret.encode(),
            sign_content.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # 创建MQTT客户端
        self.client = mqtt.Client(client_id=client_id)
        self.client.username_pw_set(username, password)
        
        # 保存broker地址和端口
        self.config['broker'] = broker
        self.config['port'] = 1883
        
        # 修改topic格式为阿里云格式
        if 'topics' not in self.config:
            self.config['topics'] = {}
        
        self.config['topics']['audio_in'] = f"/{product_key}/{device_name}/user/audio/in"
        self.config['topics']['audio_out'] = f"/{product_key}/{device_name}/user/audio/out"
        self.config['topics']['status'] = f"/{product_key}/{device_name}/user/status"
        self.config['topics']['command'] = f"/{product_key}/{device_name}/user/command"
        
        print(f"[MQTT] Configured for Aliyun IoT: {broker}")
    
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            print(f"[MQTT] Connected to broker")
            client.subscribe(self.config['topics']['audio_in'])
            client.subscribe(self.config['topics']['status'])
        else:
            print(f"[MQTT] Connection failed: {rc}")
    
    def on_disconnect(self, client, userdata, rc):
        self.connected = False
        print(f"[MQTT] Disconnected: {rc}")
    
    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload
        
        if topic == self.config['topics']['audio_in']:
            self._handle_audio_message(payload)
        elif topic == self.config['topics']['status']:
            self._handle_status_message(payload)
    
    def _handle_audio_message(self, payload):
        if payload == b'END':
            if self._receiving_audio and self.audio_callback:
                audio_data = bytes(self._audio_buffer)
                self.audio_callback(audio_data)
            self._audio_buffer = bytearray()
            self._receiving_audio = False
        else:
            self._receiving_audio = True
            self._audio_buffer.extend(payload)
    
    def _handle_status_message(self, payload):
        try:
            status = json.loads(payload.decode())
            if self.status_callback:
                self.status_callback(status)
        except:
            pass
    
    def connect(self):
        try:
            self.client.connect(
                self.config['broker'],
                self.config['port'],
                keepalive=60
            )
            self.client.loop_start()
            return True
        except Exception as e:
            print(f"[MQTT] Connection error: {e}")
            return False
    
    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
    
    def publish_audio(self, audio_data):
        topic = self.config['topics']['audio_out']
        chunk_size = self.config.get('chunk_size', 4096)
        
        for i in range(0, len(audio_data), chunk_size):
            chunk = audio_data[i:i+chunk_size]
            self.client.publish(topic, chunk, qos=0)
        
        self.client.publish(topic, b'END', qos=1)
    
    def publish_status(self, status):
        topic = self.config['topics']['status']
        self.client.publish(topic, json.dumps(status), qos=1)
    
    def publish_command(self, command):
        topic = self.config['topics']['command']
        self.client.publish(topic, json.dumps(command), qos=1)
    
    def set_audio_callback(self, callback):
        self.audio_callback = callback
    
    def set_status_callback(self, callback):
        self.status_callback = callback
