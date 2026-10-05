from ...callback_runtime import *

from .display_basis import prepare_simu_reciprocal_display

def simu_sc_cE(env):
    i = env.get('i')
    state = env.get('state')
    txt10 = env.get('txt10')
    txt11 = env.get('txt11')
    txt12 = env.get('txt12')
    txt13 = env.get('txt13')
    txt14 = env.get('txt14')
    txt9 = env.get('txt9')
    txt_s1 = env.get('txt_s1')
    txt_s10 = env.get('txt_s10')
    txt_s2 = env.get('txt_s2')
    txt_s3 = env.get('txt_s3')
    txt_s4 = env.get('txt_s4')
    txt_s5 = env.get('txt_s5')
    txt_s6 = env.get('txt_s6')
    txt_s7 = env.get('txt_s7')
    txt_s8 = env.get('txt_s8')
    txt_s9 = env.get('txt_s9')
    txt_ul = env.get('txt_ul')
    txt_vl = env.get('txt_vl')
    _prepare_simu_reciprocal_display = lambda *a, **kw: prepare_simu_reciprocal_display(env, *a, **kw)
    # グラフ文字の取得
    if float(txt9.get())==0:
        ul1 = 0
    elif float(txt9.get())==1:
        ul1 = str(txt_ul.get())
    elif float(txt9.get())==-1:
        ul1 = str('-')+str(txt_ul.get())
    else:
        try:
            number0 = float(txt9.get())
            if number0.is_integer():#整数である
                ul1 = str(int(float(txt9.get())))+str(txt_ul.get())
            else:#整数でない
                ul1 = str(float(txt9.get()))+str(txt_ul.get())
        except ValueError:#整数でない
            pass

    if float(txt10.get())==0:
        ul2 = 0
    elif float(txt10.get())==1:
        ul2 = str(txt_ul.get())
    elif float(txt10.get())==-1:
        ul2 = str('-')+str(txt_ul.get())
    else:
        try:
            number1 = float(txt10.get())
            if number1.is_integer():#整数である
                ul2 = str(int(float(txt10.get())))+str(txt_ul.get())
            else:#整数でない
                ul2 = str(float(txt10.get()))+str(txt_ul.get())
        except ValueError:#整数でない
            pass

    if float(txt11.get())==0:
        ul3 = 0
    elif float(txt11.get())==1:
        ul3 = str(txt_ul.get())
    elif float(txt11.get())==-1:
        ul3 = str('-')+str(txt_ul.get())
    else:
        try:
            number2 = float(txt11.get())
            if number2.is_integer():#整数である
                ul3 = str(int(float(txt11.get())))+str(txt_ul.get())
            else:#整数でない
                ul3 = str(float(txt11.get()))+str(txt_ul.get())
        except ValueError:#整数でない
            pass

    if float(txt12.get())==0:
        vl1 = 0
    elif float(txt12.get())==1:
        vl1 = str(txt_vl.get())
    elif float(txt12.get())==-1:
        vl1 = str('-')+str(txt_vl.get())
    else:
        try:
            number3 = float(txt12.get())
            if number3.is_integer():#整数である
                vl1 = str(int(float(txt12.get())))+str(txt_vl.get())
            else:#整数でない
                vl1 = str(float(txt12.get()))+str(txt_vl.get())
        except ValueError:#整数でない
            pass

    if float(txt13.get())==0:
        vl2 = 0
    elif float(txt13.get())==1:
        vl2 = str(txt_vl.get())
    elif float(txt13.get())==-1:
        vl2 = str('-')+str(txt_vl.get())
    else:
        try:
            number4 = float(txt13.get())
            if number4.is_integer():#整数である
                vl2 = str(int(float(txt13.get())))+str(txt_vl.get())
            else:#整数でない
                vl2 = str(float(txt13.get()))+str(txt_vl.get())
        except ValueError:#整数でない
            pass

    if float(txt14.get())==0:
        vl3 = 0
    elif float(txt14.get())==1:
        vl3 = str(txt_vl.get())
    elif float(txt14.get())==-1:
        vl3 = str('-')+str(txt_vl.get())
    else:
        try:
            number5 = float(txt14.get())
            if number5.is_integer():#整数である
                vl3 = str(int(float(txt14.get())))+str(txt_vl.get())
            else:#整数でない
                vl3 = str(float(txt14.get()))+str(txt_vl.get())
        except ValueError:#整数でない
            pass

    #global Ulabel,Vlabel
    Ulabel = (f"({ul1},{ul2},{ul3})")
    Vlabel = (f"({vl1},{vl2},{vl3})")

    a2_min = float(txt_s1.get())
    a2_inc = float(txt_s2.get())
    a2_max = float(txt_s3.get())
    c2_min = float(txt_s4.get())
    c2_inc = float(txt_s5.get())
    c2_max = float(txt_s6.get())
    hw_min = float(txt_s7.get())
    hw_inc = float(txt_s8.get())
    hw_max = float(txt_s9.get())
    E_simu = float(txt_s10.get())
    #U_simu = float(txt_s11.get())
    #V_simu = float(txt_s12.get())

    # UB + reference reflection based reciprocal-space setup.
    # Old txt7(c2_off) and txt8(Vt) are intentionally not used.
    # shared variables are stored in state
    # shared variables are stored in state
    # shared variables are stored in state
    (state['UBmatrix'], state['u'], state['v'], state['display_ex'], state['display_ey'], state['display_ez'],
     state['NU1'], state['NV1'], state['display_uv_angle'], display_used_angle,
     state['display_v_hkl'], state['display_mode'], display_coeff,
     simu_ref_c2, simu_omega_ref, simu_c2_sign) = \
        _prepare_simu_reciprocal_display()
    state['sign'] = 1.0
    if state['display_mode'] == 'orthogonal-crystallographic' and not np.allclose(state['display_v_hkl'], state['v']):
        Vlabel = _simu_hkl_text(state['display_v_hkl'])

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
        hw = np.array([[hw_min]])
    else:
        n_hw = round((hw_max-hw_min)/hw_inc+1)
        hw=np.zeros((n_hw,1))
        for k in range(n_hw):
            hw[k,0] = hw_min + hw_inc * k

    #検出器の角度
    d_angle=np.linspace(0, 46, 24)

    # C2 is the instrument encoder value.  Reference calibration is applied
    # inside _simu_angles_to_rlu() when C2 is converted to omega.
    C2=np.asarray(c2, dtype=float)

    Qsimu_x = None
    Qsimu_y = None
    Qsimu_x=np.zeros((n_hw,n_a2*n_c2*24))
    Qsimu_y=np.zeros((n_hw,n_a2*n_c2*24))
    Qsimu_d12_x=np.zeros((n_hw,n_a2*n_c2*1))
    Qsimu_d12_y=np.zeros((n_hw,n_a2*n_c2*1))
    A2_max = np.ones((n_hw,1))*a2_max
    A2_min = np.ones((n_hw,1))*a2_min
    A2_inc = np.ones((n_hw,1))*a2_inc
    C2_max = np.ones((n_hw,1))*c2_max
    C2_min = np.ones((n_hw,1))*c2_min
    C2_inc = np.ones((n_hw,1))*c2_inc
    for k in range(n_hw):
        for n in range(n_c2):
            for m in range(n_a2):
                for l in range(24):
                    #A2の絶対値変換
                    A2=d_angle+state['phi']+a2[m];# cover range
                    _sx, _sy, _q3, _hkl3, _res3 = _simu_angles_to_rlu(3.635+float(np.asarray(hw[k]).reshape(-1)[0]), 3.635, C2[n], A2[l], state['UBmatrix'], state['u'], state['display_v_hkl'], state['NU1'], state['NV1'], simu_ref_c2, simu_omega_ref, simu_c2_sign)
                    Qsimu_x[k,l+24*m+24*n_a2*n] = _sx
                    Qsimu_y[k,l+24*m+24*n_a2*n] = _sy
                    # D12は再計算
                    _dx, _dy, _q3d, _hkld, _resd = _simu_angles_to_rlu(3.635+float(np.asarray(hw[k]).reshape(-1)[0]), 3.635, C2[n], A2[11], state['UBmatrix'], state['u'], state['display_v_hkl'], state['NU1'], state['NV1'], simu_ref_c2, simu_omega_ref, simu_c2_sign)
                    Qsimu_d12_x[k,n+n_c2*m] = _dx
                    Qsimu_d12_y[k,n+n_c2*m] = _dy

    # sign flip is unnecessary; orientation is handled by the UB/display basis.

    # 一番近いhwの値を取り出す。浮動小数点数の精度の問題をクリア。
    ind_E = np.abs(hw - E_simu).argmin()

    # 別に格納する。このボタンがクリックされた場合、すべての変数をリセット
    # shared variables are stored in state

    state['list_hw']=hw
    state['list_Qsimu_x']=Qsimu_x
    state['list_Qsimu_y']=Qsimu_y
    state['list_Qsimu_d12_x']=Qsimu_d12_x
    state['list_Qsimu_d12_y']=Qsimu_d12_y
    state['list_A2_max']=A2_max
    state['list_A2_min']=A2_min
    state['list_A2_inc']=A2_inc
    state['list_C2_max']=C2_max
    state['list_C2_min']=C2_min
    state['list_C2_inc']=C2_inc

    # グラフスケールの定義
    xlim_min=np.nanmin(Qsimu_x)
    xlim_max=np.nanmax(Qsimu_x)

    ylim_min=np.nanmin(Qsimu_y)
    ylim_max=np.nanmax(Qsimu_y)

    # グラフを作成
    fig0,ax=plt.subplots()

    # shared variables are stored in state
    # 現在のFigure番号を取得
    state['num_fig_simu_sin'] = plt.gcf().number

    # グラフ内に表示範囲を決定するボックス
    # 最小値と最大値の初期値
    default_xmin = round(xlim_min, 2)
    default_xmax = round(xlim_max, 2)

    default_ymin = round(ylim_min, 2)
    default_ymax = round(ylim_max, 2)

    # テキストボックスを作成して最小値と最大値を設定
    xmin_box = TextBox(plt.axes([0.3, 0.10, 0.08, 0.05]), 'xMin:', initial=str(default_xmin))
    xmax_box = TextBox(plt.axes([0.65, 0.10, 0.08, 0.05]), 'xMax:', initial=str(default_xmax))

    ymin_box = TextBox(plt.axes([0.1, 0.2, 0.08, 0.05]), 'yMin:', initial=str(default_ymin))
    ymax_box = TextBox(plt.axes([0.1, 0.83, 0.08, 0.05]), 'yMax:', initial=str(default_ymax))

    # 最小値と最大値が変更されたときに呼び出される関数
    def update_axis_range(text):
        try:
            xmin_val = float(xmin_box.text)
            xmax_val = float(xmax_box.text)
            ax.set_xlim(xmin_val, xmax_val)
            ymin_val = float(ymin_box.text)
            ymax_val = float(ymax_box.text)
            ax.set_ylim(ymin_val, ymax_val)
            fig0.canvas.draw_idle()
            return xmin_val,xmax_val,ymin_val,ymax_val
        except ValueError:
            pass

    xmin_box.on_submit(update_axis_range)
    xmax_box.on_submit(update_axis_range)
    ymin_box.on_submit(update_axis_range)
    ymax_box.on_submit(update_axis_range)  

    plt.subplots_adjust(bottom=0.25)
    # アスペクト比を変更
    ax.set_aspect(state['NV1']/state['NU1'])
    sa1=ind_E#初期値をセット
    if n_a2!=1:
        ax.text(0.0,1.1,'a2 = %.3f ~ %.3f deg (step %.3f deg)' % (A2_min[ind_E,0],A2_max[ind_E,0],A2_inc[ind_E,0]), transform=ax.transAxes)
    else:
        ax.text(0.0,1.1,'a2 = %.3f deg' %A2_min[ind_E,0], transform=ax.transAxes)

    if n_c2!=1:
        ax.text(0.0,1.05,'c2 = %.3f ~ %.3f deg (step %.3f deg)' % (C2_min[ind_E,0],C2_max[ind_E,0],C2_inc[ind_E,0]), transform=ax.transAxes)
    else:
        ax.text(0.0,1.05,'c2 = %.3f deg' %C2_min[ind_E,0], transform=ax.transAxes)
    ax.text(0.0,1.00,'ℏω = %.3f meV' %hw[ind_E,0], transform=ax.transAxes)
    ax.set_xlabel(str(Ulabel))
    ax.set_ylabel(str(Vlabel))
    ax.scatter(Qsimu_x[ind_E,:], Qsimu_y[ind_E,:],s=10, color = "blue", label="Other detectors")
    ax.scatter(Qsimu_d12_x[ind_E,:], Qsimu_d12_y[ind_E,:],s=10, color = "red", label="D12")
    ax.legend()
    ax.grid()
    ax.set_xlim(xlim_min,xlim_max) #x軸の範囲を指定
    ax.set_ylim(ylim_min,ylim_max) #y軸の範囲を指定
    plt.subplots_adjust(left=0.30, right=0.75, bottom=0.25)  # マージンを調整してグラフを中央に配置
    #plt.tick_params(labelsize=20)
    #横スライドでエネルギートランスファーを変更、縦スライドで強度の最大値を変更
    ax_a = plt.axes([0.3, 0.02, 0.45, 0.04]) #plt.axes([x, y, width, height] ) 
    sli_a1 = wg.Slider(ax_a, 'ℏω', 0, len(hw)-1, valinit=sa1,valstep=1, orientation='horizontal')

    def update1(val):
        ax.clear()

        xmin_val = float(xmin_box.text)
        xmax_val = float(xmax_box.text)
        ymin_val = float(ymin_box.text)
        ymax_val = float(ymax_box.text)

        # アスペクト比を変更
        ax.set_aspect(state['NV1']/state['NU1'])

        sa1 = sli_a1.val
        if n_a2!=1:
            ax.text(0.0,1.1,'a2 = %.3f ~ %.3f deg (step %.3f deg)' % (A2_min[sa1,0],A2_max[sa1,0],A2_inc[sa1,0]), transform=ax.transAxes)
        else:
            ax.text(0.0,1.1,'a2 = %.3f' %A2_min[sa1,0], transform=ax.transAxes)

        if n_c2!=1:
            ax.text(0.0,1.05,'c2 = %.3f ~ %.3f deg (step %.3f deg)' % (C2_min[sa1,0],C2_max[sa1,0],C2_inc[sa1,0]), transform=ax.transAxes)
        else:
            ax.text(0.0,1.05,'c2 = %.3f' %C2_min[sa1,0], transform=ax.transAxes)

        ax.text(0.0,1.00,'ℏω = %.3f meV' %hw[sa1,0], transform=ax.transAxes)
        ax.set_xlabel(str(Ulabel))
        ax.set_ylabel(str(Vlabel))
        ax.scatter(Qsimu_x[sa1,:], Qsimu_y[sa1,:],s=10, color = "blue", label="Other detectors")
        ax.scatter(Qsimu_d12_x[sa1,:], Qsimu_d12_y[sa1,:],s=10, color = "red", label="D12")
        ax.legend()
        ax.grid()
        ax.set_xlim(xmin_val,xmax_val) #x軸の範囲を指定
        ax.set_ylim(ymin_val,ymax_val) #y軸の範囲を指定
        plt.draw()
    # 矢印キーにスライダを対応。上限を超えて表示しないように設定。
    def on_key(event):
        if event.key == 'right':
            new_val_a = min(sli_a1.val + 1, sli_a1.valmax)
            sli_a1.set_val(new_val_a)
        elif event.key == 'left':
            new_val_a = max(sli_a1.val - 1, sli_a1.valmin)
            sli_a1.set_val(new_val_a)
    fig0.canvas.mpl_connect('key_press_event', on_key)

    sli_a1.on_changed(update1)
    plt.show()

