from asyura_gui.callbacks.files.selection import _append_unique_paths


def test_same_path_is_not_added_twice(tmp_path):
    path = str(tmp_path / "scan001.dat")
    paths = []
    _append_unique_paths(paths, [path])
    _append_unique_paths(paths, [path])
    assert paths == [path]


def test_existing_duplicates_are_cleaned(tmp_path):
    path = str(tmp_path / "scan001.dat")
    paths = [path, path]
    _append_unique_paths(paths, [])
    assert paths == [path]


def test_different_paths_with_same_basename_are_kept(tmp_path):
    p1 = str(tmp_path / "run1" / "scan001.dat")
    p2 = str(tmp_path / "run2" / "scan001.dat")
    paths = []
    _append_unique_paths(paths, [p1, p2])
    assert paths == [p1, p2]
