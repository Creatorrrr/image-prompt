# 색 의미·후보 데이터 반영 계획

2026-10-06 KST · 실행 전 계획 · 활성 원본/코드/인덱스/이미지 변경 없음

## 1. 목적과 작업 단위

기존 **64개 색 관계 프로필과 89개 전용 후보**를 기본 관계로 유지하면서, 실제로 다른 팔레트의 색 소유·영역 역할·재질 또는 광원 mechanism을 구체화한다. 연구 초안 100개를 전부 새 entry로 넣거나 스타일 이름별 hard 프로필 100개를 만드는 계획이 아니다.

원본 뜻과 stable ID를 먼저 대조하여 reuse / strengthen / narrow sibling / compose / context metadata / hold로 판정한다. 새 색 조합보다 **실제 같은 owner에 색이 남고 잘못된 광원·재질·감정·장소가 추가되지 않는 것**을 완료 기준으로 둔다.

## 2. 우선순위

|순서|범위|구체적 작업|완료 조건|
|---|---|---|---|
|P0 · 36개 카드|1–10, 11–12, 15, 20, 24, 27, 32–34, 36, 41, 45, 50, 57, 63, 65–67, 72–73, 75, 78–79, 88, 91–92|기존 뉴트럴·강조·금속·도자기·색광·gradient 관계를 재사용하고 명시적 owner와 속성 효과를 작성|선택된 모든 색 영역과 기하·mechanism의 evidence가 실제 core target과 연결|
|P1 · 53개 카드|나머지 일반·패션·자연·식품·그래픽·다크 응용|중복 팔레트 제거, 같은 carrier 패턴, 식품/용기와 소재 관계, 열린 역할·면적 변형|기존 일반 관계의 뜻을 좁히지 않으며 새 물체·사건·감정·제작 사실이 암묵적으로 추가되지 않음|
|P2 · 11개 카드|68, 89–90, 93–100|호텔 사례의 장면 대조, 문화적 출처/정확성, 기능 표지와 데이터 타입 검토|문서 사실·가시적 응용·법규/데이터 판정이 분리되고 미지원 의미는 보류|

P0의 36개도 사전 승인된 신규 데이터 목록이 아니다. 재사용만으로 충분하면 새로운 entry/profile 수는 0일 수 있다. 카드 우선순위의 실제 목록은 [RUNTIME-MAPPING.json](RUNTIME-MAPPING.json)이 권위다.

## 3. 실제 원본에 배치하는 원칙

기준 경로는 `skills/photo-prompt-image-generator/assets/`다. 현재 HEAD·dirty 상태와 source owner는 [CURRENT-DATA-AUDIT.json](CURRENT-DATA-AUDIT.json)에 있다. 실제 변경 시 이 정보를 새로 읽는다.

|반영 표면|현재 파일/슬롯|배치 원칙|
|---|---|---|
|일반 색 관계|photo_prompt_visual_obligations_color_relations.json|64개 기존 의미를 유지. 새 색 이름을 기존 generic relation의 hard alias로 붙이지 않음|
|일반 색 관계 후보|photo_prompt_color_relations_extension.json · color / color_grading / lighting|관계 재사용과 실제로 필요한 좁은 palette application을 분리|
|기존 이름형 팔레트|tags 또는 실제 extension owner의 기존 ID|원본 stable ID·가드·뜻을 보존. 필요한 경우 narrow sibling. root로 임의 이동하지 않음|
|금속·코팅·유약·직물|surface_material / texture와 현재 재질 원본|material effect가 있을 때만 별도 효과 선언. color 슬롯에 새로운 재질을 숨기지 않음|
|선택 색 예외·toning|현재 editing effects/lighting/color 원본의 실제 ID|물체 local color와 image grade scope를 별도 target/property로 작성|
|새 모듈이 꼭 필요한 경우|photo_prompt_palette_applications_extension.json **제안**|현재 존재·등록된 파일이 아님. 기존 원본으로 충분하지 않은 경우에만 생성하고 source manifest에 순서·kind·required를 등록|
|외부 근거·브랜드·시대·문화·제한|이 연구 폴더 / extension-maintenance의 증거 기록|runtime 데이터·검색 문장·최종 프롬프트에 출처 URL·연구 상태·원문·서술 전체를 복사하지 않음|

