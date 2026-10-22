# 시각 의미 카드 72개

정의 근거와 아래 가시 실현의 창작 저술을 구분한다. 4개 context 카드는 시각 후보로 변환하지 않는다.

## D01 묘역과 도시 통로

- 연결 키워드: Necropolis
- 방식/우선순위: still / P0; 슬롯 제안: location, spatial_depth
- EN: Separate monumental tomb fronts line a paved lane leading to a cemetery gate.
- KO: 각각 분리된 기념 묘의 정면이 포장 통로 양옆에 늘어서고 통로는 묘역 문으로 이어진다.
- 소유자: tombs = several separate monumental tomb fronts; street = a walkable paved lane; gate = a distant cemetery gate
- 관계: street → passes_between → tombs; street → leads_to → gate
- 혼동: ordinary residential street; one isolated grave
- 주장 한계: 묘역의 공간 구조만 판정; 실제 규모·시신 수·죽은 도시의 행정은 불확정.
- 출처: [S15](https://www.catacombes.paris.fr/en/history/ossuary), [S16](https://www.sciencemuseum.org.uk/objects-and-stories/memento-mori)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## D02 예배 공간 아래 묘실

- 연결 키워드: Crypt
- 방식/우선순위: still / P0; 슬롯 제안: location, object_structure
- EN: A view through a collapsed side wall shows a stair descending below a chapel floor into a lower chamber with a stone tomb.
- KO: 붕괴한 측벽 너머로 예배실 바닥 아래 하부 묘실까지 내려가는 계단과 그 안의 돌무덤이 보인다.
- 소유자: chapel = an upper chapel floor visible through a broken section; stair = a stair descending below that floor; tomb = a stone tomb in the lower chamber
- 관계: stair → descends_below → chapel; tomb → lies_below → chapel
- 혼동: ordinary cellar; unrelated upper and lower rooms
- 주장 한계: 실제로 열린 시야를 통한 상하 연결의 선택안; 모든 crypt가 붕괴/절개되어야 한다는 뜻 아님.
- 출처: [S04](https://www.britishlibrary.cn/en/articles/gothic-motifs/), [S12](https://www.metmuseum.org/essays/relics-and-reliquaries-in-medieval-christianity)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## D03 통로 벽의 매장 감실

- 연결 키워드: Catacomb
- 방식/우선순위: still / P0; 슬롯 제안: location, object_structure
- EN: Horizontal burial recesses repeat along an underground passage that branches at a visible junction.
- KO: 지하 통로 벽에 가로 매장 감실이 반복되고 앞쪽에서 길이 갈라진다.
- 소유자: passage = a narrow underground passage; loculi = repeated horizontal burial recesses in its walls; junction = a visible branching junction
- 관계: loculi → cut_into → passage; junction → branches_from → passage
- 혼동: mine without burial niches; one crypt
- 주장 한계: 파리 납골장과 고대 매장 통로를 동일 역사·구조로 간주하지 않음; 이 감실 배치는 저술한 변주.
- 출처: [S15](https://www.catacombes.paris.fr/en/history/ossuary)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## D04 유골의 보관 배열

- 연결 키워드: Ossuary; Ossuary ornamentation
- 방식/우선순위: still / P0; 슬롯 제안: location, prop_placement
- EN: Long bones and skulls are stacked together inside a bounded wall recess.
- KO: 경계가 있는 벽 감실 안에 긴 뼈와 두개골이 함께 쌓여 있다.
- 소유자: bones = recognizable long bones; skulls = recognizable skulls; recess = a bounded wall recess
- 관계: bones → stacked_in → recess; skulls → interspersed_with → bones
- 혼동: anatomy classroom shelf; random rubble
- 주장 한계: 유골 보관의 가시 배열; 종·개인·사망 원인·의례 의미·진품 여부는 불확정.
- 출처: [S15](https://www.catacombes.paris.fr/en/history/ossuary), [S16](https://www.sciencemuseum.org.uk/objects-and-stories/memento-mori)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## D05 건물과 내부 보관대

- 연결 키워드: Charnel house; Charnel
- 방식/우선순위: proxy / P1; 슬롯 제안: location, prop_placement
- EN: An open doorway in a small freestanding stone building reveals storage racks of wrapped remains.
- KO: 독립된 작은 석조 건물의 열린 문 너머로 감싼 유해 보관대가 보인다.
- 소유자: house = a freestanding small masonry building; door = an open doorway; racks = interior storage racks with wrapped remains
- 관계: door → opens_into → house; racks → visible_through → door
- 혼동: living quarters; ordinary shed with bundles
- 주장 한계: 보관 용도는 명시한 설정과 함께 해석; 모든 차널 하우스의 역사적 전형 아님.
- 출처: [S15](https://www.catacombes.paris.fr/en/history/ossuary), [S16](https://www.sciencemuseum.org.uk/objects-and-stories/memento-mori)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## D06 돌관의 뚜껑과 몸체

- 연결 키워드: Sarcophagus
- 방식/우선순위: still / P0; 슬롯 제안: prop, object_structure
- EN: A carved stone lid rests slightly offset on its matching stone chest, leaving a narrow seam.
- KO: 조각된 돌뚜껑이 맞는 돌관 몸체 위에 조금 비껴 놓여 좁은 틈이 보인다.
- 소유자: chest = a heavy rectangular carved stone chest; lid = a separate fitted stone lid; gap = a narrow open seam
- 관계: lid → rests_on → chest; gap → below → lid; gap → above → chest
- 혼동: plain altar block; wooden coffin
- 주장 한계: 형태·재질 표현만; 내부 존재·봉인의 효력·부활은 불확정. 뚜껑·몸체 양쪽과 실제 틈이 함께 보여야 함.
- 출처: [S12](https://www.metmuseum.org/essays/relics-and-reliquaries-in-medieval-christianity)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## D07 기념 묘 건축과 진입

- 연결 키워드: Mausoleum
- 방식/우선순위: still / P1; 슬롯 제안: location, object_structure
- EN: A recessed entrance opens in a monumental tomb building beneath a funerary relief.
- KO: 장례 부조 아래로 기념 묘 건축의 깊게 들어간 입구가 열린다.
- 소유자: building = a monumental stone tomb building; entry = a recessed entry; memorial = a funerary relief above the entry
- 관계: entry → belongs_to → building; memorial → above → entry
- 혼동: palace facade; one sarcophagus
- 주장 한계: 왕권·실제 매장·특정 문화권은 건축 외형만으로 입증하지 않음.
- 출처: [S12](https://www.metmuseum.org/essays/relics-and-reliquaries-in-medieval-christianity), [S16](https://www.sciencemuseum.org.uk/objects-and-stories/memento-mori)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## D08 상부 개구부와 하부 방

- 연결 키워드: Oubliette
- 방식/우선순위: proxy / P1; 슬롯 제안: location, spatial_depth
- EN: A deep stone chamber has a small ceiling opening, with a retracted ladder visible above it.
- KO: 깊은 돌방 천장에 작은 구멍이 있고 그 위로 거둔 사다리가 보인다.
- 소유자: chamber = a deep stone chamber; opening = a small opening in its ceiling; ladder = a retracted ladder above the opening
- 관계: opening → cuts_through → chamber; ladder → hangs_above → opening
- 혼동: cistern; light well
- 주장 한계: 상부 접근만 묘사; 실제 감옥 기능·투옥·잊힌 세월은 불확정. 역사상 oubliette 오인 사례 추가 조사 필요.
- 출처: [S04](https://www.britishlibrary.cn/en/articles/gothic-motifs/)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## D09 회랑의 붕괴와 사용 흔적

- 연결 키워드: Ruined monastery; Forsaken
- 방식/우선순위: proxy / P0; 슬롯 제안: location, space_condition
- EN: Fallen roof stones interrupt a roofless cloister arcade beside a worn wooden bench.
- KO: 지붕을 잃은 수도원 회랑 안에 지붕 돌이 떨어져 있고 닳은 나무 벤치가 남아 있다.
- 소유자: cloister = a roofless arcaded cloister; debris = fallen roof stones; bench = a worn wooden bench
- 관계: debris → lies_inside → cloister; bench → stands_under → cloister
- 혼동: new unfinished building; staged ruin
- 주장 한계: 버려짐·신의 부재·방치 기간은 외형으로 확정하지 않음.
- 출처: [S04](https://www.britishlibrary.cn/en/articles/gothic-motifs/), [S08](https://www.musee-orsay.fr/en/program/whats-on/exhibitions/angel-odd-dark-romanticism-goya-max-ernst)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## D10 성소와 훼손된 성상

- 연결 키워드: Desecrated cathedral; Desecration; Sacrilege
- 방식/우선순위: proxy / P0; 슬롯 제안: location, aftermath_trace
- EN: A broken devotional effigy lies across a recognizable altar inside a tall church nave.
- KO: 높은 성당 네이브 안의 알아볼 수 있는 제단 위에 부서진 신앙 조각상이 가로놓여 있다.
- 소유자: nave = a tall church nave; altar = a recognizable altar; effigy = a broken devotional effigy
- 관계: altar → stands_inside → nave; effigy → lies_across → altar
- 혼동: accidental earthquake damage; secular sculpture warehouse
- 주장 한계: 훼손 상태와 종교 문맥은 보이나 모독 의도·가해자·악신은 불확정.
- 출처: [S04](https://www.britishlibrary.cn/en/articles/gothic-motifs/), [S12](https://www.metmuseum.org/essays/relics-and-reliquaries-in-medieval-christianity)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## D11 숲과 끊긴 인간 통로

- 연결 키워드: Cursed forest; Desolate
- 방식/우선순위: proxy / P0; 슬롯 제안: location, environment_detail
- EN: Thick exposed roots cross a narrow footpath beside a split wooden trail marker.
- KO: 굵게 드러난 뿌리가 좁은 산길을 가로지르고 쪼개진 길 표지가 곁으로 기울어 있다.
- 소유자: trail = a narrow human footpath; roots = thick exposed roots; marker = a split wooden trail marker
- 관계: roots → cross → trail; marker → leans_beside → trail
- 혼동: ordinary overgrown forest; camera cannot see the path
- 주장 한계: 길을 방해하는 외형 단서; 길의 이동·저주·수목의 의식은 단일 이미지로 불확정.
- 출처: [S09](https://www.bfi.org.uk/features/where-begin-with-folk-horror)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## D12 격리 경계와 식량 접근

- 연결 키워드: Plague city; Pestilence and famine
- 방식/우선순위: proxy / P0; 슬롯 제안: social_cue, situation_context
- EN: Food baskets sit outside a temporary barrier at a shut town gate, while adults wait behind it.
- KO: 닫힌 성문 앞 임시 차단벽 바깥에 식량 바구니가 놓이고 성인들은 안쪽에서 기다린다.
- 소유자: gate = a closed town gate; barrier = a temporary barrier; food = food baskets on its outside; adults = waiting adults behind the barrier
- 관계: barrier → blocks → gate; food → outside → barrier; adults → behind → barrier
- 혼동: ordinary customs queue; festival barrier
- 주장 한계: 격리·접근 불균형의 창작 단서; 병원체·진단·실제 기근은 불확정.
- 출처: [S03](https://joeabercrombie.com/the-value-of-grit/), [S36](https://www.ilo.org/resource/article/meanings-forced-labour)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## D13 거석과 같은 지면의 비교자

- 연결 키워드: Cyclopean ruins; Sublime
- 방식/우선순위: still / P0; 슬롯 제안: scale_relation, object_structure
- EN: Huge irregular masonry blocks dwarf an adult standing on the same continuous ground plane.
- KO: 거대한 불규칙 석재 벽이 같은 연속 지면에 선 성인보다 훨씬 높다.
- 소유자: blocks = huge irregular masonry blocks; adult = one standing adult; ground = one continuous ground plane
- 관계: blocks → rise_from → ground; adult → stands_on → ground
- 혼동: small miniature close to lens; isolated silhouette
- 주장 한계: 상대 크기만 판정; 고고학상 Cyclopean masonry와 모든 거대 유적을 동치화하지 않음.
- 출처: [S04](https://www.britishlibrary.cn/en/articles/gothic-motifs/)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## D14 낭떠러지의 끝과 가려진 하부

- 연결 키워드: Abyss; Abyssal
- 방식/우선순위: still / P0; 슬롯 제안: spatial_depth, composition
- EN: A rope passes beyond a clearly visible stone ledge and disappears into an unresolved dark depth.
- KO: 돌 선반의 끝을 넘은 밧줄이 아래의 분간되지 않는 어둠 속으로 사라진다.
- 소유자: ledge = a clearly visible stone ledge; rope = a hanging rope; darkness = an unresolved lower region
- 관계: rope → passes_beyond → ledge; rope → disappears_into → darkness
- 혼동: flat black backdrop; shallow pit with cropped floor
- 주장 한계: 하부 비가시는 깊이 무한·바닥 부재·실제 미터 치수를 증명하지 않음.
- 출처: [S04](https://www.britishlibrary.cn/en/articles/gothic-motifs/)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## D15 서로 다른 시대의 공간 중첩

- 연결 키워드: Gothic fantasy; Gothic horror
- 방식/우선순위: still / P1; 슬롯 제안: concept_tension, environment_detail
- EN: Exposed modern conduit follows a worn stone arch and feeds a small task lamp.
- KO: 노출된 현대 전선관이 낡은 석조 아치를 따라가 작은 작업등에 연결된다.
- 소유자: arch = a worn medieval stone arch; wiring = exposed modern electrical conduit; fixture = a small working task lamp
- 관계: wiring → runs_along → arch; fixture → attached_to → wiring
- 혼동: random collage; all Gothic must be medieval
- 주장 한계: 시대 층위의 선택안; 현대 장비 추가가 허용된 장면에서만 검토.
- 출처: [S04](https://www.britishlibrary.cn/en/articles/gothic-motifs/)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## D16 쇠잔한 문명의 태양 제단

- 연결 키워드: Dying Earth; Eschatology / Apocalypse
- 방식/우선순위: proxy / P1; 슬롯 제안: world, background_element
- EN: A weathered solar dial stands on a cracked observatory terrace beneath a dim red sun.
- KO: 균열 난 관측대 테라스에 닳은 해시계가 서 있고 수평선 가까이 희미한 붉은 태양이 보인다.
- 소유자: sun = a dim red sun near the horizon; observatory = a cracked observatory terrace; dial = a weathered solar dial
- 관계: dial → stands_on → observatory; sun → visible_beyond → observatory
- 혼동: ordinary sunset; red grading across the whole frame
- 주장 한계: 항성 수명·먼 미래·종말은 서사 설정으로 남음.
- 출처: [S40](https://sf-encyclopedia.com/entry/dying_earth), [S08](https://www.musee-orsay.fr/en/program/whats-on/exhibitions/angel-odd-dark-romanticism-goya-max-ernst)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## O01 유물과 투명 창이 있는 용기

- 연결 키워드: Relic; Reliquary
- 방식/우선순위: still / P0; 슬롯 제안: prop, object_structure
- EN: A small bone fragment is visible through the clear inset window of an ornate metal reliquary.
- KO: 장식 금속 성유물함의 투명한 삽입 창 너머로 작은 뼛조각이 보인다.
- 소유자: relic = a small bone fragment; vessel = an ornate metal reliquary; window = a clear inset window
- 관계: window → set_into → vessel; relic → visible_through → window
- 혼동: bone-shaped box with no contents visible; ordinary jewel
- 주장 한계: 유물/용기는 별개 owner; 거룩함·성인 신원·기적은 외형으로 입증하지 않음.
- 출처: [S12](https://www.metmuseum.org/essays/relics-and-reliquaries-in-medieval-christianity)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## O02 신체를 본뜬 함과 전시대

- 연결 키워드: Reliquary
- 방식/우선순위: still / P0; 슬롯 제안: prop, object_structure
- EN: A metal hand-shaped container stands on a plinth, with a fitted seam visible at its wrist.
- KO: 금속 손 모양 용기가 받침대 위에 서 있고 손목에서 맞물린 이음선이 보인다.
- 소유자: vessel = a metal hand-shaped container; base = a display plinth; seam = a small fitted seam at its wrist
- 관계: vessel → stands_on → base; seam → belongs_to → vessel
- 혼동: severed real hand; prosthetic worn on body
- 주장 한계: 신체형 용기의 창작 실현; 실제 내용물·종교적 사용은 별도.
- 출처: [S12](https://www.metmuseum.org/essays/relics-and-reliquaries-in-medieval-christianity)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## O03 향로의 사슬과 연기의 출발점

- 연결 키워드: Censer / Thurible
- 방식/우선순위: still / P0; 슬롯 제안: prop, prop_placement
- EN: An adult hand holds the upper ring of three chains attached to a perforated metal bowl, and a thin smoke plume rises from its lid.
- KO: 성인의 손이 구멍 뚫린 금속 향로에 연결된 세 사슬의 위 고리를 잡고 뚜껑에서 가는 연기가 오른다.
- 소유자: bowl = a perforated metal incense bowl; chains = three suspension chains; ring = one upper suspension ring; smoke = a thin smoke plume; hand = an adult hand holding the upper ring
- 관계: chains → attach_to → bowl; chains → hang_from → ring; hand → holds → ring; smoke → rises_from → bowl
- 혼동: smoke from separate candle; floating bowl
- 주장 한계: 세 사슬의 접점과 손/고리가 모두 필요; 향의 냄새·흡입 효과는 불확정.
- 출처: [S12](https://www.metmuseum.org/essays/relics-and-reliquaries-in-medieval-christianity)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## O04 배수구의 입과 벽 바깥 물줄기

- 연결 키워드: Gargoyle
- 방식/우선순위: still / P0; 슬롯 제안: object_structure, liquid_inclusion
- EN: A continuous rainwater stream exits the mouth of a projecting stone head and falls clear of the building wall.
- KO: 돌머리 조각의 입에서 연속 빗물 줄기가 나와 건물 벽과 떨어져 낙하한다.
- 소유자: head = a projecting carved stone head; wall = a building wall; water = a continuous rainwater stream
- 관계: head → projects_from → wall; water → exits_mouth_of → head
- 혼동: decorative grotesque without a channel; water behind the head
- 주장 한계: 출수구와 벽 바깥 배수 경로의 선택안; 단순 괴물 장식은 대체 불가.
- 출처: [S14](https://heritagecalling.com/2018/10/26/a-brief-introduction-to-gargoyles/)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## O05 마도서의 실제 펼침 구조

- 연결 키워드: Grimoire; Forbidden knowledge
- 방식/우선순위: proxy / P0; 슬롯 제안: prop, visible_text
- EN: An open bound book carries an invented hand-drawn diagram with short marginal notes on the same page.
- KO: 펼친 제본 책의 같은 면에 창작 도식과 짧은 여백 주석이 있다.
- 소유자: book = an open bound book; diagram = a hand-drawn invented diagram; notes = short invented marginal notes
- 관계: diagram → drawn_on → book; notes → beside → diagram
- 혼동: modern printed novel; diagram hovering outside page
- 주장 한계: 판독된 문구 없이 주문의 기능·금지 사유·지식의 유해성은 판정하지 않음.
- 출처: [S25](https://www.merriam-webster.com/dictionary/grimoire), [S31](https://www.merriam-webster.com/dictionary/sigil)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## O06 봉랍과 문짝의 양쪽 연결

- 연결 키워드: Ward / Seal; Sigil
- 방식/우선순위: still / P0; 슬롯 제안: prop_state, object_structure
- EN: A wax-sealed paper strip bridges a closed wooden door and its stone jamb.
- KO: 봉랍이 찍힌 종이 띠가 닫힌 나무 문짝과 돌 문설주 양쪽에 걸쳐 붙어 있다.
- 소유자: door = a closed wooden door; jamb = its stone jamb; seal = a wax seal across a joined paper strip
- 관계: seal → bridges → door; seal → bridges → jamb
- 혼동: decorative crest only on door; wax floating over a gap
- 주장 한계: 물리적 봉함만; 마법적 차단·침입 불가능·정통성은 불확정.
- 출처: [S31](https://www.merriam-webster.com/dictionary/sigil)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## O07 계약의 두 당사자와 한 문서

- 연결 키워드: Demonic pact; Faustian bargain
- 방식/우선순위: proxy / P0; 슬롯 제안: relational_action, prop
- EN: An adult human and a fictional nonhuman party each touch a different edge of the same parchment document.
- KO: 성인 인간 당사자와 가상 비인간 당사자가 한 양피지 문서의 서로 다른 가장자리에 손을 댄다.
- 소유자: human = one adult human party; other = one fictional nonhuman party; document = one shared parchment document
- 관계: human → touches → document; other → touches → document
- 혼동: two unrelated documents; mere co-presence
- 주장 한계: 당사자-문서 접점만 가시적; 계약 성립·자유로운 합의·영혼 대가는 서사 문맥.
- 출처: [S04](https://www.britishlibrary.cn/en/articles/gothic-motifs/), [S31](https://www.merriam-webster.com/dictionary/sigil)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## O08 뼈 표본과 시간의 상징

- 연결 키워드: Memento mori; Macabre
- 방식/우선순위: still / P0; 슬롯 제안: prop_placement, narrative_clue
- EN: A carved skull and a partly drained hourglass share a small wooden table.
- KO: 조각된 해골 물체와 모래가 일부 내려간 모래시계가 작은 나무 탁자에 함께 놓여 있다.
- 소유자: skull = a skull-shaped carved object; hourglass = a partly drained hourglass; table = a small wooden table
- 관계: skull → rests_on → table; hourglass → stands_beside → skull
- 혼동: undead portrait; unrelated skull pattern on clothing
- 주장 한계: 물체와 병치는 보이지만 죽음에 대한 실제 관객 반응은 입증하지 않음.
- 출처: [S16](https://www.sciencemuseum.org.uk/objects-and-stories/memento-mori), [S46](https://www.nationalgallery.org.uk/paintings/glossary/memento-mori)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## O09 성취와 소멸의 병치

- 연결 키워드: Vanitas; Decadence
- 방식/우선순위: still / P0; 슬롯 제안: prop_placement, concept_tension
- EN: A jeweled crown, one spoiled fruit and an open book are arranged on the same dark cloth.
- KO: 보석 왕관과 상한 과일 하나, 펼친 책이 같은 어두운 천 위에 놓여 있다.
- 소유자: crown = a jeweled crown; fruit = one visibly spoiled fruit; book = an open book; cloth = a shared dark cloth
- 관계: crown → rests_on → cloth; fruit → beside → crown; book → behind → fruit
- 혼동: simple luxury still life; rot pasted on unrelated background
- 주장 한계: 하나의 선택형 정물; 매 vanitas에 왕관·과일·책 전부를 강제하지 않음.
- 출처: [S17](https://www.nationalgallery.org.uk/paintings/glossary/vanitas)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## O10 계급 표지와 죽음 인물의 행렬

- 연결 키워드: Danse macabre
- 방식/우선순위: versioned / P1; 슬롯 제안: relational_action, participant_role
- EN: A skeletal allegorical figure holds a crowned adult's hand, and that adult holds the hand of a plainly dressed worker.
- KO: 해골형 알레고리 인물이 왕관 쓴 성인의 손을 잡고 그 성인은 수수한 작업복 차림 성인의 손을 잡는다.
- 소유자: royal = one adult in a crown; worker = one adult in plain work clothes; death = a skeletal allegorical figure
- 관계: death → holds_hand_of → royal; royal → holds_hand_of → worker
- 혼동: three unrelated portraits; literal proof that all classes died
- 주장 한계: Met 특정 작품의 복제 아님; 계층 병치를 새로 저술한 알레고리 변주.
- 출처: [S39](https://www.metmuseum.org/art/collection/search/361665), [S16](https://www.sciencemuseum.org.uk/objects-and-stories/memento-mori)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## O11 가시 고리와 머리의 접촉

- 연결 키워드: Crown of thorns / Thorn motif
- 방식/우선순위: still / P1; 슬롯 제안: wearable_accessory, contact_point
- EN: A thin woven circlet rests on an adult head with small pointed twigs projecting outward.
- KO: 가는 엮은 고리가 성인의 머리에 놓이고 작은 뾰족한 가지들이 바깥으로 나온다.
- 소유자: adult = one adult head; circlet = a thin woven thorn circlet; thorns = small visible pointed twigs
- 관계: circlet → rests_on → adult; thorns → project_from → circlet
- 혼동: thorn pattern behind the head; full-body bondage
- 주장 한계: 가시 구조와 접촉만; 순교·통증·동의·상처·정통 종교 상징은 자동 확정하지 않음.
- 출처: [S12](https://www.metmuseum.org/essays/relics-and-reliquaries-in-medieval-christianity), [S16](https://www.sciencemuseum.org.uk/objects-and-stories/memento-mori)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## O12 부서진 후광의 양 끝

- 연결 키워드: Broken halo; Fallen angel
- 방식/우선순위: still / P0; 슬롯 제안: prop_state, composition
- EN: Behind a fictional adult figure's head, a luminous circular halo has a clear gap with both broken ends visible.
- KO: 가상 성인 인물의 머리 뒤 원형 발광 후광에 양쪽 부러진 끝과 그 사이 틈이 보인다.
- 소유자: head = a fictional adult figure's head; ring = a luminous circular halo; ends = two visible broken ring ends
- 관계: ring → behind → head; ends → belong_to → ring
- 혼동: crescent moon; ring simply hidden by hair
- 주장 한계: 단절된 고리의 창작 기호; 신성 상실·타락의 보편 상징이라고 주장하지 않음.
- 출처: [S08](https://www.musee-orsay.fr/en/program/whats-on/exhibitions/angel-odd-dark-romanticism-goya-max-ernst), [S26](https://www.merriam-webster.com/dictionary/numinous)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## R01 왕좌의 권위와 손상

- 연결 키워드: Decaying empire; Decayed grandeur
- 방식/우선순위: proxy / P0; 슬롯 제안: environment_detail, aftermath_trace
- EN: Gold leaf peels from a ceremonial throne above a visibly cracked pedestal.
- KO: 의전용 왕좌에서 금박이 벗겨지고 그 아래 받침대에 큰 균열이 보인다.
- 소유자: throne = a gilt ceremonial throne; gilding = peeling gold leaf; support = a visibly cracked pedestal
- 관계: gilding → peels_from → throne; support → supports → throne
- 혼동: wealth without damage; random rubble without surviving status object
- 주장 한계: 낡은 권위의 병치; 제국 규모·제도 부패·쇠망 과정은 불확정.
- 출처: [S03](https://joeabercrombie.com/the-value-of-grit/), [S08](https://www.musee-orsay.fr/en/program/whats-on/exhibitions/angel-odd-dark-romanticism-goya-max-ernst)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## R02 식량과 관문의 통제

- 연결 키워드: Systemic corruption; Institutional violence; Slavery; Debt bondage; Serfdom
- 방식/우선순위: proxy / P0; 슬롯 제안: social_cue, relational_action
- EN: An adult clerk holds an account ledger beside a locked grain bin while an adult worker waits opposite.
- KO: 성인 서기가 잠긴 곡물함 곁에서 장부를 들고 성인 노동자는 맞은편에서 기다린다.
- 소유자: clerk = one adult clerk; ledger = an open account ledger; grain = a locked grain bin; worker = one waiting adult worker
- 관계: clerk → holds → ledger; clerk → stands_beside → grain; worker → waits_opposite → clerk
- 혼동: ordinary paid transaction; chains treated as proof of slavery
- 주장 한계: 가시적인 접근 비대칭만; 자발성·부채·소유권·세습 신분은 별도 설정. 네 제도를 동치화하지 않음.
- 출처: [S36](https://www.ilo.org/resource/article/meanings-forced-labour), [S03](https://joeabercrombie.com/the-value-of-grit/)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## R03 왕위의 두 주장자

- 연결 키워드: Succession crisis; Usurpation; Court intrigue
- 방식/우선순위: proxy / P1; 슬롯 제안: participant_role, proxemics
- EN: One crowned adult stands to the left of an empty throne, while another adult holds a second crown on its right.
- KO: 빈 왕좌 왼쪽에 왕관 쓴 성인이 서고 오른쪽의 다른 성인은 두 번째 왕관을 들고 있다.
- 소유자: adult_a = one crowned adult; adult_b = a second adult holding another crown; throne = one empty throne
- 관계: adult_a → stands_left_of → throne; adult_b → stands_right_of → throne
- 혼동: a coronation assistant; separate thrones
- 주장 한계: 두 당사자·한 권좌의 공간 단서; 혈연·정통성·찬탈·적대 의도는 미입증.
- 출처: [S04](https://www.britishlibrary.cn/en/articles/gothic-motifs/), [S03](https://joeabercrombie.com/the-value-of-grit/)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## R04 의전과 강제력의 동시 배치

- 연결 키워드: Theocracy; Fanaticism; Inquisitor
- 방식/우선순위: proxy / P1; 슬롯 제안: social_cue, participant_role
- EN: An adult in invented ceremonial robes stands behind a table flanked by two armed adult guards, facing a seated adult witness.
- KO: 창작 의전복을 입은 성인이 책상 뒤에 서고 무장 성인 경비 둘이 양옆에 있으며 맞은편에 성인 증인이 앉아 있다.
- 소유자: official = an adult in invented ceremonial robes; guards = two armed adult guards; table = an interrogation table; witness = one seated adult witness
- 관계: official → stands_behind → table; guards → flank → official; witness → sits_opposite → official
- 혼동: ordinary hearing; real religion treated as inherently abusive
- 주장 한계: 의전·무력·자리 관계만; 실제 신정·정통성·고문·광신은 미입증.
- 출처: [S04](https://www.britishlibrary.cn/en/articles/gothic-motifs/), [S12](https://www.metmuseum.org/essays/relics-and-reliquaries-in-medieval-christianity)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## R05 계약 전사들의 수리와 보급

- 연결 키워드: Mercenary / Mercenary company; Perpetual war; Warlordism
- 방식/우선순위: proxy / P0; 슬롯 제안: attire_context, relational_action
- EN: One adult repairs a strap on another adult's mismatched armor beside a pile of repaired equipment.
- KO: 한 성인이 옆 성인의 서로 맞지 않는 갑옷 끈을 고치고 곁에 수리된 장비 무더기가 놓여 있다.
- 소유자: fighter = an adult armored fighter; companion = another adult repairing a strap; kit = a mismatched equipment pile
- 관계: companion → repairs_strap_of → fighter; kit → lies_beside → fighter
- 혼동: uniformed royal honor guard; grit as image grain only
- 주장 한계: 고용·보수·전쟁의 기간·군벌 소속은 문맥; 해진 장비는 악인 증거가 아님.
- 출처: [S03](https://joeabercrombie.com/the-value-of-grit/), [S13](https://www.metmuseum.org/essays/fashion-in-european-armor-1500-1600)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## R06 서약 표지의 폐기

- 연결 키워드: Oathbreaker; Fallen paladin
- 방식/우선순위: proxy / P0; 슬롯 제안: relational_action, prop_state
- EN: An armored adult releases a broken oath badge over a chapel floor.
- KO: 갑옷 입은 성인이 예배실 바닥 위에서 부서진 서약 배지를 손에서 놓는다.
- 소유자: adult = an armored adult; badge = a broken oath badge; floor = a chapel floor
- 관계: adult → drops → badge; badge → above → floor
- 혼동: accidental damage; black armor as automatic evil
- 주장 한계: 서약 위반·이전 신앙·해방인지 배신인지는 외형만으로 불확정. 배지 의미는 창작 설정.
- 출처: [S04](https://www.britishlibrary.cn/en/articles/gothic-motifs/), [S13](https://www.metmuseum.org/essays/fashion-in-european-armor-1500-1600)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## R07 괴물 수호자의 차폐 행동

- 연결 키워드: Monstrous protector; Hopepunk
- 방식/우선순위: still / P0; 슬롯 제안: relational_action, character_contrast
- EN: A large fictional nonhuman adult stands in front of a sheltering adult, holding a shield with several embedded arrows.
- KO: 큰 가상 비인간 성인이 몸을 숨긴 성인 앞에 서서 화살 여러 개가 박힌 방패를 들고 있다.
- 소유자: guardian = a large fictional nonhuman adult; refugee = an adult sheltering close behind; shield = a shield held by the guardian; arrows = several arrows embedded in the guardian's shield
- 관계: guardian → stands_in_front_of → refugee; arrows → embedded_in → shield; guardian → holds → shield
- 혼동: monster threatening the sheltered person; arrows mistaken as embedded in flesh
- 주장 한계: 보호 의도의 해석은 행동 단서에 한정; 방패와 신체의 소유/접점을 혼동하지 않음.
- 출처: [S02](https://www.grimdarkmagazine.com/defining-grimdark-fantasy-and-sf-moving-to-an-inclusive-future/), [S10](https://www.bfi.org.uk/lists/10-great-body-horror-films)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## R08 구원 비용의 병치

- 연결 키워드: Pyrrhic victory; Failed redemption
- 방식/우선순위: proxy / P0; 슬롯 제안: aftermath_trace, narrative_clue
- EN: Below a raised victory banner on a ruined gate, an exhausted adult supports another adult.
- KO: 무너진 성문의 올라간 승전 깃발 아래 지친 성인이 다른 성인을 부축한다.
- 소유자: banner = a raised victory banner; gate = a ruined city gate; survivor = an exhausted adult; assisted = a second adult being supported
- 관계: banner → hangs_above → gate; survivor → stands_beneath → banner; survivor → supports → assisted
- 혼동: generic defeat; banner alone proves victory
- 주장 한계: 승전·비용은 명시된 이야기와 함께 해석; 회복 불가능성·구원 실패의 시간 경과는 미입증.
- 출처: [S02](https://www.grimdarkmagazine.com/defining-grimdark-fantasy-and-sf-moving-to-an-inclusive-future/), [S03](https://joeabercrombie.com/the-value-of-grit/)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## R09 잊힌 망자를 안내하는 역할

- 연결 키워드: Psychopomp; Revenant
- 방식/우선순위: proxy / P1; 슬롯 제안: participant_role, relational_action
- EN: A cloaked fictional adult gestures toward a narrow lit doorway as a translucent adult figure faces it.
- KO: 망토 두른 가상 성인이 좁고 밝은 문을 가리키고 반투명한 성인 형상이 그 문을 바라본다.
- 소유자: guide = a cloaked fictional adult; traveler = a translucent adult figure; threshold = a narrow illuminated doorway
- 관계: guide → gestures_toward → threshold; traveler → faces → threshold
- 혼동: executioner; translucence caused by glass reflection
- 주장 한계: 안내 관계의 선택안; 죽음·사후세계·영혼 신원·살해 행위는 문맥.
- 출처: [S24](https://www.merriam-webster.com/dictionary/psychopomp)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## R10 영혼 용기와 작품별 리치

- 연결 키워드: Lich; Soul vessel
- 방식/우선순위: versioned / P1; 슬롯 제안: prop_placement, narrative_clue
- EN: A skeletal fictional mage faces a closed small casket resting on a separate stone pedestal.
- KO: 해골형 가상 마법사가 별개 돌 받침대 위의 닫힌 작은 함을 마주한다.
- 소유자: mage = a skeletal fictional mage; casket = a closed small casket; pedestal = a separate stone pedestal
- 관계: casket → rests_on → pedestal; mage → faces → casket
- 혼동: every skeleton is a lich; ordinary jewelry box proves immortality
- 주장 한계: 2014 D&D의 용기/재생은 원전 설정; 이 배치로 영혼 보관·재생 주기를 입증하지 않음.
- 출처: [S35](https://www.dndbeyond.com/monsters/16943-lich)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## R11 귀환 망자의 묘 경계

- 연결 키워드: Draugr; Undead; Wight; Death knight
- 방식/우선순위: versioned / P1; 슬롯 제안: participant_role, body_pose
- EN: A bulky fictional armored adult stands just inside a broken door in a burial mound.
- KO: 커다란 가상 갑옷 성인이 봉분의 부서진 문 바로 안쪽에 서 있다.
- 소유자: figure = a bulky fictional armored adult; mound = a burial mound; door = a broken mound door
- 관계: figure → stands_inside → door; door → opens_in → mound
- 혼동: living tomb guard; one game skin used as all Norse folklore
- 주장 한계: 묘와 무장 인물의 위치만; 사망·귀환·종족·저주를 가시 외형에서 확정하지 않음.
- 출처: [S34](https://sites.nd.edu/manuscript-studies/tag/draugr/), [S23](https://www.merriam-webster.com/dictionary/wight)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## R12 포크 호러의 공동체 경계

- 연결 키워드: Folk horror; Secret cult
- 방식/우선순위: proxy / P0; 슬롯 제안: proxemics, social_cue
- EN: A lone adult visitor stands outside a rough circle of adults where a narrow field path ends.
- KO: 들판의 좁은 길이 끝나는 곳에서 성인 방문자 하나가 성인들의 성긴 원 바깥에 서 있다.
- 소유자: circle = several adults in a rough standing circle; visitor = one separate adult visitor; path = a single narrow approach through fields
- 관계: visitor → stands_outside → circle; path → ends_at → circle
- 혼동: ordinary community dance; all rural rites are sinister
- 주장 한계: 고립·포위의 선택형 배열; 범죄·비밀 교리·희생은 미입증.
- 출처: [S09](https://www.bfi.org.uk/features/where-begin-with-folk-horror)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## M01 망자와의 질문 관계

- 연결 키워드: Necromancy; Ritual magic
- 방식/우선순위: proxy / P0; 슬롯 제안: relational_action, gaze_target
- EN: A fictional adult ritualist faces one translucent adult apparition inside a drawn floor ring.
- KO: 가상 성인 의식자가 바닥의 그린 고리 안에 선 반투명 성인 환영 하나를 마주한다.
- 소유자: caster = a living fictional adult ritualist; apparition = a single translucent adult apparition; circle = a drawn floor ring
- 관계: caster → faces → apparition; apparition → stands_inside → circle
- 혼동: graveyard alone; all necromancy is a zombie army
- 주장 한계: 죽음·실제 대화·점술·부활 성공은 명시된 허구 설정; 인과 연결은 정지 컷만으로 미입증.
- 출처: [S22](https://www.merriam-webster.com/dictionary/necromancy), [S25](https://www.merriam-webster.com/dictionary/grimoire)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## M02 혈마법의 매개와 도착점

- 연결 키워드: Blood magic; Hemomancy
- 방식/우선순위: proxy / P0; 슬롯 제안: liquid_inclusion, surreal_physics_detail
- EN: A narrow filament of fictional blood rises from a shallow bowl and touches an invented raised sigil.
- KO: 가상 피가 든 얕은 그릇에서 붉은 액체의 가는 줄이 올라가 창작한 도드라진 인장에 닿는다.
- 소유자: bowl = a shallow bowl of fictional blood; filament = a narrow red liquid filament; sigil = an invented raised sigil
- 관계: filament → rises_from → bowl; filament → touches → sigil
- 혼동: ambient red glow; disconnected droplets
- 주장 한계: 매개-이동-대상 연결의 허구안; 혈액의 실제 화학·희생자·마법의 효력·보편 학파는 미입증.
- 출처: [S25](https://www.merriam-webster.com/dictionary/grimoire), [S31](https://www.merriam-webster.com/dictionary/sigil)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## M03 영혼 결박의 양쪽 접점

- 연결 키워드: Soulbinding; Soul vessel
- 방식/우선순위: proxy / P0; 슬롯 제안: anatomical_connection, surreal_physics_detail
- EN: A luminous thread touches a translucent fictional adult's chest and enters the opening of a small vessel.
- KO: 발광 실이 반투명 가상 성인의 가슴에 닿아 작은 용기의 입구 안으로 들어간다.
- 소유자: figure = a translucent fictional adult; thread = a luminous thread; vessel = a small hollow vessel
- 관계: thread → touches → figure; thread → enters → vessel
- 혼동: necklace cord; separate lights with no continuous connection
- 주장 한계: 양끝과 연속 경로만; 영혼의 실재·소유권·강제성·불사는 미입증.
- 출처: [S35](https://www.dndbeyond.com/monsters/16943-lich), [S24](https://www.merriam-webster.com/dictionary/psychopomp)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## M04 결계의 경계 접촉

- 연결 키워드: Ward / Seal
- 방식/우선순위: still / P0; 슬롯 제안: surreal_physics_detail, contact_point
- EN: A translucent plane spans a stone doorway and dimples at the contact point of an adult palm.
- KO: 반투명 평면이 돌문 전체를 가로막고 성인 손바닥이 닿는 지점에서 움푹 들어간다.
- 소유자: arch = a stone doorway; membrane = a translucent plane across the doorway; hand = an adult palm pressing on that plane
- 관계: membrane → spans → arch; hand → contacts → membrane
- 혼동: ordinary glass pane; glow without a barrier surface
- 주장 한계: 변형되는 허구 경계만; 실제 보호 범위·영속·차단 성공은 불확정.
- 출처: [S31](https://www.merriam-webster.com/dictionary/sigil), [S33](https://www.merriam-webster.com/dictionary/theurgy)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## M05 빙의의 그림자 불일치

- 연결 키워드: Possession; The uncanny
- 방식/우선순위: proxy / P1; 슬롯 제안: shadow_relation, body_pose
- EN: Under one exposed lamp, an adult keeps both arms down while the connected wall shadow raises one arm.
- KO: 노출된 등 하나 아래 성인은 양팔을 내리지만 연결된 벽 그림자는 한 팔을 든다.
- 소유자: body = an adult standing with both arms down; lamp = one exposed lamp; wall = one continuous wall; shadow = a matching shadow with one arm raised
- 관계: lamp → illuminates → body; shadow → lies_on → wall; shadow → corresponds_to → body
- 혼동: two light sources; second caster outside the frame
- 주장 한계: 몸/광원/수광면의 기하 모순만; 빙의·악의·행동 변화의 원인은 판정하지 않음.
- 출처: [S04](https://www.britishlibrary.cn/en/articles/gothic-motifs/)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## M06 융합 경계의 조직 연속

- 연결 키워드: Body fusion; Fleshcraft / Fleshcrafting
- 방식/우선순위: still / P0; 슬롯 제안: anatomical_connection, body_form
- EN: Two fictional adult torsos are joined by one continuous organic tissue bridge with both junctions visible.
- KO: 두 가상 성인 몸통이 하나의 연속 유기 조직 다리로 이어지고 양쪽 접합이 보인다.
- 소유자: body_a = one fictional adult torso; body_b = a second fictional adult torso; bridge = a continuous organic tissue bridge
- 관계: bridge → joins → body_a; bridge → joins → body_b
- 혼동: two people touching; cloth joining bodies
- 주장 한계: 조직 연결의 허구 형태; 인격 수·수술·유전·통증·융합 경과는 미입증.
- 출처: [S10](https://www.bfi.org.uk/lists/10-great-body-horror-films)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## M07 착용 갑옷과 피부의 생체 접점

- 연결 키워드: Living armor
- 방식/우선순위: still / P0; 슬롯 제안: anatomical_connection, garment_detail
- EN: Short organic tendrils emerge from the inner rim of an adult fictional wearer's forearm plate and meet the same wearer's exposed skin.
- KO: 가상 성인 착용자의 팔 갑옷 안쪽 가장자리에서 짧은 유기 덩굴이 나와 같은 착용자의 드러난 팔 피부에 닿는다.
- 소유자: wearer = an adult fictional wearer; plate = one curved armor plate; tendrils = short organic tendrils emerging from its inner rim; skin = the wearer's exposed forearm
- 관계: plate → worn_by → wearer; tendrils → emerge_from → plate; tendrils → meet → skin
- 혼동: ornament attached only outside armor; separate pet tentacle
- 주장 한계: 같은 착용자·판·피부의 접점 필요; 살아 있음·영양 교환·통제·벗을 수 없음은 별도 설정.
- 출처: [S10](https://www.bfi.org.uk/lists/10-great-body-horror-films), [S13](https://www.metmuseum.org/essays/fashion-in-european-armor-1500-1600)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## M08 건축 재료와 유기 조직의 연결

- 연결 키워드: Living architecture
- 방식/우선순위: still / P0; 슬롯 제안: object_structure, anatomical_connection
- EN: A continuous ribbed organic lining follows a masonry doorway and folds into a flexible tissue hinge at its edge.
- KO: 연속된 주름진 유기 내피가 석조 문틀을 따라가 가장자리의 유연한 조직 경첩으로 이어진다.
- 소유자: doorway = a masonry doorway; tissue = one continuous ribbed organic lining; hinge = a flexible tissue fold at the door edge
- 관계: tissue → lines → doorway; hinge → continues_from → tissue
- 혼동: vines covering facade; stone ribs only
- 주장 한계: 재료 전환·연결만; 건물의 호흡·소화·학습·생물학적 기능은 미입증.
- 출처: [S10](https://www.bfi.org.uk/lists/10-great-body-horror-films), [S07](https://www.jeffvandermeer.com/blog/2007/09/27/working-definition-of-new-weird)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## M09 숙주와 기생체의 부착점

- 연결 키워드: Parasitism; Infestation
- 방식/우선순위: still / P1; 슬롯 제안: anatomical_connection, species_marker
- EN: A smaller distinct organism attaches to a fictional adult creature's shoulder at a clearly visible contact ring.
- KO: 작은 별개 생물이 가상 성인 생물의 어깨에 분명한 접촉 고리로 붙어 있다.
- 소유자: host = a fictional adult creature; parasite = a smaller distinct organism; attachment = a visible contact ring on the host's shoulder
- 관계: parasite → attaches_at → attachment; attachment → belongs_to → host
- 혼동: brooch; organism merely sitting nearby
- 주장 한계: 부착만 관찰; 영양 의존·기생 피해·전염·대량 침입은 이 한 예로 입증하지 않음.
- 출처: [S10](https://www.bfi.org.uk/lists/10-great-body-horror-films)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## M10 변형 중간 형태

- 연결 키워드: Metamorphosis; Mutation; Werewolf / Lycanthropy
- 방식/우선순위: proxy / P1; 슬롯 제안: transformation_stage, body_form
- EN: A fictional adult's forearm continues into a human-shaped palm with elongated furred digits.
- KO: 가상 성인의 팔이 사람 형태 손바닥으로 이어지고 그 손바닥에서 길쭉하고 털 난 손가락이 나온다.
- 소유자: arm = a fictional adult's forearm; hand = a human-shaped palm continuous with it; digits = elongated furred digits continuous with that palm
- 관계: hand → continuous_with → arm; digits → grow_from → hand
- 혼동: fur glove; two different hands
- 주장 한계: 한 시점의 혼합 형태; 이전/이후 변신·생물학적 돌연변이·늑대 종·통제 상실은 미입증.
- 출처: [S10](https://www.bfi.org.uk/lists/10-great-body-horror-films)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## M11 신체 손상과 떨어진 부분

- 연결 키워드: Mutilation; Dismemberment; Gore
- 방식/우선순위: still / P1; 슬롯 제안: body_form, aftermath_trace
- EN: A clearly fictional anatomical adult figure has one matching hand resting separately beside its forearm with a visible gap.
- KO: 명백한 가상 성인 해부 모형의 손 하나가 팔 곁에 분리되어 있고 사이의 틈이 보인다.
- 소유자: figure = a clearly fictional anatomical adult figure; hand = a separate matching anatomical hand; forearm = the figure's matching forearm
- 관계: forearm → belongs_to → figure; hand → separate_from → forearm
- 혼동: hand hidden by sleeve; detached glove
- 주장 한계: 교육용 허구 형태안; 실제 절단 행위·원인·사망·고통은 미입증. 분리된 부분과 해당 팔을 함께 관찰.
- 출처: [S10](https://www.bfi.org.uk/lists/10-great-body-horror-films)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## M12 흐린 공기의 수광과 배경

- 연결 키워드: Miasma; Blight; Blighted
- 방식/우선순위: proxy / P0; 슬롯 제안: atmospheric_medium, environment_detail
- EN: A lateral beam passes through low haze around wilted crop stems.
- KO: 옆에서 든 빛줄기가 시든 작물 줄기 주변의 낮은 연무를 통과한다.
- 소유자: haze = a low thin visible haze; plants = wilted crop stems; light = a lateral beam passing through haze
- 관계: haze → surrounds → plants; light → passes_through → haze
- 혼동: ordinary dawn fog; green color treated as proof of poison
- 주장 한계: 연무와 시듦의 동시 외형만; 독성·감염·악취·초자연 원인은 미입증.
- 출처: [S28](https://www.merriam-webster.com/dictionary/miasma)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## F01 부피를 만드는 명암

- 연결 키워드: Chiaroscuro
- 방식/우선순위: still / P0; 슬롯 제안: lighting, light_direction
- EN: One oblique key light models an adult face, with a graded shadow turning around the cheek.
- KO: 사선 주광 하나가 성인의 얼굴을 비추고 볼을 돌아가는 점진적인 그림자가 부피를 만든다.
- 소유자: face = an adult face; key = one oblique key light; shadow = a graded shadow across the cheek
- 관계: key → illuminates → face; shadow → models_volume_of → face
- 혼동: flat silhouette; dark image with no modeled volume
- 주장 한계: 명암과 형태의 관계; 고딕 장르·공포·악인 성격은 별개.
- 출처: [S18](https://www.nationalgallery.org.uk/paintings/glossary/chiaroscuro)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## F02 어둠이 지배하는 화면의 국소 빛

- 연결 키워드: Tenebrism; Tenebrous
- 방식/우선순위: still / P0; 슬롯 제안: lighting, visual_hierarchy
- EN: Only localized highlights on one adult's face and hands emerge clearly from a predominantly dark setting.
- KO: 대부분 어두운 공간에서 한 성인의 얼굴과 손에 모인 하이라이트가 분명하게 드러난다.
- 소유자: adult = one adult; field = a predominantly dark setting; hands = an adult's localized illuminated hands; face = the same adult's localized illuminated face
- 관계: hands → stand_out_against → field; face → stand_out_against → field; hands → belong_to → adult; face → belongs_to → adult
- 혼동: uniform underexposure; bright background larger than the dark setting
- 주장 한계: 명암 면적/중심 관계를 검토; required endpoint를 숨겨도 되는 허가 아님.
- 출처: [S19](https://www.nationalgallery.org.uk/paintings/glossary/tenebrism)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## F03 구리빛 바탕의 녹색 층

- 연결 키워드: Patina / Verdigris
- 방식/우선순위: still / P0; 슬롯 제안: surface_material, texture
- EN: Patchy matte green layers cover a copper-colored fixture while a worn edge exposes brighter metal.
- KO: 구리빛 금속 기물에 얼룩진 무광 녹색 층이 덮이고 닳은 가장자리에는 밝은 금속이 드러난다.
- 소유자: metal = a copper-colored metal fixture; layer = patchy matte green surface areas; edge = a worn bright metal edge
- 관계: layer → lies_on → metal; edge → belongs_to → metal
- 혼동: green paint; orange iron rust
- 주장 한계: 외형 표현만; 화학 조성·부식 속도·연대·안정성은 픽셀로 확정하지 않음.
- 출처: [S20](https://www.canada.ca/en/conservation-institute/services/preventive-conservation/guidelines-collections/metal-objects.html)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## F04 사용 흔적의 출발과 수광면

- 연결 키워드: Wax drippings / Soot / Dust
- 방식/우선순위: still / P0; 슬롯 제안: aftermath_trace, prop_state
- EN: Hardened wax runs down a partly consumed candle onto its holder, below a localized dark deposit on the wall.
- KO: 일부 타버린 촛대의 초에서 굳은 촛농이 받침으로 흘러 모이고 뒤 벽에는 국소 검은 흔적이 있다.
- 소유자: candle = a partly consumed candle; wax = hardened wax rivulets; holder = a metal candleholder; wall = a wall with a localized dark deposit
- 관계: wax → runs_down → candle; wax → collects_on → holder; wall → behind → candle
- 혼동: generic dirt overlay; wax floating apart from source
- 주장 한계: 촛농·흔적의 위치만; 정확한 연소 시간·재 화학·원인 단정은 미입증.
- 출처: [S20](https://www.canada.ca/en/conservation-institute/services/preventive-conservation/guidelines-collections/metal-objects.html), [S16](https://www.sciencemuseum.org.uk/objects-and-stories/memento-mori)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## F05 지면 가까운 박명

- 연결 키워드: Crepuscular
- 방식/우선순위: still / P1; 슬롯 제안: time_of_day, light_color
- EN: An adult silhouette stands against a faint warm horizon band below a cooler darkening sky.
- KO: 성인의 실루엣이 차갑게 어두워지는 하늘 아래 희미한 따뜻한 수평선 띠를 배경으로 선다.
- 소유자: horizon = a faint warm horizon band; sky = a cooler darkening sky; figure = an adult silhouette
- 관계: horizon → below → sky; figure → against → horizon
- 혼동: night with bright artificial floodlights; crepuscular means necessarily scary
- 주장 한계: 박명의 선택형 빛 배치; 촬영 시각·공포 정서는 별도.
- 출처: [S21](https://science.nasa.gov/moon/eclipses/)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## F06 월식의 붉은 원반

- 연결 키워드: Eclipse / Blood-red moon
- 방식/우선순위: still / P0; 슬롯 제안: background_element, light_color
- EN: A reddish lunar disc hangs in a dark sky above a crisp roofline.
- KO: 또렷한 지붕선 위 어두운 하늘에 붉은 달 원반이 떠 있다.
- 소유자: moon = a reddish lunar disc; sky = a dark sky; roof = one crisp roofline
- 관계: moon → appears_above → roof; moon → set_against → sky
- 혼동: solar eclipse with bright corona; all scene surfaces painted red
- 주장 한계: 붉은 달의 가시 외형; 실제 월식 여부·궤도·초자연 징조는 별도 근거. 일식은 별도 branch 필요.
- 출처: [S21](https://science.nasa.gov/moon/eclipses/)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## F07 후광과 얼굴 사이의 거리

- 연결 키워드: Numinous; Apotheosis
- 방식/우선순위: proxy / P1; 슬롯 제안: composition, light_shape
- EN: A narrow circular backlight sits behind a fictional adult's head with a visible gap of air between them.
- KO: 가상 성인의 머리 뒤에 가는 원형 역광이 놓이고 머리와 빛 사이에 빈 공기 틈이 보인다.
- 소유자: figure = a fictional adult figure; light = a narrow circular backlight; space = a visible air gap behind the head
- 관계: light → behind → figure; space → behind → figure; space → in_front_of → light
- 혼동: jewelry resting on hair; divinity inferred from brightness
- 주장 한계: 빛과 거리만; 신격화·실제 신성·누미노스 감정은 미입증.
- 출처: [S26](https://www.merriam-webster.com/dictionary/numinous), [S12](https://www.metmuseum.org/essays/relics-and-reliquaries-in-medieval-christianity)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## F08 섬뜩한 분신의 실제 분리

- 연결 키워드: The uncanny; Wraith
- 방식/우선순위: proxy / P1; 슬롯 제안: subject_count, reflection_logic
- EN: Two similarly dressed adults stand apart on the same floor while a small wall mirror remains visible behind only one of them.
- KO: 비슷한 옷차림의 성인 둘이 같은 바닥에 떨어져 서고 작은 벽거울은 한 사람 뒤에만 보인다.
- 소유자: adult_a = one adult; adult_b = a second similarly dressed adult; floor = one continuous floor; mirror = a small visible wall mirror
- 관계: adult_a → stands_on → floor; adult_b → stands_on → floor; mirror → behind → adult_a
- 혼동: single person and mirror reflection; identical twins imply evil
- 주장 한계: 실제 개체 수와 반사 후보를 구분하는 창작안; 초자연 분신·악의·혈연은 미입증.
- 출처: [S04](https://www.britishlibrary.cn/en/articles/gothic-motifs/)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## F09 쇠약해 보이는 외형

- 연결 키워드: Pallid; Cadaverous; Emaciated
- 방식/우선순위: proxy / P1; 슬롯 제안: complexion_coverage, silhouette_proportion
- EN: Pronounced cheek hollows and a loose plain garment give a fictional adult a gaunt appearance.
- KO: 가상 성인의 두드러진 볼 패임과 헐거운 수수한 옷이 수척한 외형을 만든다.
- 소유자: adult = a fictional adult face and upper body; cheeks = pronounced cheek hollows; cloth = a loose plain garment
- 관계: cheeks → belong_to → adult; cloth → worn_by → adult
- 혼동: pale makeup alone; clothes imply starvation
- 주장 한계: 외형만; 영양 상태·진단·실제 사망·인종·의도는 판정하지 않음. pallid와 emaciated는 별도 branch로 분리 검토.
- 출처: [S10](https://www.bfi.org.uk/lists/10-great-body-horror-films)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## F10 황량한 공간의 남은 생활 사물

- 연결 키워드: Bleak; Desolate; Forsaken
- 방식/우선순위: proxy / P1; 슬롯 제안: space_condition, visual_density
- EN: One collapsed market stall and an empty bowl remain in an open unoccupied square.
- KO: 넓고 사람 없는 광장에 무너진 시장 좌판 하나와 빈 그릇 하나가 남아 있다.
- 소유자: square = an open unoccupied square; stall = one collapsed market stall; bowl = one empty bowl
- 관계: stall → stands_in → square; bowl → rests_beside → stall
- 혼동: ordinary off-hours market; low saturation only
- 주장 한계: 비어 있음의 시야 범위만; 실제 버림·희망 부재·기근·역사는 미입증.
- 출처: [S03](https://joeabercrombie.com/the-value-of-grit/), [S08](https://www.musee-orsay.fr/en/program/whats-on/exhibitions/angel-odd-dark-romanticism-goya-max-ernst)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## F11 시선과 비대칭 거리

- 연결 키워드: Sinister; Baleful; Ominous; Dread
- 방식/우선순위: proxy / P1; 슬롯 제안: gaze_target, proxemics
- EN: A partly open door separates an adult near the frame edge from a distant adult looking toward them.
- KO: 화면 가장자리 가까운 성인과 그를 바라보는 먼 성인 사이에 반쯤 열린 문이 있다.
- 소유자: observer = one adult near the frame edge; door = a partly open door; watcher = a distant adult looking toward the observer
- 관계: watcher → looks_toward → observer; observer → in_front_of → door; watcher → behind → door
- 혼동: friendly greeting; evil inferred from eye shape
- 주장 한계: 관계·가림의 선택안; 악의·미래 사건·실제 관객 공포는 미입증. 문 양쪽의 두 인물이 같은 시야에 있어야 함.
- 출처: [S04](https://www.britishlibrary.cn/en/articles/gothic-motifs/)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## F12 장례 행렬의 보폭과 운반

- 연결 키워드: Funereal; Sepulchral
- 방식/우선순위: proxy / P1; 슬롯 제안: relational_action, occasion_context
- EN: Four clothed adult bearers carry one covered bier along a narrow stone path.
- KO: 옷 입은 성인 운반자 넷이 좁은 돌길 위에서 덮인 들것 하나를 함께 든다.
- 소유자: bearers = four fully clothed adult bearers; bier = one covered bier; path = a narrow stone path
- 관계: bearers → carry → bier; bier → above → path
- 혼동: festival palanquin; empty coffin proves death
- 주장 한계: 운반 수·접점·피복물만; 실제 시신·애도·침묵은 설정/다른 감각.
- 출처: [S16](https://www.sciencemuseum.org.uk/objects-and-stories/memento-mori), [S39](https://www.metmuseum.org/art/collection/search/361665)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## X01 성인의 시선과 닿지 않은 손

- 연결 키워드: Eroticism; Erotic horror; Monstrous desire / Monster attraction
- 방식/우선순위: proxy / P1; 슬롯 제안: gaze_engagement, proxemics
- EN: A clothed adult human and a clothed fictional nonhuman adult look toward each other with their visible hands close but not touching.
- KO: 옷 입은 성인 인간과 옷 입은 가상 비인간 성인이 마주 보고 드러난 손들은 가깝지만 닿지 않는다.
- 소유자: human = one clothed adult human; other = one clothed fictional nonhuman adult; human_hand = the human adult's visible hand; other_hand = the nonhuman adult's visible hand
- 관계: human → looks_at → other; other → looks_at → human; human_hand → belongs_to → human; other_hand → belongs_to → other; human_hand → close_to_without_touching → other_hand
- 혼동: predatory attack; proximity proves desire
- 주장 한계: 근접·시선만; 욕망·성적 행위·동의·강압·관계 성립은 픽셀로 확정하지 않음. 두 사람의 손 소유를 각각 보존.
- 출처: [S11](https://www.bfi.org.uk/lists/10-great-erotic-horror-films), [S37](https://ncsfreedom.org/key-programs-2/consent-counts/)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## X02 페티시 재질과 봉제

- 연결 키워드: Fetish aesthetic
- 방식/우선순위: still / P1; 슬롯 제안: fetish_styling, garment_detail
- EN: A fitted glossy glove on a clothed adult has a raised stitched seam and a rigid cuff belonging to the same glove.
- KO: 옷 입은 성인의 잘 맞는 광택 장갑에 도드라진 봉제선이 있고 같은 장갑에 단단한 커프가 붙어 있다.
- 소유자: adult = one clothed adult; glove = a fitted glossy glove; seam = a raised stitched seam; cuff = a rigid cuff on that glove
- 관계: glove → worn_by → adult; seam → runs_along → glove; cuff → belongs_to → glove
- 혼동: generic black garment; gloss proves leather
- 주장 한계: 재질과 복장만; 욕망·동의·성적 지향·가학성은 미입증; 실제 소재 화학도 미확정.
- 출처: [S11](https://www.bfi.org.uk/lists/10-great-erotic-horror-films)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## X03 군중의 제의적 박자

- 연결 키워드: Orgiastic rite
- 방식/우선순위: proxy / P1; 슬롯 제안: relational_action, crowd_density
- EN: Several clothed adult dancers stand around a marked floor ring as an adult drummer faces them.
- KO: 옷 입은 성인 무용수 여럿이 바닥 표시 고리 둘레에 서고 성인 북 연주자가 그들을 마주한다.
- 소유자: adults = several clothed adult dancers; ring = a marked floor ring; drummer = one adult with a hand drum
- 관계: adults → stand_around → ring; drummer → faces → adults
- 혼동: all group rites imply sex; mere crowd
- 주장 한계: 모임과 자세의 한 시점만; 소리·집단 도취·성행위·자발성은 입증하지 않음.
- 출처: [S09](https://www.bfi.org.uk/features/where-begin-with-folk-horror), [S11](https://www.bfi.org.uk/lists/10-great-erotic-horror-films)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## X04 서로 다른 권력의 혼례 소품

- 연결 키워드: Forced marriage; Court intrigue
- 방식/우선순위: proxy / P1; 슬롯 제안: social_cue, prop_placement
- EN: Two clothed adults face each other beside a ring tray while a third adult holds one wedding contract behind the tray.
- KO: 옷 입은 성인 둘이 반지 쟁반 곁에서 마주 서고 세 번째 성인이 쟁반 뒤에서 혼인 문서 하나를 들고 있다.
- 소유자: adult_a = one clothed adult; adult_b = a second clothed adult; officiant = a third clothed adult; contract = one wedding contract; tray = a ring tray; ring = one ring
- 관계: adult_a → faces → adult_b; officiant → holds → contract; ring → rests_on → tray; contract → behind → tray
- 혼동: arranged marriage automatically coerced; uneasy face proves refusal
- 주장 한계: 혼인 정황만; 자유로운 동의의 유무·법적 성립은 별도. 문서·반지·쟁반·세 번째 인물의 소유 관계를 분리.
- 출처: [S04](https://www.britishlibrary.cn/en/articles/gothic-motifs/), [S38](https://www.unfpa.org/swp2022/risk)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## X05 상해와 강압의 의미 경계

- 연결 키워드: Torture; Sexual violence; Sexual slavery; Sadism / Masochism; BDSM
- 방식/우선순위: context / P0; 슬롯 제안: situation_context
- EN: Context record only; no visual realization is proposed by this card.
- KO: 동의·강압·착취·고통에서의 만족은 요청자가 명시한 문맥으로 보존한다.
- 소유자: context = explicit requester-authored facts about consent and coercion
- 관계: context → requires → context
- 혼동: cuffs prove consent; tears prove sexual violence; black leather proves sadism
- 주장 한계: 해당 행위를 서로 동치화하지 않고 taxonomy와 비추론 회귀에 반영. 긍정 시각 후보 아님.
- 출처: [S36](https://www.ilo.org/resource/article/meanings-forced-labour), [S37](https://ncsfreedom.org/key-programs-2/consent-counts/), [S41](https://ncsfreedom.org/wp-content/uploads/2022/01/Best-Practices-for-Consent-to-Kink.pdf)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## X06 친족과 죽음과 동물의 분류

- 연결 키워드: Incest; Necrophilia; Bestiality
- 방식/우선순위: context / P0; 슬롯 제안: situation_context
- EN: Context record only; no visual realization is proposed by this card.
- KO: 혈연·시신 지위·실제 동물과 가상 인물의 구별은 명시한 서사 정보로 보존한다.
- 소유자: context = explicit narrative relations and entity status
- 관계: context → requires → context
- 혼동: similar faces prove kinship; grief proves necrophilia; animal-shaped adult equals animal
- 주장 한계: 외형의 근접·닮음·종족 표지만으로 세 개념을 판정하지 않음. 긍정 시각 후보 아님.
- 출처: [S42](https://www.merriam-webster.com/dictionary/necrophilia), [S43](https://www.merriam-webster.com/dictionary/incest), [S44](https://www.merriam-webster.com/dictionary/bestiality)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## X07 통제된 생식과 마법의 금기

- 연결 키워드: Reproductive coercion; Sex magic; Sexual transgression
- 방식/우선순위: context / P0; 슬롯 제안: situation_context
- EN: Context record only; no visual realization is proposed by this card.
- KO: 생식 자율성 침해와 허구의 성마법·사회적 금기는 각각 다른 문맥 필드로 다룬다.
- 소유자: context = explicitly authored autonomy and fictional magic rules
- 관계: context → requires → context
- 혼동: pregnancy proves coercion; ritual circle implies sex
- 주장 한계: 임신·의식·복장 외형은 강요나 성행위의 증거 아님. 긍정 시각 후보 아님.
- 출처: [S06](https://epublications.marquette.edu/gothic_transgression/), [S38](https://www.unfpa.org/swp2022/risk)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

## X08 연애 및 복수 서사의 시간 축

- 연결 키워드: Dark romance; Psychosexual horror; Rape-revenge
- 방식/우선순위: context / P0; 슬롯 제안: narrative_core
- EN: Context record only; no visual realization is proposed by this card.
- KO: 관계 중심 서사·심리성적 갈등·피해 이후 복수의 순서는 텍스트/연속 매체에서 검토한다.
- 소유자: context = explicit narrative sequence and perspective
- 관계: context → requires → context
- 혼동: one embrace proves romance; one armed survivor proves rape-revenge
- 주장 한계: 정지 컷을 다단계 서사·치유·합의의 완결 증거로 승격하지 않음. 긍정 시각 후보 아님.
- 출처: [S04](https://www.britishlibrary.cn/en/articles/gothic-motifs/), [S11](https://www.bfi.org.uk/lists/10-great-erotic-horror-films)
- 검토: 각 성분과 모든 관계를 함께 확인. 가림/부분 구현은 통과가 아니다. 문맥 카드는 픽셀 합격 대상이 아니다.

