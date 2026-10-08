# 패션 핏 데이터 반영과 독립 이미지 테스트

데이터·이미지 테스트 기준일: 2026-10-08. 최종 전달일: 2026-10-09. 기존 513개 용어·64개 의미 카드·119개 후보 초안 연구를 실제 authored source와 검색 인덱스에 반영했다. 독립된 세 arm에서 실제 이미지 다섯 장을 생성했고, 부모도 반환 원본 다섯 장을 직접 재검사했다. 큰 재킷 비례는 관찰되지만 각 장면의 핵심 관계 전체 통과는 실패했다.

## 반영한 데이터

새 후보 114개, 대응 시각 의미 프로필 114개, 선택 가능한 단일 변형 번들 114개를 등록했다. 기존 후보 4개는 원래 좁은 의미를 유지하면서 동등한 표현만 추가했다. 연구 카드 64개 중 60개를 반영했다. 513개 용어 전체의 연구 계보는 유지하지만, 같은 계열에 속한다는 이유로 모든 용어를 같은 activation alias로 등록하지 않았다.

| 층 | 파일 | 역할 |
|---|---|---|
| 후보 | [photo_prompt_fashion_fit_extension.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_fashion_fit_extension.json) | 소유 의복·구체적 관계·영향 속성·독립 변형 |
| 시각 의미 | [photo_prompt_visual_obligations_fashion_fit.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_fashion_fit.json) | 관찰 요소, 정확한 활성화, 혼동 경계, native 검사 기준 |
| 등록 | [photo_prompt_source_manifest.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_source_manifest.json) | 기존 112개 등록 행을 보존하고 2개 source 추가 |
| 계보 | [term-runtime-map.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fashion-fit-integration-20261008/term-runtime-map.json) | 513개 연구 용어와 선택된 변형의 관련성·보류 근거 |
| 회귀 | [test_photo_fashion_fit_semantics.py](/Users/chasoik/Projects/image-prompt/tests/test_photo_fashion_fit_semantics.py) | 활성화, 부정/동음어, 부분 관계, 속성 잠금, material/pose 소유 범위 |

형태·밀착·여유·봉제·여밈·스트랩·레이어 경계를 동일 의복의 관계로 구성했다. 큰 계열의 대안들을 한꺼번에 요구하는 all-of 프로필로 만들지 않았다. 소재 효과는 appearance와 material을 함께 선언하고, 팔을 올리거나 앉는 등 명시적인 자세 전제는 pose 효과도 선언한다. 후보와 번들은 선택 사항이며 연관 프로필 ID가 있다는 이유로 hard obligation이 활성화되지 않는다.

FF39(신축률·복원력·GSM·혼용률), FF45(코르셋 spring·측정 상태), FF59(사이즈·제작·패턴 공정)는 이미지로 측정값을 입증할 수 없어 별도 문맥으로 보존했다. FF51(VPL·rear scrunch)은 해당 변형 자체에 직접 적용되는 출처를 추가 확인할 때까지 runtime 등록을 보류했다. 보류는 [runtime-integration.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fashion-fit-integration-20261008/runtime-integration.json)에 기록했다.

## 인덱스와 보존

독립 worktree에 현재 authored source와 최신 코드의 스냅샷을 옮겨 검증한 뒤 필요한 신규 source·manifest 추가만 원래 작업 트리에 반영했다. 최초 검증 인덱스 구축에서 후보 118개(신규 114개와 기존 표현 갱신 4개), 프로필 114개에 embedding을 요청했다. 원래 작업 트리 적용 및 이후 메타데이터 수정에서는 동일 text/hash/provider/model/dimensions의 벡터를 재사용했다. 총 semantic corpus 11,119개, visual profile 2,876개, 정확한 검색어 5,494개다.

본 작업 적용 직후 기존 파일 187개를 비교한 결과 184개가 바이트·모드 동일했고, 예상한 source manifest와 두 생성 인덱스만 변경됐다. 처음부터 수정돼 있던 tracked 파일 13개도 이 세 파일 외 10개를 그대로 보존했다. 원래 112개 manifest 행의 값과 순서를 유지했다. [적용 후 보존 시점](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fashion-fit-integration-20261008/PRIMARY-PRESERVATION-OWN-CHECKPOINT.json).

