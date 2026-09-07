# 개화기 시각 의미·후보 데이터 반영 및 독립 이미지 검증

## 반영 범위

조사에서 제안한 16개 형태·관계 프로파일, 각각 4개의 시각 성분(총 64개)을 실제 로더에 연결했다. 후보 64개와 선택형 묶음 16개를 추가하고 시각 프로파일/의미 검색 인덱스를 다시 생성했다. 전체 시각 프로파일은 379개, 의미 검색 항목은 8,260개다. 기존 111개 후보 묶음은 127개가 되었다.

시대명, 지명, 사회적 명칭만으로 전체 프로파일을 강제하지 않는다. 예를 들어 ‘개화기’, ‘한복’, ‘양산’, ‘정관헌’만으로 네 성분 전체를 활성화하지 않는다. component-complete exact 관계는 강제 근거가 될 수 있지만, 임베딩·검색·선택형 묶음은 기존 의미를 대체하거나 프로파일을 강제 승격하지 않는다.

이 프로파일들은 구체적인 촬영 변형의 계약이다. 한복·개량복·개화기 전체의 보편적 정의가 아니다. 의복·건축·소품의 시대별 주장과 출처 한계는 별도의 해시 결합 유지관리 레코드에 남겼다. 런타임에 자동 연대 판별기나 역사적 진위 인증기를 추가한 것은 아니다. 본문 출처는 [조사 보고서](report-source.md), 세부 성분은 [데이터 제안](candidate-data-proposal.json)을 참조한다.

| 형태·관계 묶음 | 적용 맥락 | 조사 근거 ID |
|---|---|---|
| hanbok_handheld_parasol | early_or_later_conditioned | S01, S02 |
| reformed_hanbok_length_closure | later_or_source_dated | S02 |
| durumagi_seasonal_layer | early_or_later_conditioned | S01 |
| tailcoat_formal_tail_topology | empire_1900_plus_conditioned | S03, S04 |
| frock_coat_long_skirt | empire_1905_rule_or_explicit_reference | S03 |
| western_blouse_reference | western_reference_or_modern_reinterpretation | S14 |
| bob_cloche_optional_pair | later_1920s_reference | S05, S13 |
| hybrid_veranda_architecture | named_site_state_required | S09 |
| hanok_chair_contact | creative_scene_source_conditioned | S01, S11 |
| hotel_coffee_service | hotel_1902_or_specific_source | S10, S11 |
| later_cafe_reading | later_1920s_1930s | S07, S10 |
| disc_gramophone_listening | source_model_required | S16, S17, S18 |
| wall_phone_separate_receiver | source_model_required | S15 |
| bellows_camera_sitting | source_camera_date_required | S12 |
| rail_platform_departure | route_date_required | S19 |
| modern_reinterpretation_layers | modern_reinterpretation | S14, S20, S21, S22 |

## 구현 파일

- `skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_opening_era.json`: 16개 프로파일, 64개 렌더 게이트, 혼동 대체물과 범위 제한.
- `skills/photo-prompt-image-generator/assets/photo_prompt_opening_era_extension.json`: 실제 기존 슬롯의 64개 원자 후보 및 16개 선택형 묶음.
- `skills/photo-prompt-image-generator/scripts/prompt_generator.py`: 두 확장 로더 연결.
- `skills/photo-prompt-image-generator/assets/photo_prompt_tags.json`: 필수 확장 등록. 전역 슬롯 소유 정책은 유지하고 새 소품 후보에만 setting/action 범위를 명시했다.
- `docs/research-evidence/photo-prompt/extension-maintenance/photo_prompt_opening_era_extension.json`: 조사 출처·시대 적용 범위·한계를 런타임 후보 문구 밖에 보존.
- 의미/시각 인덱스 재생성. 기존 샤드 디렉터리 교체는 인덱스 빌더의 정상 세대 교체 결과다.
- `tests/test_photo_opening_era_semantics.py`: 성분 전체/부분 경계, 광역 명칭 오활성화, 64개 후보 병합과 인덱스, 선택형 묶음 공개·누락·닫힌 차원, 출처 해시, 합성 벡터를 사용한 임베딩 후보의 optional 경계.
- `tests/test_photo_candidate_semantics.py`: 신규 데이터에 맞춰 후보 묶음 개수 111→127, 유지관리 레코드 개수 11→12만 갱신.

## 독립성 및 실행 이력

사용자 원문을 그대로 담은 요청 envelope를 각각 먼저 동결한 뒤, 주변 작업 내역을 넘기지 않는 독립 서브에이전트 3개를 만들었다. 각 에이전트는 SKILL.md와 첨부 이미지, 일반 지식만으로 난수 선택·컨셉·기본 프롬프트·테스트를 만들고 해시를 동결했다. 기본 컨셉을 만든 이후에만 로컬 후보 데이터에 접근했다. 참조 이미지는 보이는 성인 외형의 참고로 사용했으며 실제 인물의 신원이나 국적 등을 추론하지 않았다.

