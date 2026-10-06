# 물 의미 데이터 반영과 독립 이미지 테스트 — 2026-10-06

물 관련 리서치에서 관찰 가능한 관계 117개를 실제 후보 데이터와 시각 의미 데이터에 반영했다. 독립 서브에이전트 3개가 첨부 인물 사진을 사용하여 서로 다른 복잡한 컨셉을 무작위로 정하고, 테스트케이스·프롬프트·이미지를 작성했다. 최종 이미지 3장의 선택된 물 구성 요소 21개와 신체·접촉·지지 조건 15개는 모두 원본 픽셀 검사를 통과했다. 실제 이미지 생성 도구 호출은 4회였으며, 과수원 사례에서 발판을 한 번 수정했다.

추가로 미리 정한 장면 기대는 17개 중 14개를 충족했다. 작은 배의 과거 수위선, 강가의 배수 연결, 강가 인물의 마른 발판은 충분히 드러나지 않았다. 이 결과는 이번에 채택한 물 프로필 7개와 세 장면의 검증이다. 전체 프로필 117개나 원래 키워드 345개에 대한 이미지 검증으로 확대하지 않는다. 요청자의 미적 수용은 아직 기록하지 않았다.

| 실제 반영 대상 | 결과 | 확인 자료 |
|---|---:|---|
| 후보 데이터 | 117개, 기존 슬롯 21개에 추가 | [후보 원본](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_water_relations_extension.json) |
| 시각 의미 프로필 | 117개, 프로필당 구성 요소 3개 | [시각 의미 원본](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_water_relations.json) |
| 구성 요소별 원본 이미지 검사 조건 | 351개 | 선택한 프로필의 해당 조건만 적용 |
| 의미 검색 인덱스 | 10,167 → 10,284개 | [의미 인덱스](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_semantic_index.json) |
| 시각 프로필 인덱스 | 1,964 → 2,081개; 정확 일치 표현 4,638개 | [시각 인덱스](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_profile_index.json) |

단어 별칭 외에 대상, 표면 접촉, 흐름의 시작과 도착, 장비의 소유 대상, 반사 대상과 수면의 연결을 기록했다. 효과가 미치는 차원과 대상·속성을 좁게 지정하고, 식물·동물·지형·장비의 분류를 구분했다. 젖음이 자동으로 투명함을 뜻하거나 물 표현이 카메라·인체·의상 조건을 임의로 바꾸는 오류를 회귀 검사에 포함했다. 연구에서 분류한 30개 비가시적 맥락과 45개 변형군은 [채택 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-integration-20261006/ADOPTION-LEDGER.json)에 보존했다. 변형 선택이 필요한 개념을 하나의 고정 형상으로 묶지 않았다.

원본 등록은 기존 [소스 매니페스트](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_source_manifest.json)에 두 데이터 파일을 추가하는 방식으로 처리했다. 의미·시각 인덱스와 필요한 shard를 재생성하고 최종 로컬 runtime 등록을 검증했다. 동일한 텍스트·모델·차원의 벡터는 재사용했다. 임베딩 모델은 `gemini-embedding-2`, 차원은 768이다. 주제별 생성기 분기나 장면별 우회 경로는 추가하지 않았다. [설치 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-integration-20261006/INSTALLATION.json)과 [실제 데이터·검증용 복사본 일치 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-integration-20261006/LIVE-FROZEN-PARITY.json)을 남겼다.

세 에이전트는 각각 독립 난수로 일반 지식 기반 컨셉 목록에서 장면을 선택했다. 후보팩에 접근하기 전에 장면, 예상 관찰, 기본 프롬프트와 창작 core를 고정했다. 같은 사용자 요청과 같은 첨부 사진을 사용했으며, 다른 에이전트의 장면·프롬프트·후보팩·이미지는 입력으로 사용하지 않았다. 사진은 보이는 얼굴과 짧은 헤어스타일의 참고로 사용했고, 역할·의상·행동·장소는 각 에이전트가 정했다. 랜덤 seed와 사전 기대는 각 [CASE 1](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-integration-20261006/arm-1/CASE.json), [CASE 2](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-integration-20261006/arm-2/CASE.json), [CASE 3](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-integration-20261006/arm-3/CASE.json)에 있다.