동시 셀피 데이터 반영 후 확인에서는 187개 중 183개가 동일하다. 추가로 달라진 공통 시각 registry는 외부 셀피 갱신이며 source 비교로 분류했다. 기존 dirty 파일 10개, runtime code, 중립 저작 파일, 참고 문서, SKILL 및 패션 핏 두 원본은 보존됐다. 삭제나 설명되지 않은 변경은 0개다. 현재 manifest 116개 행은 원래 112개·패션 핏 2개·외부 셀피 2개를 포함한다. [현재 보존 영수증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fashion-fit-integration-20261008/PRIMARY-PRESERVATION.json).

추가 회귀에서 발견된 유지보수 기록의 external-only 표시는 이전 파일을 고치지 않고 hash-bound successor를 만들어 수정했다. 후보 본문·관계·속성·activation의 변화는 없다. [수정 근거](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/extension-maintenance/fashion-fit-maintenance-seal-20261008.json).

패션 핏 유지보수까지 완료한 발행 세대: `6576587f94bf0f5d7d44281a4dd13e6a8caa585bee7aca7b891027d8dff55563`. source fingerprint: `5b2241d4fc503a49d83e41e51c5de6303b07ec37211ebbbedaa510802df26c4b`. 먼저 시작한 인쇄소·항구 실행은 후보 의미가 동일한 직전 immutable 세대 `0c8cb761362bff39d912ae24fae79451e41c41fff886a420352adc25fa317925`에 고정돼 있다. 서로 다른 세대의 영수증을 혼합하지 않는다.

이미지 테스트 도중 동시 셀피 데이터 작업이 source 두 개, source manifest, 공통 시각 registry 및 파생 인덱스를 추가 갱신했다. source 비교에서 패션 핏 두 원본·최신 SKILL·runtime code·environment hash는 그대로다. 이 외부 갱신은 복원하거나 덮어쓰지 않았다. 인쇄소 수정 실행은 실제로 검증된 후속 세대 `4561ae291c9a5626888dc0b05c295ebbe0a4416d40b7099b3c7d3e7216376ccf` / fingerprint `333f41dd7bbc9c404ce9ac774824d4480dfd6f8d02f344538b15ea57f950196c`에 묶여 있다. 이 시점 corpus는 후보 11,223개·프로필 2,977개·정확한 검색어 5,690개이며, 외부 추가 후에도 패션 핏 회귀 10개와 dictionary/visual index 검사가 다시 통과했다. [동시 변경 비교](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fashion-fit-integration-20261008/CONCURRENT-SOURCE-DIFF.json).

관련 기존 회귀 71개와 신규 10개를 합한 81개가 통과했다. [최종 회귀 영수증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fashion-fit-integration-20261008/related-tests-final.json). 검증용 worktree는 결과·원본·벡터·검사 기록을 원래 작업 트리에 보존한 뒤 복구 가능한 archive로 정리했다.

전달 직전에도 공통 시각 registry와 파생 인덱스가 다시 갱신된 상태를 확인했다. 패션 핏 두 원본·사용 SKILL·runtime code는 그대로이며, 사전·시각 인덱스 검사와 패션 핏 회귀 10개를 다시 통과했다. 원본 수정과 추가 embedding 없이 공식 immutable publisher로 검증된 현재 source를 발행하고 `bootstrap=False`로 freshness를 확인했다. 최종 전달 세대는 `b583b7a879e534f644e2f730bfe47b4c70a6c61b7a0ea55afdcea46ee5d13f0e`, fingerprint는 `430189ad7c8a3325b543281675065a46b983c2e1d593d4eccca9d9c335801ad3`다. 이 세대는 최종 사용 준비 확인이며 앞서 생성한 다섯 이미지의 영수증 세대로 대체하지 않는다. [전달 시점 검사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fashion-fit-integration-20261008/DELIVERY-CHECKS.json), [freshness 확인](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fashion-fit-integration-20261008/DELIVERY-RUNTIME-VERIFICATION.json), [현재 source 보존](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fashion-fit-integration-20261008/DELIVERY-SOURCE-PRESERVATION.json).

