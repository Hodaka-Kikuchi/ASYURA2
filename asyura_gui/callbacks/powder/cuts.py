from ...callback_runtime import *

def show_1D_EvsI(env):
    axistypep = env.get('axistypep')
    gridtypep = env.get('gridtypep')
    scale_p_Emax_txt = env.get('scale_p_Emax_txt')
    scale_p_Emin_txt = env.get('scale_p_Emin_txt')
    scale_p_Imax_txt = env.get('scale_p_Imax_txt')
    scale_p_Imin_txt = env.get('scale_p_Imin_txt')
    state = env.get('state')
    txt11_p = env.get('txt11_p')
    txt12_p = env.get('txt12_p')
    #既に記入しているUとVの範囲を読み出し。
    Qc=float(txt11_p.get())
    Qpm=float(txt12_p.get())
    # shared variables are stored in state
    state['Ipow_1dei'] = np.zeros(len(state['energylist']))
    state['Ipowerr_1dei'] = np.zeros(len(state['energylist']))
    # 条件を満たすインデックスを取得。
    if Qpm==0:
        Pow1D_Q = [np.abs(state['Q2'] - Qc).argmin()]
    else:
        pow1D_Q = list(zip(*np.where((Qc - Qpm <= state['Q2']) & (state['Q2'] <= Qc + Qpm))))
        Pow1D_Q = list(np.ravel(pow1D_Q))
    # ないリストを参照すると、次のグラフ表示の時、空白のグラフができる。これを回避するためにリストが空の時はグラフ表示しない分岐を作成
    if len(Pow1D_Q)!=0:
        for ll in range(len(state['energylist'])):
            n_nanind = (list(zip(*np.where(~np.isnan(state['Ipow'][ll,Pow1D_Q])))))
            N_nanind = list(np.ravel(n_nanind)[::1])
            if N_nanind:
                #I_1DU[mm]=np.sum(I_ce[ind_cE1dV,mm][~np.isnan(I_ce[ind_cE1dV,ll])])/(len(I_ce[n_nanind[0]]))
                state['Ipow_1dei'][ll] = (np.nansum(state['Ipow'][ll,Pow1D_Q]))/(len(N_nanind))
                state['Ipowerr_1dei'][ll] = ((np.nansum(np.multiply(state['Ipow_err'][ll,Pow1D_Q],state['Ipow_err'][ll,Pow1D_Q])))**(1/2))/(len(N_nanind))
            else:
                state['Ipow_1dei'][ll] = np.nan
                state['Ipowerr_1dei'][ll] = np.nan

        # 例外処理
        if len(list(zip(*np.where(~np.isnan(state['Ipow_1dei'])))))!=0:
            if scale_p_Emin_txt.get()=="":
                xlim_min=state['energylist'][0]
            else:
                xlim_min=float(scale_p_Emin_txt.get())

            if scale_p_Emax_txt.get()=="":
                xlim_max=state['energylist'][-1]
            else:
                xlim_max=float(scale_p_Emax_txt.get())

            if scale_p_Imin_txt.get()=="":
                if np.nanmax(state['Ipow_1dei'])+np.nanmax(state['Ipowerr_1dei']) >= 0:
                    ylim_min=0
                elif np.nanmax(state['Ipow_1dei'])+np.nanmax(state['Ipowerr_1dei']) < 0:
                    ylim_min=round(np.nanmax(state['Ipow_1dei'])+np.nanmax(state['Ipowerr_1dei']),1)
            else:
                ylim_min=float(scale_p_Imin_txt.get())
            if scale_p_Imax_txt.get()=="":
                if np.nanmax(state['Ipow_1dei'])+np.nanmax(state['Ipowerr_1dei']) >= 0:
                    ylim_max=round(np.nanmax(state['Ipow_1dei'])+np.nanmax(state['Ipowerr_1dei']),1)
                elif np.nanmax(state['Ipow_1dei'])+np.nanmax(state['Ipowerr_1dei']) < 0:
                    ylim_max=round(np.abs(np.nanmax(state['Ipow_1dei'])+np.nanmax(state['Ipowerr_1dei'])),1)
            else:
                ylim_max=float(scale_p_Imax_txt.get())

            # エラーバーのグラフを作成
            # shared variables are stored in state
            fig12=plt.figure()

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
                    ax12.set_xlim(xmin_val, xmax_val)
                    ymin_val = float(ymin_box.text)
                    ymax_val = float(ymax_box.text)
                    ax12.set_ylim(ymin_val, ymax_val)
                    fig12.canvas.draw_idle()
                except ValueError:
                    pass

            xmin_box.on_submit(update_axis_range)
            xmax_box.on_submit(update_axis_range)
            ymin_box.on_submit(update_axis_range)
            ymax_box.on_submit(update_axis_range)

            # 現在のFigure番号を取得
            state['oneDPE'] = plt.gcf().number
            fig12.subplots_adjust(left=0.30, bottom=0.2)
            ax12 = fig12.add_subplot(111)
            #plt.text(0.1,1.1,'Q = %.3f' %Qc, transform=ax.transAxes)
            #plt.text(0.3,1.1,' ± %.3f (r.l.u.)' %Qpm, transform=ax.transAxes)
            plt.xlabel("ℏω (meV)")
            plt.ylabel("Intensity (a. u.)")
            ax12.errorbar(state['energylist'], state['Ipow_1dei'], yerr=state['Ipowerr_1dei'], capsize=10,label='Q='+str(Qc)+'±'+str(Qpm)+'(Å^-1)')

            gt=gridtypep.get()
            if gt == 0:
                #ax.set_axisbelow(True)  # グリッド線を背面に配置
                ax12.grid(False)
            elif gt == 1:
                ax12.grid(True)

            at=axistypep.get()
            if at==1:
                plt.yscale('log')
                if ylim_min==0:
                    ylim_min=np.nanmin(state['Ipow_1dei'])-np.nanmax(state['Ipowerr_1dei'])
            # shared variables are stored in state
            state['elist'] = state['energylist']
            state['qlist'] = [Qc-Qpm,Qc+Qpm]
            ax12.legend()
            ax12.set_xlim(xlim_min,xlim_max) #x軸の範囲を指定
            ax12.set_ylim(ylim_min,ylim_max) #y軸の範囲を指定
            #plt.tick_params(labelsize=20)
            plt.show()

    else:
        pass

