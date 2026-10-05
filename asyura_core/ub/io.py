"""SPICE UB-file parsing."""
import re
import numpy as np

def _parse_spice_ub_from_dat(filepath):
    """
    Read a 3x3 SPICE UB matrix from a dat-file header.

    The old code assumed line 22 (Python index 21).  Here we first search
    the header for a line containing 'UBMatrix' and fall back to index 21.
    SPICE UB/B values are assumed to use reciprocal-lattice units without
    the explicit 2*pi factor, so physical Q = 2*pi*UB@hkl.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    candidates = [line for line in lines[:80] if "UBMatrix" in line]
    if candidates:
        ub_line = candidates[0]
    elif len(lines) > 21:
        ub_line = lines[21]
    else:
        raise ValueError("UBMatrix line was not found in the SPICE dat file.")

    # Extract floating-point numbers robustly, including scientific notation.
    values = re.findall(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?", ub_line)
    values = [float(x) for x in values]

    # A line label can in rare cases contain a digit; keep the last 9 values.
    if len(values) < 9:
        raise ValueError(f"UBMatrix must contain 9 numeric values: {ub_line.strip()}")
    values = values[-9:]

    UB = np.asarray(values, dtype=float).reshape(3, 3)
    if abs(np.linalg.det(UB)) < 1e-14:
        raise ValueError("Loaded UBMatrix is singular.")
    return UB
