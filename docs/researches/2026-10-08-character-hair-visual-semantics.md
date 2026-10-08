# 캐릭터 헤어스타일 키워드의 시각 의미·후보팩 강화 연구

작성일: 2026-10-08, Asia/Seoul. 요청 범위: 참조 대화의 키워드에 기반한 상세 리서치와 반영 계획.

## 결론

헤어 데이터는 **소유자·부위·형태·색 배치·접합·상태를 분리하고 필요한 관계로 다시 연결**하는 방향으로 강화하는 것이 타당하다. 명칭 454개를 그대로 454개 후보나 hard profile로 만드는 방식은 중복, 시술 원인 추정, 잘못된 배타성, 이름 충돌을 늘린다.

우선순위는 현행 wet-look/실제 수분과 발레아주/대표 리본 외형의 경계를 검토하는 것이다. 다음으로 커트의 구역별 길이, 앞머리의 coverage/edge/length, 묶음 밑동, scalp/free braid 경로, 색의 영역·경계·겉/안층을 보강한다. 이미 있는 Y2K·subculture·캐릭터 외형 후보와 프로필을 재사용하며, 부족한 관계와 혼동 경계에 새 실현안을 제안한다.

이 연구는 카드와 설계·검증 초안을 저장한 상태다. 런타임 source, manifest, 인덱스, 코드, 테스트를 반영하거나 이미지 생성·검색 개선을 검증한 상태는 아니다.

## 입력 자료와 조사 범위

