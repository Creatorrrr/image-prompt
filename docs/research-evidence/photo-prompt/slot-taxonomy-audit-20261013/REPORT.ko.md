# 전체 태그 보강에 앞선 슬롯 체계 감사

현재 슬롯 체계는 먼저 정비할 필요가 있다. 112개가 모두 잘못된 것은 아니지만, 의미 명세가 부족하고 서로 다른 분류 축이 섞여 있어 지금 상태로 전체 후보에 태그를 늘리면 혼용이 확대될 가능성이 있다. 특히 역할 판정이 소유자·속성·관계 대신 넓은 차원 일치에 의존하는 문제까지 함께 고쳐야 한다.

2026-10-13, `main`의 `39e1b3a8a889038b6aaa20f94e7eda01b212b79b`에서 조사했다. authored corpus hash는 `dc534f949116f8b09d5c36a4f0318e1a5a2229e7386c014f58fbbdfc870aeb6c`다. 이번에는 조사 증빙과 계획만 작성했다. 운영 catalog·후보·연결·인덱스·실행 generation을 변경하지 않았고 임베딩 호출·커밋·푸시를 수행하지 않았다.

## 조사 범위와 판정의 성격

- catalog 112개와 연결 12,020개의 명세·차원·조건·효과 분포를 전수 집계했다. 코드의 슬롯 질의·활성 슬롯 선택·역할 제안·조건·제시 예산과 정확한 슬롯 문자열 사용처를 확인했다.
- 112개 모두에서 대표 후보를 읽었다. 연결이 12개 이하인 슬롯은 전부, 나머지는 원본 순서의 처음·중간·끝과 ID hash 기준 3개를 선택했다. 중복 선택을 제거한 **709개 고유 후보**의 영어 의미 카드가 감사 근거다. 쟁점 사례는 효과·관계·조건과 다른 슬롯의 관련 후보를 추가 대조했다. `medium`/`genre`와 `distance_narrative` 등은 전체 연결 본문도 확인했다.
- [슬롯별 판정 대장](REVIEWS.tsv)은 112/112개를 포함한다. 각 행의 의미·경계·목표 이름은 **정비 제안**이며 아직 운영 명세가 아니다. [inventory](INVENTORY.json)는 각 행을 실제 후보 ID와 코드 위치에 연결한다.
- 표본은 슬롯 범위 감사를 위한 대표 선택이다. 통계적인 정확도 추정도, 전체 18,250개 후보의 의미 판정도 아니다. 새 질의를 실행한 검색 정확도나 이미지 픽셀 품질을 측정하지 않았다.

## 객관적으로 확인한 명세·코드 한계

| 항목 | 확인 결과 | 의미 |
|---|---:|---|
| 의미 설명이 이름의 띄어쓰기와 동일 | 112 / 112 | 포함·제외·소유자·이웃 역할 경계가 catalog에 없음 |
| `dimensions`가 비어 있는 슬롯 | 10 | 넓은 효과 차원으로조차 역할 일치를 판정할 수 없음 |
| 위 10개에 연결된 binding | 1,515 | 원래 슬롯으로 제안해도 현재 fit 판정은 `review_required` |
| 차원이 있지만 연결 효과와 교집합이 없는 binding | 182 | 역할 명세와 실제 효과 경로를 대조해야 함; 자동으로 오태그 182건이라는 뜻은 아님 |
| 슬롯용 core 필드 투영을 지정하지 않은 슬롯 | 65 | 전체 core 검색 문맥은 유지되지만, 추가 slot focus는 짧은 역할명만 사용 |
| `appearance`를 공유하는 슬롯 | 25 | 동일 차원이라는 사실만으로 머리·피부·의복 역할을 구별할 수 없음 |

빈 차원 10개는 `capture_context`, `prop`, `motion`, `prop_direction`, `gaze_target`, `aftermath_trace`, `situation_context`, `atmosphere`, `material`, `capture_mode`다. 적절한 차원을 의미에 맞게 정하거나, 차원이 아닌 대상·속성·관계로 fit을 판단하는 명시적 계약이 필요하다. 목록을 채우기 위해 임의의 차원을 넣어서는 안 된다.

