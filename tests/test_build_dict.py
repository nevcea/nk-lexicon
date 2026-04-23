import csv
from pathlib import Path

import pytest

from nk_lexicon.build_dict import (
    build_user_dict,
    has_final_consonant,
    save_user_dict_csv,
    term_to_mecab_row,
)


def test_has_final_consonant_with_coda() -> None:
    # 국 (U+AD6D): 받침 ㄱ 있음
    assert has_final_consonant("국") is True


def test_has_final_consonant_without_coda() -> None:
    # 가 (U+AC00): 받침 없음
    assert has_final_consonant("가") is False


def test_has_final_consonant_non_syllable() -> None:
    # 자모 단독 문자 (한글 음절 블록 외)
    assert has_final_consonant("ㄹ") is None


def test_term_to_mecab_row_field_count() -> None:
    row = term_to_mecab_row("조선")
    assert len(row) == 12


def test_term_to_mecab_row_surface() -> None:
    row = term_to_mecab_row("평양")
    assert row[0] == "평양"


def test_term_to_mecab_row_left_id() -> None:
    row = term_to_mecab_row("조선")
    assert row[1] == "1786"


def test_term_to_mecab_row_right_id_coda() -> None:
    row = term_to_mecab_row("국")  # 받침 있음
    assert row[2] == "3546"


def test_term_to_mecab_row_right_id_no_coda() -> None:
    row = term_to_mecab_row("가")  # 받침 없음
    assert row[2] == "3545"


def test_term_to_mecab_row_cost_scales_with_length() -> None:
    # cost = -1000 * (len - 1): NNP→NNP 전이 비용(-956)을 넘어야 긴 용어 우선
    assert term_to_mecab_row("동무")[3] == "-1000"  # 2음절: -1000
    assert term_to_mecab_row("조선로동")[3] == "-3000"  # 4음절: -3000
    assert term_to_mecab_row("조선로동당")[3] == "-4000"  # 5음절: -4000


def test_term_to_mecab_row_pos_tag() -> None:
    row = term_to_mecab_row("조선")
    assert row[4] == "NNP"


def test_term_to_mecab_row_coda_field_true() -> None:
    row = term_to_mecab_row("국")
    assert row[6] == "T"


def test_term_to_mecab_row_coda_field_false() -> None:
    row = term_to_mecab_row("가")
    assert row[6] == "F"


def test_build_user_dict_length() -> None:
    terms = ["조선", "평양", "로동", "인민", "가나"]
    rows = build_user_dict(terms)
    assert len(rows) == 5


def test_save_user_dict_csv_writes_file(tmp_path: Path) -> None:
    out = tmp_path / "user.dic.csv"
    rows = build_user_dict(["조선", "평양"])
    save_user_dict_csv(rows, out)
    with out.open(encoding="utf-8") as f:
        written = list(csv.reader(f))
    assert len(written) == 2


def test_save_user_dict_csv_raises_if_exists(tmp_path: Path) -> None:
    out = tmp_path / "user.dic.csv"
    out.write_text("", encoding="utf-8")
    with pytest.raises(FileExistsError):
        save_user_dict_csv(build_user_dict(["조선"]), out)
