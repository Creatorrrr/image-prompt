# 궁전·고성·성채 시각 의미 데이터 강화 연구

현재 후보팩을 강화할 때 가장 가치가 큰 추가 단위는 **건축 부품의 이름이 아니라, 그 부품들이 한 장소에서 어떻게 연결되는지 설명하는 시각 관계**다. 낙하문은 격자가 출입구의 수직 홈 안에 놓이는 관계이고, 도개교는 교량판이 문턱을 축으로 움직여 도랑 횡단을 제어하는 관계다. 앙필라드는 여러 방을 통과하는 문들의 정렬이며, 거울 회랑은 실제 개구부와 반사면의 대응이다. 이런 차이를 보존해야 서로 다른 장소가 모두 ‘웅장한 돌벽과 금색 장식’으로 수렴하는 문제를 줄일 수 있다.

연구 결과는 34개 구조·공간 프로필 제안, 68개 후보 문장, 34개 선택형 묶음 제안, 102개 관찰 기준, 84개 검증 사례로 구체화했다. 이 수량은 연구 범위의 크기를 나타내며 품질 개선의 실증 결과가 아니다. 후보 문장과 카메라 구성, 관찰 기준은 출처의 건축 사실을 바탕으로 설계한 제안이다. 현재 상태는 `proposed`이며 실행 데이터 등록이나 생성 이미지 평가는 포함하지 않는다.

연구의 중심 범위는 참조 대화와 동일하게 유럽의 중세부터 20세기 초까지다. 이베리아의 나스르 궁전, 발트해권 벽돌 성곽, 베네치아 수변 궁전, 근세 포병 요새를 포함한다. 미국 국립공원관리청의 스페인계 요새 자료는 유럽 외 지역으로 범위를 확장하기 위한 것이 아니라 라블랭·해자·사면의 연결을 명확히 설명하는 비교 자료로 사용한다. 한국·중국·일본의 궁궐과 산성은 별도의 지역 연구 없이 이 분류로 대체하지 않는다.

## 1. 현재 데이터의 공백과 보강 지점

원본 자산 JSON을 직접 조사한 결과 `castle_armory_hall`, `palace_side_gate`, `palace_ceremonial_courtyard`, `ruined_palace_wing`, `palace_garden_modern` 같은 장소 항목은 이미 존재한다. 조선 궁궐과 내정 관련 항목도 있으며, 로코코는 일부 펑크 의상 후보의 설명에 나타난다. 그러나 이번 ID·명칭·별칭·활성화 필드 검색에서는 `enfilade`, `portcullis`, `machicolation`, `bastion`, `drawbridge`, `concentric`를 명시한 전용 항목을 찾지 못했다. 이는 기록한 필드의 어휘 범위에 대한 결과이며, 모든 설명 문장의 의미나 생성 모델의 능력 전체가 부재한다는 주장은 아니다.

|현재 단위|문제 또는 확인할 위험|권장 보강|
|---|---|---|
|성의 무기고, 궁전의 옆문|장소명만으로 벽·문·동선이 불명확|문루–통로–경비실, 거주동–마당 등 연결 문장|
|폐궁의 한 동|폐허가 표면의 이끼·어둠으로 축소될 가능성|지붕 소실–벽 상단–노출 하늘–남은 바닥 관계|
|현대 궁전 정원|파르테르·보스케·오랑주리의 역할이 미분화|낮은 구획 / 둘러싸인 야외 방 / 계절적 식물 보호 공간|
|로코코 의상·펑크 후보|건축 양식 요청이 의상 또는 펑크로 오염될 위험|장식의 소유 대상을 벽 패널·문틀·거울로 명시|
|다른 지역의 궁정 데이터|‘궁전’ 하나로 동아시아·유럽 공간이 혼합될 위험|지역은 요청 또는 출처로 제한하고 건물 명칭만으로 전이하지 않음|
|선택형 후보 묶음 체계|등록됐어도 공개 후보팩에 노출되지 않을 수 있음|등록·노출·선택·최종 문장 반영을 각각 확인|

현재 `photo_candidate_semantics.py`의 묶음 컴파일은 원본 행 해시, 후보 ID와 슬롯, 구성요소, 프로필 참조를 검사한다. 따라서 연구용 `source_ids`, `historical_scope`, `claim_limits`를 실행 묶음에 그대로 넣는 방식은 적절하지 않다. 역사 출처와 한계는 연구 자료에 남기고, 실행 허용 필드로 변환할 때 후보의 긍정적 시각 문장과 구조 관계만 내보내야 한다. 실행 원본과 생성된 인덱스의 소유권도 분리한다.

## 2. 하나의 ‘중세풍’ 태그로 합치지 말아야 할 축

하나의 건물은 여러 역할과 여러 시기를 동시에 가질 수 있다. 성의 주탑에는 거주실이 들어갈 수 있고, 문루도 거주·행정 공간을 포함할 수 있다. 주탑이 없는 성곽 유형도 존재하므로 `castle`이 입력됐다는 이유만으로 주탑을 필수화하면 오히려 사실성이 떨어진다. Getty의 keep 범위 설명과 Historic England의 성곽 유형 설명을 함께 읽는 것이 단일 부품 목록보다 유용하다.[^S10][^S02]

권장 의미 모델은 다음과 같다. 아래 필드는 연구 모델이며 기존 런타임에 이미 지원된다는 뜻은 아니다.

|축|값의 예|보존해야 할 차이|
|---|---|---|
|`building_function`|방어 거주, 왕실 의례, 군사 주둔, 도시 방어, 공연·사교|castle / palace / fortress / walled town / opera house|
|`built_period`|건립·증축·실내 개조 시기|외관 양식으로 건립 연도를 확정하지 않음|
|`represented_style`|노르만, 고딕, 르네상스, 바로크, 로코코, 신고전주의, 역사주의|‘중세를 재현한 19세기 건물’을 표현 가능|
|`regional_context`|잉글랜드, 웨일스, 발트해권, 베네치아, 나스르 그라나다 등|넓은 지역을 단일 형태로 축약하지 않음|
|`spatial_system`|중첩 방어선, 문루 접근, 방의 축선, 중정과 회랑|부분들의 포함·접속·분리 관계|
|`material_finish`|다듬은 석재, 불규칙 돌쌓기, 벽돌, 목재 패널, 회반죽, 금박|재료·마감·색·노후 상태 분리|
|`site_state`|사용 중, 비어 있음, 부분 붕괴, 보존 유적, 복원, 미완성|낡음·비어 있음·버려짐·파손은 다른 상태|
|`reference_state`|현존 사진, 복원 실내, 박물관 조합실, 역사 도면, 창작|참조가 증명하는 범위 기록|
|`capture_context`|현대 관광 사진, 역사 장면의 재현 촬영, 건축 기록, 판타지 편집|건물 시대와 촬영 시대 분리|
|`visibility`|전체 배치, 실내 관계, 국부 접합, 표면|카메라가 실제로 증명할 수 있는 범위|

