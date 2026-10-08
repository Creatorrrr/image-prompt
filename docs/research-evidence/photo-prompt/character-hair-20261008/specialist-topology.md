# 헤어 토폴로지·컬·묶음 관찰 카드 — 전문 분담 초안

상태: **연구 초안 / 런타임 미반영 / 후보팩·인덱스 미생성 / 픽셀 게이트 미실행**. 기준일은 2026-10-08 Asia/Seoul이다. 이 문서는 main 계획 통합을 위한 관찰 정의와 후보 문구 제안이며 기존 runtime assets, code, indexes를 수정하지 않았다. 작성 대상은 이 문서와 `topology-cards.json`, `topology-sources.json` 세 파일이다.

55개 독립 카드, 25개 구조 비교 쌍, 카드 핵심 출처 12개를 작성했다. 후반에 확인된 댕기·상투 맥락을 위해 국립민속박물관 자료 1개를 추가해 **전체 선정 공개 출처는 13개**이다. 자료 수 자체가 카드의 명칭·구조·생성 결과를 모두 입증하지는 않는다. `partial_label_support` 10개는 상위 구조가 지지되거나 구성안은 구체적이지만 정확한 named label 또는 세부 경로의 추가 교육자료가 필요한 상태다.

## 입력 범위와 복구 증거

최초 입력은 `reference/conversation-preview.md`의 20,000자 read_thread 잘림 응답 스냅샷이었다. 이후 main이 IAB 접근성 텍스트에서 원래 Markdown의 키워드 454행과 연출 조합 48행을 복구했다. 본 분담에서 `reference/keyword-inventory.tsv`를 직접 읽어 H001–H454의 454개 연속 ID와 `reference/character-combinations.tsv`의 48행을 확인했다. 두 파일의 SHA-256을 카드 JSON의 `input_snapshot`에 기록했다. UI 전사 checksum 일치는 main의 확인이며 본 분담은 UI를 독립 조작하지 않았다.

이는 **키워드 범위가 확보되었다**는 증거다. 원래 JSON 다운로드 bytes와 454개 전체 설명문 bytes를 확보했다는 의미가 아니다. R01–R48은 캐릭터 연출안이므로 그 조합을 헤어 의미의 보편적 정의로 승격하지 않는다. H204/H387 `Hair bow`, H397/H447 `Hair scarf`, H184 `Pigtails`의 문자열 중복은 문맥 손실 위험으로 따로 처리한다.

## 구조를 독립 축으로 분리해야 하는 이유

묶음의 수·밑동 위치·자유 꼬리·번 안으로 감긴 길이, weave의 가닥 수·교차·두피 feed 경로, 표면의 코일·광택·잔모 퍼짐은 서로 다른 축이다. `high ponytail + braid`, `half-up + bun`, `cornrows → ponytail`, `box braids + knotless root`, `loc bodies + loose curl tips`는 서로 결합할 수 있는 요청이다. 한 이름을 전체 머리의 배타적 종류로 사용하면 이 관계가 지워진다.

