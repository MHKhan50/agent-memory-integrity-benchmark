# Agent Memory Integrity Benchmark: A Synthetic Evaluation of Persistent-Memory Poisoning Controls

**Author:** Muzammal Hussain
**Status:** Reproducible synthetic benchmark; results must be generated locally before numerical claims are added.

## Abstract
Persistent memory can improve continuity in AI-agent workflows, but it also creates a channel through which poisoned or task-inappropriate information may influence later decisions. This work introduces the Agent Memory Integrity Benchmark (AMIB), a reproducible synthetic simulation comparing five memory-governance policies: unrestricted memory, write filtering, task-scoped retrieval, combined filtering and scoping, and a no-persistent-memory control. The benchmark measures attack success, benign-memory retention, task completion, cross-task contamination, and false rejection. Its contribution is a transparent experimental protocol and executable baseline, not evidence about deployed language models. All parameter values are explicit simulator assumptions. The benchmark is designed to support subsequent empirical validation with real agent systems.

## 1. Research motivation
Persistent memory changes the security boundary of an agent. A malicious or erroneous write may affect later tasks, while aggressive controls may discard useful information. The problem is therefore a security-utility trade-off rather than a single detection objective.

## 2. Research question
How do write-time filtering and task-scoped retrieval affect memory-poisoning risk, cross-task contamination, and benign-memory utility in a controlled synthetic environment?

## 3. Method
AMIB generates task episodes with an active task, a candidate memory's task label, a poison indicator, benign-memory availability, a detector flag, and task difficulty. Five policies are evaluated on identical episode sets for each random seed. The default design uses five seeds and 6,000 episodes per seed.

## 4. Measures
The primary measures are attack success rate and task completion rate. Secondary measures are benign-memory retention, cross-task contamination, and false rejection of benign writes.

## 5. Results
**Insert results from `outputs/summary.json` and `outputs/metrics_by_policy.csv` after running the benchmark.** Do not report invented or illustrative numbers as findings.

## 6. Discussion
The policy mechanisms encode different trade-offs. Write filtering can block poisoned writes but may reject benign writes when the detector produces false positives. Task scoping can prevent cross-task retrieval when task labels are correct, but it does not by itself detect poisoned content within the active task. Combining the controls may address both mechanisms while retaining their respective failure modes. Disabling persistent memory removes memory-mediated attack paths in this simulator but also removes potential utility from benign memory.

## 7. Limitations
AMIB is synthetic. It does not execute an LLM, implement semantic memory, model adaptive adversaries, or measure real deployments. The stipulated probabilities are not empirical estimates. Results should be interpreted as properties of the simulator and policy definitions only.

## 8. Conclusion
AMIB provides a reproducible starting point for studying the interaction between memory integrity and memory utility. The next research stage should calibrate assumptions using documented threat models, implement the policies in a real agent memory stack, and evaluate them on independently constructed tasks.

## Reproducibility statement
Source code, fixed seeds, tests, protocol, and generated CSV/JSON outputs are included. Python 3.9+ and the standard library are sufficient.
