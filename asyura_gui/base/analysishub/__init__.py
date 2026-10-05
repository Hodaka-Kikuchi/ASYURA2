"""Analysis Hub GUI container and tab builders."""

import tkinter as tk
from tkinter import ttk

from .single_crystal import build_single_crystal
from .powder import build_powder
from .scansim import build_scansim
from .anglecalc import build_anglecalc
from .toolbox import build_toolbox

def build_analysis_hub(env):
    root = env["root"]
    frame1 = ttk.Labelframe(root, text="AnalysisHub")
    frame1.grid(row=2, column=0, padx=5, pady=2, sticky="NSEW")
    frame1.columnconfigure(0, weight=1); frame1.rowconfigure(0, weight=1)
    notebook1 = ttk.Notebook(frame1, style="example.TNotebook")
    tab_01=tk.Frame(notebook1); tab_02=tk.Frame(notebook1); tab_03=tk.Frame(notebook1); tab_04=tk.Frame(notebook1); tab_05=tk.Frame(notebook1)
    notebook1.add(tab_01,text="Single Crystal"); notebook1.add(tab_02,text="Powder"); notebook1.add(tab_03,text="ScanSim"); notebook1.add(tab_05,text="AngleCalc"); notebook1.add(tab_04,text="Toolbox")
    tab_01.columnconfigure(0,weight=1); tab_01.columnconfigure(1,weight=1); tab_01.rowconfigure(0,weight=1); tab_01.rowconfigure(1,weight=12)
    tab_02.columnconfigure(0,weight=2); tab_02.columnconfigure(1,weight=1); tab_02.columnconfigure(2,weight=1); tab_02.rowconfigure(0,weight=1); tab_02.rowconfigure(1,weight=1)
    tab_03.columnconfigure(0,weight=1); tab_03.rowconfigure(0,weight=1)
    tab_04.columnconfigure(0,weight=1); tab_04.rowconfigure(0,weight=1)
    tab_05.columnconfigure(0,weight=1); tab_05.columnconfigure(1,weight=1); tab_05.rowconfigure(0,weight=1); tab_05.rowconfigure(1,weight=1); tab_05.rowconfigure(2,weight=1)
    notebook1.grid(row=0,column=0,sticky="NSEW")
    local_env=dict(env); local_env.update({"frame1":frame1,"notebook1":notebook1,"tab_01":tab_01,"tab_02":tab_02,"tab_03":tab_03,"tab_04":tab_04,"tab_05":tab_05})
    for builder in (build_single_crystal, build_powder, build_scansim, build_anglecalc, build_toolbox):
        local_env.update(builder(local_env))
    return local_env