현재 loader는 `photo_prompt_source_manifest.json`의 ordered source inventory를 사용한다. SKILL의 별도 source list를 동시에 늘리거나 임의 root `extensions` 키 또는 폴더 glob을 가정하지 않는다.

## 4. 연구 명세를 활성 데이터로 투영하는 방법

1. **중복과 뜻 대조:** 원래 후보·profile을 전체 의미로 비교한다. 가까운 색만 같고 새 골드·재질·장소가 추가되는 후보는 완전 재사용하지 않는다. 81번의 가까운 골드 포함 팔레트는 이 비교의 명시적 negative다.
2. **owner 확정:** 이미 core에 있는 어느 인물·의상·소품·벽·무대·이미지 범위의 어느 속성인지 결정한다. 연구의 예시 물체를 요청으로 승격하지 않는다. `research_owner_*`를 actual canonical target으로 모두 치환하고 사실상 같은 owner를 서로 다른 이름으로 쪼개지 않는다.
3. **속성 경로 대조:** 예를 들어 의상색은 실제 `main_subject / wardrobe.color`, 컵 표면색은 실제 컵 target의 surface color 경로에 대응한다. 정확한 경로는 현재 core가 권위이며 이 문자열 예시는 consumer 지원의 증거가 아니다. parent/child overlap과 같은 소유의 다른 dimension 우회도 검사한다.
4. **효과 완전 선언:** 국소 색 변경만 있으면 color 효과다. 패턴 구조·투명도·재질·광원·보정·구도를 바꾸면 해당 추가 dimension/property를 모두 선언한다. 기존 반사 금속을 다른 색으로 조정하는 선택과 평면을 새 반사 금속으로 만드는 선택을 구분한다.
5. **component와 relation:** 현재 `photo-authored-visual-components/v1` 또는 후보 `concept_units / relations`를 사용한다. 선택한 각 color owner와 관계에 evidence phrase·gate를 연결한다. 독립 역할·역방향·유사 표현의 false substitute를 유지한다.
6. **검색과 권한:** 긍정적 관찰 문장을 corpus로 넣되 부정 예시·출처·연구 상태·고유 브랜드 사례를 검색 답안 키로 섞지 않는다. 색 조합 이름은 advisory discovery에 사용한다. hard duty는 실제 요청자 근거 또는 명시적 opt-in selection에만 연결한다.
7. **특수 문맥:** 89–94의 문화적 사실은 근거 메타데이터에 둔다. 95–97의 실제 기능 판정과 98–100의 데이터 의미는 generic color profile의 새 alias로 활성화하지 않는다. 수치 데이터의 정확한 도표가 필요하면 제공 데이터를 표준 plotting 도구로 확인하는 별도 작업이 적합하다.
8. **기존 계약 보존:** 전체 요청 해석과 독립 core 동결 후 retrieval 순서를 유지한다. pre-core neutral feature catalog 또는 전역 프롬프트로 이 100개 예시를 미리 주입하지 않는다.

## 5. 단계별 실행과 제출 증거

### 단계 A — 새 기준과 채택 목록

구현 시점 HEAD·dirty paths·source manifest·실제 로드된 ID·원본 해시를 다시 기록한다. 현재 다른 작업이 있는 주 checkout의 상태를 reset/stash/덮어쓰기하지 않는다. 구현 격리가 필요하면 적합한 기존 worktree를 확인하고 별도 checkout을 사용한다.

