# 셀카 포즈 연구 결과 반영 계획

2026-10-08 KST · 실행 전 계획 · 기존 authoring/core/pack 계약 보존

이번 반영의 목표는 같은 이름의 셀카를 반복 검색하는 데서 그치지 않고, **요청 문맥에 맞는 표정·손 모양·소유·접촉·촬영 구조를 찾고 채택한 뒤 그 구성이 프롬프트와 이미지에 남도록 하는 것**이다. 이 문서는 작업 대상·선후 관계·완료 기준을 정한 계획이다. 저장만으로 런타임 반영이나 이미지 실행을 시작한 것은 아니다.

## 1. 기존 정의와 변형부터 결정

`original-keywords.json`의 180개 번호 행과 20개 요약 검색행을 계속 유지한다. `keyword-routing.json`은 연구 단위를 찾는 지도이며 실행용 exact alias 표가 아니다. 원문 번호를 유지해야 대표 변형만 보강한 뒤 나머지 범위를 완료한 것으로 잘못 보고하지 않는다.

| 우선 결정 | 구체 작업 | 종료 기준 |
|---|---|---|
| 입 중립형 눈웃음 | `ae_smize`의 입꼬리 상승을 유지하고 다른 입 형태의 후보/프로필을 분리 | 두 변형의 눈·입 조건과 한국어/영어 표현이 서로 덮어쓰지 않음 |
| 파우트·덕페이스·입술 틈 | 작은 돌출·강한 pucker·parted lips, Gen Z pout/Gen Z stare의 맥락을 구분 | 일반 pout·무심함·세대 이름이 다른 표정의 필수 의무로 확대되지 않음 |
| 물리 거울 | 현재 단일 성인 프로필의 scope를 확인하고 기본 반사 구조와 연령/인물 수 제약을 분리 | 일반 셀카·다인 거울·특정 성인 장면을 각각 올바른 scope로 처리 |
| 손가락 하트·고양이 하트 | 손가락 교차형·양손 빈 공간형·귀 봉우리형을 분리. 56은 실제 대표 예시 확인 | 이름과 손가락 구성 동등성이 확인되기 전 bare 이름 hard activation을 채택하지 않음 |
| 밤비·무릎 앉기 | `pv_heel_sit`의 실제 성분을 활용하되 기존 bare bambi activation 제외를 유지 | 하체 배치의 재사용과 이름 등록을 서로 다른 결정으로 기록 |
| 다중 선택 변형 | 93의 폰 위/옆, 126의 한/양팔, 133의 한 손/두 손 책 그립, 135의 립/브러시/퍼프, 156의 손목 교차/머리 뒤, 157의 로브/타월 구분 | OR 변형을 한 프로필의 AND 필수 구성으로 합치지 않음 |

`reuse-plan.json`의 119개 참조는 현재 원본에 실재하는 검토 입구다. 손 형태 하나가 같아도 소유 대상·접촉 대상·좌면 지지·손 개수·시점이 다르면 전체 후보를 재사용하지 않는다. 특히 서 있는 발목 교차에 앉은 발목 교차의 pelvis-seat 조건을 가져오지 않는다. 원본 대조가 남은 22개는 연구 카드의 literal 형태를 출발점으로 기존 ID를 추가 탐색하거나 필요한 소단위만 새로 작성한다.

결정 산출물은 번호별 `reuse / extend_equivalent_context / new_variant / compose / advisory_context / deferred_name`과 이유다. 신규 항목 수를 목표로 두지 않는다. 정의·대상·효과가 달라지면 기존 ID의 별칭을 넓히는 대신 새 변형을 만든다.

## 2. 촬영 구조와 작은 성분을 먼저 작성

세 촬영 방식을 기본 의미 단위로 둔다.

