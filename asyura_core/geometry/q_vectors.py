"""Laboratory momentum-transfer vectors."""
import math
import numpy as np

def _data_q_lab(ei_meV, ef_meV, a2_deg):
    """
    Laboratory momentum transfer for a horizontal detector.

        Q_lab = ki - kf
              = (-kf*sin(A2), 0, ki-kf*cos(A2))

    This is the same PDF convention used by the corrected scan simulation.
    """
    ei_meV = float(ei_meV)
    ef_meV = float(ef_meV)

    if ei_meV <= 0.0 or ef_meV <= 0.0:
        raise ValueError(
            f"Neutron energy must be positive: Ei={ei_meV}, Ef={ef_meV}"
        )

    ki = math.sqrt(ei_meV / 2.072)
    kf = math.sqrt(ef_meV / 2.072)
    a2 = math.radians(float(a2_deg))

    return np.array([
        -kf * math.sin(a2),
        0.0,
        ki - kf * math.cos(a2),
    ], dtype=float)

def _simu_q_lab(ei_meV, ef_meV, a2_deg):
    """
    Laboratory momentum transfer in the PDF convention.

    Lab axes:
        +z : incident beam
        +y : vertical
        +x : horizontal transverse

    For a horizontal detector (phi = 0):

        Q_lab = ki - kf
              = (-kf*sin(A2), 0, ki-kf*cos(A2))

    A2 is the full scattering angle.
    """
    ei_meV = float(ei_meV)
    ef_meV = float(ef_meV)

    if ei_meV <= 0.0 or ef_meV <= 0.0:
        raise ValueError("Ei and Ef must be positive.")

    ki = math.sqrt(ei_meV / 2.072)
    kf = math.sqrt(ef_meV / 2.072)

    a2 = math.radians(float(a2_deg))

    return np.array([
        -kf * math.sin(a2),
        0.0,
        ki - kf * math.cos(a2),
    ], dtype=float)