100개 카드마다 최종 reuse / strengthen / sibling / new / compose / metadata / hold를 결정한 adoption manifest를 작성한다. source file·stable ID·slot·actual owner/property·수용한 effect·받지 않은 effect·source-supported claim을 기록한다.

제출: 새 snapshot, 최소 채택 목록, 이전 의미와 ID의 보존 대조, held-case ledger.

### 단계 B — P0 원본과 좁은 효과

처음에는 다음 비교가 실제로 효과를 다루는지 확인한다.

- 8번: 뉴트럴 바탕/코발트 owner와 강조 범위.
- 9/15/78번: 색과 반사·투과의 material carrier.
- 65/66/73번: 물체 배색과 서로 다른 빛의 수신 geometry.
- 36/79번: 같은 표면의 공간 gradient와 tonal mapping 혼동.
- 50번: 코발트 컵과 커피/크림의 owner 분리.
- 91/92번: 같은 도자기 몸체와 문양 영역.

[PROFILE-PROTOTYPES.json](PROFILE-PROTOTYPES.json)의 형식 검사는 출발점이다. 활성 registry validation·actual owner·hard activation·pack·runtime을 통과한 증거로 간주하지 않는다.

제출: authored diff, actual owner binding trace, component compiler·candidate effect 검사, source maintenance hash와 모든 선택 evidence/gate 목록.

### 단계 C — P1 및 P2

P1은 가깝지만 다른 재료/계열에 쓰이는 배색의 중복을 줄이고 같은 carrier 패턴과 식품 경계를 보강한다. 단순 label 확장은 실제 관찰 관계를 추가하지 않으면 채택하지 않는다.

P2에서는 호텔의 특정 시대/장면·의상, 체크의 정확한 source scope, 단청의 건축물/보고서 표, 문화적 방위, 실제 표지의 관할과 문구, 데이터 타입/범례/값 관계를 별도로 검토한다. 확인되지 않은 사실을 삭제해서 문제가 해결된 것으로 보고하지 않고 좁은 시각 응용과 보류 사실을 나누어 기록한다.

제출: 보충 source receipt, 적용 조건과 보류 이유, 새 slot/schema가 정말 필요한지의 영향 분석.

### 단계 D — 파생 인덱스와 후보 노출

원본 채택 이후 semantic index와 visual profile index를 재생성한다. provider/model/dimensions와 전체 positive input text가 일치하는 기존 vector만 재사용한다. 아래는 **구현 단계의 명령 예시**이며 이번 연구에서 인덱스를 생성하지 않았다. CLI 옵션은 현재 `--help`로 확인했다.

```sh
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_semantic_index.py --dry-run
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_semantic_index.py --batch-size 1 --progress --keep-stale-generations
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py --batch-size 1 --cache-index skills/photo-prompt-image-generator/assets/photo_prompt_visual_profile_index.json
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py --check
```

새 manifest가 내구적으로 기록되고 참조 shard checksum을 확인할 때까지 이전 generation을 보호한다. 생성 index를 손으로 편집하거나 ours/theirs로 합치지 않는다. 의미 text가 같아도 policy·exact lookup·source hash가 바뀌면 재생성 범위를 현재 builder에서 확인한다.

사전 동결 core로 baseline/treatment 후보팩을 만들어 “hit → exposed candidate → selected actual effect → literal prompt evidence”를 각각 저장한다. 모든 후보를 거절해 baseline을 유지하는 경우도 기록한다.

제출: source/index/shard identity report, exposure/selection trace와 pack hash. 아직 native pixel 개선 증거는 아니다.

### 단계 E — 의미·검색·효과 회귀

[REGRESSION-PLAN.json](REGRESSION-PLAN.json)의 64개 계획 사례를 기준으로 적합한 기존 suites와 별도 동결한 구어체 holdout을 실행한다. 작성자가 본 카드 문장을 그대로 반복한 테스트를 generalization 증거로 삼지 않는다. 기존 holdout 의미와 color_coding·시간/측정 개념의 제외 경계를 보존한다.

