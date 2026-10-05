import csv
import numpy as np
import tkinter as tk
from tkinter import filedialog
from itertools import zip_longest

def save_hw_HKL(state):
    filename = tk.filedialog.asksaveasfilename(
        title = f"save as hkl-hw 2D data",
        filetypes = [("CSV", ".csv") ], # ファイルフィルタ
        initialdir = "./", # 自分自身のディレクトリ
        defaultextension = "csv"
        )
    #ヘッダーの作成
    header0 = ['hw (meV)']
    header1 = ['HKL (r.l.u.)']
    header2 = ['hkl (r.l.u.)']
    header3 = ['Intensity (a.u.) (x-axis:HKL (r.l.u.), y-axis:hw (meV) )']
    header4 = ['Error (a.u.) (x-axis:HKL (r.l.u.), y-axis:hw (meV) )']
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header0)
        writer.writerow(state['energylist'])
        writer.writerow(header1)
        writer.writerows(state['table_2D'].T)
        writer.writerow(header2)
        writer.writerows(state['table_2D_qrange'])
        writer.writerow(header3)
        writer.writerows(state['I_cq'])
        writer.writerow(header4)
        writer.writerows(state['I_cq_err'])

def save_hkl_HKL(state):
    filename = tk.filedialog.asksaveasfilename(
        title = "save as hkl-HKL 2D data",
        filetypes = [("CSV", ".csv") ], # ファイルフィルタ
        initialdir = "./", # 自分自身のディレクトリ
        defaultextension = "csv"
        )
    #ヘッダーの作成
    header0 = ['hw (meV)']
    header1 = ['HKL (r.l.u.)']
    header2 = ['hkl (r.l.u.)']
    header3 = ['Intensity (a.u.) (x-axis:HKL (r.l.u.), y-axis:hkl (r.l.u.) )']
    header4 = ['Error (a.u.) (x-axis:HKL (r.l.u.), y-axis:hkl (r.l.u.) )']
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header0)
        writer.writerow(state['E_I_ce'])
        writer.writerow(header1)
        writer.writerows(state['table_2DX'].T)
        writer.writerow(header2)
        writer.writerows(state['table_2DY'].T)
        writer.writerow(header3)
        writer.writerows(state['I_ce_adv'])
        writer.writerow(header4)
        writer.writerows(state['Ierr_ce_adv'])

def save_I_HKL(state):
    filename = tk.filedialog.asksaveasfilename(
        title = "save as advance_1D_HKL-I data",
        filetypes = [("CSV", ".csv") ], # ファイルフィルタ
        initialdir = "./", # 自分自身のディレクトリ
        defaultextension = "csv"
        )
    # ヘッダーの作成
    header = ['hw (meV)', f'{state['Ulabel']} (r.l.u.)', f'{state['Ulabel']} (r.l.u.)', f'{state['Ulabel']} (r.l.u.)', 
              f'{state['Vlabel']} (r.l.u.)', f'{state['Vlabel']} (r.l.u.)', f'{state['Vlabel']} (r.l.u.)', 
              'Intensity (a.u.)', 'Error (a.u.)']
    
    # リストを1行ごとにまとめる
    rows = zip_longest(state['I_1d_IvsHKL_E'], 
               state['I_1d_IvsHKL_hkl'][0], state['I_1d_IvsHKL_hkl'][1], state['I_1d_IvsHKL_hkl'][2],  # Uの各列
               state['I_1d_IvsHKL_HKL'][0], state['I_1d_IvsHKL_HKL'][1], state['I_1d_IvsHKL_HKL'][2],  # Vの各列
               state['I_1d_alongQ'], 
               state['I_1d_alongQ_err'])

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # ヘッダーを書き込む
        writer.writerow(header)
        
        # データ行を書き込む
        writer.writerows(rows)

def save_I_hw(state):
    filename = tk.filedialog.asksaveasfilename(
        title = "save as advance_1D_I-HKL data",
        filetypes = [("CSV", ".csv") ], # ファイルフィルタ
        initialdir = "./", # 自分自身のディレクトリ
        defaultextension = "csv"
        )
    # ヘッダーの作成
    header = ['hw (meV)', 'HKL (r.l.u.)', 'HKL (r.l.u.)', 'HKL (r.l.u.)', 
              'hkl (r.l.u.)', 'hkl (r.l.u.)', 'hkl (r.l.u.)', 
              'Intensity (a.u.)', 'Error (a.u.)']
    
    # リストを1行ごとにまとめる
    rows = zip_longest(state['I_1d_Ivshw_E'], 
               state['I_1d_Ivshw_hkl'][0], state['I_1d_Ivshw_hkl'][1], state['I_1d_Ivshw_hkl'][2],  # Uの各列
               state['I_1d_Ivshw_HKL'][0], state['I_1d_Ivshw_HKL'][1], state['I_1d_Ivshw_HKL'][2],  # Vの各列
               state['I_1d_alongE'], 
               state['I_1d_alongE_err'])

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # ヘッダーを書き込む
        writer.writerow(header)
        
        # データ行を書き込む
        writer.writerows(rows)
