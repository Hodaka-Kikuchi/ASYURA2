"""Counting-statistics checks for ASYURA binning and cuts.

Reference definition (what the paper states):
    the counts in a bin are added, sqrt(added counts) is the error, and both
    are divided by the total added monitor, where the monitor of each point is
    normalized to the sensitivity of its detector channel.

    I   = N * sum(D) / sum(M_eff)
    err = N * sqrt(sum(D)) / sum(M_eff),      M_eff = mcu * v_m / v_ref

Run with pytest, or directly:  python tests/test_counting_statistics.py
"""

import sys
import types
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from asyura_core.data_processing import (  # noqa: E402
    bin_single_crystal_data,
    combine_binned_cells,
    combine_normalized_points,
    combine_state_cells,
)

N_MCU = 1.0e5


# ----------------------------------------------------------------------------
# synthetic data in the same layout as loading.py
# ----------------------------------------------------------------------------
def _points(rng, n, energies, qu_range=(-1.0, 1.0), qv_range=(-1.0, 1.0)):
    """Return raw counts D, effective monitor M_eff and a databox (rows 0..5)."""
    D = rng.poisson(rng.uniform(0.5, 20.0, n)).astype(float)
    mcu = rng.uniform(5e4, 3e5, n)
    sens = rng.uniform(0.6, 1.4, n)          # v_m / v_ref of each channel
    M = mcu * sens
    box = np.zeros((6, n))
    box[0] = rng.uniform(*qu_range, n)       # U (already alpha*|qU|, NU1=1 below)
    box[1] = rng.uniform(*qv_range, n)       # V
    box[2] = np.hypot(box[0], box[1])        # |Q| for powder
    box[3] = rng.choice(energies, n)         # energy transfer
    box[4] = D * N_MCU / M                   # normalized intensity (loading.py)
    box[5] = np.sqrt(D) * N_MCU / M          # its error
    return D, M, box


def _ref(D, M):
    return N_MCU * D.sum() / M.sum(), N_MCU * np.sqrt(D.sum()) / M.sum()


# ----------------------------------------------------------------------------
# core functions
# ----------------------------------------------------------------------------
def test_point_combination_is_ratio_of_sums():
    rng = np.random.default_rng(1)
    D, M, box = _points(rng, 50, [0.0])
    i, e, m = combine_normalized_points(box[4], M, N_MCU, return_monitor=True)
    ri, re = _ref(D, M)
    assert np.isclose(i, ri) and np.isclose(e, re) and np.isclose(m, M.sum())


def test_zero_count_points_still_add_monitor():
    D = np.array([0.0, 0.0, 4.0])
    M = np.array([1e5, 2e5, 1e5])
    i, e = combine_normalized_points(D * N_MCU / M, M, N_MCU)
    assert np.isclose(i, N_MCU * 4 / 4e5) and np.isclose(e, N_MCU * 2 / 4e5)


def test_cut_over_cells_equals_ratio_of_sums_over_all_points():
    """Combining binned cells must give the same result as adding the raw
    counts and monitors of every point that fell into those cells."""
    rng = np.random.default_rng(2)
    energies = [0.5, 1.0, 1.5]
    D, M, box = _points(rng, 4000, energies)
    qu = np.linspace(-1, 1, 11)
    qv = np.linspace(-1, 1, 9)
    I, E, Mon = bin_single_crystal_data(
        box, M, N_MCU, 1.0, 1.0, energies, qv, qu, return_monitor=True)

    # a 1D cut: energy index 1, V cells 2..5, U cells 3..7
    sel = lambda a: a[1, 2:6, 3:8]
    ci, ce = combine_binned_cells(sel(I), sel(E), sel(Mon))

    pick = ((box[3] == 1.0)
            & (box[1] > qv[2]) & (box[1] <= qv[6])
            & (box[0] > qu[3]) & (box[0] <= qu[8]))
    ri, re = _ref(D[pick], M[pick])
    assert np.isclose(ci, ri, rtol=1e-12) and np.isclose(ce, re, rtol=1e-12)

    # via the state helper used by the GUI
    state = {"I": I, "Ierr": E, "Imon": Mon}
    si, se = combine_state_cells(state, sel)
    assert np.isclose(si, ri) and np.isclose(se, re)


def test_cut_falls_back_to_plain_mean_without_monitor():
    I = np.array([1.0, 3.0, np.nan])
    E = np.array([0.3, 0.4, 0.1])
    i, e = combine_binned_cells(I, E, None)
    assert np.isclose(i, 2.0) and np.isclose(e, 0.5 / 2)


