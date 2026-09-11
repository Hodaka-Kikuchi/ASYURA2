from ...callback_runtime import *

def time_estimate(env):
    CSPT = env.get('CSPT')
    FE_x = env.get('FE_x')
    FE_y = env.get('FE_y')
    i = env.get('i')
    txt15 = env.get('txt15')
    txt_s1 = env.get('txt_s1')
    txt_s1_1 = env.get('txt_s1_1')
    txt_s2 = env.get('txt_s2')
    txt_s2_1 = env.get('txt_s2_1')
    txt_s3 = env.get('txt_s3')
    txt_s3_1 = env.get('txt_s3_1')
    txt_s4 = env.get('txt_s4')
    txt_s4_1 = env.get('txt_s4_1')
    txt_s5 = env.get('txt_s5')
    txt_s5_1 = env.get('txt_s5_1')
    txt_s6 = env.get('txt_s6')
    txt_s6_1 = env.get('txt_s6_1')
    txt_s7 = env.get('txt_s7')
    txt_s8 = env.get('txt_s8')
    txt_s9 = env.get('txt_s9')
    txt_teh = env.get('txt_teh')
    txt_tem = env.get('txt_tem')
    #単結晶の場合
    if CSPT.get()==0:
        a2_min = float(txt_s1.get())
        a2_inc = float(txt_s2.get())
        a2_max = float(txt_s3.get())
        c2_min = float(txt_s4.get())
        c2_inc = float(txt_s5.get())
        c2_max = float(txt_s6.get())
        hw_min = float(txt_s7.get())
        hw_inc = float(txt_s8.get())
        hw_max = float(txt_s9.get())

        # incの指定を0にしたら1つだけ計算するようにする
        if a2_inc == 0 and c2_inc == 0:
            n_a2 = 1
            a2 = np.array([a2_min])
            n_c2 = 1
            c2 = np.array([c2_min])

        elif a2_inc == 0:
            n_a2 = 1
            a2 = np.array([a2_min])
            n_c2=round((c2_max-c2_min)/c2_inc+1)
            c2=np.zeros((n_c2))
            for i in range(n_c2):
                c2[i] = c2_min + c2_inc * i

        elif c2_inc == 0:
            n_c2 = 1
            c2 = np.array([c2_min])
            n_a2=round((a2_max-a2_min)/a2_inc+1)
            a2=np.zeros((n_a2))
            for j in range(n_a2):
                a2[j] = a2_min + a2_inc * j

        elif a2_inc != 0 and c2_inc != 0:
            # a2とc2のsimulationする数
            n_a2=round((a2_max-a2_min)/a2_inc+1)
            n_c2=round((c2_max-c2_min)/c2_inc+1)
            a2=np.zeros((n_a2))
            c2=np.zeros((n_c2))
            for j in range(n_a2):
                a2[j] = a2_min + a2_inc * j
            for i in range(n_c2):
                c2[i] = c2_min + c2_inc * i

        if hw_inc == 0:
            n_hw = 1
            hw = np.array([hw_min])
            # 線形補間関数を作成
            interp_func = interp1d(FE_x, FE_y, kind='linear', fill_value='extrapolate')
            # ターゲットXに対する補間値を計算
            cps = interp_func(hw)

            mcu = float(txt15.get())
            # elatic positionでのcps=2580.47577333
            TE = mcu * 2580.47577333 / cps * n_a2 * n_c2

            sum_TE=np.sum(TE)

            # 60で割った商と余りを計算
            hour, min = divmod(sum_TE, 60)

            # ボックスに出力
            txt_teh.delete(0,tk.END)
            txt_teh.insert(0,int(hour))

            # ボックスに出力
            txt_tem.delete(0,tk.END)
            txt_tem.insert(0,int(min))

        else:
            n_hw = round((hw_max-hw_min)/hw_inc+1)
            hw=np.zeros((n_hw))
            cps=np.zeros((n_hw))
            TE=np.zeros((n_hw))
            for k in range(n_hw):
                hw[k] = hw_min + hw_inc * k
                # 線形補間関数を作成
                interp_func = interp1d(FE_x, FE_y, kind='linear', fill_value='extrapolate')
                # ターゲットXに対する補間値を計算
                cps[k] = interp_func(hw[k])

                mcu = float(txt15.get())
                # elatic positionでのcps=2580.47577333
                TE[k] = mcu * 2580.47577333 / cps[k] * n_a2 * n_c2

            sum_TE=np.sum(TE)

            # 60で割った商と余りを計算
            hour, min = divmod(sum_TE, 60)

            # ボックスに出力
            txt_teh.delete(0,tk.END)
            txt_teh.insert(0,int(hour))

            # ボックスに出力
            txt_tem.delete(0,tk.END)
            txt_tem.insert(0,int(min))

    #粉末の場合
    if CSPT.get()==1:
        a2_min = float(txt_s1_1.get())
        a2_inc = float(txt_s2_1.get())
        a2_max = float(txt_s3_1.get())
        hw_min = float(txt_s4_1.get())
        hw_inc = float(txt_s5_1.get())
        hw_max = float(txt_s6_1.get())
        if a2_inc == 0 and hw_inc == 0:
            n_a2 = 1
            a2 = np.array([a2_min])
            n_hw = 1
            hw = np.array([hw_min])

            # 線形補間関数を作成
            interp_func = interp1d(FE_x, FE_y, kind='linear', fill_value='extrapolate')
            # ターゲットXに対する補間値を計算
            cps = interp_func(hw)

            mcu = float(txt15.get())
            # elatic positionでのcps=2580.47577333
            TE = mcu * 2580.47577333 / cps * n_a2

            sum_TE=np.sum(TE)

            # 60で割った商と余りを計算
            hour, min = divmod(sum_TE, 60)

            # ボックスに出力
            txt_teh.delete(0,tk.END)
            txt_teh.insert(0,int(hour))

            # ボックスに出力
            txt_tem.delete(0,tk.END)
            txt_tem.insert(0,int(min))

        elif a2_inc == 0:
            n_a2 = 1
            a2 = np.array([a2_min])
            n_hw = round((hw_max-hw_min)/hw_inc+1)
            hw=np.zeros((n_hw))
            for j in range(n_hw):
                hw[j] = hw_min + hw_inc * j

            # 線形補間関数を作成
            interp_func = interp1d(FE_x, FE_y, kind='linear', fill_value='extrapolate')
            # ターゲットXに対する補間値を計算
            cps = interp_func(hw)

            mcu = float(txt15.get())
            # elatic positionでのcps=2580.47577333
            TE = mcu * 2580.47577333 / cps * n_a2

            sum_TE=np.sum(TE)

            # 60で割った商と余りを計算
            hour, min = divmod(sum_TE, 60)

            # ボックスに出力
            txt_teh.delete(0,tk.END)
            txt_teh.insert(0,int(hour))

            # ボックスに出力
            txt_tem.delete(0,tk.END)
            txt_tem.insert(0,int(min))

        elif hw_inc == 0:
            n_a2 = round((a2_max-a2_min)/a2_inc+1)
            a2=np.zeros((n_a2))
            for i in range(n_a2):
                a2[i] = a2_min + a2_inc * i
            n_hw = 1
            hw = np.array([hw_min])

            # 線形補間関数を作成
            interp_func = interp1d(FE_x, FE_y, kind='linear', fill_value='extrapolate')
            # ターゲットXに対する補間値を計算
            cps = interp_func(hw)

            mcu = float(txt15.get())
            # elatic positionでのcps=2580.47577333
            TE = mcu * 2580.47577333 / cps * n_a2

            sum_TE=np.sum(TE)

            # 60で割った商と余りを計算
            hour, min = divmod(sum_TE, 60)

            # ボックスに出力
            txt_teh.delete(0,tk.END)
            txt_teh.insert(0,int(hour))

            # ボックスに出力
            txt_tem.delete(0,tk.END)
            txt_tem.insert(0,int(min))

        elif a2_inc != 0 and hw_inc != 0:
            # a2とhwのsimulationする数
            n_a2=round((a2_max-a2_min)/a2_inc+1)
            n_hw=round((hw_max-hw_min)/hw_inc+1)
            a2=np.zeros((n_a2))
            hw=np.zeros((n_hw))
            cps=np.zeros((n_hw))
            TE=np.zeros((n_hw))
            for i in range(n_a2):
                a2[i] = a2_min + a2_inc * i
            for j in range(n_hw):
                hw[j] = hw_min + hw_inc * j
                # 線形補間関数を作成
                interp_func = interp1d(FE_x, FE_y, kind='linear', fill_value='extrapolate')
                # ターゲットXに対する補間値を計算
                cps[j] = interp_func(hw[j])

                mcu = float(txt15.get())
                # elatic positionでのcps=2580.47577333
                TE[j] = mcu * 2580.47577333 / cps[j] * n_a2

            sum_TE=np.sum(TE)

            # 60で割った商と余りを計算
            hour, min = divmod(sum_TE, 60)

            # ボックスに出力
            txt_teh.delete(0,tk.END)
            txt_teh.insert(0,int(hour))

            # ボックスに出力
            txt_tem.delete(0,tk.END)
            txt_tem.insert(0,int(min))
