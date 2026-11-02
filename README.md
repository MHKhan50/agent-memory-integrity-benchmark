# Agent Memory Integrity Benchmark (AMIB) v0.2.0

A reproducible **synthetic** benchmark for evaluating persistent-memory integrity in multi-task AI-agent workflows.

## Research question
How do memory-write controls and task-scoped retrieval policies trade off resistance to poisoned/cross-task memory against benign-memory retention and task completion?

## Scope and evidence boundary
AMIB is a controlled simulation, not an evaluation of deployed LLM agents or real users. Episodes are generated from explicit rules. Results support claims about this simulator only; they do not establish real-world attack rates or model performance.

## Quick start
Requires Python 3.9+; standard library only.

```bash
python3 run_benchmark.py
python3 -m unittest discover -s tests -v
```

For a smaller smoke run:

```bash
python3 run_benchmark.py --n 200 --seeds 11 23
```

Outputs are written to `outputs/`:
- `episode_results.csv`: episode-level outcomes
- `metrics_by_policy.csv`: policy/seed aggregates
- `summary.json`: configuration and overall aggregates

## Policies
1. `unrestricted`: all candidate memories can be written and retrieved.
2. `write_filter`: rejects memory writes flagged as suspicious by a deterministic rule.
3. `task_scoped`: retrieval is restricted to memories tagged for the active task.
4. `verified_write_task_scoped`: combines the write filter and task-scoped retrieval.
5. `no_persistent_memory`: disables persistent memory (control condition).

## Outcomes
- `attack_success_rate`: fraction of episodes where a poisoned memory changes the task outcome.
- `benign_memory_retention`: fraction of eligible benign memories retained and available.
- `task_completion_rate`: fraction of episodes meeting the task's success criterion.
- `cross_task_contamination_rate`: fraction of episodes where a memory from another task affects the answer.
- `false_rejection_rate`: fraction of benign writes rejected by the write filter.

## Reproducibility
The default run uses 6,000 episodes per seed and five fixed seeds (11, 23, 37, 53, 71): 30,000 episode-policy evaluations per policy. Each policy sees the same generated episodes within a seed (paired design). The random generator is seeded; no network, API, model, or external dataset is used.

## Interpretation
Compare policies using paired seed-level summaries. The benchmark is suitable for methodological prototyping and hypothesis generation. A formal paper should report uncertainty intervals, sensitivity analyses, threat-model limitations, and independent replication.