노이슈반슈타인은 중세의 형태를 재조합한 역사주의 건물이다. 공식 관리기관도 이를 기존 중세 성의 복사본으로 설명하지 않는다. 카르카손의 현재 형태에는 19세기 복원이 중요하게 작용했고, 말보르크도 여러 차례 복원되었다. 따라서 현재 사진을 ‘당시 그대로’의 근거로 취급하지 않도록 출처 상태를 보존해야 한다.[^S31][^S08][^S09]

보마리스의 낮은 실루엣은 일부 구조가 계획 높이까지 완성되지 않은 역사와 연결된다. 낮거나 덜 완성된 탑을 무조건 파괴된 탑으로 해석하는 것은 부정확하다. 같은 시각 특징이 `unfinished`와 `ruined`라는 서로 다른 상태로 설명될 수 있으므로, 원인·상태 판단에는 별도 출처가 필요하다.[^S04]

## 3. 건물 유형과 시대·지역 분류

### 3.1 명칭과 관찰 가능한 모습

`Castle`은 방어와 거주의 결합을 조사하는 출발점이고, `palace`는 의례·접견·생활의 공간 연계를 조사하는 출발점이다. `fortress`와 `fort`는 군사적 방어 체계를 중심으로, `citadel`은 도시나 더 큰 방어체계 속 핵심 거점을 중심으로 문맥을 살펴야 한다. `stronghold`는 형태가 고정된 건축 유형으로 삼기보다 장소의 성격을 표현하는 상위 개념으로 남기는 편이 낫다. 성과 궁전을 배타적 분류로 만들 필요는 없다.[^S02][^S06][^S11]

프랑스어 `château`, 독일어 `Burg/Schloss`, 이탈리아어 `castello/palazzo`, 스페인어 `castillo/palacio/alcázar`는 검색 확대용으로 보존하되, 서로 완전한 동의어로 정규화하지 않는다. 이름만으로 군사성·왕실 소유·중세 건립을 결정하지 않고, 각 건물의 출처와 구조를 함께 사용한다. 이 연구에서는 언어권별 사전의 전체 의미 범위를 검증하지 않았으므로 이러한 명칭은 검색 단계의 보조 어휘다.

`manor house`, `country house`, `stately home`, `summer palace`, `pleasure palace`, `hunting lodge`는 부유한 실내라는 공통 시각 인상만으로 합치지 않는다. 실제 법적 지위·소유자·용도는 건물의 사진만으로 확정되지 않는다. 아말리엔부르크처럼 작은 사냥·유희 별궁이 정교한 실내를 가질 수도 있으므로 규모가 작다는 이유로 궁정 공간에서 제외해서도 안 된다.[^S19]

### 3.2 시대·지역을 화면의 차이로 바꾸는 방법

|범주|참고할 구성|오인 방지|
|---|---|---|
|노르만·초기 성곽|둔덕과 하부 구획, 석조 주탑의 체적|모든 초기 성이 목조·모든 노르만 건물이 같은 평면은 아님|
|중세 후기 성곽|중첩 방어선, 성문과 외곽 구획|원형 동심원이나 주탑의 존재를 강제하지 않음|
|고딕 공간|첨두 개구부, 리브와 지지부의 연결|어둠·공포·검은색을 양식 정의로 사용하지 않음|
|튜더 대홀|목조 지붕 구조, 홀과 직물·생활 영역|해머빔을 모든 중세 홀의 기본 천장으로 사용하지 않음|
|르네상스 궁정|중정, 층별 질서, 계단과 거주동 관계|첨탑이 있어도 중세 군사 성이라는 결론으로 가지 않음|
|바로크 궁정|의례 공간의 연속, 회화·대리석·장식의 결합|모든 천장화를 프레스코라 부르지 않음|
|로코코 실내|패널·개구부·곡선 조각을 한 장식 체계로|금박·파스텔·방 전체 비대칭을 필요조건으로 두지 않음|
|신고전주의|벽·천장·가구를 연결하는 고전 모티프|흰색 기둥 하나 또는 무장식 실내로 축약하지 않음|
|역사주의·중세 부흥|중세 인용과 후대 건립의 공존|고딕 리바이벌과 모든 역사주의를 동의어로 합치지 않음|
|발트해권 벽돌 성|벽돌의 구조적 반복과 개구부|붉은 필터만으로 벽돌·말보르크 판정 금지|
|베네치아 궁전|수변과 층별 개구부, 복합 건축 시기|고딕=대성당 자동 연결 금지|
|나스르 궁전|중정·회랑·수반·수로와 입체 장식|무카르나스·사자 분수·십자 수로를 모든 건물에 강제하지 않음|
|근세 포병 요새|능보의 돌출, 외보의 분리, 포대·도랑|별 모양 지붕이나 뾰족한 성탑으로 대체하지 않음|

이 표는 유럽 전체에 통용되는 연대표가 아니라 데이터 분해를 위한 분류다. 실제 시대 범위와 복합성은 지역·건물별로 확인해야 한다. 대표 근거는 English Heritage의 발전사, Met의 고딕 해설, 햄프턴코트의 대홀, 샹보르·베르사유·아말리엔부르크의 공식 해설, V&A의 Adam 연구다.[^S03][^S14][^S13][^S21][^S15][^S19][^S25]

## 4. 우선 보강할 시각 관계

### 4.1 방어 건축: 물체가 아니라 연결 체계

**문루·바비칸·낙하문·도개교**는 모두 ‘성문 장식’으로 합쳐지기 쉽다. 문루는 통로를 포함하는 건물, 바비칸은 접근을 강화하는 외곽 방어시설, 낙하문은 출입구의 격자 차단물, 도개교는 도랑을 건너는 가동 교량으로 구분한다. 실제 건물마다 모든 요소가 함께 존재하지는 않는다. 던스턴버러의 바비칸은 기초만 남아 전체 형태를 복원하기 어렵다는 공식 설명이 있어, 단어를 안다는 이유만으로 특정 유적의 소실부를 확정해서는 안 된다.[^S01][^S12]