def simu_sc_cU(env):
    i = env.get('i')
    state = env.get('state')
    txt10 = env.get('txt10')
    txt11 = env.get('txt11')
    txt12 = env.get('txt12')
    txt13 = env.get('txt13')
    txt14 = env.get('txt14')
    txt9 = env.get('txt9')
    txt_s1 = env.get('txt_s1')
    txt_s11 = env.get('txt_s11')
    txt_s2 = env.get('txt_s2')
    txt_s3 = env.get('txt_s3')
    txt_s4 = env.get('txt_s4')
    txt_s5 = env.get('txt_s5')
    txt_s6 = env.get('txt_s6')
    txt_s7 = env.get('txt_s7')
    txt_s8 = env.get('txt_s8')
    txt_s9 = env.get('txt_s9')
    txt_ul = env.get('txt_ul')
    txt_vl = env.get('txt_vl')
    _prepare_simu_reciprocal_display = lambda *a, **kw: prepare_simu_reciprocal_display(env, *a, **kw)
    a2_min = float(txt_s1.get())
    a2_inc = float(txt_s2.get())
    a2_max = float(txt_s3.get())
    c2_min = float(txt_s4.get())
    c2_inc = float(txt_s5.get())
    c2_max = float(txt_s6.get())
    hw_min = float(txt_s7.get())
    hw_inc = float(txt_s8.get())
    hw_max = float(txt_s9.get())
    #E_simu = float(txt_s10.get())
    U_simu = float(txt_s11.get())
    #V_simu = float(txt_s12.get())

    if float(txt12.get())==0:
        if float(txt9.get())==0:
            vl1 = str('0')
        else:
            vl1 = str(float(txt9.get())*U_simu)
    elif float(txt12.get())==1:
        if float(txt9.get())==0:
            vl1 = str(txt_vl.get())
        else:
            vl1 = str(float(txt9.get())*U_simu) + str('+') + str(txt_vl.get())
    elif float(txt12.get())==-1:
        if float(txt9.get())==0:
            vl1 = str('-')+str(txt_vl.get())
        else:
            vl1 = str(float(txt9.get())*U_simu) + str('-') + str(txt_vl.get())
    else:
        try:
            number0 = float(txt12.get())
            if number0.is_integer():#整数である
                if number0 > 0:
                    vl1 = str(float(txt9.get())*U_simu) + str('+') + str(int(float(txt12.get()))) + str(txt_vl.get())
                elif number0 < 0:
                    vl1 = str(float(txt9.get())*U_simu) + str('-') + str(int(np.abs(float(txt12.get())))) + str(txt_vl.get())
            else:#整数でない
                if number0 > 0:
                    vl1 = str(float(txt9.get())*U_simu) + str('+') + str(float(txt12.get())) + str(txt_vl.get())
                elif number0 < 0:
                    vl1 = str(float(txt9.get())*U_simu) + str('-') + str(float(np.abs(txt12.get()))) + str(txt_vl.get())
        except ValueError:#数値でない
            pass

    if float(txt13.get())==0:
        if float(txt10.get())==0:
            vl2 = str('0')
        else:
            vl2 = str(float(txt10.get())*U_simu)
    elif float(txt13.get())==1:
        if float(txt10.get())==0:
            vl2 = str(txt_vl.get())
        else:
            vl2 = str(float(txt10.get())*U_simu) + str('+') + str(txt_vl.get())
    elif float(txt13.get())==-1:
        if float(txt10.get())==0:
            vl2 = str('-')+str(txt_vl.get())
        else:
            vl2 = str(float(txt10.get())*U_simu) + str('-') + str(txt_vl.get())
    else:
        try:
            number1 = float(txt13.get())
            if number1.is_integer():#整数である
                if number1 > 0:
                    vl2 = str(float(txt10.get())*U_simu) + str('+') + str(int(float(txt13.get()))) + str(txt_vl.get())
                elif number1 < 0:
                    vl2 = str(float(txt10.get())*U_simu) + str('-') + str(int(np.abs(float(txt13.get())))) + str(txt_vl.get())
            else:#整数でない
                if number1 > 0:
                    vl2 = str(float(txt10.get())*U_simu) + str('+') + str(float(txt13.get())) + str(txt_vl.get())
                elif number1 < 0:
                    vl2 = str(float(txt10.get())*U_simu) + str('-') + str(np.abs(float(txt13.get()))) + str(txt_vl.get())
        except ValueError:#数値でない
            pass

    if float(txt14.get())==0:
        if float(txt11.get())==0:
            vl3 = str('0')
        else:
            vl3 = str(float(txt11.get())*U_simu)
    elif float(txt14.get())==1:
        if float(txt11.get())==0:
            vl3 = str(txt_vl.get())
        else:
            vl3 = str(float(txt11.get())*U_simu) + str('+') + str(txt_vl.get())
    elif float(txt14.get())==-1:
        if float(txt11.get())==0:
            vl3 = str('-')+str(txt_vl.get())
        else:
            vl3 = str(float(txt11.get())*U_simu) + str('-') + str(txt_vl.get())
    else:
        try:
            number2 = float(txt14.get())
            if number2.is_integer():#整数である
                if number2 > 0:
                    vl3 = str(float(txt11.get())*U_simu) + str('+') + str(int(float(txt14.get()))) + str(txt_vl.get())
                elif number2 < 0:
                    vl3 = str(float(txt11.get())*U_simu) + str('-') + str(int(np.abs(float(txt14.get())))) + str(txt_vl.get())
            else:#整数でない
                if number2 > 0:
                    vl3 = str(float(txt11.get())*U_simu) + str('+') + str(float(txt14.get())) + str(txt_vl.get())
                elif number2 < 0:
                    vl3 = str(float(txt11.get())*U_simu) + str('-') + str(np.abs(float(txt14.get()))) + str(txt_vl.get())
        except ValueError:#整数でない
            pass

    Vlabel = (f"({vl1},{vl2},{vl3})")

    # UB + reference reflection based reciprocal-space setup.
    # Old txt7(c2_off) and txt8(Vt) are intentionally not used.
    # shared variables are stored in state
    # shared variables are stored in state
    # shared variables are stored in state
    (state['UBmatrix'], state['u'], state['v'], state['display_ex'], state['display_ey'], state['display_ez'],
     state['NU1'], state['NV1'], state['display_uv_angle'], display_used_angle,
     state['display_v_hkl'], state['display_mode'], display_coeff,
     simu_ref_c2, simu_omega_ref, simu_c2_sign) = \
        _prepare_simu_reciprocal_display()
    state['sign'] = 1.0
    if state['display_mode'] == 'orthogonal-crystallographic' and not np.allclose(state['display_v_hkl'], state['v']):
        Vlabel = f"{U_simu:g}*{_simu_hkl_text(state['u'])} + {txt_vl.get()}*{_simu_hkl_text(state['display_v_hkl'])}"

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
    else:
        n_hw = round((hw_max-hw_min)/hw_inc+1)
        hw=np.zeros((n_hw))
        for k in range(n_hw):
            hw[k] = hw_min + hw_inc * k

    #検出器の角度
    d_angle=np.linspace(0, 46, 24)

    # C2 is the instrument encoder value.  Reference calibration is applied
    # inside _simu_angles_to_rlu() when C2 is converted to omega.
    C2=np.asarray(c2, dtype=float)
    Qsimu_x = None
    Qsimu_y = None
    Qsimu_x=np.zeros((n_hw,n_a2*n_c2*24))
    Qsimu_y=np.zeros((n_hw,n_a2*n_c2*24))
    Qsimu=np.zeros((n_hw,n_a2*n_c2*24))
    Qsimu_d12_x=np.zeros((n_hw,n_a2*n_c2*1))
    Qsimu_d12_y=np.zeros((n_hw,n_a2*n_c2*1))
    for k in range(n_hw):
        for n in range(n_c2):
            for m in range(n_a2):
                for l in range(24):
                    #A2の絶対値変換
                    A2=d_angle+state['phi']+a2[m];# cover range
                    _sx, _sy, _q3, _hkl3, _res3 = _simu_angles_to_rlu(3.635+float(np.asarray(hw[k]).reshape(-1)[0]), 3.635, C2[n], A2[l], state['UBmatrix'], state['u'], state['display_v_hkl'], state['NU1'], state['NV1'], simu_ref_c2, simu_omega_ref, simu_c2_sign)
                    Qsimu_x[k,l+24*m+24*n_a2*n] = _sx
                    Qsimu_y[k,l+24*m+24*n_a2*n] = _sy
                    Qsimu[k,l+24*m+24*n_a2*n] = np.linalg.norm(_q3)
                    # D12は再計算
                    _dx, _dy, _q3d, _hkld, _resd = _simu_angles_to_rlu(3.635+float(np.asarray(hw[k]).reshape(-1)[0]), 3.635, C2[n], A2[11], state['UBmatrix'], state['u'], state['display_v_hkl'], state['NU1'], state['NV1'], simu_ref_c2, simu_omega_ref, simu_c2_sign)
                    Qsimu_d12_x[k,n+n_c2*m] = _dx
                    Qsimu_d12_y[k,n+n_c2*m] = _dy

    # sign flip is unnecessary; orientation is handled by the UB/display basis.

    #Vの指定範囲内にある点を探す。
    pmU_simu = (np.max(Qsimu)-np.min(Qsimu))/(24*n_a2)/state['NU1']*2
    for k in range(n_hw):
        ind_U = np.where((U_simu-pmU_simu <= Qsimu_x[k,:]) & (Qsimu_x[k,:] <= U_simu+pmU_simu))
        ind_U12 = np.where((U_simu-pmU_simu <= Qsimu_d12_x[k,:]) & (Qsimu_d12_x[k,:] <= U_simu+pmU_simu))
        qsimu_y_cv = Qsimu_y[k,:][ind_U]
        qsimu_y_cv12 = Qsimu_d12_y[k,:][ind_U12]
        if k==0:
            ConstU = np.vstack((qsimu_y_cv, hw[k]*np.ones((1,len(qsimu_y_cv)))))
            ConstU12 = np.vstack((qsimu_y_cv12, hw[k]*np.ones((1,len(qsimu_y_cv12)))))
        else:
            ConstU = np.concatenate((ConstU, np.vstack((qsimu_y_cv, hw[k]*np.ones((1,len(qsimu_y_cv)))))), axis=1)
            ConstU12 = np.concatenate((ConstU12, np.vstack((qsimu_y_cv12, hw[k]*np.ones((1,len(qsimu_y_cv12)))))), axis=1)

    # 測定条件の位置オフセット
    # shared variables are stored in state
    state['add_ssf1'] = 0

    # エラー回避
    if len(ConstU[0]) > 0:

        # グラフスケールの定義
        xlim_min=np.nanmin(ConstU[0,:])
        xlim_max=np.nanmax(ConstU[0,:])

        ylim_min=np.nanmin(hw)
        ylim_max=np.nanmax(hw)

        # グラフを作成
        fig=plt.figure(figsize=(10, 6))
        # グラフ番号取得
        # shared variables are stored in state
        state['num_fig_simu_sc_cU'] = plt.gcf().number

        # グラフ内に表示範囲を決定するボックス
        # 最小値と最大値の初期値
        default_xmin = round(xlim_min, 2)
        default_xmax = round(xlim_max, 2)

        default_ymin = round(ylim_min, 2)
        default_ymax = round(ylim_max, 2)

        # グローバル or 関数外で定義（他の場所からアクセスできるようにする）
        # shared variables are stored in state

        # テキストボックスを作成して最小値と最大値を設定
        state['xmin_box_sscu'] = TextBox(plt.axes([0.25, 0.02, 0.08, 0.05]), 'xMin:', initial=str(default_xmin))
        state['xmax_box_sscu'] = TextBox(plt.axes([0.55, 0.02, 0.08, 0.05]), 'xMax:', initial=str(default_xmax))

        state['ymin_box_sscu'] = TextBox(plt.axes([0.05, 0.2, 0.08, 0.05]), 'yMin:', initial=str(default_ymin))
        state['ymax_box_sscu'] = TextBox(plt.axes([0.05, 0.83, 0.08, 0.05]), 'yMax:', initial=str(default_ymax))

        # 最小値と最大値が変更されたときに呼び出される関数
        def update_axis_range(text):
            try:
                xmin_val = float(state['xmin_box_sscu'].text)
                xmax_val = float(state['xmax_box_sscu'].text)
                ax.set_xlim(xmin_val, xmax_val)
                ymin_val = float(state['ymin_box_sscu'].text)
                ymax_val = float(state['ymax_box_sscu'].text)
                ax.set_ylim(ymin_val, ymax_val)
                fig.canvas.draw_idle()
            except ValueError:
                pass

        state['xmin_box_sscu'].on_submit(update_axis_range)
        state['xmax_box_sscu'].on_submit(update_axis_range)
        state['ymin_box_sscu'].on_submit(update_axis_range)
        state['ymax_box_sscu'].on_submit(update_axis_range)

        fig.subplots_adjust(left=0.2, bottom=0.2, right=0.65)
        ax = fig.add_subplot(111)
        if n_a2!=1:
            plt.text(1.05,1.0,'a2 = %.3f ~ %.3f deg (step %.3f deg)' % (a2_min,a2_max,a2_inc), transform=ax.transAxes)
        else:
            plt.text(1.05,1.0,'a2 = %.3f' %a2_min, transform=ax.transAxes)

        if n_c2!=1:
            plt.text(1.05,0.95,'c2 = %.3f ~ %.3f deg (step %.3f deg)' % (c2_min,c2_max,c2_inc), transform=ax.transAxes)
        else:
            plt.text(1.05,0.95,'c2 = %.3f' %c2_min, transform=ax.transAxes)
        plt.text(1.05,0.90,f'{txt_ul.get()} = %.3f ± %.3f (r.l.u.)' % (U_simu,pmU_simu), transform=ax.transAxes)
        plt.xlabel(str(Vlabel))
        plt.ylabel("ℏω (meV)")
        plt.scatter(ConstU[0,:],ConstU[1,:],s=10, color = "blue", label="Other detectors")
        plt.scatter(ConstU12[0,:],ConstU12[1,:],s=10, color = "red", label="D12")
        plt.legend()
        plt.xlim(xlim_min,xlim_max) #x軸の範囲を指定
        plt.ylim(ylim_min,ylim_max) #y軸の範囲を指定
        plt.grid()
        #plt.tick_params(labelsize=20)

        plt.show()
    else:
        pass

