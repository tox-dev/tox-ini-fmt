import itertools
from configparser import ConfigParser
from typing import Dict, List


def order_sections(parser: ConfigParser) -> None:
    """
    Start with tox, then testenv. The testenv elements follow the order within envlist. Then all other testenv elements,
    and end it with any other sections present in the file (e.g. pytest/mypy configuration).
    """
    order = ["tox", "testenv"]
    order.extend(f"testenv:{env}" for env in load_env_list(parser))
    order.extend(s for s in parser.sections() if s not in order and s.startswith("testenv:"))
    order.extend(s for s in parser.sections() if s not in order and not s.startswith("testenv:"))
    sections: Dict[str, Dict[str, str]] = {}
    for section in order:
        if parser.has_section(section):
            sections[section] = dict(parser[section])
            parser.pop(section)
    for k, v in sections.items():
        parser[k] = v


def load_env_list(parser: ConfigParser) -> List[str]:
    if not parser.has_section("tox"):
        return []
    if "envlist" not in parser["tox"]:
        return []
    return explode_env_list(parser["tox"]["envlist"])


def explode_env_list(env_list: str) -> List[str]:
    result: List[str] = []
    for entry in env_list.split("\n"):
        entry = entry.strip()
        if entry:
            parts = []
            for part in entry.split("-"):
                if part[0] == "{" and part[-1] == "}":
                    sub_parts = [i.strip() for i in part[1:-1].split(",")]
                else:
                    sub_parts = [part]
                parts.append(sub_parts)
            result.extend("-".join(i).strip("-") for i in itertools.product(*parts))
    return result
