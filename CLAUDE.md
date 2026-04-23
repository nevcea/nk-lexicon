# Project

Python 기반 NLP 프로젝트입니다.  
북한어 데이터를 활용해 형태소 분석 보조 사전을 구축합니다.

## Stack

- Python
- uv
- ruff
- mypy

## Rules

- 변경은 최소 범위로 수행
- 기존 코드 스타일 우선
- 모든 새 코드는 타입 힌트 포함
- mypy 통과 필수
- 새 의존성 추가 최소화

- 지금 필요한 기능만 구현
- 미래 가능성을 위한 추상화 금지
- 함수로 충분하면 클래스 사용 금지
- 불필요한 클래스, 인터페이스, 레이어 추가 금지
- 한 번만 쓰이는 추상화 금지
- 요청되지 않은 리팩터링 금지

## Commands

- 설치: `uv sync`
- 실행: `uv run python -m <module>`
- 테스트: `uv run pytest`
- 포맷: `uv run ruff format .`
- 린트: `uv run ruff check . --fix`
- 타입체크: `uv run mypy .`

## Workflow

작업 전:

- 관련 코드 먼저 읽기

작업 후:

- ruff → mypy → pytest 순서로 검증

## References

- @pyproject.toml
- @.claude/rules/code-style.md
- @.claude/rules/testing.md
- @.claude/rules/nlp.md
- @.claude/rules/data.md
