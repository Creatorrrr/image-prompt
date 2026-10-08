# 염색·표면 상태·캐릭터 헤어 의미 연구

기준일: 2026-10-08 Asia/Seoul. 담당: hair_color_state. 작업 범위는 리서치와 반영 계획이다.

독립 의미 카드 55장, 최소 대조쌍 12개, 담당 원본 키워드 179개의 disposition을 작성했다. 일차 출처 레코드 14개는 현재 본문 또는 공식 위키 API로 확인했고, legacy 검색 본문 3개는 직접 본문과 접근 상태가 달라 조건부 참고로 남겼다. Danbooru 출처 레코드는 별도 URL이 있는 위키 정의문서 49개를 묶은 것이므로 출처 레코드 수와 개별 페이지 수를 혼동하면 안 된다.

원본 키워드의 범위 확인과 각각의 의미 검증은 별개다. H001–H454와 R01–R48은 root가 원본 UI에서 확인하고 전사했지만, 원본 Markdown/JSON 다운로드 bytes는 확보하지 못했다. 이 담당 연구에서는 H235–H385, H427–H454의 179개를 다루었고, 그중 66개에 이름 또는 직접 대응 정의의 일차 확인 표시를 붙였다. 나머지는 일반 색 축으로 분해한 제안, 관련 modifier, 비시각 개념 또는 출처 재확인 대상으로 구분했다.

런타임 assets·코드·index는 수정하지 않았다. 검색 순위, 실제 hard activation, 후보 선택, 이미지 생성, native pixels, 사용자 수용 검증을 실행하지 않았다.

## 파일과 증거 경계

- [의미 카드·대조쌍·179개 disposition](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-20261008/color-state-cards.json)
- [출처 레코드·지원 주장·접근 상태](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-20261008/color-state-sources.json)
- [원본 454개 키워드 전사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-20261008/reference/keyword-inventory.tsv)
- [원본 48개 연출 조합 전사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-20261008/reference/character-combinations.tsv)
- [현행 작성 데이터 조사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-20261008/CURRENT-DATA-AUDIT.json)
- [현행 키워드 crosswalk](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-20261008/KEYWORD-CROSSWALK.json)

각 카드는 labels/aliases/namespace/domain, 정의, 모발 소유자·부위, 관찰 가능한 구성 요소, 방향 관계, 최소 시각 signature, 혼동 경계·제외, 공존 조건, 가시성, source claim, confidence·uncertainty, 선택형 후보 문구, 제안 pixel gate를 가진다. 화학 방식·임상 원인·과거 사건처럼 보이지 않는 정보는 별도 evidence requirement로 두었다. 카드의 출처 정의는 사용자의 요청이나 exact trigger가 아니다.

## 핵심 의미 구분