낙하문 후보에는 `vertical grooves`, 도개교 후보에는 `hinge at the threshold`, 바비칸 후보에는 `outer enclosure → approach → main gatehouse`의 관계를 넣는다. 이것들은 생성 결과를 구별하기 위한 연구 설계다. 도개교는 이 연구의 첫 프로필에서 한쪽 경첩형을 선택했으며, 다른 작동 방식까지 잘못 배제하지 않도록 범위를 명시했다.

**성벽·탑·보행로·성가퀴**는 서로 다른 부품으로 저장하되 조합 시 연결이 유지돼야 한다. 커튼월은 현대 유리 외벽이라는 다른 뜻도 있으므로 성곽 문맥이 필요하다. 성가퀴는 높은 실체와 열린 틈의 교대로 표현하고, 보행로는 방벽 뒤의 바닥으로 표현한다. 요철만 있는 장식 난간도 존재할 수 있으므로 이 형태를 실제 방어 기능의 충분조건으로 삼지는 않는다.[^S01][^S02]

**마시쿨레이션과 murder hole**은 위치가 다르다. 전자는 바깥으로 돌출된 석조 방벽 아래쪽을 보도록 구성하고, 후자는 문 통로의 천장 구멍을 조사하는 별도 개념이다. 라글란성의 돌출부는 전자의 실재 사례다. ‘구멍을 통해 무엇을 떨어뜨렸다’는 설명보다 돌출체·받침·바닥 개구부의 소유 관계가 이미지 데이터에 더 직접적이다.[^S05][^S01]

**중첩 성곽과 성곽도시**도 구별해야 한다. 중첩 성곽은 한 성의 안팎 방어선 관계이고, 성곽도시는 성벽 안에 도시 가로·주택·공공 또는 종교 시설이 들어 있는 관계다. 전자는 포함 구조를, 후자는 도시 조직을 보여주는 구도가 필요하다. 탑을 여러 개 배치했다는 이유만으로 어느 쪽도 충족되지 않는다.[^S04][^S08]

### 4.2 포병 요새: 돌출과 분리를 구별

능보는 주 방어선에 연결된 돌출부로, 라블랭은 본체 앞에 분리된 외보로 시각화하는 것이 유용하다. ‘별 모양’이라는 실루엣만으로는 어느 부분이 어떤 역할인지 드러나지 않는다. NPS의 설명은 도랑·외보·엄폐 통로·글라시가 서로 어떤 위치에 놓이는지를 보여주므로 관계 모델의 비교 근거가 된다. 이 배치를 보방 요새 전체에 하나의 고정 평면으로 적용하지 않는다.[^S07][^S33][^S06]

초기 후보 묶음은 두 종류로 나눈다. 첫째는 높은 사선 시점에서 능보·외보·도랑을 함께 보여주는 전체 배치, 둘째는 포가대·포신·방벽 개구부·작업 바닥을 보여주는 포대의 국부 관계다. 전경 사진 한 장에 멀리 있는 포가대 세부까지 필수로 요구하지 않는다. 카메라 거리와 증거 크기를 맞추는 것이 키워드 수를 늘리는 것보다 중요하다.

### 4.3 궁전 실내: 축선과 반사, 공적·사적 공간

앙필라드의 핵심은 여러 방과 정렬된 출입구다. 복도 양옆에 문이 늘어선 장면이나 거울이 만들어낸 무한 공간은 대체물이 아니다. 베르사유의 공식 설명은 왕의 공식 아파트와 디아나 살롱의 앙필라드 맥락을 제공하고, 문 정렬의 일반 정의는 별도의 용어 자료로 교차 확인했다. 연구 초안의 ‘세 문턱’은 가시성을 높이기 위한 시험 구성이지 역사적 최소 개수가 아니다.[^S15][^S17][^S18]

거울 회랑은 실제 창, 거울 표면, 반사된 창의 대응을 보존해야 한다. 베르사유 거울의 방은 창과 마주보는 거울들의 배치를 명확히 설명한다. 이를 참고한 일반 후보에는 정확한 거울 개수나 왕실 문장까지 넣지 않는다. 특정 장소의 복원을 요구할 때만 세부 수량·구획·장식을 추가한다.[^S16]

공식 아파트, 접견실, 전실, 살롱, 사적 내실, 침실, 무도회장은 모두 금박으로 구별되는 것이 아니다. 의례가 진행되는 방의 연결, 진입 전 대기 공간, 좌석의 배치, 통행 폭, 침대와 휘장처럼 용도에 맞는 관계를 조사해야 한다. 왕실 침실의 공개 의례처럼 현대의 공적·사적 구분과 다른 관행도 있어, 이름만으로 사람이 없어야 하거나 침실이어야 한다고 고정하지 않는다.[^S15]

### 4.4 계단·창·천장: 구조와 관찰 위치

샹보르 이중 나선계단은 비어 있는 중심부 둘레에 두 경로가 감기는 구성이다. 두 갈래가 한 계단참으로 모이는 대계단이나 단일 나선계단과 구별해야 한다. 공식 설명은 두 경로를 이용하는 사람들이 서로 볼 수 있지만 마주치지 않는다는 관계를 설명한다. 외관의 탑 실루엣만으로 내부의 이중 경로가 검증되었다고 할 수는 없다.[^S21]

깊은 창가 좌석은 창 앞 의자가 아니라 벽 깊이 안에 자리 잡은 좌석을 중심으로 구성한다. 인물의 상반신을 크게 찍으면 벽 두께가 사라질 수 있으므로 얼굴 초상과 창가 구조 검증은 별도 요구다. 창을 보는 사람의 행동은 선택 가능하며, 사람 없는 건축 사진에도 이 프로필을 사용할 수 있어야 한다.[^S12]

리브 볼트는 천장에 그어진 줄무늬가 아니라 지지부로 이어지는 입체 구조로 표현한다. 해머빔 홀은 노출 목재 구조와 아래 홀의 공간을 함께 보여준다. 공중 부벽·장미창·거대한 유색창을 성곽 전체의 기본 요소로 사용하지 않는다. 고딕 성당의 구조를 설명하는 자료를 성의 모든 방으로 옮기는 것은 범주 오류다.[^S14][^S13]

## 5. 장식·재료·정원·상태의 데이터 설계

### 5.1 로코코와 바로크를 색상으로 분류하지 않기

로코코 후보는 장식이 붙는 곳을 명시해야 한다. `boiserie`는 벽 패널에, `rocaille`와 곡선·식물 조각은 패널이나 거울 프레임에, 반사는 실제 거울에 속한다. ‘황금빛 화려한 공간’이라는 전역 문장만으로는 이 관계를 유지하기 어렵다. 아말리엔부르크의 공식 자료가 설명하는 전체 실내 구성과, Palais Paar 보아즈리의 재료·개조 이력을 함께 참고할 수 있다.[^S19][^S20]