def test_background_subtracted_cut_propagates_errors_linearly():
    """For I_c = FG_c - BG_c with weights w_c, the cut must equal
    sum(w FG)/sum(w) - sum(w BG)/sum(w) with quadrature-propagated errors."""
    rng = np.random.default_rng(3)
    fg = rng.uniform(1, 5, 8); fge = rng.uniform(0.1, 0.5, 8)
    bg = rng.uniform(0, 1, 8); bge = rng.uniform(0.05, 0.2, 8)
    w = rng.uniform(1e5, 5e5, 8)
    i, e = combine_binned_cells(fg - bg, np.hypot(fge, bge), w)
    W = w.sum()
    assert np.isclose(i, (w * fg).sum() / W - (w * bg).sum() / W)
    assert np.isclose(e, np.sqrt((w**2 * (fge**2 + bge**2)).sum()) / W)


def test_cut_counts_cells_correctly_for_1d_selection():
    """Regression: the Q-E path cut used to count only every other cell
    (np.ravel(...)[::2] on a 1D selection) and to add errors linearly."""
    I = np.arange(2 * 5 * 3, dtype=float).reshape(2, 5, 3) + 1
    E = np.full_like(I, 0.5)
    state = {"I": I, "Ierr": E}
    i, e = combine_state_cells(state, lambda a: a[:, :, 0:3][0, [0, 1, 2, 3], 1])
    assert np.isclose(i, np.mean([2, 5, 8, 11]))
    assert np.isclose(e, np.sqrt(4 * 0.25) / 4)


# ----------------------------------------------------------------------------
# windowed (smoothed) binning via cumulative sums
# ----------------------------------------------------------------------------
def _brute_windows_2d(I, M, x, y, xlo, xhi, ylo, yhi):
    out = np.full((3, len(ylo), len(xlo)), np.nan)
    for j in range(len(ylo)):
        for i in range(len(xlo)):
            s = (xlo[i] < x) & (x <= xhi[i]) & (ylo[j] < y) & (y <= yhi[j])
            out[:, j, i] = combine_normalized_points(I[s], M[s], N_MCU, return_monitor=True)
    return out


def test_window_bin_2d_matches_per_window_loop_including_edges():
    from asyura_core.data_processing import window_bin_2d
    rng = np.random.default_rng(21)
    for dU, dV in [(0.0, 0.0), (0.05, 0.025), (0.137, 0.1)]:
        QU = np.round(np.arange(-1.0, 1.0001, 0.1), 6)
        QV = np.round(np.arange(-0.6, 0.6001, 0.1), 6)
        xlo, xhi, ylo, yhi = QU[:-1] - dU, QU[1:] + dU, QV[:-1] - dV, QV[1:] + dV
        n = 2000
        x = rng.uniform(-1.3, 1.3, n)
        y = rng.uniform(-0.9, 0.9, n)
        x[:300] = rng.choice(np.concatenate([xlo, xhi]), 300)   # exactly on edges
        y[:150] = rng.choice(np.concatenate([ylo, yhi]), 150)
        D = rng.poisson(rng.uniform(0, 3, n)).astype(float)      # includes zero counts
        M = rng.uniform(5e3, 2e4, n)
        M[:20] = 0.0                                              # invalid monitor
        I = np.where(M > 0, D * N_MCU / np.where(M > 0, M, 1.0), np.nan)
        I[20:40] = np.nan
        got = np.array(window_bin_2d(I, M, N_MCU, x, y, xlo, xhi, ylo, yhi))
        ref = _brute_windows_2d(I, M, x, y, xlo, xhi, ylo, yhi)
        assert np.allclose(got[:2], ref[:2], rtol=1e-10, atol=1e-12, equal_nan=True)
        assert np.allclose(got[2], ref[2], rtol=1e-10, atol=1e-6)


def test_window_bin_1d_matches_per_window_loop_including_edges():
    from asyura_core.data_processing import window_bin_1d
    rng = np.random.default_rng(22)
    Q = np.round(np.arange(0.1, 2.0001, 0.05), 6)
    for dQ in (0.0, 0.03, 0.11):
        lo, hi = Q[:-1] - dQ, Q[1:] + dQ
        q = rng.uniform(0, 2.3, 3000)
        q[:400] = rng.choice(np.concatenate([lo, hi]), 400)
        D = rng.poisson(2.0, 3000).astype(float)
        M = rng.uniform(5e3, 2e4, 3000)
        I = D * N_MCU / M
        gi, ge, gm = window_bin_1d(I, M, N_MCU, q, lo, hi)
        for k in range(len(lo)):
            s = (lo[k] < q) & (q <= hi[k])
            ri, re, rm = combine_normalized_points(I[s], M[s], N_MCU, return_monitor=True)
            assert np.allclose([gi[k], ge[k]], [ri, re], rtol=1e-10, equal_nan=True)
            assert np.isclose(gm[k], rm, rtol=1e-10, atol=1e-6)


