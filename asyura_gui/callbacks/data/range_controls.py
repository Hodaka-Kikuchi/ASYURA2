from ...callback_runtime import *

def set_range(env):
    i = env.get('i')
    sbListbox = env.get('sbListbox')
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
    # 小数点第３位を四捨五入。float(format(a, '.2f'))±0.01
    txt22.delete(0,tk.END)
    txt23.delete(0,tk.END)

    txt22.insert(0, round(np.nanmin(state['databox'][3, :]), 3))
    txt23.insert(0, round(np.nanmax(state['databox'][3, :]), 3))

    # step sizeはもし、値が入っていれば消さない
    if txt24.get()=="":
        txt24.delete(0,tk.END)
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

        txt24.insert(0, round(estep+0.005, 3))

    txt16.delete(0,tk.END)
    txt17.delete(0,tk.END)
    txt19.delete(0,tk.END)
    txt20.delete(0,tk.END)

    # hwの最大値からq間隔の最大値を求める。
    ki_norm=((3.635+7)/2.072)**(1/2)
    kf_norm=((3.635)/2.072)**(1/2)
    q_1=(ki_norm**2+kf_norm**2-2*ki_norm*kf_norm*math.cos(math.radians(56)))**(1/2)
    q_2=(ki_norm**2+kf_norm**2-2*ki_norm*kf_norm*math.cos(math.radians(54)))**(1/2)
    dqx=format(float(abs(q_2-q_1)/state['NU1']), '.2f')
    dqy=format(float(abs(q_2-q_1)/state['NV1']), '.2f')

    # 値が入っている場合は変更しない。
    if txt18.get()=="":
        txt18.delete(0,tk.END)
        txt18.insert(0,dqx)
    if txt21.get()=="":
        txt21.delete(0,tk.END)
        txt21.insert(0,dqy)

    # defaultでδU,δVを自動入力する。正直個人的にはいらないと思ってる。
    """
    if state.get('sb_databox') is not None:
        bgt_txt2.delete(0,tk.END)
        bgt_txt2.insert(0,dqx)
        bgt_txt3.delete(0,tk.END)
        bgt_txt3.insert(0,dqy)
    """

    if sbListbox.size() != 0:# background fileが有る場合
        if np.nanmin(state['databox'][0, :])<=np.nanmin(state['sb_databox'][0, :]):
            txt16.insert(0, round(np.nanmin(state['databox'][0, :] / state['NU1']) - 0.01, 2))
        else:
            txt16.insert(0, round(np.nanmin(state['sb_databox'][0, :] / state['NU1']) - 0.01, 2))
        if np.nanmax(state['databox'][0, :])>=np.nanmax(state['sb_databox'][0, :]):
            txt17.insert(0, round(np.nanmax(state['databox'][0, :] / state['NU1']) + 0.01, 2))
        else:
            txt17.insert(0, round(np.nanmax(state['sb_databox'][0, :] / state['NU1']) + 0.01, 2))
        if np.nanmin(state['databox'][1, :])<=np.nanmin(state['sb_databox'][1, :]):
            txt19.insert(0, round(np.nanmin(state['databox'][1, :] / state['NV1']) - 0.01, 2))
        else:
            txt19.insert(0, round(np.nanmin(state['sb_databox'][1, :] / state['NV1']) - 0.01, 2))
        if np.nanmax(state['databox'][1, :])>=np.nanmax(state['sb_databox'][1, :]):
            txt20.insert(0, round(np.nanmax(state['databox'][1, :] / state['NV1']) + 0.01, 2))
        else:
            txt20.insert(0, round(np.nanmax(state['sb_databox'][1, :] / state['NV1']) + 0.01, 2))
    elif sbListbox.size() == 0:# background fileが無い場合
        txt16.insert(0, round(np.nanmin(state['databox'][0, :] / state['NU1']) - 0.01, 2))
        txt17.insert(0, round(np.nanmax(state['databox'][0, :] / state['NU1']) + 0.01, 2))
        txt19.insert(0, round(np.nanmin(state['databox'][1, :] / state['NV1']) - 0.01, 2))
        txt20.insert(0, round(np.nanmax(state['databox'][1, :] / state['NV1']) + 0.01, 2))

def gs_clear(env):
    scale_s_Emax_txt = env.get('scale_s_Emax_txt')
    scale_s_Emin_txt = env.get('scale_s_Emin_txt')
    scale_s_Imax_txt = env.get('scale_s_Imax_txt')
    scale_s_Imin_txt = env.get('scale_s_Imin_txt')
    scale_s_Umax_txt = env.get('scale_s_Umax_txt')
    scale_s_Umin_txt = env.get('scale_s_Umin_txt')
    scale_s_Vmax_txt = env.get('scale_s_Vmax_txt')
    scale_s_Vmin_txt = env.get('scale_s_Vmin_txt')
    scale_s_Emin_txt.delete(0,tk.END)
    scale_s_Emax_txt.delete(0,tk.END)
    scale_s_Umin_txt.delete(0,tk.END)
    scale_s_Umax_txt.delete(0,tk.END)
    scale_s_Vmin_txt.delete(0,tk.END)
    scale_s_Vmax_txt.delete(0,tk.END)
    scale_s_Imin_txt.delete(0,tk.END)
    scale_s_Imax_txt.delete(0,tk.END)

