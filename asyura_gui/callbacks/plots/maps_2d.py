from ...callback_runtime import *

def constQmap_V2(env):
    axistype = env.get('axistype')
    gridtype = env.get('gridtype')
    scale_s_Emax_txt = env.get('scale_s_Emax_txt')
    scale_s_Emin_txt = env.get('scale_s_Emin_txt')
    scale_s_Imax_txt = env.get('scale_s_Imax_txt')
    scale_s_Imin_txt = env.get('scale_s_Imin_txt')
    scale_s_Vmax_txt = env.get('scale_s_Vmax_txt')
    scale_s_Vmin_txt = env.get('scale_s_Vmin_txt')
    state = env.get('state')
    txt10 = env.get('txt10')
    txt11 = env.get('txt11')
    txt12 = env.get('txt12')
    txt13 = env.get('txt13')
    txt14 = env.get('txt14')
    txt9 = env.get('txt9')
    txt_3d_ini_U = env.get('txt_3d_ini_U')
    txt_ul = env.get('txt_ul')
    txt_vl = env.get('txt_vl')
    # 初期値
    if txt_3d_ini_U.get()=="":
        sa3 = 0
    else:
        # 一番近い値を探す
        sa3 = np.abs(state['QU2'] - float(txt_3d_ini_U.get())).argmin()

    # 軸設定。空欄の場合は範囲マックスを表示するようにする
    if scale_s_Vmin_txt.get()=="":
        Vlim_min=round(np.min(state['QV']),2)
    else:
        Vlim_min=float(scale_s_Vmin_txt.get())
    if scale_s_Vmax_txt.get()=="":
        Vlim_max=round(np.max(state['QV']),2)
    else:
        Vlim_max=float(scale_s_Vmax_txt.get())

    if scale_s_Emin_txt.get()=="":
        Elim_min=round(float(state['energylist'][0]), 2)
    else:
        Elim_min=float(scale_s_Emin_txt.get())
    if scale_s_Emax_txt.get()=="":
        Elim_max=float(round(state['energylist'][-1],2))
    else:
        Elim_max=float(scale_s_Emax_txt.get())


    # カラーバースケール。空欄の場合は平均値を出力するようにする。
    if scale_s_Imin_txt.get()=="":
        if np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]) >= 0:
            z_min=0
        elif np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]) < 0:
            z_min=round(np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]),1)
    else:
        z_min=float(scale_s_Imin_txt.get())

    if scale_s_Imax_txt.get()=="":
        if np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]) >= 0:
            z_max=round(np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]),1)
        elif np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]) < 0:
            z_max=0
    else:
        z_max=float(scale_s_Imax_txt.get())

    # 変数　QU, QV, QU2, QV2, I ,Ierr
    hw_num = int(len(state['energylist'])+1)
    hwlist7=np.zeros(hw_num)
    #hwが1つのときの例外処理として装置分解能の範囲を出力するようにする
    if hw_num==2:
        hwlist7[0] = float(state['energylist'][0]-(state['ef_tol']+0.005))
        hwlist7[1] = float(state['energylist'][-1]+(state['ef_tol']+0.005))
    else:
        hwlist7[0] = float(state['energylist'][0])-(float(state['energylist'][1])-float(state['energylist'][0]))
        hwlist7[-1] = float(state['energylist'][-1])+(float(state['energylist'][-1])-float(state['energylist'][-2]))

    #hwlist5[0] = float(energylist[0])-(float(energylist[1])-float(energylist[0]))
    #hwlist5[-1] = float(energylist[-1])+(float(energylist[-1])-float(energylist[-2]))

        for ne in range(hw_num-2):
            hwlist7[ne+1] = (float(state['energylist'][ne])+float(state['energylist'][ne+1]))/2
    #図を出力する

    #intensityの範囲
    #fig, ax = plt.figure()
    #axにカラーバーを表示
    fig3, ax = plt.subplots()
    plt.subplots_adjust(left=0.30, right=0.75, bottom=0.25)
    at=axistype.get()
    # グリッド線を引く
    gt=gridtype.get()
    if gt == 0:
        #ax.set_axisbelow(True)  # グリッド線を背面に配置
        ax.grid(False)
    elif gt == 1:
        ax.grid(True)
    if at==0:
        im=plt.pcolormesh(state['QV'], hwlist7, state['I'][:,:,sa3], cmap='jet', vmin=z_min, vmax=z_max)
    elif at==1:
        if z_min==0:
            z_min=np.nanmin(state['I'][state['I'] != 0])
            im=plt.pcolormesh(state['QV'], hwlist7, state['I'][:,:,sa3], cmap='jet', norm = LogNorm(vmin=np.nanmin(state['I'][state['I'] != 0]), vmax=z_max))
        else:
            im=plt.pcolormesh(state['QV'], hwlist7, state['I'][:,:,sa3], cmap='jet', norm = LogNorm(vmin=z_min, vmax=z_max))
    cbar=plt.colorbar(im,ticks=mticker.LinearLocator(numticks=3))
    # カラーバーのタイトルを設定
    cbar.set_label('Intenisty (a.u.)')
    #, cmap="jet", extend='both',ticks=np.linspace(vmin, vmax, 5)
    #plt.axis('tight')
    #横スライドでUを変更、縦スライドで強度の最大値を変更
    ax_a = plt.axes([0.3, 0.02, 0.45, 0.04]) #plt.axes([x, y, width, height] ) 
    sli_a3 = wg.Slider(ax_a, f'{txt_ul.get()}', 0, len(state['QU2'])-1, valinit=sa3,valstep=1, orientation='horizontal')
    ax.text(0.1,1.1,f'{txt_ul.get()} = %.2f (r.l.u.)' %state['QU2'][sa3], transform=ax.transAxes)

    # 図のラベルを作成
    if float(txt12.get())==0:
        if float(txt9.get())==0:
            vl1 = str('0')
        else:
            vl1 = str("{:.3f}".format(float(txt9.get())*state['QU2'][sa3]))
    elif float(txt12.get())==1:
        if float(txt9.get())==0:
            vl1 = str(txt_vl.get())
        else:
            vl1 = str("{:.3f}".format(float(txt9.get())*state['QU2'][sa3]))+str('+')+str(txt_vl.get())
    elif float(txt12.get())==-1:
        if float(txt9.get())==0:
            vl1 = str('-')+str(txt_vl.get())
        else:
            vl1 = str("{:.3f}".format(float(txt9.get())*state['QU2'][sa3]))+str('-')+str(txt_vl.get())
    else:
        try:
            number1 = float(txt12.get())
            if number1.is_integer():#整数である
                if number1<0:#Vベクトルの値が負であった場合
                    if float(txt9.get())==0:
                        vl1 = str('-')+str(int(np.abs(float(txt12.get()))))+str(txt_vl.get())
                    else:
                        vl1 = str("{:.3f}".format(float(txt9.get())*state['QU2'][sa3]))+str('-')+str(int(np.abs(float(txt12.get()))))+str(txt_vl.get())
                elif number1>0:#Vベクトルの値が正であった場合
                    if float(txt9.get())==0:
                        vl1 = str(int(float(txt12.get())))+str(txt_vl.get())
                    else:
                        vl1 = str("{:.3f}".format(float(txt9.get())*state['QU2'][sa3]))+str('+')+str(int(float(txt12.get())))+str(txt_vl.get())
            else:#整数でない
                if number1<0:#Vベクトルの値が負であった場合
                    if float(txt9.get())==0:
                        vl1 = str('-')+str(np.abs(float(txt12.get())))+str(txt_vl.get())
                    else:
                        vl1 = str("{:.3f}".format(float(txt9.get())*state['QU2'][sa3]))+str('-')+str(np.abs(float(txt12.get())))+str(txt_vl.get())
                elif number1>0:#Vベクトルの値が正であった場合
                    if float(txt9.get())==0:
                        vl1 = str(float(txt12.get()))+str(txt_vl.get())
                    else:
                        vl1 = str("{:.3f}".format(float(txt9.get())*state['QU2'][sa3]))+str('+')+str(float(txt12.get()))+str(txt_vl.get())
        except ValueError:#整数でない
            pass

    if float(txt13.get())==0:
        if float(txt10.get())==0:
            vl2 = str('0')
        else:
            vl2 = str("{:.3f}".format(float(txt10.get())*state['QU2'][sa3]))
    elif float(txt13.get())==1:
        if float(txt10.get())==0:
            vl2 = str(txt_vl.get())
        else:
            vl2 = str("{:.3f}".format(float(txt10.get())*state['QU2'][sa3]))+str('+')+str(txt_vl.get())
    elif float(txt13.get())==-1:
        if float(txt10.get())==0:
            vl2 = str('-')+str(txt_vl.get())
        else:
            vl2 = str("{:.3f}".format(float(txt10.get())*state['QU2'][sa3]))+str('-')+str(txt_vl.get())
    else:
        try:
            number2 = float(txt13.get())
            if number2.is_integer():#整数である
                if number2<0:#Vベクトルの値が負であった場合
                    if float(txt10.get())==0:
                        vl2 = str('-')+str(int(np.abs(float(txt13.get()))))+str(txt_vl.get())
                    else:
                        vl2 = str("{:.3f}".format(float(txt10.get())*state['QU2'][sa3]))+str('-')+str(int(np.abs(float(txt13.get()))))+str(txt_vl.get())
                elif number2>0:#Vベクトルの値が正であった場合
                    if float(txt10.get())==0:
                        vl2 = str(int(float(txt13.get())))+str(txt_vl.get())
                    else:
                        vl2 = str("{:.3f}".format(float(txt10.get())*state['QU2'][sa3]))+str('+')+str(int(float(txt13.get())))+str(txt_vl.get())
            else:#整数でない
                if number2<0:#Vベクトルの値が負であった場合
                    if float(txt10.get())==0:
                        vl2 = str('-')+str(np.abs(float(txt13.get())))+str(txt_vl.get())
                    else:
                        vl2 = str("{:.3f}".format(float(txt10.get())*state['QU2'][sa3]))+str('-')+str(np.abs(float(txt13.get())))+str(txt_vl.get())
                elif number2>0:#Vベクトルの値が正であった場合
                    if float(txt10.get())==0:
                        vl2 = str(float(txt13.get()))+str(txt_vl.get())
                    else:
                        vl2 = str("{:.3f}".format(float(txt10.get())*state['QU2'][sa3]))+str('+')+str(float(txt13.get()))+str(txt_vl.get())
        except ValueError:#整数でない
            pass

    if float(txt14.get())==0:
        if float(txt11.get())==0:
            vl3 = str('0')
        else:
            vl3 = str("{:.3f}".format(float(txt11.get())*state['QU2'][sa3]))
    elif float(txt14.get())==1:
        if float(txt11.get())==0:
            vl3 = str(txt_vl.get())
        else:
            vl3 = str("{:.3f}".format(float(txt11.get())*state['QU2'][sa3]))+str('+')+str(txt_vl.get())
    elif float(txt14.get())==-1:
        if float(txt11.get())==0:
            vl3 = str('-')+str(txt_vl.get())
        else:
            vl3 = str("{:.3f}".format(float(txt11.get())*state['QU2'][sa3]))+str('-')+str(txt_vl.get())
    else:
        try:
            number3 = float(txt14.get())
            if number3.is_integer():#整数である
                if number3<0:#Vベクトルの値が負であった場合
                    if float(txt11.get())==0:
                        vl3 = str('-')+str(int(np.abs(float(txt14.get()))))+str(txt_vl.get())
                    else:
                        vl3 = str("{:.3f}".format(float(txt11.get())*state['QU2'][sa3]))+str('-')+str(int(np.abs(float(txt14.get()))))+str(txt_vl.get())
                elif number3>0:#Vベクトルの値が正であった場合
                    if float(txt11.get())==0:
                        vl3 = str(int(float(txt14.get())))+str(txt_vl.get())
                    else:
                        vl3 = str("{:.3f}".format(float(txt11.get())*state['QU2'][sa3]))+str('+')+str(int(float(txt14.get())))+str(txt_vl.get())
            else:#整数でない
                if number3<0:#Vベクトルの値が負であった場合
                    if float(txt11.get())==0:
                        vl3 = str('-')+str(np.abs(float(txt14.get())))+str(txt_vl.get())
                    else:
                        vl3 = str("{:.3f}".format(float(txt11.get())*state['QU2'][sa3]))+str('-')+str(np.abs(float(txt14.get())))+str(txt_vl.get())
                elif number3>0:#Vベクトルの値が正であった場合
                    if float(txt11.get())==0:
                        vl3 = str(float(txt14.get()))+str(txt_vl.get())
                    else:
                        vl3 = str("{:.3f}".format(float(txt11.get())*state['QU2'][sa3]))+str('+')+str(float(txt14.get()))+str(txt_vl.get())
        except ValueError:#整数でない
            pass

    Vlabel3 = (f"({vl1},{vl2},{vl3})")

    ax.set_xlabel(str(Vlabel3))
    ax.set_ylabel("ℏω (meV)")
    ax.set_xlim(Vlim_min,Vlim_max)
    ax.set_ylim(Elim_min,Elim_max)

    # グラフ内に表示範囲を決定するボックス
    # 最小値と最大値の初期値
    default_xmin = round(Vlim_min, 3)
    default_xmax = round(Vlim_max, 3)

    default_ymin = round(Elim_min, 3)
    default_ymax = round(Elim_max, 3)

    default_zmin = round(z_min, 3)
    default_zmax = round(z_max, 3)

    # テキストボックスを作成して最小値と最大値を設定
    xmin_box = TextBox(plt.axes([0.3, 0.10, 0.08, 0.05]), 'xMin:', initial=str(default_xmin))
    xmax_box = TextBox(plt.axes([0.6, 0.10, 0.08, 0.05]), 'xMax:', initial=str(default_xmax))

    ymin_box = TextBox(plt.axes([0.1, 0.2, 0.08, 0.05]), 'yMin:', initial=str(default_ymin))
    ymax_box = TextBox(plt.axes([0.1, 0.83, 0.08, 0.05]), 'yMax:', initial=str(default_ymax))

    zmin_box = TextBox(plt.axes([0.9, 0.2, 0.08, 0.05]), 'zMin:', initial=str(default_zmin))
    zmax_box = TextBox(plt.axes([0.9, 0.83, 0.08, 0.05]), 'zMax:', initial=str(default_zmax))


    def update6(val):
        ax.clear()

        xmin_val = float(xmin_box.text)
        xmax_val = float(xmax_box.text)
        ax.set_xlim(xmin_val, xmax_val)
        ymin_val = float(ymin_box.text)
        ymax_val = float(ymax_box.text)
        ax.set_ylim(ymin_val, ymax_val)
        zmin_val = float(zmin_box.text)
        zmax_val = float(zmax_box.text)

        # グリッド線を引く
        gt=gridtype.get()
        if gt == 0:
            #ax.set_axisbelow(True)  # グリッド線を背面に配置
            ax.grid(False)
        elif gt == 1:
            ax.grid(True)
        sa3 = sli_a3.val
        ax.text(0.1,1.1,f'{txt_ul.get()} = %.2f (r.l.u.)' %state['QU2'][sa3], transform=ax.transAxes)
        #ax.pcolormesh(QV, hwlist7, I[:,:,sa3], cmap='jet', vmin=z_min, vmax=sb3)
        if at==0:
            ax.pcolormesh(state['QV'], hwlist7, state['I'][:,:,sa3], cmap='jet', vmin=zmin_val, vmax=zmax_val)
            cbar.mappable.set_clim(vmin=zmin_val, vmax=zmax_val)  # カラーバーのレンジを更新
        elif at==1:
            if zmin_val==0:
                ax.pcolormesh(state['QV'], hwlist7, state['I'][:,:,sa3], cmap='jet', norm = LogNorm(vmin=np.nanmin(state['I'][state['I'] != 0]), vmax=zmax_val))
                cbar.mappable.set_clim(vmin=np.nanmin(state['I'][state['I'] != 0]), vmax=zmax_val)  # カラーバーのレンジを更新
            else:
                ax.pcolormesh(state['QV'], hwlist7, state['I'][:,:,sa3], cmap='jet', norm = LogNorm(vmin=zmin_val, vmax=zmax_val))
                cbar.mappable.set_clim(vmin=zmin_val, vmax=zmax_val)  # カラーバーのレンジを更新

        # 図のラベルを作成
        if float(txt12.get())==0:
            if float(txt9.get())==0:
                vl1 = str('0')
            else:
                vl1 = str("{:.3f}".format(float(txt9.get())*state['QU2'][sa3]))
        elif float(txt12.get())==1:
            if float(txt9.get())==0:
                vl1 = str(txt_vl.get())
            else:
                vl1 = str("{:.3f}".format(float(txt9.get())*state['QU2'][sa3]))+str('+')+str(txt_vl.get())
        elif float(txt12.get())==-1:
            if float(txt9.get())==0:
                vl1 = str('-')+str(txt_vl.get())
            else:
                vl1 = str("{:.3f}".format(float(txt9.get())*state['QU2'][sa3]))+str('-')+str(txt_vl.get())
        else:
            try:
                number1 = float(txt12.get())
                if number1.is_integer():#整数である
                    if number1<0:#Vベクトルの値が負であった場合
                        if float(txt9.get())==0:
                            vl1 = str("{:.3f}".format(float(txt9.get())*state['QU2'][sa3]))+str('-')+str(int(np.abs(float(txt12.get()))))+str(txt_vl.get())
                        else:
                            vl1 = str("{:.3f}".format(float(txt9.get())*state['QU2'][sa3]))+str('-')+str(int(np.abs(float(txt12.get()))))+str(txt_vl.get())
                    elif number1>0:#Vベクトルの値が正であった場合
                        if float(txt9.get())==0:
                            vl1 = str(int(float(txt12.get())))+str(txt_vl.get())
                        else:
                            vl1 = str("{:.3f}".format(float(txt9.get())*state['QU2'][sa3]))+str('+')+str(int(float(txt12.get())))+str(txt_vl.get())
                else:#整数でない
                    if number1<0:#Vベクトルの値が負であった場合
                        if float(txt9.get())==0:
                            vl1 = str('-')+str(np.abs(float(txt12.get())))+str(txt_vl.get())
                        else:
                            vl1 = str("{:.3f}".format(float(txt9.get())*state['QU2'][sa3]))+str('-')+str(np.abs(float(txt12.get())))+str(txt_vl.get())
                    elif number1>0:#Vベクトルの値が正であった場合
                        if float(txt9.get())==0:
                            vl1 = str(float(txt12.get()))+str(txt_vl.get())
                        else:
                            vl1 = str("{:.3f}".format(float(txt9.get())*state['QU2'][sa3]))+str('+')+str(float(txt12.get()))+str(txt_vl.get())
            except ValueError:#整数でない
                pass

        if float(txt13.get())==0:
            if float(txt10.get())==0:
                vl2 = str('0')
            else:
                vl2 = str("{:.3f}".format(float(txt10.get())*state['QU2'][sa3]))
        elif float(txt13.get())==1:
            if float(txt10.get())==0:
                vl2 = str(txt_vl.get())
            else:
                vl2 = str("{:.3f}".format(float(txt10.get())*state['QU2'][sa3]))+str('+')+str(txt_vl.get())
        elif float(txt13.get())==-1:
            if float(txt10.get())==0:
                vl2 = str('-')+str(txt_vl.get())
            else:
                vl2 = str("{:.3f}".format(float(txt10.get())*state['QU2'][sa3]))+str('-')+str(txt_vl.get())
        else:
            try:
                number2 = float(txt13.get())
                if number2.is_integer():#整数である
                    if number2<0:#Vベクトルの値が負であった場合
                        if float(txt10.get())==0:
                            vl2 = str("{:.3f}".format(float(txt10.get())*state['QU2'][sa3]))+str('-')+str(int(np.abs(float(txt13.get()))))+str(txt_vl.get())
                        else:
                            vl2 = str("{:.3f}".format(float(txt10.get())*state['QU2'][sa3]))+str('-')+str(int(np.abs(float(txt13.get()))))+str(txt_vl.get())
                    elif number2>0:#Vベクトルの値が正であった場合
                        if float(txt10.get())==0:
                            vl2 = str(int(float(txt13.get())))+str(txt_vl.get())
                        else:
                            vl2 = str("{:.3f}".format(float(txt10.get())*state['QU2'][sa3]))+str('+')+str(int(float(txt13.get())))+str(txt_vl.get())
                else:#整数でない
                    if number2<0:#Vベクトルの値が負であった場合
                        if float(txt10.get())==0:
                            vl2 = str('-')+str(np.abs(float(txt13.get())))+str(txt_vl.get())
                        else:
                            vl2 = str("{:.3f}".format(float(txt10.get())*state['QU2'][sa3]))+str('-')+str(np.abs(float(txt13.get())))+str(txt_vl.get())
                    elif number2>0:#Vベクトルの値が正であった場合
                        if float(txt10.get())==0:
                            vl2 = str(float(txt13.get()))+str(txt_vl.get())
                        else:
                            vl2 = str("{:.3f}".format(float(txt10.get())*state['QU2'][sa3]))+str('+')+str(float(txt13.get()))+str(txt_vl.get())
            except ValueError:#整数でない
                pass

        if float(txt14.get())==0:
            if float(txt11.get())==0:
                vl3 = str('0')
            else:
                vl3 = str("{:.3f}".format(float(txt11.get())*state['QU2'][sa3]))
        elif float(txt14.get())==1:
            if float(txt11.get())==0:
                vl3 = str(txt_vl.get())
            else:
                vl3 = str("{:.3f}".format(float(txt11.get())*state['QU2'][sa3]))+str('+')+str(txt_vl.get())
        elif float(txt14.get())==-1:
            if float(txt11.get())==0:
                vl3 = str('-')+str(txt_vl.get())
            else:
                vl3 = str("{:.3f}".format(float(txt11.get())*state['QU2'][sa3]))+str('-')+str(txt_vl.get())
        else:
            try:
                number3 = float(txt14.get())
                if number3.is_integer():#整数である
                    if number3<0:#Vベクトルの値が負であった場合
                        if float(txt11.get())==0:
                            vl3 = str("{:.3f}".format(float(txt11.get())*state['QU2'][sa3]))+str('-')+str(int(np.abs(float(txt14.get()))))+str(txt_vl.get())
                        else:
                            vl3 = str("{:.3f}".format(float(txt11.get())*state['QU2'][sa3]))+str('-')+str(int(np.abs(float(txt14.get()))))+str(txt_vl.get())
                    elif number3>0:#Vベクトルの値が正であった場合
                        if float(txt11.get())==0:
                            vl3 = str(int(float(txt14.get())))+str(txt_vl.get())
                        else:
                            vl3 = str("{:.3f}".format(float(txt11.get())*state['QU2'][sa3]))+str('+')+str(int(float(txt14.get())))+str(txt_vl.get())
                else:#整数でない
                    if number3<0:#Vベクトルの値が負であった場合
                        if float(txt11.get())==0:
                            vl3 = str('-')+str(np.abs(float(txt14.get())))+str(txt_vl.get())
                        else:
                            vl3 = str("{:.3f}".format(float(txt11.get())*state['QU2'][sa3]))+str('-')+str(np.abs(float(txt14.get())))+str(txt_vl.get())
                    elif number3>0:#Vベクトルの値が正であった場合
                        if float(txt11.get())==0:
                            vl3 = str(float(txt14.get()))+str(txt_vl.get())
                        else:
                            vl3 = str("{:.3f}".format(float(txt11.get())*state['QU2'][sa3]))+str('+')+str(float(txt14.get()))+str(txt_vl.get())
            except ValueError:#整数でない
                pass

        Vlabel3 = (f"({vl1},{vl2},{vl3})")

        ax.set_xlabel(str(Vlabel3))
        ax.set_ylabel("ℏω (meV)")
        ax.set_xlim(xmin_val,xmax_val)
        ax.set_ylim(ymin_val,ymax_val)
        plt.draw()
    # 矢印キーにスライダを対応。
    def on_key(event):
        if event.key == 'right':
            new_val_a = min(sli_a3.val + 1, sli_a3.valmax)
            sli_a3.set_val(new_val_a)
        elif event.key == 'left':
            new_val_a = max(sli_a3.val - 1, sli_a3.valmin)
            sli_a3.set_val(new_val_a)
    fig3.canvas.mpl_connect('key_press_event', on_key)
    sli_a3.on_changed(update6)

    # 最小値と最大値が変更されたときに呼び出される関数
    def update_axis_range(text):
        try:
            xmin_val = float(xmin_box.text)
            xmax_val = float(xmax_box.text)
            ax.set_xlim(xmin_val, xmax_val)
            ymin_val = float(ymin_box.text)
            ymax_val = float(ymax_box.text)
            ax.set_ylim(ymin_val, ymax_val)
            zmin_val = float(zmin_box.text)
            zmax_val = float(zmax_box.text)
            cbar.mappable.set_clim(vmin=zmin_val, vmax=zmax_val)
            fig3.canvas.draw_idle()
            update6(None)
            return xmin_val,xmax_val,ymin_val,ymax_val,zmin_val,zmax_val
        except ValueError:
            pass

    xmin_box.on_submit(update_axis_range)
    xmax_box.on_submit(update_axis_range)
    ymin_box.on_submit(update_axis_range)
    ymax_box.on_submit(update_axis_range)
    zmin_box.on_submit(update_axis_range)
    zmax_box.on_submit(update_axis_range)

    plt.show()

