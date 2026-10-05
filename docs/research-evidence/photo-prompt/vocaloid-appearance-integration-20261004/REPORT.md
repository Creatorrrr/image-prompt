# 보컬로이드 외형 연구의 시각 의미·후보 데이터 반영

기존 의미를 유지한 대체 표현 보강을 우선으로 반영했다. 기존 시각 프로파일 **65개**에 한·영 전체 형태 표현 **134개**, 구성 요소의 매칭·증거 대체 표현 **154개**를 추가했다. 기존 일반 후보 **55개**를 보강하고, 새 관계 프로파일 **19개**, 일반 후보 **25개**, 선택형 bundle **3개**를 추가했다. 원본 데이터 19개 파일이 변경됐다. 런타임 로드·원본 보존·집중 회귀 검사는 통과했다. 독립된 세 에이전트는 첨부 얼굴 참조로 서로 다른 복잡한 컨셉을 작성하고 네이티브 이미지 생성을 **4회** 호출했다. A·B는 출력 검토에서 차단돼 픽셀 검사를 실행할 수 없었다. C는 실제 이미지 2장을 생성했지만 두 장 모두 모든 선택 관계를 한 이미지에서 보여주는 검사에는 실패했다. 데이터 반영 성공과 이미지 검증 결과를 구분한다.

## 무엇을 보강했는가

동의어만 늘리지 않고, 같은 대상의 구성 요소와 연결 관계를 한·영으로 다시 서술했다. `paraphrase_examples`에는 전체 의미를, `authored_components`의 `match_terms`·`evidence_terms`에는 각 구성 요소의 대체 표현을 넣었다. 기존 프로파일의 이름, 활성화 조건, 의미 정의, 효과, 필수 관측 항목, 혼동 경계는 유지했다. 후보의 `paraphrases`, `keywords`, 긍정 검색 텍스트도 같은 의미로 보강했다.

예를 들어 일반 트윈테일은 두 묶임 기점과 각각에서 이어지는 모발 다발을 서술한다. 두 기점이 각 귀 윗끝보다 높다는 조건은 별도의 높은 트윈테일 프로파일로 만들었다. 일반 트윈테일 전체에 높이·길이·색을 기본값으로 넣지 않았다. 이어피스형 마이크는 귀의 장착부, 그 장착부에서 나오는 붐, 같은 착용자의 입 옆 종단이라는 연결을 함께 요구한다. 손에 든 마이크나 다른 사람의 입 옆 붐은 같은 의미로 취급하지 않는다.

기존 프로파일 보강은 머리·머리 장식·얼굴 표면 표시, 의복 절개·소매·주름·단·전통 의복 구조, 코스튬 부착 구조, 소재 표면, 성인 체형 축을 포함한다. 체형 축은 성인·측정 방향·비교 기준을 유지했다. 캐릭터 이름이나 chibi라는 단어로 실제 인물의 키·체격·머리 비율을 추정하지 않는다.

## 새로 구분한 19개 관계

