"""Analysis Hub / Single Crystal tab."""

import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt

def _build_tas_data_section(tab_4, state, xaxis_select, axistype):
    #########################################################################
    # TAS modeで測定した場合のデータ表示

    # 読み込めなかった時はデータ形式がおかしい。(例えば最終の行だけ列数が少ないとか)
    # データ表示ボタンが押された時の定義

    #グラフを表示するボタンを設置
    v_btn = ttk.Button(tab_4, text='view data', command=xaxis_select,width=12)
    v_btn.grid(row=1, column=2,sticky="NSEW")

    # Xコンボボックスのリスト
    xlist =["Pt","c2", "a2", "q" ,"h", "k", "l", "e", "T"]

    # Yコンボボックスのリスト
    ylist =["D01","D02","D03","D04","D05","D06","D07","D08","D09","D10","D11","D12","D13","D14","D15","D16","D17","D18","D19","D20","D21","D22","D23","D24"]

    # Xコンボボックスのラベル
    lbl4_1 = tk.Label(tab_4,text='x-axis',width=6)
    lbl4_1.grid(row=0, column=0,sticky="NSEW")

    # ダミーのラベル
    lbl4_d1 = tk.Label(tab_4,text='',width=6)
    lbl4_d1.grid(row=2, column=0,sticky="NSEW",pady=1)
    lbl4_d2 = tk.Label(tab_4,text='',width=6)
    lbl4_d2.grid(row=3, column=0,sticky="NSEW",pady=1)

    # Xコンボボックスを設置
    cbs = ttk.Combobox(tab_4, values = xlist, width=6)
    cbs.grid(row=1, column=0,sticky="NSEW")

    #コンボボックスのリストの先頭を表示
    cbs.set(xlist[0])

    # Yコンボボックスのラベル
    lbl4_2 = tk.Label(tab_4,text='detector',width=6)
    lbl4_2.grid(row=0, column=1,sticky="NSEW")

    # Yコンボボックスを設置
    cb_ds = ttk.Combobox(tab_4, values = ylist, width=6)
    cb_ds.grid(row=1, column=1,sticky="NSEW")

    #コンボボックスのリストの先頭を表示
    cb_ds.set(ylist[11])

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
            x_select = cbs.current()

            #Y軸の項目を1つの行列にする。
            ybox=np.vstack([D01,D02,D03,D04,D05,D06,D07,D08,D09,D10,D11,D12,D13,D14,D15,D16,D17,D18,D19,D20,D21,D22,D23,D24])

            # selectされたindexを読み込む
            y_select = cb_ds.current()

            #xlim_min=np.nanmin(xbox[x_select,:])
            #xlim_max=np.nanmax(xbox[x_select,:])

            #ylim_min=0
            #ylim_max=np.nanmax(ybox[y_select,:])

            # エラーバーのグラフを作成   
            fig10=plt.figure(state['fig_tas'])
            ax10 = fig10.gca()
            ax10.errorbar(xbox[x_select,:], ybox[y_select,:], yerr=ybox[y_select,:]**(1/2), capsize=10, label='Detector'+str(y_select+1))
            at=axistype.get()
            if at==1:
                plt.yscale('log')
                #if ylim_min==0:
                #    ylim_min=np.nanmin(ybox[y_select,:])-np.nanmax(ybox[y_select,:])
            #ax10.set_xlim(xlim_min,xlim_max) #x軸の範囲を指定
            #ax10.set_ylim(ylim_min,ylim_max) #y軸の範囲を指定
            #plt.tick_params(labelsize=20)
            ax10.legend()
            plt.show()

    #追加でグラフを表示するボタンを設置
    v_btn = ttk.Button(tab_4, text='add data', command=add_axis_select,width=12)
    v_btn.grid(row=1, column=3,sticky="NSEW")


    return {
        "cbs": cbs,
        "cb_ds": cb_ds,
        "add_axis_select": add_axis_select,
    }


