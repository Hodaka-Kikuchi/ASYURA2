from ...callback_runtime import *

def pow_data_box(env):
    CSX = env.get('CSX')
    bgt_txt1 = env.get('bgt_txt1')
    bgt_txt6 = env.get('bgt_txt6')
    fgt_txt1 = env.get('fgt_txt1')
    fgt_txt4 = env.get('fgt_txt4')
    hwp_nan = env.get('hwp_nan')
    i = env.get('i')
    sb_txt1 = env.get('sb_txt1')
    sb_txt2 = env.get('sb_txt2')
    sb_txt3 = env.get('sb_txt3')
    sbtype2 = env.get('sbtype2')
    state = env.get('state')
    txt01_p = env.get('txt01_p')
    txt02_p = env.get('txt02_p')
    txt03_p = env.get('txt03_p')
    txt04_p = env.get('txt04_p')
    txt05_p = env.get('txt05_p')
    txt06_p = env.get('txt06_p')
    #energyの異なる値を取り出す(重複した数値を消してリスト化する)
    # shared variables are stored in state
    if hwp_nan.get()==0:# hw cellを指定していない場合。
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
        if Energylist[-1] == state['energylist'][-1]:
            pass
        else:
            Energylist.append(state['energylist'][-1])
        # energylistを再構成
        state['energylist']=list(set(Energylist))
        state['energylist'].sort()

    if hwp_nan.get()==1:# hw cellを指定している場合。
        Ebin = float(txt06_p.get())
        Emin = float(txt04_p.get())-Ebin/2
        Emax = float(txt05_p.get())+Ebin/2

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

    # shared variables are stored in state
    var3 = 0 # プログレスバーの変数
    state['pb3']["maximum"] = len(state['energylist']) # プログレスバーの最大値
    state['pb3']["value"] = 0
    state['pb3'].update()

    #qとhwのメッシュを用意する
    qbin = float(txt03_p.get())
    qmin = float(txt01_p.get())-qbin/2
    qmax = float(txt02_p.get())+qbin/2

    # smoothing
    if fgt_txt4.get()=="":
        dQ = 0
        #fgt_txt4.insert(0,qbin)
    else:
        dQ = (float(fgt_txt4.get())-qbin)/2

    if bgt_txt6.get()=="":
        sb_dQ = 0
    else:
        sb_dQ = (float(bgt_txt6.get())-qbin)/2

    if qmin > qmax:
        return
    elif qmin > qmax:
        return
    elif qbin < 0:
        return
    # shared variables are stored in state
    state['nq']=round((qmax-qmin)/qbin+1)

    # shared variables are stored in state
    state['Q']=np.zeros((state['nq']))
    for i in range(state['nq']):
        state['Q'][i] = qmin + qbin * i

    hw_num = int(len(state['energylist'])+1)
    # shared variables are stored in state
    state['hwlist_p']=np.zeros(hw_num)
    #hwが1つのときの例外処理として装置分解能の範囲を出力するようにする
    if hw_num==2:
        state['hwlist_p'][0] = float(state['energylist'][0]-(state['ef_tol']+0.005))
        state['hwlist_p'][1] = float(state['energylist'][-1]+(state['ef_tol']+0.005))
    else:
        state['hwlist_p'][0] = float(state['energylist'][0])-(float(state['energylist'][1])-float(state['energylist'][0]))
        state['hwlist_p'][-1] = float(state['energylist'][-1])+(float(state['energylist'][-1])-float(state['energylist'][-2]))

        #hwlist4[0] = float(energylist[0])-(float(energylist[1])-float(energylist[0]))
        #hwlist4[-1] = float(energylist[-1])+(float(energylist[-1])-float(energylist[-2]))

        for ne in range(hw_num-2):
            state['hwlist_p'][ne+1] = (float(state['energylist'][ne])+float(state['energylist'][ne+1]))/2

    # 強度とエラーバーのセルを用意する。2次元の行列
    # shared variables are stored in state
    state['Ipow'] = None
    state['Ipow_err'] = None
    state['sb_Ipow'] = None
    state['sb_Ipow_err'] = None
    state['Ipow']=np.zeros((len(state['energylist']),state['nq']-1))
    state['Ipow_err']=np.zeros((len(state['energylist']),state['nq']-1))
    state['sb_Ipow']=np.zeros((len(state['energylist']),state['nq']-1))
    state['sb_Ipow_err']=np.zeros((len(state['energylist']),state['nq']-1))

    # shared variables are stored in state
    state['Q2']=np.zeros(state['nq']-1)

    # メッシュの中にデータを入れていく。
    # S(q,w)の場合
    if CSX.get()==1:# S(q,w), kf/ki
        ssf1=1
        ssf2=float(sb_txt1.get())
        if len(state['sbfile_paths'])>0:
            for ne in range(len(state['energylist'])):
                # エネルギートランスファーのトレランスを読み込む。
                # 条件を満たすインデックスを取得。まずエネルギーが一致している部分を取り出す
                Databox_kari = None
                sb_Databox_kari=None
                ind_e = (list(zip(*np.where(((state['energylist'][ne]-E_T-dEfg) <= state['databox'][3,:]) & (state['databox'][3,:] < (state['energylist'][ne]+E_T+dEfg))))))
                sb_ind_e = (list(zip(*np.where(((state['energylist'][ne]-E_T-dEbg) <= state['sb_databox'][3,:]) & (state['sb_databox'][3,:] < (state['energylist'][ne]+E_T+dEbg))))))
                if not ind_e:
                    state['energylist'][ne] = state['energylist'][ne]
                else:
                    state['energylist'][ne] = np.mean(state['databox'][3,ind_e])

                Ind_e = list(np.ravel(ind_e))
                Databox_kari = state['databox'][:,Ind_e]
                sb_Ind_e = list(np.ravel(sb_ind_e))
                sb_Databox_kari = state['sb_databox'][:,sb_Ind_e]

                for npow in range(state['nq']-1):
                    state['Q2'][npow] = (state['Q'][npow]+state['Q'][npow+1])/2
                    #pixeld_data=Qvector[0,:][ ( QU[nx] < Qvector[0,:] ) & (Qvector[0,:] <= QU[nx])]
                    #pixeld_data2=Qvector[1,:][ ( QV[ny] < Qvector[1,:] ) & (Qvector[1,:] <= QV[ny])]
                    # Qセルの条件を満たすインデックスを取得。
                    ind_q = (list(zip(*np.where(( state['Q'][npow]-dQ < Databox_kari[2,:] ) & (Databox_kari[2,:] <= state['Q'][npow+1]+dQ)))))
                    sb_ind_q = (list(zip(*np.where(( state['Q'][npow]-sb_dQ < sb_Databox_kari[2,:] ) & (sb_Databox_kari[2,:] <= state['Q'][npow+1]+sb_dQ)))))

                    # ind_qが何もない場合はnan値として出力されるから良し
                    # ind_qを1次元化して0の要素を省く。そしてリスト型にして取り出す
                    Ind_q = list(np.ravel(ind_q)[::1])
                    # ind_xが何もない場合はnan値として出力されるから良し
                    state['Ipow'][ne,npow]=(np.nanmean(Databox_kari[4,:][Ind_q]))*ssf1
                    state['Ipow_err'][ne,npow]=((np.nansum(np.multiply(Databox_kari[5,:][Ind_q],Databox_kari[5,:][Ind_q])))**(1/2))/(len(Ind_q))*ssf1
                    sb_Ind_q = list(np.ravel(sb_ind_q)[::1])
                    # ind_xが何もない場合はnan値として出力されるから良し
                    state['sb_Ipow'][ne,npow]=(np.nanmean(sb_Databox_kari[4,:][sb_Ind_q]))*ssf2
                    state['sb_Ipow_err'][ne,npow]=((np.nansum(np.multiply(sb_Databox_kari[5,:][sb_Ind_q],sb_Databox_kari[5,:][sb_Ind_q])))**(1/2))/(len(sb_Ind_q))*ssf2

                state['Ipow'] = np.where(np.isfinite(state['Ipow']), state['Ipow'], np.nan)
                state['Ipow_err'] = np.where(np.isfinite(state['Ipow_err']), state['Ipow_err'], np.nan)
                state['sb_Ipow'] = np.where(np.isfinite(state['sb_Ipow']), state['sb_Ipow'], np.nan)
                state['sb_Ipow_err'] = np.where(np.isfinite(state['sb_Ipow_err']), state['sb_Ipow_err'], np.nan)
                # プログレスバー (確定的)。エネルギー毎にステータスが進む
                var3=var3+1
                state['pb3']["value"] = var3
                state['pb3'].update()
            # nanから数値を引くことはできない。nanを0にする
            Ipow_trans=np.nan_to_num(state['Ipow'], nan=0)-np.nan_to_num(state['sb_Ipow'], nan=0)
            # nanから数値を引くことはできない。nanを0にする
            Ipow_err_trans=np.sqrt(np.square(np.nan_to_num(state['Ipow_err'], nan=0))+np.square(np.nan_to_num(state['sb_Ipow_err'], nan=0)))

            if sbtype2.get()==0:
                # 差し引き後に両方の要素でnan値であった部分をnan値にする。
                Ipow_trans[np.isnan(state['Ipow']) & np.isnan(state['sb_Ipow'])] = np.nan
                Ipow_err_trans[np.isnan(state['Ipow_err']) & np.isnan(state['sb_Ipow_err'])] = np.nan
            elif sbtype2.get()==1:
                # 差し引き後にFGもしくはBGの要素でnan値であった部分をnan値にする。
                Ipow_trans[np.isnan(state['Ipow']) | np.isnan(state['sb_Ipow'])] = np.nan
                Ipow_err_trans[np.isnan(state['Ipow_err']) | np.isnan(state['sb_Ipow_err'])] = np.nan

            state['Ipow']=Ipow_trans
            state['Ipow_err']=Ipow_err_trans

        else:# バックグラウンドファイルが無い場合
            for ne in range(len(state['energylist'])):
                # エネルギートランスファーのトレランスを読み込む。
                # 条件を満たすインデックスを取得。まずエネルギーが一致している部分を取り出す
                Databox_kari = None
                ind_e = (list(zip(*np.where(((state['energylist'][ne]-E_T-dEfg) <= state['databox'][3,:]) & (state['databox'][3,:] < (state['energylist'][ne]+E_T+dEfg))))))
                if not ind_e:
                    state['energylist'][ne] = state['energylist'][ne]
                else:
                    state['energylist'][ne] = np.mean(state['databox'][3,ind_e])
                Ind_e = list(np.ravel(ind_e))

                Databox_kari = state['databox'][:,Ind_e]
                for npow in range(state['nq']-1):
                    state['Q2'][npow] = (state['Q'][npow]+state['Q'][npow+1])/2
                    #pixeld_data=Qvector[0,:][ ( QU[nx] < Qvector[0,:] ) & (Qvector[0,:] <= QU[nx])]
                    #pixeld_data2=Qvector[1,:][ ( QV[ny] < Qvector[1,:] ) & (Qvector[1,:] <= QV[ny])]
                    # Qセルの条件を満たすインデックスを取得。
                    ind_q = (list(zip(*np.where(( state['Q'][npow]-dQ < Databox_kari[2,:] ) & (Databox_kari[2,:] <= state['Q'][npow+1]+dQ)))))
                    # ind_qが何もない場合はnan値として出力されるから良し
                    # ind_qを1次元化して0の要素を省く。そしてリスト型にして取り出す
                    Ind_q = list(np.ravel(ind_q)[::1])
                    # ind_xが何もない場合はnan値として出力されるから良し
                    state['Ipow'][ne,npow]=(np.nanmean(Databox_kari[4,:][Ind_q]))*ssf1
                    state['Ipow_err'][ne,npow]=((np.nansum(np.multiply(Databox_kari[5,:][Ind_q],Databox_kari[5,:][Ind_q])))**(1/2))/(len(Ind_q))*ssf1
                    #sb_Ind_q = list(np.ravel(sb_ind_q)[::1])
                    # ind_xが何もない場合はnan値として出力されるから良し
                    #sb_Ipow[ne,npow]=(np.nanmean(sb_Databox_kari[4,:][sb_Ind_q]))
                    #sb_Ipow_err[ne,npow]=((np.nansum(np.multiply(sb_Databox_kari[5,:][sb_Ind_q],sb_Databox_kari[5,:][sb_Ind_q])))**(1/2))/(len(sb_Ind_q))

                #Ipow = np.where(np.isfinite(Ipow), Ipow, np.nan)
                #Ipow_err = np.where(np.isfinite(Ipow_err), Ipow_err, np.nan)
                #sb_Ipow = np.where(np.isfinite(sb_Ipow), sb_Ipow, np.nan)
                #sb_Ipow_err = np.where(np.isfinite(sb_Ipow_err), sb_Ipow_err, np.nan)
                # プログレスバー (確定的)。エネルギー毎にステータスが進む
                var3=var3+1
                state['pb3']["value"] = var3
                state['pb3'].update()
    elif CSX.get()==2:# χ(q,w), kf/ki
        if len(state['sbfile_paths'])>0:
            for ne in range(len(state['energylist'])):
                # エネルギートランスファーのトレランスを読み込む。
                # 条件を満たすインデックスを取得。まずエネルギーが一致している部分を取り出す
                Databox_kari = None
                sb_Databox_kari=None
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
                Databox_kari = state['databox'][:,Ind_e]
                sb_Ind_e = list(np.ravel(sb_ind_e))
                sb_Databox_kari = state['sb_databox'][:,sb_Ind_e]

                for npow in range(state['nq']-1):
                    state['Q2'][npow] = (state['Q'][npow]+state['Q'][npow+1])/2
                    #pixeld_data=Qvector[0,:][ ( QU[nx] < Qvector[0,:] ) & (Qvector[0,:] <= QU[nx])]
                    #pixeld_data2=Qvector[1,:][ ( QV[ny] < Qvector[1,:] ) & (Qvector[1,:] <= QV[ny])]
                    # Qセルの条件を満たすインデックスを取得。
                    ind_q = (list(zip(*np.where(( state['Q'][npow]-dQ < Databox_kari[2,:] ) & (Databox_kari[2,:] <= state['Q'][npow+1]+dQ)))))
                    sb_ind_q = (list(zip(*np.where(( state['Q'][npow]-sb_dQ < sb_Databox_kari[2,:] ) & (sb_Databox_kari[2,:] <= state['Q'][npow+1]+sb_dQ)))))

                    # ind_qが何もない場合はnan値として出力されるから良し
                    # ind_qを1次元化して0の要素を省く。そしてリスト型にして取り出す
                    Ind_q = list(np.ravel(ind_q)[::1])
                    # ind_xが何もない場合はnan値として出力されるから良し
                    state['Ipow'][ne,npow]=(np.nanmean(Databox_kari[4,:][Ind_q]))*ssf1
                    state['Ipow_err'][ne,npow]=((np.nansum(np.multiply(Databox_kari[5,:][Ind_q],Databox_kari[5,:][Ind_q])))**(1/2))/(len(Ind_q))*ssf1
                    sb_Ind_q = list(np.ravel(sb_ind_q)[::1])
                    # ind_xが何もない場合はnan値として出力されるから良し
                    state['sb_Ipow'][ne,npow]=(np.nanmean(sb_Databox_kari[4,:][sb_Ind_q]))*ssf2
                    state['sb_Ipow_err'][ne,npow]=((np.nansum(np.multiply(sb_Databox_kari[5,:][sb_Ind_q],sb_Databox_kari[5,:][sb_Ind_q])))**(1/2))/(len(sb_Ind_q))*ssf2

                state['Ipow'] = np.where(np.isfinite(state['Ipow']), state['Ipow'], np.nan)
                state['Ipow_err'] = np.where(np.isfinite(state['Ipow_err']), state['Ipow_err'], np.nan)
                state['sb_Ipow'] = np.where(np.isfinite(state['sb_Ipow']), state['sb_Ipow'], np.nan)
                state['sb_Ipow_err'] = np.where(np.isfinite(state['sb_Ipow_err']), state['sb_Ipow_err'], np.nan)
                # プログレスバー (確定的)。エネルギー毎にステータスが進む
                var3=var3+1
                state['pb3']["value"] = var3
                state['pb3'].update()
            # nanから数値を引くことはできない。nanを0にする
            Ipow_trans=np.nan_to_num(state['Ipow'], nan=0)-np.nan_to_num(state['sb_Ipow'], nan=0)
            # nanから数値を引くことはできない。nanを0にする
            Ipow_err_trans=np.sqrt(np.square(np.nan_to_num(state['Ipow_err'], nan=0))+np.square(np.nan_to_num(state['sb_Ipow_err'], nan=0)))

            if sbtype2.get()==0:
                # 差し引き後に両方の要素でnan値であった部分をnan値にする。
                Ipow_trans[np.isnan(state['Ipow']) & np.isnan(state['sb_Ipow'])] = np.nan
                Ipow_err_trans[np.isnan(state['Ipow_err']) & np.isnan(state['sb_Ipow_err'])] = np.nan
            elif sbtype2.get()==1:
                # 差し引き後にFGもしくはBGの要素でnan値であった部分をnan値にする。
                Ipow_trans[np.isnan(state['Ipow']) | np.isnan(state['sb_Ipow'])] = np.nan
                Ipow_err_trans[np.isnan(state['Ipow_err']) | np.isnan(state['sb_Ipow_err'])] = np.nan

            state['Ipow']=Ipow_trans
            state['Ipow_err']=Ipow_err_trans

        else:# バックグラウンドファイルが無い場合
            for ne in range(len(state['energylist'])):
                # エネルギートランスファーのトレランスを読み込む。
                # 条件を満たすインデックスを取得。まずエネルギーが一致している部分を取り出す
                Databox_kari = None
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
                for npow in range(state['nq']-1):
                    state['Q2'][npow] = (state['Q'][npow]+state['Q'][npow+1])/2
                    #pixeld_data=Qvector[0,:][ ( QU[nx] < Qvector[0,:] ) & (Qvector[0,:] <= QU[nx])]
                    #pixeld_data2=Qvector[1,:][ ( QV[ny] < Qvector[1,:] ) & (Qvector[1,:] <= QV[ny])]
                    # Qセルの条件を満たすインデックスを取得。
                    ind_q = (list(zip(*np.where(( state['Q'][npow]-dQ < Databox_kari[2,:] ) & (Databox_kari[2,:] <= state['Q'][npow+1]+dQ)))))
                    # ind_qが何もない場合はnan値として出力されるから良し
                    # ind_qを1次元化して0の要素を省く。そしてリスト型にして取り出す
                    Ind_q = list(np.ravel(ind_q)[::1])
                    # ind_xが何もない場合はnan値として出力されるから良し
                    state['Ipow'][ne,npow]=(np.nanmean(Databox_kari[4,:][Ind_q]))*ssf1
                    state['Ipow_err'][ne,npow]=((np.nansum(np.multiply(Databox_kari[5,:][Ind_q],Databox_kari[5,:][Ind_q])))**(1/2))/(len(Ind_q))*ssf1
                    #sb_Ind_q = list(np.ravel(sb_ind_q)[::1])
                    # ind_xが何もない場合はnan値として出力されるから良し
                    #sb_Ipow[ne,npow]=(np.nanmean(sb_Databox_kari[4,:][sb_Ind_q]))
                    #sb_Ipow_err[ne,npow]=((np.nansum(np.multiply(sb_Databox_kari[5,:][sb_Ind_q],sb_Databox_kari[5,:][sb_Ind_q])))**(1/2))/(len(sb_Ind_q))

                #Ipow = np.where(np.isfinite(Ipow), Ipow, np.nan)
                #Ipow_err = np.where(np.isfinite(Ipow_err), Ipow_err, np.nan)
                #sb_Ipow = np.where(np.isfinite(sb_Ipow), sb_Ipow, np.nan)
                #sb_Ipow_err = np.where(np.isfinite(sb_Ipow_err), sb_Ipow_err, np.nan)
                # プログレスバー (確定的)。エネルギー毎にステータスが進む
                var3=var3+1
                state['pb3']["value"] = var3
                state['pb3'].update()