첫 검색에서는 일반 물 후보가 나왔지만 새 시각 프로필은 세 사례 모두 노출되지 않았다. 구성 요소의 검색 표현이 긴 완전 문장에 치우친 문제를 발견하여 프로필 36개의 짧은 양성 형태 표현을 보강했다. 고정된 core, 기본 프롬프트, CASE와 검색 seed를 유지한 재검색에서 각각 새 물 프로필 2·4·4개가 노출됐고 2·3·2개를 채택했다. 필수 구성 요소와 이미지 검사 조건은 유지했다. 원래 검색 결과와 receipt도 보존했다. 이 비교는 검색 노출·채택의 검증이며, 수정 전후 이미지의 품질 A/B 비교는 수행하지 않았다. 인덱스의 유효성과 실제 쿼리의 검색 모드는 별개로 기록했다.

| 독립 컨셉 | 채택한 새 물 프로필 | 물 조건 | 신체·접촉·지지 조건 | 추가 장면 기대 | 도구 호출 |
|---|---|---:|---:|---:|---:|
| 비 온 뒤 작은 배의 물 빼기 | `w021` 연속 물줄기·발원·도착 / `w004` 표면 물방울·접촉·사이 질감 | 6/6 | 5/5 | 4/5 | 1 |
| 갈대밭 옆 나룻배의 항적파 | `w025` 접촉 물보라 / `w036` 배와 항적 연결 / `w047` 대상과 수면 반사 연결 | 9/9 | 5/5 | 6/8 | 1 |
| 서리 낀 과수원의 관개 재가동 | `w018` 낮은 물안개·거리별 대비 / `w044` 부착된 고드름·끝의 물방울 | 6/6 | 5/5 | 4/4 | 2 |
| 합계 | 서로 다른 물 프로필 7개 | **21/21** | **15/15** | **14/17** | **4** |

물 조건은 채택한 프로필의 구성 요소가 최종 이미지에 드러나는지 검사한다. 신체 조건은 손·장비 접촉, 팔과 몸의 연결, 발판과 균형 등을 검사한다. 추가 장면 기대는 각 에이전트가 후보 검색 전에 정한 진단 항목으로, 요청자가 정한 의미나 필수 조건으로 소급하지 않았다. 각 에이전트의 검사에 더해 주 에이전트도 세 최종 이미지와 과수원의 수정 전 이미지를 직접 확인했다.

첫 사례에서는 빌지의 흡입 호스, 고정 펌프, 배 밖 배출 호스와 지면 웅덩이의 경로가 이어진다. 호스 끝에서 연속 물줄기가 떨어지고 같은 충돌점에 물보라와 동심원 파문이 보인다. 전경의 나무 테두리에는 볼록한 물방울, 곡선 접촉 경계, 물방울 사이 나뭇결이 구분된다. 손과 펌프, 다른 손과 배 테두리, 양발의 지지는 일관된다. 다만 높은 과거 수위의 흔적은 바니시·풍화 얼룩과 명확히 구분되지 않았다. [최종 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-integration-20261006/arm-1/final_prompt_en.txt)와 [검사 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-integration-20261006/arm-1/ARM_REPORT.json)를 보존했다.

![비 온 뒤 작은 배의 물 빼기](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-integration-20261006/arm-1/generated_images/dinghy-drain-attempt-1/native.png)

두 번째 사례에서는 먼 나룻배의 선미와 넓어지는 항적이 연결되고, 작은 파란 배의 옆면 접촉에서 얇은 물보라와 분리된 방울이 보인다. 오른쪽 갈대와 같은 위치의 지그재그 반사는 [원본 100% 확대](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-integration-20261006/arm-2/inspection_crops.attempt-1/reed-reflection.png)에서 접촉점부터 연결됨을 확인했다. 밧줄은 양손과 작은 배의 고리에 이어지고 발은 단단한 돌에 놓인다. 돌 틈을 따라 강으로 돌아가는 배수의 전 경로는 확실하지 않으며, 발판은 사전에 기대한 마른 돌 대신 젖은 돌이다. [최종 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-integration-20261006/arm-2/final_prompt_en.txt), [검색·채택 증거](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-integration-20261006/arm-2/water_retrieval_adoption_evidence.json), [검사 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-integration-20261006/arm-2/qualification_summary.json)를 보존했다.

