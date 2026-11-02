import argparse, csv, json
from pathlib import Path
from collections import defaultdict
from benchmark import POLICIES, generate_episodes, run_policy

OUT = Path("outputs")
METRICS = {
    "attack_success_rate": "attack_success",
    "benign_memory_retention": "benign_memory_retained",
    "task_completion_rate": "task_completed",
    "cross_task_contamination_rate": "cross_task_contamination",
    "false_rejection_rate": "false_rejection",
}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=6000, help="episodes per seed")
    p.add_argument("--seeds", type=int, nargs="+", default=[11, 23, 37, 53, 71])
    args = p.parse_args()
    if args.n < 1 or not args.seeds:
        p.error("--n must be positive and at least one seed is required")

    OUT.mkdir(exist_ok=True)
    episode_rows, metric_rows = [], []
    for seed in args.seeds:
        episodes = generate_episodes(args.n, seed)
        for policy in POLICIES:
            rows = run_policy(episodes, policy, seed)
            for row in rows:
                episode_rows.append({"seed": seed, **row})
            record = {"seed": seed, "policy": policy, "episodes": args.n}
            for label, key in METRICS.items():
                record[label] = sum(r[key] for r in rows) / len(rows)
            metric_rows.append(record)

    def write_csv(path, rows):
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    write_csv(OUT / "episode_results.csv", episode_rows)
    write_csv(OUT / "metrics_by_policy.csv", metric_rows)

    overall = {}
    for policy in POLICIES:
        subset = [r for r in metric_rows if r["policy"] == policy]
        overall[policy] = {
            metric: sum(r[metric] for r in subset) / len(subset)
            for metric in METRICS
        }
    summary = {
        "benchmark": "Agent Memory Integrity Benchmark (AMIB)",
        "version": "0.2.0",
        "synthetic_episodes_per_seed": args.n,
        "seeds": args.seeds,
        "policies": list(POLICIES),
        "total_episode_policy_evaluations": args.n * len(args.seeds) * len(POLICIES),
        "metrics": overall,
        "interpretation_warning": "Synthetic simulator results only; not real-world agent or LLM measurements."
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
