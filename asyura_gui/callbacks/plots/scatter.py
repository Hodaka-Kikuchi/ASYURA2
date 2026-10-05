from ...callback_runtime import *

def disp3D(env):
    check_var = env.get('check_var')
    color_mode_var = env.get('color_mode_var')
    grid_var = env.get('grid_var')
    i = env.get('i')
    scale_s_Emax_txt_2 = env.get('scale_s_Emax_txt_2')
    scale_s_Emin_txt_2 = env.get('scale_s_Emin_txt_2')
    scale_s_Imax_txt_2 = env.get('scale_s_Imax_txt_2')
    scale_s_Imin_txt_2 = env.get('scale_s_Imin_txt_2')
    scale_s_Umax_txt_2 = env.get('scale_s_Umax_txt_2')
    scale_s_Umin_txt_2 = env.get('scale_s_Umin_txt_2')
    scale_s_Vmax_txt_2 = env.get('scale_s_Vmax_txt_2')
    scale_s_Vmin_txt_2 = env.get('scale_s_Vmin_txt_2')
    size_txt = env.get('size_txt')
    state = env.get('state')
    txt10 = env.get('txt10')
    txt11 = env.get('txt11')
    txt12 = env.get('txt12')
    txt13 = env.get('txt13')
    txt14 = env.get('txt14')
    txt9 = env.get('txt9')
    txt_dhw = env.get('txt_dhw')
    txt_pcs = env.get('txt_pcs')
    txt_rQ = env.get('txt_rQ')
    txt_vr_I1 = env.get('txt_vr_I1')
    txt_vr_I2 = env.get('txt_vr_I2')
    txt_vr_U1 = env.get('txt_vr_U1')
    txt_vr_U2 = env.get('txt_vr_U2')
    txt_vr_V1 = env.get('txt_vr_V1')
    txt_vr_V2 = env.get('txt_vr_V2')
    txt_vr_hw1 = env.get('txt_vr_hw1')
    txt_vr_hw2 = env.get('txt_vr_hw2')
    # 例: databox = np.loadtxt('your_file.dat')  # shape: (N, 6)
    # 各成分の抽出
    qx = state['databox'][0, :]
    qy = state['databox'][1, :]
    hw = state['databox'][3, :]  # ℏω（Z軸）
    try:
        # sb_databox が存在し、サイズも一致していれば差分で強度を定義
        if state['sb_databox'].shape == state['databox'].shape:
            intensity = state['databox'][4, :] - state['sb_databox'][4, :]
            intensity_err = np.sqrt(state['databox'][5, :]**2 + state['sb_databox'][5, :]**2)
        else:
            intensity = state['databox'][4, :]
            intensity_err = state['databox'][5, :]
    except NameError:
        # sb_databox が定義されていない場合
        intensity = state['databox'][4, :]
        intensity_err = state['databox'][5, :]

    # 強度の閾値を設定
    # 強度の下限と上限。これだけは設定しないと意味不明なので例外無し。
    I_min = float(txt_vr_I1.get())
    I_max = float(txt_vr_I2.get())

    # ℏω の下限・上限（例: 10 ～ 60 meV の間だけ可視化）
    if txt_vr_hw1.get()=="":
        hw_min = np.min(state['databox'][3, :])
    else:
        hw_min = float(txt_vr_hw1.get())
    if txt_vr_hw2.get()=="":
        hw_max = np.max(state['databox'][3, :])
    else:
        hw_max = float(txt_vr_hw2.get())

    # qxの下限・上限
    if txt_vr_U1.get()=="":
        qx_min = np.min(state['databox'][0, :])/state['NU1']
    else:
        qx_min = float(txt_vr_U1.get())
    if txt_vr_U2.get()=="":
        qx_max = np.max(state['databox'][0, :])/state['NU1']
    else:
        qx_max = float(txt_vr_U2.get())

    # qyの下限・上限
    if txt_vr_V1.get()=="":
        qy_min = np.min(state['databox'][1, :])/state['NV1']
    else:
        qy_min = float(txt_vr_V1.get())
    if txt_vr_V2.get()=="":
        qy_max = np.max(state['databox'][1, :])/state['NV1']
    else:
        qy_max = float(txt_vr_V2.get())

    # 強度が I_min 以上かつ I_max 以下の点だけを表示
    # 条件を組み合わせる
    mask1 = (
        (intensity >= I_min) & (intensity <= I_max) &
        (hw >= hw_min) & (hw <= hw_max) & 
        (qx >= qx_min*state['NU1']) & (qx <= qx_max*state['NU1']) & 
        (qy >= qy_min*state['NV1']) & (qy <= qy_max*state['NV1'])
    )

    if check_var.get(): # checkbox on
        # さらに、空間的に孤立している点をマスク
        # マスク1を通過したデータ
        qx_m = qx[mask1]
        qy_m = qy[mask1]
        hw_m = hw[mask1]
        coords = np.vstack((qx_m, qy_m)).T

        # さらにブラッグテイルなどの外れ値を除外する
        radius_q = float(txt_rQ.get()) # q空間での近傍半径 dq
        min_neighbors = float(txt_pcs.get())     # 最低近傍点数（孤立除去の基準）
        hw_window = float(txt_dhw.get())  # ± meV 以内のみを近傍とする

        # KDTree構築（qx, qy 空間）
        tree = KDTree(coords)

        # mask2作成：空間的に孤立していない点のみ通す
        neighbor_counts = []
        for i, point in enumerate(coords):
            # qx-qy 半径で候補点を取得
            idxs = tree.query_ball_point(point, r=radius_q)
            # 候補の中で hw が近いものだけに限定
            count = 0
            for j in idxs:
                if abs(hw_m[j] - hw_m[i]) <= hw_window:
                    count += 1
            neighbor_counts.append(count)

        neighbor_counts = np.array(neighbor_counts)
        mask2 = neighbor_counts >= min_neighbors

        # mask1 のインデックスを通じて final_mask を作成
        final_mask = mask1.copy()
        final_mask_indices = np.where(mask1)[0]
        final_mask[final_mask_indices[~mask2]] = False
    else:
        final_mask = mask1

    # マスクしたデータ
    x = qx[final_mask]
    y = qy[final_mask]
    z = hw[final_mask]
    c = intensity[final_mask]
    c_err = intensity_err[final_mask]

    # shared variables are stored in state
    state['masked_3d_databox'] = np.array([float(txt9.get())*x/state['NU1'],float(txt10.get())*x/state['NU1'],float(txt11.get())*x/state['NU1'],
                                  float(txt12.get())*y/state['NV1'],float(txt13.get())*y/state['NV1'],float(txt14.get())*y/state['NV1'],
                                  z,c,c_err]).T

    # グラフスケール
    # グラフの軸設定
    if scale_s_Umin_txt_2.get()=="":
        xlim_min=round(qx_min,2)
    else:
        xlim_min=float(scale_s_Umin_txt_2.get())
    if scale_s_Umax_txt_2.get()=="":
        xlim_max=round(qx_max,2)
    else:
        xlim_max=float(scale_s_Umax_txt_2.get())

    if scale_s_Vmin_txt_2.get()=="":
        ylim_min=round(qy_min,2)
    else:
        ylim_min=float(scale_s_Vmin_txt_2.get())
    if scale_s_Vmax_txt_2.get()=="":
        ylim_max=round(qy_max,2)
    else:
        ylim_max=float(scale_s_Vmax_txt_2.get())

    if scale_s_Emin_txt_2.get()=="":
        zlim_min=round(hw_min, 2)
    else:
        zlim_min=float(scale_s_Emin_txt_2.get())
    if scale_s_Emax_txt_2.get()=="":
        zlim_max=round(hw_max, 2)
    else:
        zlim_max=float(scale_s_Emax_txt_2.get())

    # カラーバースケール。
    if scale_s_Imin_txt_2.get()=="":
        clim_min = round(I_min,2)
    else:
        clim_min=float(scale_s_Imin_txt_2.get())

    if scale_s_Imax_txt_2.get()=="":
        clim_max = round(I_max,2)
    else:
        clim_max=float(scale_s_Imax_txt_2.get())

    pt_s = float(size_txt.get()) # 散布図表示サイズ

    # option, log scale
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    if color_mode_var.get() == "linear":
        # 通常のカラーマップ付き
        sc = ax.scatter(x/state['NU1'], y/state['NV1'], z, c=c, cmap='jet', s=pt_s, vmin=clim_min, vmax=clim_max)
        #fig.colorbar(sc, ax=ax, label='Intensity (a. u.)')
        # カラーバー追加
        cbar = fig.colorbar(sc, ax=ax, label='Intensity (a. u.)')
        # カラーバーの目盛りを3つ（最小・中間・最大）に設定
        cbar.locator = mticker.LinearLocator(numticks=3)
        cbar.update_ticks()
    elif color_mode_var.get() == "log":        
        norm = LogNorm(vmin=clim_min, vmax=clim_max)
        sc = ax.scatter(x/state['NU1'], y/state['NV1'], z, c=c, cmap='jet', s=pt_s, norm=norm)
        #fig.colorbar(sc, ax=ax, label='Intensity (a. u.)')
        # Logスケール用のカラーバー作成
        cbar = fig.colorbar(sc, ax=ax, label='Intensity (a. u.)')
        # 目盛りを最小値・最大値（など）に限定
        cbar.locator = mticker.LogLocator(numticks=3)  # 例えば3目盛り（min, mid, max）
        cbar.update_ticks()
    elif color_mode_var.get() == "coloroff": 
        # 単色（例：グレー）で描画
        sc = ax.scatter(x/state['NU1'], y/state['NV1'], z, c='gray', s=pt_s)
    ax.set_xlabel(str(state['Ulabel']))
    ax.set_ylabel(str(state['Vlabel']))
    ax.set_zlabel('ℏω (meV)')
    #ax.set_title('3D Scatter (Rotating View)')

    # 軸スケール適用
    ax.set_xlim(xlim_min,xlim_max)  # x軸（U軸）のスケール（必要に応じて）
    ax.set_ylim(ylim_min,ylim_max)        # y軸（V軸）
    ax.set_zlim(zlim_min,zlim_max)        # z軸（エネルギー）

    ax.grid(grid_var.get())

    plt.show()

