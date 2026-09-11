from ...callback_runtime import *

def constQmap_1D(env):
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
    txt_1d_3 = env.get('txt_1d_3')
    txt_1d_4 = env.get('txt_1d_4')
    txt_1d_5 = env.get('txt_1d_5')
    txt_1d_6 = env.get('txt_1d_6')
    txt_ul = env.get('txt_ul')
    txt_vl = env.get('txt_vl')
    energy_axis = get_single_crystal_map_energy_axis(state)

    #既に記入しているUとVの範囲を読み出し。
    Uc=float(txt_1d_3.get())
    Upm=float(txt_1d_4.get())
    Vc=float(txt_1d_5.get())
    Vpm=float(txt_1d_6.get())
    # 変数　QU, QV, QU2, QV2, I ,Ierr
    hw_num = int(len(energy_axis)+1)
    hwlist6=np.zeros(hw_num)
    #hwが1つのときの例外処理として装置分解能の範囲を出力するようにする
    if hw_num==2:
        hwlist6[0] = float(energy_axis[0]-(state['ef_tol']+0.005))
        hwlist6[1] = float(energy_axis[-1]+(state['ef_tol']+0.005))
    else:
        hwlist6[0] = float(energy_axis[0])-(float(energy_axis[1])-float(energy_axis[0]))
        hwlist6[-1] = float(energy_axis[-1])+(float(energy_axis[-1])-float(energy_axis[-2]))

        #hwlist5[0] = float(energylist[0])-(float(energylist[1])-float(energylist[0]))
        #hwlist5[-1] = float(energylist[-1])+(float(energylist[-1])-float(energylist[-2]))

        for ne in range(hw_num-2):
            hwlist6[ne+1] = (float(energy_axis[ne])+float(energy_axis[ne+1]))/2

    if Upm==0:
        Ind_1dE_U = [np.abs(state['QU2'] - Uc).argmin()]
    else:
        ind_1dE_U = list(zip(*np.where((Uc - Upm <= state['QU2'] ) & (state['QU2'] <= Uc + Upm))))
        Ind_1dE_U = list(np.ravel(ind_1dE_U))

    if Vpm==0:
        Ind_1dE_V = [np.abs(state['QV2'] - Vc).argmin()]
    else:
        ind_1dE_V = list(zip(*np.where((Vc - Vpm <= state['QV2'] ) & (state['QV2'] <= Vc + Vpm))))
        Ind_1dE_V = list(np.ravel(ind_1dE_V))

    # ないリストを参照すると、次のグラフ表示の時、空白のグラフができる。これを回避するためにリストが空の時はグラフ表示しない分岐を作成
    if len(Ind_1dE_U)!=0 and len(Ind_1dE_V)!=0:
        #旧コード
        #I_hw1d1 = np.nanmean(I[:,ind_1dE_V,:],axis = 1)
        #Ierr_hw1d1 = ((np.nansum(Ierr[:,ind_1dE_V,:]*Ierr[:,ind_1dE_V,:],axis = 1))**(1/2))/len(ind_1dE_V)
        # 強度はNan値を省いて足し、Nan値を省いた値の個数で割る。誤差に関してはNan値を省いて２乗和を取り、平方根を取ってから、NaN値を省いた値の個数で割る
        """
        I_hw1d1=np.zeros((len(energylist),len(QV)-1))
        Ierr_hw1d1=np.zeros((len(energylist),len(QV)-1))
        for ll in range(len(energylist)):
            for nn in range(len(QV)-1):
                n_nanind0 = (list(zip(*np.where(~np.isnan(I[ll,nn,Ind_1dE_U])))))
                N_nanind0 = list(np.ravel(n_nanind0)[::1])
                if N_nanind0:
                    I_hw1d1[ll,nn] = np.nansum(I[ll,nn,Ind_1dE_U])/(len(N_nanind0))
                    Ierr_hw1d1[ll,nn] = ((np.nansum(np.multiply(Ierr[ll,nn,Ind_1dE_U],Ierr[ll,nn,Ind_1dE_U])))**(1/2))/(len(N_nanind0))
                else:
                    I_hw1d1[ll,nn] = np.nan
                    Ierr_hw1d1[ll,nn] = np.nan

        global I_hw1d2,Ierr_hw1d2
        #I_hw1d2 = np.nanmean(I_hw1d1[:,:,ind_1dE_U],axis = 2)
        #Ierr_hw1d2 = ((np.nansum(Ierr_hw1d1[:,:,ind_1dE_U]*Ierr_hw1d1[:,:,ind_1dE_U],axis = 2))**(1/2))/len(ind_1dE_U)
        I_hw1d2 = np.zeros(len(energylist))
        Ierr_hw1d2 = np.zeros(len(energylist))
        for ll in range(len(energylist)):
            n_nanind = (list(zip(*np.where(~np.isnan(I_hw1d1[ll,Ind_1dE_V])))))
            N_nanind = list(np.ravel(n_nanind)[::1])
            if N_nanind:
                #I_1DU[mm]=np.sum(I_ce[ind_cE1dV,mm][~np.isnan(I_ce[ind_cE1dV,ll])])/(len(I_ce[n_nanind[0]]))
                I_hw1d2[ll] = (np.nansum(I_hw1d1[ll,Ind_1dE_V]))/(len(N_nanind))
                Ierr_hw1d2[ll] = ((np.nansum(np.multiply(Ierr_hw1d1[ll,Ind_1dE_V],Ierr_hw1d1[ll,Ind_1dE_V])))**(1/2))/(len(N_nanind))
            else:
                I_hw1d2[ll] = np.nan
                Ierr_hw1d2[ll] = np.nan
        """

        # shared variables are stored in state
        state['I_hw1d2'] = np.zeros(len(energy_axis))
        state['Ierr_hw1d2'] = np.zeros(len(energy_axis))

        for ll in range(len(energy_axis)):
            n_nanind = (list(zip(*np.where(~np.isnan(state['I'][ll, Ind_1dE_V[0]:Ind_1dE_V[-1]+1, Ind_1dE_U[0]:Ind_1dE_U[-1]+1])))))
            N_nanind = list(np.ravel(n_nanind)[::2])
            state['I_hw1d2'][ll] = np.nansum(state['I'][ll,Ind_1dE_V[0]:Ind_1dE_V[-1]+1, Ind_1dE_U[0]:Ind_1dE_U[-1]+1])/(len(N_nanind))
            state['Ierr_hw1d2'][ll] = ((np.nansum(np.multiply(state['Ierr'][ll,Ind_1dE_V[0]:Ind_1dE_V[-1]+1, Ind_1dE_U[0]:Ind_1dE_U[-1]+1],state['Ierr'][ll,Ind_1dE_V[0]:Ind_1dE_V[-1]+1, Ind_1dE_U[0]:Ind_1dE_U[-1]+1])))**(1/2))/(len(N_nanind))


        # 例外処理
        if len(list(zip(*np.where(~np.isnan(state['I_hw1d2'])))))!=0:
            # グラフの軸設定
            if scale_s_Emin_txt.get()=="":
                xlim_min=round(float(energy_axis[0]), 2)
            else:
                xlim_min=float(scale_s_Emin_txt.get())
            if scale_s_Emax_txt.get()=="":
                xlim_max=float(round(energy_axis[-1],2))
            else:
                xlim_max=float(scale_s_Emax_txt.get())

            if scale_s_Imin_txt.get()=="":
                if np.nanmax(state['I_hw1d2'])+np.nanmax(state['Ierr_hw1d2']) >= 0:
                    ylim_min=0
                elif np.nanmax(state['I_hw1d2'])+np.nanmax(state['Ierr_hw1d2']) < 0:
                    ylim_min=np.nanmax(state['I_hw1d2'])+np.nanmax(state['Ierr_hw1d2'])
            else:
                ylim_min=float(scale_s_Imin_txt.get())

            if scale_s_Imax_txt.get()=="":
                if np.nanmax(state['I_hw1d2'])+np.nanmax(state['Ierr_hw1d2']) >= 0:
                    ylim_max=np.nanmax(state['I_hw1d2'])+np.nanmax(state['Ierr_hw1d2'])
                elif np.nanmax(state['I_hw1d2'])+np.nanmax(state['Ierr_hw1d2']) < 0:
                    ylim_max=np.abs(np.nanmax(state['I_hw1d2'])+np.nanmax(state['Ierr_hw1d2']))
            else:
                ylim_max=float(scale_s_Imax_txt.get())

            # shared variables are stored in state
            # エラーバーのグラフを作成
            fig9=plt.figure()

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
                    ax9.set_xlim(xmin_val, xmax_val)
                    ymin_val = float(ymin_box.text)
                    ymax_val = float(ymax_box.text)
                    ax9.set_ylim(ymin_val, ymax_val)
                    fig9.canvas.draw_idle()
                except ValueError:
                    pass

            xmin_box.on_submit(update_axis_range)
            xmax_box.on_submit(update_axis_range)
            ymin_box.on_submit(update_axis_range)
            ymax_box.on_submit(update_axis_range)

            # 現在のFigure番号を取得
            state['oneDE'] = plt.gcf().number
            fig9.subplots_adjust(left=0.30, bottom=0.2)
            ax9 = fig9.add_subplot(111)
            #plt.text(0.1,1.1,f'{txt_vl.get()} = %.3f' %Vc, transform=ax.transAxes)
            #plt.text(0.3,1.1,' ± %.3f (r.l.u.)' %Vpm, transform=ax.transAxes)
            #plt.text(0.1,1.05,f'{txt_ul.get()} = %.3f' %Uc, transform=ax.transAxes)
            #plt.text(0.3,1.05,' ± %.3f (r.l.u.)' %Upm, transform=ax.transAxes)
            plt.xlabel("ℏω (meV)")
            plt.ylabel("Intensity (a. u.)")
            ax9.errorbar(energy_axis, state['I_hw1d2'], yerr=state['Ierr_hw1d2'], capsize=10,label=f'{txt_ul.get()}='+str(Uc)+'±'+str(Upm)+'(r.l.u.) ,'f'{txt_vl.get()}='+str(Vc)+'±'+str(Vpm)+'(r.l.u.)')

            # shared variables are stored in state
            state['Erange_1d_Ivshw'] = energy_axis.copy()
            state['Urange_1d_Ivshw'] = [[float(txt9.get())*(Uc - Upm),float(txt9.get())*(Uc + Upm)],[float(txt10.get())*(Uc - Upm),float(txt10.get())*(Uc + Upm)],[float(txt11.get())*(Uc - Upm),float(txt11.get())*(Uc + Upm)]]
            state['Vrange_1d_Ivshw'] = [[float(txt12.get())*(Vc - Vpm),float(txt12.get())*(Vc + Vpm)],[float(txt13.get())*(Vc - Vpm),float(txt13.get())*(Vc + Vpm)],[float(txt14.get())*(Vc - Vpm),float(txt14.get())*(Vc + Vpm)]]

            gt=gridtype.get()
            if gt == 0:
                #ax.set_axisbelow(True)  # グリッド線を背面に配置
                ax9.grid(False)
            elif gt == 1:
                ax9.grid(True)
            at=axistype.get()
            if at==1:
                plt.yscale('log')
                if ylim_min==0:
                    ylim_min=np.nanmin(state['I_hw1d2'])-np.nanmax(state['Ierr_hw1d2'])
            ax9.legend()
            ax9.set_xlim(xlim_min,xlim_max) #x軸の範囲を指定
            ax9.set_ylim(ylim_min,ylim_max) #y軸の範囲を指定
            #plt.tick_params(labelsize=20)
            plt.show()

    else:
        pass

