# Benchmark Protocol

## Scope

This repo is a public benchmark scaffold for continuous-control policy optimization. It starts with synthetic results so the data schema, reporting, and verification path are stable before adding expensive environment runs.

## Algorithms

- A2C: included as a simple actor-critic baseline.
- PPO: included as the practical policy-gradient reference point.
- TRPO: included because trust-region methods are useful for discussing stability.

## Metrics

- `average_return`: higher is better.
- `return_stddev`: lower is more stable.
- `sample_steps`: synthetic count of environment interaction steps.

The first ranking sorts by average return and breaks ties by lower standard deviation. That rule is simple enough to verify and explicit enough to challenge later.

## Decisions

Synthetic data is used in this first pass because it avoids overclaiming experimental results. The repo proves that result handling is reproducible, not that a compute-heavy benchmark has been completed.

The parser uses Python standard library modules only. That keeps the current proof runnable in a fresh checkout and avoids package-cache blockers during automation.

## Rejected Approaches

- Publishing invented training logs was rejected because it would blur synthetic and real evidence.
- Adding heavyweight RL dependencies immediately was rejected because setup friction would dominate the proof.
- Reporting a winner without stability context was rejected because variance matters in policy optimization.

## Verification Contract

Every run should pass:

```powershell
python -m unittest discover -s tests
python src\control_policy_benchmark.py data\synthetic_results.csv
```

The CLI should report the top algorithm, row count, and average-return table.

