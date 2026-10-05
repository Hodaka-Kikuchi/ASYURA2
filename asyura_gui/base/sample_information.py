"""Sample Information GUI section."""



def build_sample_information(env):
    alpha = env['alpha']
    beta = env['beta']
    entry_u_var = env['entry_u_var']
    entry_v_var = env['entry_v_var']
    gamma = env['gamma']
    initialize_param = env['initialize_param']
    load_param = env['load_param']
    loadfile = env['loadfile']
    root = env['root']
    save_param = env['save_param']
    state = env['state']
    tk = env['tk']
    ttk = env['ttk']

    frame3 = ttk.Labelframe(root, text= "Sample Information")
    frame3.grid(row=1,column=0,padx=5,sticky="NSEW")
    #frame3.grid_propagate(True)

    # グリッドの重みを設定
    #tab_001.columnconfigure(0, weight=1)
    #tab_001.rowconfigure(0, weight=1)
    frame3.columnconfigure(0, weight=1)
    frame3.columnconfigure(1, weight=1)
    frame3.columnconfigure(2, weight=1)
    frame3.columnconfigure(3, weight=1)
    frame3.columnconfigure(4, weight=1)
    frame3.columnconfigure(5, weight=1)
    frame3.columnconfigure(6, weight=1)
    frame3.columnconfigure(7, weight=1)
    frame3.rowconfigure(0, weight=1)
    frame3.rowconfigure(1, weight=1)
    frame3.rowconfigure(2, weight=1)
    frame3.rowconfigure(3, weight=1)
    frame3.rowconfigure(4, weight=1)
    frame3.rowconfigure(5, weight=1)
    frame3.rowconfigure(6, weight=0)

    # 格子定数を入力欄ラベル
    lbl1 = tk.Label(frame3,text='a',width=6)
    lbl1.grid(row=0, column=0, sticky="NSEW")
    lbl2 = tk.Label(frame3,text='b',width=6)
    lbl2.grid(row=0, column=1, sticky="NSEW")
    lbl3 = tk.Label(frame3,text='c',width=6)
    lbl3.grid(row=0, column=2, sticky="NSEW")

    # 格子定数の入力欄
    txt1 = ttk.Entry(frame3,width=6)
    txt1.grid(row=1, column=0, sticky="NSEW")
    txt2 = ttk.Entry(frame3,width=6)
    txt2.grid(row=1, column=1, sticky="NSEW")
    txt3 = ttk.Entry(frame3,width=6)
    txt3.grid(row=1, column=2, sticky="NSEW")

    # alpha,beta,gammaの入力欄ラベル
    lbl4 = tk.Label(frame3,text=alpha,width=6)
    lbl4.grid(row=2, column=0, sticky="NSEW")
    lbl5 = tk.Label(frame3,text=beta,width=6)
    lbl5.grid(row=2, column=1, sticky="NSEW")
    lbl6 = tk.Label(frame3,text=gamma,width=6)
    lbl6.grid(row=2, column=2, sticky="NSEW")

    # alpha,beta,gammaの入力欄
    txt4 = ttk.Entry(frame3,width=6)
    txt4.grid(row=3, column=0, sticky="NSEW")
    txt5 = ttk.Entry(frame3,width=6)
    txt5.grid(row=3, column=1, sticky="NSEW")
    txt6 = ttk.Entry(frame3,width=6)
    txt6.grid(row=3, column=2, sticky="NSEW")

    # mcu規格化の入力欄ラベルと入力欄
    lbl15 = tk.Label(frame3,text='N_mcu',width=6)
    lbl15.grid(row=4, column=0, sticky="NSEW")
    txt15 = ttk.Entry(frame3,width=6)
    txt15.grid(row=5, column=0, sticky="NSEW")
    txt15.insert(0,'1') # デフォルト1分でええやろ

    # ダミーのラベル欄
    #lbl_sp = tk.Label(frame3,text='',width=1)
    #lbl_sp.grid(row=3, column=3, sticky="NSEW")

    # UVベクトルの入力欄ラベル
    lbl9 = tk.Label(frame3,text='U1',width=6)
    lbl9.grid(row=0, column=4, sticky="NSEW")
    lbl10 = tk.Label(frame3,text='U2',width=6)
    lbl10.grid(row=0, column=5, sticky="NSEW")
    lbl11 = tk.Label(frame3,text='U3',width=6)
    lbl11.grid(row=0, column=6, sticky="NSEW")
    lbl12 = tk.Label(frame3,text='V1',width=6)
    lbl12.grid(row=2, column=4, sticky="NSEW")
    lbl13 = tk.Label(frame3,text='V2',width=6)
    lbl13.grid(row=2, column=5, sticky="NSEW")
    lbl14 = tk.Label(frame3,text='V3',width=6)
    lbl14.grid(row=2, column=6, sticky="NSEW")

    # Uベクトルの入力欄
    txt9 = ttk.Entry(frame3,width=6)
    txt9.grid(row=1, column=4, sticky="NSEW")
    txt10 = ttk.Entry(frame3,width=6)
    txt10.grid(row=1, column=5, sticky="NSEW")
    txt11 = ttk.Entry(frame3,width=6)
    txt11.grid(row=1, column=6, sticky="NSEW")

    # Uベクトルの名前入力欄
    lbl_ul = tk.Label(frame3,text='U label',width=6)
    lbl_ul.grid(row=0, column=7, sticky="NSEW")
    txt_ul = ttk.Entry(frame3, textvariable=entry_u_var,width=6)
    txt_ul.grid(row=1, column=7, sticky="NSEW")

    # Vベクトルの入力欄
    txt12 = ttk.Entry(frame3,width=6)
    txt12.grid(row=3, column=4, sticky="NSEW")
    txt13 = ttk.Entry(frame3,width=6)
    txt13.grid(row=3, column=5, sticky="NSEW")
    txt14 = ttk.Entry(frame3,width=6)
    txt14.grid(row=3, column=6, sticky="NSEW")

    # Vベクトルの名前入力欄
    lbl_vl = tk.Label(frame3,text='V label',width=6)
    lbl_vl.grid(row=2, column=7, sticky="NSEW")
    txt_vl = ttk.Entry(frame3, textvariable=entry_v_var,width=6)
    txt_vl.grid(row=3, column=7, sticky="NSEW")

    # reference frame
    frame3r = ttk.Labelframe(frame3,text='Reference peak1')
    frame3r.grid(row=4,rowspan=2, column=1,columnspan=7,sticky="NSEW")

    frame3r.columnconfigure(0, weight=1)
    frame3r.columnconfigure(1, weight=1)
    frame3r.columnconfigure(2, weight=1)
    frame3r.columnconfigure(3, weight=1)
    frame3r.columnconfigure(4, weight=1)
    frame3r.columnconfigure(5, weight=1)
    frame3r.columnconfigure(6, weight=1)
    frame3r.columnconfigure(7, weight=1)
    frame3r.columnconfigure(8, weight=1)
    frame3r.rowconfigure(0, weight=1)
    frame3r.rowconfigure(1, weight=1)

    # refベクトルのラベル
    lbl_ref_h = tk.Label(frame3r,text='ref H')
    lbl_ref_h.grid(row=0, column=0, sticky="NSEW")
    lbl_ref_k = tk.Label(frame3r,text='ref K')
    lbl_ref_k.grid(row=0, column=1, sticky="NSEW")
    lbl_ref_l = tk.Label(frame3r,text='ref L')
    lbl_ref_l.grid(row=0, column=2, sticky="NSEW")
    lbl_ref_c2 = tk.Label(frame3r,text='ref c2')
    lbl_ref_c2.grid(row=0, column=3, sticky="NSEW")
    lbl_ref_a2 = tk.Label(frame3r,text='ref a2')
    lbl_ref_a2.grid(row=0, column=4, sticky="NSEW")
    lbl_ref_rx = tk.Label(frame3r,text='ref rx')
    lbl_ref_rx.grid(row=0, column=5, sticky="NSEW")
    lbl_ref_ry = tk.Label(frame3r,text='ref ry')
    lbl_ref_ry.grid(row=0, column=6, sticky="NSEW")
    lbl_ref_ei = tk.Label(frame3r,text='ref Ei')
    lbl_ref_ei.grid(row=0, column=7, sticky="NSEW")
    lbl_ref_ef = tk.Label(frame3r,text='ref Ef')
    lbl_ref_ef.grid(row=0, column=8, sticky="NSEW")

    # refベクトルの入力欄
    txt_ref_h = ttk.Entry(frame3r,width=6)
    txt_ref_h.grid(row=1, column=0, sticky="NSEW")
    txt_ref_k = ttk.Entry(frame3r,width=6)
    txt_ref_k.grid(row=1, column=1, sticky="NSEW")
    txt_ref_l = ttk.Entry(frame3r,width=6)
    txt_ref_l.grid(row=1, column=2, sticky="NSEW")
    txt_ref_c2 = ttk.Entry(frame3r,width=6)
    txt_ref_c2.grid(row=1, column=3, sticky="NSEW")
    txt_ref_a2 = ttk.Entry(frame3r,width=6)
    txt_ref_a2.grid(row=1, column=4, sticky="NSEW")
    txt_ref_rx = ttk.Entry(frame3r,width=6)
    txt_ref_rx.grid(row=1, column=5, sticky="NSEW")
    txt_ref_ry = ttk.Entry(frame3r,width=6)
    txt_ref_ry.grid(row=1, column=6, sticky="NSEW")
    txt_ref_ei = ttk.Entry(frame3r,width=6)
    txt_ref_ei.grid(row=1, column=7, sticky="NSEW")
    txt_ref_ef = ttk.Entry(frame3r,width=6)
    txt_ref_ef.grid(row=1, column=8, sticky="NSEW")

    ##############################################################
    # これまでに打ち込んだ数値群を保存する。

    ##################################################################

    #ファイルの読み込みのボタンの作成
    button4 = ttk.Button(frame3,text="save param",command=save_param)
    button4.grid(row=6, column=0, sticky="NSEW")

    # SPICEのファイルからパラメータを読みだす。 

    #SPICE出力ファイルを読み込みサンプル情報をボックスに自動入力してくれるボタンの作成
    button5 = ttk.Button(frame3,text="initialize",command=initialize_param)
    button5.grid(row=6, column=2, sticky="NSEW")


    #csv形式で保存したパラメータを呼び出すボタン
    button5_2 = ttk.Button(frame3,text="load param",command=load_param)
    button5_2.grid(row=6, column=1, sticky="NSEW")

    # 空のプログレスバーを表示
    state['pb'] = ttk.Progressbar(frame3, orient="horizontal", mode="determinate")
    state['pb'].grid(row=6, column=6, columnspan=2, sticky="NSEW")

    # ============================================================
    # UB / reciprocal-space helper functions
    # ============================================================







    # ---- reciprocal-space display helpers ---------------------------------------
    # These helpers implement two display modes automatically:
    #   1) If a physically orthogonal crystallographic in-plane vector can be
    #      represented by a simple integer combination of the entered U,V, use it.
    #      The display is then an ordinary Cartesian Q map (circles remain circles).
    #   2) Otherwise keep the entered non-orthogonal U,V as the crystallographic
    #      axes, but draw those two axes orthogonally on the screen.  This is an
    #      oblique-coordinate -> rectangular-display transformation, so a constant
    #      |Q| circle generally appears as an ellipse.
    #
    # SPICE UB is assumed not to contain 2*pi, consistent with Q = 2*pi*UB*HKL.
























    # Same encoder sense that reproduced the corrected scan simulation.








    #ファイルの読み込みのボタンの作成:
    button6 = ttk.Button(frame3,text="load data file(s)",command=loadfile)
    button6.grid(row=6, column=4,columnspan=2, sticky="NSEW")

    ############################################################
    # 単結晶と粉末とシミュレーションで切り替えるフレームを作成

    # まずは単結晶
    # ファイル選択のフレームの作成と設置

    result = dict(locals())
    result.pop('env', None)
    return result