def constQmap_1D2(env):
    axistype = env.get('axistype')
    state = env.get('state')
    txt10 = env.get('txt10')
    txt11 = env.get('txt11')
    txt12 = env.get('txt12')
    txt13 = env.get('txt13')
    txt14 = env.get('txt14')
    txt9 = env.get('txt9')
    txt_1d_3 = env.get('txt_1d_3')
    txt_1d_4 = env.get('txt_1d_4')
    txt_1d_5 = env.get('txt_1d_5')
    txt_1d_6 = env.get('txt_1d_6')
    txt_ul = env.get('txt_ul')
    txt_vl = env.get('txt_vl')
    energy_axis = get_single_crystal_map_energy_axis(state)

    # 図番号が存在するかどうかの確認
    if plt.fignum_exists(state['oneDE'])==True:
        Uc=float(txt_1d_3.get())
        Upm=float(txt_1d_4.get())
        Vc=float(txt_1d_5.get())
        Vpm=float(txt_1d_6.get())
        # 変数　QU, QV, QU2, QV2, I ,Ierr
        hw_num = int(len(energy_axis)+1)
        hwlist6=np.zeros(hw_num)
        hwlist6[0] = float(energy_axis[0])-(float(energy_axis[1])-float(energy_axis[0]))
        hwlist6[-1] = float(energy_axis[-1])+(float(energy_axis[-1])-float(energy_axis[-2]))

        #hwlist5[0] = float(energylist[0])-(float(energylist[1])-float(energylist[0]))
        #hwlist5[-1] = float(energylist[-1])+(float(energylist[-1])-float(energylist[-2]))

        for ne in range(hw_num-2):
            hwlist6[ne+1] = (float(energy_axis[ne])+float(energy_axis[ne+1]))/2

        if Upm==0:
            Ind_1dE_U = [np.abs(state['QU2'] - Uc).argmin()]
        else:
            ind_1dE_U = list(zip(*np.where((Uc - Upm <= state['QU2'] ) & (state['QU2'] <= Uc + Upm))))
            Ind_1dE_U = list(np.ravel(ind_1dE_U))

        if Vpm==0:
            Ind_1dE_V = [np.abs(state['QV2'] - Vc).argmin()]
        else:
            ind_1dE_V = list(zip(*np.where((Vc - Vpm <= state['QV2'] ) & (state['QV2'] <= Vc + Vpm))))
            Ind_1dE_V = list(np.ravel(ind_1dE_V))

        # ないリストを参照すると、次のグラフ表示の時、空白のグラフができる。これを回避するためにリストが空の時はグラフ表示しない分岐を作成
        if len(Ind_1dE_U)!=0 and len(Ind_1dE_V)!=0:
            #旧コード
            #I_hw1d1 = np.nanmean(I[:,ind_1dE_V,:],axis = 1)
            #Ierr_hw1d1 = ((np.nansum(Ierr[:,ind_1dE_V,:]*Ierr[:,ind_1dE_V,:],axis = 1))**(1/2))/len(ind_1dE_V)
            # 強度はNan値を省いて足し、Nan値を省いた値の個数で割る。誤差に関してはNan値を省いて２乗和を取り、平方根を取ってから、NaN値を省いた値の個数で割る
            # shared variables are stored in state
            state['I_hw1d2'] = np.zeros(len(energy_axis))
            state['Ierr_hw1d2'] = np.zeros(len(energy_axis))

            for ll in range(len(energy_axis)):
                n_nanind = (list(zip(*np.where(~np.isnan(state['I'][ll, Ind_1dE_V[0]:Ind_1dE_V[-1]+1, Ind_1dE_U[0]:Ind_1dE_U[-1]+1])))))
                N_nanind = list(np.ravel(n_nanind)[::2])
                state['I_hw1d2'][ll] = np.nansum(state['I'][ll,Ind_1dE_V[0]:Ind_1dE_V[-1]+1, Ind_1dE_U[0]:Ind_1dE_U[-1]+1])/(len(N_nanind))
                state['Ierr_hw1d2'][ll] = ((np.nansum(np.multiply(state['Ierr'][ll,Ind_1dE_V[0]:Ind_1dE_V[-1]+1, Ind_1dE_U[0]:Ind_1dE_U[-1]+1],state['Ierr'][ll,Ind_1dE_V[0]:Ind_1dE_V[-1]+1, Ind_1dE_U[0]:Ind_1dE_U[-1]+1])))**(1/2))/(len(N_nanind))

            # 例外処理
            if len(list(zip(*np.where(~np.isnan(state['I_hw1d2'])))))!=0:
                # グラフの軸設定
                #xlim_min=energylist[0]
                #xlim_max=energylist[-1]

                #ylim_min=0
                #ylim_max=np.nanmax(I_hw1d2)+np.nanmax(Ierr_hw1d2)

                # 図番号に対応するaxオブジェクトにアクセス
                fig9 = plt.figure(state['oneDE'])
                ax9 = fig9.gca()
                ax9.errorbar(energy_axis, state['I_hw1d2'], yerr=state['Ierr_hw1d2'], capsize=10,label=f'{txt_ul.get()}='+str(Uc)+'±'+str(Upm)+'(r.l.u.) ,'f'{txt_vl.get()}='+str(Vc)+'±'+str(Vpm)+'(r.l.u.)')

                # shared variables are stored in state
                state['Erange_1d_Ivshw'] = energy_axis.copy()
                state['Urange_1d_Ivshw'] = [[float(txt9.get())*(Uc - Upm),float(txt9.get())*(Uc + Upm)],[float(txt10.get())*(Uc - Upm),float(txt10.get())*(Uc + Upm)],[float(txt11.get())*(Uc - Upm),float(txt11.get())*(Uc + Upm)]]
                state['Vrange_1d_Ivshw'] = [[float(txt12.get())*(Vc - Vpm),float(txt12.get())*(Vc + Vpm)],[float(txt13.get())*(Vc - Vpm),float(txt13.get())*(Vc + Vpm)],[float(txt14.get())*(Vc - Vpm),float(txt14.get())*(Vc + Vpm)]]

                at=axistype.get()
                if at==1:
                    plt.yscale('log')
                    #if ylim_min==0:
                    #    ylim_min=np.nanmin(I_hw1d2)-np.nanmax(Ierr_hw1d2)
                ax9.legend()
                #ax9.set_xlim(xlim_min,xlim_max) #x軸の範囲を指定
                #ax9.set_ylim(ylim_min,ylim_max) #y軸の範囲を指定
                plt.draw()

