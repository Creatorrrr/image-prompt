# 독립 평가 B: 철도 대합실 랜턴 작업 공간의 광학 인물 사진

**세 광학 키워드는 통과했지만 전체 장면 검증은 실패입니다.** 최초 native 이미지 한 장에서 전경 보케, 같은 창문의 반사와 투과, 오른쪽 가장자리 굴절은 보입니다. 두 번째 손의 소유·연결과 리본을 수평으로 당기는 접촉은 읽히지 않아 4개 embodiment gate를 실패로 유지했습니다. `partial_is_fail`을 적용했고 추가 생성은 하지 않았습니다.

| 독립 테스트 | 판정 | 원본에서 확인한 내용 |
|---|---|---|
| foreground bokeh | PASS | 좌측과 하단의 가까운 사프란 천이 부드럽게 흐리며 중앙에 열린 공간을 만듭니다. 그 뒤 얼굴·눈·머리카락은 선명합니다. 배경 흐림만으로 대체되지 않았습니다. |
| glass reflection and transmission | PASS | 우측 창 부재와 하단 창턱, 유리 물방울이 동일 pane을 표시합니다. 실내 인물·손·작업대가 투과되고 위쪽 canopy 및 wire 반사가 겹칩니다. 중앙 표정 부위는 읽힙니다. |
| peripheral refraction | PASS | 극우측의 좁은 slice에 붉은 램프 윤곽이 두 위치로 이동·중복되고 spectrum band가 동반됩니다. 중앙 얼굴은 하나의 윤곽을 유지합니다. 무지개 조명만 나타난 결과와 구분됩니다. |
| 두 손의 리본 비교·수평 pull | FAIL | 보이는 한 손은 리본을 단추 옆에 집지만 느슨한 리본은 수직으로 늘어집니다. 다른 손과 팔 연결, 수평으로 당기는 접촉은 가려져 판정할 수 없습니다. |

`pixel_review_audit.json`은 17개 정확한 gate를 검증했고 `schema_failures=[]`입니다. 시각 계약 12개는 모두 PASS, embodiment는 지지·균형 1개 PASS와 소유·joint chain·contact·projection 4개 FAIL입니다. 감사는 제출된 픽셀 관찰 기록과 해시를 검증하며, 픽셀을 자동 분석한 결과로 주장하지 않습니다. 사용자 직접 수용은 pending입니다.

## 독립 컨셉과 입력 경계

난수 seed는 **1292956637129113158**이고 추첨 목록과 순서는 `random_selection.json`에 저장했습니다. 추첨된 장면은 옛 철도 대합실의 랜턴 작업 공간, 코트 단추와 실크 리본의 색 비교, 번호표 금속 상자, 비 오는 아침 창문광과 붉은 표시등, 렌즈 가까이 사프란 천, 흰 셔츠와 남색 앞치마입니다. 이 조합을 하나의 사진으로 독립 작성했습니다.

pre-core에는 실제 요청 envelope, 원 대화 키워드 데이터, 일반 지식, 두 SKILL.md, 지정 neutral catalog, 참조 사진만 사용했습니다. 다른 arm의 이미지·프롬프트·팩·테스트는 읽지 않았습니다. 10개 neutral feature selection 검증이 경고 없이 통과했고 296단어 baseline을 candidate 조회 전에 동결했습니다. 최종 조합은 433단어로 hard evidence와 source baseline을 유지하며 증거 조정 권고 상한 434단어 안에 들어갑니다. 기본 360단어 권고와 pack의 uncovered-intent bookkeeping에 대한 비차단 경고는 남아 있습니다.

참조 사진은 보이는 짧은 어두운 bob, 나뉜 가는 앞머리, 부드러운 볼 윤곽의 외형 안내로만 사용했습니다. 신원·실제 나이·민족·성격·직업은 추론하거나 검증하지 않았습니다. 인물·의상·활동은 명백한 성인 가상 인물 장면으로 창작했습니다.

## 새 후보의 실제 노출과 채택

`pack_id=51366a22b095f223`는 정상 v6 `selection_mode=semantic`로 한 번 생성했습니다. 실제 pack에 `pc_pc19`, `pc_pc21`, `pc_pc24` visual concepts가 노출되어 이 세 개의 전체 opt-in 계약을 채택했습니다. ordinary composition 후보 `pc_pc19_component_3`와 `pc_pc21_component_2`도 실제 노출되었고, 원본 core 의미를 유지하는 새 관계 증거를 써서 채택했습니다. 다른 hand·mirror·seating·architectural-symmetry 제안과 창 맞은편 facade를 필요로 하는 optional 후보는 거절했습니다. 노출되지 않은 후보는 강제로 선택하지 않았습니다.

노출 목록, source pointers, 채택 ID, 최종 literal evidence는 `pc_candidate_exposure_adoption.json`에 분리 기록했습니다. pre-core typed assertions와 최종 opt-in 계약은 후보의 검색 점수나 이름으로 대체하지 않았습니다.

## 호출과 저장 기록

- 도구: native `image_gen`, 실제 호출 1회, API/CLI fallback 0회, retry 0회.
- 저장 원본: `/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/qualification/arm_b/render_attempt_01.png`
- 원본 크기: 1237×1272; SHA-256: `440a78544172611c65f0b3975cd04c145d22117b08c80d04b9a5dab98b45ea16`
- 반환된 native 원본과 workspace copy의 바이트가 동일합니다. thumbnail 및 손·edge detail은 검토용 파생물이고 원본을 교체하지 않았습니다.
- 참조 SHA-256: `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`
- 독립 manifest: `photo-independent-run-manifest/v2`; ledger run: `e4f6279c33979f59`.
- ledger의 `status=success`는 native 도구 호출 성공이며 `failure_reason`은 픽셀 qualification 실패를 명시합니다. 전체 평가 상태는 `arm_summary.json`의 `overall_status=fail`입니다.

`composed_audit.json`과 `render_request_audit.json`은 PASS입니다. 실제 도구에 넘긴 positive+negative 및 참조 경로는 `native_tool_inputs.json`에 exact bytes로 보존했습니다. 이 initial run은 lineage repair target이 없으므로 `audit_image_render_review.py`를 임의의 초기 픽셀 감사로 사용하지 않았습니다. 선정 visual+embodiment gate의 정상 `audit_moe_render_review.py`를 사용했고 범위는 `review_audit_scope.json`에 명시했습니다.

결과를 대표 성공 이미지로 승격하지 않으며, 첫 결과와 모든 근거를 보존합니다.