def btn_click_1DPE(env):
    axistypep = env.get('axistypep')
    state = env.get('state')
    txt11_p = env.get('txt11_p')
    txt12_p = env.get('txt12_p')
    # 図番号が存在するかどうかの確認
    if plt.fignum_exists(state['oneDPE'])==True:
        #既に記入しているUとVの範囲を読み出し。
        Qc=float(txt11_p.get())
        Qpm=float(txt12_p.get())
        # shared variables are stored in state
        state['Ipow_1dei'] = np.zeros(len(state['energylist']))
        state['Ipowerr_1dei'] = np.zeros(len(state['energylist']))
        # 条件を満たすインデックスを取得。
        if Qpm==0:
            Pow1D_Q = [np.abs(state['Q2'] - Qc).argmin()]
        else:
            pow1D_Q = list(zip(*np.where((Qc - Qpm <= state['Q2']) & (state['Q2'] <= Qc + Qpm))))
            Pow1D_Q = list(np.ravel(pow1D_Q))
        # ないリストを参照すると、次のグラフ表示の時、空白のグラフができる。これを回避するためにリストが空の時はグラフ表示しない分岐を作成
        if len(Pow1D_Q)!=0:
            for ll in range(len(state['energylist'])):
                n_nanind = (list(zip(*np.where(~np.isnan(state['Ipow'][ll,Pow1D_Q])))))
                N_nanind = list(np.ravel(n_nanind)[::1])
                if N_nanind:
                    #I_1DU[mm]=np.sum(I_ce[ind_cE1dV,mm][~np.isnan(I_ce[ind_cE1dV,ll])])/(len(I_ce[n_nanind[0]]))
                    state['Ipow_1dei'][ll] = (np.nansum(state['Ipow'][ll,Pow1D_Q]))/(len(N_nanind))
                    state['Ipowerr_1dei'][ll] = ((np.nansum(np.multiply(state['Ipow_err'][ll,Pow1D_Q],state['Ipow_err'][ll,Pow1D_Q])))**(1/2))/(len(N_nanind))
                else:
                    state['Ipow_1dei'][ll] = np.nan
                    state['Ipowerr_1dei'][ll] = np.nan

            # 例外処理
            if len(list(zip(*np.where(~np.isnan(state['Ipow_1dei'])))))!=0:         
                fig12 = plt.figure(state['oneDPE'])
                ax12 = fig12.gca()
                ax12.errorbar(state['energylist'], state['Ipow_1dei'], yerr=state['Ipowerr_1dei'], capsize=10,label='Q='+str(Qc)+'±'+str(Qpm)+'(Å^-1)')
                at=axistypep.get()
                if at==1:
                    plt.yscale('log')
                    if ylim_min==0:
                        ylim_min=np.nanmin(state['Ipow_1dei'])-np.nanmax(state['Ipowerr_1dei'])
                # shared variables are stored in state
                state['elist'] = state['energylist']
                state['qlist'] = [Qc-Qpm,Qc+Qpm]
                ax12.legend()
                #ax12.set_xlim(xlim_min,xlim_max) #x軸の範囲を指定
                #ax12.set_ylim(ylim_min,ylim_max) #y軸の範囲を指定
                plt.draw()

