"""Compatibility facade for the former monolithic SPICE geometry module."""
from .ub.io import _parse_spice_ub_from_dat
from .ub.transform import _canonicalize_spice_ub_for_pdf
from .geometry.angles import _spice_raw_Rx_deg, _spice_raw_Ry_deg, _data_Ry_deg, _data_Rz_deg, _data_Rx_deg, _rotation_z_deg
from .geometry.tilt import _spice_tilt_matrix_raw, _spice_relative_tilt_in_pdf
from .geometry.q_vectors import _data_q_lab
from .geometry.reference import DATA_C2_TO_OMEGA_SIGN, _calculate_data_reference_omega
from .geometry.conversion import _angles_to_hkl_and_uv
