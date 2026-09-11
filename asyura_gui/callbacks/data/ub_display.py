from ...callback_runtime import *

def show_ubmatrix(env, UB):
    i = env.get('i')
    txt_ub_11 = env.get('txt_ub_11')
    txt_ub_12 = env.get('txt_ub_12')
    txt_ub_13 = env.get('txt_ub_13')
    txt_ub_21 = env.get('txt_ub_21')
    txt_ub_22 = env.get('txt_ub_22')
    txt_ub_23 = env.get('txt_ub_23')
    txt_ub_31 = env.get('txt_ub_31')
    txt_ub_32 = env.get('txt_ub_32')
    txt_ub_33 = env.get('txt_ub_33')

    """Write a 3x3 UB matrix to the existing readonly Entry widgets."""
    entries = (
        (txt_ub_11, txt_ub_12, txt_ub_13),
        (txt_ub_21, txt_ub_22, txt_ub_23),
        (txt_ub_31, txt_ub_32, txt_ub_33),
    )
    for i in range(3):
        for j in range(3):
            entry = entries[i][j]
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.insert(0, f"{UB[i, j]:.6f}")
            entry.config(state="readonly")