| 촬영 방식 | 구성과 손 역할 | 픽셀·실행 기록의 범위 |
|---|---|---|
| 직접 handheld selfie | 전면/후면은 기기별 지정. 촬영 손 하나, 나머지 손은 포즈·소품·지지 중 가능한 역할 | 기기가 최종 화면에 반드시 보이지는 않음. 팔·얼굴·깊이 단서와 입력 capture 조건을 나눠 심사 |
| physical mirror capture | 거울, 같은 반사 공간의 인물과 폰, 손 그립, 기기 가림, 지정한 시선 대상 | 물리 반사와 preview/저장 미러링을 구별. 작은 눈동자 시선은 원본에서도 판단 보류 가능 |
| fixed self-portrait | 안정된 장치·타이머/리모컨 등 촬영 조건. 양손 포즈 가능 | 타이머·실제 촬영자·셔터 원인은 실행 조건이다. 장치를 이미지에 추가해야 한다는 요구가 아님 |

이 세 가지의 상호 배타적인 capture 상태를 장면마다 해결한 뒤 포즈 성분을 붙인다. 같은 사진에 직접 전면 셀카와 물리 거울 촬영을 동시에 자동 채택하지 않는다. 두 사람이 한 손씩 하트를 만들면 남는 손 촬영이 가능하고, 한 사람이 양손 하트를 만들면 그 사람의 손은 촬영에 남지 않는다는 인물별 역할 계산을 넣는다.

P0 데이터는 04–08 눈·입 혼동, 21–30 접촉면·지지, 34–36 가림, 41–58 V·하트 손가락, 71–79 높이·롤·크롭, 81–87 깊이 투영, 91–99 거울·시선, 143·147–148 손 소유/반사/컷, 167–168 손가락 종류, 175–180 빛·반사/투과·그림자부터 검토한다. 나머지 전신·휴식·소품·성인 패션·액션도 연구 범위를 유지하며 기존 자세 성분을 연결한다.

## 3. 원본 데이터에 좁게 연결

예상 새 소스는 다음 두 파일이다. 이름은 현 manifest와 충돌 여부를 실행 시작 때 다시 확인한다.

| 예상 대상 | 반영 내용 | 주의할 계약 |
|---|---|---|
| `skills/photo-prompt-image-generator/assets/photo_prompt_selfie_pose_extension.json` | 검토 후 채택한 slot entries와 조합 정보 | 연구 wrapper·출처 상태·미검증 성능 문구를 runtime entry로 복사하지 않음 |
| `skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_selfie_pose.json` | 검토 후 채택한 exact terms, authored components, 혼동 경계 | derived gates/evidence fields를 원본과 중복 저작하지 않음 |
| 기존 pose/acting-expression/portrait-composition/lighting 소스 | 실제 동등한 표현·문맥만 좁게 보강 | ID의 소유·effect·보호 조건을 넓히는 변경은 별도 변형으로 분리 |
| `skills/photo-prompt-image-generator/assets/photo_prompt_source_manifest.json` | candidate/visual 소스 kind·required 여부·load order 등록 | `SourceInventory.validate()`가 미등록 소스와 누락 required 파일을 검출하므로 manifest 등록을 함께 수행 |
| extension maintenance 기록 | provenance·원문 번호·출처 지지 범위·변형 결정 | runtime 양의 검색 문장에 출처/ID/부정 예시/오케스트레이션 정보를 넣지 않음 |

현재 원본을 다시 읽어 `affected_dimensions`와 `affected_properties`를 실제 효과에 맞춘다. 연구의 `main_subject`, `partner_subject`, `declared_actors`, `capture_camera`, `image` 같은 역할 표기는 설계용 이름이다. 실제 frozen core의 actor/target에 매핑되어야 하며 문자열이 들어 있다는 이유만으로 바인딩 완료로 세지 않는다. 손가락 구성, 접촉 대상, 머리 방향, 시선 대상, 폰 위치, 크롭, 렌즈·노출, 광원, 의상/헤어/액세서리 배치는 각각 보호해야 할 property다.

