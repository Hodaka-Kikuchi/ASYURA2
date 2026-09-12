from ...callback_runtime import *


def _path_key(path):
    """Return a normalized key used only for duplicate detection."""
    return os.path.normcase(os.path.abspath(os.fspath(path)))


def _append_unique_paths(paths, selected):
    """Keep *paths* ordered and unique, then append only new selections.

    The stored path itself is left unchanged. Normalization is used only for
    comparison, so downstream data readers continue to receive the same path
    strings selected by the user.
    """
    unique_paths = []
    existing = set()

    # Also clean up duplicates that may already be present in state from an
    # older selection made before this fix.
    for path in paths:
        key = _path_key(path)
        if key not in existing:
            unique_paths.append(path)
            existing.add(key)

    for path in selected:
        key = _path_key(path)
        if key not in existing:
            unique_paths.append(path)
            existing.add(key)

    paths[:] = unique_paths


def _refresh_path_listbox(listbox, paths):
    """Show exactly one row for each path that will actually be read."""
    listbox.delete(0, tk.END)
    for path in paths:
        listbox.insert(tk.END, os.path.basename(path))


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
    state['flist'] = [os.path.basename(path) for path in state['file_paths']]
    _refresh_path_listbox(Listbox, state['file_paths'])


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
    state['sblists'] = [
        os.path.basename(path) for path in state['sbfile_paths']
    ]
    _refresh_path_listbox(sbListbox, state['sbfile_paths'])


def sbclear(env):
    sbListbox = env.get('sbListbox')
    state = env.get('state')
    sbListbox.delete(0, tk.END)
    state['sbfile_paths'].clear()
    state['sblists'] = []