## 독립 저작과 검사 기준

최신 photo-prompt-image-generator SKILL SHA-256: `9e9b87e6f0b2c1ec1c36bd8e9d55f90950d53529a0b873722b546924dfc7043b`.

세 서브에이전트는 코디네이터가 고정한 실제 사용자 요청과 같은 참고 이미지를 받고 각각 다른 무작위 복합 컨셉을 작성했다. 후보 내용 접근 전에 core·baseline·controls·embodiment를 고정했다. 참고 이미지는 보이는 얼굴·머리의 지침으로 사용했다. 참고 파일 SHA-256: `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`.

인쇄소 arm은 검색 전에 지나치게 잠긴 저작 선택의 소유 범위를 정정하고 최초 자료를 보존했다. 드레스 arm은 최초 파일 경로 검색과 memory registry에서 다른 자료의 제목·경로를 본 접근을 공개했다. 다른 arm의 prompt·후보·profile 본문은 독립 core 고정 전에 읽지 않았다는 agent 기록을 보존했다.

source 등록 → 실제 public pack 노출 → 맥락상 호환 선택 → literal prompt → composed/runtime audit → 실제 image_gen 반환 → 같은 의복의 관계 및 endpoint 원본 픽셀 → 전체 장면 품질을 분리한다. 한 층의 PASS로 다음 층을 대체하지 않는다. 보이지 않는 연결점은 `UNOBSERVABLE_NOT_PASS`, 일부만 구현된 관계는 전체 PASS로 세지 않는다. 사용자의 결과 수용은 `not_yet_received`다.

## 실행 결과

세 arm 모두 생성 결과를 얻었고, 인쇄소·항구는 각각 검증된 국소 수정 한 번까지 실행했다. 원본·실패·수정 이력을 보존했다. 부모의 원본 픽셀 관찰은 [parent_pixel_observations.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fashion-fit-integration-20261008/parent_pixel_observations.json)에 기록했다.

| arm / 무작위 컨셉 | 실제 신규 채택과 검사 | 픽셀 결과 | 실제 호출 |
|---|---|---|---|
| 1 / 보랏빛 황혼 인쇄소, 첫 전시 인쇄물 건조를 기다리는 순간 | `ff10_v2` 소매산 능선·같은 재킷 부착 솔기 | 최초 구별 불가; 수정은 한쪽만 식별 → 전체 PARTIAL_NOT_PASS. 버튼도 열려 있음 | 2 |
| 2 / 새벽 항구 터미널의 행사 카드 수습 | 드레스 호환 신규 후보 0개; 기존 드레스 관계 검사 | 새 데이터 효과 검증 FAIL. 드레스의 큰 핏은 읽히나 기존 소매 솔기·주름 접합은 식별 불가 | 1 |
| 3 / 비가 그친 항구 수리소의 조끼 스트랩 확인 | `ff03_v2` 넓은 재킷, `ff62_v3` 조끼 연결점·버클; 수정에서 새 `ff62_v3` 시각 프로필 선택 | 넓은 재킷 PASS. 뒤 fabric attachment가 계속 가려져 전체 스트랩 관계는 UNOBSERVABLE_NOT_PASS | 2 |

세 사례 전체의 qualification은 FAIL이다. 후보/시각 프로필 등록 성공과 큰 핏의 부분적인 관찰 성공을, 모든 관계의 이미지 구현 성공으로 합산하지 않았다. 원본 PNG 다섯 장은 바이트 동일한 검토용 사본으로 모았고, 작성 프롬프트와 실제 runtime 문자열도 각각 내보냈다. [이미지 계보](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fashion-fit-integration-20261008/IMAGE-EXPORTS.json), [프롬프트 계보](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fashion-fit-integration-20261008/PROMPT-EXPORTS.json), [최종 전달 영수증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fashion-fit-integration-20261008/DELIVERY.json).

### arm_1 — 보랏빛 황혼의 인쇄소

