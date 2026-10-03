시각 의미 데이터의 대체 표현 보강과 후보팩 반영을 완료했습니다. 기존 시각 의미 owner **18개**, 기존 후보 **22개**에 관계를 유지하는 한국어·영어 표현을 보강했고, 새로운 관찰 관계 **12개**를 시각 의미 profile과 일반 후보에 각각 추가했습니다. 세 독립 agent가 참조 사진을 사용하여 서로 다른 복잡한 장면을 작성하고 총 **5회** native 이미지를 생성했습니다. 최종 장면 단위 판정은 **1 PASS / 2 FAIL**입니다. 실패한 요소와 관찰할 수 없는 요소를 성공한 요소와 함께 보존했습니다.

이 통합·이미지 검증 단계에서는 commit·push를 수행하지 않았습니다. 이후 요청에 따른 pull·양쪽 의미 보존·병합 검증 기록은 [병합 보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-merge-20261003/README.md)에 별도로 연결합니다. 아래 수치와 receipt는 통합 당시의 관찰을 보존합니다. 첨부 사진은 보이는 얼굴·머리카락의 안내로 사용했습니다. 각 장면의 26·28·27세 성인 설정, 체형, 의복과 행동은 별도로 작성한 가상 인물의 설정입니다.

**반영한 데이터와 의미 경계**

[선행 리서치](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-visual-semantics-20261003/RESEARCH.md)의 234개 표기를 모두 새 exact alias로 넣지 않았습니다. 28개 후보 초안을 **신규 12 / 기존 owner 재사용 10 / 보류 6**으로 전환했습니다. [DISPOSITION-BRIDGE.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/DISPOSITION-BRIDGE.json)에 모든 표기의 근거 수준, 연구 판단, 관련 시각 관계, runtime owner와 보류 이유를 연결했습니다. 새로 승격한 원문 은어 exact alias는 **0개**입니다. 직접 확인되지 않은 표기, 사건·역할·시간·평가 의미는 연구 기록에 남습니다.

| 보강한 계열 | 관찰 가능한 대체 표현의 중심 | 구분하는 경계 |
|---|---|---|
| 눈·입·혀·볼 | 각 개안부 안의 동공 위치, 입술 사이 틈과 턱 하강, 자기 입에서 이어져 입술 경계를 넘는 혀, 지정 볼의 국소 붉은 색 | 고개 각도와 동공 배치, 반개안과 감은 눈, 입 안의 혀와 바깥 혀, 프레임 전체의 붉은 조명 |
| 한손·양손 V | 검지·중지의 분리, 나머지 손가락 접힘, 각 손목·팔꿈치·어깨로 이어지는 소유 관계 | 다른 인물의 손, 복제 손, 손가락 일부만 보이는 자세 |
| 앉기·벌림·M형·누움 | 같은 골반의 좌면 지지, 굽힌 무릎의 좌우 분리, 개별 다리 연결, 발 지지, 선택한 정면에서 읽히는 M 윤곽 | 서서 발만 벌린 자세, 의자 걸터앉기, 시점을 바꿔 만든 문자형 윤곽 |
| 몸의 양감·의복 | 전신과 국소 부위 양감, 부위 간 연속 윤곽, 의복 접촉면, 지정 패딩의 외곽 | 한 부위의 크기와 전체 체형, 원단 부피와 신체 부피, 신체와 의복 패딩 |
| 눈·피부 문양 | 동공 영역 안의 하트와 지정 매체, 배꼽 기준 피부 문양의 방향·거리, 선택한 선 연결·분리·대칭·색 | 눈 전체를 하트로 대체, 하트 반사광, 옷 위 기호, 기본 하트·발광·대칭을 임의 추가 |

새 관찰 관계는 `sv_upward_pupils`, `sv_inward_pupils`, `sv_left_right_pupil_relation`, `sv_tongue_lip_boundary`, `sv_local_cheek_redness`, `sv_pupil_heart_motif`, `sv_seated_knees_apart`, `sv_supported_m_legs`, `sv_supine_limb_spread`, `sv_padded_garment_contour`, `sv_lower_abdominal_skin_marking`, `sv_declared_skin_motif_topology`입니다. `sv_supported_m_legs`는 정면에서 골반과 양발 지지가 보이는 좁은 변형입니다. 일반적인 모든 M자 포즈와 동의어로 취급하지 않습니다.

[새 시각 의미 데이터](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_slang_visual.json)는 **36개 authored component와 원본 픽셀 gate**를 가집니다. 각 component에 원래 영어 관찰, 대체 영어, 한국어 표현을 함께 작성했습니다. 지지·소유자·매체·동시성 등 필요한 구성요소를 모두 요구합니다. 기존 4개 component owner에도 26개 대체 표현을 추가했습니다. [후보 데이터](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_slang_visual_extension.json)는 새 일반 후보 12개와 기존 후보 22개의 표현 overlay를 담당합니다. 기존 후보의 ID, label, 속성 효과와 guard는 유지했습니다.

