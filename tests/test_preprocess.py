import csv
from pathlib import Path

import pytest

from nk_lexicon.preprocess import (
    clean_terms,
    deduplicate,
    is_valid_term,
    load_raw_csv,
    save_clean_csv,
    strip_term,
)


def test_strip_term_removes_whitespace() -> None:
    assert strip_term("  가나다  ") == "가나다"
    assert strip_term("\t조선\t") == "조선"


def test_is_valid_term_rejects_empty() -> None:
    assert is_valid_term("") is False
    assert is_valid_term("   ") is False


def test_is_valid_term_rejects_single_syllable() -> None:
    assert is_valid_term("역") is False
    assert is_valid_term("모") is False


def test_is_valid_term_accepts_korean() -> None:
    assert is_valid_term("조선") is True
    assert is_valid_term("-ㄹ가") is True


def test_is_valid_term_rejects_ascii_punctuation_only() -> None:
    assert is_valid_term("...") is False
    assert is_valid_term("---") is False


def test_clean_terms_filters_and_strips() -> None:
    terms = ["  조선  ", "", "  ", "평양", "!!!", "로동"]
    result = clean_terms(terms)
    assert result == ["조선", "평양", "로동"]


def test_deduplicate_preserves_order() -> None:
    terms = ["가", "나", "가", "다", "나"]
    assert deduplicate(terms) == ["가", "나", "다"]


def test_deduplicate_no_duplicates() -> None:
    terms = ["가", "나", "다"]
    assert deduplicate(terms) == ["가", "나", "다"]


def test_load_raw_csv_file_not_found(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_raw_csv(tmp_path / "nonexistent.csv")


def test_load_raw_csv_missing_column(tmp_path: Path) -> None:
    csv_file = tmp_path / "bad.csv"
    csv_file.write_text("단어,설명\n조선,북한어\n", encoding="utf-8-sig")
    with pytest.raises(KeyError):
        load_raw_csv(csv_file)


def test_save_clean_csv_writes_file(tmp_path: Path) -> None:
    out = tmp_path / "out.csv"
    save_clean_csv(["조선", "평양"], out)
    with out.open(encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))
    assert rows[0] == ["용어"]
    assert rows[1] == ["조선"]
    assert rows[2] == ["평양"]


def test_save_clean_csv_raises_if_exists(tmp_path: Path) -> None:
    out = tmp_path / "out.csv"
    out.write_text("", encoding="utf-8")
    with pytest.raises(FileExistsError):
        save_clean_csv(["조선"], out)
