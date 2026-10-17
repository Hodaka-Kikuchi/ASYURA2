"""Array-based data processing helpers independent of Tkinter."""

from __future__ import annotations

import numpy as np
from scipy import stats


def combine_normalized_points(intensity, effective_monitor, nominal_monitor,
                              return_monitor=False):
    """Combine normalized counting data by summing counts and exposure.

    Parameters
    ----------
    intensity : array-like
        Per-point intensity already normalized to ``nominal_monitor``.
        For ASYURA this is
            I_i = D_i * nominal_monitor / M_eff_i,
        where D_i is the raw detector count and M_eff_i includes the
        detector-channel sensitivity correction.
    effective_monitor : array-like
        Per-point effective monitor M_eff_i.
    nominal_monitor : float
        The nominal monitor value used when ``intensity`` was created.
    return_monitor : bool, optional
        If True, also return sum(M_eff_i) of the points that entered the bin
        (0.0 for an empty bin).  This is the weight used later when binned
        cells are combined into cuts (see ``combine_binned_cells``).

    Returns
    -------
    intensity_bin, error_bin[, monitor_sum] : float
        Ratio-of-sums intensity and its Poisson uncertainty:
            I_bin = nominal_monitor * sum(D_i) / sum(M_eff_i)
            err   = nominal_monitor * sqrt(sum(D_i)) / sum(M_eff_i)

    Notes
    -----
    Since I_i * M_eff_i = nominal_monitor * D_i, the raw counts need not
    be stored separately.  Keeping M_eff_i is sufficient, including for
    zero-count points (which still contribute exposure to the denominator).
    """
    intensity = np.asarray(intensity, dtype=float)
    effective_monitor = np.asarray(effective_monitor, dtype=float)
    nominal_monitor = float(nominal_monitor)

    if intensity.shape != effective_monitor.shape:
        raise ValueError(
            "intensity/effective_monitor shape mismatch: "
            f"{intensity.shape} vs {effective_monitor.shape}"
        )
    if not np.isfinite(nominal_monitor) or nominal_monitor <= 0:
        raise ValueError("nominal_monitor must be a positive finite number")

    def _out(i, e, m):
        return (i, e, m) if return_monitor else (i, e)

    valid = (
        np.isfinite(intensity)
        & np.isfinite(effective_monitor)
        & (effective_monitor > 0)
    )
    if not np.any(valid):
        return _out(np.nan, np.nan, 0.0)

    weighted_sum = np.sum(intensity[valid] * effective_monitor[valid])
    monitor_sum = np.sum(effective_monitor[valid])

    if not np.isfinite(weighted_sum) or monitor_sum <= 0:
        return _out(np.nan, np.nan, 0.0)

    # weighted_sum = nominal_monitor * sum(raw_counts)
    raw_counts_sum = weighted_sum / nominal_monitor
    # Detector counts should be non-negative.  Tiny negative round-off is
    # clipped; a genuinely negative value is not a valid Poisson count sum.
    if raw_counts_sum < 0:
        if np.isclose(raw_counts_sum, 0.0, atol=1e-12, rtol=1e-12):
            raw_counts_sum = 0.0
        else:
            return _out(weighted_sum / monitor_sum, np.nan, monitor_sum)

    bin_i = weighted_sum / monitor_sum
    bin_ierr = nominal_monitor * np.sqrt(raw_counts_sum) / monitor_sum
    return _out(bin_i, bin_ierr, monitor_sum)


def _window_ratio_of_sums(d_sum, m_sum, d_total, m_total, nominal_monitor):
    """Shared tail of window_bin_1d/2d: ratio of sums and Poisson error."""
    # Window sums come from differences of cumulative sums, so an empty
    # window is +-1e-16*total rather than exactly 0.  Snap those to 0.
    d_sum = np.where(np.abs(d_sum) <= 1e-12 * abs(d_total), 0.0, d_sum)
    m_sum = np.where(m_sum <= 1e-12 * abs(m_total), 0.0, m_sum)
    with np.errstate(divide="ignore", invalid="ignore"):
        bin_i = np.where(m_sum > 0, nominal_monitor * d_sum / m_sum, np.nan)
        # a genuinely negative count sum has no Poisson error (as in
        # combine_normalized_points)
        bin_e = np.where(
            (m_sum > 0) & (d_sum >= 0),
            nominal_monitor * np.sqrt(np.abs(d_sum)) / m_sum,
            np.nan,
        )
    return bin_i, bin_e, m_sum


