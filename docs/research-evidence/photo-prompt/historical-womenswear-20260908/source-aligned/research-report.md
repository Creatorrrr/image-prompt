# 중세·근대 여성복: 원문 연계 시각 의미·후보팩 보강 연구

조사일: 2026-09-08  
기준 저장소: image-prompt, HEAD 1aa4d9b29b18d93c7a8d9a4be0b014d109e7b3b2  
원문: **중세 근대 여성복 조사**, 대화 ID 6a9e4eb9-563c-83e8-b0a8-5096d1e80ad7

핵심 보강 방향은 **옷 이름을 늘리는 것보다, 어느 천이 어디에서 시작하고 무엇에 붙으며 어느 방향으로 부피를 만드는지를 데이터로 갖추는 것**이다. 같은 시대의 의복도 서로 다른 구조가 있으며, 한 옷 안에 두 분류가 함께 성립하기도 한다. 이번 산출물은 원문에 맞춘 연구·데이터 제안이며 운영 데이터 채택이나 이미지 성능 검증 결과가 아니다.

원문을 직접 읽어 13개 표의 **110개 데이터 행**과 표 밖의 중요한 범위·주의점 7개를 연결했다. 유럽 14세기부터 1930년대까지, 한국·일본·중국 관련 항목을 포함한다. 이전에 만들어져 있던 서유럽 중심 36개 초안은 원문과 다시 대조했고, **46개 후보를 추가하여 82개 후보·159개 시각 구성요소**로 확장했다. 인접 시대 비교용 후보, 창작 표현, 출처 보강이 필요한 항목을 구분했다. 이 수치는 고증을 마친 후보의 수가 아니다.

출처 대장은 이전 40건과 이번 30건을 합쳐 **70건**이다. 이번 조사에서 본문·도록 메타데이터를 확인한 자료는 45건, 검색으로 제공된 기사 본문만 확인한 자료 1건, PDF 검색 발췌만 확보한 자료 1건이다. 이전 조사 기록을 유지하고 재확인하지 않은 22건과 재접근 실패 1건도 명시했다. 소장품 사진은 **4건 직접 관찰**했다. 세부 접근 상태는 [출처 대장](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/historical-womenswear-20260908/source-aligned/source-ledger.json)에 있다.

## 1. 데이터가 해결해야 하는 문제

원문의 용어는 같은 종류의 태그가 아니다. 프랑세즈는 가운 계열, 파니에는 속 지지 구조, 앙가장트는 소매 끝 장식, 새틴은 직조·표면 표현, mourning은 용도, window light는 촬영 조건이다. 이를 모두 동등한 미감 태그로 취급하면 검색은 되어도 무엇이 화면에 있어야 하는지 불분명해진다.

| 층 | 데이터의 역할 | 예 | 피해야 할 결합 |
|---|---|---|---|
| 역사·용어 | 명칭, 지역, 시기, 선택 표본, 자료의 확실성 | 1920년대 소장 치파오 / 1930년대 변형 | 원문 시대 카드 하나를 단일 의상으로 고정 |
| 의복 구조 | 레이어, 부착점, 여밈, 주름의 시작점, 부피 방향 | 목선→등 주름→허리 아래 | 옷의 부피를 인체 비율로 변경 |
| 표면 | 섬유, 직조, 파일, 반사, 문양 제작법 | 실크 + 새틴 / 다마스크 + 브로케이딩 | 광택으로 실크 성분·재단 방향을 확정 |
| 장면 관계 | 인물·손·소품·동작·받는 대상 | 손→부채 경첩→펼쳐진 살 | 떠 있는 소품, 직업·신분의 외모 추정 |
| 촬영·판독 | 특징이 보이는 시점과 크기 | 후면 전신 / 소매 접합부 근접 | 이름이 프롬프트에 있다는 이유로 픽셀 통과 |

각 후보에는 긍정적인 영어 구성요소, 한국어 혼동 경계, 근거 출처, 선택 변형의 범위, 필요한 시점, 원문 행 ID, 검증 상태를 넣었다. 역사 해설과 제한 문구를 그대로 생성 프롬프트에 넣는 방식은 피했다. 12개 의미 축과 검사 설계는 [검증 계획](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/historical-womenswear-20260908/source-aligned/verification-plan.v2.json)에 기계가 읽을 수 있는 형태로 기록했다.

