from ...callback_runtime import *

def calculate_c2(env):
    lbl_ubc_m2 = env.get('lbl_ubc_m2')
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
    txt_ref_a2 = env.get('txt_ref_a2')
    txt_ref_c2 = env.get('txt_ref_c2')
    txt_ref_ef = env.get('txt_ref_ef')
    txt_ref_ei = env.get('txt_ref_ei')
    txt_ref_h = env.get('txt_ref_h')
    txt_ref_k = env.get('txt_ref_k')
    txt_ref_l = env.get('txt_ref_l')
    txt_ref_rx = env.get('txt_ref_rx')
    txt_ref_ry = env.get('txt_ref_ry')
    txt_ub_11 = env.get('txt_ub_11')
    txt_ub_12 = env.get('txt_ub_12')
    txt_ub_13 = env.get('txt_ub_13')
    txt_ub_21 = env.get('txt_ub_21')
    txt_ub_22 = env.get('txt_ub_22')
    txt_ub_23 = env.get('txt_ub_23')
    txt_ub_31 = env.get('txt_ub_31')
    txt_ub_32 = env.get('txt_ub_32')
    txt_ub_33 = env.get('txt_ub_33')
    txt_ubc_0 = env.get('txt_ubc_0')
    txt_ubc_1 = env.get('txt_ubc_1')
    txt_ubc_2 = env.get('txt_ubc_2')
    txt_ubc_3 = env.get('txt_ubc_3')
    txt_ubc_hl11 = env.get('txt_ubc_hl11')
    txt_ubc_hl12 = env.get('txt_ubc_hl12')
    txt_ubc_hl21 = env.get('txt_ubc_hl21')
    txt_ubc_hl22 = env.get('txt_ubc_hl22')
    txt_ubc_hl31 = env.get('txt_ubc_hl31')
    txt_ubc_hl32 = env.get('txt_ubc_hl32')
    txt_ubc_r1 = env.get('txt_ubc_r1')
    txt_ubc_r2 = env.get('txt_ubc_r2')
    txt_ubc_r3 = env.get('txt_ubc_r3')
    txt_ubc_r4 = env.get('txt_ubc_r4')
    txt_ubc_r5 = env.get('txt_ubc_r5')
    txt_ubc_r6 = env.get('txt_ubc_r6')
    """
    Reference Peak1 をアンカーとして target (H,K,L,hw) の
    C1, A1, C2, A2, rx, ry を計算する。

    この版では rx/ry の扱いを、データ -> HKL 変換側と同じ
    raw SPICE motor frame の相対回転として扱う。

    raw SPICE tilt:
        A(rx, ry) = Rx_raw(-ry) @ Ry_raw(-rx)

    Reference Peak1 に対する相対回転:
        C_rel
          = T
            @ A(rx_target, ry_target)
            @ A(rx_ref, ry_ref).T
            @ T.T

    データ -> HKL 側:
        q0 = C_rel @ Ry(omega).T @ q_lab

    したがって角度計算側では、その逆変換

        q_lab = Ry(omega) @ C_rel.T @ q0

    を満たす motor angles を求める。

    HODACA 4-axis mode:
        rx は Reference Peak1 の値に固定し、
        ry のみを tilt adjustment として動かす。

    NOTE
    ----
    _canonicalize_spice_ub_for_pdf() は修正版を使用し、

        UB_pdf, T = _canonicalize_spice_ub_for_pdf(...)

    の2つを返すことを前提とする。
    """

    # ============================================================
    # helper functions
    # ============================================================

    def normalize_angle_deg(angle):
        """Angle in degrees -> [-180, 180)."""
        return (float(angle) + 180.0) % 360.0 - 180.0

    def angle_near_reference(angle_deg, reference_deg):
        """Return an equivalent 360-deg branch nearest reference_deg."""
        return float(reference_deg) + normalize_angle_deg(
            float(angle_deg) - float(reference_deg)
        )

    def set_entry(entry, value=None, foreground=None):
        entry.config(state="normal")
        entry.delete(0, tk.END)

        if value is not None:
            entry.insert(0, value)

        if foreground is not None:
            entry.config(foreground=foreground)

        entry.config(state="readonly")

    # ------------------------------------------------------------
    # PDF-frame omega rotation
    # ------------------------------------------------------------
    def Ry_pdf_deg(angle_deg):
        """
        Right-handed rotation about PDF laboratory +y.

        PDF convention:
            +z : incident beam
            +y : vertical
            +x : horizontal transverse
        """
        a = math.radians(float(angle_deg))
        c = math.cos(a)
        s = math.sin(a)

        return np.array([
            [ c, 0.0,  s],
            [0.0, 1.0, 0.0],
            [-s, 0.0,  c],
        ], dtype=float)

    # ------------------------------------------------------------
    # raw SPICE motor-frame rotations
    # ------------------------------------------------------------
    def Rx_raw_deg(angle_deg):
        """Right-handed rotation about raw-SPICE +x."""
        a = math.radians(float(angle_deg))
        c = math.cos(a)
        s = math.sin(a)

        return np.array([
            [1.0, 0.0, 0.0],
            [0.0,  c, -s],
            [0.0,  s,  c],
        ], dtype=float)

    def Ry_raw_deg(angle_deg):
        """Right-handed rotation about raw-SPICE +y."""
        a = math.radians(float(angle_deg))
        c = math.cos(a)
        s = math.sin(a)

        return np.array([
            [ c, 0.0,  s],
            [0.0, 1.0, 0.0],
            [-s, 0.0,  c],
        ], dtype=float)

    def spice_raw_tilt_matrix(rx_deg, ry_deg):
        """
        Absolute SPICE rx/ry motor orientation in raw SPICE coordinates.

        User-verified SPICE convention:

            A(rx, ry)
                = Rx_raw(-ry)
                  @ Ry_raw(-rx)

        The matrix product automatically contains the finite-rotation
        effect that the second rotation acts after the first rotation
        has changed the orientation of the sample frame.
        """
        return (
            Rx_raw_deg(-float(ry_deg))
            @ Ry_raw_deg(-float(rx_deg))
        )

    def relative_spice_tilt_pdf(
        rx_deg,
        ry_deg,
        ref_rx_deg,
        ref_ry_deg,
        spice_to_pdf_transform,
    ):
        """
        Relative rx/ry rotation from Reference Peak1 to target,
        expressed in the canonical PDF frame.

            C_rel
              = T
                @ A_target
                @ A_ref.T
                @ T.T
        """
        T = np.asarray(spice_to_pdf_transform, dtype=float)

        if T.shape != (3, 3):
            raise ValueError(
                "SPICE-to-PDF transform must be a 3x3 matrix."
            )

        A_target = spice_raw_tilt_matrix(
            rx_deg,
            ry_deg,
        )

        A_ref = spice_raw_tilt_matrix(
            ref_rx_deg,
            ref_ry_deg,
        )

        C_rel = (
            T
            @ A_target
            @ A_ref.T
            @ T.T
        )

        return C_rel

    # ------------------------------------------------------------
    # neutron scattering geometry
    # ------------------------------------------------------------
    def q_lab_pdf(ei_meV, ef_meV, a2_deg):
        """
        Laboratory momentum transfer in the PDF frame.

            Q_lab = ki - kf
                  = (-kf sin A2,
                      0,
                      ki - kf cos A2)
        """
        ei_meV = float(ei_meV)
        ef_meV = float(ef_meV)

        if ei_meV <= 0.0 or ef_meV <= 0.0:
            raise ValueError(
                f"Neutron energy must be positive: "
                f"Ei={ei_meV}, Ef={ef_meV}"
            )

        ki = math.sqrt(ei_meV / 2.072)
        kf = math.sqrt(ef_meV / 2.072)
        a2 = math.radians(float(a2_deg))

        return np.array([
            -kf * math.sin(a2),
            0.0,
            ki - kf * math.cos(a2),
        ], dtype=float)

    def scattering_angle_from_q(qnorm, ei_meV, ef_meV):
        """
        Calculate positive instrument A2 from |Q|, Ei and Ef.
        """
        ki = math.sqrt(float(ei_meV) / 2.072)
        kf = math.sqrt(float(ef_meV) / 2.072)

        arg = (
            ki * ki
            + kf * kf
            - float(qnorm) * float(qnorm)
        ) / (2.0 * ki * kf)

        if arg < -1.0 - 1.0e-10 or arg > 1.0 + 1.0e-10:
            raise ValueError(
                f"Requested Q is inaccessible: "
                f"|Q|={qnorm:.6f} A^-1, "
                f"Ei={ei_meV:.6f} meV, "
                f"Ef={ef_meV:.6f} meV"
            )

        return math.degrees(
            math.acos(
                float(np.clip(arg, -1.0, 1.0))
            )
        )

    # ------------------------------------------------------------
    # reference omega
    # ------------------------------------------------------------
    def calculate_reference_omega(
        UB_pdf,
        ref_hkl,
        ref_a2,
        ref_ei,
        ref_ef,
    ):
        """
        Determine omega at Reference Peak1 from

            q_lab_ref = Ry(omega_ref) @ q0_ref

        with

            q0_ref = 2*pi*UB_pdf@HKL_ref.

        At Reference Peak1,

            C_rel = I

        by definition, irrespective of the absolute Peak1 rx/ry values.
        """
        q0_ref = (
            2.0
            * math.pi
            * (
                np.asarray(UB_pdf, dtype=float)
                @ np.asarray(ref_hkl, dtype=float)
            )
        )

        if np.linalg.norm(q0_ref) < 1.0e-12:
            raise ValueError(
                "Reference HKL gives zero Q."
            )

        qlab_ref = q_lab_pdf(
            ref_ei,
            ref_ef,
            ref_a2,
        )

        phi_lab = math.degrees(
            math.atan2(
                float(qlab_ref[0]),
                float(qlab_ref[2]),
            )
        )

        phi_zero = math.degrees(
            math.atan2(
                float(q0_ref[0]),
                float(q0_ref[2]),
            )
        )

        omega_ref = normalize_angle_deg(
            phi_lab - phi_zero
        )

        qlab_ref_calc = (
            Ry_pdf_deg(omega_ref)
            @ q0_ref
        )

        mismatch = float(
            np.linalg.norm(
                qlab_ref_calc - qlab_ref
            )
        )

        return (
            float(omega_ref),
            q0_ref,
            qlab_ref,
            qlab_ref_calc,
            mismatch,
        )

    # ------------------------------------------------------------
    # solve omega / C2 for a chosen rx,ry
    # ------------------------------------------------------------
    def solve_c2_for_fixed_tilts(
        q0_target,
        qlab_target,
        T,
        rx_deg,
        ry_deg,
        ref_rx_deg,
        ref_ry_deg,
        omega_ref,
        c2_ref,
        c2_sign,
    ):
        """
        For a chosen absolute rx/ry pair, calculate the relative tilt
        in the PDF frame and solve omega analytically.

        Forward equation:

            q_lab
              = Ry(omega)
                @ C_rel.T
                @ q0

        Since Ry(omega) does not change the PDF y component,
        the y component of

            q_pre = C_rel.T @ q0

        must be zero for the horizontal scattering condition.
        """
        C_rel = relative_spice_tilt_pdf(
            rx_deg,
            ry_deg,
            ref_rx_deg,
            ref_ry_deg,
            T,
        )

        q_pre = (
            C_rel.T
            @ np.asarray(q0_target, dtype=float)
        )

        qperp = float(q_pre[1])

        phi_lab = math.degrees(
            math.atan2(
                float(qlab_target[0]),
                float(qlab_target[2]),
            )
        )

        phi_pre = math.degrees(
            math.atan2(
                float(q_pre[0]),
                float(q_pre[2]),
            )
        )

        omega_raw = phi_lab - phi_pre

        omega = angle_near_reference(
            omega_raw,
            omega_ref,
        )

        if abs(float(c2_sign)) < 1.0e-14:
            raise ValueError(
                "C2-to-omega sign must be non-zero."
            )

        c2_deg = (
            float(c2_ref)
            + (
                float(omega)
                - float(omega_ref)
            ) / float(c2_sign)
        )

        return (
            float(c2_deg),
            float(omega),
            float(qperp),
            C_rel,
            q_pre,
        )

    # ------------------------------------------------------------
    # 4-axis objective: rx fixed, ry varied
    # ------------------------------------------------------------
    def objective_for_ry(
        q0_target,
        qlab_target,
        T,
        rx_fixed,
        ry_deg,
        ref_rx,
        ref_ry,
        omega_ref,
        c2_ref,
        c2_sign,
    ):
        """
        HODACA 4-axis mode objective.

        rx is fixed at Reference Peak1.
        ry is varied until the transformed target Q lies in the
        horizontal PDF scattering plane.
        """
        (
            c2_deg,
            omega_deg,
            qperp,
            C_rel,
            q_pre,
        ) = solve_c2_for_fixed_tilts(
            q0_target,
            qlab_target,
            T,
            rx_fixed,
            ry_deg,
            ref_rx,
            ref_ry,
            omega_ref,
            c2_ref,
            c2_sign,
        )

        qscale = max(
            1.0,
            float(np.linalg.norm(q0_target)),
        )

        # Strongly enforce the scattering-plane condition.
        plane_term = (
            qperp / qscale
        ) ** 2 * 1.0e8

        # If equivalent solutions exist, prefer a ry value near Peak1.
        dry = (
            float(ry_deg)
            - float(ref_ry)
        )

        move_term = dry * dry

        objective = (
            plane_term
            + move_term
        )

        return (
            float(objective),
            float(c2_deg),
            float(omega_deg),
            float(qperp),
            C_rel,
            q_pre,
        )

    def solve_target_motors(
        q0_target,
        qlab_target,
        T,
        c2_ref,
        omega_ref,
        ref_rx,
        ref_ry,
        c2_sign,
    ):
        """
        Solve target HODACA sample motors.

        4-axis restriction:
            rx_target = rx_ref

        and only ry is searched.

        For each ry candidate, C2 is obtained analytically through omega.
        """
        rx_target = float(ref_rx)

        # --------------------------------------------------------
        # coarse search in ry
        # --------------------------------------------------------
        dry_grid = np.linspace(
            -20.0,
            20.0,
            321,
        )

        best = None

        for dry in dry_grid:
            ry_target = (
                float(ref_ry)
                + float(dry)
            )

            result = objective_for_ry(
                q0_target,
                qlab_target,
                T,
                rx_target,
                ry_target,
                ref_rx,
                ref_ry,
                omega_ref,
                c2_ref,
                c2_sign,
            )

            value = result[0]

            if best is None or value < best[0]:
                best = (
                    value,
                    ry_target,
                    result,
                )

        if best is None:
            raise ValueError(
                "Failed to find an initial ry solution."
            )

        ry_target = float(best[1])

        # --------------------------------------------------------
        # one-dimensional refinement
        # --------------------------------------------------------
        step = 0.25

        while step > 1.0e-7:
            current = objective_for_ry(
                q0_target,
                qlab_target,
                T,
                rx_target,
                ry_target,
                ref_rx,
                ref_ry,
                omega_ref,
                c2_ref,
                c2_sign,
            )[0]

            plus_value = objective_for_ry(
                q0_target,
                qlab_target,
                T,
                rx_target,
                ry_target + step,
                ref_rx,
                ref_ry,
                omega_ref,
                c2_ref,
                c2_sign,
            )[0]

            minus_value = objective_for_ry(
                q0_target,
                qlab_target,
                T,
                rx_target,
                ry_target - step,
                ref_rx,
                ref_ry,
                omega_ref,
                c2_ref,
                c2_sign,
            )[0]

            if (
                plus_value < current
                and plus_value <= minus_value
            ):
                ry_target += step

            elif minus_value < current:
                ry_target -= step

            else:
                step *= 0.5

        (
            c2_target,
            omega_target,
            qperp,
            C_rel,
            q_pre,
        ) = solve_c2_for_fixed_tilts(
            q0_target,
            qlab_target,
            T,
            rx_target,
            ry_target,
            ref_rx,
            ref_ry,
            omega_ref,
            c2_ref,
            c2_sign,
        )

        return (
            float(c2_target),
            float(rx_target),
            float(ry_target),
            float(omega_target),
            float(qperp),
            C_rel,
            q_pre,
        )

    # ============================================================
    # 1) Sample information
    # ============================================================
    la = float(txt1.get())
    lb = float(txt2.get())
    lc = float(txt3.get())
    lal = float(txt4.get())
    lbe = float(txt5.get())
    lga = float(txt6.get())

    U_hkl = np.array([
        float(txt9.get()),
        float(txt10.get()),
        float(txt11.get()),
    ], dtype=float)

    V_hkl = np.array([
        float(txt12.get()),
        float(txt13.get()),
        float(txt14.get()),
    ], dtype=float)

    # ============================================================
    # 2) UB matrix and SPICE -> PDF transform
    # ============================================================
    if state['file_paths'] and state['file_paths'][0]:
        with open(
            state['file_paths'][0],
            "r",
            encoding="utf-8",
        ) as f:
            lines = f.readlines()

        try:
            UB_raw = _parse_spice_ub_from_dat(
                state['file_paths'][0]
            )

        except Exception:
            if len(lines) <= 21:
                raise ValueError(
                    "SPICE file does not contain the expected UB line."
                )

            ub_line = lines[21].strip()
            ub_parts = ub_line.split(",")

            if len(ub_parts) < 9:
                raise ValueError(
                    "Could not parse 3x3 UB matrix from the SPICE file."
                )

            first_value = re.sub(
                r"[^\d.eE+\-]",
                "",
                ub_parts[0],
            )

            ub_values = (
                [first_value]
                + [
                    x.strip()
                    for x in ub_parts[1:9]
                ]
            )

            UB_raw = np.array(
                [
                    float(x)
                    for x in ub_values
                ],
                dtype=float,
            ).reshape(3, 3)

        ub_entries = [
            txt_ub_11,
            txt_ub_12,
            txt_ub_13,
            txt_ub_21,
            txt_ub_22,
            txt_ub_23,
            txt_ub_31,
            txt_ub_32,
            txt_ub_33,
        ]

        for entry, value in zip(
            ub_entries,
            UB_raw.reshape(-1),
        ):
            set_entry(
                entry,
                f"{float(value):.6f}",
            )

        # IMPORTANT:
        # revised canonicalizer returns both UB_pdf and T.
        canonicalized = _canonicalize_spice_ub_for_pdf(
            UB_raw,
            U_hkl,
            V_hkl,
        )

        if (
            not isinstance(canonicalized, tuple)
            or len(canonicalized) != 2
        ):
            raise ValueError(
                "_canonicalize_spice_ub_for_pdf() must return "
                "(UB_pdf, spice_to_pdf_transform). "
                "Please use the revised UB conversion helper."
            )

        UB_pdf, spice_to_pdf_transform = canonicalized

        UB_pdf = np.asarray(
            UB_pdf,
            dtype=float,
        )

        spice_to_pdf_transform = np.asarray(
            spice_to_pdf_transform,
            dtype=float,
        )

        ub_source = "SPICE file"

    else:
        # --------------------------------------------------------
        # Simulation mode
        # --------------------------------------------------------
        # _make_simulation_ub_from_lattice_uv() already builds UB in
        # the canonical PDF frame.
        #
        # There is no independently measured raw-SPICE orientation
        # matrix in this branch, so define the synthetic motor frame
        # to coincide with the generated canonical frame.
        UB_pdf = _make_simulation_ub_from_lattice_uv(
            la,
            lb,
            lc,
            lal,
            lbe,
            lga,
            U_hkl,
            V_hkl,
        )

        spice_to_pdf_transform = np.eye(
            3,
            dtype=float,
        )

        ub_entries = [
            txt_ub_11,
            txt_ub_12,
            txt_ub_13,
            txt_ub_21,
            txt_ub_22,
            txt_ub_23,
            txt_ub_31,
            txt_ub_32,
            txt_ub_33,
        ]

        for entry, value in zip(
            ub_entries,
            UB_pdf.reshape(-1),
        ):
            set_entry(
                entry,
                f"{float(value):.6f}",
            )

        UB_raw = None
        ub_source = "lattice + U,V"

    # ============================================================
    # 3) Reference Peak1 input
    # ============================================================
    ref_hkl = np.array([
        float(txt_ref_h.get()),
        float(txt_ref_k.get()),
        float(txt_ref_l.get()),
    ], dtype=float)

    C2_ref = float(
        txt_ref_c2.get()
    )

    A2_ref = float(
        txt_ref_a2.get()
    )

    # SPICE absolute motor readings at Peak1.
    ref_ry = float(
        txt_ref_ry.get()
    )

    ref_rx = float(
        txt_ref_rx.get()
    )

    Ei_ref = float(
        txt_ref_ei.get()
    )

    Ef_ref = float(
        txt_ref_ef.get()
    )

    # Same C2 encoder sense used by the data conversion.
    try:
        c2_sign = float(
            DATA_C2_TO_OMEGA_SIGN
        )
    except NameError:
        c2_sign = +1.0

    # ============================================================
    # 4) Target input
    # ============================================================
    hw_cal = float(
        txt_ubc_0.get()
    )

    target_hkl = np.array([
        float(txt_ubc_1.get()),
        float(txt_ubc_2.get()),
        float(txt_ubc_3.get()),
    ], dtype=float)

    A1_min = float(
        txt_ubc_hl11.get()
    )

    A1_max = float(
        txt_ubc_hl12.get()
    )

    C2_min = float(
        txt_ubc_hl21.get()
    )

    C2_max = float(
        txt_ubc_hl22.get()
    )

    A2_min = float(
        txt_ubc_hl31.get()
    )

    A2_max = float(
        txt_ubc_hl32.get()
    )

    # HODACA fixed-Ef mode.
    Ef = 3.635
    Ei = Ef + hw_cal

    try:
        if Ei <= 0.0:
            raise ValueError(
                f"Ei must be positive: "
                f"Ei={Ei:.6f} meV"
            )

        if Ei_ref <= 0.0 or Ef_ref <= 0.0:
            raise ValueError(
                "Reference Peak1 Ei and Ef must be positive."
            )

        # ========================================================
        # 5) Reference omega calibration
        # ========================================================
        (
            omega_ref,
            q0_ref,
            qlab_ref,
            qlab_ref_calc,
            reference_mismatch,
        ) = calculate_reference_omega(
            UB_pdf,
            ref_hkl,
            A2_ref,
            Ei_ref,
            Ef_ref,
        )

        # At Peak1:
        #
        #   A_target = A_ref
        #       -> C_rel = I
        #
        # therefore absolute Peak1 rx/ry are already included through
        # the relative-rotation definition and are NOT applied again
        # to q0_ref.

        # ========================================================
        # 6) target HKL / hw -> A2
        # ========================================================
        q0_target = (
            2.0
            * math.pi
            * (
                UB_pdf
                @ target_hkl
            )
        )

        qnorm_target = float(
            np.linalg.norm(q0_target)
        )

        if qnorm_target < 1.0e-12:
            raise ValueError(
                "Requested HKL gives zero Q."
            )

        A2 = scattering_angle_from_q(
            qnorm_target,
            Ei,
            Ef,
        )

        qlab_target = q_lab_pdf(
            Ei,
            Ef,
            A2,
        )

        # ========================================================
        # 7) target C2, rx, ry
        # ========================================================
        (
            C2,
            rx_cal,
            ry_cal,
            omega_cal,
            qperp_after_tilt,
            C_rel_cal,
            q_pre_cal,
        ) = solve_target_motors(
            q0_target,
            qlab_target,
            spice_to_pdf_transform,
            C2_ref,
            omega_ref,
            ref_rx,
            ref_ry,
            c2_sign,
        )

        # ========================================================
        # 8) monochromator C1, A1
        # ========================================================
        d = 3.355  # PG(002)

        mono_arg = (
            (2.0 * math.pi / d)
            / (
                2.0
                * math.sqrt(
                    Ei / 2.072
                )
            )
        )

        if (
            mono_arg < -1.0 - 1.0e-10
            or mono_arg > 1.0 + 1.0e-10
        ):
            raise ValueError(
                "Requested Ei is inaccessible for the monochromator."
            )

        C1 = math.degrees(
            math.asin(
                float(
                    np.clip(
                        mono_arg,
                        -1.0,
                        1.0,
                    )
                )
            )
        )

        A1 = 2.0 * C1

        # ========================================================
        # 9) verify target reconstruction
        # ========================================================
        qlab_target_calc = (
            Ry_pdf_deg(omega_cal)
            @ C_rel_cal.T
            @ q0_target
        )

        target_mismatch = float(
            np.linalg.norm(
                qlab_target_calc
                - qlab_target
            )
        )

        target_qnorm = float(
            np.linalg.norm(
                qlab_target
            )
        )

        if target_qnorm > 1.0e-12:
            target_mismatch_percent = (
                target_mismatch
                / target_qnorm
                * 100.0
            )

        else:
            target_mismatch_percent = float(
                "nan"
            )

        # ========================================================
        # 10) output
        # ========================================================
        a1_color = (
            "red"
            if (
                A1 < A1_min
                or A1 > A1_max
            )
            else "black"
        )

        c2_color = (
            "red"
            if (
                C2 < C2_min
                or C2 > C2_max
            )
            else "black"
        )

        a2_color = (
            "red"
            if (
                A2 < A2_min
                or A2 > A2_max
            )
            else "black"
        )

        set_entry(
            txt_ubc_r1,
            f"{C1:.3f}",
            a1_color,
        )

        set_entry(
            txt_ubc_r2,
            f"{A1:.3f}",
            a1_color,
        )

        set_entry(
            txt_ubc_r3,
            f"{C2:.3f}",
            c2_color,
        )

        set_entry(
            txt_ubc_r4,
            f"{A2:.3f}",
            a2_color,
        )

        # Existing GUI order:
        #   r5 = rx
        #   r6 = ry
        set_entry(
            txt_ubc_r5,
            f"{rx_cal:.3f}",
        )

        set_entry(
            txt_ubc_r6,
            f"{ry_cal:.3f}",
        )

        # ========================================================
        # 11) diagnostic messages
        # ========================================================
        reference_qnorm = float(
            np.linalg.norm(
                qlab_ref
            )
        )

        if reference_qnorm > 1.0e-12:
            reference_mismatch_percent = (
                reference_mismatch
                / reference_qnorm
                * 100.0
            )

        else:
            reference_mismatch_percent = float(
                "nan"
            )

        messages = []

        if np.isfinite(
            reference_mismatch_percent
        ):
            if reference_mismatch_percent >= 1.0:
                messages.append(
                    "Reference mismatch: "
                    f"{reference_mismatch_percent:.2f}% "
                    "[WARNING]"
                )

            else:
                messages.append(
                    "Reference mismatch: "
                    f"{reference_mismatch_percent:.2f}%"
                )

        else:
            messages.append(
                "Reference mismatch: unavailable"
            )

        if abs(qperp_after_tilt) > max(
            1.0e-8,
            1.0e-6 * qnorm_target,
        ):
            messages.append(
                "finite Q_perp remains after tilt "
                f"({qperp_after_tilt:.3g} A^-1)"
            )

        if np.isfinite(
            target_mismatch_percent
        ):
            if target_mismatch_percent >= 1.0e-3:
                messages.append(
                    "Target reconstruction mismatch: "
                    f"{target_mismatch_percent:.5f}%"
                )

        lbl_ubc_m2.config(
            text="; ".join(messages)
        )

        # ========================================================
        # 12) diagnostic output
        # ========================================================
        print("================================")
        print("UB source =", ub_source)

        if UB_raw is not None:
            print(
                "SPICE UB raw =\n",
                UB_raw,
            )

        print(
            "UB canonical PDF frame =\n",
            UB_pdf,
        )

        print(
            "SPICE -> PDF transform T =\n",
            spice_to_pdf_transform,
        )

        print(
            "U HKL =",
            U_hkl,
        )

        print(
            "V HKL =",
            V_hkl,
        )

        print("--- reference Peak1 ---")
        print(
            "reference HKL =",
            ref_hkl,
        )
        print(
            "reference C2 =",
            C2_ref,
        )
        print(
            "reference A2 =",
            A2_ref,
        )
        print(
            "reference ry =",
            ref_ry,
        )
        print(
            "reference rx =",
            ref_rx,
        )
        print(
            "reference Ei =",
            Ei_ref,
        )
        print(
            "reference Ef =",
            Ef_ref,
        )
        print(
            "reference omega =",
            omega_ref,
        )
        print(
            "Q0_ref =",
            q0_ref,
        )
        print(
            "Qlab_ref =",
            qlab_ref,
        )
        print(
            "Qlab_ref_calc =",
            qlab_ref_calc,
        )
        print(
            "reference mismatch =",
            reference_mismatch,
        )

        A_ref = spice_raw_tilt_matrix(
            ref_rx,
            ref_ry,
        )

        C_rel_ref = (
            spice_to_pdf_transform
            @ A_ref
            @ A_ref.T
            @ spice_to_pdf_transform.T
        )

        print(
            "C_rel_ref =\n",
            C_rel_ref,
        )

        print("--- target ---")
        print(
            "target HKL =",
            target_hkl,
        )
        print(
            "hw =",
            hw_cal,
        )
        print(
            "target Ei =",
            Ei,
        )
        print(
            "target Ef =",
            Ef,
        )
        print(
            "target A2 =",
            A2,
        )
        print(
            "calculated C2 =",
            C2,
        )
        print(
            "calculated omega =",
            omega_cal,
        )
        print(
            "calculated rx (fixed) =",
            rx_cal,
        )
        print(
            "calculated ry =",
            ry_cal,
        )
        print(
            "C_rel target =\n",
            C_rel_cal,
        )
        print(
            "q_pre target =",
            q_pre_cal,
        )
        print(
            "Qlab_target =",
            qlab_target,
        )
        print(
            "Qlab_target_calc =",
            qlab_target_calc,
        )
        print(
            "Qperp target =",
            qperp_after_tilt,
        )
        print(
            "target mismatch =",
            target_mismatch,
        )
        print(
            "target mismatch percent =",
            target_mismatch_percent,
        )
        print("================================")

    except (
        ValueError,
        np.linalg.LinAlgError,
    ) as exc:
        lbl_ubc_m2.config(
            text=str(exc)
        )

        for entry in [
            txt_ubc_r1,
            txt_ubc_r2,
            txt_ubc_r3,
            txt_ubc_r4,
            txt_ubc_r5,
            txt_ubc_r6,
        ]:
            set_entry(entry)
