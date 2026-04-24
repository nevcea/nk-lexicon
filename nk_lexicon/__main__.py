import argparse
from pathlib import Path

from nk_lexicon.build_dict import build_user_dict, save_user_dict_csv
from nk_lexicon.preprocess import (
    clean_terms,
    deduplicate,
    load_raw_csv,
    save_clean_csv,
)

_PROJECT_ROOT = Path(__file__).parent.parent
_RAW_CSV = _PROJECT_ROOT / "data/raw/북한용어사전.csv"
_CLEAN_CSV = _PROJECT_ROOT / "data/processed/terms_clean.csv"
_USER_DICT_CSV = _PROJECT_ROOT / "data/processed/user_dict.csv"


def main(force: bool = False) -> None:
    raw_terms = load_raw_csv(_RAW_CSV)
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

    save_clean_csv(deduped, _CLEAN_CSV, overwrite=force)
    print("terms_clean.csv 저장 완료")

    rows = build_user_dict(deduped)
    if len(rows) != len(deduped):
        raise ValueError("Mecab 변환 행 수가 일치하지 않습니다")

    save_user_dict_csv(rows, _USER_DICT_CSV, overwrite=force)
    print(f"user_dict.csv 저장 완료: {len(rows):,}개 항목")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="기존 출력 파일 덮어쓰기")
    args = parser.parse_args()
    main(force=args.force)