시드 `17845346690454733953`. 전시를 앞두고 젖은 교정 인쇄물이 마르기를 기다리는 상황을 독립 저작했다. public pack에서 `fit_ff10_v2_candidate`를 읽고 선택해, 같은 wool jacket 소매산의 좁은 솟은 능선과 그 아래 부착 솔기의 관계를 literal prompt에 넣었다. 전체 원칙에 맞지 않는 oversized jacket·boxy torso 대안은 거절했다.

첫 560단어 프롬프트와 runtime 검사가 통과한 뒤 생성했다. 일반적인 어깨 구조는 있으나 별도 rope ridge가 식별되지 않았다. 재킷 밑단이 허리밴드를 가리고 버튼도 열려 있어 공식 visibility gate가 실패했다. 이 원본/실패/ledger를 보존하고, 검증된 `pixel_realization_mismatch` projection으로 appearance의 소매산·밑단·여밈 및 jacket illumination만 허용해 477단어 수정 프롬프트를 독립적으로 다시 고정했다. source는 실제 `4561ae...` 세대다.

수정 결과는 짧은 차콜 재킷과 어두운 바지로 표현됐다. 화면 왼쪽의 굽힌 팔 소매산에서 raised/rolled edge는 구별되지만 오른쪽 능선과 같은 부착 솔기는 완전히 구별되지 않는다. 선언한 양쪽 관계는 **PARTIAL_NOT_PASS**다. 버튼은 여전히 front를 연결하지 않는다. 원래 custom 7개 항목은 3 PASS / 4 FAIL로 판정했고, 최종 formal embodiment도 contact·visibility에서 실패했다.

두 번째 tool 반환 파일은 실제 존재했지만, 로컬 observer의 공백 허용 regex가 `folder as file`을 한 경로로 읽어 managed history에 `preview_only`를 남겼다. 원 역사 상태를 바꾸지 않고 같은 반환 bytes만 보존했고, 지원되는 개별 native-plan recorder 재감사로 같은 호출 ledger/manifest를 기록했다. 이 복구는 생성 재호출이나 API fallback이 아니다. 이 capture limitation과 실제 returned-image 기록을 분리해 보존했다.

수정 이미지의 managed review admission은 `review_result_not_bound_to_observed_attempt`로 실패한 상태를 유지한다. 별도로 공식 receipt-bound worker와 native-scale validator에 exact ledger/image/request 대조를 더한 독립 감사는 `record_valid=true`, `technical_qualification=fail`을 확인했다. 이를 managed admission 성공으로 표기하지 않는다. [독립 반환 이미지 감사](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/fashion-fit-integration-20261008/arm_1/ownership_narrowed/repair_1/render_review_repair_1_audit.json), [원 managed 오류](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/fashion-fit-integration-20261008/arm_1/ownership_narrowed/repair_1/managed_review_audit_diagnostic.json).

- [최초 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fashion-fit-integration-20261008/prompts/arm1_attempt1.composed.en.txt) · [수정 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fashion-fit-integration-20261008/prompts/arm1_attempt2.composed.en.txt)
- [최초 이미지](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/fashion-fit-integration-20261008/results/arm1_attempt1.png) · [수정 이미지](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/fashion-fit-integration-20261008/results/arm1_attempt2.png)
- [독립 픽셀 판정과 전체 이미지 평가](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/fashion-fit-integration-20261008/arm_1/ownership_narrowed/pixel_review_attempt_1.json)
- [최초·수정 테스트 케이스와 최종 판정](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/fashion-fit-integration-20261008/arm_1/ownership_narrowed/arm_result.md) · [구조화 영수증](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/fashion-fit-integration-20261008/arm_1/ownership_narrowed/arm_result.json)

### arm_2 — 새벽 항구 터미널의 행사 카드 수습

장면 시드 `5799112123705302875`. 독립 baseline은 차콜 드레스의 몸판·소매·네크라인과 카드/상자의 낮은 움직임을 선택했다. 처음과 한 번의 추가 시드에서 실제 정상 public pack을 두 개 얻었지만, 신규 후보는 oversized jacket `fit_ff03_v2` 하나뿐이어서 이 드레스 장면에 호환되는 신규 채택은 0개다. 새 `fit_ff` 시각 프로필의 노출도 0개다. **신규 데이터 검색/채택 검증 FAIL, native 데이터 효과는 검증 불가**로 기록했다.

