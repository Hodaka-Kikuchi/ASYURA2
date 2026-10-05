"""Reciprocal-lattice magnitude calculations."""
import math
import numpy as np

def reciprocal_q_and_d(a, b, c, alpha_deg, beta_deg, gamma_deg, h, k, l):
    """Calculate |Q| and d-spacing for an arbitrary triclinic lattice."""
    alpha = math.radians(alpha_deg)
    beta = math.radians(beta_deg)
    gamma = math.radians(gamma_deg)

    avec = np.array([float(a), 0.0, 0.0])
    bvec = np.array([float(b) * math.cos(gamma), float(b) * math.sin(gamma), 0.0])
    cvec = np.array([
        float(c) * math.cos(beta),
        float(c) * (math.cos(alpha) - math.cos(beta) * math.cos(gamma)) / math.sin(gamma),
        0.0,
    ])
    cvec[2] = math.sqrt(max(float(c) ** 2 - cvec[0] ** 2 - cvec[1] ** 2, 0.0))

    astar = 2.0 * math.pi * np.cross(bvec, cvec) / np.dot(avec, np.cross(bvec, cvec))
    bstar = 2.0 * math.pi * np.cross(cvec, avec) / np.dot(bvec, np.cross(cvec, avec))
    cstar = 2.0 * math.pi * np.cross(avec, bvec) / np.dot(cvec, np.cross(avec, bvec))

    qvec = float(h) * astar + float(k) * bstar + float(l) * cstar
    q = float(np.linalg.norm(qvec))
    d = 2.0 * math.pi / q
    return q, d