def simu_sc_cV(env):
    i = env.get('i')
    state = env.get('state')
    txt10 = env.get('txt10')
    txt11 = env.get('txt11')
    txt12 = env.get('txt12')
    txt13 = env.get('txt13')
    txt14 = env.get('txt14')
    txt9 = env.get('txt9')
    txt_s1 = env.get('txt_s1')
    txt_s12 = env.get('txt_s12')
    txt_s2 = env.get('txt_s2')
    txt_s3 = env.get('txt_s3')
    txt_s4 = env.get('txt_s4')
    txt_s5 = env.get('txt_s5')
    txt_s6 = env.get('txt_s6')
    txt_s7 = env.get('txt_s7')
    txt_s8 = env.get('txt_s8')
    txt_s9 = env.get('txt_s9')
    txt_ul = env.get('txt_ul')
    txt_vl = env.get('txt_vl')
    _prepare_simu_reciprocal_display = lambda *a, **kw: prepare_simu_reciprocal_display(env, *a, **kw)
    # グラフ文字の取得    
    a2_min = float(txt_s1.get())
    a2_inc = float(txt_s2.get())
    a2_max = float(txt_s3.get())
    c2_min = float(txt_s4.get())
    c2_inc = float(txt_s5.get())
    c2_max = float(txt_s6.get())
    hw_min = float(txt_s7.get())
    hw_inc = float(txt_s8.get())
    hw_max = float(txt_s9.get())
    #E_simu = float(txt_s10.get())
    #U_simu = float(txt_s11.get())
    V_simu = float(txt_s12.get())

    # グラフラベルを作成
    if float(txt9.get())==0:
        if float(txt12.get())==0:
            ul1 = str('0')
        else:
            ul1 = str(float(txt12.get())*V_simu)
    elif float(txt9.get())==1:
        if float(txt12.get())==0:
            ul1 = str(txt_ul.get())
        else:
            ul1 = str(float(txt12.get())*V_simu) + str('+') + str(txt_ul.get())
    elif float(txt9.get())==-1:
        if float(txt12.get())==0:
            ul1 = str('-')+str(txt_ul.get())
        else:
            ul1 = str(float(txt12.get())*V_simu) + str('-') + str(txt_ul.get())
    else:
        try:
            number0 = float(txt9.get())
            if number0.is_integer():#整数である
                if number0 > 0:
                    ul1 = str(float(txt12.get())*V_simu) + str('+') + str(int(float(txt9.get()))) + str(txt_ul.get())
                elif number0 < 0:
                    ul1 = str(float(txt12.get())*V_simu) + str('-') + str(int(np.abs(float(txt9.get())))) + str(txt_ul.get())
            else:#整数でない
                if number0 > 0:
                    ul1 = str(float(txt12.get())*V_simu) + str('+') + str(float(txt9.get())) + str(txt_ul.get())
                elif number0 < 0:
                    ul1 = str(float(txt12.get())*V_simu) + str('-') + str(np.abs(float(txt9.get()))) + str(txt_ul.get())
        except ValueError:#整数でない
            pass

    if float(txt10.get())==0:
        if float(txt13.get())==0:
            ul2 = str('0')
        else:
            ul2 = str(float(txt13.get())*V_simu)
    elif float(txt10.get())==1:
        if float(txt13.get())==0:
            ul2 = str(txt_ul.get())
        else:
            ul2 = str(float(txt13.get())*V_simu) + str('+') + str(txt_ul.get())
    elif float(txt10.get())==-1:
        if float(txt13.get())==0:
            ul2 = str('-')+str(txt_ul.get())
        else:
            ul2 = str(float(txt13.get())*V_simu) + str('-') + str(txt_ul.get())
    else:
        try:
            number1 = float(txt10.get())
            if number1.is_integer():#整数である
                if number1 > 0:
                    ul2 = str(float(txt13.get())*V_simu) + str('+') + str(int(float(txt10.get()))) + str(txt_ul.get())
                elif number1 < 0:
                    ul2 = str(float(txt13.get())*V_simu) + str('-') + str(int(np.abs(float(txt10.get())))) + str(txt_ul.get())
            else:#整数でない
                if number1 > 0:
                    ul2 = str(float(txt13.get())*V_simu) + str('+') + str(float(txt10.get())) + str(txt_ul.get())
                elif number1 < 0:
                    ul2 = str(float(txt13.get())*V_simu) + str('-') + str(np.abs(float(txt10.get()))) + str(txt_ul.get())
        except ValueError:#整数でない
            pass

    if float(txt11.get())==0:
        if float(txt14.get())==0:
            ul3 = str('0')
        else:
            ul3 = str(float(txt14.get())*V_simu)
    elif float(txt11.get())==1:
        if float(txt14.get())==0:
            ul3 = str(txt_ul.get())
        else:
            ul3 = str(float(txt14.get())*V_simu) + str('+') + str(txt_ul.get())
    elif float(txt11.get())==-1:
        if float(txt14.get())==0:
            ul3 = str('-')+str(txt_ul.get())
        else:
            ul3 = str(float(txt14.get())*V_simu) + str('-') + str(txt_ul.get())
    else:
        try:
            number2 = float(txt11.get())
            if number2.is_integer():#整数である
                if number2 > 0:
                    ul3 = str(float(txt14.get())*V_simu) + str('+') + str(int(float(txt11.get()))) + str(txt_ul.get())
                elif number2 < 0:
                    ul3 = str(float(txt14.get())*V_simu) + str('-') + str(int(np.abs(float(txt11.get())))) + str(txt_ul.get())
            else:#整数でない
                if number2 > 0:
                    ul3 = str(float(txt14.get())*V_simu) + str('+') + str(float(txt11.get())) + str(txt_ul.get())
                elif number2 < 0:
                    ul3 = str(float(txt14.get())*V_simu) + str('-') + str(np.abs(float(txt11.get()))) + str(txt_ul.get())
        except ValueError:#整数でない
            pass

    Ulabel = (f"({ul1},{ul2},{ul3})")

    # UB + reference reflection based reciprocal-space setup.
    # Old txt7(c2_off) and txt8(Vt) are intentionally not used.
    # shared variables are stored in state
    # shared variables are stored in state
    # shared variables are stored in state
    (state['UBmatrix'], state['u'], state['v'], state['display_ex'], state['display_ey'], state['display_ez'],
     state['NU1'], state['NV1'], state['display_uv_angle'], display_used_angle,
     state['display_v_hkl'], state['display_mode'], display_coeff,
     simu_ref_c2, simu_omega_ref, simu_c2_sign) = \
        _prepare_simu_reciprocal_display()
    state['sign'] = 1.0
    if state['display_mode'] == 'orthogonal-crystallographic' and not np.allclose(state['display_v_hkl'], state['v']):
        Ulabel = f"{txt_ul.get()}*{_simu_hkl_text(state['u'])} + {V_simu:g}*{_simu_hkl_text(state['display_v_hkl'])}"

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
    else:
        n_hw = round((hw_max-hw_min)/hw_inc+1)
        hw=np.zeros((n_hw))
        for k in range(n_hw):
            hw[k] = hw_min + hw_inc * k

    #検出器の角度
    d_angle=np.linspace(0, 46, 24)

    # C2 is the instrument encoder value.  Reference calibration is applied
    # inside _simu_angles_to_rlu() when C2 is converted to omega.
    C2=np.asarray(c2, dtype=float)
    Qsimu_x = None
    Qsimu_y = None
    Qsimu_x=np.zeros((n_hw,n_a2*n_c2*24))
    Qsimu_y=np.zeros((n_hw,n_a2*n_c2*24))
    Qsimu=np.zeros((n_hw,n_a2*n_c2*24))
    Qsimu_d12_x=np.zeros((n_hw,n_a2*n_c2*1))
    Qsimu_d12_y=np.zeros((n_hw,n_a2*n_c2*1))
    for k in range(n_hw):
        for n in range(n_c2):
            for m in range(n_a2):
                for l in range(24):
                    #A2の絶対値変換
                    A2=d_angle+state['phi']+a2[m];# cover range
                    _sx, _sy, _q3, _hkl3, _res3 = _simu_angles_to_rlu(3.635+float(np.asarray(hw[k]).reshape(-1)[0]), 3.635, C2[n], A2[l], state['UBmatrix'], state['u'], state['display_v_hkl'], state['NU1'], state['NV1'], simu_ref_c2, simu_omega_ref, simu_c2_sign)
                    Qsimu_x[k,l+24*m+24*n_a2*n] = _sx
                    Qsimu_y[k,l+24*m+24*n_a2*n] = _sy
                    Qsimu[k,l+24*m+24*n_a2*n] = np.linalg.norm(_q3)
                    # D12は再計算
                    _dx, _dy, _q3d, _hkld, _resd = _simu_angles_to_rlu(3.635+float(np.asarray(hw[k]).reshape(-1)[0]), 3.635, C2[n], A2[11], state['UBmatrix'], state['u'], state['display_v_hkl'], state['NU1'], state['NV1'], simu_ref_c2, simu_omega_ref, simu_c2_sign)
                    Qsimu_d12_x[k,n+n_c2*m] = _dx
                    Qsimu_d12_y[k,n+n_c2*m] = _dy
    # sign flip is unnecessary; orientation is handled by the UB/display basis.
    #Vの指定範囲内にある点を探す。
    pmV_simu = (np.max(Qsimu)-np.min(Qsimu))/(24*n_a2)/state['NV1']*2
    for k in range(n_hw):
        ind_V = np.where((V_simu-pmV_simu <= Qsimu_y[k,:]) & (Qsimu_y[k,:] <= V_simu+pmV_simu))
        ind_V12 = np.where((V_simu-pmV_simu <= Qsimu_d12_y[k,:]) & (Qsimu_d12_y[k,:] <= V_simu+pmV_simu))
        qsimu_x_cv = Qsimu_x[k,:][ind_V]
        qsimu_x_cv12 = Qsimu_d12_x[k,:][ind_V12]
        if k==0:
            ConstV = np.vstack((qsimu_x_cv, hw[k]*np.ones((1,len(qsimu_x_cv)))))
            ConstV12 = np.vstack((qsimu_x_cv12, hw[k]*np.ones((1,len(qsimu_x_cv12)))))
        else:
            ConstV = np.concatenate((ConstV, np.vstack((qsimu_x_cv, hw[k]*np.ones((1,len(qsimu_x_cv)))))), axis=1)
            ConstV12 = np.concatenate((ConstV12, np.vstack((qsimu_x_cv12, hw[k]*np.ones((1,len(qsimu_x_cv12)))))), axis=1)

    # 測定条件の位置オフセット
    # shared variables are stored in state
    state['add_ssf2'] = 0

    # エラー回避
    if len(ConstV[0]) > 0:

        # グラフスケールの定義
        xlim_min=np.nanmin(ConstV[0,:])
        xlim_max=np.nanmax(ConstV[0,:])

        ylim_min=np.nanmin(hw)
        ylim_max=np.nanmax(hw)

        # グラフを作成
        fig=plt.figure(figsize=(10, 6))
        # グラフ番号取得
        # shared variables are stored in state
        state['num_fig_simu_sc_cV'] = plt.gcf().number

        # グラフ内に表示範囲を決定するボックス
        # 最小値と最大値の初期値
        default_xmin = round(xlim_min, 2)
        default_xmax = round(xlim_max, 2)

        default_ymin = round(ylim_min, 2)
        default_ymax = round(ylim_max, 2)

        # グローバル or 関数外で定義（他の場所からアクセスできるようにする）
        # shared variables are stored in state

        # テキストボックスを作成して最小値と最大値を設定
        state['xmin_box_sscv'] = TextBox(plt.axes([0.25, 0.02, 0.08, 0.05]), 'xMin:', initial=str(default_xmin))
        state['xmax_box_sscv'] = TextBox(plt.axes([0.55, 0.02, 0.08, 0.05]), 'xMax:', initial=str(default_xmax))

        state['ymin_box_sscv'] = TextBox(plt.axes([0.05, 0.2, 0.08, 0.05]), 'yMin:', initial=str(default_ymin))
        state['ymax_box_sscv'] = TextBox(plt.axes([0.05, 0.83, 0.08, 0.05]), 'yMax:', initial=str(default_ymax))

        # 最小値と最大値が変更されたときに呼び出される関数
        def update_axis_range(text):
            try:
                xmin_val = float(state['xmin_box_sscv'].text)
                xmax_val = float(state['xmax_box_sscv'].text)
                ax.set_xlim(xmin_val, xmax_val)
                ymin_val = float(state['ymin_box_sscv'].text)
                ymax_val = float(state['ymax_box_sscv'].text)
                ax.set_ylim(ymin_val, ymax_val)
                fig.canvas.draw_idle()
            except ValueError:
                pass

        state['xmin_box_sscv'].on_submit(update_axis_range)
        state['xmax_box_sscv'].on_submit(update_axis_range)
        state['ymin_box_sscv'].on_submit(update_axis_range)
        state['ymax_box_sscv'].on_submit(update_axis_range)

        fig.subplots_adjust(left=0.2, bottom=0.2, right=0.65)
        ax = fig.add_subplot(111)
        if n_a2!=1:
            plt.text(1.05,1.0,'a2 = %.3f ~ %.3f deg (step %.3f deg)' % (a2_min,a2_max,a2_inc), transform=ax.transAxes)
        else:
            plt.text(1.05,1.0,'a2 = %.3f' %a2_min, transform=ax.transAxes)

        if n_c2!=1:
            plt.text(1.05,0.95,'c2 = %.3f ~ %.3f deg (step %.3f deg)' % (c2_min,c2_max,c2_inc), transform=ax.transAxes)
        else:
            plt.text(1.05,0.95,'c2 = %.3f' %c2_min, transform=ax.transAxes)
        plt.text(1.05,0.9,f'{txt_vl.get()} = %.3f ± %.3f (r.l.u.)' % (V_simu,pmV_simu), transform=ax.transAxes)
        plt.xlabel(str(Ulabel))
        plt.ylabel("ℏω (meV)")
        plt.scatter(ConstV[0,:],ConstV[1,:],s=10, color = "blue", label="Other detectors")
        plt.scatter(ConstV12[0,:],ConstV12[1,:],s=10, color = "red", label="D12")
        plt.legend()
        plt.xlim(xlim_min,xlim_max) #x軸の範囲を指定
        plt.ylim(ylim_min,ylim_max) #y軸の範囲を指定
        #plt.tick_params(labelsize=20)
        plt.grid()

        plt.show()
    else:
        pass

