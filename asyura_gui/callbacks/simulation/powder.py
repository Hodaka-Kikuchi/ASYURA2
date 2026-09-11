from ...callback_runtime import *

from .display_basis import prepare_simu_reciprocal_display

def simu_pow(env):
    i = env.get('i')
    state = env.get('state')
    txt_s1_1 = env.get('txt_s1_1')
    txt_s2_1 = env.get('txt_s2_1')
    txt_s3_1 = env.get('txt_s3_1')
    txt_s4_1 = env.get('txt_s4_1')
    txt_s5_1 = env.get('txt_s5_1')
    txt_s6_1 = env.get('txt_s6_1')
    # shared variables are stored in state
    state['add_psf'] = 0
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
    elif a2_inc == 0:
        n_a2 = 1
        a2 = np.array([a2_min])
        n_hw = round((hw_max-hw_min)/hw_inc+1)
        hw=np.zeros((n_hw))
        for j in range(n_hw):
            hw[j] = hw_min + hw_inc * j
    elif hw_inc == 0:
        n_a2 = round((a2_max-a2_min)/a2_inc+1)
        a2=np.zeros((n_a2))
        for i in range(n_a2):
            a2[i] = a2_min + a2_inc * i
        n_hw = 1
        hw = np.array([hw_min])
    elif a2_inc != 0 and hw_inc != 0:
        # a2とhwのsimulationする数
        n_a2=round((a2_max-a2_min)/a2_inc+1)
        n_hw=round((hw_max-hw_min)/hw_inc+1)
        a2=np.zeros((n_a2))
        hw=np.zeros((n_hw))
        for i in range(n_a2):
            a2[i] = a2_min + a2_inc * i
        for j in range(n_hw):
            hw[j] = hw_min + hw_inc * j

    #検出器の角度
    d_angle=np.linspace(0, 46, 24)


    Qsimu=np.zeros((n_hw*n_a2*24))
    Qsimu12=np.zeros((n_hw*n_a2))
    hw_list=np.zeros((n_hw*n_a2*24))
    hw_list12=np.zeros((n_hw*n_a2))
    for n in range(n_hw):
        for m in range(n_a2):
            A2=d_angle+state['phi']+a2[m];# cover range
            # D12は別計算
            Qsimu12[m+n_a2*n] = math.sqrt((math.sqrt((3.635+hw[n])/2.072)*math.cos(math.radians(0))-math.sqrt(3.635/2.072)*math.cos(math.radians(A2[11])))**2 + (-math.sqrt((3.635+hw[n])/2.072)*math.sin(math.radians(0))+math.sqrt(3.635/2.072)*math.sin(math.radians(A2[11])))**2 )
            hw_list12[m+n_a2*n] = hw[n]
            for l in range(24):
                #A2の絶対値変換
                A2=d_angle+state['phi']+a2[m];# cover range
                # 粉末だからc2は関係ない
                hw_list[l+24*m+24*n_a2*n] = hw[n]
                Qsimu[l+24*m+24*n_a2*n] = math.sqrt((math.sqrt((3.635+hw[n])/2.072)*math.cos(math.radians(0))-math.sqrt(3.635/2.072)*math.cos(math.radians(A2[l])))**2 + (-math.sqrt((3.635+hw[n])/2.072)*math.sin(math.radians(0))+math.sqrt(3.635/2.072)*math.sin(math.radians(A2[l])))**2 )
    # グラフスケールの定義
    xlim_min=np.nanmin(Qsimu)
    xlim_max=np.nanmax(Qsimu)

    ylim_min=np.nanmin(hw_list)
    ylim_max=np.nanmax(hw_list)

    # グラフを作成
    # shared variables are stored in state
    fig=plt.figure(figsize=(10, 6))

    # グラフ内に表示範囲を決定するボックス
    # 最小値と最大値の初期値
    default_xmin = round(xlim_min, 2)
    default_xmax = round(xlim_max, 2)

    default_ymin = round(ylim_min, 2)
    default_ymax = round(ylim_max, 2)

    # グローバル or 関数外で定義（他の場所からアクセスできるようにする）
    # shared variables are stored in state

    # テキストボックスを作成して最小値と最大値を設定
    state['xmin_box_p'] = TextBox(plt.axes([0.25, 0.02, 0.08, 0.05]), 'xMin:', initial=str(default_xmin))
    state['xmax_box_p'] = TextBox(plt.axes([0.55, 0.02, 0.08, 0.05]), 'xMax:', initial=str(default_xmax))

    state['ymin_box_p'] = TextBox(plt.axes([0.05, 0.2, 0.08, 0.05]), 'yMin:', initial=str(default_ymin))
    state['ymax_box_p'] = TextBox(plt.axes([0.05, 0.83, 0.08, 0.05]), 'yMax:', initial=str(default_ymax))

    # 最小値と最大値が変更されたときに呼び出される関数
    def update_axis_range(text):
        try:
            xmin_val = float(state['xmin_box_p'].text)
            xmax_val = float(state['xmax_box_p'].text)
            ax.set_xlim(xmin_val, xmax_val)
            ymin_val = float(state['ymin_box_p'].text)
            ymax_val = float(state['ymax_box_p'].text)
            ax.set_ylim(ymin_val, ymax_val)
            fig.canvas.draw_idle()
        except ValueError:
            pass

    state['xmin_box_p'].on_submit(update_axis_range)
    state['xmax_box_p'].on_submit(update_axis_range)
    state['ymin_box_p'].on_submit(update_axis_range)
    state['ymax_box_p'].on_submit(update_axis_range)

    fig.subplots_adjust(left=0.20, bottom=0.2, right=0.65)
    ax = fig.add_subplot(111)
    if n_a2!=1:
        plt.text(1.05,1.0,'a2 = %.3f ~ %.3f deg (step %.3f deg)' %(a2_min,a2_max,a2_inc), transform=ax.transAxes)
    else:
        plt.text(1.05,1.0,'a2 = %.3f' %a2_min, transform=ax.transAxes)

    if n_hw!=1:
        plt.text(1.05,0.95,'ℏω = %.3f ~ %.3f meV (step %.3f meV)' %(hw_min,hw_max,hw_inc), transform=ax.transAxes)
    else:
        plt.text(1.05,0.95,'ℏω = %.3f' %hw_min, transform=ax.transAxes)
    plt.xlabel("Q (Å^-1)")
    plt.ylabel("ℏω (meV)")
    # 現在のFigure番号を取得
    state['num_fig_simu_pow'] = plt.gcf().number
    plt.scatter(Qsimu,hw_list, s=10, color = "blue", label="Other detectors")
    plt.scatter(Qsimu12,hw_list12, s=10, color = "red", label="D12")
    plt.legend()

    #plt.tick_params(labelsize=20)
    plt.xlim(xlim_min,xlim_max) #x軸の範囲を指定
    plt.ylim(ylim_min,ylim_max) #y軸の範囲を指定
    plt.grid()

    plt.show()

