# 배색 시각 의미 리서치 패키지

2026-10-06 KST · 연구와 반영 계획 · 활성 데이터 채택 전

- [핵심 조사와 13개 계열의 결론](RESEARCH.md)
- [100개 상세 카드](SEMANTIC-CARDS.md)
- [색칩 검색·비교](PALETTE-ATLAS.html) — 데이터·구문 검사 완료, 실제 브라우저 표시 미검증
- [실행 단계와 완료 기준](IMPLEMENTATION-PLAN.md)
- [100개 후보 초안](CANDIDATE-DRAFTS.json) · [실제 원본과의 연결](RUNTIME-MAPPING.json)
- [공통 원리 16개](MECHANISM-CARDS.json) · [출처 37개와 제한](SOURCES.md)
- [64개 제안 회귀 사례](REGRESSION-PLAN.json) · [16개 제안 픽셀 평가](PIXEL-QUALIFICATION-PLAN.json)
- [형식 예시 4개](PROFILE-PROTOTYPES.json) · [313개 평면 색칩 계산](SWATCH-METRICS.json)
- [검증 결과](VALIDATION-REPORT.json) · [조사 시점 원본](CURRENT-DATA-AUDIT.json) · [연구 중 코드 변화](SOURCE-DRIFT.json)

이 폴더의 JSON은 연구 명세이며 활성 asset이나 요청별 candidate-pack가 아니다. 후보의 research_owner placeholder를 실제 frozen core의 owner/property로 치환하기 전에는 채택할 수 없다. 출처 확인, 원본 데이터, retrieval, 선택, 프롬프트, 원본 픽셀, 사용자 판단은 서로 다른 증거다.

전용 폴더의 빌드/검증을 재현하는 명령:

```sh
.venv/bin/python docs/research-evidence/photo-prompt/color-palette-semantics-20261006/build_research.py
.venv/bin/python docs/research-evidence/photo-prompt/color-palette-semantics-20261006/validate_research.py
```

실행 시 현재 loader와 원본 ID의 존재를 확인한다. 보존 검사는 최초 기록한 120개 파일과 비교하므로 이후 다른 작업이 변경되면 SOURCE_DRIFT를 보고한다. 해당 파일을 자동 수정하지 않는다.

atlas는 palette-atlas.template.html에 SEMANTIC-CARDS.json과 SWATCH-METRICS.json, SOURCES.json의 필요한 필드만 삽입한 자체 포함 HTML이다. 별도 외부 스크립트·네트워크 호출은 없다. 이 연구에서 브라우저 file URL 열기가 거부되어 HTTP 서버·다른 브라우저로 우회하지 않았다.