def add_simu_sc_cU(env):
    i = env.get('i')
    state = env.get('state')
    txt10 = env.get('txt10')
    txt11 = env.get('txt11')
    txt12 = env.get('txt12')
    txt13 = env.get('txt13')
    txt14 = env.get('txt14')
    txt9 = env.get('txt9')
    txt_s1 = env.get('txt_s1')
    txt_s11 = env.get('txt_s11')
    txt_s2 = env.get('txt_s2')
    txt_s3 = env.get('txt_s3')
    txt_s4 = env.get('txt_s4')
    txt_s5 = env.get('txt_s5')
    txt_s6 = env.get('txt_s6')
    txt_s7 = env.get('txt_s7')
    txt_s8 = env.get('txt_s8')
    txt_s9 = env.get('txt_s9')
    txt_ul = env.get('txt_ul')
    txt_vl = env.get('txt_vl')
    _prepare_simu_reciprocal_display = lambda *a, **kw: prepare_simu_reciprocal_display(env, *a, **kw)
    # 図番号が存在するかどうかの確認
    if plt.fignum_exists(state['num_fig_simu_sc_cU'])==True:
        a2_min = float(txt_s1.get())
        a2_inc = float(txt_s2.get())
        a2_max = float(txt_s3.get())
        c2_min = float(txt_s4.get())
        c2_inc = float(txt_s5.get())
        c2_max = float(txt_s6.get())
        hw_min = float(txt_s7.get())
        hw_inc = float(txt_s8.get())
        hw_max = float(txt_s9.get())
        #E_simu = float(txt_s10.get())
        U_simu = float(txt_s11.get())
        #V_simu = float(txt_s12.get())

        if float(txt12.get())==0:
            if float(txt9.get())==0:
                vl1 = str('0')
            else:
                vl1 = str(float(txt9.get())*U_simu)
        elif float(txt12.get())==1:
            if float(txt9.get())==0:
                vl1 = str(txt_vl.get())
            else:
                vl1 = str(float(txt9.get())*U_simu) + str('+') + str(txt_vl.get())
        elif float(txt12.get())==-1:
            if float(txt9.get())==0:
                vl1 = str('-')+str(txt_vl.get())
            else:
                vl1 = str(float(txt9.get())*U_simu) + str('-') + str(txt_vl.get())
        else:
            try:
                number0 = float(txt12.get())
                if number0.is_integer():#整数である
                    if number0 > 0:
                        vl1 = str(float(txt9.get())*U_simu) + str('+') + str(int(float(txt12.get()))) + str(txt_vl.get())
                    elif number0 < 0:
                        vl1 = str(float(txt9.get())*U_simu) + str('-') + str(int(np.abs(float(txt12.get())))) + str(txt_vl.get())
                else:#整数でない
                    if number0 > 0:
                        vl1 = str(float(txt9.get())*U_simu) + str('+') + str(float(txt12.get())) + str(txt_vl.get())
                    elif number0 < 0:
                        vl1 = str(float(txt9.get())*U_simu) + str('-') + str(float(np.abs(txt12.get()))) + str(txt_vl.get())
            except ValueError:#数値でない
                pass

        if float(txt13.get())==0:
            if float(txt10.get())==0:
                vl2 = str('0')
            else:
                vl2 = str(float(txt10.get())*U_simu)
        elif float(txt13.get())==1:
            if float(txt10.get())==0:
                vl2 = str(txt_vl.get())
            else:
                vl2 = str(float(txt10.get())*U_simu) + str('+') + str(txt_vl.get())
        elif float(txt13.get())==-1:
            if float(txt10.get())==0:
                vl2 = str('-')+str(txt_vl.get())
            else:
                vl2 = str(float(txt10.get())*U_simu) + str('-') + str(txt_vl.get())
        else:
            try:
                number1 = float(txt13.get())
                if number1.is_integer():#整数である
                    if number1 > 0:
                        vl2 = str(float(txt10.get())*U_simu) + str('+') + str(int(float(txt13.get()))) + str(txt_vl.get())
                    elif number1 < 0:
                        vl2 = str(float(txt10.get())*U_simu) + str('-') + str(int(np.abs(float(txt13.get())))) + str(txt_vl.get())
                else:#整数でない
                    if number1 > 0:
                        vl2 = str(float(txt10.get())*U_simu) + str('+') + str(float(txt13.get())) + str(txt_vl.get())
                    elif number1 < 0:
                        vl2 = str(float(txt10.get())*U_simu) + str('-') + str(np.abs(float(txt13.get()))) + str(txt_vl.get())
            except ValueError:#数値でない
                pass

        if float(txt14.get())==0:
            if float(txt11.get())==0:
                vl3 = str('0')
            else:
                vl3 = str(float(txt11.get())*U_simu)
        elif float(txt14.get())==1:
            if float(txt11.get())==0:
                vl3 = str(txt_vl.get())
            else:
                vl3 = str(float(txt11.get())*U_simu) + str('+') + str(txt_vl.get())
        elif float(txt14.get())==-1:
            if float(txt11.get())==0:
                vl3 = str('-')+str(txt_vl.get())
            else:
                vl3 = str(float(txt11.get())*U_simu) + str('-') + str(txt_vl.get())
        else:
            try:
                number2 = float(txt14.get())
                if number2.is_integer():#整数である
                    if number2 > 0:
                        vl3 = str(float(txt11.get())*U_simu) + str('+') + str(int(float(txt14.get()))) + str(txt_vl.get())
                    elif number2 < 0:
                        vl3 = str(float(txt11.get())*U_simu) + str('-') + str(int(np.abs(float(txt14.get())))) + str(txt_vl.get())
                else:#整数でない
                    if number2 > 0:
                        vl3 = str(float(txt11.get())*U_simu) + str('+') + str(float(txt14.get())) + str(txt_vl.get())
                    elif number2 < 0:
                        vl3 = str(float(txt11.get())*U_simu) + str('-') + str(np.abs(float(txt14.get()))) + str(txt_vl.get())
            except ValueError:#整数でない
                pass

        Vlabel = (f"({vl1},{vl2},{vl3})")

        # UB + reference reflection based reciprocal-space setup.
        # Old txt7(c2_off) and txt8(Vt) are intentionally not used.
        # shared variables are stored in state
        # shared variables are stored in state
        # shared variables are stored in state
        (state['UBmatrix'], state['u'], state['v'], state['display_ex'], state['display_ey'], state['display_ez'],
         state['NU1'], state['NV1'], state['display_uv_angle'], display_used_angle,
         state['display_v_hkl'], state['display_mode'], display_coeff,
         simu_ref_c2, simu_omega_ref, simu_c2_sign) = \
            _prepare_simu_reciprocal_display()
        state['sign'] = 1.0
        if state['display_mode'] == 'orthogonal-crystallographic' and not np.allclose(state['display_v_hkl'], state['v']):
            Vlabel = f"{U_simu:g}*{_simu_hkl_text(state['u'])} + {txt_vl.get()}*{_simu_hkl_text(state['display_v_hkl'])}"

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
        else:
            n_hw = round((hw_max-hw_min)/hw_inc+1)
            hw=np.zeros((n_hw))
            for k in range(n_hw):
                hw[k] = hw_min + hw_inc * k

        #検出器の角度
        d_angle=np.linspace(0, 46, 24)

        # C2 is the instrument encoder value.  Reference calibration is applied
        # inside _simu_angles_to_rlu() when C2 is converted to omega.
        C2=np.asarray(c2, dtype=float)
        Qsimu_x = None
        Qsimu_y = None
        Qsimu_x=np.zeros((n_hw,n_a2*n_c2*24))
        Qsimu_y=np.zeros((n_hw,n_a2*n_c2*24))
        Qsimu=np.zeros((n_hw,n_a2*n_c2*24))
        Qsimu_d12_x=np.zeros((n_hw,n_a2*n_c2*1))
        Qsimu_d12_y=np.zeros((n_hw,n_a2*n_c2*1))
        for k in range(n_hw):
            for n in range(n_c2):
                for m in range(n_a2):
                    for l in range(24):
                        #A2の絶対値変換
                        A2=d_angle+state['phi']+a2[m];# cover range
                        _sx, _sy, _q3, _hkl3, _res3 = _simu_angles_to_rlu(3.635+float(np.asarray(hw[k]).reshape(-1)[0]), 3.635, C2[n], A2[l], state['UBmatrix'], state['u'], state['display_v_hkl'], state['NU1'], state['NV1'], simu_ref_c2, simu_omega_ref, simu_c2_sign)
                        Qsimu_x[k,l+24*m+24*n_a2*n] = _sx
                        Qsimu_y[k,l+24*m+24*n_a2*n] = _sy
                        Qsimu[k,l+24*m+24*n_a2*n] = np.linalg.norm(_q3)
                        # D12は再計算
                        _dx, _dy, _q3d, _hkld, _resd = _simu_angles_to_rlu(3.635+float(np.asarray(hw[k]).reshape(-1)[0]), 3.635, C2[n], A2[11], state['UBmatrix'], state['u'], state['display_v_hkl'], state['NU1'], state['NV1'], simu_ref_c2, simu_omega_ref, simu_c2_sign)
                        Qsimu_d12_x[k,n+n_c2*m] = _dx
                        Qsimu_d12_y[k,n+n_c2*m] = _dy

        # sign flip is unnecessary; orientation is handled by the UB/display basis.

        #Vの指定範囲内にある点を探す。
        pmU_simu = (np.max(Qsimu)-np.min(Qsimu))/(24*n_a2)/state['NU1']*2
        for k in range(n_hw):
            ind_U = np.where((U_simu-pmU_simu <= Qsimu_x[k,:]) & (Qsimu_x[k,:] <= U_simu+pmU_simu))
            ind_U12 = np.where((U_simu-pmU_simu <= Qsimu_d12_x[k,:]) & (Qsimu_d12_x[k,:] <= U_simu+pmU_simu))
            qsimu_y_cv = Qsimu_y[k,:][ind_U]
            qsimu_y_cv12 = Qsimu_d12_y[k,:][ind_U12]
            if k==0:
                ConstU = np.vstack((qsimu_y_cv, hw[k]*np.ones((1,len(qsimu_y_cv)))))
                ConstU12 = np.vstack((qsimu_y_cv12, hw[k]*np.ones((1,len(qsimu_y_cv12)))))
            else:
                ConstU = np.concatenate((ConstU, np.vstack((qsimu_y_cv, hw[k]*np.ones((1,len(qsimu_y_cv)))))), axis=1)
                ConstU12 = np.concatenate((ConstU12, np.vstack((qsimu_y_cv12, hw[k]*np.ones((1,len(qsimu_y_cv12)))))), axis=1)

        # 現状のグラフの最小最大を取ってくる。
        xmin_val = float(state['xmin_box_sscu'].text)
        xmax_val = float(state['xmax_box_sscu'].text)
        ymin_val = float(state['ymin_box_sscu'].text)
        ymax_val = float(state['ymax_box_sscu'].text)

        # 新しく計算した値の最大最小を取得
        xlim_min_sscu2=round(np.nanmin(ConstU[0,:]),2)
        xlim_max_sscu2=round(np.nanmax(ConstU[0,:]),2)
        ylim_min_sscu2=round(np.nanmin(hw),2)
        ylim_max_sscu2=round(np.nanmax(hw),2)

        # グラフスケール変更
        if xmin_val > xlim_min_sscu2:
            state['xmin_box_sscu'].set_val(xlim_min_sscu2)
        if xmax_val < xlim_max_sscu2:
            state['xmax_box_sscu'].set_val(xlim_max_sscu2)
        if ymin_val > ylim_min_sscu2:
            state['ymin_box_sscu'].set_val(ylim_min_sscu2)
        if ymax_val < ylim_max_sscu2:
            state['ymax_box_sscu'].set_val(ylim_max_sscu2)

        # 測定条件の位置オフセット
        # shared variables are stored in state
        state['add_ssf1'] = 1 + state['add_ssf1']

        # エラー回避
        if len(ConstU[0]) > 0:
            # グラフを作成
            fig=plt.figure(state['num_fig_simu_sc_cU'],figsize=(10, 6))

            fig.subplots_adjust(left=0.2, bottom=0.2, right=0.65)
            ax = fig.gca()
            #ax = fig.add_subplot(111)

            if n_a2!=1:
                plt.text(1.05,1.0 - state['add_ssf1']*0.15,'a2 = %.3f ~ %.3f deg (step %.3f deg)' % (a2_min,a2_max,a2_inc), transform=ax.transAxes)
            else:
                plt.text(1.05,1.0 - state['add_ssf1']*0.15,'a2 = %.3f' %a2_min, transform=ax.transAxes)

            if n_c2!=1:
                plt.text(1.05,0.95 - state['add_ssf1']*0.15,'c2 = %.3f ~ %.3f deg (step %.3f deg)' % (c2_min,c2_max,c2_inc), transform=ax.transAxes)
            else:
                plt.text(1.05,0.95 - state['add_ssf1']*0.15,'c2 = %.3f' %c2_min, transform=ax.transAxes)
            plt.text(1.05,0.90 - state['add_ssf1']*0.15,f'{txt_ul.get()} = %.3f ± %.3f (r.l.u.)' % (U_simu,pmU_simu), transform=ax.transAxes)
            plt.xlabel(str(Vlabel))
            plt.ylabel("ℏω (meV)")
            plt.scatter(ConstU[0,:],ConstU[1,:],s=10, color = "blue")
            plt.scatter(ConstU12[0,:],ConstU12[1,:],s=10, color = "red")
            #plt.tick_params(labelsize=20)

            plt.draw()
        else:
            pass

