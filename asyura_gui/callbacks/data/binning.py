from ...callback_runtime import *

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
        state['energylist']=(list(set(state['databox'][3,:])))
        # さらにソートする(元のリストを書き換え)
        state['energylist'].sort()
        # さらにエネルギートランスファーのトレランスを考慮して±E_TmeV以内は同じ数値にする。
        Energylist = [state['energylist'][0]]  # 初めて値を代入

        for i in range(1, (len(state['energylist'])-1)):
            if Energylist[-1] <= state['energylist'][i] and state['energylist'][i] < Energylist[-1] + 2*E_T:
                pass
            else:
                Energylist.append(state['energylist'][i+1])
        # 最後の範囲が記録されないので最後に付け足す。
        if Energylist[-1] < state['energylist'][-1] + 2*E_T:
            pass
        else:
            Energylist.append(state['energylist'][-1])
        # energylistを再構成
        state['energylist']=list(set(Energylist))
        state['energylist'].sort()

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
        if len(state['sbfile_paths'])>0:
            if dEfg==0 and dU==0 and dV==0 and dEbg==0 and sb_dU==0 and sb_dV==0:#smoothing処理をしない場合
                for ne in range(len(state['energylist'])):
                    # 条件を満たすインデックスを取得。まずエネルギーが一致している部分を取り出す。このときエネルギートランスファートレランスを考慮する。
                    # Ind_e = (list(zip(*np.where(databox[3,:] == energylist[ne]))))
                    ind_e = (list(zip(*np.where(((state['energylist'][ne]-E_T) <= state['databox'][3,:]) & (state['databox'][3,:] < (state['energylist'][ne]+E_T))))))
                    if not ind_e: # 空行列の時
                        state['energylist'][ne] = state['energylist'][ne]
                    else: # 空行列でない時
                        state['energylist'][ne] = np.mean(state['databox'][3,ind_e])

                    # プログレスバー (確定的)。エネルギー毎にステータスが進む
                    var2=var2+1
                    state['pb2']["value"] = var2
                    state['pb2'].update()

                # databoxとsb_databoxの処理
                state['I'], state['Ierr'] = bin_single_crystal_data(state['databox'], state['NV1'], state['NU1'], state['energylist'], state['QV'], state['QU'])
                state['I']=ssf1*state['I']
                state['Ierr']=ssf1*state['Ierr']

                state['sb_I'], state['sb_Ierr'] = bin_single_crystal_data(state['sb_databox'], state['NV1'], state['NU1'], state['energylist'], state['QV'], state['QU'])
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
                    ind_e = (list(zip(*np.where(((state['energylist'][ne]-E_T-dEfg) <= state['databox'][3,:]) & (state['databox'][3,:] < (state['energylist'][ne]+E_T+dEfg))))))
                    sb_ind_e = (list(zip(*np.where(((state['energylist'][ne]-E_T-dEbg) <= state['sb_databox'][3,:]) & (state['sb_databox'][3,:] < (state['energylist'][ne]+E_T+dEbg))))))
                    if not ind_e: # 空行列の時
                        state['energylist'][ne] = state['energylist'][ne]
                    else: # 空行列でない時
                        state['energylist'][ne] = np.mean(state['databox'][3,ind_e])

                    Ind_e = list(np.ravel(ind_e))
                    sb_Ind_e = list(np.ravel(sb_ind_e))
                    Databox_kari = state['databox'][:,Ind_e]
                    sb_Databox_kari = state['sb_databox'][:,sb_Ind_e]
                    for nx in range(state['nqu']-1):
                        for ny in range(state['nqv']-1):
                            #pixeld_data=Qvector[0,:][ ( QU[nx] < Qvector[0,:] ) & (Qvector[0,:] <= QU[nx])]
                            #pixeld_data2=Qvector[1,:][ ( QV[ny] < Qvector[1,:] ) & (Qvector[1,:] <= QV[ny])]
                            # 条件を満たすインデックスを取得。
                            ind_x = None
                            Ind_x = None
                            sb_ind_x = None
                            sb_Ind_x = None
                            ind_x = (list(zip(*np.where(( state['QU'][nx]-dU < Databox_kari[0,:]/state['NU1'] ) & (Databox_kari[0,:]/state['NU1'] <= state['QU'][nx+1]+dU) & ( state['QV'][ny]-dV < Databox_kari[1,:]/state['NV1'] ) & ( Databox_kari[1,:]/state['NV1'] <= state['QV'][ny+1]+dV )))))
                            # バックグラウンドは別にsmoothingをかけられる。
                            sb_ind_x = (list(zip(*np.where(( state['QU'][nx]-sb_dU < sb_Databox_kari[0,:]/state['NU1'] ) & (sb_Databox_kari[0,:]/state['NU1'] <= state['QU'][nx+1]+sb_dU) & ( state['QV'][ny]-sb_dV < sb_Databox_kari[1,:]/state['NV1'] ) & ( sb_Databox_kari[1,:]/state['NV1'] <= state['QV'][ny+1]+sb_dV )))))
                            # ind_xが何もない場合はnan値として出力されるから良し
                            # ind_xを1次元化して0の要素を省く。そしてリスト型にして取り出す
                            Ind_x = list(np.ravel(ind_x)[::1])
                            sb_Ind_x = list(np.ravel(sb_ind_x)[::1])
                            # ind_xが[(49, 0)]のように出力されるためInd_xで1次元化する。すると49,0...という１次元配列になるため、2つおきの数値[49]を取ってくるように[::1]を追加

                            # runtimeエラーが出ないように工夫
                            state['I'][ne,ny,nx]=(np.nansum(Databox_kari[4,:][Ind_x]))/len(Ind_x)*ssf1
                            state['Ierr'][ne,ny,nx]=((np.nansum(np.multiply(Databox_kari[5,:][Ind_x],Databox_kari[5,:][Ind_x])))**(1/2))/len(Ind_x)*ssf1
                            state['sb_I'][ne,ny,nx]=(np.nansum(sb_Databox_kari[4,:][sb_Ind_x]))/len(sb_Ind_x)*ssf2
                            state['sb_Ierr'][ne,ny,nx]=((np.nansum(np.multiply(sb_Databox_kari[5,:][sb_Ind_x],sb_Databox_kari[5,:][sb_Ind_x])))**(1/2))/len(sb_Ind_x)*ssf2

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
                    ind_e = (list(zip(*np.where(((state['energylist'][ne]-E_T) <= state['databox'][3,:]) & (state['databox'][3,:] < (state['energylist'][ne]+E_T))))))
                    if not ind_e: # 空行列の時
                        state['energylist'][ne] = state['energylist'][ne]
                    else: # 空行列でない時
                        state['energylist'][ne] = np.mean(state['databox'][3,ind_e])

                    # プログレスバー (確定的)。エネルギー毎にステータスが進む
                    var2=var2+1
                    state['pb2']["value"] = var2
                    state['pb2'].update()

                # databoxとsb_databoxの処理
                state['I'], state['Ierr'] = bin_single_crystal_data(state['databox'], state['NV1'], state['NU1'], state['energylist'], state['QV'], state['QU'])
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
                    ind_e = (list(zip(*np.where(((state['energylist'][ne]-E_T-dEfg) <= state['databox'][3,:]) & (state['databox'][3,:] < (state['energylist'][ne]+E_T+dEfg))))))
                    if not ind_e:
                        state['energylist'][ne] = state['energylist'][ne]
                    else:
                        state['energylist'][ne] = np.mean(state['databox'][3,ind_e])

                    Ind_e = list(np.ravel(ind_e))
                    Databox_kari = state['databox'][:,Ind_e]
                    for nx in range(state['nqu']-1):
                        for ny in range(state['nqv']-1):
                            #pixeld_data=Qvector[0,:][ ( QU[nx] < Qvector[0,:] ) & (Qvector[0,:] <= QU[nx])]
                            #pixeld_data2=Qvector[1,:][ ( QV[ny] < Qvector[1,:] ) & (Qvector[1,:] <= QV[ny])]
                            # 条件を満たすインデックスを取得。
                            ind_x = None
                            Ind_x = None
                            ind_x = (list(zip(*np.where(( state['QU'][nx]-dU < Databox_kari[0,:]/state['NU1'] ) & (Databox_kari[0,:]/state['NU1'] <= state['QU'][nx+1]+dU) & ( state['QV'][ny]-dV < Databox_kari[1,:]/state['NV1'] ) & ( Databox_kari[1,:]/state['NV1'] <= state['QV'][ny+1]+dV )))))
                            # ind_xが何もない場合はnan値として出力されるから良し
                            # ind_xを1次元化して0の要素を省く。そしてリスト型にして取り出す
                            Ind_x = list(np.ravel(ind_x)[::1])
                            # ind_xが[(49, 0)]のように出力されるためInd_xで1次元化する。すると49,0...という１次元配列になるため、2つおきの数値[49]を取ってくるように[::1]を追加

                            # runtimeエラーが出ないように工夫
                            state['I'][ne,ny,nx]=(np.nansum(Databox_kari[4,:][Ind_x]))/len(Ind_x)*ssf1
                            state['Ierr'][ne,ny,nx]=((np.nansum(np.multiply(Databox_kari[5,:][Ind_x],Databox_kari[5,:][Ind_x])))**(1/2))/len(Ind_x)*ssf1
                            #sb_I[ne,ny,nx]=(np.nansum(sb_Databox_kari[4,:][sb_Ind_x]))/len(sb_Ind_x)*ssf2
                            #sb_Ierr[ne,ny,nx]=((np.nansum(np.multiply(sb_Databox_kari[5,:][sb_Ind_x],sb_Databox_kari[5,:][sb_Ind_x])))**(1/2))/len(sb_Ind_x)*ssf2

                    #I = np.where(np.isfinite(I), I, np.nan)
                    #Ierr = np.where(np.isfinite(Ierr), Ierr, np.nan)
                    #sb_I = np.where(np.isfinite(sb_I), sb_I, np.nan)
                    #sb_Ierr = np.where(np.isfinite(sb_Ierr), sb_Ierr, np.nan)

                    # プログレスバー (確定的)。エネルギー毎にステータスが進む
                    var2=var2+1
                    state['pb2']["value"] = var2
                    state['pb2'].update()


    elif CSX.get()==2:# χ(q,w), kf/ki
        if len(state['sbfile_paths'])>0:#バックグラウンドファイルがあった場合。
            # smoothing処理をしない場合
            if dEfg==0 and dU==0 and dV==0 and dEbg==0 and sb_dU==0 and sb_dV==0:#smoothing処理をしない場合
                for ne in range(len(state['energylist'])):
                    # 条件を満たすインデックスを取得。まずエネルギーが一致している部分を取り出す。このときエネルギートランスファートレランスを考慮する。
                    # Ind_e = (list(zip(*np.where(databox[3,:] == energylist[ne]))))
                    ind_e = (list(zip(*np.where(((state['energylist'][ne]-E_T) <= state['databox'][3,:]) & (state['databox'][3,:] < (state['energylist'][ne]+E_T))))))
                    if not ind_e: # 空行列の時
                        state['energylist'][ne] = state['energylist'][ne]
                    else: # 空行列でない時
                        state['energylist'][ne] = np.mean(state['databox'][3,ind_e])

                # databoxとsb_databoxの処理
                state['I'], state['Ierr'] = bin_single_crystal_data(state['databox'], state['NV1'], state['NU1'], state['energylist'], state['QV'], state['QU'])
                state['sb_I'], state['sb_Ierr'] = bin_single_crystal_data(state['sb_databox'], state['NV1'], state['NU1'], state['energylist'], state['QV'], state['QU'])

                for ne in range(len(state['energylist'])):
                    if state['energylist'][ne]>=0:
                        ssf1=(1-math.exp(-11.60497*(state['energylist'][ne])/float(sb_txt2.get())))
                        state['I'][ne,:,:]=ssf1*state['I'][ne,:,:]
                        state['Ierr'][ne,:,:]=ssf1*state['Ierr'][ne,:,:]
                        ssf2=(1-math.exp(-11.60497*(state['energylist'][ne])/float(sb_txt3.get())))
                        state['sb_I'][ne,:,:]=ssf2*state['sb_I'][ne,:,:]
                        state['sb_Ierr'][ne,:,:]=ssf2*state['sb_Ierr'][ne,:,:]
                    else:
                        ssf1=(math.exp(11.60497*-(state['energylist'][ne])/float(sb_txt2.get()))-1)
                        state['I'][ne,:,:]=ssf1*state['I'][ne,:,:]
                        state['Ierr'][ne,:,:]=ssf1*state['Ierr'][ne,:,:]
                        ssf2=(math.exp(11.60497*-(state['energylist'][ne])/float(sb_txt3.get()))-1)
                        state['sb_I'][ne,:,:]=ssf2*state['sb_I'][ne,:,:]
                        state['sb_Ierr'][ne,:,:]=ssf2*state['sb_Ierr'][ne,:,:]
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
                    ind_e = (list(zip(*np.where(((state['energylist'][ne]-E_T-dEfg) <= state['databox'][3,:]) & (state['databox'][3,:] < (state['energylist'][ne]+E_T+dEfg))))))
                    sb_ind_e = (list(zip(*np.where(((state['energylist'][ne]-E_T-dEbg) <= state['sb_databox'][3,:]) & (state['sb_databox'][3,:] < (state['energylist'][ne]+E_T+dEbg))))))
                    if not ind_e:
                        state['energylist'][ne] = state['energylist'][ne]
                    else:
                        state['energylist'][ne] = np.mean(state['databox'][3,ind_e])
                    if state['energylist'][ne]>=0:
                        ssf1=(1-math.exp(-11.60497*(state['energylist'][ne])/float(sb_txt2.get())))
                        ssf2=(1-math.exp(-11.60497*(state['energylist'][ne])/float(sb_txt3.get())))
                    else:
                        ssf1=(math.exp(11.60497*-(state['energylist'][ne])/float(sb_txt2.get()))-1)
                        ssf2=(math.exp(11.60497*-(state['energylist'][ne])/float(sb_txt3.get()))-1)
                    Ind_e = list(np.ravel(ind_e))
                    sb_Ind_e = list(np.ravel(sb_ind_e))
                    Databox_kari = state['databox'][:,Ind_e]
                    sb_Databox_kari = state['sb_databox'][:,sb_Ind_e]
                    for nx in range(state['nqu']-1):
                        for ny in range(state['nqv']-1):
                            #pixeld_data=Qvector[0,:][ ( QU[nx] < Qvector[0,:] ) & (Qvector[0,:] <= QU[nx])]
                            #pixeld_data2=Qvector[1,:][ ( QV[ny] < Qvector[1,:] ) & (Qvector[1,:] <= QV[ny])]
                            # 条件を満たすインデックスを取得。
                            ind_x = None
                            Ind_x = None
                            sb_ind_x = None
                            sb_Ind_x = None
                            ind_x = (list(zip(*np.where(( state['QU'][nx]-dU < Databox_kari[0,:]/state['NU1'] ) & (Databox_kari[0,:]/state['NU1'] <= state['QU'][nx+1]+dU) & ( state['QV'][ny]-dV < Databox_kari[1,:]/state['NV1'] ) & ( Databox_kari[1,:]/state['NV1'] <= state['QV'][ny+1]+dV )))))
                            # バックグラウンドは別にsmoothingをかけられる。
                            sb_ind_x = (list(zip(*np.where(( state['QU'][nx]-sb_dU < sb_Databox_kari[0,:]/state['NU1'] ) & (sb_Databox_kari[0,:]/state['NU1'] <= state['QU'][nx+1]+sb_dU) & ( state['QV'][ny]-sb_dV < sb_Databox_kari[1,:]/state['NV1'] ) & ( sb_Databox_kari[1,:]/state['NV1'] <= state['QV'][ny+1]+sb_dV )))))
                            # ind_xが何もない場合はnan値として出力されるから良し
                            # ind_xを1次元化して0の要素を省く。そしてリスト型にして取り出す
                            Ind_x = list(np.ravel(ind_x)[::1])
                            sb_Ind_x = list(np.ravel(sb_ind_x)[::1])
                            # ind_xが[(49, 0)]のように出力されるためInd_xで1次元化する。すると49,0...という１次元配列になるため、2つおきの数値[49]を取ってくるように[::1]を追加
                            # runtimeエラーが出ないように工夫
                            state['I'][ne,ny,nx]=(np.nansum(Databox_kari[4,:][Ind_x]))/len(Ind_x)*ssf1
                            state['Ierr'][ne,ny,nx]=((np.nansum(np.multiply(Databox_kari[5,:][Ind_x],Databox_kari[5,:][Ind_x])))**(1/2))/len(Ind_x)*ssf1
                            state['sb_I'][ne,ny,nx]=(np.nansum(sb_Databox_kari[4,:][sb_Ind_x]))/len(sb_Ind_x)*ssf2
                            state['sb_Ierr'][ne,ny,nx]=((np.nansum(np.multiply(sb_Databox_kari[5,:][sb_Ind_x],sb_Databox_kari[5,:][sb_Ind_x])))**(1/2))/len(sb_Ind_x)*ssf2

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
                    ind_e = (list(zip(*np.where(((state['energylist'][ne]-E_T) <= state['databox'][3,:]) & (state['databox'][3,:] < (state['energylist'][ne]+E_T))))))
                    if not ind_e: # 空行列の時
                        state['energylist'][ne] = state['energylist'][ne]
                    else: # 空行列でない時
                        state['energylist'][ne] = np.mean(state['databox'][3,ind_e])

                # databoxとsb_databoxの処理
                state['I'], state['Ierr'] = bin_single_crystal_data(state['databox'], state['NV1'], state['NU1'], state['energylist'], state['QV'], state['QU'])

                for ne in range(len(state['energylist'])):    
                    if state['energylist'][ne]>=0:
                        ssf1=(1-math.exp(-11.60497*(state['energylist'][ne])/float(sb_txt2.get())))
                        state['I'][ne,:,:]=ssf1*state['I'][ne,:,:]
                        state['Ierr'][ne,:,:]=ssf1*state['Ierr'][ne,:,:]
                    else:
                        ssf1=(math.exp(11.60497*-(state['energylist'][ne])/float(sb_txt2.get()))-1)
                        state['I'][ne,:,:]=ssf1*state['I'][ne,:,:]
                        state['Ierr'][ne,:,:]=ssf1*state['Ierr'][ne,:,:]

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
                    ind_e = (list(zip(*np.where(((state['energylist'][ne]-E_T-dEfg) <= state['databox'][3,:]) & (state['databox'][3,:] < (state['energylist'][ne]+E_T+dEfg))))))
                    if not ind_e:
                        state['energylist'][ne] = state['energylist'][ne]
                    else:
                        state['energylist'][ne] = np.mean(state['databox'][3,ind_e])
                    if state['energylist'][ne]>=0:
                        ssf1=(1-math.exp(-11.60497*(state['energylist'][ne])/float(sb_txt2.get())))
                        ssf2=(1-math.exp(-11.60497*(state['energylist'][ne])/float(sb_txt3.get())))
                    else:
                        ssf1=(math.exp(11.60497*-(state['energylist'][ne])/float(sb_txt2.get()))-1)
                        ssf2=(math.exp(11.60497*-(state['energylist'][ne])/float(sb_txt3.get()))-1)
                    Ind_e = list(np.ravel(ind_e))
                    Databox_kari = state['databox'][:,Ind_e]
                    for nx in range(state['nqu']-1):
                        for ny in range(state['nqv']-1):
                            #pixeld_data=Qvector[0,:][ ( QU[nx] < Qvector[0,:] ) & (Qvector[0,:] <= QU[nx])]
                            #pixeld_data2=Qvector[1,:][ ( QV[ny] < Qvector[1,:] ) & (Qvector[1,:] <= QV[ny])]
                            # 条件を満たすインデックスを取得。
                            ind_x = None
                            Ind_x = None
                            ind_x = (list(zip(*np.where(( state['QU'][nx]-dU < Databox_kari[0,:]/state['NU1'] ) & (Databox_kari[0,:]/state['NU1'] <= state['QU'][nx+1]+dU) & ( state['QV'][ny]-dV < Databox_kari[1,:]/state['NV1'] ) & ( Databox_kari[1,:]/state['NV1'] <= state['QV'][ny+1]+dV )))))
                            # ind_xが何もない場合はnan値として出力されるから良し
                            # ind_xを1次元化して0の要素を省く。そしてリスト型にして取り出す
                            Ind_x = list(np.ravel(ind_x)[::1])
                            # ind_xが[(49, 0)]のように出力されるためInd_xで1次元化する。すると49,0...という１次元配列になるため、2つおきの数値[49]を取ってくるように[::1]を追加

                            # runtimeエラーが出ないように工夫
                            state['I'][ne,ny,nx]=(np.nansum(Databox_kari[4,:][Ind_x]))/len(Ind_x)*ssf1
                            state['Ierr'][ne,ny,nx]=((np.nansum(np.multiply(Databox_kari[5,:][Ind_x],Databox_kari[5,:][Ind_x])))**(1/2))/len(Ind_x)*ssf1
                            #sb_I[ne,ny,nx]=(np.nansum(sb_Databox_kari[4,:][sb_Ind_x]))/len(sb_Ind_x)*ssf2
                            #sb_Ierr[ne,ny,nx]=((np.nansum(np.multiply(sb_Databox_kari[5,:][sb_Ind_x],sb_Databox_kari[5,:][sb_Ind_x])))**(1/2))/len(sb_Ind_x)*ssf2

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
