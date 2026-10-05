"""Typed data models for SPICE metadata."""

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True, slots=True)
class SpiceReferencePeak:
    """Reference Bragg peak stored in a SPICE ``peak1`` record.

    SPICE peak1 order:
        h k l s2 s1 sgl sgu ei ef

    ASYURA names:
        s2  -> a2
        s1  -> c2
        sgl -> ry
        sgu -> rx
    """

    h: float
    k: float
    l: float
    a2: float
    c2: float
    ry: float
    rx: float
    ei: float
    ef: float

    @property
    def hkl(self) -> np.ndarray:
        """Return (h, k, l) as a new float NumPy array."""
        return np.array([self.h, self.k, self.l], dtype=float)

    @classmethod
    def from_values(
        cls,
        h,
        k,
        l,
        a2,
        c2,
        ry,
        rx,
        ei,
        ef,
    ):
        """Create a reference peak while normalizing all fields to float."""
        return cls(
            h=float(h),
            k=float(k),
            l=float(l),
            a2=float(a2),
            c2=float(c2),
            ry=float(ry),
            rx=float(rx),
            ei=float(ei),
            ef=float(ef),
        )
