# 물 시각 의미 데이터 리서치·반영 계획

2026-10-06 · 원 대화 **물 관련 용어 조사**의 24개 분야, 345개 용어 행을 기반으로 작성했다. 후반부까지 읽기 전용 브라우저로 회수하고 관능·폭력·공포·문화 용어도 coverage에 유지했다.

**192개 연구 카드 → 시각 구조 117개 후보 초안, 분해할 형태 가족 45개, 맥락 의미 30개**로 정리했다. 공개 출처는 45개이며 본문·검색 excerpt·논문 abstract·제목 용례의 근거 수준을 구분했다. 후보 초안은 실제 owner/property·activation·registry 검증 전이다.

핵심 강화 방향은 물–소재 경계, 광원–수면–수광면, 같은 몸과 물선, 물길의 분기·합류, 생물·잠수 장비의 접합 관계다. 기존 ID와 guard를 보존하고 재사용할 의미와 다른 상태의 sibling을 구분한다.

- [리서치 본문](RESEARCH.md) — 현행 데이터 조사, 주요 메커니즘·오인 경계·근거 한계.
- [반영 계획](IMPLEMENTATION-PLAN.md) — P0/P1/P2 순서, 실제 source owner·중앙 manifest·component compiler·effects·index·후보팩·픽셀 검증.
- [192개 시각 의미 카드](SEMANTIC-CARDS.md) — 각 용어의 관찰 요소·같은 owner 관계·혼동 대상·출처·반영 경로.
- [117개 후보 초안](CANDIDATE-DRAFTS.json), [11개 검토 묶음](BUNDLE-DRAFTS.json), [현행 ID·파일 연결](RUNTIME-MAPPING.json).
- [공개 출처](SOURCES.md), [345행 원 설명](SEED-INVENTORY.json), [행별 coverage](SEED-COVERAGE.json), [원 조합 예시](SOURCE-COMBINATION-EXAMPLES.json).
- [회귀 계획](REGRESSION-PLAN.json), [원본 픽셀 계획](PIXEL-QUALIFICATION-PLAN.json), [compiler 형식 프로토타입](PROFILE-PROTOTYPES.json).
- [검증 결과](VALIDATION.json), [원본 보존 확인](PRESERVATION-CHECK.json), [집계](RESEARCH-STATS.json).

현재 저장소는 확장 source를 `photo_prompt_source_manifest.json`에 등록하고 `authored_components`에서 evidence·gate를 생성한다. 연구 JSON을 활성 자산에 직접 복사하지 않는다. 45개 family는 다른 의미를 aliases로 합치는 대상이 아니며, 30개 context는 이름만으로 anatomy·행위·노출·화학 품질을 강제하지 않는다.

이번 작업은 **리서치와 반영 계획 작성**이다. 이 연구는 활성 원본·index·후보팩·프롬프트 실행·이미지를 변경하거나 생성하지 않았다. 공유 checkout의 다른 변경으로 전체 무변경은 성립하지 않으며 [기준점 차이](LIVE-DRIFT-NOTE.md)를 남겼다. 4개 prototype의 형식 투영 확인은 runtime·픽셀 합격의 증거가 아니다.

재현·검증은 이 폴더의 산출물만 쓴다. `snapshot_current.py`는 기존 baseline snapshot을 덮어쓰지 않고 현재 원본을 읽어 catalog를 갱신한다. 해시 보존 검사는 열거된 live inputs 범위이며 shard·이미지·모든 untracked 파일의 완전한 백업 검사가 아니다.

```sh
python3 docs/research-evidence/photo-prompt/water-semantics-20261006/build_research.py
python3 docs/research-evidence/photo-prompt/water-semantics-20261006/validate_research.py
python3 docs/research-evidence/photo-prompt/water-semantics-20261006/snapshot_current.py --verify
```