Palais Paar의 박물관 실내는 적어도 두 방에서 온 요소를 합친 것이며, 도료 분석은 원래 서로 다른 회색 계열을 보여준다. 이는 로코코를 파스텔 분홍·금색 또는 원형 그대로의 한 방으로 고정하면 안 된다는 직접적인 반례다. 원위치 건물 사진, 이전된 부재, 박물관 재구성은 같은 증거 유형이 아니다.[^S20]

베르사유 헤라클레스 살롱의 천장화는 캔버스를 천장에 붙이는 방식으로 설명된다. 따라서 `painted ceiling`을 모두 `fresco`로 정규화해서는 안 된다. 마찬가지로 대리석처럼 보이는 표면, 실제 석재, 수리된 충전부의 구별은 확대 이미지와 재료 기록이 필요하다. 일반 후보는 확인 가능한 패널·줄눈·광택 관계까지만 약속하는 편이 적절하다.[^S15][^S17]

### 5.2 재료·표면·상태·상징의 독립성

다듬은 돌쌓기는 줄눈과 정형 블록으로, 불규칙 돌쌓기는 서로 다른 돌 윤곽과 접합으로 기술한다. `rubble masonry`를 붕괴 잔해로 번역하면 사용 중인 건물도 폐허로 바뀔 수 있다. 줄눈·표면 요철·도장·습윤·식생은 별도 속성이며, 표면이 거칠다는 이유로 건축 연대나 암석 종류를 확정하지 않는다.[^S30]

태피스트리, 벨벳, 다마스크, 브로케이드, 침대 휘장, 콘솔 테이블, 조각 궤, 촛대 등은 기존 소품 슬롯과 재사용 가능성을 먼저 확인한다. 건축 후보가 이런 목록을 한꺼번에 삽입하지 않도록, 장면의 기능을 구별하는 소품 1–2개를 선택하는 설계를 권한다. 개별 직물 조직·가구 양식의 연대 판별은 이번 연구보다 더 좁은 박물관 객체 조사가 필요하다. 따라서 이 어휘들은 전용 hard profile보다 보조 조합 어휘로 남긴다.

가문 문장·백합·튜더 장미·전리품 장식은 시각적으로 나타날 수 있지만, 무명 인물의 신분이나 실제 건물의 소유자를 확정하는 단서로 쓰지 않는다. 특정 왕조·장소의 재현에서는 올바른 도안과 시기를 따로 검증한다. 일반 궁전 후보에서는 임의의 실존 문장을 추가하지 않아도 건축 관계가 읽히도록 구성한다.

### 5.3 정원은 하나의 녹색 배경이 아니다

파르테르는 낮은 구획과 길이 만드는 지면 패턴, 보스케는 녹지 벽 안에 형성된 작은 야외 공간, 오랑주리는 식물을 계절에 따라 보호·배치하는 공간으로 연구한다. 같은 정원 안에 모두 있을 수 있으므로 서로 배타적인 스타일로 만들지는 않는다. 베르사유 자료는 보스케의 형태가 시기별로 바뀌었으며 오랑주리의 식물 배치도 계절에 따라 달라진다는 점을 설명한다.[^S26][^S27]

`orangery`를 모든 면이 유리인 온실로 고정하면 베르사유의 두꺼운 벽과 갤러리형 공간을 놓친다. 반대로 이 사례를 모든 오랑주리의 필수 형태로 일반화해서도 안 된다. 연구 초안은 ‘베르사유형 석조 월동 갤러리’라는 사례 범위를 유지한다. 겨울 실내 보관과 여름 야외 진열을 한 프레임에 동시에 필수화하지 않는다.[^S26]

그로토는 자연동굴뿐 아니라 정원에 조성한 인공 동굴을 가리킬 수 있다. 스투어헤드의 등재 기록은 재료, 조성된 방, 개구부, 수경 장치를 구체적으로 기록한다. 바위처럼 보이는 표면과 그 뒤의 설계된 공간을 함께 보여주는 후보가 적절하다. 정원의 인공 폐허 역시 실제 성의 붕괴와 분리해야 하며, 건축 이력 없이 사진만으로 구분하기 어려운 경우는 남겨둔다.[^S28]

### 5.4 나스르 궁전: 평면 장식과 수리 구조를 분리

나스르 중정에서는 중심 수반, 연결 수로, 주변 회랑과 방의 접속이 중요한 조합이다. 무카르나스는 별 모양 평면 타일이 아니라 여러 셀의 깊이와 층이 드러나는 입체 구조로 따로 다룬다. 알람브라 두 자매의 방 자료는 천장과 타일 기단, 작은 분수에서 사자의 중정으로 이어지는 수로를 설명한다.[^S22][^S23]

사자의 중정 원래 바닥에 관해서는 포장과 낮은 정원이라는 해석 차이가 공식 설명에 남아 있다. ‘역사적으로 정확한 원형’ 프롬프트에는 확인되지 않은 바닥 상태를 넣지 않는다. 또한 모든 나스르 궁전에 동일한 동물상이나 수로 평면을 요구하지 않는다. 기관의 개별 건축물 설명과 일반화된 생성용 장면의 경계를 유지한다.[^S22]

### 5.5 풍경·날씨·분위기는 가변 축

언덕·절벽·호수·섬·숲은 입지, 안개·비·눈은 환경, 담쟁이·이끼·장미는 식생, 지붕 소실·벽체 붕괴는 구조 상태다. ‘고성’이라는 단어만으로 이들 속성을 묶어 활성화하지 않는다. 안개가 핵심 구조를 가리면 미적 효과가 좋아도 구조 프로필의 가시성은 충족되지 않을 수 있다.

`regal`, `majestic`, `gothic romance`, `enchanted`, `faded grandeur` 같은 말은 요청의 정서를 유지하는 보조 앵커로 남길 수 있다. 다만 왕실 혈통·실제 쇠락 원인·종교적 용도를 판정하는 시각 증거로 사용하지 않는다. ‘장엄함’을 구현하는 촬영 제안은 큰 공간 대비 인물 크기, 반복 기둥, 축선, 원근 같은 관찰 가능한 제어로 연결한다. 이는 창작 설계이며 역사 자료의 사실 진술과 구별된다.

## 6. 참조 대화의 키워드 처리표

