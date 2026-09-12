"""ASYURA launcher.

The Tkinter interface lives in :mod:`asyura_gui.app`; calculation and file
processing code lives in :mod:`asyura_core`.
"""

from asyura_gui import run_app


if __name__ == "__main__":
    run_app()

# EXE化コマンド
# python -m PyInstaller --clean --noconsole --onefile --icon "ASYURA_logo.ico" --add-data "ASYURA_logo.ico;." "ASYURA2.py"