def constQmap_U2(env):
    axistype = env.get('axistype')
    gridtype = env.get('gridtype')
    scale_s_Emax_txt = env.get('scale_s_Emax_txt')
    scale_s_Emin_txt = env.get('scale_s_Emin_txt')
    scale_s_Imax_txt = env.get('scale_s_Imax_txt')
    scale_s_Imin_txt = env.get('scale_s_Imin_txt')
    scale_s_Umax_txt = env.get('scale_s_Umax_txt')
    scale_s_Umin_txt = env.get('scale_s_Umin_txt')
    state = env.get('state')
    txt10 = env.get('txt10')
    txt11 = env.get('txt11')
    txt12 = env.get('txt12')
    txt13 = env.get('txt13')
    txt14 = env.get('txt14')
    txt9 = env.get('txt9')
    txt_3d_ini_V = env.get('txt_3d_ini_V')
    txt_ul = env.get('txt_ul')
    txt_vl = env.get('txt_vl')
    # 初期値
    if txt_3d_ini_V.get()=="":
        sa2 = 0
    else:
        # 一番近い値を探す
        sa2 = np.abs(state['QV2'] - float(txt_3d_ini_V.get())).argmin()

    # 軸設定。空欄の場合は範囲マックスを表示するようにする
    if scale_s_Umin_txt.get()=="":
        Ulim_min=round(np.min(state['QU']),2)
    else:
        Ulim_min=float(scale_s_Umin_txt.get())
    if scale_s_Umax_txt.get()=="":
        Ulim_max=round(np.max(state['QU']),2)
    else:
        Ulim_max=float(scale_s_Umax_txt.get())

    if scale_s_Emin_txt.get()=="":
        Elim_min=round(float(state['energylist'][0]), 2)
    else:
        Elim_min=float(scale_s_Emin_txt.get())
    if scale_s_Emax_txt.get()=="":
        Elim_max=float(round(state['energylist'][-1],2))
    else:
        Elim_max=float(scale_s_Emax_txt.get())


    # カラーバースケール。空欄の場合は平均値を出力するようにする。
    if scale_s_Imin_txt.get()=="":
        if np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]) >= 0:
            z_min=0
        elif np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]) < 0:
            z_min=round(np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]),1)
    else:
        z_min=float(scale_s_Imin_txt.get())

    if scale_s_Imax_txt.get()=="":
        if np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]) >= 0:
            z_max=round(np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]),1)
        elif np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]) < 0:
            z_max=0
    else:
        z_max=float(scale_s_Imax_txt.get())

    # 変数　QU, QV2, QU2, QV2, I ,Ierr
    hw_num = int(len(state['energylist'])+1)
    hwlist8=np.zeros(hw_num)
    #hwが1つのときの例外処理として装置分解能の範囲を出力するようにする
    if hw_num==2:
        hwlist8[0] = float(state['energylist'][0]-(state['ef_tol']+0.005))
        hwlist8[1] = float(state['energylist'][-1]+(state['ef_tol']+0.005))
    else:
        hwlist8[0] = float(state['energylist'][0])-(float(state['energylist'][1])-float(state['energylist'][0]))
        hwlist8[-1] = float(state['energylist'][-1])+(float(state['energylist'][-1])-float(state['energylist'][-2]))

        #hwlist5[0] = float(energylist[0])-(float(energylist[1])-float(energylist[0]))
        #hwlist5[-1] = float(energylist[-1])+(float(energylist[-1])-float(energylist[-2]))

        for ne in range(hw_num-2):
            hwlist8[ne+1] = (float(state['energylist'][ne])+float(state['energylist'][ne+1]))/2

    #図を出力する
    #intensityの範囲
    #fig, ax = plt.figure()
    #axにカラーバーを表示
    fig2, ax = plt.subplots()
    plt.subplots_adjust(left=0.30, right=0.75, bottom=0.25)
    #im=plt.pcolormesh(QU, hwlist8, I[:,0,:], cmap='jet', vmin=z_min, vmax=z_max)
    at=axistype.get()
    # グリッド線を引く
    gt=gridtype.get()
    if gt == 0:
        #ax.set_axisbelow(True)  # グリッド線を背面に配置
        ax.grid(False)
    elif gt == 1:
        ax.grid(True)
    if at==0:
        im=plt.pcolormesh(state['QU'], hwlist8, state['I'][:,sa2,:], cmap='jet', vmin=z_min, vmax=z_max)
    elif at==1:
        if z_min==0:
            z_min=np.nanmin(state['I'][state['I'] != 0])
            im=plt.pcolormesh(state['QU'], hwlist8, state['I'][:,sa2,:], cmap='jet', norm = LogNorm(vmin=np.nanmin(state['I'][state['I'] != 0]), vmax=z_max))
        else:
            im=plt.pcolormesh(state['QU'], hwlist8, state['I'][:,sa2,:], cmap='jet', norm = LogNorm(vmin=z_min, vmax=z_max))
    #sb2=z_max#初期値を一応セット
    cbar=plt.colorbar(im,ticks=mticker.LinearLocator(numticks=3))
    # カラーバーのタイトルを設定
    cbar.set_label('Intenisty (a.u.)')
    #, cmap="jet", extend='both',ticks=np.linspace(vmin, vmax, 5)
    #plt.axis('tight')
    #横スライドでVを変更、縦スライドで強度の最大値を変更
    ax_a = plt.axes([0.3, 0.02, 0.45, 0.04]) #plt.axes([x, y, width, height] ) 
    sli_a2 = wg.Slider(ax_a, f'{txt_vl.get()}', 0, len(state['QV2'])-1, valinit=sa2,valstep=1, orientation='horizontal')
    ax.text(0.1,1.1,f'{txt_vl.get()} = %.2f (r.l.u.)' %state['QV2'][sa2], transform=ax.transAxes)
    # 図のラベルを作成
    if float(txt9.get())==0:
        if float(txt12.get())==0:
            ul1 = str('0')
        else:
            ul1 = str("{:.3f}".format(float(txt12.get()) * state['QV2'][sa2]))
    elif float(txt9.get())==1:
        if float(txt12.get())==0:
            ul1 = str(txt_ul.get())
        else:
            ul1 = str("{:.3f}".format(float(txt12.get()) * state['QV2'][sa2]))+str('+')+str(txt_ul.get())
    elif float(txt9.get())==-1:
        if float(txt12.get())==0:
            ul1 = str('-')+str(txt_ul.get())
        else:
            ul1 = str("{:.3f}".format(float(txt12.get()) * state['QV2'][sa2]))+str('-')+str(txt_ul.get())
    else:
        try:
            number1 = float(txt9.get())
            if number1.is_integer():#整数である
                if number1<0:#Vベクトルの値が負であった場合
                    if float(txt12.get())==0:
                        ul1 = str('-')+str(int(np.abs(float(txt9.get()))))+str(txt_ul.get())
                    else:
                        ul1 = str("{:.3f}".format(float(txt12.get()) * state['QV2'][sa2]))+str('-')+str(int(np.abs(float(txt9.get()))))+str(txt_ul.get())
                elif number1>0:#Vベクトルの値が正であった場合
                    if float(txt12.get())==0:
                        ul1 = str(int(float(txt9.get())))+str(txt_ul.get())
                    else:
                        ul1 = str("{:.3f}".format(float(txt12.get()) * state['QV2'][sa2]))+str('+')+str(int(float(txt9.get())))+str(txt_ul.get())
            else:#整数でない
                if number1<0:#Vベクトルの値が負であった場合
                    if float(txt12.get())==0:
                        ul1 = str('-')+str(np.abs(float(txt9.get())))+str(txt_ul.get())
                    else:
                        ul1 = str("{:.3f}".format(float(txt12.get()) * state['QV2'][sa2]))+str('-')+str(np.abs(float(txt9.get())))+str(txt_ul.get())
                elif number1>0:#Vベクトルの値が正であった場合
                    if float(txt12.get())==0:
                        ul1 = str(float(txt9.get()))+str(txt_ul.get())
                    else:
                        ul1 = str("{:.3f}".format(float(txt12.get()) * state['QV2'][sa2]))+str('+')+str(float(txt9.get()))+str(txt_ul.get())
        except ValueError:#整数でない
            pass

    if float(txt10.get())==0:
        if float(txt13.get())==0:
            ul2 = str('0')
        else:
            ul2 = str("{:.3f}".format(float(txt13.get()) * state['QV2'][sa2]))
    elif float(txt10.get())==1:
        if float(txt13.get())==0:
            ul2 = str(txt_ul.get())
        else:
            ul2 = str("{:.3f}".format(float(txt13.get()) * state['QV2'][sa2]))+str('+')+str(txt_ul.get())
    elif float(txt10.get())==-1:
        if float(txt13.get())==0:
            ul2 = str('-')+str(txt_ul.get())
        else:
            ul2 = str("{:.3f}".format(float(txt13.get()) * state['QV2'][sa2]))+str('-')+str(txt_ul.get())
    else:
        try:
            number2 = float(txt10.get())
            if number2.is_integer():#整数である
                if number2<0:#Vベクトルの値が負であった場合
                    if float(txt13.get())==0:
                        ul2 = str('-')+str(int(np.abs(float(txt10.get()))))+str(txt_ul.get())
                    else:
                        ul2 = str("{:.3f}".format(float(txt13.get()) * state['QV2'][sa2]))+str('-')+str(int(np.abs(float(txt10.get()))))+str(txt_ul.get())
                elif number2>0:#Vベクトルの値が正であった場合
                    if float(txt13.get())==0:
                        ul2 = str(int(float(txt10.get())))+str(txt_ul.get())
                    else:
                        ul2 = str("{:.3f}".format(float(txt13.get()) * state['QV2'][sa2]))+str('+')+str(int(float(txt10.get())))+str(txt_ul.get())
            else:#整数でない
                if number2<0:#Vベクトルの値が負であった場合
                    if float(txt13.get())==0:
                        ul2 = str('-')+str(np.abs(float(txt10.get())))+str(txt_ul.get())
                    else:
                        ul2 = str("{:.3f}".format(float(txt13.get()) * state['QV2'][sa2]))+str('-')+str(np.abs(float(txt10.get())))+str(txt_ul.get())
                elif number2>0:#Vベクトルの値が正であった場合
                    if float(txt13.get())==0:
                        ul2 = str(float(txt10.get()))+str(txt_ul.get())
                    else:
                        ul2 = str("{:.3f}".format(float(txt13.get()) * state['QV2'][sa2]))+str('+')+str(float(txt10.get()))+str(txt_ul.get())
        except ValueError:#整数でない
            pass

    if float(txt11.get())==0:
        if float(txt14.get())==0:
            ul3 = str('0')
        else:
            ul3 = str("{:.3f}".format(float(txt14.get()) * state['QV2'][sa2]))
    elif float(txt11.get())==1:
        if float(txt14.get())==0:
            ul3 = str(txt_ul.get())
        else:
            ul3 = str("{:.3f}".format(float(txt14.get()) * state['QV2'][sa2]))+str('+')+str(txt_ul.get())
    elif float(txt11.get())==-1:
        if float(txt14.get())==0:
            ul3 = str('-')+str(txt_ul.get())
        else:
            ul3 = str("{:.3f}".format(float(txt14.get()) * state['QV2'][sa2]))+str('-')+str(txt_ul.get())
    else:
        try:
            number3 = float(txt11.get())
            if number3.is_integer():#整数である
                if number3<0:#Vベクトルの値が負であった場合
                    if float(txt14.get())==0:
                        ul3 = str('-')+str(int(np.abs(float(txt11.get()))))+str(txt_ul.get())
                    else:
                        ul3 = str("{:.3f}".format(float(txt14.get()) * state['QV2'][sa2]))+str('-')+str(int(np.abs(float(txt11.get()))))+str(txt_ul.get())
                elif number3>0:#Vベクトルの値が正であった場合
                    if float(txt14.get())==0:
                        ul3 = str(int(float(txt11.get())))+str(txt_ul.get())
                    else:
                        ul3 = str("{:.3f}".format(float(txt14.get()) * state['QV2'][sa2]))+str('+')+str(int(float(txt11.get())))+str(txt_ul.get())
            else:#整数でない
                if number3<0:#Vベクトルの値が負であった場合
                    if float(txt14.get())==0:
                        ul3 = str('-')+str(np.abs(float(txt11.get())))+str(txt_ul.get())
                    else:
                        ul3 = str("{:.3f}".format(float(txt14.get()) * state['QV2'][sa2]))+str('-')+str(np.abs(float(txt11.get())))+str(txt_ul.get())
                elif number3>0:#Vベクトルの値が正であった場合
                    if float(txt14.get())==0:
                        ul3 = str(float(txt11.get()))+str(txt_ul.get())
                    else:
                        ul3 = str("{:.3f}".format(float(txt14.get()) * state['QV2'][sa2]))+str('+')+str(float(txt11.get()))+str(txt_ul.get())
        except ValueError:#整数でない
            pass

    Ulabel3 = (f"({ul1},{ul2},{ul3})")

    ax.set_xlabel(str(Ulabel3))
    ax.set_ylabel("ℏω (meV)")
    ax.set_xlim(Ulim_min,Ulim_max)
    ax.set_ylim(Elim_min,Elim_max)

    # グラフ内に表示範囲を決定するボックス
    # 最小値と最大値の初期値
    default_xmin = round(Ulim_min, 3)
    default_xmax = round(Ulim_max, 3)

    default_ymin = round(Elim_min, 3)
    default_ymax = round(Elim_max, 3)

    default_zmin = round(z_min, 3)
    default_zmax = round(z_max, 3)

    # テキストボックスを作成して最小値と最大値を設定
    xmin_box = TextBox(plt.axes([0.3, 0.10, 0.08, 0.05]), 'xMin:', initial=str(default_xmin))
    xmax_box = TextBox(plt.axes([0.6, 0.10, 0.08, 0.05]), 'xMax:', initial=str(default_xmax))

    ymin_box = TextBox(plt.axes([0.1, 0.2, 0.08, 0.05]), 'yMin:', initial=str(default_ymin))
    ymax_box = TextBox(plt.axes([0.1, 0.83, 0.08, 0.05]), 'yMax:', initial=str(default_ymax))

    zmin_box = TextBox(plt.axes([0.9, 0.2, 0.08, 0.05]), 'zMin:', initial=str(default_zmin))
    zmax_box = TextBox(plt.axes([0.9, 0.83, 0.08, 0.05]), 'zMax:', initial=str(default_zmax))

    def update7(val):
        ax.clear()

        xmin_val = float(xmin_box.text)
        xmax_val = float(xmax_box.text)
        ymin_val = float(ymin_box.text)
        ymax_val = float(ymax_box.text)
        zmin_val = float(zmin_box.text)
        zmax_val = float(zmax_box.text)

        # グリッド線を引く
        gt=gridtype.get()
        if gt == 0:
            #ax.set_axisbelow(True)  # グリッド線を背面に配置
            ax.grid(False)
        elif gt == 1:
            ax.grid(True)
        sa2 = sli_a2.val
        ax.text(0.1,1.1,f'{txt_vl.get()} = %.2f (r.l.u.)' %state['QV2'][sa2], transform=ax.transAxes)
        #ax.pcolormesh(QU, hwlist8, I[:,sa,:], cmap='jet', vmin=z_min, vmax=sb2)
        if at==0:
            ax.pcolormesh(state['QU'], hwlist8, state['I'][:,sa2,:], cmap='jet', vmin=zmin_val, vmax=zmax_val)
            cbar.mappable.set_clim(vmin=zmin_val, vmax=zmax_val)  # カラーバーのレンジを更新
        elif at==1:
            if zmin_val==0:
                ax.pcolormesh(state['QU'], hwlist8, state['I'][:,sa2,:], cmap='jet', norm = LogNorm(vmin=np.nanmin(state['I'][state['I'] != 0]), vmax=zmax_val))
                cbar.mappable.set_clim(vmin=np.nanmin(state['I'][state['I'] != 0]), vmax=zmax_val)  # カラーバーのレンジを更新
            else:
                ax.pcolormesh(state['QU'], hwlist8, state['I'][:,sa2,:], cmap='jet', norm = LogNorm(vmin=zmin_val, vmax=zmax_val))
                cbar.mappable.set_clim(vmin=zmin_val, vmax=zmax_val)  # カラーバーのレンジを更新

        # 図のラベルを作成
        if float(txt9.get())==0:
            if float(txt12.get())==0:
                ul1 = str('0')
            else:
                ul1 = str("{:.3f}".format(float(txt12.get()) * state['QV2'][sa2]))
        elif float(txt9.get())==1:
            if float(txt12.get())==0:
                ul1 = str(txt_ul.get())
            else:
                ul1 = str("{:.3f}".format(float(txt12.get()) * state['QV2'][sa2]))+str('+')+str(txt_ul.get())
        elif float(txt9.get())==-1:
            if float(txt12.get())==0:
                ul1 = str('-')+str(txt_ul.get())
            else:
                ul1 = str("{:.3f}".format(float(txt12.get()) * state['QV2'][sa2]))+str('-')+str(txt_ul.get())
        else:
            try:
                number1 = float(txt9.get())
                if number1.is_integer():#整数である
                    if number1<0:#Vベクトルの値が負であった場合
                        if float(txt12.get())==0:
                            ul1 = str('-')+str(int(np.abs(float(txt9.get()))))+str(txt_ul.get())
                        else:
                            ul1 = str("{:.3f}".format(float(txt12.get()) * state['QV2'][sa2]))+str('-')+str(int(np.abs(float(txt9.get()))))+str(txt_ul.get())
                    elif number1>0:#Vベクトルの値が正であった場合
                        if float(txt12.get())==0:
                            ul1 = str(int(float(txt9.get())))+str(txt_ul.get())
                        else:
                            ul1 = str("{:.3f}".format(float(txt12.get()) * state['QV2'][sa2]))+str('+')+str(int(float(txt9.get())))+str(txt_ul.get())
                else:#整数でない
                    if number1<0:#Vベクトルの値が負であった場合
                        if float(txt12.get())==0:
                            ul1 = str('-')+str(np.abs(float(txt9.get())))+str(txt_ul.get())
                        else:
                            ul1 = str("{:.3f}".format(float(txt12.get()) * state['QV2'][sa2]))+str('-')+str(np.abs(float(txt9.get())))+str(txt_ul.get())
                    elif number1>0:#Vベクトルの値が正であった場合
                        if float(txt12.get())==0:
                            ul1 = str(float(txt9.get()))+str(txt_ul.get())
                        else:
                            ul1 = str("{:.3f}".format(float(txt12.get()) * state['QV2'][sa2]))+str('+')+str(float(txt9.get()))+str(txt_ul.get())
            except ValueError:#整数でない
                pass

        if float(txt10.get())==0:
            if float(txt13.get())==0:
                ul2 = str('0')
            else:
                ul2 = str("{:.3f}".format(float(txt13.get()) * state['QV2'][sa2]))
        elif float(txt10.get())==1:
            if float(txt13.get())==0:
                ul2 = str(txt_ul.get())
            else:
                ul2 = str("{:.3f}".format(float(txt13.get()) * state['QV2'][sa2]))+str('+')+str(txt_ul.get())
        elif float(txt10.get())==-1:
            if float(txt13.get())==0:
                ul2 = str('-')+str(txt_ul.get())
            else:
                ul2 = str("{:.3f}".format(float(txt13.get()) * state['QV2'][sa2]))+str('-')+str(txt_ul.get())
        else:
            try:
                number2 = float(txt10.get())
                if number2.is_integer():#整数である
                    if number2<0:#Vベクトルの値が負であった場合
                        if float(txt13.get())==0:
                            ul2 = str('-')+str(int(np.abs(float(txt10.get()))))+str(txt_ul.get())
                        else:
                            ul2 = str("{:.3f}".format(float(txt13.get()) * state['QV2'][sa2]))+str('-')+str(int(np.abs(float(txt10.get()))))+str(txt_ul.get())
                    elif number2>0:#Vベクトルの値が正であった場合
                        if float(txt13.get())==0:
                            ul2 = str(int(float(txt10.get())))+str(txt_ul.get())
                        else:
                            ul2 = str("{:.3f}".format(float(txt13.get()) * state['QV2'][sa2]))+str('+')+str(int(float(txt10.get())))+str(txt_ul.get())
                else:#整数でない
                    if number2<0:#Vベクトルの値が負であった場合
                        if float(txt13.get())==0:
                            ul2 = str('-')+str(np.abs(float(txt10.get())))+str(txt_ul.get())
                        else:
                            ul2 = str("{:.3f}".format(float(txt13.get()) * state['QV2'][sa2]))+str('-')+str(np.abs(float(txt10.get())))+str(txt_ul.get())
                    elif number2>0:#Vベクトルの値が正であった場合
                        if float(txt13.get())==0:
                            ul2 = str(float(txt10.get()))+str(txt_ul.get())
                        else:
                            ul2 = str("{:.3f}".format(float(txt13.get()) * state['QV2'][sa2]))+str('+')+str(float(txt10.get()))+str(txt_ul.get())
            except ValueError:#整数でない
                pass

        if float(txt11.get())==0:
            if float(txt14.get())==0:
                ul3 = str('0')
            else:
                ul3 = str("{:.3f}".format(float(txt14.get()) * state['QV2'][sa2]))
        elif float(txt11.get())==1:
            if float(txt14.get())==0:
                ul3 = str(txt_ul.get())
            else:
                ul3 = str("{:.3f}".format(float(txt14.get()) * state['QV2'][sa2]))+str('+')+str(txt_ul.get())
        elif float(txt11.get())==-1:
            if float(txt14.get())==0:
                ul3 = str('-')+str(txt_ul.get())
            else:
                ul3 = str("{:.3f}".format(float(txt14.get()) * state['QV2'][sa2]))+str('-')+str(txt_ul.get())
        else:
            try:
                number3 = float(txt11.get())
                if number3.is_integer():#整数である
                    if number3<0:#Vベクトルの値が負であった場合
                        if float(txt14.get())==0:
                            ul3 = str('-')+str(int(np.abs(float(txt11.get()))))+str(txt_ul.get())
                        else:
                            ul3 = str("{:.3f}".format(float(txt14.get()) * state['QV2'][sa2]))+str('-')+str(int(np.abs(float(txt11.get()))))+str(txt_ul.get())
                    elif number3>0:#Vベクトルの値が正であった場合
                        if float(txt14.get())==0:
                            ul3 = str(int(float(txt11.get())))+str(txt_ul.get())
                        else:
                            ul3 = str("{:.3f}".format(float(txt14.get()) * state['QV2'][sa2]))+str('+')+str(int(float(txt11.get())))+str(txt_ul.get())
                else:#整数でない
                    if number3<0:#Vベクトルの値が負であった場合
                        if float(txt14.get())==0:
                            ul3 = str('-')+str(np.abs(float(txt11.get())))+str(txt_ul.get())
                        else:
                            ul3 = str("{:.3f}".format(float(txt14.get()) * state['QV2'][sa2]))+str('-')+str(np.abs(float(txt11.get())))+str(txt_ul.get())
                    elif number3>0:#Vベクトルの値が正であった場合
                        if float(txt14.get())==0:
                            ul3 = str(float(txt11.get()))+str(txt_ul.get())
                        else:
                            ul3 = str("{:.3f}".format(float(txt14.get()) * state['QV2'][sa2]))+str('+')+str(float(txt11.get()))+str(txt_ul.get())
            except ValueError:#整数でない
                pass

        Ulabel3 = (f"({ul1},{ul2},{ul3})")
        ax.set_xlabel(str(Ulabel3))
        ax.set_ylabel("ℏω (meV)")
        ax.set_xlim(xmin_val,xmax_val)
        ax.set_ylim(ymin_val,ymax_val)
        #cbar.mappable.set_clim(vmin=z_min, vmax=sb2)  # カラーバーのレンジを更新
        plt.draw()
    # 矢印キーにスライダを対応。
    def on_key(event):
        if event.key == 'right':
            new_val_a = min(sli_a2.val + 1, sli_a2.valmax)
            sli_a2.set_val(new_val_a)
        elif event.key == 'left':
            new_val_a = max(sli_a2.val - 1, sli_a2.valmin)
            sli_a2.set_val(new_val_a)
    fig2.canvas.mpl_connect('key_press_event', on_key)
    sli_a2.on_changed(update7)

    # 最小値と最大値が変更されたときに呼び出される関数
    def update_axis_range(text):
        try:
            xmin_val = float(xmin_box.text)
            xmax_val = float(xmax_box.text)
            ax.set_xlim(xmin_val, xmax_val)
            ymin_val = float(ymin_box.text)
            ymax_val = float(ymax_box.text)
            ax.set_ylim(ymin_val, ymax_val)
            zmin_val = float(zmin_box.text)
            zmax_val = float(zmax_box.text)
            cbar.mappable.set_clim(vmin=zmin_val, vmax=zmax_val)
            fig2.canvas.draw_idle()
            update7(None)
            return xmin_val,xmax_val,ymin_val,ymax_val,zmin_val,zmax_val
        except ValueError:
            pass

    xmin_box.on_submit(update_axis_range)
    xmax_box.on_submit(update_axis_range)
    ymin_box.on_submit(update_axis_range)
    ymax_box.on_submit(update_axis_range)
    zmin_box.on_submit(update_axis_range)
    zmax_box.on_submit(update_axis_range)

    plt.show()

