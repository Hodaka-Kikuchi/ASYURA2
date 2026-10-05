from ...callback_runtime import *

def advanced_1D_alongE(env):
    axistype = env.get('axistype')
    gridtype = env.get('gridtype')
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
    txt_ad04_1 = env.get('txt_ad04_1')
    txt_ad04_2 = env.get('txt_ad04_2')
    # 散乱面の読み込み
    u1=float(txt9.get())
    u2=float(txt10.get())
    u3=float(txt11.get())
    v1=float(txt12.get())
    v2=float(txt13.get())
    v3=float(txt14.get())
    u = [u1,u2,u3]
    v = [v1,v2,v3]

    # 入力情報の読み込み    
    h_cen=float(txt_ad02_1.get())
    k_cen=float(txt_ad02_2.get())
    l_cen=float(txt_ad02_3.get())
    parp_pm=float(txt_ad04_1.get())
    para_pm=float(txt_ad04_2.get())

    hkl_cen=[h_cen,k_cen,l_cen]

    # ラベル作成用に
    label_hkl_cen=[round(h_cen,3),round(k_cen,3),round(l_cen,3)]
    label_pm1=[round(u1*para_pm,3),round(u2*para_pm,3),round(u3*para_pm,3)]
    label_pm2=[round(v1*parp_pm,3),round(v2*parp_pm,3),round(v3*parp_pm,3)]

    # 入力した方向を生成するuとvの定数を計算。Uの定数とVの定数
    constants1 = np.dot(np.linalg.pinv(np.vstack((u, v)).T), hkl_cen)

    #U,Vの要素から範囲内のインデックスを取り出す
    ind_para_range = list(zip(*np.where((constants1[0]-para_pm <= state['QU2'] ) & (state['QU2'] <= constants1[0]+para_pm))))
    Ind_para_range = list(np.ravel(ind_para_range))
    ind_parp_range = list(zip(*np.where((constants1[1]-parp_pm <= state['QV2'] ) & (state['QV2'] <= constants1[1]+parp_pm))))
    Ind_parp_range = list(np.ravel(ind_parp_range))

    if not Ind_para_range:
        Ind_para_range = [np.abs(state['QU2'] - constants1[0]).argmin()]
    if not Ind_parp_range:
        Ind_parp_range = [np.abs(state['QV2'] - constants1[1]).argmin()]

    # shared variables are stored in state
    state['I_1d_alongE']=np.zeros((len(state['energylist'])))
    state['I_1d_alongE_err']=np.zeros((len(state['energylist'])))
    for ll in range(len(state['energylist'])):
        n_nanind = (list(zip(*np.where(~np.isnan(state['I'][ll, Ind_parp_range[0]:Ind_parp_range[-1]+1, Ind_para_range[0]:Ind_para_range[-1]+1])))))
        N_nanind = list(np.ravel(n_nanind)[::2])
        state['I_1d_alongE'][ll] = np.nansum(state['I'][ll,Ind_parp_range[0]:Ind_parp_range[-1]+1,Ind_para_range[0]:Ind_para_range[-1]+1])/(len(N_nanind))
        state['I_1d_alongE_err'][ll] = ((np.nansum(np.multiply(state['Ierr'][ll,Ind_parp_range[0]:Ind_parp_range[-1]+1,Ind_para_range[0]:Ind_para_range[-1]+1],state['Ierr'][ll,Ind_parp_range[0]:Ind_parp_range[-1]+1,Ind_para_range[0]:Ind_para_range[-1]+1])))**(1/2))/(len(N_nanind))

    if np.all(np.isnan(state['I_1d_alongE'])):
        pass
    else:
        # グラフの軸設定
        if scale_s_Emin_txt.get()=="":
            xlim_min=round(float(state['energylist'][0]), 2)
        else:
            xlim_min=float(scale_s_Emin_txt.get())
        if scale_s_Emax_txt.get()=="":
            xlim_max=round(float(state['energylist'][-1]), 2)
        else:
            xlim_max=float(scale_s_Emax_txt.get())

        # カラーバースケール。空欄の場合は平均値を出力するようにする。
        if scale_s_Imin_txt.get()=="":
            if np.nanmax(state['I_1d_alongE'])+np.nanmax(state['I_1d_alongE_err']) >= 0:
                ylim_min=0
            elif np.nanmax(state['I_1d_alongE'])+np.nanmax(state['I_1d_alongE_err']) < 0:
                ylim_min=round(np.nanmax(state['I_1d_alongE'])+np.nanmax(state['I_1d_alongE_err']),1)
        else:
            ylim_min=float(scale_s_Imin_txt.get())

        if scale_s_Imax_txt.get()=="":
            if np.nanmax(state['I_1d_alongE'])+np.nanmax(state['I_1d_alongE_err']) >= 0:
                ylim_max=round(np.nanmax(state['I_1d_alongE'])+np.nanmax(state['I_1d_alongE_err']),1)
            elif np.nanmax(state['I_1d_alongE'])+np.nanmax(state['I_1d_alongE_err']) < 0:
                ylim_max=np.abs(round(np.nanmax(state['I_1d_alongE'])+np.nanmax(state['I_1d_alongE_err']),1))
        else:
            ylim_max=float(scale_s_Imax_txt.get())

        # shared variables are stored in state
        # エラーバーのグラフを作成
        fig02=plt.figure()

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
                ax02.set_xlim(xmin_val, xmax_val)
                ymin_val = float(ymin_box.text)
                ymax_val = float(ymax_box.text)
                ax02.set_ylim(ymin_val, ymax_val)
                fig02.canvas.draw_idle()
            except ValueError:
                pass

        xmin_box.on_submit(update_axis_range)
        xmax_box.on_submit(update_axis_range)
        ymin_box.on_submit(update_axis_range)
        ymax_box.on_submit(update_axis_range)

        # 現在のFigure番号を取得
        state['adv1DE'] = plt.gcf().number
        fig02.subplots_adjust(left=0.30, bottom=0.2)
        ax02 = fig02.add_subplot(111)
        ax02.set_xlabel("ℏω (meV)")
        ax02.set_ylabel("Intensity (a. u.)")

        ax02.errorbar(state['energylist'], state['I_1d_alongE'], yerr=state['I_1d_alongE_err'], capsize=10, label = str(label_hkl_cen) + '±' + str(label_pm1)+ '±' + str(label_pm2) + '(r.l.u.)')
        gt=gridtype.get()
        if gt == 0:
            #ax.set_axisbelow(True)  # グリッド線を背面に配置
            ax02.grid(False)
        elif gt == 1:
            ax02.grid(True)

        at=axistype.get()
        if at==1:
            plt.yscale('log')
            if ylim_min==0:
                ylim_min=np.nanmin(state['I_1d_alongE'])-np.nanmax(state['I_1d_alongE_err'])

        # shared variables are stored in state
        state['I_1d_Ivshw_E'] = state['energylist']
        state['I_1d_Ivshw_HKL'] = [[round(h_cen+u1*-para_pm,3),round(h_cen+u1*para_pm,3)],[round(k_cen+u2*-para_pm,3),round(k_cen+u2*para_pm,3)],[round(l_cen+u3*-para_pm,3),round(l_cen+u3*para_pm,3)]]
        state['I_1d_Ivshw_hkl'] = [[round(h_cen+v1*-parp_pm,3),round(h_cen+v1*parp_pm,3)],[round(k_cen+v2*-parp_pm,3),round(k_cen+v2*parp_pm,3)],[round(l_cen+v3*-parp_pm,3),round(l_cen+v3*parp_pm,3)]]

        ax02.legend()
        ax02.set_xlim(xlim_min, xlim_max)
        ax02.set_ylim(ylim_min, ylim_max)

        plt.show()

