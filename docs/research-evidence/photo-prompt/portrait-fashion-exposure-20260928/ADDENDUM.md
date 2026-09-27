# 참조 대화에 추가된 분석의 검증과 데이터 반영

확인일: 2026-09-28. 같은 대화를 다시 조회해 뒤에 추가된 분석 한 턴을 전부 읽었다. 새 응답은 가슴의 측면·하부, 배꼽·아랫배, 밀착 의복, 메쉬, 스타킹, 절대영역, 자세와 촬영 각도를 다룬다. 원래 연구·검증 결과는 [첫 조사 스냅샷](revisions/initial/snapshot-manifest.json)에 동결했다. 아래 분석은 추가 응답의 인용 번호를 재사용하지 않고 원출처와 현행 레지스트리를 다시 대조한 것이다.

## 1. 반영 원칙과 추가 범위

**노출 위치, 의복 구조, 밀착도, 투과성, 표면 광택, 자세, 시점은 별도 축**이다. 관능성은 시각 요소를 고르는 요청의 맥락이지, 피부 면적이나 특정 체형에서 자동 계산할 수 있는 속성이 아니다. 새 용어도 넓은 표기는 탐색용으로 두며, 같은 소유자에 속하는 완전한 관계 또는 명시적 채택만 강한 의무를 만든다.

이번 추가분은 **14개 프로필, 22개 후보, 8개 선택형 묶음**이다. 첫 조사분을 합치면 **28개 프로필, 40개 후보, 14개 묶음**, 확인 출처는 **34개**다. 기존 쇄골, 데콜타주, 허리–골반 윤곽, 콘트라포스토, 모래시계 비례, 시어 레이어 프로필은 재사용한다. 실제 인물의 신체 비례를 바꾸거나 자세를 체형으로 승격하는 규칙은 추가하지 않았다.

다음 표는 의미 축을 비교하기 위한 연구 카탈로그다. 모든 표현이 동의어라는 뜻이 아니며, 표의 설명형 문구에는 이번 연구가 작성한 표현도 포함된다. 출처가 없는 특정 신체·의복 조합은 문헌상의 정식 용어 또는 효과 검증 결과로 표시하지 않는다.

## 2. 노출 위치와 실제 신체 지시 대상

