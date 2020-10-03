import pytest

from tox_ini_fmt.__main__ import run


@pytest.mark.parametrize("in_place", [True, False])
@pytest.mark.parametrize("cwd", [True, False])
@pytest.mark.parametrize(
    "start, outcome, output",
    [
        (
            "[tox]\nenvlist=py39,py38",
            "[tox]\nenvlist =\n    py39\n    py38\n",
            "--- {0}\n\n+++ {0}\n\n@@ -1,2 +1,4 @@\n\n "
            "[tox]\n-envlist=py39,py38\n+envlist =\n+    py39\n+    py38\n",
        ),
        ("[tox]\nenvlist =\n    py39\n    py38\n", "[tox]\nenvlist =\n    py39\n    py38\n", "no change for {0}\n"),
    ],
)
def test_main(tmp_path, capsys, in_place, start, outcome, output, monkeypatch, cwd):
    if cwd:
        monkeypatch.chdir(tmp_path)
    tox_ini = tmp_path / "tox.ini"
    tox_ini.write_text(start)
    args = [str(tox_ini)]
    if not in_place:
        args.append("--stdout")

    result = run(args)
    assert result == (0 if start == outcome else 1)

    outcome = "[tox]\nenvlist =\n    py39\n    py38\n"
    out, err = capsys.readouterr()
    assert not err

    if in_place:
        name = "tox.ini" if cwd else str(tmp_path / "tox.ini")
        output = output.format(name)
        assert tox_ini.read_text() == outcome
        assert out == output
    else:
        assert out == outcome