발레아주는 모발 표면에 자유롭게 쓸어 칠하는 시술 방식이고, 옴브레는 길이 방향의 색 변화다. 직접 읽은 L’Oréal Professional Products Division 교육 글은 두 방식의 결합을 허용한다. 따라서 일반 `balayage` 요청에서 어두운 뿌리·밝은 끝·옴브레 금지를 필수화할 수 없다. 불규칙한 밝은 리본 외형은 명시적으로 선택된 결과 counterpart로 보존할 수 있다. [일차 교육](https://www.hair.com/balayage-vs-highlights.html)

베이비라이트의 중심은 미세한 가닥 폭이다. 현재 직접 읽은 교육은 매우 가는 하이라이트로 설명한다. legacy Wella 검색 본문에는 어두운 가닥에도 폭 중심으로 쓰는 변형이 있지만, 예전 URL이 다른 글로 이동했으므로 이를 전 업계의 보편 정의로 승격하지 않았다. 하이라이트/로라이트의 상대 명도, 베이비/청키의 폭, 발레아주의 도포, 옴브레의 위치 변화를 별도 축으로 둔다. [직접 확인](https://www.hair.com/how-to-get-natural-highlights.html)

딥다이는 옴브레보다 혼합이 적은 끝 구역 배색이고, 컬러 멜트는 인접 색 사이의 중간색과 흐린 경계가 중심이다. 스플릿 컬러는 머리 윗부분에서 나뉜 두 큰 색 구역이며 정확한 50/50 면적을 요구하지 않는 platform 정의가 확인됐다. 아래층 색 배치와 피카부의 부분 가림은 함께 성립할 수 있다. [딥다이](https://www.hair.com/dip-dye-hair-ideas.html), [컬러 멜트](https://www.hair.com/color-melt.html), [스플릿 컬러 정의](https://danbooru.donmai.us/wiki_pages/split-color_hair)

화이트 포록은 이마 앞 국소 흰 묶음이라는 관찰 위치·색으로 투영했다. 폴리오시스는 국소 흰 모발의 임상 sign이며 질병 진단명이나 미용 염색의 동의어로 사용하지 않는다. 흰색 외형만으로 나이, natural-gray, 탈색 또는 clinical origin을 결정하지 않는다. 이 자료는 용어 정의만 사용하며 진단·치료를 제안하지 않는다. [DermNet 정의와 감별 경계](https://dermnetnz.org/topics/poliosis)

네온은 선명한 색 묘사이고, 자체 발광은 모발이 주변에 빛을 기여하는 별도 판타지 관계다. 외부 색 조명은 모발과 이웃 피부·옷의 입사면을 함께 바꿀 수 있다. 모발색, 조명색, 광택 반사, 후처리 색 변화는 저장 축을 구분해야 한다. [네온 색 예시](https://www.hair.com/dip-dye-hair-ideas.html), [발광 모발 정의](https://danbooru.donmai.us/wiki_pages/glowing_hair)

Ahoge는 한 개의 긴 돌출 lock, antenna hair는 두 개 이상의 얇은 돌출 lock이다. Drill hair는 끝으로 좁아지는 원뿔 나선이며, 일반 ringlets는 같은 정의가 아니다. Hair intakes는 머리 위에서 앞을 향한 scoop이고 hairline을 기점으로 하는 curtain bangs와 다르다. Prehensile hair는 목표를 조작하는 appendage 관계, expressive hair는 감정 표현 연출로 구분했다. 바보·귀족·수줍음·신비로움 같은 원문/태그 관습은 외형의 고유 의미나 실제 사람의 성격으로 사용하지 않는다. [Ahoge](https://danbooru.donmai.us/wiki_pages/ahoge), [Drill hair](https://danbooru.donmai.us/wiki_pages/drill_hair), [Hair intakes](https://danbooru.donmai.us/wiki_pages/hair_intakes), [Prehensile hair](https://danbooru.donmai.us/wiki_pages/prehensile_hair)

## 현행 작성 데이터에 대한 좁은 반영 계획

### P0: H368 웻룩과 H369 실제 수분 상태 분리

Wella의 공식 wet-look gel은 마른 또는 축축한 머리에 바른 뒤 자연 건조하도록 안내한다. Hair.com의 공식 wet-look 교육에도 젤이 완전히 건조된 뒤 연출을 유지하는 예가 있다. `wet-look`은 지속되는 실제 물기·물방울·비·땀·피부부착의 필수조건이 아니다. [Wella 공식 제품 정의](https://www.wella.com/international/hair-style/gel/wella-shockwaves-extra-strong-wet-look-gel-200-ml), [L’Oréal 공식 연출 교육](https://www.hair.com/wet-look-hairstyles.html)

읽은 `wet_damp_clumped_hair_state` profile의 exact_terms에 `wet-look hair`, `wet look hair`가 있고, 동명 후보 alias에도 `wet-look hair`가 있었다. 이 profile은 실제 수분 상태의 reduced volume, damp bundles, coherent moisture, downward weight 또는 localized adherence를 요구하고 gel styling 단독 대체를 배제한다. 따라서 범용 웻룩 alias가 실제 수분 gate를 유도할 위험이 있다. 이는 작성 소스 정적 증거이며 현재 live activation을 확인한 결과는 아니다.

후속 구현은 H368을 표면 finish counterpart로 분리하고 해당 exact alias를 실제 수분 profile/candidate에서 분리한다. H369의 실제 수분 요청은 유지하되 피부에 닿지 않는 무거운 처짐 대안을 보존한다. 기존 profile에는 이미 downward behavior OR local adherence 대안이 있으므로 접촉을 새 필수조건으로 만들면 안 된다. 현재 후보 embedding이 face/neck adherence 쪽으로 더 강하게 표현된 부분도 같은 대안에 맞춰 좁게 정렬한다.

| prospective case | 제안 판정 |
|---|---|
| 마른 젤 연출의 웻룩 | shiny/set finish만 선택; 실제 물기 profile hard activation은 없어야 함 |
| 실제 damp hair가 피부에서 떨어져 무겁게 처짐 | 기존 비부착 대안을 통과시켜야 함 |
| 젖은 관자놀이 가닥의 피부부착을 명시 | 지정 피부와 가닥 contact가 같은 crop에서 보여야 함 |

### P0: H265 발레아주 시술과 선택형 리본 결과 분리

읽은 `balayage_ribbon_color_placement`는 darker roots, lighter mid/end ribbons, base continuity 및 not-full-width-ombre를 required groups와 reject_substitutes에 넣고 있다. 이 정의는 특정 전통적 외형을 설명하는 데 쓸 수 있지만 일반 발레아주 시술의 필수 결과는 아니다. `balayage_brown` 및 리본 후보와 같은 색·결과 후보는 요청에 맞게 선택 가능하게 두고, generic method에서 옴브레 공존을 금지하거나 어두운 뿌리를 자동 고정하는 exact 연결은 분리한다.

후속 검증은 발레아주+옴브레 공존, 밝은 바탕의 어두운 가닥 추가, 극세/청키 폭 variation을 비교한다. 사용자에게 명시된 brown base·리본 위치·경계는 보존하며 pigment placement와 lighting/specular 반사는 계속 구분한다. 이번 작업은 계획만 작성했고 profile, candidate 또는 index를 바꾸지 않았다.

### P1: 이름 충돌과 소유자 분리

H397의 textile `Hair scarf`와 H447의 머리카락 자체를 목·어깨에 둘러 쓰는 `Hair scarf`는 소유자·재질·관계가 다르다. H204의 bow-shaped hair와 H387의 bow ornament도 각각 모발 구조와 붙인 장식이다. H278 피카부 컬러와 H429 눈앞을 덮는 peek-a-boo wave 역시 별도 의미다. bare English surface 하나를 서로 다른 의미의 exact alias로 합치지 않는다. [모발을 두르는 platform 정의](https://danbooru.donmai.us/wiki_pages/hair_scarf)

### 읽은 소스의 고정 증거

| 파일 | SHA-256 | 읽은 행 |
|---|---|---|
| [photo_prompt_visual_obligations.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json) | `b687a8f540747d5e6fedaffbddc753b8b0c6b9abf071bb93740a5087d0106d7c` | balayage_ribbon_color_placement, wet_damp_clumped_hair_state |
| [photo_prompt_tags.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_tags.json) | `7a3c5615395d51e2cb6525940c128c66f8c8dd32a7e499dd9e7d75ff4300b9a4` | slicked_back_wet, balayage_brown, wet_damp_clumped_hair_state, balayage_ribbon_color_placement |

이 해시는 해당 담당자가 읽은 작성 소스의 상태이며 live loader·manifest·ranker 또는 generated pixels의 성공을 뜻하지 않는다.

## 55개 독립 의미 카드

| 카드 | 원본 keyword 연결 | Namespace |
|---|---|---|
| hair_color_state.highlights — 밝은 부분 가닥 | H258 | hair.visual.color_placement |
| hair_color_state.lowlights — 어두운 부분 가닥 | H259 | hair.visual.color_placement |
| hair_color_state.babylights — 극세 부분 가닥 | H260 | hair.visual.color_placement |
| hair_color_state.chunky_highlights — 굵은 밝은 부분 가닥 | H261, H262 | hair.visual.color_placement |
| hair_color_state.balayage_process — 발레아주 도포 방식 | H264, H265, H266, H267, H268 | hair.process.coloring |
| hair_color_state.balayage_pattern — 발레아주형 색 배치 | H265, H267 | hair.visual.color_placement |
| hair_color_state.ombre — 길이 방향 그라데이션 | H269 | hair.visual.color_placement |
| hair_color_state.reverse_ombre — 밝은 뿌리에서 어두운 끝 | H271 | hair.visual.color_placement |
| hair_color_state.sombre — 약한 옴브레 변화 | H270 | hair.visual.color_placement |
| hair_color_state.dip_dye — 끝부분의 뚜렷한 배색 | H272 | hair.visual.color_placement |
| hair_color_state.color_melt — 경계가 녹아 이어지는 배색 | H275 | hair.visual.color_placement |
| hair_color_state.shadow_root — 어두운 뿌리와 흐린 연결 | H273, H274 | hair.visual.color_placement |
| hair_color_state.money_piece — 얼굴 앞쪽 강조 가닥 | H263 | hair.visual.color_placement |
| hair_color_state.split_color — 두 큰 구역의 배색 | H276 | hair.visual.color_placement |
| hair_color_state.color_block — 넓은 색 면 배치 | H277 | hair.visual.color_placement |
| hair_color_state.peekaboo — 겉층 아래 가려졌다 드러나는 색 | H278 | hair.visual.color_placement |
| hair_color_state.underlights — 아래층·안쪽층 배색 | H279 | hair.visual.color_placement |
| hair_color_state.colored_streak — 좁은 대비색 줄 | H280, H281 | hair.visual.color_placement |
| hair_color_state.colored_bangs — 앞머리 전체 구역 배색 | H282 | hair.visual.color_placement |
| hair_color_state.colored_tips — 끝부분 다른색 | H283 | hair.visual.color_placement |
| hair_color_state.white_forelock — 이마 부근 흰 모발 묶음 | H324 | hair.visual.color_placement |
| hair_color_state.poliosis_boundary — 폴리오시스 용어 경계 | H325 | hair.clinical.nonvisual_cause |
| hair_color_state.salt_and_pepper — 흰 가닥과 어두운 가닥 혼합 | H322 | hair.visual.color_placement |
| hair_color_state.gray_blending — 흰 가닥의 색 대비 연결 | H249 | hair.process.result_boundary |
| hair_color_state.gray_coverage — 흰머리 덮기의 결과 경계 | H250 | hair.process.result_boundary |
| hair_color_state.white_appearance — 모발의 흰색 외형 | H323 | hair.visual.color_placement |
| hair_color_state.bleached_origin — 탈색 이력과 외형의 분리 | H255 | hair.process.lightening |
| hair_color_state.temporary_color — 일시 컬러의 외형 경계 | H251 | hair.process.coloring |
| hair_color_state.semi_permanent_color — 세미퍼머넌트의 외형 경계 | H252 | hair.process.coloring |
| hair_color_state.demi_permanent_color — 데미퍼머넌트의 외형 경계 | H253 | hair.process.coloring |
| hair_color_state.permanent_color — 퍼머넌트의 외형 경계 | H254 | hair.process.coloring |
| hair_color_state.neon_color — 네온을 연상시키는 선명색 | H354 | hair.visual.color_placement |
| hair_color_state.emissive_hair — 자체 발광 모발 | H357 | hair.illustration.light_behavior |
| hair_color_state.colored_illumination — 색 조명에 따른 모발의 겉색 | 보완 경계 연구 | hair.visual.illumination_boundary |
| hair_color_state.wet_hair — 실제 수분이 있는 모발의 가시 상태 | H367, H369, H372, H373, H375, H431 | hair.state.surface |
| hair_color_state.frizz_flyaways — 주 형태 밖 잔가닥·프리즈 | H364, H365, H371 | hair.state.surface |
| hair_color_state.matted_hair — 엉켜 압축된 모발 | H384 | hair.state.surface |
| hair_color_state.wind_displaced — 한 방향으로 떠밀린 모발 | H370, H449 | hair.state.surface |
| hair_color_state.singed_hair — 그을린·탄 모발 상태 | H379 | hair.state.surface |
| hair_color_state.cut_hair — 모발을 자르는 접촉과 잘린 결과 | H381, H382 | hair.interaction.cutting |
| hair_color_state.hair_grabbing_pulling — 다른 소유자의 모발 잡기·당기기 | 보완 경계 연구 | hair.interaction.contact |
| hair_color_state.blood_stained_hair — 모발에 붙은 혈흔 | H383, H384 | hair.state.surface |
| hair_color_state.ahoge — 한 가닥 돌출 캐릭터 머리 | H433, H435, H436 | hair.illustration.tag |
| hair_color_state.antenna_hair — 두개 이상 돌출 가는 모발 | H434 | hair.illustration.tag |
| hair_color_state.drill_hair — 원뿔형 나선 모발 | H441 | hair.illustration.tag |
| hair_color_state.twin_drills — 쌍으로 묶인 드릴 모발 | H442 | hair.illustration.tag |
| hair_color_state.hair_intakes — 머리 위 앞향 스쿱 아치 | H438 | hair.illustration.tag |
| hair_color_state.prehensile_hair — 부속기관처럼 조작하는 모발 | H450 | hair.illustration.action_relation |
| hair_color_state.expressive_hair — 감정에 반응한 모발 형상 | H435, H437, H439 | hair.illustration.affect_symbol |
| hair_color_state.narrative_change — 참조 대비 헤어 변화와 서사 | 보완 경계 연구 | hair.narrative.reference_comparison |
| hair_color_state.rainbow_hair — 스펙트럼형 다색 모발 | H285 | hair.visual.fantasy_palette |
| hair_color_state.wet_look — 스타일링된 젖은 듯한 표면 | H368 | hair.visual.surface_finish |
| hair_color_state.hair_body_overlap — 모발의 몸 앞 겹침·가림 | H452, H453 | hair.illustration.owner_occlusion |
| hair_color_state.hair_bikini_structure — 모발을 묶어 만든 의복형 구조 | H454 | hair.illustration.constructed_hair_garment |
| hair_color_state.convenient_hair — 특정 부위를 모발로 가린 관계 | H451 | hair.illustration.occlusion_effect |

각 카드의 세부 구성 요소·방향 관계·최소 signature·예시 후보·실패 gate는 JSON에 있다. 같은 구역에 혈흔과 matting을 요청하면 두 property가 모두 보여야 한다. Blood 색 잔여만으로 혈액의 주체나 injury 원인은 알 수 없고, matting만으로 위생·질병·문화적 스타일을 판단할 수 없다. [혈흔 위치 정의](https://danbooru.donmai.us/wiki_pages/blood_in_hair), [matting의 정의 경계](https://dermnetnz.org/topics/acute-hair-matting)

## 대표 최소 대조쌍 12개

각 대조쌍은 향후 비교용이며 생성하지 않았다. 동일 소유자·유효 crop·조명을 통제하되 조명 자체가 비교축이면 그 차이를 명시한다.

| ID | 비교 | 바꾸는 축 | 판정 경계 |
|---|---|---|---|
| MP-CS01 | Balayage-like pattern / ombre | 가닥별분포 | 가닥별 시작 높이와 바탕 공간을 전체 폭의 길이 변화와 비교한다. 결과만으로 실제 시술 방식을 판정하지 않는다. |
| MP-CS02 | Babylights / chunky highlights | 가닥폭 | 같은 바탕색·강조색·조명에서 가닥 폭만 바꾼다. 절대 cm 기준을 만들지 않는다. |
| MP-CS03 | Colored highlights / colored illumination | 물체색과빛 | 모발 구역과 인접 피부의 광원 분포를 함께 본다. 단일 사진에서 원인 분해가 모호하면 모호함을 보존한다. |
| MP-CS04 | Ombre / dip dye | 경계폭 | 같은 색·길이에서 전환 폭만 바꾼다. 실제로 액체에 담갔다는 시술은 추정하지 않는다. |
| MP-CS05 | Color melt / split-color | 연결과분할 | 색 팔레트는 유지하고 부드러운 중간색 연결과 세로 두 구역 분할을 비교한다. |
| MP-CS06 | Peekaboo / exposed underlights | 가림상태 | 안쪽층 배치는 두 상태 모두 성립할 수 있다. 피카부의 부분 가림 조건을 따로 평가한다. |
| MP-CS07 | White forelock / poliosis attribution | 외형과원인 | 픽셀이 같은 의도적 음성 대조다. 임상 적용은 별도 문서가 있어야 하며 이미지 평가에서 원인을 판정하지 않는다. |
| MP-CS08 | Neon-colored / emissive hair | 빛원역할 | 색의 선명도는 유지하고 모발의 주변 빛 기여를 바꾼다. 수신면 요구는 구분력을 높이기 위한 제안 기준이다. |
| MP-CS09 | Ahoge / antenna hair | 돌출수량 | 같은 길이·굵기·위치에서 돌출 모발 묶음 수를 바꾼다. 짧고 굵은 tuft와 장식은 제외한다. |
| MP-CS10 | Drill hair / ordinary ringlets | 원뿔taper | 나선 반복은 유지하고 원뿔 taper와 끝 형상만 바꾼다. 계층·성격은 평가하지 않는다. |
| MP-CS11 | Hair intakes / curtained bangs | 기점과열림방향 | 머리 위 기점과 앞머리 hairline 기점을 같은 crop 안에서 구분한다. |
| MP-CS12 | Prehensile / expressive hair | 목표조작과감정표현 | 목표 접촉·지지와 감정 표현을 구분한다. 사고에 의한 제어 능력 자체는 정지사진으로 증명하지 않는다. |

P0의 웻룩/실제 수분/명시 피부부착 triplet은 위 일반 대조쌍과 별도의 좁은 회귀 계획이다. 세 경우를 하나의 평균 점수로 합치지 않고 각 의미 연결을 판정한다.

## 미확정·비시각 용어 처리

`temporary/semi/demi/permanent`, bleach, root retouch, gray blending/coverage는 과정·제품·이력과 결과색을 분리했다. 영구 제품도 퇴색할 수 있고, 같은 색 외형에 여러 과정이 대응할 수 있다. 자연색·시술 이력을 pixels로 확인하지 않는다. [제품 범주 설명](https://www.hair.com/how-long-does-hair-dye-last.html), [그레이 결과 비교](https://www.redken.com/blog/everything-you-need-to-know-about-covering-gray-hair.html)

명도, 톤, 색 계열, 채도, base/accent의 구역은 별도 축이다. Wella도 브랜드별 numbering system이 다름을 명시한다. `ash`는 금색·적색 온기를 줄인 방향이지 항상 밝은색을 뜻하지 않는다. Mocha/champagne/pearl/opal 등의 창작색 이름은 전역 RGB·성분·배합을 고정하지 않는다. `dirty blonde`의 dirty를 청결 상태로 해석하지 않는다. [명도·톤·브랜드 체계](https://www.wella.com/international/wella-magazine/want-achieve-your-dream-shade-hair-levels-and-tones-can-help)

Foilyage, reverse balayage, oil-slick, stenciled process, opal, holographic의 좁은 명명은 직접 정의를 재확인할 항목으로 남겼다. 특히 Danbooru의 patterned_hair는 그림의 고정 무늬 관습을 다뤄 실제 salon stenciling과 exact 동의어가 아니다. 해당 위키의 '실제 머리에 불가능' 표현을 모든 실제 hair pattern에 대한 과학적 사실로 확대하지 않는다.

H427–H432의 pin-up/bombshell/boudoir/sex hair/trichophilia는 서로 다른 범주다. 시기·화보 연출과 모발 형상, 젖은 가닥의 피부붙음, 비시각 관심 개념을 분리한다. `sex_hair`의 platform 정의는 땀이나 물 때문에 피부에 붙은 가닥도 허용하므로 선행 성적 사건의 증거가 아니다. `trichophilia`/`hair_fetish`의 원문 키워드는 보존하지만 이번 native wiki 조회는 record를 반환하지 않았다. 일차 정의가 미확보이며 이미지 후보·행동·심리 진단을 만들지 않는다. [피부붙음 태그의 범위](https://danbooru.donmai.us/wiki_pages/sex_hair)

Hair over breasts/crotch는 모발이 해당 구역 앞에 내려오는 위치, convenient hair는 실제 가림 효과, hair bikini는 모발을 몸에 묶은 의복형 구조다. 관심 성향·노출·나이를 자동 뜻하지 않는다. 후보 예시는 옷으로 가려진 중립적인 가림/묶임 관계로 작성했고 platform의 해부학적 censorship을 완전히 재현하는 예시라고 주장하지 않는다. 연구 정의와 default image candidate를 분리한다. [모발 앞겹침](https://danbooru.donmai.us/wiki_pages/hair_over_breasts), [가림 효과](https://danbooru.donmai.us/wiki_pages/convenient_hair), [묶인 구조](https://danbooru.donmai.us/wiki_pages/hair_bikini)

## 출처 레코드와 접근 상태

| 출처 | 확인 방식 | 지원 범위 / 제한 |
|---|---|---|
| [hc_src_01: Balayage Vs. Highlights Vs. Ombre: What's The Difference?](https://www.hair.com/balayage-vs-highlights.html) | direct_body_verified | balayage, appearance, highlights, peekaboo, reverse; The article sometimes names both processes and results 'techniques'; the research cards separate them for still-image verification. |
| [hc_src_02: Natural-Looking Highlights: 5 Expert Tips for Laidback Color](https://www.hair.com/how-to-get-natural-highlights.html) | direct_body_verified | baby, low, front; Childhood-inspired marketing is not a subject-age requirement. |
| [hc_src_03: From Basic To Bright: 20 Dip-Dye Hair Color Ideas](https://www.hair.com/dip-dye-hair-ideas.html) | direct_body_verified | dip, neon, rainbow; The absence of an emission requirement is a boundary inference, supplemented by the separate glowing_hair wiki definition. |
| [hc_src_04: 16 Low-Maintenance Hair Color Ideas](https://www.hair.com/low-maintenance-hair-color.html) | direct_body_verified | root, dip; This source uses smudge/shadow as overlapping descriptions; it does not support fixed centimeter or inch classes. |
| [hc_src_05: Coloring, Styling, and Caring for White Blonde Hair](https://www.hair.com/white-hair-ideas.html) | direct_body_verified | white, bleach, money, split, inner; This cosmetic article does not establish that a person with white hair was bleached, is older, or has a clinical condition. |
| [hc_src_06: How Long Does Every Type Of Hair Dye Last?](https://www.hair.com/how-long-does-hair-dye-last.html) | direct_body_verified | temporary, semi, demi, permanent; These are product-category explanations, not a means of identifying chemistry from pixels. |
| [hc_src_07: Everything You Need To Know About Covering Grey Hair](https://www.redken.com/blog/everything-you-need-to-know-about-covering-gray-hair.html) | direct_body_verified | blend, cover; The visual result is not proof of product category or treatment history. |
| [hc_src_08: Want Flawlessly Blended Tresses? Ask For Color Melt Hair](https://www.hair.com/color-melt.html) | direct_body_verified | melt, any, contrast; Its process description cannot be inferred from a finished still. |
| [hc_src_09: Highlights vs. Lowlights (legacy Wella educational text)](https://blog.wella.com/us/highlights-vs-lowlights) | official_search_snapshot_only_direct_redirect_mismatch | relative, baby_variant, chunky; On direct open the legacy URL redirected to a different Wellastore article; this is retained as a source-limited variant, not current body confirmation. |
| [hc_src_10: Balayage vs. Ombre Hair (legacy Wella educational text)](https://blog.wella.com/us/balayage-vs-ombre-hair) | official_search_snapshot_only_direct_redirect_mismatch | method, foil, sombre; Legacy routes redirect or return errors; process-specific foilyage semantics need a renewed direct primary source before execution. |
| [hc_src_12: Seasonal Hair Color Trends (legacy opal passage)](https://www.redken.com/blog/seasonal-hair-color-trends.html) | search_snapshot_current_body_missing_claim | opal; The directly opened updated page did not yield the Opal passage during find; do not treat the old passage as confirmed current. |
| [hc_src_13: Poliosis](https://dermnetnz.org/topics/poliosis) | direct_body_verified | patch, pigment, limits; Used only to define vocabulary and avoid overdiagnosis; no diagnosis or treatment recommendation. |
| [hc_src_14: Acute Hair Matting](https://dermnetnz.org/topics/acute-hair-matting) | direct_body_verified | mass, other; Only the observable entangled/compacted appearance is used; clinical severity, permanence and cause are not inferred. |
| [hc_src_15: Danbooru Native Hair Wiki Definitions](https://danbooru.donmai.us/wiki_pages/tag_group%3Ahair) | direct_official_json_api_verified | ahoge, drills, intakes, prehensile, wet, burnt, grab, cut, blood, glow, floating, colors, inner, bangs, tips, streaks, split, rainbow, frizz, roots, alternate, occlusion, bikini, scarf, sex_hair, flaps, flat, symbol, gloss, big, pattern; HTML wiki opens failed; verified body text came from the platform's own wiki_pages.json endpoint. |
| [hc_src_16: Want to achieve your dream shade? Hair levels and tones can help](https://www.wella.com/international/wella-magazine/want-achieve-your-dream-shade-hair-levels-and-tones-can-help) | direct_body_verified | axes, brand, ash; No salon formula or fixed numeric scale is used in the research. |
| [hc_src_17: Shockwaves Extra Strong Wet Look Gel](https://www.wella.com/international/hair-style/gel/wella-shockwaves-extra-strong-wet-look-gel-200-ml) | direct_body_verified | dry; This directly supports a wet-look finish without requiring ongoing visible liquid water. |
| [hc_src_18: How To Pull Off A Wet Look Hairstyle On Any Hair Texture](https://www.hair.com/wet-look-hairstyles.html) | direct_body_verified | finish, regions; Wet-look styling and actual moisture may coexist, but neither term is a synonym for the other. |

Source JSON은 각 claim의 정확한 지원 문장을 짧게 paraphrase했고, platform wiki마다 독립 URL과 API URL을 넣었다. HTML 위키 접근 실패는 공식 JSON endpoint 읽기로 보완했다. Legacy 검색 스냅샷과 현재 직접 본문은 별도로 표시했고, 접근하지 못한 내용을 확인 완료라고 기록하지 않았다.

## 179개 원본 키워드 disposition

원본 keyword 존재 확인, 일차 의미 확인, 연구 카드 연결, 실제 activation은 서로 다른 상태다. 다음 표는 담당 범위의 빠짐 여부와 후속 반영 방향을 보여주며, named primary flag가 없는 항목을 자동 승인하지 않는다. 색명 다수는 명도·톤·채도·소유 구역을 쓰는 제안 차원이며 개별 브랜드 레시피 검증이 아니다.

| H ID | 원본 용어 | Disposition | 카드 / 후속 경계 |
|---|---|---|
| H235 | 명도·레벨 / Level / depth | descriptive_label_dimensions_only | Level/depth is brightness; preserve the user's scale label only with its named brand. Never reinterpret tone as level. |
| H236 | 색상 / Hue | descriptive_label_dimensions_only | Hue specifies a color family independently of darkness and saturation. Brand hue labels require context. |
| H237 | 톤 / Tone | descriptive_label_dimensions_only | Tone is the color tendency or warm/cool direction; keep it distinct from brightness. |
| H238 | 채도 / Saturation | descriptive_label_dimensions_only | Saturation is a proposed chroma axis; vividness does not imply light emission or a dye chemistry. |
| H239 | 따뜻한 톤 / Warm tone | descriptive_label_dimensions_only | Warm-direction accents may be gold/orange/red; use a palette description, not personality. |
| H240 | 차가운 톤 / Cool tone | descriptive_label_dimensions_only | Cool-direction accents may be ash/blue/violet; ash need not mean a lighter depth. |
| H241 | 중성 톤 / Neutral tone | descriptive_label_dimensions_only | Neutral is a balanced tone direction within the selected system, not one universal RGB. |
| H242 | 베이스 컬러 / Base color | descriptive_label_dimensions_only | Specify the main hair-owned color and the region it occupies; do not bind a lighting hue as the base. |
| H243 | 보조색 / Accent color | descriptive_label_dimensions_only | Specify additional hair-owned color, region and amount; accent need not be brighter. |
| H244 | 언더라잉 피그먼트 / Underlying pigment | descriptive_label_dimensions_only | Underlying pigment is process/biological metadata; do not infer it from a bright rendered color. |
| H245 | 리프트 / Lift | descriptive_label_dimensions_only | Lift is a lightening change relative to a supplied baseline; final lightness alone does not show the change. |
| H246 | 디포짓 / Deposit | descriptive_label_dimensions_only | Deposit is a product/process attribute; show a final color while leaving chemistry unscored. |
| H247 | 브래시니스 / Brassiness | descriptive_label_dimensions_only | Brassiness includes an unwanted warm tendency; 'unwanted' requires the user's target-tone context. Warm copper is not automatically a defect. |
| H248 | 토너 / Toner | descriptive_label_dimensions_only | Toner adjusts color tendency and is not synonymous with bleaching. Final color does not identify its product category. |
| H249 | 그레이 블렌딩 / Gray blending | draft_card_or_related_modifier | gray_blending; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H250 | 그레이 커버리지 / Gray coverage | draft_card_or_related_modifier | gray_coverage; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H251 | 템퍼러리 컬러 / Temporary color | draft_card_or_related_modifier | temporary_color; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H252 | 세미퍼머넌트 컬러 / Semi-permanent color | draft_card_or_related_modifier | semi_permanent_color; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H253 | 데미퍼머넌트 컬러 / Demi-permanent color | draft_card_or_related_modifier | demi_permanent_color; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H254 | 퍼머넌트 컬러 / Permanent color | draft_card_or_related_modifier | permanent_color; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H255 | 블리치·탈색 / Bleaching / lightening | draft_card_or_related_modifier | bleached_origin; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H256 | 올오버 컬러 / All-over color | descriptive_label_dimensions_only | All-over describes broad coverage of a chosen main color. Uniform color does not establish dye use. |
| H257 | 루트 리터치 / Root retouch | descriptive_label_dimensions_only | Root retouch concerns a supplied growth/treatment baseline. Describe matched or differing root color without inventing the history. |
| H258 | 하이라이트 / Highlights | draft_card_or_related_modifier | highlights; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H259 | 로라이트 / Lowlights | draft_card_or_related_modifier | lowlights; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H260 | 베이비라이트 / Babylights | draft_card_or_related_modifier | babylights; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H261 | 청키 하이라이트 / Chunky highlights | draft_card_or_related_modifier | chunky_highlights; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H262 | 리본 하이라이트 / Ribbon highlights | draft_card_or_related_modifier | chunky_highlights; Ribbon describes a long visible color band. Specify its width, color and flow; it can coexist with balayage or chunky highlights. |
| H263 | 머니피스 / Money piece | draft_card_or_related_modifier | money_piece; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H264 | 프리핸드 페인팅 / Freehand painting | draft_card_or_related_modifier | balayage_process; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H265 | 발레아주 / Balayage | priority_separate_process_from_optional_result | balayage_process, balayage_pattern; Keep freehand process separate from a selected lighter-ribbon result. Balayage can make or coexist with ombre; no fixed dark roots or not-ombre condition for generic method. |
| H266 | 포일리야주 / Foilyage | hold_specific_term_until_direct_definition_reconfirmation | balayage_process; Foilyage adds foil development to a freehand-like coloring layout. Legacy indexed wording only; finished hair cannot establish this process. |
| H267 | 파셜 발레아주 / Partial balayage | draft_card_or_related_modifier | balayage_process, balayage_pattern; Partial balayage is a scope modifier. Bind the selected region; do not demand a whole-head gradient. |
| H268 | 리버스 발레아주 / Reverse balayage | hold_specific_term_until_direct_definition_reconfirmation | balayage_process; Reverse balayage describes adding darker depth within lighter hair in some education. It is not reverse ombre's length direction; reconfirm direct definition before adoption. |
| H269 | 옴브레 / Ombré | draft_card_or_related_modifier | ombre; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H270 | 솜브레 / Sombré | draft_card_or_related_modifier | sombre; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H271 | 리버스 옴브레 / Reverse ombré | draft_card_or_related_modifier | reverse_ombre; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H272 | 딥다이 / Dip dye | draft_card_or_related_modifier | dip_dye; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H273 | 섀도 루트 / Shadow root | draft_card_or_related_modifier | shadow_root; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H274 | 루트 스머지 / Root smudge | draft_card_or_related_modifier | shadow_root; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H275 | 컬러 멜트 / Color melt | draft_card_or_related_modifier | color_melt; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H276 | 스플릿 다이 / Split dye | draft_card_or_related_modifier | split_color; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H277 | 컬러 블로킹 / Color blocking | draft_card_or_related_modifier | color_block; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H278 | 피카부 컬러 / Peekaboo color | draft_card_or_related_modifier | peekaboo; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H279 | 언더라이트 / Underlights | draft_card_or_related_modifier | underlights; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H280 | 컬러 스트리크 / Colored streak | draft_card_or_related_modifier | colored_streak; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H281 | 스컹크 스트라이프 / Skunk stripe | draft_card_or_related_modifier | colored_streak; Skunk stripe is a broad high-contrast color nickname; specify dark/light areas and width. Do not infer odor, animal identity or personality. |
| H282 | 염색 앞머리 / Colored bangs | draft_card_or_related_modifier | colored_bangs; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H283 | 염색 끝가닥 / Dyed tips | draft_card_or_related_modifier | colored_tips; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H284 | 오일슬릭 헤어 / Oil-slick hair | hold_specific_term_until_direct_definition_reconfirmation | Oil-slick is a creative palette nickname, commonly proposed as jewel-like hues over a dark base. Preserve requested colors and regions; no actual oil layer or optical iridescence is implied. |
| H285 | 레인보 헤어 / Rainbow hair | draft_card_or_related_modifier | rainbow_hair; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H286 | 스텐실 헤어 / Stenciled hair | hold_specific_term_until_direct_definition_reconfirmation | Salon stenciling is a process with a visible pattern result. Danbooru patterned_hair has an illustration-specific unmoving-pattern convention, so the two must not be exact aliases. |
| H287 | 내추럴 블랙 / Natural black | descriptive_label_dimensions_only | Very dark black appearance; 'natural' origin remains unknown without supplied provenance. |
| H288 | 제트 블랙 / Jet black | descriptive_label_dimensions_only | Very deep black appearance; no fixed RGB or contrast threshold. |
| H289 | 소프트 블랙 / Soft black | descriptive_label_dimensions_only | Near-black with a softer/lower-contrast impression; exposure may produce the same change. |
| H290 | 블루 블랙 / Blue-black | descriptive_label_dimensions_only | Near-black base with a blue/cool tendency; exclude external blue illumination. |
| H291 | 브라운 블랙 / Brown-black | descriptive_label_dimensions_only | Near-black base with a brown tendency; do not infer natural origin. |
| H292 | 차콜 / Charcoal | descriptive_label_dimensions_only | Dark neutral/cool gray appearance. |
| H293 | 다크 브라운 / Dark brown | descriptive_label_dimensions_only | Deep brown appearance; specify warm/cool tendency separately. |
| H294 | 에스프레소 / Espresso brown | descriptive_label_dimensions_only | A very deep brown creative shade name; no universal recipe. |
| H295 | 초콜릿 브라운 / Chocolate brown | descriptive_label_dimensions_only | A warm medium-to-deep brown creative shade name. |
| H296 | 모카 브라운 / Mocha brown | descriptive_label_dimensions_only | A muted coffee/gray-brown motif; brand formulations vary. |
| H297 | 체스트넛 / Chestnut brown | descriptive_label_dimensions_only | Warm red-brown tendency. |
| H298 | 애시 브라운 / Ash brown | descriptive_label_dimensions_only | Brown with reduced gold/red warmth and an ash/cool direction; not necessarily a lighter brown. |
| H299 | 머시룸 브라운 / Mushroom brown | descriptive_label_dimensions_only | Low-chroma gray/beige-brown motif. |
| H300 | 카라멜 브라운 / Caramel brown | descriptive_label_dimensions_only | Warm golden/copper light-brown motif. |
| H301 | 토피 브라운 / Toffee brown | descriptive_label_dimensions_only | A deeper yellow-brown creative shade name. |
| H302 | 골든 브라운 / Golden brown | descriptive_label_dimensions_only | Brown with a clear golden tendency. |
| H303 | 로즈 브라운 / Rose brown | descriptive_label_dimensions_only | Brown with a pink/rose tendency. |
| H304 | 마호가니 / Mahogany | descriptive_label_dimensions_only | Deep brown with red/violet tendency. |
| H305 | 다크 블론드 / Dark blonde | descriptive_label_dimensions_only | Lower-depth blonde within the selected visual palette, not one mandatory brand level. |
| H306 | 더티 블론드 / Dirty blonde | descriptive_label_dimensions_only | Muted blonde mixed with light-brown/gray impression; 'dirty' is not a hygiene state. |
| H307 | 브론드 / Bronde | descriptive_label_dimensions_only | Brown/blonde mixture or intermediate appearance; not one mandatory dye process. |
| H308 | 골든 블론드 / Golden blonde | descriptive_label_dimensions_only | Blonde with a distinct yellow-gold tendency. |
| H309 | 허니 블론드 / Honey blonde | descriptive_label_dimensions_only | Deeper warm golden-blonde motif. |
| H310 | 버터 블론드 / Butter blonde | descriptive_label_dimensions_only | Pale creamy yellow-blonde motif. |
| H311 | 베이지 블론드 / Beige blonde | descriptive_label_dimensions_only | Balanced beige blonde with neither ash nor gold dominant. |
| H312 | 샌디 블론드 / Sandy blonde | descriptive_label_dimensions_only | Blonde with a light gray/beige-brown sandy impression. |
| H313 | 애시 블론드 / Ash blonde | descriptive_label_dimensions_only | Cool/ash blonde with reduced gold/red warmth. |
| H314 | 샴페인 블론드 / Champagne blonde | descriptive_label_dimensions_only | A pale champagne motif whose neutral, pink or beige tendency varies; clarify rather than fix RGB. |
| H315 | 플래티넘 블론드 / Platinum blonde | descriptive_label_dimensions_only | Very pale near-white blonde; slight warmth may distinguish it from white in the cited cosmetic convention. |
| H316 | 아이시 블론드 / Icy blonde | descriptive_label_dimensions_only | Very pale cool blonde with a silver/blue impression. |
| H317 | 펄 블론드 / Pearl blonde | descriptive_label_dimensions_only | Pale blonde with neutral/violet pearly tendency; pearl is not an actual material or emission. |
| H318 | 스트로베리 블론드 / Strawberry blonde | descriptive_label_dimensions_only | Red/copper and golden-blonde mixture, rather than generic pink hair. |
| H319 | 실버 / Silver hair | descriptive_label_dimensions_only | Cool gray-white/silver impression; no metallic material, age or emission required. |
| H320 | 스틸 그레이 / Steel gray | descriptive_label_dimensions_only | Medium-to-deep cool gray steel motif. |
| H321 | 스모키 그레이 / Smoky gray | descriptive_label_dimensions_only | Soft muted smoky-gray motif. |
| H322 | 솔트앤페퍼 / Salt-and-pepper hair | draft_card_or_related_modifier | salt_and_pepper; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H323 | 화이트 헤어 / White hair | draft_card_or_related_modifier | white_appearance; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H324 | 흰 앞가닥 / White forelock | draft_card_or_related_modifier | white_forelock; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H325 | 폴리오시스 / Poliosis | draft_card_or_related_modifier | poliosis_boundary; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H326 | 코퍼 / Copper | descriptive_label_dimensions_only | Orange-red copper tendency; not copper metal material. |
| H327 | 진저 / Ginger | descriptive_label_dimensions_only | Orange/gold-red hair-color family; no natural-origin requirement. |
| H328 | 오번 / Auburn | descriptive_label_dimensions_only | Red-brown mixture. |
| H329 | 시나몬 / Cinnamon | descriptive_label_dimensions_only | Warm brown/copper cinnamon motif. |
| H330 | 버건디 / Burgundy | descriptive_label_dimensions_only | Deep wine-red with violet tendency. |
| H331 | 체리 레드 / Cherry red | descriptive_label_dimensions_only | Strong deep red/cherry motif. |
| H332 | 체리 콜라 / Cherry cola | descriptive_label_dimensions_only | Very dark brown base with red/violet tendency; no cola liquid material. |
| H333 | 크림슨 / Crimson | descriptive_label_dimensions_only | Deep strong red/crimson motif; color boundaries vary. |
| H334 | 스칼렛 / Scarlet | descriptive_label_dimensions_only | Brighter strong red with some orange tendency. |
| H335 | 로즈 골드 / Rose gold | descriptive_label_dimensions_only | Pink plus golden tendency; no gold material implied. |
| H336 | 파스텔 핑크 / Pastel pink | descriptive_label_dimensions_only | Low-chroma/high-lightness pink. |
| H337 | 더스티 로즈 / Dusty rose | descriptive_label_dimensions_only | Muted gray-influenced rose pink. |
| H338 | 핫핑크 / Hot pink | descriptive_label_dimensions_only | High-chroma strong pink. |
| H339 | 마젠타 / Magenta | descriptive_label_dimensions_only | Strong red-violet/magenta tendency. |
| H340 | 라벤더 / Lavender | descriptive_label_dimensions_only | Pale cool violet/lavender motif. |
| H341 | 라일락 / Lilac | descriptive_label_dimensions_only | Pale pink-violet lilac motif, with convention-dependent overlap. |
| H342 | 바이올렛 / Violet | descriptive_label_dimensions_only | Strong violet with blue tendency. |
| H343 | 플럼 / Plum | descriptive_label_dimensions_only | Deep red-violet plum motif. |
| H344 | 페리윙클 / Periwinkle | descriptive_label_dimensions_only | Pale blue-violet periwinkle motif. |
| H345 | 코발트 블루 / Cobalt blue | descriptive_label_dimensions_only | Strong deep blue/cobalt motif; no cobalt material. |
| H346 | 네이비 / Navy | descriptive_label_dimensions_only | Very deep blue/navy motif. |
| H347 | 파우더 블루 / Powder blue | descriptive_label_dimensions_only | Pale low-chroma powder-blue motif. |
| H348 | 청록 / Teal | descriptive_label_dimensions_only | Deeper blue-green/teal tendency. |
| H349 | 터쿼이즈 / Turquoise | descriptive_label_dimensions_only | Brighter blue-green/turquoise tendency. |
| H350 | 민트 / Mint | descriptive_label_dimensions_only | Very pale green/blue-green mint motif. |
| H351 | 에메랄드 / Emerald green | descriptive_label_dimensions_only | Deep strong green/emerald motif. |
| H352 | 세이지 / Sage green | descriptive_label_dimensions_only | Muted gray-green sage motif. |
| H353 | 라임 / Lime green | descriptive_label_dimensions_only | Bright yellow-green/lime tendency. |
| H354 | 네온 컬러 / Neon color | draft_card_or_related_modifier | neon_color; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H355 | 오팔 컬러 / Opal hair | hold_specific_term_until_direct_definition_reconfirmation | Opal palette: keep a near-white base plus specified soft pink/lavender/blue patches as an author proposal. Indexed historical Redken text is not current-body verified. |
| H356 | 홀로그래픽 컬러 / Holographic hair | hold_specific_term_until_direct_definition_reconfirmation | Holographic may mean a pastel multicolor nickname or an angle-sensitive optical effect. Keep palette and optical behavior separate; source/intent clarification is needed. |
| H357 | 발광 머리 / Emissive / glowing hair | draft_card_or_related_modifier | emissive_hair; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H358 | 실키 / Silky hair | descriptive_label_dimensions_only | Silky is a smooth flowing strand surface metaphor; real tactile softness, material origin or health is not visible. |
| H359 | 글로시 / Glossy hair | descriptive_label_dimensions_only | Glossy is sheen due to reflected light on the hair surface. It does not imply lighter dyed strands. |
| H360 | 매트 / Matte hair | descriptive_label_dimensions_only | Matte is a proposed lower-sheen surface descriptor. Low shine does not prove dirty, dry or damaged hair. |
| H361 | 글래스 헤어 / Glass hair | descriptive_label_dimensions_only | Glass hair combines smooth aligned surface and strong sheen as a styling nickname. It is not glass material or an obligatory hair color. |
| H362 | 플러피 / Fluffy hair | descriptive_label_dimensions_only | Fluffy describes airy, separated-looking volume. Do not infer actual softness or curly/coily pattern. |
| H363 | 에어리 / Airy hair | descriptive_label_dimensions_only | Airy describes space or light separation between hair sections. It does not establish wind or low density. |
| H364 | 터슬드 / Tousled hair | draft_card_or_related_modifier | frizz_flyaways; Tousled is deliberate or incidental loose disruption of section flow. Do not replace it with frizz, matting or a grooming history. |
| H365 | 베드헤드 / Bedhead | draft_card_or_related_modifier | frizz_flyaways; Bedhead is a state nickname; separate messy directions from an inferred sleep event. |
| H366 | 리브드인 / Lived-in hair | descriptive_label_dimensions_only | Lived-in is a creative styling nickname for softened, less freshly set structure; passage of days and lifestyle are not pixel facts. |
| H367 | 스트링기 / Stringy hair | draft_card_or_related_modifier | wet_hair; Stringy describes separated narrow bundles. Wetness, oiliness or damage need independent context; dry styled hair may group similarly. |
| H368 | 웻룩 / Wet-look hair | priority_split_finish_from_actual_moisture | wet_look; H368 wet-look can remain after gel dries, so remove its future exact equivalence to H369 actual damp state; use shiny styled finish with localized region binding. |
| H369 | 실제로 젖은 머리 / Wet hair | priority_preserve_actual_damp_state_alternatives | wet_hair; H369 actual damp state is independent of H368 finish. Preserve the existing heavier downward hanging OR skin-adherence alternative; require contact only when selected. |
| H370 | 바람에 흩날리는 머리 / Windblown hair | draft_card_or_related_modifier | wind_displaced; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H371 | 역광 잔머리 / Backlit flyaways | draft_card_or_related_modifier | frizz_flyaways; Backlit flyaways require small protruding strands plus a back/rim-light relation. They do not create a lightened pigment color. |
| H372 | 얼굴에 붙은 가닥 / Strands clinging to the face | draft_card_or_related_modifier | wet_hair; Strands cling to a face region by visible contact. Actual moisture and its source remain separate. |
| H373 | 젖은 관자놀이 머리 / Sweat-damp temple hair | draft_card_or_related_modifier | wet_hair; Sweat-damp temple hair binds damp state to temples; sweat origin must be supplied or have separate scene evidence, rather than inferred from gloss. |
| H374 | 헬멧에 눌린 머리 / Helmet-flattened hair | proposed_owner_region_state_relation_material_or_cause_unverified | Helmet-flattened appearance is a localized compressed silhouette. A helmet-contact relation or before/after evidence is required to claim the cause. |
| H375 | 빗물에 젖은 머리 / Rain-soaked hair | draft_card_or_related_modifier | wet_hair; Rain-soaked hair needs wet state and separately visible/supplied rain context. Preserve damp non-skin-contact hanging alternatives. |
| H376 | 먼지가 앉은 머리 / Dust-coated hair | proposed_owner_region_state_relation_material_or_cause_unverified | Dust-coated hair: define fine particulate residue on strands and the affected region. A gray color alone does not prove dust; material identity needs context. |
| H377 | 재가 묻은 머리 / Ash-dusted hair | proposed_owner_region_state_relation_material_or_cause_unverified | Ash-dusted hair: use irregular pale/gray particles on hair. Do not infer a fire, death, smoke or singed state from a deposit alone. |
| H378 | 진흙에 뭉친 머리 / Mud-clumped hair | proposed_owner_region_state_relation_material_or_cause_unverified | Mud-clumped hair combines specified muddy residue with cohesive grouped strands. Brown dye or ordinary wet clumps are not enough. |
| H379 | 탄 머리끝 / Singed ends | draft_card_or_related_modifier | singed_hair; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H380 | 헝클어진 브레이드 / Disrupted braid | proposed_owner_region_state_relation_material_or_cause_unverified | Disrupted braid requires a local failure in the plait's crossing continuity or loose released strands. Violence, wind and neglect are separate causes. |
| H381 | 잘린 브레이드 / Cut-off braid | draft_card_or_related_modifier | cut_hair; Cut-off braid combines braid structure and lost scalp continuity; cause and actor require the cutting action or supplied reference. |
| H382 | 불규칙하게 잘린 머리 / Unevenly shorn hair | draft_card_or_related_modifier | cut_hair; Unevenly shorn hair describes irregular remaining length/end geometry. Do not infer violence, who cut it, or consent. |
| H383 | 피가 묻은 머리 / Blood-streaked hair | draft_card_or_related_modifier | blood_stained_hair; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H384 | 피로 뭉친 머리 / Blood-matted hair | draft_card_or_related_modifier | blood_stained_hair, matted_hair; Blood-matted hair needs blood/residue context plus compact entanglement in the same owner-bound region; neither property substitutes for the other. |
| H385 | 흉터로 끊긴 헤어라인 / Scar-interrupted hairline | proposed_owner_region_state_relation_material_or_cause_unverified | Scar-interrupted hairline relates a specified skin scar to a localized break in the hairline. A bare patch alone is not scar proof or a medical diagnosis. |
| H427 | 핀업 헤어 / Pin-up hair | optional_creative_association_no_intrinsic_hair_trigger | Pin-up is an optional genre/era styling association. Instantiate specific wave/roll/part structure rather than an inherent personality or age. |
| H428 | 봄셸 웨이브 / Bombshell waves | optional_creative_association_no_intrinsic_hair_trigger | Bombshell waves is a creative large-wave/volume nickname. Describe wave scale, volume and surface finish without assuming sexual intent. |
| H429 | 피카부 웨이브 / Peek-a-boo wave | descriptive_label_dimensions_only | Peek-a-boo wave means a wave falling across an eye/face region. It is not peekaboo color beneath the outer layer; avoid the shared bare 'peekaboo' exact alias. |
| H430 | 부두아르 헤어 / Boudoir hair | optional_creative_association_no_intrinsic_hair_trigger | Boudoir is a scene/editorial styling label, not a unique hair geometry. Keep setting, styling and effective sensual context separate. |
| H431 | 섹스 헤어 / Sex hair | draft_card_or_related_modifier | wet_hair; Sex hair is a platform state tag allowing wet skin-adhering strands from sweat or water; no prior sex event may be inferred. |
| H432 | 헤어 페티시 / Hair fetish / trichophilia | nonvisual_concept_no_pixel_candidate | Hair fetish/trichophilia is a purported interest concept, not a hairstyle, personality diagnosis or visible property. No native wiki record was found; hold primary terminology and provide no generation candidate. |
| H433 | 아호게 / Ahoge | draft_card_or_related_modifier | ahoge; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H434 | 안테나 헤어 / Antenna hair | draft_card_or_related_modifier | antenna_hair; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H435 | 하트 아호게 / Heart ahoge | draft_card_or_related_modifier | ahoge, expressive_hair; Heart ahoge is a single protruding lock shaped like a heart; love, happiness and relationship are optional supplied narrative context. |
| H436 | 물음표 아호게 / Question-mark ahoge | draft_card_or_related_modifier | ahoge; Question-mark ahoge requires that visible symbol shape; confusion is a creative association, not a real person's trait. |
| H437 | 감정 표현 머리 / Expressive hair | draft_card_or_related_modifier | expressive_hair; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H438 | 헤어 인테이크 / Hair intakes | draft_card_or_related_modifier | hair_intakes; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H439 | 헤어 플랩 / Hair flaps | draft_card_or_related_modifier | expressive_hair; Hair flaps are side-emerging tufts and may carry expressive context. They are not biological ears or personality. |
| H440 | 헤어 혼 / Hair horns | descriptive_label_dimensions_only | Hair horns are horn-like shapes made of hair; preserve material/attachment and distinguish biological horns or an accessory. |
| H441 | 드릴 헤어 / Drill hair | draft_card_or_related_modifier | drill_hair; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H442 | 트윈 드릴 / Twin drills | draft_card_or_related_modifier | twin_drills; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H443 | 키시멘 헤어 / Kishimen hair | descriptive_label_dimensions_only | Kishimen hair uses many thin, flat locks; it does not mean noodle material. Keep flat strip geometry independent of curl or stiffness. |
| H444 | 센터 가닥 / Hair between eyes | descriptive_label_dimensions_only | Hair between eyes is a bang bunch long enough to reach the interocular region, with forehead origin visible. |
| H445 | 한쪽 눈 가림 / Hair over one eye | descriptive_label_dimensions_only | Hair over one eye overlaps one eye region; opaque coverage and eye-visible-through-hair are additional visibility states, and shyness/mystery is not intrinsic. |
| H446 | 양눈 가림 / Hair over eyes | descriptive_label_dimensions_only | Hair over eyes overlaps both eye regions. Whether eyes are fully hidden or visible through gaps is separately bound. |
| H447 | 머리 스카프 / Hair scarf | descriptive_label_dimensions_only | Hair scarf wraps owner-bound hair around self/another neck and shoulders. It is distinct from H397 textile scarf accessory and needs source/target owners. |
| H448 | 과장된 머리 부피 / Big hair | descriptive_label_dimensions_only | Big hair is unusual visible hair thickness/volume; distinguish enlarged silhouette from optical texture, cropped perspective or an assumed personality. |
| H449 | 부유하는 머리 / Floating hair | draft_card_or_related_modifier | wind_displaced; Floating hair is broader than windblown hair; airborne suspension does not establish wind, underwater, levitation or gravity failure. |
| H450 | 의지를 가진 머리 / Prehensile hair | draft_card_or_related_modifier | prehensile_hair; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H451 | 편의적 머리 가림 / Convenient hair | draft_card_or_related_modifier | convenient_hair; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H452 | 가슴을 덮는 머리 / Hair over breasts | draft_card_or_related_modifier | hair_body_overlap; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H453 | 사타구니를 가리는 머리 / Hair over crotch | draft_card_or_related_modifier | hair_body_overlap; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |
| H454 | 헤어 비키니 / Hair bikini | draft_card_or_related_modifier | hair_bikini_structure; Use the referenced draft card with explicit owner/region binding; it is not runtime adoption. |

## 납품 검증과 반영 순서

메모리상의 일반 소유자·관계·optional 후보 원칙은 참고했지만, 현재 정의의 사실 주장은 위 직접 자료와 현재 작성 행에서 다시 확인했다. 저장 JSON 파싱과 구조 검증이 통과했다. 카드 55개의 ID 유일성, 필수 필드, source/claim 참조, 179개 담당 H ID의 범위와 유일성, 대조쌍 12개, exact-trigger 비생성 및 모든 pixel gate의 `not_run` 상태를 점검했다. 읽은 기존 profile/candidate 작성 소스 두 파일의 SHA-256도 읽기 전후 같았다. 소스 파일 변경·test suite·runtime smoke·embedding·이미지 생성은 수행 범위에 포함하지 않았다.

후속 구현 순서는 P0 의미 충돌의 좁은 분리, 소유자·재질 namespace 정렬, 직접 정의가 충분한 카드의 선택형 authored candidate 연결, 조건부 용어의 추가 일차 확인, 필요한 기존 회귀 검사와 최소 대조 렌더다. 색 라벨이 검색됐다는 사실만으로 user intent lock을 바꾸거나 hard obligations를 만들지 않는다. 결과물 생성이 실행될 때는 각 required contact·구역·경계가 같은 crop에 보여야 하고, unobservable을 추정 pass로 바꾸지 않는다.
