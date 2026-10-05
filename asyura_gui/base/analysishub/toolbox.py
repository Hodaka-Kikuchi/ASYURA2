"""Analysis Hub / Toolbox tab."""

import tkinter as tk
from tkinter import ttk

def build_toolbox(env):
    tab_04 = env['tab_04']
    tta_calc = env['tta_calc']
    high_harmo = env['high_harmo']
    low_harmo = env['low_harmo']
    trans_ELK = env['trans_ELK']
    # なんか色々計算できる便利なやーつ
    # 便利なやーつののフレームを作成
    frameS_cal = ttk.Labelframe(tab_04, text= "Calculation")
    frameS_cal.grid(row=0,column=0,sticky="NSEW")
    #frameS_cal.grid_propagate(True)

    frameS_cal.columnconfigure(0, weight=1)
    frameS_cal.columnconfigure(1, weight=1)
    frameS_cal.columnconfigure(2, weight=1)
    frameS_cal.columnconfigure(3, weight=1)
    frameS_cal.rowconfigure(0, weight=1)
    frameS_cal.rowconfigure(1, weight=1)
    frameS_cal.rowconfigure(2, weight=1)
    frameS_cal.rowconfigure(3, weight=1)
    frameS_cal.rowconfigure(4, weight=1)
    frameS_cal.rowconfigure(5, weight=1)
    frameS_cal.rowconfigure(6, weight=1)
    frameS_cal.rowconfigure(7, weight=1)

    # 指数を指定
    lbl_s1_2 = tk.Label(frameS_cal,text='h',width=6)
    lbl_s1_2.grid(row=0, column=1)
    txt_s1_2 = ttk.Entry(frameS_cal,width=5)
    txt_s1_2.insert(0,'0')
    txt_s1_2.grid(row=1, column=1,sticky="NSEW")

    lbl_s2_2 = tk.Label(frameS_cal,text='k',width=6)
    lbl_s2_2.grid(row=0, column=2)
    txt_s2_2 = ttk.Entry(frameS_cal,width=5)
    txt_s2_2.insert(0,'0')
    txt_s2_2.grid(row=1, column=2,sticky="NSEW")

    lbl_s3_2 = tk.Label(frameS_cal,text='l',width=6)
    lbl_s3_2.grid(row=0, column=3)
    txt_s3_2 = ttk.Entry(frameS_cal,width=5)
    txt_s3_2.insert(0,'0')
    txt_s3_2.grid(row=1, column=3,sticky="NSEW")

    lbl_s4_2hw = tk.Label(frameS_cal,text='ℏω (meV)',width=8)
    lbl_s4_2hw.grid(row=0, column=0)
    txt_s4_2hw = ttk.Entry(frameS_cal,width=6)
    txt_s4_2hw.insert(0,'0')
    txt_s4_2hw.grid(row=1, column=0,sticky="NSEW")

    lbl_s4_2f = tk.Label(frameS_cal,text='Ef (meV)',width=6)
    lbl_s4_2f.grid(row=2, column=0)
    txt_s4_2f = ttk.Entry(frameS_cal,width=6)
    txt_s4_2f.insert(0,'3.635')
    txt_s4_2f.grid(row=3, column=0,sticky="NSEW")

    lbl_s4_3 = tk.Label(frameS_cal,text='λ (Å)',width=6)
    lbl_s4_3.grid(row=2, column=1,pady=1)
    txt_s4_3 = ttk.Entry(frameS_cal,width=6)
    txt_s4_3.insert(0,'4.744')
    txt_s4_3.grid(row=3, column=1,sticky="NSEW")

    lbl_s4_4 = tk.Label(frameS_cal,text='k (Å^-1)',width=6)
    lbl_s4_4.grid(row=2, column=2)
    txt_s4_4 = ttk.Entry(frameS_cal,width=6)
    txt_s4_4.insert(0,'1.324')
    txt_s4_4.grid(row=3, column=2,sticky="NSEW")

    lbl_s5_2 = tk.Label(frameS_cal,text='2θ (deg)',width=8)
    lbl_s5_2.grid(row=6, column=0)
    txt_s5_2 = ttk.Entry(frameS_cal,width=10)
    txt_s5_2.grid(row=7, column=0,sticky="NSEW")

    lbl_s7_2 = tk.Label(frameS_cal,text='d (Å)',width=8)
    lbl_s7_2.grid(row=6, column=1)
    txt_s7_2 = ttk.Entry(frameS_cal,width=10)
    txt_s7_2.grid(row=7, column=1,sticky="NSEW")

    lbl_s6_2 = tk.Label(frameS_cal,text='Q (Å^-1)',width=8)
    lbl_s6_2.grid(row=6, column=2)
    txt_s6_2 = ttk.Entry(frameS_cal,width=10)
    txt_s6_2.grid(row=7, column=2,sticky="NSEW")


    button_s3 = ttk.Button(frameS_cal, text="calc", width=6, command=tta_calc)
    button_s3.grid(row=5, column=2,columnspan=2,sticky="NSEW")

    # λ/2のエネルギーで計算したい場合

    lbl_s6_2 = tk.Label(frameS_cal,text='harmonics',width=10)
    lbl_s6_2.grid(row=4, column=0,columnspan=2)
    button_s4 = ttk.Button(frameS_cal, text="λ/2", width=3, command=high_harmo)
    button_s4.grid(row=5, column=0,sticky="NSEW")

    # 2*λのエネルギーで計算したい場合

    button_s5 = ttk.Button(frameS_cal, text="2λ", width=3, command=low_harmo)
    button_s5.grid(row=5, column=1,sticky="NSEW")
    """
    # Eから換算したいとき
    def trans_E_to_LK():
        E=float(txt_s4_2f.get())
        L=9.045/(E**(1/2))
        K=2*3.1415926535/L
        txt_s4_3.delete(0,tk.END)
        txt_s4_4.delete(0,tk.END)
        txt_s4_3.insert(0,round(L,3))
        txt_s4_4.insert(0,round(K,3))

    # Lから換算したいとき
    def trans_L_to_EK():
        L=float(txt_s4_3.get())
        K=2*3.1415926535/L
        E=81.81/(L**(2))
        txt_s4_4.delete(0,tk.END)
        txt_s4_2f.delete(0,tk.END)
        txt_s4_4.insert(0,round(K,3))
        txt_s4_2f.insert(0,round(E,3))

    # Kから換算したいとき
    def trans_K_to_LE():
        K=float(txt_s4_4.get())
        L=2*3.1415926535/K
        E=81.81/(L**(2))
        txt_s4_3.delete(0,tk.END)
        txt_s4_2f.delete(0,tk.END)
        txt_s4_3.insert(0,round(L,3))
        txt_s4_2f.insert(0,round(E,3))

    button_s6 = ttk.Button(frameS_cal, text="calc E", width=6, command=trans_E_to_LK)
    button_s6.grid(row=3, column=0,sticky="NSEW")

    button_s7 = ttk.Button(frameS_cal, text="calc λ", width=6, command=trans_L_to_EK)
    button_s7.grid(row=7, column=0,pady=1,sticky="NSEW")

    button_s7 = ttk.Button(frameS_cal, text="calc k", width=6, command=trans_K_to_LE)
    button_s7.grid(row=9, column=0,pady=1,sticky="NSEW")
    """

    # エンターキーで計算を実行
    txt_s4_2f.bind("<Return>", trans_ELK)
    txt_s4_3.bind("<Return>", trans_ELK)
    txt_s4_4.bind("<Return>", trans_ELK)


    return {
        "frameS_cal": frameS_cal,
        "txt_s1_2": txt_s1_2,
        "txt_s2_2": txt_s2_2,
        "txt_s3_2": txt_s3_2,
        "txt_s4_2hw": txt_s4_2hw,
        "txt_s4_2f": txt_s4_2f,
        "txt_s4_3": txt_s4_3,
        "txt_s4_4": txt_s4_4,
        "txt_s5_2": txt_s5_2,
        "txt_s7_2": txt_s7_2,
        "txt_s6_2": txt_s6_2,
    }
