Arm C v2는 후보 노출·조합·런타임 감사에 통과했으나, 실제 픽셀의 엄격 전체 판정은 **FAIL (효과 1/3 통과)** 입니다. PARTIAL은 FAIL로 처리했습니다. 사용자 수용 판단은 pending입니다.

| 테스트 | 원본 픽셀 결과 | 근거 |
| --- | --- | --- |
| 붉은 문진 컬러 스플래시 | FAIL | 문진은 붉지만 나머지 화면에 넓은 따뜻한/세피아 색조가 남음. 문진 마스크 외 RGB 채널차 중앙값 7/255; 88.36%가 3 초과. |
| 상승 검정 계조 | FAIL | 어두운 세부는 읽히지만 가장 깊은 머리뿌리와 선반 안쪽에 충분히 명백한 soft-charcoal floor가 유지되지 않음. 뿌리 p01 휘도 21.82, p05 28.07; 선반 p01 24.07. |
| 피부결 보존 국부 톤 정리 | PASS | 원래 해상도에서 볼의 국부 톤 전환과 미세 모공/자연스러운 피부 변화가 함께 읽히며, 참조 얼굴의 가시적 구성이 유지됨. |

선택 프로필 게이트 4/6, 물리 게이트 5/5, 결합 게이트 9/11입니다. `vo_pe_red_object_splash_relation_2`와 `vo_pe_lifted_black_floor_relation_1`이 실패했습니다. 형태·소유·관절/도달·지지·접촉·가시성의 물리 조건과 얼굴/헤어 범위의 참조 가이드는 통과했습니다. 픽셀 감사 레코드의 schema_failures는 빈 목록이며 technical_qualified는 false입니다. 감사기는 사람이 작성한 픽셀 근거를 검증하며 픽셀을 독립 추론하지 않습니다.

원래 secrets 랜덤 seed `8f0040ca75299371254dbda8c32957fd`와 theater-repair 컨셉을 그대로 사용했습니다. 마지막 공연 직후 극장 소품 수리실에서, 가상의 성인 여성이 붉은 에나멜 문진과 반대 손으로 말리는 무대 도면을 펴면서 사진가를 잠깐 바라봅니다. 새 장면·새 core·새 controls resolver·requester lock 승격은 없습니다. 이전 안전한 retry의 단추 잠긴 면 작업셔츠와 neutral engaged expression을 유지하는 open authorial repair를 적용했습니다. 가장 낮은 계조의 45/255 표현은 렌더 안내이며 새로운 requester 수치 조건이나 독립 판정 임계값이 아닙니다.

v2 source로 정확히 한 팩 `b8ac119256abc2dd`을 생성했고 compact composer view를 먼저 읽은 뒤 전체 선택 상세를 읽었습니다. 실제 선택 후보는 `slot:color_grading:pe_red_object_splash`, `slot:color_grading:pe_lifted_black_floor`, `slot:skin_finish:pe_texture_preserving_tone_evening`입니다. 실제 선택 opt-in 프로필은 `visual-concept:pe_red_object_splash_relation`, `visual-concept:pe_lifted_black_floor_relation`, `visual-concept:pe_texture_preserving_tone_evening_relation`입니다. 세 슬롯의 모든 concept unit/relation과 세 프로필의 모든 literal component/게이트를 보존했습니다. 관련 없는 optional bundle은 선택하지 않았습니다.

최종 prompt는 312 단어입니다. composed/runtime PASS, negative 원문 일치, reference 파일 해시 일치입니다. 조합의 일반 anchor 후보 미노출 경고 4개는 literal free description으로 보존된 원래 네 anchor에 대한 경고이며 실패는 없습니다. 이 결과는 올바른 후보 노출이 실제 픽셀 성공을 보장하지 않는다는 증거입니다.

builtin `image_gen.imagegen`을 v2에서 1회 호출했습니다. arm 누적 호출은 3회이며 v1의 최초 safety block은 unscored로, 성공 retry와 모든 원문/ledger/image를 그대로 보존했습니다. 새 성공 run `9d2f2d49080ac1e9`은 v1의 마지막 run `598e8c9471e7c156`에 연결했습니다. 추가 생성이나 CLI/provider 전환은 없었습니다. v2 누적 ledger는 v1 두 행을 정확한 byte prefix로 보존하고 세 번째 행만 추가합니다.

원본 경로: `/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/photo-editing-effects-20261001/qualification/arm-c-tonal-skin/v2/generated-original.png`

원본 SHA256: `5b94e4215dfc4c31dbe0d270ef86d612a50b32ddee51b7920c7e4b3365756624`; 1237×1272. 반환된 원래 파일과 보존본이 byte-identical입니다. 검사 crop은 정수 좌표의 원래 해상도 잘라보기만 수행했으며 색·톤·필터·크기 변경은 없습니다. 모든 결과는 같은 저장 이미지에서 판정했습니다.

source dictionary SHA `70379562ac6e618750d724a51659049174aec2e4cb95f3226e3bf6a1036f4ed4`; registry SHA `103e10149bcda2a0ba846b215c309d07ed3f0102d49d5b0a25741f5483e6d45c`; pack object SHA `1f7451bea06fe97ade0754bcdeff0e9d8c05a4f50feb26090efd18a620c331a6`; core canonical SHA `a7aff6a3462a015b8a5c985d13dbdc48160493ef9a67b395ea477a0e8fcbff51`; intent-lock SHA `7a26d10876c1f9502c89381a46295016eb8a2787739e3e1daad485a50eb6446a`; effective visual contract SHA `371aaea627e9282c50f89fd188b26a1c590b80fe6869e38722b29bdc178fb7cd`; prompt SHA `fb024c220c4317e6fbb374d2e58693ae3ec16e9a462a6d281a4d6f7459b6538f`. 파일별 원본 SHA는 `render_input_hashes.json`과 `artifact_hashes.json`에 있습니다.

재현·검토 근거는 `pre_render_test_cases.json`, `keyword_target_ledger.json`, `keyword_target_ledger_post_render.json`, `moe_render_review.json`, `render_review_audit.json`, `native_read_only_diagnostics.json`, `reference_scope_review.json`, `image_runs.ndjson`, `run_manifest.json`, `cumulative_attempt_provenance.json`입니다. 참조는 성인 가상 인물의 가시적 얼굴·헤어에만 적용했으며 신원·생체·성향·체형이나 사용자 수용을 주장하지 않습니다.
