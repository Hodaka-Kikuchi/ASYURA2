from ...callback_runtime import *

def switch_mode(env):
    mode_var = env.get('mode_var')
    scatter_frame = env.get('scatter_frame')
    slice_frame = env.get('slice_frame')
    if mode_var.get() == "slice":
        slice_frame.tkraise()
    elif mode_var.get() == "scatter":
        scatter_frame.tkraise()