def add_simu_pow(env):
    i = env.get('i')
    state = env.get('state')
    txt_s1_1 = env.get('txt_s1_1')
    txt_s2_1 = env.get('txt_s2_1')
    txt_s3_1 = env.get('txt_s3_1')
    txt_s4_1 = env.get('txt_s4_1')
    txt_s5_1 = env.get('txt_s5_1')
    txt_s6_1 = env.get('txt_s6_1')
    # 図番号が存在するかどうかの確認
    if plt.fignum_exists(state['num_fig_simu_pow'])==True:
        # shared variables are stored in state
        state['add_psf'] = 1 + state['add_psf']

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
        elif a2_inc == 0:
            n_a2 = 1
            a2 = np.array([a2_min])
            n_hw = round((hw_max-hw_min)/hw_inc+1)
            hw=np.zeros((n_hw))
            for j in range(n_hw):
                hw[j] = hw_min + hw_inc * j
        elif hw_inc == 0:
            n_a2 = round((a2_max-a2_min)/a2_inc+1)
            a2=np.zeros((n_a2))
            for i in range(n_a2):
                a2[i] = a2_min + a2_inc * i
            n_hw = 1
            hw = np.array([hw_min])
        elif a2_inc != 0 and hw_inc != 0:
            # a2とhwのsimulationする数
            n_a2=round((a2_max-a2_min)/a2_inc+1)
            n_hw=round((hw_max-hw_min)/hw_inc+1)
            a2=np.zeros((n_a2))
            hw=np.zeros((n_hw))
            for i in range(n_a2):
                a2[i] = a2_min + a2_inc * i
            for j in range(n_hw):
                hw[j] = hw_min + hw_inc * j

        #検出器の角度
        d_angle=np.linspace(0, 46, 24)


        Qsimu=np.zeros((n_hw*n_a2*24))
        Qsimu12=np.zeros((n_hw*n_a2))
        hw_list=np.zeros((n_hw*n_a2*24))
        hw_list12=np.zeros((n_hw*n_a2))
        for n in range(n_hw):
            for m in range(n_a2):
                A2=d_angle+state['phi']+a2[m];# cover range
                # D12は別計算
                Qsimu12[m+n_a2*n] = math.sqrt((math.sqrt((3.635+hw[n])/2.072)*math.cos(math.radians(0))-math.sqrt(3.635/2.072)*math.cos(math.radians(A2[11])))**2 + (-math.sqrt((3.635+hw[n])/2.072)*math.sin(math.radians(0))+math.sqrt(3.635/2.072)*math.sin(math.radians(A2[11])))**2 )
                hw_list12[m+n_a2*n] = hw[n]
                for l in range(24):
                    #A2の絶対値変換
                    A2=d_angle+state['phi']+a2[m];# cover range
                    # 粉末だからc2は関係ない
                    hw_list[l+24*m+24*n_a2*n] = hw[n]
                    Qsimu[l+24*m+24*n_a2*n] = math.sqrt((math.sqrt((3.635+hw[n])/2.072)*math.cos(math.radians(0))-math.sqrt(3.635/2.072)*math.cos(math.radians(A2[l])))**2 + (-math.sqrt((3.635+hw[n])/2.072)*math.sin(math.radians(0))+math.sqrt(3.635/2.072)*math.sin(math.radians(A2[l])))**2 )

        # グラフを作成
        fig=plt.figure(state['num_fig_simu_pow'], figsize=(10, 6))
        fig.subplots_adjust(left=0.2, bottom=0.2, right=0.65)
        ax = fig.gca()

        # 現状のグラフの最小最大を取ってくる。
        xmin_val = float(state['xmin_box_p'].text)
        xmax_val = float(state['xmax_box_p'].text)
        ymin_val = float(state['ymin_box_p'].text)
        ymax_val = float(state['ymax_box_p'].text)

        # 新しく計算した値の最大最小を取得
        xlim_min_p2=round(np.nanmin(Qsimu),2)
        xlim_max_p2=round(np.nanmax(Qsimu),2)
        ylim_min_p2=round(np.nanmin(hw),2)
        ylim_max_p2=round(np.nanmax(hw),2)

        # グラフスケール変更
        if xmin_val > xlim_min_p2:
            state['xmin_box_p'].set_val(xlim_min_p2)
        if xmax_val < xlim_max_p2:
            state['xmax_box_p'].set_val(xlim_max_p2)
        if ymin_val > ylim_min_p2:
            state['ymin_box_p'].set_val(ylim_min_p2)
        if ymax_val < ylim_max_p2:
            state['ymax_box_p'].set_val(ylim_max_p2)

        if n_a2!=1:
            plt.text(1.05,1.0-state['add_psf']*0.1,'a2 = %.3f ~ %.3f deg (step %.3f deg)' %(a2_min,a2_max,a2_inc), transform=ax.transAxes)
        else:
            plt.text(1.05,1.0-state['add_psf']*0.1,'a2 = %.3f' %a2_min, transform=ax.transAxes)

        if n_hw!=1:
            plt.text(1.05,0.95-state['add_psf']*0.1,'ℏω = %.3f ~ %.3f meV (step %.3f meV)' %(hw_min,hw_max,hw_inc), transform=ax.transAxes)
        else:
            plt.text(1.05,0.95-state['add_psf']*0.1,'ℏω = %.3f' %hw_min, transform=ax.transAxes)
        plt.xlabel("Q (Å^-1)")
        plt.ylabel("ℏω (meV)")

        plt.scatter(Qsimu,hw_list, s=10, color = "blue")
        plt.scatter(Qsimu12,hw_list12, s=10, color = "red")
        plt.legend()

        plt.draw()
