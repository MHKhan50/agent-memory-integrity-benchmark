# Dataset card: AMIB synthetic scenarios

- **Name:** Agent Memory Integrity Benchmark synthetic episode stream
- **Version:** 0.2.0
- **Type:** Generated tabular simulation data
- **Source:** `benchmark.py`; generated locally at run time
- **Personal data:** None
- **External data:** None
- **Intended use:** Reproducibility, policy-mechanism prototyping, teaching, hypothesis generation
- **Out-of-scope use:** Claims about real-world attack prevalence, deployed agent security, or comparative LLM performance
- **Generation:** Fixed-seed pseudorandom draws using Python's standard library
- **Fields:** episode_id, seed, active_task, memory_task, poisoned, benign_memory_available, filter_flag, base_task_difficulty; result files add policy and outcome indicators
- **Limitations:** Simplified binary memory representation and non-adaptive attacker; detector assumptions are stipulated rather than empirically calibrated
