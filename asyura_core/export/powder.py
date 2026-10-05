import csv
import numpy as np
import tkinter as tk
from tkinter import filedialog
from itertools import zip_longest

def save_1D_hwI_pow(state):
    filename = tk.filedialog.asksaveasfilename(
        title = "save as I-hw 1D data",
        filetypes = [("CSV", ".csv") ], # ファイルフィルタ
        initialdir = "./", # 自分自身のディレクトリ
        defaultextension = "csv"
        )
        
    # ヘッダーの作成
    header = ['hw (meV)','q (A^-1)','Intensity (a.u.)','Error (a.u.)']
    
    # リストを1行ごとにまとめる
    rows = zip_longest(state['elist'],state['qlist'],state['Ipow_1dei'],state['Ipowerr_1dei'])

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # ヘッダーを書き込む
        writer.writerow(header)
        
        # データ行を書き込む
        writer.writerows(rows)

def save_1D_qI_pow(state):
    filename = tk.filedialog.asksaveasfilename(
        title = "save as I-Q 1D data",
        filetypes = [("CSV", ".csv") ], # ファイルフィルタ
        initialdir = "./", # 自分自身のディレクトリ
        defaultextension = "csv"
        )
   
    # ヘッダーの作成
    header = ['hw (meV)','q (A^-1)','Intensity (a.u.)','Error (a.u.)']
    
    # リストを1行ごとにまとめる
    rows = zip_longest(state['elist2'],state['qlist2'],state['Ipow_1dqi'],state['Ipowerr_1dqi'])

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # ヘッダーを書き込む
        writer.writerow(header)
        
        # データ行を書き込む
        writer.writerows(rows)