def add_advanced_1D_alongE(env):
    axistype = env.get('axistype')
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
    txt_ad04_1 = env.get('txt_ad04_1')
    txt_ad04_2 = env.get('txt_ad04_2')
    # 図番号が存在するかどうかの確認
    if plt.fignum_exists(state['adv1DE'])==True:
        # 散乱面の読み込み
        u1=float(txt9.get())
        u2=float(txt10.get())
        u3=float(txt11.get())
        v1=float(txt12.get())
        v2=float(txt13.get())
        v3=float(txt14.get())
        u = [u1,u2,u3]
        v = [v1,v2,v3]

        # 入力情報の読み込み    
        h_cen=float(txt_ad02_1.get())
        k_cen=float(txt_ad02_2.get())
        l_cen=float(txt_ad02_3.get())
        parp_pm=float(txt_ad04_1.get())
        para_pm=float(txt_ad04_2.get())

        hkl_cen=[h_cen,k_cen,l_cen]

        # ラベル作成用に
        label_hkl_cen=[round(h_cen,3),round(k_cen,3),round(l_cen,3)]
        label_pm1=[round(u1*para_pm,3),round(u2*para_pm,3),round(u3*para_pm,3)]
        label_pm2=[round(v1*parp_pm,3),round(v2*parp_pm,3),round(v3*parp_pm,3)]

        # 入力した方向を生成するuとvの定数を計算。Uの定数とVの定数
        constants1 = np.dot(np.linalg.pinv(np.vstack((u, v)).T), hkl_cen)

        #U,Vの要素から範囲内のインデックスを取り出す
        ind_para_range = list(zip(*np.where((constants1[0]-para_pm <= state['QU2'] ) & (state['QU2'] <= constants1[0]+para_pm))))
        Ind_para_range = list(np.ravel(ind_para_range))
        ind_parp_range = list(zip(*np.where((constants1[1]-parp_pm <= state['QV2'] ) & (state['QV2'] <= constants1[1]+parp_pm))))
        Ind_parp_range = list(np.ravel(ind_parp_range))

        if not Ind_para_range:
            Ind_para_range = [np.abs(state['QU2'] - constants1[0]).argmin()]
        if not Ind_parp_range:
            Ind_parp_range = [np.abs(state['QV2'] - constants1[1]).argmin()]

        # shared variables are stored in state
        state['I_1d_alongE']=np.zeros((len(state['energylist'])))
        state['I_1d_alongE_err']=np.zeros((len(state['energylist'])))
        for ll in range(len(state['energylist'])):
            n_nanind = (list(zip(*np.where(~np.isnan(state['I'][ll, Ind_parp_range[0]:Ind_parp_range[-1]+1, Ind_para_range[0]:Ind_para_range[-1]+1])))))
            N_nanind = list(np.ravel(n_nanind)[::2])
            state['I_1d_alongE'][ll] = np.nansum(state['I'][ll,Ind_parp_range[0]:Ind_parp_range[-1]+1,Ind_para_range[0]:Ind_para_range[-1]+1])/(len(N_nanind))
            state['I_1d_alongE_err'][ll] = ((np.nansum(np.multiply(state['Ierr'][ll,Ind_parp_range[0]:Ind_parp_range[-1]+1,Ind_para_range[0]:Ind_para_range[-1]+1],state['Ierr'][ll,Ind_parp_range[0]:Ind_parp_range[-1]+1,Ind_para_range[0]:Ind_para_range[-1]+1])))**(1/2))/(len(N_nanind))

        if np.all(np.isnan(state['I_1d_alongE'])):
            pass
        else:
            # グラフの軸設定
            xlim_min=state['energylist'][0]
            xlim_max=state['energylist'][-1]

            ylim_min=0
            ylim_max=np.nanmax(state['I_1d_alongE'])+np.nanmax(state['I_1d_alongE_err'])

            ## エラーバーのグラフを作成
            # 図番号に対応するaxオブジェクトにアクセス
            fig03 = plt.figure(state['adv1DE'])
            ax03 = fig03.gca()
            ax03.errorbar(state['energylist'], state['I_1d_alongE'], yerr=state['I_1d_alongE_err'], capsize=10, label = str(label_hkl_cen) + '±' + str(label_pm1)+ '±' + str(label_pm2) + '(r.l.u.)')

            at=axistype.get()
            if at==1:
                plt.yscale('log')
                if ylim_min==0:
                    ylim_min=np.nanmin(state['I_1d_alongE'])-np.nanmax(state['I_1d_alongE_err'])

            # shared variables are stored in state
            state['I_1d_Ivshw_E'] = state['energylist']
            state['I_1d_Ivshw_HKL'] = [[round(h_cen+u1*-para_pm,3),round(h_cen+u1*para_pm,3)],[round(k_cen+u2*-para_pm,3),round(k_cen+u2*para_pm,3)],[round(l_cen+u3*-para_pm,3),round(l_cen+u3*para_pm,3)]]
            state['I_1d_Ivshw_hkl'] = [[round(h_cen+v1*-parp_pm,3),round(h_cen+v1*parp_pm,3)],[round(k_cen+v2*-parp_pm,3),round(k_cen+v2*parp_pm,3)],[round(l_cen+v3*-parp_pm,3),round(l_cen+v3*parp_pm,3)]]

            ax03.legend()
            #ax03.set_xlim(xlim_min,xlim_max) #x軸の範囲を指定
            #ax03.set_ylim(ylim_min,ylim_max) #y軸の範囲を指定

            plt.draw()