재검색은 core·baseline·controls 등을 다시 쓰지 않고 13개 frozen role을 바이트 동일하게 유지했다. source successor의 private-store 발행 포인터를 갱신하기 전 실패했던 두 transaction도 삭제하지 않았다. 최종 pack `a4b3576c4621c124`는 `657658...` 세대에 묶여 있다.

446단어 프롬프트와 runtime audit가 모두 통과한 뒤 실제 image_gen을 한 번 호출했다. 반환 후 local observer의 PIL import 오류는 접근 가능한 원본 경로·SHA로 복구했고, 생성 재호출은 하지 않았다. 보존 PNG는 1024×1536 / SHA `ccc3675aa52c1d01065dab236fb1a336a045f07341f54426ea785ca042298883`이다.

드레스 몸판·여유 있는 소매·네크라인·행사 카드 행동·참고 bob/fringe는 관찰된다. 기존 시각 프로필 `pr_fabric_tension_fold_attachment`를 별도로 선택했으나, 미세 주름 뿌리와 안쪽 소매 봉제선의 접합이 원본에서도 식별되지 않아 그 gate와 embodiment visibility gate가 실패했다. 정식 검사 7 PASS / 2 FAIL. 리뷰 기록은 `record_valid=true`, 픽셀 기술 판정은 `technical_qualification=fail`이다. 기존 프로필의 결과를 신규 패션 핏 데이터의 성공으로 계산하지 않는다.

- [최종 프롬프트](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/fashion-fit-integration-20261008/arm_2/retrieval_replay_01_store_published/prompt.final.en.txt)
- [보존 이미지](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/fashion-fit-integration-20261008/arm_2/generated_images/ferry-terminal-dress-fit-20261008/image.png)
- [테스트 케이스·전체 경로·상세 판정](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/fashion-fit-integration-20261008/arm_2/run_summary.md)
- [구조화 영수증](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/fashion-fit-integration-20261008/arm_2/run_summary.json)

### arm_3 — 비가 그친 항구 수리소

시드 `310820261`. 조끼 스트랩을 확인하고 수리 키트를 배로 가져가기 전의 순간을 독립 저작했다. 초기 pack에서 roomy jacket `ff03_v2`와 동일 조끼의 fabric-anchor/webbing/buckle `ff62_v3`를 채택했다. 최초 563단어 prompt/runtime 검사가 통과했고 실제 이미지를 생성했다. 넓은 어깨·소매·몸통이 같은 재킷에 속하는 비례와 레이어 차이는 PASS였다. 앞쪽 패치와 버클은 보이지만 뒤쪽 fabric anchor가 외투에 가려져 전체 연결 관계는 실패했다.

parent audits를 검증한 closed projection에서 appearance의 jacket panel fold와 camera 방향만 허용하고 controls를 보존했다. 최초 0c 세대와 실패 원본을 유지한 채 repair core를 새로 고정해 `657658...` 세대의 public pack `b640a0327a07aa83`를 얻었다. 이번에는 새 `visual-concept:fit_ff62_v3`가 실제 노출됐다. 전체 opt-in 조건을 읽고 명시적으로 선택했으며 두 관찰 요소의 literal evidence를 채웠다. 새 requester definition을 만들거나 공개되지 않은 ID를 강제로 선택하지 않았다.

494단어 수정 prompt/runtime/native-plan 검사가 통과한 뒤 한 번 더 생성했다. 뒤쪽 올리브 strip은 더 보이지만 upper attachment도 외투 edge 아래에서 추적이 끊기고, lower attachment는 손과 외투에 가려졌다. 두 source VO criterion은 모두 FAIL, embodiment는 4 PASS / visibility FAIL, render repair는 class/contact 2 PASS와 structure/recognition 2 FAIL이다. 이 여러 실패 gate는 같은 가림 문제와 연결되므로 독립적인 통계 관측으로 취급하지 않는다. 정식 리뷰는 `record_valid=true`, 픽셀 기술 판정은 `technical_qualification=fail`, user judgment는 `not_yet_received`다.

