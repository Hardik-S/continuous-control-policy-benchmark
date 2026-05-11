import unittest
from pathlib import Path

from src.control_policy_benchmark import format_table, load_runs, summarize


FIXTURE = Path(__file__).resolve().parents[1] / "data" / "synthetic_results.csv"


class ControlPolicyBenchmarkTests(unittest.TestCase):
    def test_loads_all_synthetic_rows(self):
        runs = load_runs(FIXTURE)

        self.assertEqual(len(runs), 9)
        self.assertEqual({run.algorithm for run in runs}, {"A2C", "PPO", "TRPO"})

    def test_summary_ranks_higher_return_first(self):
        summaries = summarize(load_runs(FIXTURE))

        self.assertEqual(summaries[0].algorithm, "PPO")
        self.assertGreater(summaries[0].mean_return, summaries[-1].mean_return)
        self.assertEqual(summaries[0].runs, 3)

    def test_format_table_is_csv_like_for_readme_copying(self):
        table = format_table(summarize(load_runs(FIXTURE)))

        self.assertIn("algorithm,runs,mean_return,mean_stddev,total_steps", table)
        self.assertIn("PPO,3,", table)


if __name__ == "__main__":
    unittest.main()