사전에서 `sideboob`은 의복 옆으로 보이는 가슴의 바깥 곡선, `underboob`은 가슴의 하부에 대한 속어다. 중앙의 가슴골, 어깨·쇄골, 복부와 서로 바꿔 쓰지 않는다. [Dictionary.com](https://www.dictionary.com/browse/side-boob), [Collins](https://www.collinsdictionary.com/us/dictionary/english/underboob)

| 용어군 | 관찰 대상 또는 관계 | 분리할 축·혼동 경계 | 데이터 반영 |
|---|---|---|---|
| sideboob / 사이드부브 | 팔구멍·옆선 경계와 인접한 가슴 측면 | 중앙 골, 위팔, 등 노출 | `pfe_lateral_chest`; 범위를 한정한 설계 |
| underboob / 언더부브 | 불투명 상의 하단과 가슴 하부의 피부 곡선 | crop top 아래 복부만 보인 경우 | `pfe_lower_chest`; 중앙 면의 의복 피복 보존 |
| collarbone-baring / 쇄골 노출 | 목 아래 쇄골과 주변 함몰의 가독성 | 어깨 노출, 목선 깊이, 가슴골 | 기존 `clavicle_supraclavicular_hollow` |
| keyhole neckline / 가슴 컷아웃 | 목선 몸판의 지정 개구·연결된 경계 | 가슴골, 배꼽, 허리 컷아웃 | 위치를 지정하는 연구 축; 기존 의복 후보 연계 |
| navel-baring / 배꼽 노출 / umbilicus | 피부 위에서 식별되는 배꼽과 이를 가리지 않는 의복 경계 | 단순 midriff, 단추, 장식·그림자 | `pfe_navel`; 상하의 사이 관계를 한정 |
| bare lower abdomen / 아랫배 노출 | 하의 허리선 위에 남는 복부 피부 | 배꼽 보임, 골반 뼈, 성기 주변 지시 | `pfe_lower_abdomen_candidate` |
| low-rise waist / 낮은 허리선 | 하의 허리밴드의 위치 | 상의 길이, 배꼽 가시성, 이너 밴드 | 기존 후보; 노출 자동 활성화 없음 |
| V-shaped waistband / V자 허리밴드 | 같은 하의의 경사진 두 가장자리와 V자 연결 | 피부 위 V자 선, 복부 근육, low-rise | `pfe_v_waistband_candidate` |
| waist-to-hip contour / 허리–골반 윤곽 | 옆구리에서 엉덩이 외곽으로 이어지는 표면 | 골반 뼈 자체, 이상적 체형, 의복 압박 | 기존 `lateral_waist_hip_contour_transition` |
| pubis / 치골 | 골반뼈 앞쪽의 특정 부분 | 아랫배 전체, 장골능, 연부조직 | 해부학 혼동 방지용 연구 항목 |
| iliac crest / 장골능 | 장골 상단의 뼈 가장자리 | 치골, 겉으로 보이는 옆구리 곡선 | 픽셀에서 뼈 위치를 확정하지 않음 |
| mons pubis / 치구 | 치골 앞쪽의 둥근 연부조직 영역 | 치골이라는 뼈, 아랫배 전체 | 명칭 구분만 기록; 생성용 세부 노출 후보 없음 |

배꼽은 복부의 특정 표지다. 배꼽이 가려진 피부 띠만으로 배꼽 노출 조건을 충족하지 않는다. 함몰·돌출 형태, 장신구, 복부 체형은 독립 선택이며 특정 형태의 배꼽을 보편적 기준으로 만들지 않았다. [Merriam-Webster](https://www.merriam-webster.com/dictionary/navel)

OpenStax는 장골과 치골 및 장골능을 서로 다른 뼈 구조로 설명하고, NCI는 치구를 치골 앞쪽의 둥근 영역으로 설명한다. 이에 따라 추가 대화의 “골반·치골”을 일반적인 아랫배나 허리–골반 곡선의 별칭으로 가져오지 않았다. 이는 용어 정리이며 영상에서 해부학을 진단하는 모델이 아니다. [OpenStax](https://openstax.org/books/anatomy-and-physiology/pages/8-3-the-pelvic-girdle-and-pelvis), [NCI](https://www.cancer.gov/types/vulvar/what-is-vulvar-cancer)

## 3. 몸선을 읽는 방식: 핏과 투과성의 분리

AYM의 실제 상품 설명에는 몸의 윤곽에 맞는 의복과 이중 레이어가 함께 등장한다. 이 사례는 핏과 레이어 구성이 별도 특성이라는 근거다. 이중 레이어 문구만으로 모든 조명에서 불투명하다고 단정하지 않는다. David’s Bridal의 상품도 메쉬, 착시 목선, 안감, 키홀 등을 별도 구조로 설명한다. 상품 전체의 안감 문구를 모든 패널의 피복 상태로 확대하지 않았다. [AYM](https://www.aym-studio.com/pages/sets/siren-set), [David’s Bridal](https://www.davidsbridal.com/product/mesh-a-line-with-allover-beaded-illusion-neckline-sdwg0153)

| 용어군 | 관찰 대상 또는 관계 | 분리할 축·혼동 경계 | 데이터 반영 |
|---|---|---|---|
| opaque figure-hugging / 불투명 밀착 실루엣 | 천이 몸 윤곽을 따르면서 피부 세부를 가림 | 투과, 압박감, body paint | `pfe_opaque_fit` |
| form-fitting / skin-tight / second-skin fit | 의복과 신체 표면의 근접한 핏·비유 | 피부 노출, 비침, 체형 변경 | 넓은 탐색 표현; 불투명 조건 자동 추가 없음 |
| clingy / clinging fabric | 천의 국소적인 달라붙음 | 작은 치수, 젖음, 모든 곳의 균일 압박 | 설명형 관찰 축; 원인 자동 추정 없음 |
| slinky / body-skimming | 유연한 흐름·윤곽을 따르는 여유 | 소재 이름, 바이어스 재단, 강한 압박 | 기존 `pfe_skimming`; 둘을 완전한 동의어로 취급하지 않음 |
| structured bodice / corset-style | 패널·레이싱·보닝 등 몸판 구조 | 가슴 크기, 실제 압박, 골 노출 | 기존 의복 후보; 보이지 않는 보닝 추정 없음 |
| fine mesh / fine-net fabric | 작은 망눈과 연결된 실 | 투과 정도, 안감, 망눈 프린트 | `pfe_mesh_skin`의 지정 복부 관계 |
| fishnet / 열린 그물 패턴 | 열린 망눈의 가독성 | 모든 시어 직물, 모든 mesh의 크기 | 기존 mesh 후보; 패턴 크기 독립 |
| sheer overlay / 시어 겉층 | 비치는 외층과 그 아래 피부·의복 | 빈 컷아웃, 안감 없는 상태 | 기존 시어 광학 레이어·`pfe_sheer_liner` |
| illusion neckline / illusion panel | 몸판과 연결된 망 패널이 있는 목선 | 천이 없는 개구, 피부 위 구슬, 목걸이 | `pfe_illusion_panel` |
| fitted semi-sheer / 밀착 반투명 | 밀착과 부분 투과를 함께 선택 | 밀착이 비침을 필연적으로 만듦 | 두 축의 동시 선택; 일부만으로 hard 관계 없음 |
| lace overlay / opaque lining | 열린 레이스와 불투명 안감의 레이어 | 레이스 프린트, 피부를 안감으로 해석 | 기존 레이스 가장자리·시어 안감 후보 |

mesh는 열린 직물 구조, sheer는 투과하는 외관을 기술한다. 관찰 데이터에는 **부위 → 망눈 → 부착 경계 → 투과된 대상 → 안감 → 핏** 순으로 기록한다. 이번 `pfe_mesh_skin`은 복부 피부와 인접한 불투명 패널을 다룬다. 모든 메쉬 의복을 그 노출 위치로 변환하지 않는다. 세부 직조·섬유·압박 정도는 제작 정보 또는 별도 요청이다. [FIT](https://www.fitnyc.edu/museum/exhibitions/fabric-in-fashion.php), [직물 용어집](https://www.arcsinfo.org/content/documents/glossary_of_textile_terms.pdf)

## 4. 스타킹: 투과·광택·길이·밴드·연결을 분리

Wolford와 FALKE의 실제 분류·상품은 투과, 표면, 상단 밴드, 길이와 고정 구조를 구분한다. 동일한 망·색·데니어가 항상 같은 픽셀을 만든다는 규칙은 추출하지 않았다. [Wolford 안내](https://www.wolford.com/en-ca/our-tights-guide.html), [FALKE](https://www.falke.com/lt_en/women/socks-hosiery/hold-up-stockings/)

| 용어군 | 관찰 대상 또는 관계 | 분리할 축·혼동 경계 | 데이터 반영 |
|---|---|---|---|
| sheer tights / sheer hosiery | 연속된 스타킹 층 아래 피부색의 투과 | 맨다리, 광택, 데니어 수치 | `pfe_hosiery_sheer` |
| semi-opaque tights | 중간 투과 외관의 설명 | 고정 투명도 백분율, 정해진 D 값 | 연구 축; 조명·색·밀도 함께 기록 |
| opaque tights / 불투명 타이츠 | 천이 피부 세부를 가리는 연속된 다리 피복 | 검은색만, 바지, 부츠 | `pfe_hosiery_opaque` |
| matte finish / 무광 표면 | 강한 정반사 띠가 두드러지지 않는 표면 | 불투명도, 실제 젖음, 소재 | 투과와 별도로 선택; 광택 강제 없음 |
| soft sheen / glossy / high-shine / wet-look finish | 스타킹의 곡면을 따르는 반사 띠 | 기름 바른 피부, 흰 프린트, 실제 물 | `pfe_hosiery_sheen`; 강도는 독립 선택 |
| back-seam stockings / faux backseam | 뒤꿈치 부근부터 뒤면을 따라 이어지는 선 | 실제 봉제 접합, 맨다리 문신 | `pfe_hosiery_backline` |
| thigh-high stockings / 허벅지형 스타킹 | 무릎 위에서 끝나는 상단 위치 | 실리콘·가터·레이스 유무 | 길이와 지지 방식 분리 |
| hold-ups / stay-ups | 상단 밴드 등을 이용하는 고정 유형 | 모든 thigh-high, 항상 레이스 상단 | 상품 구성 정보; 실제 하중은 픽셀에서 추정하지 않음 |
| lace-top / lace welt | 스타킹 상단에 붙은 레이스 밴드 | 프린트, 단순 밴드, 가터 연결 | `pfe_lace_welt_candidate` |
| plain welt / 단순 상단 밴드 | 상단의 연속된 단순 직물 밴드 | 레이스, 독립 끈, 피부 선 | `pfe_plain_welt_candidate` |
| garter belt / suspender straps | 허리 지지대–끈–스타킹 상단의 연결 | 장식 리본, 어깨 서스펜더 | `pfe_garter_path` |
| sheer-to-waist tights | 허리 영역까지 이어지는 투과 외관 | 별도 보강 상단, 상단이 가려진 사진 | 연구 축; 보이지 않는 상단 구조에 게이트 없음 |
| denier / 데니어 / D | 원사·필라멘트의 선밀도 단위 | 투명도 %, 광택·색·패턴 | 제작 메타데이터; 정확한 D 수치를 픽셀 게이트로 쓰지 않음 |

데니어는 **9,000m의 원사 또는 필라멘트 질량을 g로 표시하는 단위**다. 낮은 수치를 특정 투과 백분율로 변환하지 않는다. 직물 구조, 색, 신장, 조명, 안감은 별도다. [OQLF 용어 자료](https://vitrinelinguistique.oqlf.gouv.qc.ca/fiche-gdt/fiche/17056211/denier)

Wolford의 Backseam Illusion Stay-Up은 뒤 세로선을 knitted-in, faux로 설명한다. 따라서 `back-seam`의 시각 게이트는 **후면의 선이 같은 스타킹 표면에 붙어 이어지는가**이며, 실제로 두 패널을 봉제했는가는 아니다. Individual 10 Stay-Up의 단순 상단 밴드는 thigh-high가 항상 lace-top이라는 대체도 막는다. [뒤 세로선 상품](https://us.wolford.com/en-us/backseam-illusion-stay-up-28161.7005.html), [단순 밴드 상품](https://us.wolford.com/en-us/individual-10-stay-up-21663.7005.html)

## 5. 부분 보임의 다른 방식과 절대영역

| 용어군 | 관찰 대상 또는 관계 | 분리할 축·혼동 경계 | 데이터 반영 |
|---|---|---|---|
| 絶対領域 / zettai ryōiki / 절대영역 | 짧은 밑단과 무릎 위 양말·스타킹 사이의 허벅지 피부 | 다리 사이 배경, 연속된 타이츠, 속옷 천 | `pfe_thigh_skin_band` |
| visible panty line / VPL / 팬티 라인 | 겉옷을 통해 드러나는 안쪽 의복 가장자리 | 속옷 천의 직접 노출, 겉옷 자체 솔기 | `pfe_covered_underlayer_relief`는 불투명 요철 방식만 선택 |
| visible underwear waistband / 이너 허리밴드 | 하의 위로 나온 별도 이너의 상단 | 판치라, 덮인 겉옷의 요철 | 기존 부분 보임 축; 치마 밑단 관계로 승격 없음 |
| visible bra straps / 브라 끈 | 이너에 연결된 별도 끈의 가독성 | 어깨끈 하나로 이너 종류 확정, 목걸이 | 기존 레이어 후보; `pfe_neck_foundation`과 다른 위치 |
| peekaboo detail / 부분 디테일 | 피부·이너·장식 일부를 드러내는 넓은 표현 | 항상 속옷, 항상 가슴골 | broad advisory 유지 |

mixi의 해당 커뮤니티 운영 글은 절대영역을 밑단과 무릎 위 양말 사이의 허벅지 피부로 설명한다. 이는 용어의 실제 사용 근거이며, 그 커뮤니티의 이미지 금지 규칙을 보편적인 용어 정의나 생성 정책으로 가져오지는 않았다. 출처가 성인·비성인 모두의 보편적 사용을 검증하는 것도 아니다. 이 저장소의 새 후보와 프로필은 성인 조건을 별도로 가진다. “황금 비율” 수치·기원·현행 인기·매력 효과는 채택하지 않았다. [커뮤니티 원문](https://mixi.jp/view_bbs.pl?comm_id=44814&id=51046220)

기존 `inner_thigh_negative_space`의 프로젝트 별칭은 **절대공역**, 새 피부 띠의 명칭은 **절대영역**이다. 전자는 두 허벅지 안쪽 사이의 배경 공간이고 후자는 한 다리의 두 의복 경계 사이 피부다. 기존 프로필·별칭은 변경하지 않았다.

Cambridge의 panty line 정의는 옷을 통해 보이는 속옷 가장자리를 뜻한다. 이 넓은 정의에 요철과 투과를 모두 구분 없이 넣지 않는다. Journelle의 피터 설명은 천의 가장자리·부피가 겉옷 위 선을 만드는 방식을 설명한다. 새 프로필은 **불투명한 겉옷의 연속 표면이 안쪽 가장자리를 덮으며 국소 요철을 보이는 방식**으로 한정했다. 관찰되는 요철만으로 속옷의 정확한 형태를 확정하지 않는다. [Cambridge](https://dictionary.cambridge.org/us/dictionary/english/panty-line), [Journelle](https://www.journelle.com/blogs/le-jour/how-to-avoid-visible-panty-lines-the-underwear-guide-from-our-fitters)

## 6. S자 자세와 시점 결합

| 용어군 | 관찰 대상 또는 관계 | 분리할 축·혼동 경계 | 데이터 반영 |
|---|---|---|---|
| S-curve pose / S자 자세 | 연결된 몸 축과 어깨·골반의 완만한 오프셋 | 모래시계 체형, 과도한 허리 굽힘 | `pfe_supported_s_curve_candidate`; 지지 관계 포함 |
| weight shift / hip shift / hip pop | 접지된 체중 이동과 골반 위치 | 실제 체중·외력 추정, 골반 크기 변경 | 기존 `contrapposto_weight_shift` 재사용 |
| torso twist / 몸통 회전 | 어깨와 골반 방향의 차이·연속된 몸통 | 분리된 몸통, 얼굴만의 회전 | `pfe_torso_twist_candidate` |
| arched back / 허리·등의 곡선 | 지정된 굽힘과 연결된 관절 | 항상 S자, 이상적 허리 비례 | 강도는 별도 요청; 자동으로 과장하지 않음 |
| three-quarter / side profile | 몸 방향과 보이는 외곽 | 카메라 높이, 실제 폭·체형 변화 | 기존 방향 후보 |
| extended leg / pointed toes | 다리·발끝의 방향과 관절 연속성 | 실제 다리 길이 증가, 접지 소실 | 기존 포즈 후보; 지지 확인 |
| mini / micro-mini / mini hemline | 실제 밑단 위치·무릎·다리·신발 | 속옷 보임, 로우앵글, 보편 길이 수치 | `pfe_mini_outer_leg`의 외곽 구도 |
| front slit / asymmetric hem | 트임의 위치 또는 밑단 높이 차이 | 옆 트임, 전체 치마 들림 | 별도 의복 구조 축; 기존 side slit 정의 변경 없음 |
| high angle / 하이앵글 | 높은 시점의 얼굴·목선·연결된 목 | 가슴골 보장, 무단 촬영 행동 | 얼굴·쇄골 선택형 조합 |
| low angle / 로우앵글 | 낮은 시점의 바깥 의복·다리 실루엣 | 치마 안쪽 보임, 촬영 동의, 길이 변화 | 미니 외곽 선택형 조합 |

촬영 각도는 의상 구조를 대신하지 않는다. 약한 하이앵글과 열린 목선을 선택해도 가슴골을 강제하지 않으며, 낮은 시점과 미니를 선택해도 이너의 가시성을 요구하지 않는다. 거리와 몸의 가까운·먼 부분, 몸 방향, 렌즈·크롭은 각각 기록한다. 고정 초점거리 하나를 모든 신체 비례의 해결책으로 만들지 않았다. [Canon](https://www.canon-europe.com/get-inspired/tips-and-techniques/portrait-photography-tips/)

PSNI가 설명하는 upskirting/downblousing은 동의 없는 의복 안쪽 촬영이라는 행위를 포함한다. 이를 중립적 카메라 각도의 별칭으로 사용하지 않았다. 이는 해당 기관 안내의 용례 구분이며 보편적인 법률 판단이나 사진만으로 동의를 판정하는 규칙이 아니다. [PSNI](https://www.psni.police.uk/safety-and-support/online-safety/upskirting-and-downblousing)

## 7. 후보팩의 구체적 적용과 검증 경계

새 묶음은 배꼽+얼굴, 불투명 핏+지지된 몸 축, 복부 메쉬+착시 목선, 스타킹 투과+광택, 허벅지 피부 띠+레이스 밴드, 가터 연결+뒤 세로선, 미니+낮은 시점 외곽, 얼굴+높은 시점 목선이다. 모두 선택형이다. 개별 멤버의 가용성과 모든 관련 차원의 개방이 확인될 때만 노출되고, 묶음의 관련 프로필 목록은 자동으로 강한 의무를 만들지 않는다.

특히 스타킹 투과와 광택은 같은 표면에 공존할 수 있지만, 불투명 핏과 메쉬 피부 보임을 동일한 패널에 동시에 요구하지 않는다. 복부 메쉬와 착시 목선의 묶음은 서로 다른 위치의 연결된 패널과 불투명 몸판을 다룬다. 자세로 피부 노출이나 체형 비례를 대체하지 않는다.

새 검증은 완전한 관계·부분 문구·부정·성인 조건, 절대영역/절대공역의 경계, 선택형 조합의 차원 잠금, 실제 인덱스 연결 및 기존 데이터·벡터 보존을 점검한다. 첫 12개 검색 진단의 문구와 기대값은 수정하지 않는다. 추가 분석용 진단은 [추가 검색 진단](addendum_retrieval_probes.json)으로 별도 동결한다. 이들은 작성자가 설계한 개발 진단이며 독립 holdout 또는 픽셀 실현률이 아니다. 최종 실행 결과와 남은 탐색 오탐은 [validation.json](validation.json)에 기록한다.

현재 데이터에서 **집중 검사 12/12, 관련 계약 검사 48/48**, 사전과 두 색인의 검사가 통과했다. 시각 색인은 988개 프로필, 후보 의미 색인은 9,168개 항목이다. 작업 시작 데이터의 960개 시각 항목·9,128개 후보 항목뿐 아니라 첫 조사 완료 시점의 974개·9,146개 항목도 텍스트와 벡터가 모두 동일하다. 첫 조사 프로필 14개와 후보 18개의 내용도 그대로 유지했다. 변경된 코퍼스의 BM25F 통계와 최상위 해시는 재계산했다.

실제 Gemini 벡터를 사용한 검색은 첫 진단의 긍정 6/6, 추가 진단의 긍정 14/14에서 기대 프로필을 발견했고, 총 34개 문장의 새 hard 활성화는 0이다. **선택형 검색의 의미 분리는 아직 충분하지 않다.** 첫 진단의 속치마·쇼츠에서 인접 프로필이 남고, 추가 진단의 부정·인접 사례 8개 모두에서 선택형 인접 검색 결과가 나왔다. 예를 들어 다리 사이 배경에도 피부 띠가, 맨 종아리 문신에도 스타킹 선이, 겉옷 솔기에도 안쪽 가장자리 요철이 선택형으로 검색됐다. `navel orange`는 배꼽 프로필 자체는 제외했지만 다른 의복 프로필이 반환됐다. 이 문장들은 진단을 위해 성인 맥락을 강제로 지정했으며 실제 비인물 요청의 후보 채택 결과로 해석할 수 없다.

따라서 검색, 요청에 따른 채택, 같은 부위의 실제 구현은 각각 다른 판단이다. 부정·소유자·대상 식별을 검색 점수만으로 보장하지 않는다. 이번 결과를 근거로 부정 사례 문구에 맞춘 필터를 추가하거나 기대값을 바꾸지 않았다. 후보 채택 시 완전한 부위·의복·연결 관계를 확인하고, 이미지를 검증할 때 해당 관계의 모든 게이트를 판단해야 한다. 상세 결과는 [추가 진단 결과](addendum_retrieval-results.json)에 남겼다.

픽셀 평가·사용자 미감 판단·SNS 성과 검증은 실시하지 않았다. 기존 전체 회귀의 실패·중단 기록은 첫 조사 스냅샷에 그대로 남기며, 이번 범위 검사 통과를 전체 테스트 통과로 표현하지 않는다. 추가 정의의 품질은 이미지 생성 결과가 해당 소유자·경계·지지·가시성을 실제로 보존하는지에 대한 별도 평가가 필요하다.
