from ...callback_runtime import *

def xaxis_selectp(env):
    axistypep = env.get('axistypep')
    cb_dp = env.get('cb_dp')
    cbp = env.get('cbp')
    gridtypep = env.get('gridtypep')
    state = env.get('state')
    xlist = env.get('xlist')
    # まずデータを読み込む
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
    fig10=plt.figure()

    # グラフ内に表示範囲を決定するボックス
    # 最小値と最大値の初期値
    default_xmin = round(xlim_min, 2)
    default_xmax = round(xlim_max, 2)

    default_ymin = round(ylim_min, 2)
    default_ymax = round(ylim_max, 2)

    # テキストボックスを作成して最小値と最大値を設定
    xmin_box = TextBox(plt.axes([0.3, 0.02, 0.08, 0.05]), 'xMin:', initial=str(default_xmin))
    xmax_box = TextBox(plt.axes([0.82, 0.02, 0.08, 0.05]), 'xMax:', initial=str(default_xmax))
    ymin_box = TextBox(plt.axes([0.1, 0.2, 0.08, 0.05]), 'yMin:', initial=str(default_ymin))
    ymax_box = TextBox(plt.axes([0.1, 0.83, 0.08, 0.05]), 'yMax:', initial=str(default_ymax))

    # 最小値と最大値が変更されたときに呼び出される関数
    def update_axis_range(text):
        try:
            xmin_val = float(xmin_box.text)
            xmax_val = float(xmax_box.text)
            ax10.set_xlim(xmin_val, xmax_val)
            ymin_val = float(ymin_box.text)
            ymax_val = float(ymax_box.text)
            ax10.set_ylim(ymin_val, ymax_val)
            fig10.canvas.draw_idle()
        except ValueError:
            pass

    xmin_box.on_submit(update_axis_range)
    xmax_box.on_submit(update_axis_range)
    ymin_box.on_submit(update_axis_range)
    ymax_box.on_submit(update_axis_range)

    # shared variables are stored in state
    # 現在のFigure番号を取得
    state['fig_tas'] = plt.gcf().number
    fig10.subplots_adjust(left=0.30,bottom=0.2)
    ax10 = fig10.add_subplot(111)
    xlist =['Pt','c2 (deg)', 'a2 (deg)', 'q (Å^-1)' ,'h (r.l.u.)', 'k (r.l.u.)', 'l (r.l.u.)', 'e (meV)', 'T (K)']
    plt.xlabel(xlist[x_select])
    plt.ylabel("Intensity (count)")
    ax10.errorbar(xbox[x_select,:], ybox[y_select,:], yerr=ybox[y_select,:]**(1/2), capsize=10, label='Detector'+str(y_select+1))
    gt=gridtypep.get()
    if gt == 0:
        #ax.set_axisbelow(True)  # グリッド線を背面に配置
        ax10.grid(False)
    elif gt == 1:
        ax10.grid(True)
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
