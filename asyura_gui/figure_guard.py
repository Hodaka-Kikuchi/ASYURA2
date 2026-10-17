"""Guards used by the 'add …' buttons, which draw onto an existing plot window."""

import matplotlib.pyplot as plt
from tkinter import messagebox


def base_figure_open(state, key, base_label):
    """Return True if the plot window stored in ``state[key]`` is still open.

    Otherwise tell the user which plot to create first and return False.
    Previously a missing key raised KeyError (button appeared dead) and a
    closed window silently did nothing.
    """
    num = state.get(key)
    if num is not None and plt.fignum_exists(num):
        return True
    messagebox.showinfo(
        "ASYURA",
        f"Please draw '{base_label}' first.\n"
        "'add' overlays a new curve on that open plot window.",
    )
    return False


def require_state(state, key, base_label):
    """Return True if ``key`` exists in state; otherwise ask for ``base_label`` first."""
    if state.get(key) is not None:
        return True
    messagebox.showinfo("ASYURA", f"Please run '{base_label}' first.")
    return False