| 연구 항목 | 런타임 프로파일 | 반드시 함께 보여야 하는 관계·범위 |
|---|---|---|
| K02 | `sca_high_twin_tail_roots` | 양쪽 기점이 각각의 귀 윗끝 위에 있고, 각 기점에서 별도의 모발 꼬리가 이어짐 |
| K06 | `sca_outward_hair_tips` | 모발 말단이 주변 흐름에서 바깥쪽으로 꺾임 |
| K09 | `sca_short_rear_long_sidelocks` | 짧은 후두부 머리와 얼굴 양옆의 긴 모발이 공존함; hime cut으로 치환하지 않음 |
| K15 | `sca_facial_surface_dot_scatter` | 얼굴 표면의 작은 분산 점; 원인·체질·정체성을 추정하지 않음 |
| K16 | `sca_local_dark_lip_contrast` | 입술 영역과 인접 피부의 명도 대비; 화장품·건강·색소 원인을 추정하지 않음 |
| K26 | `accessory_uncovered_foot` | 발이 신발·양말에 덮이지 않은 관측 가능한 상태 |
| K34 | `clothing_crop_top_waist_hem` | 상의 단과 허리의 길이 관계; 피부 노출을 자동 요구하지 않음 |
| K35 | `clothing_abdominal_bounded_opening` | 복부 위치의 경계가 있는 의복 개구부; 의상 종류를 수영복으로 고정하지 않음 |
| K44 | `costume_attached_rear_panel` | 코스튬의 뒤쪽에 이어지는 부착 패널과 연결부 |
| K51 | `accessory_earpiece_mouth_boom` | 귀 장착부 → 연결된 붐 → 같은 착용자의 입 옆 종단 |
| K52 | `sca_rigid_hair_tie_hardware` | 묶임 위치에 연결된 단단한 판·링형 장식; 발광·장치 기능을 추정하지 않음 |
| K53 | `sca_flat_equalizer_bars` | 같은 의복 표면의 평행 막대와 서로 다른 높이; 입체 장치로 치환하지 않음 |
| K54 | `sca_flat_keyboard_motif` | 같은 직물의 긴 밝은 직사각형과 짧고 어긋난 어두운 직사각형; 실제 건반 장치와 구분 |
| K55 | `sca_flat_control_panel_motif` | 같은 의복 표면의 평면 박스·표시 배열; 실제 버튼·작동 화면과 구분 |
| K56 | `accessory_arm_circular_speaker_gear` | 팔에 연결된 원형 스피커형 장식과 부착 관계 |
| K61 | `costume_external_membrane_wings` | 등에 외부 부착된 막형 날개; 실제 생물의 몸·비행 기능과 구분 |
| K62 | `costume_external_thin_wing_plates` | 등에 외부 부착된 얇은 판과 선 패턴; 투명·광택·발광은 별도 재질 선택 |
| K64 | `accessory_cap_face_motif` | 같은 모자의 눈·입형 표면 모티프; 착용자의 얼굴과 구분 |
| K68 | `accessory_cap_cross_glyph` | 모자 표면의 교차 선 도형; 흰 모자·빨간 기호·직업을 기본값으로 넣지 않음 |

새 프로파일마다 구성 요소 전체를 요구하는 관측 검사와 인접 형태의 오인 방지 조건을 넣었다. 구체적인 원본 출처, 대체 표현, 후보 ID, 원본 파일별 해시는 [INTEGRATION-LEDGER.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/vocaloid-appearance-integration-20261004/INTEGRATION-LEDGER.json)에 기록했다.

일반 후보 25개는 위 관계 19개와 기존 프로파일의 일반 후보 대응 6개다. 대응 6개는 짧은 bob, 늘어지는 땋은 머리, 모자 돌출부, 표면 선 모티프, 경계가 있는 몸 표면 패치, 머리 옆으로 치운 가면이다. 기존 의미 프로파일을 재사용했다. 새 bundle 3개는 짧은 후두부·긴 옆머리, 이어피스·입 옆 붐, 평면 이퀄라이저 막대다. bundle의 프로파일 연관 정보만으로 hard 의무가 자동 활성화되지는 않는다.

## 72개 연구 카드의 처리와 보류 경계

| 처리 | 카드 수 |
|---|---:|
| 기존 동등 표현 보강 | 37 |
| 새로 선택 가능한 관계 추가 | 19 |
| 기존 성인 체형 경계 보강 | 5 |
| 제한된 증거로 보류하거나 범위를 제한 | 11 |
| 합계 | 72 |

보류 11개는 뒷머리 묶음의 확정되지 않은 길이, 접힌 고리 땋기와 고정부, 너비를 길이로 확장하는 체형 표현, 피부·의복의 두 대상 색 대비, 측면 비대칭 단, pinafore의 bib·끈·치마 연결, 독립 부유 장식, 캐노피와 소매 스트리머의 서로 다른 소유자, 눈 주변 가림을 겹친 붕대 전체로 확장하는 해석, 독립 봉제 인형, 독립 파라솔 소품이다. 연구에 등장했다는 이유만으로 현재 슬롯 범위나 검증되지 않은 구조를 확대하지 않았다.

