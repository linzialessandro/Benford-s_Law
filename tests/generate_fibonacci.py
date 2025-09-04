import os
import sys
from typing import List

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Ensure project root (parent of tests/) is on sys.path for local imports
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from benford_constants.benford import benford_expected, digit_frequencies


def fibonacci_first_n(n: int) -> List[int]:
    if n <= 0:
        return []
    if n == 1:
        return [1]
    seq = [1, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq


def save_numbers_txt(numbers: List[int], path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for x in numbers:
            f.write(f"{x}\n")


def plot_benford(numbers: List[float], title: str, out_path: str, dpi: int = 150) -> None:
    obs = digit_frequencies(numbers)
    exp = benford_expected()
    digits = list(range(1, 10))
    observed = [obs[d] for d in digits]
    expected = [exp[d] for d in digits]
    x = range(len(digits))
    width = 0.38
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar([i - width / 2 for i in x], observed, width=width, label="Observed")
    ax.bar([i + width / 2 for i in x], expected, width=width, label="Expected (Benford)")
    ax.set_xticks(list(x))
    ax.set_xticklabels([str(d) for d in digits])
    ax.set_xlabel("Leading digit")
    ax.set_ylabel("Probability")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.savefig(out_path, dpi=dpi)
    plt.close(fig)
    print(f"Saved {out_path}")


def main() -> None:
    n = 8999
    numbers = fibonacci_first_n(n)
    data_path = os.path.join("tests", "fibonacci_8999.txt")
    plot_path = os.path.join("tests", "plot_fibonacci_8999.png")
    save_numbers_txt(numbers, data_path)
    print(f"Saved {data_path}")
    plot_benford(numbers, "Benford vs Fibonacci (first 8999 terms)", plot_path)


if __name__ == "__main__":
    main()


