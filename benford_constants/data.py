from typing import Dict, List, Tuple

from scipy import constants


def load_physical_constants_values() -> List[float]:
    """
    Return numeric values of SciPy physical constants.

    Uses constants.physical_constants: mapping name -> (value, unit, uncertainty)
    Returns only finite numeric values.
    """
    values: List[float] = []
    for spec in constants.physical_constants.values():
        try:
            value = float(spec[0])
        except Exception:
            continue
        if value != 0.0 and value == value:  # exclude NaN and zero
            values.append(abs(value))
    return values


def load_physical_constants_table() -> List[Tuple[str, float, str, float]]:
    """Return a list of (name, value, unit, uncertainty)."""
    rows: List[Tuple[str, float, str, float]] = []
    for name, spec in constants.physical_constants.items():
        try:
            value = float(spec[0])
            unit = str(spec[1])
            uncertainty = float(spec[2])
        except Exception:
            continue
        rows.append((name, value, unit, uncertainty))
    return rows
