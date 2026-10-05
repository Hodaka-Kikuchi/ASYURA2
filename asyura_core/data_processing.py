"""Array-based data processing helpers independent of Tkinter."""

from __future__ import annotations

import numpy as np
from scipy import stats


def combine_normalized_points(intensity, effective_monitor, nominal_monitor):
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

    Returns
    -------
    intensity_bin, error_bin : float
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

    valid = (
        np.isfinite(intensity)
        & np.isfinite(effective_monitor)
        & (effective_monitor > 0)
    )
    if not np.any(valid):
        return np.nan, np.nan

    weighted_sum = np.sum(intensity[valid] * effective_monitor[valid])
    monitor_sum = np.sum(effective_monitor[valid])

    if not np.isfinite(weighted_sum) or monitor_sum <= 0:
        return np.nan, np.nan

    # weighted_sum = nominal_monitor * sum(raw_counts)
    raw_counts_sum = weighted_sum / nominal_monitor
    # Detector counts should be non-negative.  Tiny negative round-off is
    # clipped; a genuinely negative value is not a valid Poisson count sum.
    if raw_counts_sum < 0:
        if np.isclose(raw_counts_sum, 0.0, atol=1e-12, rtol=1e-12):
            raw_counts_sum = 0.0
        else:
            return weighted_sum / monitor_sum, np.nan

    bin_i = weighted_sum / monitor_sum
    bin_ierr = nominal_monitor * np.sqrt(raw_counts_sum) / monitor_sum
    return bin_i, bin_ierr


def bin_single_crystal_data(
    box,
    effective_monitor,
    nominal_monitor,
    nv,
    nu,
    energy_list,
    qv_edges,
    qu_edges,
):
    """Bin single-crystal data into (energy, V, U) cells.

    The point intensities in ``box[4, :]`` are already normalized to the
    common nominal monitor.  Binning is therefore performed by reconstructing
    the summed raw counts through ``I_i * M_eff_i`` and dividing by the summed
    effective monitor, rather than by taking an arithmetic mean of the
    normalized points.
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
