#!/usr/bin/env python3
"""
Generate EasyEDA (嘉立创EDA) standard schematic JSON for AI Figurine project.
Run this script to generate the .json schematic file that can be opened in LCEDA.
"""

import json
import time
import os

def gen_id():
    gen_id.counter = getattr(gen_id, 'counter', 1000000) + 1
    return str(gen_id.counter)

def make_shape(shape_str):
    return shape_str

def create_schematic():
    shapes = []
    
    # Grid spacing: 10mil = 2.54mm
    G = 10  # grid unit in mils (EasyEDA uses mil)
    D = 254  # 10mil in 0.01mm = 254
    
    # ===================== TITLE BLOCK =====================
    shapes.append(f"TITLE~0~0~0~0~0~0~0~0~0~AI Figurine Schematic~2026-06-16~v2.0~~~")
    
    # ===================== SECTION BOXES =====================
    # Power supply section box
    shapes.append(f"RECT~800~2000~2800~4500~0~#808080~1~none~~{gen_id()}")
    shapes.append(f"TEXT~1000~1900~0~8~0~0~0~1~0~Power Supply~#000000")
    
    # MCU section box
    shapes.append(f"RECT~3200~1500~6800~5000~0~#808080~1~none~~{gen_id()}")
    shapes.append(f"TEXT~3400~1400~0~8~0~0~0~1~0~MCU (ESP32-S3)~#000000")
    
    # Audio input section
    shapes.append(f"RECT~7200~1500~9500~3500~0~#808080~1~none~~{gen_id()}")
    shapes.append(f"TEXT~7400~1400~0~8~0~0~0~1~0~Microphone (INMP441)~#000000")
    
    # Audio output section
    shapes.append(f"RECT~7200~3800~9500~5500~0~#808080~1~none~~{gen_id()}")
    shapes.append(f"TEXT~7400~3700~0~8~0~0~0~1~0~Amplifier (MAX98357A)~#000000")
    
    # LED section
    shapes.append(f"RECT~7200~5800~9500~7500~0~#808080~1~none~~{gen_id()}")
    shapes.append(f"TEXT~7400~5700~0~8~0~0~0~1~0~LEDs (WS2812B)~#000000")
    
    # Touch section
    shapes.append(f"RECT~7200~7800~9500~9200~0~#808080~1~none~~{gen_id()}")
    shapes.append(f"TEXT~7400~7700~0~8~0~0~0~1~0~Touch Sensor (TTP223)~#000000")
    
    # ===================== POWER SECTION =====================
    # --- USB Type-C Connector J1 ---
    # VBUS pin
    shapes.append(f"TEXT~1100~2300~0~6~1~0~0~1~0~J1 USB Type-C~#000080")
    shapes.append(f"TEXT~1100~2500~0~5~1~0~0~1~0~Pin A4/B4: VBUS (+5V)~#000000")
    shapes.append(f"TEXT~1100~2700~0~5~1~0~0~1~0~Pin A1/B1: GND~#000000")
    shapes.append(f"TEXT~1100~2900~0~5~1~0~0~1~0~CC1->GND (Rd 5.1K)~#000000")
    shapes.append(f"TEXT~1100~3100~0~5~1~0~0~1~0~CC2->GND (Rd 5.1K)~#000000")
    
    # +5V power symbol
    shapes.append(f"PS~1600~2300~0~#000000~{gen_id()}~+5V~5V")
    # GND symbol  
    shapes.append(f"PS~1600~3400~180~#000000~{gen_id()}~GND~GND")
    
    # --- AMS1117-3.3 LDO U4 ---
    shapes.append(f"TEXT~1100~3600~0~6~1~0~0~1~0~U4 AMS1117-3.3~#000080")
    shapes.append(f"TEXT~1100~3800~0~5~1~0~0~1~0~Pin1: IN (+5V)~#000000")
    shapes.append(f"TEXT~1100~4000~0~5~1~0~0~1~0~Pin2: GND~#000000")
    shapes.append(f"TEXT~1100~4200~0~5~1~0~0~1~0~Pin3: OUT (+3.3V)~#000000")
    
    # +3.3V power symbol
    shapes.append(f"PS~1600~4400~0~#000000~{gen_id()}~+3V3~3.3V")
    
    # C5 10uF input cap
    shapes.append(f"TEXT~2200~3700~0~5~1~0~0~1~0~C5: 10uF (Input)~#008000")
    # C6 10uF output cap
    shapes.append(f"TEXT~2200~4300~0~5~1~0~0~1~0~C6: 10uF (Output)~#008000")
    
    # ===================== MCU SECTION =====================
    # ESP32-S3 Module
    shapes.append(f"TEXT~3600~1800~0~6~1~0~0~1~0~U1: ESP32-S3 DevKitC~#000080")
    shapes.append(f"TEXT~3600~2000~0~5~0~0~0~1~0~Pin1: 3V3 <-- +3V3~#000000")
    shapes.append(f"TEXT~3600~2200~0~5~0~0~0~1~0~Pin2: EN <-- R1(10K) to 3V3~#000000")
    shapes.append(f"TEXT~3600~2400~0~5~0~0~0~1~0~Pin7: IO4  --> MIC_BCK~#FF0000")
    shapes.append(f"TEXT~3600~2600~0~5~0~0~0~1~0~Pin8: IO5  --> MIC_WS~#FF0000")
    shapes.append(f"TEXT~3600~2800~0~5~0~0~0~1~0~Pin9: IO6  <-- MIC_SD~#FF0000")
    shapes.append(f"TEXT~3600~3000~0~5~0~0~0~1~0~Pin10: IO7 <-- TOUCH~#FF0000")
    shapes.append(f"TEXT~3600~3200~0~5~0~0~0~1~0~Pin18: IO15 --> AMP_BCK~#FF0000")
    shapes.append(f"TEXT~3600~3400~0~5~0~0~0~1~0~Pin19: IO16 --> AMP_WS~#FF0000")
    shapes.append(f"TEXT~3600~3600~0~5~0~0~0~1~0~Pin20: IO17 --> AMP_SD~#FF0000")
    shapes.append(f"TEXT~3600~3800~0~5~0~0~0~1~0~Pin24: IO21 --> LED_R DIN~#FF0000")
    shapes.append(f"TEXT~3600~4000~0~5~0~0~0~1~0~Pin28: IO48 --> LED_L DIN~#FF0000")
    shapes.append(f"TEXT~3600~4200~0~5~0~0~0~1~0~GND pins --> GND~#000000")
    shapes.append(f"TEXT~3600~4400~0~5~0~0~0~1~0~C1: 100nF on 3V3~#008000")
    shapes.append(f"TEXT~3600~4600~0~5~0~0~0~1~0~C2: 100nF on 3V3~#008000")
    
    # Net labels for MCU signals
    shapes.append(f"NL~6000~2400~0~#FF0000~0~{gen_id()}~MIC_BCK")
    shapes.append(f"NL~6000~2600~0~#FF0000~0~{gen_id()}~MIC_WS")
    shapes.append(f"NL~6000~2800~0~#FF0000~0~{gen_id()}~MIC_SD")
    shapes.append(f"NL~6000~3000~0~#FF0000~0~{gen_id()}~TOUCH")
    shapes.append(f"NL~6000~3200~0~#FF0000~0~{gen_id()}~AMP_BCK")
    shapes.append(f"NL~6000~3400~0~#FF0000~0~{gen_id()}~AMP_WS")
    shapes.append(f"NL~6000~3600~0~#FF0000~0~{gen_id()}~AMP_SD")
    shapes.append(f"NL~6000~3800~0~#FF0000~0~{gen_id()}~LED_R")
    shapes.append(f"NL~6000~4000~0~#FF0000~0~{gen_id()}~LED_L")
    
    # Power labels
    shapes.append(f"PL~6000~2000~0~#000000~{gen_id()}~+3V3~3.3V")
    shapes.append(f"PL~6000~4200~180~#000000~{gen_id()}~GND~GND")
    
    # ===================== INMP441 MICROPHONE =====================
    shapes.append(f"TEXT~7600~1700~0~6~1~0~0~1~0~U2: INMP441~#000080")
    shapes.append(f"TEXT~7600~1900~0~5~0~0~0~1~0~Pin1: VDD <-- +3V3~#000000")
    shapes.append(f"TEXT~7600~2100~0~5~0~0~0~1~0~Pin2: GND --> GND~#000000")
    shapes.append(f"TEXT~7600~2300~0~5~0~0~0~1~0~Pin3: WS  <-- MIC_WS~#FF0000")
    shapes.append(f"TEXT~7600~2500~0~5~0~0~0~1~0~Pin4: SCK <-- MIC_BCK~#FF0000")
    shapes.append(f"TEXT~7600~2700~0~5~0~0~0~1~0~Pin5: SD  --> MIC_SD~#FF0000")
    shapes.append(f"TEXT~7600~2900~0~5~0~0~0~1~0~Pin6: L/R --> GND (Left)~#000000")
    shapes.append(f"TEXT~7600~3100~0~5~0~0~0~1~0~C3: 100nF on VDD~#008000")
    
    # Net labels for INMP441
    shapes.append(f"NL~9000~2300~180~#FF0000~0~{gen_id()}~MIC_WS")
    shapes.append(f"NL~9000~2500~180~#FF0000~0~{gen_id()}~MIC_BCK")
    shapes.append(f"NL~9000~2700~180~#FF0000~0~{gen_id()}~MIC_SD")
    
    # ===================== MAX98357A AMPLIFIER =====================
    shapes.append(f"TEXT~7600~4000~0~6~1~0~0~1~0~U3: MAX98357A~#000080")
    shapes.append(f"TEXT~7600~4200~0~5~0~0~0~1~0~Pin1: VIN <-- +5V~#000000")
    shapes.append(f"TEXT~7600~4400~0~5~0~0~0~1~0~Pin2: DIN <-- AMP_SD~#FF0000")
    shapes.append(f"TEXT~7600~4600~0~5~0~0~0~1~0~Pin3: BCLK <-- AMP_BCK~#FF0000")
    shapes.append(f"TEXT~7600~4800~0~5~0~0~0~1~0~Pin4: LRC <-- AMP_WS~#FF0000")
    shapes.append(f"TEXT~7600~5000~0~5~0~0~0~1~0~Pin5: GND --> GND~#000000")
    shapes.append(f"TEXT~7600~5200~0~5~0~0~0~1~0~Pin7: OUT+ --> J2 SPK+~#008000")
    shapes.append(f"TEXT~7600~5400~0~5~0~0~0~1~0~Pin8: OUT- --> J2 SPK-~#008000")
    
    # Net labels for MAX98357A
    shapes.append(f"NL~9000~4400~180~#FF0000~0~{gen_id()}~AMP_SD")
    shapes.append(f"NL~9000~4600~180~#FF0000~0~{gen_id()}~AMP_BCK")
    shapes.append(f"NL~9000~4800~180~#FF0000~0~{gen_id()}~AMP_WS")
    
    # Speaker connector
    shapes.append(f"TEXT~7600~5600~0~5~1~0~0~1~0~J2: Speaker Connector (2pin)~#008000")
    shapes.append(f"TEXT~7600~5800~0~5~0~0~0~1~0~Pin1: SPK+ <-- AMP OUT+~#008000")
    shapes.append(f"TEXT~7600~6000~0~5~0~0~0~1~0~Pin2: SPK- <-- AMP OUT-~#008000")
    
    # ===================== WS2812B LEDs =====================
    shapes.append(f"TEXT~7600~6200~0~6~1~0~0~1~0~D1: WS2812B (Left Eye)~#000080")
    shapes.append(f"TEXT~7600~6400~0~5~0~0~0~1~0~Pin1: VDD <-- +5V~#000000")
    shapes.append(f"TEXT~7600~6600~0~5~0~0~0~1~0~Pin2: DIN <-- LED_L (GPIO48)~#FF0000")
    shapes.append(f"TEXT~7600~6800~0~5~0~0~0~1~0~Pin3: DOUT --> D2 DIN~#FF0000")
    shapes.append(f"TEXT~7600~7000~0~5~0~0~0~1~0~Pin4: VSS --> GND~#000000")
    
    shapes.append(f"TEXT~7600~7200~0~6~1~0~0~1~0~D2: WS2812B (Right Eye)~#000080")
    shapes.append(f"TEXT~7600~7400~0~5~0~0~0~1~0~Pin1: VDD <-- +5V~#000000")
    shapes.append(f"TEXT~7600~7600~0~5~0~0~0~1~0~Pin2: DIN <-- D1 DOUT~#FF0000")
    shapes.append(f"TEXT~7600~7800~0~5~0~0~0~1~0~Pin3: DOUT --> NC~#000000")
    shapes.append(f"TEXT~7600~8000~0~5~0~0~0~1~0~Pin4: VSS --> GND~#000000")
    
    # LED power label
    shapes.append(f"PL~9000~6400~0~#000000~{gen_id()}~+5V~5V")
    
    # ===================== TTP223 TOUCH SENSOR =====================
    shapes.append(f"TEXT~7600~8200~0~6~1~0~0~1~0~S1: TTP223 Touch Sensor~#000080")
    shapes.append(f"TEXT~7600~8400~0~5~0~0~0~1~0~Pin1: VCC <-- +3V3~#000000")
    shapes.append(f"TEXT~7600~8600~0~5~0~0~0~1~0~Pin2: I/O --> TOUCH (GPIO7)~#FF0000")
    shapes.append(f"TEXT~7600~8800~0~5~0~0~0~1~0~Pin3: GND --> GND~#000000")
    
    # Net label for touch
    shapes.append(f"NL~9000~8600~180~#FF0000~0~{gen_id()}~TOUCH")
    
    # ===================== DECOUPLING CAPS NOTE =====================
    shapes.append(f"TEXT~3600~4800~0~6~1~0~0~1~0~Decoupling Capacitors:~#008000")
    shapes.append(f"TEXT~3600~5000~0~5~0~0~0~1~0~C1: 100nF (ESP32 3V3 pin)~#008000")
    shapes.append(f"TEXT~3600~5200~0~5~0~0~0~1~0~C2: 100nF (ESP32 3V3 pin)~#008000")
    shapes.append(f"TEXT~3600~5400~0~5~0~0~0~1~0~C3: 100nF (INMP441 VDD)~#008000")
    shapes.append(f"TEXT~3600~5600~0~5~0~0~0~1~0~C4: 100nF (MAX98357A VIN)~#008000")
    shapes.append(f"TEXT~3600~5800~0~5~0~0~0~1~0~C5: 10uF (AMS1117 Input)~#008000")
    shapes.append(f"TEXT~3600~6000~0~5~0~0~0~1~0~C6: 10uF (AMS1117 Output)~#008000")
    
    shapes.append(f"TEXT~3600~6300~0~6~1~0~0~1~0~Resistors:~#008000")
    shapes.append(f"TEXT~3600~6500~0~5~0~0~0~1~0~R1: 10K (EN pull-up to 3V3)~#008000")
    shapes.append(f"TEXT~3600~6700~0~5~0~0~0~1~0~R2: 1K (Data line protection, optional)~#008000")
    
    # ===================== POWER DISTRIBUTION =====================
    shapes.append(f"TEXT~800~4800~0~6~1~0~0~1~0~Power Distribution:~#000080")
    shapes.append(f"TEXT~800~5000~0~5~0~0~0~1~0~+5V  --> USB VBUS, MAX98357A VIN, WS2812B VDD~#000000")
    shapes.append(f"TEXT~800~5200~0~5~0~0~0~1~0~+3V3 --> ESP32 3V3, INMP441 VDD, TTP223 VCC~#000000")
    shapes.append(f"TEXT~800~5400~0~5~0~0~0~1~0~GND  --> All GND pins connected~#000000")
    
    # ===================== BOM SUMMARY =====================
    shapes.append(f"TEXT~800~5800~0~6~1~0~0~1~0~Bill of Materials:~#000080")
    shapes.append(f"TEXT~800~6000~0~5~0~0~0~1~0~U1: ESP32-S3 DevKitC x1~#000000")
    shapes.append(f"TEXT~800~6200~0~5~0~0~0~1~0~U2: INMP441 I2S Microphone x1~#000000")
    shapes.append(f"TEXT~800~6400~0~5~0~0~0~1~0~U3: MAX98357A I2S Amplifier x1~#000000")
    shapes.append(f"TEXT~800~6600~0~5~0~0~0~1~0~U4: AMS1117-3.3 LDO x1~#000000")
    shapes.append(f"TEXT~800~6800~0~5~0~0~0~1~0~D1,D2: WS2812B RGB LED x2~#000000")
    shapes.append(f"TEXT~800~7000~0~5~0~0~0~1~0~S1: TTP223 Touch Sensor Module x1~#000000")
    shapes.append(f"TEXT~800~7200~0~5~0~0~0~1~0~J1: USB Type-C Connector x1~#000000")
    shapes.append(f"TEXT~800~7400~0~5~0~0~0~1~0~J2: Speaker Connector 2pin x1~#000000")
    shapes.append(f"TEXT~800~7600~0~5~0~0~0~1~0~C1-C4: 100nF MLCC x4~#000000")
    shapes.append(f"TEXT~800~7800~0~5~0~0~0~1~0~C5-C6: 10uF MLCC x2~#000000")
    shapes.append(f"TEXT~800~8000~0~5~0~0~0~1~0~R1: 10K resistor x1~#000000")
    shapes.append(f"TEXT~800~8200~0~5~0~0~0~1~0~R2: 1K resistor x1 (optional)~#000000")
    
    # ===================== NET LABELS SUMMARY =====================
    shapes.append(f"TEXT~800~8600~0~6~1~0~0~1~0~Signal Net Summary:~#000080")
    shapes.append(f"TEXT~800~8800~0~5~0~0~0~1~0~MIC_BCK:  GPIO4  <-> INMP441 SCK~#FF0000")
    shapes.append(f"TEXT~800~9000~0~5~0~0~0~1~0~MIC_WS:   GPIO5  <-> INMP441 WS~#FF0000")
    shapes.append(f"TEXT~800~9200~0~5~0~0~0~1~0~MIC_SD:   GPIO6  <-> INMP441 SD~#FF0000")
    shapes.append(f"TEXT~800~9400~0~5~0~0~0~1~0~AMP_BCK:  GPIO15 <-> MAX98357A BCLK~#FF0000")
    shapes.append(f"TEXT~800~9600~0~5~0~0~0~1~0~AMP_WS:   GPIO16 <-> MAX98357A LRC~#FF0000")
    shapes.append(f"TEXT~800~9800~0~5~0~0~0~1~0~AMP_SD:   GPIO17 <-> MAX98357A DIN~#FF0000")
    shapes.append(f"TEXT~800~10000~0~5~0~0~0~1~0~TOUCH:    GPIO7  <-> TTP223 I/O~#FF0000")
    shapes.append(f"TEXT~800~10200~0~5~0~0~0~1~0~LED_L:    GPIO48 <-> D1 DIN (WS2812B)~#FF0000")
    shapes.append(f"TEXT~800~10400~0~5~0~0~0~1~0~LED_R:    GPIO21 <-> D2 DIN (via D1 DOUT)~#FF0000")
    
    # Build the EasyEDA JSON
    schematic = {
        "head": {
            "docType": "1",
            "editorVersion": "6.5.41",
            "x": "4000",
            "y": "3000",
            "c_para": {
                "title": "AI Figurine Schematic",
                "date": "2026-06-16",
                "rev": "v2.0",
                "company": "",
                "drawing_number": "",
                "revision": "",
                "comment1": "AI Companion Figurine Hardware",
                "comment2": "ESP32-S3 + INMP441 + MAX98357A + WS2812B",
                "comment3": "",
                "comment4": ""
            }
        },
        "shape": shapes,
        "BBox": {
            "x": 0,
            "y": 0,
            "width": 10000,
            "height": 11000
        }
    }
    
    return schematic


