# Web Performance & Core Web Vitals Invariants

## 1. Core Web Vitals Budget
- **First Contentful Paint (FCP)**: $\le 1.2\text{s}$
- **Largest Contentful Paint (LCP)**: $\le 2.5\text{s}$
- **Cumulative Layout Shift (CLS)**: $\le 0.1$
- **Interaction to Next Paint (INP)**: $\le 200\text{ms}$
- **Time to First Byte (TTFB)**: $\le 200\text{ms}$

## 2. Asset & Bundle Constraints
- **Initial Production JS Bundle**: $\le 150\text{KB}$ gzipped payload.
- **Critical CSS**: Inlined or preloaded above-the-fold with zero render-blocking stylesheets.
- **Image Optimization**: All images must serve modern WebP/AVIF formats with explicit `width` and `height` dimensions.
