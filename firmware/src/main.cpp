#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <driver/i2s.h>
#include <FastLED.h>
#include <ArduinoJson.h>

#include "config.h"

WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);

CRGB leds[NUM_LEDS];

uint8_t currentState = STATE_IDLE;
bool touchPressed = false;
unsigned long lastTouchTime = 0;

int16_t* audioBuffer = nullptr;
size_t audioBufferIndex = 0;
bool isRecording = false;

int16_t* playbackBuffer = nullptr;
size_t playbackSize = 0;
size_t playbackIndex = 0;
bool isPlaying = false;

unsigned long breathingStart = 0;
int breathingBrightness = 0;

void setupWiFi() {
    Serial.print("Connecting to WiFi...");
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    
    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED && attempts < 20) {
        delay(500);
        Serial.print(".");
        attempts++;
    }
    
    if (WiFi.status() == WL_CONNECTED) {
        Serial.println(" connected!");
        Serial.print("IP: ");
        Serial.println(WiFi.localIP());
    } else {
        Serial.println(" failed!");
    }
}

void setupMQTT() {
    mqtt.setServer(MQTT_BROKER, MQTT_PORT);
    mqtt.setCallback(mqttCallback);
    mqtt.setBufferSize(8192);
}

void mqttCallback(char* topic, byte* payload, unsigned int length) {
    if (strcmp(topic, TOPIC_AUDIO_OUT) == 0) {
        if (length == 3 && memcmp(payload, "END", 3) == 0) {
            if (playbackIndex > 0) {
                currentState = STATE_SPEAKING;
                playbackIndex = 0;
                isPlaying = true;
            }
        } else {
            if (playbackBuffer == nullptr) {
                playbackBuffer = (int16_t*)ps_malloc(AUDIO_BUFFER_SIZE * 100);
            }
            if (playbackBuffer && playbackIndex + length <= AUDIO_BUFFER_SIZE * 100) {
                memcpy(playbackBuffer + playbackIndex / 2, payload, length);
                playbackIndex += length;
            }
        }
    } else if (strcmp(topic, TOPIC_COMMAND) == 0) {
        StaticJsonDocument<256> doc;
        if (deserializeJson(doc, payload, length) == DeserializationOk) {
            const char* cmd = doc["command"];
            if (cmd && strcmp(cmd, "greeting") == 0) {
                currentState = STATE_SPEAKING;
            }
        }
    }
}

void reconnectMQTT() {
    if (!mqtt.connected()) {
        Serial.print("Connecting to MQTT...");
        if (mqtt.connect(MQTT_CLIENT_ID, MQTT_USERNAME, MQTT_PASSWORD)) {
            Serial.println(" connected!");
            mqtt.subscribe(TOPIC_AUDIO_OUT);
            mqtt.subscribe(TOPIC_COMMAND);
            
            publishStatus("idle");
        } else {
            Serial.println(" failed!");
        }
    }
}

void setupI2SMic() {
    i2s_config_t i2s_config = {
        .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
        .sample_rate = SAMPLE_RATE,
        .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
        .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
        .communication_format = I2S_COMM_FORMAT_STAND_I2S,
        .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
        .dma_buf_count = 8,
        .dma_buf_len = 1024,
        .use_apll = false,
        .tx_desc_auto_clear = false,
        .fixed_mclk = 0
    };
    
    i2s_pin_config_t pin_config = {
        .bck_io_num = MIC_I2S_BCK,
        .ws_io_num = MIC_I2S_WS,
        .data_out_num = I2S_PIN_NO_CHANGE,
        .data_in_num = MIC_I2S_SD
    };
    
    i2s_driver_install(I2S_NUM_0, &i2s_config, 0, NULL);
    i2s_set_pin(I2S_NUM_0, &pin_config);
}

void setupI2SAmp() {
    i2s_config_t i2s_config = {
        .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_TX),
        .sample_rate = SAMPLE_RATE,
        .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
        .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
        .communication_format = I2S_COMM_FORMAT_STAND_I2S,
        .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
        .dma_buf_count = 8,
        .dma_buf_len = 1024,
        .use_apll = false,
        .tx_desc_auto_clear = true,
        .fixed_mclk = 0
    };
    
    i2s_pin_config_t pin_config = {
        .bck_io_num = AMP_I2S_BCK,
        .ws_io_num = AMP_I2S_WS,
        .data_out_num = AMP_I2S_SD,
        .data_in_num = I2S_PIN_NO_CHANGE
    };
    
    i2s_driver_install(I2S_NUM_1, &i2s_config, 0, NULL);
    i2s_set_pin(I2S_NUM_1, &pin_config);
}

void setupLEDs() {
    FastLED.addLeds<WS2812B, LED_LEFT_PIN, GRB>(leds, NUM_LEDS);
    FastLED.setBrightness(50);
    leds[0] = CRGB::WarmWhite;
    leds[1] = CRGB::WarmWhite;
    FastLED.show();
}

