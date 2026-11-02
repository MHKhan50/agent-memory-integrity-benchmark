from dataclasses import dataclass
from typing import Dict, Iterable, List
import random

POLICIES = (
    "unrestricted",
    "write_filter",
    "task_scoped",
    "verified_write_task_scoped",
    "no_persistent_memory",
)

@dataclass(frozen=True)
class Episode:
    episode_id: int
    active_task: str
    memory_task: str
    poisoned: bool
    benign_memory_available: bool
    filter_flag: bool
    base_task_difficulty: float

def generate_episodes(n: int, seed: int) -> List[Episode]:
    rng = random.Random(seed)
    tasks = ("finance", "travel", "coding", "health", "shopping")
    out = []
    for i in range(n):
        active = rng.choice(tasks)
        memory_task = active if rng.random() < 0.72 else rng.choice([t for t in tasks if t != active])
        poisoned = rng.random() < 0.20
        benign = rng.random() < 0.78
        # Imperfect detector: 82% sensitivity, 10% false-positive rate.
        flag = (rng.random() < (0.82 if poisoned else 0.10))
        out.append(Episode(i, active, memory_task, poisoned, benign, flag,
                           rng.uniform(0.0, 1.0)))
    return out

def evaluate_episode(ep: Episode, policy: str, rng: random.Random) -> Dict[str, float]:
    if policy not in POLICIES:
        raise ValueError("Unknown policy: " + policy)

    persistent = policy != "no_persistent_memory"
    filtered = policy in ("write_filter", "verified_write_task_scoped")
    scoped = policy in ("task_scoped", "verified_write_task_scoped")

    write_allowed = persistent and not (filtered and ep.filter_flag)
    retrieval_allowed = write_allowed and not (scoped and ep.memory_task != ep.active_task)
    poison_retrieved = retrieval_allowed and ep.poisoned
    benign_retrieved = retrieval_allowed and ep.benign_memory_available and not ep.poisoned
    cross_task = retrieval_allowed and ep.memory_task != ep.active_task

    # A retrieved poison causes failure with probability increasing with task difficulty.
    attack_success = bool(poison_retrieved and rng.random() < (0.55 + 0.25 * ep.base_task_difficulty))
    # Benign memory improves completion; baseline capability is intentionally imperfect.
    base_success = rng.random() < (0.68 - 0.16 * ep.base_task_difficulty)
    completed = bool(base_success or (benign_retrieved and rng.random() < 0.55))
    if attack_success:
        completed = False

    benign_write_rejected = bool(filtered and ep.filter_flag and not ep.poisoned and ep.benign_memory_available)
    return {
        "attack_success": int(attack_success),
        "benign_memory_retained": int(benign_retrieved),
        "task_completed": int(completed),
        "cross_task_contamination": int(cross_task),
        "false_rejection": int(benign_write_rejected),
    }

def run_policy(episodes: Iterable[Episode], policy: str, seed: int):
    rng = random.Random(seed + 1000003 * (POLICIES.index(policy) + 1))
    rows = []
    for ep in episodes:
        result = evaluate_episode(ep, policy, rng)
        rows.append({"episode_id": ep.episode_id, "policy": policy, **result})
    return rows
