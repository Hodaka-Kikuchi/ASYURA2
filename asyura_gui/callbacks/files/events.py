from ...callback_runtime import *

def on_entry_change(env, event):
    selected_detector = env.get('selected_detector')
    update_phi = env.get('update_phi')
    if selected_detector.get() == "arbitral":
        update_phi()