```sh
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py
.venv/bin/python -m unittest tests.test_photo_color_relations tests.test_photo_lighting_color_owner_data_cleanup tests.test_photo_lighting_visual_semantics
.venv/bin/python -m unittest tests.test_photo_candidate_semantics tests.test_photo_visual_profile_retrieval tests.test_photo_positive_retrieval tests.test_photo_bm25f_retrieval
.venv/bin/python -m unittest tests.test_photo_authorial_core_v6 tests.test_photo_core_retrieval tests.test_photo_semantic_index tests.test_photo_visual_profile_shards
```

현재 실제 존재하는 모듈을 제시했다. 변경 범위가 source registration까지 포함하면 `tests.test_photo_structure_maintenance`도 포함한다. 새로운 실패·여러 독립 route의 영향·해결되지 않은 회귀 위험이 있으면 full discovery로 넓힌다. 연구 문서만 작성한 이번 작업의 검증과 위 명령을 실제 실행한 것으로 혼동하지 않는다.

제출: 최초 실패와 수정 후 결과, holdout 고정 해시, 사용자 재정의·부정·다른 owner·부분 lock·advisory hit의 강제 방지 결과.

### 단계 F — 원본 픽셀 비교와 사용자 판단

[PIXEL-QUALIFICATION-PLAN.json](PIXEL-QUALIFICATION-PLAN.json)의 16개 설계 가운데 P0 mechanism부터 진행한다. synthetic scenario는 실제 사용자의 요청/수락으로 위장하지 않는다. 필요한 현재 사용자 이미지 요청이 있거나 별도로 승인된 평가 범위에서 수행한다.

A는 후보 없는 독립 baseline, B는 기존 데이터, C는 채택한 좁은 데이터 diff다. 같은 frozen request/core/control을 쓰되 도구가 지원하지 않는 seed를 동일하게 사용했다고 쓰지 않는다. 모든 attempt·exact prompt/runtime bytes·모델·출력·SHA-256을 보존한다.

thumbnail은 색 역할·영역·주요 owner를, native pixels는 같은 carrier 경계·재질 cue·광원 footprint·selected scope를 검사한다. 필수 gate를 빠뜨리지 않으며 `partial_is_fail`을 유지한다. 정밀 색 일치가 중요한 경우 출력 색 공간·ICC·화이트밸런스와 평가 영역을 기록하고 미리 정한 색 기준을 사용한다.

사용자의 좋아함·의도 달성·기준보다 개선됨은 별도 판단이다. prompt audit·semantic retrieval·단일 좋은 이미지가 대신할 수 없다.

제출: 실제 n, 각 attempt의 all-gate review, A/B/C 비교와 한계, 실제 사용자 판단 상태.

## 6. 최종 반영 완료 조건

- 중복 제거·기존 의미·source ownership이 보존된다.
- placeholder가 0개이며 실제 owner/property로 모든 채택 효과가 설명된다.
- broad palette·감정·브랜드·스타일 이름과 approximate retrieval가 hard 권한을 만들지 않는다.
- 명도/채도/물체색/빛/보정/재질/패턴/데이터 의미가 서로 대체되지 않는다.
- 인덱스가 채택 원본과 일치하고 별도 core에서 실제 노출·선택·literal evidence가 추적된다.
- 의미·lock·부정·문맥·동결 holdout과 필요한 기존 checks를 통과한다.
- 이미지 효과를 주장하는 항목은 saved native pixels의 모든 필수 gate를 통과하고 사용자 판단은 별도로 기록된다.
- 보류 항목은 보류인 채 남아 있으며 수량을 채우기 위해 활성화하지 않는다.

이번 연구의 결과물은 이 계획을 실행할 수 있게 만드는 자료다. 활성 데이터 적용·embedding 호출·생성 이미지·commit·push·PR·배포는 수행하지 않았다.