초기 v1 스냅샷의 추가 테스트에서 소품 범위 누락 및 유지관리 해시 형식 불일치를 발견했다. 이미지는 생성하지 않은 상태에서 v1 프리플라이트를 폐기 표시하고, 기본 컨셉을 변경하지 않은 채 수정된 v2 스냅샷으로 모두 통일했다. 따라서 스냅샷 재발급 이력이 있으며 ‘처음부터 재실행이 전혀 없었다’고 주장하지 않는다. 이미지 생성은 각 에이전트 1회, 결과를 고르기 위한 재생성은 없다.

최종 동결 스냅샷 SHA-256: `d19b7a555e4a36810daa54314014b8c28da419afb4d29cd753d34221cb131b2a`.
아티팩트 루트: `artifacts/photo-runs/opening-era-three-arm-20260907/`.

## 후보 전달 판정 — FAIL, 0/3

세 실제 v6 공개 후보팩에는 `opening_` 후보가 0개이고, 신규 묶음도 0개였다. 세 기본 컨셉은 촬영·구도·조명 등의 차원만 열어 두었고, 신규 묶음 16개는 모두 하나 이상의 닫힌 차원을 필요로 했다. 따라서 **16개 묶음 전부가 기존 차원 소유 규칙에 의해 각 테스트에서 선택 불가**였음은 확인했다. 이것만으로 모든 원자 후보의 검색 미노출 원인까지 확정할 수는 없다.

`candidate_scope_diagnostic.json`에 각 테스트/묶음별 닫힌 차원을 남겼다. 모든 구성원이 실제 공개되고 차원이 열려 있는 통제된 단위 테스트에서는 16개 묶음의 노출과 누락 시 차단이 통과했다. 그러나 이는 이번 실제 요청에서 후보가 전달됐다는 증거가 아니다.

이 세 이미지는 독립적으로 정한 개화기 관련 장면을 얼마나 표현했는지 검사한다. **신규 후보를 실제로 채택해 이미지가 개선되었다는 인과적 검증은 성립하지 않는다.** 기본 프롬프트를 신규 데이터에 맞춰 다시 쓰거나, 미채택 후보를 채택한 것으로 기록하지 않았다. 이후 후보 전달 개선 실험은 새로운 독립 사전 동결 설계로 검증해야 한다.

## 최종 검증 결과

코드 회귀검증 62건 PASS, 별도로 추가한 임베딩 경계 테스트 1건 PASS. 사전 의미 경계 테스트의 16개 프로파일별 subtest도 통과했다. 사전 전체 저장소 테스트를 통과했다는 주장은 하지 않는다. 사전·시각 인덱스·의미 인덱스·장면 표현 감사 PASS. 추가 테스트 전에 발견한 실패와 수정 이력은 위에 남겼다.

프롬프트 감사와 정확한 이미지 요청 감사는 3/3 PASS. 이미지 파일 3개가 실제 반환됐으며 각 1회 생성했다. 부모 에이전트도 세 이미지의 픽셀을 직접 확인했다. 초기 기본 프롬프트 파일 해시 불변, 정규화 core/intent-lock과 manifest 일치, 생성 파일 해시 일치, 최종 스냅샷 83개 파일 불변을 확인했다.

| 독립 컨셉 | 사전 시각 조건 | 실패/한계 | 새 후보 전달 |
|---|---:|---|---|
| 한복·비 갠 마당·여행함의 리본 | 8/8 PASS | 동작은 정지 화면의 손 접촉·리본 형태로 판정 | 0개, FAIL |
| 프록코트·회중시계·벨로스 사진관 | 3/5 PASS, 전체 FAIL | 나뉜 코트 자락 확인 불가, 지정한 3/4 프레임 대신 신발까지 포함 | 0개, FAIL |
| 1935년풍 카페·신문·축음기 | 4/7 PASS, 전체 FAIL | 왼손이 신문을 눌러 펴지 않음, 청취 시선 불명확, 바늘이 바깥 홈이 아닌 라벨 부근 | 0개, FAIL |

이 비율은 서로 다른 사전 테스트의 조건 개수이며 동일 난이도 점수나 통계적 성공률이 아니다. 부분 충족은 해당 조건 FAIL로 처리했다. 사용자 미적 판단은 pending이다.

표준 `moe-render-review` 계약 검증은 활성 프로파일 계약이 없어 arm01에서 schema FAIL을 반환했다. arm02/03은 해당 검증을 not applicable로 기록했다. 따라서 위 픽셀 결과는 **사전 동결된 독립 테스트의 수동 관찰**이며 표준 시각 프로파일 검증기를 통과한 것으로 보고하지 않는다.

정확한 판정: **데이터 구현 완료, 코드 검증 통과, 3개 이미지 테스트 완료, 실제 신규 후보 전달 검증은 실패**. 신규 데이터의 렌더 효과나 미적 개선을 승격하지 않는다. 커밋·푸시는 하지 않았다.

전체 실행 기록: `artifacts/photo-runs/opening-era-three-arm-20260907/validation-result.json`.
부모 픽셀 검토: 같은 경로의 `parent_pixel_review.json`.
각 arm에는 사용자 envelope, 난수 선택, 동결 기본 프롬프트, 실제 공개 후보팩, 최종 프롬프트, composed/runtime audit, 생성 이미지, pixel review, 실행 ledger와 manifest를 보존했다.
