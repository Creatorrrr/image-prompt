# 키워드 리서치 반영과 독립 이미지 검증

작성일: 2026-10-07. 원 요청은 시각 의미·후보 데이터 반영 및 서로 다른 복잡한 컨셉을 사용하는 독립 서브에이전트 3개의 참조 이미지 기반 생성·검사다.

리서치의 40개 제안을 모두 검토해 신규 관계 후보 18개, 시각 의미 프로필 18개, 선택형 묶음 18개를 반영했다. 기존 후보 31개에는 사용 맥락과 혼동 경계를 추가했고, 그중 5개에는 원래 의미와 동등한 한국어·영어 긍정 표현을 추가했다. 실제 작업 디렉터리에 적용하고 인덱스와 불변 런타임 스냅샷을 갱신했다.

세 사례의 이미지 검사는 해당 사례의 관찰 증거다. 18개 전체 프로필의 렌더링 성공, 새 데이터의 인과적 개선, 사용자 선호·수용을 입증하지 않는다. 실패·미노출·불명확 항목은 통과로 올리지 않았다.

## 반영 범위와 의미 경계

| 데이터 | 이전 | 최종 | 변화 |
|---|---:|---:|---:|
| 일반 후보 항목 | 10,500 | 10,518 | +18 |
| 의미 인덱스 문서 | 10,536 | 10,554 | +18 |
| 시각 의미 프로필 | 2,290 | 2,308 | +18 |
| 선택형 후보 묶음 | 1,099 | 1,117 | +18 |
| 기존 후보 맥락 보강 | — | 31 | 원래 소유자·속성·구성요소 보존 |

신규 데이터는 관찰 가능한 구성요소 → 소유자 → 관계 → 영향 속성 → 혼동 경계 → 프롬프트 근거 → 원본 픽셀 검사로 연결했다. 일반적인 단어 또는 근사 검색 일치만으로 필수 시각 의무를 만들지 않는다. 선택형 묶음의 관련 프로필도 별도의 명시적 채택 없이 활성화하지 않는다. 잠긴 외모·속성·차원은 후보를 통해 바꾸지 못한다.

출처 URL, 조사 경위, 효과 한계와 오답 예시는 유지관리 기록에 두었다. 긍정 검색 문장에 섞지 않았다. G06·G20·G25는 저작 지침과 경계로 남겼고, G39·G40은 사진 속 도안·작품·구도의 해석으로 제한했다. 순수 2D 표현을 사람의 신체 재질로 강제하지 않았다.