def advanced_1D_alongQ(env):
    axistype = env.get('axistype')
    gridtype = env.get('gridtype')
    i = env.get('i')
    scale_s_Imax_txt = env.get('scale_s_Imax_txt')
    scale_s_Imin_txt = env.get('scale_s_Imin_txt')
    state = env.get('state')
    txt10 = env.get('txt10')
    txt11 = env.get('txt11')
    txt12 = env.get('txt12')
    txt13 = env.get('txt13')
    txt14 = env.get('txt14')
    txt9 = env.get('txt9')
    txt_ad01_1 = env.get('txt_ad01_1')
    txt_ad01_2 = env.get('txt_ad01_2')
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

    # 入力情報の読み込み    
    hw_ini=float(txt_ad01_1.get())
    hw_fin=float(txt_ad01_2.get())

    hwlist2_ad=np.zeros(len(state['energylist']))
    for ne in range(len(state['energylist'])):
        hwlist2_ad[ne] = float(state['energylist'][ne])

    # 条件を満たすエネルギーの面を指定
    ind_e = list(zip(*np.where(( hw_ini <=  hwlist2_ad ) & (  hwlist2_ad <= hw_fin ))))
    Ind_e = list(np.ravel(ind_e))
    if not Ind_e:
        Ind_e = [np.abs(hw_ini-hwlist2_ad).argmin()]

    h_ini=float(txt_ad02_1.get())
    k_ini=float(txt_ad02_2.get())
    l_ini=float(txt_ad02_3.get())
    h_fin=float(txt_ad03_1.get())
    k_fin=float(txt_ad03_2.get())
    l_fin=float(txt_ad03_3.get())
    pm=float(txt_ad04_1.get())

    hkl_ini=[h_ini,k_ini,l_ini]
    hkl_fin=[h_fin,k_fin,l_fin]

    # 入力した方向を生成するuとvの定数を計算。Uの定数とVの定数
    constants1 = np.dot(np.linalg.pinv(np.vstack((u, v)).T), hkl_ini)
    constants2 = np.dot(np.linalg.pinv(np.vstack((u, v)).T), hkl_fin)

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
            #Xrange=QU2[Uini_index:Ufin_index+1]
            Xrange=np.linspace(state['QU2'][Uini_index],state['QU2'][Ufin_index], N)
        elif Uini_index>Ufin_index:
            #Xrange=QU2[Ufin_index:Uini_index+1]
            Xrange=np.linspace(state['QU2'][Ufin_index],state['QU2'][Uini_index], N)

        # Xrange[0]に最も近い値のインデックスを取得
        index_Xrange_0 = np.abs(state['QU2'] - Xrange[0]).argmin()
        # Xrange[-1]に最も近い値のインデックスを取得
        index_Xrange_last = np.abs(state['QU2'] - Xrange[-1]).argmin()

        # shared variables are stored in state
        state['I_1d_alongQ']=np.zeros((len(Xrange)))
        state['I_1d_alongQ_err']=np.zeros((len(Xrange)))

        # 理想のXYのテーブルを作成
        Xtable=Xrange
        Ytable=np.zeros((len(Xtable)))
        # shared variables are stored in state
        state['table_1D']=np.zeros((len(Xtable),3))

        for i in range(len(Xrange)):
            if Vfin_index!=Vini_index:
                Ycenter=(constants1[1]-constants2[1])/(constants1[0]-constants2[0])*Xrange[i]+constants2[1]-(constants1[1]-constants2[1])/(constants1[0]-constants2[0])*constants2[0]
                Ytable[i]=Ycenter
            elif Vfin_index==Vini_index:# 傾きが定義できない場合と0の場合を除く
                Ycenter=state['QV2'][Vini_index]
                Ytable[i]=constants1[1]
            state['table_1D'][i]=np.array([u1, u2, u3])* Xtable[i] + np.array([v1, v2, v3])*Ytable[i]
            ind_1d_range = list(zip(*np.where((Ycenter-pm <= state['QV2'] ) & (state['QV2'] <= Ycenter+pm))))
            Ind_1d_range = list(np.ravel(ind_1d_range))

            n_nanind = (list(zip(*np.where(~np.isnan(state['I'][:,:,index_Xrange_0:index_Xrange_last+1][Ind_e, Ind_1d_range[0]:Ind_1d_range[-1]+1, i])))))
            N_nanind = list(np.ravel(n_nanind)[::2])
            state['I_1d_alongQ'][i] = np.nansum(state['I'][:,:,index_Xrange_0:index_Xrange_last+1][Ind_e, Ind_1d_range[0]:Ind_1d_range[-1]+1, i])/(len(N_nanind))
            state['I_1d_alongQ_err'][i] = ((np.nansum(np.multiply(state['Ierr'][:,:,index_Xrange_0:index_Xrange_last+1][Ind_e, Ind_1d_range[0]:Ind_1d_range[-1]+1, i],state['Ierr'][:,:,index_Xrange_0:index_Xrange_last+1][Ind_e, Ind_1d_range[0]:Ind_1d_range[-1]+1, i])))**(1/2))/(len(N_nanind))

        # グラフの軸設定
        # X軸の範囲は入力した範囲
        Xlim_min=constants1[0]
        Xlim_max=constants2[0]

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

    if Vnum>=Unum:
        N=Vnum
        if Vini_index<Vfin_index:
            #Xrange=QU2[Uini_index:Ufin_index+1]
            Xrange=np.linspace(state['QV2'][Vini_index],state['QV2'][Vfin_index], N)
        elif Vini_index>Vfin_index:
            #Xrange=QU2[Ufin_index:Uini_index+1]
            Xrange=np.linspace(state['QV2'][Vfin_index],state['QV2'][Vini_index], N)

        # Xrange[0]に最も近い値のインデックスを取得
        index_Xrange_0 = np.abs(state['QV2'] - Xrange[0]).argmin()
        # Xrange[-1]に最も近い値のインデックスを取得
        index_Xrange_last = np.abs(state['QV2'] - Xrange[-1]).argmin()

        state['I_1d_alongQ']=np.zeros((len(Xrange)))
        state['I_1d_alongQ_err']=np.zeros((len(Xrange)))

        # 理想のXYのテーブルを作成
        Xtable=Xrange
        Ytable=np.zeros((len(Xtable)))
        state['table_1D']=np.zeros((len(Xtable),3))

        for i in range(len(Xrange)):
            if Ufin_index!=Uini_index:
                Ycenter=(constants1[0]-constants2[0])/(constants1[1]-constants2[1])*Xrange[i]+constants2[0]-(constants1[0]-constants2[0])/(constants1[1]-constants2[1])*constants2[1]
                Ytable[i]=Ycenter
            elif Ufin_index==Uini_index:# 傾きが定義できない場合と0の場合を除く
                Ycenter=state['QU2'][Uini_index]
                Ytable[i]=constants1[0]
            state['table_1D'][i]=np.array([v1, v2, v3])* Xtable[i] + np.array([u1, u2, u3])*Ytable[i]
            ind_1d_range = list(zip(*np.where((Ycenter-pm <= state['QU2'] ) & (state['QU2'] <= Ycenter+pm))))
            Ind_1d_range = list(np.ravel(ind_1d_range))
            n_nanind = (list(zip(*np.where(~np.isnan(state['I'][:,index_Xrange_0:index_Xrange_last+1,:][Ind_e, i, Ind_1d_range[0]:Ind_1d_range[-1]+1])))))
            N_nanind = list(np.ravel(n_nanind)[::2])
            state['I_1d_alongQ'][i] = np.nansum(state['I'][:,index_Xrange_0:index_Xrange_last+1,:][Ind_e, i, Ind_1d_range[0]:Ind_1d_range[-1]+1])/(len(N_nanind))
            state['I_1d_alongQ_err'][i] = ((np.nansum(np.multiply(state['Ierr'][:,index_Xrange_0:index_Xrange_last+1,:][Ind_e, i, Ind_1d_range[0]:Ind_1d_range[-1]+1],state['Ierr'][:,index_Xrange_0:index_Xrange_last+1,:][Ind_e, i, Ind_1d_range[0]:Ind_1d_range[-1]+1])))**(1/2))/(len(N_nanind))
        # グラフの軸設定
        # X軸の範囲は入力した範囲

        Xlim_min=constants1[1]
        Xlim_max=constants2[1]

        # X軸を3等分する
        x_values = np.linspace(constants1[1], constants2[1], 3)
        y_values = np.linspace(constants1[0], constants2[0], 3)
        # x_labels を生成
        x_labels = []
        for u, v in zip(x_values, y_values):
            h = float(round(u1*u + v1*v, 3))
            k = float(round(u2*u + v2*v, 3))
            l = float(round(u3*u + v3*v, 3))

            label = f"[{h:g}, {k:g}, {l:g}]"
            x_labels.append(label)

    if np.all(np.isnan(state['I_1d_alongQ'])):
        pass
    else:
        # InfをNaNに変換
        #I_1d_alongQ[I_1d_alongQ == np.inf] = np.nan
        #I_1d_alongQ_err[I_1d_alongQ_err == np.inf] = np.nan

        # グラフの軸設定
        # カラーバースケール。空欄の場合は平均値を出力するようにする。
        if scale_s_Imin_txt.get()=="":
            if np.nanmax(state['I_1d_alongQ'])+np.nanmax(state['I_1d_alongQ_err']) >= 0:
                ylim_min=0
            elif np.nanmax(state['I_1d_alongQ'])+np.nanmax(state['I_1d_alongQ_err']) < 0:
                ylim_min=round(np.nanmax(state['I_1d_alongQ'])+np.nanmax(state['I_1d_alongQ_err']),1)
        else:
            ylim_min=float(scale_s_Imin_txt.get())

        if scale_s_Imax_txt.get()=="":
            if np.nanmax(state['I_1d_alongQ'])+np.nanmax(state['I_1d_alongQ_err']) >= 0:
                ylim_max=round(np.nanmax(state['I_1d_alongQ'])+np.nanmax(state['I_1d_alongQ_err']),1)
            elif np.nanmax(state['I_1d_alongQ'])+np.nanmax(state['I_1d_alongQ_err']) < 0:
                ylim_max=np.abs(round(np.nanmax(state['I_1d_alongQ'])+np.nanmax(state['I_1d_alongQ_err']),1))
        else:
            ylim_max=float(scale_s_Imax_txt.get())

        # shared variables are stored in state
        # エラーバーのグラフを作成
        fig04=plt.figure()

        # グラフ内に表示範囲を決定するボックス
        # 最小値と最大値の初期値
        default_ymin = round(ylim_min, 2)
        default_ymax = round(ylim_max, 2)

        # テキストボックスを作成して最小値と最大値を設定
        ymin_box = TextBox(plt.axes([0.1, 0.2, 0.08, 0.05]), 'yMin:', initial=str(default_ymin))
        ymax_box = TextBox(plt.axes([0.1, 0.83, 0.08, 0.05]), 'yMax:', initial=str(default_ymax))

        # 最小値と最大値が変更されたときに呼び出される関数
        def update_axis_range(text):
            try:
                ymin_val = float(ymin_box.text)
                ymax_val = float(ymax_box.text)
                ax04.set_ylim(ymin_val, ymax_val)
                fig04.canvas.draw_idle()
            except ValueError:
                pass

        ymin_box.on_submit(update_axis_range)
        ymax_box.on_submit(update_axis_range)

        # 現在のFigure番号を取得
        state['adv1DQ'] = plt.gcf().number
        fig04.subplots_adjust(left=0.30, bottom=0.2)
        ax04 = fig04.add_subplot(111)

        #plt.text(0.1,1.1,f'{txt_vl.get()} = %.3f' %Vc, transform=ax.transAxes)
        #plt.text(0.3,1.1,' ± %.3f (r.l.u.)' %Vpm, transform=ax.transAxes)
        #plt.text(0.1,1.05,f'{txt_ul.get()} = %.3f' %Uc, transform=ax.transAxes)
        #plt.text(0.3,1.05,' ± %.3f (r.l.u.)' %Upm, transform=ax.transAxes)
        plt.xticks(x_values,x_labels)
        plt.ylabel("Intensity (a. u.)")
        plt.xlabel("[H, K, L] (r. l. u.)")
        if Unum>=Vnum:
            ax04.errorbar(Xrange, state['I_1d_alongQ'], yerr=state['I_1d_alongQ_err'], capsize=10, label = 'ℏω = ' + str(hw_ini) + '~' + str(hw_fin) + ' meV, ±' + str([pm*v1,pm*v2,pm*v3]) + ' (r.l.u.)')
        if Vnum>=Unum:
            ax04.errorbar(Xrange, state['I_1d_alongQ'], yerr=state['I_1d_alongQ_err'], capsize=10, label = 'ℏω = ' + str(hw_ini) + '~' + str(hw_fin) + ' meV, ±' + str([pm*u1,pm*u2,pm*u3]) + ' (r.l.u.)')
        # shared variables are stored in state
        state['I_1d_IvsHKL_E'] = [hw_ini,hw_fin]
        state['I_1d_IvsHKL_hkl'] = state['table_1D'].T
        if Unum>=Vnum:
            state['I_1d_IvsHKL_HKL'] = [[-pm*v1,pm*v1],[-pm*v2,pm*v2],[-pm*v3,pm*v3]]
        if Vnum>=Unum:
            state['I_1d_IvsHKL_HKL'] = [[-pm*u1,pm*u1],[-pm*u2,pm*u2],[-pm*u3,pm*u3]]
        at=axistype.get()
        if at==1:
            plt.yscale('log')
            if ylim_min==0:
                ylim_min=np.nanmin(state['I_1d_alongQ'])-np.nanmax(state['I_1d_alongQ_err'])
        ax04.legend()
        ax04.set_xlim(Xlim_min,Xlim_max) #x軸の範囲を指定
        ax04.set_ylim(ylim_min,ylim_max) #y軸の範囲を指定
        #plt.tick_params(labelsize=20)

        gt=gridtype.get()
        if gt == 0:
            #ax.set_axisbelow(True)  # グリッド線を背面に配置
            ax04.grid(False)
        elif gt == 1:
            ax04.grid(True)
        plt.show()

