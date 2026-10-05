#!/usr/bin/env python3
"""
Mock IoT Peripheral & Synthetic GATT Daemon
Emulates a Nordic nRF52/nRF53 BLE GATT peripheral running SensorTelemetryAndControlService.
"""
import time
import random
from typing import Dict, Any

class MockIoTPeripheral:
    def __init__(self, device_id: str = "NRF5340_DEV_01"):
        self.device_id = device_id
        self.service_uuid = "0000FEAA-0000-1000-8000-00805F9B34FB"
        self.telemetry_char_uuid = "0000FEA1-0000-1000-8000-00805F9B34FB"
        self.sequence_number = 0
        self.is_advertising = True

    def generate_telemetry_packet(self) -> Dict[str, Any]:
        self.sequence_number += 1
        return {
            "device_id": self.device_id,
            "timestamp_epoch_ms": int(time.time() * 1000),
            "temperature_celsius": round(20.0 + random.uniform(0.5, 5.0), 2),
            "relative_humidity_percent": round(45.0 + random.uniform(1.0, 10.0), 1),
            "battery_level_percent": 98.5,
            "sequence_number": self.sequence_number
        }

if __name__ == "__main__":
    peripheral = MockIoTPeripheral()
    print("Mock IoT Peripheral initialized:", peripheral.generate_telemetry_packet())
