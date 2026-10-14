# Enterprise UI Token Consistency & Invariant Rules

**Rule ID**: `ui_token_consistency_rules`  
**Governing Plan**: `.nb/plan/master/enterprise-ui-design-system`  
**Classification**: Enterprise Front-End Invariants (Strict Enforcement)

---

## 1. Mathematical 8px Base Spatial Rhythm

All layouts, containers, gutters, padding, margin, and control heights must strictly conform to the 8px spatial grid with an allowed 4px micro-increment:

$$\text{Spacing}(n) = 8n \text{ px}, \quad n \in \{0.5, 1, 1.5, 2, 2.5, 3, 4, 6, 8, 12\}$$

- `--space-0-5`: `4px`
- `--space-1`: `8px`
- `--space-1-5`: `12px`
- `--space-2`: `16px`
- `--space-2-5`: `20px`
- `--space-3`: `24px`
- `--space-4`: `32px`
- `--space-6`: `48px`
- `--space-8`: `64px`
- `--space-12`: `96px`

Arbitrary hardcoded pixels (e.g. `margin: 17px`, `padding: 13px`) are strictly forbidden in production stylesheets and trigger PR quarantine.

---

## 2. Standardized Control Sizing Tiers

Form inputs, action triggers, buttons, and badges must map directly to the 5 standardized height tiers:

| Tier | Height | Target Use Case |
| :--- | :---: | :--- |
| **Control-XS** | `24px` | Compact blotter action badges, inline table chips |
| **Control-SM** | `32px` | Pro trading order controls, blotter filter inputs |
| **Control-MD** | `40px` | Default admin forms, primary dropdowns, dialog buttons |
| **Control-LG** | `48px` | Corporate marketing CTAs, authentication inputs, search |
| **Control-XL** | `56px` | Marketing hero callouts, enterprise pricing buttons |

---

## 3. Tabular Numerics for Financial Data

All monetary quantities, Greek derivatives, percentages, strikes, prices, and timestamps must render using **Tabular Numerics** (`font-variant-numeric: tabular-nums lining-nums` or `.numeric-tabular`):

```css
.numeric-tabular, [data-numeric="tabular"] {
  font-family: 'JetBrains Mono', 'SF Mono', monospace;
  font-variant-numeric: tabular-nums lining-nums;
  letter-spacing: -0.02em;
}
```

This prevents horizontal layout shift during real-time tick updates.

---

## 4. Multi-Theme Color Semantics & WCAG 2.2 AAA Contrast

The application supports 3 certified semantic themes:
1. `corporate-light`: Clean slate/white surface, high contrast, brand indigo.
2. `enterprise-dark`: Slate/navy `#0b0f19`, low eye strain, indigo accents.
3. `pro-oled`: True black `#000000`, neon cyan/emerald/rose accents for institutional trading desks.

Financial status indicators must use certified semantic tokens:
- **Gain / Bullish / Long / Credit**: `--color-finance-gain` (`#10b981` in light, `#00e676` in OLED)
- **Loss / Bearish / Short / Debit**: `--color-finance-loss` (`#f43f5e` in light, `#ff1744` in OLED)
- **Neutral / Zero Greeks**: `--color-finance-neutral` (`#64748b` in light, `#718096` in OLED)
- **Uptick Flash**: `--color-finance-flash-up`
- **Downtick Flash**: `--color-finance-flash-down`

All body text must achieve $\ge 4.5:1$ contrast ratio against its surface background, and $\ge 7.0:1$ in high-contrast mode.

---

## 5. Decluttering Standard: The Rule of 3

To prevent cognitive overload on complex dashboards:
1. **Primary Viewport**: Displays at most **2 to 3 tightly correlated, interdependent panes** simultaneously.
2. **Secondary Tools**: Disassociated tools must be tabbed into `<ContextTabbedWorkspace />` rather than stacked vertically.
3. **State Preservation**: Inactive tab panes are hidden using `display: none` to retain internal state and WebAssembly / WebGL memory without recalculation lag.

---

## 6. Mobile & Touch Ergonomics (WCAG 2.5.5)

- Minimum touch target size on mobile viewports must be $\ge 44\text{px}$ (`--touch-target-min: 44px`, `.btn-touch`).
- High-frequency blotters must freeze the `Symbol` column (`position: sticky; left: 0`) while enabling horizontal touch scrolling across Greek metrics and PnL.
