from ...callback_runtime import *
from asyura_core.data_processing import bin_single_crystal_data, combine_normalized_points, group_energy_transfers, window_bin_2d

def data_box(env):
    CSX = env.get('CSX')
    bgt_txt1 = env.get('bgt_txt1')
    bgt_txt2 = env.get('bgt_txt2')
    bgt_txt3 = env.get('bgt_txt3')
    fgt_txt1 = env.get('fgt_txt1')
    fgt_txt2 = env.get('fgt_txt2')
    fgt_txt3 = env.get('fgt_txt3')
    hw_nan = env.get('hw_nan')
    i = env.get('i')
    sb_txt1 = env.get('sb_txt1')
    sb_txt2 = env.get('sb_txt2')
    sb_txt3 = env.get('sb_txt3')
    sbtype2 = env.get('sbtype2')
    state = env.get('state')
    txt16 = env.get('txt16')
    txt17 = env.get('txt17')
    txt18 = env.get('txt18')
    txt19 = env.get('txt19')
    txt20 = env.get('txt20')
    txt21 = env.get('txt21')
    txt22 = env.get('txt22')
    txt23 = env.get('txt23')
    txt24 = env.get('txt24')

    #UとVのメッシュを用意する
    Ubin = float(txt18.get())
    Umin = float(txt16.get())-Ubin/2
    Umax = float(txt17.get())+Ubin/2

    Vbin = float(txt21.get())
    Vmin = float(txt19.get())-Vbin/2
    Vmax = float(txt20.get())+Vbin/2

    #energy transferを出す。
    # shared variables are stored in state
    if hw_nan.get()==0:# hw cellにℏが入っていない場合
        if fgt_txt1.get()=='':
            E_T = round(state['ef_tol']+0.005,3)
        else:
            E_T = float(fgt_txt1.get())
        dEfg = 0 # energy方向のsmoothing
        dEbg = 0 # energy方向のsmoothing
        # もとのコード
        # さらにエネルギートランスファーのトレランスを考慮して±E_TmeV以内は同じ数値にする。
        state['energylist'] = group_energy_transfers(state['databox'][3,:], E_T)

    if hw_nan.get()==1:# hw cellにℏが入っている場合
        Ebin = float(txt24.get())
        Emin = float(txt22.get())-Ebin/2
        Emax = float(txt23.get())+Ebin/2
        # 処理速度更新のため、E_Tに統一
        E_T = Ebin/2
        if fgt_txt1.get()=="":
            dEfg=0
        else:
            dEfg = (float(fgt_txt1.get())-Ebin)/2 # energy方向のsmoothing

        if bgt_txt1.get()=="":
            dEbg=0
        else:
            dEbg = (float(bgt_txt1.get())-Ebin)/2 # energy方向のsmoothing

        Ne=round((Emax-Emin)/Ebin+1)
        if Ne==1:
            Energylist_cal = [Emin,Emax]
            #ind_e = (list(zip(*np.where(((Energylist_cal[0]) <= databox[3,:]) & (databox[3,:] < (Energylist_cal[-1]))))))
            state['energylist'] = [(Energylist_cal[i] + Energylist_cal[i+1])/2]
        else:
            Energylist_cal=np.zeros((Ne))
            state['energylist']=np.zeros((Ne-1))
            for i in range(Ne):
                Energylist_cal[i] = Emin + Ebin * i
            for i in range(Ne-1):
                #ind_e = (list(zip(*np.where(((Energylist_cal[i]) <= databox[3,:]) & (databox[3,:] < (Energylist_cal[i+1]))))))
                state['energylist'][i] = (Energylist_cal[i] + Energylist_cal[i+1])/2

    # smoothing
    if fgt_txt2.get()=="":
        dU = 0
        #fgt_txt2.insert(0,Ubin)
    else:
        dU = (float(fgt_txt2.get())-Ubin)/2
    if fgt_txt3.get()=="":
        dV = 0
        #fgt_txt3.insert(0,Vbin)
    else:
        dV = (float(fgt_txt3.get())-Vbin)/2

    # backgroundのsmoothing
    if bgt_txt2.get()=="":
        sb_dU = 0
    else:
        sb_dU = (float(bgt_txt2.get())-Ubin)/2
    if bgt_txt3.get()=="":
        sb_dV = 0
    else:
        sb_dV = (float(bgt_txt3.get())-Vbin)/2

    if Umin > Umax:
        return
    if Vmin > Vmax:
        return
    if Ubin < 0:
        return
    if Vbin < 0:
        return
    # shared variables are stored in state
    state['nqu']=round((Umax-Umin)/Ubin+1)
    state['nqv']=round((Vmax-Vmin)/Vbin+1)

    # shared variables are stored in state
    state['QU']=np.zeros((state['nqu']))
    state['QV']=np.zeros((state['nqv']))
    for i in range(state['nqu']):
        state['QU'][i] = Umin + Ubin * i
    for i in range(state['nqv']):
        state['QV'][i] = Vmin + Vbin * i

    # 強度とエラーバーのセルを用意する。もちろん3次元の行列
    # shared variables are stored in state
    state['I'] = None
    state['Ierr'] = None
    state['sb_I'] = None
    state['sb_Ierr'] = None
    state['I']=np.zeros((len(state['energylist']),state['nqv']-1,state['nqu']-1))
    state['Ierr']=np.zeros((len(state['energylist']),state['nqv']-1,state['nqu']-1))
    state['sb_I']=np.zeros((len(state['energylist']),state['nqv']-1,state['nqu']-1))
    state['sb_Ierr']=np.zeros((len(state['energylist']),state['nqv']-1,state['nqu']-1))
    # Summed effective (sensitivity-normalized) foreground monitor of each cell.
    # Used as the weight when cells are combined into cuts, so that cuts are
    # also "sum of counts / sum of monitor".
    state['Imon']=np.zeros((len(state['energylist']),state['nqv']-1,state['nqu']-1))
    # shared variables are stored in state
    state['QU2']=np.zeros((state['nqu']-1))
    state['QV2']=np.zeros((state['nqv']-1))

    for nx in range(state['nqu']-1):
        state['QU2'][nx] = (state['QU'][nx]+state['QU'][nx+1])/2
        for ny in range(state['nqv']-1):
            state['QV2'][ny] = (state['QV'][ny]+state['QV'][ny+1])/2

    # Cell binning is implemented in asyura_core.data_processing.

    # プログレスバーの表示
    # shared variables are stored in state
    var2 = 0 # プログレスバーの変数
    state['pb2']["maximum"] = len(state['energylist']) # プログレスバーの最大値
    state['pb2']["value"] = 0
    state['pb2'].update()
    if CSX.get()==1:# S(q,w), kf/ki
        ssf1=1
        ssf2=float(sb_txt1.get())
        #バックグラウンドファイルがあった場合。
        if state.get('sb_databox') is not None:
            if dEfg==0 and dU==0 and dV==0 and dEbg==0 and sb_dU==0 and sb_dV==0:#smoothing処理をしない場合
                for ne in range(len(state['energylist'])):
                    # 条件を満たすインデックスを取得。まずエネルギーが一致している部分を取り出す。このときエネルギートランスファートレランスを考慮する。
                    # Ind_e = (list(zip(*np.where(databox[3,:] == energylist[ne]))))
                    ind_e = np.flatnonzero(((state['energylist'][ne]-E_T) <= state['databox'][3,:]) & (state['databox'][3,:] < (state['energylist'][ne]+E_T)))
                    if ind_e.size == 0: # 空行列の時
                        state['energylist'][ne] = state['energylist'][ne]
                    else: # 空行列でない時
                        state['energylist'][ne] = np.mean(state['databox'][3,ind_e])

                    # プログレスバー (確定的)。エネルギー毎にステータスが進む
                    var2=var2+1
                    state['pb2']["value"] = var2
                    state['pb2'].update()

                # databoxとsb_databoxの処理
                state['I'], state['Ierr'], state['Imon'] = bin_single_crystal_data(state['databox'], state['monitorbox'], state['N_mcu'], state['NV1'], state['NU1'], state['energylist'], state['QV'], state['QU'], return_monitor=True)
                state['I']=ssf1*state['I']
                state['Ierr']=ssf1*state['Ierr']

                state['sb_I'], state['sb_Ierr'] = bin_single_crystal_data(state['sb_databox'], state['sb_monitorbox'], state['N_mcu'], state['NV1'], state['NU1'], state['energylist'], state['QV'], state['QU'])
                state['sb_I']=ssf2*state['sb_I']
                state['sb_Ierr']=ssf2*state['sb_Ierr']

                state['I'] = np.where(np.isfinite(state['I']), state['I'], np.nan)
                state['Ierr'] = np.where(np.isfinite(state['Ierr']), state['Ierr'], np.nan)
                state['sb_I'] = np.where(np.isfinite(state['sb_I']), state['sb_I'], np.nan)
                state['sb_Ierr'] = np.where(np.isfinite(state['sb_Ierr']), state['sb_Ierr'], np.nan)

                # nanから数値を引くことはできない。nanを0にする
                I_trans=np.nan_to_num(state['I'], nan=0)-np.nan_to_num(state['sb_I'], nan=0)
                # nanから数値を引くことはできない。nanを0にする
                Ierr_trans=np.sqrt(np.square(np.nan_to_num(state['Ierr'], nan=0))+np.square(np.nan_to_num(state['sb_Ierr'], nan=0)))

                if sbtype2.get()==0:
                    # 差し引き後に両方の要素でnan値であった部分をnan値にする。
                    I_trans[np.isnan(state['I']) & np.isnan(state['sb_I'])] = np.nan
                    Ierr_trans[np.isnan(state['Ierr']) & np.isnan(state['sb_Ierr'])] = np.nan
                elif sbtype2.get()==1:
                    # 差し引き後にFGもしくはBGの要素でnan値であった部分をnan値にする。
                    I_trans[np.isnan(state['I']) | np.isnan(state['sb_I'])] = np.nan
                    Ierr_trans[np.isnan(state['Ierr']) | np.isnan(state['sb_Ierr'])] = np.nan

                state['I']=I_trans
                state['Ierr']=Ierr_trans

            else:#smoothing処理をする場合
                # メッシュの中にデータを入れていく。
                for ne in range(len(state['energylist'])):
                    # 条件を満たすインデックスを取得。まずエネルギーが一致している部分を取り出す。このときエネルギートランスファートレランスを考慮する。
                    Databox_kari=None
                    Ind_e = None
                    sb_Databox_kari=None
                    sb_Ind_e = None
                    # Ind_e = (list(zip(*np.where(databox[3,:] == energylist[ne]))))
                    ind_e = np.flatnonzero(((state['energylist'][ne]-E_T-dEfg) <= state['databox'][3,:]) & (state['databox'][3,:] < (state['energylist'][ne]+E_T+dEfg)))
                    sb_ind_e = np.flatnonzero(((state['energylist'][ne]-E_T-dEbg) <= state['sb_databox'][3,:]) & (state['sb_databox'][3,:] < (state['energylist'][ne]+E_T+dEbg)))
                    if ind_e.size == 0: # 空行列の時
                        state['energylist'][ne] = state['energylist'][ne]
                    else: # 空行列でない時
                        state['energylist'][ne] = np.mean(state['databox'][3,ind_e])

                    Ind_e = ind_e
                    sb_Ind_e = sb_ind_e
                    Databox_kari = state['databox'][:,Ind_e]
                    Monitorbox_kari = state['monitorbox'][Ind_e]
                    sb_Databox_kari = state['sb_databox'][:,sb_Ind_e]
                    sb_Monitorbox_kari = state['sb_monitorbox'][sb_Ind_e]
                    # Windowed (smoothed) binning: every window QU[nx]-dU < U <= QU[nx+1]+dU,
                    # QV[ny]-dV < V <= QV[ny+1]+dV is read from a summed-area table instead of
                    # searching all points for every (nx, ny).  Same points, same statistics.
                    _bin_i, _bin_ierr, _bin_mon = window_bin_2d(
                        Databox_kari[4,:], Monitorbox_kari, state['N_mcu'],
                        Databox_kari[0,:]/state['NU1'], Databox_kari[1,:]/state['NV1'],
                        state['QU'][:-1]-dU, state['QU'][1:]+dU, state['QV'][:-1]-dV, state['QV'][1:]+dV)
                    state['I'][ne] = _bin_i*ssf1
                    state['Ierr'][ne] = _bin_ierr*abs(ssf1)
                    state['Imon'][ne] = _bin_mon
                    # background may use its own smoothing width
                    _sb_bin_i, _sb_bin_ierr, _ = window_bin_2d(
                        sb_Databox_kari[4,:], sb_Monitorbox_kari, state['N_mcu'],
                        sb_Databox_kari[0,:]/state['NU1'], sb_Databox_kari[1,:]/state['NV1'],
                        state['QU'][:-1]-sb_dU, state['QU'][1:]+sb_dU, state['QV'][:-1]-sb_dV, state['QV'][1:]+sb_dV)
                    state['sb_I'][ne] = _sb_bin_i*ssf2
                    state['sb_Ierr'][ne] = _sb_bin_ierr*abs(ssf2)

                    state['I'] = np.where(np.isfinite(state['I']), state['I'], np.nan)
                    state['Ierr'] = np.where(np.isfinite(state['Ierr']), state['Ierr'], np.nan)
                    state['sb_I'] = np.where(np.isfinite(state['sb_I']), state['sb_I'], np.nan)
                    state['sb_Ierr'] = np.where(np.isfinite(state['sb_Ierr']), state['sb_Ierr'], np.nan)

                    # プログレスバー (確定的)。エネルギー毎にステータスが進む
                    var2=var2+1
                    state['pb2']["value"] = var2
                    state['pb2'].update()
                # nanから数値を引くことはできない。nanを0にする
                I_trans=np.nan_to_num(state['I'], nan=0)-np.nan_to_num(state['sb_I'], nan=0)
                # nanから数値を引くことはできない。nanを0にする
                Ierr_trans=np.sqrt(np.square(np.nan_to_num(state['Ierr'], nan=0))+np.square(np.nan_to_num(state['sb_Ierr'], nan=0)))

                if sbtype2.get()==0:
                    # 差し引き後に両方の要素でnan値であった部分をnan値にする。
                    I_trans[np.isnan(state['I']) & np.isnan(state['sb_I'])] = np.nan
                    Ierr_trans[np.isnan(state['Ierr']) & np.isnan(state['sb_Ierr'])] = np.nan
                elif sbtype2.get()==1:
                    # 差し引き後にFGもしくはBGの要素でnan値であった部分をnan値にする。
                    I_trans[np.isnan(state['I']) | np.isnan(state['sb_I'])] = np.nan
                    Ierr_trans[np.isnan(state['Ierr']) | np.isnan(state['sb_Ierr'])] = np.nan

                state['I']=I_trans
                state['Ierr']=Ierr_trans

        else:# background fileがない場合
            if dEfg==0 and dU==0 and dV==0:#smoothing処理をしない場合
                for ne in range(len(state['energylist'])):
                    # 条件を満たすインデックスを取得。まずエネルギーが一致している部分を取り出す。このときエネルギートランスファートレランスを考慮する。
                    # Ind_e = (list(zip(*np.where(databox[3,:] == energylist[ne]))))
                    ind_e = np.flatnonzero(((state['energylist'][ne]-E_T) <= state['databox'][3,:]) & (state['databox'][3,:] < (state['energylist'][ne]+E_T)))
                    if ind_e.size == 0: # 空行列の時
                        state['energylist'][ne] = state['energylist'][ne]
                    else: # 空行列でない時
                        state['energylist'][ne] = np.mean(state['databox'][3,ind_e])

                    # プログレスバー (確定的)。エネルギー毎にステータスが進む
                    var2=var2+1
                    state['pb2']["value"] = var2
                    state['pb2'].update()

                # databoxとsb_databoxの処理
                state['I'], state['Ierr'], state['Imon'] = bin_single_crystal_data(state['databox'], state['monitorbox'], state['N_mcu'], state['NV1'], state['NU1'], state['energylist'], state['QV'], state['QU'], return_monitor=True)
                state['I']=ssf1*state['I']
                state['Ierr']=ssf1*state['Ierr']

                state['I'] = np.where(np.isfinite(state['I']), state['I'], np.nan)
                state['Ierr'] = np.where(np.isfinite(state['Ierr']), state['Ierr'], np.nan)

            # smoothing処理をする場合
            else:
                # メッシュの中にデータを入れていく。
                for ne in range(len(state['energylist'])):
                    # 条件を満たすインデックスを取得。まずエネルギーが一致している部分を取り出す。このときエネルギートランスファートレランスを考慮する。
                    Databox_kari=None
                    Ind_e = None
                    # Ind_e = (list(zip(*np.where(databox[3,:] == energylist[ne]))))
                    ind_e = np.flatnonzero(((state['energylist'][ne]-E_T-dEfg) <= state['databox'][3,:]) & (state['databox'][3,:] < (state['energylist'][ne]+E_T+dEfg)))
                    if ind_e.size == 0:
                        state['energylist'][ne] = state['energylist'][ne]
                    else:
                        state['energylist'][ne] = np.mean(state['databox'][3,ind_e])

                    Ind_e = ind_e
                    Databox_kari = state['databox'][:,Ind_e]
                    Monitorbox_kari = state['monitorbox'][Ind_e]
                    # Windowed (smoothed) binning: every window QU[nx]-dU < U <= QU[nx+1]+dU,
                    # QV[ny]-dV < V <= QV[ny+1]+dV is read from a summed-area table instead of
                    # searching all points for every (nx, ny).  Same points, same statistics.
                    _bin_i, _bin_ierr, _bin_mon = window_bin_2d(
                        Databox_kari[4,:], Monitorbox_kari, state['N_mcu'],
                        Databox_kari[0,:]/state['NU1'], Databox_kari[1,:]/state['NV1'],
                        state['QU'][:-1]-dU, state['QU'][1:]+dU, state['QV'][:-1]-dV, state['QV'][1:]+dV)
                    state['I'][ne] = _bin_i*ssf1
                    state['Ierr'][ne] = _bin_ierr*abs(ssf1)
                    state['Imon'][ne] = _bin_mon

                    #I = np.where(np.isfinite(I), I, np.nan)
                    #Ierr = np.where(np.isfinite(Ierr), Ierr, np.nan)
                    #sb_I = np.where(np.isfinite(sb_I), sb_I, np.nan)
                    #sb_Ierr = np.where(np.isfinite(sb_Ierr), sb_Ierr, np.nan)

                    # プログレスバー (確定的)。エネルギー毎にステータスが進む
                    var2=var2+1
                    state['pb2']["value"] = var2
                    state['pb2'].update()


    elif CSX.get()==2:# χ(q,w), kf/ki
        if state.get('sb_databox') is not None:#バックグラウンドファイルがあった場合。
            # smoothing処理をしない場合
            if dEfg==0 and dU==0 and dV==0 and dEbg==0 and sb_dU==0 and sb_dV==0:#smoothing処理をしない場合
                for ne in range(len(state['energylist'])):
                    # 条件を満たすインデックスを取得。まずエネルギーが一致している部分を取り出す。このときエネルギートランスファートレランスを考慮する。
                    # Ind_e = (list(zip(*np.where(databox[3,:] == energylist[ne]))))
                    ind_e = np.flatnonzero(((state['energylist'][ne]-E_T) <= state['databox'][3,:]) & (state['databox'][3,:] < (state['energylist'][ne]+E_T)))
                    if ind_e.size == 0: # 空行列の時
                        state['energylist'][ne] = state['energylist'][ne]
                    else: # 空行列でない時
                        state['energylist'][ne] = np.mean(state['databox'][3,ind_e])

                # databoxとsb_databoxの処理
                state['I'], state['Ierr'], state['Imon'] = bin_single_crystal_data(state['databox'], state['monitorbox'], state['N_mcu'], state['NV1'], state['NU1'], state['energylist'], state['QV'], state['QU'], return_monitor=True)
                state['sb_I'], state['sb_Ierr'] = bin_single_crystal_data(state['sb_databox'], state['sb_monitorbox'], state['N_mcu'], state['NV1'], state['NU1'], state['energylist'], state['QV'], state['QU'])

                for ne in range(len(state['energylist'])):
                    # Detailed-balance correction for chi'': use the same
                    # factor for both positive and negative energy transfer.
                    # For E < 0, ssf is negative, making chi'' odd in E.
                    ssf1 = 1 - math.exp(
                        -11.60497 * state['energylist'][ne] / float(sb_txt2.get())
                    )
                    state['I'][ne,:,:] = ssf1 * state['I'][ne,:,:]
                    state['Ierr'][ne,:,:] = abs(ssf1) * state['Ierr'][ne,:,:]

                    ssf2 = 1 - math.exp(
                        -11.60497 * state['energylist'][ne] / float(sb_txt3.get())
                    )
                    state['sb_I'][ne,:,:] = ssf2 * state['sb_I'][ne,:,:]
                    state['sb_Ierr'][ne,:,:] = abs(ssf2) * state['sb_Ierr'][ne,:,:]
                    # プログレスバー (確定的)。エネルギー毎にステータスが進む
                    var2=var2+1
                    state['pb2']["value"] = var2
                    state['pb2'].update()

                state['I'] = np.where(np.isfinite(state['I']), state['I'], np.nan)
                state['Ierr'] = np.where(np.isfinite(state['Ierr']), state['Ierr'], np.nan)
                state['sb_I'] = np.where(np.isfinite(state['sb_I']), state['sb_I'], np.nan)
                state['sb_Ierr'] = np.where(np.isfinite(state['sb_Ierr']), state['sb_Ierr'], np.nan)

                # nanから数値を引くことはできない。nanを0にする
                I_trans=np.nan_to_num(state['I'], nan=0)-np.nan_to_num(state['sb_I'], nan=0)
                # nanから数値を引くことはできない。nanを0にする
                Ierr_trans=np.sqrt(np.square(np.nan_to_num(state['Ierr'], nan=0))+np.square(np.nan_to_num(state['sb_Ierr'], nan=0)))

                if sbtype2.get()==0:
                    # 差し引き後に両方の要素でnan値であった部分をnan値にする。
                    I_trans[np.isnan(state['I']) & np.isnan(state['sb_I'])] = np.nan
                    Ierr_trans[np.isnan(state['Ierr']) & np.isnan(state['sb_Ierr'])] = np.nan
                elif sbtype2.get()==1:
                    # 差し引き後にFGもしくはBGの要素でnan値であった部分をnan値にする。
                    I_trans[np.isnan(state['I']) | np.isnan(state['sb_I'])] = np.nan
                    Ierr_trans[np.isnan(state['Ierr']) | np.isnan(state['sb_Ierr'])] = np.nan

                state['I']=I_trans
                state['Ierr']=Ierr_trans

            else:# smoothing処理を行う場合
                # メッシュの中にデータを入れていく。
                for ne in range(len(state['energylist'])):
                    # 条件を満たすインデックスを取得。まずエネルギーが一致している部分を取り出す。このときエネルギートランスファートレランスを考慮する。
                    Databox_kari=None
                    Ind_e = None
                    sb_Databox_kari=None
                    sb_Ind_e = None
                    # Ind_e = (list(zip(*np.where(databox[3,:] == energylist[ne]))))
                    ind_e = np.flatnonzero(((state['energylist'][ne]-E_T-dEfg) <= state['databox'][3,:]) & (state['databox'][3,:] < (state['energylist'][ne]+E_T+dEfg)))
                    sb_ind_e = np.flatnonzero(((state['energylist'][ne]-E_T-dEbg) <= state['sb_databox'][3,:]) & (state['sb_databox'][3,:] < (state['energylist'][ne]+E_T+dEbg)))
                    if ind_e.size == 0:
                        state['energylist'][ne] = state['energylist'][ne]
                    else:
                        state['energylist'][ne] = np.mean(state['databox'][3,ind_e])
                    # Same detailed-balance factor on both sides of E=0.
                    ssf1 = 1 - math.exp(
                        -11.60497 * state['energylist'][ne] / float(sb_txt2.get())
                    )
                    ssf2 = 1 - math.exp(
                        -11.60497 * state['energylist'][ne] / float(sb_txt3.get())
                    )
                    Ind_e = ind_e
                    sb_Ind_e = sb_ind_e
                    Databox_kari = state['databox'][:,Ind_e]
                    Monitorbox_kari = state['monitorbox'][Ind_e]
                    sb_Databox_kari = state['sb_databox'][:,sb_Ind_e]
                    sb_Monitorbox_kari = state['sb_monitorbox'][sb_Ind_e]
                    # Windowed (smoothed) binning: every window QU[nx]-dU < U <= QU[nx+1]+dU,
                    # QV[ny]-dV < V <= QV[ny+1]+dV is read from a summed-area table instead of
                    # searching all points for every (nx, ny).  Same points, same statistics.
                    _bin_i, _bin_ierr, _bin_mon = window_bin_2d(
                        Databox_kari[4,:], Monitorbox_kari, state['N_mcu'],
                        Databox_kari[0,:]/state['NU1'], Databox_kari[1,:]/state['NV1'],
                        state['QU'][:-1]-dU, state['QU'][1:]+dU, state['QV'][:-1]-dV, state['QV'][1:]+dV)
                    state['I'][ne] = _bin_i*ssf1
                    state['Ierr'][ne] = _bin_ierr*abs(ssf1)
                    state['Imon'][ne] = _bin_mon
                    # background may use its own smoothing width
                    _sb_bin_i, _sb_bin_ierr, _ = window_bin_2d(
                        sb_Databox_kari[4,:], sb_Monitorbox_kari, state['N_mcu'],
                        sb_Databox_kari[0,:]/state['NU1'], sb_Databox_kari[1,:]/state['NV1'],
                        state['QU'][:-1]-sb_dU, state['QU'][1:]+sb_dU, state['QV'][:-1]-sb_dV, state['QV'][1:]+sb_dV)
                    state['sb_I'][ne] = _sb_bin_i*ssf2
                    state['sb_Ierr'][ne] = _sb_bin_ierr*abs(ssf2)

                    state['I'] = np.where(np.isfinite(state['I']), state['I'], np.nan)
                    state['Ierr'] = np.where(np.isfinite(state['Ierr']), state['Ierr'], np.nan)
                    state['sb_I'] = np.where(np.isfinite(state['sb_I']), state['sb_I'], np.nan)
                    state['sb_Ierr'] = np.where(np.isfinite(state['sb_Ierr']), state['sb_Ierr'], np.nan)

                    # プログレスバー (確定的)。エネルギー毎にステータスが進む
                    var2=var2+1
                    state['pb2']["value"] = var2
                    state['pb2'].update()
                # nanから数値を引くことはできない。nanを0にする
                I_trans=np.nan_to_num(state['I'], nan=0)-np.nan_to_num(state['sb_I'], nan=0)
                # nanから数値を引くことはできない。nanを0にする
                Ierr_trans=np.sqrt(np.square(np.nan_to_num(state['Ierr'], nan=0))+np.square(np.nan_to_num(state['sb_Ierr'], nan=0)))

                if sbtype2.get()==0:
                    # 差し引き後に両方の要素でnan値であった部分をnan値にする。
                    I_trans[np.isnan(state['I']) & np.isnan(state['sb_I'])] = np.nan
                    Ierr_trans[np.isnan(state['Ierr']) & np.isnan(state['sb_Ierr'])] = np.nan
                elif sbtype2.get()==1:
                    # 差し引き後にFGもしくはBGの要素でnan値であった部分をnan値にする。
                    I_trans[np.isnan(state['I']) | np.isnan(state['sb_I'])] = np.nan
                    Ierr_trans[np.isnan(state['Ierr']) | np.isnan(state['sb_Ierr'])] = np.nan

                state['I']=I_trans
                state['Ierr']=Ierr_trans

        else:# background fileがない場合
            if dEfg==0 and dU==0 and dV==0:#smoothing処理をしない場合
                for ne in range(len(state['energylist'])):
                    # 条件を満たすインデックスを取得。まずエネルギーが一致している部分を取り出す。このときエネルギートランスファートレランスを考慮する。
                    # Ind_e = (list(zip(*np.where(databox[3,:] == energylist[ne]))))
                    ind_e = np.flatnonzero(((state['energylist'][ne]-E_T) <= state['databox'][3,:]) & (state['databox'][3,:] < (state['energylist'][ne]+E_T)))
                    if ind_e.size == 0: # 空行列の時
                        state['energylist'][ne] = state['energylist'][ne]
                    else: # 空行列でない時
                        state['energylist'][ne] = np.mean(state['databox'][3,ind_e])

                # databoxとsb_databoxの処理
                state['I'], state['Ierr'], state['Imon'] = bin_single_crystal_data(state['databox'], state['monitorbox'], state['N_mcu'], state['NV1'], state['NU1'], state['energylist'], state['QV'], state['QU'], return_monitor=True)

                for ne in range(len(state['energylist'])):    
                    # Detailed-balance correction for chi''.
                    ssf1 = 1 - math.exp(
                        -11.60497 * state['energylist'][ne] / float(sb_txt2.get())
                    )
                    state['I'][ne,:,:] = ssf1 * state['I'][ne,:,:]
                    state['Ierr'][ne,:,:] = abs(ssf1) * state['Ierr'][ne,:,:]

                    # プログレスバー (確定的)。エネルギー毎にステータスが進む
                    var2=var2+1
                    state['pb2']["value"] = var2
                    state['pb2'].update()

                state['I'] = np.where(np.isfinite(state['I']), state['I'], np.nan)
                state['Ierr'] = np.where(np.isfinite(state['Ierr']), state['Ierr'], np.nan)

            else:#smoothing処理をする場合
                # メッシュの中にデータを入れていく。
                for ne in range(len(state['energylist'])):
                    # 条件を満たすインデックスを取得。まずエネルギーが一致している部分を取り出す。このときエネルギートランスファートレランスを考慮する。
                    Databox_kari=None
                    Ind_e = None
                    # Ind_e = (list(zip(*np.where(databox[3,:] == energylist[ne]))))
                    ind_e = np.flatnonzero(((state['energylist'][ne]-E_T-dEfg) <= state['databox'][3,:]) & (state['databox'][3,:] < (state['energylist'][ne]+E_T+dEfg)))
                    if ind_e.size == 0:
                        state['energylist'][ne] = state['energylist'][ne]
                    else:
                        state['energylist'][ne] = np.mean(state['databox'][3,ind_e])
                    # Same detailed-balance factor on both sides of E=0.
                    ssf1 = 1 - math.exp(
                        -11.60497 * state['energylist'][ne] / float(sb_txt2.get())
                    )
                    ssf2 = 1 - math.exp(
                        -11.60497 * state['energylist'][ne] / float(sb_txt3.get())
                    )
                    Ind_e = ind_e
                    Databox_kari = state['databox'][:,Ind_e]
                    Monitorbox_kari = state['monitorbox'][Ind_e]
                    # Windowed (smoothed) binning: every window QU[nx]-dU < U <= QU[nx+1]+dU,
                    # QV[ny]-dV < V <= QV[ny+1]+dV is read from a summed-area table instead of
                    # searching all points for every (nx, ny).  Same points, same statistics.
                    _bin_i, _bin_ierr, _bin_mon = window_bin_2d(
                        Databox_kari[4,:], Monitorbox_kari, state['N_mcu'],
                        Databox_kari[0,:]/state['NU1'], Databox_kari[1,:]/state['NV1'],
                        state['QU'][:-1]-dU, state['QU'][1:]+dU, state['QV'][:-1]-dV, state['QV'][1:]+dV)
                    state['I'][ne] = _bin_i*ssf1
                    state['Ierr'][ne] = _bin_ierr*abs(ssf1)
                    state['Imon'][ne] = _bin_mon

                    #I = np.where(np.isfinite(I), I, np.nan)
                    #Ierr = np.where(np.isfinite(Ierr), Ierr, np.nan)
                    #sb_I = np.where(np.isfinite(sb_I), sb_I, np.nan)
                    #sb_Ierr = np.where(np.isfinite(sb_Ierr), sb_Ierr, np.nan)

                    # プログレスバー (確定的)。エネルギー毎にステータスが進む
                    var2=var2+1
                    state['pb2']["value"] = var2
                    state['pb2'].update()

    # Keep the energy axis that belongs to the current single-crystal map.
    # state['energylist'] is also used by other modes, so it must not be used
    # later as the implicit axis of state['I'].
    state['map_energylist'] = np.asarray(state['energylist'], dtype=float).copy()

    if state['I'] is not None and state['I'].shape[0] != len(state['map_energylist']):
        raise ValueError(
            "Single-crystal map energy-axis mismatch immediately after data_box(): "
            f"I.shape[0]={state['I'].shape[0]}, "
            f"len(map_energylist)={len(state['map_energylist'])}"
        )
