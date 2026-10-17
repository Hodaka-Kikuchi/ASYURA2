"""Make 'Save Data' menu items tell the user when there is nothing to save yet.

Each exporter reads fixed results from ``state`` (e.g. ``state['I_hwV']``).
Before this guard, choosing a save item before the corresponding plot had been
drawn raised KeyError *after* the file dialog, so the menu appeared to do
nothing (and could leave an empty file behind).  The keys an exporter needs are
taken from its own source, and are checked before the file dialog opens.
"""

import ast
import functools
import inspect
import textwrap

from tkinter import messagebox

# Friendlier hints for a few keys; everything else gets the generic message.
_HINTS = {
    "databox": "Load data files first ('load data file(s)').",
    "sb_databox": "No background data is loaded. Select background file(s) and load again.",
}


def _required_state_keys(func):
    tree = ast.parse(textwrap.dedent(inspect.getsource(func)))
    return sorted({
        node.slice.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Subscript)
        and isinstance(node.value, ast.Name)
        and node.value.id == "state"
        and isinstance(node.slice, ast.Constant)
        and isinstance(node.slice.value, str)
    })


def requires_results(func):
    keys = _required_state_keys(func)

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
