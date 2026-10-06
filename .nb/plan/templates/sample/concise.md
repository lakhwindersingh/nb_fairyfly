---
plan_type: "layerable_domain_plan"
plan_id: "domain_sample_iot_mobile"
name: "Sample IoT & Mobile BLE Ecosystem (Concise Plan)"
parent_master_plan: "master/parent-master-plan/concise.md"
tier_mapping:
  tier_2: "Enterprise Domain Rules & Wire Contracts (.nb/context/contracts/, .nb/context/rules/)"
  tier_3: "Specialist Subagents & Delivery Workflows (.nb/agentic/custom/agents/, .nb/agentic/custom/workflows/)"
model_tiering_policy:
  provider_agnostic: true
  tier_a_model: "claude-3-7-sonnet / pro"
  tier_b_model: "claude-3-5-haiku / flash"
---

# Layerable Context Engineering Plan: Sample IoT & Mobile Space (Concise Plan)

### Executive Overview & Domain Grounding

This document is a sample **Layerable Domain-Specific Context Engineering Plan** demonstrating how to layer device-level embedded firmware and mobile application architectures onto the generic **Parent Master Context Engineering Framework**. It injects concrete Bluetooth Low Energy (BLE 5.3) GATT wire contracts, FreeRTOS / Zephyr MCU simulators, mobile client state stores, and virtual socket bridges required for:

1. **Embedded Firmware & MCU Subsystem (`mod_embedded_firmware`)**: C/C++ embedded code running under FreeRTOS / Zephyr OS abstractions with low-power state machines.
2. **Mobile Companion Application (`mod_mobile_companion_app`)**: Kotlin Multiplatform / Swift client managing connection pools, background sync, and telemetry ingestion.
3. **BLE 5.3 GATT Wire Contracts**: Strictly typed binary packet specifications with MTU bounded payloads ($244\text{ bytes}$) and CRC-32 integrity.
4. **Virtual Socket Bridge Simulator**: Inter-process Unix domain socket daemon bridging MCU serial emulators with mobile clients for deterministic CI testing.

```mermaid
graph TD
  subgraph Device_Layer["Embedded Device Subsystem (mod_embedded_firmware)"]
    FirmwareCore["MCU Firmware Core (FreeRTOS / Zephyr)"]
    BleGattServer["GATT Telemetry Server"]
    UartEmulation["UART Serial Streamer"]
  end

  subgraph Mobile_Layer["Mobile Companion Client (mod_mobile_companion_app)"]
    BleCentralClient["GATT Central Client"]
    TelemetryStore["SQLite / Realm Telemetry Store"]
    MobileDashboard["User Interface / Control Surface"]
  end

  subgraph Test_Harness["Virtual Loopback Bridge"]
    VirtualSocketDaemon["Virtual BLE Daemon Bridge (Unix Socket)"]
  end

  subgraph Governance_Platform[".nb/ Percipience Platform"]
    ContractSchema[".nb/context/contracts/ble_gatt_telemetry_contract.yaml"]
    RuleInvariants[".nb/context/rules/ble_packet_mtu_invariants.md"]
    Gatekeeper[".nb/bin/percipience gate"]
  end

  FirmwareCore --> BleGattServer
  BleGattServer --> UartEmulation
  UartEmulation <--> VirtualSocketDaemon
  VirtualSocketDaemon <--> BleCentralClient
  BleCentralClient --> TelemetryStore
  TelemetryStore --> MobileDashboard

  BleGattServer -.->|Enforces| ContractSchema
  BleCentralClient -.->|Validates| RuleInvariants
  Gatekeeper -.->|Audit| Device_Layer
```

---

## 1. Domain-Specific Quad-Space Mapping

- `.nb/context/contracts/`: `ble_gatt_telemetry_contract.yaml`, `device_command_rpc_contract.json`.
- `.nb/context/rules/`: `ble_packet_mtu_invariants.md`, `firmware_memory_bounds.md`.
- `.nb/agentic/custom/agents/`: `agent_iot_developer.yaml`, `agent_mobile_developer.yaml`.
- `.nb/agentic/custom/workflows/`: `iot_mobile_delivery_flow.yaml`.
- `workplace/modules/`: `mod_embedded_firmware/`, `mod_mobile_companion_app/`.
- `user/outputs/`: Device telemetry logs, MTU compliance receipts, and test reports.

---

## 2. Dynamic Tier Action Matrix & CLI Governance

| Tier | Entitled Buttons & Features | Platform Tools Exposure | Domain Capabilities |
| :--- | :--- | :--- | :---: |
| **Free Community** (`plan_free`) | 🚀 Bootstrap, 🚦 Gatekeeper, 🛡️ Merkle Audit, ▶️ CI/CD, 🔍 Validate Layer, ⚡ Token Summary | Safe Gatekeeper Actions Only (Internal tools unexposed) | Basic C/Kotlin syntax checks & contract validation |
| **Team Tier** (`plan_team`) | + 🌿 Worktrees, 🤖 Agent Registry, 🔄 Anti-Drift Check | Safe Gatekeeper Actions + Custom Agents | Multi-agent firmware/mobile handoffs & mock loops |
| **Business Tier** (`plan_business`) | + 📦 Sealed NBPack Packaging, 🌐 Gateway Provisioner, 🧠 Cognitive Parity Report | Standard & Full Platform Tool APIs + Encrypted Packaging | Virtual socket bridge daemon & packet fuzzing |
| **Enterprise Dedicated** (`plan_enterprise`) | + 🐝 Swarm Triad Orchestrator, 🔒 Private VPC Enclave, 📜 Immutable WORM Egress | Full Unrestricted Platform Tool APIs + Air-gapped VPC | Full hardware-in-the-loop (HIL) automation |

---

## 3. CLI, Multi-Tier Packaging & Layer Management

```bash
# Package standard universal layer bundle
./.nb/bin/percipience layer pack \
  --plan .nb/plan/templates/sample/concise.md \
  --output .nb/bundles/sample_iot_mobile_domain.nbpack

# Apply layer bundle to ephemeral context
./.nb/bin/percipience layer apply \
  --pack .nb/bundles/sample_iot_mobile_domain.nbpack \
  --in-memory-only

# Verify domain invariants via Gatekeeper
./.nb/bin/percipience gate
```