`composite_overwhelmed_expression`에서는 작고 대칭적인 O형 입, 중앙의 작은 혀, 홍조·피로·특정 눈썹을 모든 변형의 필수 조건으로 강제하던 부분을 바로잡았습니다. 원래 장르 의미는 claim limit에 유지하고, 중립적인 얼굴 형태는 부분적인 시각 투영으로 명시했습니다. 이미 존재하던 일부 구성요소의 optional 발견 기준은 유지합니다. 채택 후의 픽셀 통과는 **지정 눈 배치 + 선택한 벌어진 입 + 밖으로 이어진 혀 + 같은 얼굴의 동시 표시**를 모두 요구합니다.

`soft_full_figure_volume`와 `bust_prominence_relation`에서는 비시각적인 설명 문장을 필수 관찰 증거로 쓰던 부분을 긍정적인 윤곽 관계로 수정했습니다. 얼굴 표정·몸의 형태·의복·피부 문양의 효과를 각 owner/property에 선언했고, 상위 속성 효과가 하위 property lock을 우회하지 못하도록 검사합니다.

**세 독립 테스트의 실제 결과**

각 agent는 독립 seed로 장면을 선택하고 참조 범위를 정한 뒤, 후보를 보기 전에 controls·baseline·core·embodiment review를 동결했습니다. 다른 arm의 후보·프롬프트·이미지를 읽지 않았습니다. 각 arm은 원래 V6 후보팩 한 개를 사용했습니다. 실패 arm은 동일 core와 후보 선택을 유지한 표적 재시도 한 회만 추가했습니다.

| 장면과 seed | 실제 채택 | 원본 픽셀 결과 | 최종 전달 |
|---|---|---|---|
| 항구 창고 인형극 축제의 매표소 고장 순간 · `187680095935288485` | 복합 얼굴 표정 profile, 양손 V bundle | 눈·입·혀와 양손 V가 같은 인물에서 동시 표시. 정식 **10/10**, 보충 **7/7 PASS** | [프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-1/prompt.txt) · [원본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-1/attempt-1/native.png) · [보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-1/report.md) |
| 운하 수문 옆 이동식 그림자극 무대의 작업 휴식 · `8290468901664686725` | 지지된 M형 일반 후보, 전신 양감·좌면 압축 profile | M 윤곽·좌면·양발 지지 PASS. **8/12 → 11/12**, 몸통·복부 양감 FAIL. 종아리 양감 UNOBSERVABLE. 전체 **FAIL** | [최종 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-2/prompt.retry1.en.txt) · [최종 원본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-2/native_attempt_2.png) · [보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-2/report.md) |
| 유리 지붕 식물 작업실의 문양·색소 점검 · `6406798815013629455` | 최초 후보팩에서는 대상 후보 미노출, 선택 0개 | 양쪽 동공 하트·하복부 피부·네 도형 연결 관계 PASS. 배꼽→중앙 도형 거리/전체 문양 폭 목표 **0.67**, 수동 추정 **약 0.25 → 0.39**로 FAIL. 전체 **FAIL** | [최종 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-3/final_prompt.txt) · [최종 원본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-3/native-attempt-2.png) · [보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-3/report.md) |

첫 생성의 실패 원본도 보존했습니다: [그림자극 첫 이미지](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-2/native_attempt_1.png), [식물 작업실 첫 이미지](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-3/native-attempt-1.png). 서로 다른 이미지의 성공 요소를 합쳐 한 장의 PASS로 판정하지 않았습니다.

식물 작업실의 투명 렌즈 경계는 원본에서 해상되지 않습니다. 따라서 **동공 안 하트의 보이는 형태**와 **물리적인 인쇄 렌즈 매체**를 구분합니다. 렌즈 소재·제작 방식과 실제 센티미터 크기는 UNOBSERVABLE입니다. 이 arm의 정식 embodiment 5/5는 이 국소 문양 테스트를 인증하지 않습니다. [Root의 별도 원본 검수](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/ROOT-PIXEL-REVIEW.json)도 세 agent와 같은 장면별 판정을 기록했습니다.

모든 대상 형태는 후보 조회 전의 baseline에도 있었습니다. Baseline-only 생성이나 통제된 A/B가 없으므로 보이는 결과를 새 데이터만의 인과 효과로 주장할 수 없습니다. 특히 식물 작업실 arm은 대상 후보가 노출·채택되지 않았으므로 대상 데이터의 기여는 0입니다. PASS는 기술적인 시각 조건의 판정이며 사용자의 선호·수용 판정은 별도입니다.

**후보 노출 결함 수정과 검증**

식물 작업실에서 `adult`라는 나이 맥락 태그가 기존 adult-content guard로 처리되어 sensual=0일 때 중립적인 눈·피부 후보를 제거하는 결함을 발견했습니다. 새 중립 후보들에 기존 runtime이 지원하는 `age_context_only`를 선언했습니다. Runtime 분류 규칙이나 기존 성적 연출 후보의 guard는 변경하지 않았습니다.

