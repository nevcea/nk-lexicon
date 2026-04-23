import csv
from pathlib import Path

_TERM_COLUMN = "용어"
_ZERO_WIDTH_CHARS = "​‌‍﻿­"
_ASCII_PUNCT = frozenset("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")


def load_raw_csv(path: Path) -> list[str]:
    with path.open(encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return [row[_TERM_COLUMN] for row in reader]


def strip_term(term: str) -> str:
    return term.strip().strip(_ZERO_WIDTH_CHARS)


def is_valid_term(term: str) -> bool:
    if not term:
        return False
    if term.isspace():
        return False
    # 순수 ASCII 구두점만으로 구성된 항목 제외
    if all(c in _ASCII_PUNCT for c in term):
        return False
    # 1음절은 동사/조사 어간과 충돌 가능성이 높아 제외
    if len(term) == 1:
        return False
    return True


def clean_terms(terms: list[str]) -> list[str]:
    result = []
    for term in terms:
        stripped = strip_term(term)
        if is_valid_term(stripped):
            result.append(stripped)
    return result


def deduplicate(terms: list[str]) -> list[str]:
    seen: set[str] = set()
    result = []
    for term in terms:
        if term not in seen:
            seen.add(term)
            result.append(term)
    return result


def save_clean_csv(terms: list[str], path: Path) -> None:
    if path.exists():
        raise FileExistsError(f"출력 파일이 이미 존재합니다: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([_TERM_COLUMN])
        for term in terms:
            writer.writerow([term])
