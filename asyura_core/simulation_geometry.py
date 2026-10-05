"""Compatibility facade for the former monolithic simulation geometry module."""
from .ub.construction import _make_B_from_lattice_for_simulation, _make_simulation_ub_from_lattice_uv
from .geometry.angles import _normalize_simu_angle_deg, _simu_Ry_deg
from .geometry.q_vectors import _simu_q_lab
from .geometry.reference import SIMU_C2_TO_OMEGA_SIGN, _calculate_simu_reference_omega
from .geometry.conversion import _simu_hkl_text, _simu_angles_to_rlu
