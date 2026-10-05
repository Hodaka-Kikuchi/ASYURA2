"""UB coordinate-frame transformations."""
import numpy as np

def _canonicalize_spice_ub_for_pdf(UB, u_hkl, v_hkl):
    """
    Convert raw SPICE UB to the canonical PDF frame.

    The physical scattering-plane normal is kept independent of
    the order of entered U and V.

        entered U                         -> +z
        in-plane direction perpendicular U -> +x
        scattering-plane normal          -> +y

    U and V do not need to be orthogonal.
    """

    UB = np.asarray(UB, dtype=float)
    U = np.asarray(u_hkl, dtype=float)
    V = np.asarray(v_hkl, dtype=float)

    if np.linalg.norm(U) < 1.0e-12 or np.linalg.norm(V) < 1.0e-12:
        raise ValueError(
            "U and V must be non-zero reciprocal-space directions."
        )

    q_u = UB @ U
    q_v = UB @ V

    n_u = np.linalg.norm(q_u)

    if n_u < 1.0e-12:
        raise ValueError(
            "U vector gives zero reciprocal-space vector."
        )

    # U direction
    e1 = q_u / n_u

    # ------------------------------------------------------------
    # Scattering-plane normal
    # ------------------------------------------------------------
    normal = np.cross(q_u, q_v)

    n_normal = np.linalg.norm(normal)

    if n_normal < 1.0e-12:
        raise ValueError(
            "U and V must define a non-degenerate scattering plane."
        )

    # Raw SPICE convention used here:
    # keep the physical vertical direction on the +z side.
    raw_vertical = np.array(
        [0.0, 0.0, 1.0],
        dtype=float
    )

    if np.dot(normal, raw_vertical) < 0.0:
        normal = -normal

    e3 = normal / np.linalg.norm(normal)

    # Fixed physical handedness.
    e2 = np.cross(e3, e1)
    e2 /= np.linalg.norm(e2)

    # Source orthonormal frame in raw SPICE coordinates
    T_spice = np.column_stack(
        (e1, e2, e3)
    )

    # PDF frame:
    # e1 -> +z
    # e2 -> +x
    # e3 -> +y
    T_pdf = np.array([
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0],
    ], dtype=float)

    transform = T_pdf @ T_spice.T

    UB_pdf = transform @ UB

    # Keep the same coordinate transformation for the SPICE goniometer axes.
    # A rotation defined in the raw SPICE Cartesian frame must be conjugated
    # by this transform before it can act in the canonical PDF frame.
    return UB_pdf, transform