def test_window_bin_handles_empty_input():
    from asyura_core.data_processing import window_bin_1d, window_bin_2d
    e = np.array([])
    i, err, m = window_bin_2d(e, e, N_MCU, e, e, [0.0, 0.1], [0.1, 0.2], [0.0], [0.1])
    assert i.shape == (1, 2) and np.all(np.isnan(i)) and np.all(m == 0)
    i, err, m = window_bin_1d(e, e, N_MCU, e, [0.0], [0.1])
    assert np.isnan(i[0]) and m[0] == 0


# ----------------------------------------------------------------------------
# automatic energy axis
# ----------------------------------------------------------------------------
def _old_single_crystal_grouping(values, E_T):
    """Verbatim copy of the loop previously in callbacks/data/binning.py."""
    el = sorted(set(values))
    Energylist = [el[0]]
    for i in range(1, (len(el) - 1)):
        if Energylist[-1] <= el[i] and el[i] < Energylist[-1] + 2 * E_T:
            pass
        else:
            Energylist.append(el[i + 1])
    if Energylist[-1] < el[-1] + 2 * E_T:
        pass
    else:
        Energylist.append(el[-1])
    return sorted(set(Energylist))


def test_energy_grouping_unchanged_for_dense_detector_data():
    from asyura_core.data_processing import group_energy_transfers
    rng = np.random.default_rng(6)
    offsets = rng.normal(0, 0.01, 24)          # per-channel Ef calibration
    for _ in range(20):
        scan = np.round(np.arange(-1.0, 5.0, rng.choice([0.25, 0.5])), 3)
        values = (scan[:, None] - offsets[None, :]).ravel()
        E_T = 0.055
        new = group_energy_transfers(values, E_T)
        assert np.allclose(new, _old_single_crystal_grouping(values, E_T))
        assert len(new) == len(scan)


def test_energy_grouping_keeps_isolated_values():
    from asyura_core.data_processing import group_energy_transfers
    values = [0.5, 1.0, 1.5, 2.0]
    assert _old_single_crystal_grouping(values, 0.1) == [0.5, 1.5]   # old bug
    assert group_energy_transfers(values, 0.1) == values
    # powder used to add the last raw value again (near-duplicate energy)
    dense_end = [0.49, 0.5, 0.51, 1.99, 2.0, 2.01]
    assert group_energy_transfers(dense_end, 0.1) == [0.49, 2.0]


# ----------------------------------------------------------------------------
# save-menu guard: its fixed key table must match the exporters' source
# ----------------------------------------------------------------------------
def test_export_guard_table_matches_exporter_source():
    """guard.REQUIRED_STATE_KEYS is a fixed table (the frozen app has no .py
    sources to inspect).  Re-derive it from the exporter sources here."""
    import ast
    export_dir = ROOT / "asyura_core" / "export"
    derived = {}
    for path in sorted(export_dir.glob("*.py")):
        if path.name in ("__init__.py", "guard.py"):
            continue
        for node in ast.parse(path.read_text(encoding="utf-8")).body:
            if isinstance(node, ast.FunctionDef) and node.name.startswith("save_"):
                derived[node.name] = tuple(sorted({
                    n.slice.value for n in ast.walk(node)
                    if isinstance(n, ast.Subscript) and isinstance(n.value, ast.Name)
                    and n.value.id == "state" and isinstance(n.slice, ast.Constant)
                    and isinstance(n.slice.value, str)}))
    guard_src = (export_dir / "guard.py").read_text(encoding="utf-8")
    table = next(ast.literal_eval(n.value) for n in ast.parse(guard_src).body
                 if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "REQUIRED_STATE_KEYS")
    assert table == derived


def test_shipped_modules_do_not_read_their_own_source():
    """PyInstaller apps contain only bytecode: inspect.getsource() etc. fail there."""
    for path in list((ROOT / "asyura_core").rglob("*.py")) + list((ROOT / "asyura_gui").rglob("*.py")):
        text = path.read_text(encoding="utf-8")
        for bad in ("inspect.getsource", "getsourcelines", "inspect.findsource"):
            assert bad not in text, f"{path.relative_to(ROOT)} uses {bad}"


