"""Triple-axis spectrometer kinematics."""
import math
import numpy as np

def tas_scattering_angle_deg(q_Ainv, ei_meV, ef_meV):
    """Return the unsigned sample scattering angle 2theta in degrees."""
    li = 9.045 / math.sqrt(float(ei_meV))
    lf = 9.045 / math.sqrt(float(ef_meV))
    ki = 2.0 * math.pi / li
    kf = 2.0 * math.pi / lf
    cosine = (ki**2 + kf**2 - float(q_Ainv) ** 2) / (2.0 * ki * kf)
    cosine = max(-1.0, min(1.0, cosine))
    return math.degrees(math.acos(cosine))