def _valid_points(intensity, monitor, *coords):
    intensity = np.asarray(intensity, dtype=float)
    monitor = np.asarray(monitor, dtype=float)
    coords = [np.asarray(c, dtype=float) for c in coords]
    valid = np.isfinite(intensity) & np.isfinite(monitor) & (monitor > 0)
    for c in coords:
        valid &= np.isfinite(c)
    return intensity[valid], monitor[valid], [c[valid] for c in coords]


def window_bin_1d(intensity, effective_monitor, nominal_monitor, x, lo, hi):
    """Ratio-of-sums binning into (possibly overlapping) windows lo < x <= hi.

    Gives the same result as calling ``combine_normalized_points`` on the
    points of every window separately, but sorts the points once and reads
    each window from cumulative sums.  Returns (I, err, monitor_sum), each
    of length len(lo).
    """
    intensity, monitor, (x,) = _valid_points(intensity, effective_monitor, x)
    nominal_monitor = float(nominal_monitor)
    order = np.argsort(x, kind="mergesort")
    xs = x[order]
    counts = (intensity * monitor / nominal_monitor)[order]   # raw counts D
    cd = np.concatenate([[0.0], np.cumsum(counts)])
    cm = np.concatenate([[0.0], np.cumsum(monitor[order])])
    i_lo = np.searchsorted(xs, np.asarray(lo, dtype=float), side="right")
    i_hi = np.searchsorted(xs, np.asarray(hi, dtype=float), side="right")
    return _window_ratio_of_sums(cd[i_hi] - cd[i_lo], cm[i_hi] - cm[i_lo],
                                 cd[-1], cm[-1], nominal_monitor)


def window_bin_2d(intensity, effective_monitor, nominal_monitor, x, y,
                  xlo, xhi, ylo, yhi):
    """Ratio-of-sums binning into windows (xlo, xhi] x (ylo, yhi].

    Used for the smoothed single-crystal maps, where the window
    [QU[n]-dU, QU[n+1]+dU] is larger than the bin and windows overlap.
    The window edges define a fine grid; points are accumulated into it once
    and every window is read from a summed-area table (2D cumulative sum).
    The selection and statistics are identical to calling
    ``combine_normalized_points`` per window, but the cost is
    O(points + windows) instead of O(points * windows).

    Returns (I, err, monitor_sum), each of shape (len(ylo), len(xlo)).
    """
    intensity, monitor, (x, y) = _valid_points(intensity, effective_monitor, x, y)
    nominal_monitor = float(nominal_monitor)
    xlo, xhi = np.asarray(xlo, dtype=float), np.asarray(xhi, dtype=float)
    ylo, yhi = np.asarray(ylo, dtype=float), np.asarray(yhi, dtype=float)
    ex = np.unique(np.concatenate([xlo, xhi]))
    ey = np.unique(np.concatenate([ylo, yhi]))
    ncx, ncy = len(ex) - 1, len(ey) - 1

    # fine cell k holds the points with edges[k] < v <= edges[k+1]
    ix = np.searchsorted(ex, x, side="left") - 1
    iy = np.searchsorted(ey, y, side="left") - 1
    inside = (ix >= 0) & (ix < ncx) & (iy >= 0) & (iy < ncy)
    flat = iy[inside] * ncx + ix[inside]
    counts = (intensity * monitor / nominal_monitor)[inside]  # raw counts D

    def summed_area(weights):
        grid = np.bincount(flat, weights=weights, minlength=ncx * ncy)
        table = np.zeros((ncy + 1, ncx + 1))
        table[1:, 1:] = grid.reshape(ncy, ncx).cumsum(axis=0).cumsum(axis=1)
        return table

    td = summed_area(counts)
    tm = summed_area(monitor[inside])
    px0, px1 = np.searchsorted(ex, xlo), np.searchsorted(ex, xhi)
    py0, py1 = np.searchsorted(ey, ylo), np.searchsorted(ey, yhi)

    def window_sum(t):
        return t[py1][:, px1] - t[py0][:, px1] - t[py1][:, px0] + t[py0][:, px0]

    return _window_ratio_of_sums(window_sum(td), window_sum(tm),
                                 td[-1, -1], tm[-1, -1], nominal_monitor)


