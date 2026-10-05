from ...callback_runtime import *

def advanced_2D_constE(env):
    axistype = env.get('axistype')
    gridtype = env.get('gridtype')
    i = env.get('i')
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
    txt16 = env.get('txt16')
    txt17 = env.get('txt17')
    txt19 = env.get('txt19')
    txt20 = env.get('txt20')
    txt9 = env.get('txt9')
    txt_ad01_1 = env.get('txt_ad01_1')
    txt_ad01_2 = env.get('txt_ad01_2')
    # 入力情報の読み込み
    hw_ini=float(txt_ad01_1.get())
    hw_fin=float(txt_ad01_2.get())

    #Ec=(hw_ini+hw_fin)/2
    #Epm=np.abs((hw_ini-hw_fin)/2)

    # constE面の行列を生成
    # 強度はNan値を省いて足し、Nan値を省いた値の個数で割る。誤差に関してはNan値を省いて２乗和を取り、平方根を取ってから、NaN値を省いた値の個数で割る
    # shared variables are stored in state
    state['I_ce_adv']=np.zeros((len(state['QV'])-1,len(state['QU'])-1))
    state['Ierr_ce_adv']=np.zeros((len(state['QV'])-1,len(state['QU'])-1))

    hwlist1_ad=np.zeros(len(state['energylist']))
    for ne in range(len(state['energylist'])):
        hwlist1_ad[ne] = float(state['energylist'][ne])

    # 条件を満たすエネルギーの面を指定
    ind_e = list(zip(*np.where(( hw_ini <=  hwlist1_ad ) & (  hwlist1_ad <= hw_fin ))))
    Ind_e = list(np.ravel(ind_e))
    if not Ind_e:
        Ind_e = [np.abs(hw_ini-hwlist1_ad).argmin()]

    #I[ll,nn,mm]=I[hw,V,U]の順番でリスト化されている。
    for nn in range(len(state['QV'])-1):
        for mm in range(len(state['QU'])-1):
            n_nanind = (list(zip(*np.where(~np.isnan(state['I'][Ind_e,nn,mm])))))
            N_nanind = list(np.ravel(n_nanind)[::1])
            if N_nanind:
                state['I_ce_adv'][nn,mm] = np.nansum(state['I'][Ind_e,nn,mm])/(len(N_nanind))
                state['Ierr_ce_adv'][nn,mm] = ((np.nansum(np.multiply(state['Ierr'][Ind_e,nn,mm],state['Ierr'][Ind_e,nn,mm])))**(1/2))/(len(N_nanind))
            else:
                state['I_ce_adv'][nn,mm] = np.nan
                state['Ierr_ce_adv'][nn,mm] = np.nan
    #図を出力する
    # 軸設定。空欄の場合は範囲マックスを表示するようにする
    if scale_s_Umin_txt.get()=="":
        Ulim_min=float(txt16.get())
    else:
        Ulim_min=float(scale_s_Umin_txt.get())
    if scale_s_Umax_txt.get()=="":
        Ulim_max=float(txt17.get())
    else:
        Ulim_max=float(scale_s_Umax_txt.get())

    if scale_s_Vmin_txt.get()=="":
        Vlim_min=float(txt19.get())
    else:
        Vlim_min=float(scale_s_Vmin_txt.get())
    if scale_s_Vmax_txt.get()=="":
        Vlim_max=float(txt20.get())
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
            z_max=np.abs(round(np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]),1))
    else:
        z_max=float(scale_s_Imax_txt.get())

    # 散乱面の読み込み
    u1=float(txt9.get())
    u2=float(txt10.get())
    u3=float(txt11.get())
    v1=float(txt12.get())
    v2=float(txt13.get())
    v3=float(txt14.get())

    # shared variables are stored in state
    state['table_2DX'] = np.zeros((len(state['QU2']),3))
    state['table_2DY'] = np.zeros((len(state['QV2']),3))
    for i in range(len(state['QU2'])):
        state['table_2DX'][i] = state['QU2'][i] * np.array([u1, u2, u3])
    for j in range(len(state['QV2'])):
        state['table_2DY'][j] = state['QV2'][j] * np.array([v1, v2, v3])

    # 図を作成
    #fig, ax = plt.figure()
    #axにカラーバーを表示
    fig00, ax = plt.subplots()
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
        im=plt.pcolormesh(state['QU'], state['QV'], state['I_ce_adv'], cmap='jet', vmin=z_min, vmax=z_max)
    elif at==1:
        if z_min==0:
            z_min=np.nanmin(state['I'][state['I'] != 0])
            im=plt.pcolormesh(state['QU'], state['QV'], state['I_ce_adv'], cmap='jet', norm = LogNorm(vmin=np.nanmin(state['I'][state['I'] != 0]), vmax=z_max))
        else:
            im=plt.pcolormesh(state['QU'], state['QV'], state['I_ce_adv'], cmap='jet', norm = LogNorm(vmin=z_min, vmax=z_max))
    #sb4=z_max#初期値を一応セット
    cbar=plt.colorbar(im,ticks=mticker.LinearLocator(numticks=3))
    # shared variables are stored in state
    state['E_I_ce'] = [hw_ini,hw_fin]
    # カラーバーのタイトルを設定
    cbar.set_label('Intenisty (a.u.)')
    ax.set_xlabel(str(state['Ulabel']))
    ax.set_ylabel(str(state['Vlabel']))
    ax.set_xlim(Ulim_min,Ulim_max)
    ax.set_ylim(Vlim_min,Vlim_max)
    #, cmap="jet", extend='both',ticks=np.linspace(vmin, vmax, 5)
    #plt.axis('tight')

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
            fig00.canvas.draw_idle()
        except ValueError:
            pass

    xmin_box.on_submit(update_axis_range)
    xmax_box.on_submit(update_axis_range)
    ymin_box.on_submit(update_axis_range)
    ymax_box.on_submit(update_axis_range)
    zmin_box.on_submit(update_axis_range)
    zmax_box.on_submit(update_axis_range)

    plt.show()

