# Y2K 시각 의미·후보팩 데이터 보강 리서치

조사일: 2026-09-27. 기준 대화: [Y2K 스타일 조사](chatgpt-conversation://6ab8ae0e-2324-83e9-a0e6-2457899b580c). 저장소 기준 리비전과 읽은 데이터 파일의 SHA-256은 [validation.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/y2k-style-20260927/validation.json)에 기록했다.

**보강의 중심은 ‘Y2K’라는 라벨의 반복이 아니라, 형태·재료·배치·소유 대상·시대 조건을 서로 분리하는 것이다.** 참조 대화의 20개 분류, 308개 키워드 행을 검토하고 306개의 구성요소 정의, 21개 스타일 계열, 20개의 선택적 후보 묶음으로 재구성했다. 37개 자료를 조사했으며 31개는 본문 또는 PDF 텍스트를 읽었고 6개는 검색 발췌까지만 확인했다. ACROSS 원본 페이지 3개의 일부 사진도 직접 확인했다. 이는 3개의 독립적인 사진집이나 전체 사진 표본을 뜻하지 않는다.

이번 결과는 연구 자료와 코드 계약을 검사한 **데이터 제안**이다. 실제 생성기의 소스 목록에 등록하거나 인덱스를 재생성하지 않았으며, 이미지 생성·실제 후보 노출·선택·픽셀 품질·사용자 수용성은 검증하지 않았다. 308개 행 모두에 연결 대상을 만들었다는 것은 역사적 사실 308개가 확인됐다는 뜻이 아니다. 개별 정의는 연구자가 작성한 관찰 가능한 조건이고, 출처가 그 모든 조건을 직접 입증하는 것은 아니다.

## 1. 참조 대화에서 수정하거나 분리해야 할 전제

| 참조 키워드의 묶음 | 조사 결과와 수정 방향 | 데이터 처리 |
|---|---|---|
| 초기 미래주의와 McBling | 1999년 Givenchy 런웨이에는 회로·플라스틱·빛을 사용한 미래주의 사례가 있다. McBling은 후대 기사에서 대략 2003–2008로 분류한다. | 같은 연대의 동의어로 합치지 않고 시대·장르 문맥을 별도로 둔다. |
| Cyber Y2K / Cybercore | 테크·클럽·SF 시각 요소는 겹칠 수 있으나 현대 인터넷 명칭까지 당대의 자칭으로 확정할 수 없다. | 명칭은 검색 계열, 실제 후보는 메시·렌즈 곡률·프린트·표면으로 연결한다. |
| Sporty / Streetwear | 스포츠 패널, 힙합의 의복 역사, 스케이트 착장에는 다른 맥락이 있다. | 저지·트랙 재킷·넓은 팬츠를 원자 요소로 두고 문화·활동은 별도 증거를 요구한다. |
| Mall Goth / Nu-metal / Emo / Scene | 인접 계열이지만 음악 장르·착장·후기 인터넷 유행은 동일하지 않다. | 한 검은 상의에서 다른 계열의 모든 요소를 연쇄 활성화하지 않는다. 정확한 지역·연대는 보류 항목도 있다. |
| Gyaru / Heisei Gyaru | 시부야·갸루 자료와 1999 거리 관찰은 확인된다. 하나의 시대명과 내부 변이가 있는 스타일을 동일시하면 정보가 소실된다. | 시기·장소·하위 계열을 따로 기록하고 피부색·국적·교복은 필수 요소로 만들지 않는다. |
| Boho 2004–2007 | 중반 2000년대 층입기 문맥은 지지되지만 정확한 시작·종료 연도는 이번 자료로 확정하지 않았다. | 근사 시대 문맥으로 유지한다. |
| Indie Sleaze 2006–2012 | 읽은 회고 기사는 대략 2006–2013을 사용한다. | 범위를 근사치로 보존하며 특정 종료 연도를 정답으로 고정하지 않는다. |
| Acubi / Balletcore / Frutiger Aero | 현대 재해석, 현대 명칭의 재유행, 디지털 디자인 분류가 서로 다른 축이다. | 원조 Y2K 고증·현대 혼합·UI 배경을 분리한다. |

초기 미래주의 사례는 [Vogue의 Givenchy Fall 1999 아카이브](https://www.vogue.com/fashion-shows/fall-1999-ready-to-wear/givenchy), McBling의 근사 범위는 [Vogue의 분류 기사](https://www.vogue.com/article/what-is-mcbling)에 근거한다. 이는 전 세계 패션의 보편적인 시대 경계가 아니다.

힙합의 긴 역사와 디자이너·스포츠 의복·데님의 연결은 [Museum at FIT 전시](https://www.fitnyc.edu/museum/exhibitions/hip-hop-style/)에서 확인했다. 이 자료를 스케이트 착장 전체의 검증 근거로 확대하지 않았다. 레이브 요소가 Y2K 이전에도 존재했다는 선행 맥락은 [V&A Club to Catwalk 전시 자료](https://media.vam.ac.uk/media/documents/ClubtoCatwalk-press-release.pdf)의 검색 발췌에 한정한다.

갸루의 시부야 문맥은 [Web Japan](https://web-japan.org/trends/trend_scene/ts005/ts005_map.html), 후기 계열의 근사 범위는 [Vogue의 What Comes After Y2K?](https://www.vogue.com/article/what-comes-after-y2k)에 근거한다. Nu-metal·Emo·Scene의 정확한 시작 연도는 추가 당대 자료가 필요하다. Acubi의 현대 문맥은 [CNA의 2026 설명](https://cnalifestyle.channelnewsasia.com/style-beauty/acubi-gen-z-korean-fashion-583516), Balletcore 명칭의 현대 재유행은 [Vogue의 2022 기사](https://www.vogue.com/article/ballet-style-is-back-this-time-lets-make-it-size-inclusive), Frutiger Aero의 약 2005–2013 범위는 [CARI의 디자인 분류](https://cari.institute/aesthetics/frutiger-aero)를 각각 사용했다.

## 2. 당대 사진과 후대 설명을 다르게 사용하기

당대 거리 관찰은 ‘그 시기·그 장소에서 존재했는가’를 확인하는 데 유용하다. 후대 기사는 스타일 명칭과 재유행을 찾는 데 유용하고, 현대 튜토리얼은 형태를 문장으로 설명하는 데 유용하다. 세 종류를 한 수준의 역사 증거로 계산하면 안 된다.

직접 본 [1999-02-13 ACROSS 페이지](https://www.web-across.com/observe/srnrj2000003pfyx.html)의 첫 화면에는 작은 가방을 몸 앞에 낮게 내려 들거나 긴 스트랩으로 착용한 사례가 보인다. 따라서 `mini shoulder bag`을 `short-strap underarm baguette`로 전부 바꾸면 실제 변이가 사라진다. **크기, 가방의 가로세로 형태, 스트랩 길이, 착용 위치는 서로 다른 필드여야 한다.** 이는 일부 화면의 관찰이며 시대 전체의 빈도 추정이 아니다.

직접 본 [2000-05-20 ACROSS 페이지](https://www.web-across.com/observe/d6eo3n000001p0d1.html)에는 짧은 팬츠와 여러 종류의 상의·작은 가방이 함께 보인다. 모든 2000년 착장이 낮은 허리, 핫핑크, 플랫폼, 반짝이는 미래주의였다는 결론은 나오지 않는다.

[당시 장식류의 하위 조사](https://www.web-across.com/observe/d6eo3n000001p0oq.html)는 ‘rhinestone’ 집계에 비즈·스팽글·자수·유리·크리스털 도안을 넓게 포함한다. 사진 화면에도 데님 재킷의 점 장식과 다른 의복의 장식·프린지가 보인다. 역사 자료의 집계 명칭은 그대로 보존하되, 새 물리 사전에서는 `faceted stone`, `flat sequin disc`, `bead`, `embroidery`를 서로 구별해야 한다. 작은 사진의 반짝이는 점을 모두 스톤으로 인증할 수는 없다.

사진 사용 범위와 읽기 상태는 [sources.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/y2k-style-20260927/sources.json)에 출처별로 기록했다. 원본 사진을 재배포하거나 학습 데이터셋으로 복제하지 않았다. 문화 명칭·당대 인터뷰의 개인 정보는 긍정 프롬프트에 넣지 않는다.

## 3. 현재 데이터의 공백

실제 로더가 선언한 기본 사전 1개와 확장 33개를 읽고, 후보·프리셋의 직접 필드만 조사했다. 생성된 인덱스나 프리셋 전체의 하위 필터를 검색해서 중복을 증폭시키지 않았다. 원문 필드의 문자열 포함 여부는 의미적 중복 판정과 다르므로 [current-data-gap-audit.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/y2k-style-20260927/current-data-gap-audit.json)에 검색 범위를 명시했다.

| 현재 확인한 자산 | 이미 있는 역할 | 보강할 부분 |
|---|---|---|
| `y2k_desk_gadget_stack`, `retro_flip_phone_prop`, `mp3_cd_sticker_stack_prop` | 포괄적인 레트로 소품·정물 | 모델별 구조, 세대·색·연도, 고리·케이블 연결 관계 |
| `kpop_glossy_y2k_stagewear`, `cyber_y2k_aesthetic`, Y2K 월드·팔레트 | 광택·스타일 검색 계열 | 광택의 표면 소유 대상, 직물과 플라스틱, 눈꺼풀과 입술의 영역 |
| `gyaru_fashion`, `gyaru_shibuya_glam` | 갸루 스타일·활동 문맥 | 하위 계열의 시기별 자료, 실제 부품·형태, 선택적으로 사용되는 요소 |
| `heisei_y2k_revival` | 현대 재해석임을 명시 | 고증 모드와 혼합 모드를 명시적으로 구분 |
| `direct_flash_y2k_snapshot` | 직광의 조명 관계 | Y2K 착장과 독립적으로 사용; 창문광 요청에서도 외형 유지 |
| 수영복의 `sw_candidate_midlowrise` | 수영복의 허리선 문맥 | 청바지·팬츠의 허리선과 동일 프로필로 취급하지 않기 |

이 범위에서 `spiky bun`, `butterfly clip`, `velour`, `baguette`, `bootcut`, `Razr`, `Sidekick`, `zigzag`, `crimp`, `chunky highlights` 등의 직접 문자열은 0건이었다. `terry`, `shield`, `nano`, `scene`처럼 다른 뜻이나 다른 소유 대상에서도 나타날 수 있는 문자열은 개별 레코드 검토가 필요하다. 0건을 개념의 완전 부재로, 검색 적중을 적절한 의복 데이터의 존재로 단정하지 않았다.

## 4. 제안 데이터의 구조

기본 단위는 다음과 같다.

`사용자 의미 → 구체 구성요소 → 소유 대상과 공간 범위 → 관계 → 혼동 대체물 → 필요한 촬영 범위 → 픽셀 판정`

예를 들어 `spiky bun`은 ‘Y2K 헤어’라는 설명에 머무르지 않는다. 모은 머리의 조밀한 번, 번의 외곽을 넘어 솟은 분리된 직선 끝가닥, 해당 머리 영역을 함께 정의한다. 번 없이 짧은 스파이크 머리를 만들거나 풀린 잔머리만 있는 번을 만드는 경우를 구별한다. 가르마와 끝가닥이 가려진 사진은 통과로 계산하지 않는다.

[semantic-components.proposed.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/y2k-style-20260927/semantic-components.proposed.json)의 각 레코드는 아래 내용을 갖는다.

- 정확한 소유 대상, 관찰 가능한 조건, 혼동 경계, 최소 화면 범위.
- 현재 슬롯과 기존 차원에 대한 연결.
- 출처의 역할과 주장 한계, 역사적 보급 여부의 미확인 상태.
- 소유 대상·형태·혼동 경계의 3개 픽셀 게이트.
- 아직 렌더링하거나 픽셀로 자격을 확인하지 않았다는 상태.

출처의 ‘존재·문맥’ 근거와 연구자의 ‘형태 정의’는 분리했다. 특히 일반 소재·네일·모자 지역 명칭은 원문 기술 자료나 당대 사진 추가 확인이 필요한 항목이 있다. 정의가 있다는 이유로 시대 고증을 인증하지 않는다.

### 헤어: 묶는 구조·가르마·질감·색·장식을 분리

| 구별할 항목 | 보강할 관찰 조건 | 주요 혼동 |
|---|---|---|
| Spiky bun / messy bun / spiky updo | 모은 덩어리, 번의 유무, 끝가닥의 분리와 방향 | 풀린 잔머리만 있거나 머리 전체를 짧게 바꿈 |
| Space buns / mini buns | 좌우의 큰 두 번과 여러 작은 번의 개수·배치 | 이름만 다르고 결과는 하나의 번 |
| Zigzag part / crimped lengths | 두피 가르마의 꺾임과 머리 길이의 작은 반복 굴곡 | 가르마 요청을 웨이브로 대체 |
| Tendrils / piecey strands | 앞쪽의 얇은 별도 가닥과 머리 전체의 분리된 다발 | 굵은 앞머리 또는 균일한 한 덩어리 |
| Chunky highlights / money piece / skunk stripe / peekaboo | 폭, 경계, 얼굴 앞쪽·연속 띠·안쪽 층의 위치 | 부드러운 전역 그라데이션 또는 조명 색으로 대체 |
| Butterfly / snap / mini claw clips | 날개 모양과 실제 클립, 납작한 스냅 구조, 맞물린 작은 집게 | 나비 프린트가 머리핀 증거를 대신함 |
| Baby braids / micro braids / beaded braids | 일부 가닥·촘촘한 여러 가닥·가닥에 붙은 비즈를 분리 | 모든 땋기를 동일화하거나 문화 기원을 Y2K로 주장 |

[L’Oréal의 현대 헤어 설명](https://www.lorealparisusa.com/beauty-magazine/hair-style/hairstyle-trends/2000s-hairstyles)과 [zigzag part 설명](https://www.lorealparisusa.com/beauty-magazine/hair-style/hairstyle-trends/zigzag-part-hairstyle)은 형태를 설명하는 참고자료다. 여기서 시작 연도·발명자·당대 전체의 보급률을 도출하지 않는다.

### 의복: 한 단어가 여러 축을 덮지 않게 하기

| 축 | 별도로 기록할 내용 | 예시 |
|---|---|---|
| 길이 | 상의·재킷·치마·팬츠 밑단 위치 | cropped denim jacket을 일반 denim jacket과 구별 |
| 허리선 | 자연 허리와 팬츠 상단의 상대 위치 | crop top이 있어도 high-rise일 수 있음 |
| 다리 형태 | 허벅지·무릎·밑단의 상대 폭 | bootcut의 작은 벌어짐과 큰 flare 구별 |
| 품 | 의복의 여유와 몸의 비율을 분리 | tiny top + big pants는 의복 볼륨 대비 |
| 구성 | 한 벌·여러 층·별도 경계 | dress over pants, layered tanks, visible straps |
| 부착 | 주머니·지퍼·셔링·고리·끈의 실제 위치 | cargo mini는 팬츠가 아니라 주머니 있는 짧은 치마 |
| 소재 | 팬츠 형태와 섬유 표면을 분리 | flare yoga pants에 데님 봉제선을 강제하지 않음 |

`low-rise`, `exposed midriff`, `cropped top`, `long torso impression`은 동의어가 아니다. 낮은 팬츠 허리와 높은 상의 밑단이 함께 보일 때 의복 경계 사이가 길어 보일 수 있지만, 이를 위해 인체 몸통을 늘리면 안 된다. `ultra-low`도 단순히 더 강한 Y2K로 자동 선택하지 않는다.

`whale tail`은 팬츠 위에 나온 별도의 속옷 옆선이라는 명시적 구성요소로만 남겼다. 허리 체인·벨트와 구별하며 모든 Y2K 착장에 자동 추가하지 않는다. 의미적으로 선택적인 세부라는 점을 데이터에 보존했다.

### 소재: 외관, 구조, 기능, 성분은 별개

| 표면 | 시각 정의 제안 | 사진만으로 확정할 수 없는 것 |
|---|---|---|
| Velour / terry | 짧고 조밀한 파일 / 작은 미절단 루프 | 원단 명칭·섬유 함유율의 인증 |
| Satin | 유연한 주름 위 연속적인 방향성 광택 | 실크 섬유라는 결론 |
| Mesh / sheer cloth | 반복된 구멍 / 이어진 얇은 반투명 막 | nylon 등 성분 |
| Metallic / iridescent / holographic | 금속 같은 반사 / 표면의 색 변화 / 회절처럼 나뉜 색 띠 | 실제 코팅 방식·광학 성능 |
| PVC / vinyl / patent | 필름형 구조·연속 광택·코팅된 형태를 분리 | PVC와 vinyl을 화학적으로 완전히 별개 물질로 인증 |
| Rhinestone / sequin / bead | 각면이 있는 입체 스톤 / 얇고 납작한 디스크 / 구슬과 연결 줄 | 실제 보석 등급·유리나 플라스틱 성분 |
| Chainmail / metal mesh | 연결된 고리 / 가는 금속형 망 구조 | 실제 금속 합금과 보호 성능 |
| Retroreflective trim | 광원과 가까운 관찰 방향으로 밝아지는 부분 | 안전 규격·재귀반사 성능 인증 |

재귀반사가 빛을 광원 쪽으로 돌려보내는 성질은 [3M의 기술 설명](https://www.3m.com/3M/en_US/scotchlite-reflective-material-us/industries-active-lifestyle/active-lifestyle/how-retroreflection-works/)과 [3M의 비교 도식이 있는 PDF](https://multimedia.3m.com/mws/media/1614613O/3mtm-scotchlitetm-reflective-material.pdf)를 읽었다. 단일 사진의 밝은 부분은 광택·노출·코팅의 다른 원인과 구별되지 않을 수 있다. 관련 픽셀 게이트는 인증이 아닌 표현 판정이다.

초기 [Cotton Incorporated 경로](https://www.cottoninc.com/quality-products/textile-resources/)는 열리지 않았지만, 후속 조사에서 CottonWorks의 기술 원문을 확인했다. [Mechanical Finishing](https://cottonworks.com/learning-hub/finishing/mechanical-finishing/)은 니트 velour의 한 제작 경로를 terry 루프 끝을 전단하는 과정으로 설명한다. [Pile Fabric 사전](https://cottonworks.com/encyclopedia-item/pile-fabric/)은 루프·절단 루프를, [직물 조직 설명](https://cottonworks.com/learning-hub/weaving/basic-woven-fabric-designs/)은 satin weave의 긴 float와 표면 광택을 설명한다. 따라서 루프와 절단 파일의 구별에는 기술 근거가 추가됐지만, 개별 생성 사진의 섬유 성분·원단 명칭·성능을 인증할 수는 없다. 공급자별 명칭 변이와 실제 표본의 확인은 남아 있다.

### 액세서리: 크기·토폴로지·곡률·착용 위치

`shield`는 하나의 차폐형 렌즈 구조를, `wraparound`는 얼굴 옆으로 감싸는 곡률을 설명한다. 단일 shield가 감쌀 수도 있고 두 렌즈가 감쌀 수도 있다. 같은 축의 경쟁 후보로 처리하지 않는다. 정면 한 장으로 옆 곡률을 확정하지 않도록 4가지 조합의 확인 설계를 만들었다.

가방은 크기, 가로로 긴 몸체, 짧은 스트랩, 겨드랑이 아래 위치, 형태의 유연성, 패턴, 금속 장식, 참 부착을 분리했다. [Fendi의 Baguette 자료](https://www.fendi.com/us-en/cm/articles/the-baguette-26424)는 대표적인 형태 문맥이며, 현재 제품의 모든 소재가 원형 출시 당시에도 같았다는 근거는 아니다.

Hoop의 기본 구조, oversized 크기, 귓불에 가까운 huggie 크기를 별도 레코드로 만들었다. 모티프는 목걸이·머리핀·네일·프린트에 각각 소유 대상을 지정한다. `star`라는 적중 하나로 네일의 별 장식을 목걸이로 대신할 수 없다. Pageboy·baker-boy·cabbie 같은 지역별 모자 명칭은 모양의 정교한 추가 검토를 명시해 두었다.

### 메이크업·네일: 영역과 마감을 분리

입술에서는 외곽선의 색, 중심부의 색, 둘 사이의 경계, 표면 gloss를 분리했다. 갈색 립 전체에 번쩍이는 하이라이트가 있다고 ‘갈색 외곽선 + 밝은 중심’이 완성된 것은 아니다. 눈꺼풀의 라일락 안료, 미세 서리광, 은색 안료, 안쪽 작은 광택도 각각 다른 영역·마감이다. [L’Oréal의 현대 재현 설명](https://www.lorealparisusa.com/beauty-magazine/makeup/makeup-trends/2000s-makeup)과 [Allure의 회고·재현 기사](https://www.allure.com/story/y2k-makeup-looks)는 이런 구별의 참고자료로 사용했다.

얇은 눈썹과 pencil처럼 그린 선은 별도 관찰 조건이며 Y2K 전체의 필수 조건이 아니다. 네일에서는 자유단의 사각 형태, 프렌치 끝의 색 경계, 코팅 표면, 부착한 스톤, 입체 별·나비를 분리했다. 전체 착장 사진에서 손톱이 몇 픽셀밖에 되지 않으면 네일 조건은 판정할 수 없다. 기술별 최초 유행 연도는 이번 조사에서 확정하지 않았다.

### 그래픽·글자: 도안과 실제 사물을 혼동하지 않기

참조 대화의 그래픽 13개 분류를 [graphic-groups.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/y2k-style-20260927/graphic-groups.json)에 보존하고 실제 형태로 연결했다. 과일·나비·별·왕관·회로·바코드·픽셀·불꽃·동물무늬·얼룩무늬·거미줄·글자는 도안 선택지이며 전부 동시 필수인 한 세트가 아니다.

프린트의 소유 대상은 의복 패널이다. `tattoo graphics`가 피부 문신이 되거나, 체리 프린트가 손에 든 실제 과일이 되거나, 회로 프린트가 배경의 작동 기계가 되면 의미가 바뀐다. `tribal`이라는 포괄 검색어는 특정 문화의 문양을 대신하는 긍정 정의로 넣지 않고, 뾰족한 추상 곡선 형태로 제한했다.

문자도 ‘글자의 형태’와 ‘실제 문자열’을 나눈다. 사용자가 티셔츠에 `SUN`을 요청하면 그 문자를 유지해야 한다. 모든 이미지에 무조건 `no text`를 넣으면 slogan tee의 의미가 사라진다. 상표·번호·바코드는 요청된 의미와 시각 판정 범위에 맞춰 처리하며, 장식 번호에서 실제 팀·선수·개인을 추론하지 않는다.

### 색: 이름보다 역할과 원인을 저장하기

8개의 배색 제안은 의복·소품 영역의 관계이다. 핫핑크는 McBling의 자동 필수색이 아니며, 다른 색의 벨루어와 스톤으로도 관련 구성은 표현할 수 있다. 얼굴이나 배경에 핑크빛 조명을 비추는 것은 핑크 후디 원단과 다른 원인이다.

`intrinsic_surface`, `illumination`, `capture_white_balance`, `global_grade`, `regional_grade`, `tone_response`를 계속 구분해야 한다. 원단 색을 판정하는 장면에서는 중성광을 사용하고, 조명을 시험하는 장면에서는 원단을 고정한다. 이번 제안은 기존 `color` 차원에 연결하며 새 상위 `palette` 차원을 만들지 않았다.

## 5. 소품의 연도와 세대

| 소품 | 확인한 시간 정보 | 고증에서 적용할 제한 |
|---|---|---|
| 첫 iPod | 2001-10-23 발표, 2001-11-10 구매 가능 예정 | 일반 소매 사용 장면의 1999·2000·2001년 초에 넣지 않음. 모든 MP3 플레이어를 금지하는 규칙은 아님. |
| 첫 iPod nano | 2005-09-07 발표 및 즉시 판매, 흰색·검정 | 1999·2001 nano는 부적합. 후대 핑크 금속형 세대와 구별. |
| Razr V3 | 2004-07-27 발표 | 발표 전 일반 장면을 제외하는 근거. 당일 지역별 소매 보급·핑크 변형은 별도 확인 필요. |
| Danger Hiptop / Sidekick | 박물관 기록의 2002 발표 | 1999 고증의 자동 소품으로 사용하지 않음. 세대별 키보드·회전 구조 별도 지정. |
| Sony DSC-F1 | 회사 역사에 1996 디지털 카메라 사례 | 모든 디지털 카메라가 후대라는 주장은 틀림. 모든 은색 초슬림 카메라가 1996 모델이라는 주장도 안 됨. |
| 프리쿠라 | 읽은 자료는 2011 기능 설명 | 촬영·편집·스티커 출력의 구조와 자동 보정 기능의 시기를 분리. |

시점은 [Apple의 2001 발표](https://www.apple.com/newsroom/2001/10/23Apple-Presents-iPod/), [Apple의 nano 발표](https://www.apple.com/newsroom/2005/09/07Apple-Introduces-iPod-nano/), [Mobile Phone Museum의 Razr 기록](https://www.mobilephonemuseum.com/phone-detail/razr-v3), [Sidekick 기록](https://www.mobilephonemuseum.com/phone-detail/danger-hiptop-sidekick), [Sony 회사 역사](https://www.sony.com/en/SonyInfo/CorporateInfo/History/sonyhistory-g.html)에 근거한다. 발표와 판매·지역별 일상 보급은 서로 다른 날짜다.

폰의 힌지·별도 화면·키패드 구조는 [Motorola 매뉴얼](https://en-us.support.motorola.com/euf/assets/downloads/Manuals/V3_06_UG.pdf), 프리쿠라와 폰 장식의 구조는 [Web Japan의 2011 자료](https://web-japan.org/trends/11_about/pdf/trends11_01_pop.pdf)를 참고했다. 매뉴얼의 저작권 연도를 제품 출시 연도로 쓰지 않았다. 자세한 시간 규칙은 [era-compatibility.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/y2k-style-20260927/era-compatibility.json)에 저장했다.

현대 Y2K 혼합을 명시한 요청에는 이런 고증 제외 규칙을 기계적으로 적용하지 않는다. 원형 재현인지 현대 재해석인지 먼저 정하고, 연도가 없으면 특정 모델의 정확한 연대를 임의로 선언하지 않는다.

## 6. 촬영 과정과 스타일을 분리

직광 플래시는 빛의 배치와 표면 반응이다. Y2K·갸루·McBling·인디 슬리즈의 의복 자체가 아니다. 부드러운 창문광을 요청해도 해당 착장의 구조는 유지할 수 있어야 한다. 날짜 스탬프, 노이즈, 저해상도, 어두운 배경을 플래시의 필수 결과로 추가하지 않는다.

‘그 시기에 실제로 촬영된 원본’, ‘오래 보관되어 열화된 자료’, ‘현대 카메라로 만든 레트로 재현’은 다른 원인이다. 후면 LCD가 있는 카메라 소품을 화면에 넣었다고 그 장면이 그 카메라로 촬영되었다는 결론도 나오지 않는다. 소품 구조와 촬영 장치·조명·출력은 별도 데이터로 유지한다.

## 7. 후보 묶음 20개와 채택 계약

| 묶음 | 함께 읽을 구성요소 | 우선 확인 범위 |
|---|---|---|
| Pop denim | baby tee, 낮은 허리, bootcut, 나비핀, 플랫폼 | 허리·밑단·머리 장식의 복수 규모 |
| Spiky hair | 번, zigzag part, 앞가닥 | 머리 앞·위·옆 |
| Millennium surface | 메탈릭 직물, 투명층, shield, 회로 프린트 | 각 표면과 렌즈 |
| Cyber club | 메시 상의, 메시, 비닐, wraparound, 바코드 도안 | 구멍·고체 표면·렌즈 곡률 |
| Velour set | 후디, 팬츠, 파일, 스톤 벨트, trucker | 원단·장식·별도 의복 경계 |
| Bling detail | 왕관 도안, 스톤, 장식 가방, gloss | 평면 도안과 입체 반짝임 |
| Sport panels | 트랙 재킷, 낮은 카고, visor, 띠 | 패널과 부착 주머니 |
| Hiphop volume | 저지, 숫자, 넓은 팬츠, 목걸이 층 | 프린트 소유 대상과 품 |
| Skate volume | 큰 티셔츠, 넓은 팬츠, 낮은 신발, 격자 | 밑단과 신발 |
| Mallgoth hardware | 메시, 아일렛, 플랫폼 부츠, 도안 | 구멍 조직과 금속 테두리 |
| Rave trim | 메시, 반사 트림, 털 부츠 | 원단과 광원 반응 |
| Boho layers | 셔링 상의, 층진 치마, 가는 스카프, 넓은 벨트, bolero | 여러 의복 경계 |
| Gyaru detail | 데님 미니, 플랫폼, 루즈삭스, 큰 링 | 독립된 양말과 신발 구조 |
| Frost lip | 라일락 서리광, 갈색 외곽, 밝은 중심, gloss | 눈과 입술의 세부 |
| Nail macro | 사각 자유단, 프렌치 끝, 입체 별 | 손톱 확대 |
| Early devices | 첫 iPod, 접이식 폰, 유선 이어폰 | 기기 구조와 케이블; 2001년 말 이후 |
| Mid devices | 첫 nano, Razr, 카메라, 폰 참 | 별도 기기·부착; 2005년 이후 |
| Revival layers | 얇은 층, 메시, 비대칭, 카고 | 현대 의복 경계 |
| Ballet neighbor | 겹친 니트, 리본, 플랫, 다리 토시 | 현대 인접 계열의 구조 |
| Palette roles | 유색 후디, 파일, 스톤 | 원단 색과 장식 광택 |

이 표는 해당 스타일의 보편적인 필수 체크리스트가 아니다. 서로 맞는 요소를 하나의 장면에서 읽어볼 수 있도록 만든 **선택적 예시 묶음**이다. 한 묶음에 최대 5개 후보가 있으며, 현재 계약의 멤버 상한 8개 안에 있다. 한번에 노출할 묶음 상한도 8개이므로 제안 20개가 모두 항상 사용자 후보팩에 보이는 것은 아니다.

현재 `photo_candidate_semantics.py`의 확장 키 검사, 후보 검사, 묶음 컴파일러와 프로필 참조 검사를 통과했다. 각 묶음은 존재하는 슬롯·ID로 연결되고 `profile_activation = independent_request_evidence_only`를 유지한다. 새 하드 프로필을 연결하거나 활성화하지 않았다.

추가 합성 계약 입력에서는 차원을 모두 열고 노출 조건을 맞췄을 때 소유권이 있는 18개 묶음이 포함됐고, 빈 차원의 기기 묶음 2개는 일반 경로에서 제외됐다. 모든 차원을 잠그면 제안 묶음이 모두 제외됐으며 기본 노출 상한 8개도 유지됐다. 이는 직접 만든 계약 입력을 사용한 검사이며 실제 생성기 팩의 노출 검증을 대신하지 않는다.

일반 후보 노출 경로에서는 멤버가 모두 실제 팩에 보이고, 적합성이 통과하고, 관련 차원이 열려 있으며 충돌이 없어야 한다. 합동 채택 경로도 별도로 검증해야 한다. 검색·임베딩 적중이나 후보 선택이 `spiky bun`, 낮은 허리 같은 하드 의무를 자동 발생시켜서는 안 된다.

특히 **`prop` 차원의 소유권은 현재 정책에서 빈 배열**이다. 새 소품 18개와 기기 묶음 2개는 문맥별 소유권 연결이 필요하다. 들고 쓰는 기기, 책상 위 배열, 옷에 붙인 참을 모두 임의의 `setting`으로 정하면 사용자의 고정 의미를 침범할 수 있다. 필요한 역할을 먼저 선언한 뒤 실제 채택 경로를 확인해야 한다.

출처·연도·문화 분류·미확인 주장·검증 상태는 유지보수 자료에만 두었다. [runtime-extension.proposed.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/y2k-style-20260927/runtime-extension.proposed.json)에는 관찰 가능한 긍정 언어와 기존 계약 필드만 투영했다. 이 파일은 **등록되지 않은 제안**이며 바로 복사하면 모든 문맥에서 정상 노출되는 완성 패키지가 아니다.

## 8. 검증 설계와 합격 기준

[qualification-plan.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/y2k-style-20260927/qualification-plan.json)에 텍스트 계약 사례 48개와 비교 렌더 설계 12개를 고정했다. 아직 실행하지 않았다. 렌즈 수×곡률 사례는 네 가지 조합이 필요하므로 모든 설계를 단순히 ‘24회 이미지 생성’으로 계산하지 않는다.

| 검증 축 | 대표 비교 | 필요한 판정 |
|---|---|---|
| 머리 구조 | spiky / messy, zigzag part / crimp | 번·끝가닥·두피 경로·길이 질감 구별 |
| 의복 경계 | low-rise bootcut / 높은 허리와 큰 flare | 상의·허리·무릎·밑단 소유 대상 |
| 소재 | 짧은 파일 / 루프, 스톤 / 디스크 | 충분한 확대와 구조적 차이 |
| 안경 | 렌즈 1개·2개 × 평면·감싸는 곡률 | 정면과 옆면 관찰 |
| 소유 대상 | 나비핀 / 나비 프린트, 네일 별 / 다른 장식 별 | 같은 모티프의 다른 위치는 대체 불가 |
| 색의 원인 | 핑크 원단 중성광 / 흰 원단 핑크광 | 조명과 고유 표면색 분리 |
| 촬영 과정 | 같은 착장의 직광 / 창문광 | 착장 유지, 조명 변화만 읽기 |
| 연대 | 1999 / 2001 말 / 2005의 특정 기기 | 출처 기반 시간 계약; 픽셀로 출시일 추론하지 않음 |
| 고정 의미 | 헤어·상의 고정, 조명만 개방 | 외형 변경 묶음의 노출·채택 차단 |
| 검색과 의무 | 목록에 spiky 후보만 존재 | 선택·검색을 하드 활성화 근거로 사용하지 않음 |

실제 평가에서는 요청 의미·연대 모드·고정 차원·게이트를 후보 노출 전에 고정한다. 비교군마다 동일한 인물 설명·카메라·광원·구도를 유지하고, 비교할 차이만 바꾼다. 구현 전후의 효과를 말하려면 현재 소스를 기준선으로 동결한 뒤 같은 평가 모집단을 사용해야 한다.

각 평가군은 한 번 생성하고 재시도·다른 군의 프롬프트·결과를 사용하지 않는다. 원본 후보팩, 선택 ID, 최종 문장 증거, 실제 런타임 프롬프트, 이미지 해시, 모델 설정, moderation 상태와 판정 근거를 남긴다. 소유 대상·형태·혼동 경계가 모두 맞아야 해당 요소가 통과한다. 일부 성공은 성공으로 계산하지 않는 `partial_is_fail`을 적용한다.

가려짐·화면 밖·부족한 크기·차단된 생성은 이유와 함께 `unscored`로 기록한다. 이는 통과도 시각적 0점도 아니다. 요구된 촬영 범위 자체를 구현하지 못했다면 별도의 프레이밍 계약 실패를 기록한다. 프롬프트 감사, 실제 런타임 감사, 픽셀, 사용자 판단을 서로 대신할 수 없다.

## 9. 보강의 우선순위

| 우선순위 | 작업 | 이유와 완료 증거 |
|---|---|---|
| P0 | 시대 모드, 모델·세대 구분, 광택·무늬·소유 대상 경계 | 분류 오류가 여러 후보로 퍼지는 것을 차단. 부정문·연도·소유 대상 계약 사례 통과 필요. |
| P0 | spiky bun, zigzag, crop/waist/bootcut, velour/terry, shield/wraparound, lip regions | 참조 키워드의 형태를 실제로 구별. 최소 비교 렌더의 모든 게이트 필요. |
| P1 | 20개 묶음의 문맥별 노출, 차원 고정, 멤버 동시 채택 | 등록 성공이 실질 노출로 이어지는지 확인. 실제 팩과 선택 로그 필요. |
| P1 | 소품 18개의 역할·차원 소유권 | 빈 차원 상태로 임의 채택되지 않게 하기. 기기·케이블·참 부착 관계와 채택 경로 필요. |
| P1 | 소재 기술 원문, 신발·가방·모자·네일 확대 자료 | 연구자 정의의 더 정교한 형태 확인. 이미지별 구조와 불확실성 주석 필요. |
| P2 | 지역·시기별 힙합·스케이트·갸루·Nu-metal·Emo·Scene 당대 자료 | 하나의 서구 팝스타 이미지로 모든 계열을 대표하지 않기. 연도·장소가 확인되는 추가 자료 필요. |
| P2 | 피부색·체형·연령과 독립적인 동일 착장 평가 | 스타일이 인물 속성으로 대체되지 않는지 확인. 의복 게이트와 사용자 수용성 구분. |
| P3 | 더 많은 현대 재해석과 그래픽 변이 | P0/P1 형태·노출 기준이 먼저 충족된 뒤 다양성 확대. |

후속 구현 순서는 ① 제안 정의의 미확인 항목 검토, ② 소품 역할 연결, ③ 명시 요청의 형태 의무 설계, ④ 제한된 확장 등록, ⑤ 소스 해시에 맞춘 인덱스 생성, ⑥ 실제 노출·선택 검사, ⑦ 고정 비교 렌더와 픽셀 평가, ⑧ 사용자 판단이다. 이번 조사에서는 ①을 위한 문헌·형태 제안과 코드 계약 검사를 완료했고, 원문·지역 표본이 부족한 항목은 명시적으로 남겼다.

## 10. 파일 안내와 현재 상태

| 파일 | 내용 |
|---|---|
| [seed-keywords.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/y2k-style-20260927/seed-keywords.json) | 참조 대화의 308개 행과 출처 상태 |
| [sources.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/y2k-style-20260927/sources.json) | 37개 URL, 읽기 상태, 지지하는 주장과 한계 |
| [style-families.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/y2k-style-20260927/style-families.json) | 21개 계열, 시대·문맥·혼동 경계 |
| [components.tsv](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/y2k-style-20260927/components.tsv), [additional-components.tsv](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/y2k-style-20260927/additional-components.tsv) | 사람이 수정할 수 있는 구성요소 원문 |
| [semantic-components.proposed.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/y2k-style-20260927/semantic-components.proposed.json) | 수정·세분화 후 306개 정의, 소유 대상과 게이트 |
| [graphic-groups.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/y2k-style-20260927/graphic-groups.json) | 그래픽 13개 분류와 실제 도안 선택지 |
| [keyword-coverage.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/y2k-style-20260927/keyword-coverage.json) | 원래 308개 행과 새 정의·계열의 연결 |
| [candidate-bundle-designs.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/y2k-style-20260927/candidate-bundle-designs.json) | 20개 묶음과 관계·연대·보류 항목 |
| [runtime-extension.proposed.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/y2k-style-20260927/runtime-extension.proposed.json) | 기존 계약 형태로 투영한 등록 전 확장 |
| [era-compatibility.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/y2k-style-20260927/era-compatibility.json) | 모델별 시간 근거와 적용 한계 |
| [qualification-plan.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/y2k-style-20260927/qualification-plan.json) | 미실행 텍스트 48개·비교 렌더 설계 12개 |
| [current-data-gap-audit.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/y2k-style-20260927/current-data-gap-audit.json) | 실제 로더의 저작 데이터 34개 파일에 대한 좁은 조사 |
| [validation.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/y2k-style-20260927/validation.json), [maintenance.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/y2k-style-20260927/maintenance.json) | 코드 계약 검사 결과, 소스 해시, 주장 한계 |
| [build_proposals.py](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/y2k-style-20260927/build_proposals.py), [qualification_plan.py](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/y2k-style-20260927/qualification_plan.py) | 이 폴더의 제안·계획을 재생성하는 도구 |

재생성: 저장소 루트에서 `python3 docs/research-evidence/photo-prompt/y2k-style-20260927/build_proposals.py`와 `python3 docs/research-evidence/photo-prompt/y2k-style-20260927/qualification_plan.py`를 실행한다. 이 도구들은 연구 폴더에만 쓰며 생성기 등록·인덱스 생성·이미지 호출을 하지 않는다.

완료된 것은 자료 읽기, 키워드 분해, 혼동 경계·관계·연대 설계, 원래 목록의 연결, 제안 확장의 코드 계약 검사다. 데이터 채택과 실제 시각 개선의 측정은 다음 단계이며 아직 완료로 표시하지 않았다.

후속 요청으로 진행한 실제 런타임 반영과 독립 이미지 3장 시험은 [반영·이미지 검증 보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/y2k-style-20260927/implementation-and-render-test.ko.md)에 별도로 기록했다. 위 제안과 미실행 비교 설계는 조사 당시의 기록으로 유지한다.
