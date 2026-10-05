# 고딕·장식 디테일 연구 패키지

상태: **RESEARCH_COMPLETE / ADOPTION_PLANNED / RUNTIME_AND_PIXELS_NOT_RUN**.

먼저 [RESEARCH.md](RESEARCH.md), 실행 범위는 [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)를 읽는다.

| 파일 | 내용 |
|---|---|
| [SEMANTIC-UNITS.md](SEMANTIC-UNITS.md) | 복원한 124개 항목 + 20개 보조 관계의 의미·가시 형태·혼동 경계 |
| [CANDIDATE-DETAILS.md](CANDIDATE-DETAILS.md) | 71개 후보의 owner·관계·전체 effects·기존 ID·채택 조건 |
| [TERM-DISPOSITIONS.md](TERM-DISPOSITIONS.md) | 모든 단위의 reuse/extend/optional/context/defer 결정 |
| [SOURCES.md](SOURCES.md) | 60개 출처와 접근 실패한 후속 문헌 1개; 접근 깊이 |
| [ADOPTION-MAP.json](ADOPTION-MAP.json) | 현재 기록과 후보 초안의 기계 판독 연결 |
| [BUNDLE-DRAFTS.json](BUNDLE-DRAFTS.json) | 12개 조합의 대안/선택/효과 합집합 규칙 |
| [REGRESSION-PLAN.json](REGRESSION-PLAN.json) | 92개 의미 probe, 22개 native 사례, 48개 이미지 파일럿 제안 |
| [PIXEL-QUALIFICATION-PLAN.md](PIXEL-QUALIFICATION-PLAN.md) | 원본 픽셀의 all-of 조건과 대체 실패 |
| [CHECKOUT-SNAPSHOT.json](CHECKOUT-SNAPSHOT.json) | 저작 인벤토리 당시 HEAD/manifest/source 해시 |
| [VALIDATION.json](VALIDATION.json) | 패키지 구조 검증과 실행하지 않은 증거층 |
| [MANIFEST.json](MANIFEST.json) | 연구 파일의 SHA-256 |

긴 참조 답변은 도구의 20,000자 한도로 끝부분이 잘렸다. 124개는 복원한 표 항목이며 원문 전체의 총 용어 수는 미확인이다. `GX` 보조 관계는 이번 연구자가 쓴 제안이다. 초안 JSON을 runtime assets에 복사하거나 구조 PASS를 후보 노출·픽셀 성공으로 해석하지 않는다.

재구성/구조 확인:

```bash
.venv/bin/python docs/research-evidence/photo-prompt/gothic-ornament-semantics-20261005/audit_existing.py
.venv/bin/python docs/research-evidence/photo-prompt/gothic-ornament-semantics-20261005/build_research.py
.venv/bin/python docs/research-evidence/photo-prompt/gothic-ornament-semantics-20261005/build_validation_plan.py
.venv/bin/python docs/research-evidence/photo-prompt/gothic-ornament-semantics-20261005/validate_package.py
```

인벤토리 재실행은 현재 authored snapshot을 새로 읽는다. 과거 snapshot을 runtime acceptance로 재해싱하지 않는다. 생성된 의미/후보/검증 문서는 위의 검토된 TSV 저작 파일에서만 재구성된다.
