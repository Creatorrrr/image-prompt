# 현실적 배경 표현을 위한 시각 의미와 후보팩 보강 연구

현실적인 배경을 강화하려면 **장소의 구조, 물체의 사용과 지지, 재료의 상태, 광원과 수광면, 카메라가 보여 주는 깊이**를 서로 연결하는 데이터가 필요하다. `realistic`, `RAW`, `lived-in` 같은 표현만 추가하거나 모든 장면에 오염·안개·노이즈를 넣는 방식은 이 관계를 보장하지 않는다. 깨끗한 호텔, 맑고 건조한 거리, 잘 보정된 에디토리얼, 노이즈가 적은 야간 사진도 보강 범위에 포함해야 한다.

우선순위는 배경의 접속 구조와 인물–환경의 일관성, 다음은 요청에 맞는 재료·사용 흔적, 마지막은 선택적인 광학·처리 질감이다. 이 순서는 생성 모델에서 측정한 최적 순위가 아니라, 원하지 않은 스타일 변화와 기존 데이터 중복을 줄이기 위한 설계 판단이다. 구체적인 관찰 조건을 만들되, 이미지가 실제 장소에서 촬영되었거나 특정 장비·RAW 처리 과정을 거쳤다는 사실까지 픽셀로 인증하지 않는다.

참조 대화의 14개 본문 분류와 마지막 핵심어 목록에서 **253개 코드 표기, 중복 제거한 233개 표기**를 보존했다. 이 수에는 긴 예문·설정 조합도 포함되어 있으므로 233개 독립 개념이나 233개 검증된 용어를 뜻하지 않는다. 외부 근거는 **19개 1차·공식 자료**, 결과 데이터는 **37개 시각 관계 제안, 20개 상황별 후보 묶음, 98개 검증 명세**다.

산출물은 **연구 초안**이다. 기존 소스와 로더에 대한 읽기 전용 진단은 수행했지만 신규 데이터를 운영 자산이나 인덱스에 통합하지 않았다. 후보팩 노출·선택, 최종 프롬프트 감사, 이미지 생성·픽셀 평가도 실행하지 않았다. 따라서 이 보고서는 데이터 보강의 근거와 구현 설계이며, 생성 품질 개선을 실증했다는 보고서가 아니다.

## 핵심 판단과 원 대화의 보정

| 원 대화의 표현 | 확인한 경계 | 데이터에 반영할 판단 |
|---|---|---|
| `on-location`, `existing light` | 현장 촬영과 현장광만 사용하는 촬영은 다름 | 장소 표현, 광원 관계, 실제 제작 이력을 분리 |
| `lived-in`, `mundane details` | 생활감과 지저분함은 동일한 요구가 아님 | 지지면·사용 위치·동선을 가진 소품을 선택적으로 제안 |
| `mixed lighting` | 공간별 광원색과 전역 화이트밸런스는 다름 | 광원→지정 수광면→국소 색 영역을 연결 |
| `uneven illumination`, `deep shadows` | 확산광 아래 낮은 대비도 물리적으로 가능 | 광원 크기와 방향에 맞는 명암; 깊은 그림자 강제 금지 |
| `occasional clipped highlights` | 클리핑은 필수 현실감 증거가 아님 | 작은 광원 코어의 허용 여부와 필수 디테일 보존을 분리 |
| `atmospheric haze` | 대기 산란은 거리·매질 조건에 의존 | 맑은 근거리 실내에 전역 안개를 자동 삽입하지 않음 |
| `imperfect reflections` | 반사는 재료·입사 방향·표면 상태에 의존 | 원본·반사면·가림의 기하를 유지; 무작위 왜곡 금지 |
| `focus breathing / imperfect focus` | 초점 이동 중 화각 변화와 정지 영상의 초점 상태는 별개 | 브리딩은 단일 사진의 hard 픽셀 계약에서 제외 |
| `35mm f/4` | 심도는 조리개만으로 결정되지 않음 | 렌즈 수치보다 읽혀야 할 배경 구조를 명시 |
| `sensor noise`, `film grain` | 디지털 노이즈와 필름 입자의 원인이 다름 | 매체별 선택 효과; 노이즈 없는 사진도 허용 |
| `HDR` 회피 | HDR 범위·표시와 과도한 톤 매핑을 구분해야 함 | `HDR` 자체를 금지하지 않고 후광·톤 평준화 같은 결과를 다룸 |
| `RAW`, `unretouched`, `unstaged` | 파일·작업·사건의 이력과 시각적 인상은 다름 | 스타일을 설명하되 실제 제작 사실을 인증하지 않음 |