현재 slot 기본 scope가 비어 있거나 다른 차원을 갖더라도 전역 slot 정책을 편의상 넓히지 않는다. 예를 들어 capture/무빙 정보는 새 entry의 effect를 명시하고 그 효과가 허용되는 문맥만 채택한다. hair tuck/포니테일/안경/모자/긴 소매는 기존 장면에 해당 대상이 있다는 조건을 먼저 확인한다. 후보가 그 대상을 새로 추가하거나 참조 외형을 바꾸지 않는다.

입·눈·손가락의 미세한 형태는 actor 기준 좌우를 쓰고, image 기준 좌우 및 저장 미러링 여부와 구분한다. 다인 포즈는 각각의 손·목·팔꿈치·무릎을 특정 actor에 연결한다. 네 컷은 패널마다 count와 identity를 따로 유지한다. 반사 수를 actor 수로 세지 않는다.

**활성화 기준은 이름의 명확성보다 문맥과 요청 우선이다.** 명시된 사용자 정의·부정·제외·참조 외형·소유 대상이 우선한다. 정확한 이름도 현재 문맥에서 그 뜻으로 사용됐는지 확인해야 한다. 이름이 없는 한국어/영어 관찰 문장은 의미 검색으로 후보를 노출하되 그 유사도만으로 hard obligation을 만들지 않는다. broad ‘무심한/귀여운/시크한/빌런/관능적’은 하나의 기하를 강제하는 alias가 아니다.

`candidate-proposals.json`의 초안을 자동 통째로 import하지 않는다. `visual-profile-proposals.json`의 컴파일 성공 역시 exact terms 등록 승인이나 실제 owner 매핑 완료가 아니다. 자연 한국어 성분 표현이 현재 31개 프로필군에 들어 있으므로 나머지 채택 대상도 같은 형태를 보존하는 표현을 작성하고 혼동 예시와 함께 검토한다.

## 4. 파생 인덱스와 runtime를 함께 재생성

authored sources와 manifest를 정한 뒤 두 인덱스를 같은 inventory로 재생성한다. 바뀐 text의 벡터를 기존 ID가 같다는 이유만으로 재사용하지 않는다. text·provider·model·dimensions 및 현재 recipe와 일치할 때만 호환 캐시를 재사용한다. 신규 문장의 embedding이 실제 필요한 경우 그 호출과 비용을 기록한다. 이번 연구에는 embedding 호출이 없다.

채택 원본의 `validate_candidate_entries`·`validate_visual_profile_source`·`compile_visual_profile` 순수 계약과 `SourceInventory.validate()` 검사를 먼저 통과시킨다. 전체 dictionary validator는 visual profile index도 확인하므로 새 원본을 등록한 후에는 두 인덱스를 재생성한 뒤 실행한다.

