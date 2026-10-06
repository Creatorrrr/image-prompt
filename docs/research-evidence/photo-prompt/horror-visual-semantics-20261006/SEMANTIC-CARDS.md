# 호러 시각 의미 카드
2026-10-06 KST. 250개 입력 항목 전부를 유지한 연구용 카드다. 구체적인 연출은 독자 설계이며 원 출처의 권고나 고정 정의가 아니다. 후보·profile·영상/음향 계획의 실행과 이미지 성공은 아직 검증하지 않았다.

## 절 1

### hvr_terror_anticipation — 테러 — Terror
직접 드러나기 전의 위협을 예상하게 하는 구도 선택이다.
- 반영 구분: visual; 원본 슬롯 제안: composition.
- 관찰 구성: a closed threshold conceals the possible threat / a visible adult attends to that threshold / the withheld region stays spatially identifiable.
- 관계: a closed threshold conceals the possible threat → jointly_visible_in_same_event → a visible adult attends to that threshold and the withheld region stays spatially identifiable.
- 혼동 경계: an explicit creature reveal; ordinary closed door without attention relation.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_horror_confrontation — 호러 — Horror
장르명 호러와 래드클리프의 직접 대면 개념을 구분한다.
- 반영 구분: context; 원본 슬롯 제안: genre.
- 관찰 구성: a confronting threat occupies the visible scene / the observer and threat share one encounter.
- 관계: a confronting threat occupies the visible scene → jointly_visible_in_same_event → the observer and threat share one encounter.
- 혼동 경계: horror always means gore; terror and horror as universal exclusive bins.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_dread_held_exit — 드레드 — Dread
지속적인 불안의 한 순간은 접근 위험과 제한된 출구를 함께 배치할 수 있다.
- 반영 구분: visual; 원본 슬롯 제안: composition.
- 관찰 구성: an adult holds position between a visible exit and an unresolved approach / the approach remains partly unreadable.
- 관계: an adult holds position between a visible exit and an unresolved approach → jointly_visible_in_same_event → the approach remains partly unreadable.
- 혼동 경계: dark grading alone; proof of prolonged fear from a still.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_suspense_information_gap — 서스펜스 — Suspense
결과 지연은 아직 확인되지 않은 영역과 관찰자의 주의를 연결한다.
- 반영 구분: visual; 원본 슬롯 제안: composition.
- 관찰 구성: a readable foreground reaction points toward a concealed doorway / the doorway withholds its occupant.
- 관계: a readable foreground reaction points toward a concealed doorway → jointly_visible_in_same_event → the doorway withholds its occupant.
- 혼동 경계: blur everywhere; a still proving time spent waiting.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01), [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_eerie_expected_absence — 이리 — Eerie
있을 것으로 기대되는 활동이 부재한 공간의 어긋남을 설계한다.
- 반영 구분: visual; 원본 슬롯 제안: situation_context.
- 관찰 구성: an operational service area retains ready equipment / its expected users are absent / one fresh use trace contradicts the vacancy.
- 관계: an operational service area retains ready equipment → jointly_visible_in_same_event → its expected users are absent and one fresh use trace contradicts the vacancy.
- 혼동 경계: all empty rooms are eerie; abandoned ruin alone.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_uncanny_familiar_discrepancy — 언캐니 — Uncanny
낯익은 기준을 유지한 상태에서 국소적인 불일치가 드러난다.
- 반영 구분: visual; 원본 슬롯 제안: reflection_logic.
- 관찰 구성: an ordinary adult and aligned mirror share matching clothing / the reflected hand takes a different pose / other reflected geometry remains coherent.
- 관계: an ordinary adult and aligned mirror share matching clothing → jointly_visible_in_same_event → the reflected hand takes a different pose and other reflected geometry remains coherent.
- 혼동 경계: all uncanny means uncanny valley; random bad anatomy.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01), [S02](SOURCES.md#s02); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_uncanny_valley_local_mismatch — 불쾌한 골짜기 — Uncanny valley
인간과 유사한 형상에서 작은 채널 불일치를 다룬다는 가설이다.
- 반영 구분: reuse; 원본 슬롯 제안: appearance_type.
- 관찰 구성: a broadly coherent humanlike face remains readable / one bounded skin or eye channel differs from the otherwise matched face.
- 관계: a broadly coherent humanlike face remains readable → jointly_visible_in_same_event → one bounded skin or eye channel differs from the otherwise matched face.
- 혼동 경계: any monster face; universal revulsion claim; caricature.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S02](SOURCES.md#s02); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_grotesque_hybrid_joint — 그로테스크 — Grotesque
기괴함은 서로 다른 형태가 같은 몸에서 어떻게 접합되는지에 있다.
- 반영 구분: visual; 원본 슬롯 제안: anatomical_connection.
- 관찰 구성: one recognizable humanlike torso meets a nonhuman limb / the junction connects both structures continuously.
- 관계: one recognizable humanlike torso meets a nonhuman limb → jointly_visible_in_same_event → the junction connects both structures continuously.
- 혼동 경계: separate creature collage; amusing exaggeration alone.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S05](SOURCES.md#s05); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_abject_boundary_failure — 애브젝트 — Abject / Abjection
안과 밖 또는 청결과 오염의 경계를 침범하는 표현을 분해한다.
- 반영 구분: visual; 원본 슬롯 제안: surface_material.
- 관찰 구성: a clean washable surface borders organic residue / residue visibly crosses that boundary.
- 관계: a clean washable surface borders organic residue → jointly_visible_in_same_event → residue visibly crosses that boundary.
- 혼동 경계: abject means ugly; clinical material itself proves disgust.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S20](SOURCES.md#s20); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_macabre_memorial_presence — 마카브르 — Macabre
죽음을 의례와 일상 배치의 중심에 놓는 선택이다.
- 반영 구분: visual; 원본 슬롯 제안: prop.
- 관찰 구성: a readable memorial arrangement contains bone-shaped objects / living-use objects remain adjacent to it.
- 관계: a readable memorial arrangement contains bone-shaped objects → jointly_visible_in_same_event → living-use objects remain adjacent to it.
- 혼동 경계: any black outfit; every skull is a literal corpse.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_ominous_local_sign — 불길함 — Ominous
아직 발생하지 않은 사건의 징조로 국소 변화 하나를 배치한다.
- 반영 구분: visual; 원본 슬롯 제안: aftermath_trace.
- 관찰 구성: one fresh dark hand-shaped trace interrupts an otherwise orderly wall / a nearby adult notices that specific mark.
- 관계: one fresh dark hand-shaped trace interrupts an otherwise orderly wall → jointly_visible_in_same_event → a nearby adult notices that specific mark.
- 혼동 경계: global dirt; a mark proves a future event.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_sublime_scale_limit — 숭고 — Sublime
과도한 규모와 위력이 인간의 공간 기준을 넘어서는 표현이다.
- 반영 구분: visual; 원본 슬롯 제안: scale_relation.
- 관찰 구성: a small adult provides a readable scale reference / a vast enclosing form extends beyond the frame / the form has coherent near-to-far depth.
- 관계: a small adult provides a readable scale reference → jointly_visible_in_same_event → a vast enclosing form extends beyond the frame and the form has coherent near-to-far depth.
- 혼동 경계: big monster alone; wide lens distortion as size evidence.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01), [S04](SOURCES.md#s04); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_claustrophobic_body_clearance — 폐쇄감 — Claustrophobic
폐쇄감은 실제 몸과 출구의 여유 공간을 비교한다.
- 반영 구분: visual; 원본 슬롯 제안: space_condition.
- 관찰 구성: walls and low ceiling closely bound an adult body / one narrow exit remains visible / body clearance is legible at the bottleneck.
- 관계: walls and low ceiling closely bound an adult body → jointly_visible_in_same_event → one narrow exit remains visible and body clearance is legible at the bottleneck.
- 혼동 경계: tight face crop only; impossibly compressed anatomy.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_disorientation_route_conflict — 방향감각 상실 — Disorientation
위치와 거리 기준이 서로 충돌하는 장면이다.
- 반영 구분: visual; 원본 슬롯 제안: surreal_physics_detail.
- 관찰 구성: two readable route cues disagree at one junction / the same junction geometry remains otherwise coherent.
- 관계: two readable route cues disagree at one junction → jointly_visible_in_same_event → the same junction geometry remains otherwise coherent.
- 혼동 경계: busy hallway; illegible labels; ordinary different destinations.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

## 절 2a

### hvr_gothic_past_present — 고딕 호러 — Gothic horror
고딕은 옛 건물 외형뿐 아니라 현재를 침범하는 과거와 권력 관계를 포함한다.
- 반영 구분: visual; 원본 슬롯 제안: concept_tension.
- 관찰 구성: a functioning contemporary room contains a sealed older architectural threshold / fresh occupation stops at that threshold.
- 관계: a functioning contemporary room contains a sealed older architectural threshold → jointly_visible_in_same_event → fresh occupation stops at that threshold.
- 혼동 경계: black lace means gothic horror; pointed arches prove haunting.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_folk_horror_collective_boundary — 포크 호러 — Folk horror
풍경의 고립과 공동체 질서가 방문자의 이동을 제한하는 구성이다.
- 반영 구분: visual; 원본 슬롯 제안: relational_action.
- 관찰 구성: adult residents form an inward-facing boundary / one adult visitor stands outside their shared arrangement / the landscape limits alternative routes.
- 관계: adult residents → limits_route_of → adult visitor; landscape → isolates_alternative_routes_of → visitor.
- 혼동 경계: countryside alone; all folk ritual is evil.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S03](SOURCES.md#s03); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_cosmic_incompatible_scale — 코즈믹 호러 — Cosmic horror
인간이 의지하던 자연 규칙과 위치 기준이 무너지는 공포다.
- 반영 구분: visual; 원본 슬롯 제안: surreal_physics_detail.
- 관찰 구성: one tiny observer anchors scale / the sky pattern and its water reflection disagree / ordinary shoreline geometry remains consistent.
- 관계: small observer → provides_scale_for → vast environment; water reflection → pattern_differs_from → sky pattern.
- 혼동 경계: tentacles as sole cosmic definition; decorative starry sky.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S04](SOURCES.md#s04); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_supernatural_coherent_breach — 초자연 호러 — Supernatural horror
장면의 정상 법칙 하나와 그 국소 위반을 함께 보여준다.
- 반영 구분: visual; 원본 슬롯 제안: surreal_physics_detail.
- 관찰 구성: a solid closed door retains continuous construction / one identifiable apparition occupies both sides of that threshold.
- 관계: a solid closed door retains continuous construction → jointly_visible_in_same_event → one identifiable apparition occupies both sides of that threshold.
- 혼동 경계: whole-frame blur; invisible cause asserted from debris alone.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_psychological_record_conflict — 심리 호러 — Psychological horror
지각 또는 기록과 직접 보이는 사건의 불일치를 표현하되 원인을 단정하지 않는다.
- 반영 구분: visual; 원본 슬롯 제안: reflection_logic.
- 관찰 구성: a present adult is visible beside a live monitor / the monitor depicts a different local gesture / shared room landmarks establish comparison.
- 관계: a present adult is visible beside a live monitor → jointly_visible_in_same_event → the monitor depicts a different local gesture and shared room landmarks establish comparison.
- 혼동 경계: mental illness equals danger; a monitor proves diagnosis.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01), [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_occult_directed_ritual — 오컬트 호러 — Occult horror
의식의 주체와 대상 및 경계를 연결한다.
- 반영 구분: visual; 원본 슬롯 제안: relational_action.
- 관찰 구성: an adult operator directs a gesture toward a bounded ritual center / objects mark that exact boundary.
- 관계: an adult operator directs a gesture toward a bounded ritual center → jointly_visible_in_same_event → objects mark that exact boundary.
- 혼동 경계: random candles; every real religious tool is occult evil.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_religious_protection_breach — 종교 호러 — Religious horror
보호를 기대하는 종교적 경계의 훼손이라는 특정 허구 설정이다.
- 반영 구분: visual; 원본 슬롯 제안: situation_context.
- 관찰 구성: an explicitly identified protective arrangement remains recognizable / one physically breached segment admits an unrelated anomaly.
- 관계: an explicitly identified protective arrangement remains recognizable → jointly_visible_in_same_event → one physically breached segment admits an unrelated anomaly.
- 혼동 경계: religion itself as villain; invented symbols presented as historical.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01), [S26](SOURCES.md#s26); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_body_horror_uncontrolled_change — 바디 호러 — Body horror
몸의 연속성과 통제권을 잃는 변형이 핵심이며 피는 필수가 아니다.
- 반영 구분: visual; 원본 슬롯 제안: anatomical_connection.
- 관찰 구성: one body remains identifiable across normal and altered regions / the altered structure connects through a visible transition.
- 관계: one body remains identifiable across normal and altered regions → jointly_visible_in_same_event → the altered structure connects through a visible transition.
- 혼동 경계: blood alone; separate costume attachment; injury equals mutation.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S05](SOURCES.md#s05); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_creature_ecological_trace — 크리처 호러 — Creature horror
괴생명체의 일부 구조와 그 구조가 남기는 흔적을 연결한다.
- 반영 구분: visual; 원본 슬롯 제안: aftermath_trace.
- 관찰 구성: a partial nonhuman limb has a distinct contact shape / nearby tracks repeat that same shape.
- 관계: a partial nonhuman limb has a distinct contact shape → jointly_visible_in_same_event → nearby tracks repeat that same shape.
- 혼동 경계: unrelated claw marks; generic monster portrait without relation.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S05](SOURCES.md#s05); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_slasher_pursuit_corridor — 슬래셔 — Slasher
추적자와 피추적자의 이동 경로 및 차단 지점을 비교한다.
- 반영 구분: visual; 원본 슬롯 제안: relational_action.
- 관찰 구성: one adult pursuer occupies the route behind another adult / a visible obstruction closes one escape branch.
- 관계: one adult pursuer occupies the route behind another adult → jointly_visible_in_same_event → a visible obstruction closes one escape branch.
- 혼동 경계: weapon portrait; every stalker implies gore.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_splatter_visible_aftermath — 스플래터 — Splatter
직접적 신체 훼손 노출의 표현 범주를 다른 호러 형식과 구별한다.
- 반영 구분: visual; 원본 슬롯 제안: aftermath_trace.
- 관찰 구성: a fictional injury scene includes localized blood and disrupted bodily continuity / the residue remains tied to its originating body region.
- 관계: a fictional injury scene includes localized blood and disrupted bodily continuity → jointly_visible_in_same_event → the residue remains tied to its originating body region.
- 혼동 경계: splattered paint; splatter equals all body horror.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S05](SOURCES.md#s05); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_splatterpunk_context — 스플래터펑크 — Splatterpunk
반문화적 호러 문학의 계열로 보존하며 피의 양으로 자동 분류하지 않는다.
- 반영 구분: context; 원본 슬롯 제안: genre.
- 관찰 구성: a selected text or artwork supplies the declared literary context.
- 관계: a selected text or artwork supplies the declared literary context → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: all gore images are splatterpunk; a visual-only hard style.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S33](SOURCES.md#s33); SOURCE_GAP_RETAINED. 전체 seed 사실 검증은 아님.

### hvr_giallo_partial_witness — 지알로 — Giallo
양식적인 범죄 미스터리의 불완전한 목격 구도다.
- 반영 구분: visual; 원본 슬롯 제안: composition.
- 관찰 구성: a partially obscured adult witnesses a fragmentary event / one black-gloved hand enters the visible fragment / the rest of the event remains blocked.
- 관계: a partially obscured adult witnesses a fragmentary event → jointly_visible_in_same_event → one black-gloved hand enters the visible fragment and the rest of the event remains blocked.
- 혼동 경계: black glove proves genre; neon alone; yellow palette mandatory.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S07](SOURCES.md#s07); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_grand_guignol_stage_artifice — 그랑기뇰 — Grand Guignol
충격적 극장 표현과 분장 또는 무대 장치를 구별해 기록한다.
- 반영 구분: visual; 원본 슬롯 제안: capture_context.
- 관찰 구성: a theatrical stage contains visible prosthetic injury effects / stage framing separates performance from documentary event.
- 관계: a theatrical stage contains visible prosthetic injury effects → jointly_visible_in_same_event → stage framing separates performance from documentary event.
- 혼동 경계: any real injury; generic cinematic gore.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S05](SOURCES.md#s05); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

## 절 2b

### hvr_found_footage_record_boundary — 파운드 푸티지 — Found footage
발견된 기록으로 제시하는 형식의 한 프레임이다.
- 반영 구분: visual; 원본 슬롯 제안: capture_context.
- 관찰 구성: an in-world recording viewpoint limits the scene / a foreground camera edge or recording screen identifies that viewpoint.
- 관계: an in-world recording viewpoint limits the scene → jointly_visible_in_same_event → a foreground camera edge or recording screen identifies that viewpoint.
- 혼동 경계: grain alone; timestamp automatically proves authenticity.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S08](SOURCES.md#s08); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_mockumentary_evidence_display — 모큐멘터리 — Mockumentary
허구의 다큐멘터리 자료 제시 방식을 시각화한다.
- 반영 구분: visual; 원본 슬롯 제안: caption_context.
- 관찰 구성: an interview-like frame places an adult beside displayed fictional evidence / evidence remains distinct from the interview subject.
- 관계: an interview-like frame places an adult beside displayed fictional evidence → jointly_visible_in_same_event → evidence remains distinct from the interview subject.
- 혼동 경계: handheld shot alone; real documentary truth claim.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S08](SOURCES.md#s08); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_screenlife_interface_relation — 스크린라이프 — Screenlife
기기 화면 안의 정보 배치가 장면의 주요 공간이 된다.
- 반영 구분: visual; 원본 슬롯 제안: frame_anchor_medium.
- 관찰 구성: a legible device interface contains a video-call pane / a local call pane and a remote pane disagree in one visible presence.
- 관계: a legible device interface contains a video-call pane → jointly_visible_in_same_event → a local call pane and a remote pane disagree in one visible presence.
- 혼동 경계: phone anywhere in frame; exact prose legibility assumed.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_analog_broadcast_intrusion — 아날로그 호러 — Analog horror
낡은 방송 기록의 안내 형식과 국소 침입을 함께 설계한다.
- 반영 구분: visual; 원본 슬롯 제안: frame_anchor_medium.
- 관찰 구성: a fictional broadcast slate retains stable layout / one bounded signal tear interrupts the slate / a local anomalous face remains distinct from ordinary noise.
- 관계: a fictional broadcast slate retains stable layout → jointly_visible_in_same_event → one bounded signal tear interrupts the slate and a local anomalous face remains distinct from ordinary noise.
- 혼동 경계: VHS grain equals horror; copyrighted station duplication.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S32](SOURCES.md#s32); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_surreal_one_rule_violation — 초현실적 호러 — Surreal horror
꿈 같은 연결을 장면 전체의 무질서 대신 하나의 불가능한 관계로 만든다.
- 반영 구분: visual; 원본 슬롯 제안: surreal_physics_detail.
- 관찰 구성: a room retains continuous walls and flooring / one doorway opens onto an incompatible outdoor scale.
- 관계: a room retains continuous walls and flooring → jointly_visible_in_same_event → one doorway opens onto an incompatible outdoor scale.
- 혼동 경계: all geometry broken; generic dream mood.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_horror_comedy_task_contrast — 호러 코미디 — Horror comedy
위협과 평범한 업무 대응의 병치를 선택할 수 있다.
- 반영 구분: visual; 원본 슬롯 제안: situation_context.
- 관찰 구성: an adult calmly labels a clearly fictional monstrous prop / the threat object dominates the same workstation.
- 관계: an adult calmly labels a clearly fictional monstrous prop → jointly_visible_in_same_event → the threat object dominates the same workstation.
- 혼동 경계: smiling person alone; comedy effect objectively proved.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S05](SOURCES.md#s05); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_erotic_horror_attraction_threat — 에로틱 호러 — Erotic horror
성인 사이의 매혹과 위협 관계를 분석하며 단순 노출량과 구분한다.
- 반영 구분: visual; 원본 슬롯 제안: proxemics.
- 관찰 구성: two clearly adult fictional figures approach closely / an inviting gesture coexists with a visible predatory identity cue / each figure remains separately identifiable.
- 관계: two clearly adult fictional figures approach closely → jointly_visible_in_same_event → an inviting gesture coexists with a visible predatory identity cue and each figure remains separately identifiable.
- 혼동 경계: latex alone; coercion relabelled as consent; underage styling.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S06](SOURCES.md#s06); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_ero_guro_history_context — 에로구로 — Ero guro
역사적 에로 그로 넌센스와 현대 고어 태그를 하나의 외형으로 통합하지 않는다.
- 반영 구분: context; 원본 슬롯 제안: aesthetic_trend.
- 관찰 구성: a declared historical artwork context distinguishes the intended usage.
- 관계: a declared historical artwork context distinguishes the intended usage → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: all erotic gore equals the historical movement.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S06](SOURCES.md#s06); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

## 절 3

### hvr_wongwi_identity_return — 원귀 — 怨鬼
원한 있는 망자의 정체와 관련 장소를 보존하는 귀환 구조다.
- 반영 구분: reuse; 원본 슬롯 제안: subject.
- 관찰 구성: one apparition matches a former person's memorial cue / that same identity returns at a related threshold.
- 관계: one apparition matches a former person's memorial cue → jointly_visible_in_same_event → that same identity returns at a related threshold.
- 혼동 경계: generic angry stare; all ghosts are vengeful.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01), [S11](SOURCES.md#s11); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_virgin_ghost_media_variant — 처녀귀신
흰 소복과 긴 머리는 특정 대중매체 변형으로 관리하며 모든 전승의 필수 외형으로 삼지 않는다.
- 반영 구분: variant_hold; 원본 슬롯 제안: wardrobe_style.
- 관찰 구성: an explicitly requested Korean female ghost wears loose white mourning cloth / long hair covers part of the same adult face.
- 관계: an explicitly requested Korean female ghost wears loose white mourning cloth → jointly_visible_in_same_event → long hair covers part of the same adult face.
- 혼동 경계: Japanese burial attire substituted; marital status inferred from clothing.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S10](SOURCES.md#s10); SOURCE_GAP_RETAINED. 전체 seed 사실 검증은 아님.

### hvr_bachelor_ghost_context — 총각귀신·몽달귀신
혼인하지 못한 남성 망자의 전승 맥락을 보존하되 고정 외형은 유보한다.
- 반영 구분: context; 원본 슬롯 제안: subject.
- 관찰 구성: a named adult male deceased identity is preserved in the story context.
- 관계: a named adult male deceased identity is preserved in the story context → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: male ghost always faceless; one costume proves unmarried status.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S34](SOURCES.md#s34); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_guest_ghost_unreturned_belonging — 객귀 — 客鬼
객지의 죽음과 돌아가지 못함이라는 관계를 외형과 분리한다.
- 반영 구분: context; 원본 슬롯 제안: narrative_core.
- 관찰 구성: one dead traveler's identity is connected to unreturned belongings.
- 관계: one dead traveler's identity is connected to unreturned belongings → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: any traveler is a ghost; luggage alone proves death away from home.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S34](SOURCES.md#s34); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_unclaimed_soul_context — 무주고혼 — 無主孤魂
돌봄이나 제사의 부재는 사회적 맥락이며 빈 제사상만으로 정체를 확정하지 않는다.
- 반영 구분: context; 원본 슬롯 제안: narrative_core.
- 관찰 구성: an unclaimed memorial record identifies the declared deceased context.
- 관계: an unclaimed memorial record identifies the declared deceased context → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: unmarked grave automatically means this exact category.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S34](SOURCES.md#s34); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_water_ghost_variant — 물귀신
특정 수역과 결부된 죽은 인물이라는 설정과 젖은 외형의 매체 변형을 구분한다.
- 반영 구분: variant_hold; 원본 슬롯 제안: subject.
- 관찰 구성: a declared adult drowned apparition is tied to one visible water margin / wet clothing belongs to that same figure.
- 관계: a declared adult drowned apparition is tied to one visible water margin → jointly_visible_in_same_event → wet clothing belongs to that same figure.
- 혼동 경계: wet swimmer; mermaid; every water spirit is drowned human.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S10](SOURCES.md#s10); SOURCE_GAP_RETAINED. 전체 seed 사실 검증은 아님.

### hvr_dokkaebi_object_origin — 도깨비
도깨비는 망자의 영혼과 다른 자연물 또는 생활물건의 변신 계열을 포함한다.
- 반영 구분: visual; 원본 슬롯 제안: subject.
- 관찰 구성: an animated form retains one recognizable worn-tool structure / a nearby original tool shape confirms the transformation cue.
- 관계: an animated form retains one recognizable worn-tool structure → jointly_visible_in_same_event → a nearby original tool shape confirms the transformation cue.
- 혼동 경계: Japanese oni horns as universal; deceased human ghost.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S09](SOURCES.md#s09); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_gumiho_mimicry_boundary — 구미호
인간 모방과 여우 존재의 경계를 특정 선택형 단서로 표현한다.
- 반영 구분: visual; 원본 슬롯 제안: species_marker.
- 관찰 구성: an otherwise humanlike adult figure retains one expressly selected fox-anatomy cue / the cue connects to that same body.
- 관계: an otherwise humanlike adult figure retains one expressly selected fox-anatomy cue → jointly_visible_in_same_event → the cue connects to that same body.
- 혼동 경계: all attractive women are fox spirits; nine visible tails forced in disguise.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S12](SOURCES.md#s12); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_jangsanbeom_modern_variant — 장산범
장산범은 인터넷 도시괴담 계열이며 개별 외형과 목소리 설정을 판본별로 보존한다.
- 반영 구분: variant_hold; 원본 슬롯 제안: subject.
- 관찰 구성: a specified pale-furred creature remains partly occluded at a forest edge / a visible adult attends toward that edge.
- 관계: a specified pale-furred creature remains partly occluded at a forest edge → jointly_visible_in_same_event → a visible adult attends toward that edge.
- 혼동 경계: ancient canonical Korean deity; still proves voice mimicry.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S13](SOURCES.md#s13); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_yurei_named_variant — 유레이 — Yūrei
유레이는 넓은 유령 범주다. 흰 수의와 사라진 발 등의 조합은 선택된 도상 판본에 한정한다.
- 반영 구분: variant_hold; 원본 슬롯 제안: subject.
- 관찰 구성: a chosen print-based ghost silhouette preserves that print's garment and lower-body treatment.
- 관계: a chosen print-based ghost silhouette preserves that print's garment and lower-body treatment → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: all Japanese ghosts have identical white clothing; Korean sobok substituted.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S14](SOURCES.md#s14), [S29](SOURCES.md#s29); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_onryo_grievance_context — 온료 — Onryō, 원령
복수와 원한의 기능을 망자의 외모와 구분한다.
- 반영 구분: context; 원본 슬롯 제안: subject.
- 관찰 구성: a declared deceased identity is linked to an unresolved grievance.
- 관계: a declared deceased identity is linked to an unresolved grievance → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: every female ghost is onryo; hostile expression proves history.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S11](SOURCES.md#s11); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_yokai_family_context — 요괴 — Yōkai
동물 사물 자연 현상을 포괄하는 넓은 분류로 보존한다.
- 반영 구분: context; 원본 슬롯 제안: subject.
- 관찰 구성: one declared yokai family supplies the requested visible form.
- 관계: one declared yokai family supplies the requested visible form → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: all yokai are dead people; one universal monster anatomy.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S29](SOURCES.md#s29); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_tsukumogami_tool_agency — 츠쿠모가미 — Tsukumogami
오래된 도구의 구조를 유지한 생명과 의지의 표현이다.
- 반영 구분: visual; 원본 슬롯 제안: subject.
- 관찰 구성: a recognizable worn household tool remains the main body / an animate eye or limb grows from that same tool / the original functional structure stays legible.
- 관계: a recognizable worn household tool remains the main body → jointly_visible_in_same_event → an animate eye or limb grows from that same tool and the original functional structure stays legible.
- 혼동 경계: toy with hidden motor; random humanoid holding an umbrella.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S29](SOURCES.md#s29); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_kuchisake_mask_reveal — 쿠치사케온나 — 입 찢어진 여자
기록된 도시괴담의 마스크와 입의 비정상 형태를 하나의 성인 얼굴에 결합한다.
- 반영 구분: visual; 원본 슬롯 제안: expression.
- 관찰 구성: a clearly adult fictional woman's mask is partly lowered / an unusually extended mouth is visible on that same face.
- 관계: a clearly adult fictional woman's mask is partly lowered → jointly_visible_in_same_event → an unusually extended mouth is visible on that same face.
- 혼동 경계: ordinary mask; smiling portrait; all versions share one weapon.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S30](SOURCES.md#s30); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_jiangshi_rigid_pose — 강시 — Jiangshi
되살아난 시체 계열과 뻣뻣한 자세를 구분하며 영화 의복은 별도 변형이다.
- 반영 구분: visual; 원본 슬롯 제안: body_pose.
- 관찰 구성: one corporeal fictional figure holds both arms stiffly forward / feet and torso retain rigid alignment.
- 관계: one corporeal fictional figure holds both arms stiffly forward → jointly_visible_in_same_event → feet and torso retain rigid alignment.
- 혼동 경계: translucent ghost; every Chinese ghost wears Qing robes; still proves hopping.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S15](SOURCES.md#s15), [S12](SOURCES.md#s12); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

## 절 4

### hvr_ghost_general_identity — 고스트 — Ghost
망자의 영혼 또는 나타남이라는 기존 프로필을 재사용하되 특정 연출을 보편 정의로 강제하지 않는다.
- 반영 구분: reuse; 원본 슬롯 제안: subject.
- 관찰 구성: one declared dead person's identity remains recognizable / one locally impossible presence relation is visible.
- 관계: one declared dead person's identity remains recognizable → jointly_visible_in_same_event → one locally impossible presence relation is visible.
- 혼동 경계: lens ghosting; ghost kitchen; translucent cloth.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01), [S16](SOURCES.md#s16); SOURCE_GAP_RETAINED. 전체 seed 사실 검증은 아님.

### hvr_apparition_event_context — 어패리션 — Apparition
나타났다는 사건을 강조하는 겹치는 어휘이며 독립 종으로 늘리지 않는다.
- 반영 구분: context; 원본 슬롯 제안: subject.
- 관찰 구성: one apparition event supplies a visible form in the declared scene.
- 관계: one apparition event supplies a visible form in the declared scene → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: apparition automatically means one fixed translucent anatomy.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S16](SOURCES.md#s16); SOURCE_GAP_RETAINED. 전체 seed 사실 검증은 아님.

### hvr_phantom_overlap_context — 팬텀 — Phantom
환영과 유령의 문맥을 분리하고 매체별 고정 설정을 일반화하지 않는다.
- 반영 구분: context; 원본 슬롯 제안: subject.
- 관찰 구성: a declared illusory or spectral presence is interpreted in whole-request context.
- 관계: a declared illusory or spectral presence is interpreted in whole-request context → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: Phantom brand; phantom pain medical topic; separate species by synonym.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S16](SOURCES.md#s16); SOURCE_GAP_RETAINED. 전체 seed 사실 검증은 아님.

### hvr_specter_spelling_context — 스펙터 — Specter / Spectre
스펙터와 스펙트르는 철자 변형이며 별개의 생물 종이 아니다.
- 반영 구분: context; 원본 슬롯 제안: subject.
- 관찰 구성: a spectral presence inherits the explicitly requested ontology.
- 관계: a spectral presence inherits the explicitly requested ontology → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: spectre and specter as different anatomy; unrelated franchise.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S16](SOURCES.md#s16); SOURCE_GAP_RETAINED. 전체 seed 사실 검증은 아님.

### hvr_wraith_overlap_context — 레이스 — Wraith
살아 있는 사람의 분신 용례도 있어 검은 로브 사신으로 고정하지 않는다.
- 반영 구분: context; 원본 슬롯 제안: subject.
- 관찰 구성: a declared spectral double preserves the owner's recognizable likeness.
- 관계: a declared spectral double preserves the owner's recognizable likeness → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: mandatory scythe; all wraiths are dead and hooded.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S17](SOURCES.md#s17); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_revenant_corporeal_return — 레버넌트 — Revenant
죽음 또는 긴 부재에서 돌아온 존재이며 물질적 시체 버전과 영혼 버전을 요청으로 구별한다.
- 반영 구분: visual; 원본 슬롯 제안: subject.
- 관찰 구성: a corporeal adult returnee stands at a familiar occupied threshold / an identity-linked memorial cue establishes the declared return.
- 관계: a corporeal adult returnee stands at a familiar occupied threshold → jointly_visible_in_same_event → an identity-linked memorial cue establishes the declared return.
- 혼동 경계: all revenants are decayed; generic stranger proves death.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01), [S16](SOURCES.md#s16); SOURCE_GAP_RETAINED. 전체 seed 사실 검증은 아님.

### hvr_poltergeist_object_displacement — 폴터가이스트 — Poltergeist
소란과 사물 변화로 존재를 암시하며 화면에 귀신 몸을 자동 추가하지 않는다.
- 반영 구분: visual; 원본 슬롯 제안: surreal_physics_detail.
- 관찰 구성: one household object is visibly suspended away from its resting place / nearby dust outlines the original object footprint / the surrounding room remains stable.
- 관계: one household object is visibly suspended away from its resting place → jointly_visible_in_same_event → nearby dust outlines the original object footprint and the surrounding room remains stable.
- 혼동 경계: windstorm debris; visible ghost body required; still proves knocking sound.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S18](SOURCES.md#s18); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_doppelganger_pair_divergence — 도플갱어 — Doppelgänger
같은 외형 두 존재의 행동 차이와 독립 존재 여부를 함께 확인한다.
- 반영 구분: visual; 원본 슬롯 제안: relational_action.
- 관찰 구성: two separate adult figures share face and clothing / their hands take different gestures / both occupy distinct physical positions.
- 관계: second adult → matches_appearance_of → first adult; second adult → occupies_independent_position_from → first adult.
- 혼동 경계: mirror reflection; twins prove supernatural origin.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01), [S17](SOURCES.md#s17); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_vampire_identity_variant — 뱀파이어 — Vampire
흡혈 존재의 핵심과 송곳니 망토 거울 부재 등 선택형 관습을 분리한다.
- 반영 구분: visual; 원본 슬롯 제안: species_marker.
- 관찰 구성: a declared adult vampire displays one specified fang cue / its approach targets a separately visible adult.
- 관계: a declared adult vampire displays one specified fang cue → jointly_visible_in_same_event → its approach targets a separately visible adult.
- 혼동 경계: wine proves blood; mandatory cape; every version lacks reflections.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S06](SOURCES.md#s06); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_werewolf_transition — 늑대인간 — Werewolf
인간과 늑대형 구조의 연속 변형을 특정 판본으로 표현한다.
- 반영 구분: visual; 원본 슬롯 제안: anatomical_connection.
- 관찰 구성: one adult fictional body contains linked human and lupine regions / the transition junction remains visible.
- 관계: one adult fictional body contains linked human and lupine regions → jointly_visible_in_same_event → the transition junction remains visible.
- 혼동 경계: fur costume; full moon universally required.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S05](SOURCES.md#s05), [S20](SOURCES.md#s20); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_ghoul_grave_relation — 구울 — Ghoul
무덤 및 시체를 먹는 존재라는 용례와 특정 게임의 외형을 분리한다.
- 반영 구분: variant_hold; 원본 슬롯 제안: subject.
- 관찰 구성: a declared corpse-feeding creature relates to a specific burial setting.
- 관계: a declared corpse-feeding creature relates to a specific burial setting → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: generic ghost; zombie synonym universally; one game design as folklore canon.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S34](SOURCES.md#s34); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_zombie_reanimated_body — 좀비 — Zombie
되살아난 시체 설정과 살아 있는 감염자 설정을 구분한다.
- 반영 구분: visual; 원본 슬롯 제안: subject.
- 관찰 구성: a declared reanimated body retains one selected corpse-condition cue / it moves among physically distinct figures.
- 관계: a declared reanimated body retains one selected corpse-condition cue → jointly_visible_in_same_event → it moves among physically distinct figures.
- 혼동 경계: ill person is zombie; all zombies rotten or contagious.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S05](SOURCES.md#s05); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_banshee_death_omen — 밴시 — Banshee
아일랜드의 울음과 죽음 예고 관계이며 공격형 비명 괴물로 고정하지 않는다.
- 반영 구분: context; 원본 슬롯 제안: subject.
- 관찰 구성: a declared female apparition is associated with an approaching death context.
- 관계: a declared female apparition is associated with an approaching death context → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: universal lethal scream; static open mouth proves audible wail.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S19](SOURCES.md#s19); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_succubus_folklore_context — 서큐버스 — Succubus
수면 중 성적 침입의 여성형 악령 전승을 연구 맥락으로 보존한다.
- 반영 구분: critical; 원본 슬롯 제안: narrative_core.
- 관찰 구성: a declared adult dream-intrusion context preserves the female-form folklore distinction.
- 관계: a declared adult dream-intrusion context preserves the female-form folklore distinction → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: bat wings and lingerie as universal canon; unconscious person implies consent.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S23](SOURCES.md#s23); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_incubus_folklore_context — 인큐버스 — Incubus
수면 중 압박과 침입의 남성형 악령 전승이며 현실 수면 현상과 동일시하지 않는다.
- 반영 구분: critical; 원본 슬롯 제안: narrative_core.
- 관찰 구성: a declared adult sleep-intrusion context preserves the male-form folklore distinction.
- 관계: a declared adult sleep-intrusion context preserves the male-form folklore distinction → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: medical diagnosis from a horror motif; attraction substitutes for coercion.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S24](SOURCES.md#s24); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_penanggalan_variant — 페낭갈란 — Penanggalan
분리된 머리와 매달린 내부 조직이라는 말레이 전승 설명을 기록하되 지역 판본 근거는 추가 확인한다.
- 반영 구분: variant_hold; 원본 슬롯 제안: subject.
- 관찰 구성: a fictional detached head and suspended internal tissue remain one continuous design / the form is explicitly tied to the selected regional variant.
- 관계: a fictional detached head and suspended internal tissue remain one continuous design → jointly_visible_in_same_event → the form is explicitly tied to the selected regional variant.
- 혼동 경계: jiangshi; generic severed head; region-free universal female monster.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S35](SOURCES.md#s35); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

## 절 5

### hvr_haunting_place_residue — 출몰 — Haunting
특정 장소의 출몰 흔적 한 순간을 설계하며 반복 자체는 영상 증거가 필요하다.
- 반영 구분: visual; 원본 슬롯 제안: aftermath_trace.
- 관찰 구성: one identity-linked trace interrupts a specific occupied threshold / surrounding wear confirms the same location.
- 관계: one identity-linked trace interrupts a specific occupied threshold → jointly_visible_in_same_event → surrounding wear confirms the same location.
- 혼동 경계: any dirty abandoned room; a still proves repeated visits.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_possession_agency_split — 빙의 — Possession
신체를 점유하는 다른 의지라는 설정을 국소 동작과 반응의 충돌로 선택한다.
- 반영 구분: visual; 원본 슬롯 제안: body_orientation.
- 관찰 구성: one adult's face reacts away from their hand's directed gesture / both actions belong to the same body.
- 관계: one adult's face reacts away from their hand's directed gesture → jointly_visible_in_same_event → both actions belong to the same body.
- 혼동 경계: odd expression proves possession; medical symptoms as evil.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_curse_object_consequence — 저주 — Curse
저주 설정은 특정 물건과 결과의 관계를 요청에서 유지한다.
- 반영 구분: visual; 원본 슬롯 제안: concept_tension.
- 관찰 구성: a declared curse-bearing object touches one bounded residue trail / the consequence remains tied to that exact object.
- 관계: a declared curse-bearing object touches one bounded residue trail → jointly_visible_in_same_event → the consequence remains tied to that exact object.
- 혼동 경계: any antique object is cursed; causality proven by coincidence.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_summoning_center_intrusion — 소환 — Summoning
호출하는 행위와 그 중심의 이상을 연결한다.
- 반영 구분: visual; 원본 슬롯 제안: relational_action.
- 관찰 구성: an adult ritual gesture points toward a bounded center / one anomalous form occupies that same center.
- 관계: an adult ritual gesture points toward a bounded center → jointly_visible_in_same_event → one anomalous form occupies that same center.
- 혼동 경계: ordinary prayer; disconnected monster overlay.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_seance_shared_focus — 교령회 — Séance
참여자의 공동 초점과 접촉 구조를 한 프레임에서 읽게 한다.
- 반영 구분: visual; 원본 슬롯 제안: relational_action.
- 관찰 구성: clearly adult participants direct attention toward one table center / their hands establish a shared contact arrangement.
- 관계: clearly adult participants direct attention toward one table center → jointly_visible_in_same_event → their hands establish a shared contact arrangement.
- 혼동 경계: dinner table; historical authenticity claimed from generic candles.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_exorcism_contested_threshold — 퇴마 — Exorcism
퇴마는 의식 주체 보호 대상 위협의 관계이며 실제 치료로 주장하지 않는다.
- 반영 구분: visual; 원본 슬롯 제안: relational_action.
- 관찰 구성: an adult officiant faces a declared threatened adult / a protective object sits between them / the threatened figure reacts toward that object.
- 관계: an adult officiant faces a declared threatened adult → jointly_visible_in_same_event → a protective object sits between them and the threatened figure reacts toward that object.
- 혼동 경계: religious portrait alone; medical efficacy claim.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01), [S26](SOURCES.md#s26); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_sealing_bounded_breach — 봉인 — Sealing
봉인은 표면의 닫힘과 그 훼손을 동시에 보인다.
- 반영 구분: visual; 원본 슬롯 제안: prop_direction.
- 관찰 구성: a marked seal bridges one closed seam / a tear opens a gap at that exact seam.
- 관계: a marked seal bridges one closed seam → jointly_visible_in_same_event → a tear opens a gap at that exact seam.
- 혼동 경계: loose decorative paper; intact seal called broken.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S26](SOURCES.md#s26); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_taboo_crossing_boundary — 금기 위반 — Taboo violation
금기 규칙은 서사로 선언하고 경계 침범 한 순간을 시각화한다.
- 반영 구분: visual; 원본 슬롯 제안: relational_action.
- 관찰 구성: a visible adult foot crosses a clearly marked boundary / the mark continues on both sides of the crossing.
- 관계: a visible adult foot crosses a clearly marked boundary → jointly_visible_in_same_event → the mark continues on both sides of the crossing.
- 혼동 경계: every line is sacred; a still proves supernatural punishment.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S26](SOURCES.md#s26); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_residual_haunting_repeat — 반복 재현형 출몰
과거 장면의 비반응 반복은 시간 증거가 필요하며 한 프레임은 반복을 증명하지 못한다.
- 반영 구분: temporal; 원본 슬롯 제안: narrative_phase.
- 관찰 구성: the same identity repeats the same action across ordered frames / a present observer's intervention receives no response.
- 관계: the same identity repeats the same action across ordered frames → jointly_visible_in_same_event → a present observer's intervention receives no response.
- 혼동 경계: one repeated pose; one image proves lack of response over time.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_responsive_haunting_answer — 반응형 출몰
질문이나 접근에 대한 반응은 입력과 응답의 순서를 보존해야 한다.
- 반영 구분: temporal; 원본 슬롯 제안: relational_action.
- 관찰 구성: one adult's visible query gesture precedes an apparition's directed answer / the pair retains shared spatial identity across frames.
- 관계: one adult's visible query gesture precedes an apparition's directed answer → jointly_visible_in_same_event → the pair retains shared spatial identity across frames.
- 혼동 경계: single reciprocal look proves a conversation.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_voice_mimicry_sequence — 목소리 모방 — Voice mimicry
목소리 모방은 발화자 음색 발화 위치의 비교가 필요하다.
- 반영 구분: audio; 원본 슬롯 제안: narrative_core.
- 관찰 구성: a known voice and an impossible source position are compared in synchronized audio.
- 관계: a known voice and an impossible source position are compared in synchronized audio → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: open mouth alone proves a copied voice; white fur proves mimicry.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S25](SOURCES.md#s25), [S13](SOURCES.md#s13); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_reflection_pose_disagreement — 반사 이상 — Reflection anomaly
실제 인물과 물리적으로 맞는 반사의 특정 자세가 어긋난다.
- 반영 구분: visual; 원본 슬롯 제안: reflection_logic.
- 관찰 구성: an adult and mirror share matching location and wardrobe / the actual mouth is neutral / only the reflected mouth smiles.
- 관계: reflected adult → shares_identity_with → physical adult; reflected mouth → mouth_pose_differs_from → physical mouth.
- 혼동 경계: two different people; skewed mirror angle; whole-image corruption.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01), [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_shadow_independent_pose — 독립된 그림자
같은 몸과 연결된 그림자의 자세를 비교하되 광원 자체는 일관되게 둔다.
- 반영 구분: visual; 원본 슬롯 제안: reflection_logic.
- 관찰 구성: one visible adult holds both hands down / the connected cast shadow raises one hand / one readable light source anchors the shadow direction.
- 관계: connected shadow → cast_from → visible adult caster; shadow hand → pose_differs_from → caster hand.
- 혼동 경계: shadow from a second unseen person; multiple-light explanation.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S21](SOURCES.md#s21), [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_missing_time_record — 시간 누락 — Missing time
시간 누락은 같은 사건의 전후 기록 대조로 관리한다.
- 반영 구분: temporal; 원본 슬롯 제안: narrative_phase.
- 관찰 구성: the same scene anchor persists across ordered frames / time markers and environmental state show a discontinuity.
- 관계: the same scene anchor persists across ordered frames → jointly_visible_in_same_event → time markers and environmental state show a discontinuity.
- 혼동 경계: two clocks disagree proves missing time; different photos no shared anchor.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S27](SOURCES.md#s27); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_curse_transmission_lineage — 저주의 전염
전염 조건은 전달자 매개체 수신자 및 순서를 분리한다.
- 반영 구분: temporal; 원본 슬롯 제안: narrative_core.
- 관찰 구성: one object passes between identified adults across frames / the declared anomaly follows the recipient.
- 관계: one object passes between identified adults across frames → jointly_visible_in_same_event → the declared anomaly follows the recipient.
- 혼동 경계: holding same object proves transmission; incidental touch as cause.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_dream_waking_object_match — 꿈의 침입
꿈의 물건과 깨어난 장면의 동일성을 비교하는 선택형 시각 대응이다.
- 반영 구분: visual; 원본 슬롯 제안: concept_tension.
- 관찰 구성: a waking adult holds one distinct object / a nearby dream record contains the same object shape.
- 관계: a waking adult holds one distinct object → jointly_visible_in_same_event → a nearby dream record contains the same object shape.
- 혼동 경계: same generic cup; a still proves dream history.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

## 절 6

### hvr_pallor_local_color — 창백함 — Pallor
혈색 감소는 조명 색과 분리해 같은 얼굴의 피부 입술을 비교한다.
- 반영 구분: visual; 원본 슬롯 제안: skin_condition.
- 관찰 구성: skin and lips have low warm-color separation / nearby neutral material retains normal scene color.
- 관계: skin and lips have low warm-color separation → jointly_visible_in_same_event → nearby neutral material retains normal scene color.
- 혼동 경계: blue light alone; health or death inferred from pallor.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S21](SOURCES.md#s21); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_waxy_skin_surface — 밀랍 같은 피부 — Waxy skin
밀랍 같은 표면과 실제 반투명 신체를 구별한다.
- 반영 구분: visual; 원본 슬롯 제안: skin_finish.
- 관찰 구성: smooth skin shows broad wax-like highlights / facial volume remains opaque and coherent.
- 관계: smooth skin shows broad wax-like highlights → jointly_visible_in_same_event → facial volume remains opaque and coherent.
- 혼동 경계: plastic doll equals living ghost; global blur.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S02](SOURCES.md#s02); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_sunken_eye_socket — 움푹 팬 눈가 — Sunken eyes
눈가의 깊은 음영과 실제 안구 또는 골격 변형을 구분한다.
- 반영 구분: visual; 원본 슬롯 제안: face_shape_relation.
- 관찰 구성: eye sockets have recessed shadow borders / brows and cheek planes retain readable shape.
- 관계: eye sockets have recessed shadow borders → jointly_visible_in_same_event → brows and cheek planes retain readable shape.
- 혼동 경계: top light alone proves altered anatomy; clinical condition label.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S21](SOURCES.md#s21); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_clouded_iris_surface — 흐린 눈 — Clouded eyes
눈 표면이 뿌옇게 가려져 홍채 동공 경계가 약해진 허구 외형이다.
- 반영 구분: visual; 원본 슬롯 제안: eye_detail.
- 관찰 구성: a milky veil crosses the visible iris / the surrounding eyelid remains sharply resolved.
- 관계: a milky veil crosses the visible iris → jointly_visible_in_same_event → the surrounding eyelid remains sharply resolved.
- 혼동 경계: blurred whole face; cataract diagnosis; white contact as universal ghost cue.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S02](SOURCES.md#s02); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_blackened_sclera — 눈 전체의 암흑화 — Blackened eyes
흰자까지 어두운 눈 표면이며 눈가 분장과 다르다.
- 반영 구분: visual; 원본 슬롯 제안: eye_detail.
- 관찰 구성: the visible eye surface including sclera is uniformly dark / eyelid and orbital skin remain separately readable.
- 관계: the visible eye surface including sclera is uniformly dark → jointly_visible_in_same_event → eyelid and orbital skin remain separately readable.
- 혼동 경계: black eyeliner only; dark eye socket with unseen eyeball.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S02](SOURCES.md#s02); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_faceless_smooth_plane — 무안면 — Facelessness
얼굴 면의 부재와 가림을 구분한다.
- 반영 구분: visual; 원본 슬롯 제안: appearance_type.
- 관찰 구성: a coherent head contour contains continuous facial skin / the visible face lacks distinct eye nose and mouth structures.
- 관계: a coherent head contour contains continuous facial skin → jointly_visible_in_same_event → the visible face lacks distinct eye nose and mouth structures.
- 혼동 경계: hair covers face; mask; severe underexposure.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S02](SOURCES.md#s02); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_displaced_features — 이목구비의 위치 이탈
한정된 이목구비 배치 변화와 나머지 얼굴의 정상 기준을 함께 둔다.
- 반영 구분: visual; 원본 슬롯 제안: face_shape_relation.
- 관찰 구성: one eye sits slightly outside its normal alignment / the other facial landmarks remain coherent.
- 관계: one eye sits slightly outside its normal alignment → jointly_visible_in_same_event → the other facial landmarks remain coherent.
- 혼동 경계: random generation defect; dramatic head rotation.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S02](SOURCES.md#s02); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_extended_smile_geometry — 과도하게 긴 미소
비현실적인 입 길이와 단순한 즐거운 표정을 분리한다.
- 반영 구분: visual; 원본 슬롯 제안: expression.
- 관찰 구성: the mouth corners extend beyond normal cheek alignment / the same face retains stable eyes and jaw shape.
- 관계: the mouth corners extend beyond normal cheek alignment → jointly_visible_in_same_event → the same face retains stable eyes and jaw shape.
- 혼동 경계: broad ordinary smile; duration asserted from one frame.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S02](SOURCES.md#s02); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_mouth_eye_affect_split — 눈과 입의 감정 불일치
입의 웃음과 눈 주변의 반응이 서로 맞지 않는 선택형 외형이다.
- 반영 구분: visual; 원본 슬롯 제안: expression.
- 관찰 구성: mouth corners rise visibly / the upper face remains fixed without matching cheek or eye change.
- 관계: mouth corners rise visibly → jointly_visible_in_same_event → the upper face remains fixed without matching cheek or eye change.
- 혼동 경계: proof of fake emotion; every closed-mouth smile uncanny.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S02](SOURCES.md#s02); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_wet_hair_skin_contact — 젖어 뭉친 머리카락
젖은 머리카락은 피부 접촉과 뭉침으로 확인한다.
- 반영 구분: visual; 원본 슬롯 제안: hair_style.
- 관찰 구성: wet hair strands cluster into narrow ropes / several strands adhere to cheek and neck / skin contact remains visible.
- 관계: wet hair strands cluster into narrow ropes → jointly_visible_in_same_event → several strands adhere to cheek and neck and skin contact remains visible.
- 혼동 경계: dry fringe; black blob covering all required facial evidence.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S21](SOURCES.md#s21); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_translucent_body_occlusion — 반투명한 신체 — Translucency
뒤의 구조가 몸 내부를 통과해 보이고 가림 순서가 일관된다.
- 반영 구분: visual; 원본 슬롯 제안: surreal_physics_detail.
- 관찰 구성: a background rail continues visibly through one apparition's torso / the torso's boundary remains readable / opaque surrounding objects retain correct occlusion.
- 관계: apparition torso → transmits_visible_structure_of → background rail.
- 혼동 경계: transparent dress; double exposure of unrelated scenes; blur.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_localized_unstable_outline — 불완전한 윤곽 — Unstable outline
윤곽 흔들림의 한 프레임은 대상 주변 국소 잔상으로만 평가한다.
- 반영 구분: visual; 원본 슬롯 제안: lens_artifact.
- 관찰 구성: a recognizable figure has a bounded secondary edge / nearby stationary room edges stay single and sharp.
- 관계: a recognizable figure has a bounded secondary edge → jointly_visible_in_same_event → nearby stationary room edges stay single and sharp.
- 혼동 경계: global motion blur; whole image noise; still proves ongoing flicker.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_shroud_floor_drag — 낡은 수의·천 — Tattered shroud
덮는 천의 찢김 길이와 바닥 접촉을 각각 확인한다.
- 반영 구분: visual; 원본 슬롯 제안: wardrobe_style.
- 관찰 구성: a worn shroud has readable torn edges / its lower cloth folds drag on the floor / the covered body remains spatially continuous.
- 관계: a worn shroud has readable torn edges → jointly_visible_in_same_event → its lower cloth folds drag on the floor and the covered body remains spatially continuous.
- 혼동 경계: bridal gown automatically shroud; fog replaces fabric.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S21](SOURCES.md#s21); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_levitation_clearance — 부유 — Levitation
부유는 발 지면 틈과 지지의 부재를 볼 수 있어야 한다.
- 반영 구분: visual; 원본 슬롯 제안: body_pose.
- 관찰 구성: both feet remain visibly separated from the floor / a cast shadow occupies the floor beneath / no visible support connects feet to floor.
- 관계: both feet → separated_by_visible_air_gap_from → floor.
- 혼동 경계: cropped feet; low fog hides contact; ordinary jump proves sustained levitation.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_puppet_articulation — 인형 같은 관절 운동
분절 관절의 동작 순서와 몸통 지연은 영상으로 검증한다.
- 반영 구분: temporal; 원본 슬롯 제안: motion.
- 관찰 구성: limb joints initiate motion in separate ordered intervals / the torso follows with a visible lag.
- 관계: limb joints initiate motion in separate ordered intervals → jointly_visible_in_same_event → the torso follows with a visible lag.
- 혼동 경계: one awkward pose proves mechanical timing.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S02](SOURCES.md#s02); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_reverse_travel_direction — 역방향 이동
얼굴 방향과 실제 이동 방향의 분리는 프레임 간 위치 변화로 판정한다.
- 반영 구분: temporal; 원본 슬롯 제안: motion.
- 관찰 구성: the face keeps one orientation / the body changes position backward across ordered frames.
- 관계: the face keeps one orientation → jointly_visible_in_same_event → the body changes position backward across ordered frames.
- 혼동 경계: back-facing pose; blurred trail alone identifies movement direction.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_intermittent_twitch — 단속적 경련 — Twitching
긴 정지 사이의 짧은 경련이라는 시간 구조다.
- 반영 구분: temporal; 원본 슬롯 제안: motion.
- 관찰 구성: a stable pause alternates with short localized motion / the same body persists across the sequence.
- 관계: a stable pause alternates with short localized motion → jointly_visible_in_same_event → the same body persists across the sequence.
- 혼동 경계: one motion smear; neurological diagnosis.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S02](SOURCES.md#s02); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_extended_stillness — 비정상적으로 긴 정지
숨 깜박임 체중 이동의 부재는 관찰 시간을 포함한 영상 설명으로 보존한다.
- 반영 구분: temporal; 원본 슬롯 제안: motion.
- 관찰 구성: a figure remains fixed across a declared duration / nearby ordinary activity continues.
- 관계: a figure remains fixed across a declared duration → jointly_visible_in_same_event → nearby ordinary activity continues.
- 혼동 경계: one still photograph proves no breathing; death inferred.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S02](SOURCES.md#s02); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

## 절 7

### hvr_gore_localized_tissue — 고어 — Gore
피와 손상 조직의 직접 노출을 허구 특수효과 또는 연구 맥락에서 구별한다.
- 반영 구분: visual; 원본 슬롯 제안: aftermath_trace.
- 관찰 구성: a fictional body region carries localized injury detail / blood residue stays connected to that region.
- 관계: a fictional body region carries localized injury detail → jointly_visible_in_same_event → blood residue stays connected to that region.
- 혼동 경계: red paint anywhere; gore mandatory for horror.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S05](SOURCES.md#s05); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_dismemberment_separation — 절단 — Dismemberment
절단은 분리된 부분과 해당 몸의 연속성 단절이라는 관계다.
- 반영 구분: visual; 원본 슬롯 제안: anatomical_connection.
- 관찰 구성: a fictional limb is physically separate from its corresponding body / the anatomical origin remains identifiable.
- 관계: a fictional limb is physically separate from its corresponding body → jointly_visible_in_same_event → the anatomical origin remains identifiable.
- 혼동 경계: cropped limb; detached prosthetic beside unrelated person.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S05](SOURCES.md#s05); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_decapitation_head_body — 참수 — Decapitation
머리 몸 분리의 상태와 절단 행위의 시간적 순간을 구분한다.
- 반영 구분: visual; 원본 슬롯 제안: anatomical_connection.
- 관찰 구성: a fictional head is separated from its identifiable torso / both occupy one continuous scene.
- 관계: a fictional head is separated from its identifiable torso → jointly_visible_in_same_event → both occupy one continuous scene.
- 혼동 경계: head outside crop; mask on a table; Penanggalan conflated with all decapitation.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S05](SOURCES.md#s05); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_flaying_surface_layer — 박피 — Flaying
피부층 제거의 연구 용어를 다른 상처 형태와 분리 보존한다.
- 반영 구분: context; 원본 슬롯 제안: skin_condition.
- 관찰 구성: a declared fictional surface-layer loss differs from a shallow scratch.
- 관계: a declared fictional surface-layer loss differs from a shallow scratch → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: all torn cloth is flaying; every wound exposes the same layer.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S05](SOURCES.md#s05); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_evisceration_inside_outside — 내장 노출 — Evisceration / Disembowelment
내부 장기의 외부 노출이라는 경계 전도를 별도 정의로 관리한다.
- 반영 구분: context; 원본 슬롯 제안: anatomical_connection.
- 관찰 구성: a declared fictional internal structure crosses its normal bodily enclosure.
- 관계: a declared fictional internal structure crosses its normal bodily enclosure → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: generic blood pool; every body transformation implies organ exposure.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S05](SOURCES.md#s05); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_putrefaction_material_state — 부패 — Putrefaction
부패는 변색 형태 붕괴 표면 변화의 조합이며 의학 진단으로 사용하지 않는다.
- 반영 구분: visual; 원본 슬롯 제안: skin_condition.
- 관찰 구성: a fictional remains surface has uneven discoloration / localized tissue form loses structural firmness.
- 관계: a fictional remains surface has uneven discoloration → jointly_visible_in_same_event → localized tissue form loses structural firmness.
- 혼동 경계: dirty live skin; rust texture; one color identifies cause of death.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S05](SOURCES.md#s05); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_parasite_host_junction — 침습·기생 — Infestation / Parasitism
기생은 숙주와 다른 생물의 접점과 점유 구조로 표현한다.
- 반영 구분: visual; 원본 슬롯 제안: anatomical_connection.
- 관찰 구성: one identifiable host body retains its contour / a distinct organism enters or attaches at a visible junction.
- 관계: distinct organism → attaches_at_visible_junction_to → host body.
- 혼동 경계: necklace insect; scattered bugs unrelated to host.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S05](SOURCES.md#s05); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_metamorphosis_transition_band — 돌연변이·변태 — Mutation / Metamorphosis
변형의 중간 단계는 정상 부위 변형 부위 접합띠를 함께 보인다.
- 반영 구분: visual; 원본 슬롯 제안: transition_stage.
- 관찰 구성: one body connects normal structure to altered structure / the intervening transition band remains visibly continuous.
- 관계: one body connects normal structure to altered structure → jointly_visible_in_same_event → the intervening transition band remains visibly continuous.
- 혼동 경계: before-after collage; bodybuilder size change alone.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S05](SOURCES.md#s05); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_bodily_fusion_shared_junction — 신체 융합 — Bodily fusion
융합은 서로 다른 재질이 분리 없이 연결되는 부위에 있다.
- 반영 구분: visual; 원본 슬롯 제안: anatomical_connection.
- 관찰 구성: organic tissue and metal meet at one shared junction / both structures continue through the join.
- 관계: organic tissue → continuously_joins_at_visible_junction → metal structure.
- 혼동 경계: wearable harness; prosthesis simply held beside skin.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S05](SOURCES.md#s05); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_body_melt_support_loss — 신체 액화 — Body melt
몸의 윤곽과 지지력 상실을 흘러내리는 연결된 형상으로 구별한다.
- 반영 구분: visual; 원본 슬롯 제안: surreal_physics_detail.
- 관찰 구성: a fictional body contour slumps into a connected pool / upper structure visibly loses support toward that same pool.
- 관계: a fictional body contour slumps into a connected pool → jointly_visible_in_same_event → upper structure visibly loses support toward that same pool.
- 혼동 경계: wet clothing; a separate puddle; generic blur.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S05](SOURCES.md#s05); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

## 절 8

### hvr_psychosexual_competing_attention — 사이코섹슈얼 호러 — Psychosexual horror
성인 욕망과 불안의 관계를 접근 회피 시선으로 분석한다.
- 반영 구분: visual; 원본 슬롯 제안: proxemics.
- 관찰 구성: one clearly adult figure leans toward another adult / the approaching figure's hand holds back at a visible boundary.
- 관계: one clearly adult figure leans toward another adult → jointly_visible_in_same_event → the approaching figure's hand holds back at a visible boundary.
- 혼동 경계: nudity equals psychosexual horror; one glance proves desire.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S06](SOURCES.md#s06), [S20](SOURCES.md#s20); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_eros_thanatos_critical_frame — 에로스와 타나토스 — Eros / Thanatos
삶 욕망 죽음 충동을 읽는 비평 틀이며 특정 장면의 사실이나 심리 진단이 아니다.
- 반영 구분: critical; 원본 슬롯 제안: concept_tension.
- 관찰 구성: a declared artwork juxtaposes intimacy and a mortality motif.
- 관계: a declared artwork juxtaposes intimacy and a mortality motif → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: all romance leads to death; psychoanalytic theory as empirical fact.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01), [S20](SOURCES.md#s20); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_vampiric_seduction_dual_signal — 흡혈의 매혹 — Vampiric seduction
성인 사이의 접근 친밀감과 포식 단서를 같은 관계 안에 둔다.
- 반영 구분: visual; 원본 슬롯 제안: relational_action.
- 관찰 구성: an adult vampire offers an inviting hand to another adult / one specified fang is visible / the target retains an independently readable response.
- 관계: an adult vampire offers an inviting hand to another adult → jointly_visible_in_same_event → one specified fang is visible and the target retains an independently readable response.
- 혼동 경계: red lipstick proves vampire; sexual violence called romantic.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S06](SOURCES.md#s06); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_voyeuristic_occluded_view — 관음적 공포 — Voyeuristic horror
관찰의 주체 가림 위치 대상 인식 여부를 따로 명시한다.
- 반영 구분: visual; 원본 슬롯 제안: viewer_position.
- 관찰 구성: a foreground doorway edge partly hides the viewpoint / a separately visible adult occupies the observed room.
- 관계: a foreground doorway edge partly hides the viewpoint → jointly_visible_in_same_event → a separately visible adult occupies the observed room.
- 혼동 경계: every POV is voyeurism; still proves legal or private consent status.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_fetish_material_owner — 페티시 미학 — Fetish aesthetics
성인 의복의 물질과 부착 구조를 다루되 성적 동의나 공포를 자동 추론하지 않는다.
- 반영 구분: visual; 원본 슬롯 제안: fetish_styling.
- 관찰 구성: a chosen latex or leather garment follows the adult wearer's body / a visible fastening joins the garment pieces.
- 관계: a chosen latex or leather garment follows the adult wearer's body → jointly_visible_in_same_event → a visible fastening joins the garment pieces.
- 혼동 경계: shiny surface alone; medical restraints recast as consensual fetish.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S06](SOURCES.md#s06); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_restraint_escape_geometry — 구속·지배의 이미지
구속의 접점과 이동 제한을 보이며 합의 여부는 요청의 별도 사실이다.
- 반영 구분: visual; 원본 슬롯 제안: contact_point.
- 관찰 구성: a fictional restraint has visible attachment points / the adult's possible movement ends at those attachments.
- 관계: a fictional restraint has visible attachment points → jointly_visible_in_same_event → the adult's possible movement ends at those attachments.
- 혼동 경계: loose jewelry called restraint; posture implies consent.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01), [S06](SOURCES.md#s06); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_reproductive_autonomy_context — 생식·임신 호러 — Reproductive horror
임신 출산 생식 통제권 상실의 연구 범주이며 모든 임신을 공포로 분류하지 않는다.
- 반영 구분: critical; 원본 슬롯 제안: narrative_core.
- 관찰 구성: a declared adult reproductive-control narrative distinguishes institutional power from bodily state.
- 관계: a declared adult reproductive-control narrative distinguishes institutional power from bodily state → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: pregnancy automatically monstrous; visual diagnosis.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S20](SOURCES.md#s20); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_monstrous_feminine_critical — 괴물적 여성성 — Monstrous-feminine
여성 몸 젠더 성적 차이가 괴물성으로 구성되는 방식을 비평하는 개념이다.
- 반영 구분: critical; 원본 슬롯 제안: genre.
- 관찰 구성: a declared analysis identifies the artwork's gendered representation choices.
- 관계: a declared analysis identifies the artwork's gendered representation choices → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: women intrinsically monsters; automatic female-monster anatomy.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S20](SOURCES.md#s20); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_sexual_violence_autonomy_context — 성적 폭력의 공포
동의와 신체 자율성 박탈을 분석하며 매혹과 강압을 서로 대체하지 않는다.
- 반영 구분: critical; 원본 슬롯 제안: narrative_core.
- 관찰 구성: a declared adult narrative identifies coercion and autonomy loss independently of attraction.
- 관계: a declared adult narrative identifies coercion and autonomy loss independently of attraction → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: erotic styling implies consent; graphic assault as an optional decorative candidate.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01), [S20](SOURCES.md#s20); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_family_taboo_context — 가족 내부의 성적 금기
가족 내부의 보호 권력 착취 구조를 비평 맥락으로 보존한다.
- 반영 구분: critical; 원본 슬롯 제안: narrative_core.
- 관찰 구성: a declared adult family narrative specifies the power relationship.
- 관계: a declared adult family narrative specifies the power relationship → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: family portrait proves abuse; romantic substitution for coercion.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_necrophilia_critical_context — 네크로필리아 — Necrophilia
시체 대상 성적 욕망이라는 금기 용어를 연구 정의로 보존한다.
- 반영 구분: critical; 원본 슬롯 제안: narrative_core.
- 관찰 구성: a critical account distinguishes corpse-directed desire from grief and memorial attachment.
- 관계: a critical account distinguishes corpse-directed desire from grief and memorial attachment → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: mourning gesture equals necrophilia; eroticized corpse candidate.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S34](SOURCES.md#s34); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_cannibalism_person_food_context — 카니벌리즘 — Cannibalism, 식인
인간을 먹이로 취급하는 행위의 범주이며 행위와 음식 소품의 의미를 구분한다.
- 반영 구분: critical; 원본 슬롯 제안: narrative_core.
- 관찰 구성: a declared fictional narrative identifies human-as-food treatment.
- 관계: a declared fictional narrative identifies human-as-food treatment → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: ordinary meat dish proves cannibalism; all ghoul traditions identical.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S08](SOURCES.md#s08); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

## 절 9

### hvr_mansion_inherited_barrier — 폐저택·폐성
폐저택은 생활 흔적과 건물의 닫힌 경로를 비교하는 공간이다.
- 반영 구분: visual; 원본 슬롯 제안: location.
- 관찰 구성: old occupied-room traces remain within a large house / one sealed internal passage interrupts the route.
- 관계: old occupied-room traces remain within a large house → jointly_visible_in_same_event → one sealed internal passage interrupts the route.
- 혼동 경계: all old architecture haunted; Gothic architecture mandatory.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_attic_hidden_volume — 다락방
다락은 아래 생활 공간에서 보이지 않는 위쪽 저장 공간을 만든다.
- 반영 구분: visual; 원본 슬롯 제안: location.
- 관찰 구성: a narrow hatch connects an occupied room to stored attic objects / the opening hides the rear attic volume.
- 관계: a narrow hatch connects an occupied room to stored attic objects → jointly_visible_in_same_event → the opening hides the rear attic volume.
- 혼동 경계: any messy room; footsteps proved without sound.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_basement_single_stair — 지하실
지하실은 아래층과 계단 위 출구의 상대 위치가 중요하다.
- 반영 구분: visual; 원본 슬롯 제안: location.
- 관찰 구성: a below-ground room contains one stair rising to a closed upper door / the adult remains below that door level.
- 관계: a below-ground room contains one stair rising to a closed upper door → jointly_visible_in_same_event → the adult remains below that door level.
- 혼동 경계: dark room at ground level; no visible egress comparison.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_corridor_repeating_bay — 긴 복도
반복되는 문 조명 간격을 유지해 하나의 변화가 보이게 한다.
- 반영 구분: visual; 원본 슬롯 제안: location.
- 관찰 구성: a long corridor repeats door bays and lights / one far bay differs visibly from the repeated baseline.
- 관계: a long corridor repeats door bays and lights → jointly_visible_in_same_event → one far bay differs visibly from the repeated baseline.
- 혼동 경계: distance alone proves infinite loop; every hotel hallway liminal.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_stairwell_hidden_landing — 계단실
위아래의 연결과 가려진 계단참으로 위치 불확실성을 만든다.
- 반영 구분: visual; 원본 슬롯 제안: location.
- 관찰 구성: stairs connect two visible levels / a central landing occludes the next flight.
- 관계: stairs connect two visible levels → jointly_visible_in_same_event → a central landing occludes the next flight.
- 혼동 경계: random floating stairs; impossible floor labels necessary.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_elevator_presence_comparison — 엘리베이터
엘리베이터 실내와 거울의 인원 비교를 같은 프레임에 둔다.
- 반영 구분: visual; 원본 슬롯 제안: reflection_logic.
- 관찰 구성: the physical elevator contains one adult / its aligned mirror includes one additional figure / door and rail geometry correspond.
- 관계: aligned reflection → contains_additional_presence_beyond → physical elevator occupancy.
- 혼동 경계: real person just outside frame; convex mirror field difference.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_well_depth_boundary — 우물
우물은 보이는 가장자리와 읽히지 않는 안쪽 깊이의 관계다.
- 반영 구분: visual; 원본 슬롯 제안: location.
- 관찰 구성: a stone rim bounds a descending shaft / water or darkness obscures the shaft bottom.
- 관계: a stone rim bounds a descending shaft → jointly_visible_in_same_event → water or darkness obscures the shaft bottom.
- 혼동 경계: ordinary circular basin; blur replaces geometry.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_tunnel_two_exit_limits — 터널·지하 통로
터널은 양 끝의 출구와 중간 차광 영역을 구분한다.
- 반영 구분: visual; 원본 슬롯 제안: location.
- 관찰 구성: a tunnel has readable near and distant openings / the middle region withholds detail.
- 관계: a tunnel has readable near and distant openings → jointly_visible_in_same_event → the middle region withholds detail.
- 혼동 경계: black backdrop; a still proves changing distance.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_cemetery_name_absence — 묘지·납골 공간
이름과 매장 위치의 배열에서 한 국소 결손을 만드는 선택이다.
- 반영 구분: visual; 원본 슬롯 제안: prop.
- 관찰 구성: grave markers form an ordered sequence / one marker retains a visibly blank identity panel.
- 관계: grave markers form an ordered sequence → jointly_visible_in_same_event → one marker retains a visibly blank identity panel.
- 혼동 경계: anonymous marker proves specific dead identity; text correctness assumed.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_morgue_inventory_mismatch — 영안실·해부실
보관 신체와 기록 수량을 비교하는 설정이다.
- 반영 구분: visual; 원본 슬롯 제안: situation_context.
- 관찰 구성: three covered storage forms share one room / a clearly countable three-slot inventory has an extra occupied marker.
- 관계: three covered storage forms share one room → jointly_visible_in_same_event → a clearly countable three-slot inventory has an extra occupied marker.
- 혼동 경계: small illegible text; every covered object corpse.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_hospital_protection_gap — 폐병원
보호 기능의 부재를 설비 작동 상태와 점유 부재의 차이로 보인다.
- 반영 구분: visual; 원본 슬롯 제안: location.
- 관찰 구성: ready clinical furniture remains aligned / a single call indicator is lit beside an empty bed.
- 관계: ready clinical furniture remains aligned → jointly_visible_in_same_event → a single call indicator is lit beside an empty bed.
- 혼동 경계: hospital inherently evil; illuminated button proves audible alarm.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_laboratory_observation_barrier — 실험실·격리 시설
관찰 유리가 관찰자와 피관찰자의 이동을 분리하는 관계다.
- 반영 구분: visual; 원본 슬롯 제안: composition.
- 관찰 구성: an adult observer stands outside a transparent enclosure / a separately visible adult remains inside / the enclosure's locked access point is visible.
- 관계: an adult observer stands outside a transparent enclosure → jointly_visible_in_same_event → a separately visible adult remains inside and the enclosure's locked access point is visible.
- 혼동 경계: same side of glass; laboratory equals abusive institution.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_school_schedule_absence — 폐교
학교 기능 표식과 비어 있는 활동 공간을 비교한다.
- 반영 구분: visual; 원본 슬롯 제안: location.
- 관찰 구성: ordered desks and an active clock remain visible / the room lacks expected occupants / one freshly moved chair interrupts the order.
- 관계: ordered desks and an active clock remain visible → jointly_visible_in_same_event → the room lacks expected occupants and one freshly moved chair interrupts the order.
- 혼동 경계: abandoned ruin only; child or injury implicitly added.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_hotel_connecting_door — 호텔·모텔
낯선 숙소의 연결문과 이웃 공간의 부재 정보를 보존한다.
- 반영 구분: visual; 원본 슬롯 제안: location.
- 관찰 구성: a temporary-use room has a connecting door / one recent guest trace lies beside that door.
- 관계: a temporary-use room has a connecting door → jointly_visible_in_same_event → one recent guest trace lies beside that door.
- 혼동 경계: ordinary bedroom; sound heard through wall proven by still.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_pool_submerged_presence — 수영장·목욕탕
수면 위와 아래의 수량 비교는 반사 굴절 가림을 통제해야 한다.
- 반영 구분: visual; 원본 슬롯 제안: reflection_logic.
- 관찰 구성: a clearly bounded pool edge shows no standing figure / one distinct submerged humanlike shape occupies the corresponding visible water region.
- 관계: a clearly bounded pool edge shows no standing figure → jointly_visible_in_same_event → one distinct submerged humanlike shape occupies the corresponding visible water region.
- 혼동 경계: reflection mistaken for submerged body; murky water hides required relation.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_mall_operational_absence — 텅 빈 쇼핑몰·사무실
쇼핑몰 사무실의 기능 유지와 기대 점유 부재를 기존 리미널 의미로 보강한다.
- 반영 구분: reuse; 원본 슬롯 제안: location.
- 관찰 구성: a maintained commercial or office interior retains operational service cues / the expected users are absent.
- 관계: a maintained commercial or office interior retains operational service cues → jointly_visible_in_same_event → the expected users are absent.
- 혼동 경계: ruin automatically liminal; no use-function evidence.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_industrial_processing_route — 도살장·산업 시설
레일 배수구 세척 표면을 실제 이동 처리 경로로 연결한다.
- 반영 구분: visual; 원본 슬롯 제안: location.
- 관찰 구성: a rail leads toward a washable work area / a floor drain sits below that same route / one obstruction interrupts the path.
- 관계: a rail leads toward a washable work area → jointly_visible_in_same_event → a floor drain sits below that same route and one obstruction interrupts the path.
- 혼동 경계: factory photograph alone; automatic gore or victims.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_forest_occluded_depth — 숲·갈대밭
시야를 잘게 가리는 식생과 한정된 이동 흔적을 설계한다.
- 반영 구분: visual; 원본 슬롯 제안: composition.
- 관찰 구성: near reeds occlude a deeper path / one localized gap reveals a partly hidden nonhuman form.
- 관계: near reeds occlude a deeper path → jointly_visible_in_same_event → one localized gap reveals a partly hidden nonhuman form.
- 혼동 경계: all trees equally blurred; ordinary forest proves monster.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_flooded_depth_uncertainty — 늪·저수지·침수 공간
수면 위 평온과 바닥 깊이의 미확인을 분리한다.
- 반영 구분: visual; 원본 슬롯 제안: location.
- 관찰 구성: still water covers a recognizable flooded room / submerged furniture fades below the surface / the visible doorway establishes depth scale.
- 관계: still water covers a recognizable flooded room → jointly_visible_in_same_event → submerged furniture fades below the surface and the visible doorway establishes depth scale.
- 혼동 경계: haze as water; unsupported floating architecture.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_sealed_habitat_external_limit — 배·심해·우주 시설
배 심해 우주 시설은 내부 위협과 외부 탈출 불가 환경을 함께 보여준다.
- 반영 구분: visual; 원본 슬롯 제안: location.
- 관찰 구성: an enclosed working interior faces a visible hostile external environment / one sealed exit separates the two / an internal anomaly lies on the exit route.
- 관계: an enclosed working interior faces a visible hostile external environment → jointly_visible_in_same_event → one sealed exit separates the two and an internal anomaly lies on the exit route.
- 혼동 경계: ordinary cabin; every exterior darkness vacuum.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S04](SOURCES.md#s04), [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

## 절 9p

### hvr_liminal_maintained_use_gap — 리미널 스페이스 — Liminal space
통과 대기 전이 기능이 유지되는데 예정된 사용이 비어 있는 관계다.
- 반영 구분: reuse; 원본 슬롯 제안: space_condition.
- 관찰 구성: a maintained transit space has route and waiting cues / ready service objects remain unused / one threshold lacks its expected destination or activity.
- 관계: a maintained transit space has route and waiting cues → jointly_visible_in_same_event → ready service objects remain unused and one threshold lacks its expected destination or activity.
- 혼동 경계: all vacant rooms; all backrooms; all ruins.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

## 절 10

### hvr_fog_distance_occlusion — 짙은 안개 — Dense fog
짙은 안개는 먼 정보 감소이며 대상 존재의 증거가 아니다.
- 반영 구분: visual; 원본 슬롯 제안: weather.
- 관찰 구성: near objects retain readable edges / far objects lose contrast through the same air volume.
- 관계: near objects retain readable edges → jointly_visible_in_same_event → far objects lose contrast through the same air volume.
- 혼동 경계: global blur; opaque painted background.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_ground_fog_low_band — 낮게 깔린 안개 — Ground fog
낮은 안개는 발과 접촉면을 가리므로 부유 검증과 함께 요구하면 충돌한다.
- 반영 구분: visual; 원본 슬롯 제안: atmosphere.
- 관찰 구성: a fog band occupies the floor region / upper bodies remain clearer than lower legs.
- 관계: a fog band occupies the floor region → jointly_visible_in_same_event → upper bodies remain clearer than lower legs.
- 혼동 경계: whole-room haze; hidden feet scored as levitation.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_haze_light_volume — 연무 — Haze
연무는 공간의 산란과 명암 감소로 읽는다.
- 반영 구분: visual; 원본 슬롯 제안: ambient_particle.
- 관찰 구성: a localized light beam scatters through suspended air particles / room structures remain recognizable beyond it.
- 관계: a localized light beam scatters through suspended air particles → jointly_visible_in_same_event → room structures remain recognizable beyond it.
- 혼동 경계: glow outline painted on body; universal depth blur.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S21](SOURCES.md#s21); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_rain_window_cutoff — 장대비 — Torrential rain
장대비의 한 순간은 물방울 경로와 외부 정보 차단으로 표현한다.
- 반영 구분: visual; 원본 슬롯 제안: weather.
- 관찰 구성: dense rain streaks cross the window plane / outside details weaken behind that same wet glass.
- 관계: dense rain streaks cross the window plane → jointly_visible_in_same_event → outside details weaken behind that same wet glass.
- 혼동 경계: vertical scratches as rain; still proves acoustic masking.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_lightning_reveal_frame — 천둥과 번개
번개에 따른 위치 변화는 시간 비교가 필요하다.
- 반영 구분: temporal; 원본 슬롯 제안: lighting.
- 관찰 구성: ordered dark and lightning-lit frames preserve the same room / the revealed form changes position between frames.
- 관계: ordered dark and lightning-lit frames preserve the same room → jointly_visible_in_same_event → the revealed form changes position between frames.
- 혼동 경계: one flash-lit photograph proves movement; strobe noise.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S21](SOURCES.md#s21); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_snow_track_terminal — 눈 덮인 적막
눈의 흰 바탕에서 발자국 경로의 종료를 비교한다.
- 반영 구분: visual; 원본 슬롯 제안: aftermath_trace.
- 관찰 구성: one readable track chain crosses undisturbed snow / the chain ends at an otherwise empty bounded area.
- 관계: one readable track chain crosses undisturbed snow → jointly_visible_in_same_event → the chain ends at an otherwise empty bounded area.
- 혼동 경계: tracks hidden behind subject; snowfall erased evidence.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_twilight_detail_threshold — 박명 — Twilight
박명은 시간대 문맥과 외부 밝기를 유지하며 세부 읽기 한계를 조절한다.
- 반영 구분: visual; 원본 슬롯 제안: time_of_day.
- 관찰 구성: the sky retains low twilight luminance / foreground silhouettes remain readable / fine background detail weakens.
- 관계: the sky retains low twilight luminance → jointly_visible_in_same_event → foreground silhouettes remain readable and fine background detail weakens.
- 혼동 경계: night blue filter alone; sunset always safe.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S21](SOURCES.md#s21); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_predawn_still_frame — 새벽 직전의 정적
새벽 직전과 정적을 한 이미지의 보편 감정으로 확정하지 않는다.
- 반영 구분: context; 원본 슬롯 제안: time_of_day.
- 관찰 구성: a declared predawn scene retains low ambient light and ordinary morning-use cues.
- 관계: a declared predawn scene retains low ambient light and ordinary morning-use cues → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: time of day inferred from color alone; sound absence proved.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S21](SOURCES.md#s21), [S25](SOURCES.md#s25); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_daylight_exposed_threat — 한낮의 공포 — Daylight dread
밝음과 안전을 분리하여 명확히 보이는 위협과 평상 행동을 병치한다.
- 반영 구분: visual; 원본 슬롯 제안: lighting.
- 관찰 구성: bright even daylight reveals the whole setting / a bounded anomaly remains clearly visible / adult bystanders retain ordinary task poses.
- 관계: bright even daylight reveals the whole setting → jointly_visible_in_same_event → a bounded anomaly remains clearly visible and adult bystanders retain ordinary task poses.
- 혼동 경계: overexposed white frame; smiling crowd inherently cult.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S03](SOURCES.md#s03), [S21](SOURCES.md#s21); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_still_air_single_cloth — 무풍 — Unnatural stillness
정지한 주변과 한 재질의 움직임 차이는 정지 순간의 형태 대비로만 읽는다.
- 반영 구분: visual; 원본 슬롯 제안: surreal_physics_detail.
- 관찰 구성: nearby hanging fabrics fall vertically / one selected cloth extends sideways without a visible support.
- 관계: nearby hanging fabrics fall vertically → jointly_visible_in_same_event → one selected cloth extends sideways without a visible support.
- 혼동 경계: wind globally affects every object; still proves absence of airflow.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S21](SOURCES.md#s21); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_damp_material_consistency — 눅눅함 — Dampness
습기는 표면 젖음과 재질별 반응을 일관되게 배치한다.
- 반영 구분: visual; 원본 슬롯 제안: texture.
- 관찰 구성: wall discoloration follows a damp lower band / cloth at that height darkens and clumps / metal nearby carries wet highlights.
- 관계: wall discoloration follows a damp lower band → jointly_visible_in_same_event → cloth at that height darkens and clumps and metal nearby carries wet highlights.
- 혼동 경계: same overlay on all materials; mold required.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S21](SOURCES.md#s21); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_stale_air_recent_trace — 정체된 공기 — Stale air
정체된 공기는 직접 보이지 않으므로 먼지 정지와 최근 사용 흔적으로 제한해 옮긴다.
- 반영 구분: visual; 원본 슬롯 제안: aftermath_trace.
- 관찰 구성: settled dust covers a closed room / one fresh hand-width clean streak interrupts the dust.
- 관계: settled dust covers a closed room → jointly_visible_in_same_event → one fresh hand-width clean streak interrupts the dust.
- 혼동 경계: smell or air age objectively proven from image; poverty equals horror.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_odor_context — 쇠·곰팡이·부패의 냄새
금속 곰팡이 부패 냄새는 시각 설명과 별도 감각 정보로 보존한다.
- 반영 구분: context; 원본 슬롯 제안: sensory_focus.
- 관찰 구성: visible rust mold or fictional decay may motivate a declared odor description.
- 관계: visible rust mold or fictional decay may motivate a declared odor description → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: visible stain proves actual odor; illness inferred from room.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S21](SOURCES.md#s21); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_ambient_sound_drop — 환경음의 갑작스러운 소실
환경음 소실은 이전 음장과 이후 음장의 시간 차다.
- 반영 구분: audio; 원본 슬롯 제안: narrative_phase.
- 관찰 구성: a continuous environment recording abruptly loses a previously present sound layer.
- 관계: a continuous environment recording abruptly loses a previously present sound layer → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: empty room proves silence; universal fear-frequency claim.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S25](SOURCES.md#s25); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

## 절 11

### hvr_palette_moon_ink — 달빛과 먹빛
먹색 청회색 은회색을 배경 중간거리 가장자리의 소유자에 배치한다.
- 반영 구분: visual; 원본 슬롯 제안: color.
- 관찰 구성: ink-dark background bounds blue-gray depth layers / silver-gray edges separate the focal shape.
- 관계: ink-dark background bounds blue-gray depth layers → jointly_visible_in_same_event → silver-gray edges separate the focal shape.
- 혼동 경계: all blue means fear; global tint without spatial owners.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_palette_mold_ward — 곰팡이 든 병실
회녹색 누런 흰색 녹슨 갈색은 각 재질에 소속된다.
- 반영 구분: visual; 원본 슬롯 제안: color.
- 관찰 구성: yellowed off-white tiles border gray-green stains / rust-brown metal remains separately identifiable.
- 관계: yellowed off-white tiles border gray-green stains → jointly_visible_in_same_event → rust-brown metal remains separately identifiable.
- 혼동 경계: every sickly green proves disease; random color patches.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_palette_single_crimson — 상복과 피의 한 점
검정 뼈색 배경에 하나의 제한된 짙은 적색 초점을 둔다.
- 반영 구분: visual; 원본 슬롯 제안: color.
- 관찰 구성: black and bone-colored surfaces dominate the frame / one crimson object forms a localized focal accent.
- 관계: black and bone-colored surfaces dominate the frame → jointly_visible_in_same_event → one crimson object forms a localized focal accent.
- 혼동 경계: red everywhere; any red necessarily blood.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_palette_candle_cold_exterior — 촛불과 깊은 밤
호박색의 국소 광원 영역과 차가운 외부 음영을 공간적으로 분리한다.
- 반영 구분: visual; 원본 슬롯 제안: color.
- 관찰 구성: a small amber light pool surrounds a visible candle / dark blue space remains beyond the pool.
- 관계: a small amber light pool surrounds a visible candle → jointly_visible_in_same_event → dark blue space remains beyond the pool.
- 혼동 경계: global orange filter; color without source ownership.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S21](SOURCES.md#s21), [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_palette_neon_opposed_sources — 네온의 독성
자홍과 청록은 서로 다른 인공 광원과 영향을 받는 표면에 묶는다.
- 반영 구분: visual; 원본 슬롯 제안: color.
- 관찰 구성: magenta light strikes one side of a surface / cyan light strikes a different side / violet-black areas retain separation.
- 관계: magenta light strikes one side of a surface → jointly_visible_in_same_event → cyan light strikes a different side and violet-black areas retain separation.
- 혼동 경계: all neon means giallo; random colored objects.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S07](SOURCES.md#s07), [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_palette_faded_record — 빛바랜 가족사진
세피아 종이색 회갈색은 기록물의 표면 색이며 장면 전체의 시대를 증명하지 않는다.
- 반영 구분: visual; 원본 슬롯 제안: color.
- 관찰 구성: a sepia photographic print lies on paper-colored backing / gray-brown fading remains inside the print surface.
- 관계: a sepia photographic print lies on paper-colored backing → jointly_visible_in_same_event → gray-brown fading remains inside the print surface.
- 혼동 경계: sepia everywhere proves old memory; foxing automatically face anomaly.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_palette_underwater_depth — 해저의 어둠
흑청 탁한 청록 창백한 민트는 물의 깊이와 피사체 소속을 분리한다.
- 반영 구분: visual; 원본 슬롯 제안: color.
- 관찰 구성: black-blue depth encloses muted teal near-water detail / pale mint belongs to the selected submerged surface.
- 관계: black-blue depth encloses muted teal near-water detail → jointly_visible_in_same_event → pale mint belongs to the selected submerged surface.
- 혼동 경계: universal color psychology; mint skin diagnoses death.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_palette_clean_cold_room — 지나치게 깨끗한 공간
회백 옅은 청색 흑색은 정돈된 밝은 공간에서도 경계 대비를 만든다.
- 반영 구분: visual; 원본 슬롯 제안: color.
- 관찰 구성: off-white room planes retain detail / pale-blue fixtures are organized evenly / one dark opening interrupts the arrangement.
- 관계: off-white room planes retain detail → jointly_visible_in_same_event → pale-blue fixtures are organized evenly and one dark opening interrupts the arrangement.
- 혼동 경계: cleanliness inherently sinister; clipped white hides evidence.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S21](SOURCES.md#s21), [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_palette_daylight_ritual — 아름다운 낮의 의식
볏짚 꽃의 흰색 잎색은 실제 재질에 묶고 공동체 관계는 별도로 요구한다.
- 반영 구분: visual; 원본 슬롯 제안: color.
- 관찰 구성: straw-colored ground supports white floral objects / leaf-green forms enclose the same gathering.
- 관계: straw-colored ground supports white floral objects → jointly_visible_in_same_event → leaf-green forms enclose the same gathering.
- 혼동 경계: folk ritual proven by palette alone; mandatory blood accent.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S03](SOURCES.md#s03), [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_palette_flesh_steel — 살과 기계
살구 강철 암적색은 유기 무기 접합의 각 소유자에 묶는다.
- 반영 구분: visual; 원본 슬롯 제안: color.
- 관찰 구성: muted flesh-colored organic material joins steel-gray hardware / dark-red tone remains localized at the junction.
- 관계: muted flesh-colored organic material joins steel-gray hardware → jointly_visible_in_same_event → dark-red tone remains localized at the junction.
- 혼동 경계: metal tint painted on skin; all fusion needs gore.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S05](SOURCES.md#s05), [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_palette_display_limited — 낡은 방송 신호
푸른 화면 전자녹 바랜 회색은 표시 매체 영역 안에서 작동한다.
- 반영 구분: visual; 원본 슬롯 제안: color.
- 관찰 구성: a bounded display emits limited blue and green tones / faded gray interface elements remain inside that screen.
- 관계: a bounded display emits limited blue and green tones → jointly_visible_in_same_event → faded gray interface elements remain inside that screen.
- 혼동 경계: screen palette tints all physical skin; any CRT horror.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S32](SOURCES.md#s32); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_palette_metal_monochrome — 금속성 흑백
금속성 흑백은 명암과 반사 거칠기 차이를 통해 재질을 읽게 한다.
- 반영 구분: visual; 원본 슬롯 제안: color.
- 관찰 구성: black white and gray surfaces retain distinct roughness / specular metal highlights differ from matte skin.
- 관계: black white and gray surfaces retain distinct roughness → jointly_visible_in_same_event → specular metal highlights differ from matte skin.
- 혼동 경계: grayscale equals metal; blown highlights hide junction.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

## 절 12

### hvr_low_key_key_fill — 로우키 — Low-key lighting
로우키는 보조광이 작아 생기는 큰 명암 대비이며 단순 저노출과 다르다.
- 반영 구분: reuse; 원본 슬롯 제안: lighting.
- 관찰 구성: one lit facial or object plane remains readable / opposing fill stays weak / large shadow regions preserve spatial structure.
- 관계: one lit facial or object plane remains readable → jointly_visible_in_same_event → opposing fill stays weak and large shadow regions preserve spatial structure.
- 혼동 경계: everything underexposed; low-key equals soft light.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S21](SOURCES.md#s21); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_high_key_even_fill — 하이키 — High-key lighting
하이키는 키광과 보조광의 관계로 그림자 대비가 약하며 과다노출과 다르다.
- 반영 구분: reuse; 원본 슬롯 제안: lighting.
- 관찰 구성: principal surfaces receive broadly even illumination / soft shadows retain detail / bright textures remain unclipped.
- 관계: principal surfaces receive broadly even illumination → jointly_visible_in_same_event → soft shadows retain detail and bright textures remain unclipped.
- 혼동 경계: white clipping; all bright images high-key.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S21](SOURCES.md#s21); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_hard_light_shadow_edge — 하드 라이트 — Hard light
하드 라이트는 그림자 경계가 뚜렷한 광질이다.
- 반영 구분: reuse; 원본 슬롯 제안: light_type.
- 관찰 구성: a cast shadow has a sharply readable edge / the lit receiving surface remains visible.
- 관계: a cast shadow has a sharply readable edge → jointly_visible_in_same_event → the lit receiving surface remains visible.
- 혼동 경계: hard mood; high contrast automatically sharp edges.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S21](SOURCES.md#s21); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_soft_light_transition — 소프트 라이트 — Soft light
소프트 라이트는 그림자 경계가 부드러운 광질이며 공포 내용과 독립이다.
- 반영 구분: reuse; 원본 슬롯 제안: light_type.
- 관찰 구성: a cast shadow transitions gradually across a visible surface / face or object contours remain resolved.
- 관계: a cast shadow transitions gradually across a visible surface → jointly_visible_in_same_event → face or object contours remain resolved.
- 혼동 경계: out-of-focus subject; no shadows required.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S21](SOURCES.md#s21); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_underlight_face_planes — 언더라이팅 — Underlighting
아래 광원의 실제 명암 방향을 이마 코 볼에서 확인한다.
- 반영 구분: visual; 원본 슬롯 제안: light_direction.
- 관찰 구성: a visible low light source illuminates lower facial planes / the nose shadow rises toward the upper face.
- 관계: a visible low light source illuminates lower facial planes → jointly_visible_in_same_event → the nose shadow rises toward the upper face.
- 혼동 경계: lower camera angle; spooky label without light geometry.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S21](SOURCES.md#s21); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_toplight_orbital_shadow — 탑 라이팅 — Top lighting
상부 광원과 눈가 음영 및 이마 어깨 하이라이트의 관계다.
- 반영 구분: visual; 원본 슬롯 제안: light_direction.
- 관찰 구성: upper facial planes and shoulders receive light / eye sockets fall into downward cast shadow.
- 관계: upper facial planes and shoulders receive light → jointly_visible_in_same_event → eye sockets fall into downward cast shadow.
- 혼동 경계: sunken-eye anatomy inferred from lighting; required eyes obscured.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S21](SOURCES.md#s21); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_backlight_source_separation — 백라이팅 — Backlighting
뒤의 광원과 대상 내부 정보 부족을 구분한다.
- 반영 구분: reuse; 원본 슬롯 제안: light_direction.
- 관찰 구성: a source behind the figure brightens hair or cloth edges / the front face receives less light.
- 관계: a source behind the figure brightens hair or cloth edges → jointly_visible_in_same_event → the front face receives less light.
- 혼동 경계: ring painted around subject; necessarily faceless ghost.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S21](SOURCES.md#s21); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_rim_edge_localization — 림 라이트 — Rim light
림 라이트는 가장자리에 제한된 빛의 띠이며 전체 광륜이 아니다.
- 반영 구분: reuse; 원본 슬롯 제안: lighting.
- 관찰 구성: a narrow highlight follows selected outer edges / interior surfaces remain differently illuminated.
- 관계: a narrow highlight follows selected outer edges → jointly_visible_in_same_event → interior surfaces remain differently illuminated.
- 혼동 경계: global glow aura; cutout border.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S21](SOURCES.md#s21); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_silhouette_background_relation — 실루엣 — Silhouette
밝은 배경과 어두운 대상의 관계로 외곽을 읽는다.
- 반영 구분: visual; 원본 슬롯 제안: lighting.
- 관찰 구성: a dark opaque figure stands before a brighter background / pose remains identifiable from the contour.
- 관계: a dark opaque figure stands before a brighter background → jointly_visible_in_same_event → pose remains identifiable from the contour.
- 혼동 경계: dark face crop only; translucent ghost automatically.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S21](SOURCES.md#s21); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_practical_visible_source — 프랙티컬 라이트 — Practical light
장면 안의 광원을 실제 밝은 영역과 연결한다.
- 반영 구분: reuse; 원본 슬롯 제안: lighting.
- 관찰 구성: a visible lamp candle or monitor emits light / nearby surfaces brighten toward that source.
- 관계: a visible lamp candle or monitor emits light → jointly_visible_in_same_event → nearby surfaces brighten toward that source.
- 혼동 경계: unseen studio key called practical; isolated lamp no effect.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S21](SOURCES.md#s21); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_flicker_temporal_envelope — 플리커 — Flicker
플리커는 밝기의 시간 변화이므로 한 프레임 조명 상태로 성공 판정하지 않는다.
- 반영 구분: temporal; 원본 슬롯 제안: lighting.
- 관찰 구성: the same visible source changes brightness across ordered frames / the receiving surfaces follow those changes.
- 관계: the same visible source changes brightness across ordered frames → jointly_visible_in_same_event → the receiving surfaces follow those changes.
- 혼동 경계: one broken bulb proves flicker; noise alone.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S21](SOURCES.md#s21); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_chiaroscuro_shape — 키아로스쿠로 — Chiaroscuro
키아로스쿠로는 명암을 통한 형태 조직이며 무조건 어두운 화면이 아니다.
- 반영 구분: visual; 원본 슬롯 제안: lighting.
- 관찰 구성: bright and dark planes articulate one three-dimensional form / the lit-to-shadow boundary follows the form.
- 관계: bright and dark planes articulate one three-dimensional form → jointly_visible_in_same_event → the lit-to-shadow boundary follows the form.
- 혼동 경계: black overlay; high contrast without shape continuity.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S21](SOURCES.md#s21); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

## 절 13

### hvr_negative_space_reserved_region — 네거티브 스페이스 — Negative space
주요 대상 옆의 빈 영역을 공간 기능이 읽히는 상태로 남긴다.
- 반영 구분: reuse; 원본 슬롯 제안: composition.
- 관찰 구성: one focal adult occupies a limited frame region / an adjacent empty route occupies substantial visible space.
- 관계: one focal adult occupies a limited frame region → jointly_visible_in_same_event → an adjacent empty route occupies substantial visible space.
- 혼동 경계: blank canvas without scene; emptiness itself proves threat.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_offscreen_reaction_vector — 화면 밖 공간 — Off-screen space
프레임 밖 공간은 인물의 시선 방향과 경계 근처 반응으로 제한해서 암시한다.
- 반영 구분: visual; 원본 슬롯 제안: gaze_target.
- 관찰 구성: one adult's eyes and head orient beyond the same frame edge / visible room geometry continues toward that edge.
- 관계: one adult's eyes and head orient beyond the same frame edge → jointly_visible_in_same_event → visible room geometry continues toward that edge.
- 혼동 경계: monster automatically added; claim of exact unseen identity.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_frame_within_threshold — 프레임 속 프레임 — Frame within a frame
문 창 거울 테두리가 대상 둘레의 두 번째 경계를 만든다.
- 반영 구분: reuse; 원본 슬롯 제안: composition.
- 관찰 구성: a doorway or window frame encloses one adult / the outer photograph frame remains separately readable.
- 관계: a doorway or window frame encloses one adult → jointly_visible_in_same_event → the outer photograph frame remains separately readable.
- 혼동 경계: random rectangle; cropped frame missing enclosure.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_foreground_occluded_view — 전경 가림 — Foreground occlusion
가까운 물체가 중요한 영역을 부분 차단하되 비교 증거는 남긴다.
- 반영 구분: visual; 원본 슬롯 제안: composition.
- 관찰 구성: a near object occludes one side of the scene / a focal adult remains partly visible behind it.
- 관계: a near object occludes one side of the scene → jointly_visible_in_same_event → a focal adult remains partly visible behind it.
- 혼동 경계: full evidence occlusion scored as pass; decorative vignette.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_dutch_camera_roll — 더치 앵글 — Dutch angle
더치 앵글은 카메라 롤에 따른 기울어진 수평이다.
- 반영 구분: reuse; 원본 슬롯 제안: camera_direction.
- 관찰 구성: normally vertical walls tilt consistently in the image plane / the scene geometry remains internally continuous.
- 관계: normally vertical walls tilt consistently in the image plane → jointly_visible_in_same_event → the scene geometry remains internally continuous.
- 혼동 경계: tilted building alone; wrong perspective; guaranteed panic.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_low_angle_height — 로우 앵글 — Low angle
카메라가 대상보다 낮아 위로 향하는 관계이며 거대한 대상 자체와 다르다.
- 반영 구분: reuse; 원본 슬롯 제안: camera_height.
- 관찰 구성: undersides of the focal structure remain visible / the perspective viewpoint sits below the subject.
- 관계: undersides of the focal structure remain visible → jointly_visible_in_same_event → the perspective viewpoint sits below the subject.
- 혼동 경계: head tilted up only; long legs prove low angle.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_high_angle_height — 하이 앵글 — High angle
카메라가 대상보다 높은 관계이며 위쪽 광원과 다르다.
- 반영 구분: reuse; 원본 슬롯 제안: camera_height.
- 관찰 구성: upper surfaces and surrounding floor remain visible / the viewpoint looks down on the focal subject.
- 관계: upper surfaces and surrounding floor remain visible → jointly_visible_in_same_event → the viewpoint looks down on the focal subject.
- 혼동 경계: top lighting; overhead crop without relational context.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_wide_close_distance — 광각 근접 촬영
근접 광각의 가까운 부위와 먼 부위 크기 차이를 비교한다.
- 반영 구분: visual; 원본 슬롯 제안: lens.
- 관찰 구성: a near hand or face plane appears enlarged / far body and room planes recede coherently.
- 관계: a near hand or face plane appears enlarged → jointly_visible_in_same_event → far body and room planes recede coherently.
- 혼동 경계: focal length guessed from metadata; malformed body.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_deep_focus_dual_evidence — 딥 포커스 — Deep focus
전후경을 동시에 읽을 수 있는 선명도와 깊은 배치 자체를 구분한다.
- 반영 구분: reuse; 원본 슬롯 제안: focus.
- 관찰 구성: foreground adult features remain readable / a separate background anomaly also remains sharply identifiable.
- 관계: foreground adult features remain readable → jointly_visible_in_same_event → a separate background anomaly also remains sharply identifiable.
- 혼동 경계: deep staging but blurred back; exposure artifacts.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_shallow_focus_unresolved_back — 얕은 심도 — Shallow depth of field
제한된 거리만 선명하므로 배경 이상을 hard gate로 요구하면 충돌한다.
- 반영 구분: reuse; 원본 슬롯 제안: focus.
- 관찰 구성: one selected focal plane stays sharp / background forms remain softly unresolved.
- 관계: one selected focal plane stays sharp → jointly_visible_in_same_event → background forms remain softly unresolved.
- 혼동 경계: blurred whole picture; hidden background gate passed.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_rack_focus_transition — 랙 포커스 — Rack focus
촬영 중 선명도 중심이 이동하는 시간 과정이다.
- 반영 구분: temporal; 원본 슬롯 제안: focus.
- 관찰 구성: foreground focus becomes soft across the sequence / background focus becomes sharp in the same continuous shot.
- 관계: foreground focus becomes soft across the sequence → jointly_visible_in_same_event → background focus becomes sharp in the same continuous shot.
- 혼동 경계: one deep-focus still; split-focus still proves rack.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_pov_declared_owner — POV 숏 — Point-of-view shot
누구의 시점인지 요청에서 선언하고 시점 자체로 관찰자의 악의를 추론하지 않는다.
- 반영 구분: visual; 원본 슬롯 제안: apparatus_pov.
- 관찰 구성: a declared adult viewpoint aligns with visible foreground hands or apparatus / the watched region follows that viewing direction.
- 관계: a declared adult viewpoint aligns with visible foreground hands or apparatus → jointly_visible_in_same_event → the watched region follows that viewing direction.
- 혼동 경계: all POV predatory; unnamed camera proves a ghost.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_long_take_duration — 롱테이크 — Long take
컷 없는 지속은 영상 편집 단위로 보존한다.
- 반영 구분: temporal; 원본 슬롯 제안: capture_context.
- 관찰 구성: continuous spatial and action evidence spans a declared shot duration.
- 관계: continuous spatial and action evidence spans a declared shot duration → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: one photo is a long take; panoramic width proves time.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S27](SOURCES.md#s27); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_jump_cut_discontinuity — 점프 컷 — Jump cut
편집의 도약과 순간이동 설정을 구분한다.
- 반영 구분: temporal; 원본 슬롯 제안: narrative_phase.
- 관찰 구성: ordered shots keep the same scene anchor / position or action changes across a visible edit boundary.
- 관계: ordered shots keep the same scene anchor → jointly_visible_in_same_event → position or action changes across a visible edit boundary.
- 혼동 경계: single afterimage; glitch effect proves cut.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S27](SOURCES.md#s27); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

## 절 14

### hvr_diegetic_source_axis — 디제틱 사운드 — Diegetic sound
이야기 세계 안 발생원이라는 축이며 화면 안 밖과 독립이다.
- 반영 구분: audio; 원본 슬롯 제안: sensory_focus.
- 관찰 구성: a story-world sound source is explicitly identified / the audible event belongs to that world.
- 관계: a story-world sound source is explicitly identified → jointly_visible_in_same_event → the audible event belongs to that world.
- 혼동 경계: offscreen automatically non-diegetic; visible radio proves sound heard.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S25](SOURCES.md#s25); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_non_diegetic_source_axis — 비디제틱 사운드 — Non-diegetic sound
세계 밖 음악 내레이션이라는 축이며 공간 밖 발생원과 다르다.
- 반영 구분: audio; 원본 슬롯 제안: sensory_focus.
- 관찰 구성: a soundtrack layer is assigned outside the story world's sources.
- 관계: a soundtrack layer is assigned outside the story world's sources → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: offscreen footsteps automatically soundtrack music.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S25](SOURCES.md#s25); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_offscreen_sound_position — 화면 밖 소리 — Off-screen sound
발생원이 프레임 밖에 있다는 공간 축이다.
- 반영 구분: audio; 원본 슬롯 제안: sensory_focus.
- 관찰 구성: audio places a source outside the visible frame / the sound can still belong inside the story world.
- 관계: audio places a source outside the visible frame → jointly_visible_in_same_event → the sound can still belong inside the story world.
- 혼동 경계: invisible source equals imaginary or non-diegetic.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S25](SOURCES.md#s25); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_sound_perspective_distance — 사운드 퍼스펙티브 — Sound perspective
음량 음색 반향의 거리 표현을 시각 거리와 대조한다.
- 반영 구분: audio; 원본 슬롯 제안: sensory_focus.
- 관찰 구성: one source changes audible distance cues / the scene retains its visible distance reference.
- 관계: one source changes audible distance cues → jointly_visible_in_same_event → the scene retains its visible distance reference.
- 혼동 경계: loud always near; perspective proved by still.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S25](SOURCES.md#s25); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_drone_sustained_layer — 드론 — Drone
길게 지속되는 음층은 지속 시간과 음원 배치를 기록한다.
- 반영 구분: audio; 원본 슬롯 제안: sensory_focus.
- 관찰 구성: a sustained tonal or noise layer remains present across a declared interval.
- 관계: a sustained tonal or noise layer remains present across a declared interval → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: drone aircraft; particular frequency inevitably fear.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S28](SOURCES.md#s28); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_dissonance_interval — 불협화 — Dissonance
음 사이 관계의 불안정성을 음악 조건으로 관리한다.
- 반영 구분: audio; 원본 슬롯 제안: sensory_focus.
- 관찰 구성: simultaneous or sequential tones form a declared unstable interval relation.
- 관계: simultaneous or sequential tones form a declared unstable interval relation → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: large volume equals dissonance; visual red color proves sound.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S28](SOURCES.md#s28); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_tone_cluster_density — 음군 — Tone cluster
가까운 음을 밀집시키는 음악적 구조다.
- 반영 구분: audio; 원본 슬롯 제안: sensory_focus.
- 관찰 구성: multiple adjacent pitches form one dense audible group.
- 관계: multiple adjacent pitches form one dense audible group → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: random noise; single low tone.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S28](SOURCES.md#s28); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_glissando_pitch_path — 글리산도 — Glissando
음높이가 미끄러지는 경로와 방향을 시간으로 확인한다.
- 반영 구분: audio; 원본 슬롯 제안: sensory_focus.
- 관찰 구성: pitch moves along a continuous or rapid stepped path / the interval spans a declared time.
- 관계: pitch moves along a continuous or rapid stepped path → jointly_visible_in_same_event → the interval spans a declared time.
- 혼동 경계: one fixed tone; image smear proves glissando.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S28](SOURCES.md#s28); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_ostinato_repeat_break — 오스티나토 — Ostinato
짧은 음형 반복과 끊김의 시간 관계다.
- 반영 구분: audio; 원본 슬롯 제안: sensory_focus.
- 관찰 구성: one audible pattern repeats across several cycles / one specified cycle breaks that pattern.
- 관계: one audible pattern repeats across several cycles → jointly_visible_in_same_event → one specified cycle breaks that pattern.
- 혼동 경계: any looping picture; no recorded duration.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S28](SOURCES.md#s28); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_stinger_event_sync — 스팅어 — Stinger
짧은 음향 타격을 시각 사건의 시간 위치와 결합한다.
- 반영 구분: audio; 원본 슬롯 제안: narrative_phase.
- 관찰 구성: a short sound accent has a defined onset / its onset aligns with or deliberately offsets a visible event.
- 관계: a short sound accent has a defined onset → jointly_visible_in_same_event → its onset aligns with or deliberately offsets a visible event.
- 혼동 경계: one loud track; still image proves synchronized startle.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S28](SOURCES.md#s28); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_signature_sound_identity — 시그니처 사운드 — Signature sound
존재를 식별하는 음향은 앞선 노출과 같은 소리의 재등장을 필요로 한다.
- 반영 구분: audio; 원본 슬롯 제안: sensory_focus.
- 관찰 구성: one sound pattern is bound to one declared entity / that pattern recurs before or during its appearance.
- 관계: one sound pattern is bound to one declared entity → jointly_visible_in_same_event → that pattern recurs before or during its appearance.
- 혼동 경계: any eerie noise; one occurrence proves learned identity.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S28](SOURCES.md#s28); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_pitch_bend_dynamic — 피치 벤드 — Pitch bend
피치 변조 범위와 시간 경로를 음향 데이터에 보존한다.
- 반영 구분: audio; 원본 슬롯 제안: sensory_focus.
- 관찰 구성: a voice or instrument's fundamental pitch follows a declared bend curve.
- 관계: a voice or instrument's fundamental pitch follows a declared bend curve → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: ordinary loudness change; frequency guaranteed hallucination.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S28](SOURCES.md#s28); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_distortion_audio_domain — 왜곡 — Distortion
음색 왜곡과 영상 노이즈의 매체 영역을 분리한다.
- 반영 구분: audio; 원본 슬롯 제안: sensory_focus.
- 관찰 구성: a recorded sound gains nonlinear or roughened timbre / the unprocessed source remains available for comparison.
- 관계: a recorded sound gains nonlinear or roughened timbre → jointly_visible_in_same_event → the unprocessed source remains available for comparison.
- 혼동 경계: lens distortion; bitmap glitch; one screenshot proves timbre.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S28](SOURCES.md#s28); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_convolution_response — 컨볼루션 — Convolution
응답 특성과 음원을 결합하는 처리이며 이미지 질감과 직접 동일하지 않다.
- 반영 구분: audio; 원본 슬롯 제안: sensory_focus.
- 관찰 구성: a sound source is processed using a declared impulse response / the processed result is compared with the original.
- 관계: a sound source is processed using a declared impulse response → jointly_visible_in_same_event → the processed result is compared with the original.
- 혼동 경계: any echo equals convolution; image proves exact algorithm.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S28](SOURCES.md#s28); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_lip_audio_mismatch — 소리와 입 모양의 불일치
입술과 소리 시간 불일치는 동기화된 영상 음향으로 검증한다.
- 반영 구분: audio; 원본 슬롯 제안: relational_action.
- 관찰 구성: visible lip events and audible syllables have a declared offset / one speaker remains identifiable across the sequence.
- 관계: visible lip events and audible syllables have a declared offset → jointly_visible_in_same_event → one speaker remains identifiable across the sequence.
- 혼동 경계: mouth shape in one image proves mismatch.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S25](SOURCES.md#s25); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_sound_image_contrast — 음향적 대비
평온한 음향과 위협 장면의 대비는 두 매체의 실제 증거를 필요로 한다.
- 반영 구분: audio; 원본 슬롯 제안: concept_tension.
- 관찰 구성: a benign lullaby or routine announcement plays / a concurrent visible threat supplies the contrasting image.
- 관계: a benign lullaby or routine announcement plays → jointly_visible_in_same_event → a concurrent visible threat supplies the contrasting image.
- 혼동 경계: music box appearance proves its soundtrack; all lullabies sinister.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S25](SOURCES.md#s25), [S28](SOURCES.md#s28); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

## 절 15

### hvr_talisman_bridge_seam — 부적·봉인문
보호 부적과 봉인의 실제 배치 방향을 문화 판본에 맞춘다.
- 반영 구분: visual; 원본 슬롯 제안: prop_direction.
- 관찰 구성: a chosen talisman bridges a closed doorway seam / a local tear changes that same boundary.
- 관계: a chosen talisman bridges a closed doorway seam → jointly_visible_in_same_event → a local tear changes that same boundary.
- 혼동 경계: generic symbols as authentic writing; every talisman threatens.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S26](SOURCES.md#s26); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_ritual_boundary_crossing — 경계선·금줄·원형 문양
금줄 원형 선의 경계를 실제 이동과 연결하되 전승별 의미를 구분한다.
- 반영 구분: visual; 원본 슬롯 제안: prop_direction.
- 관찰 구성: one specified boundary material encircles a readable zone / a single crossing interrupts the boundary.
- 관계: one specified boundary material encircles a readable zone → jointly_visible_in_same_event → a single crossing interrupts the boundary.
- 혼동 경계: all cultures share magic circle; ordinary safety cordon as sacred.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S09](SOURCES.md#s09), [S26](SOURCES.md#s26); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_bell_displaced_clapper — 의식용 종
종의 소리는 못 보여도 타종 상태와 접촉 부재의 한 순간은 보인다.
- 반영 구분: visual; 원본 슬롯 제안: prop.
- 관찰 구성: a ritual bell has a displaced visible clapper / nearby hands remain away from the bell.
- 관계: a ritual bell has a displaced visible clapper → jointly_visible_in_same_event → nearby hands remain away from the bell.
- 혼동 경계: still proves ringing duration; every bell summons ghosts.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S25](SOURCES.md#s25); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_smoke_bounded_deflection — 향과 연기
연기는 공기의 경로를 시각화하지만 초자연 원인은 설정으로 한정한다.
- 반영 구분: visual; 원본 슬롯 제안: surreal_physics_detail.
- 관찰 구성: one smoke stream bends around a sharply bounded empty region / the source and surrounding stream remain continuous.
- 관계: one smoke stream bends around a sharply bounded empty region → jointly_visible_in_same_event → the source and surrounding stream remain continuous.
- 혼동 경계: fog anywhere; disconnected smoke person.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S21](SOURCES.md#s21); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_wax_elapsed_material — 촛농
촛농은 물질 축적이며 경과 시간의 정확한 양은 독립 기록이 필요하다.
- 반영 구분: visual; 원본 슬롯 제안: texture.
- 관찰 구성: thick wax layers accumulate below one candle / the remaining candle is visibly short.
- 관계: thick wax layers accumulate below one candle → jointly_visible_in_same_event → the remaining candle is visibly short.
- 혼동 경계: wax volume proves exact minutes; unrelated candle pile.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S21](SOURCES.md#s21); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_mirror_shared_geometry — 거울
거울은 실제 반사 기하 기준을 먼저 확보하고 이상을 한 관계에 국한한다.
- 반영 구분: reuse; 원본 슬롯 제안: reflection_logic.
- 관찰 구성: a visible mirror plane aligns room landmarks / one chosen reflected feature differs from its physical counterpart.
- 관계: a visible mirror plane aligns room landmarks → jointly_visible_in_same_event → one chosen reflected feature differs from its physical counterpart.
- 혼동 경계: convex reflection difference; extra crop-hidden people.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_doll_gaze_relation — 인형
인형의 물체 구조와 눈의 방향을 주변 대상과 연결한다.
- 반영 구분: visual; 원본 슬롯 제안: gaze_target.
- 관찰 구성: a doll retains visible rigid material joints / its eyes orient toward one named adult position.
- 관계: a doll retains visible rigid material joints → jointly_visible_in_same_event → its eyes orient toward one named adult position.
- 혼동 경계: ordinary toy portrait proves sentience; gaze movement from a still.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S02](SOURCES.md#s02); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_mannequin_population_difference — 마네킹·밀랍 인형
마네킹 집단의 반복과 한 인물의 재질 차이를 읽게 한다.
- 반영 구분: visual; 원본 슬롯 제안: subject.
- 관찰 구성: rigid mannequins repeat a shared pose / one adult figure among them has distinct skin and garment response.
- 관계: rigid mannequins repeat a shared pose → jointly_visible_in_same_event → one adult figure among them has distinct skin and garment response.
- 혼동 경계: all figures actual humans; waxlike finish alone proves life.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S02](SOURCES.md#s02); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_mask_face_layer — 가면
가면 표면과 그 아래 얼굴을 별도 층으로 보여준다.
- 반영 구분: visual; 원본 슬롯 제안: prop_direction.
- 관찰 구성: one mask edge visibly lifts from an adult face / the underlying facial surface remains distinct.
- 관계: one mask edge visibly lifts from an adult face → jointly_visible_in_same_event → the underlying facial surface remains distinct.
- 혼동 경계: face paint; seamless face implies actual mask layer.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S02](SOURCES.md#s02); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_automaton_drive_trace — 오르골·자동 장난감
자동 장난감의 구동 구조를 보여주며 현재 소리는 별도다.
- 반영 구분: visual; 원본 슬롯 제안: prop.
- 관찰 구성: one wound mechanism connects to the toy's moving part / its visible linkage explains an ordinary operation baseline.
- 관계: one wound mechanism connects to the toy's moving part → jointly_visible_in_same_event → its visible linkage explains an ordinary operation baseline.
- 혼동 경계: all self-moving toys supernatural; still proves motion after music ends.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_portrait_identity_discrepancy — 초상화·가족사진
현재 인물과 기록 얼굴의 정체 비교와 불일치 부위를 나눈다.
- 반영 구분: visual; 원본 슬롯 제안: reflection_logic.
- 관찰 구성: a present adult shares one distinctive identity cue with a nearby portrait / one local feature differs inside the portrait.
- 관계: a present adult shares one distinctive identity cue with a nearby portrait → jointly_visible_in_same_event → one local feature differs inside the portrait.
- 혼동 경계: two unrelated people; faded paper itself proves curse.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_diary_present_record — 일기·관찰 기록
과거 기록과 현재 상황의 대응은 읽히는 간단한 그림이나 배치를 쓴다.
- 반영 구분: visual; 원본 슬롯 제안: prop.
- 관찰 구성: an open fictional diary contains a simple room diagram / the current room matches the diagram / one newly present object appears in both.
- 관계: an open fictional diary contains a simple room diagram → jointly_visible_in_same_event → the current room matches the diagram and one newly present object appears in both.
- 혼동 경계: dense invented prose; handwriting proves prophecy.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_roster_countable_gap — 명부·번호표
명부 번호표는 문자 성공과 관계 성공을 별도 판정한다.
- 반영 구분: visual; 원본 슬롯 제안: prop.
- 관찰 구성: a fictional roster has a countable sequence of slots / one visibly filled slot corresponds to an otherwise absent occupant.
- 관계: a fictional roster has a countable sequence of slots → jointly_visible_in_same_event → one visibly filled slot corresponds to an otherwise absent occupant.
- 혼동 경계: illegible names; precise text fidelity assumed.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_recording_local_discrepancy — 낡은 녹화물
현재 장소와 기록 화면의 국소 차이를 한 프레임에서 비교한다.
- 반영 구분: visual; 원본 슬롯 제안: frame_anchor_medium.
- 관찰 구성: one physical room remains beside its recording display / a distinct extra presence occupies only the display.
- 관계: room recording → depicts_additional_presence_beyond → corresponding physical room.
- 혼동 경계: generic noise; different camera angle explains difference.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S08](SOURCES.md#s08), [S32](SOURCES.md#s32); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_warning_rule_visual_context — 안내문·경고문
경고문은 규칙 문맥이며 실제 문자는 최소한으로 분리 검증한다.
- 반영 구분: visual; 원본 슬롯 제안: prop.
- 관찰 구성: an unbranded warning panel stands beside a matching physical boundary / a simple pictogram contradicts the visible route.
- 관계: an unbranded warning panel stands beside a matching physical boundary → jointly_visible_in_same_event → a simple pictogram contradicts the visible route.
- 혼동 경계: long text automatically correct; real emergency authority impersonation.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S32](SOURCES.md#s32); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_body_trace_wrong_location — 머리카락·치아·손톱
몸의 흔적은 양과 위치를 생활 기준과 대조한다.
- 반영 구분: visual; 원본 슬롯 제안: aftermath_trace.
- 관찰 구성: a small clump of hair or tooth-like props occupies an unexpected sealed compartment / the compartment and trace remain separately readable.
- 관계: a small clump of hair or tooth-like props occupies an unexpected sealed compartment → jointly_visible_in_same_event → the compartment and trace remain separately readable.
- 혼동 경계: every hair implies violence; forensic certainty.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_wreath_fresh_decay_contrast — 시든 꽃·마른 화환
애도 물건의 신선도와 공간의 오래된 상태를 대비한다.
- 반영 구분: visual; 원본 슬롯 제안: prop.
- 관찰 구성: one fresh floral wreath sits against a long-decayed wall / fresh petals differ visibly from nearby dried flowers.
- 관계: one fresh floral wreath sits against a long-decayed wall → jointly_visible_in_same_event → fresh petals differ visibly from nearby dried flowers.
- 혼동 경계: all flowers funeral; timeline derived from one species.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S21](SOURCES.md#s21); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_corrosion_used_touch_zone — 녹·부식·벗겨진 도장
오랜 부식과 최근 손 접촉으로 닦인 영역을 국소 비교한다.
- 반영 구분: visual; 원본 슬롯 제안: texture.
- 관찰 구성: rust and flaking paint cover a metal handle surround / the exact grip zone remains polished and clean.
- 관계: rust and flaking paint cover a metal handle surround → jointly_visible_in_same_event → the exact grip zone remains polished and clean.
- 혼동 경계: all surfaces uniformly grungy; no specific use trace.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S21](SOURCES.md#s21); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_fungal_boundary_spread — 곰팡이·균사·점액
곰팡이 균사 점액을 각 구조로 구별하고 경계 침범으로 설계한다.
- 반영 구분: visual; 원본 슬롯 제안: texture.
- 관찰 구성: threadlike fungal growth crosses a wall seam / wet translucent residue collects below that seam.
- 관계: threadlike fungal growth crosses a wall seam → jointly_visible_in_same_event → wet translucent residue collects below that seam.
- 혼동 경계: rust as fungus; mold diagnoses environment or health.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S21](SOURCES.md#s21); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_dust_removed_silhouette — 먼지와 지워진 자국
먼지가 지워진 윤곽과 주변 쌓인 층을 동시에 보인다.
- 반영 구분: visual; 원본 슬롯 제안: aftermath_trace.
- 관찰 구성: settled dust covers an otherwise intact surface / one human-shaped clean region interrupts the dust / its boundary remains sharply readable.
- 관계: clean human-shaped region → locally_interrupts → settled dust field.
- 혼동 경계: painted silhouette; random missing texture; origin proven.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

## 절 16

### hvr_jump_scare_event — 점프 스케어 — Jump scare
갑작스러움은 이전 상태와 등장 또는 음향의 전환을 필요로 한다.
- 반영 구분: temporal; 원본 슬롯 제안: narrative_phase.
- 관찰 구성: an established quiet frame precedes an abrupt entity reveal / audio onset is recorded separately if used.
- 관계: an established quiet frame precedes an abrupt entity reveal → jointly_visible_in_same_event → audio onset is recorded separately if used.
- 혼동 경계: large face in one still guarantees startle.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S27](SOURCES.md#s27), [S25](SOURCES.md#s25); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_slow_burn_accumulation — 슬로 번 — Slow burn
작은 이상 축적은 순서와 이전 설명의 실패를 기록한다.
- 반영 구분: temporal; 원본 슬롯 제안: narrative_phase.
- 관찰 구성: ordered scenes retain one stable baseline / successive bounded anomalies accumulate.
- 관계: ordered scenes retain one stable baseline → jointly_visible_in_same_event → successive bounded anomalies accumulate.
- 혼동 경계: one dark photograph proves pacing; more props equals slow burn.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01), [S27](SOURCES.md#s27); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_incomplete_witness_fragment — 불완전한 목격
목격자의 위치와 가려진 결정 정보를 함께 보인다.
- 반영 구분: visual; 원본 슬롯 제안: composition.
- 관찰 구성: one adult witness has a restricted sightline / a foreground structure hides the decisive part of the event.
- 관계: one adult witness has a restricted sightline → jointly_visible_in_same_event → a foreground structure hides the decisive part of the event.
- 혼동 경계: all blur means mystery; witness history proven from single pose.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S07](SOURCES.md#s07), [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_unreliable_narrator_context — 신뢰할 수 없는 화자
기억 진술과 사건의 신뢰성은 서사 근거이며 얼굴로 확정하지 않는다.
- 반영 구분: context; 원본 슬롯 제안: narrative_core.
- 관찰 구성: a declared narrator account is compared against independently supplied event evidence.
- 관계: a declared narrator account is compared against independently supplied event evidence → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: unusual expression proves liar; mental illness stereotype.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_dramatic_irony_unseen_back — 극적 아이러니 — Dramatic irony
관객에게 읽히는 위협과 인물이 보지 못하는 시선 관계를 만든다.
- 반영 구분: visual; 원본 슬롯 제안: composition.
- 관찰 구성: a clearly visible background presence lies behind an adult / that adult's gaze remains directed elsewhere / both are readable in one frame.
- 관계: a clearly visible background presence lies behind an adult → jointly_visible_in_same_event → that adult's gaze remains directed elsewhere and both are readable in one frame.
- 혼동 경계: blurred threat; a still proves all character knowledge.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_red_herring_context — 거짓 단서 — Red herring
거짓 단서는 최종 사건과 관계를 가진 서사 기능으로 보존한다.
- 반영 구분: context; 원본 슬롯 제안: narrative_core.
- 관찰 구성: a declared clue receives attention before an independent later explanation.
- 관계: a declared clue receives attention before an independent later explanation → jointly_visible_in_same_event → the declared comparison context.
- 혼동 경계: random suspicious prop proves a red herring.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S07](SOURCES.md#s07); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_safe_boundary_failure — 안전지대의 붕괴
안전 장치가 실제 닫힘 기능을 잃는 부위를 보여준다.
- 반영 구분: visual; 원본 슬롯 제안: concept_tension.
- 관찰 구성: one recognizable protective barrier remains mostly intact / a localized breach connects the protected and threatened zones.
- 관계: one recognizable protective barrier remains mostly intact → jointly_visible_in_same_event → a localized breach connects the protected and threatened zones.
- 혼동 경계: religious motif intrinsically dangerous; boundary not visibly broken.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01), [S26](SOURCES.md#s26); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_returning_past_identity — 돌아오는 과거
과거 인물 물건의 정체가 현재 공간에 이어지는 관계다.
- 반영 구분: reuse; 원본 슬롯 제안: concept_tension.
- 관찰 구성: one old identity-linked object corresponds to a present apparition / current room use remains clearly contemporary.
- 관계: one old identity-linked object corresponds to a present apparition → jointly_visible_in_same_event → current room use remains clearly contemporary.
- 혼동 경계: sepia filter; anonymous antique collection.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_forbidden_knowledge_context — 금지된 지식
지식 획득의 위험은 설정으로 보존하고 읽는 행위와 결과를 선택형으로 연결한다.
- 반영 구분: visual; 원본 슬롯 제안: prop_direction.
- 관찰 구성: an adult reads one opened fictional diagram / a bounded nearby anomaly repeats a shape from that diagram.
- 관계: an adult reads one opened fictional diagram → jointly_visible_in_same_event → a bounded nearby anomaly repeats a shape from that diagram.
- 혼동 경계: any book cursed; invented text proves historical ritual.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S04](SOURCES.md#s04); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_rule_change_record — 위협의 규칙 변경
규칙 변경과 이전 이해 실패는 전후 조건을 분리해야 한다.
- 반영 구분: temporal; 원본 슬롯 제안: narrative_phase.
- 관찰 구성: one demonstrated response works in an earlier event / the same response fails after one declared condition changes.
- 관계: one demonstrated response works in an earlier event → jointly_visible_in_same_event → the same response fails after one declared condition changes.
- 혼동 경계: two arbitrary snapshots; ordinary wrong sign proves rules changed.
- 정지 이미지 증거: NO_DIRECT_STILL_IMAGE_PROOF; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S27](SOURCES.md#s27); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_false_escape_repeated_marker — 탈출의 위장
다른 출구 풍경에 같은 고유 표식이 반복되는 공간 불일치다.
- 반영 구분: visual; 원본 슬롯 제안: surreal_physics_detail.
- 관찰 구성: two apparently distinct exits share one unusual damaged marker / continuous surrounding geometry supports the comparison.
- 관계: two apparently distinct exits share one unusual damaged marker → jointly_visible_in_same_event → continuous surrounding geometry supports the comparison.
- 혼동 경계: standard exit signs repeated normally; still proves traversal loop.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_lingering_end_trace — 여운형 결말
사건 뒤 남은 흔적의 한 순간을 다루며 결말 순서는 별도 서사다.
- 반영 구분: visual; 원본 슬롯 제안: aftermath_trace.
- 관찰 구성: an apparently restored room retains one identity-linked abnormal mark / ordinary use has resumed around it.
- 관계: an apparently restored room retains one identity-linked abnormal mark → jointly_visible_in_same_event → ordinary use has resumed around it.
- 혼동 경계: generic dirt; one still establishes story ending.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

## 절 17

### hvr_bundle_korean_threshold_trace — 한국적 원귀 분위기
원귀 분위기 조합은 한국 목조 복도 젖은 천 새벽빛 국소 흔적의 선택형 구성이다.
- 반영 구분: bundle; 원본 슬롯 제안: situation_context.
- 관찰 구성: one timber corridor preserves readable joinery / a damp white cloth remains tied to one apparition / one wet handprint sits above its corresponding doorway.
- 관계: one timber corridor preserves readable joinery → jointly_visible_in_same_event → a damp white cloth remains tied to one apparition and one wet handprint sits above its corresponding doorway.
- 혼동 경계: Japanese costume blended as Korean canon; sound scored in still.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S01](SOURCES.md#s01), [S11](SOURCES.md#s11), [S21](SOURCES.md#s21); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_bundle_clean_cctv_difference — 현대 일상 속 언캐니
깨끗한 편의점과 CCTV 속 추가 인물을 함께 비교하는 조합이다.
- 반영 구분: bundle; 원본 슬롯 제안: reflection_logic.
- 관찰 구성: a clean shop retains even practical lighting / physical aisle occupancy is readable / its live CCTV pane contains one additional adult figure.
- 관계: a clean shop retains even practical lighting → jointly_visible_in_same_event → physical aisle occupancy is readable and its live CCTV pane contains one additional adult figure.
- 혼동 경계: camera blind spot explains extra person; VHS noise substitute.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S22](SOURCES.md#s22), [S32](SOURCES.md#s32); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_bundle_bright_folk_boundary — 밝은 포크 호러
꽃 들판 주민 방문자 자리 규칙은 밝은 공동체 경계의 선택형 조합이다.
- 반영 구분: bundle; 원본 슬롯 제안: relational_action.
- 관찰 구성: bright field and flowers retain visible detail / adult residents share a directional seating pattern / one adult visitor conflicts with that pattern.
- 관계: bright field and flowers retain visible detail → jointly_visible_in_same_event → adult residents share a directional seating pattern and one adult visitor conflicts with that pattern.
- 혼동 경계: all rural festivals malicious; flower costume as mandatory tradition.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S03](SOURCES.md#s03), [S21](SOURCES.md#s21); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_bundle_analog_instruction_gap — 아날로그·기록물 공포
정상 안내 형식 안의 이상 규칙은 허구 방송 매체 조합이다.
- 반영 구분: bundle; 원본 슬롯 제안: frame_anchor_medium.
- 관찰 구성: one fictional broadcast layout remains stable / one simple warning pictogram contradicts another / signal distortion stays local to the display.
- 관계: one fictional broadcast layout remains stable → jointly_visible_in_same_event → one simple warning pictogram contradicts another and signal distortion stays local to the display.
- 혼동 경계: copy a real warning authority; all static noise proves anomaly.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S32](SOURCES.md#s32), [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_bundle_cosmic_water_mismatch — 코즈믹·심해 공포
작은 관찰자 수면 하늘 반사 불일치의 조합이다.
- 반영 구분: bundle; 원본 슬롯 제안: surreal_physics_detail.
- 관찰 구성: a small adult provides scale at a wide shoreline / the visible sky pattern differs from its aligned water reflection / ordinary shore reflections remain coherent.
- 관계: a small adult provides scale at a wide shoreline → jointly_visible_in_same_event → the visible sky pattern differs from its aligned water reflection and ordinary shore reflections remain coherent.
- 혼동 경계: water ripples explain mismatch; huge tentacles forced.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S04](SOURCES.md#s04), [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.

### hvr_bundle_body_industrial_junction — 바디·산업 호러
유기 신체와 배선의 접합을 산업 공간의 물성과 연결한다.
- 반영 구분: bundle; 원본 슬롯 제안: anatomical_connection.
- 관찰 구성: one adult fictional body has a visible organic-to-cable junction / cable routing connects to nearby hardware / monochrome material contrasts retain the join.
- 관계: one adult fictional body has a visible organic-to-cable junction → jointly_visible_in_same_event → cable routing connects to nearby hardware and monochrome material contrasts retain the join.
- 혼동 경계: wire necklace; medical impairment equated with monstrosity.
- 정지 이미지 증거: PROPOSED_NOT_RENDERED; 전부 보일 때만 판정하고 가림은 UNOBSERVABLE_NOT_PASS.
- 근거 범위: [S05](SOURCES.md#s05), [S22](SOURCES.md#s22); SOURCE_FRAMEWORK_PARTIAL_ONLY. 전체 seed 사실 검증은 아님.
