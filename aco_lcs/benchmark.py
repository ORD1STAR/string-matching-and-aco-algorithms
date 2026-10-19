"""Accuracy of the ACO longest-common-subsequence search against exact dynamic programming.

Runs aco() on one pair of sequences for several colony sizes and iteration counts
(averaged over several random seeds), writes a CSV to results/ and a chart to docs/.

    python aco_lcs/benchmark.py
"""
import os
import sys
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aco import aco  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W1 = "AAAArtzAAAAAAAAAArpvAAA6AAAzyuAAAAALSRAAA"
W2 = "AAAAAAAAAAAAAyxhnAAAAAAAAAAAAAAAAAutrxAAA"
ANTS = [1, 5, 20]
ITERATIONS = [1, 2, 5, 10, 20, 40]
SEEDS = range(8)
EVAPORATION = 0.4


def lcs_length(a, b):
    """Exact LCS length (classic O(n*m) dynamic programming)."""
    prev = [0] * (len(b) + 1)
    for ca in a:
        cur = [0]
        for j, cb in enumerate(b, 1):
            cur.append(prev[j - 1] + 1 if ca == cb else max(prev[j], cur[-1]))
        prev = cur
    return prev[-1]


def main():
    exact = lcs_length(W1, W2)
    print("exact LCS length:", exact)
    rows = []
    for ants in ANTS:
        for iters in ITERATIONS:
            scores, times = [], []
            for seed in SEEDS:
                np.random.seed(seed)
                t = time.perf_counter()
                best = aco(W1, W2, ants=ants, iterations=iters, evaporation=EVAPORATION)
                times.append(time.perf_counter() - t)
                scores.append(best[1])
            rows.append({"ants": ants, "iterations": iters, "mean_lcs_found": np.mean(scores),
                         "accuracy": np.mean(scores) / exact, "mean_time_s": np.mean(times), "exact_lcs": exact})
            print(rows[-1])
    df = pd.DataFrame(rows)
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "docs"), exist_ok=True)
    df.to_csv(os.path.join(ROOT, "results", "benchmark_aco_lcs.csv"), index=False)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))
    for ants, g in df.groupby("ants"):
        axes[0].plot(g["iterations"], g["accuracy"] * 100, marker="o", label=f"{ants} ant(s)")
        axes[1].plot(g["iterations"], g["mean_time_s"], marker="o", label=f"{ants} ant(s)")
    axes[0].set_ylabel("Mean LCS found / exact LCS (%)")
    axes[0].set_title(f"Accuracy (exact LCS = {exact}, mean of {len(SEEDS)} seeds)")
    axes[1].set_ylabel("Mean run time (s)")
    axes[1].set_title("Run time")
    for ax in axes:
        ax.set_xscale("log"); ax.set_xlabel("ACO iterations"); ax.grid(True, alpha=0.3); ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(ROOT, "docs", "benchmark_aco_lcs.png"), dpi=130)


if __name__ == "__main__":
    main()