공식 패키지·원본 이미지를 추가로 확인한 8건도 기록했다. Macne 패키지는 측면 비대칭 단의 충분한 근거가 아니었고, Luka의 뒤 패널은 원본에서 보이는 범위로 제한했다. 모자 얼굴 표시와 모자 교차 기호는 색·직업·착용자 얼굴과 분리했다. 날개는 외부 코스튬 부착 구조로 다뤘다. 기존 연구의 캐릭터 이름·URL·설정 설명은 긍정 검색 별칭이나 인물 속성으로 옮기지 않았다.

## 원본 보존과 인덱스 반영

[PRESERVATION-AUDIT.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/vocaloid-appearance-integration-20261004/PRESERVATION-AUDIT.json)의 19개 원본 파일 검사는 모두 통과했다. 기존 ID와 보강 대상 이외의 값이 유지됐고, 실제 편집 입력 해시가 작업 시작 백업과 일치한다. 출처 유지 기록은 기존 기록을 지우지 않고 7개 후속 기록을 추가했다.

활성 런타임은 시각 프로파일 **1,690개**, 일반 후보 **9,865개**, 슬롯 **112개**, 의미 인덱스 문서 **9,901개**를 로드한다. 시각 인덱스와 sharded 의미 인덱스를 재생성했다. 기존 의미 인덱스 9,876개와 비교해 **25개 추가·80개 검색 텍스트 변경·0개 삭제**를 확인했고, 양쪽 manifest의 shard 해시도 검증했다. 갱신 전 시각 인덱스는 원본 해시 불일치로 거부되는 것도 확인했다.

인덱스 도구의 기본 정리 동작이 이전 shard 세대를 제거한 것을 발견해, 원래 존재하던 추적 파일 256개는 작업 시작 시 깨끗했던 HEAD 원본으로, 미추적 파일 48개는 보관된 동일 세대 백업으로 복구했다. 미추적 파일은 작업 시작 시 개별 바이트 백업을 만들지 않았으므로 동일 세대 백업과의 해시 확인을 복구 근거로 기록했다. 활성 manifest와 생성 테스트의 동결 스냅샷은 바꾸지 않았다. [SHARD-PRESERVATION-RECOVERY.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/vocaloid-appearance-integration-20261004/SHARD-PRESERVATION-RECOVERY.json)에 복구 출처·해시가 있다. 이후 재생성에는 `--keep-stale-generations`를 사용해야 한다.

런타임 생성·검색 코드의 동작은 이번 작업에서 변경하지 않았다. 작업 시작 때 있던 별도 변경을 포함한 현재 skill을 읽기 전용으로 복사해 세 에이전트가 같은 원본을 사용하게 했다. [SOURCE-SNAPSHOT.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/vocaloid-appearance-integration-20261004/SOURCE-SNAPSHOT.json)의 146개 파일은 스냅샷과 현재 원본 모두 해시가 일치한다. 공통 스냅샷 SHA-256은 `bbd95b0793a771491068b19315a537ea981917aec483ad101a111137f61cfe9d`다.

## 회귀 검증

집중 테스트 `tests/test_photo_vocaloid_appearance_paraphrases.py`의 6개 테스트가 통과했다. 하위 사례는 기존 65개 프로파일의 활성화·정의·효과·의무 보존, 새 19개 관계의 한·영 전체 구성 요소와 구성 요소를 하나씩 제거한 실패 사례, 긍정·부정·제외·advisory 구분, 잘못된 소유자와 인접 구조, 부모 속성 잠금과 재질 독립성, 성인 경계·출처 문구·보류 항목을 검사한다.

