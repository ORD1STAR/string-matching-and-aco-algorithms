# String Matching and ACO Algorithms

From-scratch Python implementations of classic exact string-matching algorithms (Aho-Corasick, Boyer-Moore, Rabin-Karp) and an Ant Colony Optimization (ACO) solver for the longest common subsequence problem, with reproducible benchmarks.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?logo=numpy&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

![Benchmark of the three string-matching algorithms](docs/benchmark_string_matching.png)

*Real benchmark produced by `python -m string_matching.benchmark`: 10 random DNA motifs of length 10 searched in random texts of 1k to 500k characters.*

## Features

- **Aho-Corasick** automaton (trie plus failure links built by BFS) for multi-pattern search in a single pass.
- **Boyer-Moore** (bad-character rule) for single patterns.
- **Rabin-Karp** rolling-hash search with false-positive counting.
- **ACO for LCS**: ants walk the alignment grid (down / right / diagonal), deposit pheromone proportional to the matches found, and evaporation keeps exploration alive. Multiple sequences are handled by chaining pairwise results.
- **Exhaustive DFS baseline** that enumerates every path of the grid, plus an interactive console menu comparing ACO, DFS and a dynamic-programming reference.
- **Instrumented code**: the matchers return their own comparison counters next to the matches, so complexity can be compared independently of wall-clock noise.
- Unit tests that check every matcher against a naive scan on random inputs.

## Tech stack

Python 3.12, NumPy, pandas, Matplotlib, `unittest`.

## Results

### String matching (random DNA, 10 patterns of length 10)

| Text length | Aho-Corasick | Boyer-Moore (x10) | Rabin-Karp (x10) |
| --- | --- | --- | --- |
| 10,000 | 6.5 ms | 27.9 ms | 353 ms |
| 100,000 | 35.6 ms | 180 ms | 1.95 s |
| 500,000 | 170 ms | 813 ms | 9.62 s |

Aho-Corasick takes about one pass over the text regardless of the number of patterns, while the other two re-scan the text once per pattern. All three agree on the matches (asserted in the benchmark). The raw numbers are in `results/benchmark_string_matching.csv`; the original experiment spreadsheets from the coursework are kept in `results/*.xlsx`.

### ACO versus exact LCS

![ACO accuracy and run time](docs/benchmark_aco_lcs.png)

On a pair of 41-character sequences whose exact LCS is 28 (computed by dynamic programming), ACO is a heuristic: mean accuracy rises from about 66% (1 ant, 1 iteration) to about 86% (20 ants, 40 iterations), at the cost of roughly 2 s per run. Averages over 8 random seeds; data in `results/benchmark_aco_lcs.csv`.

## Getting started

```bash
pip install -r requirements.txt

python -m unittest discover -s tests         # correctness tests
python -m string_matching.benchmark          # ~1 minute, writes results/ and docs/
python aco_lcs/benchmark.py                  # ~1 minute
python aco_lcs/menu.py                       # interactive ACO / DFS demo
python aco_lcs/demo_animation.py             # pheromone matrix animation (needs a display)
```

## Project structure

```
string_matching/
  aho_corasick.py   trie + failure links
  boyer_moore.py    bad-character heuristic
  rabin_karp.py     rolling hash, single and multi pattern
  benchmark.py      reproducible benchmark and chart
aco_lcs/
  aco.py            ACO for LCS (pheromone matrix, evaporation)
  dfs.py            exhaustive path enumeration baseline
  menu.py           interactive console comparison
  parameter_study.py  grid search over ants / iterations / evaporation (long running)
  benchmark.py      ACO vs exact DP, produces the chart above
tests/              unittest suite
results/            CSV and spreadsheet results
docs/               charts
```

## Notes and limitations

- These are teaching implementations written for a university algorithms course; identifiers and comments in the source are partly in French.
- `AhoCorasick.recherche` reports the pattern stored at the current node only (no dictionary-suffix links), so it is exact for patterns that are not suffixes of one another, which is how it is tested here.
- The three Rabin-Karp hash values currently use the same base and modulus, so they behave like a single hash; using independent moduli would reduce false positives.
- The Boyer-Moore version applies only the bad-character rule.
- A Commentz-Walter attempt from the coursework was left out because it was unfinished.
- The DFS baseline is exponential and only suitable for very short strings.

## Author

**Hannoun Amine Amar**, Algeria
[LinkedIn](https://www.linkedin.com/in/hannoun-amine/) | hannoun.amine25@gmail.com

Licensed under the MIT License.
