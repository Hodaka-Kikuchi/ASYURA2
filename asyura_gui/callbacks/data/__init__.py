from .ub_display import show_ubmatrix
from .loading import loadfile
from .mode import switch_mode
from .binning import data_box
from .range_controls import set_range
from .range_controls import gs_clear
from .range_controls import gs_auto
from .range_controls import gs_clear2
from .range_controls import gs_auto2
from .range_controls import threshold_auto
from .range_controls import range_auto_3D

from functools import partial

def create_data_callbacks(env):
    """Build callback registry for this feature package."""
    return {
        '_show_ubmatrix': partial(show_ubmatrix, env),
        'loadfile': partial(loadfile, env),
        'switch_mode': partial(switch_mode, env),
        'data_box': partial(data_box, env),
        'set_range': partial(set_range, env),
        'gs_clear': partial(gs_clear, env),
        'gs_auto': partial(gs_auto, env),
        'gs_clear2': partial(gs_clear2, env),
        'gs_auto2': partial(gs_auto2, env),
        'threshold_auto': partial(threshold_auto, env),
        'range_auto_3D': partial(range_auto_3D, env),
    }