아래 표는 원 대화의 아홉 영역을 빠짐없이 연구 설계에 연결한다. 이 표에 이름이 있다는 사실만으로 각 용어의 지역별 역사 전체가 검증된 것은 아니다. 상세 구조가 정의된 항목은 `profile-matrix.md`, 보조 어휘는 아래 보류 조건을 따른다.

|영역|보존할 키워드|데이터 처리|
|---|---|---|
|건물·장소 유형|castle, historic castle, palace, fortress, fort, citadel, stronghold, fortifications, walled city, manor house, stately home, country house, summer/pleasure palace, hunting lodge, ruins|용도·지역·상태 축 분리. 지역어 château/palais/Burg/Schloss/castello/palazzo/castillo/palacio/alcázar는 검색 보조|
|시대·양식|Romanesque, Norman, medieval, Gothic, Tudor, Elizabethan, Renaissance, Baroque, Rococo, Neoclassical, Gothic Revival, historicism|연대 범위는 사례별. Brick Gothic, Venetian Gothic, Nasrid, bastioned fort를 독립 지역·구조 갈래로 유지|
|전체 배치·탑|keep, great tower, donjon, bailey, ward, motte-and-bailey, concentric, quadrangular, round/drum tower, mural/flanking tower, watchtower, turret|주탑·구획·중첩·연결 프로필 우선. quadrangular와 탑별 세부 계통은 후속 보조 후보|
|성벽·출입|curtain wall, rampart, wall walk, battlement, crenellation, merlon, crenel, gatehouse, portcullis, barbican, drawbridge, moat, dry moat, arrow slit, loophole, machicolation, palisade|실체/빈틈, 상하 이동/회전, 포함/접속으로 분해. murder hole을 혼동 경계에 추가|
|포병 요새|bastion, bastioned fort, star fort, battery, gunport, embrasure|ravelin, glacis, covered way를 연결 어휘로 보강. 상세 전술 성능 주장은 범위 밖|
|아치·창|round/pointed arch, arcade, blind arcade, lancet, rose window, tracery, trefoil, quatrefoil, stained glass, mullion, deep recess, window seat|개구부와 벽면 장식 분리. religious-context 없는 성에 rose window 자동 삽입 금지|
|천장·계단·지붕|barrel/ribbed vault, hammerbeam/exposed timber roof, dome, cupola, painted ceiling, buttress, flying buttress, spiral/double-helix/grand staircase, spire, conical roof, gable, dormer, lantern|입체 지지·경로를 우선. 지붕 실루엣만으로 실내 구조 판정 금지|
|성의 생활 공간|great hall, chapel, keep chamber, bedchamber, private chamber, hearth, courtyard, inner ward, guardroom, armoury|군사시설만이 아닌 거주·식사·예배·일의 맥락. kitchen, bakehouse, stores, stables, workshops, well은 생활 지원 조사축|
|궁정 실내|state apartments, audience chamber, throne room, antechamber, salon, cabinet, ballroom, long/picture gallery, mirror gallery, enfilade, royal bedchamber, landing|공식/사적 용도는 자료로 확인. 금박이나 왕좌 하나로 유형 판정 금지|
|재료·장식|ashlar/rubble masonry, brick, marble, oak/carved panelling, boiserie, gilding, gilded/antique bronze, stucco, bas-relief, foliage, mural, ceiling painting|기질·마감·문양·노후 상태 독립. 석재 종·제작기법은 확인한 범위만|
|상징·직물·소품|coat of arms, banner, fleur-de-lis, Tudor rose, garland/swag, rocaille, C/S-scroll, cartouche, trophy of arms, tapestry, velvet, damask, brocade, bed hangings, drapery, four-poster bed, banquet table, bench, chest, mirror, console, candlestick, candelabrum, sconce, candle chandelier|기존 슬롯 재사용 우선. 개별 객체 연대는 후속 조사, 전역 시대 필터로 단정하지 않음|
|정원|formal garden, parterre, topiary, bosquet, hedge maze, orangery, grotto, landscape garden, fountain/basin, canal/channel, terrace/balustrade, pavilion|지면 구획·공간 둘러쌈·계절 보호·수로 연결. 유지관리·계절·개조 시기 별도|
|입지·상태|hilltop, clifftop, rocky ridge, lakeside, moated, island, woodland, mist, snow, frozen moat, frost, roofless hall, collapsed tower, broken stair, ivy, moss, roses, rain-soaked paving, puddles|입지/날씨/식생/파손 독립; 구성요소를 가리는 정도 평가|
|인접 장소|abbey, monastery, cloister, chapter house, cathedral, royal chapel, medieval street, opera house, foyer, garden folly, hermitage|별도 용도 유지. 회랑 아치만으로 수도원·왕궁 확정 금지. 수도원 세부 기능은 후속 전용 연구|
|분위기·장면|regal, majestic, ceremonial, solemn, elegant, refined, fairytale, enchanted, dreamlike, gothic romance, brooding, mysterious, forgotten, abandoned, faded grandeur, isolated, imposing, sacred, contemplative, ethereal|요청에서 온 정서 앵커로만 사용. 건축 구조와 역사적 사실을 대체하지 않음|

## 7. 후보팩으로 옮길 때의 구체적인 설계

### 7.1 프로필, 후보, 묶음의 역할

34개 연구 프로필은 같은 수준의 역사적 유형 목록이 아니다. 전체 성곽 배치, 문 작동 구조, 특정 실내 관계, 재료 마감처럼 서로 다른 관찰 규모를 의도적으로 나눴다. 각 프로필에 대상 규모와 범위를 남기고, 하나의 장면에서 전부 충족하도록 합치지 않는다. P0는 다음 단계에서 먼저 구별 능력을 검증할 우선순위이며 이미 검증됐다는 뜻이 아니다.

각 프로필에는 두 후보를 작성했다. `location`은 실제 구조 관계를 표현하고, `composition`은 그 관계를 볼 수 있는 카메라 위치를 제안한다. 벽·도개교·능보 같은 고정 건축물을 인물이 들고 있는 `prop`로 잘못 배치하지 않기 위한 선택이다. 필요하다면 후속 구현에서 재료·공간 상태를 기존 슬롯으로 분리하되, 단순 후보 수 증가를 목적으로 문장을 복제하지 않는다.

예를 들어 `pf_portcullis_location`의 영어 문장은 “a heavy gridded gate partly lowered within vertical side grooves inside a fortified entrance”이다. 대응 구도는 격자 가장자리와 가이드 홈을 동시에 보여주는 사선 시점이다. 긍정 문장은 그릴·개구부·수직 홈의 관계만 서술한다. ‘옆으로 여는 철문이 아니다’와 같은 반례는 혼동 경계에 저장하며 검색용 긍정 텍스트에 섞지 않는다.

