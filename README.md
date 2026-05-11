# Continuous-Control Policy Optimization Benchmark

This public repo packages a small, reproducible benchmark surface for comparing continuous-control policy optimization methods. The first proof point is a deterministic result summarizer with synthetic scores, explicit compute caveats, and tests that can run without MuJoCo, GPUs, or paid simulators.

## What This Proves

- Research discipline: algorithms, environments, seeds, and metrics are explicit.
- Communication quality: result tables distinguish evidence from planned experiments.
- Practical judgment: the repo starts with a cheap verifier before expensive training.
- Public safety: the data is synthetic and does not imply unpublished research results.

## File Structure

- `src/control_policy_benchmark.py` loads synthetic runs and summarizes score stability.
- `data/synthetic_results.csv` contains fictional A2C, PPO, and TRPO benchmark rows.
- `tests/test_control_policy_benchmark.py` verifies parser and ranking behavior.
- `docs/BENCHMARK_PROTOCOL.md` documents assumptions, rejected approaches, and next work.

## Current Benchmark

The current artifact compares average return and stability across synthetic runs for three algorithms. It should be treated as a packaging and methodology proof point, not a claim that any algorithm was trained here.

Run:

```powershell
python -m unittest discover -s tests
python src\control_policy_benchmark.py data\synthetic_results.csv
```

## Next Work

The next useful change is adding a small real-environment smoke run, likely Pendulum or MountainCarContinuous, with a strict time budget and cached output. Full MuJoCo-style benchmarking should wait until the repo has clear compute expectations and result provenance.

