"""Analysis Hub / AngleCalc tab."""



def build_anglecalc(env):
    calculate_c2 = env['calculate_c2']
    tab_05 = env['tab_05']
    tk = env['tk']
    ttk = env['ttk']

    ###############################################################################
    # UB calculationからsample omegaを計算する

    # データボックスを作成するボタン周りのフレーム作成。
    frame_ub2 = ttk.Labelframe(tab_05, text= "Target Q Position (from Reference Peak1)")
    frame_ub2.grid(row = 0, column = 0, columnspan=2, sticky="NSEW")

    frame_ub2.columnconfigure(0, weight=1)
    frame_ub2.columnconfigure(1, weight=1)
    frame_ub2.columnconfigure(2, weight=1)
    frame_ub2.columnconfigure(3, weight=1)
    frame_ub2.columnconfigure(4, weight=1)
    frame_ub2.rowconfigure(0, weight=1)
    frame_ub2.rowconfigure(1, weight=1)

    # UB matrixを表示するフレーム作成。
    frame_ub4 = ttk.Labelframe(tab_05, text= "UB matrix")
    frame_ub4.grid(row = 1, column = 0,sticky="NSEW")

    frame_ub4.columnconfigure(0, weight=1)
    frame_ub4.columnconfigure(1, weight=1)
    frame_ub4.columnconfigure(2, weight=1)
    frame_ub4.rowconfigure(0, weight=1)
    frame_ub4.rowconfigure(1, weight=1)
    frame_ub4.rowconfigure(2, weight=1)

    # データボックスを作成するボタン周りのフレーム作成。
    frame_ub3 = ttk.Labelframe(tab_05, text= "Angle Calculation")
    frame_ub3.grid(row = 2, column = 0,columnspan=2, sticky="NSEW")

    frame_ub3.columnconfigure(0, weight=1)
    frame_ub3.columnconfigure(1, weight=1)
    frame_ub3.columnconfigure(2, weight=1)
    frame_ub3.columnconfigure(3, weight=1)
    frame_ub3.columnconfigure(4, weight=1)
    frame_ub3.columnconfigure(5, weight=1)
    frame_ub3.rowconfigure(0, weight=1)
    frame_ub3.rowconfigure(1, weight=1)
    frame_ub3.rowconfigure(2, weight=2)

    # hardware limitを表示するフレーム作成。
    frame_ub5 = ttk.Labelframe(tab_05, text= "Hardware Limit")
    frame_ub5.grid(row = 1, column = 1,sticky="NSEW")

    frame_ub5.columnconfigure(0, weight=1)
    frame_ub5.columnconfigure(1, weight=1)
    frame_ub5.columnconfigure(2, weight=1)
    frame_ub5.columnconfigure(3, weight=1)
    frame_ub5.rowconfigure(0, weight=1)
    frame_ub5.rowconfigure(1, weight=1)
    frame_ub5.rowconfigure(2, weight=1)

    # Bragg Peak Position frame is no longer used here.
    # The reference reflection and its motor positions are read directly from
    # the reference Peak1 entries:
    #   txt_ref_h, txt_ref_k, txt_ref_l
    #   txt_ref_c2, txt_ref_a2, txt_ref_ry, txt_ref_rx
    #   txt_ref_ei, txt_ref_ef
    #
    # If frame_ub1 itself is created elsewhere only for the old
    # "Bragg Peak Position" panel, its creation/grid call can be removed there.

    # hwの入力
    lbl_ubc_0 = tk.Label(frame_ub2,text='ℏω')
    lbl_ubc_0.grid(row=0, column=0)
    txt_ubc_0 = ttk.Entry(frame_ub2)
    txt_ubc_0.insert(0,'0')
    txt_ubc_0.grid(row=1, column=0,sticky="NSEW")

    # 指数を指定
    lbl_ubc_1 = tk.Label(frame_ub2,text='h')
    lbl_ubc_1.grid(row=0, column=1)
    txt_ubc_1 = ttk.Entry(frame_ub2)
    txt_ubc_1.insert(0,'0')
    txt_ubc_1.grid(row=1, column=1,sticky="NSEW")

    lbl_ubc_2 = tk.Label(frame_ub2,text='k')
    lbl_ubc_2.grid(row=0, column=2)
    txt_ubc_2 = ttk.Entry(frame_ub2)
    txt_ubc_2.insert(0,'0')
    txt_ubc_2.grid(row=1, column=2,sticky="NSEW")

    lbl_ubc_3 = tk.Label(frame_ub2,text='l')
    lbl_ubc_3.grid(row=0, column=3)
    txt_ubc_3 = ttk.Entry(frame_ub2)
    txt_ubc_3.insert(0,'0')
    txt_ubc_3.grid(row=1, column=3,sticky="NSEW")

    # UBmatrixの表示
    txt_ub_11 = ttk.Entry(frame_ub4,state="readonly")
    txt_ub_11.insert(0,'0')
    txt_ub_11.grid(row=0, column=0,sticky="NSEW")
    txt_ub_12 = ttk.Entry(frame_ub4,state="readonly")
    txt_ub_12.insert(0,'0')
    txt_ub_12.grid(row=0, column=1,sticky="NSEW")
    txt_ub_13 = ttk.Entry(frame_ub4,state="readonly")
    txt_ub_13.insert(0,'0')
    txt_ub_13.grid(row=0, column=2,sticky="NSEW")
    txt_ub_21 = ttk.Entry(frame_ub4,state="readonly")
    txt_ub_21.insert(0,'0')
    txt_ub_21.grid(row=1, column=0,sticky="NSEW")
    txt_ub_22 = ttk.Entry(frame_ub4,state="readonly")
    txt_ub_22.insert(0,'0')
    txt_ub_22.grid(row=1, column=1,sticky="NSEW")
    txt_ub_23 = ttk.Entry(frame_ub4,state="readonly")
    txt_ub_23.insert(0,'0')
    txt_ub_23.grid(row=1, column=2,sticky="NSEW")
    txt_ub_31 = ttk.Entry(frame_ub4,state="readonly")
    txt_ub_31.insert(0,'0')
    txt_ub_31.grid(row=2, column=0,sticky="NSEW")
    txt_ub_32 = ttk.Entry(frame_ub4,state="readonly")
    txt_ub_32.insert(0,'0')
    txt_ub_32.grid(row=2, column=1,sticky="NSEW")
    txt_ub_33 = ttk.Entry(frame_ub4,state="readonly")
    txt_ub_33.insert(0,'0')
    txt_ub_33.grid(row=2, column=2,sticky="NSEW")

    # angle calculationの結果表示
    lbl_ubc_r1 = tk.Label(frame_ub3,text='C1')
    lbl_ubc_r1.grid(row=0, column=0)
    txt_ubc_r1 = ttk.Entry(frame_ub3,state="readonly")
    txt_ubc_r1.insert(0,'0')
    txt_ubc_r1.grid(row=1, column=0,sticky="NSEW")

    lbl_ubc_r2 = tk.Label(frame_ub3,text='A1')
    lbl_ubc_r2.grid(row=0, column=1)
    txt_ubc_r2 = ttk.Entry(frame_ub3,state="readonly")
    txt_ubc_r2.insert(0,'0')
    txt_ubc_r2.grid(row=1, column=1,sticky="NSEW")

    lbl_ubc_r3 = tk.Label(frame_ub3,text='C2')
    lbl_ubc_r3.grid(row=0, column=2)
    txt_ubc_r3 = ttk.Entry(frame_ub3,state="readonly")
    txt_ubc_r3.insert(0,'0')
    txt_ubc_r3.grid(row=1, column=2,sticky="NSEW")

    lbl_ubc_r4 = tk.Label(frame_ub3,text='A2')
    lbl_ubc_r4.grid(row=0, column=3)
    txt_ubc_r4 = ttk.Entry(frame_ub3,state="readonly")
    txt_ubc_r4.insert(0,'0')
    txt_ubc_r4.grid(row=1, column=3,sticky="NSEW")

    lbl_ubc_r5 = tk.Label(frame_ub3,text='rx')
    lbl_ubc_r5.grid(row=0, column=4)
    txt_ubc_r5 = ttk.Entry(frame_ub3,state="readonly")
    txt_ubc_r5.insert(0,'0')
    txt_ubc_r5.grid(row=1, column=4,sticky="NSEW")

    lbl_ubc_r6 = tk.Label(frame_ub3,text='ry')
    lbl_ubc_r6.grid(row=0, column=5)
    txt_ubc_r6 = ttk.Entry(frame_ub3,state="readonly")
    txt_ubc_r6.insert(0,'0')
    txt_ubc_r6.grid(row=1, column=5,sticky="NSEW")

    lbl_ubc_m1 = tk.Label(frame_ub3,text='warning')
    lbl_ubc_m1.grid(row=2, column=0)

    lbl_ubc_m2 = tk.Label(frame_ub3,text='')
    lbl_ubc_m2.grid(row=2, column=1,columnspan=5)

    # hardware limitの入力
    lbl_ubc_hl1 = tk.Label(frame_ub5,text='A1', width=16)
    lbl_ubc_hl1.grid(row=0, column=0)
    txt_ubc_hl11 = ttk.Entry(frame_ub5)
    txt_ubc_hl11.insert(0,'39.861')
    txt_ubc_hl11.grid(row=0, column=1,sticky="NSEW")
    lbl_ubc_hl1 = tk.Label(frame_ub5,text='~', width=16)
    lbl_ubc_hl1.grid(row=0, column=2)
    txt_ubc_hl12 = ttk.Entry(frame_ub5)
    txt_ubc_hl12.insert(0,'116.964')
    txt_ubc_hl12.grid(row=0, column=3,sticky="NSEW")

    lbl_ubc_hl2 = tk.Label(frame_ub5,text='C2', width=16)
    lbl_ubc_hl2.grid(row=1, column=0)
    txt_ubc_hl21 = ttk.Entry(frame_ub5)
    txt_ubc_hl21.insert(0,'-135')
    txt_ubc_hl21.grid(row=1, column=1,sticky="NSEW")
    lbl_ubc_hl2 = tk.Label(frame_ub5,text='~', width=16)
    lbl_ubc_hl2.grid(row=1, column=2)
    txt_ubc_hl22 = ttk.Entry(frame_ub5)
    txt_ubc_hl22.insert(0,'150')
    txt_ubc_hl22.grid(row=1, column=3,sticky="NSEW")

    lbl_ubc_hl3 = tk.Label(frame_ub5,text='A2', width=16)
    lbl_ubc_hl3.grid(row=2, column=0)
    txt_ubc_hl31 = ttk.Entry(frame_ub5)
    txt_ubc_hl31.insert(0,'6')
    txt_ubc_hl31.grid(row=2, column=1,sticky="NSEW")
    lbl_ubc_hl3 = tk.Label(frame_ub5,text='~', width=16)
    lbl_ubc_hl3.grid(row=2, column=2)
    txt_ubc_hl32 = ttk.Entry(frame_ub5)
    txt_ubc_hl32.insert(0,'120')
    txt_ubc_hl32.grid(row=2, column=3,sticky="NSEW")

    # SPICEのファイルからUBパラメータを読みだし、
    # Sample Information に読み込まれている reference Peak1 を基準として、
    # "Target Q position (from Reference peak1)" に入力された (H,K,L,hw) に必要な
    # C1, A1, C2, A2, mu, nu を計算する。
    #
    # reference Peak1:
    #   txt_ref_h, txt_ref_k, txt_ref_l
    #   txt_ref_c2, txt_ref_a2
    #   txt_ref_ry, txt_ref_rx
    #   txt_ref_ei, txt_ref_ef
    #
    # target:
    #   txt_ubc_0      : energy transfer hw [meV]
    #   txt_ubc_1..3   : target (H,K,L)
    #
    # 重要:
    #   PDF の回転順序を使うが、SPICE の mu モーター正方向は
    #   PDF の右手系 Rz(+mu) と逆向きなので
    #
    #       Rz_SPICE(mu) = Rz_PDF(-mu)
    #
    #   として扱う。
    #
    #   reference Peak1 の mu,nu は絶対モーター角として回転に含める。
    #   一つの Q ベクトルだけでは (C2, mu, nu) は1自由度余るため、
    #   target では reference Peak1 からの tilt 移動
    #
    #       (mu-mu_ref)^2 + (nu-nu_ref)^2
    #
    #   が最小になる解を採用する。
    #
    # SPICE UB は明示的な 2*pi を含まないものとして扱う。





    # SPICE出力ファイルからUBマトリックスを読み込みC2を自動入力
    button_ubc_1 = ttk.Button(
        frame_ub2,
        text="calc",
        command=calculate_c2,
        width=16,
    )
    button_ubc_1.grid(row=1, column=4, sticky="NSEW")


    ###############################################################################
    #サブウィンドウでfittingプログラムを作成する。

    ###############################################################################

    result = dict(locals())
    result.pop('env', None)
    return result
