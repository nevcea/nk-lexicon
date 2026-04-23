# Code Style

- PEP 8 준수
- 모든 함수에 타입 힌트 작성
- mypy 오류 0 유지

## Naming
- 변수/함수: snake_case
- 클래스: PascalCase
- 상수: UPPER_CASE

## Structure
- 함수는 짧고 단일 책임 유지
- 깊은 중첩(if/for) 지양
- 매직 넘버 금지 → 상수로 분리

## Imports
- 표준 라이브러리 우선
- wildcard import 금지

## Comments
- “왜” 필요한지 설명
- 불필요한 주석 금지

## Error Handling
- except Exception 남용 금지
- 에러 메시지는 구체적으로 작성