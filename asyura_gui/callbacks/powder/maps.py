from ...callback_runtime import *

def show_powderEmap(env):
    axistypep = env.get('axistypep')
    gridtypep = env.get('gridtypep')
    scale_p_Emax_txt = env.get('scale_p_Emax_txt')
    scale_p_Emin_txt = env.get('scale_p_Emin_txt')
    scale_p_Imax_txt = env.get('scale_p_Imax_txt')
    scale_p_Imin_txt = env.get('scale_p_Imin_txt')
    scale_p_Qmax_txt = env.get('scale_p_Qmax_txt')
    scale_p_Qmin_txt = env.get('scale_p_Qmin_txt')
    state = env.get('state')
    #図を出力する
    # グラフの出力範囲を指定する。
    if scale_p_Qmin_txt.get()=="":
        Qlim_min=round(np.min(state['Q']),2)
    else:
        Qlim_min=float(scale_p_Qmin_txt.get())
    if scale_p_Qmax_txt.get()=="":
        Qlim_max=round(np.max(state['Q']),2)
    else:
        Qlim_max=float(scale_p_Qmax_txt.get())
    if scale_p_Emin_txt.get()=="":
        Elim_min=state['energylist'][0]
    else:
        Elim_min=float(scale_p_Emin_txt.get())
    if scale_p_Emax_txt.get()=="":
        Elim_max=state['energylist'][-1]
    else:
        Elim_max=float(scale_p_Emax_txt.get())

    #intensityの範囲
    # カラーバースケール。空欄の場合は平均値を出力するようにする。
    if scale_p_Imin_txt.get()=="":
        if np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]) >= 0:
            z_min=0
        elif np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]) < 0:
            z_min=round(np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]),1)
    else:
        z_min=float(scale_p_Imin_txt.get())
    if scale_p_Imax_txt.get()=="":
        if np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]) >= 0:
            z_max=round(np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]),1)
        elif np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]) < 0:
            z_max=round(np.abs(np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:])),1)
    else:
        z_max=float(scale_p_Imax_txt.get())

    #fig, ax = plt.figure()
    #axにカラーバーを表示
    fig11, ax = plt.subplots()
    plt.subplots_adjust(left=0.30, right=0.75, bottom=0.2)
    # グリッド線を引く
    gt=gridtypep.get()
    if gt == 0:
        #ax.set_axisbelow(True)  # グリッド線を背面に配置
        ax.grid(False)
    elif gt == 1:
        ax.grid(True)
    #im=plt.pcolormesh(Q, hwlist_p , Ipow, cmap='jet', vmin=z_min, vmax=z_max)
    at=axistypep.get()
    if at==0:
        im=plt.pcolormesh(state['Q'], state['hwlist_p'] , state['Ipow'], cmap='jet', vmin=z_min, vmax=z_max)
    elif at==1:
        if z_min==0:
            z_min=np.nanmin(state['Ipow'][state['Ipow'] != 0])
            im=plt.pcolormesh(state['Q'], state['hwlist_p'] , state['Ipow'], cmap='jet', norm = LogNorm(vmin=np.nanmin(state['Ipow'][state['Ipow'] != 0]), vmax=z_max))
        else:
            im=plt.pcolormesh(state['Q'], state['hwlist_p'] , state['Ipow'], cmap='jet', norm = LogNorm(vmin=z_min, vmax=z_max))
    cbar=plt.colorbar(im,ticks=mticker.LinearLocator(numticks=3))
    # カラーバーのタイトルを設定
    cbar.set_label('Intenisty (a.u.)')
    ax.set_xlabel("Q (Å^-1)")
    ax.set_ylabel("ℏω (meV)")
    ax.set_xlim(Qlim_min,Qlim_max)
    ax.set_ylim(Elim_min,Elim_max)
    #, cmap="jet", extend='both',ticks=np.linspace(vmin, vmax, 5)
    #plt.axis('tight')
    #横スライドでエネルギートランスファーを変更、縦スライドで強度の最大値を変更

    # グラフ内に表示範囲を決定するボックス
    # 最小値と最大値の初期値
    default_xmin = round(Qlim_min, 3)
    default_xmax = round(Qlim_max, 3)

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
            fig11.canvas.draw_idle()
        except ValueError:
            pass

    xmin_box.on_submit(update_axis_range)
    xmax_box.on_submit(update_axis_range)
    ymin_box.on_submit(update_axis_range)
    ymax_box.on_submit(update_axis_range)
    zmin_box.on_submit(update_axis_range)
    zmax_box.on_submit(update_axis_range)

    plt.show()
