"""Analysis Hub / ScanSim tab."""



def build_scansim(env):
    U_lavel = env['U_lavel']
    V_lavel = env['V_lavel']
    add_simu_pow = env['add_simu_pow']
    add_simu_sc_cE = env['add_simu_sc_cE']
    add_simu_sc_cU = env['add_simu_sc_cU']
    add_simu_sc_cV = env['add_simu_sc_cV']
    calc_add_constU_buttom = env['calc_add_constU_buttom']
    calc_add_constV_buttom = env['calc_add_constV_buttom']
    calc_constU_buttom = env['calc_constU_buttom']
    calc_constV_buttom = env['calc_constV_buttom']
    simu_pow = env['simu_pow']
    simu_sc_cE = env['simu_sc_cE']
    simu_sc_cU = env['simu_sc_cU']
    simu_sc_cV = env['simu_sc_cV']
    tab_03 = env['tab_03']
    time_estimate = env['time_estimate']
    tk = env['tk']
    ttk = env['ttk']

    ###############################################################################
    # simulation の項目

    # データボックスを作成するボタン周りのフレーム作成。
    frameS = ttk.Labelframe(tab_03, text= "Scan Range Simulation")
    frameS.grid(row=0,column=0,sticky="NSEW")
    #frameS.grid_propagate(True)

    frameS.columnconfigure(0, weight=1)
    frameS.columnconfigure(1, weight=1)
    frameS.rowconfigure(0, weight=2)
    frameS.rowconfigure(1, weight=1)

    # 単結晶用のフレームを作成
    frameS_SC = ttk.Labelframe(frameS, text= "Single Crystal1")
    frameS_SC.grid(row=0,column=0,rowspan=2,sticky="NSEW")
    #frameS_SC.grid_propagate(True)

    frameS_SC.columnconfigure(0, weight=1)
    frameS_SC.columnconfigure(1, weight=1)
    frameS_SC.columnconfigure(2, weight=1)
    frameS_SC.rowconfigure(0, weight=1)
    frameS_SC.rowconfigure(1, weight=1)
    frameS_SC.rowconfigure(2, weight=1)
    frameS_SC.rowconfigure(3, weight=1)
    frameS_SC.rowconfigure(4, weight=1)
    frameS_SC.rowconfigure(5, weight=1)
    frameS_SC.rowconfigure(6, weight=1)
    frameS_SC.rowconfigure(7, weight=1)
    frameS_SC.rowconfigure(8, weight=1)
    frameS_SC.rowconfigure(9, weight=1)

    # a2とc2の範囲を指定
    lbl_s1 = tk.Label(frameS_SC,text='min a2')
    lbl_s1.grid(row=0, column=0)
    txt_s1 = ttk.Entry(frameS_SC)
    txt_s1.insert(0,'34')
    txt_s1.grid(row=1, column=0,sticky="NSEW")

    lbl_s2 = tk.Label(frameS_SC,text='inc a2')
    lbl_s2.grid(row=0, column=1)
    txt_s2 = ttk.Entry(frameS_SC)
    txt_s2.insert(0,'1')
    txt_s2.grid(row=1, column=1,sticky="NSEW")

    lbl_s3 = tk.Label(frameS_SC,text='max a2')
    lbl_s3.grid(row=0, column=2)
    txt_s3 = ttk.Entry(frameS_SC)
    txt_s3.insert(0,'35')
    txt_s3.grid(row=1, column=2,sticky="NSEW")

    lbl_s4 = tk.Label(frameS_SC,text='min c2')
    lbl_s4.grid(row=2, column=0)
    txt_s4 = ttk.Entry(frameS_SC)
    txt_s4.insert(0,'0')
    txt_s4.grid(row=3, column=0,sticky="NSEW")

    lbl_s5 = tk.Label(frameS_SC,text='inc c2')
    lbl_s5.grid(row=2, column=1)
    txt_s5 = ttk.Entry(frameS_SC)
    txt_s5.insert(0,'2')
    txt_s5.grid(row=3, column=1,sticky="NSEW")

    lbl_s6 = tk.Label(frameS_SC,text='max c2')
    lbl_s6.grid(row=2, column=2)
    txt_s6 = ttk.Entry(frameS_SC)
    txt_s6.insert(0,'90')
    txt_s6.grid(row=3, column=2,sticky="NSEW")

    lbl_s7 = tk.Label(frameS_SC,text='min ℏω')
    lbl_s7.grid(row=4, column=0)
    txt_s7 = ttk.Entry(frameS_SC)
    txt_s7.insert(0,'0')
    txt_s7.grid(row=5, column=0,sticky="NSEW")

    lbl_s8 = tk.Label(frameS_SC,text='inc ℏω')
    lbl_s8.grid(row=4, column=1)
    txt_s8 = ttk.Entry(frameS_SC)
    txt_s8.insert(0,'0.1')
    txt_s8.grid(row=5, column=1,sticky="NSEW")

    lbl_s9 = tk.Label(frameS_SC,text='max ℏω')
    lbl_s9.grid(row=4, column=2)
    txt_s9 = ttk.Entry(frameS_SC)
    txt_s9.insert(0,'3')
    txt_s9.grid(row=5, column=2,sticky="NSEW")

    lbl_s10 = tk.Label(frameS_SC,text='ℏω')
    lbl_s10.grid(row=6, column=0)
    txt_s10 = ttk.Entry(frameS_SC)
    txt_s10.insert(0,'0')
    txt_s10.grid(row=7, column=0,sticky="NSEW")

    lbl_s11 = tk.Label(frameS_SC,textvariable=U_lavel)
    lbl_s11.grid(row=6, column=1)
    txt_s11 = ttk.Entry(frameS_SC)
    txt_s11.insert(0,'0')
    txt_s11.grid(row=7, column=1,sticky="NSEW")

    lbl_s12 = tk.Label(frameS_SC,textvariable=V_lavel)
    lbl_s12.grid(row=6, column=2)
    txt_s12 = ttk.Entry(frameS_SC)
    txt_s12.insert(0,'0')
    txt_s12.grid(row=7, column=2,sticky="NSEW")

    # ---- scan-simulation reciprocal-space helpers -------------------------------
    # This section uses the same coordinate policy as loadfile_UB_HKL_oblique_display.py:
    #   * SPICE UB + reference reflection determine the reciprocal-space geometry
    #     and c2 offset.  txt7/txt8 (old c2_off/Vt) are not used.
    #   * If a simple crystallographic in-plane vector perpendicular to U exists,
    #     it is used automatically as display V (e.g. hexagonal (100),(010)
    #     -> display V parallel to (-1,2,0)).
    #   * Otherwise the entered non-orthogonal U,V are retained as crystallographic
    #     coordinates and drawn on perpendicular screen axes.  A constant-|Q|
    #     circle therefore appears as an ellipse in this rectangular display.
    #
    # The following function is expected to exist in the main program:
    #   _make_crystallographic_display_basis
    #
    # The simulation geometry itself is self-contained here.  It follows the
    # UB-matrix PDF convention:
    #
    #     Q_lab = 2*pi * R_y(omega) * UB * HKL
    #
    # with the horizontal scattering plane in laboratory x-z and vertical y.





    # HODACA/SPICE instrument convention used here:
    # increasing C2 corresponds to increasing right-handed omega about +y.
    # If an instrument installation is known to use the opposite encoder sense,
    # this one constant is the only sign that should be changed.















    #constEのボタンを押した時の定義

    #constUのボタンを押した時の定義

    #constVのボタンを押した時の定義

    button_s1 = ttk.Button(frameS_SC, text="const E", command=simu_sc_cE)
    button_s1.grid(row=8, column=0,sticky="NSEW")

    #constUのボタンを押した時の定義

    button_s2 = ttk.Button(frameS_SC, command=simu_sc_cU,textvariable=calc_constU_buttom)
    button_s2.grid(row=8, column=1,sticky="NSEW")

    button_s3 = ttk.Button(frameS_SC, command=simu_sc_cV,textvariable=calc_constV_buttom)
    button_s3.grid(row=8, column=2,sticky="NSEW")

    #add add_simu_sc_cEのボタンを押した時の定義

    #add constVのボタンを押した時の定義

    button_s1a = ttk.Button(frameS_SC, text="add const E", command=add_simu_sc_cE)
    button_s1a.grid(row=9, column=0,sticky="NSEW")

    button_s2a = ttk.Button(frameS_SC, command=add_simu_sc_cU,textvariable=calc_add_constU_buttom)
    button_s2a.grid(row=9, column=1,sticky="NSEW")

    button_s3a = ttk.Button(frameS_SC, command=add_simu_sc_cV,textvariable=calc_add_constV_buttom)
    button_s3a.grid(row=9, column=2,sticky="NSEW")


    # 粉末用のフレームを作成
    frameS_pow = ttk.Labelframe(frameS, text= "Powder")
    frameS_pow.grid(row=0,column=1,sticky="NSEW")
    #frameS_pow.grid_propagate(True)

    frameS_pow.columnconfigure(0, weight=1)
    frameS_pow.columnconfigure(1, weight=1)
    frameS_pow.columnconfigure(2, weight=1)
    frameS_pow.rowconfigure(0, weight=1)
    frameS_pow.rowconfigure(1, weight=1)
    frameS_pow.rowconfigure(2, weight=1)
    frameS_pow.rowconfigure(3, weight=1)
    frameS_pow.rowconfigure(4, weight=1)

    # a2とhwの範囲を指定
    lbl_s1_1 = tk.Label(frameS_pow,text='min a2')
    lbl_s1_1.grid(row=0, column=0)
    txt_s1_1 = ttk.Entry(frameS_pow)
    txt_s1_1.insert(0,'34')
    txt_s1_1.grid(row=1, column=0,sticky="NSEW")

    lbl_s2_1 = tk.Label(frameS_pow,text='inc a2')
    lbl_s2_1.grid(row=0, column=1)
    txt_s2_1 = ttk.Entry(frameS_pow)
    txt_s2_1.insert(0,'1')
    txt_s2_1.grid(row=1, column=1,sticky="NSEW")

    lbl_s3_1 = tk.Label(frameS_pow,text='max a2')
    lbl_s3_1.grid(row=0, column=2)
    txt_s3_1 = ttk.Entry(frameS_pow)
    txt_s3_1.insert(0,'35')
    txt_s3_1.grid(row=1, column=2,sticky="NSEW")

    lbl_s4_1 = tk.Label(frameS_pow,text='min ℏω')
    lbl_s4_1.grid(row=2, column=0)
    txt_s4_1 = ttk.Entry(frameS_pow)
    txt_s4_1.insert(0,'0')
    txt_s4_1.grid(row=3, column=0,sticky="NSEW")

    lbl_s5_1 = tk.Label(frameS_pow,text='inc ℏω')
    lbl_s5_1.grid(row=2, column=1)
    txt_s5_1 = ttk.Entry(frameS_pow)
    txt_s5_1.insert(0,'0.1')
    txt_s5_1.grid(row=3, column=1,sticky="NSEW")

    lbl_s6_1 = tk.Label(frameS_pow,text='max ℏω')
    lbl_s6_1.grid(row=2, column=2)
    txt_s6_1 = ttk.Entry(frameS_pow)
    txt_s6_1.insert(0,'7')
    txt_s6_1.grid(row=3, column=2,sticky="NSEW")


    button_s2 = ttk.Button(frameS_pow, text="simu", command=simu_pow)
    button_s2.grid(row=4, column=0,sticky="NSEW")


    button_s2a = ttk.Button(frameS_pow, text="add simu", command=add_simu_pow)
    button_s2a.grid(row=4, column=2,sticky="NSEW")

    # 時間計算用
    frameS_T = ttk.Labelframe(frameS, text= "Time Estimate")
    frameS_T.grid(row=1,column=1,sticky="NSEW")
    #frameS_T.grid_propagate(True)

    frameS_T.columnconfigure(0, weight=1)
    frameS_T.columnconfigure(1, weight=1)
    frameS_T.columnconfigure(2, weight=1)
    frameS_T.columnconfigure(3, weight=1)
    frameS_T.columnconfigure(4, weight=1)
    frameS_T.rowconfigure(0, weight=1)
    frameS_T.rowconfigure(1, weight=1)

    # fluxのEi依存性
    # hw
    FE_x=[-0.485, -0.435, -0.384, -0.334, -0.285, -0.235, -0.185, -0.134, -0.085, -0.035, 0.016, 0.066, 0.115, 0.165, 0.214, 0.265, 0.315, 0.365, 0.415, 0.466, 0.5, 0.515, 0.565, 0.6, 0.7, 0.802, 0.901, 0.999, 1.101, 1.2, 1.301, 1.765, 2.165, 2.565, 2.965, 3.365, 3.765, 4.165, 4.565, 4.965, 5.365, 5.765, 6.165, 6.565, 6.965, 7.365]
    # CPS
    FE_y=[2561.31011, 2594.64212, 2633.54555, 2647.72387, 2682.38289, 2709.97367, 2741.19031, 2757.06989, 2777.31066, 2762.74889, 2497.15092, 2140.32882, 2171.19592, 2340.66631, 2409.86552, 2435.72529, 2436.12747, 2443.79417, 2434.92133, 2426.5117, 2393.83451, 2407.89903, 2368.85202, 2326.27319, 2273.22685, 2251.71695, 2239.75306, 2227.57927, 2193.46846, 2051.0658, 1846.2501, 1714.28571, 1714.28571, 1578.94737, 1518.98734, 1463.41463, 1276.59574, 1237.1134, 1165.04854, 1165.04854, 991.73554, 882.35294, 863.30935, 827.58621, 779.22078, 722.89157]

    # チェック有無変数
    CSPT = tk.IntVar()
    # value=0のラジオボタンにチェックを入れる
    CSPT.set(0)

    # ラジオボタン作成
    rdo_te1 = tk.Radiobutton(frameS_T, value=0, variable=CSPT, text='single')
    rdo_te1.grid(row=0,column=0, columnspan=2,sticky="")

    rdo_te2 = tk.Radiobutton(frameS_T, value=1, variable=CSPT, text='powder')
    rdo_te2.grid(row=0,column=2, columnspan=3,sticky="")

    # 時間見積もりの定義

    # 時間を計算するボタン
    button_te = ttk.Button(frameS_T, text="calc", command=time_estimate, width=6)
    button_te.grid(row=1, column=0,sticky="NSEW")

    # 時間を計算するボックス
    txt_teh = ttk.Entry(frameS_T,width=4)
    txt_teh.grid(row=1, column=1,sticky="NSEW")
    # 単位のラベル
    lbl_te = tk.Label(frameS_T,text='h')
    lbl_te.grid(row=1, column=2,sticky="NSEW")
    lbl_te = tk.Label(frameS_T,text='m')
    lbl_te.grid(row=1, column=4,sticky="NSEW")
    # 時間を計算するボックス
    txt_tem = ttk.Entry(frameS_T,width=4)
    txt_tem.grid(row=1, column=3,sticky="NSEW")

    result = dict(locals())
    result.pop('env', None)
    return result