def constEmap(env):
    axistype = env.get('axistype')
    gridtype = env.get('gridtype')
    scale_s_Imax_txt = env.get('scale_s_Imax_txt')
    scale_s_Imin_txt = env.get('scale_s_Imin_txt')
    scale_s_Umax_txt = env.get('scale_s_Umax_txt')
    scale_s_Umin_txt = env.get('scale_s_Umin_txt')
    scale_s_Vmax_txt = env.get('scale_s_Vmax_txt')
    scale_s_Vmin_txt = env.get('scale_s_Vmin_txt')
    state = env.get('state')
    txt10 = env.get('txt10')
    txt11 = env.get('txt11')
    txt12 = env.get('txt12')
    txt13 = env.get('txt13')
    txt14 = env.get('txt14')
    txt9 = env.get('txt9')
    txt_2d_1e = env.get('txt_2d_1e')
    txt_2d_2e = env.get('txt_2d_2e')
    # 軸設定。空欄の場合は範囲マックスを表示するようにする
    if scale_s_Umin_txt.get()=="":
        Ulim_min=round(np.min(state['QU']),2)
    else:
        Ulim_min=float(scale_s_Umin_txt.get())
    if scale_s_Umax_txt.get()=="":
        Ulim_max=round(np.max(state['QU']),2)
    else:
        Ulim_max=float(scale_s_Umax_txt.get())

    if scale_s_Vmin_txt.get()=="":
        Vlim_min=round(np.min(state['QV']),2)
    else:
        Vlim_min=float(scale_s_Vmin_txt.get())
    if scale_s_Vmax_txt.get()=="":
        Vlim_max=round(np.max(state['QV']),2)
    else:
        Vlim_max=float(scale_s_Vmax_txt.get())

    # カラーバースケール。空欄の場合は平均値を出力するようにする。
    if scale_s_Imin_txt.get()=="":
        if np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]) >= 0:
            z_min=0
        elif np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]) < 0:
            z_min=round(np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]),1)
    else:
        z_min=float(scale_s_Imin_txt.get())

    if scale_s_Imax_txt.get()=="":
        if np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]) >= 0:
            z_max=round(np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]),1)
        elif np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]) < 0:
            z_max=0
    else:
        z_max=float(scale_s_Imax_txt.get())

    Ind_e = None
    hwlist1 = None
    Ec=float(txt_2d_1e.get())
    Epm=float(txt_2d_2e.get())
    if Epm < 0:
        return

    hwlist1=np.zeros(len(state['energylist']))
    for ne in range(len(state['energylist'])):
        hwlist1[ne] = float(state['energylist'][ne])

    # 条件を満たすエネルギーの面を指定
    if Epm==0:
        Ind_e = [np.abs(hwlist1 - Ec).argmin()]
    else:
        ind_e = list(zip(*np.where(( Ec - Epm <=  hwlist1 ) & (  hwlist1 <= Ec + Epm ))))
        Ind_e = list(np.ravel(ind_e))

    # ないリストを参照すると、次のグラフ表示の時、空白のグラフができる。これを回避するためにリストが空の時はグラフ表示しない分岐を作成
    if len(Ind_e)!=0:
        # shared variables are stored in state
        # 旧コード
        #I_ce = np.nanmean(I[ind_e],axis=0)
        #Ierr_ce = ((np.nansum(Ierr[ind_e]*Ierr[ind_e],axis=0))**(1/2))/len(ind_e)

        # 強度はNan値を省いて足し、Nan値を省いた値の個数で割る。誤差に関してはNan値を省いて２乗和を取り、平方根を取ってから、NaN値を省いた値の個数で割る
        state['I_ce']=np.zeros((len(state['QV'])-1,len(state['QU'])-1))
        state['Ierr_ce']=np.zeros((len(state['QV'])-1,len(state['QU'])-1))

        #I[ll,nn,mm]=I[hw,V,U]の順番でリスト

        for nn in range(len(state['QV'])-1):
            for mm in range(len(state['QU'])-1):
                n_nanind = (list(zip(*np.where(~np.isnan(state['I'][Ind_e,nn,mm])))))
                N_nanind = list(np.ravel(n_nanind)[::1])
                if N_nanind:
                    state['I_ce'][nn,mm] = np.nansum(state['I'][Ind_e,nn,mm])/(len(N_nanind))
                    state['Ierr_ce'][nn,mm] = ((np.nansum(np.multiply(state['Ierr'][Ind_e,nn,mm],state['Ierr'][Ind_e,nn,mm])))**(1/2))/(len(N_nanind))
                else:
                    state['I_ce'][nn,mm] = np.nan
                    state['Ierr_ce'][nn,mm] = np.nan

        #図を出力する
        #intensityの範囲
        #fig, ax = plt.figure()
        #axにカラーバーを表示
        fig4, ax = plt.subplots()
        #plt.subplots_adjust(left=0.15, bottom=0.2)
        plt.subplots_adjust(left=0.30, right=0.75, bottom=0.2)  # マージンを調整してグラフを中央に配置
        # アスペクト比を変更
        ax.set_aspect(state['NV1']/state['NU1'])
        # グリッド線を引く
        gt=gridtype.get()
        if gt == 0:
            #ax.set_axisbelow(True)  # グリッド線を背面に配置
            ax.grid(False)
        elif gt == 1:
            ax.grid(True)
        #im=plt.pcolormesh(QU, QV, I_ce, cmap='jet', vmin=z_min, vmax=z_max)
        at=axistype.get()
        if at==0:
            im=plt.pcolormesh(state['QU'], state['QV'], state['I_ce'], cmap='jet', vmin=z_min, vmax=z_max)

        elif at==1:
            if z_min==0:
                z_min=np.nanmin(state['I'][state['I'] != 0])
                im=plt.pcolormesh(state['QU'], state['QV'], state['I_ce'], cmap='jet', norm = LogNorm(vmin=np.nanmin(state['I'][state['I'] != 0]), vmax=z_max))
            else:
                im=plt.pcolormesh(state['QU'], state['QV'], state['I_ce'], cmap='jet', norm = LogNorm(vmin=z_min, vmax=z_max))
        #sb4=z_max#初期値を一応セット
        cbar=plt.colorbar(im,ticks=mticker.LinearLocator(numticks=3))
        # カラーバーのタイトルを設定
        cbar.set_label('Intenisty (a.u.)')
        ax.text(0.1,1.1,f'ℏω = %.3f ± %.3f meV' %(Ec,Epm), transform=ax.transAxes)
        ax.set_xlabel(str(state['Ulabel']))
        ax.set_ylabel(str(state['Vlabel']))
        ax.set_xlim(Ulim_min,Ulim_max)
        ax.set_ylim(Vlim_min,Vlim_max)
        #, cmap="jet", extend='both',ticks=np.linspace(vmin, vmax, 5)
        #plt.axis('tight')

        # shared variables are stored in state
        state['Erange_2d_VvsU'] = [Ec - Epm,Ec + Epm]
        state['Urange_2d_VvsU'] = [float(txt9.get())*state['QU2'],float(txt10.get())*state['QU2'],float(txt11.get())*state['QU2']]
        state['Vrange_2d_VvsU'] = [float(txt12.get())*state['QV2'],float(txt13.get())*state['QV2'],float(txt14.get())*state['QV2']]

        # グラフ内に表示範囲を決定するボックス
        # 最小値と最大値の初期値
        default_xmin = round(Ulim_min, 3)
        default_xmax = round(Ulim_max, 3)

        default_ymin = round(Vlim_min, 3)
        default_ymax = round(Vlim_max, 3)

        default_zmin = round(z_min, 3)
        default_zmax = round(z_max, 3)

        # テキストボックスを作成して最小値と最大値を設定
        xmin_box = TextBox(plt.axes([0.3, 0.02, 0.08, 0.05]), 'xMin:', initial=str(default_xmin))
        xmax_box = TextBox(plt.axes([0.6, 0.02, 0.08, 0.05]), 'xMax:', initial=str(default_xmax))

        ymin_box = TextBox(plt.axes([0.1, 0.2, 0.08, 0.05]), 'yMin:', initial=str(default_ymin))
        ymax_box = TextBox(plt.axes([0.1, 0.83, 0.08, 0.05]), 'yMax:', initial=str(default_ymax))

        zmin_box = TextBox(plt.axes([0.9, 0.2, 0.08, 0.05]), 'zMin:', initial=str(default_zmin))
        zmax_box = TextBox(plt.axes([0.9, 0.83, 0.08, 0.05]), 'zMax:', initial=str(default_zmax))

        # 最小値と最大値が変更されたときに呼び出される関数
        def update_axis_range(text):
            try:
                xmin_val = float(xmin_box.text)
                xmax_val = float(xmax_box.text)
                ax.set_xlim(xmin_val, xmax_val)
                ymin_val = float(ymin_box.text)
                ymax_val = float(ymax_box.text)
                ax.set_ylim(ymin_val, ymax_val)
                zmin_val = float(zmin_box.text)
                zmax_val = float(zmax_box.text)
                cbar.mappable.set_clim(vmin=zmin_val, vmax=zmax_val)
                fig4.canvas.draw_idle()
            except ValueError:
                pass

        xmin_box.on_submit(update_axis_range)
        xmax_box.on_submit(update_axis_range)
        ymin_box.on_submit(update_axis_range)
        ymax_box.on_submit(update_axis_range)
        zmin_box.on_submit(update_axis_range)
        zmax_box.on_submit(update_axis_range)

        plt.show()
    else:
        pass     