# ----------------------------------------------------------------------------
# GUI callbacks end to end (tkinter widgets replaced by tiny fakes)
# ----------------------------------------------------------------------------
def _import_callbacks():
    """Import GUI callbacks; stub tkinter/sympy only if they are missing."""
    for name in ("tkinter",):
        try:
            __import__(name)
        except ImportError:
            tk = types.ModuleType("tkinter")
            for sub in ("ttk", "filedialog", "messagebox", "simpledialog"):
                m = types.ModuleType("tkinter." + sub)
                setattr(tk, sub, m)
                sys.modules["tkinter." + sub] = m
            sys.modules["tkinter"] = tk
            bt = types.ModuleType("matplotlib.backends.backend_tkagg")
            bt.FigureCanvasTkAgg = object
            sys.modules["matplotlib.backends.backend_tkagg"] = bt
    try:
        import sympy  # noqa: F401
    except ImportError:
        sm = types.ModuleType("sympy")
        sm.init_printing = lambda *a, **k: None
        sm.Symbol = lambda s: s
        sys.modules["sympy"] = sm
    import matplotlib
    _use = matplotlib.use
    matplotlib.use = lambda *a, **k: None   # keep the headless backend
    try:
        from asyura_gui.callbacks.data.binning import data_box
        from asyura_gui.callbacks.powder.data import pow_data_box
    finally:
        matplotlib.use = _use
    return data_box, pow_data_box


class _V:
    def __init__(self, v):
        self.v = v

    def get(self):
        return self.v


class _PB(dict):
    def update(self):
        pass


def _base_state(box, M):
    return {
        "databox": box.copy(), "monitorbox": M.copy(),
        "sb_databox": None, "sb_monitorbox": None, "sbfile_paths": [],
        "N_mcu": N_MCU, "NU1": 1.0, "NV1": 1.0, "ef_tol": 0.05,
        "pb2": _PB(), "pb3": _PB(),
    }


def test_single_crystal_data_box_with_smoothing_records_monitor():
    data_box, _ = _import_callbacks()
    rng = np.random.default_rng(4)
    energies = [0.5, 1.0, 1.5, 2.0]
    D, M, box = _points(rng, 4000, energies)
    state = _base_state(box, M)
    env = {
        "state": state, "CSX": _V(1), "hw_nan": _V(0), "sbtype2": _V(0),
        "sb_txt1": _V("1"), "sb_txt2": _V("1"), "sb_txt3": _V("1"),
        "fgt_txt1": _V("0.1"), "bgt_txt1": _V(""),
        "fgt_txt2": _V("0.4"), "fgt_txt3": _V(""),      # smoothing along U
        "bgt_txt2": _V(""), "bgt_txt3": _V(""),
        "txt16": _V("-0.9"), "txt17": _V("0.9"), "txt18": _V("0.2"),
        "txt19": _V("-0.9"), "txt20": _V("0.9"), "txt21": _V("0.2"),
        "txt22": _V(""), "txt23": _V(""), "txt24": _V(""), "i": None,
    }
    data_box(env)
    assert state["Imon"].shape == state["I"].shape
    # each smoothed cell must itself be the ratio of sums of its points
    ne = int(np.argmin(np.abs(np.asarray(state["energylist"]) - 1.0)))
    assert np.isclose(state["energylist"][ne], 1.0)
    ny, nx = 3, 4
    QU, QV = state["QU"], state["QV"]
    dU = (0.4 - 0.2) / 2
    pick = ((np.abs(box[3] - 1.0) < 0.1)
            & (QU[nx] - dU < box[0]) & (box[0] <= QU[nx + 1] + dU)
            & (QV[ny] < box[1]) & (box[1] <= QV[ny + 1]))
    ri, re = _ref(D[pick], M[pick])
    assert np.isclose(state["I"][ne, ny, nx], ri)
    assert np.isclose(state["Ierr"][ne, ny, nx], re)
    assert np.isclose(state["Imon"][ne, ny, nx], M[pick].sum())


