"""SPICE/HODACA tilt-motor geometry."""
import numpy as np
from .angles import _spice_raw_Rx_deg, _spice_raw_Ry_deg

def _spice_tilt_matrix_raw(rx_deg, ry_deg):
    """
    Absolute SPICE tilt orientation in the raw SPICE Cartesian frame.

    The motor convention used for the measured data is

        A(rx, ry) = Rx_raw(-ry) @ Ry_raw(-rx)

    Keeping the product in the raw frame is important: the second rotation
    is not replaced by a fixed PDF-axis rotation after UB canonicalization.
    """
    return (
        _spice_raw_Rx_deg(-float(ry_deg))
        @ _spice_raw_Ry_deg(-float(rx_deg))
    )

def _spice_relative_tilt_in_pdf(
    rx_deg, ry_deg, ref_rx, ref_ry, spice_to_pdf_transform
):
    """
    Relative sample tilt from Peak1 to the measured point, expressed in PDF.

        C_rel = T @ A(data) @ A(ref).T @ T.T

    This transports both the SPICE motor axes and their ordered finite
    rotations into the canonical PDF coordinate system.
    """
    T = np.asarray(spice_to_pdf_transform, dtype=float)
    if T.shape != (3, 3):
        raise ValueError("spice_to_pdf_transform must be a 3x3 matrix.")

    A_data = _spice_tilt_matrix_raw(rx_deg, ry_deg)
    A_ref = _spice_tilt_matrix_raw(ref_rx, ref_ry)
    return T @ A_data @ A_ref.T @ T.T