def scatter_2d_cE(env):
    check_var = env.get('check_var')
    color_mode_var = env.get('color_mode_var')
    grid_var = env.get('grid_var')
    i = env.get('i')
    scale_s_Emax_txt_2 = env.get('scale_s_Emax_txt_2')
    scale_s_Emin_txt_2 = env.get('scale_s_Emin_txt_2')
    scale_s_Imax_txt_2 = env.get('scale_s_Imax_txt_2')
    scale_s_Imin_txt_2 = env.get('scale_s_Imin_txt_2')
    scale_s_Umax_txt_2 = env.get('scale_s_Umax_txt_2')
    scale_s_Umin_txt_2 = env.get('scale_s_Umin_txt_2')
    scale_s_Vmax_txt_2 = env.get('scale_s_Vmax_txt_2')
    scale_s_Vmin_txt_2 = env.get('scale_s_Vmin_txt_2')
    size_txt = env.get('size_txt')
    state = env.get('state')
    txt10 = env.get('txt10')
    txt11 = env.get('txt11')
    txt12 = env.get('txt12')
    txt13 = env.get('txt13')
    txt14 = env.get('txt14')
    txt9 = env.get('txt9')
    txt_3dsca_1e = env.get('txt_3dsca_1e')
    txt_3dsca_2e = env.get('txt_3dsca_2e')
    txt_dhw = env.get('txt_dhw')
    txt_pcs = env.get('txt_pcs')
    txt_rQ = env.get('txt_rQ')
    txt_vr_I1 = env.get('txt_vr_I1')
    txt_vr_I2 = env.get('txt_vr_I2')
    txt_vr_U1 = env.get('txt_vr_U1')
    txt_vr_U2 = env.get('txt_vr_U2')
    txt_vr_V1 = env.get('txt_vr_V1')
    txt_vr_V2 = env.get('txt_vr_V2')
    txt_vr_hw1 = env.get('txt_vr_hw1')
    txt_vr_hw2 = env.get('txt_vr_hw2')
    # 例: databox = np.loadtxt('your_file.dat')  # shape: (N, 6)
    # 各成分の抽出
    qx = state['databox'][0, :]
    qy = state['databox'][1, :]
    hw = state['databox'][3, :]  # ℏω（Z軸）
    try:
        # sb_databox が存在し、サイズも一致していれば差分で強度を定義
        if state['sb_databox'].shape == state['databox'].shape:
            intensity = state['databox'][4, :] - state['sb_databox'][4, :]
            intensity_err = np.sqrt(state['databox'][5, :]**2 + state['sb_databox'][5, :]**2)
        else:
            intensity = state['databox'][4, :]
            intensity_err = state['databox'][5, :]
    except NameError:
        # sb_databox が定義されていない場合
        intensity = state['databox'][4, :]
        intensity_err = state['databox'][5, :]

    # 強度の閾値を設定
    # 強度の下限と上限。これだけは設定しないと意味不明なので例外無し。
    I_min = float(txt_vr_I1.get())
    I_max = float(txt_vr_I2.get())

    # ℏω の下限・上限（例: 10 ～ 60 meV の間だけ可視化）
    if txt_vr_hw1.get()=="":
        hw_min = np.min(state['databox'][3, :])
    else:
        hw_min = float(txt_vr_hw1.get())
    if txt_vr_hw2.get()=="":
        hw_max = np.max(state['databox'][3, :])
    else:
        hw_max = float(txt_vr_hw2.get())

    # qxの下限・上限
    if txt_vr_U1.get()=="":
        qx_min = np.min(state['databox'][0, :])/state['NU1']
    else:
        qx_min = float(txt_vr_U1.get())
    if txt_vr_U2.get()=="":
        qx_max = np.max(state['databox'][0, :])/state['NU1']
    else:
        qx_max = float(txt_vr_U2.get())

    # qyの下限・上限
    if txt_vr_V1.get()=="":
        qy_min = np.min(state['databox'][1, :])/state['NV1']
    else:
        qy_min = float(txt_vr_V1.get())
    if txt_vr_V2.get()=="":
        qy_max = np.max(state['databox'][1, :])/state['NV1']
    else:
        qy_max = float(txt_vr_V2.get())

    # 強度が I_min 以上かつ I_max 以下の点だけを表示
    # 条件を組み合わせる
    mask1 = (
        (intensity >= I_min) & (intensity <= I_max) &
        (hw >= hw_min) & (hw <= hw_max) & 
        (qx >= qx_min*state['NU1']) & (qx <= qx_max*state['NU1']) & 
        (qy >= qy_min*state['NV1']) & (qy <= qy_max*state['NV1'])
    )

    if check_var.get(): # checkbox on
        # さらに、空間的に孤立している点をマスク
        # マスク1を通過したデータ
        qx_m = qx[mask1]
        qy_m = qy[mask1]
        hw_m = hw[mask1]
        coords = np.vstack((qx_m, qy_m)).T

        # さらにブラッグテイルなどの外れ値を除外する
        radius_q = float(txt_rQ.get()) # q空間での近傍半径 dq
        min_neighbors = float(txt_pcs.get())     # 最低近傍点数（孤立除去の基準）
        hw_window = float(txt_dhw.get())  # ± meV 以内のみを近傍とする

        # KDTree構築（qx, qy 空間）
        tree = KDTree(coords)

        # mask2作成：空間的に孤立していない点のみ通す
        neighbor_counts = []
        for i, point in enumerate(coords):
            # qx-qy 半径で候補点を取得
            idxs = tree.query_ball_point(point, r=radius_q)
            # 候補の中で hw が近いものだけに限定
            count = 0
            for j in idxs:
                if abs(hw_m[j] - hw_m[i]) <= hw_window:
                    count += 1
            neighbor_counts.append(count)

        neighbor_counts = np.array(neighbor_counts)
        mask2 = neighbor_counts >= min_neighbors

        # mask1 のインデックスを通じて final_mask を作成
        final_mask = mask1.copy()
        final_mask_indices = np.where(mask1)[0]
        final_mask[final_mask_indices[~mask2]] = False
    else:
        final_mask = mask1

    # マスクしたデータ
    x = qx[final_mask]
    y = qy[final_mask]
    z = hw[final_mask]
    c = intensity[final_mask]
    c_err = intensity_err[final_mask]

    # グラフスケール
    # グラフの軸設定
    if scale_s_Umin_txt_2.get()=="":
        xlim_min=round(qx_min,2)
    else:
        xlim_min=float(scale_s_Umin_txt_2.get())
    if scale_s_Umax_txt_2.get()=="":
        xlim_max=round(qx_max,2)
    else:
        xlim_max=float(scale_s_Umax_txt_2.get())

    if scale_s_Vmin_txt_2.get()=="":
        ylim_min=round(qy_min,2)
    else:
        ylim_min=float(scale_s_Vmin_txt_2.get())
    if scale_s_Vmax_txt_2.get()=="":
        ylim_max=round(qy_max,2)
    else:
        ylim_max=float(scale_s_Vmax_txt_2.get())

    if scale_s_Emin_txt_2.get()=="":
        zlim_min=round(hw_min, 2)
    else:
        zlim_min=float(scale_s_Emin_txt_2.get())
    if scale_s_Emax_txt_2.get()=="":
        zlim_max=round(hw_max, 2)
    else:
        zlim_max=float(scale_s_Emax_txt_2.get())

    # カラーバースケール。
    if scale_s_Imin_txt_2.get()=="":
        clim_min = round(I_min,2)
    else:
        clim_min=float(scale_s_Imin_txt_2.get())

    if scale_s_Imax_txt_2.get()=="":
        clim_max = round(I_max,2)
    else:
        clim_max=float(scale_s_Imax_txt_2.get())

    pt_s = float(size_txt.get()) # 散布図表示サイズ

    # スライス範囲
    z_min = float(txt_3dsca_1e.get())-float(txt_3dsca_2e.get())
    z_max = float(txt_3dsca_1e.get())+float(txt_3dsca_2e.get())

    # z方向でのスライス
    slice_mask = (z >= z_min) & (z <= z_max)

    # スライスされた x, y, 色
    x_slice = x[slice_mask]
    y_slice = y[slice_mask]
    c_slice = c[slice_mask]
    z_slice = z[slice_mask]
    c_err_slice = c_err[slice_mask]

    # データ結合
    # shared variables are stored in state
    state['masked_2d_constE'] = np.array([float(txt9.get())*x_slice/state['NU1'],float(txt10.get())*x_slice/state['NU1'],float(txt11.get())*x_slice/state['NU1'],
                                  float(txt12.get())*y_slice/state['NV1'],float(txt13.get())*y_slice/state['NV1'],float(txt14.get())*y_slice/state['NV1'],
                                  z_slice,c_slice,c_err_slice]).T

    # プロット
    fig, ax = plt.subplots()
    fig.subplots_adjust(left=0.30, right=0.75, bottom=0.2)

    # カラーモードに応じた描画
    if color_mode_var.get() == "coloroff":
        # 単色（グレー）で描画（カラーバーなし）
        sc = ax.scatter(x / state['NU1'], y / state['NV1'], color='gray', s=pt_s)
    else:
        # 通常のカラーマップを用いた描画
        sc = ax.scatter(x_slice / state['NU1'], y_slice / state['NV1'], c=c_slice, cmap='jet', s=pt_s,
                        vmin=clim_min, vmax=clim_max)

        # カラーバーの追加と目盛設定
        cbar = fig.colorbar(sc, ax=ax, label='Intensity (a. u.)')
        if color_mode_var.get() == "linear":
            cbar.locator = mticker.LinearLocator(numticks=3)
            cbar.update_ticks()
        elif color_mode_var.get() == "log":
            cbar.locator = mticker.LogLocator(numticks=3)
            cbar.update_ticks()

    # 軸ラベル
    ax.set_xlabel(str(state['Ulabel']))
    ax.set_ylabel(str(state['Vlabel']))

    # タイトル（ℏω = 中心 ± 幅）
    z_center = (z_min + z_max) / 2
    z_error = (z_max - z_min) / 2
    ax.set_title(f"ℏω = {z_center:.3f} ± {z_error:.3f} meV")

    # グリッドとアスペクト比
    ax.grid(grid_var.get())
    ax.set_aspect(state['NV1'] / state['NU1'])

    # 軸スケール適用
    ax.set_xlim(xlim_min, xlim_max)
    ax.set_ylim(ylim_min, ylim_max)

    # グラフ中のエントリーボックス
    # 初期値設定
    default_xmin = round(xlim_min, 3)
    default_xmax = round(xlim_max, 3)
    default_ymin = round(ylim_min, 3)
    default_ymax = round(ylim_max, 3)
    default_zmin = round(clim_min, 3)
    default_zmax = round(clim_max, 3)

    # TextBox配置
    xmin_box = TextBox(plt.axes([0.3, 0.02, 0.08, 0.05]), 'xMin:', initial=str(default_xmin))
    xmax_box = TextBox(plt.axes([0.6, 0.02, 0.08, 0.05]), 'xMax:', initial=str(default_xmax))
    ymin_box = TextBox(plt.axes([0.1, 0.2, 0.08, 0.05]), 'yMin:', initial=str(default_ymin))
    ymax_box = TextBox(plt.axes([0.1, 0.83, 0.08, 0.05]), 'yMax:', initial=str(default_ymax))
    zmin_box = TextBox(plt.axes([0.9, 0.2, 0.08, 0.05]), 'zMin:', initial=str(default_zmin))
    zmax_box = TextBox(plt.axes([0.9, 0.83, 0.08, 0.05]), 'zMax:', initial=str(default_zmax))

    # スケール変更関数
    def update_axis_range(text):
        try:
            xmin_val = float(xmin_box.text)
            xmax_val = float(xmax_box.text)
            ymin_val = float(ymin_box.text)
            ymax_val = float(ymax_box.text)
            zmin_val = float(zmin_box.text)
            zmax_val = float(zmax_box.text)

            ax.set_xlim(xmin_val, xmax_val)
            ax.set_ylim(ymin_val, ymax_val)
            sc.set_clim(vmin=zmin_val, vmax=zmax_val)
            fig.canvas.draw_idle()
        except ValueError:
            pass  # 無効な入力は無視

    # イベント登録
    xmin_box.on_submit(update_axis_range)
    xmax_box.on_submit(update_axis_range)
    ymin_box.on_submit(update_axis_range)
    ymax_box.on_submit(update_axis_range)
    zmin_box.on_submit(update_axis_range)
    zmax_box.on_submit(update_axis_range)

    plt.show()

