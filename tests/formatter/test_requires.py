import pytest

from tox_ini_fmt.formatter.requires import requires


@pytest.mark.parametrize(
    "value, result",
    [
        ("", []),
        ("\t", []),
        ("\n\t\n", []),
        ("b\na\n", ["a", "b"]),
        ("a\nb\n", ["a", "b"]),
        ("A\na\n", ["A", "a"]),
        ("\nA\n\n\nb\n\n", ["A", "b"]),
        (
            'packaging>=20.0;python_version>"3.4"\n'
            "xonsh>=0.9.16;python_version > '3.4' and python_version != '3.9'\n"
            "pytest-xdist>=1.31.0\n",
            [
                "pytest-xdist>=1.31",
                'packaging>=20;python_version>"3.4"',
                "xonsh>=0.9.16;python_version > '3.4' and python_version != '3.9'",
            ],
        ),
        ("pytest>=6.0.0", ["pytest>=6"]),
        ("pytest==6.0.0", ["pytest==6"]),
        ("pytest~=6.0.0", ["pytest~=6.0.0"]),
    ],
)
def test_requires_fmt(value, result):
    outcome = requires([i.strip() for i in value.splitlines() if i.strip()])
    assert outcome == result


@pytest.mark.parametrize(
    "char",
    [
        "!",
        "=",
        ">",
        "<",
        " ",
        "\t",
        "@",
    ],
)
def test_bad_syntax_requires(char):
    with pytest.raises(ValueError, match=f"[{char}]" if char.strip() else None):
        requires(f"{char};")
