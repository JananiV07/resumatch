import json
import re
from functools import lru_cache
from pathlib import Path
from rapidfuzz import fuzz

_SKILLS_PATH = Path(__file__).parent / "skills.json"
_FUZZY_THRESHOLD = 88


@lru_cache(maxsize=1)
def load_skills() -> list[str]:
    data = json.loads(_SKILLS_PATH.read_text(encoding="utf-8"))
    return [s.lower() for s in data["skills"]]


def _alnum_tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def find_skills(text: str, skills: list[str]) -> set[str]:
    """Return the subset of `skills` present in `text`.

    A skill matches when it appears as a standalone token (boundaries that are
    not letters/digits), which correctly handles trailing punctuation and
    symbol skills like ``c++``, ``c#``, ``node.js``, ``scikit-learn``. A fuzzy
    fallback catches typos for plain alphanumeric skills.
    """
    low = text.lower()
    tokens = _alnum_tokens(low)
    found: set[str] = set()
    for skill in skills:
        s = skill.lower()
        pattern = r"(?<![a-z0-9])" + re.escape(s) + r"(?![a-z0-9])"
        if re.search(pattern, low):
            found.add(skill)
            continue
        if s.isalnum():
            for tok in tokens:
                if abs(len(tok) - len(s)) <= 2 and fuzz.ratio(tok, s) >= _FUZZY_THRESHOLD:
                    found.add(skill)
                    break
    return found
