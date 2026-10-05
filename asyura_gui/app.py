# Automation System for Utility in Research Analysis
# ASYURA
# UB matrixによるoffsetの自動入力
# 右上にバージョン情報を表示
__version__ = '4.0.0'

# cd C:\Users\h34\Documents\Python\ASYURA
"""
セマンティック バージョニング (Semantic Versioning)
セマンティック バージョニング（セムバ―、SemVer）は、バージョン番号を「MAJOR.MINOR.PATCH」の形式で表します。それぞれの部分には以下のような意味があります：

MAJOR（メジャー）バージョン:

後方互換性のない変更が導入された場合に増加します。
例：既存のAPIの変更、破壊的な変更。
MINOR（マイナー）バージョン

後方互換性のある新機能が追加された場合に増加します。
例：新しい機能の追加、既存機能の改良（後方互換性がある場合）。
PATCH（パッチ）バージョン:

後方互換性のあるバグ修正が行われた場合に増加します。
例：バグの修正、セキュリティ修正。

バージョン番号の例
1.0.0: 最初の安定版リリース。
1.1.0: 後方互換性のある新機能が追加されたリリース。
1.1.1: バグ修正やマイナーな改良が行われたリリース。
2.0.0: 後方互換性のない変更が導入されたリリース。

新機能付与とバグ修正を行った場合、patchバージョンを+、ラストの数値は0に戻す(更新の必要はない。)。
常に左側の数値の更新が優先。
"""

# tlinterのインポート
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

# 確定的progressbarの設置
from tkinter import messagebox
from tkinter import simpledialog
#import pyperclip

# osのインポート
import os

# ギリシャ文字の定義
import sympy as sm
sm.init_printing()

mu    = sm.Symbol("μ")
theta = sm.Symbol("θ")# "\theta"から変更
alpha    = sm.Symbol("α")
beta    = sm.Symbol("β")
gamma    = sm.Symbol("γ")
AA    = sm.Symbol("Å")

# 数値計算を行うためのパッケージのインポート
from scipy.interpolate import interp1d

# smoothing処理のパッケージ
from scipy.ndimage import gaussian_filter

import numpy as np
import math
import matplotlib
matplotlib.use('TkAgg')#よくわかんないけどこれないとexe化したときにグラフが表示されない。超重要
import matplotlib.pyplot as plt
import matplotlib.widgets as wg #from  matplotlib.widgets import Slider
# 試しにdataboxを3dで可視化
from mpl_toolkits.mplot3d import Axes3D

from itertools import product

import matplotlib.ticker as mticker

from matplotlib.backend_tools import ToolBase, ToolToggleBase

from matplotlib.colors import LogNorm

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib.widgets import TextBox

import statistics as stat
from scipy import stats
from scipy.stats import norm
from scipy.optimize import minimize
from scipy.optimize import curve_fit
from scipy.spatial import KDTree

from fractions import Fraction

from itertools import zip_longest

import configparser

# gif保存用
from PIL import Image
#import imageio
from io import BytesIO

# ファイル読み込みのためのやつ
import re

# webに飛ぶやつ
import webbrowser

from functools import partial
from .assets import apply_app_icon

# Numerical helpers split out from the original monolithic script.
from asyura_core.reciprocal_space import (
    _normalize_angle_deg,
    _find_simple_orthogonal_inplane_hkl,
    _make_crystallographic_display_basis,
    _display_uv_to_hkl,
)
from asyura_core.spice_geometry import (
    DATA_C2_TO_OMEGA_SIGN,
    _parse_spice_ub_from_dat,
    _spice_raw_Rx_deg,
    _spice_raw_Ry_deg,
    _spice_tilt_matrix_raw,
    _spice_relative_tilt_in_pdf,
    _data_Ry_deg,
    _data_Rz_deg,
    _data_Rx_deg,
    _data_q_lab,
    _canonicalize_spice_ub_for_pdf,
    _calculate_data_reference_omega,
    _rotation_z_deg,
    _angles_to_hkl_and_uv,
)
from asyura_core.simulation_geometry import (
    SIMU_C2_TO_OMEGA_SIGN,
    _make_B_from_lattice_for_simulation,
    _make_simulation_ub_from_lattice_uv,
    _normalize_simu_angle_deg,
    _simu_q_lab,
    _simu_Ry_deg,
    _calculate_simu_reference_omega,
    _simu_hkl_text,
    _simu_angles_to_rlu,
)

