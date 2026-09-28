import csv
import numpy as np
import tkinter as tk
from tkinter import filedialog
from itertools import zip_longest

def save_constEmap(state):
    filename = tk.filedialog.asksaveasfilename(
        title = f"save as {state['Ulabel']}-{state['Vlabel']} 2D data",
        filetypes = [("CSV", ".csv") ], # ファイルフィルタ
        initialdir = "./", # 自分自身のディレクトリ
        defaultextension = "csv"
        )
    #ヘッダーの作成
    # {u}と{v}の場合は[]のまま出力されてしまうので()に変換
    #u_str = f"({', '.join(map(str, u))})"
    #v_str = f"({', '.join(map(str, v))})"
    #header1 = [f'{Ulabel} [= {u_str}] (r.l.u.)']
    #header2 = [f'{Vlabel} [= {v_str}] (r.l.u.)']

    header0 = ['hw (meV)']
    header1 = [f'{state['Ulabel']} (r.l.u.)']
    header2 = [f'{state['Vlabel']} (r.l.u.)']
    header3 = [f'Intensity (a.u.) (x-axis:{state['Ulabel']} (r.l.u.), y-axis:{state['Vlabel']} (r.l.u.) )']
    header4 = [f'Error (a.u.) (x-axis:{state['Ulabel']} (r.l.u.), y-axis:{state['Vlabel']} (r.l.u.) )']
    #データ保存(データの大きさが違うので、行列を連結することができない。なので１行目から順に保存していく形式にした。)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header0)
        writer.writerow(state['Erange_2d_VvsU'])
        writer.writerow(header1)
        writer.writerows(state['Urange_2d_VvsU'])
        writer.writerow(header2)
        writer.writerows(state['Vrange_2d_VvsU'])
        writer.writerow(header3)
        writer.writerows(state['I_ce'])
        writer.writerow(header4)
        writer.writerows(state['Ierr_ce'])

def save_hw_Umap(state):
    filename = tk.filedialog.asksaveasfilename(
        title = f"save as {state['Ulabel']}-hw 2D data",
        filetypes = [("CSV", ".csv") ], # ファイルフィルタ
        initialdir = "./", # 自分自身のディレクトリ
        defaultextension = "csv"
        )
    #ヘッダーの作成
    # {u}と{v}の場合は[]のまま出力されてしまうので()に変換
    #u_str = f"({', '.join(map(str, u))})"
    #v_str = f"({', '.join(map(str, v))})"
    #header1 = [f'{Ulabel} [= {u_str}] (r.l.u.)']
    #header2 = [f'{Vlabel} [= {v_str}] (r.l.u.)']
    
    header0 = ['hw (meV)']
    header1 = [f'{state['Ulabel']} (r.l.u.)']
    header2 = [f'{state['Vlabel']} (r.l.u.)']
    header3 = [f'Intensity (a.u.) (x-axis:{state['Ulabel']} (r.l.u.), y-axis:hw (meV) )']
    header4 = [f'Error (a.u.) (x-axis:{state['Ulabel']} (r.l.u.), y-axis:hw (meV) )']
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header0)
        writer.writerow(state['Erange_2d_UvsE'])
        writer.writerow(header1)
        writer.writerows(state['Urange_2d_UvsE'])
        writer.writerow(header2)
        writer.writerows(state['Vrange_2d_UvsE'])
        writer.writerow(header3)
        writer.writerows(state['I_hwU'])
        writer.writerow(header4)
        writer.writerows(state['Ierr_hwU'])

def save_hw_Vmap(state):
    filename = tk.filedialog.asksaveasfilename(
        title = f"save as {state['Vlabel']}-hw 2D data",
        filetypes = [("CSV", ".csv") ], # ファイルフィルタ
        initialdir = "./", # 自分自身のディレクトリ
        defaultextension = "csv"
        )
    #ヘッダーの作成
    # {u}と{v}の場合は[]のまま出力されてしまうので()に変換
    #u_str = f"({', '.join(map(str, u))})"
    #v_str = f"({', '.join(map(str, v))})"
    #header1 = [f'{Ulabel} [= {u_str}] (r.l.u.)']
    #header2 = [f'{Vlabel} [= {v_str}] (r.l.u.)']
    
    header0 = ['hw (meV)']
    header1 = [f'{state['Ulabel']} (r.l.u.)']
    header2 = [f'{state['Vlabel']} (r.l.u.)']
    header3 = [f'Intensity (a.u.) (x-axis:{state['Vlabel']} (r.l.u.), y-axis:hw (meV) )']
    header4 = [f'Error (a.u.) (x-axis:{state['Vlabel']} (r.l.u.), y-axis:hw (meV) )']
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header0)
        writer.writerow(state['Erange_2d_VvsE'])
        writer.writerow(header1)
        writer.writerows(state['Urange_2d_VvsE'])
        writer.writerow(header2)
        writer.writerows(state['Vrange_2d_VvsE'])
        writer.writerow(header3)
        writer.writerows(state['I_hwV'])
        writer.writerow(header4)
        writer.writerows(state['Ierr_hwV'])

def save_2D_hw_qmap(state):#plt.pcolormesh(Q, hwlist_p , Ipow, cmap='jet', vmin=z_min, vmax=z_max)
    filename = tk.filedialog.asksaveasfilename(
        title = "save as hw-Q 2D data",
        filetypes = [("CSV", ".csv") ], # ファイルフィルタ
        initialdir = "./", # 自分自身のディレクトリ
        defaultextension = "csv"
        )
    #ヘッダーの作成
    header1 = ['hw (meV)']
    header2 = ['Q (A^-1)']
    header3 = ['Intensity (a.u.)']
    header4 = ['Error (a.u.)']
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header1)
        writer.writerow(state['energylist'])
        writer.writerow(header2)
        writer.writerow(state['Q2'])
        writer.writerow(header3)
        writer.writerows(state['Ipow'])
        writer.writerow(header4)
        writer.writerows(state['Ipow_err'])