def add_simu_sc_cE(env):
    i = env.get('i')
    state = env.get('state')
    txt10 = env.get('txt10')
    txt11 = env.get('txt11')
    txt12 = env.get('txt12')
    txt13 = env.get('txt13')
    txt14 = env.get('txt14')
    txt9 = env.get('txt9')
    txt_s1 = env.get('txt_s1')
    txt_s10 = env.get('txt_s10')
    txt_s2 = env.get('txt_s2')
    txt_s3 = env.get('txt_s3')
    txt_s4 = env.get('txt_s4')
    txt_s5 = env.get('txt_s5')
    txt_s6 = env.get('txt_s6')
    txt_s7 = env.get('txt_s7')
    txt_s8 = env.get('txt_s8')
    txt_s9 = env.get('txt_s9')
    txt_ul = env.get('txt_ul')
    txt_vl = env.get('txt_vl')
    _prepare_simu_reciprocal_display = lambda *a, **kw: prepare_simu_reciprocal_display(env, *a, **kw)
    # グラフ文字の取得
    if float(txt9.get())==0:
        ul1 = 0
    elif float(txt9.get())==1:
        ul1 = str(txt_ul.get())
    elif float(txt9.get())==-1:
        ul1 = str('-')+str(txt_ul.get())
    else:
        try:
            number0 = float(txt9.get())
            if number0.is_integer():#整数である
                ul1 = str(int(float(txt9.get())))+str(txt_ul.get())
            else:#整数でない
                ul1 = str(float(txt9.get()))+str(txt_ul.get())
        except ValueError:#整数でない
            pass

    if float(txt10.get())==0:
        ul2 = 0
    elif float(txt10.get())==1:
        ul2 = str(txt_ul.get())
    elif float(txt10.get())==-1:
        ul2 = str('-')+str(txt_ul.get())
    else:
        try:
            number1 = float(txt10.get())
            if number1.is_integer():#整数である
                ul2 = str(int(float(txt10.get())))+str(txt_ul.get())
            else:#整数でない
                ul2 = str(float(txt10.get()))+str(txt_ul.get())
        except ValueError:#整数でない
            pass

    if float(txt11.get())==0:
        ul3 = 0
    elif float(txt11.get())==1:
        ul3 = str(txt_ul.get())
    elif float(txt11.get())==-1:
        ul3 = str('-')+str(txt_ul.get())
    else:
        try:
            number2 = float(txt11.get())
            if number2.is_integer():#整数である
                ul3 = str(int(float(txt11.get())))+str(txt_ul.get())
            else:#整数でない
                ul3 = str(float(txt11.get()))+str(txt_ul.get())
        except ValueError:#整数でない
            pass

    if float(txt12.get())==0:
        vl1 = 0
    elif float(txt12.get())==1:
        vl1 = str(txt_vl.get())
    elif float(txt12.get())==-1:
        vl1 = str('-')+str(txt_vl.get())
    else:
        try:
            number3 = float(txt12.get())
            if number3.is_integer():#整数である
                vl1 = str(int(float(txt12.get())))+str(txt_vl.get())
            else:#整数でない
                vl1 = str(float(txt12.get()))+str(txt_vl.get())
        except ValueError:#整数でない
            pass

    if float(txt13.get())==0:
        vl2 = 0
    elif float(txt13.get())==1:
        vl2 = str(txt_vl.get())
    elif float(txt13.get())==-1:
        vl2 = str('-')+str(txt_vl.get())
    else:
        try:
            number4 = float(txt13.get())
            if number4.is_integer():#整数である
                vl2 = str(int(float(txt13.get())))+str(txt_vl.get())
            else:#整数でない
                vl2 = str(float(txt13.get()))+str(txt_vl.get())
        except ValueError:#整数でない
            pass

    if float(txt14.get())==0:
        vl3 = 0
    elif float(txt14.get())==1:
        vl3 = str(txt_vl.get())
    elif float(txt14.get())==-1:
        vl3 = str('-')+str(txt_vl.get())
    else:
        try:
            number5 = float(txt14.get())
            if number5.is_integer():#整数である
                vl3 = str(int(float(txt14.get())))+str(txt_vl.get())
            else:#整数でない
                vl3 = str(float(txt14.get()))+str(txt_vl.get())
        except ValueError:#整数でない
            pass

    #global Ulabel,Vlabel
    Ulabel = (f"({ul1},{ul2},{ul3})")
    Vlabel = (f"({vl1},{vl2},{vl3})")

    a2_min = float(txt_s1.get())
    a2_inc = float(txt_s2.get())
    a2_max = float(txt_s3.get())
    c2_min = float(txt_s4.get())
    c2_inc = float(txt_s5.get())
    c2_max = float(txt_s6.get())
    hw_min = float(txt_s7.get())
    hw_inc = float(txt_s8.get())
    hw_max = float(txt_s9.get())
    E_simu = float(txt_s10.get())
    #U_simu = float(txt_s11.get())
    #V_simu = float(txt_s12.get())

    # UB + reference reflection based reciprocal-space setup.
    # Old txt7(c2_off) and txt8(Vt) are intentionally not used.
    # shared variables are stored in state
    # shared variables are stored in state
    # shared variables are stored in state
    (state['UBmatrix'], state['u'], state['v'], state['display_ex'], state['display_ey'], state['display_ez'],
     state['NU1'], state['NV1'], state['display_uv_angle'], display_used_angle,
     state['display_v_hkl'], state['display_mode'], display_coeff,
     simu_ref_c2, simu_omega_ref, simu_c2_sign) = \
        _prepare_simu_reciprocal_display()
    state['sign'] = 1.0
    if state['display_mode'] == 'orthogonal-crystallographic' and not np.allclose(state['display_v_hkl'], state['v']):
        Vlabel = _simu_hkl_text(state['display_v_hkl'])

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
        hw=np.zeros((n_hw,1))
        hw = np.array([hw_min,0])
    else:
        n_hw = round((hw_max-hw_min)/hw_inc+1)
        hw=np.zeros((n_hw,1))
        for k in range(n_hw):
            hw[k,0] = hw_min + hw_inc * k

    #検出器の角度
    d_angle=np.linspace(0, 46, 24)

    # C2 is the instrument encoder value.  Reference calibration is applied
    # inside _simu_angles_to_rlu() when C2 is converted to omega.
    C2=np.asarray(c2, dtype=float)

    Qsimu_x = None
    Qsimu_y = None
    Qsimu_x=np.zeros((n_hw,n_a2*n_c2*24))
    Qsimu_y=np.zeros((n_hw,n_a2*n_c2*24))
    Qsimu_d12_x=np.zeros((n_hw,n_a2*n_c2*1))
    Qsimu_d12_y=np.zeros((n_hw,n_a2*n_c2*1))
    A2_max = np.ones((n_hw,1))*a2_max
    A2_min = np.ones((n_hw,1))*a2_min
    A2_inc = np.ones((n_hw,1))*a2_inc
    C2_max = np.ones((n_hw,1))*c2_max
    C2_min = np.ones((n_hw,1))*c2_min
    C2_inc = np.ones((n_hw,1))*c2_inc
    for k in range(n_hw):
        for n in range(n_c2):
            for m in range(n_a2):
                for l in range(24):
                    #A2の絶対値変換
                    A2=d_angle+state['phi']+a2[m];# cover range
                    _sx, _sy, _q3, _hkl3, _res3 = _simu_angles_to_rlu(3.635+float(np.asarray(hw[k]).reshape(-1)[0]), 3.635, C2[n], A2[l], state['UBmatrix'], state['u'], state['display_v_hkl'], state['NU1'], state['NV1'], simu_ref_c2, simu_omega_ref, simu_c2_sign)
                    Qsimu_x[k,l+24*m+24*n_a2*n] = _sx
                    Qsimu_y[k,l+24*m+24*n_a2*n] = _sy
                    # D12は再計算
                    _dx, _dy, _q3d, _hkld, _resd = _simu_angles_to_rlu(3.635+float(np.asarray(hw[k]).reshape(-1)[0]), 3.635, C2[n], A2[11], state['UBmatrix'], state['u'], state['display_v_hkl'], state['NU1'], state['NV1'], simu_ref_c2, simu_omega_ref, simu_c2_sign)
                    Qsimu_d12_x[k,n+n_c2*m] = _dx
                    Qsimu_d12_y[k,n+n_c2*m] = _dy

    # sign flip is unnecessary; orientation is handled by the UB/display basis.

    # 一番近いhwの値を取り出す。浮動小数点数の精度の問題をクリア。
    ind_E = np.abs(hw - E_simu).argmin()

    # shared variables are stored in state

    # サイズが違う部分をNan値にする。0では機能した。計算も軽い。
    def pad_and_stack(arrays, pad_value=np.nan):
        # 最大の長さを調べる
        max_len = max(arr.shape[-1] for arr in arrays)

        # 長さが違う配列をゼロパディングして縦連結する関数
        padded_arrays = []
        for arr in arrays:
            # もし1次元なら2次元に変換しておく（行ベクトル想定）
            arr_2d = arr if arr.ndim > 1 else arr[np.newaxis, :]

            # パディング幅を計算
            pad_width = max_len - arr_2d.shape[-1]

            # 右側にpad_valueで埋める
            if pad_width > 0:
                padding = ((0, 0), (0, pad_width))  # 行は変えず、列をpad
                arr_padded = np.pad(arr_2d, padding, mode='constant', constant_values=pad_value)
            else:
                arr_padded = arr_2d

            padded_arrays.append(arr_padded)

        # 縦に連結
        stacked = np.vstack(padded_arrays)
        return stacked

    state['list_hw'] = pad_and_stack([state['list_hw'], hw], pad_value=np.nan)
    state['list_Qsimu_x'] = pad_and_stack([state['list_Qsimu_x'], Qsimu_x], pad_value=np.nan)
    state['list_Qsimu_y'] = pad_and_stack([state['list_Qsimu_y'], Qsimu_y], pad_value=np.nan)
    state['list_Qsimu_d12_x'] = pad_and_stack([state['list_Qsimu_d12_x'], Qsimu_d12_x], pad_value=np.nan)
    state['list_Qsimu_d12_y'] = pad_and_stack([state['list_Qsimu_d12_y'], Qsimu_d12_y], pad_value=np.nan)
    state['list_A2_max'] = pad_and_stack([state['list_A2_max'], A2_max], pad_value=np.nan)
    state['list_A2_min'] = pad_and_stack([state['list_A2_min'], A2_min], pad_value=np.nan)
    state['list_A2_inc'] = pad_and_stack([state['list_A2_inc'], A2_inc], pad_value=np.nan)
    state['list_C2_max'] = pad_and_stack([state['list_C2_max'], C2_max], pad_value=np.nan)
    state['list_C2_min'] = pad_and_stack([state['list_C2_min'], C2_min], pad_value=np.nan)
    state['list_C2_inc'] = pad_and_stack([state['list_C2_inc'], C2_inc], pad_value=np.nan)

    state['list_hw'] = np.array(state['list_hw'])
    state['list_Qsimu_x'] = np.array(state['list_Qsimu_x'])
    state['list_Qsimu_y'] = np.array(state['list_Qsimu_y'])
    state['list_Qsimu_d12_x'] = np.array(state['list_Qsimu_d12_x'])
    state['list_Qsimu_d12_y'] = np.array(state['list_Qsimu_d12_y'])
    state['list_A2_max'] = np.array(state['list_A2_max'])
    state['list_A2_min'] = np.array(state['list_A2_min'])
    state['list_A2_inc'] = np.array(state['list_A2_inc'])
    state['list_C2_max'] = np.array(state['list_C2_max'])
    state['list_C2_min'] = np.array(state['list_C2_min'])
    state['list_C2_inc'] = np.array(state['list_C2_inc'])

    # 並び替えのために index を取得
    sort_idx = np.argsort(state['list_hw'][:, 0])

    # ソート適用
    state['list_hw'] = state['list_hw'][sort_idx]
    state['list_Qsimu_x'] = state['list_Qsimu_x'][sort_idx]
    state['list_Qsimu_y'] = state['list_Qsimu_y'][sort_idx]
    state['list_Qsimu_d12_x'] = state['list_Qsimu_d12_x'][sort_idx]
    state['list_Qsimu_d12_y'] = state['list_Qsimu_d12_y'][sort_idx]
    state['list_A2_max'] = state['list_A2_max'][sort_idx]
    state['list_A2_min'] = state['list_A2_min'][sort_idx]
    state['list_A2_inc'] = state['list_A2_inc'][sort_idx]
    state['list_C2_max'] = state['list_C2_max'][sort_idx]
    state['list_C2_min'] = state['list_C2_min'][sort_idx]
    state['list_C2_inc'] = state['list_C2_inc'][sort_idx]

    # グラフスケールの定義
    xlim_min=np.nanmin(state['list_Qsimu_x'])
    xlim_max=np.nanmax(state['list_Qsimu_x'])

    ylim_min=np.nanmin(state['list_Qsimu_y'])
    ylim_max=np.nanmax(state['list_Qsimu_y'])

    # すでに存在する図を閉じる
    plt.close(state['num_fig_simu_sin'])
    # グラフを作成
    fig0,ax=plt.subplots()
    # グラフ内に表示範囲を決定するボックス
    # 最小値と最大値の初期値
    default_xmin = round(xlim_min, 2)
    default_xmax = round(xlim_max, 2)

    default_ymin = round(ylim_min, 2)
    default_ymax = round(ylim_max, 2)

    # テキストボックスを作成して最小値と最大値を設定
    xmin_box = TextBox(plt.axes([0.3, 0.10, 0.08, 0.05]), 'xMin:', initial=str(default_xmin))
    xmax_box = TextBox(plt.axes([0.65, 0.10, 0.08, 0.05]), 'xMax:', initial=str(default_xmax))

    ymin_box = TextBox(plt.axes([0.1, 0.2, 0.08, 0.05]), 'yMin:', initial=str(default_ymin))
    ymax_box = TextBox(plt.axes([0.1, 0.83, 0.08, 0.05]), 'yMax:', initial=str(default_ymax))

    # 最小値と最大値が変更されたときに呼び出される関数
    def update_axis_range(text):
        try:
            xmin_val = float(xmin_box.text)
            xmax_val = float(xmax_box.text)
            ax.set_xlim(xmin_val, xmax_val)
            ymin_val = float(ymin_box.text)
            ymax_val = float(ymax_box.text)
            ax.set_ylim(ymin_val, ymax_val)
            fig0.canvas.draw_idle()
            return xmin_val,xmax_val,ymin_val,ymax_val
        except ValueError:
            pass

    xmin_box.on_submit(update_axis_range)
    xmax_box.on_submit(update_axis_range)
    ymin_box.on_submit(update_axis_range)
    ymax_box.on_submit(update_axis_range)  

    plt.subplots_adjust(bottom=0.25)
    # アスペクト比を変更
    ax.set_aspect(state['NV1']/state['NU1'])
    sa1=ind_E#初期値をセット

    if state['list_A2_inc'][ind_E,0]!=0:
        ax.text(0.0,1.1,'a2 = %.3f ~ %.3f deg (step %.3f deg)' % (state['list_A2_min'][ind_E,0],state['list_A2_max'][ind_E,0],state['list_A2_inc'][ind_E,0]), transform=ax.transAxes)
    elif state['list_A2_inc'][ind_E,0]==0:
        ax.text(0.0,1.1,'a2 = %.3f deg' %state['list_A2_min'][ind_E,0], transform=ax.transAxes)

    if state['list_C2_inc'][ind_E,0]!=0:
        ax.text(0.0,1.05,'c2 = %.3f ~ %.3f deg (step %.3f deg)' % (state['list_C2_min'][ind_E,0],state['list_C2_max'][ind_E,0],state['list_C2_inc'][ind_E,0]), transform=ax.transAxes)
    elif state['list_C2_inc'][ind_E,0]==0:
        ax.text(0.0,1.05,'c2 = %.3f deg' %state['list_C2_min'][ind_E,0], transform=ax.transAxes)
    ax.text(0.0,1.00,'ℏω = %.3f meV' %state['list_hw'][ind_E,0], transform=ax.transAxes)
    ax.set_xlabel(str(Ulabel))
    ax.set_ylabel(str(Vlabel))
    ax.scatter(state['list_Qsimu_x'][ind_E,:], state['list_Qsimu_y'][ind_E,:],s=10, color = "blue", label="Other detectors")
    ax.scatter(state['list_Qsimu_d12_x'][ind_E,:], state['list_Qsimu_d12_y'][ind_E,:],s=10, color = "red", label="D12")
    ax.legend()
    ax.grid()
    ax.set_xlim(xlim_min,xlim_max) #x軸の範囲を指定
    ax.set_ylim(ylim_min,ylim_max) #y軸の範囲を指定
    plt.subplots_adjust(left=0.30, right=0.75, bottom=0.25)  # マージンを調整してグラフを中央に配置
    #plt.tick_params(labelsize=20)
    #横スライドでエネルギートランスファーを変更、縦スライドで強度の最大値を変更
    ax_a = plt.axes([0.3, 0.02, 0.45, 0.04]) #plt.axes([x, y, width, height] ) 
    sli_a1 = wg.Slider(ax_a, 'ℏω', 0, len(state['list_hw'])-1, valinit=sa1,valstep=1, orientation='horizontal')

    # gif 保存
    """
    import imageio
    from io import BytesIO
    from PIL import Image

    frames = []
    for ind_E in range(len(list_hw)):
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.set_aspect(NV1 / NU1)

        # 情報描画
        if list_A2_inc[ind_E, 0] != 0:
            ax.text(0.0, 1.1, f'a2 = {list_A2_min[ind_E,0]:.3f} ~ {list_A2_max[ind_E,0]:.3f} deg (step {list_A2_inc[ind_E,0]:.3f} deg)', transform=ax.transAxes)
        else:
            ax.text(0.0, 1.1, f'a2 = {list_A2_min[ind_E,0]:.3f} deg', transform=ax.transAxes)

        if list_C2_inc[ind_E, 0] != 0:
            ax.text(0.0, 1.05, f'c2 = {list_C2_min[ind_E,0]:.3f} ~ {list_C2_max[ind_E,0]:.3f} deg (step {list_C2_inc[ind_E,0]:.3f} deg)', transform=ax.transAxes)
        else:
            ax.text(0.0, 1.05, f'c2 = {list_C2_min[ind_E,0]:.3f} deg', transform=ax.transAxes)

        ax.text(0.0, 1.00, f'ℏω = {list_hw[ind_E,0]:.3f} meV', transform=ax.transAxes)
        ax.set_xlabel(str(Ulabel))
        ax.set_ylabel(str(Vlabel))

        # プロット
        ax.scatter(list_Qsimu_x[ind_E, :], list_Qsimu_y[ind_E, :], s=10, color="blue", label="Other detectors")
        ax.scatter(list_Qsimu_d12_x[ind_E, :], list_Qsimu_d12_y[ind_E, :], s=10, color="red", label="D12")
        ax.set_xlim(xlim_min, xlim_max)
        ax.set_ylim(ylim_min, ylim_max)
        ax.grid()
        ax.legend()

        # 描画をPIL画像に変換
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img = Image.open(buf)
        frames.append(img.copy())
        plt.close(fig)

    # GIFとして保存
    frames[0].save('energy_scan.gif', save_all=True, append_images=frames[1:], duration=200, loop=0)
    """

    def update1(val):
        ax.clear()

        xmin_val = float(xmin_box.text)
        xmax_val = float(xmax_box.text)
        ymin_val = float(ymin_box.text)
        ymax_val = float(ymax_box.text)

        # アスペクト比を変更
        ax.set_aspect(state['NV1']/state['NU1'])

        sa1 = sli_a1.val
        if state['list_A2_inc'][sa1,0]!=0:
            ax.text(0.0,1.1,'a2 = %.3f ~ %.3f deg (step %.3f deg)' % (state['list_A2_min'][sa1,0],state['list_A2_max'][sa1,0],state['list_A2_inc'][sa1,0]), transform=ax.transAxes)
        elif state['list_A2_inc'][sa1,0]==0:
            ax.text(0.0,1.1,'a2 = %.3f deg' %state['list_A2_min'][sa1,0], transform=ax.transAxes)

        if state['list_C2_inc'][sa1,0]!=0:
            ax.text(0.0,1.05,'c2 = %.3f ~ %.3f deg (step %.3f deg)' % (state['list_C2_min'][sa1,0],state['list_C2_max'][sa1,0],state['list_C2_inc'][sa1,0]), transform=ax.transAxes)
        elif state['list_C2_inc'][sa1,0]==0:
            ax.text(0.0,1.05,'c2 = %.3f deg' %state['list_C2_min'][sa1,0], transform=ax.transAxes)

        ax.text(0.0,1.00,'ℏω = %.3f meV' %state['list_hw'][sa1,0], transform=ax.transAxes)
        ax.set_xlabel(str(Ulabel))
        ax.set_ylabel(str(Vlabel))
        ax.scatter(state['list_Qsimu_x'][sa1,:], state['list_Qsimu_y'][sa1,:],s=10, color = "blue", label="Other detectors")
        ax.scatter(state['list_Qsimu_d12_x'][sa1,:], state['list_Qsimu_d12_y'][sa1,:],s=10, color = "red", label="D12")
        ax.legend()
        ax.grid()
        ax.set_xlim(xmin_val,xmax_val) #x軸の範囲を指定
        ax.set_ylim(ymin_val,ymax_val) #y軸の範囲を指定
        plt.draw()
    # 矢印キーにスライダを対応。上限を超えて表示しないように設定。
    def on_key(event):
        if event.key == 'right':
            new_val_a = min(sli_a1.val + 1, sli_a1.valmax)
            sli_a1.set_val(new_val_a)
        elif event.key == 'left':
            new_val_a = max(sli_a1.val - 1, sli_a1.valmin)
            sli_a1.set_val(new_val_a)
    fig0.canvas.mpl_connect('key_press_event', on_key)

    sli_a1.on_changed(update1)
    plt.show()