def gs_auto(env):
    scale_s_Emax_txt = env.get('scale_s_Emax_txt')
    scale_s_Emin_txt = env.get('scale_s_Emin_txt')
    scale_s_Imax_txt = env.get('scale_s_Imax_txt')
    scale_s_Imin_txt = env.get('scale_s_Imin_txt')
    scale_s_Umax_txt = env.get('scale_s_Umax_txt')
    scale_s_Umin_txt = env.get('scale_s_Umin_txt')
    scale_s_Vmax_txt = env.get('scale_s_Vmax_txt')
    scale_s_Vmin_txt = env.get('scale_s_Vmin_txt')
    state = env.get('state')
    scale_s_Emin_txt.delete(0,tk.END)
    scale_s_Emax_txt.delete(0,tk.END)
    if round(state['energylist'][0], 2) == round(state['energylist'][-1], 2):
        scale_s_Emin_txt.insert(0, round(state['energylist'][0]-(state['ef_tol']), 2))
        scale_s_Emax_txt.insert(0, round(state['energylist'][-1]+(state['ef_tol']), 2))
    else:
        scale_s_Emin_txt.insert(0, round(state['energylist'][0], 2))
        scale_s_Emax_txt.insert(0, round(state['energylist'][-1], 2))
    scale_s_Umin_txt.delete(0,tk.END)
    scale_s_Umin_txt.insert(0, round(np.min(state['QU']),2))
    scale_s_Umax_txt.delete(0,tk.END)
    scale_s_Umax_txt.insert(0, round(np.max(state['QU']),2))
    scale_s_Vmin_txt.delete(0,tk.END)
    scale_s_Vmin_txt.insert(0, round(np.min(state['QV']),2))
    scale_s_Vmax_txt.delete(0,tk.END)
    scale_s_Vmax_txt.insert(0, round(np.max(state['QV']),2))
    scale_s_Imin_txt.delete(0,tk.END)
    scale_s_Imax_txt.delete(0,tk.END)
    # カラーバースケール。空欄の場合は平均値を出力するようにする。
    if np.nanmean(state['I']) >= 0:
        scale_s_Imax_txt.insert(0,round(np.nanmean(state['I']),1))
        scale_s_Imin_txt.insert(0,0)
    elif np.nanmean(state['I']) < 0:
        scale_s_Imin_txt.insert(0,round(np.nanmean(state['I']),1))
        scale_s_Imax_txt.insert(0,np.abs(round(np.nanmean(state['I']),1)))

def gs_clear2(env):
    scale_s_Emax_txt_2 = env.get('scale_s_Emax_txt_2')
    scale_s_Emin_txt_2 = env.get('scale_s_Emin_txt_2')
    scale_s_Imax_txt_2 = env.get('scale_s_Imax_txt_2')
    scale_s_Imin_txt_2 = env.get('scale_s_Imin_txt_2')
    scale_s_Umax_txt_2 = env.get('scale_s_Umax_txt_2')
    scale_s_Umin_txt_2 = env.get('scale_s_Umin_txt_2')
    scale_s_Vmax_txt_2 = env.get('scale_s_Vmax_txt_2')
    scale_s_Vmin_txt_2 = env.get('scale_s_Vmin_txt_2')
    scale_s_Emin_txt_2.delete(0,tk.END)
    scale_s_Emax_txt_2.delete(0,tk.END)
    scale_s_Umin_txt_2.delete(0,tk.END)
    scale_s_Umax_txt_2.delete(0,tk.END)
    scale_s_Vmin_txt_2.delete(0,tk.END)
    scale_s_Vmax_txt_2.delete(0,tk.END)
    scale_s_Imin_txt_2.delete(0,tk.END)
    scale_s_Imax_txt_2.delete(0,tk.END)

