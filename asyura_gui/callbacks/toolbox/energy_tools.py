from ...callback_runtime import *

def high_harmo(env):
    txt_s4_2f = env.get('txt_s4_2f')
    E0f=float(txt_s4_2f.get())
    txt_s4_2f.delete(0,tk.END)
    E1f=harmonic_energy(E0f, 0.5)
    txt_s4_2f.insert(0,E1f)

def low_harmo(env):
    txt_s4_2f = env.get('txt_s4_2f')
    E0f=float(txt_s4_2f.get())
    txt_s4_2f.delete(0,tk.END)
    E1f=harmonic_energy(E0f, 2.0)
    txt_s4_2f.insert(0,E1f)

def trans_ELK(env, event=None):
    root = env.get('root')
    txt_s4_2f = env.get('txt_s4_2f')
    txt_s4_3 = env.get('txt_s4_3')
    txt_s4_4 = env.get('txt_s4_4')
    """
    入力された値に基づいてエネルギー、波長、波数を計算し、エントリーボックスを更新します。
    """
    try:
        # フォーカスされているウィジェットを特定
        focused_widget = root.focus_get()

        # 各エントリーボックスの値を取得
        energy = txt_s4_2f.get().strip()
        wavelength = txt_s4_3.get().strip()
        wavenumber = txt_s4_4.get().strip()

        # フォーカスされているエントリーボックスに応じて処理
        if focused_widget == txt_s4_2f and energy:
            energy = float(energy)
            wavelength, wavenumber = energy_to_wavelength_wavenumber(energy)
            # 他のボックスをクリアして計算結果を出力
            txt_s4_3.delete(0, tk.END)
            txt_s4_4.delete(0, tk.END)
            txt_s4_3.insert(0, f"{wavelength:.4f}")
            txt_s4_4.insert(0, f"{wavenumber:.4f}")

        elif focused_widget == txt_s4_3 and wavelength:
            wavelength = float(wavelength)
            energy, wavenumber = wavelength_to_energy_wavenumber(wavelength)
            # 他のボックスをクリアして計算結果を出力
            txt_s4_2f.delete(0, tk.END)
            txt_s4_4.delete(0, tk.END)
            txt_s4_2f.insert(0, f"{energy:.4f}")
            txt_s4_4.insert(0, f"{wavenumber:.4f}")

        elif focused_widget == txt_s4_4 and wavenumber:
            wavenumber = float(wavenumber)
            energy, wavelength = wavenumber_to_energy_wavelength(wavenumber)
            # 他のボックスをクリアして計算結果を出力
            txt_s4_2f.delete(0, tk.END)
            txt_s4_3.delete(0, tk.END)
            txt_s4_3.insert(0, f"{wavelength:.4f}")
            txt_s4_2f.insert(0, f"{energy:.4f}")

        else:
            pass
            return

    except ValueError:
        pass
