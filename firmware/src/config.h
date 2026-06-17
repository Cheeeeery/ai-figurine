#ifndef CONFIG_H
#define CONFIG_H

#define WIFI_SSID "YourWiFiSSID"
#define WIFI_PASSWORD "YourWiFiPassword"

// MQTT服务器配置
// 方式1：使用本地MQTT Broker
#define MQTT_BROKER "your-server-ip"
#define MQTT_PORT 1883
#define MQTT_USERNAME "figurine"
#define MQTT_PASSWORD "figurine123"
#define MQTT_CLIENT_ID "figurine_device"

// 方式2：使用阿里云物联网平台（取消注释并填入设备信息）
// #define MQTT_BROKER "${productKey}.iot-as-mqtt.${region}.aliyuncs.com"
// #define MQTT_PORT 1883
// #define MQTT_USERNAME "${deviceName}&${productKey}"
// #define MQTT_PASSWORD "使用阿里云签名工具生成"
// #define MQTT_CLIENT_ID "${deviceName}|securemode=2,signmethod=hmacsha256|"

// MQTT主题配置
// 方式1：使用本地MQTT Broker
#define TOPIC_AUDIO_IN "figurine/audio/in"
#define TOPIC_AUDIO_OUT "figurine/audio/out"
#define TOPIC_STATUS "figurine/status"
#define TOPIC_COMMAND "figurine/command"

// 方式2：使用阿里云物联网平台（取消注释并修改设备信息）
// #define TOPIC_AUDIO_IN "/${productKey}/${deviceName}/user/audio/in"
// #define TOPIC_AUDIO_OUT "/${productKey}/${deviceName}/user/audio/out"
// #define TOPIC_STATUS "/${productKey}/${deviceName}/user/status"
// #define TOPIC_COMMAND "/${productKey}/${deviceName}/user/command"

#define MIC_I2S_BCK 4
#define MIC_I2S_WS 5
#define MIC_I2S_SD 6

#define AMP_I2S_BCK 15
#define AMP_I2S_WS 16
#define AMP_I2S_SD 17

#define TOUCH_PIN 7

#define LED_LEFT_PIN 48
#define LED_RIGHT_PIN 21
#define NUM_LEDS 2

#define SAMPLE_RATE 16000
#define AUDIO_BUFFER_SIZE 4096
#define CHUNK_SIZE 4096

#define STATE_IDLE 0
#define STATE_LISTENING 1
#define STATE_WAITING 2
#define STATE_SPEAKING 3

#endif