실제 [역할 판정 함수 실험](ROLE-FIT-PROBES.json)도 수행했다.

| 실제 후보 | 요청 역할 | 현재 판정 | 문제 |
|---|---|---|---|
| 별도 흰 커프가 같은 소매 옆에서 손목을 감쌈 | `hair_color` | `eligible` | `appearance`만 공유할 뿐 모발 색을 표현하지 않음 |
| 나뭇잎 사이의 얼룩 빛무늬 | `light_direction` | `eligible` | `lighting` 공유가 입사 방향의 근거는 아님 |
| 양안테나 테레민 소품 | 원래 `prop` | `review_required` | 대상 슬롯의 차원이 비어 있음 |
| 유리 파편과 불투명 잔해의 표면 대비 | 원래 `material` | `review_required` | 후보 효과는 `material`인데 대상 슬롯 차원은 비어 있음 |

이 실험은 `photo_role_proposals.propose`를 직접 호출한 결과다. caller가 전달하는 source binding 자격을 가정한 **fit 함수의 한계**를 확인했으며, 실제 end-to-end 검색이 이 오역할 후보를 반환했다는 증거는 아니다. 이후 조건·잠금 검사와 선택 검토가 존재한다. `eligible`을 의미 적합성 검증 완료로 간주하는 것은 현재 코드로 뒷받침되지 않는다.

관련 운영 코드: `photo_slot_queries.py:15`(명세), `prompt_generator.py:1584`(focus), `photo_role_proposals.py:6`(fit), `photo_slot_retrieval.py:14`(활성 슬롯)와 같은 파일의 제시 예산 처리. catalog schema는 현재 `id/description/dimensions/applicability`만 허용하므로 새 명세를 코드가 읽게 하려면 validator·reader·질의 계약도 함께 바꿔야 한다.

## 의미가 섞이거나 중복된 주요 그룹

| 현재 슬롯·그룹 | 실제 후보에서 확인한 문제 | 권고 |
|---|---|---|
| `medium` / `genre` / `capture_context` | medium에 여행·다큐·패션 장르, 셀피·CCTV 방식, 플랫폼 용도, 물리 사진 지지체가 함께 있음. genre에도 여행·패션·셀피가 있음 | medium은 물리 매체·지지체 역할로 정제하고 장르·촬영 구성·용도를 각각 재배치 |
| `material` / `surface_material` | material의 유일한 연결은 유리/불투명 잔해의 표면 광학 대비로 surface_material 역할과 겹침 | material을 surface_material로 통합하는 안 우선 검토 |
| `texture` / `grain_profile` / `lens_artifact` / `ambient_particle` | texture에 종이·나무 조직뿐 아니라 JPEG 압축, 공중 먼지, 렌즈 먼지가 있음 | 물리 표면, 이미지 면, 광학 경로, 공기 중 물질의 **소유 공간**으로 분리 |
| `mood` / `atmosphere` / `weather` / `ambient_particle` | mood는 정서, atmosphere는 안개·연무와 바람 없는 정지 요소. ambient_particle에는 입자 없는 원거리 대비 감쇠도 있음 | 정서와 물리 대기 상태를 명확히 구별. atmosphere를 atmospheric_medium으로 개명하는 안; 정지 요소는 motion 계열로 검토 |
| `subject_framing` / `body_framing` / `partner_framing` / `shot_scale` | 일부는 대상별 같은 프레임 포함 범위를 나누고, shot_scale은 촬영 범위 규모를 지정 | body/partner framing은 소유자·대상 목록을 가진 subject_framing으로 통합 검토. shot_scale은 독립 축으로 유지 |
| `proxemics` / `distance_narrative` / `viewer_position` | distance_narrative의 14개는 한 자리 간격·카운터·문턱·등 돌림 등 물리 배치와 그 해석 | 물리 배치는 proxemics 및 배치 역할, 해석은 관계 맥락으로 보존. distance_narrative의 별도 검색 슬롯은 통합 검토 |
| `quality` | 피부 마감, VHS 노이즈, 색 번짐, solarization, 대기 선명도, 연출 자연스러움이 같은 슬롯 | quality 총칭 슬롯을 폐지하고 구체 역할 또는 평가·연출 계약으로 재분류하는 안 |
| `frame_anchor_medium` | 전경 겹침, 화면 속 다른 장면, 단일 사진/레이아웃 금지, 전신 크롭, bokeh, grain이 혼재 | 현재 슬롯을 폐지하고 실제 역할과 제약 계약으로 분해하는 안 |
| `world` / `aesthetic_trend` / `narrative_core` / `situation_context` | world에 dystopian tension, aesthetic_trend에 수사·범죄 시스템·설화 전승, narrative_core에 세계 체계와 짧은 제목이 있음 | 지속적 세계 규칙, 표현 관습, 중심 사건, 국소 상황의 경계를 명세화하고 후보 재분류 |
| `light_intensity` / `light_type` / 영상 표현 | intensity에 bloom·하이라이트 클리핑·노출 보존, type에 long-exposure light drag | 광원 수준/종류와 이미지 면의 톤·흔적을 구별 |
| `gaze_target` / `gaze_engagement` / `expression` | engagement에 목표·위 방향·눈 감음이 섞이고 action에도 시선 접촉이 있음 | 목표, 참여자와의 시선 관계, 눈꺼풀/얼굴 반응을 구별 |
| `skin_finish` / `skin_condition` / `body_marking` / `silhouette_proportion` | 피부 마감에 체모·눈밑 형태·홍조, 피부 상태에 주근깨, 실루엣에 레깅스 길이 | 광학 마감·현재 상태·표식·몸 형상·의복 형태를 소유자와 속성별로 재분류 |

