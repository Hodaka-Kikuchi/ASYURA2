"""Array-based data processing helpers independent of Tkinter."""

from __future__ import annotations

import numpy as np
from scipy import stats


def bin_single_crystal_data(box, nv, nu, energy_list, qv_edges, qu_edges):
    """Bin single-crystal data into (energy, V, U) cells.

    This is the numerical part that used to be nested inside the GUI callback
    ``data_box``.  It has no dependency on Tkinter or GUI state.
    """
    box = np.asarray(box)
    x = box[3, :]
    y = box[1, :] / nv
    z = box[0, :] / nu

    intensity = box[4, :]
    intensity_error = box[5, :]

    energy = np.asarray(energy_list, dtype=float)

    if len(energy) != 1:
        mid_points = (energy[:-1] + energy[1:]) / 2
        x_edges = np.insert(mid_points, 0, energy[0] - (mid_points[0] - energy[0]))
        x_edges = np.append(x_edges, energy[-1] + (energy[-1] - mid_points[-1]))
    else:
        x_edges = [np.min(box[3, :]), np.max(box[3, :])]

    data = np.vstack([x, y, z]).T

    i_sum, _, _ = stats.binned_statistic_dd(
        data, intensity, statistic="sum", bins=[x_edges, qv_edges, qu_edges]
    )
    ierr_sum, _, _ = stats.binned_statistic_dd(
        data, intensity_error**2, statistic="sum", bins=[x_edges, qv_edges, qu_edges]
    )
    count, _, _ = stats.binned_statistic_dd(
        data, None, statistic="count", bins=[x_edges, qv_edges, qu_edges]
    )

    with np.errstate(divide="ignore", invalid="ignore"):
        bin_i = np.where(count != 0, i_sum / count, np.nan)
        bin_ierr = np.where(count != 0, np.sqrt(ierr_sum) / count, np.nan)

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
