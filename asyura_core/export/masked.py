import csv
import numpy as np
import tkinter as tk
from tkinter import filedialog
from itertools import zip_longest

def save_masked_3d_data(state):
    filename = tk.filedialog.asksaveasfilename(
        title = "Save Masked 3D Scattering Data",
        filetypes = [("CSV Files", "*.csv")],
        defaultextension = ".csv"
    )
    
    if not filename:
        return  # キャンセルされた場合
    
    # {u}と{v}の場合は[]のまま出力されてしまうので()に変換
    #u_str = f"({', '.join(map(str, u))})"
    #v_str = f"({', '.join(map(str, v))})"
    #'Qx (Å^-1)', f'{Ulabel} [= {u_str}] (r.l.u.)',
    #'Qy (Å^-1)', f'{Vlabel} [= {v_str}] (r.l.u.)',
    
    header = [
        f'{state['Ulabel']} (r.l.u.)',f'{state['Ulabel']} (r.l.u.)',f'{state['Ulabel']} (r.l.u.)',
        f'{state['Vlabel']} (r.l.u.)',f'{state['Vlabel']} (r.l.u.)',f'{state['Vlabel']} (r.l.u.)',
        'hw (meV)',
        'normalizerd I (a.u.)',
        'normalizerd Err (a.u.)'
    ]
    
    # 保存処理
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(state['masked_3d_databox'])

def save_masked_2dcE_data(state):
    filename = tk.filedialog.asksaveasfilename(
        title = f"Save Masked 2D {state['Ulabel']}-{state['Vlabel']} Scattering Data",
        filetypes = [("CSV Files", "*.csv")],
        defaultextension = ".csv"
    )
    
    if not filename:
        return  # キャンセルされた場合
    
    # {u}と{v}の場合は[]のまま出力されてしまうので()に変換
    #u_str = f"({', '.join(map(str, u))})"
    #v_str = f"({', '.join(map(str, v))})"
    #'Qx (Å^-1)', f'{Ulabel} [= {u_str}] (r.l.u.)',
    #'Qy (Å^-1)', f'{Vlabel} [= {v_str}] (r.l.u.)',
    
    header = [
        f'{state['Ulabel']} (r.l.u.)',f'{state['Ulabel']} (r.l.u.)',f'{state['Ulabel']} (r.l.u.)',
        f'{state['Vlabel']} (r.l.u.)',f'{state['Vlabel']} (r.l.u.)',f'{state['Vlabel']} (r.l.u.)',
        'hw (meV)',
        'normalizerd I (a.u.)',
        'normalizerd Err (a.u.)'
    ]
    
    # 保存処理
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(state['masked_2d_constE'])

def save_masked_2dcU_data(state):
    filename = tk.filedialog.asksaveasfilename(
        title = f"Save Masked 2D {state['Vlabel']}-hw Scattering Data",
        filetypes = [("CSV Files", "*.csv")],
        defaultextension = ".csv"
    )
    
    if not filename:
        return  # キャンセルされた場合
    
    # {u}と{v}の場合は[]のまま出力されてしまうので()に変換
    #u_str = f"({', '.join(map(str, u))})"
    #v_str = f"({', '.join(map(str, v))})"
    #'Qx (Å^-1)', f'{Ulabel} [= {u_str}] (r.l.u.)',
    #'Qy (Å^-1)', f'{Vlabel} [= {v_str}] (r.l.u.)',
    
    header = [
        f'{state['Ulabel']} (r.l.u.)',f'{state['Ulabel']} (r.l.u.)',f'{state['Ulabel']} (r.l.u.)',
        f'{state['Vlabel']} (r.l.u.)',f'{state['Vlabel']} (r.l.u.)',f'{state['Vlabel']} (r.l.u.)',
        'hw (meV)',
        'normalizerd I (a.u.)',
        'normalizerd Err (a.u.)'
    ]
    
    # 保存処理
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(state['masked_2d_constU'])

def save_masked_2dcV_data(state):
    filename = tk.filedialog.asksaveasfilename(
        title = f"Save Masked 2D {state['Ulabel']}-hw Scattering Data",
        filetypes = [("CSV Files", "*.csv")],
        defaultextension = ".csv"
    )
    
    if not filename:
        return  # キャンセルされた場合
    
    # {u}と{v}の場合は[]のまま出力されてしまうので()に変換
    #u_str = f"({', '.join(map(str, u))})"
    #v_str = f"({', '.join(map(str, v))})"
    #'Qx (Å^-1)', f'{Ulabel} [= {u_str}] (r.l.u.)',
    #'Qy (Å^-1)', f'{Vlabel} [= {v_str}] (r.l.u.)',
    
    header = [
        f'{state['Ulabel']} (r.l.u.)',f'{state['Ulabel']} (r.l.u.)',f'{state['Ulabel']} (r.l.u.)',
        f'{state['Vlabel']} (r.l.u.)',f'{state['Vlabel']} (r.l.u.)',f'{state['Vlabel']} (r.l.u.)',
        'hw (meV)',
        'normalizerd I (a.u.)',
        'normalizerd Err (a.u.)'
    ]
    
    # 保存処理
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(state['masked_2d_constV'])
