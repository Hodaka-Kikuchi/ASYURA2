from ...callback_runtime import *

from .ub_display import show_ubmatrix

def loadfile(env):
    bg_type = env.get('bg_type')
    bgt_txt1 = env.get('bgt_txt1')
    bgt_txt4 = env.get('bgt_txt4')
    bgt_txt5 = env.get('bgt_txt5')
    check_vars = env.get('check_vars')
    i = env.get('i')
    sbListbox = env.get('sbListbox')
    sbtype1 = env.get('sbtype1')
    sbtype2 = env.get('sbtype2')
    state = env.get('state')
    txt1 = env.get('txt1')
    txt10 = env.get('txt10')
    txt11 = env.get('txt11')
    txt12 = env.get('txt12')
    txt13 = env.get('txt13')
    txt14 = env.get('txt14')
    txt15 = env.get('txt15')
    txt2 = env.get('txt2')
    txt3 = env.get('txt3')
    txt4 = env.get('txt4')
    txt5 = env.get('txt5')
    txt6 = env.get('txt6')
    txt9 = env.get('txt9')
    txt_ref_a2 = env.get('txt_ref_a2')
    txt_ref_c2 = env.get('txt_ref_c2')
    txt_ref_ef = env.get('txt_ref_ef')
    txt_ref_ei = env.get('txt_ref_ei')
    txt_ref_h = env.get('txt_ref_h')
    txt_ref_k = env.get('txt_ref_k')
    txt_ref_l = env.get('txt_ref_l')
    txt_ref_rx = env.get('txt_ref_rx')
    txt_ref_ry = env.get('txt_ref_ry')
    txt_ul = env.get('txt_ul')
    txt_vl = env.get('txt_vl')
    update_phi = env.get('update_phi')
    var = env.get('var')
    _show_ubmatrix = lambda UB: show_ubmatrix(env, UB)
    # 補正用fittingは常に毎回行う。変なファイルを選んだ時にcalibrationを毎回押すのはめんどくさい。そんなに時間もかからないし。
    # fittingから検出器効率の補正値を算出する
    with open(state['vfile_path'][0], "r", encoding="utf-8") as f:
        line = f.readlines()
        chead = line[31]
        chead2 = chead.split()
        if "Pt." in chead2:
            pass
        else:
            chead = line[32]
            chead2 = chead.split()

        #パラメータは何番目ですか？
        No_Pt=chead2.index('Pt.')
        No_c2=chead2.index('c2')
        No_a2=chead2.index('a2')
        No_timeact=chead2.index('time-act')
        #mcuは最初から読み込まない
        No_e=chead2.index('e')
        No_ei=chead2.index('ei')
        No_D01=chead2.index('D01')
        No_D24=chead2.index('D24')

    #リストにあるファイルを順に読み込んでいく
    with open(state['vfile_path'][0],"r", encoding="utf-8") as f:
        #選択ファイルの数値を全て読み込む
        vrdb = np.loadtxt(state['vfile_path'][0], comments='#')

    t_a = vrdb[:,No_timeact-1]
    # time-actが0のデータを検索
    Ind_t0 = np.where(t_a == 0)
    # time-actが0のデータを削除
    vrdb = np.delete(vrdb, Ind_t0, axis=0)

    pt = vrdb[:,No_Pt-1]
    c2 = vrdb[:,No_c2-1]
    a2 = vrdb[:,No_a2-1]

    e = vrdb[:,No_e-1]
    ei = vrdb[:,No_ei-1]
    D_I = vrdb[:,No_D01-1:No_D24]

    #ガウス関数fitting
    def func(x, a, mu, sigma, bg):
        return a*np.exp(-(x-mu)**2/(2*sigma**2))+bg

    """#旧コード
    #初期値
    param_ini = [500,0,0.1,0]
    fit_param = np.zeros((24,4))
    fit_result=np.zeros((3,24))
    for i in range(24):
        popt, pcov = curve_fit(func, e, D_I[:,i], p0=param_ini)
        #高さ popt[0]
        #中心 popt[1]
        #幅　popt[2]
        #background popt[3]
        #fit_result[0,i]=popt[0]#intensity
        #積分強度
        fit_param[i,:]=[popt[0],popt[1],popt[2],popt[3]]
        #検出器効率補正
        #fit_result[0,i]=popt[0]# height
        fit_result[0,i]=popt[0]*2*(2*math.log(2))**(1/2)*abs(popt[2])*(3.1415926535/(4*math.log(2)))**(1/2)#intensity
        fit_result[1,i]=popt[1]#energy transfer
        fit_result[2,i]=2*(2*math.log(2))**(1/2)*abs(popt[2])#FWHM
    """
    fit_param = np.zeros((24,4))
    fit_result=np.zeros((3,24))
    for i in range(24):
        ydata = D_I[:, i]
        xdata = e

        # --- データに基づいた初期値 ---
        a_init = np.max(ydata)
        mu_init = xdata[np.argmax(ydata)]
        sigma_init = 0.1
        bg_init = np.min(ydata)
        param_ini = [a_init, mu_init, sigma_init, bg_init]

        # --- フィッティング ---
        popt, pcov = curve_fit(func, xdata, ydata, p0=param_ini)

        # --- パラメータ保存 ---
        fit_param[i, :] = [popt[0], popt[1], popt[2], popt[3]]

        # --- 結果保存 ---
        # 積分強度（正規化因子付き）
        #fit_result[0, i] = popt[0]
        fit_result[0, i] = popt[0] * 2 * (2 * math.log(2))**0.5 * abs(popt[2]) * (math.pi / (4 * math.log(2)))**0.5
        fit_result[1, i] = popt[1]  # 中心
        fit_result[2, i] = 2 * (2 * math.log(2))**0.5 * abs(popt[2])  # FWHM

    # Efのtoleranceは保存する。
    # shared variables are stored in state
    state['ef_tol'] = np.max(fit_result[1,:]) - np.min(fit_result[1,:])
    state['ef_cen'] = np.mean(fit_result[1,:])

    """
    # デフォルトでcalibrationのFHWMが入力される
    if fgt_txt1.get()=='':
        if hw_nan.get()==0:
            fgt_txt1.insert(0,round(ef_tol+0.005,3))
    """

    with open(state['file_paths'][0], "r", encoding="utf-8") as f:
        line = f.readlines()
        chead = line[31]
        chead2 = chead.split()
        # powder / single-crystal mode is decided once and then reused by
        # every foreground/background branch below.
        is_single_crystal = "Pt." not in chead2
        # shared variables are stored in state
        # shared variables are stored in state
        state['sign'] = 1.0  # orientation is handled by the crystallographic display basis
        state['UBmatrix'] = None
        state['data_UBmatrix'] = None
        state['data_spice_to_pdf'] = None
        state['display_ex'] = state['display_ey'] = state['display_ez'] = None
        state['display_uv_angle'] = None
        state['display_v_hkl'] = None
        state['display_mode'] = None

        if not is_single_crystal:  # powder
            w_off = 0.0
            data_ref_c2 = None
            data_omega_ref = None
            data_c2_sign = +1.0
            # ry/rx are still read from the DAT file.  These values are not
            # used by the powder conversion, but define harmless zero offsets
            # so the common call signature remains valid.
            data_ref_ry = 0.0
            data_ref_rx = 0.0
            state['NU1'] = state['NV1'] = 1.0
            N_mcu = float(txt15.get())
            bgm = bg_type.get()

        else:  # single crystal
            # Lattice constants remain GUI parameters for display/metadata,
            # but Q->HKL now uses the SPICE UB matrix directly.
            la = float(txt1.get())
            lb = float(txt2.get())
            lc = float(txt3.get())
            lal = float(txt4.get())
            lbe = float(txt5.get())
            lga = float(txt6.get())
            N_mcu = float(txt15.get())

            # shared variables are stored in state
            state['u'] = np.array([float(txt9.get()), float(txt10.get()), float(txt11.get())], dtype=float)
            state['v'] = np.array([float(txt12.get()), float(txt13.get()), float(txt14.get())], dtype=float)

            ref_hkl = np.array([
                float(txt_ref_h.get()),
                float(txt_ref_k.get()),
                float(txt_ref_l.get()),
            ], dtype=float)
            ref_c2 = float(txt_ref_c2.get())
            ref_a2 = float(txt_ref_a2.get())
            ref_ry = float(txt_ref_ry.get())   # SPICE ry -> Mantid/PDF mu
            ref_rx = float(txt_ref_rx.get())   # SPICE rx -> Mantid/PDF nu
            ref_ei = float(txt_ref_ei.get())
            ref_ef = float(txt_ref_ef.get())

            # Reference Peak1 motor readings are the offsets for the
            # two tilt axes.
            #
            # SPICE ry -> Mantid/PDF mu
            # SPICE rx -> Mantid/PDF nu
            #
            #   mu = ry_point - ry_ref
            #   nu = rx_point - rx_ref
            #
            # Hence, if rx and ry remain at their Reference Peak1
            # values during the experiment, mu = nu = 0.
            data_ref_ry = float(ref_ry)
            data_ref_rx = float(ref_rx)

            # PDF/Mantid rotation order:
            #
            #     Q_lab
            #       = Ry(omega)
            #         @ Rz_SPICE(mu)
            #         @ Rx(nu)
            #         @ Q0
            #
            # where Rz_SPICE(mu) = Rz_PDF(-mu).
            #
            # SPICE ry corresponds to Mantid/PDF mu, and SPICE rx
            # corresponds to Mantid/PDF nu.  Reference Peak1 defines
            # their zero points in the canonical reciprocal-space frame.
            # The measured data therefore use
            #
            #     mu = ry - ry_ref
            #     nu = rx - rx_ref.

            bgm = bg_type.get()

            # SPICE UB from the first foreground dat file.
            # Keep the raw matrix for display / diagnostics.
            state['UBmatrix'] = _parse_spice_ub_from_dat(state['file_paths'][0])
            _show_ubmatrix(state['UBmatrix'])

            # ------------------------------------------------------------
            # Q-calculation UB
            #
            # The raw SPICE Cartesian axis convention is not assumed to be
            # identical to the PDF lab-axis convention.  Re-express the same
            # reciprocal metric in the canonical PDF frame:
            #
            #     U -> +z
            #     in-plane perpendicular -> +x
            #     plane normal -> +y
            #
            # No reciprocal lengths or crystallographic angles are changed.
            # ------------------------------------------------------------
            state['data_UBmatrix'], state['data_spice_to_pdf'] = _canonicalize_spice_ub_for_pdf(
                state['UBmatrix'],
                state['u'],
                state['v']
            )

            # Display-axis policy is evaluated in this canonical frame.
            (
                state['display_ex'],
                state['display_ey'],
                state['display_ez'],
                state['NU1'],
                state['NV1'],
                state['display_uv_angle'],
                display_used_angle,
                state['display_v_hkl'],
                state['display_mode'],
                display_coeff
            ) = _make_crystallographic_display_basis(
                state['data_UBmatrix'],
                state['u'],
                state['v']
            )

            # ------------------------------------------------------------
            # Absolute C2 calibration from the elastic reference reflection.
            #
            # Do not use the old q_angle+theta-90 C2 offset here.
            # Instead determine the physical omega of the reference directly
            # from Q_lab = R_y(omega) Q0.
            # ------------------------------------------------------------
            data_ref_c2 = float(ref_c2)

            data_omega_ref = _calculate_data_reference_omega(
                state['data_UBmatrix'],
                ref_hkl,
                data_ref_c2,
                ref_a2,
                ref_ei,
                ref_ef,
            )

            data_c2_sign = float(DATA_C2_TO_OMEGA_SIGN)

            # Keep a zero powder-style offset variable so legacy branches that
            # only inspect its existence do not fail.  It is NOT used for the
            # single-crystal Q transformation.
            w_off = 0.0

            print("SPICE UB matrix (raw):\n", state['UBmatrix'])
            print("Q-calculation UB matrix (PDF frame):\n", state['data_UBmatrix'])
            print("raw SPICE -> PDF transform T:\n", state['data_spice_to_pdf'])
            print(f"reference C2 = {data_ref_c2:.6f} deg")
            print(f"reference ry (mu zero) = {data_ref_ry:.6f} deg")
            print(f"reference rx (nu zero) = {data_ref_rx:.6f} deg")
            print(f"reference omega = {data_omega_ref:.6f} deg")
            print(f"C2 -> omega sign = {data_c2_sign:+.0f}")
            print(f"entered physical U-V angle = {state['display_uv_angle']:.6f} deg")

            if state['display_mode'] == "orthogonal-crystallographic":
                print(
                    "display mode: crystallographic orthogonal axis found; "
                    f"Y uses HKL {np.array2string(state['display_v_hkl'], precision=6)} "
                    f"(used angle = {display_used_angle:.6f} deg)"
                )
                if display_coeff is not None and display_coeff != (0, 1):
                    print(
                        f"Y = {display_coeff[0]}*U "
                        f"+ {display_coeff[1]}*V"
                    )
            else:
                print(
                    "display mode: non-orthogonal crystallographic U,V "
                    "rendered on perpendicular screen axes "
                    "(constant-|Q| contours become elliptical)."
                )
                print(
                    "monoclinic/general oblique mode: entered V is "
                    "preserved exactly as ",
                    np.array2string(state['display_v_hkl'], precision=6)
                )

    # プログレスバー内の変数にアクセスできるように一番外枠でglobal定義
    # shared variables are stored in state
    var1 = 0 # 変数の初期値
    # 最初にバックグラウンドを差し引くか決定。(処理スピードを優先)
    if sbListbox.size() == 0:# background fileが無い場合
        # background処理を行った後に、foregroundのみの処理を行うとauto rangeが効かない可能性がある。
        # プログレスバーの表示
        state['pb']["maximum"] = len(state['file_paths']) # プログレスバーの最大値
        state['pb']["value"] = 0
        state['pb'].update()

        for i in range(len(state['file_paths'])):
            # データ形式が異なっているファイル(例えば、c2 scanとenergy scanが混じっていても)でも読み取れるように毎回読む仕様に変更する。
            with open(state['file_paths'][i],"r", encoding="utf-8") as f:
                line = f.readlines()
                head = line[31]
                head2 = head.split()
                if "Pt." in head2:
                    pass
                else:
                    head = line[32]
                    head2 = head.split()

                #パラメータは何番目ですか？
                #global No_Pt,No_c2,No_a2,No_mcu,No_e,No_ei,No_D01,No_D02,No_D03,No_D04,No_D05,No_D06,No_D07,No_D08,No_D09,No_D10,No_D11,No_D12,No_D13,No_D14,No_D15,No_D16,No_D17,No_D18,No_D19,No_D20,No_D21,No_D22,No_D23,No_D24
                No_Pt=head2.index('Pt.')
                No_c2=head2.index('c2')
                No_a2=head2.index('a2')
                No_ry=head2.index('ry')
                No_rx=head2.index('rx')
                No_timeact=head2.index('time-act')
                #mcuがない場合は読み込まない。もちろんデータも表示されないけどね
                if head.find('mcu')!=-1:
                    No_mcu=head2.index('mcu')
                else :
                    pass

                #No_mcu=data2.index('mcu')
                No_e=head2.index('e')
                No_ei=head2.index('ei')
                No_D01=head2.index('D01')
                No_D24=head2.index('D24')

            #リストにあるファイルを順に読み込んでいく
            with open(state['file_paths'][i],"r", encoding="utf-8") as f:
                #選択ファイルの数値を全て読み込む
                rdb = np.loadtxt(state['file_paths'][i], comments='#')
                # データが１次元配列の際に２次元配列に格納
                if len(rdb.shape) == 1:
                    rdb = np.expand_dims(rdb, axis=0)

                t_a = rdb[:,No_timeact-1]
                # time-actが0のデータを検索
                Ind_t0 = np.where(t_a == 0)
                # time-actが0のデータを削除
                rdb = np.delete(rdb, Ind_t0, axis=0)

                pt = rdb[:,No_Pt-1]
                c2 = rdb[:,No_c2-1]
                a2 = rdb[:,No_a2-1]
                ry = rdb[:,No_ry-1]   # SPICE ry -> Mantid/PDF mu
                rx = rdb[:,No_rx-1]   # SPICE rx -> Mantid/PDF nu
                #mcuがない場合は読み込まない。強制的にmcuが0となり、IntensityはNan値となる。
                if head.find('mcu')!=-1:
                    mcu = rdb[:,No_mcu-1]
                else :
                    mcu = np.zeros((len(pt)))
                e = rdb[:,No_e-1]
                ei = rdb[:,No_ei-1]
                D = rdb[:,No_D01-1:No_D24]

            #kiとkfの定義
            ki = np.zeros((2, len(pt)))
            kf = np.zeros((2, len(pt)*24))
            #ki2 = np.zeros((2, len(pt)*24))
            #Qのベクトルとスカラーの定義、あとここに強度の情報を加える。
            # shared variables are stored in state
            state['Qvector']=np.zeros((6, len(pt)*24))# single crystal: 0 alpha*|qU| [A^-1], 1 beta*|qV| [A^-1], 2 |Q|; powder: 0 Qx, 1 Qy; 3 dE, 4 intensity, 5 error
            #検出器の角度
            d_angle=np.linspace(0, 46, 24)
            A2 = np.zeros((1, 24))

            # C2 is the measured instrument encoder value.
            C2=np.asarray(c2, dtype=float)

            #　HODACAで測定した点を計算してくれる
            #pythonでは行列の数えやfor文は0から始まるので注意すること
            for n in range(len(pt)):# nは各ファイルのデータの個数に対応
                if is_single_crystal and n == 0:
                    print(
                        "tilt check:",
                        "ry_data =", float(ry[n]),
                        "ry_ref =", float(data_ref_ry),
                        "mu_eff =", float(ry[n]) - float(data_ref_ry),
                        "rx_data =", float(rx[n]),
                        "rx_ref =", float(data_ref_rx),
                        "nu_eff =", float(rx[n]) - float(data_ref_rx),
                    )
                #ki_x[0,n] = math.sqrt(ei[n]/2.072)*math.cos(math.radians(-c2[n]))
                #ki_y[0,n] = -math.sqrt(ei[n]/2.072)*math.sin(math.radians(-c2[n]))
                ki[0:2,n] = [math.sqrt(ei[n]/2.072)*math.cos(math.radians(-C2[n])),-math.sqrt(ei[n]/2.072)*math.sin(math.radians(-C2[n]))]
                #A2の絶対値変換
                update_phi()
                A2 = d_angle + state['phi'] + a2[n] 
                for m in range(24):# mは検出器の番号に対応
                    #ki2[:,24*n+m] = ki[:,n]
                    # 各検出器の補正として-fit_result[1,m]
                    kf[0:2,24*n+m] = [math.sqrt((3.635+fit_result[1,m])/2.072)*math.cos(math.radians(A2[m]-C2[n])),-math.sqrt((3.635+fit_result[1,m])/2.072)*math.sin(math.radians(A2[m]-C2[n]))]
                    #kf[0:2,24*n+m] = [math.sqrt(3.635/2.072)*math.cos(math.radians(A2[m]-C2[n])),-math.sqrt(3.635/2.072)*math.sin(math.radians(A2[m]-C2[n]))]
                    state['Qvector'][0:2,24*n+m] = _angles_to_hkl_and_uv(
                                    ei[n],
                                    3.635+fit_result[1,m],
                                    C2[n],
                                    A2[m],
                                    is_single_crystal,
                                    state['data_UBmatrix'] if is_single_crystal else None,
                                    state['u'] if is_single_crystal else None,
                                    state['display_v_hkl'] if is_single_crystal else None,
                                data_ref_c2 if is_single_crystal else None,
                                data_omega_ref if is_single_crystal else None,
                                data_c2_sign if is_single_crystal else +1.0,
                                    ry_deg=ry[n],
                                    rx_deg=rx[n],
                                    ref_ry=data_ref_ry,
                                    ref_rx=data_ref_rx,
                                    spice_to_pdf_transform=state['data_spice_to_pdf']
                                )[0]                   
                    #powder用にqも入れておく
                    state['Qvector'][2,24*n+m] = math.sqrt((ki[0,n] - kf[0,24*n+m])**2+(ki[1,n] - kf[1,24*n+m])**2)
                    # エネルギートランスファーの情報を入れる。各検出器の補正として-fit_result[1,m]
                    state['Qvector'][3,24*n+m] = e[n]-fit_result[1,m]
                    # 強度の情報を入れる。ここでバナジウムとmcuの補正をする。12番を基準とする
                    #lorentz_factor = 1/math.sin(math.radians(A2[m]))
                    lorentz_factor = 1
                    state['Qvector'][4,24*n+m] = D[n,m]/fit_result[0,m]*fit_result[0,11]*N_mcu/mcu[n]*lorentz_factor
                    state['Qvector'][5,24*n+m] = math.sqrt(D[n,m])/fit_result[0,m]*fit_result[0,11]*N_mcu/mcu[n]*lorentz_factor

            # 全てのデータを格納するボックスを立ち上げる。Qvectorのデータをどんどん連結していく。最初のファイルだけdataboxをQvectorにする。

            if i == 0:
                Databox=state['Qvector']
            #databox.extend(Qvector)
            if i > 0:
                Databox=(np.concatenate([Databox, state['Qvector']], 1))

            # プログレスバー (確定的)。エネルギー毎にステータスが進む
            var1=var1+1
            #pb.configure(value = var1)
            state['pb']["value"] = var1
            state['pb'].update()

    else: #バックグラウンドファイルのリストボックスにファイルがあるとき
        if bgm==0:# detectro by detector
            # detector by detectorFGとBGの許容エネルギー差を入力。
            #if bgt_txt1.get()=='':
            #    bgt_txt1.insert(0,0.01)#とりあえず±0.01meV以内のバックグラウンドを選ぶ。2025/03/26　自動入力されることがそもそもおかしい。
            # この段階でバックグラウンドのすべてのデータを読み込んでしまう。
            # プログレスバーの表示
            state['pb']["maximum"] = len(state['file_paths'])+len(state['sbfile_paths']) # プログレスバーの最大値
            state['pb']["value"] = 0
            state['pb'].update()

            # detector by detectorにおけるA2,C2 tolerance
            if sbtype1.get()==0:# チェックボックスが平均化の場合
                # detector by detectorFGとBGの許容エネルギー差を入力。
                if bgt_txt1.get()=='':
                    dE = 0.01
                else:
                    dE = float(bgt_txt1.get())
                tol_A2 = float(bgt_txt4.get())
                tol_C2 = float(bgt_txt5.get())
                for k in range(len(state['sbfile_paths'])):
                    # データ形式が異なっているファイル(例えば、c2 scanとenergy scanが混じっていても)でも読み取れるように毎回読む仕様に変更する。
                    with open(state['sbfile_paths'][k],"r", encoding="utf-8") as f:
                        line = f.readlines()
                        sbhead = line[31]
                        sbhead2 = sbhead.split()
                        if "Pt." in sbhead2:
                            pass
                        else:
                            sbhead = line[32]
                            sbhead2 = sbhead.split()

                        #パラメータは何番目ですか？
                        #global SbNo_Pt,SbNo_c2,SbNo_a2,SbNo_mcu,SbNo_e,SbNo_ei,SbNo_D01,SbNo_D02,SbNo_D03,SbNo_D04,SbNo_D05,SbNo_D06,SbNo_D07,SbNo_D08,SbNo_D09,SbNo_D10,SbNo_D11,SbNo_D12,SbNo_D13,SbNo_D14,SbNo_D15,SbNo_D16,SbNo_D17,SbNo_D18,SbNo_D19,SbNo_D20,SbNo_D21,SbNo_D22,SbNo_D23,SbNo_D24
                        sbNo_Pt=sbhead2.index('Pt.')
                        sbNo_c2=sbhead2.index('c2')
                        sbNo_a2=sbhead2.index('a2')
                        sbNo_ry=sbhead2.index('ry')
                        sbNo_rx=sbhead2.index('rx')
                        sbNo_timeact=sbhead2.index('time-act')
                        #mcuがない場合は読み込まない。もちろんデータも表示されないけどね
                        if sbhead.find('mcu')!=-1:
                            sbNo_mcu=sbhead2.index('mcu')
                        else :
                            pass

                        #SbNo_mcu=data2.index('mcu')
                        sbNo_e=sbhead2.index('e')
                        sbNo_ei=sbhead2.index('ei')
                        sbNo_D01=sbhead2.index('D01')
                        sbNo_D24=sbhead2.index('D24')

                    #リストにあるファイルを順に読み込んでいく
                    with open(state['sbfile_paths'][k],"r", encoding="utf-8") as f:
                        #選択ファイルの数値を全て読み込む
                        sbrdb = np.loadtxt(state['sbfile_paths'][k], comments='#')

                        # データが１次元配列の際に２次元配列に格納
                        if len(sbrdb.shape) == 1:
                            sbrdb = np.expand_dims(sbrdb, axis=0)

                        sbt_a = sbrdb[:,sbNo_timeact-1]
                        # time-actが0のデータを検索
                        sbInd_t0 = np.where(sbt_a == 0)
                        # time-actが0のデータを削除
                        sbrdb = np.delete(sbrdb, sbInd_t0, axis=0)
                        sbpt = sbrdb[:,sbNo_Pt-1].reshape(-1, 1)
                        sbe = sbrdb[:,sbNo_e-1].reshape(-1, 1)
                        sbei = sbrdb[:,sbNo_ei-1].reshape(-1, 1)
                        sbc2 = sbrdb[:,sbNo_c2-1].reshape(-1, 1)
                        sba2 = sbrdb[:,sbNo_a2-1].reshape(-1, 1)
                        sbry = sbrdb[:,sbNo_ry-1].reshape(-1, 1)   # SPICE ry -> Mantid/PDF mu
                        sbrx = sbrdb[:,sbNo_rx-1].reshape(-1, 1)   # SPICE rx -> Mantid/PDF nu
                        #mcuがない場合は読み込まない。強制的にmcuが0となり、IntensityはNan値となる。
                        if sbhead.find('mcu')!=-1:
                            sbmcu = sbrdb[:,sbNo_mcu-1].reshape(-1, 1)
                        else :
                            sbmcu = np.zeros((len(sbpt))).reshape(-1, 1)
                        sbD = sbrdb[:,sbNo_D01-1:sbNo_D24]

                    # プログレスバー (確定的)。エネルギー毎にステータスが進む
                    var1=var1+1
                    state['pb'].configure(value = var1)
                    state['pb'].update()
                    #バックグラウンドのデータを積算する。

                    if k == 0:
                        # 縦方向に連結
                        sb_Databox0 = np.hstack((sbpt,sbe,sbei,sbc2,sba2,sbD,sbmcu))
                    #databox.extend(Qvector)
                    if k > 0:
                        # 横方向に連結
                        sb_Databox0=np.vstack((sb_Databox0,np.hstack((sbpt,sbe,sbei,sbc2,sba2,sbD,sbmcu))))
                #sb_Databox=sb_Databox.T

                for i in range(len(state['file_paths'])):
                    # データ形式が異なっているファイル(例えば、c2 scanとenergy scanが混じっていても)でも読み取れるように毎回読む仕様に変更する。
                    with open(state['file_paths'][i],"r", encoding="utf-8") as f:
                        line = f.readlines()
                        head = line[31]
                        head2 = head.split()
                        if "Pt." in head2:
                            pass
                        else:
                            head = line[32]
                            head2 = head.split()

                        #パラメータは何番目ですか？
                        #global No_Pt,No_c2,No_a2,No_mcu,No_e,No_ei,No_D01,No_D02,No_D03,No_D04,No_D05,No_D06,No_D07,No_D08,No_D09,No_D10,No_D11,No_D12,No_D13,No_D14,No_D15,No_D16,No_D17,No_D18,No_D19,No_D20,No_D21,No_D22,No_D23,No_D24
                        No_Pt=head2.index('Pt.')
                        No_c2=head2.index('c2')
                        No_a2=head2.index('a2')
                        No_ry=head2.index('ry')
                        No_rx=head2.index('rx')
                        No_timeact=head2.index('time-act')
                        #mcuがない場合は読み込まない。もちろんデータも表示されないけどね
                        if head.find('mcu')!=-1:
                            No_mcu=head2.index('mcu')
                        else :
                            pass

                        #No_mcu=data2.index('mcu')
                        No_e=head2.index('e')
                        No_ei=head2.index('ei')
                        No_D01=head2.index('D01')
                        No_D24=head2.index('D24')

                    #リストにあるファイルを順に読み込んでいく
                    with open(state['file_paths'][i],"r", encoding="utf-8") as f:
                        #選択ファイルの数値を全て読み込む
                        rdb = np.loadtxt(state['file_paths'][i], comments='#')

                        # データが１次元配列の際に２次元配列に格納
                        if len(rdb.shape) == 1:
                            rdb = np.expand_dims(rdb, axis=0)

                        t_a = rdb[:,No_timeact-1]
                        # time-actが0のデータを検索
                        Ind_t0 = np.where(t_a == 0)
                        # time-actが0のデータを削除
                        rdb = np.delete(rdb, Ind_t0, axis=0)

                        pt = rdb[:,No_Pt-1]
                        c2 = rdb[:,No_c2-1]
                        a2 = rdb[:,No_a2-1]
                        ry = rdb[:,No_ry-1]   # SPICE ry -> Mantid/PDF mu
                        rx = rdb[:,No_rx-1]   # SPICE rx -> Mantid/PDF nu
                        print(rx,ry)
                        #mcuがない場合は読み込まない。強制的にmcuが0となり、IntensityはNan値となる。
                        if head.find('mcu')!=-1:
                            mcu = rdb[:,No_mcu-1]
                        else :
                            mcu = np.zeros((len(pt)))
                        e = rdb[:,No_e-1]
                        ei = rdb[:,No_ei-1]
                        D = rdb[:,No_D01-1:No_D24]

                    #kiとkfの定義
                    ki = np.zeros((2, len(pt)))
                    kf = np.zeros((2, len(pt)*24))
                    #ki2 = np.zeros((2, len(pt)*24))
                    #Qのベクトルとスカラーの定義、あとここに強度の情報を加える。
                    state['Qvector']=np.zeros((6, len(pt)*24))# single crystal: 0 alpha*|qU| [A^-1], 1 beta*|qV| [A^-1], 2 |Q|; powder: 0 Qx, 1 Qy; 3 dE, 4 intensity, 5 error
                    # shared variables are stored in state
                    state['sb_Qvector']=np.zeros((6, len(pt)*24))# backgroundファイル用
                    #検出器の角度
                    d_angle=np.linspace(0, 46, 24)
                    A2 = np.zeros((1, 24))

                    # C2 is the measured instrument encoder value.
                    C2=np.asarray(c2, dtype=float)

                    #　HODACAで測定した点を計算してくれる
                    #pythonでは行列の数えやfor文は0から始まるので注意すること
                    for n in range(len(pt)):# nは各ファイルのデータの個数に対応

                        #ki_x[0,n] = math.sqrt(ei[n]/2.072)*math.cos(math.radians(-c2[n]))
                        #ki_y[0,n] = -math.sqrt(ei[n]/2.072)*math.sin(math.radians(-c2[n]))
                        ki[0:2,n] = [math.sqrt(ei[n]/2.072)*math.cos(math.radians(-C2[n])),-math.sqrt(ei[n]/2.072)*math.sin(math.radians(-C2[n]))]
                        #A2の絶対値変換
                        update_phi()
                        A2 = d_angle + state['phi'] + a2[n] 

                        # ここで対応するバックグラウンドデータを差し引く。
                        # ((sbpt,sbe,sbei,sbc2,sba2,sbD01,sbD02,sbD03,sbD04,sbD05,sbD06,sbD07,sbD08,sbD09,sbD10,sbD11,sbD12,sbD13,sbD14,sbD15,sbD16,sbD17,sbD18,sbD19,sbD20,sbD21,sbD22,sbD23,sbD24))

                        # まずはエネルギートランスファーが一致する部分を抜き出す。補正をする前同士作業なのでOK。
                        # エネルギースキャンステップに依存するがとりあえず一般的なモータートレランスの範囲内にあるエネルギー値のものをサーチする。
                        # 補正する前のエネルギー値なので、そこまでずれない。
                        ind_E = (list(zip(*np.where(((e[n]-dE) < sb_Databox0[:,1]) & (sb_Databox0[:,1] < (e[n]+dE))))))
                        # リスト型に出力
                        Ind_E = list(np.ravel(ind_E))

                        if len(Ind_E) > 0:# Ind_Eが空でないとき
                            sb_data_e=sb_Databox0[Ind_E,:]
                            # まずA2が最も近いデータを選び、その中からC2が最も近いデータを選ぶ。
                            sba2 = sb_data_e[:,4]
                            sbc2 = sb_data_e[:,3]

                            # 新しいコードではtol_A2とtol_C2を設定できる。指定がない場合は±180degの範囲から選択する。                       
                            ind_tol_A2C2 = (list(zip(*np.where( ((a2[n] - tol_A2) < sba2) & (sba2 < (a2[n] + tol_A2)) & ((c2[n] - tol_C2) < sbc2) & (sbc2 < (c2[n] + tol_C2)) ))))
                            index_BG = list(np.ravel(ind_tol_A2C2))

                            for m in range(24):# mは検出器の番号に対応
                                #ki2[:,24*n+m] = ki[:,n]
                                # 各検出器の補正として-fit_result[1,m]
                                kf[0:2,24*n+m] = [math.sqrt((3.635+fit_result[1,m])/2.072)*math.cos(math.radians(A2[m]-C2[n])),-math.sqrt((3.635+fit_result[1,m])/2.072)*math.sin(math.radians(A2[m]-C2[n]))]
                                #kf[0:2,24*n+m] = [math.sqrt(3.635/2.072)*math.cos(math.radians(A2[m]-C2[n])),-math.sqrt(3.635/2.072)*math.sin(math.radians(A2[m]-C2[n]))]
                                state['Qvector'][0:2,24*n+m] = _angles_to_hkl_and_uv(
                                    ei[n],
                                    3.635+fit_result[1,m],
                                    C2[n],
                                    A2[m],
                                    is_single_crystal,
                                    state['data_UBmatrix'] if is_single_crystal else None,
                                    state['u'] if is_single_crystal else None,
                                    state['display_v_hkl'] if is_single_crystal else None,
                                data_ref_c2 if is_single_crystal else None,
                                data_omega_ref if is_single_crystal else None,
                                data_c2_sign if is_single_crystal else +1.0,
                                    ry_deg=ry[n],
                                    rx_deg=rx[n],
                                    ref_ry=data_ref_ry,
                                    ref_rx=data_ref_rx,
                                    spice_to_pdf_transform=state['data_spice_to_pdf']
                                )[0]
                                state['sb_Qvector'][0:2,24*n+m] = _angles_to_hkl_and_uv(
                                    ei[n],
                                    3.635+fit_result[1,m],
                                    C2[n],
                                    A2[m],
                                    is_single_crystal,
                                    state['data_UBmatrix'] if is_single_crystal else None,
                                    state['u'] if is_single_crystal else None,
                                    state['display_v_hkl'] if is_single_crystal else None,
                                data_ref_c2 if is_single_crystal else None,
                                data_omega_ref if is_single_crystal else None,
                                data_c2_sign if is_single_crystal else +1.0,
                                    ry_deg=ry[n],
                                    rx_deg=rx[n],
                                    ref_ry=data_ref_ry,
                                    ref_rx=data_ref_rx,
                                    spice_to_pdf_transform=state['data_spice_to_pdf']
                                )[0]
                                #powder用にqも入れておく
                                state['Qvector'][2,24*n+m] = math.sqrt((ki[0,n] - kf[0,24*n+m])**2+(ki[1,n] - kf[1,24*n+m])**2)
                                state['sb_Qvector'][2,24*n+m] = math.sqrt((ki[0,n] - kf[0,24*n+m])**2+(ki[1,n] - kf[1,24*n+m])**2)
                                # エネルギートランスファーの情報を入れる。各検出器の補正として-fit_result[1,m]
                                state['Qvector'][3,24*n+m] = e[n]-fit_result[1,m]
                                state['sb_Qvector'][3,24*n+m] = e[n]-fit_result[1,m]
                                # 強度の情報を入れる。ここでバナジウムとmcuの補正をする。12番を基準とする。
                                lorentz_factor = 1
                                state['Qvector'][4,24*n+m] = D[n,m]/fit_result[0,m]*fit_result[0,11]*N_mcu/mcu[n]*lorentz_factor
                                state['sb_Qvector'][4,24*n+m] = np.sum(sb_data_e[index_BG,5+m])/fit_result[0,m]*fit_result[0,11]*N_mcu/np.sum(sb_data_e[index_BG,29])*lorentz_factor
                                state['Qvector'][5,24*n+m] = (math.sqrt(D[n,m])/fit_result[0,m]*fit_result[0,11]*N_mcu/mcu[n])*lorentz_factor
                                state['sb_Qvector'][5,24*n+m] = math.sqrt(np.sum(sb_data_e[index_BG,5+m]))/fit_result[0,m]*fit_result[0,11]*N_mcu/np.sum(sb_data_e[index_BG,29])*lorentz_factor

                        else:# 対応するエネルギーが無かった場合
                            if sbtype2.get()==0:# Nanが選択されていない
                                for m in range(24):# mは検出器の番号に対応
                                    #ki2[:,24*n+m] = ki[:,n]
                                    # 各検出器の補正として-fit_result[1,m]
                                    kf[0:2,24*n+m] = [math.sqrt((3.635+fit_result[1,m])/2.072)*math.cos(math.radians(A2[m]-C2[n])),-math.sqrt((3.635+fit_result[1,m])/2.072)*math.sin(math.radians(A2[m]-C2[n]))]
                                    #kf[0:2,24*n+m] = [math.sqrt(3.635/2.072)*math.cos(math.radians(A2[m]-C2[n])),-math.sqrt(3.635/2.072)*math.sin(math.radians(A2[m]-C2[n]))]
                                    state['Qvector'][0:2,24*n+m] = _angles_to_hkl_and_uv(
                                    ei[n],
                                    3.635+fit_result[1,m],
                                    C2[n],
                                    A2[m],
                                    is_single_crystal,
                                    state['data_UBmatrix'] if is_single_crystal else None,
                                    state['u'] if is_single_crystal else None,
                                    state['display_v_hkl'] if is_single_crystal else None,
                                data_ref_c2 if is_single_crystal else None,
                                data_omega_ref if is_single_crystal else None,
                                data_c2_sign if is_single_crystal else +1.0,
                                    ry_deg=ry[n],
                                    rx_deg=rx[n],
                                    ref_ry=data_ref_ry,
                                    ref_rx=data_ref_rx,
                                    spice_to_pdf_transform=state['data_spice_to_pdf']
                                )[0]
                                    state['sb_Qvector'][0:2,24*n+m] = _angles_to_hkl_and_uv(
                                    ei[n],
                                    3.635+fit_result[1,m],
                                    C2[n],
                                    A2[m],
                                    is_single_crystal,
                                    state['data_UBmatrix'] if is_single_crystal else None,
                                    state['u'] if is_single_crystal else None,
                                    state['display_v_hkl'] if is_single_crystal else None,
                                data_ref_c2 if is_single_crystal else None,
                                data_omega_ref if is_single_crystal else None,
                                data_c2_sign if is_single_crystal else +1.0,
                                    ry_deg=ry[n],
                                    rx_deg=rx[n],
                                    ref_ry=data_ref_ry,
                                    ref_rx=data_ref_rx,
                                    spice_to_pdf_transform=state['data_spice_to_pdf']
                                )[0]
                                    #powder用にqも入れておく
                                    state['Qvector'][2,24*n+m] = math.sqrt((ki[0,n] - kf[0,24*n+m])**2+(ki[1,n] - kf[1,24*n+m])**2)
                                    state['sb_Qvector'][2,24*n+m] = math.sqrt((ki[0,n] - kf[0,24*n+m])**2+(ki[1,n] - kf[1,24*n+m])**2)
                                    # エネルギートランスファーの情報を入れる。各検出器の補正として-fit_result[1,m]
                                    state['Qvector'][3,24*n+m] = e[n]-fit_result[1,m]
                                    state['sb_Qvector'][3,24*n+m] = e[n]-fit_result[1,m]
                                    lorentz_factor = 1
                                    state['Qvector'][4,24*n+m] = D[n,m]/fit_result[0,m]*fit_result[0,11]*N_mcu/mcu[n]*lorentz_factor
                                    state['sb_Qvector'][4,24*n+m] = np.nan*lorentz_factor
                                    state['Qvector'][5,24*n+m] = math.sqrt(D[n,m])/fit_result[0,m]*fit_result[0,11]*N_mcu/mcu[n]*lorentz_factor
                                    state['sb_Qvector'][5,24*n+m] = np.nan*lorentz_factor
                            else:# Nanが選択されている
                                pass

                    # 全てのデータを格納するボックスを立ち上げる。Qvectorのデータをどんどん連結していく。最初のファイルだけdataboxをQvectorにする。
                    if i == 0:
                        Databox=state['Qvector']
                        sb_Databox=state['sb_Qvector']
                    #databox.extend(Qvector)
                    if i > 0:
                        Databox=(np.concatenate([Databox, state['Qvector']], 1))
                        sb_Databox=(np.concatenate([sb_Databox, state['sb_Qvector']], 1))

                    # プログレスバー (確定的)。エネルギー毎にステータスが進む
                    var1=var1+1
                    state['pb']["value"] = var1
                    state['pb'].update() 

            elif sbtype1.get()==1:# チェックボックスが最隣接選択の場合。デフォルトはこっち。
                # detector by detectorFGとBGの許容エネルギー差を入力。
                if bgt_txt1.get()=='':
                    dE = 0.01
                else:
                    dE = float(bgt_txt1.get())
                for k in range(len(state['sbfile_paths'])):
                    # データ形式が異なっているファイル(例えば、c2 scanとenergy scanが混じっていても)でも読み取れるように毎回読む仕様に変更する。
                    with open(state['sbfile_paths'][k],"r", encoding="utf-8") as f:
                        line = f.readlines()
                        sbhead = line[31]
                        sbhead2 = sbhead.split()
                        if "Pt." in sbhead2:
                            pass
                        else:
                            sbhead = line[32]
                            sbhead2 = sbhead.split()

                        #パラメータは何番目ですか？
                        #global SbNo_Pt,SbNo_c2,SbNo_a2,SbNo_mcu,SbNo_e,SbNo_ei,SbNo_D01,SbNo_D02,SbNo_D03,SbNo_D04,SbNo_D05,SbNo_D06,SbNo_D07,SbNo_D08,SbNo_D09,SbNo_D10,SbNo_D11,SbNo_D12,SbNo_D13,SbNo_D14,SbNo_D15,SbNo_D16,SbNo_D17,SbNo_D18,SbNo_D19,SbNo_D20,SbNo_D21,SbNo_D22,SbNo_D23,SbNo_D24
                        sbNo_Pt=sbhead2.index('Pt.')
                        sbNo_c2=sbhead2.index('c2')
                        sbNo_a2=sbhead2.index('a2')
                        sbNo_ry=sbhead2.index('ry')
                        sbNo_rx=sbhead2.index('rx')
                        sbNo_timeact=sbhead2.index('time-act')
                        #mcuがない場合は読み込まない。もちろんデータも表示されないけどね
                        if sbhead.find('mcu')!=-1:
                            sbNo_mcu=sbhead2.index('mcu')
                        else :
                            pass

                        #SbNo_mcu=data2.index('mcu')
                        sbNo_e=sbhead2.index('e')
                        sbNo_ei=sbhead2.index('ei')
                        sbNo_D01=sbhead2.index('D01')
                        sbNo_D24=sbhead2.index('D24')

                    #リストにあるファイルを順に読み込んでいく
                    with open(state['sbfile_paths'][k],"r", encoding="utf-8") as f:
                        #選択ファイルの数値を全て読み込む
                        sbrdb = np.loadtxt(state['sbfile_paths'][k], comments='#')

                        # データが１次元配列の際に２次元配列に格納
                        if len(sbrdb.shape) == 1:
                            sbrdb = np.expand_dims(sbrdb, axis=0)

                        sbt_a = sbrdb[:,sbNo_timeact-1].reshape(-1, 1)
                        # time-actが0のデータを検索
                        sbInd_t0 = np.where(sbt_a == 0)
                        # time-actが0のデータを削除
                        sbrdb = np.delete(sbrdb, sbInd_t0, axis=0)
                        sbpt = sbrdb[:,sbNo_Pt-1].reshape(-1, 1)
                        sbe = sbrdb[:,sbNo_e-1].reshape(-1, 1)
                        sbei = sbrdb[:,sbNo_ei-1].reshape(-1, 1)
                        sbc2 = sbrdb[:,sbNo_c2-1].reshape(-1, 1)
                        sba2 = sbrdb[:,sbNo_a2-1].reshape(-1, 1)
                        sbry = sbrdb[:,sbNo_ry-1].reshape(-1, 1)   # SPICE ry -> Mantid/PDF mu
                        sbrx = sbrdb[:,sbNo_rx-1].reshape(-1, 1)   # SPICE rx -> Mantid/PDF nu
                        #mcuがない場合は読み込まない。強制的にmcuが0となり、IntensityはNan値となる。
                        if sbhead.find('mcu')!=-1:
                            sbmcu = sbrdb[:,sbNo_mcu-1].reshape(-1, 1)
                        else :
                            sbmcu = np.zeros((len(sbpt))).reshape(-1, 1)
                        sbD = sbrdb[:,sbNo_D01-1:sbNo_D24]

                    # プログレスバー (確定的)。エネルギー毎にステータスが進む
                    var1=var1+1
                    state['pb'].configure(value = var1)
                    state['pb'].update()
                    #バックグラウンドのデータを積算する。

                    if k == 0:
                        # 縦方向に連結
                        sb_Databox0 = np.hstack((sbpt,sbe,sbei,sbc2,sba2,sbD,sbmcu))
                    #databox.extend(Qvector)
                    if k > 0:
                        # 横方向に連結
                        sb_Databox0=np.vstack((sb_Databox0,np.hstack((sbpt,sbe,sbei,sbc2,sba2,sbD,sbmcu))))
                for i in range(len(state['file_paths'])):
                    # データ形式が異なっているファイル(例えば、c2 scanとenergy scanが混じっていても)でも読み取れるように毎回読む仕様に変更する。
                    with open(state['file_paths'][i],"r", encoding="utf-8") as f:
                        line = f.readlines()
                        head = line[31]
                        head2 = head.split()
                        if "Pt." in head2:
                            pass
                        else:
                            head = line[32]
                            head2 = head.split()

                        #パラメータは何番目ですか？
                        #global No_Pt,No_c2,No_a2,No_mcu,No_e,No_ei,No_D01,No_D02,No_D03,No_D04,No_D05,No_D06,No_D07,No_D08,No_D09,No_D10,No_D11,No_D12,No_D13,No_D14,No_D15,No_D16,No_D17,No_D18,No_D19,No_D20,No_D21,No_D22,No_D23,No_D24
                        No_Pt=head2.index('Pt.')
                        No_c2=head2.index('c2')
                        No_a2=head2.index('a2')
                        No_ry=head2.index('ry')
                        No_rx=head2.index('rx')
                        No_timeact=head2.index('time-act')
                        #mcuがない場合は読み込まない。もちろんデータも表示されないけどね
                        if head.find('mcu')!=-1:
                            No_mcu=head2.index('mcu')
                        else :
                            pass

                        #No_mcu=data2.index('mcu')
                        No_e=head2.index('e')
                        No_ei=head2.index('ei')
                        No_D01=head2.index('D01')
                        No_D24=head2.index('D24')

                    #リストにあるファイルを順に読み込んでいく
                    with open(state['file_paths'][i],"r", encoding="utf-8") as f:
                        #選択ファイルの数値を全て読み込む
                        rdb = np.loadtxt(state['file_paths'][i], comments='#')

                        # データが１次元配列の際に２次元配列に格納
                        if len(rdb.shape) == 1:
                            rdb = np.expand_dims(rdb, axis=0)

                        t_a = rdb[:,No_timeact-1]
                        # time-actが0のデータを検索
                        Ind_t0 = np.where(t_a == 0)
                        # time-actが0のデータを削除
                        rdb = np.delete(rdb, Ind_t0, axis=0)

                        pt = rdb[:,No_Pt-1]
                        c2 = rdb[:,No_c2-1]
                        a2 = rdb[:,No_a2-1]
                        ry = rdb[:,No_ry-1]   # SPICE ry -> Mantid/PDF mu
                        rx = rdb[:,No_rx-1]   # SPICE rx -> Mantid/PDF nu
                        #mcuがない場合は読み込まない。強制的にmcuが0となり、IntensityはNan値となる。
                        if head.find('mcu')!=-1:
                            mcu = rdb[:,No_mcu-1]
                        else :
                            mcu = np.zeros((len(pt)))
                        e = rdb[:,No_e-1]
                        ei = rdb[:,No_ei-1]
                        D = rdb[:,No_D01-1:No_D24]

                    #kiとkfの定義
                    ki = np.zeros((2, len(pt)))
                    kf = np.zeros((2, len(pt)*24))
                    #ki2 = np.zeros((2, len(pt)*24))
                    #Qのベクトルとスカラーの定義、あとここに強度の情報を加える。
                    state['Qvector']=np.zeros((6, len(pt)*24))# single crystal: 0 alpha*|qU| [A^-1], 1 beta*|qV| [A^-1], 2 |Q|; powder: 0 Qx, 1 Qy; 3 dE, 4 intensity, 5 error
                    state['sb_Qvector']=np.zeros((6, len(pt)*24))# single crystal: 0 alpha*|qU| [A^-1], 1 beta*|qV| [A^-1], 2 |Q|; powder: 0 Qx, 1 Qy; 3 dE, 4 intensity, 5 error
                    #検出器の角度
                    d_angle=np.linspace(0, 46, 24)
                    A2 = np.zeros((1, 24))

                    # C2 is the measured instrument encoder value.
                    C2=np.asarray(c2, dtype=float)

                    #　HODACAで測定した点を計算してくれる
                    #pythonでは行列の数えやfor文は0から始まるので注意すること
                    for n in range(len(pt)):# nは各ファイルのデータの個数に対応

                        #ki_x[0,n] = math.sqrt(ei[n]/2.072)*math.cos(math.radians(-c2[n]))
                        #ki_y[0,n] = -math.sqrt(ei[n]/2.072)*math.sin(math.radians(-c2[n]))
                        ki[0:2,n] = [math.sqrt(ei[n]/2.072)*math.cos(math.radians(-C2[n])),-math.sqrt(ei[n]/2.072)*math.sin(math.radians(-C2[n]))]
                        #A2の絶対値変換
                        update_phi()
                        A2 = d_angle + state['phi'] + a2[n] 

                        # ここで対応するバックグラウンドデータを差し引く。
                        # ((sbpt,sbe,sbei,sbc2,sba2,sbD01,sbD02,sbD03,sbD04,sbD05,sbD06,sbD07,sbD08,sbD09,sbD10,sbD11,sbD12,sbD13,sbD14,sbD15,sbD16,sbD17,sbD18,sbD19,sbD20,sbD21,sbD22,sbD23,sbD24))

                        # まずはエネルギートランスファーが一致する部分を抜き出す。補正をする前同士作業なのでOK。
                        # エネルギースキャンステップに依存するがとりあえず指定したモータートレランスの範囲内にあるエネルギー値のものをサーチする。
                        ind_E = (list(zip(*np.where(((e[n]-dE) < sb_Databox0[:,1]) & (sb_Databox0[:,1] < (e[n]+dE))))))
                        # リスト型に出力
                        Ind_E = list(np.ravel(ind_E))
                        if len(Ind_E) > 0:# Ind_Eが空でないとき
                            # 最も近い場所を選ぶコード
                            sb_data_e=sb_Databox0[Ind_E,:]
                            # まずA2が最も近いデータを選び、その中からC2が最も近いデータを選ぶ。
                            sba2 = sb_data_e[:,4]
                            sbc2 = sb_data_e[:,3]

                            nearestA2 = np.argmin(np.abs(sba2 - a2[n]))
                            closest_a2_indices = np.where(sba2 == sba2[nearestA2])[0]  # インデックスのリストを取得

                            # closest_a2_indices に対応する sbc2 の値を取得し、c2[n] に最も近い値を持つインデックスを取得
                            subset_c2 = sbc2[closest_a2_indices]
                            closest_c2_index = np.argmin(np.abs(subset_c2 - c2[n]))

                            # closest_a2_indices かつ closest_c2_index に含まれるインデックスを取得
                            index_BG = closest_a2_indices[closest_c2_index]
                            for m in range(24):# mは検出器の番号に対応
                                #ki2[:,24*n+m] = ki[:,n]
                                # 各検出器の補正として-fit_result[1,m]
                                kf[0:2,24*n+m] = [math.sqrt((3.635+fit_result[1,m])/2.072)*math.cos(math.radians(A2[m]-C2[n])),-math.sqrt((3.635+fit_result[1,m])/2.072)*math.sin(math.radians(A2[m]-C2[n]))]
                                #kf[0:2,24*n+m] = [math.sqrt(3.635/2.072)*math.cos(math.radians(A2[m]-C2[n])),-math.sqrt(3.635/2.072)*math.sin(math.radians(A2[m]-C2[n]))]
                                state['Qvector'][0:2,24*n+m] = _angles_to_hkl_and_uv(
                                    ei[n],
                                    3.635+fit_result[1,m],
                                    C2[n],
                                    A2[m],
                                    is_single_crystal,
                                    state['data_UBmatrix'] if is_single_crystal else None,
                                    state['u'] if is_single_crystal else None,
                                    state['display_v_hkl'] if is_single_crystal else None,
                                data_ref_c2 if is_single_crystal else None,
                                data_omega_ref if is_single_crystal else None,
                                data_c2_sign if is_single_crystal else +1.0,
                                    ry_deg=ry[n],
                                    rx_deg=rx[n],
                                    ref_ry=data_ref_ry,
                                    ref_rx=data_ref_rx,
                                    spice_to_pdf_transform=state['data_spice_to_pdf']
                                )[0]
                                state['sb_Qvector'][0:2,24*n+m] = _angles_to_hkl_and_uv(
                                    ei[n],
                                    3.635+fit_result[1,m],
                                    C2[n],
                                    A2[m],
                                    is_single_crystal,
                                    state['data_UBmatrix'] if is_single_crystal else None,
                                    state['u'] if is_single_crystal else None,
                                    state['display_v_hkl'] if is_single_crystal else None,
                                data_ref_c2 if is_single_crystal else None,
                                data_omega_ref if is_single_crystal else None,
                                data_c2_sign if is_single_crystal else +1.0,
                                    ry_deg=ry[n],
                                    rx_deg=rx[n],
                                    ref_ry=data_ref_ry,
                                    ref_rx=data_ref_rx,
                                    spice_to_pdf_transform=state['data_spice_to_pdf']
                                )[0]
                                #powder用にqも入れておく
                                state['Qvector'][2,24*n+m] = math.sqrt((ki[0,n] - kf[0,24*n+m])**2+(ki[1,n] - kf[1,24*n+m])**2)
                                state['sb_Qvector'][2,24*n+m] = math.sqrt((ki[0,n] - kf[0,24*n+m])**2+(ki[1,n] - kf[1,24*n+m])**2)
                                # エネルギートランスファーの情報を入れる。各検出器の補正として-fit_result[1,m]
                                state['Qvector'][3,24*n+m] = e[n]-fit_result[1,m]
                                state['sb_Qvector'][3,24*n+m] = e[n]-fit_result[1,m]
                                # 強度の情報を入れる。ここでバナジウムとmcuの補正をする。12番を基準とする。
                                lorentz_factor = 1
                                state['Qvector'][4,24*n+m] = D[n,m]/fit_result[0,m]*fit_result[0,11]*N_mcu/mcu[n]*lorentz_factor
                                state['sb_Qvector'][4,24*n+m] = np.sum(sb_data_e[index_BG,5+m])/fit_result[0,m]*fit_result[0,11]*N_mcu/np.sum(sb_data_e[index_BG,29])*lorentz_factor
                                state['Qvector'][5,24*n+m] = math.sqrt(D[n,m])/fit_result[0,m]*fit_result[0,11]*N_mcu/mcu[n]*lorentz_factor
                                state['sb_Qvector'][5,24*n+m] = math.sqrt(np.sum(sb_data_e[index_BG,5+m]))/fit_result[0,m]*fit_result[0,11]*N_mcu/np.sum(sb_data_e[index_BG,29])*lorentz_factor

                        else:# 対応するエネルギーが無かった場合
                            if sbtype2.get()==0:# Nanが選択されていない
                                for m in range(24):# mは検出器の番号に対応
                                    #ki2[:,24*n+m] = ki[:,n]
                                    # 各検出器の補正として-fit_result[1,m]
                                    kf[0:2,24*n+m] = [math.sqrt((3.635+fit_result[1,m])/2.072)*math.cos(math.radians(A2[m]-C2[n])),-math.sqrt((3.635+fit_result[1,m])/2.072)*math.sin(math.radians(A2[m]-C2[n]))]
                                    #kf[0:2,24*n+m] = [math.sqrt(3.635/2.072)*math.cos(math.radians(A2[m]-C2[n])),-math.sqrt(3.635/2.072)*math.sin(math.radians(A2[m]-C2[n]))]
                                    state['Qvector'][0:2,24*n+m] = _angles_to_hkl_and_uv(
                                    ei[n],
                                    3.635+fit_result[1,m],
                                    C2[n],
                                    A2[m],
                                    is_single_crystal,
                                    state['data_UBmatrix'] if is_single_crystal else None,
                                    state['u'] if is_single_crystal else None,
                                    state['display_v_hkl'] if is_single_crystal else None,
                                data_ref_c2 if is_single_crystal else None,
                                data_omega_ref if is_single_crystal else None,
                                data_c2_sign if is_single_crystal else +1.0,
                                    ry_deg=ry[n],
                                    rx_deg=rx[n],
                                    ref_ry=data_ref_ry,
                                    ref_rx=data_ref_rx,
                                    spice_to_pdf_transform=state['data_spice_to_pdf']
                                )[0]
                                    state['sb_Qvector'][0:2,24*n+m] = _angles_to_hkl_and_uv(
                                    ei[n],
                                    3.635+fit_result[1,m],
                                    C2[n],
                                    A2[m],
                                    is_single_crystal,
                                    state['data_UBmatrix'] if is_single_crystal else None,
                                    state['u'] if is_single_crystal else None,
                                    state['display_v_hkl'] if is_single_crystal else None,
                                data_ref_c2 if is_single_crystal else None,
                                data_omega_ref if is_single_crystal else None,
                                data_c2_sign if is_single_crystal else +1.0,
                                    ry_deg=ry[n],
                                    rx_deg=rx[n],
                                    ref_ry=data_ref_ry,
                                    ref_rx=data_ref_rx,
                                    spice_to_pdf_transform=state['data_spice_to_pdf']
                                )[0]
                                    #powder用にqも入れておく
                                    state['Qvector'][2,24*n+m] = math.sqrt((ki[0,n] - kf[0,24*n+m])**2+(ki[1,n] - kf[1,24*n+m])**2)
                                    state['sb_Qvector'][2,24*n+m] = math.sqrt((ki[0,n] - kf[0,24*n+m])**2+(ki[1,n] - kf[1,24*n+m])**2)
                                    # エネルギートランスファーの情報を入れる。各検出器の補正として-fit_result[1,m]
                                    state['Qvector'][3,24*n+m] = e[n]-fit_result[1,m]
                                    state['sb_Qvector'][3,24*n+m] = e[n]-fit_result[1,m]
                                    lorentz_factor = 1
                                    state['Qvector'][4,24*n+m] = D[n,m]/fit_result[0,m]*fit_result[0,11]*N_mcu/mcu[n]*lorentz_factor
                                    state['sb_Qvector'][4,24*n+m] = np.nan*lorentz_factor
                                    state['Qvector'][5,24*n+m] = math.sqrt(D[n,m])/fit_result[0,m]*fit_result[0,11]*N_mcu/mcu[n]*lorentz_factor
                                    state['sb_Qvector'][5,24*n+m] = np.nan*lorentz_factor
                            elif sbtype2.get()==1:# Nanoptionがon
                                pass

                    # 全てのデータを格納するボックスを立ち上げる。Qvectorのデータをどんどん連結していく。最初のファイルだけdataboxをQvectorにする。
                    if i == 0:
                        Databox=state['Qvector']
                        sb_Databox=state['sb_Qvector']
                    #databox.extend(Qvector)
                    if i > 0:
                        Databox=(np.concatenate([Databox, state['Qvector']], 1))
                        sb_Databox=(np.concatenate([sb_Databox, state['sb_Qvector']], 1))

                    # プログレスバー (確定的)。エネルギー毎にステータスが進む
                    var1=var1+1
                    state['pb']["value"] = var1
                    state['pb'].update()          

        elif bgm==1:# ユーザーがある程度の範囲でバックグラウンドを測定している場合に対応。
            # プログレスバーの表示
            state['pb']["maximum"] = len(state['file_paths'])+len(state['sbfile_paths']) # プログレスバーの最大値
            state['pb']["value"] = 0
            state['pb'].update()

            for i in range(len(state['file_paths'])):
                # データ形式が異なっているファイル(例えば、c2 scanとenergy scanが混じっていても)でも読み取れるように毎回読む仕様に変更する。
                with open(state['file_paths'][i],"r", encoding="utf-8") as f:
                    line = f.readlines()
                    head = line[31]
                    head2 = head.split()
                    if "Pt." in head2:
                        pass
                    else:
                        head = line[32]
                        head2 = head.split()

                    #パラメータは何番目ですか？
                    #global No_Pt,No_c2,No_a2,No_mcu,No_e,No_ei,No_D01,No_D02,No_D03,No_D04,No_D05,No_D06,No_D07,No_D08,No_D09,No_D10,No_D11,No_D12,No_D13,No_D14,No_D15,No_D16,No_D17,No_D18,No_D19,No_D20,No_D21,No_D22,No_D23,No_D24
                    No_Pt=head2.index('Pt.')
                    No_c2=head2.index('c2')
                    No_a2=head2.index('a2')
                    No_ry=head2.index('ry')
                    No_rx=head2.index('rx')
                    No_timeact=head2.index('time-act')
                    #mcuがない場合は読み込まない。もちろんデータも表示されないけどね
                    if head.find('mcu')!=-1:
                        No_mcu=head2.index('mcu')
                    else :
                        pass

                    #No_mcu=data2.index('mcu')
                    No_e=head2.index('e')
                    No_ei=head2.index('ei')
                    No_D01=head2.index('D01')
                    No_D24=head2.index('D24')

                #リストにあるファイルを順に読み込んでいく
                with open(state['file_paths'][i],"r", encoding="utf-8") as f:
                    #選択ファイルの数値を全て読み込む
                    rdb = np.loadtxt(state['file_paths'][i], comments='#')

                    # データが１次元配列の際に２次元配列に格納
                    if len(rdb.shape) == 1:
                        rdb = np.expand_dims(rdb, axis=0)

                    t_a = rdb[:,No_timeact-1]
                    # time-actが0のデータを検索
                    Ind_t0 = np.where(t_a == 0)
                    # time-actが0のデータを削除
                    rdb = np.delete(rdb, Ind_t0, axis=0)

                    pt = rdb[:,No_Pt-1]
                    c2 = rdb[:,No_c2-1]
                    a2 = rdb[:,No_a2-1]
                    ry = rdb[:,No_ry-1]   # SPICE ry -> Mantid/PDF mu
                    rx = rdb[:,No_rx-1]   # SPICE rx -> Mantid/PDF nu
                    #mcuがない場合は読み込まない。強制的にmcuが0となり、IntensityはNan値となる。
                    if head.find('mcu')!=-1:
                        mcu = rdb[:,No_mcu-1]
                    else :
                        mcu = np.zeros((len(pt)))
                    e = rdb[:,No_e-1]
                    ei = rdb[:,No_ei-1]
                    D = rdb[:,No_D01-1:No_D24]

                #kiとkfの定義
                ki = np.zeros((2, len(pt)))
                kf = np.zeros((2, len(pt)*24))
                #ki2 = np.zeros((2, len(pt)*24))
                #Qのベクトルとスカラーの定義、あとここに強度の情報を加える。
                state['Qvector']=np.zeros((6, len(pt)*24))# single crystal: 0 alpha*|qU| [A^-1], 1 beta*|qV| [A^-1], 2 |Q|; powder: 0 Qx, 1 Qy; 3 dE, 4 intensity, 5 error
                #検出器の角度
                d_angle=np.linspace(0, 46, 24)
                A2 = np.zeros((1, 24))

                # C2 is the measured instrument encoder value.
                C2=np.asarray(c2, dtype=float)

                #　HODACAで測定した点を計算してくれる
                #pythonでは行列の数えやfor文は0から始まるので注意すること
                for n in range(len(pt)):# nは各ファイルのデータの個数に対応
                    #ki_x[0,n] = math.sqrt(ei[n]/2.072)*math.cos(math.radians(-c2[n]))
                    #ki_y[0,n] = -math.sqrt(ei[n]/2.072)*math.sin(math.radians(-c2[n]))
                    ki[0:2,n] = [math.sqrt(ei[n]/2.072)*math.cos(math.radians(-C2[n])),-math.sqrt(ei[n]/2.072)*math.sin(math.radians(-C2[n]))]
                    #A2の絶対値変換
                    update_phi()
                    A2 = d_angle + state['phi'] + a2[n] 
                    for m in range(24):# mは検出器の番号に対応
                        #ki2[:,24*n+m] = ki[:,n]
                        # 各検出器の補正として-fit_result[1,m]
                        kf[0:2,24*n+m] = [math.sqrt((3.635+fit_result[1,m])/2.072)*math.cos(math.radians(A2[m]-C2[n])),-math.sqrt((3.635+fit_result[1,m])/2.072)*math.sin(math.radians(A2[m]-C2[n]))]
                        #kf[0:2,24*n+m] = [math.sqrt(3.635/2.072)*math.cos(math.radians(A2[m]-C2[n])),-math.sqrt(3.635/2.072)*math.sin(math.radians(A2[m]-C2[n]))]
                        state['Qvector'][0:2,24*n+m] = _angles_to_hkl_and_uv(
                                    ei[n],
                                    3.635+fit_result[1,m],
                                    C2[n],
                                    A2[m],
                                    is_single_crystal,
                                    state['data_UBmatrix'] if is_single_crystal else None,
                                    state['u'] if is_single_crystal else None,
                                    state['display_v_hkl'] if is_single_crystal else None,
                                data_ref_c2 if is_single_crystal else None,
                                data_omega_ref if is_single_crystal else None,
                                data_c2_sign if is_single_crystal else +1.0,
                                    ry_deg=ry[n],
                                    rx_deg=rx[n],
                                    ref_ry=data_ref_ry,
                                    ref_rx=data_ref_rx,
                                    spice_to_pdf_transform=state['data_spice_to_pdf']
                                )[0]                   
                        #powder用にqも入れておく
                        state['Qvector'][2,24*n+m] = math.sqrt((ki[0,n] - kf[0,24*n+m])**2+(ki[1,n] - kf[1,24*n+m])**2)
                        # エネルギートランスファーの情報を入れる。各検出器の補正として-fit_result[1,m]
                        state['Qvector'][3,24*n+m] = e[n]-fit_result[1,m]
                        lorentz_factor = 1
                        state['Qvector'][4,24*n+m] = D[n,m]/fit_result[0,m]*fit_result[0,11]*N_mcu/mcu[n]*lorentz_factor
                        state['Qvector'][5,24*n+m] = math.sqrt(D[n,m])/fit_result[0,m]*fit_result[0,11]*N_mcu/mcu[n]*lorentz_factor

                # 全てのデータを格納するボックスを立ち上げる。Qvectorのデータをどんどん連結していく。最初のファイルだけdataboxをQvectorにする。
                if i == 0:
                    Databox=state['Qvector']
                #databox.extend(Qvector)
                if i > 0:
                    Databox=(np.concatenate([Databox, state['Qvector']], 1))

                # プログレスバー (確定的)。エネルギー毎にステータスが進む
                var1=var1+1
                #pb.configure(value = var1)
                state['pb']["value"] = var1
                state['pb'].update()

            # backgroundのdataを読み込む。   
            # backgroundのdataを読み込む。すべての範囲をスキャンすることを前提にしている。そうしないと場合分けが不可能なので疑似データを作成できない。   
            for i in range(len(state['sbfile_paths'])):
                # データ形式が異なっているファイル(例えば、c2 scanとenergy scanが混じっていても)でも読み取れるように毎回読む仕様に変更する。
                with open(state['sbfile_paths'][i],"r", encoding="utf-8") as f:
                    line = f.readlines()
                    head = line[31]
                    head2 = head.split()
                    if "Pt." in head2:
                        pass
                    else:
                        head = line[32]
                        head2 = head.split()

                    #パラメータは何番目ですか？
                    #global SbNo_Pt,SbNo_c2,SbNo_a2,SbNo_mcu,SbNo_e,SbNo_ei,SbNo_D01,SbNo_D02,SbNo_D03,SbNo_D04,SbNo_D05,SbNo_D06,SbNo_D07,SbNo_D08,SbNo_D09,SbNo_D10,SbNo_D11,SbNo_D12,SbNo_D13,SbNo_D14,SbNo_D15,SbNo_D16,SbNo_D17,SbNo_D18,SbNo_D19,SbNo_D20,SbNo_D21,SbNo_D22,SbNo_D23,SbNo_D24
                    sb_No_Pt=head2.index('Pt.')
                    sb_No_c2=head2.index('c2')
                    sb_No_a2=head2.index('a2')
                    sb_No_ry=head2.index('ry')
                    sb_No_rx=head2.index('rx')
                    sb_No_timeact=head2.index('time-act')
                    #mcuがない場合は読み込まない。もちろんデータも表示されないけどね
                    if head.find('mcu')!=-1:
                        sb_No_mcu=head2.index('mcu')
                    else :
                        pass

                    #SbNo_mcu=data2.index('mcu')
                    sb_No_e=head2.index('e')
                    sb_No_ei=head2.index('ei')
                    sb_No_D01=head2.index('D01')
                    sb_No_D24=head2.index('D24')

                #リストにあるファイルを順に読み込んでいく
                with open(state['sbfile_paths'][i],"r", encoding="utf-8") as f:
                    #選択ファイルの数値を全て読み込む
                    sb_rdb = np.loadtxt(state['sbfile_paths'][i], comments='#')

                    # データが１次元配列の際に２次元配列に格納
                    if len(sb_rdb.shape) == 1:
                        sb_rdb = np.expand_dims(sb_rdb, axis=0)

                    t_a = sb_rdb[:,sb_No_timeact-1]
                    # time-actが0のデータを検索
                    Ind_t0 = np.where(t_a == 0)
                    # time-actが0のデータを削除
                    sb_rdb = np.delete(sb_rdb, Ind_t0, axis=0)

                    sb_pt = sb_rdb[:,sb_No_Pt-1]
                    sb_c2 = sb_rdb[:,sb_No_c2-1]
                    sb_a2 = sb_rdb[:,sb_No_a2-1]
                    if is_single_crystal:
                        sb_ry = sb_rdb[:,sb_No_ry-1]   # SPICE ry -> Mantid/PDF mu
                        sb_rx = sb_rdb[:,sb_No_rx-1]   # SPICE rx -> Mantid/PDF nu
                    else:
                        sb_ry = np.zeros(len(sb_pt), dtype=float)
                        sb_rx = np.zeros(len(sb_pt), dtype=float)
                    #mcuがない場合は読み込まない。強制的にmcuが0となり、IntensityはNan値となる。
                    if head.find('mcu')!=-1:
                        sb_mcu = sb_rdb[:,sb_No_mcu-1]
                    else :
                        sb_mcu = np.zeros((len(sb_pt)))
                    sb_e = sb_rdb[:,sb_No_e-1]
                    sb_ei = sb_rdb[:,sb_No_ei-1]
                    sb_D = sb_rdb[:,sb_No_D01-1:sb_No_D24]

                #sb_kiとsb_kfの定義
                sb_ki = np.zeros((2, len(sb_pt)))
                sb_kf = np.zeros((2, len(sb_pt)*24))
                #sb_ki2 = np.zeros((2, len(pt)*24))
                #Qのベクトルとスカラーの定義、あとここに強度の情報を加える。
                state['sb_Qvector']=np.zeros((6, len(sb_pt)*24))# single crystal: 0 alpha*|qU| [A^-1], 1 beta*|qV| [A^-1], 2 |Q|; powder: 0 Qx, 1 Qy
                #検出器の角度
                d_angle=np.linspace(0, 46, 24)
                sb_A2 = np.zeros((1, 24))

                #sb_C2のオフセット
                sb_C2=sb_c2-w_off

                #　HODACAで測定した点を計算してくれる
                #pythonでは行列の数えやfor文は0から始まるので注意すること
                for n in range(len(sb_pt)):# nは各ファイルのデータの個数に対応
                    #sb_ki_x[0,n] = math.sqrt(ei[n]/2.072)*math.cos(math.radians(-c2[n]))
                    #sb_ki_y[0,n] = -math.sqrt(ei[n]/2.072)*math.sin(math.radians(-c2[n]))
                    sb_ki[0:2,n] = [math.sqrt(sb_ei[n]/2.072)*math.cos(math.radians(-sb_C2[n])),-math.sqrt(sb_ei[n]/2.072)*math.sin(math.radians(-sb_C2[n]))]
                    #sb_A2の絶対値変換
                    sb_A2=d_angle+state['phi']+sb_a2[n];# cover range
                    for m in range(24):# mは検出器の番号に対応
                        #sb_ki2[:,24*n+m] = sb_ki[:,n]
                        # 各検出器の補正として-fit_result[1,m]
                        sb_kf[0:2,24*n+m] = [math.sqrt((3.635+fit_result[1,m])/2.072)*math.cos(math.radians(sb_A2[m]-sb_C2[n])),-math.sqrt((3.635+fit_result[1,m])/2.072)*math.sin(math.radians(sb_A2[m]-sb_C2[n]))]
                        #sb_kf[0:2,24*n+m] = [math.sqrt(3.635/2.072)*math.cos(math.radians(sb_A2[m]-sb_C2[n])),-math.sqrt(3.635/2.072)*math.sin(math.radians(sb_A2[m]-sb_C2[n]))]
                        state['sb_Qvector'][0:2,24*n+m] = _angles_to_hkl_and_uv(
                            sb_ei[n],
                            3.635+fit_result[1,m],
                            sb_C2[n],
                            sb_A2[m],
                            is_single_crystal,
                            state['data_UBmatrix'] if is_single_crystal else None,
                            state['u'] if is_single_crystal else None,
                            state['display_v_hkl'] if is_single_crystal else None,
                        data_ref_c2 if is_single_crystal else None,
                        data_omega_ref if is_single_crystal else None,
                        data_c2_sign if is_single_crystal else +1.0,
                                    ry_deg=sb_ry[n],
                                    rx_deg=sb_rx[n],
                                    ref_ry=data_ref_ry,
                                    ref_rx=data_ref_rx,
                                    spice_to_pdf_transform=state['data_spice_to_pdf']
                        )[0]                   
                        #powder用にqも入れておく
                        state['sb_Qvector'][2,24*n+m] = math.sqrt((sb_ki[0,n] - sb_kf[0,24*n+m])**2+(sb_ki[1,n] - sb_kf[1,24*n+m])**2)
                        # エネルギートランスファーの情報を入れる。各検出器の補正として-fit_result[1,m]
                        state['sb_Qvector'][3,24*n+m] = sb_e[n]-fit_result[1,m]
                        lorentz_factor = 1
                        state['sb_Qvector'][4,24*n+m] = sb_D[n,m]/fit_result[0,m]*fit_result[0,11]*N_mcu/sb_mcu[n]*lorentz_factor
                        state['sb_Qvector'][5,24*n+m] = math.sqrt(sb_D[n,m])/fit_result[0,m]*fit_result[0,11]*N_mcu/sb_mcu[n]*lorentz_factor
                # 全てのデータを格納するボックスを立ち上げる。sb_Qvectorのデータをどんどん連結していく。最初のファイルだけdataboxをsb_Qvectorにする。
                if i == 0:
                    sb_Databox=state['sb_Qvector']
                #databox.extend(sb_Qvector)
                if i > 0:
                    sb_Databox=(np.concatenate([sb_Databox, state['sb_Qvector']], 1))

                # プログレスバー (確定的)。エネルギー毎にステータスが進む
                var1=var1+1
                #pb.configure(value = var1)
                state['pb']["value"] = var1
                state['pb'].update()  

    # 全ての処理が終わった後にmaskした検出器のデータ点を省く
    # maskする検出器の番号を取得する。
    mask_det = [var.get() for var in check_vars]
    # 値が1である要素のインデックスを取得
    n_delete = [i for i, value in enumerate(mask_det) if value == 1]
    # 削除する余りの番号を指定
    remainder_numbers_to_delete = n_delete

    # 対応する列を特定し、削除
    # shared variables are stored in state # 0 Qx, 1 Qy, 2 Q, 3 エネルギートランスファー,　4 規格化強度,  5 規格化エラーバー
    columns_to_delete = [i for i in range(len(Databox[0,:])) if i % 24 in remainder_numbers_to_delete]
    state['databox'] = np.delete(Databox, columns_to_delete, axis=1)

    #バックグラウンドファイルがあった場合
    if len(state['sbfile_paths'])>0:
        # shared variables are stored in state # 0 Qx, 1 Qy, 2 Q, 3 エネルギートランスファー,　4 規格化強度,  5 規格化エラーバー
        sb_columns_to_delete = [i for i in range(len(sb_Databox[0,:])) if i % 24 in remainder_numbers_to_delete]
        state['sb_databox'] = np.delete(sb_Databox, sb_columns_to_delete, axis=1)

    # The display basis is explicitly right-handed, so the old post-hoc
    # Qx sign flip is no longer needed.  Keep sign=1 for compatibility.

    # Cache HKL values without changing the 6-row databox layout:
    # single crystal rows are [alpha*NU1, beta*NV1, |Q|, dE, intensity, error],
    # where HKL = alpha*U + beta*display_V.
    # This preserves the historical A^-1 display-coordinate scale.
    # powder rows remain [Qx, Qy, |Q|, dE, intensity, error].
    # shared variables are stored in state
    if is_single_crystal:
        state['hklbox'] = np.empty((3, state['databox'].shape[1]), dtype=float)
        for _j in range(state['databox'].shape[1]):
            state['hklbox'][:, _j] = _display_uv_to_hkl(
                state['databox'][0:2, _j], state['u'], state['display_v_hkl'], state['NU1'], state['NV1']
            )
        if len(state['sbfile_paths']) > 0:
            state['sb_hklbox'] = np.empty((3, state['sb_databox'].shape[1]), dtype=float)
            for _j in range(state['sb_databox'].shape[1]):
                state['sb_hklbox'][:, _j] = _display_uv_to_hkl(
                    state['sb_databox'][0:2, _j], state['u'], state['display_v_hkl'], state['NU1'], state['NV1']
                )
        else:
            state['sb_hklbox'] = None
    else:
        state['hklbox'] = None
        state['sb_hklbox'] = None

    # single crystalの場合の軸の名前
    with open(state['file_paths'][0], "r", encoding="utf-8") as f:
        line = f.readlines()
        chead = line[31]
        chead2 = chead.split()
        if "Pt." in chead2:# powderの場合行数が少ない。
            pass

        else:
            # single crystalの場合

            # ------------------------------------------------------------
            # U-axis label
            # ------------------------------------------------------------

            u_label_hkl = np.array([
                float(txt9.get()),
                float(txt10.get()),
                float(txt11.get())
            ], dtype=float)


            # ------------------------------------------------------------
            # V-axis label
            #
            # single crystalでは、自動選択されたdisplay_v_hklを使う。
            # 例:
            #   entered V = (0,1,0)
            #   triangular lattice
            #       -> display V = (-1,2,0)
            # ------------------------------------------------------------

            if is_single_crystal and state['display_v_hkl'] is not None:
                v_label_hkl = np.asarray(state['display_v_hkl'], dtype=float)
            else:
                v_label_hkl = np.array([
                    float(txt12.get()),
                    float(txt13.get()),
                    float(txt14.get())
                ], dtype=float)


            # ------------------------------------------------------------
            # HKLラベル作成用
            # ------------------------------------------------------------

            def _format_hkl_component(x, suffix):
                x = float(x)

                if abs(x) < 1.0e-10:
                    return "0"

                # ほぼ整数
                if abs(x - round(x)) < 1.0e-10:
                    n = int(round(x))

                    if n == 1:
                        return str(suffix)

                    elif n == -1:
                        return "-" + str(suffix)

                    else:
                        return str(n) + str(suffix)

                # 非整数
                return f"{x:g}{suffix}"


            # ------------------------------------------------------------
            # U label
            # ------------------------------------------------------------

            ul1 = _format_hkl_component(
                u_label_hkl[0],
                txt_ul.get()
            )

            ul2 = _format_hkl_component(
                u_label_hkl[1],
                txt_ul.get()
            )

            ul3 = _format_hkl_component(
                u_label_hkl[2],
                txt_ul.get()
            )


            # ------------------------------------------------------------
            # V label
            # ------------------------------------------------------------

            vl1 = _format_hkl_component(
                v_label_hkl[0],
                txt_vl.get()
            )

            vl2 = _format_hkl_component(
                v_label_hkl[1],
                txt_vl.get()
            )

            vl3 = _format_hkl_component(
                v_label_hkl[2],
                txt_vl.get()
            )


            # shared variables are stored in state

            state['Ulabel'] = f"({ul1},{ul2},{ul3})"
            state['Vlabel'] = f"({vl1},{vl2},{vl3})"