## 2. 유럽 복식에서 우선 고쳐야 할 구분

### 등판과 겉치마는 별개 축이다

가장 중요한 사례는 **앙글레즈와 폴로네즈식 드레이프의 공존**이다. Met의 약1780년 가운은 소장품명이 robe à l’anglaise이고, 설명은 겉치마를 세 부분으로 걷어 올리는 polonaise 구성을 다룬다. 따라서 “프랑세즈/앙글레즈/폴로네즈 중 하나만 선택”하는 배타적 열거형은 부정확하다. [Met, 1976.146a,b](https://www.metmuseum.org/art/collection/search/84611)

이를 등판과 스커트 드레이핑 두 축으로 분리했다.

| 판단 축 | 보이는 관계 | 결정적인 반례 | 필요한 시점 |
|---|---|---|---|
| 프랑세즈의 자유로운 등 주름 | 등목선에서 시작한 깊은 주름이 허리를 지나 아래로 이어짐 | 허리에서 시작한 치마 주름만 있음 | 등목선부터 밑단까지 후면 |
| 앙글레즈의 맞춘 등판 | 등판이 허리에 맞춰지고 그 아래로 치마가 퍼짐 | 목선부터 늘어진 자유로운 등 주름 | 후면 |
| 폴로네즈식 걷어 올림 | 들어 올린 겉치마 구획과 아래의 별도 페티코트 | 뒤쪽에 큰 부피 하나만 있음 | 여러 구획과 아래 치마를 확인할 수 있는 시점 |

프랑세즈의 설명과 후면 소장품 사진은 목선의 주름 시작점을 뒷받침한다. 앙글레즈 검사용 번들에서는 후면과 동시에 보기 어려운 “앞 페티코트 노출”을 분리했다. 앞 열림은 독립적인 오버스커트 레이어 후보에서 검사한다. [Met 프랑세즈, 2001.472a,b](https://www.metmuseum.org/art/collection/search/83094), [Met 프랑세즈, 2009.300.903a,b](https://www.metmuseum.org/art/collection/search/159485), [Met 앙글레즈, C.I.37.66a,b](https://www.metmuseum.org/art/collection/search/82288)

### 넓은 치마는 부피의 방향부터 구분한다

파니에는 좌우 폭, 케이지 크리놀린은 선택 표본의 후프 외곽, 버슬은 뒤쪽 돌출이 주요 비교점이다. 크리놀린도 시기에 따라 뒤로 부피가 이동하므로 “항상 정원형”으로 고정하면 안 된다. 1870년대 버슬과 1880년대의 높은 후방 돌출도 별도 변형으로 유지한다. [V&A, Corsets, crinolines and bustles](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear)

속구조가 가려진 완성복에서는 **외곽선만** 검사한다. 후프, 테이프, 스테이즈의 본, 내부 끈은 구조 전시나 제작 자료의 검사 대상이다. 같은 이유로 파니에의 정면 사진 한 장에서 앞뒤 깊이를 정확히 산출하지 않는다. [Met, Nineteenth-Century Silhouette and Support](https://www.metmuseum.org/pt/essays/nineteenth-century-silhouette-and-support)

1780년대 슈미즈 가운의 자연 허리 부근 새시와, 뒤이어 올라간 허리선을 구분했다. “가벼운 흰 천”을 공유한다는 이유로 모두 엠파이어 웨이스트가 되면 실패다. [Met, Eighteenth-Century Silhouette and Support](https://www.metmuseum.org/de/essays/eighteenth-century-silhouette-and-support)

### 중세·르네상스는 이름보다 부착 관계를 구체화한다

| 원문 용어 | 추가할 시각 의미 | 혼동·범위 제한 | 근거 |
|---|---|---|---|
| Kirtle / Cotte / Cotehardie | 선택한 긴 가운의 몸판 피팅, 소매, 안쪽 레이어 | 용어의 시대별 차이 보존; 모든 커틀에 밀착·끈 여밈 강제 금지 | [FIT 1430s](https://fashionhistory.fitnyc.edu/1430-1439/) |
| Houppelande / Bombard | 풍성한 겉가운, 위보다 아래가 넓게 열리는 소매 | 크게 부푼 위팔·좁은 손목의 gigot와 구분; 다른 우플랑드 소매도 존재 | [FIT 1400s](https://fashionhistory.fitnyc.edu/1400-1409/) |
| Tippet | 긴 천 조각이 **소매 뒤쪽에 붙어** 늘어남 | 목 스카프·손에 든 리본으로 바뀌면 실패 | [FIT 1400s](https://fashionhistory.fitnyc.edu/1400-1409/) |
| Chemise / Smock | 목선·소매 틈에서 보이는 별도 안쪽 천 | 18세기 슈미즈 가운·현대 슬립과 구분 | [FIT 1490s](https://fashionhistory.fitnyc.edu/1490-1499/) |
| Gamurra | 선택 표본의 몸판, 분리 소매, 끈 접합 | 사각 목선은 선택형; 모든 가무라의 보편 조건 아님 | [National Gallery, Costanza Caetani](https://www.nationalgallery.org.uk/paintings/style-of-domenico-ghirlandaio-costanza-caetani) |
| Giornea | 가무라 위에 걸친 앞뒤 패널과 보이는 안쪽 옷 | 열린 옆선과 닫힌 옆선이 모두 존재; 본 후보는 열린 변형 | [FIT 1490s](https://fashionhistory.fitnyc.edu/1490-1499/) |

바베트는 턱 아래로 지나가는 좁은 띠, 윔플은 턱과 목을 감싸는 넓은 면, 필릿은 머리둘레 띠로 나눴다. 머리 모양이 비슷해도 경로와 덮는 면적이 다르다. 베일은 얼굴 전체를 가릴 필요가 없다. [FIT, Barbette](https://fashionhistory.fitnyc.edu/barbette/)

원문의 hennin 관련 주의점도 보존했다. **hennin 검색 별칭을 삭제하지 않고** conical headdress / turret / haut bonnet과 연결하되, 선택한 원뿔과 베일 형태를 설명한다. 명칭의 역사적 구분을 곧바로 이미지 분류의 절대 규칙으로 바꾸지 않는다. [FIT 1450s](https://fashionhistory.fitnyc.edu/1450-1459/)

### 목·몸판·소매 장식은 위치를 잃지 않아야 한다

러프는 목 둘레의 반복된 주름 구조다. 당시에도 크기·층·세움 방식이 달랐으며, 같은 계열의 목 장식을 한 가지 원반으로 고정하지 않는다. 소매 끝 장식 engageantes가 목으로 이동하는 것도 구분할 오류다. [National Portrait Gallery, Collars and Ruffs](https://www.npg.org.uk/whatson/display/2016/framing-the-face-collars-and-ruffs/), [Met, Engageantes](https://www.metmuseum.org/art/collection/search/218114)

falling band는 여성 사례가 있지만 주로 남성 용례를 다루는 용어다. 여성 후보는 해당 초상의 넓은 어깨 칼라 변형으로 한정한다. Fichu는 별도 삼각형 어깨 천이며 목의 러프나 머리 베일과 다르다. [FIT, Falling band](https://fashionhistory.fitnyc.edu/falling-band/), [V&A, French lace fichu](https://www.vam.ac.uk/blog/caring-for-our-collections/the-twelve-days-of-christmas-at-clothworkers-french-lace-fichu)

스토머커는 몸판 앞 열림 안에 놓이는 앞판이다. 스테이즈, 앞이 뾰족한 보디스와 같은 물건으로 합치지 않는다. NMS 만투아는 원래 스토머커가 남지 않았다고 명시한다. 전시 보완물의 정확한 형태를 해당 가운 원형의 확정 증거로 쓰면 안 된다. 또한 이 18세기 궁정 만투아를 원문의 17세기 후반 초기 만투아 전체에 적용하지 않는다. [National Museums Scotland, Court mantua](https://www.nms.ac.uk/discover-catalogue/luxury-in-fashion-the-18th-century-court-mantua)

## 3. 1900–1930년대의 오해를 막는 후보

| 항목 | 이번 보강 | 판정의 한계 |
|---|---|---|
| Shirtwaist | 별도 블라우스와 치마의 허리 경계 | 직업 여성이라는 인물 속성은 옷에서 추론하지 않음 |
| Pigeon-breast | 허리 앞에서 부푸는 **옷감** | 흉곽·가슴 크기·척추를 과장하는 신체 지시로 바꾸지 않음 |
| Lingerie dress | 여름 외출용의 가벼운 긴 겉옷, 선택한 레이스 인서션 | 현대 속옷·잠옷으로 라우팅하지 않음 |
| Mourning dress | 문맥으로 상복을 확정한 뒤 선택한 직물·단계 표현 | morning과 구별; 검정·표정만으로 상복 판정 금지 |
| Drop waist | 몸의 자연 허리보다 아래에 있는 **옷의 허리선** | 술 장식·무릎 길이·단발이 모두 필수인 것은 아님 |
| Cloche | 머리에 밀착한 종 모양과 선택한 짧은 챙 | 넓은 챙 모자와 구별; 재료·머리 길이 강제 금지 |
| Bias cut | 재단의 근거와 유연한 드레이프의 픽셀 결과 분리 | 새틴 광택만으로 45도 재단을 증명할 수 없음 |

란제리 드레스는 Avenir Museum 전시 설명과 UNH 소장품 기록을 연결했다. UNH 표본은 약1905–1910년 흰 면 드레스의 레이스 요크·소매, 허리, 뒤 여밈을 구체적으로 기록한다. 이것은 선택 표본의 구조이지 모든 란제리 드레스가 같은 패턴이라는 뜻은 아니다. [Avenir Museum 전시 해설](https://www.chhs.colostate.edu/avenir/exhibitions/past-exhibitions/tigers-leap-fashion-past-present-future/tigers-leap-fashion-past-present-future-part-i-exhibition-text/), [UNH, Bowen Collection 198](https://scholars.unh.edu/bowen_collection/198/)

상복 전시는 직물·색이 달라지는 사례를 보여준다. 플래퍼·클로슈도 1920년대 안에서 변형이 있으므로 한 고정 외형으로 만들지 않는다. [Met, Death Becomes Her](https://www.metmuseum.org/exhibitions/listings/2014/death-becomes-her), [FIT 1920s](https://fashionhistory.fitnyc.edu/1920-1929/), [ASU FIDM, 1920s cloche](https://fidmmuseum.org/learn/articles/1920s-cloche)

바이어스 컷은 **직물 결에 대한 재단 방향**이며, 결과적인 드레이프를 연출하는 후보와 생산기법의 증거는 분리했다. Vionnet의 개별 드레스를 참고해 모든 1930년대 드레스에 등 파임이나 동일한 길이를 강요하지 않는다. [V&A, Madeleine Vionnet](https://www.vam.ac.uk/articles/madeleine-vionnet-an-introduction)

## 4. 한국·일본·중국: 이미 있는 기본형에 시대와 착용 관계를 더한다

| 원문 범위 | 시각 의미의 추가분 | 중요한 혼동 경계 | 근거 |
|---|---|---|---|
| 장옷 | 머리에 걸친 **소매 있는 포**, 얼굴 둘레 앞자락, 고름과 소매끝의 구별 | 소매 없는 쓰개치마로 대체하지 않음; 색·신분은 고정하지 않음 | [한국민족문화대백과 장옷](https://encykorea.aks.ac.kr/Article/E0048702) |
| 쓰개치마 | 머리 위의 모인 띠, 그 아래 넓은 천, 턱 아래로 모이는 끈 | 일반 치마처럼 허리에 입히거나 소매를 만들지 않음 | [전통생활문화포털 쓰개치마](https://www.kculture.or.kr/brd/board/1077/L/menu/1067?bbIdx=303&brdType=R&searchField=title&searchText=%EC%93%B0%EA%B0%9C%EC%B9%98%EB%A7%88&thisPage=1) |
| 당의 | 긴 앞뒤 자락, 열린 옆선, 아래 치마, 선택한 거들지 | 짧은 저고리만 묘사하는 것과 구별; 왕실 표본의 모든 장식 강제 금지 | [국립고궁박물관 영친왕비 당의](https://www.gogung.go.kr/gogung/pgm/psgudMng/view.do?cl=&gubunCd=&menuNo=8000653&pageIndex=&pn=&psgudSn=364772&searchClCd=&searchCondition=&searchKeyword=) |
| 1920–30년대 개량한복 | 선택 도판의 긴 저고리, 짧은 통치마, 드러난 신발 등 | 현대 생활한복과 구별; 버튼·단발을 전체의 의무로 만들지 않음 | [이상례·소황옥, 2019](https://kjournal.co.kr/_PR/view/?aidx=20922&bidx=1683) |
| 고소데 | 큰 소매 패널 내부의 **작은 입구** | 작은 입구가 반팔을 뜻하지 않음; 후대 수선 기록 보존 | [Met, 2023.730](https://www.metmuseum.org/art/collection/search/901856) |
| 기모노·오비 | 착용자의 왼 앞섶이 오른 앞섶 위로 오고 별도 오비가 겹침 | 화면 좌우 혼동; 모든 시대에 동일한 오비 매듭 강제 금지 | [V&A, Kimono](https://www.vam.ac.uk/articles/kimono) |
| 청 말기 장포 | 긴 몸판, 넓은 소매, 가장자리 트림과 의복에 속한 자수 | 혼례 상의+치마 두 벌 구성과 구별; 모든 여성복을 용포로 치환 금지 | [Met, 1970.145](https://www.metmuseum.org/art/collection/search/70499) |
| 청 말기 혼례 상의·치마 | 별도 상의, 치마의 평평한 앞판과 주름부 | 장포 한 벌과 구별; 일상복의 보편형으로 확대 금지 | [Met, 46.187.2a,b](https://www.metmuseum.org/art/collection/search/65367) |
| 1920년대 치파오 | 넉넉하고 긴 몸판, 선택 표본의 넓고 긴 소매 | 현대 초밀착·높은 양옆 트임을 기본값으로 넣지 않음 | [NHB, 1995-03865](https://www.roots.gov.sg/Collection-Landing/listing/1081212) |
| 1930년대 치파오 | 앞선 느슨한 형과 비교해 허리·소매가 좁아진 사례 | 모든 옷에 같은 전환 연도·트임을 강요하지 않음 | [NHB, Cheongsam 전시 해설](https://www.roots.gov.sg/stories-landing/stories/be-in-the-mood-for-cheongsam/story) |

치파오의 1920년대 실물은 싱가포르/말레이시아로 기록되어 있다. 중국 도시복이라는 원문 관심사와 비교할 수 있지만, 그 사진을 중국에서 실제 촬영된 기록으로 바꾸면 안 된다. 고소데 실물도 소매가 후대에 개조되었다고 기록하므로 현재 모습의 모든 치수를 원형으로 확정하지 않았다.

신여성은 단일 옷의 이름이 아니다. 개량한복·양장·혼용의 구체 사례는 후보가 될 수 있지만, 옷이나 단발을 입은 인물의 사상·교육·성격을 확정하는 규칙은 만들지 않는다. 2019년 논문의 복식 기록과 사회적 인물 해석도 구분해서 사용했다. [국립현대미술관, 신여성 도착하다](https://www.mmca.go.kr/pr/newsDetail.do?bdCId=201712220006128)

## 5. 소재·장식·생활 소품의 데이터 방식

소재는 최소한 **섬유 / 직조·파일 / 표면 반사 / 문양 제작법 / 의복에 부착된 위치**를 나눠야 한다. 섬유와 직조는 다른 축이며, 박물관 직물에는 satin damask 바탕에 supplementary brocading을 더한 사례도 있다. 이 관계가 “실크 또는 새틴”, “다마스크 또는 브로케이드” 같은 잘못된 배타 분류를 막는다. [Smithsonian, Weave construction](https://www.si.edu/spotlight/national-woven-coverlet-collection/history-and-construction), [Cooper Hewitt, 1999-18-1](https://www.si.edu/object/textile%3Achndm_1999-18-1)

| 원문 소재 묶음 | 관찰 문구로 보강할 것 | 사진으로 확정하지 않을 것 |
|---|---|---|
| matte wool / washed linen | 낮은 반사와 교차하는 실의 표면 | 울·리넨 성분, 세탁 이력, 경제 수준 |
| silk velvet | 짧은 파일이 천의 방향에 따라 만드는 명암 | 실크 성분·산지·가격 |
| silk satin | 곡면 주름을 따라 이어지는 넓은 하이라이트 | 섬유 성분·바이어스 재단 |
| crisp taffeta | 표면에서 떨어져 형태를 유지하는 또렷한 접힘 | 소리·손감, 모든 타프타의 같은 강성 |
| brocade / damask | 바탕 조직의 명암 대비와 추가 직조 문양 | 둘의 상호 배타성 |
| fine muslin / light cotton | 가벼운 겹의 독립된 가장자리와 모임 | 완전 투명한 피부 노출, 특정 허리선 |
| lace insertion / cuffs / pintucks | 패널을 잇는 레이스, 소매끝 자수, 봉제한 가는 턱 | 줄무늬 프린트를 턱으로 인정 |
| rosettes / flounces | 접힌 리본의 고리와 겹치는 자유로운 단 | 실제 꽃이나 평면 무늬로 대체 |
| metal thread / braid / trim | 천에 고정된 실 경로를 따르는 작은 반사 | 실제 금·은 성분, 전신 금속 재질 |

벨벳 구조는 V&A 직물 연구를, 타프타·러플 등은 FIT의 1865년 드레스 분석을 사용했다. 다만 **핀턱과 리본 로제트의 정확한 시대별 실물 검증은 아직 남아 있다**. 해당 후보는 일반 시각 설계 단계로 표시하고 24개 우선 번들에 넣지 않았다. 가구용 다마스크 자료도 표면 관계만 참고하며 여성복의 시대 근거로 재사용하지 않았다. [V&A, Project Interwoven](https://www.vam.ac.uk/blog/projects/project-interwoven-studying-textiles-from-the-outside-in), [FIT, 1865 taffeta dress](https://fashionhistory.fitnyc.edu/1865-cream-silk-taffeta-dress/), [Smithsonian, Cheney satin damask](https://americanhistory.si.edu/collections/object/nmah_1168895)

원문 소품 7묶음은 [장면 레시피](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/historical-womenswear-20260908/source-aligned/scene-recipes.json)로 정리했다. 쓰기·바느질·채집·사교·몸단장·이동·허리 도구를 각각 손과 물체의 접촉 관계로 설명한다. 모든 물건을 한 장에 넣지 않고 동작에 필요한 것만 선택한다. 예를 들어 **손이 부채의 아래 경첩을 잡고 살이 그 지점에서 펼쳐짐**, **허리 고리→체인→도구통이 끊기지 않음**이 시각 의미다.

샤틀렌은 도구통을 연결한 실물을 확인했으며, 그 안의 가위를 반드시 밖에 노출할 이유가 없다. 레티큘은 이번에 이름·날짜·재료의 도록 정보만 확인했으므로 조임끈이나 금속 프레임의 정확한 형태를 강제하지 않는다. 나머지 소품은 장면 설계이며, 특정 연대에 넣기 전 그 시대의 형태·재료를 추가 확인한다. [Met, Nécessaire and châtelaine](https://www.metmuseum.org/art/collection/search/195098), [Met, Reticule](https://www.metmuseum.org/art/collection/search/84629)

## 6. 현재 저장소와 연결한 설계

기준 자산 34개 JSON의 슬롯 레코드를 검사했다. 생성된 검색 인덱스·shard는 제외했으며, 이 조사는 실제 라우팅·임베딩 검색·모든 하드 프로필의 전체 동작 시험이 아니다. [현재 자산 대조와 해시](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/historical-womenswear-20260908/source-aligned/local-coverage.v2.json)

| 기존 후보 또는 검색 결과 | 판단 | 보강 방식 |
|---|---|---|
| hanbok_jeogori_lower_layer_system / classical_hanbok_layered | 한복 기본 레이어를 이미 표현 | 기본형 재사용, 장옷·쓰개치마·당의의 특수 관계 추가 |
| kimono_kosode_obi_system / kimono_wrap_front_obi_layer_boundary | 기모노 앞섶·오비 기본형 존재 | 착용자 좌우, 고소데 입구, 시기·수선 범위 보강 |
| qipao_standing_collar_diagonal_closure | 칼라·대각선 여밈 존재 | 1920년대 느슨한 몸판과 시대별 소매·길이 선택형 추가 |
| opening_reformed_hanbok_length_closure | 긴 저고리·짧은 하의·버튼 후보 존재 | 이번 개량한복 표본과 중복 검토; 버튼을 전체 변형의 필수로 확대하지 않음 |
| rococopunk 관련 파니에·스토머커 | 원형을 변형하는 펑크 맥락 | 역사 원형 후보와 구분하되 기존 요청 맥락 보존 |
| ruff 검색→광대 칼라·새 목깃 | 형태/단어가 겹치는 다의어 | 역사 복식과 동물·광대 문맥의 교차 오작동 시험 |
| 앙글레즈 검색→broderie anglaise | 레이스 문맥으로도 검색됨 | 가운 등판과 아일릿 장식 분리 |

특히 “개량한복”의 단순 문자열 검색은 무일치인데 관련 opening_era 구조 후보는 존재했다. **문자열 무일치는 의미 데이터 부재의 증명이 아니다.** 이번 보고서는 검색 건수를 그대로 결손 수로 사용하지 않았다.

현재 후보 정책에서 silhouette_proportion 슬롯은 body_geometry 차원에 연결된다. 따라서 이번의 의복 폭·허리선·등판은 garment_detail 또는 costume_style의 appearance 차원으로 제안했다. surface_material은 material을 사용한다. 이는 기존 전체 동작의 버그 판정이 아니라, 새 후보가 옷의 형태를 신체 변형으로 전달하지 않도록 한 설계 선택이다.

prop·일부 맥락 슬롯은 현재 차원 표가 비어 있다. 그 상태에서 별도 소품 레시피를 번들로 만들면 컴파일은 되어도 선택 자격에서 빠질 수 있다. 따라서 첫 번들은 의복·착용 장식·표면만 사용한다. 샤틀렌은 허리 착용물로 한정했다. 소품 행동 번들은 차원과 접촉 관계를 먼저 정의해야 한다.

### 우선 번들 제안

[optional-extension.proposed.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/historical-womenswear-20260908/source-aligned/optional-extension.proposed.json)은 **24개 번들 / 50개 슬롯 항목 / 4개 슬롯 종류**를 담는다.

- 등판·치마·허리: 프랑세즈, 앙글레즈, 폴로네즈식 걷어 올림, 파니에, 스토머커, 슈미즈 가운, 엠파이어, 후기 버슬.
- 위치·시대 혼동: 티펫, 윔플, 바베트, 란제리 드레스, 드롭 웨이스트, 클로슈.
- 동아시아 변형: 장옷, 쓰개치마, 당의, 고소데 입구, 청 말기 장포, 1920년대 치파오.
- 표면·연결: 레이스 인서션, 브로케이딩, 다마스크, 샤틀렌.

각 번들은 실제 제안 슬롯 ID에만 연결되고, 구성요소·관계·출처 해시를 가진다. 관련 하드 프로필 목록은 비워 두었다. 검색 또는 선택만으로 새로운 하드 의무가 활성화되어서는 안 된다. 이 파일은 docs 안의 검토용 초안으로, 운영 자산·필수 확장 목록·검색 인덱스에 등록하지 않았다.

## 7. 무엇을 실제로 확인했는가

| 증거 층 | 이번 결과 | 해석 |
|---|---|---|
| 원문 회수 | 전체 읽기 성공, 추가 페이지 없음 | 이전 초안의 원문 미확인 상태를 이번 산출물에서 해소 |
| 원문 대조 | 110행 전부 매핑, 별도 본문 주의점7개 | 각 행이 모두 역사적으로 검증되었다는 뜻은 아님 |
| 소장품 픽셀 | 후면 가운2건, 쓰개치마 펼침1건, 청 말기 장포1건 관찰 | 모델 생성 이미지의 성능 증거가 아님 |
| 제안 구조 | ID·참조·허용 키·차원·해시·실제 번들 컴파일 검사 통과 | 실제 pack에 노출되는지와 별도 |
| 런타임 등록·전체 로더 | 미실행 | maintenance registry 연결도 미시험 |
| 실제 후보 노출·프롬프트·생성 이미지 | 미실행 | 개선 효과 또는 렌더 성공률 주장 없음 |
| 기존 파일 보존 | 부모 연구6개 파일 및 런타임 자산·스크립트 해시 유지 | source-aligned 하위에만 추가 |

직접 본 사진의 관찰과 보이지 않은 사항은 [검증 계획의 source_image_observations](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/historical-womenswear-20260908/source-aligned/verification-plan.v2.json)에 기록했다. 프랑세즈와 앙글레즈는 후면의 주름 시작점이 달랐고, 쓰개치마 사진은 펼침 상태라 턱 아래 손동작을 직접 보여주지 않았다. 장포의 나비는 천 위 문양이며 실제 곤충 장면이 아니었다.

재현 가능한 검사는 [build_research.py](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/historical-womenswear-20260908/source-aligned/build_research.py)와 [artifact-check.v2.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/historical-womenswear-20260908/source-aligned/artifact-check.v2.json)에 있다. 이 스크립트는 연구 파일을 재구성하며 운영 자산은 변경하지 않는다.

## 8. 채택 순서와 남은 연구 범위

1. **먼저 다의어와 원래 의도 보존을 검사한다.** ruff/동물, anglaise/레이스, mourning/morning, cloche/식탁 덮개 등 12개 회귀 입력을 준비했다. 잠긴 신체·장면·촬영 의도가 의복 후보로 바뀌지 않아야 한다.
2. **실제 생성 pack에서 노출·선택을 검사한다.** 컴파일 성공으로 대신하지 않는다. 최대 번들2·멤버8 제한과 열린 차원을 지킨다. 24개를 한 번에 모두 보여주는 것이 목표가 아니다.
3. **모양을 구별하는 픽셀 시험을 수행한다.** 26개 사례에 양성 변형, 최소 반례, 결정적인 관계, 필요한 시점을 작성했다. 첫 8개 사례를 현재 런타임 A / 제안 후보 추가 B / 같은 의미를 명시적으로 쓴 참고 문장 C로 비교하도록 설계했다. 아직 실행하지 않았다.
4. **통과한 항목만 단계적으로 채택한다.** 소매·머리쓰개·등판 등 서로 다른 문제로 결과를 확대하지 않는다. 프롬프트와 런타임 기록, 전달·차단 여부, 픽셀, 사용자 판단을 따로 남긴다.

남은 자료 보강도 구체화했다. 프렌치·게이블 후드는 당시 원 초상 대조가 필요하고, 영화 의상 분석을 대체 근거로 쓰지 않는다. Virago sleeves의 원 페이지는 재접근에 실패하여 보류했다. Bliaut는 더 이른 시대의 비교용이며 PDF 본문이 미확인이다. 핀턱·리본 로제트, 레티큘 여밈, 특정 시대의 소품 형태는 추가 실물 확인 후에만 해당 범위의 고증 후보가 된다. 단일 소장품의 수선·복원·전시 보완 요소도 유지한다.

의복 시대와 촬영 방식은 끝까지 독립적으로 보존한다. 라파엘전파의 중세 재해석은 후대의 표현이고, 중세 복식을 입은 현대 컬러 촬영은 중세 당시의 사진이 아니다. [V&A, Arts and Crafts fashion](https://www.vam.ac.uk/articles/how-arts-and-crafts-influenced-fashion)

## 산출물 안내

| 파일 | 용도 |
|---|---|
| [원문 대조표](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/historical-womenswear-20260908/source-aligned/keyword-alignment.md) / [JSON](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/historical-womenswear-20260908/source-aligned/keyword-alignment.json) | 110개 원문 행과 데이터 처리 경로 |
| [82개 후보 초안](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/historical-womenswear-20260908/source-aligned/candidate-drafts.v2.json) | 구성요소·범위·반례·출처·원문 ID·보류 상태 |
| [30개 출처·46개 추가 후보의 작성 원본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/historical-womenswear-20260908/source-aligned/research-additions.json) | 추가 조사 데이터의 수정 출발점 |
| [70개 출처 대장](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/historical-womenswear-20260908/source-aligned/source-ledger.json) | 현재 확인/이전 기록/접근 실패의 구분 |
| [24개 선택 번들 제안](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/historical-womenswear-20260908/source-aligned/optional-extension.proposed.json) | 운영 등록 전 검토할 스키마 호환 초안 |
| [컴파일 미리보기](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/historical-womenswear-20260908/source-aligned/compiled-bundles.preview.json) | 실제 컴파일러로 변환한 관계·차원·해시 |
| [검증 설계](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/historical-womenswear-20260908/source-aligned/verification-plan.v2.json) | 의미 축12개, 관찰4건, 형태사례26개, 회귀입력12개 |
| [장면 레시피](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/historical-womenswear-20260908/source-aligned/scene-recipes.json) | 소품7묶음의 행동·접촉·시대 확인 항목 |
| [구조 검사 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/historical-womenswear-20260908/source-aligned/artifact-check.v2.json) | 수행한 검사와 미실행 범위 |

