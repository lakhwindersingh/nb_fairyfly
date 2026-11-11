# Hardware Enclave & Resource Rules

## Invariants
1. **Volatile RAM Footprint**: The transient mutation workspace and parameter buffer must not exceed $512\text{MB}$.
2. **Splicing Latency Budget**: In-core parameter hot-swapping via `torch.func` must complete in $\le 2.0\text{ms}$.
3. **Hardware Portability**: Algorithms must run identically across NVIDIA CUDA, Apple Silicon MPS, and hermetic CPU backends.
4. **Memory Bandwidth Cap**: Peak memory bandwidth consumption must not exceed $80\%$ of physical hardware ceiling.