`pf_enfilade_location`은 방들의 문이 한 시선축에 정렬된 문장이고, 구도 후보는 문턱과 벽 돌아감을 보도록 한다. `pf_mirror_gallery`는 맞은편 창과 거울의 대응을 따로 정의한다. 둘 다 긴 원근감이 있지만 물리적 생성 원리가 다르므로 하나의 “endless palace corridor” 후보로 합치면 안 된다.

### 7.2 활성화와 사용자 의도 보존

명시적으로 정확한 의미의 `portcullis` 또는 `enfilade`를 요구한 경우에는 해당 구조가 요청의 일부다. 반면 `castle`, `palace`, `medieval`, `luxury`, `gothic romance`처럼 넓은 단어만으로 특정 부품 전체를 hard-activate해서는 안 된다. 부정문, 인용된 문장, 문장 무늬의 그림, 일반 동사 `keep`, 현대 유리 `curtain wall`도 구분해야 한다.

검색 유사도와 후보 선택은 구성 제안에만 쓰고, 독립된 요청 증거 없이 필수 프로필로 승격하지 않는다. 사용자 정의가 사전 정의보다 구체적이면 그 정의를 우선한다. 판타지 혼합을 명시한 요청은 혼합을 보존하고 ‘역사적으로 사실’이라는 주장만 분리한다. 현대 관광객 요청의 옷을 중세 의상으로 바꾸거나 사람 없는 전경에 인물을 추가하는 것은 강화가 아니다.

카메라 제안 역시 요청의 크롭을 덮어쓰지 않는다. 타이트한 얼굴 초상에서는 성곽 전체 배치가 검증 불가능할 수 있으며, 그때는 구조 증거의 한계를 기록해야 한다. 초상을 억지로 드론 전경으로 바꿔 프로필을 통과시키는 설계는 피한다.

### 7.3 실행 반영 순서

1. 연구 데이터에서 채택할 P0 구조와 의미 범위를 확정한다. 상세 출처가 부족한 보조 어휘는 계속 선택형으로 둔다.
2. 현재 허용 스키마에 맞는 원본 extension과 registry 항목으로 변환한다. 연구용 필드를 그대로 주입하지 않는다.
3. 후보 ID·슬롯·태그·프로필 참조를 검사하고 원본 해시에 묶어 선택형 번들을 컴파일한다.
4. 파생 인덱스를 갱신한 뒤 공개 v6 후보팩에서 실제 후보 ID와 관계 텍스트가 노출되는지 확인한다.
5. 요청 의도에 맞는 선택과 최종 프롬프트의 구조 관계 보존을 검사한다.
6. 고정한 조건으로 이미지를 생성하고 원본 픽셀을 평가한다. 구조 체크 통과를 이미지 개선으로 보고하지 않는다.

이번 초안은 2번 이후를 실행하지 않았다. 해시가 존재하는 연구 스냅샷과 런타임에 승인된 해시 계약도 구별한다. 문서에 `source_ids`가 있다는 것만으로 공개 후보팩에 출처 연결이나 구조 보존이 자동으로 구현되는 것은 아니다.

## 8. 검증 계획과 충분한 보강의 기준

### 8.1 어휘 수가 아닌 구별 능력

충분한 보강의 기준은 동의어 수가 아니다. 첫째, 낙하문/도개교, 중첩 성/성곽도시, 앙필라드/거울 회랑, 로카유 패널/일반 금박, 능보/분리 외보, 실제 폐허/인공 그로토 같은 주요 혼동쌍이 구별돼야 한다. 둘째, 밝기·날씨·인물 유무가 달라져도 그 관계가 유지돼야 한다. 셋째, 다른 요청에서 불필요한 시대·의상·왕좌·문장을 추가하지 않아야 한다.

|증거 단계|무엇을 확인하는가|무엇을 증명하지 못하는가|
|---|---|---|
|연구 자료 정합성|ID·출처·검증 기준 연결|역사적 완전성이나 생성 품질|
|스키마·컴파일|현재 코드가 원본을 수용하고 참조가 유효함|공개 후보 노출|
|후보 노출|의도한 ID와 구성 문장이 후보팩에 있음|선택되었다는 사실|
|후보 선택|해당 후보가 선택돼 사용 경로에 들어감|최종 프롬프트 반영|
|문장 반영|핵심 구조 관계가 최종 텍스트에 남음|생성 모델의 실행 충실도|
|생성 전달|이미지 파일을 받음|픽셀의 구조 정확도|
|픽셀 판정|동일 프레임의 필수 관계가 관찰됨|역사적 장소의 진위·사용자 미적 선호|
|사용자 판단|의도한 의미와 매력이 충분함|다른 요청에 대한 일반 성능|

### 8.2 84개 사례와 이미지 실험

프로필별 양성 사례 34개와 혼동 음성 사례 34개, 교차 영역 홀드아웃 16개를 작성했다. 양성 사례는 해당 구조를 명시한 요청이고, 음성 사례는 첫 번째 주요 대체물을 제공한다. 후속 구현에서는 한국어·영어·자연스러운 우회 표현을 추가하고, 음성의 단순 문자열 유무가 아니라 실제 의도와 활성화 결과를 평가해야 한다. 여기의 사례는 실행 가능한 테스트 프로그램이 아니라 검증 명세다.

가장 먼저 볼 홀드아웃은 “낙하문 무늬 깃발”, “I keep my notebook near a glass curtain wall”, “해자 없는 궁전”, “현대 관광객의 노이슈반슈타인 방문”, “금박 없는 회색 로코코 패널”, “사람 없는 마른 해자 요새 전경”이다. 이런 요청을 보존하지 못하면 전용 양성 장면이 좋아져도 보강을 채택하기 어렵다.

이미지 실험은 동일 원요청에 대해 기존 데이터, 선택형 후보 보강, 명시 구조 프로필 적용의 세 조건을 분리한다. 각 조건의 최종 문장·후보팩·모델 설정·참조 사용을 고정하고, 형제 조건의 출력 이미지를 보고 문장을 수정하지 않는다. 첫 비교가 좋아도 여러 대응 시행과 다른 장면의 결과 없이 일반적 인과 효과로 결론내리지 않는다. 이 계획은 현재 턴에서 에이전트 위임이나 이미지 생성을 수행했다는 의미가 아니다.

