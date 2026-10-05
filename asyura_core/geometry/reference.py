"""Reference-Bragg orientation calculations."""
import math
import numpy as np
from .angles import _normalize_angle_deg, _data_Ry_deg, _normalize_simu_angle_deg, _simu_Ry_deg
from .q_vectors import _data_q_lab, _simu_q_lab

DATA_C2_TO_OMEGA_SIGN = +1.0
SIMU_C2_TO_OMEGA_SIGN = +1.0

def _calculate_data_reference_omega(
    UB_pdf,
    ref_hkl,
    ref_c2,
    ref_a2,
    ref_ei,
    ref_ef,
):
    """
    Determine omega_ref from Reference Peak1.

    The canonical reciprocal-space frame is defined at Reference Peak1.
    Therefore the effective tilt angles at the reference are

        mu_ref_eff = ry_ref - ry_ref = 0
        nu_ref_eff = rx_ref - rx_ref = 0

    and the reference condition is

        Q_lab_ref = Ry(omega_ref) @ Q0_ref

        Q0_ref = 2*pi*UB_pdf@HKL_ref.

    Unlike ry and rx, the C2 encoder value itself is not the omega
    offset.  omega_ref must be obtained from UB and the Bragg geometry.

    After omega_ref has been determined,

        omega = omega_ref + c2_sign*(C2 - C2_ref).
    """
    UB_pdf = np.asarray(UB_pdf, dtype=float)
    hkl = np.asarray(ref_hkl, dtype=float)

    q0 = 2.0 * math.pi * (UB_pdf @ hkl)
    qnorm = np.linalg.norm(q0)

    if qnorm < 1.0e-12:
        raise ValueError("Reference HKL gives zero Q.")

    qlab = _data_q_lab(
        ref_ei,
        ref_ef,
        ref_a2,
    )

    # Reference Peak1 has zero effective rx/ry tilt by definition.
    # Ry rotates only the x-z components.
    phi_lab = math.degrees(
        math.atan2(qlab[0], qlab[2])
    )
    phi_zero = math.degrees(
        math.atan2(q0[0], q0[2])
    )

    omega_ref = _normalize_angle_deg(
        phi_lab - phi_zero
    )

    qlab_ref_calc = (
        _data_Ry_deg(omega_ref)
        @ q0
    )

    reference_mismatch = float(
        np.linalg.norm(qlab_ref_calc - qlab)
    )

    qlab_norm = float(np.linalg.norm(qlab))
    if qlab_norm > 1.0e-12:
        reference_mismatch_percent = (
            reference_mismatch / qlab_norm * 100.0
        )
    else:
        reference_mismatch_percent = float("nan")

    print("================================")
    print("data reference HKL =", hkl)
    print("reference C2       =", float(ref_c2))
    print("reference A2       =", float(ref_a2))
    print("reference Ei       =", float(ref_ei))
    print("reference Ef       =", float(ref_ef))
    print("Q0_ref             =", q0)
    print("Qlab_ref           =", qlab)
    print("Qlab_ref_calc      =", qlab_ref_calc)
    print("omega_ref          =", omega_ref)
    print(
        "reference mismatch = "
        f"{reference_mismatch:.6g} A^-1 "
        f"({reference_mismatch_percent:.4f}%)"
    )
    print("================================")

    return omega_ref

def _calculate_simu_reference_omega(
    UB,
    ref_hkl,
    ref_c2,
    energy_meV=3.635,
):
    """
    Calibrate the absolute relation between instrument C2 and physical omega
    from one elastic reference reflection.

    The reference scattering angle is obtained from |Q_ref|, then the PDF
    single-vertical-axis relation is used:

        omega_ref
          = atan2(Qlab_x, Qlab_z)
          - atan2(Q0_x,   Q0_z)

    where

        Q0   = 2*pi*UB@ref_hkl
        Qlab = R_y(omega_ref) Q0

    This removes the old ad-hoc C2-offset geometry and does not require the
    reference reflection to be parallel to U.
    """
    UB = np.asarray(UB, dtype=float)
    ref_hkl = np.asarray(ref_hkl, dtype=float)

    q0 = 2.0 * np.pi * (UB @ ref_hkl)
    qnorm = np.linalg.norm(q0)

    if qnorm < 1.0e-12:
        raise ValueError("Reference HKL gives zero Q.")

    # With the simulation UB constructed from U,V, an in-plane reference
    # must have essentially zero laboratory-y component.
    if abs(q0[1]) > max(1.0e-8, 1.0e-6 * qnorm):
        raise ValueError(
            "Reference HKL is outside the requested simulation scattering "
            f"plane: Q0_y={q0[1]:.6g} A^-1."
        )

    k = math.sqrt(float(energy_meV) / 2.072)
    arg = qnorm / (2.0 * k)

    if arg > 1.0 + 1.0e-10:
        raise ValueError(
            f"Reference HKL is inaccessible at {energy_meV} meV: "
            f"|Q|={qnorm:.6f} A^-1, 2k={2.0*k:.6f} A^-1"
        )

    theta = math.asin(float(np.clip(arg, -1.0, 1.0)))
    ref_a2_deg = math.degrees(2.0 * theta)

    qlab_ref = _simu_q_lab(
        energy_meV,
        energy_meV,
        ref_a2_deg,
    )

    phi_lab = math.degrees(
        math.atan2(qlab_ref[0], qlab_ref[2])
    )
    phi_zero = math.degrees(
        math.atan2(q0[0], q0[2])
    )

    omega_ref = _normalize_simu_angle_deg(
        phi_lab - phi_zero
    )

    print("================================")
    print("simulation reference HKL =", ref_hkl)
    print("reference C2             =", float(ref_c2))
    print("reference A2             =", ref_a2_deg)
    print("reference Q0             =", q0)
    print("reference Qlab           =", qlab_ref)
    print("omega_ref                =", omega_ref)
    print("C2 -> omega sign         =", SIMU_C2_TO_OMEGA_SIGN)
    print("================================")

    return omega_ref, ref_a2_deg