def show_1D_QvsI(env):
    axistypep = env.get('axistypep')
    gridtypep = env.get('gridtypep')
    scale_p_Imax_txt = env.get('scale_p_Imax_txt')
    scale_p_Imin_txt = env.get('scale_p_Imin_txt')
    scale_p_Qmax_txt = env.get('scale_p_Qmax_txt')
    scale_p_Qmin_txt = env.get('scale_p_Qmin_txt')
    state = env.get('state')
    txt13_p = env.get('txt13_p')
    txt14_p = env.get('txt14_p')
    #既に記入しているUとVの範囲を読み出し。
    Ec=float(txt13_p.get())
    Epm=float(txt14_p.get())
    # shared variables are stored in state
    state['Ipow_1dqi'] = np.zeros(len(state['Q2']))
    state['Ipowerr_1dqi'] = np.zeros(len(state['Q2']))
    # エネルギーリストをフロートに変換
    hwlist_p2=np.zeros(len(state['energylist']))
    for ne in range(len(state['energylist'])):
        hwlist_p2[ne] = float(state['energylist'][ne])
    # 条件を満たすインデックスを取得。
    if Epm==0:
        Pow1D_E = [np.abs(hwlist_p2 - Ec).argmin()]
    else:
        pow1D_E = list(zip(*np.where((Ec - Epm <= hwlist_p2) & (hwlist_p2 <= Ec + Epm))))
        Pow1D_E = list(np.ravel(pow1D_E))
    # ないリストを参照すると、次のグラフ表示の時、空白のグラフができる。これを回避するためにリストが空の時はグラフ表示しない分岐を作成
    if len(Pow1D_E)!=0:
        for qq in range(len(state['Q2'])):
            n_nanind = (list(zip(*np.where(~np.isnan(state['Ipow'][Pow1D_E,qq])))))
            N_nanind = list(np.ravel(n_nanind)[::1])
            if N_nanind:
                #I_1DU[mm]=np.sum(I_ce[ind_cE1dV,mm][~np.isnan(I_ce[ind_cE1dV,ll])])/(len(I_ce[n_nanind[0]]))
                state['Ipow_1dqi'][qq] = (np.nansum(state['Ipow'][Pow1D_E,qq]))/(len(N_nanind))
                state['Ipowerr_1dqi'][qq] = ((np.nansum(np.multiply(state['Ipow_err'][Pow1D_E,qq],state['Ipow_err'][Pow1D_E,qq])))**(1/2))/(len(N_nanind))
            else:
                state['Ipow_1dqi'][qq] = np.nan
                state['Ipowerr_1dqi'][qq] = np.nan

        # 例外処理
        if len(list(zip(*np.where(~np.isnan(state['Ipow_1dqi'])))))!=0:
            # 軸の設定
            if scale_p_Qmin_txt.get()=="":
                xlim_min=round(np.min(state['Q']),2)
            else:
                xlim_min=float(scale_p_Qmin_txt.get())

            if scale_p_Qmax_txt.get()=="":
                xlim_max=round(np.max(state['Q']),2)
            else:
                xlim_max=float(scale_p_Qmax_txt.get())

            if scale_p_Imin_txt.get()=="":
                if np.nanmax(state['Ipow_1dqi'])+np.nanmax(state['Ipowerr_1dqi']) >= 0:
                    ylim_min=0
                elif np.nanmax(state['Ipow_1dqi'])+np.nanmax(state['Ipowerr_1dqi']) < 0:
                    ylim_min=round(np.nanmax(state['Ipow_1dqi'])+np.nanmax(state['Ipowerr_1dqi']),1)
            else:
                ylim_min=float(scale_p_Imin_txt.get())
            if scale_p_Imax_txt.get()=="":
                if np.nanmax(state['Ipow_1dqi'])+np.nanmax(state['Ipowerr_1dqi']) >= 0:
                    ylim_max=round(np.nanmax(state['Ipow_1dqi'])+np.nanmax(state['Ipowerr_1dqi']),1)
                elif np.nanmax(state['Ipow_1dqi'])+np.nanmax(state['Ipowerr_1dqi']) < 0:
                    ylim_max=round(np.abs(np.nanmax(state['Ipow_1dqi'])+np.nanmax(state['Ipowerr_1dqi'])),1)
            else:
                ylim_max=float(scale_p_Imax_txt.get())

            # エラーバーのグラフを作成
            # shared variables are stored in state
            fig13=plt.figure()

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
                    ax13.set_xlim(xmin_val, xmax_val)
                    ymin_val = float(ymin_box.text)
                    ymax_val = float(ymax_box.text)
                    ax13.set_ylim(ymin_val, ymax_val)
                    fig13.canvas.draw_idle()
                except ValueError:
                    pass

            xmin_box.on_submit(update_axis_range)
            xmax_box.on_submit(update_axis_range)
            ymin_box.on_submit(update_axis_range)
            ymax_box.on_submit(update_axis_range)

            # 現在のFigure番号を取得
            state['oneDPQ'] = plt.gcf().number
            fig13.subplots_adjust(left=0.30, bottom=0.2)
            ax13 = fig13.add_subplot(111)
            #plt.text(0.1,1.1,'E = %.3f' %Ec, transform=ax.transAxes)
            #plt.text(0.3,1.1,' ± %.3f (r.l.u.)' %Epm, transform=ax.transAxes)
            plt.xlabel("Q (Å^-1)")
            plt.ylabel("Intensity (a. u.)")
            ax13.errorbar(state['Q2'], state['Ipow_1dqi'], yerr=state['Ipowerr_1dqi'], capsize=10,label='E='+str(Ec)+'±'+str(Epm)+'meV')
            # shared variables are stored in state
            state['elist2'] = [Ec-Epm,Ec+Epm]
            state['qlist2'] = state['Q2']

            gt=gridtypep.get()
            if gt == 0:
                #ax.set_axisbelow(True)  # グリッド線を背面に配置
                ax13.grid(False)
            elif gt == 1:
                ax13.grid(True)

            at=axistypep.get()
            if at==1:
                plt.yscale('log')
                if ylim_min==0:
                    ylim_min=np.nanmin(state['Ipow_1dqi'])-np.nanmax(state['Ipowerr_1dqi'])
            ax13.legend()
            ax13.set_xlim(xlim_min,xlim_max) #x軸の範囲を指定
            ax13.set_ylim(ylim_min,ylim_max) #y軸の範囲を指定
            #plt.tick_params(labelsize=20)

            plt.show()

    else:
        # 何もしない
        pass

