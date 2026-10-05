from .data import pow_data_box
from .range_controls import p_set_range
from .range_controls import gsp_clear
from .range_controls import gsp_auto
from .maps import show_powderEmap
from .cuts import show_1D_EvsI
from .cuts import btn_click_1DPE
from .cuts import show_1D_QvsI
from .cuts import btn_click_1DPQ
from .axis_controls import xaxis_selectp

from functools import partial

def create_powder_callbacks(env):
    """Build callback registry for this feature package."""
    return {
        'pow_data_box': partial(pow_data_box, env),
        'p_set_range': partial(p_set_range, env),
        'gsp_clear': partial(gsp_clear, env),
        'gsp_auto': partial(gsp_auto, env),
        'show_powderEmap': partial(show_powderEmap, env),
        'show_1D_EvsI': partial(show_1D_EvsI, env),
        'btn_click_1DPE': partial(btn_click_1DPE, env),
        'show_1D_QvsI': partial(show_1D_QvsI, env),
        'btn_click_1DPQ': partial(btn_click_1DPQ, env),
        'xaxis_selectp': partial(xaxis_selectp, env),
    }