def constE_1D_U(env):
    axistype = env.get('axistype')
    gridtype = env.get('gridtype')
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
    txt_1d_1 = env.get('txt_1d_1')
    txt_1d_2 = env.get('txt_1d_2')
    txt_1d_5 = env.get('txt_1d_5')
    txt_1d_6 = env.get('txt_1d_6')
    txt_vl = env.get('txt_vl')
    # いきなりこちらのボタンを押しても1Dカットができるように
    Ind_e = None
    hwlist3 = None
    Ec=float(txt_1d_1.get())
    Epm=float(txt_1d_2.get())
    Vc=float(txt_1d_5.get())
    Vpm=float(txt_1d_6.get())
    hwlist3=np.zeros(len(state['energylist']))
    for ne in range(len(state['energylist'])):
        hwlist3[ne] = float(state['energylist'][ne])

    if Epm==0:
        Ind_e = [np.abs(hwlist3 - Ec).argmin()]
    else:
        ind_e = list(zip(*np.where(( Ec - Epm <=  hwlist3 ) & (  hwlist3 <= Ec + Epm ))))
        Ind_e = list(np.ravel(ind_e))

    if Vpm==0:
        Ind_cE1dV = [np.abs(state['QV2'] - Vc).argmin()]
    else:
        ind_cE1dV = list(zip(*np.where((Vc - Vpm <= state['QV2'] ) & (state['QV2'] <= Vc + Vpm))))
        Ind_cE1dV = list(np.ravel(ind_cE1dV))

    # ないリストを参照すると、次のグラフ表示の時、空白のグラフができる。これを回避するためにリストが空の時はグラフ表示しない分岐を作成
    if len(Ind_e)!=0 and len(Ind_cE1dV)!=0:
        # 強度はNan値を省いて足し、Nan値を省いた値の個数で割る。誤差に関してはNan値を省いて２乗和を取り、平方根を取ってから、NaN値を省いた値の個数で割る
        # shared variables are stored in state
        state['I_1DU'] = np.zeros(len(state['QU'])-1)
        state['Ierr_1DU'] = np.zeros(len(state['QU'])-1)

        for mm in range(len(state['QU'])-1):
            n_nanind = (list(zip(*np.where(~np.isnan(state['I'][Ind_e[0]:Ind_e[-1]+1,Ind_cE1dV[0]:Ind_cE1dV[-1]+1,mm])))))
            N_nanind = list(np.ravel(n_nanind)[::2])
            state['I_1DU'][mm] = np.nansum(state['I'][Ind_e[0]:Ind_e[-1]+1,Ind_cE1dV[0]:Ind_cE1dV[-1]+1,mm])/(len(N_nanind))
            state['Ierr_1DU'][mm] = ((np.nansum(np.multiply(state['Ierr'][Ind_e[0]:Ind_e[-1]+1,Ind_cE1dV[0]:Ind_cE1dV[-1]+1,mm],state['Ierr'][Ind_e[0]:Ind_e[-1]+1,Ind_cE1dV[0]:Ind_cE1dV[-1]+1,mm])))**(1/2))/(len(N_nanind))

        #例外処理
        if len(list(zip(*np.where(~np.isnan(state['I_1DU'])))))!=0:
            # グラフの軸設定
            if scale_s_Umin_txt.get()=="":
                xlim_min=round(np.min(state['QU']),2)
            else:
                xlim_min=float(scale_s_Umin_txt.get())
            if scale_s_Umax_txt.get()=="":
                xlim_max=round(np.max(state['QU']),2)
            else:
                xlim_max=float(scale_s_Umax_txt.get())

            if scale_s_Imin_txt.get()=="":
                if np.nanmax(state['I_1DU'])+np.nanmax(state['Ierr_1DU']) >= 0:
                    ylim_min=0
                elif np.nanmax(state['I_1DU'])+np.nanmax(state['Ierr_1DU']) < 0:
                    ylim_min=np.nanmax(state['I_1DU'])+np.nanmax(state['Ierr_1DU'])
            else:
                ylim_min=float(scale_s_Imin_txt.get())

            if scale_s_Imax_txt.get()=="":
                if np.nanmax(state['I_1DU'])+np.nanmax(state['Ierr_1DU']) >= 0:
                    ylim_max=np.nanmax(state['I_1DU'])+np.nanmax(state['Ierr_1DU'])
                elif np.nanmax(state['I_1DU'])+np.nanmax(state['Ierr_1DU']) < 0:
                    ylim_max=np.abs(np.nanmax(state['I_1DU'])+np.nanmax(state['Ierr_1DU']))
            else:
                ylim_max=float(scale_s_Imax_txt.get())

            # エラーバーのグラフを作成
            # shared variables are stored in state
            fig8=plt.figure()

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
                    ax8.set_xlim(xmin_val, xmax_val)
                    ymin_val = float(ymin_box.text)
                    ymax_val = float(ymax_box.text)
                    ax8.set_ylim(ymin_val, ymax_val)
                    fig8.canvas.draw_idle()
                except ValueError:
                    pass

            xmin_box.on_submit(update_axis_range)
            xmax_box.on_submit(update_axis_range)
            ymin_box.on_submit(update_axis_range)
            ymax_box.on_submit(update_axis_range)

            # 現在のFigure番号を取得
            state['oneDU'] = plt.gcf().number
            fig8.subplots_adjust(left=0.30, bottom=0.2)
            ax8 = fig8.add_subplot(111)
            #ax.text(0.1,1.1,f'{txt_vl.get()} = %.3f' %Vc, transform=ax.transAxes)
            #ax.text(0.3,1.1,' ± %.3f (r.l.u.)' %Vpm, transform=ax.transAxes)
            #plt.text(0.1,1.05,'E = %.3f' %Ec, transform=ax.transAxes)
            #plt.text(0.3,1.05,' ± %.3f meV' %Epm, transform=ax.transAxes)
            plt.xlabel(str(state['Ulabel']))
            plt.ylabel("Intensity (a. u.)")
            ax8.errorbar(state['QU2'], state['I_1DU'], yerr=state['Ierr_1DU'], capsize=10,label=f'E={Ec}±{Epm}meV, {txt_vl.get()}={Vc}±{Vpm}(r.l.u.)')

            # shared variables are stored in state
            state['Erange_1d_IvsU'] = [Ec - Epm,Ec + Epm]
            state['Urange_1d_IvsU'] = [float(txt9.get())*state['QU2'],float(txt10.get())*state['QU2'],float(txt11.get())*state['QU2']]
            state['Vrange_1d_IvsU'] = [[float(txt12.get())*(Vc - Vpm),float(txt12.get())*(Vc + Vpm)],[float(txt13.get())*(Vc - Vpm),float(txt13.get())*(Vc + Vpm)],[float(txt14.get())*(Vc - Vpm),float(txt14.get())*(Vc + Vpm)]]

            gt=gridtype.get()
            if gt == 0:
                #ax.set_axisbelow(True)  # グリッド線を背面に配置
                ax8.grid(False)
            elif gt == 1:
                ax8.grid(True)

            at=axistype.get()
            if at==1:
                plt.yscale('log')
                #if ylim_min==0:
                #    ylim_min=np.nanmin(I_1DU)-np.nanmax(Ierr_1DU)
            ax8.legend()
            ax8.set_xlim(xlim_min,xlim_max) #x軸の範囲を指定
            ax8.set_ylim(ylim_min,ylim_max) #y軸の範囲を指定
            #plt.tick_params(labelsize=20)
            plt.show()            
    else:
        # 何もしない
        pass