def add_advanced_1D_alongQ(env):
    axistype = env.get('axistype')
    i = env.get('i')
    state = env.get('state')
    txt10 = env.get('txt10')
    txt11 = env.get('txt11')
    txt12 = env.get('txt12')
    txt13 = env.get('txt13')
    txt14 = env.get('txt14')
    txt9 = env.get('txt9')
    txt_ad01_1 = env.get('txt_ad01_1')
    txt_ad01_2 = env.get('txt_ad01_2')
    txt_ad02_1 = env.get('txt_ad02_1')
    txt_ad02_2 = env.get('txt_ad02_2')
    txt_ad02_3 = env.get('txt_ad02_3')
    txt_ad03_1 = env.get('txt_ad03_1')
    txt_ad03_2 = env.get('txt_ad03_2')
    txt_ad03_3 = env.get('txt_ad03_3')
    txt_ad04_1 = env.get('txt_ad04_1')
    # 図番号が存在するかどうかの確認
    if plt.fignum_exists(state['adv1DQ'])==True:
        # 散乱面の読み込み
        u1=float(txt9.get())
        u2=float(txt10.get())
        u3=float(txt11.get())
        v1=float(txt12.get())
        v2=float(txt13.get())
        v3=float(txt14.get())
        u = [u1,u2,u3]
        v = [v1,v2,v3]

        # 入力情報の読み込み    
        hw_ini=float(txt_ad01_1.get())
        hw_fin=float(txt_ad01_2.get())

        hwlist2_ad=np.zeros(len(state['energylist']))
        for ne in range(len(state['energylist'])):
            hwlist2_ad[ne] = float(state['energylist'][ne])

        # 条件を満たすエネルギーの面を指定
        ind_e = list(zip(*np.where(( hw_ini <=  hwlist2_ad ) & (  hwlist2_ad <= hw_fin ))))
        Ind_e = list(np.ravel(ind_e))

        h_ini=float(txt_ad02_1.get())
        k_ini=float(txt_ad02_2.get())
        l_ini=float(txt_ad02_3.get())
        h_fin=float(txt_ad03_1.get())
        k_fin=float(txt_ad03_2.get())
        l_fin=float(txt_ad03_3.get())
        pm=float(txt_ad04_1.get())

        hkl_ini=[h_ini,k_ini,l_ini]
        hkl_fin=[h_fin,k_fin,l_fin]

        # 入力した方向を生成するuとvの定数を計算。Uの定数とVの定数
        constants1 = np.dot(np.linalg.pinv(np.vstack((u, v)).T), hkl_ini)
        constants2 = np.dot(np.linalg.pinv(np.vstack((u, v)).T), hkl_fin)

        # U,Vの要素とvalueの差の絶対値を計算し、最小値のインデックスを取得
        Uini_index = np.abs(state['QU2'] - constants1[0]).argmin()
        Vini_index = np.abs(state['QV2'] - constants1[1]).argmin()

        Ufin_index = np.abs(state['QU2'] - constants2[0]).argmin()
        Vfin_index = np.abs(state['QV2'] - constants2[1]).argmin()

        Unum=np.abs(Ufin_index-Uini_index)+1
        Vnum=np.abs(Vfin_index-Vini_index)+1

        # 条件分岐の設定
        if len(Ind_e)!=0:

            # スライス及びカットの際に自動的に個数が多い方をX軸として選択。
            #I[ll,nn,mm]=I[hw,V,U]の順番でリスト化されている。
            if Unum>=Vnum:
                N=Unum
                if Uini_index<Ufin_index:
                    #Xrange=QU2[Uini_index:Ufin_index+1]
                    Xrange=np.linspace(state['QU2'][Uini_index],state['QU2'][Ufin_index], N)
                elif Uini_index>Ufin_index:
                    #Xrange=QU2[Ufin_index:Uini_index+1]
                    Xrange=np.linspace(state['QU2'][Ufin_index],state['QU2'][Uini_index], N)

                # shared variables are stored in state
                state['I_1d_alongQ']=np.zeros((len(Xrange)))
                state['I_1d_alongQ_err']=np.zeros((len(Xrange)))

                # 理想のXYのテーブルを作成
                Xtable=Xrange
                Ytable=np.zeros((len(Xtable)))
                # shared variables are stored in state
                state['table']=np.zeros((len(Xtable),3))

                for i in range(len(Xrange)):
                    if Vfin_index!=Vini_index:
                        Ycenter=(constants1[1]-constants2[1])/(constants1[0]-constants2[0])*Xrange[i]+constants2[1]-(constants1[1]-constants2[1])/(constants1[0]-constants2[0])*constants2[0]
                        Ytable[i]=Ycenter
                    elif Vfin_index==Vini_index:# 傾きが定義できない場合と0の場合を除く
                        Ycenter=state['QV2'][Vini_index]
                        Ytable[i]=constants1[1]
                    state['table'][i]=np.array([u1, u2, u3])* Xtable[i] + np.array([v1, v2, v3])*Ytable[i]
                    ind_1d_range = list(zip(*np.where((Ycenter-pm <= state['QV2'] ) & (state['QV2'] <= Ycenter+pm))))
                    Ind_1d_range = list(np.ravel(ind_1d_range))
                    n_nanind = (list(zip(*np.where(~np.isnan(state['I'][:,:,Uini_index:Ufin_index+1][Ind_e, Ind_1d_range[0]:Ind_1d_range[-1]+1, i])))))
                    N_nanind = list(np.ravel(n_nanind)[::2])
                    state['I_1d_alongQ'][i] = np.nansum(state['I'][:,:,Uini_index:Ufin_index+1][Ind_e, Ind_1d_range[0]:Ind_1d_range[-1]+1, i])/(len(N_nanind))
                    state['I_1d_alongQ_err'][i] = ((np.nansum(np.multiply(state['Ierr'][:,:,Uini_index:Ufin_index+1][Ind_e, Ind_1d_range[0]:Ind_1d_range[-1]+1, i],state['Ierr'][:,:,Uini_index:Ufin_index+1][Ind_e, Ind_1d_range[0]:Ind_1d_range[-1]+1, i])))**(1/2))/(len(N_nanind))
            # グラフの軸設定
            # X軸の範囲は入力した範囲
            Xlim_min=constants1[0]
            Xlim_max=constants2[0]

            if Vnum>=Unum:
                N=Vnum
                if Vini_index<Vfin_index:
                    #Xrange=QU2[Uini_index:Ufin_index+1]
                    Xrange=np.linspace(state['QV2'][Vini_index],state['QV2'][Vfin_index], N)
                elif Vini_index>Vfin_index:
                    #Xrange=QU2[Ufin_index:Uini_index+1]
                    Xrange=np.linspace(state['QV2'][Vfin_index],state['QV2'][Vini_index], N)

                # Xrange[0]に最も近い値のインデックスを取得
                index_Xrange_0 = np.abs(state['QV2'] - Xrange[0]).argmin()
                # Xrange[-1]に最も近い値のインデックスを取得
                index_Xrange_last = np.abs(state['QV2'] - Xrange[-1]).argmin()

                state['I_1d_alongQ']=np.zeros((len(Xrange)))
                state['I_1d_alongQ_err']=np.zeros((len(Xrange)))

                # 理想のXYのテーブルを作成
                Xtable=Xrange
                Ytable=np.zeros((len(Xtable)))
                state['table']=np.zeros((len(Xtable),3))

                for i in range(len(Xrange)):
                    if Ufin_index!=Uini_index:
                        Ycenter=(constants1[0]-constants2[0])/(constants1[1]-constants2[1])*Xrange[i]+constants2[0]-(constants1[0]-constants2[0])/(constants1[1]-constants2[1])*constants2[1]
                        Ytable[i]=Ycenter
                    elif Ufin_index==Uini_index:# 傾きが定義できない場合と0の場合を除く
                        Ycenter=state['QU2'][Uini_index]
                        Ytable[i]=constants1[0]
                    state['table'][i]=np.array([v1, v2, v3])* Xtable[i] + np.array([u1, u2, u3])*Ytable[i]
                    ind_1d_range = list(zip(*np.where((Ycenter-pm <= state['QU2'] ) & (state['QU2'] <= Ycenter+pm))))
                    Ind_1d_range = list(np.ravel(ind_1d_range))
                    n_nanind = (list(zip(*np.where(~np.isnan(state['I'][:,index_Xrange_0:index_Xrange_last+1,:][Ind_e, i, Ind_1d_range[0]:Ind_1d_range[-1]+1])))))
                    N_nanind = list(np.ravel(n_nanind)[::2])
                    state['I_1d_alongQ'][i] = np.nansum(state['I'][:,index_Xrange_0:index_Xrange_last+1,:][Ind_e, i, Ind_1d_range[0]:Ind_1d_range[-1]+1])/(len(N_nanind))
                    state['I_1d_alongQ_err'][i] = ((np.nansum(np.multiply(state['Ierr'][:,index_Xrange_0:index_Xrange_last+1,:][Ind_e, i, Ind_1d_range[0]:Ind_1d_range[-1]+1],state['Ierr'][:,index_Xrange_0:index_Xrange_last+1,:][Ind_e, i, Ind_1d_range[0]:Ind_1d_range[-1]+1])))**(1/2))/(len(N_nanind))
                # グラフの軸設定
                # X軸の範囲は入力した範囲
                Xlim_min=constants1[1]
                Xlim_max=constants2[1]

            if np.all(np.isnan(state['I_1d_alongQ'])):
                pass
            else:

                ylim_min=0
                ylim_max=np.nanmax(state['I_1d_alongQ'])+np.nanmax(state['I_1d_alongQ_err'])

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

                # エラーバーのグラフを作成
                fig06=plt.figure(state['adv1DQ'])
                ax06 = fig06.gca()
                if Unum>=Vnum:
                    ax06.errorbar(Xrange, state['I_1d_alongQ'], yerr=state['I_1d_alongQ_err'], capsize=10, label = 'ℏω = ' + str(hw_ini) + '~' + str(hw_fin) + ' meV, ±' + str([pm*v1,pm*v2,pm*v3]) + ' (r.l.u.)')
                if Vnum>=Unum:
                    ax06.errorbar(Xrange, state['I_1d_alongQ'], yerr=state['I_1d_alongQ_err'], capsize=10, label = 'ℏω = ' + str(hw_ini) + '~' + str(hw_fin) + ' meV, ±' + str([pm*u1,pm*u2,pm*u3]) + ' (r.l.u.)')
                # shared variables are stored in state
                state['I_1d_IvsHKL_E'] = [hw_ini,hw_fin]
                state['I_1d_IvsHKL_hkl'] = state['table'].T
                if Unum>=Vnum:
                    state['I_1d_IvsHKL_HKL'] = [[-pm*v1,pm*v1],[-pm*v2,pm*v2],[-pm*v3,pm*v3]]
                if Vnum>=Unum:
                    state['I_1d_IvsHKL_HKL'] = [[-pm*u1,pm*u1],[-pm*u2,pm*u2],[-pm*u3,pm*u3]]
                at=axistype.get()
                if at==1:
                    plt.yscale('log')
                    if ylim_min==0:
                        ylim_min=np.nanmin(state['I_1d_alongQ'])-np.nanmax(state['I_1d_alongQ_err'])
                ax06.legend()
                #ax06.set_xlim(Xlim_min,Xlim_max) #x軸の範囲を指定
                #ax06.set_ylim(ylim_min,ylim_max) #y軸の範囲を指定
                #plt.tick_params(labelsize=20)
                plt.show()