참조 대화는 [캐릭터 헤어스타일 용어 조사](https://chatgpt.com/c/6ac643c0-926c-83ee-b8f8-62e52ef07784)다. `read_thread`의 20,000자 제한 preview만으로 전체 목록을 단정하지 않고, 원본 대화와 Markdown 미리보기의 렌더된 표를 읽었다. H001–H454의 한·영 표기와 20개 category, R01–R48 창작 조합을 전사하고 UI와 로컬 전사의 checksum을 확인했다.

원본 Markdown/JSON의 다운로드 bytes는 확보하지 못했다. 따라서 로컬 TSV의 hash는 **전사본 hash**이며 원본 파일 hash가 아니다. 원본 표의 설명은 조사 입력이고, 표에 나온 연상·성격·권장 조합은 증거가 아니다. 454행의 존재 확인과 454개 독립 정의의 일차 검증은 구분한다.

원본은 [키워드 전사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-20261008/reference/keyword-inventory.tsv), [48개 조합](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-20261008/reference/character-combinations.tsv), [출처 수령 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-20261008/reference/SOURCE-RECEIPT.json)에 보존했다. 초기 잘린 preview도 별도로 남겼다.

### 20개 입력 영역과 반영 방향

아래 명칭은 이 보고서의 범위 요약이다. category 숫자와 H ID는 원본을 따른다. 모든 행의 처리 방향과 의미 카드 연결은 [전체 연구 crosswalk](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-20261008/RESEARCH-CROSSWALK.json)에 있다.

| 원본 범위 | 수 | 의미 분해와 반영 방향 |
|---|---:|---|
| 01 H001–H030 길이·해부 부위·볼륨 | 30 | body landmark와 selected ends, 앞/뒤/옆 scope; 수축·자세·크롭 제한; 가마/헤어라인은 커트 identity와 분리 |
| 02 H031–H046 굵기·밀도·컬 | 16 | diameter/density/volume 독립 축, S/spiral/zigzag, 혼합 pattern과 가닥 뭉침; 숫자 curl taxonomy는 출처별 scheme |
| 03 H047–H064 커트 구조·끝 처리 | 18 | 길이 배열·연결·무게·끝 분리; point/razor/texturizing 도구·시술은 결과와 별도 |
| 04 H065–H093 쇼트컷·바버 | 29 | family와 변형, side/top/nape 구역; fade 위치×경로×최단 endpoint; guard/각도는 사진에서 역산하지 않음 |
| 05 H094–H110 보브·중장발 커트 | 17 | perimeter, front/back contrast, stacking, short cap/long underlayer; family끼리 배타성 금지 |
| 06 H111–H127 한국 통칭·펌 | 17 | 살롱 이름과 cut/service/current fringe shape를 분리; 허쉬·태슬·리프·가일의 고정 규격 보류 |
| 07 H128–H150 앞머리·가르마 | 23 | coverage, tip texture, edge, 끝 위치, opening, part path; 안 보이는 scalp line은 방향만으로 확정하지 않음 |
| 08 H151–H172 세팅·컬·끝 방향 | 22 | 현재 가닥 경로와 root/end 방향; 열기구/펌/드라이/teasing 원인은 명시 문맥으로만 유지 |
| 09 H173–H191 꼬리·반묶음·puff | 19 | base count/height/side, tail continuity, free lower layer; 꼬리 끝 위치≠묶음 위치 |
| 10 H192–H209 번·롤·업두 | 18 | 감겨 들어가는 길이, 밑동, loop/fold orientation; 세로 twist/가로 tuck, 자유 curl puff를 분리 |
| 11 H210–H234 땋기·꼬임·locs | 25 | over/under crossing, 추가 가닥, scalp/free path, partition, two-section twist/cord; 설치·자연/faux origin은 별도 |
| 12 H235–H250 색 축·그레이 처리 | 16 | hair owner의 상대 명도·색상·채도·온도; brand scale, pigment/process와 외형을 분리 |
| 13 H251–H286 염색법·배색 | 36 | method/longevity 대 result, ribbon width, root/tip, split/inner/face/tip region, boundary; 공존 가능한 축 |
| 14 H287–H304 검정·갈색 계열 | 18 | 상대 명도·온도·채도·반사와 region grammar; natural/ash/blue-black은 원인·광원과 구분 |
| 15 H305–H325 블론드·회색·흰색 | 21 | 여러 외형 조합, salt-and-pepper/forelock의 분포; poliosis는 임상 sign과 흰 외형의 경계 |
| 16 H326–H357 레드·패션색·발광 | 32 | 공통 색 축 재사용, 지역별 palette와 관계; 선명한 neon/금속 반사/자체 발광 구분 |
| 17 H358–H385 표면·환경·상태 | 28 | gloss/matte/clump/frizz/disorder/water/stain/damage 부위; 사건·물질·행동 원인 미확인 표시 |
| 18 H386–H415 장식·모발 피스 | 30 | wraps/grips/inserts/threads/connects, piece base와 주변 hair; subtype 설치 구조의 직접 자료 부족은 hold |
| 19 H416–H432 문화·서브컬처·화보 용어 | 17 | 댕기/상투 구조와 맥락, broad editorial realization; 정체성·행동·성격 의무 금지; 비시각 관심은 context-only |
| 20 H433–H454 캐릭터·판타지 헤어 | 22 | platform namespace, protruding count, taper, material, occlusion/interaction/light; 시간적 운동과 정지 형상 분리 |

### 결과물의 읽는 순서

[SEMANTIC-MODEL.md](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-20261008/SEMANTIC-MODEL.md)는 13개 관찰 축과 관계 모델, [INTEGRATION-PLAN.md](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-20261008/INTEGRATION-PLAN.md)는 실제 source·후보·프로필·인덱스·검증 반영 순서를 설명한다.

[커트 분야](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-20261008/specialist-cuts.md), [묶음·땋기·질감 분야](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-20261008/specialist-topology.md), [염색·표면·판타지 분야](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-20261008/specialist-color-state.md)에 개별 정의와 출처를 정리했다. 추가 쇼트컷·보브 구분은 [보충 조사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-20261008/cuts-supplement.md)에 있다.

<!-- ASSEMBLY-STATS:START -->
최종 집계: **의미 카드 194개**, 전체 **454개 처리 경로**, 그중 232개 입력에 상세 카드 연결, **후보 초안 32개**, **프로필·번들 설계 16개**, **대조 설계 69개 + 경계 사례 20개**다. 모두 연구 산출물이며 production 채택 수가 아니다.

출처 레코드는 105개이며 직접 본문/API 100개와 검색·접근 제한 5개를 구분했다. 중복을 정규화한 URL 문자열은 151개다. 플랫폼 위키의 여러 문서를 묶은 레코드가 있어 레코드 수와 페이지 수가 다르다. 이 숫자는 독립 기관 수나 모든 명칭의 검증 수가 아니다.
<!-- ASSEMBLY-STATS:END -->

## 현행 데이터에서 확인한 상태

manifest에 등록된 102개 extension과 base authored source를 읽었다. 조사 시점의 raw candidate rows는 10,531개, raw profile rows는 2,321개다. 생성 인덱스나 runtime 로더를 실행한 수치가 아니다. 기존 미커밋 source도 포함한 working checkout의 상태다.

hair_style는 105개, hair_color는 27개다. 이 132개 중 `concept_units` 78개, `relations` 47개, `affected_properties` 40개가 있다. 모든 simple 후보에 구조 필드가 없다고 오류로 볼 수는 없지만, 새로운 세부 선택·잠금·소유자 제어에는 효과와 관계의 명시가 필요하다.

원본 전체 용어의 whole-term normalized surface match는 36/454다. 그중 hair_style/hair_color/wearable_accessory 또는 profile에 연결된 행은 31개이며 다른 sense/slot의 문자열 일치도 있다. 전체 긍정 문구의 bounded mention으로 범위를 넓히면 124행이 잡힌다. **418개의 문자열 미일치는 418개의 의미 공백을 뜻하지 않는다.** 예컨대 long/color/tail 복합 후보, Y2K의 구조 문구, 한국·영문 변형이 다른 이름으로 존재한다.

기본 전용 헤어 프로필 7개만 조사하면 기존 subculture/Y2K/캐릭터 의미를 놓친다. 원본 전용 profile은 two-block, hime, cornrows, locs, bilateral twintails, balayage ribbons, 실제 wet/damp state다. 전체 등록 source까지 대조한 결과와 raw hash는 [CURRENT-DATA-AUDIT.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-20261008/CURRENT-DATA-AUDIT.json)에 있다. exact/BM25F/embedding 순위·실제 hard activation은 실행하지 않았다.

## 조사로 달라지는 중요한 의미 경계

### 1. 커트: 이름보다 영역·길이 배열을 보존

Pivot Point의 구조 교육과 Sassoon의 혼합 사례를 보면, one-length 외곽, graduation의 무게, 내부 layering은 같은 측정값이 아니다. 같은 머리에 여러 구조가 함께 있을 수 있다. 완성 사진에서 시술 elevation angle·strand length equality를 역산했다고 판단하지 않는다. [Pivot Point](https://www.pivot-point.com/measurements-structures/), [Sassoon](https://online.sassoon-global.com/online-content-finder/course/bac-graduation-lines-and-layers.html).

A-line은 전후 끝선의 길이 차이, stacked는 후두부·목덜미에서 층이 쌓이는 부위의 축으로 다룬다. 브랜드별 명명은 겹친다. 이를 배타 클래스로 만들면 A-line stacked bob 같은 직접 교육 용례를 잘못 거부한다. 정면만 보이면 뒤 stacking은 미확인이다. [John Frieda의 A-line 용례](https://www.johnfrieda.com/en-uk/blog/hairstyles/hairstyles-for-straight-hair/), [직접 A-line stacked bob 교육](https://boysandgirlshairstyles.com/a-line-haircut-stacked-bob/).

히메의 얼굴 옆 shelf와 젤리피시의 옆·뒤 둘레 cap은 정면 단차만으로 같다고 판단하면 안 된다. 현대 히메에는 얼굴 레이어·컬과 합쳐진 사례가 있고, fringe 높이도 달라진다. 모든 히메에 조밀한 검정 blunt bangs를 추가하는 기본값은 제거 대상이 아니라 **만들지 말아야 할 추론**이다. [Alexim](https://www.aleximparrucchieri.com/jellyfish-cut-hime-cut/), [MINX 혼합 사례](https://minx-net.co.jp/styling/5103), [EARTH의 히메 사례](https://hairmake-earth.com/hair-style/hair_style-36205/).

한국 통칭은 살롱이 제안하는 cut·perm·현재 styling을 분리한다. 가일은 실제로 한쪽을 올린 형태와 양쪽을 내린 parted 연출, 리프와의 혼합이 있다. 허쉬·태슬·리프·애즈를 고정 layer-height/끝 질감/이마 opening 비율로 정의하지 않는다. H115의 원문 영문 `Gail-style parted hair`는 유지하고 제안 검색 철자와 유래 검증을 따로 둔다. [EVANSTYLE 가일](https://evanstyle.co.kr/product/b-030/2207/), [가일·리프 혼합](https://evanstyle.co.kr/product/detail.html?cate_no=12&display_group=1&product_no=2293).

### 2. 앞머리와 페이드: 독립 축의 조합

full/blunt/micro 앞머리는 덮는 범위·끝선·길이 축이다. 세 가지를 동시에 요청할 수 있다. see-through의 반복 skin gap과 wispy의 가벼운 끝 처리는 용례상 중첩되므로 배타적인 동의어 집합을 만들지 않는다. [Wella의 유형 구분](https://www.wella.com/professional/en-SE/blog/hair-care/bangs-hair-ideas), [L’Oréal 앞머리 용례](https://www.lorealparisusa.com/beauty-magazine/hair-style/hairstyle-trends/the-best-bangs-for-every-hair-type).

fade는 높이(low/high), 경로(drop/burst), 최단 부분(skin/retained hair)을 분리한다. 귀 뒤에서 내려가는 drop은 피부까지 짧게 끝나는 skin과 동시에 있을 수 있다. taper/fade의 지역적 범위도 중첩되므로 숫자 cm·guard로 보편 경계를 만든다는 계획은 세우지 않았다. [Pall Mall Barbers](https://www.pallmallbarbers.com/pmb-news/best-mens-fade-haircuts-2024-your-guide-to-the-latest-trends/).

### 3. 묶음: 밑동과 남은 길이의 연결

포니테일의 높이는 꼬리 끝 위치가 아니라 묶는 밑동 위치다. side ponytail도 한쪽으로 흘러내린 꼬리와 한쪽 밑동이 다르다. half-up은 상부 묶음 외에 별도의 풀린 아래층이 있어야 하며 앞에 남은 tendril 두 가닥으로 이를 대체하지 않는다. bubble ponytail의 밴드 분할은 실제 strand weave와 구분한다. [L’Oréal 포니테일 사례](https://www.lorealparisusa.com/beauty-magazine/hair-style/updo-and-bun-hairstyles/cool-ponytails-for-curly-hair).

pineapple의 자유 컬, 감겨 들어간 topknot, 국소 puff는 결과 구조로 분리하되 이름의 현대 변형도 허용한다. 세로 French twist와 가로 Gibson tuck은 rear view의 fold 방향이 중요하다. [Davines 업두 사례](https://ca.davines.com/blogs/news/20-updo-hairstyles-for-everyone), [Royal Collection Trust Gibson tuck](https://media.rct.uk/sites/default/files/resources/PDF%20Gibson%20Tuck%20Hairstyle.pdf).

### 4. 땋기: 교차·두피 경로·partition·설치법

French/Dutch는 교차의 위/아래와 추가 가닥 경로를 함께 봐야 한다. 자유 끝만 보고 두피의 방법을 판정하지 않는다. cornrows는 두피를 따라 이어지는 row, box braids는 구획과 자유 길이, rope twist는 두 묶음의 나선 경계로 설명한다. [L’Oréal의 직접 땋기 교육](https://www.lorealparisusa.com/beauty-magazine/hair-style/updo-and-bun-hairstyles/five-braid-tutorials).

box partition과 knotless root/설치 방식은 공존한다. 정지 사진에서 보이는 root geometry와 실제 설치 provenance를 구분한다. locs의 섬유 몸체, 꼬임 경계, faux 제작 이력도 일대일 분류가 아니다. protective라는 이름을 인물의 실제 모발 건강·안전 효과로 저장하지 않는다. [Box/knotless](https://www.hair.com/box-braids-vs-knotless-braids.html), [protective 용례](https://www.hair.com/protective-hairstyles.html).

### 5. 질감: 직경·밀도·부피·잔가닥

fine hair의 개별 굵기, 모발 분포, 외곽 volume은 독립적으로 표현한다. broad curl clump는 단일 coarse fiber가 아니다. 일반 인물사진에는 실제 직경과 단위 면적 모발 수를 측정할 정보가 충분하지 않을 수 있으므로 apparent coverage/외곽 부피를 보고하고 측정 의미는 보류한다. [Aveda의 굵기·숱 구분](https://www.aveda.com/hair-care/for-fine-and-thinning-hair).

H022의 baby hairs/flyaways는 하나의 원본 행에서 두 카드로 나눴다. baby hair는 헤어라인의 짧은 가닥, flyaway는 주 흐름에서 솟는 상태이며 함께 존재할 수 있다. laid edges는 짧은 헤어라인 가닥의 정렬·곡선 변형이다. 이를 실제 성장·손상·위생·인종의 증거로 사용하지 않는다. [Flyaways](https://www.lorealparisusa.com/beauty-magazine/hair-care/frizzy-hair/tips-to-tame-flyaways), [헤어라인 styling](https://www.lorealparisusa.com/beauty-magazine/hair-style/hairstyle-trends/guide-to-edge-styling).

### 6. 색: 방법·대비·위치·경계·광원을 분리

balayage는 시술 방식이고 ombré는 길이 방향 색 변화다. 직접 교육은 둘의 결합을 허용한다. 기존 `balayage_ribbon_color_placement`의 불규칙한 밝은 ribbon·어두운 roots는 **좁은 선택형 결과**로 유용하지만, 모든 발레아주의 보편적 결과로 활성화하기 어렵다. generic method와 selected pattern을 분리하는 P0 계획을 세웠다. [L’Oréal PPD 교육](https://www.hair.com/balayage-vs-highlights.html).

highlight/lowlight는 바탕과 상대적인 명도, babylight/chunky는 폭, shadow root는 뿌리와 전이, money piece는 얼굴 앞 구역, peekaboo/underlights는 층 위치와 가림 관계다. 이 축은 조합 가능하다. legacy Wella 일부 본문은 현재 다른 글로 이동했으므로 검색에 남은 내용만으로 정의 검증 완료를 선언하지 않았다. [직접 babylight 교육](https://www.hair.com/how-to-get-natural-highlights.html), [color melt](https://www.hair.com/color-melt.html).

갈색·블론드·패션색 이름은 동일한 hue/lightness/saturation/temperature grammar를 재사용한다. 브랜드별 level은 namespace를 보존하고 universal RGB로 고정하지 않는다. 모발의 흡수·반사와 시점·광원 때문에 겉색은 달라질 수 있다. 검색용 positive 의미는 모발 소유자의 색을 설명하고, 외부 조명·specular·전역 grading을 separate boundary로 둔다. [Marschner et al. 물리 연구](https://graphics.stanford.edu/papers/hair/), [PBRT](https://www.pbr-book.org/4ed/Reflection_Models/Scattering_from_Hair).

### 7. Wet look과 실제 수분: 현재 데이터의 우선 수정 후보

Wella의 wet-look gel은 마르거나 축축한 모발에 바르고 자연 건조하는 연출을 안내한다. 따라서 wet look이라는 말이 물방울·비·피부부착·실제 수분의 지속을 필수로 뜻하지 않는다. [Wella 공식 제품](https://www.wella.com/international/hair-style/gel/wella-shockwaves-extra-strong-wet-look-gel-200-ml).

현행 `wet_damp_clumped_hair_state.activation.exact_terms`에는 `wet-look hair`/`wet look hair`가 있으나 정의·evidence는 실제/coherent moisture, reduced volume, bundles, local adherence 또는 downward weight를 다룬다. H368 finish와 H369 actual moisture를 분리하는 계획이 필요하다. 이미 있는 비부착 처짐 대안은 유지한다. horror의 명시적 cheek/neck contact 변형은 그대로 좁은 변형으로 남긴다. 이는 source 정적 조사 결과이며 live activation이나 픽셀 오류를 재현했다고 보고하지 않는다.

표면 반사·뭉침만으로 실제 젖은 원인을 판별할 수는 없다. 물리 연구의 응집 모형은 형상의 개연성을 설명할 뿐 이미지 분류기의 정답을 제공하지 않는다. 환경과 사용자 문맥, 선택된 evidence를 별도로 연결한다. [Bico et al. 초록](https://pubmed.ncbi.nlm.nih.gov/15592402/).

### 8. 장식과 피스: 물체 나열에서 접합 관계로

30개 장식·피스 용어를 wrap/tie, insert, grip/clip, head-cover, strand-adornment, placed ornament, extension-piece, hairpiece-base의 8개 접합군으로 정리했다. scrunchie의 밑동 encircling, claw clip의 hair-section grip, ponytail-piece의 기존 밑동 연결은 직접 제조사 용례를 확인했다. [Kitsch scrunchie](https://www.mykitsch.com/products/cherry-blossom-ruched-satin-scrunchies-5pc-set), [Kitsch clip](https://www.mykitsch.com/products/black-tort-micro-cloud-clip-set), [BELLAMI 설치 변형](https://eu.bellamihair.com/pages/frequently-asked-questions).

lace-front와 topper는 배타 클래스가 아니다. 국소 topper에 lace front가 있는 제품이 존재하며 색명도 설치 위치에 따라 front placement가 달라진다. 제품명·clip 수·cm·치수는 제품 namespace의 사례이며 전역 의미 규칙으로 고정하지 않는다. 일반 완성 사진이 특정 설치법·실제 가발·임상 상태를 입증하는 것은 아니다. [Jon Renau Top Smart](https://jonrenau.com/top-smart-18), [제품별 front placement](https://jonrenau.com/blog/catalina-blonde-toppers/).

barrette/snap/banana, U-pin/comb, beads/cuffs/rings/tinsel, halo/clip bangs 등의 특정 subtype은 관계 설계와 직접 정의 확인을 구분해 후속 근거 보완 대상으로 남겼다. tape-in hybrid 자료는 현재 직접 URL이 404이며 검색 본문만 참고 상태다. 30개 모두의 실제 설치법을 검증했다는 주장은 하지 않는다. [ACCESSORY-DISPOSITION.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-20261008/ACCESSORY-DISPOSITION.json).

### 9. 문화·판타지·서사: 이름의 맥락을 보존

댕기는 천 장식과 땋은 끝의 연결, 상투는 정수리로 모아 감아 올린 길이의 구조로 분리했다. 역사적 용도의 다양성이 있으므로 색·실루엣만으로 혼인·신분·시대를 확정하지 않는다. [한국학중앙연구원 댕기](https://encykorea.aks.ac.kr/Article/E0015303), [상투](https://encykorea.aks.ac.kr/Article/E0027380).

ahoge/antenna의 돌출 수, drill의 tapering conical spiral, hair intakes의 forward scoop는 플랫폼의 현재 자체 정의를 공식 wiki API로 확인했다. 이 의미는 해당 namespace에 보존하며 자연 헤어스타일과 인물의 지능·성격·사회적 역할로 옮기지 않는다. [Ahoge](https://danbooru.donmai.us/wiki_pages/ahoge), [Drill hair](https://danbooru.donmai.us/wiki_pages/drill_hair), [Hair intakes](https://danbooru.donmai.us/wiki_pages/hair_intakes).

H204/H387 hair bow, H397/H447 hair scarf는 재료와 연결 경로가 다르다. 편의적 가림·모발로 만든 garment·prehensile manipulation도 서로 다른 관계다. 정지 프레임은 겹침·접촉·공중 위치를 보여줄 수 있으나 시간적 의지·감정 변화·사건 원인을 확정하지 않는다. 폴리오시스의 흰 patch는 appearance counterpart로 표현하고 사진 진단을 하지 않는다. [모발 scarf 정의](https://danbooru.donmai.us/wiki_pages/hair_scarf), [Poliosis 정의](https://dermnetnz.org/topics/poliosis).

원본 R01–R48은 스타일링·캐릭터 조합안으로 보존한다. hairstyle→personality/age/ethnicity/behavior라는 hard 매핑을 만들지 않는다. 감정이나 서사가 필요하면 별도의 actor/target/action/affect/consequence와 관찰 가능한 접촉·변화로 작성한다. 비시각 관심 개념 H432에는 특정 헤어 외형의 의무를 만들지 않는다.

## 기존 데이터와의 구체적인 대응

아래는 실제 authored ID를 조회한 reuse/enrichment 방향이다. 동일 이름이 있다는 사실만으로 source의 모든 의미가 동등하다고 판정하지 않는다. 완전한 기존 source ref와 provisional entry는 [32개 후보 초안](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-20261008/CANDIDATE-DRAFTS.json)에 있다.

| 의미 | 현행 대응 | 제안 |
|---|---|---|
| 히메 / 투블럭 | `hime_cut`, `hime_cut_structural`; `two_block_korean_cut`, `two_block_disconnected_cut` | 기존 구조 보존, 지역 변형·bangs 옵션 검토, broad 명칭이 고정 recipe를 확대하지 않도록 함 |
| 보브·자유 땋기·링렛 | `ca_compact_bob`, `ca_hanging_hair_braid`, `appearance_h042` | 단순 family와 구체 관계를 재사용; 필요 부위와 effect lock 연결 |
| 높은 포니·반묶음·버블 | `y2kr_high_pony`, `y2kr_half_up`, `y2kr_bubble_pony` | root height, lower layer, band partition 관계 재사용 |
| 좌우 땋은 꼬리·옆 포니 | `sca_h11`, `sca_h09` | count/root/path를 보존; pigtails ambiguous bare alias 검토 |
| 콘로우 / locs | `cornrows`, `cornrow_scalp_row_topology`; legacy ID `dreadlocks`, `locs_cord_structure` | scalp path/cord body 강화, compatibility ID 유지, preferred term은 locs |
| 좌우색·겉/안층·root/tip | `sca_h19/20/21`, `y2kr_two_tone/peekaboo` | 기존 partition 관계 재사용, owner/color/lighting 경계와 공존 fixture 보강 |
| money piece·chunky·skunk | `y2kr_money_piece`, `y2kr_chunky_highlights`, `y2kr_skunk_stripe` | front position/width/lightness 분리; hair_style의 legacy color 후보와 source 대응 검토 |
| ahoge·antenna·drill | `sca_h01`, `sca_h02`, `sca_h05` | platform definition과 count/taper/roots 정렬; 새 동의 후보 중복을 줄임 |
| 천 리본·스크런치 | `appearance_h106`, `egr_attached_trailing_hair_ribbon`, `y2kr_scrunchie` | hair_style/장식 slot의 원본 owner와 effect 범위 대조 후 접합 재사용 |
| 실제 수분·물속 부유·horror contact | `wet_damp_clumped_hair_state`, `water_w156/157`, `hr_wet_hair_skin_contact` | generic finish와 환경·contact 선택형 관계를 분리; 기존 좁은 의무 보존 |

base의 long-black-twintails, balayage_brown, copper_red_hair처럼 style/color/accessory가 함께 들어간 legacy 후보는 history와 ID를 유지하면서 원자 후보와 optional bundle로 분해할 수 있다. 기존 archived record를 조용히 바꾸는 직접 rename이나 일괄 재작성은 제안하지 않는다.

## 반영 계획과 검증

반영은 P0 의미 경계 수정 → P1 전체 crosswalk·재사용 확정 → P2 authored source·후보·프로필·번들 → P3 인덱스 재생성 → P4 source/조회/선택 회귀 → P5 native 픽셀 판정 순으로 진행한다. 실제 파일명, 현행 schema·maintenance successor·벡터 재사용 조건, 테스트 범위와 발행 경계는 [상세 반영 계획](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-20261008/INTEGRATION-PLAN.md)에 있다.

[프로필·번들 설계](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-20261008/PROFILE-AND-BUNDLE-PLAN.json)는 profile association이 hard activation을 뜻하지 않게 구성했다. 단순 색·길이마다 profile을 만들지 않고, 관계 판정과 여러 구성요소의 duty가 필요한 곳을 우선한다.

[검증 사례](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-20261008/VALIDATION-CASES.jsonl)는 분야별 최소 대조쌍과 20개 소유자·부정·공존·의미 경계 사례다. 전부 실행 전 설계다. 앞뒤 cap, 두피 crossing, 묶임점, 안층 reveal, 재료 continuity 등은 해당 관계가 같은 crop에서 보이는 경우만 판정한다. 가림은 `UNOBSERVABLE_NOT_PASS`, 선택된 의무의 일부 실패는 실패이며 나머지 요소의 성공으로 상쇄하지 않는다.

이번에 확인한 것은 전사 무결성, raw source 현황, 출처의 주장 범위, 연구 artifact 참조와 schema 형태다. source-image 픽셀, live runtime, BM25F/embedding 순위, 후보 선택, 최종 prompt, native 생성 픽셀, 사용자 수용은 검증하지 않았다. 자료량 자체나 이름 검색 hit를 실제 품질 개선으로 보고하지 않는다.

연구 참조·원본 표기·초안 형태의 무결성 검사는 통과했다. 작업 중 체크아웃의 HEAD가 별도 VEL 변경 커밋 `30fc97a8`로 진행했고, 조사 스냅샷 1,502개 중 semantic index와 V35 history test 2개가 달라졌다. 1,500개는 bytes/mode가 같고 삭제된 파일은 없으며, 이번 raw audit에 사용한 authored source의 hash는 모두 동일하다. 해당 두 파일과 커밋은 이 연구에서 작성하거나 복원하지 않았다. 전체 기존 체크아웃이 고정됐다는 주장 대신 관찰된 차이를 [RESEARCH-VALIDATION.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-20261008/RESEARCH-VALIDATION.json)에 기록했다.

## 출처 한계와 남은 작업

[SOURCE-CATALOG.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/character-hair-20261008/SOURCE-CATALOG.json)은 출처 레코드와 URL 수, 직접 본문/API와 검색·redirect·접근 제한을 구분한다. 제조사·교육·살롱의 직접 용례는 해당 주장의 일차 자료이지만 전 업계의 보편 표준은 아니다. source의 사진은 이 연구에서 픽셀로 독립 확인하지 않았다. 카드의 observable geometry·후보 문구·게이트는 이를 이용한 작성자의 설계 제안이다.

세부 정의의 근거가 부족한 지역 통칭·일부 설치 subtype·일부 색명·판타지 변형은 보류를 유지한다. 이미 직접 자료가 있는 공통 축으로 확장 가능한 항목은 그 축을 재사용하고, 선택에 실질적인 차이가 있는 명칭은 직접 자료를 보완한다. 454행 전부에 경로를 지정했다는 사실이 이 후속 검증을 대신하지 않는다.

현재 산출물은 다음 반영을 리뷰하고 시작할 수 있는 구체적 연구와 계획이다. 실제 source 채택, 빌드, 조회, 픽셀 판정은 각각의 증거가 생긴 뒤 완료 상태를 갱신한다.