from asyura_core.data_processing import (
    bin_single_crystal_data,
    get_single_crystal_map_energy_axis,
)
from asyura_core.physics import (
    energy_to_wavelength_wavenumber,
    wavelength_to_energy_wavenumber,
    wavenumber_to_energy_wavelength,
    harmonic_energy,
    reciprocal_q_and_d,
    tas_scattering_angle_deg,
)

from asyura_core.exporters import (
    save_FGdata as _save_FGdata,
    save_BGdata as _save_BGdata,
    save_constEmap as _save_constEmap,
    save_hw_Umap as _save_hw_Umap,
    save_hw_Vmap as _save_hw_Vmap,
    save_1Dhw_I as _save_1Dhw_I,
    save_1DI_U as _save_1DI_U,
    save_1DI_V as _save_1DI_V,
    save_hw_HKL as _save_hw_HKL,
    save_hkl_HKL as _save_hkl_HKL,
    save_I_HKL as _save_I_HKL,
    save_I_hw as _save_I_hw,
    save_masked_3d_data as _save_masked_3d_data,
    save_masked_2dcE_data as _save_masked_2dcE_data,
    save_masked_2dcU_data as _save_masked_2dcU_data,
    save_masked_2dcV_data as _save_masked_2dcV_data,
    save_2D_hw_qmap as _save_2D_hw_qmap,
    save_1D_hwI_pow as _save_1D_hwI_pow,
    save_1D_qI_pow as _save_1D_qI_pow,
)


# GUI actions are implemented in separate callback modules.
from .callbacks.files import create_files_callbacks
from .callbacks.data import create_data_callbacks
from .callbacks.plots import create_plots_callbacks
from .callbacks.powder import create_powder_callbacks
from .callbacks.simulation import create_simulation_callbacks
from .callbacks.toolbox import create_toolbox_callbacks

from .base import build_dataset_information, build_sample_information, build_analysis_hub

