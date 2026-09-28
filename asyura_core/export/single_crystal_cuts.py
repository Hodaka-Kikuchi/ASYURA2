import csv
import numpy as np
import tkinter as tk
from tkinter import filedialog
from itertools import zip_longest

def save_1Dhw_I(state):
    filename = tk.filedialog.asksaveasfilename(
        title="save as hw-I 1D data",
        filetypes=[("CSV", ".csv")],  # ファイルフィルタ
        initialdir="./",  # 自分自身のディレクトリ
        defaultextension="csv"
    )
    
    # ヘッダーの作成
    header = ['hw (meV)', f'{state['Ulabel']} (r.l.u.)', f'{state['Ulabel']} (r.l.u.)', f'{state['Ulabel']} (r.l.u.)', 
              f'{state['Vlabel']} (r.l.u.)', f'{state['Vlabel']} (r.l.u.)', f'{state['Vlabel']} (r.l.u.)', 
              'Intensity (a.u.)', 'Error (a.u.)']
    
    # リストを1行ごとにまとめる
    rows = zip_longest(state['Erange_1d_Ivshw'], 
               state['Urange_1d_Ivshw'][0], state['Urange_1d_Ivshw'][1], state['Urange_1d_Ivshw'][2],  # Uの各列
               state['Vrange_1d_Ivshw'][0], state['Vrange_1d_Ivshw'][1], state['Vrange_1d_Ivshw'][2],  # Vの各列
               state['I_hw1d2'], 
               state['Ierr_hw1d2'])

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # ヘッダーを書き込む
        writer.writerow(header)
        
        # データ行を書き込む
        writer.writerows(rows)

def save_1DI_U(state):
    filename = tk.filedialog.asksaveasfilename(
        title = f"save as {state['Ulabel']}-I 1D data",
        filetypes = [("CSV", ".csv") ], # ファイルフィルタ
        initialdir = "./", # 自分自身のディレクトリ
        defaultextension = "csv"
        )
    # ヘッダーの作成
    header = ['hw (meV)', f'{state['Ulabel']} (r.l.u.)', f'{state['Ulabel']} (r.l.u.)', f'{state['Ulabel']} (r.l.u.)', 
              f'{state['Vlabel']} (r.l.u.)', f'{state['Vlabel']} (r.l.u.)', f'{state['Vlabel']} (r.l.u.)', 
              'Intensity (a.u.)', 'Error (a.u.)']
    
    # リストを1行ごとにまとめる
    rows = zip_longest(state['Erange_1d_IvsU'], 
               state['Urange_1d_IvsU'][0], state['Urange_1d_IvsU'][1], state['Urange_1d_IvsU'][2],  # Uの各列
               state['Vrange_1d_IvsU'][0], state['Vrange_1d_IvsU'][1], state['Vrange_1d_IvsU'][2],  # Vの各列
               state['I_1DU'], 
               state['Ierr_1DU'])

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # ヘッダーを書き込む
        writer.writerow(header)
        
        # データ行を書き込む
        writer.writerows(rows)

def save_1DI_V(state):
    filename = tk.filedialog.asksaveasfilename(
        title = f"save as {state['Vlabel']}-I 1D data",
        filetypes = [("CSV", ".csv") ], # ファイルフィルタ
        initialdir = "./", # 自分自身のディレクトリ
        defaultextension = "csv"
        )
    # ヘッダーの作成
    header = ['hw (meV)', f'{state['Ulabel']} (r.l.u.)', f'{state['Ulabel']} (r.l.u.)', f'{state['Ulabel']} (r.l.u.)', 
              f'{state['Vlabel']} (r.l.u.)', f'{state['Vlabel']} (r.l.u.)', f'{state['Vlabel']} (r.l.u.)', 
              'Intensity (a.u.)', 'Error (a.u.)']
    
    # リストを1行ごとにまとめる
    rows = zip_longest(state['Erange_1d_IvsV'], 
               state['Urange_1d_IvsV'][0], state['Urange_1d_IvsV'][1], state['Urange_1d_IvsV'][2],  # Uの各列
               state['Vrange_1d_IvsV'][0], state['Vrange_1d_IvsV'][1], state['Vrange_1d_IvsV'][2],  # Vの各列
               state['I_1DV'], 
               state['Ierr_1DV'])

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # ヘッダーを書き込む
        writer.writerow(header)
        
        # データ行を書き込む
        writer.writerows(rows)
