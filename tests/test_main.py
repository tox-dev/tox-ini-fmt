import pytest

from tox_ini_fmt.__main__ import run


@pytest.mark.parametrize("in_place", [True, False])
def test_main(tmp_path, capsys, in_place):
    start_text = "[tox]\nenvlist=py39,py38"
    tox_ini = tmp_path / "tox.ini"
    tox_ini.write_text(start_text)
    args = [str(tox_ini)]
    if not in_place:
        args.append("--stdout")

    result = run(args)
    assert result == 0

    outcome = "[tox]\nenvlist =\n  py39\n  py38\n"
    out, err = capsys.readouterr()
    assert not err

    if in_place:
        assert tox_ini.read_text() == outcome
        assert f"updated {tox_ini}" in out
    else:
        assert out == outcome
