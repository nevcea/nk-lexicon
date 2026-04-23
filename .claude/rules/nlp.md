# NLP Rules

## Goal
- 북한어를 형태소 분석에서 하나의 토큰으로 인식하도록 처리
- OOV 최소화

## Approach
- 사용자 사전 기반 처리
- 모든 단어 기본 NNP 처리

## Data Handling
- "용어" 컬럼만 사용
- 중복 제거 필수
- 공백/특수문자 정리

## Implementation
- 사전 → Mecab user dictionary 변환
- 적용 전/후 결과 비교 코드 작성

## Validation
- 최소 3개 문장 테스트
- 토큰 분해 여부 확인

## Constraints
- 과도한 모델 학습 금지 (초기 단계)
- 규칙 기반 접근 우선