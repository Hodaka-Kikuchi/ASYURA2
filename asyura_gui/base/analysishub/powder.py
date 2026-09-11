"""Analysis Hub / Powder tab."""



def build_powder(env):
    bgt_lbl1 = env['bgt_lbl1']
    bgt_txt1 = env['bgt_txt1']
    btn_click_1DPE = env['btn_click_1DPE']
    btn_click_1DPQ = env['btn_click_1DPQ']
    fgt_lbl1 = env['fgt_lbl1']
    fgt_txt1 = env['fgt_txt1']
    gsp_auto = env['gsp_auto']
    gsp_clear = env['gsp_clear']
    np = env['np']
    p_set_range = env['p_set_range']
    plt = env['plt']
    pow_data_box = env['pow_data_box']
    show_1D_EvsI = env['show_1D_EvsI']
    show_1D_QvsI = env['show_1D_QvsI']
    show_powderEmap = env['show_powderEmap']
    state = env['state']
    tab_02 = env['tab_02']
    tk = env['tk']
    ttk = env['ttk']
    xaxis_selectp = env['xaxis_selectp']

    frame1p = ttk.Labelframe(tab_02, text= "Data Construction")
    frame1p.grid(row = 0, column = 0,columnspan=2,sticky="NSEW")
    #frame1p.grid_propagate(True)

    frame1p.columnconfigure(0, weight=1)
    frame1p.columnconfigure(1, weight=1)
    frame1p.columnconfigure(2, weight=1)
    frame1p.columnconfigure(3, weight=1)
    frame1p.columnconfigure(4, weight=1)
    frame1p.columnconfigure(5, weight=1)
    frame1p.columnconfigure(6, weight=1)
    frame1p.columnconfigure(7, weight=1)
    frame1p.columnconfigure(8, weight=1)
    frame1p.rowconfigure(0, weight=1)
    frame1p.rowconfigure(1, weight=1)
    frame1p.rowconfigure(2, weight=1)

    # hw範囲とQ範囲とbin sizeの入力欄
    lbl04_p = tk.Label(frame1p,text='min ℏω',width=6)
    lbl04_p.grid(row=0, column=0,sticky="NSEW")
    txt04_p = ttk.Entry(frame1p,width=6)
    txt04_p.grid(row=1, column=0,sticky="NSEW")

    lbl05_p = tk.Label(frame1p,text='max ℏω',width=6)
    lbl05_p.grid(row=0, column=1,sticky="NSEW")
    txt05_p = ttk.Entry(frame1p,width=6)
    txt05_p.grid(row=1, column=1,sticky="NSEW")

    lbl06_p = tk.Label(frame1p,text='bin ℏω',width=6)
    lbl06_p.grid(row=0, column=2,sticky="NSEW")
    txt06_p = ttk.Entry(frame1p,width=6)
    txt06_p.grid(row=1, column=2,sticky="NSEW")

    lbl01_p = tk.Label(frame1p,text='min Q',width=6)
    lbl01_p.grid(row=0, column=3,sticky="NSEW")
    txt01_p = ttk.Entry(frame1p,width=6)
    txt01_p.grid(row=1, column=3,sticky="NSEW")

    lbl02_p = tk.Label(frame1p,text='max Q',width=6)
    lbl02_p.grid(row=0, column=4,sticky="NSEW")
    txt02_p = ttk.Entry(frame1p,width=6)
    txt02_p.grid(row=1, column=4,sticky="NSEW")

    lbl03_p = tk.Label(frame1p,text='bin Q',width=6)
    lbl03_p.grid(row=0, column=5,sticky="NSEW")
    txt03_p = ttk.Entry(frame1p,width=6)
    txt03_p.grid(row=1, column=5,sticky="NSEW")
    #txt03_p.insert(0,'0.05')

    """
    # 大きさをそろえるためのダミーの入力欄
    lblp_d = tk.Label(frame1p,text='     ',width=6)
    lblp_d.grid(row=1, column=6,sticky="NSEW")
    lblp_d = tk.Label(frame1p,text='     ',width=6)
    lblp_d.grid(row=1, column=7,sticky="NSEW")
    lblp_d = tk.Label(frame1p,text='     ',width=6)
    lblp_d.grid(row=1, column=8,sticky="NSEW")
    """

    # 空のプログレスバーの表示
    state['pb3'] = ttk.Progressbar(frame1p,orient='horizontal',mode='determinate')
    state['pb3'].grid(row=2, column=6, columnspan=3,sticky="NSEW")



    # hwに関するoptionボタン
    # チェック有無変数
    hwp_nan = tk.IntVar()
    # value=0のラジオボタンにチェックを入れる
    hwp_nan.set(0)

    # toleranceの自動設定
    def update_plabels():
        if hwp_nan.get():
            fgt_lbl1.config(text="δℏω")
            bgt_lbl1.config(text="δℏω")
        else:
            fgt_lbl1.config(text="±δℏω")
            bgt_lbl1.config(text="±Δℏω")

    # チェックボタンの状態を保持する変数
    hwp_nan = tk.BooleanVar()

    hwp_nan_op = tk.Checkbutton(frame1p, variable=hwp_nan, text='ℏω cell',command=update_plabels)
    hwp_nan_op.grid(row=2, column=0, columnspan=2,sticky="")

    def toggle_entry_hwpcell():
        if hwp_nan.get()==0:
            txt04_p.config(state=tk.DISABLED) # min hw 
            txt05_p.config(state=tk.DISABLED) # max hw
            txt06_p.config(state=tk.DISABLED) # bin hw
            #fgt_txt1.config(state=tk.NORMAL) # tolerance ±δhw (FG)
            #bgt_txt1.config(state=tk.NORMAL) # tolerance ±δhw (BG)
            # チェックボックスの有無で意味が変わるので値を削除
            fgt_txt1.delete(0,tk.END)
            bgt_txt1.delete(0,tk.END)
        elif  hwp_nan.get()==1:#ユーザーがhw cellを指定したい場合
            txt04_p.config(state=tk.NORMAL) # min hw 
            txt05_p.config(state=tk.NORMAL) # max hw
            txt06_p.config(state=tk.NORMAL) # bin hw
            #fgt_txt1.config(state=tk.DISABLED) # tolerance ±δhw (FG)
            #bgt_txt1.config(state=tk.DISABLED) # tolerance ±δhw (BG)pow_data_box
            # チェックボックスの有無で意味が変わるので値を削除
            fgt_txt1.delete(0,tk.END)
            bgt_txt1.delete(0,tk.END)

    # プログラム開始時に一度だけtoggle_entryを呼び出す
    toggle_entry_hwpcell()

    # Radiobutton選択状態の変更時にtoggle_entry関数を呼び出す
    hwp_nan.trace('w', lambda *args: toggle_entry_hwpcell())

    # 自動でボックスのサイズを決めてくれるボタン
    button1_p_0 = ttk.Button(frame1p,text="auto bin",command=p_set_range,width=12)
    button1_p_0.grid(row=2, column=2, columnspan=2,sticky="NSEW")

    # 指定した範囲とbinサイズの箱にデータを詰めるボタン
    button1_p = ttk.Button(frame1p,text="re-bin",command=pow_data_box,width=12)
    button1_p.grid(row=2, column=4, columnspan=2,sticky="NSEW")

    # powderデータを見たり、1Dカットしたりするボタン周りのフレーム作成。
    frame2p = ttk.Labelframe(tab_02, text= "Visualization")
    frame2p.grid(row = 1, column = 0,sticky="NSEW")
    #frame2p.grid_propagate(True)

    # Notebookウィジェットの作成
    notebookp = ttk.Notebook(frame2p,style="example.TNotebook")

    # タブの作成
    tab_2dp = tk.Frame(notebookp)
    tab_1dp = tk.Frame(notebookp)
    tab_ptas = tk.Frame(notebookp)

    # notebookにタブを追加
    notebookp.add(tab_2dp, text="2D view")# 2D mapの表示
    notebookp.add(tab_1dp, text="1D view")# 1D mapの表示
    notebookp.add(tab_ptas, text="TAS mode")# TAS modeの表示

    tab_2dp.columnconfigure(0, weight=1)
    tab_2dp.rowconfigure(0, weight=1)

    tab_1dp.columnconfigure(0, weight=1)
    tab_1dp.columnconfigure(1, weight=1)
    tab_1dp.columnconfigure(2, weight=1)
    tab_1dp.columnconfigure(3, weight=1)
    tab_1dp.rowconfigure(0, weight=1)
    tab_1dp.rowconfigure(1, weight=1)
    tab_1dp.rowconfigure(2, weight=1)
    tab_1dp.rowconfigure(3, weight=1)

    tab_ptas.columnconfigure(0, weight=1)
    tab_ptas.columnconfigure(1, weight=1)
    tab_ptas.columnconfigure(2, weight=1)
    tab_ptas.columnconfigure(3, weight=1)
    tab_ptas.rowconfigure(0, weight=1)
    tab_ptas.rowconfigure(1, weight=1)
    tab_ptas.rowconfigure(2, weight=1)
    tab_ptas.rowconfigure(3, weight=1)

    # ウィジェットの配置
    notebookp.pack(expand=True, fill='both')

    ################################################
    # グラフオプションの定義

    # graph opetionを表示するボタン周りのフレーム作成。
    frame3p = ttk.Labelframe(tab_02, text= "Option")
    frame3p.grid(row = 0, column = 2, sticky="NSEW")
    #frame3p.grid_propagate(True)

    frame3p.columnconfigure(0, weight=1)
    frame3p.rowconfigure(0, weight=1)
    frame3p.rowconfigure(1, weight=1)
    frame3p.rowconfigure(2, weight=1)

    # チェック有無変数
    axistypep = tk.IntVar()
    # value=0のラジオボタンにチェックを入れる
    axistypep.set(0)

    # ラジオボタン作成
    #rdolbl = tk.Label(frameGL, text='axis type',width=7)
    #rdolbl.grid(row=0,column=6,columnspan=2)

    # powder option
    #at=axistype.get()で線形スケールかログスケールを選択
    rdo_at1p = tk.Radiobutton(frame3p, value=0, variable=axistypep, text='linear')#もともとframeGL
    rdo_at1p.grid(row=0,column=0,sticky="")

    rdo_at2p = tk.Radiobutton(frame3p, value=1, variable=axistypep, text='log')#もともとframeGL
    rdo_at2p.grid(row=1,column=0,sticky="")

    # チェック有無変数
    gridtypep = tk.IntVar()
    # value=0のラジオボタンにチェックを入れる
    gridtypep.set(1)

    #gt=gridtype.get()でグリッドをonかoffかを選択
    # チェック有無変数
    gridtypep = tk.IntVar()
    # value=0のラジオボタンにチェックを入れる
    gridtypep.set(1)

    rdo_gtp = tk.Checkbutton(frame3p, variable=gridtypep, text='grid')
    rdo_gtp.grid(row=2, column=0,sticky="")

    ################################################
    # graph scaleの定義

    # graph scaleを表示するボタン周りのフレーム作成。
    frameGSp = ttk.Labelframe(tab_02, text= "Graph Scale")
    frameGSp.grid(row = 1, column = 1,columnspan=2,sticky="NSEW")
    #frameGSp.grid_propagate(True)

    frameGSp.columnconfigure(0, weight=1)
    frameGSp.columnconfigure(1, weight=1)
    frameGSp.columnconfigure(2, weight=1)
    frameGSp.rowconfigure(0, weight=1)
    frameGSp.rowconfigure(1, weight=1)
    frameGSp.rowconfigure(2, weight=1)
    frameGSp.rowconfigure(3, weight=1)
    frameGSp.rowconfigure(4, weight=1)
    frameGSp.rowconfigure(5, weight=1)

    graph_scale_lbl0 = tk.Label(frameGSp,text='min',width=6)
    graph_scale_lbl0.grid(row=1, column=1,sticky="NSEW")
    graph_scale_lbl1 = tk.Label(frameGSp,text='max',width=6)
    graph_scale_lbl1.grid(row=1, column=2,sticky="NSEW")

    scale_p_Imin_lbl = tk.Label(frameGSp,text='Intensity',width=6)
    scale_p_Imin_lbl.grid(row=2, column=0,sticky="NSEW")
    scale_p_Imin_txt = ttk.Entry(frameGSp,width=6)
    scale_p_Imin_txt.grid(row=2, column=1,sticky="NSEW")
    scale_p_Imax_txt = ttk.Entry(frameGSp,width=6)
    scale_p_Imax_txt.grid(row=2, column=2,sticky="NSEW")

    scale_p_Emin_lbl = tk.Label(frameGSp,text='ℏω',width=6)
    scale_p_Emin_lbl.grid(row=3, column=0,sticky="NSEW")
    scale_p_Emin_txt = ttk.Entry(frameGSp,width=6)
    scale_p_Emin_txt.grid(row=3, column=1,sticky="NSEW")
    scale_p_Emax_txt = ttk.Entry(frameGSp,width=6)
    scale_p_Emax_txt.grid(row=3, column=2,sticky="NSEW")

    scale_p_Qmin_lbl = tk.Label(frameGSp,text='Q',width=6)
    scale_p_Qmin_lbl.grid(row=4, column=0,sticky="NSEW")
    scale_p_Qmin_txt = ttk.Entry(frameGSp,width=6)
    scale_p_Qmin_txt.grid(row=4, column=1,sticky="NSEW")
    scale_p_Qmax_txt = ttk.Entry(frameGSp,width=6)
    scale_p_Qmax_txt.grid(row=4, column=2,sticky="NSEW")


    gsp_clear = ttk.Button(frameGSp,text="clear",command=gsp_clear,width=6)
    gsp_clear.grid(row=5, column=0, columnspan=3, sticky="NSEW")


    gsp_auto = ttk.Button(frameGSp,text="auto scale",command=gsp_auto)
    gsp_auto.grid(row=0, column=0, columnspan=3,sticky="NSEW")

    ################################################
    # 2d view

    # powderデータを表示するボタンの定義

    # powderのmapを表示するボタン
    button2_p = ttk.Button(tab_2dp,text="Q vs ℏω",command=show_powderEmap,width=12)
    button2_p.grid(row=0, column=0, sticky="NSEW")

    ####################################################
    # 1D view

    # 1次元カット用の入力欄

    # E範囲指定
    lbl13_p = tk.Label(tab_1dp,text='ℏω',width=6)
    lbl13_p.grid(row=0, column=0,sticky="NSEW")
    lbl14_p = tk.Label(tab_1dp,text='±ℏω',width=6)
    lbl14_p.grid(row=0, column=1,sticky="NSEW")

    txt13_p = ttk.Entry(tab_1dp,width=6)
    txt13_p.insert(0,'0')
    txt13_p.grid(row=1, column=0,sticky="NSEW")
    txt14_p = ttk.Entry(tab_1dp,width=6)
    txt14_p.insert(0,'0.1')
    txt14_p.grid(row=1, column=1,sticky="NSEW")

    # Q範囲指定
    lbl11_p = tk.Label(tab_1dp,text='Q',width=6)
    lbl11_p.grid(row=0, column=2,sticky="NSEW")
    lbl12_p = tk.Label(tab_1dp,text='±Q',width=6)
    lbl12_p.grid(row=0, column=3,sticky="NSEW")

    txt11_p = ttk.Entry(tab_1dp,width=6)
    txt11_p.insert(0,'1')
    txt11_p.grid(row=1, column=2,sticky="NSEW")
    txt12_p = ttk.Entry(tab_1dp,width=6)
    txt12_p.insert(0,'0.1')
    txt12_p.grid(row=1, column=3,sticky="NSEW")

    # エネルギー方向の1次元カット

    # powderの1次元カットを表示するボタン
    button3_p = ttk.Button(tab_1dp,text="ℏω vs I",command=show_1D_EvsI,width=12)
    button3_p.grid(row=2, column=2,columnspan=2,sticky="NSEW")

    # 追加の1Dカットを重ね書きする機能の定義

    # powderの1次元カットを追加表示するボタン
    button3_pa = ttk.Button(tab_1dp,text="add ℏω vs I",command=btn_click_1DPE,width=12)
    button3_pa.grid(row=3, column=2,columnspan=2,sticky="NSEW")

    # Q方向の1次元カット

    button4_p = ttk.Button(tab_1dp,text="Q vs I",command=show_1D_QvsI,width=12)
    button4_p.grid(row=2, column=0,columnspan=2,sticky="NSEW")


    button4_p2 = ttk.Button(tab_1dp,text="add Q vs I",command=btn_click_1DPQ,width=12)
    button4_p2.grid(row=3, column=0,columnspan=2,sticky="NSEW")

    ###############################################################################
    # TAS mode(単結晶と同じ。ただし。コンボボックスの値取得時に挙動がおかしくなるので変数を変えている。)
    # TASモードで測定した場合のデータ表示

    # 読み込めなかった時はデータ形式がおかしい。(例えば最終の行だけ列数が少ないとか)
    # データ表示ボタンが押された時の定義

    # Xコンボボックスのリスト
    xlist =['Pt','c2', 'a2', 'q' ,'h', 'k', 'l', 'e', 'T']

    # Yコンボボックスのリスト
    ylist =['D01','D02','D03','D04','D05','D06','D07','D08','D09','D10','D11','D12','D13','D14','D15','D16','D17','D18','D19','D20','D21','D22','D23','D24']

    # Xコンボボックスのラベル
    lbl4_1 = tk.Label(tab_ptas,text='x-axis',width=6)
    lbl4_1.grid(row=0, column=0,sticky="NSEW")

    # Xコンボボックスを設置
    cbp = ttk.Combobox(tab_ptas, values = xlist, width=6)
    cbp.grid(row=1, column=0,sticky="NSEW")

    #コンボボックスのリストの先頭を表示
    cbp.set(xlist[0])

    # Yコンボボックスのラベル
    lbl4_2 = tk.Label(tab_ptas,text='detector',width=6)
    lbl4_2.grid(row=0, column=1,sticky="NSEW")

    # Yコンボボックスを設置
    cb_dp = ttk.Combobox(tab_ptas, values = ylist, width=6)
    cb_dp.grid(row=1, column=1,sticky="NSEW")

    #コンボボックスのリストの先頭を表示
    cb_dp.set(ylist[11])

    #グラフを表示するボタンを設置
    v_btn = ttk.Button(tab_ptas, text='view data', command=xaxis_selectp, width=12)
    v_btn.grid(row=1, column=2,sticky="NSEW")

    # ダミーのラベル
    lbl4_dp1 = tk.Label(tab_ptas,text='',width=6)
    lbl4_dp1.grid(row=2, column=0,sticky="NSEW",pady=1)
    lbl4_dp2 = tk.Label(tab_ptas,text='',width=6)
    lbl4_dp2.grid(row=3, column=0,sticky="NSEW",pady=1)

    #追加でグラフを表示するボタンの定義
    def add_axis_select(): 
        # 図番号が存在するかどうかの確認
        if plt.fignum_exists(state['fig_tas'])==True:
            # データを読み込む
            #特定の行を読み込む
            with open(state['file_paths'][0],"r", encoding="utf-8") as f:
                line = f.readlines()
                data = line[31]
                data2 = data.split()
                if "Pt." in data2:
                    pass
                else:
                    data = line[32]
                    data2 = data.split()

            No_Pt=data2.index('Pt.')
            No_c2=data2.index('c2')
            No_a2=data2.index('a2')
            No_timeact=data2.index('time-act')
            #mcuがない場合は読み込まない。
            if data.find('mcu')!=-1:
                No_mcu=data2.index('mcu')
            else :
                pass
            No_e=data2.index('e')
            No_q=data2.index('q')
            No_h=data2.index('h')
            No_k=data2.index('k')
            No_l=data2.index('l')
            No_tsample=data2.index('tsample')
            No_D01=data2.index('D01')
            No_D02=data2.index('D02')
            No_D03=data2.index('D03')
            No_D04=data2.index('D04')
            No_D05=data2.index('D05')
            No_D06=data2.index('D06')
            No_D07=data2.index('D07')
            No_D08=data2.index('D08')
            No_D09=data2.index('D09')
            No_D10=data2.index('D10')
            No_D11=data2.index('D11')
            No_D12=data2.index('D12')
            No_D13=data2.index('D13')
            No_D14=data2.index('D14')
            No_D15=data2.index('D15')
            No_D16=data2.index('D16')
            No_D17=data2.index('D17')
            No_D18=data2.index('D18')
            No_D19=data2.index('D19')
            No_D20=data2.index('D20')
            No_D21=data2.index('D21')
            No_D22=data2.index('D22')
            No_D23=data2.index('D23')
            No_D24=data2.index('D24')
            """
            No_1l=data2.index('1l')
            No_1r=data2.index('1r')
            No_1t=data2.index('1t')
            No_1b=data2.index('1b')
            """

            #ファイルの数値を全て読み込む
            #tt = np.loadtxt(file_paths[0], usecols = 0, delimiter=" ")
            pt = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_Pt-1)
            c2 = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_c2-1)
            a2 = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_a2-1)
            #mcuがない場合は読み込まない。強制的にmcuが0となる。しかし、このモードではカウント値しか読み込まないため問題ない。
            if data.find('mcu')!=-1:
                mcu = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_mcu-1)
            else :
                #mcu = np.zeros((len(c2)))
                pass
            t_a = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_timeact-1)
            e = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_e-1)
            D01 = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_D01-1)
            D02 = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_D02-1)
            D03 = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_D03-1)
            D04 = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_D04-1)
            D05 = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_D05-1)
            D06 = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_D06-1)
            D07 = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_D07-1)
            D08 = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_D08-1)
            D09 = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_D09-1)
            D10 = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_D10-1)
            D11 = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_D11-1)
            D12 = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_D12-1)
            D13 = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_D13-1)
            D14 = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_D14-1)
            D15 = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_D15-1)
            D16 = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_D16-1)
            D17 = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_D17-1)
            D18 = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_D18-1)
            D19 = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_D19-1)
            D20 = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_D20-1)
            D21 = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_D21-1)
            D22 = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_D22-1)
            D23 = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_D23-1)
            D24 = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_D24-1)

            q = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_q-1)
            h = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_h-1)
            k = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_k-1)
            l = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_l-1)
            T = np.loadtxt(state['file_paths'][0], comments='#', usecols = No_tsample-1)
            """
            l1 = np.loadtxt(file_paths[0], comments='#', usecols = No_1l-1)
            r1 = np.loadtxt(file_paths[0], comments='#', usecols = No_1r-1)
            b1 = np.loadtxt(file_paths[0], comments='#', usecols = No_1b-1)
            t1 = np.loadtxt(file_paths[0], comments='#', usecols = No_1t-1)
            """

            # X軸の項目を1つの行列にする。
            xbox=np.vstack([pt,c2,a2,q,h,k,l,e,T])

            # selectされたindexを読み込む
            x_select = cbp.current()

            #Y軸の項目を1つの行列にする。
            ybox=np.vstack([D01,D02,D03,D04,D05,D06,D07,D08,D09,D10,D11,D12,D13,D14,D15,D16,D17,D18,D19,D20,D21,D22,D23,D24])

            # selectされたindexを読み込む
            y_select = cb_dp.current()

            xlim_min=np.nanmin(xbox[x_select,:])
            xlim_max=np.nanmax(xbox[x_select,:])

            ylim_min=0
            ylim_max=np.nanmax(ybox[y_select,:])

            # エラーバーのグラフを作成   
            fig10=plt.figure(state['fig_tas'])
            ax10 = fig10.gca()
            ax10.errorbar(xbox[x_select,:], ybox[y_select,:], yerr=ybox[y_select,:]**(1/2), capsize=10, label='Detector'+str(y_select+1))
            at=axistypep.get()
            if at==1:
                plt.yscale('log')
                if ylim_min==0:
                    ylim_min=np.nanmin(ybox[y_select,:])-np.nanmax(ybox[y_select,:])
            ax10.set_xlim(xlim_min,xlim_max) #x軸の範囲を指定
            ax10.set_ylim(ylim_min,ylim_max) #y軸の範囲を指定
            #plt.tick_params(labelsize=20)
            ax10.legend()
            plt.show()

    #追加でグラフを表示するボタンを設置
    v_btn = ttk.Button(tab_ptas, text='add data', command=add_axis_select,width=12)
    v_btn.grid(row=1, column=3,sticky="NSEW")

    result = dict(locals())
    result.pop('env', None)
    return result
