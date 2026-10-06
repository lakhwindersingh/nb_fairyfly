# Sample L1 Domain Plan: IoT & Mobile BLE Ecosystem Space

**Plan ID**: `domain_sample_iot_mobile`  
**Capability Rating**: `L1 Foundation (Device Space)`  
**Version**: `1.0.0`  

## Overview

This is a **concrete reference implementation** of a layerable domain plan created using the Percipience Standard Template Kit. It demonstrates how to specify cross-platform embedded firmware, Bluetooth Low Energy (BLE 5.3) GATT wire contracts, mobile companion applications, and virtual socket bridges.

## Quick Links

- **Concise Plan**: [concise.md](./concise.md) — Compact domain specification (~95 lines)
- **Detailed Plan**: [detailed.md](./detailed.md) — Full engineering blueprint, GATT specs, and test harness (~330 lines)
- **Version Manifest**: [MANIFEST.yaml](./MANIFEST.yaml) — Cryptographic version ledger and dependency bindings

## Key Capabilities

- **Embedded Firmware & MCU Subsystem (`mod_embedded_firmware`)**: C/C++ FreeRTOS / Zephyr OS runtime emulation.
- **Mobile Companion Application (`mod_mobile_companion_app`)**: Kotlin Multiplatform / Swift client with reactive state stores.
- **BLE 5.3 GATT Wire Contracts**: Strictly typed binary protocol packets with CRC-32 validation.
- **Virtual Socket Bridge Simulator**: Ephemeral mock daemon bridging MCU serial output to mobile virtual sockets.

## Success Criteria

- 100% compliance with `ble_gatt_telemetry_contract.yaml`.
- Zero dropped packets across 10,000 synthetic telemetry iterations.
- Full verification through pre-commit gatekeeper.
