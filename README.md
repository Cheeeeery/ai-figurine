# 「她」AI 陪伴智能手办

## 项目结构

```
ai-figurine/
├── firmware/           # ESP32固件代码
│   └── src/
│       ├── main.cpp    # 主程序
│       └── config.h    # 引脚和配置
├── server/             # 云端Python服务
│   ├── main.py         # 服务主入口
│   ├── mqtt_handler.py # MQTT通信
│   ├── asr_engine.py   # 语音识别
│   ├── llm_engine.py   # AI对话
│   ├── tts_engine.py   # 语音合成
│   └── config.yaml     # 服务配置
├── prompt/             # AI人格配置
│   ├── system.txt      # System Prompt
│   └── memories.json   # 共同记忆
├── tests/              # 测试脚本
└── broker.yaml         # MQTT Broker配置
```

## 快速开始

### 1. 安装依赖

```bash
pip install paho-mqtt pyyaml edge-tts
```

### 2. 配置

编辑 `server/config.yaml`，填入：
- DeepSeek API Key（用于AI对话）
- WiFi名称和密码（用于ESP32）
- 阿里云物联网平台配置（可选，如果使用阿里云IoT）

### 阿里云物联网平台配置（可选）

如果要使用阿里云物联网平台，需要：

1. 在阿里云物联网平台控制台创建产品和设备
2. 获取设备三元组：ProductKey、DeviceName、DeviceSecret
3. 编辑 `server/config.yaml`，在 `mqtt.aliyun_iot` 部分填入：
   - `enabled: true`
   - `product_key`: 你的ProductKey
   - `device_name`: 你的DeviceName
   - `device_secret`: 你的DeviceSecret
   - `region`: 阿里云区域（默认cn-shanghai）

4. 修改ESP32固件配置：
   - 编辑 `firmware/src/config.h`
   - 修改MQTT_BROKER为：`${productKey}.iot-as-mqtt.${region}.aliyuncs.com`
   - 修改MQTT_PORT为：1883
   - 修改MQTT_USERNAME为：`${deviceName}&${productKey}`
   - 修改MQTT_PASSWORD为：使用阿里云提供的签名工具生成
   - 修改MQTT_CLIENT_ID为：`${deviceName}|securemode=2,signmethod=hmacsha256|`
   - 修改TOPIC格式为：`/${productKey}/${deviceName}/user/自定义topic`

### 3. 启动MQTT Broker

```bash
# 方式1: 使用Mosquitto
mosquitto -d

# 方式2: 使用Python amqtt
pip install amqtt
amqtt -c broker.yaml
```

### 4. 启动服务

```bash
cd server
python main.py
```

### 5. 测试

```bash
python tests/test_mock_device.py
```

## ESP32固件

使用Arduino IDE 2编译上传：
1. 安装ESP32板支持包
2. 安装依赖库：PubSubClient, FastLED
3. 修改 `firmware/src/config.h` 中的WiFi和服务器配置
4. 选择板子：ESP32-S3 DevKitC
5. 上传代码

## 硬件连接

| 功能 | GPIO |
|------|------|
| 麦克风 BCK | GPIO4 |
| 麦克风 WS | GPIO5 |
| 麦克风 SD | GPIO6 |
| 功放 BCK | GPIO15 |
| 功放 WS | GPIO16 |
| 功放 SD | GPIO17 |
| 触摸传感器 | GPIO7 |
| 左眼LED | GPIO48 |
| 右眼LED | GPIO21 |

## 部署到云服务器

1. 将 `server/` 和 `prompt/` 目录上传到云服务器
2. 安装Mosquitto并配置认证
3. 运行 `python main.py`
4. 修改ESP32固件中的服务器地址
