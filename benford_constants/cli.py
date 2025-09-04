from __future__ import annotations

from typing import List, Optional
from pathlib import Path

import click
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .data import load_physical_constants_values
from .benford import benford_expected, digit_frequencies, frequencies_table


@click.group()
def main() -> None:
    """Analyze SciPy physical constants against Benford's Law."""


@main.command()
def freq() -> None:
    """Compute and print observed vs expected leading-digit frequencies."""
    values = load_physical_constants_values()
    obs = digit_frequencies(values)
    exp = benford_expected()
    click.echo("digit, observed, expected")
    for d in range(1, 10):
        click.echo(f"{d}, {obs[d]:.4f}, {exp[d]:.4f}")


@main.command()
@click.option("--save", "save_path", type=click.Path(dir_okay=False), default=None,
              help="If provided, save the plot to this file instead of showing it.")
@click.option("--dpi", type=int, default=150, show_default=True,
              help="DPI when saving the figure.")
def plot(save_path: str | None, dpi: int) -> None:
    """Show or save a bar chart comparing observed vs expected frequencies."""
    values = load_physical_constants_values()
    obs = digit_frequencies(values)
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
    ax.set_title("Benford's Law on SciPy Physical Constants")
    ax.legend()
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=dpi)
        click.echo(f"Saved plot to {save_path}")
    else:
        plt.show()


def _load_numbers_from_file(file_path: str, column: Optional[str]) -> List[float]:
    path = Path(file_path)
    if not path.exists():
        raise click.ClickException(f"File not found: {file_path}")
    suffix = path.suffix.lower()
    if suffix in {".txt", ".dat", ".lst"}:
        # Expect one number per line
        numbers: List[float] = []
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if not s:
                    continue
                try:
                    numbers.append(float(s))
                except Exception:
                    # skip non-numeric lines
                    continue
        return numbers
    elif suffix in {".csv"}:
        df = pd.read_csv(path)
        if column:
            series = pd.to_numeric(df[column], errors="coerce")
            return [float(x) for x in series.dropna().tolist()]
        # auto-pick first numeric-looking column
        for col in df.columns:
            series = pd.to_numeric(df[col], errors="coerce")
            non_na = series.dropna()
            if not non_na.empty:
                return [float(x) for x in non_na.tolist()]
        return []
    else:
        raise click.ClickException("Unsupported file type. Use .txt (one number per line) or .csv")


@main.command("plot-file")
@click.option("--file", "file_path", type=click.Path(exists=True, dir_okay=False), required=True,
              help="Path to dataset file (.txt with one number per line, or .csv)")
@click.option("--column", type=str, default=None,
              help="For CSV files, optional column name to use as numeric data")
@click.option("--save", "save_path", type=click.Path(dir_okay=False), default=None,
              help="If provided, save the plot to this file. Default is tests/plot_<name>.png")
@click.option("--dpi", type=int, default=150, show_default=True,
              help="DPI when saving the figure.")
def plot_file(file_path: str, column: Optional[str], save_path: Optional[str], dpi: int) -> None:
    """Plot observed vs Benford for an uploaded dataset file and save to tests/ by default."""
    numbers = _load_numbers_from_file(file_path, column)
    if not numbers:
        raise click.ClickException("No numeric values found in the provided file")

    from .benford import digit_frequencies, benford_expected

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
    name = Path(file_path).stem
    ax.set_title(f"Benford's Law on {name}")
    ax.legend()
    fig.tight_layout()

    if not save_path:
        out_dir = Path("tests")
        out_dir.mkdir(parents=True, exist_ok=True)
        save_path = str(out_dir / f"plot_{name}.png")
    fig.savefig(save_path, dpi=dpi)
    click.echo(f"Saved plot to {save_path}")


if __name__ == "__main__":  # pragma: no cover
    main()