def create_netlist():
    """Generate a structured netlist for reference"""
    netlist = {
        "components": [
            {"ref": "U1", "value": "ESP32-S3 DevKitC", "footprint": "Module:ESP32-S3-DevKitC", "description": "Main MCU"},
            {"ref": "U2", "value": "INMP441", "footprint": "Sensor_Audio:INMP441", "description": "I2S MEMS Microphone"},
            {"ref": "U3", "value": "MAX98357A", "footprint": "Audio:MAX98357A", "description": "I2S Class D Amplifier"},
            {"ref": "U4", "value": "AMS1117-3.3", "footprint": "Regulator_Linear:AMS1117_SOT-223", "description": "3.3V LDO"},
            {"ref": "J1", "value": "USB-C", "footprint": "Connector_USB:USB_C_Receptacle", "description": "USB Type-C Power Input"},
            {"ref": "J2", "value": "Speaker", "footprint": "Connector_PinHeader_2.54mm:PinHeader_1x02", "description": "Speaker Connector"},
            {"ref": "D1", "value": "WS2812B", "footprint": "LED_SMD:LED_WS2812B_PLCC4", "description": "Left Eye LED"},
            {"ref": "D2", "value": "WS2812B", "footprint": "LED_SMD:LED_WS2812B_PLCC4", "description": "Right Eye LED"},
            {"ref": "S1", "value": "TTP223", "footprint": "Module:Touch_TTP223", "description": "Touch Sensor"},
            {"ref": "C1", "value": "100nF", "footprint": "Capacitor_SMD:C_0402_1005Metric", "description": "ESP32 decoupling"},
            {"ref": "C2", "value": "100nF", "footprint": "Capacitor_SMD:C_0402_1005Metric", "description": "ESP32 decoupling"},
            {"ref": "C3", "value": "100nF", "footprint": "Capacitor_SMD:C_0402_1005Metric", "description": "INMP441 decoupling"},
            {"ref": "C4", "value": "100nF", "footprint": "Capacitor_SMD:C_0402_1005Metric", "description": "MAX98357A decoupling"},
            {"ref": "C5", "value": "10uF", "footprint": "Capacitor_SMD:C_0805_2012Metric", "description": "AMS1117 input bulk"},
            {"ref": "C6", "value": "10uF", "footprint": "Capacitor_SMD:C_0805_2012Metric", "description": "AMS1117 output bulk"},
            {"ref": "R1", "value": "10K", "footprint": "Resistor_SMD:R_0402_1005Metric", "description": "EN pull-up"},
            {"ref": "R2", "value": "1K", "footprint": "Resistor_SMD:R_0402_1005Metric", "description": "Data line protection"},
        ],
        "nets": [
            {"name": "+5V", "pins": ["J1:A4", "J1:B4", "U3:1", "D1:1", "D2:1", "U4:1", "C5:1"]},
            {"name": "+3V3", "pins": ["U4:3", "U1:1", "U2:1", "S1:1", "C1:1", "C2:1", "C3:1", "C6:1", "R1:1"]},
            {"name": "GND", "pins": ["J1:A1", "J1:B1", "U1:GND", "U2:2", "U3:5", "U4:2", "D1:4", "D2:4", "S1:3", "U2:6", "C1:2", "C2:2", "C3:2", "C4:2", "C5:2", "C6:2", "R1:2", "R2:2"]},
            {"name": "MIC_BCK", "pins": ["U1:7", "U2:4"]},
            {"name": "MIC_WS", "pins": ["U1:8", "U2:3"]},
            {"name": "MIC_SD", "pins": ["U1:9", "U2:5"]},
            {"name": "TOUCH", "pins": ["U1:10", "S1:2"]},
            {"name": "AMP_BCK", "pins": ["U1:18", "U3:3"]},
            {"name": "AMP_WS", "pins": ["U1:19", "U3:4"]},
            {"name": "AMP_SD", "pins": ["U1:20", "U3:2"]},
            {"name": "LED_L", "pins": ["U1:28", "D1:2"]},
            {"name": "LED_R", "pins": ["D1:3", "D2:2"]},
            {"name": "EN", "pins": ["U1:2", "R1:1"]},
            {"name": "SPK+", "pins": ["U3:7", "J2:1"]},
            {"name": "SPK-", "pins": ["U3:8", "J2:2"]},
        ]
    }
    return netlist


if __name__ == '__main__':
    output_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Generate schematic JSON
    schematic = create_schematic()
    schematic_path = os.path.join(output_dir, 'ai-figurine-schematic.json')
    with open(schematic_path, 'w', encoding='utf-8') as f:
        json.dump(schematic, f, indent=2, ensure_ascii=False)
    print(f"Schematic JSON saved to: {schematic_path}")
    
    # Generate netlist
    netlist = create_netlist()
    netlist_path = os.path.join(output_dir, 'ai-figurine-netlist.json')
    with open(netlist_path, 'w', encoding='utf-8') as f:
        json.dump(netlist, f, indent=2, ensure_ascii=False)
    print(f"Netlist saved to: {netlist_path}")
    
    print("\n=== AI Figurine Schematic Generated ===")
    print("Open ai-figurine-schematic.json in 嘉立创EDA (EasyEDA)")
    print("Note: This is a schematic description. You may need to")
    print("re-place components using the netlist as reference.")
    print("\nNetlist provides complete component and connection info.")