def group_energy_transfers(values, half_width):
    """Group measured energy transfers into representative energies.

    Sorted unique values are scanned; a value starts a new group when it lies
    outside [rep, rep + 2*half_width) of the current representative.  As in
    the original ASYURA code, the value *after* the group start is used as the
    representative when it belongs to the same group (dense data from the 24
    detector-shifted channels therefore gives exactly the previous result).

    Fixes relative to the previous inline loop:
      * a group consisting of a single value is no longer skipped (the old
        code always appended values[i+1], even when it belonged to the next
        group, so that group was lost and merged into a neighbouring bin);
      * the last group is appended exactly once (single-crystal mode used to
        drop an isolated last value; powder mode appended the last raw value
        even when it was already covered, creating a near-duplicate energy).
    """
    v = np.asarray(values, dtype=float).ravel()
    x = np.unique(v[np.isfinite(v)]).tolist()   # sorted unique values
    if not x:
        return []
    width = 2.0 * float(half_width)
    reps = [x[0]]
    for i in range(1, len(x)):
        if reps[-1] <= x[i] < reps[-1] + width:
            continue
        if i + 1 < len(x) and x[i + 1] < x[i] + width:
            reps.append(x[i + 1])
        else:
            reps.append(x[i])
    return reps


def combine_binned_cells(intensity, error, monitor=None, return_monitor=False):
    """Combine already-binned cells into one value (used for 1D/2D cuts).

    Each cell c carries I_c = N * D_c / M_c and err_c = N * sqrt(D_c) / M_c,
    where M_c is the summed effective monitor of the cell.  Weighting by M_c,

        I_cut   = sum(M_c * I_c) / sum(M_c)                = N * sum(D) / sum(M)
        err_cut = sqrt(sum(M_c**2 * err_c**2)) / sum(M_c)  = N * sqrt(sum(D)) / sum(M)

    i.e. the cut is again "add counts, add (sensitivity-normalized) monitor,
    then divide", exactly as for a single bin.  For background-subtracted or
    detailed-balance-scaled cells the same weights give the correct linear
    error propagation.

    Cells with non-finite intensity/error, or with no foreground exposure
    (monitor <= 0), are skipped.  If ``monitor`` is None, every finite cell
    gets weight 1 (plain mean, error sqrt(sum err^2)/n).
    """
    intensity = np.asarray(intensity, dtype=float).ravel()
    error = np.asarray(error, dtype=float).ravel()
    if monitor is None:
        weight = np.ones_like(intensity)
    else:
        weight = np.asarray(monitor, dtype=float).ravel()
    if not (intensity.shape == error.shape == weight.shape):
        raise ValueError(
            "intensity/error/monitor shape mismatch: "
            f"{intensity.shape}, {error.shape}, {weight.shape}"
        )

    valid = (
        np.isfinite(intensity)
        & np.isfinite(error)
        & np.isfinite(weight)
        & (weight > 0)
    )
    if not np.any(valid):
        return (np.nan, np.nan, 0.0) if return_monitor else (np.nan, np.nan)

    w = weight[valid]
    w_sum = np.sum(w)
    cut_i = np.sum(w * intensity[valid]) / w_sum
    cut_err = np.sqrt(np.sum((w * error[valid]) ** 2)) / w_sum
    if return_monitor:
        return cut_i, cut_err, w_sum
    return cut_i, cut_err


def cell_monitor(state, intensity_key="I", monitor_key=None):
    """Return the per-cell monitor array that belongs to ``state[intensity_key]``.

    Falls back to None (equal weights) when the monitor array is missing or
    does not match the intensity array, e.g. for state saved by an older run.
    """
    if monitor_key is None:
        monitor_key = {"I": "Imon", "Ipow": "Ipow_mon"}.get(intensity_key)
    intensity = state.get(intensity_key)
    monitor = state.get(monitor_key) if monitor_key else None
    if intensity is None or monitor is None:
        return None
    monitor = np.asarray(monitor, dtype=float)
    if monitor.shape != np.shape(intensity):
        return None
    return monitor


def combine_state_cells(state, select, intensity_key="I", error_key=None):
    """Monitor-weighted combination of a selection of binned map cells.

    ``select`` is a function applied identically to the intensity, error and
    monitor arrays (e.g. ``lambda a: a[ll, v0:v1, u0:u1]``).
    """
    if error_key is None:
        error_key = {"I": "Ierr", "Ipow": "Ipow_err"}[intensity_key]
    monitor = cell_monitor(state, intensity_key)
    return combine_binned_cells(
        select(state[intensity_key]),
        select(state[error_key]),
        None if monitor is None else select(monitor),
    )