def advanced_2D_constQ(env):
    axistype = env.get('axistype')
    gridtype = env.get('gridtype')
    i = env.get('i')
    scale_s_Emax_txt = env.get('scale_s_Emax_txt')
    scale_s_Emin_txt = env.get('scale_s_Emin_txt')
    scale_s_Imax_txt = env.get('scale_s_Imax_txt')
    scale_s_Imin_txt = env.get('scale_s_Imin_txt')
    state = env.get('state')
    txt10 = env.get('txt10')
    txt11 = env.get('txt11')
    txt12 = env.get('txt12')
    txt13 = env.get('txt13')
    txt14 = env.get('txt14')
    txt9 = env.get('txt9')
    txt_ad02_1 = env.get('txt_ad02_1')
    txt_ad02_2 = env.get('txt_ad02_2')
    txt_ad02_3 = env.get('txt_ad02_3')
    txt_ad03_1 = env.get('txt_ad03_1')
    txt_ad03_2 = env.get('txt_ad03_2')
    txt_ad03_3 = env.get('txt_ad03_3')
    txt_ad04_1 = env.get('txt_ad04_1')
    # 散乱面の読み込み
    u1=float(txt9.get())
    u2=float(txt10.get())
    u3=float(txt11.get())
    v1=float(txt12.get())
    v2=float(txt13.get())
    v3=float(txt14.get())
    u = [u1,u2,u3]
    v = [v1,v2,v3]

    # 入力情報の読み込み、2D viewの場合エネルギーの読み込みは不要
    #hw_ini=float(txt_ad01_1.get())
    #hw_fin=float(txt_ad01_2.get())

    h_ini=float(txt_ad02_1.get())
    k_ini=float(txt_ad02_2.get())
    l_ini=float(txt_ad02_3.get())
    h_fin=float(txt_ad03_1.get())
    k_fin=float(txt_ad03_2.get())
    l_fin=float(txt_ad03_3.get())
    pm=float(txt_ad04_1.get())

    hkl_ini=[h_ini,k_ini,l_ini]
    hkl_fin=[h_fin,k_fin,l_fin]

    # uとvを連結して逆行列を生成する。
    #np.linalg.pinv(np.vstack((u, v)).T)

    # 入力した方向を生成するuとvの定数を計算。Uの定数とVの定数
    constants1 = np.dot(np.linalg.pinv(np.vstack((u, v)).T), hkl_ini)
    constants2 = np.dot(np.linalg.pinv(np.vstack((u, v)).T), hkl_fin)
    # constant1=[U_ini,V_ini],constant2=[U_fin,V_fin]

    # U,Vの要素とvalueの差の絶対値を計算し、最小値のインデックスを取得
    Uini_index = np.abs(state['QU2'] - constants1[0]).argmin()
    Vini_index = np.abs(state['QV2'] - constants1[1]).argmin()

    Ufin_index = np.abs(state['QU2'] - constants2[0]).argmin()
    Vfin_index = np.abs(state['QV2'] - constants2[1]).argmin()

    Unum=np.abs(Ufin_index-Uini_index)+1
    Vnum=np.abs(Vfin_index-Vini_index)+1

    # スライス及びカットの際に自動的に個数が多い方をX軸として選択。
    #I[ll,nn,mm]=I[hw,V,U]の順番でリスト化されている。
    if Unum>=Vnum:
        N=Unum
        if Uini_index<Ufin_index:
            Xrange=np.linspace(state['QU2'][Uini_index],state['QU2'][Ufin_index], N)
            Xtable=Xrange
        elif Uini_index>Ufin_index:
            Xrange=np.linspace(state['QU2'][Ufin_index],state['QU2'][Uini_index], N)
            Xtable=Xrange
        if Vfin_index!=Vini_index:
            #Yrange=(constants1[0]-constants2[0])/(constants1[1]-constants2[1])*Xrange+constants2[0]-(constants1[0]-constants2[0])/(constants1[1]-constants2[1])*constants2[1]
            Yrange=(constants1[1]-constants2[1])/(constants1[0]-constants2[0])*Xrange+constants2[1]-(constants1[1]-constants2[1])/(constants1[0]-constants2[0])*constants2[0]
            Ytable=Yrange
        elif Vfin_index==Vini_index:# 傾きが定義できない場合と0の場合を除く
            Yrange=np.ones(len(Xrange))*state['QV2'][Vini_index]
            Ytable=np.ones(len(Yrange))*constants1[1]
        # shared variables are stored in state
        state['table_2D']=np.zeros((len(Xtable),3))
        # Xrange[0]に最も近い値のインデックスを取得
        index_Xrange_0 = np.abs(state['QU2'] - Xrange[0]).argmin()
        # Xrange[-1]に最も近い値のインデックスを取得
        index_Xrange_last = np.abs(state['QU2'] - Xrange[-1]).argmin()
        # shared variables are stored in state
        state['I_cq']=np.zeros((len(state['energylist']), len(Xrange)))
        state['I_cq_err']=np.zeros((len(state['energylist']), len(Xrange)))
        for ll in range(len(state['energylist'])):
            for i in range(len(Xrange)):
                state['table_2D'][i]=np.array([u1, u2, u3])* Xtable[i] + np.array([v1, v2, v3])*Ytable[i]
                # 条件を満たすインデックスを取得。Yrangeの±pmの範囲内にあるインデックス。この条件ではY軸はV
                ind_cut = list(zip(*np.where((Yrange[i] - pm <= state['QV2'] ) & (state['QV2'] <= Yrange[i] + pm))))
                Ind_cut = list(np.ravel(ind_cut))
                n_nanind = (list(zip(*np.where(~np.isnan(state['I'][:,:,index_Xrange_0:index_Xrange_last+1][ll,Ind_cut,i])))))
                N_nanind = list(np.ravel(n_nanind)[::2])
                if N_nanind:
                    state['I_cq'][ll,i] = np.nansum(state['I'][:,:,index_Xrange_0:index_Xrange_last+1][ll,Ind_cut,i])/(len(N_nanind))
                    state['I_cq_err'][ll,i] = np.nansum((np.multiply(state['Ierr'][:,:,index_Xrange_0:index_Xrange_last+1][ll,Ind_cut,i],state['Ierr'][:,:,index_Xrange_0:index_Xrange_last+1][ll,Ind_cut,i]))**(1/2))/(len(N_nanind))
                else:
                    state['I_cq'][ll,i] = np.nan
                    state['I_cq_err'][ll,i] = np.nan

    elif Unum<Vnum:
        N=Vnum
        if Vini_index<Vfin_index:
            Xrange=np.linspace(state['QV2'][Vini_index],state['QV2'][Vfin_index], N)
            Xtable=Xrange
        elif Vini_index>Vfin_index:
            Xrange=np.linspace(state['QV2'][Vfin_index],state['QV2'][Vini_index], N)
            Xtable=Xrange
        if Ufin_index!=Uini_index:
            #Yrange=(constants1[1]-constants2[1])/(constants1[0]-constants2[0])*Xrange+constants2[1]-(constants1[1]-constants2[1])/(constants1[0]-constants2[0])*constants2[0]
            Yrange=(constants1[0]-constants2[0])/(constants1[1]-constants2[1])*Xrange+constants2[0]-(constants1[0]-constants2[0])/(constants1[1]-constants2[1])*constants2[1]
            Ytable=Yrange
        elif Ufin_index==Uini_index:# 傾きが定義できない場合と0の場合を除く
            Yrange=np.ones(len(Xrange))*state['QU2'][Uini_index]
            Ytable=np.ones(len(Yrange))*constants1[0]
        state['table_2D']=np.zeros((len(Xtable),3))
        # Xrange[0]に最も近い値のインデックスを取得
        index_Xrange_0 = np.abs(state['QV2'] - Xrange[0]).argmin()
        # Xrange[-1]に最も近い値のインデックスを取得
        index_Xrange_last = np.abs(state['QV2'] - Xrange[-1]).argmin()

        state['I_cq']=np.zeros((len(state['energylist']), len(Xrange)))
        state['I_cq_err']=np.zeros((len(state['energylist']), len(Xrange)))
        for ll in range(len(state['energylist'])):
            for i in range(len(Xrange)):
                state['table_2D'][i]=np.array([v1, v2, v3])* Xtable[i] + np.array([u1, u2, u3])*Ytable[i]
                # 条件を満たすインデックスを取得。Yrangeの±pmの範囲内にあるインデックス。この条件ではY軸はV
                ind_cut = list(zip(*np.where((Yrange[i] - pm <= state['QU2'] ) & (state['QU2'] <= Yrange[i] + pm))))
                Ind_cut = list(np.ravel(ind_cut))
                n_nanind = (list(zip(*np.where(~np.isnan(state['I'][:,index_Xrange_0:index_Xrange_last+1,:][ll,i,Ind_cut])))))
                N_nanind = list(np.ravel(n_nanind)[::2])
                if N_nanind:
                    state['I_cq'][ll,i] = np.nansum(state['I'][:,index_Xrange_0:index_Xrange_last+1,:][ll,i,Ind_cut])/(len(N_nanind))
                    state['I_cq_err'][ll,i] = np.nansum((np.multiply(state['Ierr'][:,index_Xrange_0:index_Xrange_last+1,:][ll,i,Ind_cut],state['Ierr'][:,index_Xrange_0:index_Xrange_last+1,:][ll,i,Ind_cut]))**(1/2))/(len(N_nanind))
                else:
                    state['I_cq'][ll,i] = np.nan
                    state['I_cq_err'][ll,i] = np.nan
    # X軸の範囲は入力した範囲
    if Unum>=Vnum:
        Xlim_min=constants1[0]
        Xlim_max=constants2[0]
    elif Unum<Vnum:
        Xlim_min=constants1[1]
        Xlim_max=constants2[1]

    if scale_s_Emin_txt.get()=="":
        Elim_min=round(float(state['energylist'][0]), 2)
    else:
        Elim_min=float(scale_s_Emin_txt.get())
    if scale_s_Emax_txt.get()=="":
        Elim_max=round(float(state['energylist'][-1]), 2)
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
            z_max=np.abs(round(np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]),1))
    else:
        z_max=float(scale_s_Imax_txt.get())

    # X軸を3等分する
    x_values = np.linspace(constants1[0], constants2[0], 3)
    y_values = np.linspace(constants1[1], constants2[1], 3)

    # x_labels を生成
    x_labels = []
    for u, v in zip(x_values, y_values):
        h = float(round(u1*u + v1*v, 3))
        k = float(round(u2*u + v2*v, 3))
        l = float(round(u3*u + v3*v, 3))

        label = f"[{h:g}, {k:g}, {l:g}]"
        x_labels.append(label)

    #図を出力する
    #intensityの範囲
    fig01, ax = plt.subplots()
    plt.subplots_adjust(left=0.30, right=0.75, bottom=0.2)  # マージンを調整してグラフを中央に配置
    # shared variables are stored in state
    if Unum>=Vnum:
        ax.text(0.1,1.1,f'{str(state['Vlabel'])} ± %.3f (r.l.u.)' %(pm), transform=ax.transAxes)
        state['table_2D_qrange']=[[-pm*v1,pm*v1],[-pm*v2,pm*v2],[-pm*v3,pm*v3]]
    elif Unum<=Vnum:
        ax.text(0.1,1.1,f'{str(state['Ulabel'])} ± %.3f (r.l.u.)' %(pm), transform=ax.transAxes)
        state['table_2D_qrange']=[[-pm*u1,pm*u1],[-pm*u2,pm*u2],[-pm*u3,pm*u3]]
    #ax.set_xlabel(str(xlabel))
    # X軸の目盛りとラベルを設定
    if Unum >= Vnum:
        ax.set_xticks(x_values)
        ax.set_xticklabels(x_labels, rotation=0)
    elif Unum < Vnum:
        ax.set_xticks(y_values)
        ax.set_xticklabels(x_labels, rotation=0)
    ax.set_xlabel("[H, K, L] (r.l.u.)")
    ax.set_ylabel("ℏω (meV)")
    ax.set_xlim(Xlim_min,Xlim_max)
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
        im=plt.pcolormesh(Xrange, state['energylist'], state['I_cq'], cmap='jet', vmin=z_min, vmax=z_max)
    elif at==1:
        if z_min==0:
            z_min=np.nanmin(state['I'][state['I'] != 0])
            im=plt.pcolormesh(Xrange, state['energylist'], state['I_cq'], cmap='jet', norm = LogNorm(vmin=np.nanmin(state['I'][state['I'] != 0]), vmax=z_max))
        else:
            im=plt.pcolormesh(Xrange, state['energylist'], state['I_cq'], cmap='jet', norm = LogNorm(vmin=z_min, vmax=z_max))
    cbar=plt.colorbar(im,ticks=mticker.LinearLocator(numticks=3))
    # カラーバーのタイトルを設定
    cbar.set_label('Intenisty (a.u.)')
    #ax.text(0.1,1.1,f'{txt_ul.get()} = %.3f ± %.3f (r.l.u.)' %(Uc,Upm), transform=ax.transAxes)

    # グラフ内に表示範囲を決定するボックス
    # 最小値と最大値の初期値
    default_ymin = round(Elim_min, 3)
    default_ymax = round(Elim_max, 3)

    default_zmin = round(z_min, 3)
    default_zmax = round(z_max, 3)

    # テキストボックスを作成して最小値と最大値を設定
    ymin_box = TextBox(plt.axes([0.1, 0.2, 0.08, 0.05]), 'yMin:', initial=str(default_ymin))
    ymax_box = TextBox(plt.axes([0.1, 0.83, 0.08, 0.05]), 'yMax:', initial=str(default_ymax))

    zmin_box = TextBox(plt.axes([0.9, 0.2, 0.08, 0.05]), 'zMin:', initial=str(default_zmin))
    zmax_box = TextBox(plt.axes([0.9, 0.83, 0.08, 0.05]), 'zMax:', initial=str(default_zmax))

    # 最小値と最大値が変更されたときに呼び出される関数
    def update_axis_range(text):
        try:
            ymin_val = float(ymin_box.text)
            ymax_val = float(ymax_box.text)
            ax.set_ylim(ymin_val, ymax_val)
            zmin_val = float(zmin_box.text)
            zmax_val = float(zmax_box.text)
            cbar.mappable.set_clim(vmin=zmin_val, vmax=zmax_val)
            fig01.canvas.draw_idle()
        except ValueError:
            pass

    ymin_box.on_submit(update_axis_range)
    ymax_box.on_submit(update_axis_range)
    zmin_box.on_submit(update_axis_range)
    zmax_box.on_submit(update_axis_range)

    plt.show()