def run_app():
    # Mutable state belongs to one GUI session.
    state = {}

    # Button/menu/trace commands are lightweight proxies.  The real callback
    # functions are created after all Tk widgets exist, using an explicit GUI environment.
    callback_registry = {}

    def _callback_proxy(name):
        def proxy(*args, **kwargs):
            callback = callback_registry.get(name)
            if callback is None:
                raise RuntimeError(f"GUI callback {name!r} was invoked before callback initialization.")
            return callback(*args, **kwargs)
        return proxy

    _prepare_simu_reciprocal_display = _callback_proxy('_prepare_simu_reciprocal_display')
    _show_ubmatrix = _callback_proxy('_show_ubmatrix')
    add_advanced_1D_alongE = _callback_proxy('add_advanced_1D_alongE')
    add_advanced_1D_alongQ = _callback_proxy('add_advanced_1D_alongQ')
    add_simu_pow = _callback_proxy('add_simu_pow')
    add_simu_sc_cE = _callback_proxy('add_simu_sc_cE')
    add_simu_sc_cU = _callback_proxy('add_simu_sc_cU')
    add_simu_sc_cV = _callback_proxy('add_simu_sc_cV')
    advanced_1D_alongE = _callback_proxy('advanced_1D_alongE')
    advanced_1D_alongQ = _callback_proxy('advanced_1D_alongQ')
    advanced_2D_constE = _callback_proxy('advanced_2D_constE')
    advanced_2D_constQ = _callback_proxy('advanced_2D_constQ')
    btn_click_1DPE = _callback_proxy('btn_click_1DPE')
    btn_click_1DPQ = _callback_proxy('btn_click_1DPQ')
    calculate_c2 = _callback_proxy('calculate_c2')
    calibration = _callback_proxy('calibration')
    clear = _callback_proxy('clear')
    constE_1D_U = _callback_proxy('constE_1D_U')
    constE_1D_U2 = _callback_proxy('constE_1D_U2')
    constE_1D_V = _callback_proxy('constE_1D_V')
    constE_1D_V2 = _callback_proxy('constE_1D_V2')
    constEmap = _callback_proxy('constEmap')
    constQmap_1D = _callback_proxy('constQmap_1D')
    constQmap_1D2 = _callback_proxy('constQmap_1D2')
    constQmap_U = _callback_proxy('constQmap_U')
    constQmap_U2 = _callback_proxy('constQmap_U2')
    constQmap_V = _callback_proxy('constQmap_V')
    constQmap_V2 = _callback_proxy('constQmap_V2')
    data_box = _callback_proxy('data_box')
    disp3D = _callback_proxy('disp3D')
    file_select = _callback_proxy('file_select')
    remove_selected = _callback_proxy('remove_selected')
    gs_auto = _callback_proxy('gs_auto')
    gs_auto2 = _callback_proxy('gs_auto2')
    gs_clear = _callback_proxy('gs_clear')
    gs_clear2 = _callback_proxy('gs_clear2')
    gsp_auto = _callback_proxy('gsp_auto')
    gsp_clear = _callback_proxy('gsp_clear')
    high_harmo = _callback_proxy('high_harmo')
    initialize_param = _callback_proxy('initialize_param')
    load_param = _callback_proxy('load_param')
    loadfile = _callback_proxy('loadfile')
    low_harmo = _callback_proxy('low_harmo')
    maskall = _callback_proxy('maskall')
    maskclear = _callback_proxy('maskclear')
    mergefile = _callback_proxy('mergefile')
    mergefile_sb = _callback_proxy('mergefile_sb')
    on_entry_change = _callback_proxy('on_entry_change')
    p_set_range = _callback_proxy('p_set_range')
    pow_data_box = _callback_proxy('pow_data_box')
    range_auto_3D = _callback_proxy('range_auto_3D')
    save_param = _callback_proxy('save_param')
    sbclear = _callback_proxy('sbclear')
    sbfile_select = _callback_proxy('sbfile_select')
    sbremove_selected = _callback_proxy('sbremove_selected')
    scatter_2d_cE = _callback_proxy('scatter_2d_cE')
    scatter_2d_cU = _callback_proxy('scatter_2d_cU')
    scatter_2d_cV = _callback_proxy('scatter_2d_cV')
    set_range = _callback_proxy('set_range')
    show_1D_EvsI = _callback_proxy('show_1D_EvsI')
    show_1D_QvsI = _callback_proxy('show_1D_QvsI')
    show_3DconEmap = _callback_proxy('show_3DconEmap')
    show_powderEmap = _callback_proxy('show_powderEmap')
    simu_pow = _callback_proxy('simu_pow')
    simu_sc_cE = _callback_proxy('simu_sc_cE')
    simu_sc_cU = _callback_proxy('simu_sc_cU')
    simu_sc_cV = _callback_proxy('simu_sc_cV')
    switch_mode = _callback_proxy('switch_mode')
    threshold_auto = _callback_proxy('threshold_auto')
    time_estimate = _callback_proxy('time_estimate')
    trans_ELK = _callback_proxy('trans_ELK')
    tta_calc = _callback_proxy('tta_calc')
    update_UVlabel1 = _callback_proxy('update_UVlabel1')
    vclear = _callback_proxy('vclear')
    vfile_select = _callback_proxy('vfile_select')
    xaxis_select = _callback_proxy('xaxis_select')
    xaxis_selectp = _callback_proxy('xaxis_selectp')


    #windowの作成
    root=tk.Tk()
    #windowのタイトル変更
    root.title(f"ASYURA    ver: {__version__}")
    #windowのサイズ指定
    root.geometry("550x840")#550*840

    # フォント設定
    default_font_size = 10
    entry_font = ('Helvetica', default_font_size)
    #ttk.entry(フレーム名,text=*****,, font=entry_font)で統一可能。ラベルも同様。

    # ×ボタンを押すと作成したグラフ全てがクリアされる。
    # ウィンドウが閉じられたときの処理
    def on_closing():
        # すべてのグラフウィンドウを閉じる
        plt.close('all')
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)  # ウィンドウが閉じられるときの振る舞いを指定

    # gif画像を次のコマンドで文字列に変換(gifじゃないとダメ)
    # certutil -encode asyura_logo_w_trans.gif text3.txt

    # Application icon is stored in asyura_assets/icon_data.py

    # 選んだ画像を画面左上に埋め込み表示
    apply_app_icon(root) 

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=15)
    root.rowconfigure(1, weight=8)
    root.rowconfigure(2, weight=13)

    # ファイル選択のフレームの作成と設置

    # Build the GUI according to the application's visible hierarchy.
    layout_env = dict(globals())
    layout_env.update(locals())
    layout_env.update(build_dataset_information(layout_env))
    layout_env.update(build_sample_information(layout_env))
    layout_env.update(build_analysis_hub(layout_env))
    entry_u_var = layout_env["entry_u_var"]
    entry_v_var = layout_env["entry_v_var"]
    update_labels = layout_env["update_labels"]
    update_plabels = layout_env["update_plabels"]


    #メニューバーの作成
    menubar = tk.Menu(root)
    root.configure(menu=menubar)

    import csv

    #saveメニューの定義群
        

    #saveメニューの定義

    #saveメニューの定義

    #saveメニューの定義

    #saveメニューの定義

    #saveメニューの定義

    #saveメニューの定義
        
    #saveメニューの定義
        
    #saveメニューの定義
        
    #saveメニューの定義
        
    #saveメニューの定義

        
        
        


    # Bind export callbacks to the shared state dictionary once.
    save_FGdata = partial(_save_FGdata, state)
    save_BGdata = partial(_save_BGdata, state)
    save_constEmap = partial(_save_constEmap, state)
    save_hw_Umap = partial(_save_hw_Umap, state)
    save_hw_Vmap = partial(_save_hw_Vmap, state)
    save_1Dhw_I = partial(_save_1Dhw_I, state)
    save_1DI_U = partial(_save_1DI_U, state)
    save_1DI_V = partial(_save_1DI_V, state)
    save_hw_HKL = partial(_save_hw_HKL, state)
    save_hkl_HKL = partial(_save_hkl_HKL, state)
    save_I_HKL = partial(_save_I_HKL, state)
    save_I_hw = partial(_save_I_hw, state)
    save_masked_3d_data = partial(_save_masked_3d_data, state)
    save_masked_2dcE_data = partial(_save_masked_2dcE_data, state)
    save_masked_2dcU_data = partial(_save_masked_2dcU_data, state)
    save_masked_2dcV_data = partial(_save_masked_2dcV_data, state)
    save_2D_hw_qmap = partial(_save_2D_hw_qmap, state)
    save_1D_hwI_pow = partial(_save_1D_hwI_pow, state)
    save_1D_qI_pow = partial(_save_1D_qI_pow, state)

    #fileメニュー(単結晶)
    filemenu = tk.Menu(menubar,tearoff=0)
    menubar.add_cascade(label="Save Data (s.c.)",menu=filemenu)
    #fileメニューにsaveを追加
    filemenu.add_command(label="foreground table data",command=save_FGdata)
    #fileメニューにsaveを追加
    filemenu.add_command(label="background table data",command=save_BGdata)
    #fileメニューにsaveを追加
    filemenu.add_command(label=f"2D {entry_u_var.get()} vs {entry_v_var.get()}",command=save_constEmap)
    save_menu_index1 = filemenu.index(tk.END)
    #fileメニューにsaveを追加
    filemenu.add_command(label=f"2D {entry_v_var.get()} vs ℏω",command=save_hw_Vmap)
    save_menu_index2 = filemenu.index(tk.END)
    #fileメニューにsaveを追加
    filemenu.add_command(label=f"2D {entry_u_var.get()} vs ℏω",command=save_hw_Umap)
    save_menu_index3 = filemenu.index(tk.END)
    #fileメニューにsaveを追加
    filemenu.add_command(label="1D ℏω vs I",command=save_1Dhw_I)
    #fileメニューにsaveを追加
    filemenu.add_command(label=f"1D {entry_u_var.get()} vs I",command=save_1DI_U)
    save_menu_index4 = filemenu.index(tk.END)
    #fileメニューにsaveを追加
    filemenu.add_command(label=f"1D {entry_v_var.get()} vs I",command=save_1DI_V)
    save_menu_index5 = filemenu.index(tk.END)
    #fileメニューにsaveを追加
    filemenu.add_command(label=f"advanced 2D {entry_u_var.get()}-{entry_v_var.get()}",command=save_hkl_HKL)
    save_menu_index6 = filemenu.index(tk.END)
    #fileメニューにsaveを追加
    filemenu.add_command(label="advanced 2D hkl vs ℏω",command=save_hw_HKL)
    #fileメニューにsaveを追加
    filemenu.add_command(label="advanced 1D ℏω vs I",command=save_I_hw)
    #fileメニューにsaveを追加
    filemenu.add_command(label="advanced 1D hkl vs I",command=save_I_HKL)
    #fileメニューにsaveを追加
    filemenu.add_command(label="3D scattering data",command=save_masked_3d_data)
    #fileメニューにsaveを追加
    filemenu.add_command(label=f"2D {entry_u_var.get()} vs {entry_v_var.get()} scattering data",command=save_masked_2dcE_data)
    save_menu_index7 = filemenu.index(tk.END)
    #fileメニューにsaveを追加
    filemenu.add_command(label=f"2D {entry_v_var.get()} vs hw scattering data",command=save_masked_2dcU_data)
    save_menu_index8 = filemenu.index(tk.END)
    #fileメニューにsaveを追加
    filemenu.add_command(label=f"2D {entry_u_var.get()} vs hw scattering data",command=save_masked_2dcV_data)
    save_menu_index9 = filemenu.index(tk.END)
    #fileメニューにexitを追加。ついでにexit funcも実装
    filemenu.add_command(label="exit",command=lambda:root.destroy())

    #saveメニューの定義


    #saveメニューの定義

    #saveメニューの定義

    #fileメニュー(粉末)
    filemenu_p = tk.Menu(menubar,tearoff=0)
    menubar.add_cascade(label="Save Data (p.)",menu=filemenu_p)
    #fileメニューにsaveを追加
    filemenu_p.add_command(label="foreground table data",command=save_FGdata)
    #fileメニューにsaveを追加
    filemenu_p.add_command(label="background table data",command=save_BGdata)
    #fileメニューにsaveを追加
    filemenu_p.add_command(label="2D Q vs ℏω",command=save_2D_hw_qmap)#plt.pcolormesh(Q, hwlist_p , Ipow, cmap='jet', vmin=z_min, vmax=z_max)
    #fileメニューにsaveを追加
    filemenu_p.add_command(label="1D ℏω vs I",command=save_1D_hwI_pow)#plt.errorbar(energylist, Ipow_1dei, yerr=Ipowerr_1dei, capsize=10)
    #fileメニューにsaveを追加
    filemenu_p.add_command(label="1D Q vs I",command=save_1D_qI_pow)#plt.errorbar(Q2, Ipow_1dqi, yerr=Ipowerr_1dqi, capsize=10)
    #fileメニューにexitを追加。ついでにexit funcも実装
    filemenu_p.add_command(label="exit",command=lambda:root.destroy())

    '''
    #helpメニュー
    helpmenu = tk.Menu(menubar,tearoff=0)
    menubar.add_cascade(label="Support",menu=helpmenu)

    def copy_email_to_clipboard(email):
        pyperclip.copy(email)
        messagebox.showinfo("Copy to Clipboard", f"{email} has been copied to the clipboard.")

    def show_contact():
        email = "hodaka.kikuchi@issp.u-tokyo.ac.jp"
    
        # 連絡先情報のメッセージを作成
        contact_message = (
            "e-mail address:\n"
            f"{email}\n\n"
            "This software, if you have any questions, requests, or issues, please contact the email address above.\n"
            "When sending an email, please include 'ASYURA' in the subject to prevent it from being classified as spam.\n\n"
            "Would you like to copy the email address to the clipboard?\n"
        )
    
        # Yes/No ボタンの結果を取得
        result = messagebox.askyesno("Contact Information", contact_message, icon=messagebox.INFO)

        # Yes ボタンがクリックされた場合にのみクリップボードにコピー
        if result:
            copy_email_to_clipboard(email)

    #helpメニューにcontactを追加
    helpmenu.add_command(label="contact developer",command=show_contact)

    # HODACAのURLのリンク
    def open_manual():
        # HODACAのURLを指定
        manual_url = "https://sites.google.com/view/hodaca/%E3%83%9B%E3%83%BC%E3%83%A0"

        # 確認ダイアログを表示
        result = messagebox.askyesno("Confirmation", "Do you want to access the HODACA websiteℏ")

        # ユーザーがYesを選択した場合、URLをブラウザで開く
        if result:
            webbrowser.open(manual_url)

    # "Contact"メニュー項目を作成し、クリック時にopen_manual()関数を呼び出す
    helpmenu.add_command(label="HODACA web site", command=open_manual)
    '''
    ##########################################################################
    # labelの初回updateコマンド

    # Build the real callbacks now that every widget/figure/Tk variable has been created.
    # locals() is used only as an explicit construction-time environment; callbacks themselves
    # do not read module globals or the run_app() local namespace dynamically.
    callback_env = dict(layout_env)
    callback_env.update(locals())
    callback_registry.update(create_files_callbacks(callback_env))
    callback_registry.update(create_data_callbacks(callback_env))
    callback_registry.update(create_plots_callbacks(callback_env))
    callback_registry.update(create_powder_callbacks(callback_env))
    callback_registry.update(create_simulation_callbacks(callback_env))
    callback_registry.update(create_toolbox_callbacks(callback_env))

    # 初期表示のためにラベルを更新
    update_labels()
    update_plabels()

    # StringVarに変更があった時に呼ばれる関数をバインド
    # HKLの名称を変更する場合のtrace、メニューバーの名称を変更しているためここに無いと最初の立ち上げでエラーを吐く。ただしちゃんと反映はされる。
    entry_u_var.trace("w", update_UVlabel1)
    entry_v_var.trace("w", update_UVlabel1)

    # 初期値を設定
    entry_u_var.set("H")
    entry_v_var.set("K")

    #window状態の維持
    root.mainloop()

    #############
    # pyinstaller 
    # 最初にディレクトリ移動
    # cd C:\DATA_HK\python\ASYURA
    # pyinstaller -F --noconsole  --icon=ASYURA_logo.ico ASYURA.py

    # ORNLのPCではこれまでのコマンドが効かない
    # python -m PyInstaller --noconsole --onefile --add-data "ASYURA_logo.ico;." --icon=ASYURA_logo.ico ASYURA2.py

    # 次回から以下のコマンドでexe化する。うまくいったコマンド
    # pyinstaller -F --noconsole --icon=asyura.ico ASYURA.py
    # 2023/10/07 21:00以降 noconsoleが効かない。onefileにはできからよしとする
    # セキュリティソフトの問題らしい。endpoint antivirusを1時オフにしたけどできなかった。正直UIもよくわからんし、勝手にファイルを隔離するしでクソ。
    # 以下推奨。コンソールは表示されるけど、この問題が解決するまではこれで行く。
    # pyinstaller -F --icon=asyuraicon.ico ASYURA.py
    # 2023/10/08 なんかtrendアンチウイルスソフトの検索除外にこのディレクトリを指定したら以下のコマンドでも動くようになった。
    # pyinstaller -F --noconsole  --icon=ASYURA_logo.ico ASYURA.py
    """
    コマンド
    pyinstaller ASYURA.py --noconsole
    --onedir or -D
    出力を1ディレクトリにまとめる
    --onefile or -F
    出力を1ファイルにまとめる
    --noconsole or -w
    コンソールを表示しない
    --clean
    ビルド前に前回のキャッシュと出力ディレクトリを削除
    """


    #############


if __name__ == '__main__':
    run_app()
