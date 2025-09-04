import os
from typing import Iterable, Optional

import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def get_first_digit(n: Optional[float]) -> Optional[int]:
    if n is None or pd.isna(n) or n == 0:
        return None
    n = abs(float(n))
    while n < 1:
        n *= 10
    return int(str(n)[0])


def plot_series_against_benford(series: pd.Series, title: str, out_path: str) -> None:
    digits = [get_first_digit(v) for v in series]
    counts = {d: 0 for d in range(1, 10)}
    total = 0
    for d in digits:
        if d is not None and 1 <= d <= 9:
            counts[d] += 1
            total += 1
    if total == 0:
        print(f"No valid data to plot for {title}")
        return
    observed = [counts[d] / total for d in range(1, 10)]
    benford = [np.log10(1 + 1 / d) for d in range(1, 10)]

    x = np.arange(9)
    width = 0.38
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(x - width / 2, observed, width=width, label="Observed")
    ax.bar(x + width / 2, benford, width=width, label="Expected (Benford)")
    ax.set_xticks(x)
    ax.set_xticklabels([str(d) for d in range(1, 10)])
    ax.set_xlabel("Leading digit")
    ax.set_ylabel("Probability")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"Saved {out_path}")


def main() -> None:
    # 1) Country populations (should follow Benford)
    pop_url = "https://datahub.io/core/population/r/population.csv"
    try:
        pop_df = pd.read_csv(pop_url)
        pop_2016 = pop_df[pop_df["Year"] == 2016]["Value"]
        plot_series_against_benford(
            pop_2016,
            "Benford vs Country Populations (2016)",
            os.path.join("tests", "plot_populations_2016.png"),
        )
    except Exception as e:
        print(f"Population dataset failed: {e}")

    # 2) Uniform random 1000-9999 (should not follow Benford)
    # np.random.randint high bound is exclusive; use 10000 to include 9999
    uniform = np.random.randint(1000, 10000, 5000)
    plot_series_against_benford(
        pd.Series(uniform),
        "Benford vs Uniform Integers [1000,9999]",
        os.path.join("tests", "plot_uniform_1000_9999.png"),
    )

    # 3) S&P 500 market caps (should roughly follow Benford)
    sp_url = "https://datahub.io/core/s-and-p-500-companies-financials/r/constituents-financials.csv"
    try:
        sp_df = pd.read_csv(sp_url)
        market_caps = pd.to_numeric(sp_df["Market Cap"], errors="coerce").dropna()
        plot_series_against_benford(
            market_caps,
            "Benford vs S&P 500 Market Caps",
            os.path.join("tests", "plot_sp500_market_caps.png"),
        )
    except Exception as e:
        print(f"S&P 500 dataset failed: {e}")


if __name__ == "__main__":
    main()