def build_single_crystal(env):
    IvsU_buttom = env['IvsU_buttom']
    IvsV_buttom = env['IvsV_buttom']
    U_lavel = env['U_lavel']
    V_lavel = env['V_lavel']
    addIvsU_buttom = env['addIvsU_buttom']
    addIvsV_buttom = env['addIvsV_buttom']
    add_advanced_1D_alongE = env['add_advanced_1D_alongE']
    add_advanced_1D_alongQ = env['add_advanced_1D_alongQ']
    advanced_1D_alongE = env['advanced_1D_alongE']
    advanced_1D_alongQ = env['advanced_1D_alongQ']
    advanced_2D_constE = env['advanced_2D_constE']
    advanced_2D_constQ = env['advanced_2D_constQ']
    bgt_txt1 = env['bgt_txt1']
    binU_label = env['binU_label']
    binV_label = env['binV_label']
    constE_1D_U = env['constE_1D_U']
    constE_1D_U2 = env['constE_1D_U2']
    constE_1D_V = env['constE_1D_V']
    constE_1D_V2 = env['constE_1D_V2']
    constE_buttom = env['constE_buttom']
    constEmap = env['constEmap']
    constQmap_1D = env['constQmap_1D']
    constQmap_1D2 = env['constQmap_1D2']
    constQmap_U = env['constQmap_U']
    constQmap_U2 = env['constQmap_U2']
    constQmap_V = env['constQmap_V']
    constQmap_V2 = env['constQmap_V2']
    constU_buttom = env['constU_buttom']
    constV_buttom = env['constV_buttom']
    data_box = env['data_box']
    disp3D = env['disp3D']
    fgt_txt1 = env['fgt_txt1']
    gs_auto = env['gs_auto']
    gs_auto2 = env['gs_auto2']
    gs_clear = env['gs_clear']
    gs_clear2 = env['gs_clear2']
    initialU_label = env['initialU_label']
    initialV_label = env['initialV_label']
    maxU_label = env['maxU_label']
    maxV_label = env['maxV_label']
    minU_label = env['minU_label']
    minV_label = env['minV_label']
    notebook1 = env['notebook1']
    pmU_lavel = env['pmU_lavel']
    pmV_lavel = env['pmV_lavel']
    range_auto_3D = env['range_auto_3D']
    scatter3d_buttom = env['scatter3d_buttom']
    scatter_2d_cE = env['scatter_2d_cE']
    scatter_2d_cU = env['scatter_2d_cU']
    scatter_2d_cV = env['scatter_2d_cV']
    set_range = env['set_range']
    show_3DconEmap = env['show_3DconEmap']
    state = env['state']
    switch_mode = env['switch_mode']
    tab_01 = env['tab_01']
    threshold_auto = env['threshold_auto']
    tk = env['tk']
    ttk = env['ttk']
    update_labels = env['update_labels']
    vr_U_label = env['vr_U_label']
    vr_V_label = env['vr_V_label']
    xaxis_select = env['xaxis_select']

    # ウィジェットの配置
    notebook1.pack(expand=True, fill='both')

    # sliceとscatterを切り替え

    # モード切替用ラジオボタン（row=0）
    mode_var = tk.StringVar(value="slice")
    tk.Radiobutton(tab_01, text="Slicing Mode", variable=mode_var, value="slice", command=switch_mode).grid(row=0, column=0, sticky="nsew")
    tk.Radiobutton(tab_01, text="Scattering Mode", variable=mode_var, value="scatter", command=switch_mode).grid(row=0, column=1, sticky="nsew")

    # Slicing UIを格納するサブフレーム（row=1にまとめて配置）
    slice_frame = tk.Frame(tab_01)
    slice_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

    slice_frame.columnconfigure(0, weight=1)
    slice_frame.columnconfigure(1, weight=1)
    slice_frame.columnconfigure(2, weight=1)
    slice_frame.rowconfigure(0, weight=1)
    slice_frame.rowconfigure(1, weight=1)
    slice_frame.rowconfigure(2, weight=1)

    # Scattering UIを格納するサブフレーム（row=1にまとめて配置）
    scatter_frame = tk.Frame(tab_01)
    scatter_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

    scatter_frame.columnconfigure(0, weight=3)
    scatter_frame.columnconfigure(1, weight=2)
    scatter_frame.columnconfigure(2, weight=2)
    scatter_frame.rowconfigure(0, weight=1)
    scatter_frame.rowconfigure(1, weight=1)

    # 最初の呼び出し
    # 初期表示
    slice_frame.tkraise()

    # データボックスを作成するボタン周りのフレーム作成。
    frame4 = ttk.Labelframe(slice_frame, text= "Data Construction")
    frame4.grid(row = 0, column = 0,columnspan=2,sticky="NSEW")
    #frame4.grid_propagate(True)

    frame4.columnconfigure(0, weight=1)
    frame4.columnconfigure(1, weight=1)
    frame4.columnconfigure(2, weight=1)
    frame4.columnconfigure(3, weight=1)
    frame4.columnconfigure(4, weight=1)
    frame4.columnconfigure(5, weight=1)
    frame4.columnconfigure(6, weight=1)
    frame4.columnconfigure(7, weight=1)
    frame4.columnconfigure(8, weight=1)
    frame4.rowconfigure(0, weight=1)
    frame4.rowconfigure(1, weight=1)
    frame4.rowconfigure(2, weight=1)

    # Q範囲とbin sizeの入力欄
    # 範囲に関しては自動で入るようにする
    lbl22 = tk.Label(frame4,text='min ℏω',width=6)
    lbl22.grid(row=0, column=0,sticky="NSEW")
    txt22 = ttk.Entry(frame4,width=6)
    txt22.grid(row=1, column=0,sticky="NSEW")

    lbl23 = tk.Label(frame4,text='max ℏω',width=6)
    lbl23.grid(row=0, column=1,sticky="NSEW")
    txt23 = ttk.Entry(frame4,width=6)
    txt23.grid(row=1, column=1,sticky="NSEW")

    lbl24 = tk.Label(frame4,text='bin ℏω',width=6)
    lbl24.grid(row=0, column=2,sticky="NSEW")
    txt24 = ttk.Entry(frame4,width=6)
    txt24.grid(row=1, column=2,sticky="NSEW")

    lbl16 = tk.Label(frame4,textvariable=minU_label,width=6)
    lbl16.grid(row=0, column=3,sticky="NSEW")
    txt16 = ttk.Entry(frame4,width=6)
    txt16.grid(row=1, column=3,sticky="NSEW")

    lbl17 = tk.Label(frame4,textvariable=maxU_label,width=6)
    lbl17.grid(row=0, column=4,sticky="NSEW")
    txt17 = ttk.Entry(frame4,width=6)
    txt17.grid(row=1, column=4,sticky="NSEW")

    lbl18 = tk.Label(frame4,textvariable=binU_label,width=6)
    lbl18.grid(row=0, column=5,sticky="NSEW")
    txt18 = ttk.Entry(frame4,width=6)
    #txt18.insert(0,'0.05')
    txt18.grid(row=1, column=5,sticky="NSEW")

    lbl19 = tk.Label(frame4,textvariable=minV_label,width=6)
    lbl19.grid(row=0, column=6,sticky="NSEW")
    txt19 = ttk.Entry(frame4,width=6)
    txt19.grid(row=1, column=6,sticky="NSEW")

    lbl20 = tk.Label(frame4,textvariable=maxV_label,width=6)
    lbl20.grid(row=0, column=7,sticky="NSEW")
    txt20 = ttk.Entry(frame4,width=6)
    txt20.grid(row=1, column=7,sticky="NSEW")

    lbl21 = tk.Label(frame4,textvariable=binV_label,width=6)
    lbl21.grid(row=0, column=8,sticky="NSEW")
    txt21 = ttk.Entry(frame4,width=6)
    #txt21.insert(0,'0.05')
    txt21.grid(row=1, column=8,sticky="NSEW")

    state['pb2'] = ttk.Progressbar(frame4,orient='horizontal',mode='determinate')
    state['pb2'].grid(row=2, column=6, columnspan=3,sticky="NSEW")


    # 自動でボックスのサイズを決めてくれるボタンの動作定義

    # hwに関するoptionボタン
    # チェック有無変数
    hw_nan = tk.IntVar()
    # value=0のラジオボタンにチェックを入れる
    hw_nan.set(0)

    hw_nan_op = tk.Checkbutton(frame4, variable=hw_nan, text='ℏω cell',command=update_labels)
    hw_nan_op.grid(row=2, column=0, columnspan=2,sticky="")

    def toggle_entry_hwcell():
        if hw_nan.get()==0:
            txt22.config(state=tk.DISABLED) # min hw 
            txt23.config(state=tk.DISABLED) # max hw
            txt24.config(state=tk.DISABLED) # bin hw
            #fgt_txt1.config(state=tk.NORMAL) # tolerance ±δhw (FG)
            #bgt_txt1.config(state=tk.NORMAL) # tolerance ±δhw (BG)
            # チェックボックスの有無で意味が変わるので値を削除
            fgt_txt1.delete(0,tk.END)
            bgt_txt1.delete(0,tk.END)
        elif  hw_nan.get()==1:#ユーザーがhw cellを指定したい場合
            txt22.config(state=tk.NORMAL) # min hw 
            txt23.config(state=tk.NORMAL) # max hw
            txt24.config(state=tk.NORMAL) # bin hw
            #fgt_txt1.config(state=tk.DISABLED) # tolerance ±δhw (FG)
            #bgt_txt1.config(state=tk.DISABLED) # tolerance ±δhw (BG)
            # チェックボックスの有無で意味が変わるので値を削除
            fgt_txt1.delete(0,tk.END)
            bgt_txt1.delete(0,tk.END)

    # プログラム開始時に一度だけtoggle_entryを呼び出す
    toggle_entry_hwcell()

    # Radiobutton選択状態の変更時にtoggle_entry関数を呼び出す
    hw_nan.trace('w', lambda *args: toggle_entry_hwcell())

    # 自動でボックスのサイズを決めてくれるボタン
    button7_0 = ttk.Button(frame4,text="auto bin",command=set_range,width=12)
    button7_0.grid(row=2, column=2, columnspan=2,sticky="NSEW")

    #指定した範囲とbinサイズの箱にデータを詰めるボタン
    button7 = ttk.Button(frame4,text="re-bin",command=data_box,width=12)
    button7.grid(row=2, column=4, columnspan=2,sticky="NSEW")

    ###########################################################################

    # graph opetionを表示するボタン周りのフレーム作成。
    frame6 = ttk.Labelframe(slice_frame, text= "Option")
    frame6.grid(row = 0, column = 2, sticky="NSEW")
    #frame6.grid_propagate(True)

    frame6.columnconfigure(0, weight=1)
    frame6.rowconfigure(0, weight=1)
    frame6.rowconfigure(1, weight=1)
    frame6.rowconfigure(2, weight=1)

    # チェック有無変数
    axistype = tk.IntVar()
    # value=0のラジオボタンにチェックを入れる
    axistype.set(0)

    # ラジオボタン作成
    #rdolbl = tk.Label(frameGL, text='axis type',width=7)
    #rdolbl.grid(row=0,column=6,columnspan=2)

    #at=axistype.get()で線形スケールかログスケールを選択
    rdo_at1 = tk.Radiobutton(frame6, value=0, variable=axistype, text='linear')#もともとframeGL
    rdo_at1.grid(row=0,column=0, sticky="")

    rdo_at2 = tk.Radiobutton(frame6, value=1, variable=axistype, text='log')#もともとframeGL
    rdo_at2.grid(row=1,column=0, sticky="")

    # チェック有無変数
    gridtype = tk.IntVar()
    # value=0のラジオボタンにチェックを入れる
    gridtype.set(1)

    chk_gt = tk.Checkbutton(frame6, variable=gridtype, text='grid')
    chk_gt.grid(row=2, column=0, sticky="")

    # 3D,2D,1Dを表示するボタン周りのフレーム作成。
    frame5 = ttk.Labelframe(slice_frame, text= "Visualization")
    frame5.grid(row = 1, column = 0,sticky="NSEW")
    #frame5.grid_propagate(True)

    # graph opetionを表示するボタン周りのフレーム作成。
    frameGSs = ttk.Labelframe(slice_frame, text= "Graph Scale")
    frameGSs.grid(row = 1, column = 1,columnspan=2,sticky="NSEW")
    #frameGSs.grid_propagate(True)

    frameGSs.columnconfigure(0, weight=1)
    frameGSs.columnconfigure(1, weight=1)
    frameGSs.columnconfigure(2, weight=1)
    frameGSs.rowconfigure(0, weight=1)
    frameGSs.rowconfigure(1, weight=1)
    frameGSs.rowconfigure(2, weight=1)
    frameGSs.rowconfigure(3, weight=1)
    frameGSs.rowconfigure(4, weight=1)
    frameGSs.rowconfigure(5, weight=1)
    frameGSs.rowconfigure(6, weight=1)

    # graph scale
    graph_scale_lbl0 = tk.Label(frameGSs,text='min',width=6)
    graph_scale_lbl0.grid(row=1, column=1,sticky="NSEW")
    graph_scale_lbl1 = tk.Label(frameGSs,text='max',width=6)
    graph_scale_lbl1.grid(row=1, column=2,sticky="NSEW")

    scale_s_Imin_lbl = tk.Label(frameGSs,text='Intensity',width=6)
    scale_s_Imin_lbl.grid(row=2, column=0,sticky="NSEW")
    scale_s_Imin_txt = ttk.Entry(frameGSs,width=6)
    scale_s_Imin_txt.grid(row=2, column=1,sticky="NSEW")
    scale_s_Imax_txt = ttk.Entry(frameGSs,width=6)
    scale_s_Imax_txt.grid(row=2, column=2,sticky="NSEW")

    scale_s_Emin_lbl = tk.Label(frameGSs,text='ℏω',width=6)
    scale_s_Emin_lbl.grid(row=3, column=0,sticky="NSEW")
    scale_s_Emin_txt = ttk.Entry(frameGSs,width=6)
    scale_s_Emin_txt.grid(row=3, column=1,sticky="NSEW")
    scale_s_Emax_txt = ttk.Entry(frameGSs,width=6)
    scale_s_Emax_txt.grid(row=3, column=2,sticky="NSEW")

    scale_s_Umin_lbl = tk.Label(frameGSs,width=6,textvariable=U_lavel)
    scale_s_Umin_lbl.grid(row=4, column=0,sticky="NSEW")
    scale_s_Umin_txt = ttk.Entry(frameGSs,width=6)
    scale_s_Umin_txt.grid(row=4, column=1,sticky="NSEW")
    scale_s_Umax_txt = ttk.Entry(frameGSs,width=6)
    scale_s_Umax_txt.grid(row=4, column=2,sticky="NSEW")

    scale_s_Vmin_lbl = tk.Label(frameGSs,width=6,textvariable=V_lavel)
    scale_s_Vmin_lbl.grid(row=5, column=0,sticky="NSEW")
    scale_s_Vmin_txt = ttk.Entry(frameGSs,width=6)
    scale_s_Vmin_txt.grid(row=5, column=1,sticky="NSEW")
    scale_s_Vmax_txt = ttk.Entry(frameGSs,width=6)
    scale_s_Vmax_txt.grid(row=5, column=2,sticky="NSEW")


    gs_clear = ttk.Button(frameGSs,text="clear",command=gs_clear,width=6)
    gs_clear.grid(row=6, column=0, columnspan=3, sticky="NSEW")


    gs_auto = ttk.Button(frameGSs,text="auto scale",command=gs_auto)
    gs_auto.grid(row=0, column=0, columnspan=3,sticky="NSEW")
    #################

    # Notebookウィジェットの作成
    notebook = ttk.Notebook(frame5,style="example.TNotebook")

    # タブの作成
    tab_3d = tk.Frame(notebook)
    tab_2d = tk.Frame(notebook)
    tab_1d = tk.Frame(notebook)
    # 斜め方向のスライス及び１次元カットを行うモード。ここではテストモードとして独立したタブを作成。
    tab_slice = tk.Frame(notebook)
    tab_4 = tk.Frame(notebook)

    # notebookにタブを追加
    notebook.add(tab_3d, text="3D view")# 3D mapの表示
    notebook.add(tab_2d, text="2D view")# 2D mapの表示
    notebook.add(tab_1d, text="1D view")# 1D cutの作成
    notebook.add(tab_slice, text="Advanced")# 斜め方向のスライス
    notebook.add(tab_4, text="TAS mode")# 各検出器のデータを見る。これだけtime-actに対応するため、個別に対応

    # ウィジェットの配置
    notebook.pack(expand=True, fill='both')

    tab_3d.columnconfigure(0, weight=1)
    tab_3d.columnconfigure(1, weight=1)
    tab_3d.columnconfigure(2, weight=1)
    tab_3d.rowconfigure(0, weight=1)
    tab_3d.rowconfigure(1, weight=1)
    tab_3d.rowconfigure(2, weight=1)
    tab_3d.rowconfigure(3, weight=1)

    tab_2d.columnconfigure(0, weight=1)
    tab_2d.columnconfigure(1, weight=1)
    tab_2d.columnconfigure(2, weight=1)
    tab_2d.columnconfigure(3, weight=1)
    tab_2d.columnconfigure(4, weight=1)
    tab_2d.columnconfigure(5, weight=1)
    tab_2d.rowconfigure(0, weight=1)
    tab_2d.rowconfigure(1, weight=1)
    tab_2d.rowconfigure(2, weight=1)
    tab_2d.rowconfigure(3, weight=1)

    tab_1d.columnconfigure(0, weight=1)
    tab_1d.columnconfigure(1, weight=1)
    tab_1d.columnconfigure(2, weight=1)
    tab_1d.columnconfigure(3, weight=1)
    tab_1d.columnconfigure(4, weight=1)
    tab_1d.columnconfigure(5, weight=1)
    tab_1d.rowconfigure(0, weight=1)
    tab_1d.rowconfigure(1, weight=1)
    tab_1d.rowconfigure(2, weight=1)
    tab_1d.rowconfigure(3, weight=1)

    tab_slice.columnconfigure(0, weight=1)
    tab_slice.columnconfigure(1, weight=1)
    tab_slice.columnconfigure(2, weight=1)
    tab_slice.columnconfigure(3, weight=1)
    tab_slice.columnconfigure(4, weight=1)
    tab_slice.columnconfigure(5, weight=1)
    tab_slice.columnconfigure(6, weight=1)
    tab_slice.rowconfigure(0, weight=1)
    tab_slice.rowconfigure(1, weight=1)
    tab_slice.rowconfigure(2, weight=1)
    tab_slice.rowconfigure(3, weight=1)

    tab_4.columnconfigure(0, weight=1)
    tab_4.columnconfigure(1, weight=1)
    tab_4.columnconfigure(2, weight=1)
    tab_4.columnconfigure(3, weight=1)
    tab_4.rowconfigure(0, weight=1)
    tab_4.rowconfigure(1, weight=1)
    tab_4.rowconfigure(2, weight=1)
    tab_4.rowconfigure(3, weight=1)
    #########################################################
    # advancedモードの内容

    lbl_ad01 = tk.Label(tab_slice,text='h',width=6)
    lbl_ad01.grid(row=0, column=2,sticky="NSEW")
    lbl_ad02 = tk.Label(tab_slice,text='k',width=6)
    lbl_ad02.grid(row=0, column=3,sticky="NSEW")
    lbl_ad03 = tk.Label(tab_slice,text='l',width=6)
    lbl_ad03.grid(row=0, column=4,sticky="NSEW")

    lbl_ad04 = tk.Label(tab_slice,text='from',width=3)
    lbl_ad04.grid(row=1, column=0,sticky="NSEW")
    lbl_ad05 = tk.Label(tab_slice,text='to',width=3)
    lbl_ad05.grid(row=2, column=0,sticky="NSEW")

    lbl_ad06 = tk.Label(tab_slice,text='±δhkl(ver)',width=7)
    lbl_ad06.grid(row=0, column=5,sticky="NSEW")
    lbl_ad07 = tk.Label(tab_slice,text='±δhkl(hor)',width=7)
    lbl_ad07.grid(row=2, column=5,sticky="NSEW")

    lbl_ad08 = tk.Label(tab_slice,text='ℏω',width=6)
    lbl_ad08.grid(row=0, column=1,sticky="NSEW")
    txt_ad01_1 = ttk.Entry(tab_slice,width=6)
    txt_ad01_1.grid(row=1, column=1,sticky="NSEW")
    txt_ad01_2 = ttk.Entry(tab_slice,width=6)
    txt_ad01_2.grid(row=2, column=1,sticky="NSEW")

    txt_ad02_1 = ttk.Entry(tab_slice,width=6)
    txt_ad02_1.grid(row=1, column=2,sticky="NSEW")
    txt_ad02_2 = ttk.Entry(tab_slice,width=6)
    txt_ad02_2.grid(row=1, column=3,sticky="NSEW")
    txt_ad02_3 = ttk.Entry(tab_slice,width=6)
    txt_ad02_3.grid(row=1, column=4,sticky="NSEW")

    txt_ad03_1 = ttk.Entry(tab_slice,width=6)
    txt_ad03_1.grid(row=2, column=2,sticky="NSEW")
    txt_ad03_2 = ttk.Entry(tab_slice,width=6)
    txt_ad03_2.grid(row=2, column=3,sticky="NSEW")
    txt_ad03_3 = ttk.Entry(tab_slice,width=6)
    txt_ad03_3.grid(row=2, column=4,sticky="NSEW")

    txt_ad04_1 = ttk.Entry(tab_slice,width=6)
    txt_ad04_1.grid(row=1, column=5,sticky="NSEW")
    txt_ad04_2 = ttk.Entry(tab_slice,width=6)
    txt_ad04_2.grid(row=3, column=5,sticky="NSEW")



    # constant E mapを表示するボタン
    button01_ad = ttk.Button(tab_slice,command=advanced_2D_constE,width=12,textvariable=constE_buttom)
    button01_ad.grid(row=3, column=1,columnspan=2,sticky="NSEW")

    # constant Q mapを表示するボタン
    button02_ad = ttk.Button(tab_slice,text="hkl vs ℏω",command=advanced_2D_constQ,width=12)
    button02_ad.grid(row=3, column=3,columnspan=2,sticky="NSEW")



    # 1Dcut along Eを表示するボタン
    button02_ad = ttk.Button(tab_slice,text="ℏω vs I",command=advanced_1D_alongE,width=11)
    button02_ad.grid(row=0, column=6,sticky="NSEW")

    # 1Dcut along Eを追加表示するボタン
    button02_ad = ttk.Button(tab_slice,text="add ℏω vs I",command=add_advanced_1D_alongE,width=11)
    button02_ad.grid(row=1, column=6,sticky="NSEW")



    # 1Dcut along Qを表示するボタン
    button02_ad = ttk.Button(tab_slice,text="hkl vs I",command=advanced_1D_alongQ,width=11)
    button02_ad.grid(row=2, column=6,sticky="NSEW")

    # 1Dcut along Qを追加表示するボタン
    button02_ad = ttk.Button(tab_slice,text="add hkl vs I",command=add_advanced_1D_alongQ,width=11)
    button02_ad.grid(row=3, column=6,sticky="NSEW")

    #########################################################
    # 3D view scattering mode

    frame_3d_RF = ttk.Labelframe(scatter_frame, text= "Range Filter")
    frame_3d_RF.grid(row = 0, column = 0, sticky="NSEW")

    frame_3d_RF.columnconfigure(0, weight=1)
    frame_3d_RF.columnconfigure(1, weight=1)
    frame_3d_RF.columnconfigure(2, weight=1)
    frame_3d_RF.rowconfigure(0, weight=1)
    frame_3d_RF.rowconfigure(1, weight=1)
    frame_3d_RF.rowconfigure(2, weight=1)
    frame_3d_RF.rowconfigure(3, weight=1)
    frame_3d_RF.rowconfigure(4, weight=1)

    label_vr_I = tk.Label(frame_3d_RF,text='Intensity',width=6)
    label_vr_I.grid(row=1, column=0,sticky="NSEW")
    label_vr_hw = tk.Label(frame_3d_RF,text='ℏω',width=6)
    label_vr_hw.grid(row=2,column=0,sticky="NSEW")
    label_vr_U = tk.Label(frame_3d_RF,textvariable=vr_U_label,width=6)
    label_vr_U.grid(row=3, column=0,sticky="NSEW")
    label_vr_V = tk.Label(frame_3d_RF,textvariable=vr_V_label,width=6)
    label_vr_V.grid(row=4, column=0,sticky="NSEW")

    label_vr_I = tk.Label(frame_3d_RF,text='from',width=4)
    label_vr_I.grid(row=0, column=1,sticky="NSEW")
    label_vr_I = tk.Label(frame_3d_RF,text='to',width=4)
    label_vr_I.grid(row=0, column=2,sticky="NSEW")

    txt_vr_I1 = ttk.Entry(frame_3d_RF,width=4)
    txt_vr_I1.grid(row=1, column=1,sticky="NSEW")
    txt_vr_I2 = ttk.Entry(frame_3d_RF,width=4)
    txt_vr_I2.grid(row=1, column=2,sticky="NSEW")

    txt_vr_hw1 = ttk.Entry(frame_3d_RF,width=4)
    txt_vr_hw1.grid(row=2, column=1,sticky="NSEW")
    txt_vr_hw2 = ttk.Entry(frame_3d_RF,width=4)
    txt_vr_hw2.grid(row=2, column=2,sticky="NSEW")

    txt_vr_U1 = ttk.Entry(frame_3d_RF,width=4)
    txt_vr_U1.grid(row=3, column=1,sticky="NSEW")
    txt_vr_U2 = ttk.Entry(frame_3d_RF,width=4)
    txt_vr_U2.grid(row=3, column=2,sticky="NSEW")

    txt_vr_V1 = ttk.Entry(frame_3d_RF,width=4)
    txt_vr_V1.grid(row=4, column=1,sticky="NSEW")
    txt_vr_V2 = ttk.Entry(frame_3d_RF,width=4)
    txt_vr_V2.grid(row=4, column=2,sticky="NSEW")

    frame_3d_IF = ttk.Labelframe(scatter_frame, text= "Isolation Filter")
    frame_3d_IF.grid(row = 0, column = 1, sticky="NSEW")

    frame_3d_IF.columnconfigure(0, weight=1)
    frame_3d_IF.columnconfigure(1, weight=1)
    frame_3d_IF.rowconfigure(0, weight=1)
    frame_3d_IF.rowconfigure(1, weight=1)
    frame_3d_IF.rowconfigure(2, weight=1)
    frame_3d_IF.rowconfigure(3, weight=1)

    label_rQ = tk.Label(frame_3d_IF,text='Qr (Å^-1)',width=6)
    label_rQ.grid(row=1, column=0,sticky="NSEW")
    txt_rQ = ttk.Entry(frame_3d_IF,width=6)
    txt_rQ.grid(row=1, column=1,sticky="NSEW")

    label_dhw = tk.Label(frame_3d_IF,text='±δℏω',width=6)
    label_dhw.grid(row=2, column=0,sticky="NSEW")
    txt_dhw = ttk.Entry(frame_3d_IF,width=6)
    txt_dhw.grid(row=2, column=1,sticky="NSEW")

    label_pcs = tk.Label(frame_3d_IF,text='min pts',width=6)
    label_pcs.grid(row=3, column=0,sticky="NSEW")
    txt_pcs = ttk.Entry(frame_3d_IF,width=6)
    txt_pcs.grid(row=3, column=1,sticky="NSEW")

    # optionを追加
    frame_3d_op = ttk.Labelframe(scatter_frame, text= "Option")
    frame_3d_op.grid(row = 0, column = 2, sticky="NSEW")

    frame_3d_op.columnconfigure(0, weight=1)
    frame_3d_op.columnconfigure(1, weight=1)
    frame_3d_op.rowconfigure(0, weight=1)
    frame_3d_op.rowconfigure(1, weight=1)
    frame_3d_op.rowconfigure(2, weight=1)
    frame_3d_op.rowconfigure(3, weight=1)
    frame_3d_op.rowconfigure(4, weight=1)

    # graph opetionを表示するボタン周りのフレーム作成。
    frameGSs2 = ttk.Labelframe(scatter_frame, text= "Graph Scale")
    frameGSs2.grid(row = 1, column = 2,sticky="NSEW")
    #frameGSs2.grid_propagate(True)

    frameGSs2.columnconfigure(0, weight=1)
    frameGSs2.columnconfigure(1, weight=1)
    frameGSs2.columnconfigure(2, weight=1)
    frameGSs2.rowconfigure(0, weight=1)
    frameGSs2.rowconfigure(1, weight=1)
    frameGSs2.rowconfigure(2, weight=1)
    frameGSs2.rowconfigure(3, weight=1)
    frameGSs2.rowconfigure(4, weight=1)
    frameGSs2.rowconfigure(5, weight=1)
    frameGSs2.rowconfigure(6, weight=1)

    # graph scale
    graph_scale_lbl0_2 = tk.Label(frameGSs2,text='min',width=6)
    graph_scale_lbl0_2.grid(row=1, column=1,sticky="NSEW")
    graph_scale_lbl1_2 = tk.Label(frameGSs2,text='max',width=6)
    graph_scale_lbl1_2.grid(row=1, column=2,sticky="NSEW")

    scale_s_Imin_lbl_2 = tk.Label(frameGSs2,text='Intensity',width=6)
    scale_s_Imin_lbl_2.grid(row=2, column=0,sticky="NSEW")
    scale_s_Imin_txt_2 = ttk.Entry(frameGSs2,width=6)
    scale_s_Imin_txt_2.grid(row=2, column=1,sticky="NSEW")
    scale_s_Imax_txt_2 = ttk.Entry(frameGSs2,width=6)
    scale_s_Imax_txt_2.grid(row=2, column=2,sticky="NSEW")

    scale_s_Emin_lbl_2 = tk.Label(frameGSs2,text='ℏω',width=6)
    scale_s_Emin_lbl_2.grid(row=3, column=0,sticky="NSEW")
    scale_s_Emin_txt_2 = ttk.Entry(frameGSs2,width=6)
    scale_s_Emin_txt_2.grid(row=3, column=1,sticky="NSEW")
    scale_s_Emax_txt_2 = ttk.Entry(frameGSs2,width=6)
    scale_s_Emax_txt_2.grid(row=3, column=2,sticky="NSEW")

    scale_s_Umin_lbl_2 = tk.Label(frameGSs2,width=6,textvariable=U_lavel)
    scale_s_Umin_lbl_2.grid(row=4, column=0,sticky="NSEW")
    scale_s_Umin_txt_2 = ttk.Entry(frameGSs2,width=6)
    scale_s_Umin_txt_2.grid(row=4, column=1,sticky="NSEW")
    scale_s_Umax_txt_2 = ttk.Entry(frameGSs2,width=6)
    scale_s_Umax_txt_2.grid(row=4, column=2,sticky="NSEW")

    scale_s_Vmin_lbl_2 = tk.Label(frameGSs2,width=6,textvariable=V_lavel)
    scale_s_Vmin_lbl_2.grid(row=5, column=0,sticky="NSEW")
    scale_s_Vmin_txt_2 = ttk.Entry(frameGSs2,width=6)
    scale_s_Vmin_txt_2.grid(row=5, column=1,sticky="NSEW")
    scale_s_Vmax_txt_2 = ttk.Entry(frameGSs2,width=6)
    scale_s_Vmax_txt_2.grid(row=5, column=2,sticky="NSEW")


    gs_clear2 = ttk.Button(frameGSs2,text="clear",command=gs_clear2,width=6)
    gs_clear2.grid(row=6, column=0, columnspan=3, sticky="NSEW")


    gs_auto2 = ttk.Button(frameGSs2,text="auto scale",command=gs_auto2)
    gs_auto2.grid(row=0, column=0, columnspan=3,sticky="NSEW")

    # カラーモード用の変数（初期値は 'color'）
    color_mode_var = tk.StringVar(value="linear")

    radio_linear = tk.Radiobutton(
        frame_3d_op, text="linear", variable=color_mode_var, value="linear"
    )
    radio_linear.grid(row=0, column=0, columnspan=2, sticky="NSEW")

    radio_log = tk.Radiobutton(
        frame_3d_op, text="log", variable=color_mode_var, value="log"
    )
    radio_log.grid(row=1, column=0, columnspan=2, sticky="NSEW")

    radio_colorbar = tk.Radiobutton(
        frame_3d_op, text="color off", variable=color_mode_var, value="coloroff"
    )
    radio_colorbar.grid(row=2, column=0, columnspan=2, sticky="NSEW")

    # 散布図の点のサイズ
    size_lbl = tk.Label(frame_3d_op,text='point size',width=2)
    size_lbl.grid(row=3, column=0,sticky="NSEW")
    size_txt = ttk.Entry(frame_3d_op,width=2)
    size_txt.grid(row=3, column=1,sticky="NSEW")
    size_txt.insert(0, 5)

    # gridのon off
    # チェックボックスの状態を保持する変数
    grid_var = tk.BooleanVar(value=True)  # ← デフォルトでチェックあり

    # チェックボックスの作成と配置
    chk_grid = tk.Checkbutton(frame_3d_op, text="grid", variable=grid_var)
    chk_grid.grid(row=4, column=0, columnspan=2, sticky="NSEW")  # 左寄せ（必要に応じて調整）

    # thresholdボタン

    # auto rangeボタン
    button_3d_srh_auto = ttk.Button(frame_3d_IF,command=threshold_auto,text= "default",width=6)
    button_3d_srh_auto.grid(row=0, column=1, sticky="NSEW")

    # --- チェックボックス ---
    def threshold_toggle_entries():
        state = "normal" if check_var.get() else "disabled"
        txt_rQ.config(state=state)
        txt_dhw.config(state=state)
        txt_pcs.config(state=state)
        # ボタンも有効/無効を連動
        button_3d_srh_auto.config(state=state)

    # thresholdのon/offチェックボックス
    check_var = tk.BooleanVar(value=False)
    check_button = tk.Checkbutton(frame_3d_IF, text="on", variable=check_var, command=threshold_toggle_entries)
    check_button.grid(row=0, column=0, sticky="NSEW")

    # 初期状態を disabled に設定
    threshold_toggle_entries()

    # 表示範囲autoボタン

    # auto rangeボタン
    button_3d_ran_auto = ttk.Button(frame_3d_RF,command=range_auto_3D,text= "max range",width=8)
    button_3d_ran_auto.grid(row=0, column=0,sticky="NSEW")


    # 3d plotと2d plotのボタンとパラメータの入力フレームを追加
    frame_sca = ttk.Labelframe(scatter_frame, text= "Visualization")
    frame_sca.grid(row = 1, column = 0, columnspan=2, sticky="NSEW")

    # Notebookウィジェットの作成
    notebook_sca = ttk.Notebook(frame_sca,style="example.TNotebook")

    # タブの作成
    tab_3dsca = tk.Frame(notebook_sca)
    tab_2dsca = tk.Frame(notebook_sca)

    # notebookにタブを追加
    notebook_sca.add(tab_3dsca, text="3D view")# 3d scatterの表示
    notebook_sca.add(tab_2dsca, text="2D view")# 2d scatterの表示

    # ウィジェットの配置
    notebook_sca.pack(expand=True, fill='both')

    tab_3dsca.columnconfigure(0, weight=1)
    tab_3dsca.rowconfigure(0, weight=1)

    tab_2dsca.columnconfigure(0, weight=1)
    tab_2dsca.columnconfigure(1, weight=1)
    tab_2dsca.columnconfigure(2, weight=1)
    tab_2dsca.columnconfigure(3, weight=1)
    tab_2dsca.columnconfigure(4, weight=1)
    tab_2dsca.columnconfigure(5, weight=1)
    tab_2dsca.rowconfigure(0, weight=1)
    tab_2dsca.rowconfigure(1, weight=1)
    tab_2dsca.rowconfigure(2, weight=1)

    # 3D display ボタン
    button_3ddisp = ttk.Button(tab_3dsca,command=disp3D,textvariable=scatter3d_buttom,width=6)
    button_3ddisp.grid(row=0, column=0, sticky="NSEW")

    # 2D displau ボタン
    # tab_2dscaに配置するウィジェットの作成。constant E mapの表示
    # 取り出すEの範囲を指定する欄の整備
    lbl_3dsca_1e = tk.Label(tab_2dsca,text='ℏω',width=6)
    lbl_3dsca_1e.grid(row=0, column=0,sticky="NSEW")
    lbl_3dsca_2e = tk.Label(tab_2dsca,text='±ℏω',width=6)
    lbl_3dsca_2e.grid(row=0, column=1,sticky="NSEW")
    txt_3dsca_1e = ttk.Entry(tab_2dsca,width=6)
    txt_3dsca_1e.insert(0,0)
    txt_3dsca_1e.grid(row=1, column=0,sticky="NSEW")
    txt_3dsca_2e = ttk.Entry(tab_2dsca,width=6)
    txt_3dsca_2e.insert(0,0.1)
    txt_3dsca_2e.grid(row=1, column=1,sticky="NSEW")

    # tab_2dscaに配置するウィジェットの作成。V方向のconstant Q mapの表示と1次元カット
    # 取り出すEの範囲を指定する欄の整備
    lbl_3dsca_1u = tk.Label(tab_2dsca,width=6,textvariable=U_lavel)
    lbl_3dsca_1u.grid(row=0, column=2,sticky="NSEW")
    lbl_3dsca_2u = tk.Label(tab_2dsca,width=6,textvariable=pmU_lavel)
    lbl_3dsca_2u.grid(row=0, column=3,sticky="NSEW")
    txt_3dsca_1u = ttk.Entry(tab_2dsca,width=6)
    txt_3dsca_1u.insert(0,'0')
    txt_3dsca_1u.grid(row=1, column=2,sticky="NSEW")
    txt_3dsca_2u = ttk.Entry(tab_2dsca,width=6)
    txt_3dsca_2u.insert(0,'0.1')
    txt_3dsca_2u.grid(row=1, column=3,sticky="NSEW")

    # tab_2dscaに配置するウィジェットの作成。U方向のconstant Q mapの表示
    # 取り出すEの範囲を指定する欄の整備
    lbl_3dsca_1v = tk.Label(tab_2dsca,width=6,textvariable=V_lavel)
    lbl_3dsca_1v.grid(row=0, column=4,sticky="NSEW")
    lbl_3dsca_2v = tk.Label(tab_2dsca,width=6,textvariable=pmV_lavel)
    lbl_3dsca_2v.grid(row=0, column=5,sticky="NSEW")
    txt_3dsca_1v = ttk.Entry(tab_2dsca,width=6)
    txt_3dsca_1v.insert(0,'0')
    txt_3dsca_1v.grid(row=1, column=4,sticky="NSEW")
    txt_3dsca_2v = ttk.Entry(tab_2dsca,width=6)
    txt_3dsca_2v.insert(0,'0.1')
    txt_3dsca_2v.grid(row=1, column=5,sticky="NSEW")




    #constant E mapファイルの読み込みのボタンの作成
    button_2dsca_cE = ttk.Button(tab_2dsca,command=scatter_2d_cE,width=12,textvariable=constE_buttom)
    button_2dsca_cE.grid(row=2, column=0,columnspan=2,sticky="NSEW")

    # V方向にconstantQカットした図を表示するボタン
    button_2dsca_cU = ttk.Button(tab_2dsca,command=scatter_2d_cU,textvariable=constV_buttom,width=12)
    button_2dsca_cU.grid(row=2, column=2,columnspan=2,sticky="NSEW")

    button_2dsca_cV = ttk.Button(tab_2dsca,command=scatter_2d_cV,textvariable=constU_buttom,width=12)
    button_2dsca_cV.grid(row=2, column=4,columnspan=2,sticky="NSEW")

    #########################################################
    # 3D view E direction, slicing mode

    # initial値を入力する。 ℏω
    lbl_3d_ini_hw = tk.Label(tab_3d,text='initial ℏω',width=8)
    lbl_3d_ini_hw.grid(row=0, column=0,sticky="NSEW")
    txt_3d_ini_hw = ttk.Entry(tab_3d,width=6)
    txt_3d_ini_hw.grid(row=1, column=0,sticky="NSEW")

    lbl_3d_ini_U = tk.Label(tab_3d,width=8,textvariable=initialU_label)
    lbl_3d_ini_U.grid(row=0, column=1,sticky="NSEW")
    txt_3d_ini_U = ttk.Entry(tab_3d,width=6)
    txt_3d_ini_U.grid(row=1, column=1,sticky="NSEW")

    lbl_3d_ini_V = tk.Label(tab_3d,width=8,textvariable=initialV_label)
    lbl_3d_ini_V.grid(row=0, column=2,sticky="NSEW")
    txt_3d_ini_V = ttk.Entry(tab_3d,width=6)
    txt_3d_ini_V.grid(row=1, column=2,sticky="NSEW")

    # ダミーの空行
    lbl_3d_dammy = tk.Label(tab_3d,text='',width=6)
    lbl_3d_dammy.grid(row=3, column=0,sticky="NSEW")

    #constant E mapを動的に表示

    # constant E mapを動的に表示するボタン
    button17 = ttk.Button(tab_3d,command=show_3DconEmap,textvariable=constE_buttom)
    button17.grid(row=2, column=0,sticky="NSEW")

    # V方向のconstant Q mapの動的表示の定義

    # V方向にconstantQカットした図を動的に表示するボタン
    button15 = ttk.Button(tab_3d,command=constQmap_V2,textvariable=constV_buttom)
    button15.grid(row=2, column=1,sticky="NSEW")

    # U方向のconstant Q mapの動的な表示の定義

    # U方向にconstantQカットした図を動的に表示するボタン
    button16 = ttk.Button(tab_3d,command=constQmap_U2,textvariable=constU_buttom)
    button16.grid(row=2, column=2,sticky="NSEW")
    ##############################################
    # 2D view const E cut
    # tab_2dに配置するウィジェットの作成。constant E mapの表示
    # 取り出すEの範囲を指定する欄の整備
    lbl_2d_1e = tk.Label(tab_2d,text='ℏω',width=6)
    lbl_2d_1e.grid(row=0, column=0,sticky="NSEW")
    lbl_2d_2e = tk.Label(tab_2d,text='±ℏω',width=6)
    lbl_2d_2e.grid(row=0, column=1,sticky="NSEW")
    txt_2d_1e = ttk.Entry(tab_2d,width=6)
    txt_2d_1e.insert(0,0)
    txt_2d_1e.grid(row=1, column=0,sticky="NSEW")
    txt_2d_2e = ttk.Entry(tab_2d,width=6)
    txt_2d_2e.insert(0,0.1)
    txt_2d_2e.grid(row=1, column=1,sticky="NSEW")
    lbl_2d_d = tk.Label(tab_2d,text='',width=6)
    lbl_2d_d.grid(row=3, column=0,pady=1,sticky="NSEW")

    # tab_2dに配置するウィジェットの作成。V方向のconstant Q mapの表示と1次元カット
    # 取り出すEの範囲を指定する欄の整備
    lbl_2d_1v = tk.Label(tab_2d,width=6,textvariable=U_lavel)
    lbl_2d_1v.grid(row=0, column=2,sticky="NSEW")
    lbl_2d_2v = tk.Label(tab_2d,width=6,textvariable=pmU_lavel)
    lbl_2d_2v.grid(row=0, column=3,sticky="NSEW")
    txt_2d_1v = ttk.Entry(tab_2d,width=6)
    txt_2d_1v.insert(0,'0')
    txt_2d_1v.grid(row=1, column=2,sticky="NSEW")
    txt_2d_2v = ttk.Entry(tab_2d,width=6)
    txt_2d_2v.insert(0,'0.1')
    txt_2d_2v.grid(row=1, column=3,sticky="NSEW")

    # tab_2dに配置するウィジェットの作成。U方向のconstant Q mapの表示
    # 取り出すEの範囲を指定する欄の整備
    lbl_2d_1u = tk.Label(tab_2d,width=6,textvariable=V_lavel)
    lbl_2d_1u.grid(row=0, column=4,sticky="NSEW")
    lbl_2d_2u = tk.Label(tab_2d,width=6,textvariable=pmV_lavel)
    lbl_2d_2u.grid(row=0, column=5,sticky="NSEW")
    txt_2d_1u = ttk.Entry(tab_2d,width=6)
    txt_2d_1u.insert(0,'0')
    txt_2d_1u.grid(row=1, column=4,sticky="NSEW")
    txt_2d_2u = ttk.Entry(tab_2d,width=6)
    txt_2d_2u.insert(0,'0.1')
    txt_2d_2u.grid(row=1, column=5,sticky="NSEW")

    # constEmap表示の定義

    #constant E mapファイルの読み込みのボタンの作成
    button8 = ttk.Button(tab_2d,command=constEmap,width=12,textvariable=constE_buttom)
    button8.grid(row=2, column=0,columnspan=2,sticky="NSEW")

    # V方向のconstant Q mapの表示の定義

    # V方向にconstantQカットした図を表示するボタン
    button11 = ttk.Button(tab_2d,command=constQmap_V,textvariable=constV_buttom,width=12)
    button11.grid(row=2, column=2,columnspan=2,sticky="NSEW")

    # U方向のconstant Q mapの表示の定義

    # U方向にconstantQカットした図を表示するボタン
    button12 = ttk.Button(tab_2d,command=constQmap_U,textvariable=constU_buttom,width=12)
    button12.grid(row=2, column=4,columnspan=2,sticky="NSEW")

    ################################################
    # 1d view
    # 1Dカットしたい範囲を指定するboxを作成
    lbl_1d_1 = tk.Label(tab_1d,text='ℏω',width=6)
    lbl_1d_1.grid(row=0, column=0,sticky="NSEW")
    lbl_1d_2 = tk.Label(tab_1d,text='±ℏω',width=6)
    lbl_1d_2.grid(row=0, column=1,sticky="NSEW")
    txt_1d_1 = ttk.Entry(tab_1d,width=6)
    txt_1d_1.insert(0,'0')
    txt_1d_1.grid(row=1, column=0,sticky="NSEW")
    txt_1d_2 = ttk.Entry(tab_1d,width=6)
    txt_1d_2.insert(0,'0.1')
    txt_1d_2.grid(row=1, column=1,sticky="NSEW")

    lbl_1d_3 = tk.Label(tab_1d,width=6,textvariable=U_lavel)
    lbl_1d_3.grid(row=0, column=2,sticky="NSEW")
    lbl_1d_4 = tk.Label(tab_1d,width=6,textvariable=pmU_lavel)
    lbl_1d_4.grid(row=0, column=3,sticky="NSEW")
    txt_1d_3 = ttk.Entry(tab_1d,width=6)
    txt_1d_3.insert(0,'0')
    txt_1d_3.grid(row=1, column=2,sticky="NSEW")
    txt_1d_4 = ttk.Entry(tab_1d,width=6)
    txt_1d_4.insert(0,'0.1')
    txt_1d_4.grid(row=1, column=3,sticky="NSEW")

    lbl_1d_5 = tk.Label(tab_1d,width=6,textvariable=V_lavel)
    lbl_1d_5.grid(row=0, column=4,sticky="NSEW")
    lbl_1d_6 = tk.Label(tab_1d,width=6,textvariable=pmV_lavel)
    lbl_1d_6.grid(row=0, column=5,sticky="NSEW")
    txt_1d_5 = ttk.Entry(tab_1d,width=6)
    txt_1d_5.insert(0,'0')
    txt_1d_5.grid(row=1, column=4,sticky="NSEW")
    txt_1d_6 = ttk.Entry(tab_1d,width=6)
    txt_1d_6.insert(0,'0.1')
    txt_1d_6.grid(row=1, column=5,sticky="NSEW")

    # UとVの範囲を指定してE方向への1次元カットをする。

    # UとVの範囲を指定して１次元カットしグラフ表示するボタンの設定。
    button13 = ttk.Button(tab_1d,text="ℏω vs I",command=constQmap_1D,width=12)
    button13.grid(row=2, column=0,columnspan=2,sticky="NSEW")

    # 追加で1Dcutを重ね書きする機能の定義

    # UとVの範囲を指定した１次元カットを重ね書きするボタンの設定。
    button13_2 = ttk.Button(tab_1d,text="add ℏω vs I",command=constQmap_1D2,width=12)
    button13_2.grid(row=3, column=0,columnspan=2,sticky="NSEW")


    # V方向に１次元カットした図を表示するボタン
    button10 = ttk.Button(tab_1d,command=constE_1D_U,width=12,textvariable=IvsU_buttom)
    button10.grid(row=2, column=2,columnspan=2,sticky="NSEW")

    #　１次元カットのグラフを追加する機能

    # V方向に１次元カットした図を重ねするボタン
    button10_2 = ttk.Button(tab_1d,command=constE_1D_U2,width=12,textvariable=addIvsU_buttom)
    button10_2.grid(row=3, column=2,columnspan=2,sticky="NSEW")

    # V方向への１次元カットボタンの定義

    # V方向に１次元カットした図を追加表示するボタン
    button9 = ttk.Button(tab_1d,command=constE_1D_V,width=12,textvariable=IvsV_buttom)
    button9.grid(row=2, column=4,columnspan=2,sticky="NSEW")


    # U方向に１次元カットした図を重ねするボタン
    button9_2 = ttk.Button(tab_1d,command=constE_1D_V2,width=12,textvariable=addIvsV_buttom)
    button9_2.grid(row=3, column=4,columnspan=2,sticky="NSEW")

    tas_layout = _build_tas_data_section(tab_4, state, xaxis_select, axistype)
    ###############################################################################
    #powderの項目
    # データボックスを作成するボタン周りのフレーム作成。

    result = dict(locals())
    result.update(tas_layout)
    result.pop('env', None)
    return result
