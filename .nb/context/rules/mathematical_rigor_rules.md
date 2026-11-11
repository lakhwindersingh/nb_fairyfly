# Mathematical Rigor & Dynamical Stability Rules

## Invariants
1. **Lyapunov Negative Drift**: Any recurrence relation or energy attractor must possess an explicit Lyapunov function $V(z)$ with $\dot{V}(z) < 0$ or discrete Banach contraction factor $\rho < 1.0$.
2. **Spectral Norm Clamping**: All parameterized linear transformations subject to continuous mutation must enforce $\sigma_{\max}(W) \le 1.50$ via power iteration projection.
3. **Bounded Frobenius Drift**: Relative parameter drift across adaptation cycles must satisfy $\|\Delta W\|_F / \|W\|_F \le 0.10$.
4. **Complexity Asymptotics**: Time and memory complexities must be strictly bounded ($O(T \cdot d^2)$) with zero unbounded loops.
