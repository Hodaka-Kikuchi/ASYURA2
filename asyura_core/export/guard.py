"""Make 'Save Data' menu items tell the user when there is nothing to save yet.

Each exporter reads fixed results from ``state`` (e.g. ``state['I_hwV']``).
Without this guard, choosing a save item before the corresponding plot had
been drawn raised KeyError *after* the file dialog, so the menu appeared to do
nothing (and could leave an empty file behind).

The keys each exporter needs are listed in REQUIRED_STATE_KEYS below.  They
are deliberately a fixed table: the stand-alone (PyInstaller) app ships
without .py sources, so reading the exporters' source at run time is not
possible.  tests/test_counting_statistics.py checks that this table still
matches the exporters' source; update it when an exporter changes.
"""

import functools

from tkinter import messagebox

REQUIRED_STATE_KEYS = {
    'save_1DI_U': ('Erange_1d_IvsU', 'I_1DU', 'Ierr_1DU', 'Ulabel', 'Urange_1d_IvsU', 'Vlabel', 'Vrange_1d_IvsU'),
    'save_1DI_V': ('Erange_1d_IvsV', 'I_1DV', 'Ierr_1DV', 'Ulabel', 'Urange_1d_IvsV', 'Vlabel', 'Vrange_1d_IvsV'),
    'save_1D_hwI_pow': ('Ipow_1dei', 'Ipowerr_1dei', 'elist', 'qlist'),
    'save_1D_qI_pow': ('Ipow_1dqi', 'Ipowerr_1dqi', 'elist2', 'qlist2'),
    'save_1Dhw_I': ('Erange_1d_Ivshw', 'I_hw1d2', 'Ierr_hw1d2', 'Ulabel', 'Urange_1d_Ivshw', 'Vlabel', 'Vrange_1d_Ivshw'),
    'save_2D_hw_qmap': ('Ipow', 'Ipow_err', 'Q2', 'energylist'),
    'save_BGdata': ('sb_databox',),
    'save_FGdata': ('databox',),
    'save_I_HKL': ('I_1d_IvsHKL_E', 'I_1d_IvsHKL_HKL', 'I_1d_IvsHKL_hkl', 'I_1d_alongQ', 'I_1d_alongQ_err', 'Ulabel', 'Vlabel'),
    'save_I_hw': ('I_1d_Ivshw_E', 'I_1d_Ivshw_HKL', 'I_1d_Ivshw_hkl', 'I_1d_alongE', 'I_1d_alongE_err'),
    'save_constEmap': ('Erange_2d_VvsU', 'I_ce', 'Ierr_ce', 'Ulabel', 'Urange_2d_VvsU', 'Vlabel', 'Vrange_2d_VvsU'),
    'save_hkl_HKL': ('E_I_ce', 'I_ce_adv', 'Ierr_ce_adv', 'table_2DX', 'table_2DY'),
    'save_hw_HKL': ('I_cq', 'I_cq_err', 'energylist', 'table_2D', 'table_2D_qrange'),
    'save_hw_Umap': ('Erange_2d_UvsE', 'I_hwU', 'Ierr_hwU', 'Ulabel', 'Urange_2d_UvsE', 'Vlabel', 'Vrange_2d_UvsE'),
    'save_hw_Vmap': ('Erange_2d_VvsE', 'I_hwV', 'Ierr_hwV', 'Ulabel', 'Urange_2d_VvsE', 'Vlabel', 'Vrange_2d_VvsE'),
    'save_masked_2dcE_data': ('Ulabel', 'Vlabel', 'masked_2d_constE'),
    'save_masked_2dcU_data': ('Ulabel', 'Vlabel', 'masked_2d_constU'),
    'save_masked_2dcV_data': ('Ulabel', 'Vlabel', 'masked_2d_constV'),
    'save_masked_3d_data': ('Ulabel', 'Vlabel', 'masked_3d_databox'),
}

# Friendlier hints for a few keys; everything else gets the generic message.
_HINTS = {
    "databox": "Load data files first ('load data file(s)').",
    "sb_databox": "No background data is loaded. Select background file(s) and load again.",
}


def requires_results(func):
    keys = REQUIRED_STATE_KEYS.get(func.__name__, ())

    @functools.wraps(func)
    def wrapper(state, *args, **kwargs):
        missing = [k for k in keys if state.get(k) is None]
        if missing:
            hint = next((_HINTS[k] for k in missing if k in _HINTS), None)
            messagebox.showinfo(
                "ASYURA",
                hint or "Nothing to save yet.\n"
                        "Please draw the corresponding plot first, then save.",
            )
            return None
        return func(state, *args, **kwargs)

    wrapper.required_state_keys = keys
    return wrapper