102개 관찰 기준은 각각 같은 프레임에서 판단한다. 멀리서 구조가 읽히는지와 원본 해상도에서 접합·반사가 성립하는지를 나눠 본다. 핵심 부분이 가려지거나 다른 구조로 치환되면 가시성 계약에 실패한 것이다. 이미지가 전달되지 않은 경우는 픽셀 실패 점수가 아니라 `unscored`다. 서로 다른 이미지에서 조건 하나씩을 충족한 결과를 합쳐 한 장면 PASS로 처리하지 않는다.

### 8.3 우선순위와 중단 조건

첫 구현 묶음은 문루·낙하문·도개교·마시쿨레이션·마른 해자와 앙필라드·거울 회랑·창가 좌석을 권한다. 구조적 차이가 명확하고 인물 촬영 배경에서도 의미가 크기 때문이다. 다음 묶음은 주탑/구획·중첩 성곽·도시 성곽·능보/외보·이중 나선계단이다. 이들은 넓은 시야나 복잡한 경로가 필요하므로 카메라 가시성 검증 부담이 더 크다.

후보가 등록돼도 공개 후보팩 노출이 없으면 인덱스나 연결을 먼저 수정한다. 노출·선택·문장 반영은 되는데 픽셀 구조가 실패하면 용어를 더 붙이기보다 소유 관계, 관찰 위치, 증거의 크기를 수정한다. 주어진 크롭에서 관계를 보일 수 없거나 출처로 사실을 확정할 수 없으면 그 한계를 유지한다. 불명확한 역사나 임의의 촬영 구도를 추가해 통과시키지 않는다.

구현의 채택 조건은 목표 혼동쌍의 전부 통과, 요청 의도 홀드아웃 보존, 실제 후보 경로 확인, 이미지 관찰 기준 충족이다. 다수결 평균 점수가 핵심 구조의 실패를 상쇄하지 않도록 한다. 실제 개선율이나 채택 판정은 후속 실험 후에만 기록할 수 있다.

## 9. 남은 연구와 자료의 한계

이번 연구는 핵심 건축 관계를 강화할 근거와 설계를 제공한다. 각 지역의 모든 성곽 부품, 가구·직물의 세부 연대, 문장 도안, 수도원 전체의 기능 분류를 포괄적으로 검증한 사전은 아니다. 명칭만 보존한 항목은 자동으로 강한 시각 프로필로 승격하지 않는다. 실제 장소를 정확히 재현하려면 평면도·보존 조사·시기별 사진·재료 기록을 더 좁게 연결해야 한다.

주요 사실은 공식 관리기관·박물관·문화유산기관 자료로 확인했다. 앙필라드의 일반 용어 정의에는 이차 자료 한 건을 명시적으로 포함하고 공식 베르사유 사례와 연결했다. 스투어헤드 National Trust 본문은 접근 제한으로 읽지 못해, 핵심 인공 동굴 설명은 Historic England 등재 기록으로 대체했다. 검색 결과의 수집 시점을 문서 발행일로 사용하지 않았다.

픽셀을 직접 보고 역사 사진의 형태를 계측하거나 새 이미지를 생성해 성능을 비교하지는 않았다. 공식 페이지의 본문·도판 설명과 구조 설명을 바탕으로 관찰 기준을 제안했다. 특히 베네치아 입면 세부, 미세 조각 형태, 재료 판별은 후속 원본 이미지 대조를 거쳐야 한다. 연구 문헌이 정의한 건축과 생성 모델이 실제로 그린 건축의 차이는 아직 검증되지 않았다.

## 부속 자료

- `profile-matrix.md`: 34개 프로필의 검색어, 동일 프레임 관계, 혼동 경계, 출처 링크.
- `candidate-drafts.json`: 프로필·후보 문장·선택형 묶음의 연구 전용 초안.
- `verification-plan.json`: 84개 사례, 비교 조건, 증거 단계와 판정 규칙.
- `local-coverage.json`: 원본 자산 경로·해시·어휘 일치 결과와 검색 범위.
- `sources.json`: 출처 33건의 기관·제목·URL·사용 범위·날짜 상태.
- `referenced-conversation.md`: 참조 대화의 전체 응답. 과거의 인용 토큰은 이번 출처 번호와 별개다.
- `build-research-data.py`: 연구 초안과 로컬 어휘 조사 결과를 재생성하는 보조 스크립트. 실행 데이터는 변경하지 않는다.

## 출처

출처 조회일은 2026-09-09다. 별도 날짜가 없으면 본문에서 발행·갱신일을 확정하지 않은 자료다. 기관 웹사이트라는 이유만으로 모든 사진이 최초 건립 당시 모습을 보여준다고 간주하지 않는다.