Nikon의 용어집은 available/existing light를 현장에 존재하는 광원으로 설명하며 자연광만으로 한정하지 않는다. ARRI도 조명 장비를 이용한 현장 촬영과 스튜디오 제작을 함께 다룬다. 따라서 `on-location`을 `no artificial fill light`로 자동 변환할 수 없다. 실제 촬영에서는 화면 밖 광원도 가능하므로 “광원과 결과가 양립한다”와 “광원 자체가 화면 안에 보인다”는 서로 다른 계약이다. [S01](https://www.nikonusa.com/learn-and-explore/photography-glossary), [S17](https://www.arri.com/en/learn-help/lighting/lighting-handbook)

Sony가 정의하는 focus breathing은 초점 변화에 수반되는 화각 변화다. 단일 프레임에서는 그 변화 자체를 비교할 수 없으므로 `slight focus breathing`을 자연스러운 정지 사진의 필수 효과로 채택하지 않는다. 대신 요청에 따라 초점면·거리별 흐림·피사체 움직임을 별도 관계로 표현한다. [S05](https://helpguide.sony.net/di-app/cb/v1/en/Content/Lens_breathing.htm)

Adobe의 HDR 설명은 장면·파일의 밝기 범위, SDR로의 톤 매핑, HDR 디스플레이 표현을 구분한다. `HDR`라는 단어 자체와 과도한 국소 대비·윤곽 후광·그림자 평준화는 동의어가 아니다. `cinematic`, `editorial`, `pristine` 역시 요청 미감이나 상태일 수 있으므로 전역 금지어 목록에 넣지 않는다. 이런 단어가 특정 생성 모델에서 어떤 영향을 주는지는 별도 비교 실험으로 확인해야 한다. [S14](https://blog.adobe.com/en/publish/2023/10/10/hdr-explained)

## 현실감의 데이터 단위

현실감 요청을 처리하는 가장 작은 단위는 형용사가 아니라 **대상과 조건이 지정된 관계**다. 예를 들어 `weathered surface`는 벽, 유리, 금속, 의상 중 어디를 가리키는지 확정하지 못한다. `a faint runoff mark begins below the drain outlet`은 대상 부위와 위치 관계를 고정하므로 다른 표면의 얼룩으로 대체했는지 판정할 수 있다. 그 흔적의 실제 원인을 진단하는 것과 그림에서 선택한 원인–결과 관계를 표현하는 것은 구별한다.

| 필드 | 보존할 내용 | 예시 |
|---|---|---|
| owner | 효과를 받아야 하는 정확한 대상 | 창에 가까운 흰 소매 |
| scope | 효과가 존재하는 공간·표면 범위 | 소매에서 초록 벽을 향한 작은 면 |
| prerequisite | 성립을 위해 먼저 필요한 조건 | 유색 벽이 가깝고 해당 소매가 보임 |
| relation | 대상 사이의 연결 | 벽→반사광→소매 |
| visible components | 한 이미지에서 관찰할 필수 요소 | 근접 벽, 국소 색 영향, 다른 면의 원래 색 |
| confusion boundary | 비슷해 보여도 다른 경우 | 의상 배색, 전역 색보정, 다른 소매의 초록색 |
| evidence scope | 출처가 실제로 뒷받침하는 범위 | 반사 물리 원리; 이 프롬프트의 효과는 미검증 |
| verification | 구현·픽셀의 독립된 결과 | 노출 미실행, 픽셀 미실행, 사용자 판단 대기 |

`source_ids`가 있다고 해서 출처가 해당 프롬프트나 합격 기준을 제시했다는 뜻은 아니다. 연구 데이터의 각 항목은 근거의 지원 범위를 함께 가진다. 생활 소품 배치, 설비 배치, 바람 반응, 물체 밀도, 쿠션 지지, 식생 접속의 6개 항목은 직접 실증 근거가 없는 설계 가설로 분리했다. 이들은 관찰 가능한 초안이지만 통계적 성능 사실이나 자동 강제 규칙으로 승격하면 안 된다.

## 표현 계열별 상세 연구

### 장소 구조와 생활 정보

`existing architecture`, `found environment`, `ordinary surroundings`는 장소를 선택하는 방향을 제공하지만 그 장소의 사실성을 입증하지 않는다. 데이터에서는 문틀의 두께, 문턱과 바닥의 연속, 설비와 벽의 부착, 통행 가능한 경로처럼 그림 안에서 확인할 수 있는 연결을 먼저 다룬다. 특정 건축 유형의 실제 시공 규정이나 도시의 전형을 정의하는 항목은 아니다.

`incidental background details`를 “무의미한 물건을 무작위로 추가”하는 규칙으로 구현하면 물체 수는 늘어도 장면의 기능은 흐려질 수 있다. 제안하는 방식은 공간의 주제와 직접 관련되지 않아도 사용 위치가 납득되는 작은 요소를 선택하는 것이다. 예를 들어 출입문 손잡이, 바닥에 맞물린 배수구, 손이 닿는 탁자 위 컵은 각각 접속·배치 조건을 가진다. 실제 생성에서 도움이 되는지는 아직 시험하지 않았으므로 후보는 선택적이어야 한다.

서울 주택가 예시의 배관·실외기·전선·스쿠터·쓰레기봉투는 지역의 보편적 필수 요소로 만들지 않는다. 같은 도시에도 신축 건물, 정리된 골목, 차량 없는 보행로, 시대별 설비 차이가 있다. 이번 후보는 **서울 주택가를 참고한 가상 공간**으로 사용할 수 있을 뿐, 특정 장소의 재현이나 지역 사진 분포에 근거한 빈도 추정은 아니다. 실제 주소가 있는 장소를 재현할 때는 해당 시점의 현장 자료가 추가로 필요하다.

생활 흔적은 공간의 경제적 상태를 자동으로 설명하지 않는다. `lived-in`은 사용 흔적에 대한 미감 요청으로 남기고, 쓰레기·곰팡이·방치·빈곤으로 묶지 않는다. 반대로 정돈된 집은 소품이 적더라도 의자·작업면·동선의 관계를 통해 사용 가능한 공간으로 표현할 수 있다.

### 마모·변색·보수와 시간의 흔적

`minor scratches`, `scuffed metal`, `maintenance traces`는 강도가 아니라 **어디에 어떤 변화가 생겼는지**가 먼저다. 금속 손잡이의 잡는 부위, 벤치의 닿는 모서리, 한 부분만 다시 칠한 벽처럼 owner를 좁힌 후보를 만든다. 전체에 동일한 스크래치 텍스처를 덮는 방식은 서로 다른 재료와 사용 위치를 지우므로 혼동 사례로 둔다.

NPS의 Stonehaus 사례는 수분 이동, 석재·모르타르의 성질, 보수 재료가 국소 열화와 관련됨을 보여 준다. 이 사례는 아이오와 사암 건물에 관한 것이며 일반 도시 벽의 모든 변색 원인이나 서울 건물의 상태를 설명하지 않는다. 데이터에는 아래와 위, 출구와 흐름, 패치와 기존 면처럼 확인 가능한 위치 관계만 참고한다. 사진의 얼룩으로 실제 구조 안전성이나 누수 원인을 진단하지 않는다. [S10](https://www.nps.gov/articles/this-masonry-is-for-the-bees.htm)

Columbia CAVE의 TVBRDF 자료는 페인트 건조, 젖은 시멘트·직물의 건조, 먼지 축적처럼 시간에 따른 표면 반사 변화를 측정한 연구 데이터다. 이를 참고하면 `age marks`를 나이 하나로 결정하는 대신 재료와 변화 상태를 나누는 것이 타당하다. 다만 이번 연구는 원본 측정 데이터 전체를 재분석하지 않았다. 젖은 표면은 항상 어둡고 낡은 금속은 항상 주황색이라는 규칙을 만들 근거로 사용하지 않는다. [S11](https://www.cs.columbia.edu/CAVE/databases/tvbrdf/about.php)

### 표면 반사와 재질 차이

PBR 문헌의 미세면 모델은 눈에 분리되어 보이지 않는 작은 표면 방향 분포가 반사 양상에 영향을 준다는 점을 설명한다. 따라서 `micro-scratches`를 썼다는 이유로 원경 벽의 모든 작은 흠집을 과장해서 그릴 필요가 없다. 재료의 차이는 하이라이트 폭, 반사의 방향성, 투과 여부 등 더 큰 영상 특징으로 드러날 수도 있다. [S06](https://www.pbr-book.org/4ed/Reflection_Models/Roughness_Using_Microfacet_Theory)

유리는 항상 약한 반사만 가져야 하는 것이 아니다. 반사와 투과는 입사 조건·재료에 의존하며, 완벽하게 매끈한 유리도 현실에 존재할 수 있다. 제안하는 계약은 “불완전한 반사”라는 형용사 대신 반사 원본, 유리 면, 창틀, 뒤 공간을 분리하여 서로 모순되지 않게 표현하는 것이다. 유리 표면의 작은 지문을 선택하더라도 유리 전체를 뿌옇게 덮어 투과 구조를 없애지 않는다. [S07](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission)

젖은 보도는 원본 광원과 수면의 기하를 중심으로 기존 wet-surface 계약을 재사용할 수 있다. 반사가 반드시 들어가야 하는 실험에서는 원본과 젖은 면을 함께 보이게 하여 평가하기 쉽게 만든다. 일반적인 실제 사진의 모든 반사 원본이 반드시 프레임 안에 있어야 한다는 의미는 아니다. 원본이 화면 밖에 있으면 기하적 모순은 검토할 수 있어도 정확한 owner 검증은 제한된다.

### 현장광·혼합광·그림자의 연결

혼합광의 핵심은 서로 다른 색이 있다는 사실보다 어디에서 어떤 면에 영향을 주는지다. Nikon의 화이트밸런스 비교는 같은 장면도 설정에 따라 색 표현이 달라질 수 있음을 보여 준다. 연구 데이터는 창 쪽 흰 소매, 램프에 가까운 탁자, 그 사이 전이 구역을 구분하고, 전역 청록·주황 그레이드나 옷 자체의 배색을 혼합광 증거로 대체하지 않도록 한다. [S02](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/setting-white-balance)

광원의 겉보기 크기와 수광면·가림 물체의 배치는 그림자 경계를 바꾼다. 큰 면광원은 넓은 반그림자를 만들 수 있고 작은 광원은 더 선명한 경계를 만들 수 있다. 따라서 `realistic shadows`의 hard 규칙을 “항상 깊고 선명한 그림자”로 설정하면 흐린 낮 사진을 오판하게 된다. [S09](https://pbr-book.org/4ed/Light_Sources/Area_Lights)

접촉 그림자는 발 밑에 검은 띠를 추가하는 과제가 아니다. 보이는 지지 발의 밑창과 바닥이 만나고, 그 주변 어둠이 조명 조건과 양립하는지를 함께 본다. 허리 위 프레임에서는 발이 없으므로 이 계약을 통과시킬 수 없다. 허리 위 구도를 유지해야 한다면 손–탁자 접촉이나 어깨–벽의 근접광 같은 다른 관계를 선택해야 한다.

공통 광원 아래 그림자가 반드시 서로 평행해야 하는 것도 아니다. 가까운 점광원은 위치에 따라 다른 투영 방향을 만들 수 있으며, 여러 광원은 여러 그림자를 만들 수 있다. `shared_cast_shadow`는 선택된 장면의 광원 기하와 양립하는지를 요구한다. 움직이는 그림자가 깊이 지각에 영향을 준 Kersten 등의 실험은 관계를 연구할 배경 근거지만, 정지 생성 이미지의 현실감 향상률을 입증하지는 않는다. 이번에는 공개 초록만 확인했다. [S18](https://journals.sagepub.com/doi/10.1068/p260171)

### 노출·톤 응답과 배경 정보

`natural exposure`를 고정된 히스토그램으로 바꿀 수는 없다. 실제 사진에는 저대비 흐린 날, 강한 역광, 밝은 실내, 야간 장면이 모두 있으므로 보존할 대상과 밝기 위계를 먼저 선택한다. 눈·의상·건축 구조가 필수라면 작은 반사 코어의 클리핑 허용과 그 필수 영역의 디테일 보존을 별개로 기록해야 한다.

`natural highlight roll-off`는 기존 톤 응답 관계와 중복된다. 기존 항목을 재사용하되, `slight underexposure`나 `clipping`을 현실감 패키지의 의무로 추가하지 않는다. 현실적인 배경이면서 동시에 의상 정보를 읽어야 하는 에디토리얼에서는 어두운 배경과 적절한 보조광이 양립할 수 있다. 장면의 밝기 위계가 유지되는지와 사용된 촬영 장비를 분리한다.

### 대기 원근·기하 원근·심도

대기 산란은 매질을 통과하는 빛을 감쇠시키고 방향을 바꾼다. 장거리 원경의 대비 감소를 표현하는 근거가 되지만, 모든 원경을 동일한 청회색으로 만들거나 카메라 앞부터 배경까지 똑같은 뿌연 막을 덮으라는 뜻은 아니다. 거리·조명·입자 조건이 다르면 효과도 달라진다. 짧은 실내 거리에서는 가림·상대 크기·초점 차이가 더 적절한 후보일 수 있다. [S08](https://www.pbr-book.org/4ed/Volume_Scattering)

기하 원근과 렌즈의 배럴 왜곡도 나눈다. ZEISS의 기술 자료는 중심 원근과 직선이 휘는 광학 왜곡을 별도로 설명한다. 후보 데이터에서는 바닥 선의 수렴과 문들의 상대 크기를 우선 다루고, 배럴 왜곡·색수차·비네트는 선택 요청으로 남긴다. 광각 사진이 반드시 휜 벽이나 늘어난 몸을 보여야 한다는 의무를 만들지 않는다. [S04](https://lenspire.zeiss.com/photo/app/uploads/2022/02/technical-article-distortion.pdf)

Canon의 심도 설명은 초점거리, 조리개, 초점·촬영 거리, 배경 거리의 관련성을 제시한다. `35mm f/4`나 `50mm f/2.8`만으로 환경이 읽히는지 판단할 수 없다. 같은 수치의 요청에도 “중경의 출입문과 보도 경계가 식별된다”처럼 최종 영상 목표를 덧붙이는 편이 검증 가능하다. 이미 잠긴 85mm f/1.4 요청은 유지하고, 필요하면 빛·접촉으로 배경과의 합성 느낌을 줄이는 후보를 선택한다. [S03](https://www.usa.canon.com/pro/rf-lens-world/features/depth-of-field)

### 프레이밍·동작과 통합

`foreground occlusion`, `casual composition`은 전체 구도의 정밀함을 없애라는 뜻으로 구현하지 않는다. 프레임 가장자리에 실제 크기와 깊이를 가진 물체가 일부 들어오고, 뒤 물체를 일관되게 가리며, 요청한 얼굴·손·상품 디테일을 침범하지 않게 한다. 촬영자가 완벽히 계산했는지 여부는 그 구도에서 인증할 수 없다.

셔터 시간은 움직임을 정지시키거나 번짐으로 표현하는 데 관계한다. 그러나 `handheld` 자체는 흔들린 사진을 보장하지 않으며, 약한 모션 블러와 얕은 심도는 서로 다른 현상이다. 제안하는 motion 후보는 움직이는 부위와 정지 구조를 분리하고 물체·관절의 연결을 유지한다. [S19](https://www.usa.canon.com/pro/rf-lens-world/features/aperture)

“같은 바람”은 유용할 수 있는 장면 가설이지만 모든 잎·머리카락·의상이 동일 각도로 움직여야 한다는 뜻은 아니다. 고정점, 강성, 관성, 국소적인 가림이 다르므로 서로 양립하는 반응이라는 수준으로 유지한다. 이번 연구에서는 이 관계의 현실감 효과에 대한 직접 실증 자료를 확보하지 않았고, 바람 속도나 시간적 동기화를 단일 이미지로 판정하지 않는다.

### 노이즈·필름 입자·후보정

Adobe는 명도 노이즈와 색 노이즈, JPEG 블록·후광을 구분한다. 현실감 데이터 역시 벽의 실제 표면 결, 캡처 노이즈, 압축 흔적을 하나의 `texture`로 합치지 않아야 한다. 어두운 면의 작은 명도 변동을 선택할 수 있지만 맑은 저감도 사진이나 깨끗한 계산사진에 이를 강제하면 원래 요청을 훼손한다. [S12](https://helpx.adobe.com/photoshop/using/correcting-image-distortion-noise.html)

Kodak은 흑백의 은 입자와 컬러의 염료 형성에 따른 graininess를 구분하여 설명한다. 필름의 불규칙 입자를 표현할 수는 있어도 결과 영상의 입자로 실제 촬영 매체를 인증할 수는 없다. 필름 grain, 디지털 luminance noise, chroma noise, 스캔·압축 결함은 별도의 원인과 선택 조건을 유지한다. [S13](https://www.kodak.com/content/products-brochures/Film/kodak-essential-reference-guide-for-filmmakers.pdf)

RAW 데이터는 표시할 때 해석·처리를 거치며, 작업 설정과 프리뷰는 구별된다. `minimally processed RAW photograph`는 제한적인 처리 인상을 요청하는 말로 받아들일 수 있지만 실제 RAW 파일이나 무보정 이력을 뜻하는 증거는 아니다. `restrained_processing`은 과도한 윤곽 후광과 뭉개짐 없이 톤·재질 경계를 보존하는 결과를 다룬다. [S15](https://helpx.adobe.com/be_en/camera-raw/desktop/get-started/overview-and-setup/introduction-camera-raw.html)

다큐멘터리도 비슷한 경계가 필요하다. World Press Photo의 기준에는 연출, 캡션, 제작 과정의 투명성처럼 영상 바깥의 정보가 포함된다. `documentary style`을 한 장의 생성물에서 표현하는 것과 실제 사건의 기록을 인증하는 것은 구분해야 한다. 거친 외모·옷·노이즈를 다큐멘터리의 필수 외형으로 만들지 않는다. [S16](https://www.worldpressphoto.org/contest/code-of-ethics)

## 현재 데이터의 재사용과 보강 위치

현재 소스 로더에서 읽힌 시각 프로필은 **587개**, 메인 파일만의 프로필은 **333개**다. 관련 레코드 32개를 파일 경로·JSON pointer와 함께 보존했고, 사용한 authored 파일들의 SHA-256과 git HEAD도 기록했다. 메인 파일만 검색한 결과를 전체 데이터라고 간주하지 않았다. 조사 시점에는 모델·에디토리얼 확장이 로더에 포함되어 있었다.

| 현재 항목 | 확인한 범위 | 제안 |
|---|---|---|
| `lived_in_clutter` | 생활 소품이 있는 공간 조건 | 공간 사용·소품 지지·비어 있는 동선을 선택적 관계로 보강 |
| `documentary_real_person` | unpolished real-person presence | 인물 외모와 배경의 사실적 구조를 자동 결합하지 않음 |
| `photographic_grain_present` | film 또는 sensor grain을 함께 표기 | 매체별 원인·선택성 분리; 호환성 유지 여부는 구현 때 검토 |
| `lit_practical_motivated_mixed_interior` | 보이는 practical에 따른 혼합 실내광 | 광원–수광면 색 구역의 후보로 재사용 |
| `lit_practical_warm_cool_spatial_zones` | 따뜻한·차가운 광원의 공간 분리 | 색보정·표면 고유색과의 혼동 사례 추가 |
| `shallow_depth_focus_falloff_relation` | 선명면 전후의 연속적 흐림 | 재사용; 중경 가독성을 무조건 hard gate로 덧붙이지 않음 |
| `three_plane_depth_chain` | 전경·중경·후경의 연결 | 구조 깊이 표현 재사용; 세 물체의 목록으로 대체 금지 |
| `highlight_rolloff_tone_response` | 밝은 면의 점진적 톤 응답 | 재사용; 클리핑은 필수화하지 않음 |
| `hard_light_shadow_edge_relation`, `soft_light_shadow_edge_relation` | 광원 크기와 그림자 경계 | 인물·환경의 공유 조건을 추가하되 기존 의미를 유지 |
| `window_seat_daylight_activity_relation` | 창·좌석·손 행동·진행 흔적을 포함 | 일반 창광 사진에 사용 행동까지 강제하지 않음 |
| `wet_surface_light_reflection_owner_relation` | 원본·젖은 면·경계·가림의 연결 | 진단 가능한 반사 장면에서 재사용 |
| `computational_low_light_multiframe_look` | 낮은 노이즈와 야간 디테일 | “밤에는 노이즈 필수”의 반례로 보존 |
| `mep_environment_relation` | 이야기와 관련된 인물–환경 행동 | 현실 배경의 모든 인물에게 서사 행동 강제 금지 |

22개 표현의 deterministic exact 진단에서 좁은 기존 표현인 `shallow-depth focus-falloff relation`, `three-plane depth-chain relation`은 각각 해당 hard 프로필로 연결됐다. `현실적인 배경`, `available light`, `mixed lighting`, `HDR`, `서울 주택가` 등 넓은 표현은 이번 exact hard 필터에서 연결되지 않았다. **이는 의미 검색이나 v6 후보팩에서 관련 후보가 전혀 나오지 않는다는 결과가 아니다.** broad label에 좁은 시각 의무가 자동 부여되지 않는 경계는 보존할 가치가 있다.

37개 제안 중 기존 ID 연결이 있는 항목은 재사용 후보이지 무조건 기존 프로필에 병합할 항목이 아니다. 특히 창가 행동, 환경 에디토리얼, 얕은 심도는 원래 계약에 별도의 전제조건이 있다. `realistic background` 하나를 exact alias로 붙여 이 계약들을 일괄 활성화하면 원하지 않은 행동·구도·초점이 생성될 수 있다.

## 후보팩 데이터 설계

새 데이터는 단일 “현실감 코어” 장문보다 작은 선택 단위로 제공한다. 후보팩은 장소 구조, 재료 응답, 광원 관계, 배경 가독성 등 서로 다른 역할의 후보를 보여 주고, 요청의 잠긴 차원을 존중한다. 연구 묶음의 `required_if_this_bundle_is_explicitly_selected`는 해당 예시를 명시적으로 선택했을 때의 관계 목록이며, 단순 현실감 요청의 전역 필수값이 아니다.

권장 결합 절차는 다음과 같다. 이 절차와 수량은 구현 설계안이며 입증된 최적 파라미터가 아니다.

1. 원 요청에서 장소·시간·날씨·매체·구도·인물·의상과 유지할 조건을 먼저 정한다.
2. 배경이 인공적으로 느껴지는 구체 문제를 연결 구조, 재료, 광원, 접촉, 초점, 처리 중에서 선택한다.
3. 처음에는 주된 문제의 관계 1개와 보조 관계 1–2개를 조합하여 과도한 조건 누적을 줄인다.
4. 그 관계를 평가할 owner가 보이지 않으면 후보를 바꾸거나 검증 불가로 남긴다. 이미 잠긴 구도를 임의로 바꾸지 않는다.
5. 후보 검색·노출·채택 이력과 최종 프롬프트에 들어간 문구를 각각 기록한다.

| 상황별 후보 | 중심 관계 | 추가 효과의 조건 |
|---|---|---|
| 낮 카페 창가 | 창→실내 밝기, 사용 소품, 배경 가독성 | 유리 손잡이 번짐과 전경 가림은 선택 |
| 가상 서울 주택가 | 건축 접속, 설비 부착, 깊이 | 보수 흔적은 해당 상태를 허용할 때 |
| 흐린 날 공원 | 식생 접속, 확산광, 발 지지 | 안개·필름 입자를 기본으로 넣지 않음 |
| 깨끗한 고급 호텔 | 정돈된 구조, 재료별 응답, 유리 | 먼지·균열 없이도 평가 가능 |
| 야간 점포 | practical의 조명 영역, 혼합광, 밝기 위계 | 젖은 바닥·노이즈는 별도 선택 |
| 비가 그친 보도 | 젖음 경계, 반사 원본, 발 접촉 | 침수나 폭우로 자동 확장하지 않음 |
| 건조한 맑은 거리 | 원근 구조, 하드광, 청결 | 물웅덩이·헤이즈를 넣지 않음 |
| 환경 에디토리얼 | 배경 구조, 가독성, 공통 광원 | 포즈·의상·영화적 미감을 보존 |
| 얕은 심도 유지 | 가림 경계의 초점, 지지, 근접 조명 | 카메라 조건을 f/4로 바꾸지 않음 |
| 필름적 현장 사진 | 구조, 밝기 위계, 선택 grain | 실제 필름이라는 이력은 주장하지 않음 |

전체 20개 묶음에는 블루아워, 원경 도시, 정리된 집, 작업실, 주야간 정류장, 바람의 정원, 청결한 진료 공간, 유리 출입문도 포함되어 있다. 영어 예문은 관계를 보여 주기 위한 창작 예시다. 특정 도시·시설의 실재 모습이나 특정 생성 모델의 최적 프롬프트를 복제한 자료가 아니다.

## 구현 순서와 데이터 경계

**1차 반영은 재사용과 중복 제거를 중심으로 한다.** 현재의 depth, light, wet-surface, color owner 관계에 연결하고, 생활감·그레인 등의 넓은 항목은 기존 호환성을 보면서 선택 조건을 추가한다. 새 데이터 파일을 만든다면 현재 확장 형식과 실제 로더 계약에 맞게 연구 필드를 변환해야 한다. 연구 JSON을 assets에 복사했다고 후보팩이 이를 읽는 것은 아니다.

**2차 반영은 부족한 공간 관계를 좁게 추가한다.** 건축 접속, 접촉 부위 마모, 보수 패치, 재료 응답 차이, 일반 창광 깊이, 환경 가독성 등을 후보화한다. 새 exact alias는 충분히 구체적인 표현으로 한정하고, 일반적인 `realistic`, `natural`, `documentary`, `Seoul`은 advisory 검색어로 유지한다. 표면·조명·카메라의 원인을 서로 다른 차원으로 저장하되, 새 최상위 intent enum을 임의로 만들지는 않는다.

**3차 반영은 조건부 효과와 가설을 시험한다.** 헤이즈, 노이즈, 필름 입자, 비네트, 색수차, 바람 반응은 장면과 요청에 맞을 때만 노출한다. “깨끗함”, “건조함”, “바람 없음”, “노이즈 없음” 같은 조건과 충돌하면 제외한다. 직접 실증 근거가 없는 6개 관계는 수동 장면 검토를 먼저 하고, broad query로 hard 활성화하지 않는다.

인덱스 갱신 뒤에도 실제 v6 실행에서 슬롯·묶음이 노출되는지 별도로 확인해야 한다. 인덱스에 레코드가 있는 것, resolver가 hit를 내는 것, 후보팩에 들어가는 것, 작성자가 선택하는 것, 렌더에서 관계가 보이는 것은 서로 다른 결과다. 소스 변경 전후 비교에는 source hash, pack ID, intent lock hash, 선택 항목, 최종 문구를 연결해야 한다.

## 검증 설계

98개 검증 명세는 37개 관계 각각의 positive·near-miss 74개와, broad query·구도·날씨·매체·owner 충돌을 다루는 24개 경계 사례로 구성했다. 명세의 `expected`는 향후 검사할 기대값이며 실행 결과가 아니다. 현재 실행한 검사는 연구 파일의 구조·참조·개수와 기존 프로필의 exact 진단이다.

| 검증 단계 | 통과에 필요한 증거 | 이번 상태 |
|---|---|---|
| 출처·설계 | 출처와 주장 범위, 가설 표시, 혼동 경계 | 작성·연결 확인 |
| authored 구조 | ID 충돌 없음, 참조 유효, 기존 연결 식별 | 연구 파일 검사 |
| exact 기존 동작 | 입력과 실제 resolver 결과 | 22개 진단 실행 |
| 신규 인덱스·노출 | 신규 source hash와 실제 후보팩의 항목 | 미실행 |
| 선택·프롬프트 | 선택 목록, 유지할 의도, 감사 결과 | 미실행 |
| 픽셀 | 같은 이미지의 같은 owner에서 필수 요소 관찰 | 미실행 |
| 품질 향상 | 대조군과 반복 표본의 비교 | 미실행 |
| 사용자 미감 | 선호·의도 만족에 대한 판단 | 대기 |

초기 비교 실험은 8개 장면군×4개 조건×3회 반복의 **96장 파일럿**으로 설계할 수 있다. 이는 이번에 생성한 이미지 수가 아니며, 충분한 통계 검정력을 보장하는 표본 수 역시 아니다. 장면군은 청결한 호텔, 건조한 낮, 흐린 공원, 낮 카페, 야간 점포, 젖은 보도, 원경 도시, 얕은 심도 에디토리얼로 나누어 “오염을 넣을수록 좋다”는 편향을 견제한다.

| 조건 | 목적 |
|---|---|
| A: 현재 데이터 | 구현 전 기준 결과 |
| B: 일반 현실감 키워드 | 라벨 추가만의 효과 |
| C: 이번 관계 데이터 | 대상·조건·관계의 효과 |
| D: 무차별 효과 누적 | 노이즈·오염·헤이즈 누적의 부작용 점검 |

비교에서는 모델·버전·크기·참조·원래 인물/의상/장소 의도를 고정한다. 시드 고정이 가능한 모델에서는 반복별 시드를 짝지을 수 있지만, 시드 고정 불가를 동일 난수 조건처럼 보고하지 않는다. 프롬프트 길이·정보량·추가 객체 수가 결과를 설명할 수 있으므로 B와 C의 길이를 가능한 한 맞추고, 남는 차이는 기록한다. 관계 하나만 추가·제거하는 후속 ablation이 인과 판단에 더 직접적이다.

평가는 이름과 프롬프트를 가린 이미지로 진행한다. 축소 화면에서는 장소·깊이·인물 통합을 보고, 원본 크기에서는 유리 경계, 접점, 마모의 owner, 노이즈와 재질 결을 확인한다. 관찰하지 못한 영역은 `unscored`로 두고, 필수 요소가 일부만 보이면 `partial_is_fail`로 처리한다. 서로 다른 이미지에서 성공한 부분을 모아 한 장의 성공으로 계산하지 않는다.

관계 충족률, 유지해야 할 의도의 위반률, 기술적 결함률, 주관적 현실감과 미적 선호는 분리한다. 관계가 읽혀도 의상이 바뀌면 전체 요청 성공으로 볼 수 없고, 모든 구조 검사에 통과해도 사람이 보기에 더 좋은지는 별도 질문이다. 이미지를 다시 만들면 원래 시도와 사유를 보존하여 좋은 결과만 선택한 효과를 줄인다.

## 산출물과 해석 범위

| 파일 | 용도 |
|---|---|
| `source-conversation.json` | 참조 대화와 원래 예문의 출처 경계 |
| `keyword-inventory.json`, `core-keyword-map.json` | 253회 표기·233개 고유 표기의 보존·분류와 핵심 20개 용어의 개별 관계 매핑 |
| `sources.json` | 19개 자료의 제목·기관/저자·날짜·URL·근거·한계 |
| `visual-proposals.json`, `visual-catalog.md` | 37개 시각 관계의 구조화 데이터와 상세 설명 |
| `candidate-bundles.json` | 선택 가능한 20개 상황 조합과 영어 예문 |
| `evaluation-cases.jsonl` | 98개 향후 검증 명세 |
| `repo-audit.json`, `audit_repository.py` | 현재 authored 데이터와 exact 진단의 재현 근거 |
| `integration-plan.json` | 단계별 보강 위치와 구현 게이트 |
| `validation.json`, `validate_research.py` | 연구 산출물 무결성 검사 결과 |

키워드 목록의 대부분은 **원문 분류 수준의 연구 경로**로 연결되어 있으며, 모두 개별 exact alias로 심사·등록된 것은 아니다. 전체 표기를 빠짐없이 보존한 사실과 개별 용어의 실증 검증을 구분한다. 37개 관계의 조건과 혼동 경계가 실제 보강 단위이며, 다음 구현에서는 이 단위별로 노출·선택·픽셀을 검증해야 한다.

이번 자료는 사진·광학·표면·표현 계약 중심의 연구다. 원 대화의 “특정 단어가 훨씬 효과적이다”라는 생성 성능 주장을 검증한 논문은 확보하지 않았다. 서울의 지역별 배경 사진 분포, 보수 흔적의 실제 빈도, 각 생성 모델의 단어별 반응, 사용자 선호도는 미확인으로 남긴다. 오래된 기술 문헌은 안정적인 원리나 역사적 사례에 한정하고 현재 제품의 기능·성능을 설명하는 자료로 확대하지 않았다.

## 출처

아래 자료의 정확한 지원 범위와 확인 위치는 `sources.json`에 보존했다. S18은 공개 초록, S17은 안내 페이지, S11은 데이터베이스 설명을 확인한 것으로 전체 논문·PDF·측정 데이터의 재분석과 구별한다.

1. [S01](https://www.nikonusa.com/learn-and-explore/photography-glossary) Nikon. *Photography Glossary — Existing Light*. 게시일 미확인. 확인 위치: Existing Light entry.
2. [S02](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/setting-white-balance) Lindsay Silverman / Nikon. *Setting White Balance*. 게시일 미확인. 확인 위치: mixed-light comparison captions.
3. [S03](https://www.usa.canon.com/pro/rf-lens-world/features/depth-of-field) Canon. *Depth of Field*. 게시일 미확인. 확인 위치: Basic Features of Lenses / Depth of Field.
4. [S04](https://lenspire.zeiss.com/photo/app/uploads/2022/02/technical-article-distortion.pdf) B. Hönlinger and H. H. Nasse / Carl Zeiss. *Distortion*. 2009-10. 확인 위치: PDF pp. 1–4; central perspective and curved lines.
5. [S05](https://helpguide.sony.net/di-app/cb/v1/en/Content/Lens_breathing.htm) Sony. *Lens breathing compensation*. 게시일 미확인. 확인 위치: definition.
6. [S06](https://www.pbr-book.org/4ed/Reflection_Models/Roughness_Using_Microfacet_Theory) Matt Pharr, Wenzel Jakob, Greg Humphreys. *Roughness Using Microfacet Theory*. 2023. 확인 위치: 9.6 opening and Figure 9.20.
7. [S07](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission) Matt Pharr, Wenzel Jakob, Greg Humphreys. *Specular Reflection and Transmission*. 2023. 확인 위치: 9.3 physical principles / Fresnel.
8. [S08](https://www.pbr-book.org/4ed/Volume_Scattering) Matt Pharr, Wenzel Jakob, Greg Humphreys. *Volume Scattering*. 2023. 확인 위치: 11 introduction.
9. [S09](https://pbr-book.org/4ed/Light_Sources/Area_Lights) Matt Pharr, Wenzel Jakob, Greg Humphreys. *Area Lights*. 2023. 확인 위치: 12.4 / Figure 12.15.
10. [S10](https://www.nps.gov/articles/this-masonry-is-for-the-bees.htm) Mark Chavez / National Park Service. *This Masonry is for the Bees!*. 2007. 확인 위치: Stonehaus case; rising damp and efflorescence.
11. [S11](https://www.cs.columbia.edu/CAVE/databases/tvbrdf/about.php) Columbia University CAVE. *Time-Varying BRDF Database — About*. 2007 (page footer: 06/03/2007). 확인 위치: acquisition and measured phenomena.
12. [S12](https://helpx.adobe.com/photoshop/using/correcting-image-distortion-noise.html) Adobe. *Correct image distortion and noise*. 2023-05-24. 확인 위치: Reduce image noise and JPEG artifacts.
13. [S13](https://www.kodak.com/content/products-brochures/Film/kodak-essential-reference-guide-for-filmmakers.pdf) Kodak. *The Essential Reference Guide for Filmmakers*. 게시일 미확인. 확인 위치: printed pp. 54–55; PDF indexes 55–56.
14. [S14](https://blog.adobe.com/en/publish/2023/10/10/hdr-explained) Eric Chan / Adobe. *High Dynamic Range Explained*. 2023-10-10. 확인 위치: dynamic range, tone mapping, HDR displays.
15. [S15](https://helpx.adobe.com/be_en/camera-raw/desktop/get-started/overview-and-setup/introduction-camera-raw.html) Adobe. *Introduction to Camera Raw*. 2026-08-31. 확인 위치: raw processing and preview.
16. [S16](https://www.worldpressphoto.org/contest/code-of-ethics) World Press Photo. *2026 Contest code of ethics*. 2026. 확인 위치: items on staging, captions and transparency.
17. [S17](https://www.arri.com/en/learn-help/lighting/lighting-handbook) ARRI. *Lighting handbook*. 2020-02-19 (English handbook listing). 확인 위치: on-location and studio scope.
18. [S18](https://journals.sagepub.com/doi/10.1068/p260171) Daniel Kersten, Pascal Mamassian, David C. Knill. *Moving Cast Shadows Induce Apparent Motion in Depth*. 1997-02. 확인 위치: abstract; DOI 10.1068/p260171.
19. [S19](https://www.usa.canon.com/pro/rf-lens-world/features/aperture) Canon. *Aperture and Shutter Speed*. 게시일 미확인. 확인 위치: Basic Features of Lenses; moving subject and blur.
