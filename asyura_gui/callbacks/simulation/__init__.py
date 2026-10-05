from .display_basis import prepare_simu_reciprocal_display
from .single_crystal import simu_sc_cE
from .single_crystal import simu_sc_cU
from .single_crystal import simu_sc_cV
from .single_crystal import add_simu_sc_cU
from .single_crystal import add_simu_sc_cE
from .single_crystal import add_simu_sc_cV
from .powder import simu_pow
from .powder import add_simu_pow

from functools import partial

def create_simulation_callbacks(env):
    """Build callback registry for this feature package."""
    return {
        '_prepare_simu_reciprocal_display': partial(prepare_simu_reciprocal_display, env),
        'simu_sc_cE': partial(simu_sc_cE, env),
        'simu_sc_cU': partial(simu_sc_cU, env),
        'simu_sc_cV': partial(simu_sc_cV, env),
        'add_simu_sc_cU': partial(add_simu_sc_cU, env),
        'add_simu_sc_cE': partial(add_simu_sc_cE, env),
        'add_simu_sc_cV': partial(add_simu_sc_cV, env),
        'simu_pow': partial(simu_pow, env),
        'add_simu_pow': partial(add_simu_pow, env),
    }
