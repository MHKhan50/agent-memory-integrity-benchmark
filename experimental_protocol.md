# AMIB experimental protocol v1.0

## Objective
Estimate how five persistent-memory governance policies perform under controlled memory-poisoning and cross-task-contamination scenarios.

## Hypotheses
- H1: `write_filter` reduces attack success relative to `unrestricted`, but incurs benign-memory false rejections.
- H2: `task_scoped` reduces cross-task contamination when memory task labels are correct.
- H3: `verified_write_task_scoped` offers a security/utility trade-off distinct from either single control.
- H4: `no_persistent_memory` eliminates memory-mediated attacks but may reduce task completion where benign memory is useful.

These are hypotheses, not expected findings.

## Design
A paired synthetic simulation. For each seed, one episode set is generated and evaluated under every policy. Five seeds are used by default, with 6,000 episodes per seed. Random streams for policy outcomes are deterministic and policy-specific.

## Scenario parameters
- Active task drawn from five task domains.
- Candidate memory belongs to the active task with probability 0.72.
- Poison prevalence: 0.20.
- Benign-memory availability: 0.78.
- Detector sensitivity: 0.82.
- Detector false-positive probability: 0.10.
- Baseline task success probability varies with episode difficulty.
- A retrieved poison causes task failure with probability from 0.55 to 0.80.

All parameters are explicit simulator assumptions, not empirical estimates.

## Primary outcomes
Attack success rate; task completion rate.

## Secondary outcomes
Benign-memory retention; cross-task contamination rate; false-rejection rate.

## Analysis plan
Report per-seed policy means and equal-weighted mean across seeds. Use paired seed-level differences for policy comparisons. With only five seeds, uncertainty estimates are necessarily coarse; do not treat individual episodes as independent experimental replications. A follow-up paper should add a larger seed count and pre-specified bootstrap or randomisation inference.

## Threats to validity
The detector is a simple stochastic flagger; task labels are assumed available; memory content is represented by binary attributes; there are no actual language models, embeddings, retrieval systems, tool calls, human users, or adaptive attackers. Results cannot establish deployment effectiveness.

## Reproducibility
Python 3.9+, standard library only. Run `python3 run_benchmark.py` and `python3 -m unittest discover -s tests -v`. Fixed default seeds and deterministic generation.
