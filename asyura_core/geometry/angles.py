"""Angle normalization and elementary rotation matrices."""
import math
import numpy as np

def _normalize_angle_deg(angle):
    """Angle in degrees -> [-180, 180)."""
    return (float(angle) + 180.0) % 360.0 - 180.0

def _spice_raw_Rx_deg(angle_deg):
    """Right-handed rotation about raw SPICE +x."""
    a = math.radians(float(angle_deg))
    c = math.cos(a)
    s = math.sin(a)
    return np.array([
        [1.0, 0.0, 0.0],
        [0.0,   c,  -s],
        [0.0,   s,   c],
    ], dtype=float)

def _spice_raw_Ry_deg(angle_deg):
    """Right-handed rotation about raw SPICE +y."""
    a = math.radians(float(angle_deg))
    c = math.cos(a)
    s = math.sin(a)
    return np.array([
        [ c, 0.0,  s],
        [0.0, 1.0, 0.0],
        [-s, 0.0,  c],
    ], dtype=float)

def _data_Ry_deg(omega_deg):
    """
    Right-handed sample rotation about laboratory +y.

    PDF convention:
        +z : incident beam
        +y : vertical goniometer axis
        +x : horizontal transverse direction
    """
    w = math.radians(float(omega_deg))
    c = math.cos(w)
    s = math.sin(w)

    return np.array([
        [ c, 0.0,  s],
        [0.0, 1.0, 0.0],
        [-s, 0.0,  c],
    ], dtype=float)

def _data_Rz_deg(mu_deg):
    """
    Mu rotation using the SPICE motor sign convention.

    SPICE:
        ry -> Mantid/PDF mu

    The SPICE ry motor has the opposite positive direction to the
    right-handed PDF/Mantid Rz rotation.  Therefore

        Rz_SPICE(mu) = Rz_PDF(mu)

    In this data-processing code mu is the angle relative to
    Reference Peak1:

        mu = ry_point - ry_ref
    """
    a = math.radians(float(mu_deg))
    c = math.cos(a)
    s = math.sin(a)

    return np.array([
        [ c, -s, 0.0],
        [ s,  c, 0.0],
        [0.0, 0.0, 1.0],
    ], dtype=float)

def _data_Rx_deg(nu_deg):
    """
    Right-handed Rx(nu) rotation used in the PDF/Mantid convention.

    SPICE:
        rx -> Mantid/PDF nu
        すなわち右手系を保とうと思うと符号が逆になる。

    In this data-processing code nu is the angle relative to
    Reference Peak1:

        nu = rx_point - rx_ref
    """
    a = math.radians(float(-nu_deg))
    c = math.cos(a)
    s = math.sin(a)

    return np.array([
        [1.0, 0.0, 0.0],
        [0.0,  c, -s],
        [0.0,  s,  c],
    ], dtype=float)

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

def _normalize_simu_angle_deg(angle_deg):
    return (float(angle_deg) + 180.0) % 360.0 - 180.0

def _simu_Ry_deg(omega_deg):
    """Right-handed rotation about laboratory +y, as in the UB PDF."""
    w = math.radians(float(omega_deg))
    c = math.cos(w)
    s = math.sin(w)

    return np.array([
        [ c, 0.0,  s],
        [0.0, 1.0, 0.0],
        [-s, 0.0,  c],
    ], dtype=float)