통합은 이름만 바꾸는 작업이 아니다. 대상 후보의 ID·본문·효과·주체/성인/부위 조건과 묶음 참조를 보존하면서 **각 기존 연결을 새 역할로 판정하는 작업**이다. 예를 들어 partner framing을 합쳐도 두 참여자 조건을 없애지 않는다. 진정한 여러 역할은 같은 canonical 후보에 여러 연결로 유지한다.

## 특정 주제에서 만든 이름과 관측할 수 없는 맥락

`duty_prop_state`의 11개는 무전기 사용, 정리된 패키지, 체크리스트, 고정/해제된 도구 등이다. 물건 상태를 업무로 한정할 필요가 약하므로 `prop_state`로 일반화하고 업무 맥락은 조건에 남기는 안이 적합하다. `transition_stage`는 종 변신 외에 종이 선이 입체로 이어짐·재료 경계·픽셀 소멸도 포함하므로 `transformation_stage`로 범위를 명확히 할 수 있다. `emotional_contradiction`에는 권위/주도권·계급/역할 대비도 있어 `character_contrast`가 더 정확한 이름이다.

`caption_context`의 연결 5개는 모두 성인/외모 평가 SNS 문구 계열이며 이미지 안의 글자와 같은 개념이 아니다. 일반적인 캡션·게시 해석 맥락으로 정리할지, 게시 단계 계약으로 옮길지 먼저 정해야 한다. `adult_context` 3개는 명시된 성인 표현 맥락이다. 연령 조건·성적 표현·게시 용도를 한 이름으로 혼용하지 않도록 분리해야 한다. `fetish_styling` 1개의 물리 요소는 일반 소재·의복과도 겹치므로 **페티시 맥락을 실제로 선택한 경우**의 관련 역할과 물리 역할을 나눠야 한다.

`person_origin` 25개는 국가 출신이고 얼굴의 관찰 속성이 아니다. 명시된 배경 맥락으로만 다룬다. `intent_state`에도 순간 단계와 정체성 추론 금지 규칙이 섞여 있다. 개인의 마음·출신·동의를 이미지 외관에서 자동 판정하는 역할로 바꾸어서는 안 된다.

후보 수가 적다는 이유만으로 슬롯을 없애지는 않는다. eyebrow/eyeliner/lip finish, camera height, hand pose처럼 대상과 독립 속성이 명확한 역할은 세부적이어도 유용하다. 현재 연결 수는 공통 풀 전체의 해당 의미 후보 수가 아니다. 또한 `safety_profile`과 `costume_absorption_guard`는 현재 112개 catalog에 없으므로 빈 검색 슬롯을 채우는 대상에 포함하지 않는다.