[브랜드 땋기 교육](https://www.lorealparisusa.com/beauty-magazine/hair-style/updo-and-bun-hairstyles/five-braid-tutorials)은 가닥의 교차와 주변 머리를 추가하는 구간을 분리한다. 이를 카드에서는 `scalp-attached path`와 `free-hanging length`라는 저자의 관찰 원시 요소로 운영화했다. 원시 요소가 원본 대화의 독립 키워드였다고 주장하지 않는다.

- **Ponytail**: 수렴 밑동과 그곳에서 이어지는 꼬리. high/low는 꼬리 끝이 아니라 밑동 위치다. side base와 중앙 밑동의 side-draped tail은 다르다.
- **Twintails / braided pigtails**: 좌우 두 밑동과 자유 꼬리 또는 반복 weave. `pigtails`는 문맥에 따라 둘 다 가리켜 자동 동의어로 고정하지 않는다. 높이·대칭·길이도 별도다.
- **Half-up**: 고정된 위층과 풀린 아래층이 동시에 보여야 한다. 앞의 tendril 두 가닥만으로 아래층을 대체하지 않는다.
- **Puff / pineapple / topknot**: 둥글게 퍼지는 컬 덩어리, 높고 앞쪽으로 퍼지는 자유 컬, 길이가 감겨 들어간 번을 구별한다. Davines의 pineapple bun 용례와 자유 컬 pineapple 용례는 하나의 기하로 합치지 않는다.
- **Chignon / French twist / Gibson tuck**: 낮은 매듭 덩어리, 뒤통수의 세로 긴 접힘, 목덜미의 가로 롤을 구분한다. chignon의 낮은 위치는 클래식 후보의 지정값이며 모든 현대 용례의 배타 조건이 아니다.

## 땋기·트위스트·록스의 판별 경계

French/Dutch의 핵심 차이는 바깥 묶음의 중앙 위/아래 교차이다. 완성 사진에서는 두피 feed와 중앙 능선의 층이 함께 보여야 해당 명칭을 판정할 수 있다. 끝의 자유 plait만 보이면 차이가 남지 않을 수 있다. 폭이나 부피만으로 Dutch를 판정하지 않는다.

Fishtail은 두 큰 구역 사이로 작은 측면 가닥이 넘어가는 사선 전이 패턴이고 rope/two-strand twist는 두 묶음이 통으로 서로 감기는 나선 경계다. Cornrows는 두피 가까이에 붙는 경로와 구획을, box braids는 독립 구획에서 늘어지는 가닥을 관찰 기준으로 둔다. Dutch와 cornrow는 underhand 원리가 겹칠 수 있으므로 이름만으로 강한 배타성을 부여하지 않는다.

[Knotless 교육 용례](https://www.hair.com/box-braids-vs-knotless-braids.html)는 box의 구획 토폴로지와 knotless의 뿌리 설치법이 겹침을 보여 준다. 따라서 `box → knotless`는 상위형과 변형 관계 또는 독립 축으로 모델링할 수 있다. 실제 설치 과정을 보지 못한 사진에서는 큰 돌출 매듭 없는 root transition까지만 판정한다. Feed-in도 제작 과정명이고 점진 굵기 외형은 가능성 있는 관찰 후보일 뿐 과정의 증명이 아니다.

[전문 단체의 locs/twist 정의](https://www.aota.org/practice/practice-essentials/dei/-/media/d1a3e07b1f5a45dd8250b8351a86fab7.ashx)는 얽혀 하나의 단위를 이루는 loc와 두 묶음 꼬임을 구분한다. 이 차이는 반복 seam과 연속 섬유 몸체로 후보를 작성할 근거이며 사진에서 성숙 기간·설치법·천연 모발·위생을 증명하는 근거가 아니다. 자연 loc와 faux loc는 완성 외형이 겹칠 수 있어 provenance를 남긴다.

[Butterfly locs의 브랜드 용례](https://carolsdaughter.com/blogs/beauty-blog/your-ultimate-guide-to-the-butterfly-locs-hairstyle)는 연속 몸체에서 느슨한 고리가 남는 특징을 제시한다. Goddess locs의 자유 컬/컬 끝과 같은 사진에 함께 존재할 수 있으므로 배타적으로 처리하지 않는다. 큰 고리 구조를 잔모 frizz halo로 대체해서는 안 된다.

Lace의 일측 feed, stitch의 양측 짧은 반복 구획선은 구체적 후보로 작성했지만 이번 core source selection에서 exact named technique의 충분한 일차 교육자료를 채택하지 못했다. named alias 승격을 먼저 막고 해당 관찰 요소의 수동 묘사는 보존한다.

## 굴곡·한 올의 지름·밀도·부피

[Aveda의 fine 설명](https://www.aveda.com/hair-care/for-fine-and-thinning-hair)은 한 올의 지름과 전체 머리 양이 다른 개념임을 분명히 한다. 카드의 분리는 다음과 같다.

| 축 | 후보에서 관찰할 항목 | 사진만으로 입증하지 않는 항목 |
|---|---|---|
| strand diameter | 분리된 한 올의 경계와 비교 스케일 | 일반 초상만으로 실제 μm 지름·촉감 |
| density | 뿌리 분포, 같은 초점의 두피 틈, apparent coverage | 모낭 수·탈모·건강 진단 |
| volume | 두상 밖으로 솟거나 옆으로 퍼지는 전체 윤곽 | 한 올 지름·모발 수·backcombing 방법 |
| curl morphology | 열린 S, 고리/나선, 작은 코일, 각진 지그재그 | 인종·유전·자연 성장·펌/열도구 원인 |
| curl grouping | 여러 모발 선이 같은 컬 경로를 따르는 clump | 굵은 단일 모발이라는 결론·사용 제품 |

[컬 형태를 설명하는 교육자료](https://www.hair.com/how-to-plop-hair.html)의 번호는 그 체계의 용례로 보존하고 보편 표준처럼 강제하지 않는다. ringlet, corkscrew, loose/tight는 curly의 동의어 묶음보다 모양·반경의 변형으로 남긴다. 한 사람의 다른 구역에서 서로 다른 패턴이 보이는 mixed patterns는 가능하나 카메라 원근·초점·암부만으로 패턴 차이를 만들어내지 않는다. `kinky`는 hair morphology 문맥에서만 검색 별칭으로 사용하고 후보 문구에는 촘촘한 각진 굴곡을 적는다.

## 표면 상태와 원인의 분리

Slick/sleek는 지정 방향으로 눕고 정렬된 표면이다. 뒤로 향하는 slicked-back은 방향 축이 추가된 상태다. Wet-look은 반사와 뭉침으로 젖어 보이는 연출이며 [브랜드 wet updo 튜토리얼](https://ca.davines.com/blogs/news/20-updo-hairstyles-for-everyone)이 제품으로 만들 수 있는 예를 제시한다. 실제 wet hair의 물, gel, oil, wax 원인은 분리한다. 반사 한 줄로 실제 수분을 확정하지 않는다.

Frizz는 주된 경로에서 나온 잔모의 퍼짐이고 bedhead/tousled는 더 큰 구역의 가닥 방향·눌림·들림이 불규칙한 배치다. 두 축은 함께 존재할 수 있다. 수면·피로·손상·습도·위생을 명칭에서 자동 생성하지 않는다. `protective style`도 끝 감춤·가닥 그룹이라는 관찰과 문화/관리 문맥을 남길 수 있지만 보호 효능·편안함·안전·건강을 픽셀 통과 항목으로 사용하지 않는다.

## 액세서리와 모발의 접합 관계

Main이 후반 H386–H415의 30개 accessory/extension 키워드를 직접 제품·교육자료로 보강하는 별도 계획을 작성한다. 여기서는 중복 전체 카드를 만들지 않고 토폴로지 카드와 연결할 관계를 제안한다. T04에는 twist 끝을 beads에 통과시키는 예와 cuffs, T07에는 tuck의 꽃, T08에는 뒤 묶음에 리본을 더하는 예가 있다. 그 예를 아래처럼 **보이는 접합의 구성안**으로 운영화한다.

| 구조 class | directed relation 제안 | 필요한 관찰점 | 실패/보류 경계 |
|---|---|---|---|
| thread | hair bundle → passes_through → bead hole | 가닥이 비즈 양쪽/구멍에 들어가 이어짐 | 비즈가 머리 옆에 떠 있으면 fail; 구멍·접촉이 숨으면 보류 |
| wrap | cuff/ring/tie/scrunchie → encircles → braid/loc/base | 닫힌 둘레와 대상 가닥의 연결 | 가닥 바깥의 장식 원만으로 감김 통과 불가 |
| weave | ribbon → runs_with → braid path | 천 띠와 땋기 교차의 반복 관계 | 독립 리본만 옆에 있으면 woven ribbon 아님 |
| grip/clip | clip → spans_and_contacts → gathered bundle | clip 몸체/모발의 접촉과 양쪽 경계 | 실제 잠금부가 숨으면 mechanism의 성공 주장 보류 |
| insert | pin/stick/comb → enters → bun/tuck | 모발 덩어리로 들어가는 shaft/teeth 및 접촉 | 공중에 뜬 pin은 fail; 완전 숨긴 pin은 존재 검증 불가 |
| attach | added hair → joins → native hair/base | 접합 위치와 이어지는 길이 | 완성 실루엣만으로 clip/tape/weft/halo 설치법 입증 불가 |
| growth origin | long hair → continuous_from → subject.head | 머리에서 이어지는 모발 경로 | 같은 색의 천 스카프를 모발로 승격하지 않음 |

H204 `Hair bow / bow-shaped hair`는 머리카락 자체의 두 고리와 중앙 띠다. H387 `Hair bow`는 별도 천 장식이 모발에 닿거나 고정된 객체다. 검색 문자열이 같아도 owner가 다르다. H397 천 `Hair scarf`와 H447 모발이 목을 감싸는 `Hair scarf` 역시 material owner와 성장 원점의 연속성을 분리한다. 이 네 항목은 완성 card source qualification을 마쳤다는 뜻이 아니라 alias 충돌과 접합 의무를 기록한 상태다.

H408–H415의 clip-in/tape-in/weft/halo/clip-in bangs/pony extension/lace-front/topper는 추가 모발의 설치·출처 유형을 포함한다. 레이스 edge나 clip/tape/track이 실제로 보이거나 제작/source context가 제공되면 해당 provenance와 형태를 함께 기록한다. 구조가 숨겨졌을 때는 `added hair unknown` 또는 관찰된 최종 외곽을 유지한다. 사진의 머리 길이가 크다는 사실에서 extension 재료나 설치법을 역추론하지 않는다.

## 시대·문화 이름의 관찰과 맥락

[T07 Gibson tuck](https://media.rct.uk/sites/default/files/resources/PDF%20Gibson%20Tuck%20Hairstyle.pdf)과 [T08 Victory rolls](https://media.rct.uk/sites/default/files/resources/PDF%20Victory%20Rolls%20Hairstyle.pdf)는 Royal Collection Trust의 교육 재현이다. 정지 사진에서 역사적 연대·국적·계층·성격이 증명되는 것은 아니다. 재현 튜토리얼의 한 방식이 유일한 기법이라는 결론도 내리지 않는다. PDF text는 읽었지만 도해의 native pixels를 독립 판독한 상태는 아니다.

[T13 국립민속박물관의 댕기·비녀 맥락](https://webzine.nfm.go.kr/2018/07/26/%EC%96%B4%EB%A5%B8%EA%B3%BC-%EC%95%84%EC%9D%B4%EC%9D%98-%EA%B2%BD%EA%B3%84-%EB%8C%95%EA%B8%B0%EC%99%80-%EB%B9%84%EB%85%80/)은 댕기가 땋은 끝을 매는 끈이며 상투의 정수리 올림과 동곳의 접합 맥락이 있음을 설명한다. 향후 H416 댕기머리의 hair braid, H417 댕기의 textile tie, H418 상투의 raised wrapped mass를 서로 다른 owner/component로 작성한다. 해당 문헌의 역사적 사회 표지를 현대 사진의 실제 연령·혼인·나라·신분 속성으로 자동 승격하지 않는다. 상투와 일반 topknot의 외형이 겹치는 부분은 cultural provenance로 보완하고 치수·구조를 추가 자료로 특정한다.

Mohawk/faux hawk/deathhawk/liberty spikes/emo/scene/goth/punk 같은 후반 문화·서브컬처 명칭은 전체 인격 레이블로 연결하지 않는다. main의 길이·실루엣 담당과 결합할 때 중앙 ridge/spikes, 옆 구역 길이, 가닥 방향·색·배치로 분해하고 스타일 문화의 용례와 현재 사람의 실제 소속을 분리한다.

## 55개 카드 인벤토리

각 JSON 카드에는 `id`, ko/en labels, 도메인 한정 aliases, definition, observable components, owner, region, directed relations, minimum signature, exclusions/confusion boundaries, compatibility axes, camera visibility, source refs/supported claim, confidence/ambiguity, proposed candidate wording, pixel gate, 원본 H ID 대응이 있다. geometry는 출처를 운영화한 저자의 제안이고 runtime schema의 채택을 의미하지 않는다.

| 카드 | 한국어 / English | 원본 키워드 | 명칭·구조 상태 |
|---|---|---|---|
| `ponytail` | 포니테일 / Ponytail | H173 | 출처 구조 + 관찰 제안 |
| `high_ponytail` | 하이 포니테일 / High ponytail | H174 | 출처 구조 + 관찰 제안 |
| `low_ponytail` | 로우 포니테일 / Low ponytail | H175 | 출처 구조 + 관찰 제안 |
| `side_ponytail` | 사이드 포니테일 / Side ponytail | H176 | 명칭/세부 source 보완 |
| `twintails` | 양갈래 풀린 꼬리 / Twintails / two ponytails | H181, H182, H183, H184 | 출처 구조 + 관찰 제안 |
| `braided_pigtails` | 땋은 양갈래 / Braided pigtails | H184 | 출처 구조 + 관찰 제안 |
| `bubble_ponytail` | 버블 포니테일 / Bubble ponytail | H177 | 출처 구조 + 관찰 제안 |
| `braided_ponytail` | 땋은 포니테일 / Braided ponytail | H178 | 출처 구조 + 관찰 제안 |
| `hair_wrapped_base` | 머리카락으로 감싼 밑동 / Hair-wrapped ponytail base | H180 | 명칭/세부 source 보완 |
| `half_up` | 반묶음 / Half-up, half-down | H185 | 출처 구조 + 관찰 제안 |
| `half_up_bun` | 반묶음 번 / Half-up bun | H186 | 명칭/세부 source 보완 |
| `afro_puff` | 컬 퍼프 / 아프로 퍼프 / Afro puff | H190 | 출처 구조 + 관찰 제안 |
| `pineapple_updo` | 파인애플 업두 / Pineapple updo | H191 | 출처 구조 + 관찰 제안 |
| `topknot` | 톱노트 / Topknot | H193 | 출처 구조 + 관찰 제안 |
| `low_bun` | 로우 번 / Low bun | H194 | 출처 구조 + 관찰 제안 |
| `space_buns` | 양쪽 번 / 스페이스 번 / Space buns | H199 | 명칭/세부 source 보완 |
| `chignon` | 시뇽 / Chignon | H201 | 출처 구조 + 관찰 제안 |
| `french_twist` | 프렌치 트위스트 / French twist | H202 | 출처 구조 + 관찰 제안 |
| `gibson_tuck` | 깁슨 턱 / 깁슨 롤 / Gibson tuck | H203 | 출처 구조 + 관찰 제안 |
| `victory_rolls` | 빅토리 롤 / Victory rolls | H209 | 출처 구조 + 관찰 제안 |
| `three_strand_braid` | 세 가닥 땋기 / Three-strand braid | H210 | 출처 구조 + 관찰 제안 |
| `free_hanging_braid` | 자유로 늘어진 땋은 가닥 / Free-hanging braid | H210, H217 | 출처 구조 + 관찰 제안 |
| `scalp_attached_braid` | 두피를 따라 붙은 땋기 / Scalp-attached braid | H211, H212, H219 | 출처 구조 + 관찰 제안 |
| `french_braid` | 프렌치 브레이드 / French braid | H211 | 출처 구조 + 관찰 제안 |
| `dutch_braid` | 더치 브레이드 / Dutch braid | H212 | 출처 구조 + 관찰 제안 |
| `fishtail_braid` | 피시테일 브레이드 / Fishtail braid | H213 | 출처 구조 + 관찰 제안 |
| `rope_twist` | 두 가닥 로프 트위스트 / Rope twist / two-strand twist | H214 | 출처 구조 + 관찰 제안 |
| `waterfall_braid` | 워터폴 브레이드 / Waterfall braid | H215 | 출처 구조 + 관찰 제안 |
| `lace_braid` | 레이스 브레이드 / Lace braid | H216 | 명칭/세부 source 보완 |
| `crown_braid` | 크라운 브레이드 / Crown braid | H205 | 명칭/세부 source 보완 |
| `box_braids` | 박스 브레이드 / Box braids | H217 | 출처 구조 + 관찰 제안 |
| `knotless_braids` | 노트리스 브레이드 / Knotless braids | H218 | 출처 구조 + 관찰 제안 |
| `cornrows` | 콘로우 / 캔로우 / Cornrows / canerows | H219 | 출처 구조 + 관찰 제안 |
| `feed_in_braids` | 피드인 브레이드 / Feed-in braids | H220 | 명칭/세부 source 보완 |
| `stitch_braids` | 스티치 브레이드 / Stitch braids | H221 | 명칭/세부 source 보완 |
| `flat_twists` | 플랫 트위스트 / Flat twists | H227 | 출처 구조 + 관찰 제안 |
| `bantu_knots` | 반투 노트 / Bantu knots | H228 | 출처 구조 + 관찰 제안 |
| `locs` | 록스 / Locs | H229 | 출처 구조 + 관찰 제안 |
| `faux_locs` | 포 록스 / Faux locs | H230 | 출처 구조 + 관찰 제안 |
| `butterfly_locs` | 버터플라이 록스 / Butterfly locs | H231 | 출처 구조 + 관찰 제안 |
| `goddess_locs` | 갓디스 록스 / Goddess locs | H232 | 출처 구조 + 관찰 제안 |
| `senegalese_twists` | 세네갈리즈 트위스트 / Senegalese twists | H224 | 출처 구조 + 관찰 제안 |
| `wavy` | 웨이비 / S자 물결 / Wavy hair | H036 | 출처 구조 + 관찰 제안 |
| `curly` | 컬리 / 링렛 컬 / Curly hair | H037, H041, H042, H043, H044 | 출처 구조 + 관찰 제안 |
| `coily` | 코일리 / Coily hair | H038 | 출처 구조 + 관찰 제안 |
| `kinky_hair` | 촘촘한 각진 굴곡 / Kinky / zig-zag-coiled hair | H039 | 출처 구조 + 관찰 제안 |
| `mixed_curl_patterns` | 혼합 컬 패턴 / Mixed curl patterns | H040 | 출처 구조 + 관찰 제안 |
| `curl_clumps` | 컬 뭉치 / Curl clumps | H045 | 명칭/세부 source 보완 |
| `fine_strands` | 가는 모발 한 올 / Fine hair strands | H031, H032 | 출처 구조 + 관찰 제안 |
| `apparent_density` | 모발 밀도 / 보이는 채움 / Hair density / apparent coverage | H033, H034 | 출처 구조 + 관찰 제안 |
| `hair_volume` | 헤어 볼륨 / 외곽 부피 / Hair volume | H028, H029, H030, H448 | 출처 구조 + 관찰 제안 |
| `wet_look` | 웨트 룩 / 젖어 보이는 표면 / Wet-look hair | H368, H369 | 출처 구조 + 관찰 제안 |
| `slick_surface` | 매끈하게 눌러 정렬한 표면 / Slick / sleek hair surface | H152, H195 | 출처 구조 + 관찰 제안 |
| `frizz` | 프리즈 / 잔모 퍼짐 / Frizz | H046, H022, H371 | 출처 구조 + 관찰 제안 |
| `bedhead_surface` | 흐트러진 머리 / 베드헤드 외형 / Bedhead / tousled hair appearance | H364, H365, H366 | 명칭/세부 source 보완 |

## 비교 쌍과 픽셀 게이트 초안

아래 비교는 아직 실행하지 않았다. 실루엣만 다른 스타일을 여러 번 그렸다는 사실을 정확한 braid topology 검증으로 보고하지 않는다. 비교마다 주체·머리색·길이·조명·카메라·배경·노출을 고정하고 판별 차이를 최소화한다. 자체 작성한 설명으로 같은 설명의 존재만 검사하는 테스트를 만들지 않는다. 실제 출력에서 해당 region, 소유자, 관계의 형태를 판독해야 한다.

| 쌍 | 통제할 차이 | 판정 조건 |
|---|---|---|
| French/Dutch | 동일 색·길이·폭·머리 각도에서 중앙 교차의 위/아래와 둘레 흐름 대비만 바꾼다. | 두피 경로와 중앙 능선의 층이 보여야 함. |
| 두피/자유 땋기 | 같은 weave를 유지하고 두피를 따라 입력되는 구간 또는 독립 시작점에서 늘어지는 구간만 바꾼다. | 뿌리에서 길이까지 연속 관찰. |
| 세 가닥/Fishtail | 세 큰 교차 단위와 작은 사선 V 전이만 바꾼다. | 여러 반복 단위가 같은 스케일로 보여야 함. |
| Fishtail/Rope | 작은 사선 전이와 두 덩어리의 나선 경계만 바꾼다. | 폭·색·길이는 고정. |
| Cornrows/Box | 두피를 따르는 연속 줄과 독립 구획에서 늘어진 가닥의 경로만 바꾼다. | 두피 구획 전체가 보여야 함. |
| Box/Knotless roots | 같은 box 구획·독립 plaits에서 뿌리의 돌출 매듭만 달리한다. | 배타적 스타일명 분류가 아니라 root geometry 비교; 설치법 미입증. |
| Cornrow/Flat twist | 같은 두피 경로에서 세 묶음 교차와 두 묶음 나선만 바꾼다. | 루트와 반복 경계 close-up. |
| Twist/Loc bodies | 정규 두 묶음 나선 경계와 연속 섬유 몸체 표면만 바꾼다. | starter locs 등 겹침 사례는 ambiguous로 유지. |
| Natural/Faux loc provenance | 동일한 loc-like 완성 외형을 두 번 사용하고 제작 provenance만 달리한다. | 정지영상만으로 원인 분류를 성공했다고 보고하면 실패. |
| Butterfly/Goddess locs | 몸체에서 튀어나온 반복 고리와 길이/끝의 자유 컬 위치만 바꾼다. | 두 특징은 동시 존재 가능; 배타성 gate 금지. |
| Twintails/Braided pigtails | 두 밑동·높이는 유지하고 두 꼬리의 weave만 바꾼다. | 양쪽 꼬리가 동시에 보여야 함. |
| High/Low ponytail | 밑동 위치만 이동하고 꼬리 길이·부피는 고정한다. | 끝 위치가 아니라 fastening root 위치 판정. |
| Side base/Side-draped tail | 밑동 offset과 꼬리의 drape 방향을 독립적으로 바꾼다. | 보이지 않는 밑동은 통과 불가. |
| Bubble/Braided ponytail | 반복 밴드와 실제 가닥 교차만 바꾼다. | 버블의 braid 통칭 때문에 weave를 invent하면 실패. |
| Half-up/Full topknot | 상부 번을 고정하고 풀린 아래층 존재만 바꾼다. | 앞의 tendril 두 가닥은 아래층 대체가 아님. |
| Pineapple/Topknot | 높은 밑동을 유지하고 자유 컬 부채와 감겨 들어간 길이만 바꾼다. | 같은 이름의 pineapple bun은 별도 variant. |
| French twist/Gibson tuck | 뒤 업두의 세로 접힘과 목덜미 가로 롤만 바꾼다. | rear three-quarter에서 fold 전체가 보여야 함. |
| Space buns/Bantu knots | 두 큰 측면 번과 여러 구획의 작은 매듭 배치만 바꾼다. | 매듭 개수·구획 위치가 크롭 없이 보임. |
| Wavy/Curly | 열린 S와 닫히는 spiral/ringlet 형태만 바꾼다. | 가닥 굵기·두피 밀도·실루엣 크기는 고정. |
| Coily/Angular zig-zag | 작은 나선과 작고 각진 굴곡만 바꾼다. | 인종/원인/촉감 정보를 추가하면 실패. |
| Fine/Density | 한 올 지름과 뿌리 분포를 2×2로 독립 변형한다. | macro/스케일 없이 actual fine 판정 금지. |
| Density/Volume | 뿌리 채움을 고정하고 외곽 팽창을 바꾸는 쌍, 역방향 쌍을 각각 만든다. | high volume=high density라는 자동 관계가 없어야 함. |
| Curl clump/Coarse strand | 여러 가는 모발의 공유 곡선과 단일 모발 지름을 독립적으로 보여 준다. | 큰 clump가 굵은 한 올로 라우팅되면 실패. |
| Wet look/Actual wetness | 제품 연출의 광택과 실제 물/방울 evidence를 분리한다. | 반사만으로 wetness 원인 확정 시 실패. |
| Frizz/Bedhead | 잔모 halo와 큰 덩어리 방향의 헝클어짐을 2×2로 교차한다. | 수면·위생·피로 추론 금지. |

Hair bow와 Hair scarf의 owner 충돌 비교를 추가하면 27개 비교 범위다. 지금은 25개 구조 쌍을 JSON으로 작성하고 두 충돌을 `alias_collision_boundaries`에 별도 기록했다. 게이트의 결과는 PASS / FAIL / UNOBSERVABLE_NOT_PASS로 분리한다. source/process가 없으면 설치법·자연 성장·실제 wetness 판정은 `not_proven`을 유지한다. partial_is_fail은 요청한 관찰 요소가 일부만 구현된 경우에 적용하며 이름의 유사성으로 합격시키지 않는다.

주요 framing은 rear/top three-quarter의 root + path, 머리 전체의 양쪽 묶음, 길이의 반복 weave, 단일 가닥의 macro+scale이다. 정면 얼굴만 보이는 사진에서 뒤통수 fold, 두피 구획, 감춰진 extension 설치부를 검증하려고 하지 않는다. 검증 가능한 프레임을 요청한 결과물의 미학과 함께 설계하고 필수 형상을 관찰 불가로 만드는 선택은 별도 기록한다.

## 통합 순서와 보완 대상

1. Main이 H ID 대응과 각 specialist 중복을 병합한다. free/scalp 원시 요소와 source 키워드, 지역별 variant, 문화 이름·설치 과정 축을 분리한 canonical identity를 먼저 정한다.
2. partial-label 10개에서 정확한 named label 자료와 관찰 경로를 보완한다. side ponytail, hair-wrapped base, half-up bun, space buns, lace braid, crown braid, feed-in, stitch, curl clumps, bedhead는 현재 주장 범위를 넘겨 출처가 지지했다고 표시하지 않는다.
3. 아래 추가 키워드는 **이번 55개 완성 카드 밖의 보완 계획**으로 남긴다. 독립 카드 수를 채우려고 검증되지 않은 명칭을 추가하지 않는다.

| 키워드 | 필요한 분리 | 다음 자료·관찰의 목적 |
|---|---|---|
| H179 Folded ponytail | 묶음+접힌 loop, 완전 bun과 남은 tail | 접힘 loop와 tail이 동시에 보이는 교육 예 |
| H187/H188 One/Two side up | 고정 구역 수, 전체 loose lower layer | 정면만으로 한쪽/양쪽 고정을 오인하지 않는 경로 |
| H189 Multi-tied | 여러 base 수 vs bubble의 한 tail 안 bands | 모발의 수렴 그래프를 확정 |
| H192/H195–H198/H200 | bun 기본 + slick/messy + donut hole + braided surface | 모양·표면·내부 교차·받침 사용을 분리 |
| H204/H206 Hair bow/loops | hair shape와 textile accessory, 감긴/열린 고리 | hair continuity와 중앙 wrap 접합 |
| H207/H208 Bouffant/Beehive | 넓은 팽창과 높은 dome/tower | 접근 가능한 공식 교육 자료와 측면 윤곽 필요; 실패한 evo PDF 스니펫은 proof에서 제외 |
| H222 Fulani braids | cornrow/individual braids, 위치·방향·bead 조합, 문화 맥락 | 문화적 정체성 없이 version-specific 실제 구조를 확인 |
| H223 Goddess braids | 큰 scalp braids와 boho loose curls 등의 용례 변형 | 같은 이름의 혼용을 실제 브랜드/살롱 reference별로 분리 |
| H225/H226 Marley/Passion twists | 두 가닥 topology와 extension fiber/curl appearance | 재료명이 사진만으로 증명되지 않는 경계와 보이는 표면 변형 |
| H233/H234 Micro/Jumbo braids | individual braid width/count와 strand diameter | 고정 mm를 만들지 않고 동일 camera scale의 상대 굵기·가닥 수 비교 |
| H416–H418 Daenggi/Sangtu | textile end tie, hair braid/top mass, 문화 provenance | 박물관의 특정 실물·도구의 접합 위치를 추가 확인 |

4. 저자 core와 동결된 requester meaning을 유지하는 post-core 후보로 매핑한다. broad alias·BM25F/embedding 유사도는 이름을 찾는 보조 증거이지 필수 헤어 구조 활성화 증거가 아니다. 구체 owner/region을 선택한 후보만 적용하고 다른 헤어·피부·배경에 확산하지 않는다.
5. 실제 데이터 적용이 새로 허가되면 authored source와 후보 매핑을 함께 변경하고 source manifest/색인/임베딩 재사용 여부를 main의 현재 구조에 맞게 검증한다. 이 문서에서는 그 변경이나 생성·리그레션 실행을 하지 않았다.
6. 채택한 구조 쌍의 native pixels와 촬영 관찰성까지 확인한 뒤 실제 renderer/evaluator 결과를 기록한다. 자료 확보, JSON parse, 검색 성공, candidate exposure, authored prompt, native pixels, 사용자 수용은 별도 결과로 보고한다.

## 출처 인벤토리와 실제 확인 범위

모든 출처는 2026-10-08에 웹 본문을 읽었다. 아래 요약은 source의 지지 범위이며 각 카드의 전체 운영 규격을 출처가 직접 제정했다는 뜻이 아니다. 전문 단체 안내와 브랜드 용례는 가닥·배치 구분에 사용하고 제품 효능·건강·역사적 기원 일반화는 채택하지 않았다. 긴 원문 인용은 하지 않았다.

- **T01** [Braiding Basics: How to Braid Your Hair](https://www.lorealparisusa.com/beauty-magazine/hair-style/updo-and-bun-hairstyles/five-braid-tutorials) — L’Oréal Paris; official_brand_tutorial. Traditional/French/Dutch/Waterfall/Fishtail sections. 세 가닥 교차, 두피에서의 추가 가닥, 위·아래 교차, 아래로 빠지는 가닥, 피시테일의 작은 측면 가닥 전이를 구분한다.
- **T02** [AOTA’s Guide to Culturally Inclusive Hair Care Services and Incorporating Cultural Humility Into Practice](https://www.aota.org/practice/practice-essentials/dei/-/media/d1a3e07b1f5a45dd8250b8351a86fab7.ashx) — American Occupational Therapy Association; professional_association_guidance. PDF pp. 2, 6–7; Glossary. 여러 컬 유형이 한 사람에게 나타날 수 있고, Bantu knots·box braids·cornrows·locs·two-strand twists의 구조가 구분된다.
- **T03** [Box Braids vs. Knotless Braids: What’s the Difference?](https://www.hair.com/box-braids-vs-knotless-braids.html) — Hair.com / L’Oréal Professional Products Division; official_brand_educational_article. What Are Box Braids? / What Are Knotless Braids?. box는 독립적인 구획 땋기이고 knotless는 자연 모발에서 시작해 추가 모발을 점진적으로 넣는 설치 변형이다.
- **T04** [10 Super Stylish Ponytail Upgrades for Curly Hair](https://www.lorealparisusa.com/beauty-magazine/hair-style/updo-and-bun-hairstyles/cool-ponytails-for-curly-hair) — L’Oréal Paris; official_brand_tutorial. High Bubble / Flat Twist / Pineapple / Low Puff / Half Up / Pigtails. 반복된 밴드의 버블, 두 갈래 꼬리, 높게 앞으로 퍼지는 컬, 풀어 둔 아래층, 비즈·커프 접합을 제시한다.
- **T05** [20 Updo Hairstyles for Everyone](https://ca.davines.com/blogs/news/20-updo-hairstyles-for-everyone) — Davines; official_brand_tutorial. Chignon / Half Up / Banded Ponytail / Topknot / Low Bun / Wet Hair Updo. 묶음 위치·풀린 아래층·말아 올린 덩어리와 slick/wet-looking 표면을 별도로 조합하는 튜토리얼이다.
- **T06** [How To Create a Classic French Twist](https://www.lorealparisusa.com/beauty-magazine/hair-style/updo-and-bun-hairstyles/classic-french-twist) — L’Oréal Paris; official_brand_tutorial. What Is a French Twist? / Steps 2–5. 한쪽으로 넘긴 모발을 위쪽으로 말아 긴 접힘을 만들고 끝을 안쪽에 넣는 업두를 설명한다.
- **T07** [1940s Hairstyle tutorial: The Gibson Tuck](https://media.rct.uk/sites/default/files/resources/PDF%20Gibson%20Tuck%20Hairstyle.pdf) — Royal Collection Trust; museum_educational_reconstruction. PDF p. 1, steps 8–13. 가로로 긴 받침을 모발로 감아 목덜미까지 말아 올리는 방식과 꽃 장식이 제시된다.
- **T08** [1940s Hairstyle tutorial: Victory Rolls](https://media.rct.uk/sites/default/files/resources/PDF%20Victory%20Rolls%20Hairstyle.pdf) — Royal Collection Trust; museum_educational_reconstruction. PDF p. 1, forehead/side rolls and ribbon finishing. 앞·옆의 안쪽 롤을 고정하고 뒤쪽 꼬리에 리본을 더하는 재현 방식을 제시한다.
- **T09** [Protective Hairstyles: The Ultimate Guide To Styling And Care](https://www.hair.com/protective-hairstyles.html) — Hair.com / L’Oréal Professional Products Division; official_brand_educational_article. Goddess Locs / Faux Locs / Crown Braid / Senegalese Twists. faux locs는 추가 모발의 감기, goddess locs는 풀린 컬 추가, Senegalese twists는 두 가닥 꼬임이라는 용례를 구분한다.
- **T10** [How to Plop Hair in 7 Easy Steps](https://www.hair.com/how-to-plop-hair.html) — Hair.com / L’Oréal Professional Products Division; official_brand_educational_article. Who Should Try Hair Plopping? / Mizani Texture Key. S자 물결, 고리·나선·링렛·코르크스크루, 더 작은 코일, 지그재그형 굴곡을 서로 구분한다.
- **T11** [The Best Shampoo & Hair Products For Fine & Thinning Hair](https://www.aveda.com/hair-care/for-fine-and-thinning-hair) — Aveda; official_brand_faq. FAQ: What is fine hair? / How can I make fine hair look thicker?. fine은 한 올의 지름을 뜻하며 높은 밀도와 공존할 수 있고 스타일링으로 보이는 부피를 바꿀 수 있다.
- **T12** [Your Ultimate Guide to the Butterfly Locs Hairstyle](https://carolsdaughter.com/blogs/beauty-blog/your-ultimate-guide-to-the-butterfly-locs-hairstyle) — Carol’s Daughter; official_brand_tutorial. What Are Butterfly Locs? / What Makes Butterfly Locs Different. loc 형태의 길쭉한 몸체에 느슨한 컬 고리가 남는 butterfly locs 용례를 제시한다.
- **T13** [어른과 아이의 경계 : 댕기와 비녀](https://webzine.nfm.go.kr/2018/07/26/%EC%96%B4%EB%A5%B8%EA%B3%BC-%EC%95%84%EC%9D%B4%EC%9D%98-%EA%B2%BD%EA%B3%84-%EB%8C%95%EA%B8%B0%EC%99%80-%EB%B9%84%EB%85%80/) — 국립민속박물관; museum_cultural_context_article. 댕기 / 비녀·상투·동곳 paragraphs. 댕기는 땋은 끝에 연결하는 끈이며 상투는 정수리에 틀어 올린 모발과 동곳의 맥락으로 설명된다.

검증 완료 범위는 직접 읽은 출처, 55개 JSON 카드 필드, 25개 비교 쌍 참조, 로컬 TSV 454/48행과 H ID 연속성이다. 현재 런타임과 전체 테스트는 이 분담에서 실행·변경하지 않았다. 기존 dirty assets/index의 수정 주체·상태를 본 분담의 성과로 보고하지 않는다. 이 초안은 추가 source가 필요한 항목을 그대로 표시한 연구 산출물이다.