def constQmap_V(env):
    axistype = env.get('axistype')
    gridtype = env.get('gridtype')
    scale_s_Emax_txt = env.get('scale_s_Emax_txt')
    scale_s_Emin_txt = env.get('scale_s_Emin_txt')
    scale_s_Imax_txt = env.get('scale_s_Imax_txt')
    scale_s_Imin_txt = env.get('scale_s_Imin_txt')
    scale_s_Vmax_txt = env.get('scale_s_Vmax_txt')
    scale_s_Vmin_txt = env.get('scale_s_Vmin_txt')
    state = env.get('state')
    txt10 = env.get('txt10')
    txt11 = env.get('txt11')
    txt12 = env.get('txt12')
    txt13 = env.get('txt13')
    txt14 = env.get('txt14')
    txt9 = env.get('txt9')
    txt_2d_1v = env.get('txt_2d_1v')
    txt_2d_2v = env.get('txt_2d_2v')
    txt_ul = env.get('txt_ul')
    txt_vl = env.get('txt_vl')
    # 軸設定。空欄の場合は範囲マックスを表示するようにする
    if scale_s_Vmin_txt.get()=="":
        Vlim_min=round(np.min(state['QV']),2)
    else:
        Vlim_min=float(scale_s_Vmin_txt.get())
    if scale_s_Vmax_txt.get()=="":
        Vlim_max=round(np.max(state['QV']),2)
    else:
        Vlim_max=float(scale_s_Vmax_txt.get())

    if scale_s_Emin_txt.get()=="":
        Elim_min=round(float(state['energylist'][0]), 2)
    else:
        Elim_min=float(scale_s_Emin_txt.get())
    if scale_s_Emax_txt.get()=="":
        Elim_max=float(round(state['energylist'][-1],2))
    else:
        Elim_max=float(scale_s_Emax_txt.get())

    # カラーバースケール。空欄の場合は平均値を出力するようにする。
    if scale_s_Imin_txt.get()=="":
        if np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]) >= 0:
            z_min=0
        elif np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]) < 0:
            z_min=round(np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]),1)
    else:
        z_min=float(scale_s_Imin_txt.get())

    if scale_s_Imax_txt.get()=="":
        if np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]) >= 0:
            z_max=round(np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]),1)
        elif np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]) < 0:
            z_max=0
    else:
        z_max=float(scale_s_Imax_txt.get())

    Uc=float(txt_2d_1v.get())
    Upm=float(txt_2d_2v.get())
    # 変数　QU, QV, QU2, QV2, I ,Ierr
    hw_num = int(len(state['energylist'])+1)
    # shared variables are stored in state
    state['hwlist4']=np.zeros(hw_num)
    #hwが1つのときの例外処理として装置分解能の範囲を出力するようにする
    if hw_num==2:
        state['hwlist4'][0] = float(state['energylist'][0]-(state['ef_tol']+0.005))
        state['hwlist4'][1] = float(state['energylist'][-1]+(state['ef_tol']+0.005))
    else:
        state['hwlist4'][0] = float(state['energylist'][0])-(float(state['energylist'][1])-float(state['energylist'][0]))
        state['hwlist4'][-1] = float(state['energylist'][-1])+(float(state['energylist'][-1])-float(state['energylist'][-2]))
        for ne in range(hw_num-2):
            state['hwlist4'][ne+1] = (float(state['energylist'][ne])+float(state['energylist'][ne+1]))/2
    if Upm==0:
        Ind_cQV = [np.abs(state['QU2'] - Uc).argmin()]
    else:
        ind_cQV = list(zip(*np.where((Uc - Upm <= state['QU2'] ) & (state['QU2'] <= Uc + Upm))))
        Ind_cQV = list(np.ravel(ind_cQV))
    # ないリストを参照すると、次のグラフ表示の時、空白のグラフができる。これを回避するためにリストが空の時はグラフ表示しない分岐を作成
    if len(Ind_cQV)!=0:
        # shared variables are stored in state
        #I_hwV = np.nanmean(I[:,:,ind_cQV],axis = 2)
        #Ierr_hwV = ((np.nansum(Ierr[:,:,ind_cQV]*Ierr[:,:,ind_cQV],axis = 2))**(1/2))/len(ind_cQV)

        # 強度はNan値を省いて足し、Nan値を省いた値の個数で割る。誤差に関してはNan値を省いて２乗和を取り、平方根を取ってから、NaN値を省いた値の個数で割る
        state['I_hwV']=np.zeros((len(state['energylist']),len(state['QV'])-1))
        state['Ierr_hwV']=np.zeros((len(state['energylist']),len(state['QV'])-1))
        for ll in range(len(state['energylist'])):
            for nn in range(len(state['QV'])-1):
                n_nanind = (list(zip(*np.where(~np.isnan(state['I'][ll,nn,Ind_cQV])))))
                N_nanind = list(np.ravel(n_nanind)[::1])
                if N_nanind:
                    state['I_hwV'][ll,nn] = np.nansum(state['I'][ll,nn,Ind_cQV])/(len(N_nanind))     
                    state['Ierr_hwV'][ll,nn] = ((np.nansum(np.multiply(state['Ierr'][ll,nn,Ind_cQV],state['Ierr'][ll,nn,Ind_cQV])))**(1/2))/(len(N_nanind))
                else:
                    state['I_hwV'][ll,nn] = np.nan
                    state['Ierr_hwV'][ll,nn] = np.nan

        # 図のラベルを作成
        if float(txt12.get())==0:
            if float(txt9.get())==0:
                vl1 = str('0')
            else:
                vl1 = str(float(txt9.get())*Uc)
        elif float(txt12.get())==1:
            if float(txt9.get())==0:
                vl1 = str(txt_vl.get())
            else:
                vl1 = str(float(txt9.get())*Uc)+str('+')+str(txt_vl.get())
        elif float(txt12.get())==-1:
            if float(txt9.get())==0:
                vl1 = str('-')+str(txt_vl.get())
            else:
                vl1 = str(float(txt9.get())*Uc)+str('-')+str(txt_vl.get())
        else:
            try:
                number1 = float(txt12.get())
                if number1.is_integer():#整数である
                    if number1<0:#Vベクトルの値が負であった場合
                        if float(txt9.get())==0:
                            vl1 = str('-')+str(int(np.abs(float(txt12.get()))))+str(txt_vl.get())
                        else:
                            vl1 = str(float(txt9.get())*Uc)+str('-')+str(int(np.abs(float(txt12.get()))))+str(txt_vl.get())
                    elif number1>0:#Vベクトルの値が正であった場合
                        if float(txt9.get())==0:
                            vl1 = str(int(float(txt12.get())))+str(txt_vl.get())
                        else:
                            vl1 = str(float(txt9.get())*Uc)+str('+')+str(int(float(txt12.get())))+str(txt_vl.get())
                else:#整数でない
                    if number1<0:#Vベクトルの値が負であった場合
                        if float(txt9.get())==0:
                            vl1 = str('-')+str(np.abs(float(txt12.get())))+str(txt_vl.get())
                        else:
                            vl1 = str(float(txt9.get())*Uc)+str('-')+str(np.abs(float(txt12.get())))+str(txt_vl.get())
                    elif number1>0:#Vベクトルの値が正であった場合
                        if float(txt9.get())==0:
                            vl1 = str(float(txt12.get()))+str(txt_vl.get())
                        else:
                            vl1 = str(float(txt9.get())*Uc)+str('+')+str(float(txt12.get()))+str(txt_vl.get())
            except ValueError:#整数でない
                pass

        if float(txt13.get())==0:
            if float(txt10.get())==0:
                vl2 = str('0')
            else:
                vl2 = str(float(txt10.get())*Uc)
        elif float(txt13.get())==1:
            if float(txt10.get())==0:
                vl2 = str(txt_vl.get())
            else:
                vl2 = str(float(txt10.get())*Uc)+str('+')+str(txt_vl.get())
        elif float(txt13.get())==-1:
            if float(txt10.get())==0:
                vl2 = str('-')+str(txt_vl.get())
            else:
                vl2 = str(float(txt10.get())*Uc)+str('-')+str(txt_vl.get())
        else:
            try:
                number2 = float(txt13.get())
                if number2.is_integer():#整数である
                    if number2<0:#Vベクトルの値が負であった場合
                        if float(txt10.get())==0:
                            vl2 = str('-')+str(int(np.abs(float(txt13.get()))))+str(txt_vl.get())
                        else:
                            vl2 = str(float(txt10.get())*Uc)+str('-')+str(int(np.abs(float(txt13.get()))))+str(txt_vl.get())
                    elif number2>0:#Vベクトルの値が正であった場合
                        if float(txt10.get())==0:
                            vl2 = str(int(float(txt13.get())))+str(txt_vl.get())
                        else:
                            vl2 = str(float(txt10.get())*Uc)+str('+')+str(int(float(txt13.get())))+str(txt_vl.get())
                else:#整数でない
                    if number2<0:#Vベクトルの値が負であった場合
                        if float(txt10.get())==0:
                            vl2 = str('-')+str(np.abs(float(txt13.get())))+str(txt_vl.get())
                        else:
                            vl2 = str(float(txt10.get())*Uc)+str('-')+str(np.abs(float(txt13.get())))+str(txt_vl.get())
                    elif number2>0:#Vベクトルの値が正であった場合
                        if float(txt10.get())==0:
                            vl2 = str(float(txt13.get()))+str(txt_vl.get())
                        else:
                            vl2 = str(float(txt10.get())*Uc)+str('+')+str(float(txt13.get()))+str(txt_vl.get())
            except ValueError:#整数でない
                pass

        if float(txt14.get())==0:
            if float(txt11.get())==0:
                vl3 = str('0')
            else:
                vl3 = str(float(txt11.get())*Uc)
        elif float(txt14.get())==1:
            if float(txt11.get())==0:
                vl3 = str(txt_vl.get())
            else:
                vl3 = str(float(txt11.get())*Uc)+str('+')+str(txt_vl.get())
        elif float(txt14.get())==-1:
            if float(txt11.get())==0:
                vl3 = str('-')+str(txt_vl.get())
            else:
                vl3 = str(float(txt11.get())*Uc)+str('-')+str(txt_vl.get())
        else:
            try:
                number3 = float(txt14.get())
                if number3.is_integer():#整数である
                    if number3<0:#Vベクトルの値が負であった場合
                        if float(txt11.get())==0:
                            vl3 = str('-')+str(int(np.abs(float(txt14.get()))))+str(txt_vl.get())
                        else:
                            vl3 = str(float(txt11.get())*Uc)+str('-')+str(int(np.abs(float(txt14.get()))))+str(txt_vl.get())
                    elif number3>0:#Vベクトルの値が正であった場合
                        if float(txt11.get())==0:
                            vl3 = str(int(float(txt14.get())))+str(txt_vl.get())
                        else:
                            vl3 = str(float(txt11.get())*Uc)+str('+')+str(int(float(txt14.get())))+str(txt_vl.get())
                else:#整数でない
                    if number3<0:#Vベクトルの値が負であった場合
                        if float(txt11.get())==0:
                            vl3 = str('-')+str(np.abs(float(txt14.get())))+str(txt_vl.get())
                        else:
                            vl3 = str(float(txt11.get())*Uc)+str('-')+str(np.abs(float(txt14.get())))+str(txt_vl.get())
                    elif number3>0:#Vベクトルの値が正であった場合
                        if float(txt11.get())==0:
                            vl3 = str(float(txt14.get()))+str(txt_vl.get())
                        else:
                            vl3 = str(float(txt11.get())*Uc)+str('+')+str(float(txt14.get()))+str(txt_vl.get())
            except ValueError:#整数でない
                pass

        Vlabel2 = (f"({vl1},{vl2},{vl3})")

        #図を出力する
        #intensityの範囲
        fig5=plt.figure()
        fig5.subplots_adjust(left=0.30, right=0.75, bottom=0.2)
        ax = fig5.add_subplot(111)
        ax.set_xlabel(str(Vlabel2))
        ax.set_ylabel("ℏω (meV)")
        ax.set_xlim(Vlim_min,Vlim_max)
        ax.set_ylim(Elim_min,Elim_max)
        #im=plt.pcolormesh(QV, hwlist4, I_hwV, cmap='jet', vmin=z_min, vmax=z_max)
        at=axistype.get()
        # グリッド線を引く
        gt=gridtype.get()
        if gt == 0:
            #ax.set_axisbelow(True)  # グリッド線を背面に配置
            ax.grid(False)
        elif gt == 1:
            ax.grid(True)
        if at==0:
            im=plt.pcolormesh(state['QV'], state['hwlist4'], state['I_hwV'], cmap='jet', vmin=z_min, vmax=z_max)
        elif at==1:
            if z_min==0:
                z_min=np.nanmin(state['I'][state['I'] != 0])
                im=plt.pcolormesh(state['QV'], state['hwlist4'], state['I_hwV'], cmap='jet', norm = LogNorm(vmin=np.nanmin(state['I'][state['I'] != 0]), vmax=z_max))
            else:
                im=plt.pcolormesh(state['QV'], state['hwlist4'], state['I_hwV'], cmap='jet', norm = LogNorm(vmin=z_min, vmax=z_max))
        cbar=plt.colorbar(im,ticks=mticker.LinearLocator(numticks=3))
        # カラーバーのタイトルを設定
        cbar.set_label('Intenisty (a.u.)')
        ax.text(0.1,1.1,f'{txt_ul.get()} = %.3f ± %.3f (r.l.u.)' %(Uc,Upm), transform=ax.transAxes)

        # shared variables are stored in state
        state['Erange_2d_VvsE'] = state['energylist']
        state['Urange_2d_VvsE'] = [[float(txt9.get())*(Uc - Upm),float(txt9.get())*(Uc + Upm)],[float(txt10.get())*(Uc - Upm),float(txt10.get())*(Uc + Upm)],[float(txt11.get())*(Uc - Upm),float(txt11.get())*(Uc + Upm)]]
        state['Vrange_2d_VvsE'] = [float(txt12.get())*state['QV2'],float(txt13.get())*state['QV2'],float(txt14.get())*state['QV2']]

        # グラフ内に表示範囲を決定するボックス
        # 最小値と最大値の初期値
        default_xmin = round(Vlim_min, 3)
        default_xmax = round(Vlim_max, 3)

        default_ymin = round(Elim_min, 3)
        default_ymax = round(Elim_max, 3)

        default_zmin = round(z_min, 3)
        default_zmax = round(z_max, 3)

        # テキストボックスを作成して最小値と最大値を設定
        xmin_box = TextBox(plt.axes([0.3, 0.02, 0.08, 0.05]), 'xMin:', initial=str(default_xmin))
        xmax_box = TextBox(plt.axes([0.6, 0.02, 0.08, 0.05]), 'xMax:', initial=str(default_xmax))

        ymin_box = TextBox(plt.axes([0.1, 0.2, 0.08, 0.05]), 'yMin:', initial=str(default_ymin))
        ymax_box = TextBox(plt.axes([0.1, 0.83, 0.08, 0.05]), 'yMax:', initial=str(default_ymax))

        zmin_box = TextBox(plt.axes([0.9, 0.2, 0.08, 0.05]), 'zMin:', initial=str(default_zmin))
        zmax_box = TextBox(plt.axes([0.9, 0.83, 0.08, 0.05]), 'zMax:', initial=str(default_zmax))

        # 最小値と最大値が変更されたときに呼び出される関数
        def update_axis_range(text):
            try:
                xmin_val = float(xmin_box.text)
                xmax_val = float(xmax_box.text)
                ax.set_xlim(xmin_val, xmax_val)
                ymin_val = float(ymin_box.text)
                ymax_val = float(ymax_box.text)
                ax.set_ylim(ymin_val, ymax_val)
                zmin_val = float(zmin_box.text)
                zmax_val = float(zmax_box.text)
                cbar.mappable.set_clim(vmin=zmin_val, vmax=zmax_val)
                fig5.canvas.draw_idle()
            except ValueError:
                pass

        xmin_box.on_submit(update_axis_range)
        xmax_box.on_submit(update_axis_range)
        ymin_box.on_submit(update_axis_range)
        ymax_box.on_submit(update_axis_range)
        zmin_box.on_submit(update_axis_range)
        zmax_box.on_submit(update_axis_range)

        plt.show()

    else:
        # 何もしない
        pass

