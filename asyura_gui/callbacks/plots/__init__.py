from .advanced_2d import advanced_2D_constE
from .advanced_2d import advanced_2D_constQ
from .advanced_1d import advanced_1D_alongE
from .advanced_1d import add_advanced_1D_alongE
from .advanced_1d import advanced_1D_alongQ
from .advanced_1d import add_advanced_1D_alongQ
from .scatter import disp3D
from .scatter import scatter_2d_cE
from .scatter import scatter_2d_cU
from .scatter import scatter_2d_cV
from .scatter import show_3DconEmap
from .maps_2d import constQmap_V2
from .maps_2d import constQmap_U2
from .maps_2d import constEmap
from .maps_2d import constQmap_V
from .maps_2d import constQmap_U
from .cuts_1d import constQmap_1D
from .cuts_1d import constQmap_1D2
from .cuts_1d import constE_1D_U
from .cuts_1d import constE_1D_U2
from .cuts_1d import constE_1D_V
from .cuts_1d import constE_1D_V2
from .axis_controls import xaxis_select

from functools import partial

def create_plots_callbacks(env):
    """Build callback registry for this feature package."""
    return {
        'advanced_2D_constE': partial(advanced_2D_constE, env),
        'advanced_2D_constQ': partial(advanced_2D_constQ, env),
        'advanced_1D_alongE': partial(advanced_1D_alongE, env),
        'add_advanced_1D_alongE': partial(add_advanced_1D_alongE, env),
        'advanced_1D_alongQ': partial(advanced_1D_alongQ, env),
        'add_advanced_1D_alongQ': partial(add_advanced_1D_alongQ, env),
        'disp3D': partial(disp3D, env),
        'scatter_2d_cE': partial(scatter_2d_cE, env),
        'scatter_2d_cU': partial(scatter_2d_cU, env),
        'scatter_2d_cV': partial(scatter_2d_cV, env),
        'show_3DconEmap': partial(show_3DconEmap, env),
        'constQmap_V2': partial(constQmap_V2, env),
        'constQmap_U2': partial(constQmap_U2, env),
        'constEmap': partial(constEmap, env),
        'constQmap_V': partial(constQmap_V, env),
        'constQmap_U': partial(constQmap_U, env),
        'constQmap_1D': partial(constQmap_1D, env),
        'constQmap_1D2': partial(constQmap_1D2, env),
        'constE_1D_U': partial(constE_1D_U, env),
        'constE_1D_U2': partial(constE_1D_U2, env),
        'constE_1D_V': partial(constE_1D_V, env),
        'constE_1D_V2': partial(constE_1D_V2, env),
        'xaxis_select': partial(xaxis_select, env),
    }
