"""Synthetic continuous-control benchmark summarizer."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from statistics import mean


@dataclass(frozen=True)
class BenchmarkRun:
    algorithm: str
    environment: str
    seed: int
    average_return: float
    return_stddev: float
    sample_steps: int


@dataclass(frozen=True)
class AlgorithmSummary:
    algorithm: str
    runs: int
    mean_return: float
    mean_stddev: float
    total_steps: int


def load_runs(path: Path) -> list[BenchmarkRun]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return [
            BenchmarkRun(
                algorithm=row["algorithm"],
                environment=row["environment"],
                seed=int(row["seed"]),
                average_return=float(row["average_return"]),
                return_stddev=float(row["return_stddev"]),
                sample_steps=int(row["sample_steps"]),
            )
            for row in reader
        ]


def summarize(runs: list[BenchmarkRun]) -> list[AlgorithmSummary]:
    algorithms = sorted({run.algorithm for run in runs})
    summaries: list[AlgorithmSummary] = []

    for algorithm in algorithms:
        rows = [run for run in runs if run.algorithm == algorithm]
        summaries.append(
            AlgorithmSummary(
                algorithm=algorithm,
                runs=len(rows),
                mean_return=mean(row.average_return for row in rows),
                mean_stddev=mean(row.return_stddev for row in rows),
                total_steps=sum(row.sample_steps for row in rows),
            )
        )

    return sorted(summaries, key=lambda row: (-row.mean_return, row.mean_stddev, row.algorithm))


def risk_adjusted_score(summary: AlgorithmSummary) -> float:
    if summary.mean_stddev <= 0:
        return summary.mean_return
    return summary.mean_return / summary.mean_stddev


def format_table(summaries: list[AlgorithmSummary]) -> str:
    lines = ["algorithm,runs,mean_return,mean_stddev,total_steps,risk_adjusted_score"]
    for row in summaries:
        lines.append(
            f"{row.algorithm},{row.runs},{row.mean_return:.2f},{row.mean_stddev:.2f},{row.total_steps},{risk_adjusted_score(row):.2f}"
        )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize synthetic continuous-control results.")
    parser.add_argument("csv_path", type=Path)
    args = parser.parse_args()

    runs = load_runs(args.csv_path)
    summaries = summarize(runs)

    print(f"rows={len(runs)}")
    print(f"top_algorithm={summaries[0].algorithm if summaries else 'none'}")
    print(f"top_risk_adjusted={max(summaries, key=risk_adjusted_score).algorithm if summaries else 'none'}")
    print(format_table(summaries))


if __name__ == "__main__":
    main()