def add_simu_sc_cV(env):
    i = env.get('i')
    state = env.get('state')
    txt10 = env.get('txt10')
    txt11 = env.get('txt11')
    txt12 = env.get('txt12')
    txt13 = env.get('txt13')
    txt14 = env.get('txt14')
    txt9 = env.get('txt9')
    txt_s1 = env.get('txt_s1')
    txt_s12 = env.get('txt_s12')
    txt_s2 = env.get('txt_s2')
    txt_s3 = env.get('txt_s3')
    txt_s4 = env.get('txt_s4')
    txt_s5 = env.get('txt_s5')
    txt_s6 = env.get('txt_s6')
    txt_s7 = env.get('txt_s7')
    txt_s8 = env.get('txt_s8')
    txt_s9 = env.get('txt_s9')
    txt_ul = env.get('txt_ul')
    txt_vl = env.get('txt_vl')
    _prepare_simu_reciprocal_display = lambda *a, **kw: prepare_simu_reciprocal_display(env, *a, **kw)
    # 図番号が存在するかどうかの確認
    if plt.fignum_exists(state['num_fig_simu_sc_cV'])==True:    
        # グラフ文字の取得    
        a2_min = float(txt_s1.get())
        a2_inc = float(txt_s2.get())
        a2_max = float(txt_s3.get())
        c2_min = float(txt_s4.get())
        c2_inc = float(txt_s5.get())
        c2_max = float(txt_s6.get())
        hw_min = float(txt_s7.get())
        hw_inc = float(txt_s8.get())
        hw_max = float(txt_s9.get())
        #E_simu = float(txt_s10.get())
        #U_simu = float(txt_s11.get())
        V_simu = float(txt_s12.get())

        # グラフラベルを作成
        if float(txt9.get())==0:
            if float(txt12.get())==0:
                ul1 = str('0')
            else:
                ul1 = str(float(txt12.get())*V_simu)
        elif float(txt9.get())==1:
            if float(txt12.get())==0:
                ul1 = str(txt_ul.get())
            else:
                ul1 = str(float(txt12.get())*V_simu) + str('+') + str(txt_ul.get())
        elif float(txt9.get())==-1:
            if float(txt12.get())==0:
                ul1 = str('-')+str(txt_ul.get())
            else:
                ul1 = str(float(txt12.get())*V_simu) + str('-') + str(txt_ul.get())
        else:
            try:
                number0 = float(txt9.get())
                if number0.is_integer():#整数である
                    if number0 > 0:
                        ul1 = str(float(txt12.get())*V_simu) + str('+') + str(int(float(txt9.get()))) + str(txt_ul.get())
                    elif number0 < 0:
                        ul1 = str(float(txt12.get())*V_simu) + str('-') + str(int(np.abs(float(txt9.get())))) + str(txt_ul.get())
                else:#整数でない
                    if number0 > 0:
                        ul1 = str(float(txt12.get())*V_simu) + str('+') + str(float(txt9.get())) + str(txt_ul.get())
                    elif number0 < 0:
                        ul1 = str(float(txt12.get())*V_simu) + str('-') + str(np.abs(float(txt9.get()))) + str(txt_ul.get())
            except ValueError:#整数でない
                pass

        if float(txt10.get())==0:
            if float(txt13.get())==0:
                ul2 = str('0')
            else:
                ul2 = str(float(txt13.get())*V_simu)
        elif float(txt10.get())==1:
            if float(txt13.get())==0:
                ul2 = str(txt_ul.get())
            else:
                ul2 = str(float(txt13.get())*V_simu) + str('+') + str(txt_ul.get())
        elif float(txt10.get())==-1:
            if float(txt13.get())==0:
                ul2 = str('-')+str(txt_ul.get())
            else:
                ul2 = str(float(txt13.get())*V_simu) + str('-') + str(txt_ul.get())
        else:
            try:
                number1 = float(txt10.get())
                if number1.is_integer():#整数である
                    if number1 > 0:
                        ul2 = str(float(txt13.get())*V_simu) + str('+') + str(int(float(txt10.get()))) + str(txt_ul.get())
                    elif number1 < 0:
                        ul2 = str(float(txt13.get())*V_simu) + str('-') + str(int(np.abs(float(txt10.get())))) + str(txt_ul.get())
                else:#整数でない
                    if number1 > 0:
                        ul2 = str(float(txt13.get())*V_simu) + str('+') + str(float(txt10.get())) + str(txt_ul.get())
                    elif number1 < 0:
                        ul2 = str(float(txt13.get())*V_simu) + str('-') + str(np.abs(float(txt10.get()))) + str(txt_ul.get())
            except ValueError:#整数でない
                pass

        if float(txt11.get())==0:
            if float(txt14.get())==0:
                ul3 = str('0')
            else:
                ul3 = str(float(txt14.get())*V_simu)
        elif float(txt11.get())==1:
            if float(txt14.get())==0:
                ul3 = str(txt_ul.get())
            else:
                ul3 = str(float(txt14.get())*V_simu) + str('+') + str(txt_ul.get())
        elif float(txt11.get())==-1:
            if float(txt14.get())==0:
                ul3 = str('-')+str(txt_ul.get())
            else:
                ul3 = str(float(txt14.get())*V_simu) + str('-') + str(txt_ul.get())
        else:
            try:
                number2 = float(txt11.get())
                if number2.is_integer():#整数である
                    if number2 > 0:
                        ul3 = str(float(txt14.get())*V_simu) + str('+') + str(int(float(txt11.get()))) + str(txt_ul.get())
                    elif number2 < 0:
                        ul3 = str(float(txt14.get())*V_simu) + str('-') + str(int(np.abs(float(txt11.get())))) + str(txt_ul.get())
                else:#整数でない
                    if number2 > 0:
                        ul3 = str(float(txt14.get())*V_simu) + str('+') + str(float(txt11.get())) + str(txt_ul.get())
                    elif number2 < 0:
                        ul3 = str(float(txt14.get())*V_simu) + str('-') + str(np.abs(float(txt11.get()))) + str(txt_ul.get())
            except ValueError:#整数でない
                pass

        Ulabel = (f"({ul1},{ul2},{ul3})")

        # UB + reference reflection based reciprocal-space setup.
        # Old txt7(c2_off) and txt8(Vt) are intentionally not used.
        # shared variables are stored in state
        # shared variables are stored in state
        # shared variables are stored in state
        (state['UBmatrix'], state['u'], state['v'], state['display_ex'], state['display_ey'], state['display_ez'],
         state['NU1'], state['NV1'], state['display_uv_angle'], display_used_angle,
         state['display_v_hkl'], state['display_mode'], display_coeff,
         simu_ref_c2, simu_omega_ref, simu_c2_sign) = \
            _prepare_simu_reciprocal_display()
        state['sign'] = 1.0
        if state['display_mode'] == 'orthogonal-crystallographic' and not np.allclose(state['display_v_hkl'], state['v']):
            Ulabel = f"{txt_ul.get()}*{_simu_hkl_text(state['u'])} + {V_simu:g}*{_simu_hkl_text(state['display_v_hkl'])}"

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
        else:
            n_hw = round((hw_max-hw_min)/hw_inc+1)
            hw=np.zeros((n_hw))
            for k in range(n_hw):
                hw[k] = hw_min + hw_inc * k

        #検出器の角度
        d_angle=np.linspace(0, 46, 24)

        # C2 is the instrument encoder value.  Reference calibration is applied
        # inside _simu_angles_to_rlu() when C2 is converted to omega.
        C2=np.asarray(c2, dtype=float)
        Qsimu_x = None
        Qsimu_y = None
        Qsimu_x=np.zeros((n_hw,n_a2*n_c2*24))
        Qsimu_y=np.zeros((n_hw,n_a2*n_c2*24))
        Qsimu=np.zeros((n_hw,n_a2*n_c2*24))
        Qsimu_d12_x=np.zeros((n_hw,n_a2*n_c2*1))
        Qsimu_d12_y=np.zeros((n_hw,n_a2*n_c2*1))
        for k in range(n_hw):
            for n in range(n_c2):
                for m in range(n_a2):
                    for l in range(24):
                        #A2の絶対値変換
                        A2=d_angle+state['phi']+a2[m];# cover range
                        _sx, _sy, _q3, _hkl3, _res3 = _simu_angles_to_rlu(3.635+float(np.asarray(hw[k]).reshape(-1)[0]), 3.635, C2[n], A2[l], state['UBmatrix'], state['u'], state['display_v_hkl'], state['NU1'], state['NV1'], simu_ref_c2, simu_omega_ref, simu_c2_sign)
                        Qsimu_x[k,l+24*m+24*n_a2*n] = _sx
                        Qsimu_y[k,l+24*m+24*n_a2*n] = _sy
                        Qsimu[k,l+24*m+24*n_a2*n] = np.linalg.norm(_q3)
                        # D12は再計算
                        _dx, _dy, _q3d, _hkld, _resd = _simu_angles_to_rlu(3.635+float(np.asarray(hw[k]).reshape(-1)[0]), 3.635, C2[n], A2[11], state['UBmatrix'], state['u'], state['display_v_hkl'], state['NU1'], state['NV1'], simu_ref_c2, simu_omega_ref, simu_c2_sign)
                        Qsimu_d12_x[k,n+n_c2*m] = _dx
                        Qsimu_d12_y[k,n+n_c2*m] = _dy

        # sign flip is unnecessary; orientation is handled by the UB/display basis.

        #Vの指定範囲内にある点を探す。
        pmV_simu = (np.max(Qsimu)-np.min(Qsimu))/(24*n_a2)/state['NV1']*2
        for k in range(n_hw):
            ind_V = np.where((V_simu-pmV_simu <= Qsimu_y[k,:]) & (Qsimu_y[k,:] <= V_simu+pmV_simu))
            ind_V12 = np.where((V_simu-pmV_simu <= Qsimu_d12_y[k,:]) & (Qsimu_d12_y[k,:] <= V_simu+pmV_simu))
            qsimu_x_cv = Qsimu_x[k,:][ind_V]
            qsimu_x_cv12 = Qsimu_d12_x[k,:][ind_V12]
            if k==0:
                ConstV = np.vstack((qsimu_x_cv, hw[k]*np.ones((1,len(qsimu_x_cv)))))
                ConstV12 = np.vstack((qsimu_x_cv12, hw[k]*np.ones((1,len(qsimu_x_cv12)))))
            else:
                ConstV = np.concatenate((ConstV, np.vstack((qsimu_x_cv, hw[k]*np.ones((1,len(qsimu_x_cv)))))), axis=1)
                ConstV12 = np.concatenate((ConstV12, np.vstack((qsimu_x_cv12, hw[k]*np.ones((1,len(qsimu_x_cv12)))))), axis=1)

        # 測定条件の位置オフセット
        # shared variables are stored in state
        state['add_ssf2'] = 1 + state['add_ssf2']

        # エラー回避
        if len(ConstV[0]) > 0:

            # グラフを作成
            fig=plt.figure(state['num_fig_simu_sc_cV'],figsize=(10, 6))

            fig.subplots_adjust(left=0.2, bottom=0.2, right=0.65)
            ax = fig.gca()

            # グラフ内に表示範囲を決定するボックス
            # 現状のグラフの最小最大を取ってくる。
            xmin_val = float(state['xmin_box_sscv'].text)
            xmax_val = float(state['xmax_box_sscv'].text)
            ymin_val = float(state['ymin_box_sscv'].text)
            ymax_val = float(state['ymax_box_sscv'].text)

            # 新しく計算した値の最大最小を取得
            xlim_min_sscv2=round(np.nanmin(ConstV[0,:]),2)
            xlim_max_sscv2=round(np.nanmax(ConstV[0,:]),2)
            ylim_min_sscv2=round(np.nanmin(hw),2)
            ylim_max_sscv2=round(np.nanmax(hw),2)

            # グラフスケール変更
            if xmin_val > xlim_min_sscv2:
                state['xmin_box_sscv'].set_val(xlim_min_sscv2)
            if xmax_val < xlim_max_sscv2:
                state['xmax_box_sscv'].set_val(xlim_max_sscv2)
            if ymin_val > ylim_min_sscv2:
                state['ymin_box_sscv'].set_val(ylim_min_sscv2)
            if ymax_val < ylim_max_sscv2:
                state['ymax_box_sscv'].set_val(ylim_max_sscv2)

            fig=plt.figure(state['num_fig_simu_sc_cV'],figsize=(10, 6))

            fig.subplots_adjust(left=0.2, bottom=0.2, right=0.65)
            ax = fig.gca()
            if n_a2!=1:
                plt.text(1.05,1.0 - state['add_ssf2']*0.15,'a2 = %.3f ~ %.3f deg (step %.3f deg)' % (a2_min,a2_max,a2_inc), transform=ax.transAxes)
            else:
                plt.text(1.05,1.0 - state['add_ssf2']*0.15,'a2 = %.3f' %a2_min, transform=ax.transAxes)

            if n_c2!=1:
                plt.text(1.05,0.95 - state['add_ssf2']*0.15,'c2 = %.3f ~ %.3f deg (step %.3f deg)' % (c2_min,c2_max,c2_inc), transform=ax.transAxes)
            else:
                plt.text(1.05,0.95 - state['add_ssf2']*0.15,'c2 = %.3f' %c2_min, transform=ax.transAxes)
            plt.text(1.05,0.90 - state['add_ssf2']*0.15,f'{txt_vl.get()} = %.3f ± %.3f (r.l.u.)' % (V_simu,pmV_simu), transform=ax.transAxes)
            plt.xlabel(str(Ulabel))
            plt.ylabel("ℏω (meV)")
            plt.scatter(ConstV[0,:],ConstV[1,:],s=10, color = "blue", label="Other detectors")
            plt.scatter(ConstV12[0,:],ConstV12[1,:],s=10, color = "red", label="D12")
            #plt.tick_params(labelsize=20)

            plt.draw()
        else:
            pass