실제 런타임의 구성 요소 매처로 추가한 전체 대체 표현을 별도로 조회해 **65개 프로파일의 134/134개 표현이 해당 형태로 인식됨**을 확인했다. [PARAPHRASE-RUNTIME-PROBE.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/vocaloid-appearance-integration-20261004/PARAPHRASE-RUNTIME-PROBE.json)에 개별 결과가 있다. 이는 하위 매처 검증이며, 모든 입력에서 상위 후보 노출·hard 의무 활성화·이미지 표현을 보장하는 결과는 아니다.

기존 character-appearance 테스트의 특정 전체 데이터 해시·총개수 고정 검사는 현재 인덱스의 유효성과 기존 ID의 보존 검사로 바꿨다. 별도 의미 분야를 추가하면 과거 전체 해시와 총개수는 달라지기 때문이다. 기존 개별 정의·활성화·관측 검사 보존 테스트는 유지했다. 이 변경은 테스트 파일에만 적용했고 동결된 생성 스냅샷의 런타임 소스를 바꾸지 않았다.

costume 테스트는 원래 `ccx_` 계열의 94개 수를 유지하면서 전체 현재 후보 97개가 모두 인덱스에 들어 있는지 검사한다. 과거 liminal 딕셔너리와의 전체 동등성 검사는 포함된 원본·확장 파일에서 이번 연구가 선언한 대체 표현과 새 ID만 별도로 검사한다. 기존 항목은 보강 전 전체 필드를 유지하고 선언된 긍정 표현만 추가했는지 확인하며, 새 ID가 기존 항목을 덮어쓰지 않았는지도 확인한다. 이 후속 추가만 투영해 제거한 뒤 과거 전체 딕셔너리와 21개 유지 항목의 검사를 계속 수행한다. 이 함수 이외의 해당 테스트 모듈은 HEAD와 AST가 같다는 것도 확인했다.

별도 일러스트 스킬의 사진 회귀 기록은 과거 v1–v9를 바꾸지 않고 현재 데이터 관측인 [photo_regression_baseline_v10.json](/Users/chasoik/Projects/image-prompt/skills/subculture-illustration-image-generator/assets/photo_regression_baseline_v10.json)을 추가했다. 같은 동결 입력을 재생성해 코어·구성 digest, 공개 후보 64개, 부정 표현, 공개 계약의 보존을 확인했다. 일러스트 검증 코드에는 최신 v10을 선택·인식하는 두 줄만 추가하고, 현재 파생 baseline의 `validator_contract.sha256` 한 필드를 갱신했다. 시각 oracle·holdout·과거 실패 라벨·일러스트 생성 런타임은 바꾸지 않았다. [PHOTO-BOUNDARY-PRESERVATION.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/vocaloid-appearance-integration-20261004/PHOTO-BOUNDARY-PRESERVATION.json)과 [ILLUSTRATION-VALIDATOR-BINDING-REFRESH.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/vocaloid-appearance-integration-20261004/ILLUSTRATION-VALIDATOR-BINDING-REFRESH.json)에 변경 범위가 있다. 이 검증 메타데이터 변경은 사진 데이터 19개 파일의 집계와 별도다.

전체 unittest 회귀 결과는 **1,380개 고유 테스트 ID를 모두 검사하고 필요한 재검증을 거쳐 최종 1,380개 통과**다. 한 번의 깨끗한 연속 실행으로 기록하지 않는다. 처음 직렬 실행의 완료 구간 496개와 이후 분할 실행을 합쳤고, 초반 병렬 runner의 저장소 import 경로 누락으로 실행되지 않은 검사도 모두 다시 실행했다. loader·class setup 오류 자리표시는 테스트 통과 수에서 제외했다. 과거 전체 개수·해시·동등성 검사에서 생긴 실제 실패도 위 범위 수정 후 재검증했다. [FULL-REGRESSION-SUMMARY.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/vocaloid-appearance-integration-20261004/FULL-REGRESSION-SUMMARY.json)에 각 테스트의 최종 결과와 근거 실행 파일이 있고, 중간 실패 로그도 그대로 보존했다. 원본 딕셔너리 검증과 `git diff --check`는 통과했다. [FINAL-SOURCE-READBACK.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/vocaloid-appearance-integration-20261004/FINAL-SOURCE-READBACK.json)의 사진 데이터·스크립트 146개 파일은 테스트 및 생성에 사용한 동결 스냅샷과 현재 원본의 해시가 모두 같다.