def constE_1D_U2(env):
    axistype = env.get('axistype')
    state = env.get('state')
    txt10 = env.get('txt10')
    txt11 = env.get('txt11')
    txt12 = env.get('txt12')
    txt13 = env.get('txt13')
    txt14 = env.get('txt14')
    txt9 = env.get('txt9')
    txt_1d_1 = env.get('txt_1d_1')
    txt_1d_2 = env.get('txt_1d_2')
    txt_1d_5 = env.get('txt_1d_5')
    txt_1d_6 = env.get('txt_1d_6')
    txt_vl = env.get('txt_vl')
    # 図番号が存在するかどうかの確認
    if plt.fignum_exists(state['oneDU'])==True:
        # 追加の1Dカットをプロットする。
        Ind_e = None
        hwlist3 = None
        Ec=float(txt_1d_1.get())
        Epm=float(txt_1d_2.get())
        Vc=float(txt_1d_5.get())
        Vpm=float(txt_1d_6.get())
        hwlist3=np.zeros(len(state['energylist']))
        for ne in range(len(state['energylist'])):
            hwlist3[ne] = float(state['energylist'][ne])

        if Epm==0:
            Ind_e = [np.abs(hwlist3 - Ec).argmin()]
        else:
            ind_e = list(zip(*np.where(( Ec - Epm <=  hwlist3 ) & (  hwlist3 <= Ec + Epm ))))
            Ind_e = list(np.ravel(ind_e))

        if Vpm==0:
            Ind_cE1dV = [np.abs(state['QV2'] - Vc).argmin()]
        else:
            ind_cE1dV = list(zip(*np.where((Vc - Vpm <= state['QV2'] ) & (state['QV2'] <= Vc + Vpm))))
            Ind_cE1dV = list(np.ravel(ind_cE1dV))

        # ないリストを参照すると、次のグラフ表示の時、空白のグラフができる。これを回避するためにリストが空の時はグラフ表示しない分岐を作成
        if len(Ind_e)!=0 and len(Ind_cE1dV)!=0:
            # shared variables are stored in state
            state['I_1DU'] = np.zeros(len(state['QU'])-1)
            state['Ierr_1DU'] = np.zeros(len(state['QU'])-1)
            for mm in range(len(state['QU'])-1):
                n_nanind = (list(zip(*np.where(~np.isnan(state['I'][Ind_e[0]:Ind_e[-1]+1,Ind_cE1dV[0]:Ind_cE1dV[-1]+1,mm])))))
                N_nanind = list(np.ravel(n_nanind)[::2])
                state['I_1DU'][mm] = np.nansum(state['I'][Ind_e[0]:Ind_e[-1]+1,Ind_cE1dV[0]:Ind_cE1dV[-1]+1,mm])/(len(N_nanind))
                state['Ierr_1DU'][mm] = ((np.nansum(np.multiply(state['Ierr'][Ind_e[0]:Ind_e[-1]+1,Ind_cE1dV[0]:Ind_cE1dV[-1]+1,mm],state['Ierr'][Ind_e[0]:Ind_e[-1]+1,Ind_cE1dV[0]:Ind_cE1dV[-1]+1,mm])))**(1/2))/(len(N_nanind))

            #例外処理
            if len(list(zip(*np.where(~np.isnan(state['I_1DU'])))))!=0:
                #xlim_min=round(np.min(QU),2)
                #xlim_max=round(np.max(QU),2)

                #ylim_min=0
                #ylim_max=np.nanmax(I_1DU)+np.nanmax(Ierr_1DU)

                # 図番号に対応するaxオブジェクトにアクセス
                fig8 = plt.figure(state['oneDU'])
                ax8 = fig8.gca()
                ax8.errorbar(state['QU2'], state['I_1DU'], yerr=state['Ierr_1DU'], capsize=10,label=f'E={Ec}±{Epm}meV, {txt_vl.get()}={Vc}±{Vpm}(r.l.u.)')

                # shared variables are stored in state
                state['Erange_1d_IvsU'] = [Ec - Epm,Ec + Epm]
                state['Urange_1d_IvsU'] = [float(txt9.get())*state['QU2'],float(txt10.get())*state['QU2'],float(txt11.get())*state['QU2']]
                state['Vrange_1d_IvsU'] = [[float(txt12.get())*(Vc - Vpm),float(txt12.get())*(Vc + Vpm)],[float(txt13.get())*(Vc - Vpm),float(txt13.get())*(Vc + Vpm)],[float(txt14.get())*(Vc - Vpm),float(txt14.get())*(Vc + Vpm)]]

                at=axistype.get()
                if at==1:
                    plt.yscale('log')
                    #if ylim_min==0:
                    #    ylim_min=np.nanmin(I_1DU)-np.nanmax(Ierr_1DU)
                ax8.legend()
                #ax8.set_xlim(xlim_min,xlim_max) #x軸の範囲を指定
                #ax8.set_ylim(ylim_min,ylim_max) #y軸の範囲を指定
                plt.draw()

