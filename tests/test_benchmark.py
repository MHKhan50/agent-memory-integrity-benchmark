import unittest
from benchmark import POLICIES, generate_episodes, run_policy

class BenchmarkTests(unittest.TestCase):
    def test_generation_is_deterministic(self):
        self.assertEqual(generate_episodes(20, 7), generate_episodes(20, 7))

    def test_policy_names_and_row_count(self):
        episodes = generate_episodes(25, 9)
        self.assertEqual(len(POLICIES), 5)
        for policy in POLICIES:
            self.assertEqual(len(run_policy(episodes, policy, 9)), 25)

    def test_no_persistent_memory_has_no_memory_effects(self):
        episodes = generate_episodes(100, 13)
        rows = run_policy(episodes, "no_persistent_memory", 13)
        self.assertTrue(all(r["attack_success"] == 0 for r in rows))
        self.assertTrue(all(r["benign_memory_retained"] == 0 for r in rows))
        self.assertTrue(all(r["cross_task_contamination"] == 0 for r in rows))

    def test_invalid_policy_rejected(self):
        with self.assertRaises(ValueError):
            run_policy(generate_episodes(1, 1), "unknown", 1)

if __name__ == "__main__":
    unittest.main()
