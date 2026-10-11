# Real-Time Rendering & 60 FPS Frame Budgeting Rules

**Rule ID**: `realtime_rendering_rules`  
**Governing Plan**: `.nb/plan/master/enterprise-ui-design-system`  
**Classification**: High-Frequency UI Performance Invariants

---

## 1. 60 FPS Frame Budget Standard

To guarantee 60 frames per second during market volatility spikes:

$$\text{Frame Budget} = \frac{1000\text{ms}}{60} \approx 16.67\text{ms}$$

- **Main Thread Execution Ceiling**: $\le 8.0\text{ms}$ per tick cycle.
- **Browser Composite / Paint Ceiling**: $\le 8.67\text{ms}$ per cycle.

---

## 2. requestAnimationFrame Tick Debouncing

Under burst WebSocket traffic (>1,000 ticks/sec), UI rendering must NOT trigger synchronous DOM mutations per tick.
Instead, a tick queue aggregates market state and flushes updates once per animation frame via `requestAnimationFrame` (RAF).

```typescript
class MarketDataTickThrottler {
  private tickQueue: Map<string, MarketTick> = new Map();
  private isRafScheduled: boolean = false;

  public pushTick(symbol: string, tick: MarketTick): void {
    this.tickQueue.set(symbol, tick);
    if (!this.isRafScheduled) {
      this.isRafScheduled = true;
      requestAnimationFrame(() => this.flushFrame());
    }
  }

  private flushFrame(): void {
    this.isRafScheduled = false;
    const batch = new Map(this.tickQueue);
    this.tickQueue.clear();
    this.notifySubscribers(batch);
  }
}
```

---

## 3. GPU-Accelerated Cell Flashing

When a price or PnL cell updates, flash animations must execute strictly via GPU-accelerated CSS properties (`background-color`, `opacity`, `transform`) with zero layout reflow:

```css
@keyframes flash-green {
  0%   { background-color: var(--color-finance-flash-up); color: #000; }
  100% { background-color: transparent; }
}

@keyframes flash-red {
  0%   { background-color: var(--color-finance-flash-down); color: #fff; }
  100% { background-color: transparent; }
}

.tick-flash-up   { animation: flash-green 0.75s ease-out; }
.tick-flash-down { animation: flash-red 0.75s ease-out; }
```

Direct JavaScript manipulation of element geometry (e.g. `element.style.width`, `offsetHeight`) inside hot tick loops is strictly prohibited.

---

## 4. Heavy Math Web Worker Offloading

All compute-intensive mathematical operations:
1. Multi-leg Black-Scholes Greeks (Delta, Gamma, Theta, Vega, Rho)
2. Implied Volatility root-finding (Newton-Raphson / Brent solver)
3. Cubic spline yield curve fitting
4. 3D Volatility surface mesh interpolation

**MUST** execute inside dedicated background Web Workers. Results are transferred to the UI main thread using typed arrays (`Float64Array`) and zero-copy transferables.