def constE_1D_V(env):
    axistype = env.get('axistype')
    gridtype = env.get('gridtype')
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
    txt_1d_1 = env.get('txt_1d_1')
    txt_1d_2 = env.get('txt_1d_2')
    txt_1d_3 = env.get('txt_1d_3')
    txt_1d_4 = env.get('txt_1d_4')
    txt_ul = env.get('txt_ul')
    # いきなりこちらのボタンを押しても1Dカットができるように
    Ind_e = None
    hwlist2 = None
    Ec=float(txt_1d_1.get())
    Epm=float(txt_1d_2.get())
    Uc=float(txt_1d_3.get())
    Upm=float(txt_1d_4.get())
    if Epm < 0:
        return
    hwlist2=np.zeros(len(state['energylist']))
    for ne in range(len(state['energylist'])):
        hwlist2[ne] = float(state['energylist'][ne])

    if Epm==0:
        Ind_e = [np.abs(hwlist2 - Ec).argmin()]
    else:
        ind_e = list(zip(*np.where(( Ec - Epm <=  hwlist2 ) & (  hwlist2 <= Ec + Epm ))))
        Ind_e = list(np.ravel(ind_e))

    if Upm==0:
        Ind_cE1dU = [np.abs(state['QU2'] - Uc).argmin()]
    else:
        ind_cE1dU = list(zip(*np.where((Uc - Upm <= state['QU2'] ) & (state['QU2'] <= Uc + Upm))))
        Ind_cE1dU = list(np.ravel(ind_cE1dU))

    # ないリストを参照すると、次のグラフ表示の時、空白のグラフができる。これを回避するためにリストが空の時はグラフ表示しない分岐を作成
    if len(Ind_e)!=0 and len(Ind_cE1dU)!=0:
        # Nan値を省いて２乗和を取り、平方根を取ってから、NaN値を省いた値の個数で割る          
        # shared variables are stored in state
        state['I_1DV'] = np.zeros(len(state['QV'])-1)
        state['Ierr_1DV'] = np.zeros(len(state['QV'])-1)
        for nn in range(len(state['QV'])-1):
            n_nanind = (list(zip(*np.where(~np.isnan(state['I'][Ind_e[0]:Ind_e[-1]+1,nn,Ind_cE1dU[0]:Ind_cE1dU[-1]+1])))))
            N_nanind = list(np.ravel(n_nanind)[::2])
            state['I_1DV'][nn] = np.nansum(state['I'][Ind_e[0]:Ind_e[-1]+1,nn,Ind_cE1dU[0]:Ind_cE1dU[-1]+1])/(len(N_nanind))
            state['Ierr_1DV'][nn] = ((np.nansum(np.multiply(state['Ierr'][Ind_e[0]:Ind_e[-1]+1,nn,Ind_cE1dU[0]:Ind_cE1dU[-1]+1],state['Ierr'][Ind_e[0]:Ind_e[-1]+1,nn,Ind_cE1dU[0]:Ind_cE1dU[-1]+1])))**(1/2))/(len(N_nanind))

        #例外処理
        if len(list(zip(*np.where(~np.isnan(state['I_1DV'])))))!=0:
            # グラフの軸設定
            if scale_s_Vmin_txt.get()=="":
                xlim_min=round(np.min(state['QV']),2)
            else:
                xlim_min=float(scale_s_Vmin_txt.get())
            if scale_s_Vmax_txt.get()=="":
                xlim_max=round(np.max(state['QV']),2)
            else:
                xlim_max=float(scale_s_Vmax_txt.get())

            if scale_s_Imin_txt.get()=="":
                if np.nanmax(state['I_1DV'])+np.nanmax(state['Ierr_1DV']) >= 0:
                    ylim_min=0
                elif np.nanmax(state['I_1DV'])+np.nanmax(state['Ierr_1DV']) < 0:
                    ylim_min=np.nanmax(state['I_1DV'])+np.nanmax(state['Ierr_1DV'])
            else:
                ylim_min=float(scale_s_Imin_txt.get())

            if scale_s_Imax_txt.get()=="":
                if np.nanmax(state['I_1DV'])+np.nanmax(state['Ierr_1DV']) >= 0:
                    ylim_max=np.nanmax(state['I_1DV'])+np.nanmax(state['Ierr_1DV'])
                elif np.nanmax(state['I_1DV'])+np.nanmax(state['Ierr_1DV']) < 0:
                    ylim_max=np.abs(np.nanmax(state['I_1DV'])+np.nanmax(state['Ierr_1DV']))
            else:
                ylim_max=float(scale_s_Imax_txt.get())

            # エラーバーのグラフを作成
            # shared variables are stored in state
            fig7=plt.figure()

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
                    ax7.set_xlim(xmin_val, xmax_val)
                    ymin_val = float(ymin_box.text)
                    ymax_val = float(ymax_box.text)
                    ax7.set_ylim(ymin_val, ymax_val)
                    fig7.canvas.draw_idle()
                except ValueError:
                    pass

            xmin_box.on_submit(update_axis_range)
            xmax_box.on_submit(update_axis_range)
            ymin_box.on_submit(update_axis_range)
            ymax_box.on_submit(update_axis_range)

            # 現在のFigure番号を取得
            state['oneDV'] = plt.gcf().number
            fig7.subplots_adjust(left=0.30,bottom=0.2)
            ax7 = fig7.add_subplot(111)
            #plt.text(0.1,1.1,f'{txt_ul.get()} = %.3f' %Uc, transform=ax.transAxes)
            #plt.text(0.3,1.1,' ± %.3f (r.l.u.)' %Upm, transform=ax.transAxes)
            #plt.text(0.1,1.05,'E = %.3f' %Ec, transform=ax.transAxes)
            #plt.text(0.3,1.05,' ± %.3f meV' %Epm, transform=ax.transAxes)
            plt.xlabel(str(state['Vlabel']))
            plt.ylabel("Intensity (a. u.)")
            ax7.errorbar(state['QV2'], state['I_1DV'], yerr=state['Ierr_1DV'], capsize=10,label=f'E={Ec}±{Epm}meV, {txt_ul.get()}={Uc}±{Upm}(r.l.u.)')

            # shared variables are stored in state
            state['Erange_1d_IvsV'] = [Ec - Epm,Ec + Epm]
            state['Urange_1d_IvsV'] = [[float(txt9.get())*(Uc - Upm),float(txt9.get())*(Uc + Upm)],[float(txt10.get())*(Uc - Upm),float(txt10.get())*(Uc + Upm)],[float(txt11.get())*(Uc - Upm),float(txt11.get())*(Uc + Upm)]]
            state['Vrange_1d_IvsV'] = [float(txt12.get())*state['QV2'],float(txt13.get())*state['QV2'],float(txt14.get())*state['QV2']]

            gt=gridtype.get()
            if gt == 0:
                #ax.set_axisbelow(True)  # グリッド線を背面に配置
                ax7.grid(False)
            elif gt == 1:
                ax7.grid(True)

            at=axistype.get()
            if at==1:
                plt.yscale('log')
                if ylim_min==0:
                    ylim_min=np.nanmin(state['I_1DV'])-np.nanmax(state['Ierr_1DV'])
            ax7.legend()
            ax7.set_xlim(xlim_min,xlim_max) #x軸の範囲を指定
            ax7.set_ylim(ylim_min,ylim_max) #y軸の範囲を指定
            #plt.tick_params(labelsize=20)
            plt.show()

    else:
        pass

