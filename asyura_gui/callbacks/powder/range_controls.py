from ...callback_runtime import *

def p_set_range(env):
    i = env.get('i')
    sbListbox = env.get('sbListbox')
    state = env.get('state')
    txt01_p = env.get('txt01_p')
    txt02_p = env.get('txt02_p')
    txt03_p = env.get('txt03_p')
    txt04_p = env.get('txt04_p')
    txt05_p = env.get('txt05_p')
    txt06_p = env.get('txt06_p')
    # 小数点第３位を四捨五入。float(format(a, '.2f'))±0.01
    txt04_p.delete(0,tk.END)
    txt05_p.delete(0,tk.END)

    txt04_p.insert(0, round(np.nanmin(state['databox'][3, :]), 3))
    txt05_p.insert(0, round(np.nanmax(state['databox'][3, :]), 3))

    # stepサイズを変更しない。
    if txt06_p.get()=="":
        txt06_p.delete(0,tk.END)
        E_T = round(state['ef_tol']+0.005,3)
        # もとのコード
        energylist=(list(set(state['databox'][3,:])))
        # さらにソートする(元のリストを書き換え)
        energylist.sort()
        # さらにエネルギートランスファーのトレランスを考慮して±E_TmeV以内は同じ数値にする。
        Energylist = [energylist[0]]  # 初めて値を代入

        for i in range(1, (len(energylist)-1)):
            if Energylist[-1] <= energylist[i] and energylist[i] < Energylist[-1] + 2*E_T:
                pass
            else:
                Energylist.append(energylist[i+1])
        # 最後の範囲が記録されないので最後に付け足す。
        if Energylist[-1] == energylist[-1]:
            pass
        else:
            Energylist.append(energylist[-1])
        # energylistを再構成
        energylist=list(set(Energylist))
        energylist.sort()

        # 差分の平均値を計算
        estep = np.nanmean(np.diff(energylist))

        txt06_p.insert(0, round(estep+0.005, 3))

    txt01_p.delete(0,tk.END)
    txt02_p.delete(0,tk.END)
    if sbListbox.size() != 0:# background fileが有る場合
        if np.nanmin(state['databox'][2, :])<=np.nanmin(state['sb_databox'][2, :]):
            txt01_p.insert(0, round(np.nanmin(state['databox'][2, :]) - 0.01, 2))
        else:
            txt01_p.insert(0, round(np.nanmin(state['sb_databox'][2, :]) - 0.01, 2))
        if np.nanmax(state['databox'][2, :])<=np.nanmax(state['sb_databox'][2, :]):
            txt02_p.insert(0, round(np.nanmax(state['sb_databox'][2, :]) + 0.01, 2))
        else:
            txt02_p.insert(0, round(np.nanmax(state['databox'][2, :]) + 0.01, 2))
    if sbListbox.size() == 0:# background fileが有る場合
        txt01_p.insert(0, round(np.nanmin(state['databox'][2, :]) - 0.01, 2))
        txt02_p.insert(0, round(np.nanmax(state['databox'][2, :]) + 0.01, 2))

    # 差を求める。
    # hwの最大値からq間隔の最大値を求める。
    ki_norm=((3.635+7)/2.072)**(1/2)
    kf_norm=((3.635)/2.072)**(1/2)
    q_1=(ki_norm**2+kf_norm**2-2*ki_norm*kf_norm*math.cos(math.radians(54)))**(1/2)
    q_2=(ki_norm**2+kf_norm**2-2*ki_norm*kf_norm*math.cos(math.radians(56)))**(1/2)
    dq=format(float(abs(q_2-q_1)), '.2f')

    # step sizeに関しては変更しない。
    if txt03_p.get()=="":
        txt03_p.delete(0,tk.END)
        txt03_p.insert(0,dq)

def gsp_clear(env):
    scale_p_Emax_txt = env.get('scale_p_Emax_txt')
    scale_p_Emin_txt = env.get('scale_p_Emin_txt')
    scale_p_Imax_txt = env.get('scale_p_Imax_txt')
    scale_p_Imin_txt = env.get('scale_p_Imin_txt')
    scale_p_Qmax_txt = env.get('scale_p_Qmax_txt')
    scale_p_Qmin_txt = env.get('scale_p_Qmin_txt')
    scale_p_Emin_txt.delete(0,tk.END)
    scale_p_Emax_txt.delete(0,tk.END)
    scale_p_Qmin_txt.delete(0,tk.END)
    scale_p_Qmax_txt.delete(0,tk.END)
    scale_p_Imin_txt.delete(0,tk.END)
    scale_p_Imax_txt.delete(0,tk.END)

def gsp_auto(env):
    scale_p_Emax_txt = env.get('scale_p_Emax_txt')
    scale_p_Emin_txt = env.get('scale_p_Emin_txt')
    scale_p_Imax_txt = env.get('scale_p_Imax_txt')
    scale_p_Imin_txt = env.get('scale_p_Imin_txt')
    scale_p_Qmax_txt = env.get('scale_p_Qmax_txt')
    scale_p_Qmin_txt = env.get('scale_p_Qmin_txt')
    state = env.get('state')
    scale_p_Emin_txt.delete(0,tk.END)
    scale_p_Emax_txt.delete(0,tk.END)
    if round(state['energylist'][0], 2) == round(state['energylist'][-1], 2):
        scale_p_Emin_txt.insert(0, round(state['energylist'][0]-(state['ef_tol']), 2))
        scale_p_Emax_txt.insert(0, round(state['energylist'][-1]+(state['ef_tol']), 2))
    else:
        scale_p_Emin_txt.insert(0, round(state['energylist'][0], 2))
        scale_p_Emax_txt.insert(0, round(state['energylist'][-1], 2))
    scale_p_Qmin_txt.delete(0,tk.END)
    scale_p_Qmin_txt.insert(0, round(np.min(state['Q']),2))
    scale_p_Qmax_txt.delete(0,tk.END)
    scale_p_Qmax_txt.insert(0, round(np.max(state['Q']),2))
    scale_p_Imin_txt.delete(0,tk.END)
    scale_p_Imax_txt.delete(0,tk.END)
    # カラーバースケール。空欄の場合は平均値を出力するようにする。
    if np.nanmean(state['Ipow']) >= 0:
        scale_p_Imax_txt.insert(0,round(np.nanmean(state['Ipow']),1))
        scale_p_Imin_txt.insert(0,0)
    elif np.nanmean(state['Ipow']) < 0:
        scale_p_Imin_txt.insert(0,round(np.nanmean(state['Ipow']),1))
        scale_p_Imax_txt.insert(0,np.abs(round(np.nanmean(state['Ipow']),1)))