![갈대밭 옆 나룻배의 항적파](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-integration-20261006/arm-2/generated_images/the-ferry-wake-at-the-reeds-attempt-1/image.png)

세 번째 사례에서는 낮게 퍼진 분무가 먼 나무의 대비를 낮추지만 가까운 밸브·가지·얼음의 경계는 남는다. 고드름은 가지 아래에 부착되어 아래로 가늘어지고, 끝의 둥근 액체 방울과 떨어지는 방울, 고랑 수면의 충돌 파문이 보인다. [첫 이미지](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-integration-20261006/arm-3/generated_images/orchard-frost-irrigation-restart/attempt-1.png)는 물 조건 6개를 충족했지만 양발이 고랑에 놓여 의도한 지지 조건에 실패했다. 원래 인물 사진과 이 사례의 첫 이미지로 한 번 편집하여 발을 밸브 쪽의 높고 단단한 둑으로 옮겼다. 얼굴, 양손과 밸브의 접촉, 물안개와 고드름·물방울은 유지되어 최종 11개 필수 조건을 충족했다. [수정 계획](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-integration-20261006/arm-3/repair_plan.attempt-2.json), [최종 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-integration-20261006/arm-3/prompt_en.attempt-2.txt), [검사 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-integration-20261006/arm-3/qualification_summary.json)를 남겼다.

![서리 낀 과수원의 관개 재가동 — 발판 수정 후](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-integration-20261006/arm-3/generated_images/orchard-frost-irrigation-restart/attempt-2.png)

각 호출 전에 프롬프트와 실제 runtime 입력을 감사했다. 생성은 네 번 모두 내장 `image_gen.imagegen` 도구에서 반환된 이미지로 확인했고, 원본과 바이트가 같은 저장본을 보존했다. API 대체 호출은 사용하지 않았다. 도구가 실제 이미지 모델명을 공개하지 않아 모델명은 미확인으로 남겼다. 모든 최종 candidate receipt는 같은 데이터 generation `ca8d80bf02fe00c9e49c1c59607cf0d859f5ca6f96818f50561ffa488d145327` 및 source fingerprint `eb0d7b8b2a55ee0a8d174d50ccbae89be89649927fb44b3af9359b51568d39b3`에 연결된다. 요청 원문·고정 core·참고 사진의 해시와 실제 호출 기록은 각 arm의 `run_manifest.json`, `image_runs.ndjson`에 있다.

관련 코드·계약 검사 40개가 통과했다. [집중 검사 33개 로그](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-integration-20261006/final-focused-tests.log)는 물 회귀 7개, 후보 의미 계약과 시각 프로필 검색을 포함한다. [최종 runtime 등록 후 창작 core 검사 7개 로그](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-integration-20261006/authorial-core-after-publication.log)도 통과했다. [사전 검사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-integration-20261006/live-dictionary-discovery-final.log)와 [시각 인덱스 검사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-integration-20261006/final-visual-index-check.log)는 최종 데이터에서 성공했다. 반영 전에 시작한 전체 1,729개 검사 실행은 데이터 변경 시점이 섞여 중단했고 전체 통과 근거로 사용하지 않았다. [상태 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-integration-20261006/BROAD-CHECK-STATUS.json)을 남겼다.

픽셀 감사의 `technical_qualified`는 세 최종 이미지 모두 참이고 실패한 필수 조건·스키마 항목은 없다. 대표 샘플 승격은 요청자의 판단을 기다리는 별도 상태라 CLI의 비영 종료가 있다. 이를 픽셀 실패로 집계하거나 요청자 수용으로 바꾸지 않았다. 추가 장면 기대에서 드러난 세 가지 한계는 기록에 남겼다.

기존에 수정·미추적 상태였던 다른 원본 데이터와 생성기 코드는 보존했다. 관련 없는 원본 파일의 이번 변경은 없고 이전 인덱스 세대도 삭제하지 않았다. [보존 확인](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-integration-20261006/PRESERVATION-FINAL.json)에 HEAD와 비교 결과가 있다. 커밋·푸시·PR은 수행하지 않았다. 기계 판독용 전체 결과는 [TEST-SUMMARY.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-integration-20261006/TEST-SUMMARY.json), 파일 해시 목록은 [ARTIFACT-MANIFEST.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/water-integration-20261006/ARTIFACT-MANIFEST.json)에 있다.
