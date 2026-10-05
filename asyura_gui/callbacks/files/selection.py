from ...callback_runtime import *
from ...file_lists import append_unique_paths as _append_unique_paths
from ...file_lists import path_key as _path_key
from ...file_lists import refresh_path_listbox as _refresh_path_listbox
from ...file_lists import remove_selected_from_state as _remove_selected


def file_select(env):
    Listbox = env.get('Listbox')
    state = env.get('state')
    filetypes = [("dat file", "*.dat")]

    selected = tk.filedialog.askopenfilenames(
        filetypes=filetypes,
        multiple=True,
    )
    _append_unique_paths(state['file_paths'], selected)

    # Keep legacy display-name state in sync with the actual read list.
    state['flist'] = _refresh_path_listbox(Listbox, state['file_paths'])


def remove_selected(env, event=None):
    _remove_selected(env, 'Listbox', 'file_paths', 'flist')
    if event is not None:
        return 'break'


def clear(env):
    Listbox = env.get('Listbox')
    state = env.get('state')
    Listbox.delete(0, tk.END)
    state['file_paths'].clear()
    state['flist'] = []


def vfile_select(env):
    state = env.get('state')
    vListbox = env.get('vListbox')
    vListbox.delete(0, tk.END)
    filetypes = [("dat file", "*.dat")]
    state['vfile_path'] = tk.filedialog.askopenfilenames(
        filetypes=filetypes,
        multiple=False,
    )
    vflnmlst = [os.path.basename(item) for item in state['vfile_path']]
    vflist = list(vflnmlst)
    vListbox.insert(tk.END, vflist)


def vclear(env):
    vListbox = env.get('vListbox')
    vListbox.delete(0, tk.END)
    vfile_path = []


def sbfile_select(env):
    sbListbox = env.get('sbListbox')
    state = env.get('state')
    filetypes = [("dat file", "*.dat")]

    selected = tk.filedialog.askopenfilenames(
        filetypes=filetypes,
        multiple=True,
    )
    _append_unique_paths(state['sbfile_paths'], selected)

    # Background files follow the same rule as the main data files.
    state['sblists'] = _refresh_path_listbox(
        sbListbox,
        state['sbfile_paths'],
    )


def sbremove_selected(env, event=None):
    _remove_selected(env, 'sbListbox', 'sbfile_paths', 'sblists')
    if event is not None:
        return 'break'


def sbclear(env):
    sbListbox = env.get('sbListbox')
    state = env.get('state')
    sbListbox.delete(0, tk.END)
    state['sbfile_paths'].clear()
    state['sblists'] = []
