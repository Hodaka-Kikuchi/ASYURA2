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

# Numerical helpers.  The GUI layer imports from the fine-grained core packages.
from asyura_core.geometry.angles import (
    _normalize_angle_deg, _spice_raw_Rx_deg, _spice_raw_Ry_deg,
    _data_Ry_deg, _data_Rz_deg, _data_Rx_deg, _rotation_z_deg,
    _normalize_simu_angle_deg, _simu_Ry_deg,
)
from asyura_core.geometry.tilt import (
    _spice_tilt_matrix_raw, _spice_relative_tilt_in_pdf,
)
from asyura_core.geometry.q_vectors import _data_q_lab, _simu_q_lab
from asyura_core.geometry.reference import (
    DATA_C2_TO_OMEGA_SIGN, SIMU_C2_TO_OMEGA_SIGN,
    _calculate_data_reference_omega, _calculate_simu_reference_omega,
)
from asyura_core.geometry.conversion import (
    _angles_to_hkl_and_uv, _simu_hkl_text, _simu_angles_to_rlu,
)
from asyura_core.ub import (
    _parse_spice_ub_from_dat, _canonicalize_spice_ub_for_pdf,
    _make_B_from_lattice_for_simulation, _make_simulation_ub_from_lattice_uv,
    _find_simple_orthogonal_inplane_hkl, _make_crystallographic_display_basis,
    _display_uv_to_hkl,
)
from asyura_core.data_processing import (
    bin_single_crystal_data, get_single_crystal_map_energy_axis,
)
from asyura_core.physics_tools import (
    energy_to_wavelength_wavenumber, wavelength_to_energy_wavenumber,
    wavenumber_to_energy_wavelength, harmonic_energy, reciprocal_q_and_d,
    tas_scattering_angle_deg,
)
from asyura_core.export import (
    save_FGdata as _save_FGdata, save_BGdata as _save_BGdata,
    save_constEmap as _save_constEmap, save_hw_Umap as _save_hw_Umap,
    save_hw_Vmap as _save_hw_Vmap, save_1Dhw_I as _save_1Dhw_I,
    save_1DI_U as _save_1DI_U, save_1DI_V as _save_1DI_V,
    save_hw_HKL as _save_hw_HKL, save_hkl_HKL as _save_hkl_HKL,
    save_I_HKL as _save_I_HKL, save_I_hw as _save_I_hw,
    save_masked_3d_data as _save_masked_3d_data,
    save_masked_2dcE_data as _save_masked_2dcE_data,
    save_masked_2dcU_data as _save_masked_2dcU_data,
    save_masked_2dcV_data as _save_masked_2dcV_data,
    save_2D_hw_qmap as _save_2D_hw_qmap,
    save_1D_hwI_pow as _save_1D_hwI_pow, save_1D_qI_pow as _save_1D_qI_pow,
)


# Export private helper names too; callback modules mirror the original app.py module namespace.
__all__ = [name for name in globals() if not name.startswith("__")]