def gs_auto2(env):
    scale_s_Emax_txt_2 = env.get('scale_s_Emax_txt_2')
    scale_s_Emin_txt_2 = env.get('scale_s_Emin_txt_2')
    scale_s_Imax_txt_2 = env.get('scale_s_Imax_txt_2')
    scale_s_Imin_txt_2 = env.get('scale_s_Imin_txt_2')
    scale_s_Umax_txt_2 = env.get('scale_s_Umax_txt_2')
    scale_s_Umin_txt_2 = env.get('scale_s_Umin_txt_2')
    scale_s_Vmax_txt_2 = env.get('scale_s_Vmax_txt_2')
    scale_s_Vmin_txt_2 = env.get('scale_s_Vmin_txt_2')
    state = env.get('state')

    if state.get('sb_databox') is not None:
        I_min = round(np.min(state['databox'][4, :]),2) - round(np.min(state['sb_databox'][4, :]),2)
    else:
        I_min = round(np.min(state['databox'][4, :]),2)
    if state.get('sb_databox') is not None:#平均値を出力
        I_max = round((np.mean(state['databox'][4, :]) + np.mean(state['sb_databox'][4, :])) / 2 , 2)
    else:
        I_max = round(np.mean(state['databox'][4, :]) , 2)
    hw_min = round(np.min(state['databox'][3, :]),2)
    hw_max = round(np.max(state['databox'][3, :]),2)
    U_min = round(np.min(state['databox'][0, :]/state['NU1']),2)
    U_max = round(np.max(state['databox'][0, :]/state['NU1']),2)
    V_min = round(np.min(state['databox'][1, :]/state['NV1']),2)
    V_max = round(np.max(state['databox'][1, :]/state['NV1']),2)

    scale_s_Emin_txt_2.delete(0,tk.END)
    scale_s_Emax_txt_2.delete(0,tk.END)
    scale_s_Emin_txt_2.insert(0,hw_min)
    scale_s_Emax_txt_2.insert(0,hw_max)

    scale_s_Umin_txt_2.delete(0,tk.END)
    scale_s_Umin_txt_2.insert(0, U_min)
    scale_s_Umax_txt_2.delete(0,tk.END)
    scale_s_Umax_txt_2.insert(0, U_max)
    scale_s_Vmin_txt_2.delete(0,tk.END)
    scale_s_Vmin_txt_2.insert(0, V_min)
    scale_s_Vmax_txt_2.delete(0,tk.END)
    scale_s_Vmax_txt_2.insert(0, V_max)
    scale_s_Imin_txt_2.delete(0,tk.END)
    scale_s_Imax_txt_2.delete(0,tk.END)
    scale_s_Imin_txt_2.insert(0,I_min)
    scale_s_Imax_txt_2.insert(0,I_max)

def threshold_auto(env):
    state = env.get('state')
    txt_dhw = env.get('txt_dhw')
    txt_pcs = env.get('txt_pcs')
    txt_rQ = env.get('txt_rQ')
    txt_rQ.delete(0,tk.END)
    txt_dhw.delete(0,tk.END)
    txt_pcs.delete(0,tk.END)

    # q空間での近傍半径 dq
    ki_norm = ((3.635 + 7) / 2.072) ** 0.5
    kf_norm = (3.635 / 2.072) ** 0.5
    q_1 = (ki_norm**2 + kf_norm**2 - 2*ki_norm*kf_norm*np.cos(np.radians(54)))**0.5
    q_2 = (ki_norm**2 + kf_norm**2 - 2*ki_norm*kf_norm*np.cos(np.radians(56)))**0.5
    dq = abs(q_2 - q_1)

    txt_rQ.insert(0, round(3*dq,2))
    txt_dhw.insert(0, round(state['ef_tol'],4))
    txt_pcs.insert(0, 5)

def range_auto_3D(env):
    state = env.get('state')
    txt_vr_I1 = env.get('txt_vr_I1')
    txt_vr_I2 = env.get('txt_vr_I2')
    txt_vr_U1 = env.get('txt_vr_U1')
    txt_vr_U2 = env.get('txt_vr_U2')
    txt_vr_V1 = env.get('txt_vr_V1')
    txt_vr_V2 = env.get('txt_vr_V2')
    txt_vr_hw1 = env.get('txt_vr_hw1')
    txt_vr_hw2 = env.get('txt_vr_hw2')
    txt_vr_I1.delete(0,tk.END)
    txt_vr_I2.delete(0,tk.END)
    txt_vr_hw1.delete(0,tk.END)
    txt_vr_hw2.delete(0,tk.END)
    txt_vr_U1.delete(0,tk.END)
    txt_vr_U2.delete(0,tk.END)
    txt_vr_V1.delete(0,tk.END)
    txt_vr_V2.delete(0,tk.END)

    if state.get('sb_databox') is not None:
        txt_vr_I1.insert(0, round(np.min(state['databox'][4, :]),2) - round(np.min(state['sb_databox'][4, :]),2))
    else:
        txt_vr_I1.insert(0, round(np.min(state['databox'][4, :]),2))
    if state.get('sb_databox') is not None:
        txt_vr_I2.insert(0, round(np.max(state['databox'][4, :]),2) - round(np.max(state['sb_databox'][4, :]),2))
    else:
        txt_vr_I2.insert(0, round(np.max(state['databox'][4, :]),2))
    txt_vr_hw1.insert(0, round(np.min(state['databox'][3, :]),2))
    txt_vr_hw2.insert(0, round(np.max(state['databox'][3, :]),2))
    txt_vr_U1.insert(0, round(np.min(state['databox'][0, :]/state['NU1']),2))
    txt_vr_U2.insert(0, round(np.max(state['databox'][0, :]/state['NU1']),2))
    txt_vr_V1.insert(0, round(np.min(state['databox'][1, :]/state['NV1']),2))
    txt_vr_V2.insert(0, round(np.max(state['databox'][1, :]/state['NV1']),2))