def constQmap_U(env):
    axistype = env.get('axistype')
    gridtype = env.get('gridtype')
    scale_s_Emax_txt = env.get('scale_s_Emax_txt')
    scale_s_Emin_txt = env.get('scale_s_Emin_txt')
    scale_s_Imax_txt = env.get('scale_s_Imax_txt')
    scale_s_Imin_txt = env.get('scale_s_Imin_txt')
    scale_s_Umax_txt = env.get('scale_s_Umax_txt')
    scale_s_Umin_txt = env.get('scale_s_Umin_txt')
    state = env.get('state')
    txt10 = env.get('txt10')
    txt11 = env.get('txt11')
    txt12 = env.get('txt12')
    txt13 = env.get('txt13')
    txt14 = env.get('txt14')
    txt9 = env.get('txt9')
    txt_2d_1u = env.get('txt_2d_1u')
    txt_2d_2u = env.get('txt_2d_2u')
    txt_ul = env.get('txt_ul')
    txt_vl = env.get('txt_vl')
    # 軸設定。空欄の場合は範囲マックスを表示するようにする
    if scale_s_Umin_txt.get()=="":
        Ulim_min=round(np.min(state['QU']),2)
    else:
        Ulim_min=float(scale_s_Umin_txt.get())
    if scale_s_Umax_txt.get()=="":
        Ulim_max=round(np.max(state['QU']),2)
    else:
        Ulim_max=float(scale_s_Umax_txt.get())

    if scale_s_Emin_txt.get()=="":
        Elim_min=round(float(state['energylist'][0]), 2)
    else:
        Elim_min=float(scale_s_Emin_txt.get())
    if scale_s_Emax_txt.get()=="":
        Elim_max=float(round(state['energylist'][-1],2))
    else:
        Elim_max=float(scale_s_Emax_txt.get())


    # カラーバースケール。空欄の場合は平均値を出力するようにする。
    if scale_s_Imin_txt.get()=="":
        if np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]) >= 0:
            z_min=0
        elif np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]) < 0:
            z_min=round(np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]),1)
    else:
        z_min=float(scale_s_Imin_txt.get())

    if scale_s_Imax_txt.get()=="":
        if np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]) >= 0:
            z_max=round(np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]),1)
        elif np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]) < 0:
            z_max=0
    else:
        z_max=float(scale_s_Imax_txt.get())

    Vc=float(txt_2d_1u.get())
    Vpm=float(txt_2d_2u.get())
    # 変数　QU, QV, QU2, QV2, I ,Ierr
    hw_num = int(len(state['energylist'])+1)
    # shared variables are stored in state
    state['hwlist5']=np.zeros(hw_num)
    #hwが1つのときの例外処理として装置分解能の範囲を出力するようにする
    if hw_num==2:
        state['hwlist5'][0] = float(state['energylist'][0]-(state['ef_tol']+0.005))
        state['hwlist5'][1] = float(state['energylist'][-1]+(state['ef_tol']+0.005))
    else:
        state['hwlist5'][0] = float(state['energylist'][0])-(float(state['energylist'][1])-float(state['energylist'][0]))
        state['hwlist5'][-1] = float(state['energylist'][-1])+(float(state['energylist'][-1])-float(state['energylist'][-2]))

        #hwlist4[0] = float(energylist[0])-(float(energylist[1])-float(energylist[0]))
        #hwlist4[-1] = float(energylist[-1])+(float(energylist[-1])-float(energylist[-2]))

        for ne in range(hw_num-2):
            state['hwlist5'][ne+1] = (float(state['energylist'][ne])+float(state['energylist'][ne+1]))/2
    if Vpm==0:
        Ind_cQU = [np.abs(state['QV2'] - Vc).argmin()]
    else:
        ind_cQU = list(zip(*np.where((Vc - Vpm <= state['QV2'] ) & (state['QV2'] <= Vc + Vpm))))
        Ind_cQU = list(np.ravel(ind_cQU))
    # ないリストを参照すると、次のグラフ表示の時、空白のグラフができる。これを回避するためにリストが空の時はグラフ表示しない分岐を作成
    if len(Ind_cQU)!=0:
        # shared variables are stored in state
        #I_hwU = np.nanmean(I[:,ind_cQU,:],axis = 1)
        #Ierr_hwU = ((np.nansum(Ierr[:,ind_cQU,:]*Ierr[:,ind_cQU,:],axis = 1))**(1/2))/len(ind_cQU)

        # 強度はNan値を省いて足し、Nan値を省いた値の個数で割る。誤差に関してはNan値を省いて２乗和を取り、平方根を取ってから、NaN値を省いた値の個数で割る
        state['I_hwU']=np.zeros((len(state['energylist']),len(state['QU'])-1))
        state['Ierr_hwU']=np.zeros((len(state['energylist']),len(state['QU'])-1))
        for ll in range(len(state['energylist'])):
            for mm in range(len(state['QU'])-1):
                n_nanind = (list(zip(*np.where(~np.isnan(state['I'][ll,Ind_cQU,mm])))))
                N_nanind = list(np.ravel(n_nanind)[::1])
                if N_nanind:
                    state['I_hwU'][ll,mm] = np.nansum(state['I'][ll,Ind_cQU,mm])/(len(N_nanind))   
                    state['Ierr_hwU'][ll,mm] = ((np.nansum(np.multiply(state['Ierr'][ll,Ind_cQU,mm],state['Ierr'][ll,Ind_cQU,mm])))**(1/2))/(len(N_nanind))
                else:
                    state['I_hwU'][ll,mm] = np.nan
                    state['Ierr_hwU'][ll,mm] = np.nan

        # 図のラベルを作成
        if float(txt9.get())==0:
            if float(txt12.get())==0:
                ul1 = str('0')
            else:
                ul1 = str(float(txt12.get())*Vc)
        elif float(txt9.get())==1:
            if float(txt12.get())==0:
                ul1 = str(txt_ul.get())
            else:
                ul1 = str(float(txt12.get())*Vc)+str('+')+str(txt_ul.get())
        elif float(txt9.get())==-1:
            if float(txt12.get())==0:
                ul1 = str('-')+str(txt_ul.get())
            else:
                ul1 = str(float(txt12.get())*Vc)+str('-')+str(txt_ul.get())
        else:
            try:
                number1 = float(txt9.get())
                if number1.is_integer():#整数である
                    if number1<0:#Vベクトルの値が負であった場合
                        if float(txt12.get())==0:
                            ul1 = str('-')+str(int(np.abs(float(txt9.get()))))+str(txt_ul.get())
                        else:
                            ul1 = str(float(txt12.get())*Vc)+str('-')+str(int(np.abs(float(txt9.get()))))+str(txt_ul.get())
                    elif number1>0:#Vベクトルの値が正であった場合
                        if float(txt12.get())==0:
                            ul1 = str(int(np.abs(float(txt9.get()))))+str(txt_ul.get())
                        else:
                            ul1 = str(float(txt12.get())*Vc)+str('+')+str(int(float(txt9.get())))+str(txt_ul.get())
                else:#整数でない
                    if number1<0:#Vベクトルの値が負であった場合
                        if float(txt12.get())==0:
                            ul1 = str('-')+str(np.abs(float(txt9.get())))+str(txt_ul.get())
                        else:
                            ul1 = str(float(txt12.get())*Vc)+str('-')+str(np.abs(float(txt9.get())))+str(txt_ul.get())
                    elif number1>0:#Vベクトルの値が正であった場合
                        if float(txt12.get())==0:
                            ul1 = str(np.abs(float(txt9.get())))+str(txt_ul.get())
                        else:
                            ul1 = str(float(txt12.get())*Vc)+str('+')+str(float(txt9.get()))+str(txt_ul.get())
            except ValueError:#整数でない
                pass

        if float(txt10.get())==0:
            if float(txt13.get())==0:
                ul2 = str('0')
            else:
                ul2 = str(float(txt13.get())*Vc)
        elif float(txt10.get())==1:
            if float(txt13.get())==0:
                ul2 = str(txt_ul.get())
            else:
                ul2 = str(float(txt13.get())*Vc)+str('+')+str(txt_ul.get())
        elif float(txt10.get())==-1:
            if float(txt13.get())==0:
                ul2 = str('-')+str(txt_ul.get())
            else:
                ul2 = str(float(txt13.get())*Vc)+str('-')+str(txt_ul.get())
        else:
            try:
                number2 = float(txt10.get())
                if number2.is_integer():#整数である
                    if number2<0:#Vベクトルの値が負であった場合
                        if float(txt13.get())==0:
                            ul2 = str('-')+str(int(np.abs(float(txt10.get()))))+str(txt_ul.get())
                        else:
                            ul2 = str(float(txt13.get())*Vc)+str('-')+str(int(np.abs(float(txt10.get()))))+str(txt_ul.get())
                    elif number2>0:#Vベクトルの値が正であった場合
                        if float(txt13.get())==0:
                            ul2 = str(int(np.abs(float(txt10.get()))))+str(txt_ul.get())
                        else:
                            ul2 = str(float(txt13.get())*Vc)+str('+')+str(int(float(txt10.get())))+str(txt_ul.get())
                else:#整数でない
                    if number2<0:#Vベクトルの値が負であった場合
                        if float(txt13.get())==0:
                            ul2 = str('-')+str(np.abs(float(txt10.get())))+str(txt_ul.get())
                        else:
                            ul2 = str(float(txt13.get())*Vc)+str('-')+str(np.abs(float(txt10.get())))+str(txt_ul.get())
                    elif number2>0:#Vベクトルの値が正であった場合
                        if float(txt13.get())==0:
                            ul2 = str(np.abs(float(txt10.get())))+str(txt_ul.get())
                        else:
                            ul2 = str(float(txt13.get())*Vc)+str('+')+str(float(txt10.get()))+str(txt_ul.get())
            except ValueError:#整数でない
                pass

        if float(txt11.get())==0:
            if float(txt14.get())==0:
                ul3 = str('0')
            else:
                ul3 = str(float(txt14.get())*Vc)
        elif float(txt11.get())==1:
            if float(txt14.get())==0:
                ul3 = str(txt_ul.get())
            else:
                ul3 = str(float(txt14.get())*Vc)+str('+')+str(txt_ul.get())
        elif float(txt11.get())==-1:
            if float(txt14.get())==0:
                ul3 = str('-')+str(txt_ul.get())
            else:
                ul3 = str(float(txt14.get())*Vc)+str('-')+str(txt_ul.get())
        else:
            try:
                number3 = float(txt11.get())
                if number3.is_integer():#整数である
                    if number3<0:#Vベクトルの値が負であった場合
                        if float(txt14.get())==0:
                            ul2 = str('-')+str(int(np.abs(float(txt11.get()))))+str(txt_ul.get())
                        else:
                            ul2 = str(float(txt14.get())*Vc)+str('-')+str(int(np.abs(float(txt11.get()))))+str(txt_ul.get())
                    elif number3>0:#Vベクトルの値が正であった場合
                        if float(txt14.get())==0:
                            ul2 = str(int(np.abs(float(txt11.get()))))+str(txt_ul.get())
                        else:
                            ul2 = str(float(txt14.get())*Vc)+str('+')+str(int(float(txt11.get())))+str(txt_ul.get())
                else:#整数でない
                    if number3<0:#Vベクトルの値が負であった場合
                        if float(txt14.get())==0:
                            ul2 = str('-')+str(np.abs(float(txt11.get())))+str(txt_ul.get())
                        else:
                            ul2 = str(float(txt14.get())*Vc)+str('-')+str(np.abs(float(txt11.get())))+str(txt_ul.get())
                    elif number3>0:#Vベクトルの値が正であった場合
                        if float(txt14.get())==0:
                            ul2 = str(np.abs(float(txt11.get())))+str(txt_ul.get())
                        else:
                            ul2 = str(float(txt14.get())*Vc)+str('+')+str(float(txt11.get()))+str(txt_ul.get())
            except ValueError:#整数でない
                pass

        Ulabel2 = (f"({ul1},{ul2},{ul3})")

        #図を出力する
        #intensityの範囲
        fig6=plt.figure()
        fig6.subplots_adjust(left=0.30, right=0.75, bottom=0.2)
        ax = fig6.add_subplot(111)
        # グリッド線を引く
        gt=gridtype.get()
        if gt == 0:
            #ax.set_axisbelow(True)  # グリッド線を背面に配置
            ax.grid(False)
        elif gt == 1:
            ax.grid(True)
        #im=plt.pcolormesh(QU, hwlist5, I_hwU, cmap='jet', vmin=z_min, vmax=z_max)
        at=axistype.get()
        if at==0:
            im=plt.pcolormesh(state['QU'], state['hwlist5'], state['I_hwU'], cmap='jet', vmin=z_min, vmax=z_max)
        elif at==1:
            if z_min==0:
                z_min=np.nanmin(state['I'][state['I'] != 0])
                im=plt.pcolormesh(state['QU'], state['hwlist5'], state['I_hwU'], cmap='jet', norm = LogNorm(vmin=np.nanmin(state['I'][state['I'] != 0]), vmax=z_max))
            else:
                im=plt.pcolormesh(state['QU'], state['hwlist5'], state['I_hwU'], cmap='jet', norm = LogNorm(vmin=z_min, vmax=z_max))
        cbar=plt.colorbar(im,ticks=mticker.LinearLocator(numticks=3))
        # カラーバーのタイトルを設定
        cbar.set_label('Intenisty (a.u.)')
        ax.text(0.1,1.1,f'{txt_vl.get()} = %.3f ± %.3f (r.l.u.)' %(Vc,Vpm), transform=ax.transAxes)
        ax.set_xlabel(str(Ulabel2))
        ax.set_ylabel("ℏω (meV)")
        ax.set_xlim(Ulim_min,Ulim_max)
        ax.set_ylim(Elim_min,Elim_max)
        #, cmap="jet", extend='both',ticks=np.linspace(vmin, vmax, 5)
        #plt.axis('tight')

        # shared variables are stored in state
        state['Erange_2d_UvsE'] = state['energylist']
        state['Urange_2d_UvsE'] = [float(txt9.get())*state['QU2'],float(txt10.get())*state['QU2'],float(txt11.get())*state['QU2']]
        state['Vrange_2d_UvsE'] = [[float(txt12.get())*(Vc - Vpm),float(txt12.get())*(Vc + Vpm)],[float(txt13.get())*(Vc - Vpm),float(txt13.get())*(Vc + Vpm)],[float(txt14.get())*(Vc - Vpm),float(txt14.get())*(Vc + Vpm)]]

        # グラフ内に表示範囲を決定するボックス
        # 最小値と最大値の初期値
        default_xmin = round(Ulim_min, 3)
        default_xmax = round(Ulim_max, 3)

        default_ymin = round(Elim_min, 3)
        default_ymax = round(Elim_max, 3)

        default_zmin = round(z_min, 3)
        default_zmax = round(z_max, 3)

        # テキストボックスを作成して最小値と最大値を設定
        xmin_box = TextBox(plt.axes([0.3, 0.02, 0.08, 0.05]), 'xMin:', initial=str(default_xmin))
        xmax_box = TextBox(plt.axes([0.6, 0.02, 0.08, 0.05]), 'xMax:', initial=str(default_xmax))

        ymin_box = TextBox(plt.axes([0.1, 0.2, 0.08, 0.05]), 'yMin:', initial=str(default_ymin))
        ymax_box = TextBox(plt.axes([0.1, 0.83, 0.08, 0.05]), 'yMax:', initial=str(default_ymax))

        zmin_box = TextBox(plt.axes([0.9, 0.2, 0.08, 0.05]), 'zMin:', initial=str(default_zmin))
        zmax_box = TextBox(plt.axes([0.9, 0.83, 0.08, 0.05]), 'zMax:', initial=str(default_zmax))

        # 最小値と最大値が変更されたときに呼び出される関数
        def update_axis_range(text):
            try:
                xmin_val = float(xmin_box.text)
                xmax_val = float(xmax_box.text)
                ax.set_xlim(xmin_val, xmax_val)
                ymin_val = float(ymin_box.text)
                ymax_val = float(ymax_box.text)
                ax.set_ylim(ymin_val, ymax_val)
                zmin_val = float(zmin_box.text)
                zmax_val = float(zmax_box.text)
                cbar.mappable.set_clim(vmin=zmin_val, vmax=zmax_val)
                fig6.canvas.draw_idle()
            except ValueError:
                pass

        xmin_box.on_submit(update_axis_range)
        xmax_box.on_submit(update_axis_range)
        ymin_box.on_submit(update_axis_range)
        ymax_box.on_submit(update_axis_range)
        zmin_box.on_submit(update_axis_range)
        zmax_box.on_submit(update_axis_range)

        plt.show()
    else:
        pass