같은 네 authored 입력 파일, 같은 seed, 같은 baseline·core·controls·embodiment·negative로 조회한 [별도 회귀 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/postrepair-retrieval-receipt.json)에서 하트 동공·하복부 문양·선 topology 일반 후보가 모두 노출됩니다. 이 조회의 이미지 호출은 0회입니다. 새로운 optional profile의 엄격한 구성요소 admission은 유지되어 해당 재조회에서도 노출되지 않았습니다. 원래 테스트 후보팩·선택·미노출·실패 결과를 소급해서 바꾸지 않았습니다.

최종 corpus는 **profile 1,576 / slot 후보 9,795 / semantic index 9,831 entries**입니다. Visual·semantic index는 authored data에서 Gemini embedding 또는 내용이 정확히 일치하는 기존 벡터를 사용하여 다시 생성했습니다. 직접 index 벡터를 작성하지 않았습니다. Dictionary validator와 visual index 정합성 검사를 통과했습니다.

전체 발견 대상 **153개 테스트 모듈, 1,332개 테스트**를 통과했습니다. 안정된 corpus에서 수행한 전체 sweep의 실패 모듈 한 개는 새 선언된 expression 범위를 테스트 입력에서 명시하도록 수정한 뒤 **모듈 전체 27개를 재실행하여 통과**했습니다. 표정이 열려 있지 않거나 잠긴 경우 차단되는 회귀도 추가했습니다. 고정 routing fixture와 이전 V1–V7 경계 기록, 네 frozen authoring 입력은 byte 그대로 유지합니다. Corpus 변경으로 달라지는 조회 관찰만 V8에 추가했습니다. [검증 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/VERIFICATION-RESULT.json)는 각 모듈의 성공 로그와 현재 소스 hash를 연결하며, 초기 실패 sweep도 보존합니다.

5개 생성 모두 composition·runtime audit PASS이며 원본 byte·참조 이미지·프롬프트·candidate/core/lock·shared ledger 바인딩을 확인했습니다. Native 도구가 개별 image model ID를 반환하지 않아 모델 이름은 unknown으로 기록합니다. [NATIVE-INTEGRITY.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/NATIVE-INTEGRITY.json)에 모든 시도와 hash를 저장했습니다. Native 생성 시점의 corpus는 [초기 receipt](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/qualified-inputs.json)와 전체 source archive로 보존하고, 그 이후 수정된 최종 corpus는 [별도 receipt](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/FINAL-CORPUS-RECEIPT.json)로 구분합니다. 전체 source archive는 대용량 재현 자료를 로컬에 보관하는 기존 저장소 규칙에 따라 로컬에 유지하며, manifest·hash·원본 이미지와 감사 기록을 추적합니다.

**결과를 이어서 강화하는 순서**

1. 몸의 양감은 상완·몸통·골반·허벅지·종아리 관찰을 부위별로 분리하고, 같은 이미지에서 전신 연속 양감을 확인합니다. 복부를 다른 부위의 크기로 대신 통과시키지 않습니다. 다음 qualification에서는 문장의 반복보다 복부의 옆 윤곽·허리 양감과 종아리의 관찰 가능성을 먼저 설계합니다.
2. 하복부 문양은 절대 cm와 사진에서 검증할 수 있는 비율을 구분합니다. 배꼽·중앙 도형·전체 폭 landmark와 허용 오차를 생성 전 동결하고, 여러 거리 비율을 가진 별도 case에서 크기와 위치를 독립적으로 검증합니다. 렌즈 재질의 증거가 필요하면 그 매체가 실제로 보이는 별도 관찰 구도를 사용합니다.
3. 나머지 새 관계는 inward/asymmetric pupils, 국소 볼 색, seated separation, supine spread, garment padding의 최소 관계와 서로 혼동되는 negative case를 원본 이미지로 qualification합니다. 데이터·인덱스 테스트의 통과를 이미지 통과로 확대하지 않습니다.
4. 아직 직접 확인되지 않은 187개 표기는 추가 원전·실제 사용 문맥 확인과 owner 충돌 검토 후에만 alias 승격을 검토합니다. 두 인물 비교, 시간 전후와 편집 전후 초안은 필요한 다중 target·paired evidence 계약을 먼저 마련합니다.
5. 데이터 기여 자체를 측정할 필요가 생기면 같은 frozen core·참조·관찰 조건으로 baseline-only와 대체 표현 적용 arm을 별도로 설계합니다. 해당 결과가 생기기 전까지는 이번 데이터를 검색·표현·검증 계약의 보강으로 평가합니다.

반영 파일의 정확한 범위는 [authored-change-receipt.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/authored-change-receipt.json)에 있습니다. 등록 변경은 generator의 extension 목록 두 줄이며, 나머지 runtime 동작은 기존 계약을 사용합니다. 이전 다른 연구 자료와 index generation은 보존했습니다.
