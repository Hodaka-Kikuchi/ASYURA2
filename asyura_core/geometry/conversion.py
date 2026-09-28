"""Motor-angle to reciprocal-space conversion."""
import math
import numpy as np
from .angles import _data_Ry_deg, _simu_Ry_deg
from .q_vectors import _data_q_lab, _simu_q_lab
from .tilt import _spice_relative_tilt_in_pdf

DATA_C2_TO_OMEGA_SIGN = +1.0
SIMU_C2_TO_OMEGA_SIGN = +1.0

def _rotation_z_deg(angle_deg):
    """
    Right-handed rotation about +z.

    Existing HODACA convention:
        ki direction at C2=0 : +x
        detector rotation    : -A2
        sample rotation      : +C2
    """
    a = math.radians(float(angle_deg))
    c = math.cos(a)
    s = math.sin(a)

    return np.array([
        [c, -s, 0.0],
        [s,  c, 0.0],
        [0.0, 0.0, 1.0],
    ], dtype=float)

def _angles_to_hkl_and_uv(
    ei_meV,
    ef_meV,
    c2_deg,
    a2_deg,
    is_single_crystal,
    UB=None,
    u_hkl=None,
    v_hkl=None,
    ref_c2=None,
    omega_ref=None,
    c2_sign=+1.0,
    *,
    ry_deg=None,
    rx_deg=None,
    ref_ry=None,
    ref_rx=None,
    spice_to_pdf_transform=None,
):
    """
    Convert one measured detector point to display coordinates.

    Powder:
        Preserve the historical HODACA 2-D Q convention.

    Single crystal:
        Use the same PDF UB geometry as the corrected simulation:

            Q_lab = (-kf*sin(A2), 0, ki-kf*cos(A2))

            omega = omega_ref
                    + c2_sign * (C2 - ref_c2)

            C_rel = T @ A(rx_data, ry_data)
                      @ A(rx_ref, ry_ref).T @ T.T

            Q0 = C_rel @ Ry(omega).T @ Q_lab

        where A(rx,ry) is the ordered absolute SPICE tilt rotation in the
        raw SPICE Cartesian frame.

        where Rz_SPICE(mu) = Rz_PDF(-mu).

        The RAW SPICE motor readings are passed to this function:

            ry_deg = measured SPICE ry
            rx_deg = measured SPICE rx

        together with the Reference Peak1 motor readings:

            ref_ry = Reference Peak1 ry
            ref_rx = Reference Peak1 rx

        The effective rotation angles are calculated here:

            mu_eff = ry_deg - ref_ry
            nu_eff = rx_deg - ref_rx

        with

            SPICE ry -> Mantid/PDF mu
            SPICE rx -> Mantid/PDF nu

        Therefore changing only ref_ry/ref_rx changes the reciprocal-space
        conversion even though the measured ry/rx values themselves remain
        unchanged.

            HKL = UB^-1 @ Q0 / (2*pi)

        Then decompose

            HKL = alpha*U + beta*V

        and retain the historical display scale

            X = alpha * |2*pi*UB*U|
            Y = beta  * |2*pi*UB*V|

        so existing plotting / HKL-box code keeps the same units.
    """
    ei_meV = float(ei_meV)
    ef_meV = float(ef_meV)

    if ei_meV <= 0.0 or ef_meV <= 0.0:
        raise ValueError(
            f"Neutron energy must be positive: Ei={ei_meV}, Ef={ef_meV}"
        )

    # ------------------------------------------------------------
    # Powder: preserve old behavior exactly.
    # ------------------------------------------------------------
    if not is_single_crystal:
        ki_mag = math.sqrt(ei_meV / 2.072)
        kf_mag = math.sqrt(ef_meV / 2.072)

        ki0 = np.array([ki_mag, 0.0, 0.0], dtype=float)
        kf0 = _rotation_z_deg(-float(a2_deg)) @ np.array(
            [kf_mag, 0.0, 0.0],
            dtype=float
        )

        q_c2_zero = ki0 - kf0
        q_sample = _rotation_z_deg(float(c2_deg)) @ q_c2_zero

        return q_sample[:2].copy(), q_sample, None, 0.0

    # ------------------------------------------------------------
    # Single crystal: PDF Q_lab + inverse sample rotation.
    # ------------------------------------------------------------
    if UB is None or u_hkl is None or v_hkl is None:
        raise ValueError("UB, U and V are required for single-crystal data.")

    if ref_c2 is None or omega_ref is None:
        raise ValueError(
            "ref_c2 and omega_ref are required for single-crystal data."
        )

    if ry_deg is None or rx_deg is None:
        raise ValueError(
            "Measured SPICE ry and rx are required for single-crystal data."
        )
    if ref_ry is None or ref_rx is None:
        raise ValueError(
            "Reference Peak1 ry and rx are required for single-crystal data."
        )
    if spice_to_pdf_transform is None:
        raise ValueError(
            "The raw-SPICE -> PDF coordinate transform is required for "
            "single-crystal tilt correction."
        )

    # ------------------------------------------------------------
    # Absolute SPICE tilt motor readings.
    #
    # Do NOT form independent PDF-frame rotations from
    #     ry_data - ref_ry, rx_data - ref_rx.
    # After UB is canonicalized, the SPICE motor axes themselves must be
    # transported by the same coordinate transform T.  The finite relative
    # rotation is therefore built in raw SPICE coordinates first.
    # ------------------------------------------------------------
    ry_data = float(ry_deg)
    rx_data = float(rx_deg)
    ry_zero = float(ref_ry)
    rx_zero = float(ref_rx)

    UB = np.asarray(UB, dtype=float)
    U = np.asarray(u_hkl, dtype=float)
    V = np.asarray(v_hkl, dtype=float)

    #ref_a2 = float(txt_ref_a2.get())
    #ref_ei = float(txt_ref_ei.get())
    #ref_ef = float(txt_ref_ef.get())


    q_lab = _data_q_lab(
        ei_meV,
        ef_meV,
        a2_deg,
    )

    omega = (
        float(omega_ref)
        + float(c2_sign) * (
            float(c2_deg) - float(ref_c2)
        )
    )

    Ry = _data_Ry_deg(omega)

    # Relative tilt in the canonical PDF frame:
    #
    #     A(rx, ry) = Rx_raw(-ry) @ Ry_raw(-rx)
    #
    #     C_rel = T @ A(rx_data, ry_data)
    #               @ A(rx_ref,  ry_ref).T @ T.T
    #
    # This is the finite-rotation form of updating the tilted axes.  It
    # automatically includes the fact that the axes after the first tilt are
    # no longer identical to the original fixed PDF x/y/z axes.
    C_rel = _spice_relative_tilt_in_pdf(
        rx_data,
        ry_data,
        rx_zero,
        ry_zero,
        spice_to_pdf_transform,
    )

    # Undo omega first, then apply the Peak1-referenced SPICE tilt relation.
    # This follows the experimentally validated SPICE -> saved-HKL mapping.
    q0 = C_rel @ Ry.T @ q_lab

    hkl = np.linalg.solve(
        UB,
        q0 / (2.0 * math.pi)
    )

    # HKL = alpha*U + beta*V
    uv_basis = np.column_stack((U, V))
    coeff, _, _, _ = np.linalg.lstsq(
        uv_basis,
        hkl,
        rcond=None
    )
    alpha, beta = coeff

    hkl_in_plane = alpha * U + beta * V
    residual = float(
        np.linalg.norm(hkl - hkl_in_plane)
    )

    # Preserve Qvector display scale [A^-1].
    qU = 2.0 * math.pi * (UB @ U)
    qV = 2.0 * math.pi * (UB @ V)

    NU = np.linalg.norm(qU)
    NV = np.linalg.norm(qV)

    if NU == 0.0 or NV == 0.0:
        raise ValueError("U or V reciprocal vector has zero length.")

    display_xy = np.array([
        alpha * NU,
        beta  * NV,
    ], dtype=float)

    return display_xy, q_lab, hkl, residual

