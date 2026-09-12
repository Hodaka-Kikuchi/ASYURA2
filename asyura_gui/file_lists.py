"""Shared state/display helpers for foreground and background file lists."""

import os


def path_key(path):
    """Return a normalized key used only for duplicate detection."""
    return os.path.normcase(os.path.abspath(os.fspath(path)))


def append_unique_paths(paths, selected):
    """Keep *paths* ordered and unique, then append only new selections.

    The stored path itself is left unchanged. Normalization is used only for
    comparison, so downstream data readers continue to receive the same path
    strings selected by the user.
    """
    unique_paths = []
    existing = set()

    # Also clean up duplicates that may already be present in state from an
    # older selection made before duplicate prevention was added.
    for path in paths:
        key = path_key(path)
        if key not in existing:
            unique_paths.append(path)
            existing.add(key)

    for path in selected:
        key = path_key(path)
        if key not in existing:
            unique_paths.append(path)
            existing.add(key)

    paths[:] = unique_paths


def refresh_path_listbox(listbox, paths):
    """Show exactly one row for each path that will actually be read."""
    names = [os.path.basename(path) for path in paths]
    listbox.delete(0, "end")
    for name in names:
        listbox.insert("end", name)
    return names


def remove_selected_paths(listbox, paths):
    """Remove selected rows by index and rebuild the displayed file names."""
    selected_indices = {int(index) for index in listbox.curselection()}
    paths[:] = [
        path
        for index, path in enumerate(paths)
        if index not in selected_indices
    ]
    return refresh_path_listbox(listbox, paths)


def remove_selected_from_state(env, listbox_key, paths_key, names_key):
    """Synchronize one file list's full paths, display names, and Listbox."""
    listbox = env.get(listbox_key)
    state = env.get("state")
    state[names_key] = remove_selected_paths(listbox, state[paths_key])
