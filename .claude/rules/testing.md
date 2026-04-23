# Testing

- pytest 사용
- 새 기능에는 최소 1개 테스트 필수
- 버그 수정 시 회귀 테스트 필수

## Principles

- 구현이 아니라 동작을 검증
- 입력 → 출력 기준으로 테스트 작성
- edge case 포함

## Rules

- 외부 의존성은 mock 또는 fixture로 격리
- 테스트는 빠르고 결정적이어야 함 (flaky 금지)
- 한 테스트는 하나의 행동만 검증
- 의미 없는 테스트 금지 (assert 없이 통과하는 코드 금지)

## Structure

- tests/ 디렉터리 사용
- 파일명: test_*.py
- 함수명: test_*

## Coverage

- 핵심 로직은 반드시 테스트 포함
- 파싱/변환 로직은 우선적으로 테스트