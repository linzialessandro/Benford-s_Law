# Benford's Law on Physical Constants

Analyze leading digits of SciPy physical constants against Benford's Law with CLI and plots.

## Quickstart

Requires Python 3.10+ (tested on 3.14). Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -U pip
python3 -m pip install -r requirements.txt
```

Run frequency table:

```bash
python -m benford_constants freq
```

Show comparison plot:

```bash
python -m benford_constants plot
# or save to file (useful in non-interactive environments)
python -m benford_constants plot --save benford_plot.png
```

## Examples

- Compute and print frequencies:

```bash
python -m benford_constants freq
# digit, observed, expected
# 1, 0.30, 0.3010
# ...
```

- Show bar comparison plot:

```bash
python -m benford_constants plot
```

## What is Benford's Law?

Benford's Law (First-Digit Law) states that in many naturally occurring datasets, small leading digits occur more frequently than large ones. The probability that the first significant digit is \(d \in \{1,\dots,9\}\) is

\[ P(d) = \log_{10}\big(1 + \tfrac{1}{d}\big) \]

Approximate probabilities: 1 → 30.1%, 2 → 17.6%, 3 → 12.5%, 4 → 9.7%, 5 → 7.9%, 6 → 6.7%, 7 → 5.8%, 8 → 5.1%, 9 → 4.6%.

The law typically holds for measurements that span several orders of magnitude (e.g., financial figures, populations, physical constants), and does not hold for uniform or human-assigned identifiers (like IDs) by design.

## Data analyzed

The program uses the SciPy dataset of physical constants (`scipy.constants.physical_constants`). Each entry is a tuple `(value, unit, uncertainty)`. The analysis:

- **Selection**: includes finite, non-zero numeric `value`s only.
- **Transformation**: takes absolute values, extracts the first significant (leading) decimal digit.
- **Computation**: computes observed frequencies of digits 1–9 and compares them with Benford's theoretical probabilities.
- **Visualization**: a grouped bar chart shows observed vs expected probabilities.

You can inspect the raw constants via the helper `load_physical_constants_table()` which returns `(name, value, unit, uncertainty)` rows.

## Analyze your own dataset (file upload)

You can generate a Benford comparison plot from a dataset file you provide.

Accepted formats:
- **TXT**: one number per line (non-numeric lines are skipped)
- **CSV**: specify a numeric column via `--column`, or the tool will auto-pick the first numeric-looking column

Command:
```bash
python -m benford_constants plot-file --file PATH/TO/dataset.txt
# or for CSV with a specific column
python -m benford_constants plot-file --file PATH/TO/dataset.csv --column Amount
```

Output:
- By default, the plot PNG is saved under `tests/` with the name `plot_<dataset-name>.png`, where `<dataset-name>` is the file name without extension.
- You can override the output path with `--save` and control DPI with `--dpi`.

Examples:
```bash
# TXT input, default output: tests/plot_numbers.png
python -m benford_constants plot-file --file tests/numbers.txt

# CSV input with column
python -m benford_constants plot-file --file data/expenses.csv --column Amount

# Custom output location
python -m benford_constants plot-file --file data/metrics.txt --save tests/plot_metrics.png --dpi 200
```

## Extra examples and plots

This repo also includes a small script to generate additional Benford plots on public datasets, matching the examples in the attached guide.

Run the generator (images are saved in `tests/`):

```bash
source .venv/bin/activate
python tests/generate_plots.py
```

It will produce:

- `tests/plot_physical_constants.png`: SciPy physical constants vs Benford (from this package)
- `tests/plot_populations_2016.png`: Country populations (2016) vs Benford
- `tests/plot_uniform_1000_9999.png`: Uniform integers [1000, 9999] (non-example)
- `tests/plot_sp500_market_caps.png`: S&P 500 market caps vs Benford

### Fibonacci example

You can also generate a dataset of the first 8,999 Fibonacci numbers and plot its Benford comparison.

```bash
source .venv/bin/activate
python tests/generate_fibonacci.py
```

This will create:

- `tests/fibonacci_8999.txt`: one number per line (F(0)=1, F(1)=1, F(n+2)=F(n+1)+F(n))
- `tests/plot_fibonacci_8999.png`: Benford comparison for the Fibonacci dataset

Tip: You can manually save any plot from the CLI using `--save`, e.g. `python -m benford_constants plot --save tests/plot_physical_constants.png`.

## License (MIT)

This project is licensed under the **MIT License**. You are permitted to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, subject to the following condition: the copyright and permission notice shall be included in all copies or substantial portions of the software. THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND.