def constE_1D_V2(env):
    axistype = env.get('axistype')
    state = env.get('state')
    txt10 = env.get('txt10')
    txt11 = env.get('txt11')
    txt12 = env.get('txt12')
    txt13 = env.get('txt13')
    txt14 = env.get('txt14')
    txt9 = env.get('txt9')
    txt_1d_1 = env.get('txt_1d_1')
    txt_1d_2 = env.get('txt_1d_2')
    txt_1d_3 = env.get('txt_1d_3')
    txt_1d_4 = env.get('txt_1d_4')
    txt_ul = env.get('txt_ul')
    # 図番号が存在するかどうかの確認
    if plt.fignum_exists(state['oneDV'])==True:
        # 追加の1Dカットをプロットする。
        Ind_e = None
        hwlist2 = None
        Ec=float(txt_1d_1.get())
        Epm=float(txt_1d_2.get())
        Uc=float(txt_1d_3.get())
        Upm=float(txt_1d_4.get())
        if Epm < 0:
            return
        hwlist2=np.zeros(len(state['energylist']))
        for ne in range(len(state['energylist'])):
            hwlist2[ne] = float(state['energylist'][ne])

        if Epm==0:
            Ind_e = [np.abs(hwlist2 - Ec).argmin()]
        else:
            ind_e = list(zip(*np.where(( Ec - Epm <=  hwlist2 ) & (  hwlist2 <= Ec + Epm ))))
            Ind_e = list(np.ravel(ind_e))

        if Upm==0:
            Ind_cE1dU = [np.abs(state['QU2'] - Uc).argmin()]
        else:
            ind_cE1dU = list(zip(*np.where((Uc - Upm <= state['QU2'] ) & (state['QU2'] <= Uc + Upm))))
            Ind_cE1dU = list(np.ravel(ind_cE1dU))

        # ないリストを参照すると、次のグラフ表示の時、空白のグラフができる。これを回避するためにリストが空の時はグラフ表示しない分岐を作成
        if len(Ind_e)!=0 and len(Ind_cE1dU)!=0:
            # shared variables are stored in state
            state['I_1DV'] = np.zeros(len(state['QV'])-1)
            state['Ierr_1DV'] = np.zeros(len(state['QV'])-1)
            for nn in range(len(state['QV'])-1):
                n_nanind = (list(zip(*np.where(~np.isnan(state['I'][Ind_e[0]:Ind_e[-1]+1,nn,Ind_cE1dU[0]:Ind_cE1dU[-1]+1])))))
                N_nanind = list(np.ravel(n_nanind)[::2])
                state['I_1DV'][nn] = np.nansum(state['I'][Ind_e[0]:Ind_e[-1]+1,nn,Ind_cE1dU[0]:Ind_cE1dU[-1]+1])/(len(N_nanind))
                state['Ierr_1DV'][nn] = ((np.nansum(np.multiply(state['Ierr'][Ind_e[0]:Ind_e[-1]+1,nn,Ind_cE1dU[0]:Ind_cE1dU[-1]+1],state['Ierr'][Ind_e[0]:Ind_e[-1]+1,nn,Ind_cE1dU[0]:Ind_cE1dU[-1]+1])))**(1/2))/(len(N_nanind))

            #例外処理
            if len(list(zip(*np.where(~np.isnan(state['I_1DV'])))))!=0:
                #xlim_min=round(np.min(QV),2)
                #xlim_max=round(np.max(QV),2)

                #ylim_min=0
                #ylim_max=np.nanmax(I_1DV)+np.nanmax(Ierr_1DV)

                # 図番号に対応するaxオブジェクトにアクセス
                fig7 = plt.figure(state['oneDV'])
                ax7 = fig7.gca()
                ax7.errorbar(state['QV2'], state['I_1DV'], yerr=state['Ierr_1DV'], capsize=10,label=f'E={Ec}±{Epm}meV, {txt_ul.get()}={Uc}±{Upm}(r.l.u.)')

                # shared variables are stored in state
                state['Erange_1d_IvsV'] = [Ec - Epm,Ec + Epm]
                state['Urange_1d_IvsV'] = [[float(txt9.get())*(Uc - Upm),float(txt9.get())*(Uc + Upm)],[float(txt10.get())*(Uc - Upm),float(txt10.get())*(Uc + Upm)],[float(txt11.get())*(Uc - Upm),float(txt11.get())*(Uc + Upm)]]
                state['Vrange_1d_IvsV'] = [float(txt12.get())*state['QV2'],float(txt13.get())*state['QV2'],float(txt14.get())*state['QV2']]

                at=axistype.get()
                if at==1:
                    plt.yscale('log')
                    #if ylim_min==0:
                    #    ylim_min=np.nanmin(I_1DV)-np.nanmax(Ierr_1DV)
                ax7.legend()
                #ax7.set_xlim(xlim_min,xlim_max) #x軸の範囲を指定
                #ax7.set_ylim(ylim_min,ylim_max) #y軸の範囲を指定
                plt.draw()
