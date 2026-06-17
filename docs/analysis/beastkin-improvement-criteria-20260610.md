# 수인 역할 조합 프롬프트 개선 — 성능 평가 기준 (2026-06-10)

## 평가 대상

11개 역할×수인 컨셉(메이드/간호사/경찰/광부/사복 여친/공주/바니걸/고스로리/오피스룩/산타복/운동복)을
시맨틱 모드로 생성한 배치. 생성 조건: `--selection-mode semantic`, 시드 1201~1211 고정,
배치 종 회피 체인(`--exclude-species` 누적) 사용. 자동 채점: `eval_tmp/beastkin_batch_eval.py`.

## 기준 (모두 충족 시 종료)

| # | 기준 | 목표 | 측정 방법 |
|---|---|---|---|
| 1 | 종-표정 정합 | **100%** | species family → 허용 gaze id 매핑표와 choices.expression 대조 |
| 2 | 종-텍스처 정합 | **100%** | family → 허용 texture id 매핑표와 choices.texture 대조 (깃털 종에 fur 0건 등) |
| 3 | 종-소품 정합 | **100%** | 비포유류(조류·파충류·뿔 계열)에 `pointed_ear_tail_set_prop` 0건 |
| 4 | 장면 모순 | **0건** | (a) 선언된 hard slot 규칙 사후 위반 0, (b) interior location + [비 의존 action 또는 거리 조명] 0건 |
| 5 | 동음이의 오매칭 | **0건** | 수인 배치에서 surveillance-tail 계열 world 선택 0회 |
| 6a | 종 다양성 | 동일 family ≤ 2/11 | 종 회피 체인 사용 시 family 카운트 |
| 6b | transition_stage 다양성 | distinct ≥ 3/11 | choices 카운트 |
| 6c | expression 다양성 | distinct ≥ 3/11 | choices 카운트 |
| 6d | ear-tail prop 비율 | ≤ 5/11 | 포유류 종에만 허용되므로 종 분포에 종속 |
| 7 | 회귀 무결성 | 전부 통과 | pytest 전체, validator, 골든(의도 변경 반영 후), `--contradiction-check` 0, `--check-index` ok |
| 8 | 머신 게이트 | 11/11 pass | `--explain-concept` gate_results에 fail 0 |

## 종 → 슬롯 정합 매핑표 (기준 1~3의 정답표)

| family | 허용 gaze | 허용 texture | 허용 prop |
|---|---|---|---|
| feline, reptile, snake | slit_pupil_intense_gaze | fur_patch_skin_blend / scale_skin_gradient_patch | pointed_ear_tail_set_prop(포유류만) / 없음 |
| lagomorph, ungulate, equine, caprine, rodent, suid, amphibian, cephalopod | side_set_prey_alert_gaze | fur_patch / velvet_antler / damp_fur | pointed_ear_tail(포유류) / 없음(뿔·수생 계열) |
| avian, insect_arthropod | round_unblinking_bird_gaze | feather_skin_follicle_blend | single_feather_trace_prop / 없음 |
| canid, bear, mustelid, aquatic_mammal, bat, fish_shark_koi | round_pupil_quiet_predator_focus | fur_patch / damp_fur | pointed_ear_tail_set_prop / 없음 |

## 반복 절차

1. 개선 반영(데이터 우선, 필요 시 코드) → validator + 단위테스트 + 골든 갱신
2. 11종 재생성(시드 고정, 종 회피 체인)
3. `beastkin_batch_eval.py` 채점 → 미달 기준 식별
4. 미달 원인 분석 → 다음 라운드 개선 계획 → 1로
5. 기준 1~8 전부 충족 시 종료, 최종 보고

## 추가 기준 (r6, D9 반영)

| # | 기준 | 목표 | 측정 방법 |
|---|---|---|---|
| 9 | 코스프레 프레이밍 금지 | 0건 | subject=adult_cosplay_performer 선택 0, capture_context에 cosplay 계열 0 |

D9 반영 내용: 사용자 확인 결과 코스프레 라우팅은 안전 목적이 아니었음(안전은 별도 단계).
간호사/경찰/바니걸 역할 recipe를 직업·무대 정체성으로 교체:
- 간호사: subject=nurse_role, preset=clinical_handover_vitals (임상 인계 다큐)
- 경찰: subject=police_officer_role, preset=police_traffic_control_documentary (교통 통제 다큐)
- 바니걸: subject=adult_stage_dancer, preset=magician_assistant_prop_check (무대 어시스턴트, bunny_stagecraft_family)
- intent_axis/additional의 "cosplay" 문구를 duty/stage 문구로 교체. costume_style id(covered uniform)는 유지.