[^S01]: English Heritage. [Goodrich Castle Glossary](https://www.english-heritage.org.uk/siteassets/home/visit/places-to-visit/goodrich-castle/school-visits/goodrich-castle-glossary.pdf). 발행·갱신일 미확인. 사용 범위: pp.1–2; gate, wall, openings.

[^S02]: Historic England. [Stone Castles](https://historicengland.org.uk/images-books/publications/iha-stone-castles/heag235-stone-castles/). 발행·갱신일 미확인. 사용 범위: PDF pp.5–6; arrangement and residential functions.

[^S03]: English Heritage. [Castles Through Time](https://www.english-heritage.org.uk/castles/castles-through-time/). 발행·갱신일 미확인. 사용 범위: Norman castles; stone keeps; later castles.

[^S04]: Cadw. [Beaumaris Castle](https://cadw.gov.wales/visit/places-to-visit/beaumaris-castle). 발행·갱신일 미확인. 사용 범위: Concentric defences and incomplete building.

[^S05]: Cadw. [Raglan Castle](https://cadw.gov.wales/visit/places-to-visit/raglan-castle). 발행·갱신일 미확인. 사용 범위: Gatehouse and flared machicolations.

[^S06]: UNESCO World Heritage Centre. [Fortifications of Vauban](https://whc.unesco.org/en/list/1283/). 발행·갱신일 미확인. 사용 범위: Bastioned towns, citadels, coastal and mountain sites.

[^S07]: US National Park Service. [Defense in Depth Wayside](https://www.nps.gov/places/000/defense-in-depth-wayside.htm). 발행·갱신일 미확인. 사용 범위: Ravelin, dry moat, covered way, glacis.

[^S08]: UNESCO World Heritage Centre. [Historic Fortified City of Carcassonne](https://whc.unesco.org/en/list/345/). 발행·갱신일 미확인. 사용 범위: Urban enclosure and nineteenth-century restoration.

[^S09]: UNESCO World Heritage Centre. [Castle of the Teutonic Order in Malbork](https://whc.unesco.org/en/list/847/). 발행·갱신일 미확인. 사용 범위: Brick Gothic castle-monastery and restoration.

[^S10]: Getty Research Institute. [Art & Architecture Thesaurus: keeps, 300003694](https://www.getty.edu/vow/AATFullDisplay?find=&logic=&note=&subjectid=300003694). 발행·갱신일 미확인. 사용 범위: Scope note; keep/donjon sense.

[^S11]: English Heritage. [Life in a castle](https://www.english-heritage.org.uk/castles/life-in-a-castle/). 발행·갱신일 미확인. 사용 범위: Residential spaces, reconstructed Dover interiors, kitchens.

[^S12]: English Heritage. [Description of Dunstanburgh Castle](https://www.english-heritage.org.uk/visit/places/dunstanburgh-castle/history/description/). 발행·갱신일 미확인. 사용 범위: Gate passage, window seats, uncertain barbican reconstruction.

[^S13]: Historic Royal Palaces. [Great Hall, Hampton Court Palace](https://www.hrp.org.uk/hampton-court-palace/whats-on/great-hall/). 발행·갱신일 미확인. 사용 범위: Hammerbeam roof and Tudor hall.

[^S14]: The Metropolitan Museum of Art. [Gothic Art](https://www.metmuseum.org/essays/gothic-art). 2002-10. 사용 범위: Pointed arches, rib vaults, support system and ornament.

[^S15]: Château de Versailles. [The King’s State Apartment](https://en.chateauversailles.fr/discover/estate/palace/king-state-apartment). 발행·갱신일 미확인. 사용 범위: Ceremonial rooms; marble, painted ceilings, changing use.

[^S16]: Château de Versailles. [The Hall of Mirrors](https://en.chateauversailles.fr/discover/estate/palace/hall-mirrors). 발행·갱신일 미확인. 사용 범위: Mirrors opposite windows; connected ceremonial gallery.

[^S17]: Château de Versailles. [Completion of the restauration of the Salon de Diane](https://en.chateauversailles.fr/press/restorations/completion-restauration-salon-diane). 발행·갱신일 미확인. 사용 범위: Enfilade; marble revetments; restoration.

[^S18]: Wikipedia contributors. [Enfilade (architecture)](https://en.wikipedia.org/wiki/Enfilade_(architecture)). 발행·갱신일 미확인. 사용 범위: Aligned doorways through a series of rooms; terminology cross-check.

[^S19]: Bavarian Palace Administration. [Amalienburg](https://www.schloss-nymphenburg.de/englisch/p-palaces/amalien.htm). 발행·갱신일 미확인. 사용 범위: 1734–1739 pleasure/hunting palace; Rococo interior ensemble.

[^S20]: The Metropolitan Museum of Art. [Boiserie from the Palais Paar](https://www.metmuseum.org/art/collection/search/202997). 발행·갱신일 미확인. 사용 범위: ca.1765–72 with later additions; mixed-room museum installation; gray paint.

[^S21]: Domaine national de Chambord. [Not to be missed](https://www.chambord.org/en/history/the-chateau/not-to-be-missed/). 발행·갱신일 미확인. 사용 범위: Twin helical ramps around a hollow core; keep and wings.

[^S22]: Patronato de la Alhambra y Generalife. [Patio de los Leones](https://www.alhambra-patronato.es/edificios-lugares/patio-de-los-leones). 발행·갱신일 미확인. 사용 범위: Open court, perimeter arcade, fountain and disputed original paving.

[^S23]: Patronato de la Alhambra y Generalife. [The Hall of the two sisters](https://www.alhambra-patronato.es/en/edificios-lugares/the-hall-of-the-two-sisters). 발행·갱신일 미확인. 사용 범위: Muqarnas dome, tile socle, fountain-to-court channel.

[^S24]: Fondazione Musei Civici di Venezia. [Building and history — Palazzo Ducale](https://palazzoducale.visitmuve.it/en/building-and-history/). 발행·갱신일 미확인. 사용 범위: Gothic/Renaissance/Mannerist phases and waterside wing.

[^S25]: Victoria and Albert Museum. [Robert Adam: Neoclassical architect and designer](https://www.vam.ac.uk/articles/robert-adam-neoclassical-architect-and-designer). 2024-04-17. 사용 범위: Coordinated classical ornament across interior elements.

[^S26]: Château de Versailles. [The Orangery](https://en.chateauversailles.fr/discover/estate/gardens/orangery). 발행·갱신일 미확인. 사용 범위: Winter shelter/summer display; masonry galleries; parterre.

[^S27]: Château de Versailles. [The Groves](https://en.chateauversailles.fr/discover/estate/gardens/groves). 발행·갱신일 미확인. 사용 범위: Enclosed outdoor rooms, fountains and changes over time.

[^S28]: Historic England. [The Grotto and the River God’s Cave, list entry 1318473](https://historicengland.org.uk/listing/the-list/list-entry/1318473). 1987-09-09. 사용 범위: Artificial rockwork, constructed chambers and water feature.

[^S29]: Opéra national de Paris. [Palais Garnier](https://www.operadeparis.fr/en/about/theaters-and-workshops/palais-garnier). 발행·갱신일 미확인. 사용 범위: Opera auditorium, staircase and public spaces.

[^S30]: Scottish Geology Trust / McAdam and Clarkson (eds.). [Building stones of Edinburgh — Lothian geology: an excursion guide](https://geoguide.scottishgeologytrust.org/p/egs_lo/egs_lo_04_buildingstonesofedin). 1987. 사용 범위: ashlar/rubble 등 석조 용어. 현재 현장 상태의 근거로 사용하지 않음.

[^S31]: Bavarian Palace Administration. [Neuschwanstein Castle — Historicism](https://www.neuschwanstein.de/englisch/idea/histor.htm). 발행·갱신일 미확인. 사용 범위: Medieval references combined with modern building technology.

[^S32]: English Heritage. [Description of Castle Acre Castle and Bailey Gate](https://www.english-heritage.org.uk/visit/places/castle-acre-castle-and-bailey-gate/history/description/). 발행·갱신일 미확인. 사용 범위: Mound and baileys, successive changes, town and castle gates.

[^S33]: US National Park Service. [Teacher-led School Groups — Castillo de San Marcos](https://www.nps.gov/casa/learn/education/classrooms/teacher-led.htm). 발행·갱신일 미확인. 사용 범위: Bastions, gun deck and ravelin geometry.
