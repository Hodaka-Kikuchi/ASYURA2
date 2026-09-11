from .selection import file_select
from .selection import clear
from .selection import vfile_select
from .selection import vclear
from .selection import sbfile_select
from .selection import sbclear
from .merge import mergefile
from .merge import mergefile_sb
from .labels import update_UVlabel1
from .calibration import calibration
from .mask import maskclear
from .mask import maskall
from .events import on_entry_change
from .parameters import save_param
from .parameters import initialize_param
from .parameters import load_param

from functools import partial

def create_files_callbacks(env):
    """Build callback registry for this feature package."""
    return {
        'file_select': partial(file_select, env),
        'clear': partial(clear, env),
        'vfile_select': partial(vfile_select, env),
        'vclear': partial(vclear, env),
        'sbfile_select': partial(sbfile_select, env),
        'sbclear': partial(sbclear, env),
        'mergefile': partial(mergefile, env),
        'mergefile_sb': partial(mergefile_sb, env),
        'update_UVlabel1': partial(update_UVlabel1, env),
        'calibration': partial(calibration, env),
        'maskclear': partial(maskclear, env),
        'maskall': partial(maskall, env),
        'on_entry_change': partial(on_entry_change, env),
        'save_param': partial(save_param, env),
        'initialize_param': partial(initialize_param, env),
        'load_param': partial(load_param, env),
    }