def bin_single_crystal_data(
    box,
    effective_monitor,
    nominal_monitor,
    nv,
    nu,
    energy_list,
    qv_edges,
    qu_edges,
    return_monitor=False,
):
    """Bin single-crystal data into (energy, V, U) cells.

    The point intensities in ``box[4, :]`` are already normalized to the
    common nominal monitor.  Binning is therefore performed by reconstructing
    the summed raw counts through ``I_i * M_eff_i`` and dividing by the summed
    effective monitor, rather than by taking an arithmetic mean of the
    normalized points.

    If ``return_monitor`` is True, the summed effective monitor of every cell
    is returned as a third array (0 for empty cells).
    """
    box = np.asarray(box)
    effective_monitor = np.asarray(effective_monitor, dtype=float)
    nominal_monitor = float(nominal_monitor)

    x = box[3, :]
    y = box[1, :] / nv
    z = box[0, :] / nu
    intensity = box[4, :]

    if effective_monitor.shape != intensity.shape:
        raise ValueError(
            "box/effective_monitor length mismatch: "
            f"{intensity.shape} vs {effective_monitor.shape}"
        )
    if not np.isfinite(nominal_monitor) or nominal_monitor <= 0:
        raise ValueError("nominal_monitor must be a positive finite number")

    energy = np.asarray(energy_list, dtype=float)

    if len(energy) != 1:
        mid_points = (energy[:-1] + energy[1:]) / 2
        x_edges = np.insert(mid_points, 0, energy[0] - (mid_points[0] - energy[0]))
        x_edges = np.append(x_edges, energy[-1] + (energy[-1] - mid_points[-1]))
    else:
        x_edges = [np.min(box[3, :]), np.max(box[3, :])]

    data = np.vstack([x, y, z]).T

    valid = (
        np.all(np.isfinite(data), axis=1)
        & np.isfinite(intensity)
        & np.isfinite(effective_monitor)
        & (effective_monitor > 0)
    )

    data_valid = data[valid]
    intensity_valid = intensity[valid]
    monitor_valid = effective_monitor[valid]

    # I_i * M_eff_i = nominal_monitor * D_i.
    weighted_intensity = intensity_valid * monitor_valid

    weighted_sum, _, _ = stats.binned_statistic_dd(
        data_valid,
        weighted_intensity,
        statistic="sum",
        bins=[x_edges, qv_edges, qu_edges],
    )
    monitor_sum, _, _ = stats.binned_statistic_dd(
        data_valid,
        monitor_valid,
        statistic="sum",
        bins=[x_edges, qv_edges, qu_edges],
    )

    with np.errstate(divide="ignore", invalid="ignore"):
        bin_i = np.where(
            monitor_sum > 0,
            weighted_sum / monitor_sum,
            np.nan,
        )

        raw_counts_sum = weighted_sum / nominal_monitor
        raw_counts_sum = np.where(
            (raw_counts_sum >= 0) | np.isclose(raw_counts_sum, 0.0, atol=1e-12, rtol=1e-12),
            np.maximum(raw_counts_sum, 0.0),
            np.nan,
        )
        bin_ierr = np.where(
            monitor_sum > 0,
            nominal_monitor * np.sqrt(raw_counts_sum) / monitor_sum,
            np.nan,
        )

    if return_monitor:
        return bin_i, bin_ierr, np.asarray(monitor_sum, dtype=float)
    return bin_i, bin_ierr


def get_single_crystal_map_energy_axis(state):
    """Return the energy axis that belongs to ``state['I']`` / ``state['Ierr']``.

    The returned array is validated against the first dimension of the map.
    """
    if state.get("I") is None or state.get("Ierr") is None:
        raise ValueError("Single-crystal intensity map has not been created yet.")

    n_energy = int(state["I"].shape[0])
    if state["Ierr"].shape[0] != n_energy:
        raise ValueError(
            "I/Ierr energy-axis mismatch: "
            f"I.shape={state['I'].shape}, Ierr.shape={state['Ierr'].shape}"
        )

    axis = state.get("map_energylist")
    if axis is None:
        current = np.asarray(state.get("energylist", []), dtype=float)
        if len(current) == n_energy:
            axis = current.copy()
            state["map_energylist"] = axis
        else:
            raise ValueError(
                "Energy axis for the single-crystal map is unavailable: "
                f"I.shape[0]={n_energy}, len(energylist)={len(current)}. "
                "Please recreate the data box once."
            )
    else:
        axis = np.asarray(axis, dtype=float)

    if len(axis) != n_energy:
        raise ValueError(
            "Single-crystal map energy-axis mismatch: "
            f"I.shape[0]={n_energy}, len(map_energylist)={len(axis)}. "
            "Please recreate the data box once."
        )

    return axis
