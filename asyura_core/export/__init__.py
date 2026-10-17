from .raw_data import *
from .single_crystal_maps import *
from .single_crystal_cuts import *
from .hkl import *
from .masked import *
from .powder import *

# Every public save_* function checks that its results exist before asking
# for a file name (see guard.py).
from .guard import requires_results as _requires_results

for _name in [n for n in list(globals()) if n.startswith("save_") and callable(globals()[n])]:
    globals()[_name] = _requires_results(globals()[_name])
del _name
