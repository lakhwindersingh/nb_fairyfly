# Connected IoT & Mobile Management Domain Architecture

> **Autonomously Maintained by**: `agent_iot_mobile_ecosystem_architect`  
> **Status**: ✅ Verified Valid Mermaid  
> **Canonical Target**: `workplace/modules/mod_iot_mobile/` & `workplace/templates/bridge/`

## 1. System Topology & Component Layout

```mermaid
graph TD
  subgraph IoT_Firmware["Embedded IoT Node (FreeRTOS / Zephyr)"]
    GATTServer["BLE GATT Service Handler<br/>(SensorTelemetryAndControlService)"]
    RingBuf["Mutex-Locked Circular Queue<br/>(Zero-Allocation Buffer)"]
    DualOTA["Dual-Bank A/B Bootloader<br/>(ECDSA Signed Firmware)"]
  end

  subgraph Mobile_App["Cross-Platform Mobile App (KMP / Swift)"]
    BLEClient["KMP Bluetooth Client<br/>(MTU 512 Negotiation)"]
    UICompose["Jetpack Compose / SwiftUI<br/>(Real-Time Sensor Dashboard)"]
  end

  subgraph Virtual_HIL["Virtual CI/CD Emulation Bridge"]
    Bridge["Virtual BLE Socket Bridge<br/>(virtual_ble_bridge.py)"]
    MockPeripheral["Mock IoT Peripheral<br/>(mock_iot_peripheral.py)"]
  end

  GATTServer --> RingBuf
  GATTServer --> DualOTA
  BLEClient --> GATTServer
  BLEClient --> UICompose
  Bridge --> MockPeripheral
  BLEClient -.-> Bridge
```
