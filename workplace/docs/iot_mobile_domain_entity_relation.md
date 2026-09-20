# Connected IoT & Mobile Management Entity-Relationship Models

```mermaid
erDiagram
  IOT_DEVICE ||--o{ GATT_SERVICE : hosts
  GATT_SERVICE ||--o{ GATT_CHARACTERISTIC : exposes
  IOT_DEVICE ||--|| DUAL_BANK_PARTITION : contains
  MOBILE_DEVICE ||--o{ PAIRED_IOT_DEVICE : connects
  PAIRED_IOT_DEVICE ||--o{ TELEMETRY_SAMPLE : streams
```