## 112개 전체에 대한 제안 분포

| 1차 제안 | 슬롯 수 | 해석 |
|---|---:|---|
| 역할 유지 | 45 | 독립 의미 축은 유효. 포함·제외·소유자 명세는 새로 필요 |
| 범위 재정의·후보 재배치 | 44 | 현재 역할을 정제하고 혼용된 연결을 재검토 |
| 일반화·개명 | 12 | 주제에 치우친 이름이나 실제 후보보다 좁은 이름 수정 |
| 맥락 역할로 명시 | 5 | 시각 사실·연령 조건·정책과 구별 |
| 통합·폐지 검토 | 6 | material, body_framing, partner_framing, distance_narrative, quality, frame_anchor_medium |

이 수치는 슬롯 설계의 1차 판단이다. 자동 검증에서 실패한 슬롯 수나 오태그율이 아니다. 6개를 제외하면 106개라는 계산만으로 최종 슬롯 수를 확정하지 않는다. 여러 축으로 갈라야 할 역할이나 전수 검토에서 드러나는 누락 역할은 근거를 갖고 추가·통합한다.

## 목표 구조와 수정 순서

공통 후보 풀과 다대다 관계를 유지하면서 슬롯은 **대상·속성·관계를 갖는 역할 태그**로 정비한다. 각 명세에 정의, 대상/소유 범위, 직접/맥락 역할, 적용 전제, 허용되는 효과 경로, 포함·제외 예시, 이웃 역할 경계를 둔다. 물리 속성·해석 맥락·정책/제약은 구분하되 후보 본문을 각각 복사하지 않는다.

lighting/makeup 같은 넓은 역할은 완결된 복합 구성에 의미가 있을 때 유지한다. 탐색 편의를 위한 family가 필요하면 표시·검토용 metadata로 두고 자동 상위 태그, 별도 검색 투표, 추가 제시 예산을 만들지 않는다. 슬롯별 독립 BM25F·임베딩 검색의 대상은 계속 공통 positive 풀 전체다.

기존 계획은 다음 순서로 수정했다.

1. **0단계: 이번 감사에 근거한 슬롯 체계·목표 의미 명세 확정.** 이번에 감사/제안은 작성했으며 운영 전환은 수행하지 않았다.
2. 1단계: 전수 원본·참조·검토 대장 고정.
3. 2단계: intrinsic/역할 조건 분리와 새 의미 계약·역할 판정 코드 구현. 넓은 차원 공유를 의미 적합성으로 취급하지 않음.
4. 3단계: 기존 12,020개 연결과 정책·제시·query·binding 참조를 새 슬롯 체계로 이관하고 검증.
5. 4~8단계: 파일럿, 전체 후보 심사, 확정 연결 적용, 검색·shard·실행 검증, 최종 평가.

새 슬롯 ID와 core의 동명 필드·효과 경로는 같은 것이 아니다. 특히 `camera.capture_mode` 같은 중립 authoring 필드를 슬롯 개명과 함께 단순 문자열 치환하면 안 된다. 옛 슬롯을 운영 alias/fallback으로 남기지 않고, source mapping과 역사 증빙에만 보존한다. 명세 변경으로 질의가 달라지면 해당 질의 context/hash/실제 임베딩을 새로 생성하고 source 변경 단계마다 인덱스·runtime publication을 끝내야 한다.

## 증빙

- [원본·코드 hash 및 조사 범위](SOURCE-VERIFICATION.json)
- [catalog 원본 snapshot](CATALOG-SNAPSHOT.json), [112개 inventory](INVENTORY.json)
- [709개 원문 후보·연결 카드](CANDIDATE-CARDS.jsonl), [112개 제안 판정](REVIEWS.tsv)
- [역할 판정 함수 실험](ROLE-FIT-PROBES.json), [문서·증빙 검증](AUDIT-VERIFICATION.json)
- [수정된 전체 태그 보강 계획](../../../analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md)

재수집: `.venv/bin/python docs/research-evidence/photo-prompt/slot-taxonomy-audit-20261013/collect_evidence.py`.
검증: `.venv/bin/python docs/research-evidence/photo-prompt/slot-taxonomy-audit-20261013/verify_audit.py`.
