# Mobile Bluetooth Low Energy (BLE) Lifecycle Invariants

## 1. Connection & Power Management
- **Non-Blocking Asynchronous I/O**: All Bluetooth operations must run off the UI main thread using coroutines / Swift concurrency (`async`/`await`).
- **Exponential Backoff Reconnection**: Upon disconnection, the reconnection retry interval must back off exponentially ($200\text{ms} \to 400\text{ms} \to 800\text{ms} \dots \text{up to } 10\text{s}$).
- **Background Scan Throttling**: Mobile companion background scanning must consume $< 1.5\%$ battery per 24 hours.

## 2. MTU Negotiation & Security
- **Dynamic MTU Negotiation**: Explicitly request 512-byte MTU during connection setup with automatic fallback to 23 bytes.
- **Key Storage**: All mTLS device private keys and authentication tokens must be stored in iOS Keychain or Android Keystore (Hardware-Backed Keystore).
