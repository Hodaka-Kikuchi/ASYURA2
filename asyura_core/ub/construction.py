"""Construct B/UB matrices from lattice parameters and scattering-plane directions."""
import math
import numpy as np

def make_B_from_lattice(a, b, c, alpha, beta, gamma):
    """
    lattice parameters から B matrix を作る。

    ここで返す B は SPICE と同じく 2*pi を含まない convention:
        q [A^-1] = 2*pi * B @ hkl
    """

    alpha = np.radians(alpha)
    beta  = np.radians(beta)
    gamma = np.radians(gamma)

    # direct lattice vectors [A]
    avec = np.array([
        a,
        0.0,
        0.0
    ], dtype=float)

    bvec = np.array([
        b * np.cos(gamma),
        b * np.sin(gamma),
        0.0
    ], dtype=float)

    cx = c * np.cos(beta)

    cy = c * (
        np.cos(alpha)
        - np.cos(beta) * np.cos(gamma)
    ) / np.sin(gamma)

    cz2 = c**2 - cx**2 - cy**2

    # 数値丸めで非常に小さな負値になった場合を救済
    if cz2 < 0 and abs(cz2) < 1.0e-12:
        cz2 = 0.0

    if cz2 < 0:
        raise ValueError(
            "Invalid lattice parameters: c-axis z component becomes imaginary."
        )

    cvec = np.array([
        cx,
        cy,
        np.sqrt(cz2)
    ], dtype=float)

    volume = np.dot(avec, np.cross(bvec, cvec))

    if abs(volume) < 1.0e-12:
        raise ValueError("Invalid lattice parameters: unit-cell volume is zero.")

    # reciprocal vectors WITHOUT 2*pi
    astar = np.cross(bvec, cvec) / volume
    bstar = np.cross(cvec, avec) / volume
    cstar = np.cross(avec, bvec) / volume

    # columns are a*, b*, c*
    B = np.column_stack((astar, bstar, cstar))

    return B

def make_ub_from_lattice_uv(
    a, b, c, alpha, beta, gamma,
    u_hkl, v_hkl
):
    """
    lattice parameters + scattering-plane U,V から
    simulation 用 UB を作る。

    重要:
        scattering-plane normal の向きは
        entered U,V の順序に依存させない。

    これにより

        U=(100), V=(001)

    と

        U=(001), V=(100)

    で U-V plane の物理的な normal が反転しない。

    PDF frame:
        entered U                           -> +z
        in-plane direction perpendicular U -> +x or -x
        fixed scattering-plane normal       -> +y

    convention:
        Q = 2*pi * UB @ HKL
    """

    B = make_B_from_lattice(
        a, b, c,
        alpha, beta, gamma
    )

    U = np.asarray(u_hkl, dtype=float)
    V = np.asarray(v_hkl, dtype=float)

    if np.linalg.norm(U) < 1.0e-12:
        raise ValueError("U vector must not be zero.")

    if np.linalg.norm(V) < 1.0e-12:
        raise ValueError("V vector must not be zero.")

    q_u = B @ U
    q_v = B @ V

    n_u = np.linalg.norm(q_u)
    n_v = np.linalg.norm(q_v)

    if n_u < 1.0e-12:
        raise ValueError(
            "U vector gives zero reciprocal-space vector."
        )

    if n_v < 1.0e-12:
        raise ValueError(
            "V vector gives zero reciprocal-space vector."
        )

    # ------------------------------------------------------------
    # entered U direction
    # ------------------------------------------------------------
    e1 = q_u / n_u

    # ------------------------------------------------------------
    # Build a canonical plane normal independent of U/V order.
    #
    # First remove the arbitrary sign of each crystallographic
    # direction only for determining the plane-normal convention.
    #
    # Example:
    #     (100),(001)
    # and
    #     (001),(100)
    #
    # both give the same canonical ordered pair:
    #     (100),(001)
    # ------------------------------------------------------------
    def canonical_direction(vec):

        w = np.asarray(vec, dtype=float).copy()

        for x in w:
            if abs(x) > 1.0e-12:
                if x < 0.0:
                    w = -w
                break

        return w

    Uc = canonical_direction(U)
    Vc = canonical_direction(V)

    # Deterministic crystallographic ordering.
    #
    # Reverse lexicographic ordering means, for example,
    #
    #     (100) before (001)
    #
    # regardless of the order entered in the GUI.
    key_u = tuple(np.round(Uc, 12))
    key_v = tuple(np.round(Vc, 12))

    if key_u >= key_v:
        first_hkl  = Uc
        second_hkl = Vc
    else:
        first_hkl  = Vc
        second_hkl = Uc

    q_first  = B @ first_hkl
    q_second = B @ second_hkl

    fixed_normal = np.cross(
        q_first,
        q_second
    )

    n_fixed = np.linalg.norm(fixed_normal)

    if n_fixed < 1.0e-12:
        raise ValueError(
            "U and V must define a non-degenerate scattering plane."
        )

    fixed_normal /= n_fixed

    # ------------------------------------------------------------
    # Actual entered U,V cross product.
    #
    # Use only its plane information.
    # Its sign is forced to agree with fixed_normal.
    # ------------------------------------------------------------
    normal = np.cross(
        q_u,
        q_v
    )

    n_normal = np.linalg.norm(normal)

    if n_normal < 1.0e-12:
        raise ValueError(
            "U and V must not be parallel. "
            "Two independent scattering-plane vectors are required."
        )

    if np.dot(normal, fixed_normal) < 0.0:
        normal = -normal

    e3 = normal / np.linalg.norm(normal)

    # ------------------------------------------------------------
    # In-plane transverse direction.
    #
    # Because e3 is fixed independently of U/V order,
    # swapping U,V no longer reverses the physical handedness.
    # ------------------------------------------------------------
    e2 = np.cross(
        e3,
        e1
    )

    n_e2 = np.linalg.norm(e2)

    if n_e2 < 1.0e-12:
        raise ValueError(
            "Failed to construct in-plane direction."
        )

    e2 /= n_e2

    # ------------------------------------------------------------
    # Crystal Cartesian orthonormal frame
    # ------------------------------------------------------------
    T_crystal = np.column_stack(
        (
            e1,
            e2,
            e3
        )
    )

    # ------------------------------------------------------------
    # PDF laboratory frame
    #
    # e1 -> +z
    # e2 -> +x
    # e3 -> +y
    # ------------------------------------------------------------
    T_pdf = np.array(
        [
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
            [1.0, 0.0, 0.0],
        ],
        dtype=float
    )

    transform = T_pdf @ T_crystal.T

    UB = transform @ B

    return UB

_make_B_from_lattice_for_simulation = make_B_from_lattice
_make_simulation_ub_from_lattice_uv = make_ub_from_lattice_uv
