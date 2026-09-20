# Embedded C/C++ Safety & MISRA Invariants

## 1. Memory Safety & Allocation
- **Zero Dynamic Memory Allocation**: Prohibit `malloc()`, `calloc()`, `realloc()`, and `free()` after task scheduler boot. All message queues, buffers, and stacks must use static allocation.
- **Fixed-Size Ring Buffers**: High-frequency telemetry streams must use mutex-locked circular ring buffers with overflow protection flags.

## 2. MISRA C:2012 Compliance
- Prohibit undefined behavior: zero implicit type conversions across unsigned and signed integer types.
- All pointer dereferences must check against `NULL`.
- Watchdog timer (WDT) refresh hooks must be placed inside all FreeRTOS / Zephyr task loops.
