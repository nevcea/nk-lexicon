from pathlib import Path

from nk_lexicon.build_dict import build_user_dict, save_user_dict_csv
from nk_lexicon.preprocess import (
    clean_terms,
    deduplicate,
    load_raw_csv,
    save_clean_csv,
)

_RAW_CSV = Path("data/raw/북한용어사전.csv")
_CLEAN_CSV = Path("data/processed/terms_clean.csv")
_USER_DICT_CSV = Path("data/processed/user_dict.csv")


def resolve_paths(project_root: Path) -> dict[str, Path]:
    return {
        "raw": project_root / _RAW_CSV,
        "clean": project_root / _CLEAN_CSV,
        "user_dict": project_root / _USER_DICT_CSV,
    }


def main() -> None:
    project_root = Path(__file__).parent.parent
    paths = resolve_paths(project_root)

    raw_terms = load_raw_csv(paths["raw"])
    if len(raw_terms) == 0:
        raise ValueError("원본 데이터가 비어 있습니다")
    print(f"로드 완료: {len(raw_terms):,}개")

    clean = clean_terms(raw_terms)
    if len(clean) == 0:
        raise ValueError("전처리 후 데이터가 비어 있습니다")
    print(f"전처리 후: {len(clean):,}개 (▼{len(raw_terms) - len(clean):,}개)")

    deduped = deduplicate(clean)
    if len(deduped) > len(clean):
        raise ValueError("중복 제거 후 행 수가 증가했습니다")
    print(f"중복 제거 후: {len(deduped):,}개 (▼{len(clean) - len(deduped):,}개)")

    save_clean_csv(deduped, paths["clean"])
    print("terms_clean.csv 저장 완료")

    rows = build_user_dict(deduped)
    if len(rows) != len(deduped):
        raise ValueError("Mecab 변환 행 수가 일치하지 않습니다")

    save_user_dict_csv(rows, paths["user_dict"])
    print(f"user_dict.csv 저장 완료: {len(rows):,}개 항목")


if __name__ == "__main__":
    main()
