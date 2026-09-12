"""Dataset Information GUI section."""


def _configure_file_listbox(listbox, remove_callback, tk):
    listbox.configure(selectmode=tk.EXTENDED, exportselection=False)
    listbox.bind("<Delete>", remove_callback)
    listbox.bind("<BackSpace>", remove_callback)


def build_dataset_information(env):
    calibration = env['calibration']
    clear = env['clear']
    file_select = env['file_select']
    remove_selected = env['remove_selected']
    maskall = env['maskall']
    maskclear = env['maskclear']
    mergefile = env['mergefile']
    mergefile_sb = env['mergefile_sb']
    on_entry_change = env['on_entry_change']
    root = env['root']
    sbclear = env['sbclear']
    sbfile_select = env['sbfile_select']
    sbremove_selected = env['sbremove_selected']
    state = env['state']
    tk = env['tk']
    ttk = env['ttk']
    vclear = env['vclear']
    vfile_select = env['vfile_select']

    frame2 = ttk.Labelframe(root,text= "Dataset Information")
    frame2.grid(row=0,column=0,padx=5,sticky="NSEW")
    #frame2.grid_propagate(True)

    frame2.columnconfigure(0, weight=1)
    frame2.rowconfigure(0, weight=1)

    # テーマ
    style = ttk.Style()

    # タブの文字色を変えて見やすくする
    # Style.map (TNotebook.Tab)
    style.map(
        "example.TNotebook.Tab",
        foreground=[
            ('active', 'red'),
            ('disabled', 'black'),
            ('selected', 'blue'),
        ],
        background=[
            ('active', 'orange'),
            ('disabled', 'black'),
            ('selected', 'lightgreen'),
        ],
    )

    # Notebookウィジェットの作成
    notebook00 = ttk.Notebook(frame2,style="example.TNotebook")

    # タブの作成
    tab_001 = tk.Frame(notebook00)# データファイル選択
    tab_002 = tk.Frame(notebook00)# 検出器マスク
    tab_003 = tk.Frame(notebook00)# 基準点
    # notebookにタブを追加
    notebook00.add(tab_001, text="Data File(s)")# データファイル選択
    notebook00.add(tab_002, text="Detector Mask")# 検出器マスク
    notebook00.add(tab_003, text="Reference angle of A2 ")# 基準点変更

    # FGデータ処理フレーム
    frame2fg = ttk.Labelframe(tab_001,text= "ForeGround Data File(s)")
    frame2fg.grid(row=0, column=0,rowspan=3,sticky="NSEW")
    #frame2fg.grid_propagate(True)

    # グリッドの重みを設定
    tab_001.columnconfigure(0, weight=1)
    tab_001.columnconfigure(1, weight=1)
    tab_001.columnconfigure(2, weight=1)
    tab_001.rowconfigure(0, weight=2)
    tab_001.rowconfigure(1, weight=3)
    tab_001.rowconfigure(2, weight=2)
    tab_001.rowconfigure(3, weight=2)

    tab_002.columnconfigure(0, weight=1)
    tab_002.columnconfigure(1, weight=1)
    tab_002.columnconfigure(2, weight=1)
    tab_002.columnconfigure(3, weight=1)
    tab_002.columnconfigure(4, weight=1)
    tab_002.columnconfigure(5, weight=1)
    tab_002.columnconfigure(6, weight=1)
    tab_002.columnconfigure(7, weight=1)
    tab_002.columnconfigure(8, weight=1)
    tab_002.columnconfigure(9, weight=1)
    tab_002.rowconfigure(0, weight=1)
    tab_002.rowconfigure(1, weight=1)
    tab_002.rowconfigure(2, weight=1)
    tab_002.rowconfigure(3, weight=1)

    tab_003.columnconfigure(0, weight=1)
    tab_003.columnconfigure(1, weight=1)
    tab_003.columnconfigure(2, weight=1)
    tab_003.columnconfigure(3, weight=1)
    tab_003.columnconfigure(4, weight=1)
    tab_003.columnconfigure(5, weight=1)
    tab_003.rowconfigure(0, weight=1)
    tab_003.rowconfigure(1, weight=1)
    tab_003.rowconfigure(2, weight=1)
    tab_003.rowconfigure(3, weight=1)
    tab_003.rowconfigure(4, weight=1)

    frame2fg.columnconfigure(0, weight=1)
    frame2fg.columnconfigure(1, weight=1)
    frame2fg.columnconfigure(2, weight=1)
    frame2fg.columnconfigure(3, weight=1)
    frame2fg.rowconfigure(0, weight=0)
    frame2fg.rowconfigure(1, weight=0)
    frame2fg.rowconfigure(2, weight=1)
    frame2fg.rowconfigure(3, weight=0)

    # ウィジェットの配置
    notebook00.pack(expand=True, fill='both')

    # ダミーのリストボックス
    fglist=[]
    # 各種ウィジェットの作成
    Listbox = tk.Listbox(frame2fg,listvariable=fglist,width=35, height=9)
    Listbox.grid(row=2, column=0,columnspan=4,sticky="NSEW")
    _configure_file_listbox(Listbox, remove_selected, tk)
    # スクロールバーの作成
    scrollbar = ttk.Scrollbar(frame2fg, orient=tk.VERTICAL, command=Listbox.yview)
    scrollbar.grid(row=2, column=4, sticky=(tk.N, tk.S))
    # スクロールバーをListboxに反映
    Listbox["yscrollcommand"] = scrollbar.set

    sbxscrollbar = ttk.Scrollbar(frame2fg, orient=tk.HORIZONTAL, command=Listbox.xview)
    sbxscrollbar.grid(row=3, column=0,columnspan=4, sticky=(tk.W, tk.E))
    Listbox["xscrollcommand"] = sbxscrollbar.set

    state['file_paths']=[]

    #ファイル選択処理の定義。ファイル名のみを表示。

    #ボックス内をクリアしてリセットして再度検索可能にする

    #ファイルの入力欄のボタンの作成
    button2 = ttk.Button(frame2fg,text="select",command=file_select,width=6)
    button2.grid(row=0, column=0,columnspan=2,sticky="NSEW")

    button_remove = ttk.Button(
        frame2fg,
        text="Remove selected",
        command=remove_selected,
    )
    button_remove.grid(row=0, column=2, columnspan=2, sticky="NSEW")

    #ファイルのクリアのボタンの作成
    button3 = ttk.Button(frame2fg,text="clear",command=clear,width=6)
    button3.grid(row=1, column=2,columnspan=2,sticky="NSEW")

    # ファイルのマージ

    #マージファイルのクリアのボタンの作成
    button3_3 = ttk.Button(frame2fg,text="merge",command=mergefile,width=6)
    button3_3.grid(row=1, column=0,columnspan=2,sticky="NSEW")

    ########
    # toleranceの自動設定
    def update_labels():
        if hw_nan.get():
            fgt_lbl1.config(text="δℏω")
            bgt_lbl1.config(text="δℏω")
        else:
            fgt_lbl1.config(text="±δℏω")
            bgt_lbl1.config(text="±Δℏω")

    # チェックボタンの状態を保持する変数
    hw_nan = tk.BooleanVar()

    # UVラベルの自動設定

    # StringVarを作成
    entry_u_var = tk.StringVar()
    entry_v_var = tk.StringVar()

    minU_label = tk.StringVar()
    maxU_label = tk.StringVar()
    binU_label = tk.StringVar()
    minV_label = tk.StringVar()
    maxV_label = tk.StringVar()
    binV_label = tk.StringVar()

    constE_buttom = tk.StringVar()
    constV_buttom = tk.StringVar()
    constU_buttom = tk.StringVar()
    scatter3d_buttom = tk.StringVar()

    initialU_label = tk.StringVar()
    initialV_label = tk.StringVar()

    vr_V_label = tk.StringVar()
    vr_U_label = tk.StringVar()

    IvsU_buttom = tk.StringVar()
    addIvsU_buttom = tk.StringVar()
    IvsV_buttom = tk.StringVar()
    addIvsV_buttom = tk.StringVar()

    U_lavel = tk.StringVar()
    V_lavel = tk.StringVar()
    pmU_lavel = tk.StringVar()
    pmV_lavel = tk.StringVar()

    calc_constU_buttom = tk.StringVar()
    calc_constV_buttom = tk.StringVar()

    calc_add_constU_buttom = tk.StringVar()
    calc_add_constV_buttom = tk.StringVar()

    deltaU = tk.StringVar()
    deltaV = tk.StringVar()

    # 変更例
    # label = tk.Label(root, textvariable=constE_buttom)

    ########
    # Calibrationデータ処理フレーム
    frame2cb = ttk.Labelframe(tab_001,text= "Calibration Data File")
    frame2cb.grid(row=0, column=2,sticky="NSEW")
    #frame2cb.grid_propagate(True)

    frame2cb.columnconfigure(0, weight=1)
    frame2cb.columnconfigure(1, weight=1)
    frame2cb.columnconfigure(2, weight=1)
    frame2cb.rowconfigure(0, weight=1)
    frame2cb.rowconfigure(1, weight=1)

    #ダミーのリストボックスを表示
    vlist=[]
    # 各種ウィジェットの作成
    vListbox = tk.Listbox(frame2cb,listvariable=vlist,width=35, height=1)

    # 各種ウィジェットの設置
    vListbox.grid(row=1, column=0,sticky="NSEW", columnspan=3)

    #バナジウムコレクション。ファイル名のみを表示。

    #ボックス内をクリアしてリセットして再度検索可能にする

    #ファイルの入力欄のボタンの作成
    button2_2 = ttk.Button(frame2cb,text="select",command=vfile_select)
    button2_2.grid(row=0, column=0,sticky="NSEW")

    #ファイルのクリアのボタンの作成
    button3_2 = ttk.Button(frame2cb,text="clear",command=vclear)
    button3_2.grid(row=0, column=2,sticky="NSEW")

    #キャリブレーションの定義。ファイルはenergyscan。ピークセンターとピーク強度のみが必要

    #キャリブレーションのボタンの作成
    button3_4 = ttk.Button(frame2cb,text="fit",command=calibration)
    button3_4.grid(row=0, column=1,sticky="NSEW")

    # 表示するデータの形式を選択
    frame2a = ttk.Labelframe(tab_001,text= "Intensity Type")
    frame2a.grid(row=1, column=2,sticky="NSEW")
    #frame2a.grid_propagate(True)

    frame2a.columnconfigure(0, weight=1)
    frame2a.columnconfigure(1, weight=1)
    frame2a.columnconfigure(2, weight=1)
    frame2a.columnconfigure(3, weight=1)
    frame2a.rowconfigure(0, weight=1)
    frame2a.rowconfigure(1, weight=1)
    frame2a.rowconfigure(2, weight=1)

    # チェック有無変数
    CSX = tk.IntVar()
    # value=0のラジオボタンにチェックを入れる
    CSX.set(1)

    # ラジオボタン作成
    # TASの場合、出てくるデータはS(q,w)であるのでクロスセクションはいらない
    #rdo_csx1 = tk.Radiobutton(frame2a, value=0, variable=CSX, text='σ')
    #rdo_csx1.grid(row=0,column=0, sticky="w")

    rdo_csx2 = tk.Radiobutton(frame2a, value=1, variable=CSX, text='S(q,ω)')
    rdo_csx2.grid(row=0,column=0,sticky="")

    # 係数を入力する欄
    sb_lbl1 = tk.Label(frame2a,text='factor =')
    sb_lbl1.grid(row=0, column=1,sticky="NSEW")
    sb_txt1 = ttk.Entry(frame2a,width=5)
    sb_txt1.grid(row=0, column=2,sticky="NSEW")
    sb_txt1.insert(0,'1')

    rdo_csx3 = tk.Radiobutton(frame2a, value=2, variable=CSX, text='χ(q,ω)')
    rdo_csx3.grid(row=1,column=0,sticky="", rowspan=2)

    # 係数を入力する欄
    sb_lbl2_1 = tk.Label(frame2a,text='T_fg =')
    sb_lbl2_1.grid(row=1, column=1,sticky="NSEW")
    sb_txt2 = ttk.Entry(frame2a,width=5)
    sb_txt2.grid(row=1, column=2,sticky="NSEW")
    sb_txt2.insert(0,'1')
    sb_lbl2_2 = tk.Label(frame2a,text='K')
    sb_lbl2_2.grid(row=1, column=3,sticky="NSEW")

    sb_lbl3 = tk.Label(frame2a,text='T_bg =')
    sb_lbl3.grid(row=2, column=1,sticky="NSEW")
    sb_txt3 = ttk.Entry(frame2a,width=5)
    sb_txt3.grid(row=2, column=2,sticky="NSEW")
    sb_txt3.insert(0,'300')
    sb_lbl3_2 = tk.Label(frame2a,text='K')
    sb_lbl3_2.grid(row=2, column=3,sticky="NSEW")

    def factor_toggle_entries_state():
        if CSX.get() == 1:  # S(q,w)が選択されている場合
            sb_txt1.config(state=tk.NORMAL)  # sb_txt1を有効にする
            sb_txt2.config(state=tk.DISABLED)  # sb_txt2を無効にする
            sb_txt3.config(state=tk.DISABLED)  # sb_txt3を無効にする
        elif CSX.get() == 2:  # X(q,w)が選択されている場合
            sb_txt1.config(state=tk.DISABLED)  # sb_txt1を有効にする
            sb_txt2.config(state=tk.NORMAL)  # sb_txt2を有効にする
            sb_txt3.config(state=tk.NORMAL)  # sb_txt3を有効にする

    # プログラム開始時に一度だけtoggle_entries_stateを呼び出す
    factor_toggle_entries_state()

    # Radiobutton選択状態の変更時にtoggle_entries_state関数を呼び出す
    CSX.trace('w', lambda *args: factor_toggle_entries_state())

    ###############################

    # backgroundデータを選択する。
    # FGデータ処理フレーム
    frame2bg = ttk.Labelframe(tab_001,text= "BackGround Data File(s)")
    frame2bg.grid(row=0, column=1,rowspan=3,sticky="NSEW")
    #frame2bg.grid_propagate(True)

    frame2bg.columnconfigure(0, weight=1)
    frame2bg.columnconfigure(1, weight=1)
    frame2bg.columnconfigure(2, weight=1)
    frame2bg.columnconfigure(3, weight=1)
    frame2bg.rowconfigure(0, weight=0)
    frame2bg.rowconfigure(1, weight=0)
    frame2bg.rowconfigure(2, weight=1)
    frame2bg.rowconfigure(3, weight=0)

    #ダミーのリストボックス
    sblist=[]
    # 各種ウィジェットの作成
    sbListbox = tk.Listbox(frame2bg,listvariable=sblist,width=35,height=9)
    sbListbox.grid(row=2, column=0,columnspan=4,sticky="NSEW")
    _configure_file_listbox(sbListbox, sbremove_selected, tk)
    # スクロールバーの作成
    scrollbar = ttk.Scrollbar(frame2bg, orient=tk.VERTICAL, command=sbListbox.yview)
    scrollbar.grid(row=2, column=4, sticky=(tk.N, tk.S))
    # スクロールバーをListboxに反映
    sbListbox["yscrollcommand"] = scrollbar.set

    sbxscrollbar = ttk.Scrollbar(frame2bg, orient=tk.HORIZONTAL, command=sbListbox.xview)
    sbxscrollbar.grid(row=3, column=0,columnspan=4, sticky=(tk.W, tk.E))
    sbListbox["xscrollcommand"] = sbxscrollbar.set

    state['sbfile_paths']=[]
    #ファイル選択処理の定義。ファイル名のみを表示。

    #ボックス内をクリアしてリセットして再度検索可能にする

    #ファイルの入力欄のボタンの作成
    button1_sb = ttk.Button(frame2bg,text="select",command=sbfile_select,width=6)
    button1_sb.grid(row=0, column=0,columnspan=2,sticky="NSEW")

    button_remove_sb = ttk.Button(
        frame2bg,
        text="Remove selected",
        command=sbremove_selected,
    )
    button_remove_sb.grid(row=0, column=2, columnspan=2, sticky="NSEW")

    #ファイルのクリアのボタンの作成
    button2_sb = ttk.Button(frame2bg,text="clear",command=sbclear,width=6)
    button2_sb.grid(row=1, column=2,columnspan=2,sticky="NSEW")

    # ファイルのマージ

    #マージファイルのクリアのボタンの作成
    button3_sb = ttk.Button(frame2bg,text="merge",command=mergefile_sb,width=6)
    button3_sb.grid(row=1, column=0,columnspan=2,sticky="NSEW")
    ###############################

    # data toleranceフレーム
    frame2fg0 = ttk.Labelframe(tab_001,text= "Tolerance")
    frame2fg0.grid(row=3, column=0,columnspan=3,sticky="NSEW")
    #frame2fg0.grid_propagate(True)

    frame2fg0.columnconfigure(0, weight=1)
    frame2fg0.columnconfigure(1, weight=1)
    frame2fg0.columnconfigure(2, weight=1)
    frame2fg0.columnconfigure(3, weight=1)
    frame2fg0.columnconfigure(4, weight=1)
    frame2fg0.columnconfigure(5, weight=1)
    frame2fg0.columnconfigure(6, weight=1)
    frame2fg0.columnconfigure(7, weight=1)
    frame2fg0.columnconfigure(8, weight=1)
    frame2fg0.columnconfigure(9, weight=1)
    frame2fg0.columnconfigure(10, weight=1)
    frame2fg0.columnconfigure(11, weight=1)
    frame2fg0.columnconfigure(12, weight=1)
    frame2fg0.rowconfigure(0, weight=1)
    frame2fg0.rowconfigure(1, weight=1)

    # tolerance paramter
    fgt_lbl0 = tk.Label(frame2fg0,text='fg : ')
    fgt_lbl0.grid(row=0, column=0,sticky="NSEW")

    fgt_lbl1 = tk.Label(frame2fg0,text='±δℏω',width=5)
    fgt_lbl1.grid(row=0, column=1,sticky="NSEW")
    fgt_txt1 = ttk.Entry(frame2fg0,width=6)
    fgt_txt1.grid(row=0, column=2,sticky="NSEW")

    fgt_lbl2 = tk.Label(frame2fg0,width=3,textvariable=deltaU)
    fgt_lbl2.grid(row=0, column=7,sticky="NSEW")
    fgt_txt2 = ttk.Entry(frame2fg0,width=6)
    fgt_txt2.grid(row=0, column=8,sticky="NSEW")

    fgt_lbl3 = tk.Label(frame2fg0,width=3,textvariable=deltaV)
    fgt_lbl3.grid(row=0, column=9,sticky="NSEW")
    fgt_txt3 = ttk.Entry(frame2fg0,width=6)
    fgt_txt3.grid(row=0, column=10,sticky="NSEW")

    # powder
    fgt_lbl4 = tk.Label(frame2fg0,text='δQ',width=3)
    fgt_lbl4.grid(row=0, column=11,sticky="NSEW")
    fgt_txt4 = ttk.Entry(frame2fg0,width=6)
    fgt_txt4.grid(row=0, column=12,sticky="NSEW")

    # background
    bgt_lbl0 = tk.Label(frame2fg0,text='bg : ')
    bgt_lbl0.grid(row=1, column=0,sticky="NSEW")

    bgt_lbl1 = tk.Label(frame2fg0,text='±Δℏω',width=5)
    bgt_lbl1.grid(row=1, column=1,sticky="NSEW")
    bgt_txt1 = ttk.Entry(frame2fg0,width=6)
    bgt_txt1.grid(row=1, column=2,sticky="NSEW")

    bgt_lbl4 = tk.Label(frame2fg0,text='±δA2',width=4)
    bgt_lbl4.grid(row=1, column=3,sticky="NSEW")
    bgt_txt4 = ttk.Entry(frame2fg0,width=6)
    bgt_txt4.grid(row=1, column=4,sticky="NSEW")

    bgt_lbl5 = tk.Label(frame2fg0,text='±δC2',width=4)
    bgt_lbl5.grid(row=1, column=5,sticky="NSEW")
    bgt_txt5 = ttk.Entry(frame2fg0,width=6)
    bgt_txt5.grid(row=1, column=6,sticky="NSEW")

    bgt_lbl2 = tk.Label(frame2fg0,width=3,textvariable=deltaU)
    bgt_lbl2.grid(row=1, column=7,sticky="NSEW")
    bgt_txt2 = ttk.Entry(frame2fg0,width=6)
    bgt_txt2.grid(row=1, column=8,sticky="NSEW")

    bgt_lbl3 = tk.Label(frame2fg0,width=3,textvariable=deltaV)
    bgt_lbl3.grid(row=1, column=9,sticky="NSEW")
    bgt_txt3 = ttk.Entry(frame2fg0,width=6)
    bgt_txt3.grid(row=1, column=10,sticky="NSEW")

    # powder
    bgt_lbl6 = tk.Label(frame2fg0,text='δQ',width=3)
    bgt_lbl6.grid(row=1, column=11,sticky="NSEW")
    bgt_txt6 = ttk.Entry(frame2fg0,width=6)
    bgt_txt6.grid(row=1, column=12,sticky="NSEW")

    # BGデータ処理方法フレーム
    frame2bgm = ttk.Labelframe(tab_001,text= "Subtraction Method")
    frame2bgm.grid(row=2, column=2,sticky="NSEW")
    #frame2fg.grid_propagate(True)

    frame2bgm.columnconfigure(0, weight=1)
    frame2bgm.columnconfigure(1, weight=1)
    frame2bgm.rowconfigure(0, weight=1)
    frame2bgm.rowconfigure(1, weight=1)

    # チェック有無変数
    bg_type = tk.IntVar()
    # value=0のラジオボタンにチェックを入れる
    bg_type.set(0)

    # bgm=bg_type.get()でdetector by detector=0 もしくは pixel by pixel=1を選択
    rdo_bg1 = tk.Radiobutton(frame2bgm, value=0, variable=bg_type, text='detector')#もともとframeGL
    rdo_bg1.grid(row=0,column=0,sticky="")

    rdo_bg2 = tk.Radiobutton(frame2bgm, value=1, variable=bg_type, text='pixel')#もともとframeGL
    rdo_bg2.grid(row=1,column=0,sticky="")

    # チェック有無変数
    sbtype1 = tk.IntVar()
    # value=0にチェックを入れる
    sbtype1.set(1)

    sb_nearest = tk.Checkbutton(frame2bgm, variable=sbtype1, text='nearest')
    sb_nearest.grid(row=0, column=1,sticky="")

    def toggle_entry():
        if sbtype1.get()==1:
            bgt_txt4.config(state=tk.DISABLED) # dlta A2
            bgt_txt5.config(state=tk.DISABLED) # dlta C2
        elif  sbtype1.get()==0:
            bgt_txt4.config(state=tk.NORMAL) # dlta A2
            bgt_txt5.config(state=tk.NORMAL) # dlta C2

    # プログラム開始時に一度だけtoggle_entryを呼び出す
    toggle_entry()

    # Radiobutton選択状態の変更時にtoggle_entry関数を呼び出す
    sbtype1.trace('w', lambda *args: toggle_entry())

    # チェック有無変数
    sbtype2 = tk.IntVar()
    # value=0のラジオボタンにチェックを入れる
    sbtype2.set(1)

    sb_nan = tk.Checkbutton(frame2bgm, variable=sbtype2, text='trans NaN')
    sb_nan.grid(row=1, column=1,sticky="")

    def toggle_checkbox():
        if bg_type.get() == 0:# detector
            sb_nearest.config(state=tk.NORMAL)
            sb_nan.config(state=tk.NORMAL)
        elif bg_type.get() == 1: # pixel
            sb_nearest.config(state=tk.DISABLED)
            sb_nan.config(state=tk.NORMAL)  

    # プログラム開始時に一度だけtoggle_entries_stateを呼び出す
    toggle_checkbox()

    # Radiobutton選択状態の変更時にtoggle_entries_state関数を呼び出す
    bg_type.trace('w', lambda *args: toggle_checkbox())

    def toggle_entries_state():
        if bg_type.get() == 0:  # rdo_bg1が選択(detector-detector)されている場合
            #bgt_txt1.config(state=tk.NORMAL)  # dE # 有効にする
            #bgt_txt2.config(state=tk.DISABLED) # dU # 有効にする
            #bgt_txt3.config(state=tk.DISABLED) # dV
            #bgt_txt4.config(state=tk.NORMAL) # dlta A2
            #bgt_txt5.config(state=tk.NORMAL) # dlta C2
            #bgt_txt6.config(state=tk.DISABLED) # dQ
            #checkbox.config(state="disabled")
            if sbtype1.get()==1:
                bgt_txt4.config(state=tk.DISABLED) # dlta A2
                bgt_txt5.config(state=tk.DISABLED) # dlta C2
            elif  sbtype1.get()==0:
                bgt_txt4.config(state=tk.NORMAL) # dlta A2
                bgt_txt5.config(state=tk.NORMAL) # dlta C2
        else:# rdo_bg2が選択(pixel-pixel)されている場合
            #bgt_txt1.config(state=tk.DISABLED)
            #bgt_txt2.config(state=tk.NORMAL)
            #bgt_txt3.config(state=tk.NORMAL)
            bgt_txt4.config(state=tk.DISABLED)
            bgt_txt5.config(state=tk.DISABLED)
            #bgt_txt6.config(state=tk.NORMAL)
            #checkbox.config(state="normal")

    # プログラム開始時に一度だけtoggle_entries_stateを呼び出す
    toggle_entries_state()

    # Radiobutton選択状態の変更時にtoggle_entries_state関数を呼び出す
    bg_type.trace('w', lambda *args: toggle_entries_state())

    #################################################################################
    # 検出器マスク機能

    # clearボタンの定義

    # allボタンの定義

    # 選択オプション
    options = ["D {}".format(i+1) for i in range(24)]

    # チェックボタンの変数を管理するリスト
    check_vars = []

    # チェックボタンを作成し、変数をリストに追加
    check_buttons = []
    for i, option in enumerate(options):
        var = tk.IntVar()
        check_vars.append(var)
        check_button = tk.Checkbutton(tab_002, text=option, variable=var)
        check_buttons.append(check_button)
        row_num, col_num = divmod(i, 10)
        check_button.grid(row=row_num, column=col_num, sticky="w")

    # allボタンを設置
    mask_all = ttk.Button(tab_002,text="select all",command=maskall)
    mask_all.grid(row=3, column=3, columnspan=2, sticky="NSEW")

    # clearボタンを設置
    mask_cle = ttk.Button(tab_002,text="clear all",command=maskclear)
    mask_cle.grid(row=3, column=5, columnspan=2, sticky="NSEW")

    #################################################################################
    # 基準点の変更
    # phiを計算して出力する関数
    def update_phi():
        sel = selected_detector.get()
        if sel.startswith("D"):
            idx = int(sel[1:]) - 1  # D01→0, D02→1 ...
            # shared variables are stored in state
            state['phi'] = -idx * 2
            entry_arbitral.configure(state="disabled")  # 無効化
        elif sel == "arbitral":
            try:
                state['phi'] = -float(entry_arbitral.get())-22
            except ValueError:
                state['phi'] = float("nan")
            entry_arbitral.configure(state="normal")    # 有効化
        else:
            state['phi'] = float("nan")

        #print(f"Selected: {sel}, phi = {phi}")

    # --- 変数（選択状態を保持する） ---
    selected_detector = tk.StringVar(value="D12")  # デフォルトを D12 に

    # --- D01〜D24 のラジオボタンを作成 ---
    frame_detectors = ttk.Frame(tab_003)
    frame_detectors.grid(sticky="NSEW")

    # --- D01〜D24 のラジオボタンを作成 ---
    for i in range(24):
        detector_label = f"D{i+1:02d}"
        rb = ttk.Radiobutton(
            tab_003,
            text=detector_label,
            value=detector_label,
            variable=selected_detector,
            command=update_phi
        )
        rb.grid(row=i//6, column=i%6, sticky="NSEW")

    # --- arbitral value のラジオボタンとエントリ（同じタブ上に直接配置） ---
    row_offset = 24 // 6   # 下の段に配置
    rb_arbitral = ttk.Radiobutton(
        tab_003,
        text="Arbitral value (diffrence from D12 (ex : D01->-22, D12->0, D24->+24)):",
        value="arbitral",
        variable=selected_detector,
        command=update_phi
    )
    rb_arbitral.grid(row=row_offset, column=0, columnspan=5, sticky="NSEW")

    entry_arbitral = ttk.Entry(tab_003,width=5)
    entry_arbitral.grid(row=row_offset, column=5, sticky="NSEW")

    # arbitral の Entry に変化があったら phi 更新

    entry_arbitral.bind("<KeyRelease>", on_entry_change)

    # --- 初期表示 ---
    update_phi()
    #################################################################################

    # 格子定数と初期位置の入力フレーム

    result = dict(locals())
    result.pop('env', None)
    return result
