from .time_estimate import time_estimate
from .angle_calculator import tta_calc
from .energy_tools import high_harmo
from .energy_tools import low_harmo
from .energy_tools import trans_ELK
from .c2_calculator import calculate_c2

from functools import partial

def create_toolbox_callbacks(env):
    """Build callback registry for this feature package."""
    return {
        'time_estimate': partial(time_estimate, env),
        'tta_calc': partial(tta_calc, env),
        'high_harmo': partial(high_harmo, env),
        'low_harmo': partial(low_harmo, env),
        'trans_ELK': partial(trans_ELK, env),
        'calculate_c2': partial(calculate_c2, env),
    }