실제 생성 2회. 원 ledger prefix를 유지했고 연결 artifact 43개의 hash를 재확인했다. 최초 리뷰 제출의 null enum은 pixel FAIL을 유지한 채 별도 corrected pending 파일로 고쳐 정식 audit를 통과시켰으며 원 제출도 보존했다.

- [최초 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fashion-fit-integration-20261008/prompts/arm3_attempt1.composed.en.txt) · [수정 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fashion-fit-integration-20261008/prompts/arm3_attempt2.composed.en.txt)
- [최초 이미지](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/fashion-fit-integration-20261008/results/arm3_attempt1.png) · [수정 이미지](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/fashion-fit-integration-20261008/results/arm3_attempt2.png)
- [전체 source·prompt·image·proof·판정 계보](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/fashion-fit-integration-20261008/arm_3/final_summary.md)
- [정식 최종 audit](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/fashion-fit-integration-20261008/arm_3/repair_run/render_review_audit.json)

## 검증에서 확인된 후속 반영 순서

1. **검색의 의복 맥락을 먼저 보강한다.** 드레스 arm의 원래 고정 자료와 두 개의 정상 public pack을 재현 입력으로 보존한다. 같은 `main_subject`의 `wardrobe.*` 수정이 가능하다는 사실과, 제안 의복이 해당 장면에 어울린다는 판단을 구별한다. 몸을 따르는 상체·여유 있는 소매·드레스 구성에 맞는 기존 변형을 제안하는지 검사한다. 검색에서 노출된 oversized jacket을 채택시키거나 테스트 core를 후보 문구에 맞춰 다시 쓰는 것으로 해결하지 않는다.
2. **선택한 관계의 관찰 가능성을 저작 단계에서 확인한다.** 소매산 능선과 인접 어깨 솔기, 허리밴드 양 끝, 조끼의 앞·뒤 fabric anchor가 한 프레임에서 구별되는지 점검한다. 예쁜 전체 실루엣·버클·범용 어깨 구조로 endpoint를 대체하지 않는다. 이번 인쇄소·항구 실패는 원본과 판정을 보존한 채 허용 범위의 국소 수정 한 번까지 재검사했다. 다음 검증에서는 같은 실패 기록을 입력으로 삼아 저작 단계의 관찰 가능성 검사부터 보강한다.
3. **시각 의미 프로필의 optional 검색 경로를 별도로 검증한다.** 후보의 관계가 prompt에 들어간 것은 연관 시각 프로필의 노출·선택·hard activation 증거가 아니다. 의미에 필요한 관찰 요소를 유지하면서 한국어·영어의 구체적 동등 표현과 선택 가능한 문맥을 점검한다. 한 가지 변형의 모든 관계를 증명하는 예와 일부 요소·동음어·부정·다른 의복의 예를 나눠 검사한다. embedding 적중만으로 hard 의무를 만들지 않는다.
4. **보류 항목은 출처와 증거 유형을 충족한 뒤 등록한다.** FF51은 VPL·rear scrunch 변형에 직접 대응하는 출처와 관계를 확인한다. FF39/45/59의 치수·공정·제품 명세는 같은 이미지가 있다고 관찰 속성으로 승격하지 않고 별도 문맥 데이터로 유지한다.
5. **로컬 반환 observer와 복구 경로를 보강한다.** 반환 hint의 folder/file 문구를 공백 포함 정규식으로 임의 파싱하기보다 실제 파일 또는 data-URL의 바이트 증거를 사용한다. observer 오류가 provider 반환 이후 발생한 경우와 실제 preview-only 반환을 분리하고, 동일 반환 bytes의 재관측을 hash-bound 상태로 수용하는 지원 경로를 검증한다. 현재는 원 `preview_only` 상태와 별도 recorder/독립 감사의 범위를 보존했고 공통 workflow 코드는 수정하지 않았다.

이 후속 항목은 이번 세 장면에서 드러난 제한과 다음 검증 순서다. 추가 runtime 알고리즘 변경이나 전 프로필의 이미지 검증이 이미 완료됐다는 뜻은 아니다.