void updateLEDs() {
    switch (currentState) {
        case STATE_IDLE: {
            breathingBrightness = (sin((millis() - breathingStart) / 1000.0 * PI) + 1) * 30 + 20;
            FastLED.setBrightness(breathingBrightness);
            leds[0] = CRGB(255, 200, 150);
            leds[1] = CRGB(255, 200, 150);
            break;
        }
        case STATE_LISTENING:
            FastLED.setBrightness(80);
            leds[0] = CRGB(0, 100, 255);
            leds[1] = CRGB(0, 100, 255);
            break;
        case STATE_WAITING: {
            int brightness = (sin(millis() / 200.0 * PI) + 1) * 40 + 20;
            FastLED.setBrightness(brightness);
            leds[0] = CRGB(255, 200, 0);
            leds[1] = CRGB(255, 200, 0);
            break;
        }
        case STATE_SPEAKING: {
            int16_t sample = 0;
            if (isPlaying && playbackBuffer) {
                sample = abs(playbackBuffer[playbackIndex / 2]);
            }
            int brightness = map(sample, 0, 16000, 30, 100);
            FastLED.setBrightness(constrain(brightness, 30, 100));
            leds[0] = CRGB(255, 150, 0);
            leds[1] = CRGB(255, 150, 0);
            break;
        }
    }
    FastLED.show();
}

void publishStatus(const char* state) {
    StaticJsonDocument<128> doc;
    doc["device"] = "figurine";
    doc["state"] = state;
    doc["battery"] = 85;
    doc["rssi"] = WiFi.RSSI();
    doc["uptime"] = millis() / 1000;
    
    char buffer[128];
    serializeJson(doc, buffer);
    mqtt.publish(TOPIC_STATUS, buffer);
}

void startRecording() {
    if (audioBuffer == nullptr) {
        audioBuffer = (int16_t*)ps_malloc(AUDIO_BUFFER_SIZE * 20);
    }
    audioBufferIndex = 0;
    isRecording = true;
    currentState = STATE_LISTENING;
    publishStatus("listening");
}

void stopRecording() {
    isRecording = false;
    currentState = STATE_WAITING;
    publishStatus("waiting");
    
    if (audioBuffer && audioBufferIndex > 0) {
        uint8_t* data = (uint8_t*)audioBuffer;
        for (size_t i = 0; i < audioBufferIndex * 2; i += CHUNK_SIZE) {
            size_t chunkLen = min((size_t)CHUNK_SIZE, audioBufferIndex * 2 - i);
            mqtt.publish(TOPIC_AUDIO_IN, data + i, chunkLen);
        }
        mqtt.publish(TOPIC_AUDIO_IN, (uint8_t*)"END", 3);
    }
}

void readTouch() {
    bool currentTouch = digitalRead(TOUCH_PIN) == HIGH;
    
    if (currentTouch && !touchPressed) {
        touchPressed = true;
        lastTouchTime = millis();
        
        if (currentState == STATE_IDLE) {
            startRecording();
        }
    } else if (!currentTouch && touchPressed) {
        touchPressed = false;
        
        if (currentState == STATE_LISTENING) {
            stopRecording();
        }
    }
}

void readMicrophone() {
    if (!isRecording || audioBuffer == nullptr) return;
    
    size_t bytesRead;
    i2s_read(I2S_NUM_0, audioBuffer + audioBufferIndex, 
             AUDIO_BUFFER_SIZE * 2 - audioBufferIndex * 2, 
             &bytesRead, portMAX_DELAY);
    
    audioBufferIndex += bytesRead / 2;
}

void playAudio() {
    if (!isPlaying || playbackBuffer == nullptr) return;
    
    if (playbackIndex >= playbackSize) {
        isPlaying = false;
        currentState = STATE_IDLE;
        publishStatus("idle");
        return;
    }
    
    size_t bytesToWrite = min((size_t)4096, playbackSize - playbackIndex);
    size_t bytesWritten;
    
    i2s_write(I2S_NUM_1, playbackBuffer + playbackIndex / 2, 
              bytesToWrite, &bytesWritten, portMAX_DELAY);
    
    playbackIndex += bytesWritten;
}

void setup() {
    Serial.begin(115200);
    Serial.println("\n=== AI Figurine Starting ===\n");
    
    pinMode(TOUCH_PIN, INPUT);
    
    setupLEDs();
    setupI2SMic();
    setupI2SAmp();
    
    setupWiFi();
    setupMQTT();
    
    breathingStart = millis();
    
    Serial.println("Ready!");
}

void loop() {
    if (WiFi.status() != WL_CONNECTED) {
        setupWiFi();
    }
    
    if (!mqtt.connected()) {
        reconnectMQTT();
    }
    
    mqtt.loop();
    
    readTouch();
    readMicrophone();
    playAudio();
    updateLEDs();
    
    delay(10);
}
