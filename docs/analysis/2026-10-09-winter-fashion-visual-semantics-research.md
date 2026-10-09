# 겨울 패션: 시각 의미·후보 데이터 강화 리서치와 반영 계획

2026-10-09 KST. 참조 대화: [겨울 패션 용어 조사](chatgpt-conversation://6ac7dd5d-c74c-83ec-9d21-4b1ee66066c9).

겨울 패션은 **의복의 구조, 원료 명세, 표면·무늬, 지역 핏, 피복·개구, 현재 여밈 상태, 층의 순서·가림, 스타일의 선택 조합**으로 나누어 보강하는 것이 효과적이다. 예를 들어 ‘캐시미어 오프숄더 니트 + 랩 코트’는 하나의 스타일 태그가 아니라 원료 명세, 니트 표면, 어깨 아래 목선, 코트 앞판 겹침, 두 옷의 가림 관계를 가진다. 이 분해는 아래 근거에 기초한 연구자의 데이터 설계 제안이다.

원문 **304개 용어 행**을 모두 대조했고, **46개 출처, 79개 상세 의미 카드, 162개 문장 초안, 56개 비교 사례, 12개 변경 반례, 16개 이미지 검증 묶음**을 작성했다. 문장 초안은 가시 변형 146개와 선택 조합 16개다. 원문 신체 부위별 색인 15행과 코디 예시 10행은 용어 수와 분리해 모두 매핑했다. 실제 신규 런타임 엔트리 수는 동등성 검토·중복 제거·효과 범위 검토 후 결정한다.

이번 요청의 완료 범위는 **상세 리서치와 반영 계획**이다. 실행 데이터·manifest·인덱스·스킬 절차는 수정하지 않았다. 후보 선택·실제 검색·이미지 생성도 실행하지 않았다.

## 1. 원문과 출처 확보

대화 API 본문은 20,000자에서 잘렸다. 로그인된 공식 ChatGPT 페이지에서 렌더된 본문 전체 25,053자와 표의 첫 열을 추가 확인했다. 본 분류 1~15절은 하위 표를 포함해 18개 표·304행이다. 16절의 15행은 목적 부위별 검색 색인, 17절의 10행은 코디 예시다. 한 행의 별칭을 별개 용어로 중복 집계하지 않았다.

- [원문 용어 목록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/winter-fashion-20261009/seed-terms.txt)
- [원문·기존 표현 대조 원장](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/winter-fashion-20261009/term-inventory.json)
- [부위 색인·코디 예시의 의미 매핑](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/winter-fashion-20261009/reference-supplement.json)
- [출처 원장](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/winter-fashion-20261009/sources.json)

구조·소재·제작 설명은 Cotton Incorporated, Woolmark, CCMI, Mohair South Africa, Patagonia, Rab, YKK, Gloverall, Wolford, Calzedonia와 실제 패턴·편직 제작자의 자료를 우선했다. 전통·의복사는 V&A·FIT의 자료로, 미감 라벨은 해당 시기의 Vogue 편집 자료와 설계자 인터뷰로 구분했다. FIT의 문헌 종합을 새로운 실험 결과로 표현하지 않는다.

자료마다 확인 범위가 다르다. Purl Soho 인타르시아 페이지의 직접 열기는 403이어서 검색 제공 본문을 사용했다. TOTEME 스카프 코트의 직접 열기는 지역 홈페이지로 이동했으므로 검색 제공 제품 본문만 해당 상품 구조의 근거다. UGG의 구체 도움말은 검색 본문과 지원센터 접근 결과를 구분했다. 이런 자료를 직접 페이지 전체 검증으로 계산하지 않았다.

**46개 출처가 304개 별칭의 모든 정의를 독립적으로 입증한다는 뜻은 아니다.** 용어별로 근거 가족, 선택한 상품의 범위, 추가 확인할 제작·속어·내부 구조를 남겼다. 후보 문장, 그래프, 우선순위와 검증 계획은 연구자의 제안이다. 원문 대화의 설명도 독립 출처와 같은 증거 수준으로 취급하지 않는다.

## 2. 현재 저장소에서 확인한 기준

2026-10-09 **03:38:38~03:39:31 KST**에 현 작업 트리의 공식 원본 로더로 데이터를 읽었다. HEAD는 `f081ac7305210def8348cc76d3a8f9f48393b4de`이며 기존 미커밋 데이터도 포함한다. 해당 로드 구간의 원본·manifest·관련 코드·인덱스 헤더 SHA-256은 전후 동일했다. 이 결과는 원본 로드 스냅샷이며 전체 인덱스 검사나 라이브 runtime dispatch의 증거가 아니다. [스냅샷과 해시](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/winter-fashion-20261009/source-snapshot.json).

| 단위 | 확인 수량 |
|---|---:|
| 슬롯 | 114 |
| 슬롯 후보 | 11,188 |
| 의미 검색 문서 | 11,224 |
| 컴파일된 시각 의미 프로필 | 2,977 |
| 컴파일된 후보 번들 | 1,347 |
| manifest 등록 원본 | 후보 67 / 시각 프로필 49 |

304개 용어의 한·영 표현 및 행 내 별칭을 현재 코드의 **긍정 검색 필드**와 대조했다. 후보에 표현이 있는 행은 157개, 프로필에 표현이 있는 행은 126개, 합집합은 157개다. **나머지 147개를 의미 누락으로 계산하지 않는다.** 다른 표현으로 같은 구조가 이미 존재할 수 있고, 반대로 단어가 있어도 다른 소유자·문맥일 수 있다. 임베딩 검색·후보 노출·활성화·선택·픽셀의 결과도 아니다.

이 구분은 실제 대조에서 중요했다. `layering`은 272개 후보의 긍정 필드에 있지만 지형·장신구·사진 층위까지 포함한다. `rib knit`의 별칭에는 건축 리브 문맥이, `fringe`에는 앞머리가, `dart`에는 시선 행동이 섞일 수 있다. 문맥 없는 연구 질의의 혼동 신호이며, 현재 런타임이 실제로 오동작했다는 판정은 아니다.

### 재사용·보강할 실제 원본

| 조사 항목 | 확인한 기존 ID·내용 | 반영 판단 |
|---|---|---|
| 케이블 니트 | `clt_ct008_v1/v2`, `clothing_ct008_v1` — 솟은 뜬 줄·교차 | 기존 의미 재사용 우선; 아란 문맥·인쇄 반례·실 연속성 보강 |
| 리브 니트 | `clt_ct087_v1`, `clothing_ct087_v1` — 능선·오목한 홈 | 골 폭·소유자·코듀로이 대비를 보강 |
| 작은 니트 루프 | `clt_ct087_v2` — 문장에 `a macro view` 포함 | 보통 원단 표면 의미와 구도 효과를 분리 검토; 고정 구도를 바꾸는 후보로 재사용하지 않음 |
| 코듀로이 | `clt_ct089_v1`, `sff_pro_t10` — 솟은 파일 웨일 | 리브와 별개 조직·표면으로 재사용 |
| 누빔 | `clt_ct097_v1`, `clothing_ct097_v1` — 스티치와 솟은 셀 | 배플 외관과 내부 충전 명세를 분리; 기존 엠보스 변형과 혼합하지 않음 |
| 시어·불투명 | `clt_ct079_v1/v2` — 겉층과 아래층 | 실제 피부 투과·불투명 이너·피부색 안층을 추가 구분 |
| 썸홀 | `thumbhole_cuff_hand_opening` — 전용 엄지 구멍 | 후보는 있으나 스냅샷에서 명시적 `concept_units`·`relations`·`affected_properties`는 없음; 관계·전체 효과 검토 |
| 가터 지지 | `pfe_garter_path_candidate`, `pfe_garter_path`, `clt_ct025_v1` | 벨트→끈→고정부→스타킹의 기존 경로 유지; 효과 선언·같은 착용자 결속 검토 |
| 스타킹·케이프·봉제 | `clt_ct107_v1`, `clt_ct011_v1`, `clt_ct031_v2`, `clt_ct064_v2` | 기존 끝단·어깨 지지·다트·스모킹의 지역 의미 재사용 |
| 기존 핏 | `photo_prompt_fashion_fit_extension.json`과 대응 프로필 | 몸 수정 없는 지역 접촉·허리 기준·연결선·여밈 상태의 의미를 재사용 |
| 겨울 특유 표현 | 배플·피셔맨 립·페어아일·인타르시아·포인텔·시어링·셰르파·스카프 코트·페이크 시어 등은 해당 표현의 긍정 필드 이웃 없음 | 기존 근접 구조와 동등성 비교 후 새 변형·문맥 보강을 결정 |

[기존 관련 레코드 발췌](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/winter-fashion-20261009/current-positive-records.json). 일부 레코드에서 필드가 없다는 사실만으로 무효라고 판정하지 않는다. 기존 계약과 선택 경로에서 어떻게 사용되는지 후속 구현 단계에 확인한다.

## 3. 연구에서 확정한 구분과 데이터 설계

### 3.1 원료와 눈에 보이는 표면은 서로 다른 값이다

캐시미어·카멜 헤어·양모는 원료이며, 모헤어는 앙고라산양의 섬유다. 원료를 가공한 의복의 표면은 실·혼방·조직·가공에 따라 달라진다. 카멜색을 낙타털로, 잔털을 모헤어로 판정하지 않는다. 원료를 요청에서 삭제하지 않고 명세로 보존하며, 선택된 잔털·파일·그레인·광택을 별도 시각 속성으로 작성한다. [CCMI 원료 설명](https://cashmere.org/facts.php), [Mohair South Africa](https://www.mohair.co.za/natural-fibre), [Woolmark](https://www.woolmark.com/fibre/).

시어링은 양면 재료의 전통 의미와 상품의 털룩 표현을 구분해야 한다. Patagonia의 Retro Pile은 `shearling fleece`라는 표현을 재생 폴리에스터 제품에 사용한다. 또 셰르파 상품 예에는 울 혼방도 있다. 따라서 셰르파를 무조건 순수 합성, 테디를 무조건 천연 양가죽으로 저장하는 것도 부정확하다. WF05~08은 파일과 바탕의 관계, 접힌 양면, 국소 트림을 다룬다. [Patagonia Retro Pile](https://www.patagonia.com/product/mens-retro-pile-fleece-jacket/22802.html), [혼방 셰르파 제품 예](https://wornwear.patagonia.com/products/mens-reversible-recycled-sherpa-jacket_20430_smdb).

### 3.2 니트의 코·입체 교차·색무늬·제작 방식·배치를 나눈다

리브는 솟은 뜬 웨일과 홈의 반복이고 코듀로이 골은 파일 웨일이다. 케이블은 같은 뜬 줄이 교차하는 입체 구조다. 평면에 그린 줄이나 밧줄 그림으로 대체하지 않는다. 부클레의 고리 효과사, 작은 니트 루프, 성긴 오픈워크의 빈 공간, 잔털 헤일로도 다른 축이다. [CottonWorks 니트](https://cottonworks.com/learning-hub/knitting/single-and-double-knits/), [파일·코듀로이](https://cottonworks.com/learning-hub/weaving/complex-woven-fabric-designs/), [부클레](https://cottonworks.com/encyclopedia-item/boucle/).

페어아일은 전통과 작은 가로 띠 색무늬의 문맥, 노르딕은 넓은 상업 모티프군, 요크는 목·어깨 구역의 배치다. 아란도 모든 케이블과 완전한 동의어가 아니다. V&A는 오늘날의 전형적인 아란 케이블 스웨터를 20세기의 발전으로 설명하므로 고대 상징·가문 식별 같은 전설을 자동 의미로 추가하지 않는다. [V&A 니트 전통](https://www.vam.ac.uk/articles/british-knitting-traditions).

인타르시아는 큰 색면마다 별도 실을 쓰는 방식, 스트랜디드는 뒤쪽으로 실을 운반하는 방식이다. 자카드에도 다양한 구조가 있다. 정면의 큰 그림·반복 모티프만으로 내부 공정이나 뒷면 플로트를 PASS할 수 없다. 앞의 코에 맞는 색면과 실제 드러난 뒤 실 경로를 서로 다른 변형·증거로 다룬다. [Purl Soho 인타르시아](https://www.purlsoho.com/create/intarsia/), [Brooklyn Tweed 스트랜디드](https://brooklyntweed.com/pages/stranded-colorwork-101).

포인텔은 작은 규칙적 오픈워크와 연결 바탕을 검사한다. 실제 제품도 서로 다른 구멍 모티프를 사용하므로 하트 모양을 보편 기본값으로 넣지 않는다. 구멍 아래가 불투명 이너라면 그 색과 경계를 보존한다. 크로셰라는 공정, 성긴 외관, 맨살 비침을 하나로 합치지 않는다. [UNIQLO 포인텔 변형](https://www.uniqlo.com/sg/en/products/E487121-000/00).

### 3.3 헤링본은 단순 V자보다 정밀한 경계가 필요하다

원문의 ‘물고기 뼈처럼 V자’ 설명은 접근 표현으로 유지하되, 헤링본의 방향 전환에서는 사선이 끊기고 어긋나는 특징을 보강한다. 점으로 이어지는 셰브론과 구분한다. 하운드투스도 직조·편직·프린트로 표현할 수 있으므로 무늬 이름만으로 원료·공정을 확정하지 않는다. WF09와 WR09가 이 경계를 다룬다. [CottonWorks 헤링본·셰브론](https://cottonworks.com/learning-hub/weaving/basic-woven-fabric-designs/).

### 3.4 충전·배플·누빔·기능 성능은 독립이다

푸퍼는 부푼 외관 범주이며 다운과 합성 충전재 모두 가능하다. 필파워는 일정 질량 다운의 부피 지표, 충전량은 별도 질량이다. 방풍·발수·방수는 구조·성능 명세다. 사진에는 눌린 스티치 선과 그 사이 솟은 구획을 저장할 수 있지만 내부 박스월·800FP·보온 온도·방수 인증을 겉 외관에서 역추정하지 않는다. [REI 충전 외투](https://www.rei.com/learn/expert-advice/insulated-outerwear.html), [필파워](https://www.rei.com/learn/expert-advice/what-is-down-fill-power.html), [Rab 구성 설명](https://rab.equipment/eu/rab-lab/down-jackets-buying-guide).

‘퀼팅 프린트’, 실제 얕은 누빔, 부푼 배플 외관은 각각 다른 후보와 반례를 갖는다. 컷어웨이 제품 이미지가 있어야 할 명세는 보통 인물사진의 필수 픽셀 게이트로 만들지 않는다.

### 3.5 옷 이름보다 여밈의 양 끝점과 현재 상태가 중요하다

더플의 토글은 맞은편 고리를 실제로 통과해야 한다. 더블브레스트는 단추 두 줄만이 아니라 앞판의 겹침 관계가 필요하다. 랩 코트의 앞판, 허리 벨트, 그 아래 니트는 각각 소유자를 유지한다. 스카프 코트도 코트에 붙은 패널, 탈착형, 별개 목도리를 구분한다. 특정 브랜드 상품의 자수·색·기장을 모든 변형에 전파하지 않는다. [Gloverall 구조 비교](https://www.gloverall.com/blogs/journal/duffle-coat-vs-peacoat), [TOTEME 부착형 상품 예](https://toteme.com/products/embroidered-scarf-coat-black).

투웨이 지퍼는 두 슬라이더의 방향과 분리형·닫힌형이 다르다. ‘두 슬라이더 보유’와 ‘아래 슬라이더 아래만 열림’은 별개다. 후자는 닫힌 위 치형, 슬라이더, 벌어진 아래 패널을 같은 지퍼 경로에서 검사한다. 그 아래에 이너가 있으면 개방이 곧 맨살 노출은 아니다. [YKK 유형 설명](https://ykkamericas.com/what-kind-of-two-way-zipper-do-i-need/).

### 3.6 밀착·목선·개구·실제 피복을 독립 처리한다

접힌 터틀·낮은 모크·퍼널·처진 카울은 칼라 형태다. square·boat·sweetheart는 목선 경계이고, fitted·bodycon은 직물의 지역 접촉이다. 오프숄더·콜드숄더·원숄더·홀터·스트랩리스는 지지·어깨 피복 구조를 구분한다. 높은 목과 열린 등은 양립할 수 있으며, 오프숄더가 겨드랑이 노출을 보장하지 않는다. [Tilly Freya 변형](https://tillyandthebuttons.com/blogs/sewing/stretch-freya-sweater-dress), [Seamwork 퍼널넥](https://www.seamwork.com/sewing-patterns/all-about-the-ace-top), [Mood 목선 구조](https://blog.moodfabrics.com/all-about-necklines/).

원문의 성인 노출 관련 용어도 전부 보존했다. `sideboob`, `underboob`는 가시 상태이고 `underbust corset`는 별개 의복의 범위다. 크롭은 상의 길이이며 배꼽 노출은 상의 밑단·하의 허리단·이너·겉옷·배꼽 기준점 사이의 실제 관계다. 구멍이 있어도 그 아래 이너가 있으면 맨살과 다르다. WF47~52에는 자동 활성화 방지와 직접 용어 출처의 추가 확인 조건을 남겼다. [코르셋의 구조 근거](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear), [목선·피복 근거](https://blog.moodfabrics.com/all-about-necklines/).

### 3.7 타이츠·스타킹·부츠 구간의 실제 앞표면을 판정한다

타이츠·팬티호즈의 지역 용어 중첩은 유지한다. 독립 스타킹과 허리 연속형, 자체 고정 밴드와 가터 지지끈, 양말과 레그워머는 다른 구조다. 가터는 벨트→끈→고정부→같은 스타킹 상단의 전체 경로가 필요하다. 실리콘·안기모가 숨으면 그 부분은 명세이며 가시 검증 대상이 아니다.

데니어는 선밀도이므로 ‘20D=항상 이 투명도’, ‘100D=이 보온성’ 같은 보편 규칙으로 쓰지 않는다. Calzedonia의 페이크 시어 제품은 피부색 보온 안층과 시어 겉층을 명시한다. 피부색이 비쳐 보이는 인상과 실제 피부 투과를 구분해야 한다. 일반 착용샷에서는 내부 층·기모가 안 보일 수 있으며, 그 경우 제품 단면·접힌 단의 진단 증거와 원문 착장 증거를 구분한다. [CottonWorks 데니어](https://cottonworks.com/encyclopedia-item/denier/), [Wolford 타이츠 구분](https://www.wolford.com/en-ca/our-tights-guide.html), [Calzedonia 이중층 예](https://www.calzedonia.com/us/product/sheer_thermal_tights-MODC1919.html).

미니 밑단과 사이하이 부츠 윗단 사이의 구간은 그 자체로 맨살이 아니다. 불투명 타이츠가 있으면 앞표면은 타이츠다. 부츠통 높이도 같은 착용자의 무릎·허벅지를 기준으로 판단하며, 구도를 바꾸거나 다리를 늘려 실현하지 않는다. 플랫폼은 앞발 밑창도 두꺼워야 하며 높은 뒤꿈치만으로 판정하지 않는다. 러그솔과 패션 부츠 외관은 눈길 접지·방수 시험의 대체 증거가 아니다. [Charles & Keith 부츠 구조](https://www.charleskeith.in/in/guides/types-of-boots.html).

### 3.8 겨울 액세서리에는 피복 공간과 연결 관계가 있다

발라클라바의 머리·목 연속 덮개와 얼굴 개구, 후드 스카프의 연결된 머리 부분과 자유 끝, 귀마개의 두 패드와 밴드, 미튼의 엄지·공용 손가락 공간, 머프의 양손이 들어가는 공용 통을 구분한다. 스누드는 역사적 머리망·현대 목통 등 다의어를 문맥으로 해결한다. 썸홀은 장갑이 아니라 해당 소매 커프에 난 구멍이다. [BUFF 통형 넥웨어](https://www.buff.com/blog/en/neck-head-clothing-accessories/what-is-neck-gaiter/), [FIT 머프](https://fashionhistory.fitnyc.edu/muff/), [Purl Soho 손 액세서리 편직](https://www.purlsoho.com/create/working-into-the-stitch-below/).

코르셋 벨트·패션 하네스·아일릿·체인·프린지는 의복 위의 별개 경계와 부착점을 갖는다. 패션의 펑크·바이커·밀리터리·페티시 문맥을 삭제하지 않으면서, 그 이름만으로 강제·범죄·상해·성행동을 새로 추가하지 않는다. [V&A Westwood 소장 복식](https://www.vam.ac.uk/articles/vivienne-westwood-punk-new-romantic-and-beyond).

### 3.9 스타일명은 선택형 조합이며 정체성이나 성능 증거가 아니다

22개 미감 라벨은 구체 부품을 찾는 문맥으로 유지한다. Y2K·McBling의 하위 의미는 기존 데이터를 우선 재사용한다. 발레코어·코케트·고딕·고프코어를 하나의 고정 의상으로 만들지 않는다. 몹 와이프라는 이름도 실제 범죄·혼인·민족·천연 모피를 뜻하지 않는다. 당시 편집 자료의 날짜는 유지하고 현재 유행 순위로 읽지 않는다. [Vogue의 2023 미감 문맥](https://www.vogue.com/article/core-aesthetic-microtrends-2023), [2024 몹 와이프 문맥](https://www.vogue.com/article/the-mob-wife-look-is-trending-is-it-sustainable), [고프코어 용어](https://www.vogue.com/article/the-vogue-business-glossary).

아프레 스키는 스포츠 장비 없는 실내 착장도 가능하다. 테크웨어풍의 포켓·조절·스트랩은 기능의 설계 단서이지 방수 인증·검정색·무기·SF 장면의 의무가 아니다. 발레코어도 연습복에서 영향을 받은 층을 제안하는 것이며 발레 기술·나이·직업·특정 동작을 추가하지 않는다. [아프레 스키 편집 예](https://www.vogue.com/article/apres-ski-style), [설계자 인터뷰](https://www.gq.com/story/stealth-in-the-city-nike-taps-erollson-hugh-of-acronym-for-acg-re-launch), [Capezio 레이어 구조](https://www.capezio.com/pages/shop-balletcore-outfit-ideas).

## 4. 원문 분류별 보강 지도

아래는 반영 설계이며 현재 실행 데이터 등록 완료를 뜻하지 않는다. 모든 용어 행의 처리 경로와 기존 이웃은 [304행 반영 대조표](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/winter-fashion-20261009/term-plan.csv)에 있다.

| 원문 분류 | 행 수 | 주된 보강 | 카드 |
|---|---:|---|---|
| 1 기본·보온 | 12 | 층의 순서·기능 명세·충전·구획 | WF01~04 |
| 2-1 동물성·털 | 12 | 원료·털 외관·양면·트림 분리 | WF05~08 |
| 2-2 원단·가공 | 20 | 실·패턴·파일·기모·누빔 | WF03~14 |
| 3 니트 조직·무늬 | 18 | 코 크기·교차·색면·뒷면·배치·개구 | WF15~22 |
| 4-1 코트 구조 | 16 | 길이·겹침·토글·벨트·팔 틈·스카프 접합 | WF23~30 |
| 4-2 겨울 아우터 | 18 | 부푼 외곽·뒤 트임·라이너·민소매·마감 | WF07, 31~35 |
| 5 니트·상의 | 16 | 앞 개방·랩·세트·덧층·몸통 연결 | WF36~39 |
| 6 네크라인 | 21 | 목선 경계·칼라 접힘·어깨 지지·망사 | WF40~43 |
| 7 핏·구조 | 18 | 지역 접촉·컵·보닝 외관·솔기·모음 | WF44~46 |
| 8 절개·가시 상태 | 20 | 길이와 실제 피복·부위 개구·현재 여밈·아래층 | WF43, 47~52 |
| 9-1 드레스 | 10 | 구조·표면·핏·목선의 독립 조합 | WF53 및 연결 카드 |
| 9-2 스커트 | 15 | 몸 기준 길이·폭·접힘·트임·랩·숨은 반바지 | WF54~55 |
| 10 바지·쇼츠 | 14 | 지역 폭·허리단·발밑 고리·일체 연결 | WF05, 47, 56~57 |
| 11 레그웨어 | 18 | 투과·이중층·그물·뒤선·지지·끝단·발 피복 | WF58~62 |
| 12 부츠 | 16 | 같은 다리의 높이·갑피 부품·앞발 밑창·접힘 | WF07, 63~65 |
| 13 액세서리 | 20 | 목·어깨·머리·귀·손의 공간과 부착 경로 | WF66~69 |
| 14 세부 구조·장식 | 18 | 소매·썸홀·토글·끈·고리·판·프린지 | WF08, 25, 70~71 |
| 15 스타일·미감 | 22 | 날짜·하위 문맥·선택형 구성·금지된 자동 추론 | WF72~77 |
| 용어 합계 | **304** | 모든 행에 반영 경로 있음 | 상세 CSV 참고 |
| 16 부위 검색 색인 | 15 | 목적 구역의 경계·실제 앞표면 질의 | WF78 및 관련 카드 |
| 17 코디 예시 | 10 | 복수 의복·소유·가림과 원문 의도 보존 | WF79 및 관련 카드 |

대표 처리 분류는 가시 형태·상태 250행, 성능 명세 7행, 원료+선택 표면 13행, 가시 결과·숨은 구조 분리 10행, 명시 성인 상태 2행, 미감 문맥 22행이다. 이는 각 행의 우선 경로이며 자연적인 상호 배타 분류는 아니다. 한 용어의 제작·외관·제품 변형을 후속 구현 때 더 나눈다.

## 5. 데이터에 넣을 구조

시각 의미 검색과 슬롯 후보 검색의 표면을 유지하면서 `뜻 → 관찰 가능한 구성 → 소유자·관계 → 선택 변형 → 전체 효과 범위 → 관찰 조건`을 연결한다. 단어와 별칭을 모든 후보에 복제하는 방식은 피한다.

| 층 | 저장할 내용 | 이번 산출물 |
|---|---|---|
| 정의·혼동 | 원료·표면·구조·상태·문맥을 구분하는 뜻 | 의미 카드 79개 |
| 구성·관계 | 양 끝점·같은 옷·같은 착용자·다른 층 | 관계 예 79개와 카드별 관찰 조건 |
| 선택 후보 | 하나의 관찰 가능한 변형을 말하는 영어 문장 | 가시 변형 초안 146개 |
| 선택 조합 | 이미 선언된 옷·부품 사이 관계 | 조합 문장 16개와 원문 코디 10개 |
| 효과 범위 | 문장의 모든 소재·핏·구조·피복·구도 효과 | 카드별 속성 풀 및 변형별 범위 확정 조건 |
| 근거 | 직접 사실·상품 예·편집 문맥·추가 확인 조건 | 46개 출처와 304행별 가족 연결 |
| 검증 | 검색·노출·선택·구성·가시성의 별도 증거 | 비교 56개·변경 반례 12개·픽셀 묶음 16개 |

[상세 카드](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/winter-fashion-20261009/semantic-cards.md), [구조화한 카드](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/winter-fashion-20261009/semantic-cards.json), [후보 초안](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/winter-fashion-20261009/candidate-proposals.json).

### 초안을 런타임 레코드로 승격하는 조건

현재 초안의 관계 노드는 설계용 이름이고 카드의 속성 풀은 여러 대안의 합집합이다. **그대로 원본에 복사할 수 없다.** 각 문장에 맞는 실제 의복·끝점·단일 관계와 전체 효과를 확정해야 한다. 이미지에서 안 보이는 내부 사실은 하드 가시 의무로 만들지 않는다.

예를 들어 WF21 첫 후보는 `small repeating eyelets open through the declared knitted ground and reveal the declared opaque inner layer`다.

- 구성: 해당 니트 바탕, 바탕에 있는 작은 구멍의 둘레, 별개 불투명 이너.
- 관계: 구멍 테두리가 해당 니트의 개구를 둘러싸고, 그 개구 아래 별개 이너가 보인다.
- 효과: 니트의 지역 오픈워크, 두 층의 가시 관계, 아래층 피복 보존. 이 효과들을 현재 스키마의 `affected_dimensions`와 `affected_properties`에 모두 선언한다.
- 선택 조건: 니트·이너가 이미 선언되고 관련 속성이 열려 있으며, 요청이 실제로 이 변형을 지지한다.
- 픽셀 조건: 구멍·연속 바탕·불투명 이너가 모두 같은 소유 관계에서 읽힌다. 구멍만 있거나 이너가 지워진 경우 통과하지 않는다.
- 추가하지 않는 값: 원료 진위, 맨살, 체형, 색, 새로운 촬영 배율·구도·조명.

WF25 토글도 토글·맞은편 고리·양 앵커의 연결이 전부 필요하다. WF59 페이크 시어는 겉면 색 인상과 실제 두 층의 노출을 별도 변형으로 다룬다. 서로 다른 변형의 구성 요소를 모두 합쳐 한 프로필의 필수 목록으로 만들면 안 된다.

현재 관계 스키마는 `id/type/subject/object`, 효과 스키마는 `dimension/target/property`를 사용한다. 기존 핏 데이터는 `appearance`뿐 아니라 소재 거동에 `material`도 선언하는 경우가 있다. 표면·투과·드레이프 문장의 모든 차원을 확인해야 한다. 연구용 `predicate`를 원본 `type`으로 이름만 바꿔 넣거나 상징 노드를 실행 ID로 쓰지 않는다.

부분 효과를 담을 프로필은 현 `authored_components` 계약을 따른다. 단일 의무는 v1, 여러 구성 요소가 묶여 함께 증명되어야 하는 경우는 v2의 의무·증거 묶음을 사용한다. `component_semantics`, `render_gates` 등 컴파일 산출 필드는 원본 프로필에 직접 작성하지 않는다. [현재 유지보수 계약](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/references/maintenance.md).

## 6. 반영 우선순위와 파일 계획

카드 우선순위는 P0 53개, P1 26개다. P0는 관계 오인·소유 전파·피복 삭제·숨은 성능 추론이 요청을 바꾸는 항목을 우선한다. 이는 최종 신규 레코드 수나 한 번에 전부 구현할 분량은 아니다.

| 패키지 | 먼저 반영할 것 | 주 대상 원본 |
|---|---|---|
| WP1 표면·조직 | 리브/코듀로이, 케이블, 포인텔+이너, 페어아일/요크, 시어링/셰르파, 배플, 페이크 시어 | `photo_prompt_textile_surface_extension.json` 및 대응 visual obligations |
| WP2 의복·핏 | 코트 앞판·토글·벨트·스카프 접합, 목선·암홀·등판, 현재 지퍼 상태, 소매·썸홀 | clothing structure, fashion fit, portrait fashion exposure의 기존 원본·프로필 |
| WP3 액세서리·장식 | 스타킹 지지·부츠 높이·플랫폼, 발라클라바·귀마개·미튼·머프, 별개 스트랩·트림 | accessory structure, ornament structure의 기존 원본·프로필 |
| WP4 미감 | 22개 라벨의 하위 문맥과 선택 요소 연결 | subculture appearance, Y2K, sensual/fetish fashion의 기존 의미 재사용 |
| WP5 복수 의복 | 원문 부위 색인·코디의 앞표면·가림·같은 착용자 관계 | 기존 번들·관계 우선; 독립 겨울 관계가 남을 때만 새 winter extension/profile 검토 |

새 겨울 파일을 먼저 만들어 기존 의복 304개를 복제하지 않는다. 기존 원본의 중립 의복 의미와 성인·하위문화 프로필의 범위를 유지하고 실제 동등성으로 결정한다. 추가 파일이 필요하면 등록은 오직 `photo_prompt_source_manifest.json`에서 한다. 다른 filename 목록이나 스킬 설명에 용어 사전을 복제하지 않는다.

추가 자료가 필요한 항목은 정확한 앙고라토끼 원료의 직접 근거, 돌먼·배트윙 및 특정 코트의 패턴 도해, sideboob/underboob 직접 용어 근거, 숨은 홀드업 실리콘·스코트·보디수트 연결, 제품별 역사·상업 변형이다. 연구 데이터에서는 유지하되 이 확인 없이 보편 하드 의무로 승격하지 않는다.

## 7. 단계별 실행 계획과 완료 기준

목표는 용어 수가 아니라 **정확한 의복·지역 형태·관계가 검색과 구성에서 유지되고, 해당 증거 수준에 맞게 검증되는 것**이다. [실행 계획 JSON](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/winter-fashion-20261009/implementation-plan.json)에 패키지·의존성·완료 조건·파일·검증 대상을 기록했다.

1. **현 원본 재확인·동등성 판정.** 구현 시점의 HEAD·dirty 상태·관련 해시를 다시 읽고 적합한 격리 작업 공간을 사용한다. 304행을 재사용, 뜻이 같은 표현 보강, 좁은 successor, 새 변형, 명세, 출처 추가 확인으로 결정한다. 단어 유사성·표현 부재를 결정 근거로 쓰지 않는다.
2. **변형별 원본 작성.** 의복 소유·모든 관계 끝점·전체 효과를 확정한다. 임의의 신체·카메라·날씨·다른 의복 효과를 제거하고, 실제 의미 변화는 기존 ID·역사적 fixture를 통째 덮어쓰지 않는 successor로 다룬다. 성인 활성화 범위도 보존한다.
3. **인덱스·원본 검증.** 신규 파일만 manifest에 등록하고 semantic/BM25F·visual-profile 인덱스를 정규 빌더로 재생성한다. 벡터는 text/provider/model/dimensions가 모두 같을 때만 재사용한다. 새 의미 텍스트의 임베딩 비용·호출 수는 별도 집계한다. 연구 단계의 0회 호출을 구현 단계에 그대로 약속하지 않는다.
4. **검색·선택·구성 회귀.** 실제 한국어·영어 문맥 질의로 의미 검색을 확인한 뒤 슬롯 후보 노출, 명시적 선택, 구성된 문장과 잠금·소유자 보존을 별도로 확인한다. 부위 색인 15개·원문 코디 10개·비교 56개·변경 반례 12개를 사용한다.
5. **별도 생성 단계의 가시 검증.** 필요한 16개 묶음에서 어려운 변형을 선택하고 독립적으로 봉인한 표본을 확보한다. 기본 요청·핵심 제약이 같은 비교만 비교 실험으로 해석한다. 전체 활성화 게이트가 해당 소유자에 보여야 통과한다.
6. **검토 가능한 전달.** 채택·재사용·보류 용어와 변경 파일, 검색·구성·픽셀 증거를 연결한다. 배포·push가 별도로 요청되면 그 상태와 ref·runtime receipt를 추가 검증한다. 일부 변형만 렌더한 상태에서 전체 연구 데이터를 픽셀 합격으로 보고하지 않는다.

인덱스·원본 빌더는 검증·출판 후크를 가질 수 있다. 후속 구현에서는 현 source update·runtime publication 계약에 맞춰 실행하고 검증 완료 전 `CURRENT.json`을 수동 교체하지 않는다. 과거 generation·receipt·fixture는 보존한다. 이번 연구에서는 해당 빌더를 실행하지 않았다.

## 8. 검색·구성·이미지 검증 계획

[상세 회귀 계획](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/winter-fashion-20261009/regression-plan.json)의 모든 비교·반례·픽셀 묶음은 **계획 상태**다.

| 검증층 | 주요 사례 | 완료 조건 |
|---|---|---|
| 뜻·문맥 | 카멜 원료/색, 리브/건축, 프린지/앞머리, underbust/underboob, 머프/귀마개 | 긍정 정의와 대상 문맥을 찾고 반대 의미가 하드 선택되지 않음 |
| 관찰 가능한 변형 | 리브/코듀로이, 케이블/프린트, 헤링본/셰브론, 오프/콜드숄더, 플랫폼/하이힐 | 이름 대신 실제 구성·형태의 차이가 선택과 문장에 보존됨 |
| 숨은 명세 | 필파워/충전량, 원료, 인타르시아 공정, 기모·실리콘·안쪽 반바지 | 사진만으로 수치·내부 구조 PASS를 주지 않음 |
| 소유·효과 | 코트 벨트 vs 니트 허리, 소매 썸홀 vs 장갑, 별개 이너와 하네스 | 모든 관계·효과가 같은 의복·착용자에 결속됨 |
| 잠금·가림 | 전신 구도와 니트 표면, 스카프가 가린 목선, 코트가 가린 등 | 구도·몸·다른 옷을 바꾸지 않으며 가려진 의무는 미관찰 |
| 조합 | 미니+타이츠+부츠, 발레코어 여섯 층, 고딕의 레이스/레이스업 | 서로 다른 옷의 경계·앞표면·원문 목적이 모두 유지됨 |

회귀의 핵심은 ‘실패할 대체물’을 넣는 것이다. 끊긴 가터 경로, 고리를 통과하지 않는 토글, 삭제된 이너, 몸으로 전파된 코트 벨트, 자동 macro 구도, 평면 케이블 그림, 피부색 안층을 맨살로 판정하는 변형을 거부하거나 증거 수준에 맞게 미관찰 처리해야 한다.

픽셀 묶음은 니트 3개, 파일·트림, 배플, 코트 여밈, 스카프 연결, 목선·커프, 크롭·지퍼, 일루전, 등판·코트, 타이츠, 가터·부츠 구간, 손·귀 액세서리, 하네스·장식, 원문 코디 회귀로 구성했다. 원본 해상도에서 같은 소유자의 경계·접합·실 경로를 검사한다. 신체의 소유·도달·지지·접촉·가시성에 관한 실행 가능성은 의미 검증과 별도로 검토한다.

필요 경계가 가림·크롭·해상도 때문에 보이지 않으면 `UNOBSERVABLE_NOT_PASS`다. 일부 부품만 보이면 전체 관계가 통과하지 않는다. 내부 성능은 별도 명세·시험 근거가 필요하다. 생성이 차단되면 scored pixels가 없으며 그 상태를 기록한다. 뒤 시점·제품 단면 같은 진단 장면은 도움이 되지만 원래 요청에서 가려졌던 의미가 성공했다는 증거는 아니다. 원문 의도를 바꾼 대체 착장은 별도 결과로 기록한다.

## 9. 이번 연구의 검증 결과와 증거 경계

연구 빌더로 개수·ID 중복·출처 연결·304행 카드 매핑·CSV/JSON 모든 열의 일치·기존 ID 존재·분류/부위/코디/비교/픽셀 계획의 참조를 확인했다. 문서의 로컬 링크, 해시·산출물 관계, 기존 dirty 파일 보존 상태는 최종 검증 원장에 별도로 기록한다.

- [연구 구조 검증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/winter-fashion-20261009/research-validation.json)
- [문서·산출물 최종 검증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/winter-fashion-20261009/report-validation.json)
- [작업 전후 원본·dirty 파일 비교](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/winter-fashion-20261009/final-preservation.json)

| 증거층 | 이번 상태 |
|---|---|
| 원문 용어·출처·정의·후보·반영 계획 | 작성·구조 검증 완료 |
| 현재 원본 데이터 로드·표현 대조 | 시점·해시가 있는 읽기 스냅샷 |
| 실행 원본 등록·인덱스 재생성·runtime 출판 | 미실행 |
| 실제 의미 검색·후보 노출·선택·구성 audit | 미실행 |
| 이미지·원본 픽셀·사용자 판단 | 미실행 |
| commit·push | 미실행 |

재현 명령은 아래와 같다. 첫 명령은 당시 원본 스냅샷을 새 시점으로 갱신하므로 과거 증거를 보존하려면 폴더를 복사해서 실행한다. 두 번째와 세 번째는 저장한 연구 자료를 검증·문서화한다. 이 명령들은 생성 서비스나 embedding provider를 호출하지 않는다.

```bash
.venv/bin/python docs/research-evidence/photo-prompt/winter-fashion-20261009/audit_current.py
.venv/bin/python docs/research-evidence/photo-prompt/winter-fashion-20261009/build_research.py
.venv/bin/python docs/research-evidence/photo-prompt/winter-fashion-20261009/finalize_research.py
```
