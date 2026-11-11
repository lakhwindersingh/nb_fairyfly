# Lyapunov Spectral Stability Rules

## 1. Spectral Radius Upper Bound
For any injected or mutated parameter tensor $W \in \mathbb{R}^{m \times n}$:
$$\sigma_{\max}(W) \le 1.50$$

Where $\sigma_{\max}(W)$ is estimated via Power Iteration:
- Iterations: $K \ge 15$
- Initial random vector: $v_0 \sim \mathcal{N}(0, I), \|v_0\|_2 = 1$
- Recurrence: $u_{k+1} = \frac{W v_k}{\|W v_k\|_2}, v_{k+1} = \frac{W^T u_{k+1}}{\|W^T u_{k+1}\|_2}$
- Estimate: $\sigma_{\max} = \|W v_K\|_2$

## 2. Projection Clamping
If $\sigma_{\max}(W) > 1.50$:
$$W_{\text{clamped}} = W \cdot \frac{1.50}{\sigma_{\max}(W)}$$
Ensures bounded operator norm and prevents chaotic attractor blowup.
