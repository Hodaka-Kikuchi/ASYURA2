"""Reciprocal-plane display basis helpers."""
import math
import numpy as np

def _find_simple_orthogonal_inplane_hkl(
    UB,
    u_hkl,
    v_hkl,
    max_coeff=3,
    max_complexity=3,
    angle_tol_deg=0.05
):
    u_hkl = np.asarray(u_hkl, dtype=float)
    v_hkl = np.asarray(v_hkl, dtype=float)

    q_u = np.asarray(UB, dtype=float) @ u_hkl
    q_v0 = np.asarray(UB, dtype=float) @ v_hkl

    nu = np.linalg.norm(q_u)
    nv0 = np.linalg.norm(q_v0)

    if nu == 0 or nv0 == 0:
        raise ValueError("U and V must be non-zero vectors.")

    cos_tol = np.sin(np.radians(angle_tol_deg))

    # ------------------------------------------------------------
    # 入力VがすでにUと直交しているか確認
    # ------------------------------------------------------------
    cos0 = float(
        np.dot(q_u, q_v0) / (nu * nv0)
    )

    if abs(cos0) <= cos_tol:
        return v_hkl.copy(), True, (0, 1)


    best = None

    # ------------------------------------------------------------
    # 単純な整数結合だけ探索
    # ------------------------------------------------------------
    for p in range(-max_coeff, max_coeff + 1):
        for q in range(-max_coeff, max_coeff + 1):

            if p == 0 and q == 0:
                continue

            # 高次すぎる方向を除外
            complexity = abs(p) + abs(q)

            if complexity > max_complexity:
                continue

            cand = p * u_hkl + q * v_hkl

            if np.linalg.norm(cand) == 0:
                continue

            q_cand = np.asarray(UB, dtype=float) @ cand
            nc = np.linalg.norm(q_cand)

            if nc == 0:
                continue

            cosang = float(
                np.dot(q_u, q_cand) / (nu * nc)
            )

            # Uと十分直交していないものは除外
            if abs(cosang) > cos_tol:
                continue

            # 元のVと同じ側を優先
            orient_penalty = (
                0 if np.dot(q_cand, q_v0) > 0 else 1
            )

            score = (
                orient_penalty,
                complexity,
                abs(cosang),
            )

            if best is None or score < best[0]:
                best = (
                    score,
                    cand.copy(),
                    (p, q)
                )


    # ------------------------------------------------------------
    # 単純な直交HKLが見つからなかった
    # → monoclinic等では元のVをそのまま使う
    # ------------------------------------------------------------
    if best is None:
        return v_hkl.copy(), False, None

    return best[1], True, best[2]

def _make_crystallographic_display_basis(UB, u_hkl, v_hkl, hex_angle_tol_deg=1.0):
    """
    Build the display basis used for measured single-crystal data.

    Policy:
      * If entered U,V are already physically orthogonal, keep them.
      * Only for a hexagonal/triangular-like in-plane angle (about 60 or 120 deg),
        try to replace V by a simple integer combination perpendicular to U
        (e.g. (010) -> (-120) for U=(100)).
      * Otherwise, especially for monoclinic geometry, NEVER replace V.
        Keep the entered non-orthogonal U,V and render their coefficients on
        perpendicular screen axes.

    q_u and q_v returned here are the actual physical reciprocal vectors
    2*pi*UB@HKL, not unit vectors.
    """
    UB = np.asarray(UB, dtype=float)
    u_hkl = np.asarray(u_hkl, dtype=float)
    v_hkl = np.asarray(v_hkl, dtype=float)

    q_u0 = UB @ u_hkl
    q_v0 = UB @ v_hkl
    nu0 = np.linalg.norm(q_u0)
    nv0 = np.linalg.norm(q_v0)

    if nu0 == 0 or nv0 == 0:
        raise ValueError("U and V must be non-zero vectors.")
    if np.linalg.norm(np.cross(q_u0, q_v0)) < 1e-12:
        raise ValueError("U and V must define a scattering plane (they cannot be parallel).")

    entered_angle = math.degrees(math.acos(np.clip(
        np.dot(q_u0, q_v0) / (nu0 * nv0), -1.0, 1.0
    )))

    # Default: preserve the entered crystallographic V exactly.
    v_used = v_hkl.copy()
    has_simple_orthogonal = False
    coeff = None

    # If U,V are already orthogonal, there is nothing to change.
    if abs(entered_angle - 90.0) <= 0.05:
        has_simple_orthogonal = True
        coeff = (0, 1)

    # Automatic integer-axis replacement is intentionally restricted to
    # hexagonal/triangular-like geometry.  This prevents monoclinic U,V from
    # being replaced by accidental high/small-order near-orthogonal vectors.
    elif (abs(entered_angle - 60.0) <= hex_angle_tol_deg or
          abs(entered_angle - 120.0) <= hex_angle_tol_deg):
        v_candidate, found, candidate_coeff = _find_simple_orthogonal_inplane_hkl(
            UB, u_hkl, v_hkl
        )
        if found:
            v_used = v_candidate
            has_simple_orthogonal = True
            coeff = candidate_coeff

    # Physical reciprocal vectors in A^-1.
    q_u = 2.0 * math.pi * (UB @ u_hkl)
    q_v = 2.0 * math.pi * (UB @ v_used)
    nu = np.linalg.norm(q_u)
    nv = np.linalg.norm(q_v)

    normal = np.cross(q_u, q_v)
    nn = np.linalg.norm(normal)
    if nn < 1e-12:
        raise ValueError("Display U and V are parallel or nearly parallel.")
    normal /= nn

    used_angle = math.degrees(math.acos(np.clip(
        np.dot(q_u, q_v) / (nu * nv), -1.0, 1.0
    )))

    if has_simple_orthogonal:
        mode = "orthogonal-crystallographic"
    else:
        mode = "oblique-as-rectangular"

    return q_u, q_v, normal, nu, nv, entered_angle, used_angle, v_used, mode, coeff

def _display_uv_to_hkl(display_xy, u_hkl, v_hkl, nu, nv):
    """
    Convert stored single-crystal display coordinates back to HKL.

        X = alpha*nu
        Y = beta*nv

    so
        HKL = (X/nu)*U + (Y/nv)*V.
    """
    X, Y = np.asarray(display_xy, dtype=float)
    U = np.asarray(u_hkl, dtype=float)
    V = np.asarray(v_hkl, dtype=float)

    nu = float(nu)
    nv = float(nv)

    if nu == 0.0 or nv == 0.0:
        return np.full(3, np.nan)

    alpha = X / nu
    beta  = Y / nv

    return alpha * U + beta * V
