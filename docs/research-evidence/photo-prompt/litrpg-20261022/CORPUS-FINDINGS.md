# 현재 코퍼스와 연구 초안의 비교

조사 시점의 manifest는 69개 모듈, 19,813개 고유 레코드와 14,287개 바인딩을 가졌다. 종류는 visual_option 13,274 / visual_profile 3,834 / relationship_mechanism 135 / diagnostic 363 / visual_bundle 2,204 / relationship_concept 3이다. 모두를 단일 양성 후보 수라고 부르지 않는다.

`content`와 realization의 en/ko/definition/phrase/composition/runtime 필드만 읽었다. aliases·tags·research_semantics·negative metadata는 검색하지 않았다. 짧은 문구의 literal 일치는 전체 의미·중복 여부·현재 H-F2 노출·원전 적격성을 증명하지 않는다. 0건도 의미 부재의 증거가 아니다.

## 의미상 구체적으로 비교한 기존 8개

아래 D 번호는 기존 모듈의 연구 번호다. 전체 레코드·조건·효과·바인딩을 [reviewed-litrpg-sources.json](reviewed-litrpg-sources.json)에 보관했다. 모두 `requires_adult_context:true`이고 원문의 성인 인물 조건을 지워 재사용하지 않는다. 아래 판단은 언어·의미 대조이며 native source qualification이 아니다.

| 기존 | 현재 양성 원문과 슬롯 | 연구안 관계 | 반영 판단 |
|---|---|---|---|
| D01 `cand_e913530dd23453cc8a68cd95e0387bda` | 성인이 종이 시트의 큰 세 칸 중 하나에 연필을 댐. prop/hand_pose | U03/I01은 카드 행·자원 구획까지 구분 | 기존 종이·지지·연필 관계를 exact 대안으로 재사용 가능. 일반 전자 상태창으로 확대하지 않음 |
| D02 `cand_a03dfdc7f109589e8b910552779c66b2` | HP 100 손목 화면과 붕대 손의 병치. visible_text/narrative_clue | I02/X04/X17의 표시·신체·진실성 경계 | 비교·회귀 방지 사례로 유지. 자원 분리 패널 자체를 이미 포괄한다고 보지 않음 |
| D03 `cand_5d262f53dda7553b8a678afca482d252` | 두 물리 분기·자물쇠·손끝. object_structure/prop_state | I05/I06은 해금 조건·직업 분화 | 물리 자물쇠 포함 전체 대안은 재사용 가능. 텍스트 요구 조건·활성 상태는 검토할 차이 |
| D04 `cand_3c19999f8e145938a273beff18647926` | 과제판 삼각 표식→소포 봉인과 가리키는 성인. prop_placement/narrative_clue | Q01 목표–물증 대응 | 거의 겹치는 기반. 삼각형·손짓·인물을 유지할 수 있으면 exact 재사용 우선. 조건 삭제형 일반화 금지 |
| D05 `cand_1aaec75ac39251e89189c49aea01a3a5` | 세 홈 트레이의 초상 타일과 옆 성인. object_structure/image_detail | Q04/Q05는 아이템 칸 점유·신체 슬롯 | 초상·실제 인물 대응과 inventory 공간 배분은 다른 관계. 동의어 추가로 합치지 않음 |
| D06 `cand_4dc74917d3815ab9b8c4a149abfe29ad` | 손목 표식과 별도 화면 아이콘의 모양 대응. body_marking/image_detail | C04/E01은 상태의 정확한 대상 연결 | 매칭 기반으로 참고. buff/debuff 소유·효과를 기존 원문에서 자동 도출하지 않음 |
| D07 `cand_16354a4fd20558c0af3103c08c7d775f` | 작은 물품을 반복 선반의 빈 홈 위에 드는 손. contact_point/prop_state | Q08/Q09는 소켓 안쪽 가림·제작 단계 | 물품–빈자리 인접과 장착·제작은 비동치. 기존 접점 전체를 보존한 대안과 신규 관계를 분리 |
| D08 `cand_7b211801cf9655819c5b3af5434e7e03` | 두 성인 사이 heart 100, 한쪽은 물러남. proxemics/visible_text | R02/X09/X10 | 높은 값과 실제 동의의 비동치라는 회귀 사례를 재사용. 수신자 식별·관계 유형은 별도 검토 |

## 어휘 감사의 관찰

수정한 고정 정규식 기준 레코드 수는 status 5, hud 14, resources 1, progression 1, quest 12, inventory 14, craft 151, combat 0, party 20, dungeon_core 0, death 1, deck 0, affinity 1, contract 19, viewer 20, glitch 17이다. 정확한 패턴·소스 hash·28개 표본은 JSON에 있다. 이는 relevance rank나 top-k 결과가 아니다.

- `inventory`는 `sorting inventory on shelves` 같은 창고 재고와도 일치한다. 가상 수납 슬롯의 존재 증거가 아니다.
- 한국어 `레이드`를 부분 문자열로 찾으면 `브레이드` 헤어스타일이 섞였다. 앞 한글 경계를 보완했다. `party`는 행사·화장 문맥에서도 나타나므로 여전히 의미 검토가 필요하다.
- `귀속`은 아이템 영혼 귀속 외에 빛의 윤곽 귀속·사용 흔적의 접촉면 귀속이라는 출처에도 나타났다.
- `hologram underglow`, `hologram scanline texture`는 빛·질감의 후보이며 상태창 정보 구조를 보장하지 않는다.
- quest-evidence와 sponsor-registry 관련 기존 소스에는 `requires_primary_any_tags` 등의 실제 조건이 있다. 일반 판타지 소품으로 조건을 제거해 재사용하지 않는다.
- affinity 일치는 호감·동의·복종을 구별하는 diagnostic이었다. 이를 양성 호감도 창의 완성으로 세지 않는다.
- `combat/dungeon_core/deck` 0건은 이 패턴·필드의 결과일 뿐 전체 코퍼스에 같은 의미가 없다는 판정이 아니다. 후속 semantic review와 실제 retrieval 평가로 확인한다.

28개 어휘 표본과 별도로 정밀 비교한 기존 실현 8개는 일부 겹친다. 두 묶음 모두 native 적격성 심사나 전체 코퍼스 중복 판단을 완료한 것은 아니다. 새 초안 60개 역시 의미상 완전 신규라는 판정이 아니다. 재사용·차이·보류 목록을 확정한 뒤 운영 반영해야 한다.
