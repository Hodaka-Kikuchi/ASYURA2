from ...callback_runtime import *

def prepare_simu_reciprocal_display(env):
    state = env.get('state')
    txt1 = env.get('txt1')
    txt10 = env.get('txt10')
    txt11 = env.get('txt11')
    txt12 = env.get('txt12')
    txt13 = env.get('txt13')
    txt14 = env.get('txt14')
    txt2 = env.get('txt2')
    txt3 = env.get('txt3')
    txt4 = env.get('txt4')
    txt5 = env.get('txt5')
    txt6 = env.get('txt6')
    txt9 = env.get('txt9')
    txt_ref_c2 = env.get('txt_ref_c2')
    txt_ref_h = env.get('txt_ref_h')
    txt_ref_k = env.get('txt_ref_k')
    txt_ref_l = env.get('txt_ref_l')

    # ------------------------------------------------------------
    # scattering-plane vectors
    # ------------------------------------------------------------
    u_hkl = np.array(
        [
            float(txt9.get()),
            float(txt10.get()),
            float(txt11.get())
        ],
        dtype=float
    )

    v_hkl = np.array(
        [
            float(txt12.get()),
            float(txt13.get()),
            float(txt14.get())
        ],
        dtype=float
    )

    # ------------------------------------------------------------
    # reference reflection and instrument C2
    # ------------------------------------------------------------
    ref_hkl = np.array(
        [
            float(txt_ref_h.get()),
            float(txt_ref_k.get()),
            float(txt_ref_l.get())
        ],
        dtype=float
    )

    ref_c2 = float(txt_ref_c2.get())

    # ------------------------------------------------------------
    # lattice parameters
    # ------------------------------------------------------------
    la  = float(txt1.get())
    lb  = float(txt2.get())
    lc  = float(txt3.get())

    lal = float(txt4.get())
    lbe = float(txt5.get())
    lga = float(txt6.get())

    # ------------------------------------------------------------
    # Simulation UB
    #
    # Do NOT import an arbitrary measured SPICE UB here.
    # A measured UB can include a real goniometer/tilt orientation.
    # The scan simulation is instead defined by lattice + entered U,V:
    #
    #   U-V plane -> laboratory x-z plane
    #   plane normal -> laboratory +y
    #
    # Therefore mu = nu = 0 is a valid simulation geometry.
    # ------------------------------------------------------------
    if state['file_paths'] and state['file_paths'][0]:

        with open(state['file_paths'][0], "r", encoding="utf-8") as f:
            lines = f.readlines()

        if len(lines) <= 21:
            raise ValueError(
                "SPICE file does not contain the expected UB line (line 22)."
            )

        ub_line = lines[21].strip()
        ub_parts = ub_line.split(',')

        if len(ub_parts) < 9:
            raise ValueError(
                "Could not parse 3x3 UB matrix from the SPICE file."
            )

        first_value = re.sub(
            r"[^\d.eE+\-]",
            "",
            ub_parts[0]
        )

        ub_values = (
            [first_value]
            + [x.strip() for x in ub_parts[1:9]]
        )

        try:
            UB_raw = np.array(
                [float(x) for x in ub_values],
                dtype=float
            ).reshape(3, 3)

        except ValueError as exc:
            raise ValueError(
                "Could not convert the SPICE UB matrix to numbers."
            ) from exc

        # --------------------------------------------------------
        # raw SPICE UB -> PDF canonical frame
        #
        # data processing と同じ処理を使用する。
        # U/V を入れ替えても raw SPICE vertical を基準として
        # scattering-plane normal の向きを固定する。
        # --------------------------------------------------------

        ub, _ = _canonicalize_spice_ub_for_pdf(
            UB_raw,
            u_hkl,
            v_hkl
        )

        ub_source = f"SPICE UB: {state['file_paths'][0]}"

    else:

        # --------------------------------------------------------
        # SPICE data file がない場合
        #
        # lattice parameters + entered U,V から simulation UB を作る。
        # --------------------------------------------------------

        ub = _make_simulation_ub_from_lattice_uv(
            la, lb, lc,
            lal, lbe, lga,
            u_hkl, v_hkl
        )

        ub_source = "lattice + U,V"

    # ------------------------------------------------------------
    # display coordinate system
    # ------------------------------------------------------------
    (
        q_u,
        q_v,
        plane_normal,
        nu,
        nv,
        entered_angle,
        used_angle,
        v_used,
        mode,
        coeff
    ) = _make_crystallographic_display_basis(
        ub,
        u_hkl,
        v_hkl
    )

    # shared variables are stored in state
    state['u'] = u_hkl.copy()
    state['v'] = v_hkl.copy()

    # ------------------------------------------------------------
    # Absolute C2 calibration.
    #
    # This is NOT the old "C2 offset" formula.
    # ref_c2 is the encoder value at the reference reflection;
    # omega_ref is the corresponding physical sample rotation.
    # ------------------------------------------------------------
    omega_ref, ref_a2 = _calculate_simu_reference_omega(
        ub,
        ref_hkl,
        ref_c2,
        energy_meV=3.635
    )

    c2_sign = float(SIMU_C2_TO_OMEGA_SIGN)

    # ------------------------------------------------------------
    # diagnostic output
    # ------------------------------------------------------------
    print(f"scan simulation: UB source = {ub_source}")
    print("scan simulation: UB matrix:\n", ub)
    print(f"scan simulation: ref C2 = {ref_c2:.6f} deg")
    print(f"scan simulation: ref omega = {omega_ref:.6f} deg")
    print(f"scan simulation: C2->omega sign = {c2_sign:+.0f}")
    print(
        f"scan simulation: entered physical U-V angle "
        f"= {entered_angle:.6f} deg"
    )

    if mode == "orthogonal-crystallographic":
        print(
            "scan simulation display: "
            "crystallographic orthogonal axis found"
        )
        print(
            "V_display = "
            f"{np.array2string(v_used, precision=6)}"
        )
        print(
            f"display U-V angle = {used_angle:.6f} deg"
        )
        if coeff is not None:
            print(
                f"V_display = {coeff[0]} * U "
                f"+ {coeff[1]} * V"
            )
    else:
        print(
            "scan simulation display: entered non-orthogonal "
            "U,V are shown on perpendicular screen axes; "
            "constant-|Q| contours are elliptical."
        )

    return (
        ub,
        u_hkl,
        v_hkl,
        q_u,
        q_v,
        plane_normal,
        nu,
        nv,
        entered_angle,
        used_angle,
        v_used,
        mode,
        coeff,
        ref_c2,
        omega_ref,
        c2_sign
    )
