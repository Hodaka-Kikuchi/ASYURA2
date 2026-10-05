"""Energy, wavelength and wave-number conversions."""
import math

def energy_to_wavelength_wavenumber(energy_meV):
    wavelength = math.sqrt(81.81 / float(energy_meV))
    wavenumber = 2.0 * math.pi / wavelength
    return wavelength, wavenumber

def wavelength_to_energy_wavenumber(wavelength_A):
    wavelength = float(wavelength_A)
    energy = 81.81 / wavelength**2
    wavenumber = 2.0 * math.pi / wavelength
    return energy, wavenumber

def wavenumber_to_energy_wavelength(wavenumber_Ainv):
    wavenumber = float(wavenumber_Ainv)
    wavelength = 2.0 * math.pi / wavenumber
    energy = 81.81 / wavelength**2
    return energy, wavelength

def harmonic_energy(energy_meV, wavelength_factor):
    """Return energy after changing wavelength by ``wavelength_factor``.

    Since E is proportional to 1/lambda^2, lambda/2 gives 4E and 2lambda gives E/4.
    """
    factor = float(wavelength_factor)
    return float(energy_meV) / factor**2