def test_powder_binning_is_ratio_of_sums():
    _, pow_data_box = _import_callbacks()
    rng = np.random.default_rng(5)
    energies = [0.5, 1.0]
    D, M, box = _points(rng, 3000, energies)
    state = _base_state(box, M)
    env = {
        "state": state, "CSX": _V(1), "hwp_nan": _V(0), "sbtype2": _V(0),
        "sb_txt1": _V("1"), "sb_txt2": _V("1"), "sb_txt3": _V("1"),
        "fgt_txt1": _V("0.1"), "bgt_txt1": _V(""),
        "fgt_txt4": _V(""), "bgt_txt6": _V(""),
        "txt01_p": _V("0.1"), "txt02_p": _V("1.3"), "txt03_p": _V("0.2"),
        "txt04_p": _V(""), "txt05_p": _V(""), "txt06_p": _V(""), "i": None,
    }
    pow_data_box(env)
    Q = state["Q"]
    for ne, e in enumerate(energies):
        for nq in range(len(Q) - 1):
            pick = (box[3] == e) & (Q[nq] < box[2]) & (box[2] <= Q[nq + 1])
            if not pick.any():
                assert np.isnan(state["Ipow"][ne, nq])
                continue
            ri, re = _ref(D[pick], M[pick])
            assert np.isclose(state["Ipow"][ne, nq], ri)
            assert np.isclose(state["Ipow_err"][ne, nq], re)
            assert np.isclose(state["Ipow_mon"][ne, nq], M[pick].sum())

    # and a 1D cut over several |Q| cells is again a ratio of sums
    sel = lambda a: a[0, 1:4]
    ci, ce = combine_state_cells(state, sel, "Ipow")
    pick = (box[3] == energies[0]) & (Q[1] < box[2]) & (box[2] <= Q[4])
    ri, re = _ref(D[pick], M[pick])
    assert np.isclose(ci, ri) and np.isclose(ce, re)


def _chi_env(state, mode_key, extra):
    env = {"state": state, "CSX": _V(2), mode_key: _V(0), "sbtype2": _V(0),
           "sb_txt1": _V("1"), "sb_txt2": _V("10"), "sb_txt3": _V("10"),
           "fgt_txt1": _V("0.1"), "bgt_txt1": _V(""), "i": None}
    env.update(extra)
    return env


def test_chi_detailed_balance_is_odd_in_energy_in_both_modes():
    """chi'' = S * (1 - exp(-E/kT)) for both signs of E, in single-crystal and
    powder mode alike (powder used to flip the sign for E < 0)."""
    _, pow_data_box = _import_callbacks()
    data_box, _ = _import_callbacks()
    rng = np.random.default_rng(31)
    energies = [-1.0, -0.5, 0.5, 1.0]
    D, M, box = _points(rng, 6000, energies)
    T = 10.0
    factor = {e: 1 - np.exp(-11.60497 * e / T) for e in energies}

    st = _base_state(box, M)
    data_box(_chi_env(st, "hw_nan", {
        "fgt_txt2": _V(""), "fgt_txt3": _V(""), "bgt_txt2": _V(""), "bgt_txt3": _V(""),
        "txt16": _V("-0.9"), "txt17": _V("0.9"), "txt18": _V("0.6"),
        "txt19": _V("-0.9"), "txt20": _V("0.9"), "txt21": _V("0.6"),
        "txt22": _V(""), "txt23": _V(""), "txt24": _V("")}))
    for ne, e in enumerate(st["map_energylist"]):
        pick = box[3] == energies[ne]
        assert np.isclose(e, energies[ne])
        whole = np.nansum(st["I"][ne] * st["Imon"][ne]) / np.nansum(st["Imon"][ne])
        assert np.isclose(whole, _ref(D[pick], M[pick])[0] * factor[energies[ne]])
        assert (np.nanmax(st["I"][ne]) < 0) == (energies[ne] < 0)

    st2 = _base_state(box, M)
    pow_data_box(_chi_env(st2, "hwp_nan", {
        "fgt_txt4": _V(""), "bgt_txt6": _V(""),
        "txt01_p": _V("0.1"), "txt02_p": _V("1.3"), "txt03_p": _V("0.2"),
        "txt04_p": _V(""), "txt05_p": _V(""), "txt06_p": _V("")}))
    Q = st2["Q"]
    for ne, e in enumerate(energies):
        pick = (box[3] == e) & (Q[2] < box[2]) & (box[2] <= Q[3])
        assert np.isclose(st2["Ipow"][ne, 2], _ref(D[pick], M[pick])[0] * factor[e])
        assert np.isclose(st2["Ipow_err"][ne, 2], _ref(D[pick], M[pick])[1] * abs(factor[e]))
        assert (st2["Ipow"][ne, 2] < 0) == (e < 0)


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print("PASS", t.__name__)
    print(f"{len(tests)} tests passed")
