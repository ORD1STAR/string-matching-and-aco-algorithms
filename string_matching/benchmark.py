"""Benchmark Aho-Corasick, Boyer-Moore and Rabin-Karp on random DNA text.

Searches PATTERNS random motifs of length PATTERN_LEN in random texts of growing size,
records wall-clock time and the algorithms' own comparison counters, writes a CSV to
results/ and a chart to docs/.

    python -m string_matching.benchmark
"""
import os
import random
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from string_matching.aho_corasick import AhoCorasick
from string_matching.boyer_moore import boyer_moore
from string_matching.rabin_karp import rabin_karp_multiple_hashes

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT_SIZES = [1_000, 10_000, 50_000, 100_000, 250_000, 500_000]
PATTERNS = 10
PATTERN_LEN = 10
REPEATS = 3


def dna(n):
    return "".join(random.choices("ACGT", k=n))


def timed(fn):
    best = float("inf")
    result = None
    for _ in range(REPEATS):
        t = time.perf_counter()
        result = fn()
        best = min(best, time.perf_counter() - t)
    return best * 1000.0, result


def main():
    random.seed(42)
    patterns = list({dna(PATTERN_LEN) for _ in range(PATTERNS)})
    ac = AhoCorasick()
    for p in patterns:
        ac.ajouter(p)
    ac.echecs()

    rows = []
    for n in TEXT_SIZES:
        text = dna(n)
        ms_ac, (found_ac, ops_ac) = timed(lambda: ac.recherche(text))
        ms_bm, res_bm = timed(lambda: [boyer_moore(text, p) for p in patterns])
        ops_bm = sum(ops for _, ops in res_bm)
        found_bm = sum(len(occ) for occ, _ in res_bm)
        ms_rk, ((found_rk, ops_rk), _fp) = timed(lambda: rabin_karp_multiple_hashes(text, patterns))
        assert len(found_ac) == found_bm == len(found_rk), "algorithms disagree"
        for name, ms, ops in (("Aho-Corasick", ms_ac, ops_ac),
                              ("Boyer-Moore", ms_bm, ops_bm),
                              ("Rabin-Karp", ms_rk, ops_rk)):
            rows.append({"text_length": n, "algorithm": name, "time_ms": ms, "comparisons": ops,
                         "matches": len(found_ac)})
        print(f"n={n:>8}  AC {ms_ac:8.1f} ms  BM {ms_bm:8.1f} ms  RK {ms_rk:8.1f} ms  matches={len(found_ac)}")

    df = pd.DataFrame(rows)
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "docs"), exist_ok=True)
    df.to_csv(os.path.join(ROOT, "results", "benchmark_string_matching.csv"), index=False)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))
    for ax, col, label in ((axes[0], "time_ms", "Time (ms, best of %d)" % REPEATS),
                           (axes[1], "comparisons", "Character comparisons / steps")):
        for name, g in df.groupby("algorithm"):
            ax.plot(g["text_length"], g[col], marker="o", label=name)
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.set_xlabel("Text length (random DNA)"); ax.set_ylabel(label)
        ax.grid(True, alpha=0.3, which="both")
        ax.legend()
    fig.suptitle(f"Multi-pattern search: {len(patterns)} motifs of length {PATTERN_LEN}", fontweight="bold")
    fig.tight_layout()
    fig.savefig(os.path.join(ROOT, "docs", "benchmark_string_matching.png"), dpi=130)


if __name__ == "__main__":
    main()