def scatter_2d_cU(env):
    check_var = env.get('check_var')
    color_mode_var = env.get('color_mode_var')
    grid_var = env.get('grid_var')
    i = env.get('i')
    scale_s_Emax_txt_2 = env.get('scale_s_Emax_txt_2')
    scale_s_Emin_txt_2 = env.get('scale_s_Emin_txt_2')
    scale_s_Imax_txt_2 = env.get('scale_s_Imax_txt_2')
    scale_s_Imin_txt_2 = env.get('scale_s_Imin_txt_2')
    scale_s_Umax_txt_2 = env.get('scale_s_Umax_txt_2')
    scale_s_Umin_txt_2 = env.get('scale_s_Umin_txt_2')
    scale_s_Vmax_txt_2 = env.get('scale_s_Vmax_txt_2')
    scale_s_Vmin_txt_2 = env.get('scale_s_Vmin_txt_2')
    size_txt = env.get('size_txt')
    state = env.get('state')
    txt10 = env.get('txt10')
    txt11 = env.get('txt11')
    txt12 = env.get('txt12')
    txt13 = env.get('txt13')
    txt14 = env.get('txt14')
    txt9 = env.get('txt9')
    txt_3dsca_1u = env.get('txt_3dsca_1u')
    txt_3dsca_2u = env.get('txt_3dsca_2u')
    txt_dhw = env.get('txt_dhw')
    txt_pcs = env.get('txt_pcs')
    txt_rQ = env.get('txt_rQ')
    txt_ul = env.get('txt_ul')
    txt_vl = env.get('txt_vl')
    txt_vr_I1 = env.get('txt_vr_I1')
    txt_vr_I2 = env.get('txt_vr_I2')
    txt_vr_U1 = env.get('txt_vr_U1')
    txt_vr_U2 = env.get('txt_vr_U2')
    txt_vr_V1 = env.get('txt_vr_V1')
    txt_vr_V2 = env.get('txt_vr_V2')
    txt_vr_hw1 = env.get('txt_vr_hw1')
    txt_vr_hw2 = env.get('txt_vr_hw2')
    # 例: databox = np.loadtxt('your_file.dat')  # shape: (N, 6)
    # 各成分の抽出
    qx = state['databox'][0, :]
    qy = state['databox'][1, :]
    hw = state['databox'][3, :]  # ℏω（Z軸）
    try:
        # sb_databox が存在し、サイズも一致していれば差分で強度を定義
        if state['sb_databox'].shape == state['databox'].shape:
            intensity = state['databox'][4, :] - state['sb_databox'][4, :]
            intensity_err = np.sqrt(state['databox'][5, :]**2 + state['sb_databox'][5, :]**2)
        else:
            intensity = state['databox'][4, :]
            intensity_err = state['databox'][5, :]
    except NameError:
        # sb_databox が定義されていない場合
        intensity = state['databox'][4, :]
        intensity_err = state['databox'][5, :]

    # 強度の閾値を設定
    # 強度の下限と上限。これだけは設定しないと意味不明なので例外無し。
    I_min = float(txt_vr_I1.get())
    I_max = float(txt_vr_I2.get())

    # ℏω の下限・上限（例: 10 ～ 60 meV の間だけ可視化）
    if txt_vr_hw1.get()=="":
        hw_min = np.min(state['databox'][3, :])
    else:
        hw_min = float(txt_vr_hw1.get())
    if txt_vr_hw2.get()=="":
        hw_max = np.max(state['databox'][3, :])
    else:
        hw_max = float(txt_vr_hw2.get())

    # qxの下限・上限
    if txt_vr_U1.get()=="":
        qx_min = np.min(state['databox'][0, :])/state['NU1']
    else:
        qx_min = float(txt_vr_U1.get())
    if txt_vr_U2.get()=="":
        qx_max = np.max(state['databox'][0, :])/state['NU1']
    else:
        qx_max = float(txt_vr_U2.get())

    # qyの下限・上限
    if txt_vr_V1.get()=="":
        qy_min = np.min(state['databox'][1, :])/state['NV1']
    else:
        qy_min = float(txt_vr_V1.get())
    if txt_vr_V2.get()=="":
        qy_max = np.max(state['databox'][1, :])/state['NV1']
    else:
        qy_max = float(txt_vr_V2.get())

    # 強度が I_min 以上かつ I_max 以下の点だけを表示
    # 条件を組み合わせる
    mask1 = (
        (intensity >= I_min) & (intensity <= I_max) &
        (hw >= hw_min) & (hw <= hw_max) & 
        (qx >= qx_min*state['NU1']) & (qx <= qx_max*state['NU1']) & 
        (qy >= qy_min*state['NV1']) & (qy <= qy_max*state['NV1'])
    )

    if check_var.get(): # checkbox on
        # さらに、空間的に孤立している点をマスク
        # マスク1を通過したデータ
        qx_m = qx[mask1]
        qy_m = qy[mask1]
        hw_m = hw[mask1]
        coords = np.vstack((qx_m, qy_m)).T

        # さらにブラッグテイルなどの外れ値を除外する
        radius_q = float(txt_rQ.get()) # q空間での近傍半径 dq
        min_neighbors = float(txt_pcs.get())     # 最低近傍点数（孤立除去の基準）
        hw_window = float(txt_dhw.get())  # ± meV 以内のみを近傍とする

        # KDTree構築（qx, qy 空間）
        tree = KDTree(coords)

        # mask2作成：空間的に孤立していない点のみ通す
        neighbor_counts = []
        for i, point in enumerate(coords):
            # qx-qy 半径で候補点を取得
            idxs = tree.query_ball_point(point, r=radius_q)
            # 候補の中で hw が近いものだけに限定
            count = 0
            for j in idxs:
                if abs(hw_m[j] - hw_m[i]) <= hw_window:
                    count += 1
            neighbor_counts.append(count)

        neighbor_counts = np.array(neighbor_counts)
        mask2 = neighbor_counts >= min_neighbors

        # mask1 のインデックスを通じて final_mask を作成
        final_mask = mask1.copy()
        final_mask_indices = np.where(mask1)[0]
        final_mask[final_mask_indices[~mask2]] = False
    else:
        final_mask = mask1

    # マスクしたデータ
    x = qx[final_mask]
    y = qy[final_mask]
    z = hw[final_mask]
    c = intensity[final_mask]
    c_err = intensity_err[final_mask]

    # グラフスケール
    # グラフの軸設定
    if scale_s_Umin_txt_2.get()=="":
        xlim_min=round(qx_min,2)
    else:
        xlim_min=float(scale_s_Umin_txt_2.get())
    if scale_s_Umax_txt_2.get()=="":
        xlim_max=round(qx_max,2)
    else:
        xlim_max=float(scale_s_Umax_txt_2.get())

    if scale_s_Vmin_txt_2.get()=="":
        ylim_min=round(qy_min,2)
    else:
        ylim_min=float(scale_s_Vmin_txt_2.get())
    if scale_s_Vmax_txt_2.get()=="":
        ylim_max=round(qy_max,2)
    else:
        ylim_max=float(scale_s_Vmax_txt_2.get())

    if scale_s_Emin_txt_2.get()=="":
        zlim_min=round(hw_min, 2)
    else:
        zlim_min=float(scale_s_Emin_txt_2.get())
    if scale_s_Emax_txt_2.get()=="":
        zlim_max=round(hw_max, 2)
    else:
        zlim_max=float(scale_s_Emax_txt_2.get())

    # カラーバースケール。
    if scale_s_Imin_txt_2.get()=="":
        clim_min = round(I_min,2)
    else:
        clim_min=float(scale_s_Imin_txt_2.get())

    if scale_s_Imax_txt_2.get()=="":
        clim_max = round(I_max,2)
    else:
        clim_max=float(scale_s_Imax_txt_2.get())

    pt_s = float(size_txt.get()) # 散布図表示サイズ

    # スライス範囲
    U_min = float(txt_3dsca_1u.get())-float(txt_3dsca_2u.get())
    U_max = float(txt_3dsca_1u.get())+float(txt_3dsca_2u.get())

    # U方向でのスライス
    slice_mask = (x/state['NU1'] >= U_min) & (x/state['NU1'] <= U_max)

    # スライスされた x, y, 色
    x_slice = x[slice_mask]
    y_slice = y[slice_mask]
    c_slice = c[slice_mask]
    z_slice = z[slice_mask]
    c_err_slice = c_err[slice_mask]

    # データ結合
    # shared variables are stored in state
    state['masked_2d_constU'] = np.array([float(txt9.get())*x_slice/state['NU1'],float(txt10.get())*x_slice/state['NU1'],float(txt11.get())*x_slice/state['NU1'],
                                  float(txt12.get())*y_slice/state['NV1'],float(txt13.get())*y_slice/state['NV1'],float(txt14.get())*y_slice/state['NV1'],
                                  z_slice,c_slice,c_err_slice]).T

    x_center = (U_min + U_max) / 2
    x_error = (U_max - U_min) / 2

    # 図のラベルを作成
    if float(txt12.get())==0:
        if float(txt9.get())==0:
            vl1 = str('0')
        else:
            vl1 = str(float(txt9.get())*x_center)
    elif float(txt12.get())==1:
        if float(txt9.get())==0:
            vl1 = str(txt_vl.get())
        else:
            vl1 = str(float(txt9.get())*x_center)+str('+')+str(txt_vl.get())
    elif float(txt12.get())==-1:
        if float(txt9.get())==0:
            vl1 = str('-')+str(txt_vl.get())
        else:
            vl1 = str(float(txt9.get())*x_center)+str('-')+str(txt_vl.get())
    else:
        try:
            number1 = float(txt12.get())
            if number1.is_integer():#整数である
                if number1<0:#Vベクトルの値が負であった場合
                    if float(txt9.get())==0:
                        vl1 = str('-')+str(int(np.abs(float(txt12.get()))))+str(txt_vl.get())
                    else:
                        vl1 = str(float(txt9.get())*x_center)+str('-')+str(int(np.abs(float(txt12.get()))))+str(txt_vl.get())
                elif number1>0:#Vベクトルの値が正であった場合
                    if float(txt9.get())==0:
                        vl1 = str(int(float(txt12.get())))+str(txt_vl.get())
                    else:
                        vl1 = str(float(txt9.get())*x_center)+str('+')+str(int(float(txt12.get())))+str(txt_vl.get())
            else:#整数でない
                if number1<0:#Vベクトルの値が負であった場合
                    if float(txt9.get())==0:
                        vl1 = str('-')+str(np.abs(float(txt12.get())))+str(txt_vl.get())
                    else:
                        vl1 = str(float(txt9.get())*x_center)+str('-')+str(np.abs(float(txt12.get())))+str(txt_vl.get())
                elif number1>0:#Vベクトルの値が正であった場合
                    if float(txt9.get())==0:
                        vl1 = str(float(txt12.get()))+str(txt_vl.get())
                    else:
                        vl1 = str(float(txt9.get())*x_center)+str('+')+str(float(txt12.get()))+str(txt_vl.get())
        except ValueError:#整数でない
            pass

    if float(txt13.get())==0:
        if float(txt10.get())==0:
            vl2 = str('0')
        else:
            vl2 = str(float(txt10.get())*x_center)
    elif float(txt13.get())==1:
        if float(txt10.get())==0:
            vl2 = str(txt_vl.get())
        else:
            vl2 = str(float(txt10.get())*x_center)+str('+')+str(txt_vl.get())
    elif float(txt13.get())==-1:
        if float(txt10.get())==0:
            vl2 = str('-')+str(txt_vl.get())
        else:
            vl2 = str(float(txt10.get())*x_center)+str('-')+str(txt_vl.get())
    else:
        try:
            number2 = float(txt13.get())
            if number2.is_integer():#整数である
                if number2<0:#Vベクトルの値が負であった場合
                    if float(txt10.get())==0:
                        vl2 = str('-')+str(int(np.abs(float(txt13.get()))))+str(txt_vl.get())
                    else:
                        vl2 = str(float(txt10.get())*x_center)+str('-')+str(int(np.abs(float(txt13.get()))))+str(txt_vl.get())
                elif number2>0:#Vベクトルの値が正であった場合
                    if float(txt10.get())==0:
                        vl2 = str(int(float(txt13.get())))+str(txt_vl.get())
                    else:
                        vl2 = str(float(txt10.get())*x_center)+str('+')+str(int(float(txt13.get())))+str(txt_vl.get())
            else:#整数でない
                if number2<0:#Vベクトルの値が負であった場合
                    if float(txt10.get())==0:
                        vl2 = str('-')+str(np.abs(float(txt13.get())))+str(txt_vl.get())
                    else:
                        vl2 = str(float(txt10.get())*x_center)+str('-')+str(np.abs(float(txt13.get())))+str(txt_vl.get())
                elif number2>0:#Vベクトルの値が正であった場合
                    if float(txt10.get())==0:
                        vl2 = str(float(txt13.get()))+str(txt_vl.get())
                    else:
                        vl2 = str(float(txt10.get())*x_center)+str('+')+str(float(txt13.get()))+str(txt_vl.get())
        except ValueError:#整数でない
            pass

    if float(txt14.get())==0:
        if float(txt11.get())==0:
            vl3 = str('0')
        else:
            vl3 = str(float(txt11.get())*x_center)
    elif float(txt14.get())==1:
        if float(txt11.get())==0:
            vl3 = str(txt_vl.get())
        else:
            vl3 = str(float(txt11.get())*x_center)+str('+')+str(txt_vl.get())
    elif float(txt14.get())==-1:
        if float(txt11.get())==0:
            vl3 = str('-')+str(txt_vl.get())
        else:
            vl3 = str(float(txt11.get())*x_center)+str('-')+str(txt_vl.get())
    else:
        try:
            number3 = float(txt14.get())
            if number3.is_integer():#整数である
                if number3<0:#Vベクトルの値が負であった場合
                    if float(txt11.get())==0:
                        vl3 = str('-')+str(int(np.abs(float(txt14.get()))))+str(txt_vl.get())
                    else:
                        vl3 = str(float(txt11.get())*x_center)+str('-')+str(int(np.abs(float(txt14.get()))))+str(txt_vl.get())
                elif number3>0:#Vベクトルの値が正であった場合
                    if float(txt11.get())==0:
                        vl3 = str(int(float(txt14.get())))+str(txt_vl.get())
                    else:
                        vl3 = str(float(txt11.get())*x_center)+str('+')+str(int(float(txt14.get())))+str(txt_vl.get())
            else:#整数でない
                if number3<0:#Vベクトルの値が負であった場合
                    if float(txt11.get())==0:
                        vl3 = str('-')+str(np.abs(float(txt14.get())))+str(txt_vl.get())
                    else:
                        vl3 = str(float(txt11.get())*x_center)+str('-')+str(np.abs(float(txt14.get())))+str(txt_vl.get())
                elif number3>0:#Vベクトルの値が正であった場合
                    if float(txt11.get())==0:
                        vl3 = str(float(txt14.get()))+str(txt_vl.get())
                    else:
                        vl3 = str(float(txt11.get())*x_center)+str('+')+str(float(txt14.get()))+str(txt_vl.get())
        except ValueError:#整数でない
            pass

    Vlabel2 = (f"({vl1},{vl2},{vl3})")

    # プロット
    fig, ax = plt.subplots()
    fig.subplots_adjust(left=0.30, right=0.75, bottom=0.2)

    if color_mode_var.get() == "coloroff":
        # 単色（グレー）でプロット（この場合 c_slice 等は使わない）
        sc = ax.scatter(y_slice/state['NV1'], z_slice, color='gray', s=pt_s)
    else:
        # カラーマップでプロット（linear / log 共通部分）
        sc = ax.scatter(y_slice/state['NV1'], z_slice, c=c_slice, cmap='jet',
                        s=pt_s, vmin=clim_min, vmax=clim_max)

        # カラーバー設定
        cbar = fig.colorbar(sc, ax=ax, label='Intensity (a. u.)')
        if color_mode_var.get() == "linear":
            cbar.locator = mticker.LinearLocator(numticks=3)
        elif color_mode_var.get() == "log":
            cbar.locator = mticker.LogLocator(numticks=3)
        cbar.update_ticks()

    ax.set_xlabel(str(Vlabel2))
    ax.set_ylabel("ℏω (meV)")
    #plt.title(f"2D Slice: {z_min} ≤ ℏω ≤ {z_max} meV")
    ax.set_title(f"{txt_ul.get()} = {x_center:.3f} ± {x_error:.3f} (r.l.u.)")

    ax.grid(grid_var.get())

    ax.set_xlim(ylim_min, ylim_max)
    ax.set_ylim(zlim_min, zlim_max)

    # 初期値設定
    default_xmin = round(ylim_min, 3)
    default_xmax = round(ylim_max, 3)
    default_ymin = round(zlim_min, 3)
    default_ymax = round(zlim_max, 3)
    default_zmin = round(clim_min, 3)
    default_zmax = round(clim_max, 3)

    # TextBox配置
    xmin_box = TextBox(plt.axes([0.3, 0.02, 0.08, 0.05]), 'xMin:', initial=str(default_xmin))
    xmax_box = TextBox(plt.axes([0.6, 0.02, 0.08, 0.05]), 'xMax:', initial=str(default_xmax))
    ymin_box = TextBox(plt.axes([0.1, 0.2, 0.08, 0.05]), 'yMin:', initial=str(default_ymin))
    ymax_box = TextBox(plt.axes([0.1, 0.83, 0.08, 0.05]), 'yMax:', initial=str(default_ymax))
    zmin_box = TextBox(plt.axes([0.9, 0.2, 0.08, 0.05]), 'zMin:', initial=str(default_zmin))
    zmax_box = TextBox(plt.axes([0.9, 0.83, 0.08, 0.05]), 'zMax:', initial=str(default_zmax))

    # スケール変更関数
    def update_axis_range(text):
        try:
            xmin_val = float(xmin_box.text)
            xmax_val = float(xmax_box.text)
            ymin_val = float(ymin_box.text)
            ymax_val = float(ymax_box.text)
            zmin_val = float(zmin_box.text)
            zmax_val = float(zmax_box.text)

            ax.set_xlim(xmin_val, xmax_val)
            ax.set_ylim(ymin_val, ymax_val)
            sc.set_clim(vmin=zmin_val, vmax=zmax_val)
            fig.canvas.draw_idle()
        except ValueError:
            pass  # 無効な入力は無視

    # イベント登録
    xmin_box.on_submit(update_axis_range)
    xmax_box.on_submit(update_axis_range)
    ymin_box.on_submit(update_axis_range)
    ymax_box.on_submit(update_axis_range)
    zmin_box.on_submit(update_axis_range)
    zmax_box.on_submit(update_axis_range)

    plt.show()