현재 코드에서 확인한 실행 인터페이스는 다음과 같다. 실행용 checkout의 CLI와 계약을 다시 확인한 뒤 사용한다. 아래는 이번 작업에서 실행한 명령이 아니다.

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_semantic_index.py --dry-run
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_semantic_index.py --no-runtime-publication
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py --no-runtime-publication
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py --check --no-runtime-publication
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py --no-runtime-publication
.venv/bin/python skills/photo-prompt-image-generator/scripts/publish_photo_runtime_snapshot.py
```

`--dry-run`은 계획 메타데이터 확인이다. index build·`--check`·runtime publication·실제 검색은 서로 다른 확인이다. validator·두 인덱스 빌더·`--check`에는 게시를 막는 옵션을 명시한다. semantic/visual 인덱스와 BM25F 양의 검색 표면, source inventory의 hash·recipe를 맞춘 뒤 마지막 publication 명령으로 runtime snapshot을 게시하고 그 결과물을 재검증한다. publication의 기본 source root는 현재 skill root이며, 별도 checkout에서 실행하면 그 checkout의 경로를 확인한다. 중단된 maintenance revision을 명시적으로 복구하는 `--complete-update`는 정상 게시 절차에 넣지 않는다. index의 파생 shard를 이름만 보고 삭제하지 않는다.

검색에는 긍정적 형태·소유·위치 표현을 넣고, contrast·거부 예시·출처·ID는 양의 유사도를 만드는 자료로 사용하지 않는다. 파일 추가만으로 candidate exposure나 최종 prompt 반영이 완료됐다고 주장하지 않는다.

## 5. 검색·채택·프롬프트를 실제로 확인

`validation-case-plan.json`은 36개 혼동쌍, 12개 부정/정의/문맥, 12개 property 잠금, 8개 별도 언어 holdout 설계로 68개 사례를 담는다. 이번 순수 계약 검사에서 일부 property 잠금 함수를 실행했지만 전체 68개의 end-to-end 결과는 아직 없다. 별도 작성자가 만들기로 한 holdout 문장은 현재 연구 저자의 사례와 분리한다. 현재 PAIR 사례를 독립 holdout으로 부르지 않는다.

실제 흐름을 유지한다. **요청 전체 문맥과 creative controls를 해결 → 후보 자료 없이 baseline/core를 작성·고정 → post-core retrieval → 후보/시각 프로필/의무 확인 → 명시적 채택 → 최종 literal과 audit** 순서다. 이 연구 카드·초안·기존 테스트를 초기 core의 숨은 후보 메뉴로 사용하지 않는다. 테스트를 위해서는 같은 독립 core와 같은 요청을 두 데이터 조건에서 비교한다.

| 단계 | 기록할 실제 증거 | 실패 시 판단 |
|---|---|---|
| 데이터 등록 | 채택 원본 ID·source hash·slot/property·manifest | 파일은 있지만 등록되지 않으면 미반영 |
| 검색 노출 | 실제 질의와 language·문맥·top-k 내 올바른 후보 ID·순위·경쟁 후보 | 이름 hit만 있고 손/접촉형이 틀리면 실패. 인덱스/검색식 문제와 데이터 부족을 분리 |
| 후보 채택 | pack에 노출된 ID와 chosen IDs, 거부 이유·lock·scope | 노출됐어도 선택되지 않으면 후보 기여를 주장하지 않음 |
| literal 반영 | 선택한 손·대상·접점·가림·촬영 조건의 실제 prompt 문장과 binding | label만 남고 구체 관계가 사라지면 실패 |
| prompt/runtime audit | 원본 pack·core·request·transport와 literal binding | 문구가 있어도 pre-pack provenance가 어긋나면 실패 |

P0 대비는 두 언어에서 올바른 형태 후보가 실제 top-k 안에 들어오고 부정·정의·잠금 사례에서 잘못된 hard 의무가 생기지 않는 것을 확인한다. hit 증가만으로 개선을 주장하지 않는다. 현재 데이터 대조군과 새 데이터 조건의 사례별 결과를 같은 기준으로 기록하고 회귀를 검토한다. candidate cap과 열린 차원/잠금 검사 등 기존 제한을 검색 hit 수 때문에 바꾸지 않는다.

## 6. 원본 픽셀과 채택 여부를 판정

13개 렌더 시나리오군은 대표 의미를 비교하는 계획이며 이미지 13장이나 180개 전체의 픽셀 합격 수가 아니다. 먼저 구조·검색·literal 검사가 통과한 대표 조건을 고르고 촬영 방식·인물·crop·빛·모델·request/core를 고정한다. 조명·포즈·데이터·작성 규칙을 한 번에 바꿔 데이터 개선의 원인으로 결론 내리지 않는다.

| 검사 대상 | 실제 판정 | 증거 한계 |
|---|---|---|
| 눈·입 | 입꼬리·치아·입술 틈·윗/아래 눈꺼풀·물림 접점 | 원본 해상도에서 구별되지 않으면 UNOBSERVABLE. 실제 감정은 판정하지 않음 |
| 손가락 | 어느 손가락이 펴지고 접혔는지, 엄지 위치, 손목 소유 | 손 일부만 맞거나 가려진 손가락 수를 추정하면 PASS 아님 |
| 접촉·지지 | 손끝/손바닥/손등/주먹과 얼굴·소품·지지면의 접점 | 보이지 않는 하중이나 힘의 수치를 계측하지 않음 |
| 거울·가림 | 물리 반사 공간, 쥔 폰, 가림 경계, actor 수, 시선 일관성 | 픽셀로 실제 촬영자·저장 미러링 설정을 확정하지 않음 |
| 시점·원근 | 머리/손/몸/신발의 깊이와 투영, 카메라 롤 대비 머리 롤 | 기기 0.5 표기·렌즈 mm·실제 거리/높이를 원본에서 계측한 것으로 쓰지 않음 |
| 다인·네 컷 | 인물별 손·목·팔·다리 소유, 접점, 패널별 count·identity | 비슷한 외형의 반사를 추가 인물로 세지 않음 |
| 빛·흐림 | 밝고 어두운 면, 정반사 위치, 그림자 수용면, 선명한 기준과 흐린 영역 | 플래시·셔터·바람·정차 같은 원인은 입력/실행 조건과 별도. 그림과 실제 발생 이력은 다름 |

각 사례의 필수 게이트를 실행 전에 고정한다. 모든 필수 관계가 보이고 맞아야 사례 PASS다. PARTIAL 또는 UNOBSERVABLE를 전체 성공으로 올리지 않고, BLOCKED/출력 없음은 미점수로 기록한다. 출력이 전달되어도 의미 적합성·픽셀 합격·사용자 수용은 다른 상태다.

실패한 사례는 실패를 보존한 채 재설계한다. 손가락이 작은 문제면 노출·원본 해상도·가림을 먼저 확인하고, 소유가 바뀌면 actor와 contact target을 고치며, 거울 경로가 틀리면 장면 단위를 단순화한다. crop이 잠겨 있으면 확대해서 통과시키지 않고 보이지 않는 조건을 그대로 보고한다. 특정 시드의 성공으로 전체 형태 데이터의 성능을 확정하지 않는다.

## 실행 체크포인트와 완료 조건

| 체크포인트 | 리뷰 가능한 산출물 | 완료 조건 |
|---|---|---|
| C1 정의·재사용 결정 | 180개 번호의 최종 결정표·문맥/변형·출처 상태 | 모든 행의 연결 경로가 있고 미확정 이름은 별도 보류. 기존 ID 의미를 변형으로 덮어쓰지 않음 |
| C2 좁은 원본 반영 | 검토된 extension/profile·실제 actor/property 매핑·scope | 순수 계약뿐 아니라 소유·부정·정의·크롭·손 역할의 의미 검토가 통과 |
| C3 파생물·runtime | 동일 inventory의 index/BM25F/게시 영수증 | source/hash/recipe와 실제 로더의 입력이 일치 |
| C4 검색·literal | 같은 core의 대조 결과, 선택/거부·prompt audit | P0 올바른 후보 노출과 잘못된 의무 억제가 확인되고 기존 회귀가 설명됨 |
| C5 픽셀 진단 | 원본 이미지·가시성·관계별 판정·실패 기록 | 대표 사례의 필수 게이트와 한계가 모두 보고됨. 실패를 기준 완화로 숨기지 않음 |
| C6 반영 채택·전달 | scoped diff·최종 채택/보류 목록·검증 상태 | 데이터·검색·선택·prompt·pixels·사용자 수용 상태를 분리해 전달 |

작업 착수 때 현재 HEAD·dirty/untracked 상태·source inventory를 다시 확인한다. 이번 연구 스냅샷 이후 공유 작업공간에서 인덱스·manifest 변경이 관측됐다. 실행 checkout을 분리하고 해당 시점의 원본을 다시 대조해야 한다. 이번 연구 폴더 밖의 기존 수정·출력·캐시는 임의로 stage·reset·삭제하지 않는다. 원본 변경과 파생 인덱스 변경은 좁게 stage하고 과거 proof를 새 결과로 덮어쓰지 않는다.

이번 연구의 완료는 **근거와 한계가 표시된 상세 보고서·초안·실행 계획이 준비된 상태**다. 운영 반영의 완료는 C1–C6의 실제 증거로 따로 판정한다.