def btn_click_1DPQ(env):
    axistypep = env.get('axistypep')
    state = env.get('state')
    txt13_p = env.get('txt13_p')
    txt14_p = env.get('txt14_p')
    # 図番号が存在するかどうかの確認
    if plt.fignum_exists(state['oneDPQ'])==True:
        #既に記入しているUとVの範囲を読み出し。
        Ec=float(txt13_p.get())
        Epm=float(txt14_p.get())
        # shared variables are stored in state
        state['Ipow_1dqi'] = np.zeros(len(state['Q2']))
        state['Ipowerr_1dqi'] = np.zeros(len(state['Q2']))
        # エネルギーリストをフロートに変換
        hwlist_p2=np.zeros(len(state['energylist']))
        for ne in range(len(state['energylist'])):
            hwlist_p2[ne] = float(state['energylist'][ne])
        # 条件を満たすインデックスを取得。
        if Epm==0:
            Pow1D_E = [np.abs(hwlist_p2 - Ec).argmin()]
        else:
            pow1D_E = list(zip(*np.where((Ec - Epm <= hwlist_p2) & (hwlist_p2 <= Ec + Epm))))
            Pow1D_E = list(np.ravel(pow1D_E))
        # ないリストを参照すると、次のグラフ表示の時、空白のグラフができる。これを回避するためにリストが空の時はグラフ表示しない分岐を作成
        if len(Pow1D_E)!=0:
            for qq in range(len(state['Q2'])):
                n_nanind = (list(zip(*np.where(~np.isnan(state['Ipow'][Pow1D_E,qq])))))
                N_nanind = list(np.ravel(n_nanind)[::1])
                if N_nanind:
                    #I_1DU[mm]=np.sum(I_ce[ind_cE1dV,mm][~np.isnan(I_ce[ind_cE1dV,ll])])/(len(I_ce[n_nanind[0]]))
                    state['Ipow_1dqi'][qq] = (np.nansum(state['Ipow'][Pow1D_E,qq]))/(len(N_nanind))
                    state['Ipowerr_1dqi'][qq] = ((np.nansum(np.multiply(state['Ipow_err'][Pow1D_E,qq],state['Ipow_err'][Pow1D_E,qq])))**(1/2))/(len(N_nanind))
                else:
                    state['Ipow_1dqi'][qq] = np.nan
                    state['Ipowerr_1dqi'][qq] = np.nan

            #例外処理
            if len(list(zip(*np.where(~np.isnan(state['Ipow_1dqi'])))))!=0:
                fig13 = plt.figure(state['oneDPQ'])
                ax13 = fig13.gca()
                ax13.errorbar(state['Q2'], state['Ipow_1dqi'], yerr=state['Ipowerr_1dqi'], capsize=10,label='E='+str(Ec)+'±'+str(Epm)+'meV')
                at=axistypep.get()
                if at==1:
                    plt.yscale('log')
                    if ylim_min==0:
                        ylim_min=np.nanmin(state['Ipow_1dqi'])-np.nanmax(state['Ipowerr_1dqi'])
                # shared variables are stored in state
                state['elist2'] = [Ec-Epm,Ec+Epm]
                state['qlist2'] = state['Q2']
                ax13.legend()
                #ax13.set_xlim(xlim_min,xlim_max) #x軸の範囲を指定
                #ax13.set_ylim(ylim_min,ylim_max) #y軸の範囲を指定
                plt.draw()