def scatter_2d_cV(env):
    check_var = env.get('check_var')
    color_mode_var = env.get('color_mode_var')
    grid_var = env.get('grid_var')
    i = env.get('i')
    scale_s_Emax_txt_2 = env.get('scale_s_Emax_txt_2')
    scale_s_Emin_txt_2 = env.get('scale_s_Emin_txt_2')
    scale_s_Imax_txt_2 = env.get('scale_s_Imax_txt_2')
    scale_s_Imin_txt_2 = env.get('scale_s_Imin_txt_2')
    scale_s_Umax_txt_2 = env.get('scale_s_Umax_txt_2')
    scale_s_Umin_txt_2 = env.get('scale_s_Umin_txt_2')
    scale_s_Vmax_txt_2 = env.get('scale_s_Vmax_txt_2')
    scale_s_Vmin_txt_2 = env.get('scale_s_Vmin_txt_2')
    size_txt = env.get('size_txt')
    state = env.get('state')
    txt10 = env.get('txt10')
    txt11 = env.get('txt11')
    txt12 = env.get('txt12')
    txt13 = env.get('txt13')
    txt14 = env.get('txt14')
    txt9 = env.get('txt9')
    txt_3dsca_1v = env.get('txt_3dsca_1v')
    txt_3dsca_2v = env.get('txt_3dsca_2v')
    txt_dhw = env.get('txt_dhw')
    txt_pcs = env.get('txt_pcs')
    txt_rQ = env.get('txt_rQ')
    txt_ul = env.get('txt_ul')
    txt_vr_I1 = env.get('txt_vr_I1')
    txt_vr_I2 = env.get('txt_vr_I2')
    txt_vr_U1 = env.get('txt_vr_U1')
    txt_vr_U2 = env.get('txt_vr_U2')
    txt_vr_V1 = env.get('txt_vr_V1')
    txt_vr_V2 = env.get('txt_vr_V2')
    txt_vr_hw1 = env.get('txt_vr_hw1')
    txt_vr_hw2 = env.get('txt_vr_hw2')
    # 例: databox = np.loadtxt('your_file.dat')  # shape: (N, 6)
    # 各成分の抽出
    qx = state['databox'][0, :]
    qy = state['databox'][1, :]
    hw = state['databox'][3, :]  # ℏω（Z軸）
    try:
        # sb_databox が存在し、サイズも一致していれば差分で強度を定義
        if state['sb_databox'].shape == state['databox'].shape:
            intensity = state['databox'][4, :] - state['sb_databox'][4, :]
            intensity_err = np.sqrt(state['databox'][5, :]**2 + state['sb_databox'][5, :]**2)
        else:
            intensity = state['databox'][4, :]
            intensity_err = state['databox'][5, :]
    except NameError:
        # sb_databox が定義されていない場合
        intensity = state['databox'][4, :]
        intensity_err = state['databox'][5, :]

    # 強度の閾値を設定
    # 強度の下限と上限。これだけは設定しないと意味不明なので例外無し。
    I_min = float(txt_vr_I1.get())
    I_max = float(txt_vr_I2.get())

    # ℏω の下限・上限（例: 10 ～ 60 meV の間だけ可視化）
    if txt_vr_hw1.get()=="":
        hw_min = np.min(state['databox'][3, :])
    else:
        hw_min = float(txt_vr_hw1.get())
    if txt_vr_hw2.get()=="":
        hw_max = np.max(state['databox'][3, :])
    else:
        hw_max = float(txt_vr_hw2.get())

    # qxの下限・上限
    if txt_vr_U1.get()=="":
        qx_min = np.min(state['databox'][0, :])/state['NU1']
    else:
        qx_min = float(txt_vr_U1.get())
    if txt_vr_U2.get()=="":
        qx_max = np.max(state['databox'][0, :])/state['NU1']
    else:
        qx_max = float(txt_vr_U2.get())

    # qyの下限・上限
    if txt_vr_V1.get()=="":
        qy_min = np.min(state['databox'][1, :])/state['NV1']
    else:
        qy_min = float(txt_vr_V1.get())
    if txt_vr_V2.get()=="":
        qy_max = np.max(state['databox'][1, :])/state['NV1']
    else:
        qy_max = float(txt_vr_V2.get())

    # 強度が I_min 以上かつ I_max 以下の点だけを表示
    # 条件を組み合わせる
    mask1 = (
        (intensity >= I_min) & (intensity <= I_max) &
        (hw >= hw_min) & (hw <= hw_max) & 
        (qx >= qx_min*state['NU1']) & (qx <= qx_max*state['NU1']) & 
        (qy >= qy_min*state['NV1']) & (qy <= qy_max*state['NV1'])
    )

    if check_var.get(): # checkbox on
        # さらに、空間的に孤立している点をマスク
        # マスク1を通過したデータ
        qx_m = qx[mask1]
        qy_m = qy[mask1]
        hw_m = hw[mask1]
        coords = np.vstack((qx_m, qy_m)).T

        # さらにブラッグテイルなどの外れ値を除外する
        radius_q = float(txt_rQ.get()) # q空間での近傍半径 dq
        min_neighbors = float(txt_pcs.get())     # 最低近傍点数（孤立除去の基準）
        hw_window = float(txt_dhw.get())  # ± meV 以内のみを近傍とする

        # KDTree構築（qx, qy 空間）
        tree = KDTree(coords)

        # mask2作成：空間的に孤立していない点のみ通す
        neighbor_counts = []
        for i, point in enumerate(coords):
            # qx-qy 半径で候補点を取得
            idxs = tree.query_ball_point(point, r=radius_q)
            # 候補の中で hw が近いものだけに限定
            count = 0
            for j in idxs:
                if abs(hw_m[j] - hw_m[i]) <= hw_window:
                    count += 1
            neighbor_counts.append(count)

        neighbor_counts = np.array(neighbor_counts)
        mask2 = neighbor_counts >= min_neighbors

        # mask1 のインデックスを通じて final_mask を作成
        final_mask = mask1.copy()
        final_mask_indices = np.where(mask1)[0]
        final_mask[final_mask_indices[~mask2]] = False
    else:
        final_mask = mask1

    # マスクしたデータ
    x = qx[final_mask]
    y = qy[final_mask]
    z = hw[final_mask]
    c = intensity[final_mask]
    c_err = intensity_err[final_mask]

    # グラフスケール
    # グラフの軸設定
    if scale_s_Umin_txt_2.get()=="":
        xlim_min=round(qx_min,2)
    else:
        xlim_min=float(scale_s_Umin_txt_2.get())
    if scale_s_Umax_txt_2.get()=="":
        xlim_max=round(qx_max,2)
    else:
        xlim_max=float(scale_s_Umax_txt_2.get())

    if scale_s_Vmin_txt_2.get()=="":
        ylim_min=round(qy_min,2)
    else:
        ylim_min=float(scale_s_Vmin_txt_2.get())
    if scale_s_Vmax_txt_2.get()=="":
        ylim_max=round(qy_max,2)
    else:
        ylim_max=float(scale_s_Vmax_txt_2.get())

    if scale_s_Emin_txt_2.get()=="":
        zlim_min=round(hw_min, 2)
    else:
        zlim_min=float(scale_s_Emin_txt_2.get())
    if scale_s_Emax_txt_2.get()=="":
        zlim_max=round(hw_max, 2)
    else:
        zlim_max=float(scale_s_Emax_txt_2.get())

    # カラーバースケール。
    if scale_s_Imin_txt_2.get()=="":
        clim_min = round(I_min,2)
    else:
        clim_min=float(scale_s_Imin_txt_2.get())

    if scale_s_Imax_txt_2.get()=="":
        clim_max = round(I_max,2)
    else:
        clim_max=float(scale_s_Imax_txt_2.get())

    pt_s = float(size_txt.get()) # 散布図表示サイズ

    # スライス範囲
    V_min = float(txt_3dsca_1v.get())-float(txt_3dsca_2v.get())
    V_max = float(txt_3dsca_1v.get())+float(txt_3dsca_2v.get())

    # U方向でのスライス
    slice_mask = (y/state['NV1'] >= V_min) & (y/state['NV1'] <= V_max)

    # スライスされた x, y, 色
    x_slice = x[slice_mask]
    y_slice = y[slice_mask]
    c_slice = c[slice_mask]
    z_slice = z[slice_mask]
    c_err_slice = c_err[slice_mask]

    # データ結合
    # shared variables are stored in state
    state['masked_2d_constV'] = np.array([float(txt9.get())*x_slice/state['NU1'],float(txt10.get())*x_slice/state['NU1'],float(txt11.get())*x_slice/state['NU1'],
                                  float(txt12.get())*y_slice/state['NV1'],float(txt13.get())*y_slice/state['NV1'],float(txt14.get())*y_slice/state['NV1'],
                                  z_slice,c_slice,c_err_slice]).T

    y_center = (V_min + V_max) / 2
    y_error = (V_max - V_min) / 2

    # 図のラベルを作成
    if float(txt9.get())==0:
        if float(txt12.get())==0:
            ul1 = str('0')
        else:
            ul1 = str(float(txt12.get())*y_center)
    elif float(txt9.get())==1:
        if float(txt12.get())==0:
            ul1 = str(txt_ul.get())
        else:
            ul1 = str(float(txt12.get())*y_center)+str('+')+str(txt_ul.get())
    elif float(txt9.get())==-1:
        if float(txt12.get())==0:
            ul1 = str('-')+str(txt_ul.get())
        else:
            ul1 = str(float(txt12.get())*y_center)+str('-')+str(txt_ul.get())
    else:
        try:
            number1 = float(txt9.get())
            if number1.is_integer():#整数である
                if number1<0:#Vベクトルの値が負であった場合
                    if float(txt12.get())==0:
                        ul1 = str('-')+str(int(np.abs(float(txt9.get()))))+str(txt_ul.get())
                    else:
                        ul1 = str(float(txt12.get())*y_center)+str('-')+str(int(np.abs(float(txt9.get()))))+str(txt_ul.get())
                elif number1>0:#Vベクトルの値が正であった場合
                    if float(txt12.get())==0:
                        ul1 = str(int(np.abs(float(txt9.get()))))+str(txt_ul.get())
                    else:
                        ul1 = str(float(txt12.get())*y_center)+str('+')+str(int(float(txt9.get())))+str(txt_ul.get())
            else:#整数でない
                if number1<0:#Vベクトルの値が負であった場合
                    if float(txt12.get())==0:
                        ul1 = str('-')+str(np.abs(float(txt9.get())))+str(txt_ul.get())
                    else:
                        ul1 = str(float(txt12.get())*y_center)+str('-')+str(np.abs(float(txt9.get())))+str(txt_ul.get())
                elif number1>0:#Vベクトルの値が正であった場合
                    if float(txt12.get())==0:
                        ul1 = str(np.abs(float(txt9.get())))+str(txt_ul.get())
                    else:
                        ul1 = str(float(txt12.get())*y_center)+str('+')+str(float(txt9.get()))+str(txt_ul.get())
        except ValueError:#整数でない
            pass

    if float(txt10.get())==0:
        if float(txt13.get())==0:
            ul2 = str('0')
        else:
            ul2 = str(float(txt13.get())*y_center)
    elif float(txt10.get())==1:
        if float(txt13.get())==0:
            ul2 = str(txt_ul.get())
        else:
            ul2 = str(float(txt13.get())*y_center)+str('+')+str(txt_ul.get())
    elif float(txt10.get())==-1:
        if float(txt13.get())==0:
            ul2 = str('-')+str(txt_ul.get())
        else:
            ul2 = str(float(txt13.get())*y_center)+str('-')+str(txt_ul.get())
    else:
        try:
            number2 = float(txt10.get())
            if number2.is_integer():#整数である
                if number2<0:#Vベクトルの値が負であった場合
                    if float(txt13.get())==0:
                        ul2 = str('-')+str(int(np.abs(float(txt10.get()))))+str(txt_ul.get())
                    else:
                        ul2 = str(float(txt13.get())*y_center)+str('-')+str(int(np.abs(float(txt10.get()))))+str(txt_ul.get())
                elif number2>0:#Vベクトルの値が正であった場合
                    if float(txt13.get())==0:
                        ul2 = str(int(np.abs(float(txt10.get()))))+str(txt_ul.get())
                    else:
                        ul2 = str(float(txt13.get())*y_center)+str('+')+str(int(float(txt10.get())))+str(txt_ul.get())
            else:#整数でない
                if number2<0:#Vベクトルの値が負であった場合
                    if float(txt13.get())==0:
                        ul2 = str('-')+str(np.abs(float(txt10.get())))+str(txt_ul.get())
                    else:
                        ul2 = str(float(txt13.get())*y_center)+str('-')+str(np.abs(float(txt10.get())))+str(txt_ul.get())
                elif number2>0:#Vベクトルの値が正であった場合
                    if float(txt13.get())==0:
                        ul2 = str(np.abs(float(txt10.get())))+str(txt_ul.get())
                    else:
                        ul2 = str(float(txt13.get())*y_center)+str('+')+str(float(txt10.get()))+str(txt_ul.get())
        except ValueError:#整数でない
            pass

    if float(txt11.get())==0:
        if float(txt14.get())==0:
            ul3 = str('0')
        else:
            ul3 = str(float(txt14.get())*y_center)
    elif float(txt11.get())==1:
        if float(txt14.get())==0:
            ul3 = str(txt_ul.get())
        else:
            ul3 = str(float(txt14.get())*y_center)+str('+')+str(txt_ul.get())
    elif float(txt11.get())==-1:
        if float(txt14.get())==0:
            ul3 = str('-')+str(txt_ul.get())
        else:
            ul3 = str(float(txt14.get())*y_center)+str('-')+str(txt_ul.get())
    else:
        try:
            number3 = float(txt11.get())
            if number3.is_integer():#整数である
                if number3<0:#Vベクトルの値が負であった場合
                    if float(txt14.get())==0:
                        ul2 = str('-')+str(int(np.abs(float(txt11.get()))))+str(txt_ul.get())
                    else:
                        ul2 = str(float(txt14.get())*y_center)+str('-')+str(int(np.abs(float(txt11.get()))))+str(txt_ul.get())
                elif number3>0:#Vベクトルの値が正であった場合
                    if float(txt14.get())==0:
                        ul2 = str(int(np.abs(float(txt11.get()))))+str(txt_ul.get())
                    else:
                        ul2 = str(float(txt14.get())*y_center)+str('+')+str(int(float(txt11.get())))+str(txt_ul.get())
            else:#整数でない
                if number3<0:#Vベクトルの値が負であった場合
                    if float(txt14.get())==0:
                        ul2 = str('-')+str(np.abs(float(txt11.get())))+str(txt_ul.get())
                    else:
                        ul2 = str(float(txt14.get())*y_center)+str('-')+str(np.abs(float(txt11.get())))+str(txt_ul.get())
                elif number3>0:#Vベクトルの値が正であった場合
                    if float(txt14.get())==0:
                        ul2 = str(np.abs(float(txt11.get())))+str(txt_ul.get())
                    else:
                        ul2 = str(float(txt14.get())*y_center)+str('+')+str(float(txt11.get()))+str(txt_ul.get())
        except ValueError:#整数でない
            pass

    Ulabel2 = (f"({ul1},{ul2},{ul3})")

    # プロット
    fig, ax = plt.subplots()
    fig.subplots_adjust(left=0.30, right=0.75, bottom=0.2)

    # カラーモードに応じて scatter と colorbar の描画
    if color_mode_var.get() == "coloroff":
        # 単色（例：グレー）で描画
        sc = ax.scatter(x/state['NU1'], z, color='gray', s=pt_s)
    else:
        # 通常のカラーマッピング（線形または対数）
        sc = ax.scatter(x_slice/state['NU1'], z_slice, c=c_slice, cmap='jet', s=pt_s,
                        vmin=clim_min, vmax=clim_max)

        if color_mode_var.get() == "linear":
            cbar = fig.colorbar(sc, ax=ax, label='Intensity (a. u.)')
            cbar.locator = mticker.LinearLocator(numticks=3)
            cbar.update_ticks()
        elif color_mode_var.get() == "log":
            cbar = fig.colorbar(sc, ax=ax, label='Intensity (a. u.)')
            cbar.locator = mticker.LogLocator(numticks=3)
            cbar.update_ticks()

    ax.grid(grid_var.get())
    ax.set_xlim(xlim_min, xlim_max)
    ax.set_ylim(zlim_min, zlim_max)

    # 初期値設定
    default_xmin = round(xlim_min, 3)
    default_xmax = round(xlim_max, 3)
    default_ymin = round(zlim_min, 3)
    default_ymax = round(zlim_max, 3)
    default_zmin = round(clim_min, 3)
    default_zmax = round(clim_max, 3)

    # TextBox配置
    xmin_box = TextBox(plt.axes([0.3, 0.02, 0.08, 0.05]), 'xMin:', initial=str(default_xmin))
    xmax_box = TextBox(plt.axes([0.6, 0.02, 0.08, 0.05]), 'xMax:', initial=str(default_xmax))
    ymin_box = TextBox(plt.axes([0.1, 0.2, 0.08, 0.05]), 'yMin:', initial=str(default_ymin))
    ymax_box = TextBox(plt.axes([0.1, 0.83, 0.08, 0.05]), 'yMax:', initial=str(default_ymax))
    zmin_box = TextBox(plt.axes([0.9, 0.2, 0.08, 0.05]), 'zMin:', initial=str(default_zmin))
    zmax_box = TextBox(plt.axes([0.9, 0.83, 0.08, 0.05]), 'zMax:', initial=str(default_zmax))

    # スケール変更関数
    def update_axis_range(text):
        try:
            xmin_val = float(xmin_box.text)
            xmax_val = float(xmax_box.text)
            ymin_val = float(ymin_box.text)
            ymax_val = float(ymax_box.text)
            zmin_val = float(zmin_box.text)
            zmax_val = float(zmax_box.text)

            ax.set_xlim(xmin_val, xmax_val)
            ax.set_ylim(ymin_val, ymax_val)
            sc.set_clim(vmin=zmin_val, vmax=zmax_val)
            fig.canvas.draw_idle()
        except ValueError:
            pass  # 無効な入力は無視

    # イベント登録
    xmin_box.on_submit(update_axis_range)
    xmax_box.on_submit(update_axis_range)
    ymin_box.on_submit(update_axis_range)
    ymax_box.on_submit(update_axis_range)
    zmin_box.on_submit(update_axis_range)
    zmax_box.on_submit(update_axis_range)

    plt.show()