## 독립된 세 컨셉의 이미지 검증

세 에이전트는 다른 에이전트의 프롬프트·후보팩·이미지를 보지 않고, 각자 임의 시드로 복잡한 컨셉을 정했다. 데이터 상세를 읽기 전에 컨셉 코어와 baseline을 동결했고, 같은 원본 스냅샷에서 정상 생성 경로로 각자 하나의 `photo-candidate-pack/v6`를 만들었다. 첨부된 이미지는 성인 코스튬 모델의 보이는 얼굴 외형 참조로 사용한다.

프롬프트 감사, 실제 참조 파일과 바이트가 묶인 이미지 요청 감사, 네이티브 생성, 원본 해상도의 픽셀 판정을 별도로 기록한다. 모든 필수 구성 요소와 연결 관계가 한 이미지에서 확인돼야 통과하며, 일부만 확인되거나 가려진 경우는 실패다. 선택형 후보의 구성·관계 검사와 실제 opt-in된 hard 시각 의무 검사도 구분한다. 사용자 수락은 별도이며 아직 받지 않았다.

| arm | 독립 컨셉 | 실제 채택한 신규 관계 후보 | 생성·픽셀 결과 |
|---|---|---|---|
| A | 비가 그친 녹음 컨트롤룸에서 마지막 페이더 조정 후 카메라를 돌아보는 모델 | 이어피스·입 옆 붐 | 네이티브 1회, 출력 차단, 픽셀 검사 미실행 |
| B | 매화 과수원·세라믹 조형물 정원에서 회전 리허설을 마친 전자 공연 모델 | 이어피스·입 옆 붐, 외부 부착 얇은 날개판 | 네이티브 1회, 출력 차단, 픽셀 검사 미실행 |
| C | 설치 중인 프로젝션 갤러리에서 허리 패널을 고정하는 모델 | 짧은 후두부·긴 양옆 머리, 이어피스·입 옆 붐, 덮이지 않은 발 | 네이티브 2회, 실제 이미지 2장, 전체 관계 검사 실패 |

A와 B는 모두 `moderation_blocked`, `stage=output`, `categories=[sexual]`을 반환했다. 정확한 도구 오류와 요청 ID를 보존했다. 반환된 픽셀이 없으므로 형태 반영의 성공·실패를 판단하지 않는다. 이 오류만으로 어떤 문구나 참조가 원인인지 추정하지 않았고 다른 생성 경로로 우회하지 않았다.

C의 1차 이미지는 선택 데이터 구성 요소 **6/8개 확인, 2개 가림**이었다. 이어피스의 연결·입 옆 종단과 선택한 왼발은 확인됐지만, 후두부 경계가 가려져 짧은 뒤·긴 양옆 머리 전체 관계를 확인할 수 없었다. 같은 코어·후보팩·원본 참조를 유지하고 머리와 카메라 투영에 관한 두 문장만 최소 보정해 2차 이미지를 생성했다. 2차는 **4/8개 확인, 4개 관측 불가**였다. 짧은 후두부와 이어피스 관계는 보였으나, 두 긴 양옆 머리의 연속 경로가 의복 테두리와 겹쳤고 선택한 가까운 왼발이 프레임 아래로 잘렸다. 별도 신체 실현 검사도 **3/5개 통과, 2개 실패**였다. 다른 발이나 1차 이미지에서 확인한 발을 2차의 부족한 증거로 합산하지 않았다.

root가 원본 해상도로 두 결과를 독립 재검토했다. 2차의 모발·의복 겹침을 다시 확인해 처음의 더 낙관적인 판정을 4/8로 낮췄고 이전 판정 파일도 보존했다. 필수 관계가 하나라도 관측 불가이면 `partial_is_fail`에 따라 해당 이미지 전체는 실패다. 보이는 이어피스 관계는 부분 증거로 남기되 전체 컨셉 통과로 기록하지 않는다.

