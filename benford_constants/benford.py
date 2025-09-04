from __future__ import annotations

from math import log10
from typing import Dict, Iterable, List, Mapping, Tuple

import numpy as np


def leading_digit(x: float) -> int:
    """
    Return the leading (most significant) decimal digit of a positive number.

    For x <= 0 or non-finite, raises ValueError.
    """
    if not np.isfinite(x) or x <= 0:
        raise ValueError("leading_digit expects a positive, finite number")
    # Normalize to [1, 10)
    mantissa = x
    # Use scientific notation via log10 for robustness on wide ranges
    exp = int(np.floor(np.log10(mantissa)))
    mantissa /= 10 ** exp
    return int(str(mantissa)[0]) if mantissa < 10 else int(str(mantissa)[0])


def _leading_digits_vector(values: Iterable[float]) -> np.ndarray:
    arr = np.asarray(list(values), dtype=float)
    arr = np.abs(arr)
    arr = arr[np.isfinite(arr) & (arr > 0)]
    if arr.size == 0:
        return np.array([], dtype=int)
    exps = np.floor(np.log10(arr))
    mantissas = arr / (10 ** exps)
    # Convert leading digit by floor of mantissa in [1,10)
    # Add tiny epsilon to handle floating errors like 9.999999 -> 10
    eps = 1e-12
    leading = np.floor(mantissas + eps).astype(int)
    # Clamp to [1,9]
    leading = np.minimum(np.maximum(leading, 1), 9)
    return leading


def _leading_digit_from_any(value: float) -> int | None:
    """Return leading digit for ints or floats; supports arbitrarily large ints.

    Returns None for invalid values (non-finite, <= 0).
    """
    # Handle Python and NumPy integers without float conversion
    if isinstance(value, (int, np.integer)):
        n = int(value)
        if n == 0:
            return None
        n = abs(n)
        return int(str(n)[0])
    # Fallback: treat as float-like
    try:
        xf = float(value)
    except Exception:
        return None
    if not np.isfinite(xf) or xf <= 0:
        return None
    # Use scientific notation to robustly extract first significant digit
    s = f"{abs(xf):.15e}"  # e.g., '1.234567890123457e+10'
    return int(s[0])


def digit_frequencies(values: Iterable[float]) -> Dict[int, float]:
    """
    Compute observed frequency distribution of leading digits (1..9).

    Returns mapping digit -> probability (summing to 1). If no valid values,
    returns a uniform zero distribution.
    """
    counts = {d: 0 for d in range(1, 10)}
    total_int = 0
    for v in values:
        d = _leading_digit_from_any(v)
        if d is None:
            continue
        if 1 <= d <= 9:
            counts[d] += 1
            total_int += 1
    if total_int == 0:
        return {d: 0.0 for d in range(1, 10)}
    total = float(total_int)
    return {d: counts[d] / total for d in range(1, 10)}


def benford_expected() -> Dict[int, float]:
    """Return Benford expected probabilities for digits 1..9: log10(1 + 1/d)."""
    return {d: log10(1 + 1 / d) for d in range(1, 10)}


def frequencies_table(values: Iterable[float]) -> List[Tuple[int, int, float]]:
    """
    Return a list of rows (digit, count, probability) for 1..9.
    """
    leading = _leading_digits_vector(values)
    counts = {d: 0 for d in range(1, 10)}
    unique, cnts = np.unique(leading, return_counts=True) if leading.size else ([], [])
    for d, c in zip(list(map(int, unique)), list(map(int, cnts))):
        counts[d] = c
    total = max(int(leading.size), 1)
    rows: List[Tuple[int, int, float]] = []
    for d in range(1, 10):
        c = counts[d]
        rows.append((d, c, c / total))
    return rows