def show_3DconEmap(env):
    axistype = env.get('axistype')
    gridtype = env.get('gridtype')
    scale_s_Imax_txt = env.get('scale_s_Imax_txt')
    scale_s_Imin_txt = env.get('scale_s_Imin_txt')
    scale_s_Umax_txt = env.get('scale_s_Umax_txt')
    scale_s_Umin_txt = env.get('scale_s_Umin_txt')
    scale_s_Vmax_txt = env.get('scale_s_Vmax_txt')
    scale_s_Vmin_txt = env.get('scale_s_Vmin_txt')
    state = env.get('state')
    txt_3d_ini_hw = env.get('txt_3d_ini_hw')
    # 初期値
    if txt_3d_ini_hw.get()=="":
        sa1 = 0
    else:
        # 一番近い値を探す
        # energylistをNumPy配列に変換
        energylist_np = np.array(state['energylist'])
        sa1 = np.abs(energylist_np - float(txt_3d_ini_hw.get())).argmin()

    # 軸設定。空欄の場合は範囲マックスを表示するようにする
    if scale_s_Umin_txt.get()=="":
        Ulim_min=round(np.min(state['QU']),2)
    else:
        Ulim_min=float(scale_s_Umin_txt.get())
    if scale_s_Umax_txt.get()=="":
        Ulim_max=round(np.max(state['QU']),2)
    else:
        Ulim_max=float(scale_s_Umax_txt.get())

    if scale_s_Vmin_txt.get()=="":
        Vlim_min=round(np.min(state['QV']),2)
    else:
        Vlim_min=float(scale_s_Vmin_txt.get())
    if scale_s_Vmax_txt.get()=="":
        Vlim_max=round(np.max(state['QV']),2)
    else:
        Vlim_max=float(scale_s_Vmax_txt.get())

    # カラーバースケール。空欄の場合は平均値を出力するようにする。
    if scale_s_Imin_txt.get()=="":
        if np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]) >= 0:
            z_min=0
        elif np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]) < 0:
            z_min=round(np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]),1)
    else:
        z_min=float(scale_s_Imin_txt.get())

    if scale_s_Imax_txt.get()=="":
        if np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]) >= 0:
            z_max=round(np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]),1)
        elif np.mean(state['databox'][4,:])+np.mean(state['databox'][5,:]) < 0:
            z_max=0
    else:
        z_max=float(scale_s_Imax_txt.get())

    # カラーバースケールを線形かリニアで

    #図を出力する
    #intensityの範囲
    #fig, ax = plt.figure()
    #axにカラーバーを表示
    fig1, ax = plt.subplots()
    #plt.subplots_adjust(left=0.15, bottom=0.25)
    plt.subplots_adjust(left=0.30, right=0.75, bottom=0.25)  # マージンを調整してグラフを中央に配置
    ax.set_xlim(Ulim_min,Ulim_max)
    ax.set_ylim(Vlim_min,Vlim_max)
    at=axistype.get()

    # アスペクト比を変更
    ax.set_aspect(state['NV1']/state['NU1'])
    # グリッド線を引く
    gt=gridtype.get()
    if gt == 0:
        #ax.set_axisbelow(True)  # グリッド線を背面に配置
        ax.grid(False)
    elif gt == 1:
        ax.grid(True)

    if at==0:
        im=plt.pcolormesh(state['QU'], state['QV'], state['I'][sa1,:,:], cmap='jet', vmin=z_min, vmax=z_max)
    elif at==1:
        if z_min==0:
            z_min=np.nanmin(state['I'][state['I'] != 0])
            im=plt.pcolormesh(state['QU'], state['QV'], state['I'][sa1,:,:], cmap='jet', norm = LogNorm(vmin=np.nanmin(state['I'][state['I'] != 0]), vmax=z_max))
        else:
            im=plt.pcolormesh(state['QU'], state['QV'], state['I'][sa1,:,:], cmap='jet', norm = LogNorm(vmin=z_min, vmax=z_max))
    #sb1=z_max#初期値を一応セット
    cbar=plt.colorbar(im,ticks=mticker.LinearLocator(numticks=3))#カラーバーの目盛りについて最小値、中央値、最大値を表示する。
    # カラーバーのタイトルを設定
    cbar.set_label('Intenisty (a.u.)')
    ax.set_xlabel(str(state['Ulabel']))
    ax.set_ylabel(str(state['Vlabel']))
    #, cmap="jet", extend='both',ticks=np.linspace(vmin, vmax, 5)
    #plt.axis('tight')
    #横スライドでエネルギートランスファーを変更、縦スライドで強度の最大値を変更
    ax_a = plt.axes([0.3, 0.02, 0.45, 0.04]) #plt.axes([x, y, width, height] ) 
    sli_a1 = wg.Slider(ax_a, 'ℏω', 0, len(state['energylist'])-1, valinit=sa1,valstep=1, orientation='horizontal')
    ax.text(0.1,1.01,'ℏω = %.3f meV' %state['energylist'][sa1], transform=ax.transAxes)

    # グラフ内に表示範囲を決定するボックス
    # 最小値と最大値の初期値
    default_xmin = round(Ulim_min, 3)
    default_xmax = round(Ulim_max, 3)

    default_ymin = round(Vlim_min, 3)
    default_ymax = round(Vlim_max, 3)

    default_zmin = round(z_min, 3)
    default_zmax = round(z_max, 3)

    # テキストボックスを作成して最小値と最大値を設定
    xmin_box = TextBox(plt.axes([0.3, 0.1, 0.08, 0.05]), 'xMin:', initial=str(default_xmin))
    xmax_box = TextBox(plt.axes([0.6, 0.1, 0.08, 0.05]), 'xMax:', initial=str(default_xmax))

    ymin_box = TextBox(plt.axes([0.1, 0.2, 0.08, 0.05]), 'yMin:', initial=str(default_ymin))
    ymax_box = TextBox(plt.axes([0.1, 0.83, 0.08, 0.05]), 'yMax:', initial=str(default_ymax))

    zmin_box = TextBox(plt.axes([0.9, 0.2, 0.08, 0.05]), 'zMin:', initial=str(default_zmin))
    zmax_box = TextBox(plt.axes([0.9, 0.83, 0.08, 0.05]), 'zMax:', initial=str(default_zmax))

    def update1(val):
        ax.clear()

        xmin_val = float(xmin_box.text)
        xmax_val = float(xmax_box.text)
        ymin_val = float(ymin_box.text)
        ymax_val = float(ymax_box.text)
        zmin_val = float(zmin_box.text)
        zmax_val = float(zmax_box.text)

        # グリッド線を引く
        gt=gridtype.get()
        if gt == 0:
            #ax.set_axisbelow(True)  # グリッド線を背面に配置
            ax.grid(False)
        elif gt == 1:
            ax.grid(True)
        sa1 = sli_a1.val
        ax.text(0.1,1.01,'ℏω = %.3f meV' %state['energylist'][sa1], transform=ax.transAxes)
        #ax.pcolormesh(QU, QV, I[sa1,:,:], cmap='jet', vmin=z_min, vmax=sb1)
        if at==0:
            ax.pcolormesh(state['QU'], state['QV'], state['I'][sa1,:,:], cmap='jet', vmin=zmin_val, vmax=zmax_val)
            cbar.mappable.set_clim(vmin=zmin_val, vmax=zmax_val)  # カラーバーのレンジを更新
            fig1.canvas.draw_idle()
        elif at==1:
            if zmin_val==0:
                ax.pcolormesh(state['QU'], state['QV'], state['I'][sa1,:,:], cmap='jet', norm = LogNorm(vmin=np.nanmin(state['I'][state['I'] != 0]), vmax=zmax_val))
                cbar.mappable.set_clim(vmin=np.nanmin(state['I'][state['I'] != 0]), vmax=zmax_val)  # カラーバーのレンジを更新
                fig1.canvas.draw_idle()
            else:
                ax.pcolormesh(state['QU'], state['QV'], state['I'][sa1,:,:], cmap='jet', norm = LogNorm(vmin=zmin_val, vmax=zmax_val))
                cbar.mappable.set_clim(vmin=zmin_val, vmax=zmax_val)  # カラーバーのレンジを更新
                fig1.canvas.draw_idle()
        ax.set_xlabel(str(state['Ulabel']))
        ax.set_ylabel(str(state['Vlabel']))
        ax.set_xlim(xmin_val,xmax_val) # x軸のレンジを更新
        ax.set_ylim(ymin_val,ymax_val) # y軸のレンジを更新

    # 矢印キーにスライダを対応。上限を超えて表示しないように設定。
    def on_key(event):
        if event.key == 'right':
            new_val_a = min(sli_a1.val + 1, sli_a1.valmax)
            sli_a1.set_val(new_val_a)
        elif event.key == 'left':
            new_val_a = max(sli_a1.val - 1, sli_a1.valmin)
            sli_a1.set_val(new_val_a)
    fig1.canvas.mpl_connect('key_press_event', on_key)
    sli_a1.on_changed(update1)

    # 最小値と最大値が変更されたときに呼び出される関数
    def update_axis_range(text):
        try:
            xmin_val = float(xmin_box.text)
            xmax_val = float(xmax_box.text)
            ax.set_xlim(xmin_val, xmax_val)
            ymin_val = float(ymin_box.text)
            ymax_val = float(ymax_box.text)
            ax.set_ylim(ymin_val, ymax_val)
            zmin_val = float(zmin_box.text)
            zmax_val = float(zmax_box.text)
            cbar.mappable.set_clim(vmin=zmin_val, vmax=zmax_val)
            fig1.canvas.draw_idle()
            update1(None)  # テキストボックスの値が変更されたらグラフを更新する
            return xmin_val,xmax_val,ymin_val,ymax_val,zmin_val,zmax_val
        except ValueError:
            pass

    xmin_box.on_submit(update_axis_range)
    xmax_box.on_submit(update_axis_range)
    ymin_box.on_submit(update_axis_range)
    ymax_box.on_submit(update_axis_range)
    zmin_box.on_submit(update_axis_range)
    zmax_box.on_submit(update_axis_range)

    plt.show()