| C 시도 | 원본 이미지 | 프롬프트 | root 픽셀 재검토 |
|---|---|---|---|
| 1 | [이미지 1](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/vocaloid-appearance-integration-20261004/qualification/arm-c/generated_images/attempt-1.png) · 1024×1536 | [프롬프트 1](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/vocaloid-appearance-integration-20261004/qualification/arm-c/final_prompt_attempt_1.txt) | [6/8 확인, 전체 실패](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/vocaloid-appearance-integration-20261004/ROOT-REVIEW-arm-c-attempt-1.json) |
| 2 | [이미지 2](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/vocaloid-appearance-integration-20261004/qualification/arm-c/generated_images/attempt-2.png) · 1237×1272 | [프롬프트 2](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/vocaloid-appearance-integration-20261004/qualification/arm-c/final_prompt_attempt_2.txt) | [4/8 확인, 전체 실패](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/vocaloid-appearance-integration-20261004/ROOT-REVIEW-arm-c-attempt-2.json) |

A의 [실제 호출 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/vocaloid-appearance-integration-20261004/qualification/arm-a/attempt-01/final_prompt.txt), B의 [실제 호출 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/vocaloid-appearance-integration-20261004/qualification/arm-b/final_prompt.txt)도 보존했다.

각 arm의 `KEYWORD-TRACE.json`은 실제 후보 노출 → 선택 → 최종 프롬프트 문구 → 해당 이미지의 판정을 연결한다. 기존 baseline에 있던 일반 외형이 보였다는 이유로 새 데이터 채택 성공이라고 계산하지 않는다. 프로파일이 visual-concept 목록에 노출되지 않은 경우도 기록한다. 이번 세 컨셉의 결과를 보강한 프로파일 65개나 새 관계 19개 전체의 픽셀 품질로 일반화하지 않는다.

실제 채택한 신규 후보는 서로 다른 4개다. 3개 컨셉 중 이미지가 반환된 컨셉은 1개, 출력 차단은 2개이며, 반환된 이미지 2장의 완전 통과 수는 0이다. 차단 2개를 픽셀 품질 실패로 집계하지 않는다. 실제 후보·bundle 노출과 선택은 확인했으나 이 팩들에서 해당 신규 연관 프로파일은 hard opt-in 목록에 노출되지 않았다. 연관 정보만으로 의무를 강제 승격시키지 않았다.

[ROOT-BINDING-AUDIT.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/vocaloid-appearance-integration-20261004/ROOT-BINDING-AUDIT.json)은 각 팩·코어·프롬프트·부정 표현·첨부 참조 해시와 실제 네이티브 호출 인자를 확인했고, C의 두 이미지가 네이티브 원본의 정확한 바이트 복사임을 확인했다. 바인딩 감사 통과는 픽셀 통과와 구분한다. 최종 생성 경로, 실제 호출 횟수, arm별 판정은 [QUALIFICATION-SUMMARY.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/vocaloid-appearance-integration-20261004/QUALIFICATION-SUMMARY.json)에 확정했다. 소스·증거·테스트 변경은 로컬 작업 상태이며 커밋하거나 푸시하지 않았다.

## 후속 반영 우선순위

이번 대체 표현과 출처 기반 관계 데이터는 현재 원본·인덱스에 반영했다. 다음 이미지 품질 작업에서는 선택한 발 전체가 들어오는 프레이밍, 머리와 의복 테두리를 분리하는 시점·색 대비, 양옆 모발의 연속 경로를 우선 확인해야 한다. 후보가 선택됐다는 사실과 연관 시각 프로파일이 hard 의무로 노출됐다는 사실은 계속 따로 검사한다. 현재 관측으로 의미 정의나 활성화 조건을 느슨하게 만들 근거는 없다. 추가 생성과 아직 선택되지 않은 관계의 픽셀 검증은 이번 실제 결과와 별도 작업이다.
