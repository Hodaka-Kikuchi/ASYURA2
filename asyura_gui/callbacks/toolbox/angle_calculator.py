from ...callback_runtime import *

def tta_calc(env):
    state = env.get('state')
    txt1 = env.get('txt1')
    txt2 = env.get('txt2')
    txt3 = env.get('txt3')
    txt4 = env.get('txt4')
    txt5 = env.get('txt5')
    txt6 = env.get('txt6')
    txt_s1_2 = env.get('txt_s1_2')
    txt_s2_2 = env.get('txt_s2_2')
    txt_s3_2 = env.get('txt_s3_2')
    txt_s4_2f = env.get('txt_s4_2f')
    txt_s4_2hw = env.get('txt_s4_2hw')
    txt_s5_2 = env.get('txt_s5_2')
    txt_s6_2 = env.get('txt_s6_2')
    txt_s7_2 = env.get('txt_s7_2')
    #エラーが起きた時にわかりやすいように最初に2thetaの欄をデリートする
    txt_s5_2.delete(0,tk.END)
    txt_s6_2.delete(0,tk.END)
    # 入力した値を取り込む
    la=float(txt1.get())
    lb=float(txt2.get())
    lc=float(txt3.get())
    lal=float(txt4.get())
    lbe=float(txt5.get())
    lga=float(txt6.get())
    cal_h=float(txt_s1_2.get())
    cal_k=float(txt_s2_2.get())
    cal_l=float(txt_s3_2.get())
    ef=float(txt_s4_2f.get())
    hw=float(txt_s4_2hw.get())
    ei=hw+ef

    # Numerical calculation is kept outside the GUI layer.
    state['Nhkl'], state['dhkl'] = reciprocal_q_and_d(
        la, lb, lc, lal, lbe, lga, cal_h, cal_k, cal_l
    )
    tta = tas_scattering_angle_deg(state['Nhkl'], ei, ef)
    #2theta欄に入力
    txt_s5_2.insert(0,f"{tta:.4f}")
    #Q欄に入力
    txt_s6_2.insert(0,f"{state['Nhkl']:.4f}")
    #d欄に入力
    txt_s7_2.insert(0,f"{state['dhkl']:.4f}")