def _simu_hkl_text(vec):
    vals = np.asarray(vec, dtype=float)
    def f(x):
        if abs(x - round(x)) < 1e-10:
            return str(int(round(x)))
        return f"{x:.6g}"
    return "(" + ",".join(f(x) for x in vals) + ")"

def _simu_angles_to_rlu(
    ei_meV,
    ef_meV,
    c2_deg,
    a2_deg,
    UB,
    u_hkl,
    v_hkl,
    nu,
    nv,
    ref_c2,
    omega_ref,
    c2_sign,
):
    """
    Convert simulated instrument angles to crystallographic U,V coordinates
    using the PDF UB convention.

    1) Build Q_lab from Ei, Ef and detector A2:
           Q_lab = (-kf*sin(A2), 0, ki-kf*cos(A2))

    2) Convert the instrument C2 encoder to the physical sample rotation:
           omega = omega_ref + c2_sign * (C2 - ref_c2)

    3) Undo the sample rotation:
           Q0 = R_y(omega)^T @ Q_lab

    4) Convert to HKL:
           HKL = solve(UB, Q0/(2*pi))

    5) Decompose HKL on the displayed crystallographic U,V axes.

    No direct Rz(C2) rotation of Q is used.
    """
    UB = np.asarray(UB, dtype=float)
    u_hkl = np.asarray(u_hkl, dtype=float)
    v_hkl = np.asarray(v_hkl, dtype=float)

    q_lab = _simu_q_lab(
        ei_meV,
        ef_meV,
        a2_deg,
    )

    omega_deg = (
        float(omega_ref)
        + float(c2_sign) * (
            float(c2_deg) - float(ref_c2)
        )
    )

    R = _simu_Ry_deg(omega_deg)

    # R is orthogonal, so inverse(R) = R.T
    q0 = R.T @ q_lab

    hkl = np.linalg.solve(
        UB,
        q0 / (2.0 * np.pi)
    )

    uv_basis = np.column_stack(
        (u_hkl, v_hkl)
    )

    coeff = np.linalg.lstsq(
        uv_basis,
        hkl,
        rcond=None
    )[0]

    alpha = float(coeff[0])
    beta  = float(coeff[1])

    residual = float(
        np.linalg.norm(
            hkl
            - alpha * u_hkl
            - beta  * v_hkl
        )
    )

    return alpha, beta, q_lab, hkl, residual
