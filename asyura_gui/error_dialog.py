"""Show errors raised inside GUI callbacks to the user.

Tk normally prints callback exceptions to the console only, so a failing
button just looks dead.  This handler keeps the console traceback (useful for
debugging) and additionally shows a short dialog with a hint.
"""

import traceback

from tkinter import messagebox

# state keys that only exist after the corresponding step has been done
_NEEDS_LOAD = {"databox", "monitorbox", "hklbox", "N_mcu", "NU1", "NV1", "u", "v", "ef_tol"}
_NEEDS_BIN = {"I", "Ierr", "QU", "QV", "QU2", "QV2", "energylist", "map_energylist",
              "Ipow", "Ipow_err", "Q", "Q2", "hwlist_p"}


def explain(exc):
    """Return a short user-facing explanation for an exception."""
    text = str(exc)
    if isinstance(exc, ValueError) and "could not convert string to float" in text:
        return ("An input box is empty or does not contain a number.\n"
                f"({text})\nPlease check the input fields.")
    if isinstance(exc, KeyError) and exc.args:
        key = exc.args[0]
        if key == "vfile_path":
            return "Please select a vanadium (calibration) file first."
        if key in _NEEDS_LOAD:
            return "Please load data files first ('load data file(s)')."
        if key in _NEEDS_BIN:
            return "Please bin the data first ('auto bin' / 're-bin')."
    if isinstance(exc, (FileNotFoundError, PermissionError)):
        return f"File error: {text}"
    return f"{type(exc).__name__}: {text}"


def install(root):
    def report(exc_type, exc, tb):
        traceback.print_exception(exc_type, exc, tb)
        try:
            messagebox.showerror("ASYURA", explain(exc))
        except Exception:
            pass

    root.report_callback_exception = report
    return report