Faille은 가로 방향의 골이 있는 직물 구조이며 특정 섬유 하나를 뜻하지 않는다. 섬유와 색·실루엣은 별도로 지정한다. [MFA CAMEO](https://cameo.mfa.org/wiki/Faille). 필름의 halation과 표면 결로도 구분했다. [Kodak 용어집](https://www.kodak.com/en/motion/page/glossary-of-motion-picture-terms/).

주요 파일: [일반 후보 데이터](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_grammar_extension.json), [시각 의미 프로필](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_visual_grammar.json), [소스 매니페스트](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_source_manifest.json), [40개 제안 반영 원장](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/keyword-visual-integration-20261007/reflection-ledger.json), [의미·경계 검사](/Users/chasoik/Projects/image-prompt/tests/test_photo_visual_grammar_integration.py).

## 독립성, 스킬과 데이터 버전

3개 에이전트는 서로의 대화·프롬프트·결과를 읽지 않고 별도 난수 시드와 키워드 표본으로 컨셉을 작성했다. 공통 입력은 실제 사용자 요청, 첨부 이미지, 최신 스킬과 원 대화에서 얻은 키워드의 지정된 부분집합이다. 연구 결론·후보 데이터·과거 결과는 핵심 장면을 먼저 동결한 뒤 읽도록 했다. 컨셉과 상세 장면은 에이전트 저작이며 사용자 원문으로 재분류하지 않았다.

사용 스킬 SHA-256: `924c648648ab636ca7f2a17164f6684294a63ecf612d7347671e3691d154b84c`. 모든 에이전트에서 스킬 본문·중립 제어 규칙은 같다. 기본값은 sensual_editorial=1, fetish_fashion=0, creativity=1, surreal=0이다.

첨부 이미지는 얼굴 비율·짧은 검은 단발·가느다란 앞머리 등의 외형 참조로 사용했다. 실명, 실제 나이, 성격과 이력을 추론하지 않았다. 참조 파일 SHA-256: `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`.

사례 1·2는 데이터 V2(17개 신규 관계)를 사용했다. 사례 3의 독립 장면에서는 기존 크기 후보가 주요 피사체만을 대상으로 해 여행가방 속 부차적 모형에 맞지 않는 범위 공백이 드러났다. 이를 기존 모형과 기존 크기 기준의 공통 깊이 관계로 일반화한 G38을 V3에 추가했다. 장면 원문·핵심·잠금·제어값은 유지했고, 기존 V2 스냅샷도 보존했다. 최종 작업 디렉터리는 V3다. 세 사례가 동일 데이터 스냅샷을 사용한 통제 실험은 아니다.

최종 런타임 generation: `5daeab3d58ed9579894346c35f499f37d0c8ce65747f4fc9ae8866b0fa6cd719`.

## 이미지 검사 결과

| 사례 | 독립 컨셉 | 필수 픽셀 의무 | 주제 판정 | 생성 횟수 |
|---|---|---|---|---:|
| 1 | 밤의 식물 검역 온실에서 젖은 관찰 기록 복구 | 8/8 PASS | 표본 4/4 PASS | 1 |
| 2 | 폐장한 천체투영관의 물 거울 시험과 보호 동작 | 최종 5/5 PASS; 첫 이미지 2개 FAIL | 부분 구현: 미세 표정·수면·팔레트 항목 FAIL | 2 |
| 3 | 공항 분실물실에서 여행가방 속 미니어처 다리 수리 | 일반 G38/신체 8/8 PASS | 독립 고정 검사 4/6 PASS → FAIL; 정확한 깊이·여백 실패 | 1 |

PASS 기준은 활성화된 모든 필수 의무의 완전한 가시성이다. partial/unclear는 FAIL이다. 사례 2에서 물·균형·팔레트 신규 프로필은 후보팩에 노출되지 않았으므로 주입하거나 해당 프로필 통과로 보고하지 않았다. 채택된 일반 후보의 세부 주제 검사는 필수 신체 검사와 별도로 보고했다.

### 사례 1: 온실 관찰 기록 복구

표본 K146·K198·K251·K463. 손의 연필 잡기, 같은 종이에 닿는 연필 끝, 접촉점에 이어지는 흑연선, 받쳐진 종이를 검토했다. 얼굴·작업하는 손·식별 가능한 온실 공간의 공동 가독성 프로필을 명시적으로 채택했다. 필수 의무 8개와 표본 주제 4개가 통과했다. 정확한 야간 시간·호스 파열 원인은 한 장에서 입증하지 않았다.

[테스트케이스](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/keyword-visual-integration-20261007/arm_1/random_test_case.json) · [최종 프롬프트](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/keyword-visual-integration-20261007/arm_1/final_prompt_en.txt) · [검사·해시 요약](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/keyword-visual-integration-20261007/arm_1/run_summary.json)

![온실 작업 장면](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/keyword-visual-integration-20261007/arm_1/generated_images/greenhouse_record_recovery-attempt_1/native_original.png)

### 사례 2: 천체투영관 물 거울 시험

표본 K088·K137·K303·K439·K431. 웃음 직후 이완 표정 후보와 태연한 전체 자세 안의 국소 반응 묶음을 채택했다. 첫 이미지에서 지지 발이 잘려 지지·투영 검사 2개가 실패했다. 핵심과 잠금을 보존하고 열린 자세·프레이밍만 수리해 최종 신체 의무 5개를 통과했다.

태연한 전체 자세와 국소 반응, 손끝–물 접촉, 참조 외형과 장소 가독성은 보인다. 눈가의 미세 crease, 메니스커스, 금색 별 반사의 국소 변형, 정확한 발 순서와 팔레트 역할은 충분하지 않거나 불명확해 strict FAIL로 남겼다. 첫 all-hard PASS에서 생성 수리를 종료했으며, 세부 실패를 숨기기 위한 추가 호출은 하지 않았다.

[테스트케이스](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/keyword-visual-integration-20261007/arm_2/random_test_case.json) · [최종 프롬프트](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/keyword-visual-integration-20261007/arm_2/final_prompt_en.txt) · [독립 검사 보고서](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/keyword-visual-integration-20261007/arm_2/arm_report.json) · [실패한 첫 이미지](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/keyword-visual-integration-20261007/arm_2/generated_images/attempt_1.png)

![천체투영관 최종 수리 장면](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/keyword-visual-integration-20261007/arm_2/generated_images/attempt_2.png)

### 사례 3: 여행가방 속 미니어처 도시

표본 K452·K163·K331·K355. 공항 분실물실의 실제 여행가방 안 작은 도시와 다리를 손끝으로 수리하는 상황을 작성했다. 손끝·다리 구조·주변 작은 건축물이 같은 깊이에서 상대 크기를 보여야 한다. 선택형 G38 프로필을 명시적으로 채택했고, 허용 속성 선언이 부족한 다른 선택지는 감사 실패 후 배제했다. 잠금이나 허용 범위를 넓히지 않았다.

일반 크기 관계 3개와 신체 의무 5개는 통과했다. 독립적으로 먼저 고정한 6개 의무 중 4개만 통과했다. 손끝 바로 옆 출입구의 정확한 공통 깊이는 부족하고, 양쪽 가장자리는 램프·라벨·선반 때문에 밝고 복잡하다. 두 항목의 부분 구현은 FAIL이다. 분리된 난간의 수리 흔적도 soft FAIL이다. 일반 G38 통과로 더 좁은 테스트케이스의 실패를 대신하지 않았다. 생성은 1회로 종료했다.

[테스트케이스](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/keyword-visual-integration-20261007/arm_3/random_test_case.json) · [최종 프롬프트](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/keyword-visual-integration-20261007/arm_3/final_prompt_en.txt) · [독립 검사 보고서](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/keyword-visual-integration-20261007/arm_3/final_report.md) · [정량 판정 요약](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/keyword-visual-integration-20261007/arm_3/qualification_summary.json)

![여행가방 미니어처 장면](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/keyword-visual-integration-20261007/arm_3/generated_images/suitcase_city_attempt_1/original.png)

코디네이터도 최종 원본 픽셀을 각각 직접 확인했다. 독립 에이전트의 판단과 함께 보관하되 감사 스크립트 성공을 외부 시각 평가나 사용자 수용으로 간주하지 않았다. native 도구가 실제 모델 이름을 반환하지 않아 관찰 모델은 null로 기록했다.

픽셀 감사의 `technical_qualified=true`와 CLI exit 1은 함께 성립한다. 이 CLI는 실제 요청자의 사용자 판정이 있어야 대표 예시 자격을 부여하기 때문이다. 사용자 판정은 미수신이며 대표 예시로 승격하지 않았다.

## 데이터·회귀 검증

사전·시각 인덱스와 공식 소스 스냅샷 검증은 통과했다. 새로운 의미·범위·부정·제외·근사 검색·속성 잠금·묶음 활성화 검사 10개를 통과했다. 사진 소유자 이력 투영과 함께 재검사한 20개도 통과했다. 이전 소스 범위를 사용한 집중 검사 49개와 후보 속성 위조 검사 1개도 통과했다.

정확한 원문과 벡터를 유지한 의미 문서 10,531개 및 기존 시각 프로필 2,290개를 재사용했다. 의미 인덱스에서는 신규 18개와 동등 표현 변경 5개만 입력이 달라졌다. 시각 인덱스는 신규 18개만 추가됐고 기존 프로필 텍스트·벡터는 모두 동일했다. [최종 재사용 증거](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/keyword-visual-integration-20261007/index-reuse-final.json).

광범위 검사에서 실제 unittest 1,990개를 수집해 모듈 단위로 4개 프로세스에 분할했다. 변경 범위의 검증이 통과하고 기존 불변 이력 차이를 재현한 뒤 이 추가 검사는 종료했다. 완료된 결과가 있는 1,482개 사례 중 성공 이벤트는 1,464개다. 나머지는 실패·오류·subtest 실패가 있으며, 이후의 사례는 미완료다. 클래스 초기화 오류도 별도로 기록한다. 전체 1,990개를 완료하거나 통과했다고 보고하지 않는다. 테스트 기대값·불변 과거 증거·허용 범위는 그대로 유지했다. [수행 범위와 실패 분류](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/keyword-visual-integration-20261007/suite-final-summary.json).

작업 전에 이미 clothing_structure 유지관리 기록 필드 누락, liminal 과거 범위의 생략된 pose 참조, 기존 muted 색 묶음의 과거 counterexample 차이가 존재했다. 신규 문법 소스를 제외한 재현과 원본 해시로 구분했다. V24/V35 불변 이력과 실제 작업 전 스킬·인덱스·프로필 등의 해시도 이미 달랐다. 이력 봉인을 새 해시로 덮어쓰거나 실패를 제거하지 않았다. [기존 실패 근거](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/keyword-visual-integration-20261007/baseline-failures.json).

고정된 illustration/photo 경계의 현재 후보팩 바이트 불일치는 별도로 남겼다. 작업 전 소스도 원래 V35 해시와 달랐지만, 작업 전 후보팩 전체를 다시 생성해 비교한 것은 아니다. 이번 추가 데이터 역시 새 경계 자격 검증이 필요하므로 이 실패 전체를 기존 문제로 단정하지 않는다. 전체 회귀 자격은 미확인이다.

전체 검사에서 새 문법 맥락이 오래된 원본 항목의 완전 일치 검사에 함께 들어가는 차이를 발견해 원래 소스 범위로 투영했다. 새 맥락이 기존 필드·소유자·속성·구성요소·효과를 보존하는지는 별도 라이브 검사로 유지했다. 후보 데이터 위조 mock이 독립 시각 레지스트리까지 덮던 검사도 대상 파일에만 적용하도록 고쳤고 실제 속성 차단 판정을 다시 통과했다.

## 40개 연구 제안의 최종 처리

| 제안 | 내용 | 처리 | 후보/프로필 |
|---|---|---|---|
| G01 | 매체와 촬영 태도의 일관성 | 기존 후보 맥락·경계 | slot:medium:street_snapshot |
| G02 | 장르를 서로 다른 시각적 운반체에 배정 | 신규 소유자 관계 + 선택형 프로필/묶음 | slot:world:vg_separate_genre_carriers |
| G03 | 평범한 장소와 낭만적 의상의 대비 | 신규 소유자 관계 + 선택형 프로필/묶음 | slot:concept_tension:vg_wardrobe_place_contrast |
| G04 | 정서어를 상황과 관찰 단서로 연결 | 기존 후보 맥락·경계 | slot:mood:domestic_melancholy |
| G05 | 유지되는 태도와 작게 새는 반응의 동시 대비 | 신규 소유자 관계 + 선택형 프로필/묶음 | slot:emotional_contradiction:vg_composure_local_reaction |
| G06 | 개성 있는 작은 동작의 사용 범위 | authoring_boundary_guidance | 저작 지침 |
| G07 | 웃음이 풀리는 중간 표정 | 신규 소유자 관계 + 선택형 프로필/묶음 | slot:expression:vg_post_laugh_relaxation |
| G08 | 닫힌 입과 눌린 입술의 구별 | 기존 후보 맥락·경계 | slot:expression:ae_lip_press |
| G09 | 관객 위치를 실제 촬영 공간에 연결 | 기존 후보 맥락·경계 | slot:capture_context:off_camera_companion_everyday_capture, slot:viewer_position:viewer_as_confidant |
| G10 | 상호 주의의 두 끝점 | 기존 후보 맥락·경계 | slot:relational_action:two_people_sitting_without_words |
| G11 | 지지 다리와 이완 다리의 역할 | 기존 후보 맥락·경계 | slot:body_pose:pv_single_support, slot:body_pose:contrapposto_full_body |
| G12 | 동작 사이의 한 단계 선택 | 기존 후보 맥락·경계 | slot:narrative_phase:precontact_readiness_visible_gap, slot:narrative_phase:locomotion_counterturn_midphase, slot:narrative_phase:settling_aftereffect_trace_phase |
| G13 | 연필·종이·흔적의 인과 연결 | 신규 소유자 관계 + 선택형 프로필/묶음 | slot:contact_point:vg_pencil_paper_trace |
| G14 | 가방을 놓는 순간의 지지 이전 | 신규 소유자 관계 + 선택형 프로필/묶음 | slot:narrative_phase:vg_bag_support_transfer |
| G15 | 두 손이 같은 컵을 감싸는 구조 | 기존 후보 맥락·경계 | slot:contact_point:cv_two_hand_cup, slot:action:ctx_warm_cup_hold |
| G16 | 넓은 여백과 피사체 경계 | 기존 후보 맥락·경계 | slot:composition:subject_field_negative_space_relation |
| G17 | 한 강조점과 저채도 배경의 범위 | 기존 후보 맥락·경계 | slot:color:cr_candidate_vivid_on_muted |
| G18 | 얼굴·손·장소 단서의 공동 가독성 | 신규 소유자 관계 + 선택형 프로필/묶음 | slot:focus:vg_face_hands_place_readability |
| G19 | 평면 인쇄물과 입체 전경의 분리 | 신규 소유자 관계 + 선택형 프로필/묶음 | slot:composition:vg_flat_artifact_raised_foreground |
| G20 | 요청된 크롭 안에서 접촉을 읽히게 하기 | authoring_boundary_guidance | 저작 지침 |
| G21 | 광원의 모양과 가장자리 반응 | 기존 후보 맥락·경계 | slot:light_shape:egr_occluded_vertical_emissive_slit |
| G22 | 혼합광의 색을 수신 표면에 배정 | 신규 소유자 관계 + 선택형 프로필/묶음 | slot:lighting:vg_cool_window_warm_practical_receivers |
| G23 | 직접 플래시와 실내 주변광의 서로 다른 역할 | 신규 소유자 관계 + 선택형 프로필/묶음 | slot:light_type:vg_frontal_flash_warm_ambient |
| G24 | 광학 흔적의 발생 위치 구별 | 기존 후보 맥락·경계 | slot:lens_artifact:water_droplets_on_lens, slot:lens_artifact:rain_streaks_on_glass |
| G25 | 입자와 움직임 흔적을 핵심 증거와 분리 | authoring_boundary_guidance | 저작 지침 |
| G26 | 검정 바닥과 하이라이트 계조의 독립 제어 | 기존 후보 맥락·경계 | slot:color_grading:pe_faded_black_floor, slot:color_grading:lit_noir_deep_detailed_black_finish, slot:color_grading:lit_golden_protected_warm_rolloff |
| G27 | 팔레트 이름을 색의 소유자와 면적으로 번역 | 기존 후보 맥락·경계 | slot:color:pal_app_neutral_cobalt_accent |
| G28 | 같은 빛 아래 서로 다른 재질 반응 | 신규 소유자 관계 + 선택형 프로필/묶음 | slot:texture:vg_matte_cloth_polished_metal |
| G29 | 실크 섬유와 faille 직조의 분리 | new_weave_atom | slot:texture:vg_faille_crossgrain_ribs |
| G30 | 리본에서 절개선으로 이어지는 조형 연결 | 신규 소유자 관계 + 선택형 프로필/묶음 | slot:garment_detail:vg_ribbon_to_garment_seam |
| G31 | 잔머리의 뿌리·바람·역광 연결 | 기존 후보 맥락·경계 | slot:hair_style:pr_hair_strand_owner_and_cause_candidate |
| G32 | 피부 결·고유색·조명색의 분리 | 기존 후보 맥락·경계 | slot:skin_finish:skin_microtexture_local_light_response, slot:complexion_coverage:sheer_complexion_texture_preservation |
| G33 | 생활 흔적을 장면의 행동과 묶기 | 기존 후보 맥락·경계 | slot:location:lived_in_studio_room, slot:space_condition:lived_in_clutter |
| G34 | 물 접촉점과 표면 변화의 원인 연결 | 신규 소유자 관계 + 선택형 프로필/묶음 | slot:contact_point:vg_hand_water_local_ripples |
| G35 | 바람에 반응하는 여러 운반체의 정합성 | 신규 소유자 관계 + 선택형 프로필/묶음 | slot:motion:vg_shared_airflow_hair_ribbon |
| G36 | 시간 정지 연출의 정지 구역과 예외 | 신규 소유자 관계 + 선택형 프로필/묶음 | slot:surreal_physics_detail:vg_bounded_stillness_exception |
| G37 | 흑연선에서 실과 꽃으로 이어지는 입체 경계 | 신규 소유자 관계 + 선택형 프로필/묶음 | slot:transition_stage:vg_graphite_thread_raised_flower |
| G38 | 실제 축소 크기와 미니어처처럼 보이는 초점 효과 | new_artifact_scope_and_existing_context | slot:scale_relation:canonical_size_anchor_relation, slot:subject:miniature_city_scene, slot:scale_relation:vg_artifact_common_plane_scale |
| G39 | 종이 바탕과 수채 워시·흑연의 물성 | photo_artifact_or_composition_only_pure_2d_deferred | slot:surface_material:pe_pencil_print |
| G40 | 선·명암 덩어리·경계·디테일의 위계 | photo_artifact_or_composition_only_pure_2d_deferred | slot:composition:primary_secondary_figure_ground_hierarchy |

## 보존과 완료 상태

격리 작업트리에서 데이터를 작성하고 검증한 뒤 실제 작업 디렉터리에 좁게 적용했다. 기존 미커밋 작업은 초기 해시와 비교했고 덮어쓴 파일의 정확한 이전 바이트를 보관했다. 런타임 코드와 원래 프로필·관계 데이터는 변경하지 않았다. 허용된 추가 파일·인덱스·검사 어댑터와 새 유지관리 원장만 적용했다. 커밋·푸시는 수행하지 않았다.

[적용·보존 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/keyword-visual-integration-20261007/primary-application.json) · [이전 파일 백업](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/keyword-visual-integration-20261007/before-overwritten) · [최종 보존 검사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/keyword-visual-integration-20261007/final-preservation-audit.json) · [원 리서치](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-07-prompt-keyword-enrichment-research.md)

후속 검증의 우선순위는 사례 2의 미세 표정·메니스커스·국소 반사·팔레트 가시성과 실제 후보 노출 부족, 사례 3의 인접 출입구 깊이·어두운 여백·수리 흔적이다. 현재 결과로 해당 주제의 효과 검증 완료를 주장하지 않는다. 통제된 전후 비교, 전체 회귀 자격과 요청자 판정은 아직 완료되지 않았다.

## 후속 main 반영

원격 main을 fetch/pull한 뒤 별도 작업트리에서 이번 변경만 분리했다. 원격 main의 기존 소스 등록 96개와 저작 데이터 원본을 보존하고 신규 등록 2개를 추가했다. 기존 후보 10,457개 중 10,426개는 전체 필드가 같고 31개는 승인된 맥락·동등 표현만 추가됐다. 새 후보는 18개다.

커밋 대상 소스의 의미 문서는 10,511개, 시각 프로필은 2,265개다. 앞선 로컬/네이티브 검사에 포함된 별도의 미커밋 지적 활동 데이터와 프로필 보강은 원래 작업 디렉터리에 보존하며 이번 커밋에 포함하지 않았다. 의미 벡터 입력 10,510개와 시각 입력 2,265개를 정확히 재사용했고, 병합된 원문이 다른 입술 압착 입력 1개만 새로 계산했다.

관련 검사 143개 중 142개가 통과했다. 남은 과거 전체 인벤토리 검사는 이번 문법 확장을 제외한 원래 main 구현에서도 같은 실패가 재현된다. 새 의미 검사 10개, 사전 검사와 양쪽 인덱스 검사는 통과했다. 기존 스냅샷·기대값은 바꾸지 않았고 전체 회귀 통과로 승격하지 않았다. 이번 병합에서 새 이미지는 생성하지 않았다.

자세한 검증과 소스 보존 근거: docs/research-evidence/photo-prompt/keyword-main-merge-20261007/README.md.
