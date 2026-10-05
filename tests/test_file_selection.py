from types import SimpleNamespace

import pytest

from asyura_gui.base.dataset_information import _configure_file_listbox
from asyura_gui.file_lists import (
    append_unique_paths,
    remove_selected_from_state,
    remove_selected_paths,
)


class FakeListbox:
    def __init__(self, selected=()):
        self.items = []
        self.selected = selected
        self.options = {}
        self.bindings = {}

    def bind(self, sequence, callback):
        self.bindings[sequence] = callback

    def configure(self, **kwargs):
        self.options.update(kwargs)

    def curselection(self):
        return self.selected

    def delete(self, first, last):
        self.items.clear()

    def insert(self, index, item):
        self.items.append(item)


@pytest.mark.parametrize('data_kind', ['foreground', 'background'])
def test_remove_selected_keeps_paths_and_display_in_sync(data_kind):
    paths = ['/data/A.dat', '/data/B.dat', '/data/C.dat']
    listbox = FakeListbox(selected=(1,))
    if data_kind == 'foreground':
        listbox_key, paths_key, names_key = 'Listbox', 'file_paths', 'flist'
    else:
        listbox_key, paths_key, names_key = (
            'sbListbox',
            'sbfile_paths',
            'sblists',
        )
    state = {paths_key: paths, names_key: ['A.dat', 'B.dat', 'C.dat']}

    remove_selected_from_state(
        {'state': state, listbox_key: listbox},
        listbox_key,
        paths_key,
        names_key,
    )

    assert paths == ['/data/A.dat', '/data/C.dat']
    assert state[names_key] == ['A.dat', 'C.dat']
    assert listbox.items == ['A.dat', 'C.dat']


def test_remove_multiple_selected_paths():
    paths = ['/data/A.dat', '/data/B.dat', '/data/C.dat']
    listbox = FakeListbox(selected=(0, 2))

    names = remove_selected_paths(listbox, paths)

    assert paths == ['/data/B.dat']
    assert names == ['B.dat']
    assert listbox.items == ['B.dat']


def test_remove_selected_with_no_selection_is_a_noop():
    paths = ['/data/A.dat']
    listbox = FakeListbox()

    names = remove_selected_paths(listbox, paths)

    assert paths == ['/data/A.dat']
    assert names == ['A.dat']
    assert listbox.items == ['A.dat']


def test_removal_uses_index_when_basenames_match():
    paths = ['/data/run1/scan001.dat', '/data/run2/scan001.dat']
    listbox = FakeListbox(selected=(0,))

    names = remove_selected_paths(listbox, paths)

    assert paths == ['/data/run2/scan001.dat']
    assert names == ['scan001.dat']
    assert listbox.items == ['scan001.dat']


def test_same_normalized_path_is_not_added_twice(tmp_path):
    path = str(tmp_path / 'scan001.dat')
    paths = []

    append_unique_paths(paths, [path])
    append_unique_paths(paths, [path])

    assert paths == [path]


def test_existing_duplicates_are_cleaned(tmp_path):
    path = str(tmp_path / 'scan001.dat')
    paths = [path, path]

    append_unique_paths(paths, [])

    assert paths == [path]


def test_duplicate_does_not_reappear_after_removal(tmp_path):
    first = str(tmp_path / 'A.dat')
    second = str(tmp_path / 'B.dat')
    paths = [first, second]
    listbox = FakeListbox(selected=(1,))

    remove_selected_paths(listbox, paths)
    append_unique_paths(paths, [first])

    assert paths == [first]
    assert listbox.items == ['A.dat']


def test_equivalent_relative_and_absolute_paths_are_deduplicated(
    tmp_path, monkeypatch
):
    monkeypatch.chdir(tmp_path)
    relative = 'scan001.dat'
    absolute = str(tmp_path / relative)
    paths = []

    append_unique_paths(paths, [relative, absolute])

    assert paths == [relative]


def test_different_paths_with_same_basename_are_kept(tmp_path):
    first = str(tmp_path / 'run1' / 'scan001.dat')
    second = str(tmp_path / 'run2' / 'scan001.dat')
    paths = []

    append_unique_paths(paths, [first, second])

    assert paths == [first, second]


def test_file_listbox_supports_multiple_selection_and_removal_keys():
    listbox = FakeListbox()
    callback = object()
    tk = SimpleNamespace(EXTENDED='extended')

    _configure_file_listbox(listbox, callback, tk)

    assert listbox.options == {
        'selectmode': 'extended',
        'exportselection': False,
    }
    assert listbox.bindings == {
        '<Delete>': callback,
        '<BackSpace>': callback,
    }


@pytest.mark.parametrize('sequence', ['<Delete>', '<BackSpace>'])
def test_removal_keys_run_the_remove_action(sequence):
    paths = ['/data/A.dat', '/data/B.dat']
    listbox = FakeListbox(selected=(0,))
    tk = SimpleNamespace(EXTENDED='extended')

    def remove_callback(event):
        remove_selected_paths(listbox, paths)

    _configure_file_listbox(listbox, remove_callback, tk)
    listbox.bindings[sequence](object())

    assert paths == ['/data/B.dat']
    assert listbox.items == ['B.dat']
