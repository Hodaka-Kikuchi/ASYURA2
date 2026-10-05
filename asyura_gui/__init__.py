"""Tkinter GUI layer for ASYURA.

The import is intentionally lazy so importing the package does not create a
Tk/Matplotlib GUI backend until ``run_app()`` is actually called.
"""


def run_app():
    from .app import run_app as _run_app
    return _run_app()


__all__ = ["run_app"]
