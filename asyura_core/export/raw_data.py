import csv
import numpy as np
import tkinter as tk
from tkinter import filedialog
from itertools import zip_longest

def save_FGdata(state):
    filename = tk.filedialog.asksaveasfilename(
        title = "save as foreground data",
        filetypes = [("CSV", ".csv") ], # ファイルフィルタ
        initialdir = "./", # 自分自身のディレクトリ
        defaultextension = "csv"
        )
    #ヘッダーの作成,# 0 Qx, 1 Qy, 2 Q, 3 エネルギートランスファー,　4 規格化強度,  5 規格化エラーバー
    header = ['Qx (Å^-1)', 'Qy (Å^-1)', 'q (Å^-1)', 'hw (meV)', 'normalizerd I (a.u.)', 'normalizerd Err (a.u.)']
    #データ保存
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(state['databox'].T)

def save_BGdata(state):
    filename = tk.filedialog.asksaveasfilename(
        title = "save as Background data",
        filetypes = [("CSV", ".csv") ], # ファイルフィルタ
        initialdir = "./", # 自分自身のディレクトリ
        defaultextension = "csv"
        )
    #ヘッダーの作成,# 0 Qx, 1 Qy, 2 Q, 3 エネルギートランスファー,　4 規格化強度,  5 規格化エラーバー
    header = ['Qx (Å^-1)', 'Qy (Å^-1)', 'q (Å^-1)', 'hw (meV)', 'normalizerd I (a.u.)', 'normalizerd Err (a.u.)']
    #データ保存
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(state['sb_databox'].T)
