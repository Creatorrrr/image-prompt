# 지적 인상·탐구 활동 연구 패키지

「용어 조사 정리」의 **140개 키워드**를 바탕으로 시각 의미·후보팩 데이터를 보강하기 위한 연구와 반영 계획을 작성했다. 조사일은 2026-10-05다.

**핵심 제안:** 기존 표정·포즈·안경·촬영 원자를 재사용하고, 손·시선·도구가 특정 자료에 연결되는 관계와 자료 사이의 같은 항목 대응을 우선 강화한다. 지능·지향·신분·정신 건강을 외양으로 판정하거나 시간 전환을 단일 스틸의 성공으로 세지 않는다.

## 먼저 읽을 문서

- [상세 연구 결과](RESEARCH.md): 의미군별 근거, 현재 데이터, 핵심 보강 단위와 검증 경계.
- [반영 계획](IMPLEMENTATION-PLAN.md): P0–P6 단계, 실제 owner·등록·인덱스·검증·이미지 파일럿까지의 순서와 종료 조건.
- [140개 용어별 결정](TERM-DECISIONS.md): 각 용어의 뜻, 관찰 제안, 혼동 경계, 기존 ID, 초안 연결.

## 검토 가능한 데이터

| 파일 | 내용 |
|---|---|
| [SOURCE-KEYWORDS.json](SOURCE-KEYWORDS.json) | 원 대화의 140개 용어·정의·시각 분해. 원 제안과 검증된 사실을 구별 |
| [SOURCES.json](SOURCES.json) | 외부 근거 46개, 본문/검색 발췌 읽기 상태, 지원 주장과 한계 |
| [TERM-DECISIONS.json](TERM-DECISIONS.json) | 140개 결정, 기존 후보의 실제 파일·slot·ID·효과 연결 |
| [CANDIDATE-DRAFTS.json](CANDIDATE-DRAFTS.json) | 관계·구성 초안 78개, 컴포넌트·소유 역할·directed 관계·slot·제안 owner |
| [ADOPTION-MAP.json](ADOPTION-MAP.json) | 78개 초안의 구현 단계와 재사용·신규 관계 검토 방향 |
| [REGRESSION-PLAN.json](REGRESSION-PLAN.json) | 의미·잠금·문맥·소유 검증 사례 82개, 원본 이미지 all-of 판정 묶음 16개 |
| [EXISTING-COVERAGE.json](EXISTING-COVERAGE.json) | authored 파일 83개의 exact 라벨 조사. 22/140은 의미 충족률이 아님 |
| [AUTHORING-INVENTORY.json](AUTHORING-INVENTORY.json) | 전체 ID 목록과 재사용 후보 ID 60개/62레코드, 프로파일 7개의 조사 시점 본문 |
| [CHECKOUT-SNAPSHOT.json](CHECKOUT-SNAPSHOT.json) | 조사 시점 HEAD·dirty 상태·authored 파일 해시 |
| [PACKAGE-COUNTS.json](PACKAGE-COUNTS.json) | 용어·근거·초안·재사용 수량과 연구 상태 |
| [VALIDATION.json](VALIDATION.json) | 패키지 무결성 검증과 live source 차이. 실제 실행 검증과 분리 |
| [MANIFEST.json](MANIFEST.json) | 패키지 파일의 SHA-256 |

## 현재 상태

연구 결과·반영 계획·초안 데이터·검증 계획을 준비하고 패키지 참조·구조를 검증했다. **실제 assets·후보팩·index·runtime에는 아직 반영하지 않았다.** 82개 구현 프로브와 16개 이미지 묶음도 실행 전이다. 연구의 pose/gesture/scene graph predicate와 효과 차원은 검토용이며 현재 runtime schema로 바로 입력할 수 없다. 실제 `dimension/target/property`는 채택 시 grounded core와 전체 효과에 맞게 확정해야 한다.

기존 공유 체크아웃의 다른 수정은 보존했다. 조사 시점 데이터와 현재 데이터가 다르면 구현 전에 중복·owner·해시를 다시 확인한다. 특정 시대의 선비 고증, 장치별 측정 정확성, 합법 기보, 악보·번역 정답, 원본 이미지의 의미 충족은 별도 근거·실행 검증이 남아 있다.

## 재현

현재 패키지는 이미 조사한 snapshot을 보존한다. 다음 명령은 이 폴더의 산출물을 갱신하므로 재현·후속 구현에서 의도적으로 실행한다. active assets를 쓰거나 embedding·이미지 생성 도구를 호출하지 않는다.

```sh
.venv/bin/python docs/research-evidence/photo-prompt/intellectual-semantics-20261005/build_research.py
.venv/bin/python docs/research-evidence/photo-prompt/intellectual-semantics-20261005/build_validation_plan.py
.venv/bin/python docs/research-evidence/photo-prompt/intellectual-semantics-20261005/validate_package.py
```

현재 checkout으로 inventory를 다시 조사할 때만 `audit_existing.py`를 먼저 실행한다. 기존 snapshot을 갱신한다는 점을 명시하고, 이어서 위 세 명령으로 표·초안·검증을 재생성한다. 본문에 적힌 snapshot 수량과 검증기의 기대 수량도 새 조사에 맞게 검토·갱신해야 한다. 재사용 ID가 바뀌거나 사라졌다면 build가 실패하므로 의미를 검토한 뒤 연구 결정을 갱신한다.
