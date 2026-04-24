import csv
from pathlib import Path

_HANGUL_BASE = 0xAC00
_HANGUL_END = 0xD7A3
_JONGSEONG_COUNT = 28

# mecab-ko-dic left-id.def: NNP,*,*,*,*,*,*,*
_NNP_LEFT_ID = "1786"
# mecab-ko-dic right-id.def: NNP,*,F,* / NNP,*,T,*
_NNP_RIGHT_ID_NO_CODA = "3545"
_NNP_RIGHT_ID_CODA = "3546"

# cost = -_COST_PER_SYLLABLE * (len - 1)
# NNP→NNP 전이 비용이 -956이므로, 분해 경로를 이기려면 M > 956 필요
_COST_PER_SYLLABLE = 1000


def has_final_consonant(term: str) -> bool | None:
    """마지막 글자 받침 여부. 한글 음절 블록 외 문자면 None 반환."""
    if not term:
        return None
    last = ord(term[-1])
    if _HANGUL_BASE <= last <= _HANGUL_END:
        return (last - _HANGUL_BASE) % _JONGSEONG_COUNT > 0
    return None


def term_to_mecab_row(term: str) -> tuple[str, ...]:
    coda = has_final_consonant(term)
    if coda is True:
        coda_field = "T"
    elif coda is False:
        coda_field = "F"
    else:
        coda_field = ""

    cost = str(-_COST_PER_SYLLABLE * (len(term) - 1))
    right_id = _NNP_RIGHT_ID_CODA if coda is True else _NNP_RIGHT_ID_NO_CODA
    return (
        term,  # 0: 표층형
        _NNP_LEFT_ID,  # 1: 좌문맥ID
        right_id,  # 2: 우문맥ID
        cost,  # 3: 비용
        "NNP",  # 4: 품사태그
        "고유명사",  # 5: 의미분류
        coda_field,  # 6: 받침유무
        term,  # 7: 원형
        "",  # 8: 독음
        "",  # 9: 발음
        "NNP",  # 10: 타입
        "NNP",  # 11: 첫번째품사
    )


def build_user_dict(terms: list[str]) -> list[tuple[str, ...]]:
    return [term_to_mecab_row(term) for term in terms]


def save_user_dict_csv(
    rows: list[tuple[str, ...]], path: Path, *, overwrite: bool = False
) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"출력 파일이 이미 존재합니다: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)
