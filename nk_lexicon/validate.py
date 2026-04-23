"""사용자 사전 적용 전/후 토큰화 결과 비교."""

from pathlib import Path
from typing import Any

import MeCab  # type: ignore[import-not-found]

_DIC_DIR = Path("/usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ko-dic")
_RC_FILE = Path("/etc/mecabrc")

_TEST_SENTENCES = [
    "협동농장에서 로동가요를 부르며 인민교원들이 모였다",
    "동무들이 인민경제계획에 따라 협동경제를 논의했다",
    "평양의 로동가치설을 바탕으로 인민교육체계를 정비했다",
]

_NK_TERMS = [
    "협동농장",
    "로동가요",
    "인민교원",
    "인민경제계획",
    "협동경제",
    "로동가치설",
    "인민교육체계",
]


def _parse(tagger: Any, sentence: str) -> list[tuple[str, str]]:
    result = []
    node = tagger.parseToNode(sentence)
    while node:
        surface = node.surface
        feature = node.feature.split(",")[0]
        if surface:
            result.append((surface, feature))
        node = node.next
    return result


def run_validation(user_dic_path: Path) -> None:
    if not user_dic_path.exists():
        raise FileNotFoundError(
            f"user.dic 없음: {user_dic_path}\n먼저 mecab-dict-index로 컴파일하세요."
        )
    base_args = f"-r {_RC_FILE} -d {_DIC_DIR}"
    tagger_default = MeCab.Tagger(base_args)
    tagger_with_ud = MeCab.Tagger(f"{base_args} -u {user_dic_path}")

    print("=" * 60)
    print("사용자 사전 적용 전/후 비교")
    print("=" * 60)

    for sentence in _TEST_SENTENCES:
        print(f"\n문장: {sentence}")
        tokens_before = _parse(tagger_default, sentence)
        tokens_after = _parse(tagger_with_ud, sentence)
        print(f"  적용 전: {tokens_before}")
        print(f"  적용 후: {tokens_after}")

    print("\n" + "=" * 60)
    print("북한어 단일 토큰 여부")
    print("=" * 60)

    all_pass = True
    for term in _NK_TERMS:
        tokens_before = _parse(tagger_default, term)
        tokens_after = _parse(tagger_with_ud, term)
        single = len(tokens_after) == 1 and tokens_after[0][1] == "NNP"
        status = "PASS" if single else "FAIL"
        if not single:
            all_pass = False
        print(
            f"  [{status}] {term!r:12s} "
            f"전: {[t for t, _ in tokens_before]} "
            f"→ 후: {tokens_after}"
        )

    print()
    print("결과:", "전체 통과" if all_pass else "일부 실패 — 위 FAIL 항목 확인")


if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    user_dic = project_root / "data" / "processed" / "user.dic"
    run_validation(user_dic)
