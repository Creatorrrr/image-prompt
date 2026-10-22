"""One explicit disposition for each of the 150 referenced numbered seeds."""
# id | route mode | card ids | distinction to preserve
DATA = '''
1|genre_context|G12,G10|넓은 전통이며 New Weird와 동일 범위가 아님
2|genre_context|B02,F10|기술과 마법의 해석을 물건 외형과 분리
3|genre_context|E04,B04|허구 세계의 자율적 역사와 지리는 단일 배경 외형이 아님
4|genre_context|B03,A05|재앙 이후 조건과 세계의 장기 소진을 구분
5|temporal|B03,D05|새 생활 정착까지의 경과는 단일 사진으로 확정 불가
6|genre_context|G02,H02|다크 판타지가 폭력·촉수·검은 색을 강제하지 않음
7|genre_context|F01,F08|지역 관습과 실제 종교를 공포로 자동 분류하지 않음
8|genre_context|C08,C09|생태 의존·오염의 원인을 사진으로 단정하지 않음
9|genre_context|D01,G02|안락함과 호러의 비중을 별도 평가
10|genre_context|B03,D10|집·생활 중심은 특정 복식·색조가 아님
11|critical|D12,E02|적극적 친절·저항이라는 태도를 미소로 대체하지 않음
12|genre_context|A09,D05|전원 풍경과 사회적 이상화를 구분
13|critical|A10,E05|노동·불평등은 공간 대비만으로 입증되지 않음
14|genre_context|D04,F04|예법·규칙은 문맥이며 특정 찻잔이 필수 아님
15|critical|D07,E06|역사적 비평 용어를 현대 Cozy Fantasy와 구분
16|temporal|A01,A06|먼 미래 연대는 외형과 분리
17|temporal|A06,B10|층위와 절대 시간을 구분
18|temporal|A06,A12|시간 규모와 감상 효과를 분리
19|proxy|A01|붉은 원반은 자연적 항성 노화의 증명이 아님
20|temporal|A11,A12|세계 종말과 한 문명의 멸망을 분리
21|scientific_context|A11,A03|에너지 소멸이나 낡은 물건과 동일시하지 않음
22|scientific_context|A11|열평형 가설을 방 하나의 냉기와 구분
23|scientific_context|A11,A04,A08|국소 수선·정돈을 엔트로피 측정으로 쓰지 않음
24|temporal|A05,A12|세계 쇠약과 가뭄·물리 소진을 구분
25|critical|A10|문화적 쇠락과 장식의 양·성적 의미를 분리
26|temporal|A12,D07|문명사적 암흑기와 밤의 조도를 분리
27|temporal|A07,B10|닳은 책이 곧 사회 전체의 기억 상실은 아님
28|temporal|A09,A12|개체의 유일성은 맥락·기록 필요
29|critical|A12,D10|표정 하나로 수만 년 권태 확정 금지
30|critical|A12,F09|종말론은 신앙·사유 맥락
31|proxy|B10,A06|실제 밑글과 도시 층위의 비유 구분
32|visible_option|B01,B02|실제 재사용 접합과 고대풍 새 장식을 구분
33|critical|B03,B07|폐허의 형태와 매혹의 경험 구분
34|proxy|A02,B02|물건의 조작과 원리 상실 구분
35|proxy|B08,F03|오래됨·신성·진위의 별도 근거 필요
36|proxy|B09,G05|관절·도구 접촉이 자율·영원 반복의 증거 아님
37|visible_option|B04,B11|일반 성의 핵심 방어시설과 작품별 마지막 보루 구분
38|critical|F02,B11|비평적 Polder와 실제 제방 구분, 원전 확인 미완료
39|proxy|B03,B11|거주 공간의 배치와 실제 안전 보장 분리
40|critical|D04,G06|의례적 중간 상태와 문턱·리미널 미학 구분
41|critical|E12|장소의 영과 장소 고유성의 확장 의미 구분
42|visible_option|C11,B11,G08|살 같은 표면과 실제 지성·생명 분리
43|visible_option|B07|묘역의 통로와 실제 죽은 자의 도시 맥락 분리
44|visible_option|H03|유골 구획과 시신·식기·장식 분리
45|visible_option|B08|자연물·유물의 별개 소유자·구획 보존
46|scientific_context|C06,C12,D02|허구 생물학의 추론과 실제 생리 입증 분리
47|critical|C01,C09|낯선 생태와 악의·초자연성 동일시 금지
48|scientific_context|C07,H12|공생이 언제나 상리공생은 아님
49|scientific_context|C07,C01|양측 편익·지속성은 별도 관찰 필요
50|scientific_context|C08|부착이 영양 착취·질환을 증명하지 않음
51|visible_option|C01|균사 외형과 지능·기억 저장 구분
52|scientific_context|C09,B06|기질·부착과 분해 영양 경로 구분
53|proxy|C02|자체 발광·반사·형광·색보정 구분
54|temporal|C03|완성 형태와 변태 전 과정 구분
55|proxy|C03,C04|빈 외피와 시신·옷·몸의 연속부 구분
56|visible_option|C05,C06|신화적 합성 외형과 생물학의 키메라 구분
57|genre_context|C05,C08,H05|바디 호러·상처·고어·단순 변형을 구분
58|critical|C05,H12|인간성의 비평 경계를 외형 진단으로 바꾸지 않음
59|critical|C10,H12|동시 행동·여러 팔이 집단의식을 입증하지 않음
60|proxy|C06,C10|자발적 개조·적응·형벌을 외형만으로 분류하지 않음
61|critical|G09|철학적 관점과 호러 장르 구분
62|critical|G09|시선 부재가 우주적 무관심의 증거 아님
63|proxy|G01,G09|크기 대비와 인간 가치 판단 분리
64|critical|G10|아직 모름과 원리적 불가지를 구분
65|critical|G04,G06,G10|공간 모순의 실현과 존재 기반 붕괴의 해석 구분
66|critical|G03,G07,G10|관찰 차이와 기억·기록 진위 확정 구분
67|genre_context|G02|eldritch는 촉수·신격 계급의 동의어 아님
68|critical|G11|성스러움·경외는 관객 경험
69|critical|G11|두려움과 매혹의 종교학적 표현, 자세로 확정 불가
70|proxy|G01,G11|규모 단서와 숭고 경험 구분
71|critical|G12|Fisher의 비평과 일반 weird 형용사 구분
72|critical|G05,G12|빈 공간·미상 행위성과 초자연 확정 분리
73|proxy|G03|낯익음의 비교 대상·소유자 필요
74|visible_option|G04|정상 수학의 비유클리드와 모순 공간 구분
75|sequence|G07,G08,G12|보이는 연결과 이전 지식이 바뀌는 순간 구분
76|critical|E12,F01|다양한 실재 신앙을 공포 클리셰로 일반화 금지
77|proxy|F09|지하 지형과 저승 권능 구분
78|proxy|G06|꿈 같은 공간과 실제 꿈·수면 구분
79|visible_option|F03,A07|책 외형과 주문 진위 구분
80|critical|F03,E09|비전 지식의 접근 제한은 표지 외형이 아님
81|proxy|F01,F02,F11|부적의 문화 기능과 실제 효능 구분
82|critical|F05|표지·규칙과 실제 금기·권력·위반 의도 구분
83|proxy|F04|서류·서명과 신적 계약의 효력 구분
84|critical|F07|이름 문자와 본질·마법 권한 구분
85|sequence|F10|토큰은 선택적 소품, 기억 준비·사용 후 망각은 정적 증거 아님
86|critical|F06|형태 대응과 원격 주술 인과 구분
87|critical|F08,H06,H11|자원 봉헌·노동·살해를 하나의 시각 형태로 합치지 않음
88|critical|F08,H06,H11|신을 나타내는 음식·허구 신체·식인을 구분
89|critical|F09|점복·죽은 자와 소통·시체 조종의 판본 차이 보존
90|critical|F09,H01|뱃사공 외모로 영혼 인도자 확정 금지
91|critical|D10,D09|사소한 목표와 감정적 중요성의 구별
92|genre_context|D05,B03|가사 한 장면이 작품 전체의 일상물 형식을 입증하지 않음
93|critical|D11,D08|함께 앉음·식사가 선택한 가족을 입증하지 않음
94|visible_option|D01,D04|제공자·물건·수신자·통로 연결 필요
95|critical|D04,F04|환대 관습·초자연 보호와 실제 전달 동작 구분
96|visible_option|D01,D02,D05|공유 식사와 영양 호환·혈연 구분
97|visible_option|D07,B01|화롯가의 물건·사람 배치와 안전·가족 감정 구분
98|critical|H02,D01|음식 외형과 개인의 추억·위안 구분
99|sequence|F12,F01,D04|현재 행동과 반복·봉인 효능 구분
100|visible_option|C04,C05,D12|돌봄의 필요·행동·대상을 연결하되 선의·효능 추론 금지
101|visible_option|E01,D06,A08|수선 대상·도구·접점·결과 경계 필요
102|visible_option|C06,D05|제작물과 공정 단계·재료·접점 구분
103|critical|E02,D12|공동 행동과 제도·부담 분담의 공정성 구분
104|critical|H01,D08|추모 단서와 사망·감정·가족 관계 분리
105|critical|D07|속도·생산성·삶의 태도는 단일 사진으로 확정 불가
106|visible_option|B12,B02,A02|회수 물건·재사용 기능·소유권 구분
107|visible_option|A03,E03|계량·표·수신자와 정책·공정성 구분
108|critical|E02,A05|공동 접근과 공동 소유·규칙 구분
109|visible_option|E01,B05,C11|시설·손·도구·고장 부위의 동일 소유자 보존
110|critical|E05,E11|작업장과 노조·길드의 법적 조직 구분
111|proxy|E04,E03|서류·창구와 허가·행정 권한 구분
112|critical|E04,E11|외형으로 시민권·인격·법적 지위 판정 금지
113|proxy|C10,E05|몸과 작업 적응을 착취·자발성과 구분
114|critical|E12|집의 물건·이름과 지성·소유권 분리
115|critical|E06,A10|빛·공간 대비와 계급 분류 구분
116|proxy|E07|물리 경계와 감염·정당성·안전성 구분
117|visible_option|E08|운송체·프레임·화물의 소유자 분리
118|critical|E09|병·상표·거래가 기억 내용물의 증거 아님
119|critical|E10,B07|장례 작업·유골 공간과 사망·영혼·시장 구조 분리
120|critical|E11,C07|함께 있음·교환과 합의·상리성 구분
121|critical|F05,H08|선·표지와 실제 규범·위반·의도 분리
122|critical|H08,H03|비체를 오염·체액·시신 외형만으로 환원하지 않음
123|genre_context|C05,G02|기괴한 형태가 악의·질병·성적 의미를 뜻하지 않음
124|critical|H07|욕망과 공포의 관계, 외형에서 성적 의도 추론 금지
125|critical|D03,H07|성인 지성체 간 친밀함과 동의·성행위 분리
126|critical|H08,F08|상징·신화적 결합과 실제 성행위 구분
127|critical|H07,H08|신비 체험과 욕망의 비평 맥락, 자동 시각화 금지
128|critical|H09|생식 상태·통제권·공포를 외형 진단으로 확정 금지
129|critical|H08|특정 비평 개념이며 여성 괴물의 일반명 아님
130|critical|H09|성적 강제·생식 통제와 의례·돌봄을 구분
131|critical|H04,H10|기록·혈연·성행위·강제의 별도 근거 필요
132|critical|H10,H01|추모·부활자 관계와 시체성애 구분
133|critical|H05,H11|상처의 노출 강도와 몸 변형 공포 구분
134|critical|H06,H11|붉은 음식·사체 생태·봉헌과 실제 동종섭식 구분
135|critical|H06,H11|제단·봉헌과 의례적 살해 분리
136|critical|D12,H12|구체적 필요에 대한 응답과 윤리적 정당화 구분
137|critical|B09,E12,H12|접촉·움직임 외형과 실제 의식·행위성 구분
138|critical|H12,C07|인간 중심성의 비평과 특정 외형 양식 구분
139|critical|C01,H12|함께 만듦과 접촉·자원 교환 단서의 차이
140|critical|D11,D03,H12|선택 관계·책임과 혈연·외형 구분
141|critical|C09,H12|철학적 공존과 어두운 색·오염의 미학 구분
142|critical|B12,D09,H12|수집·보존의 저술 관점과 가방 소품 구분
143|proxy|G01|일상과 크기 대비는 숭고의 선택적 실현안
144|critical|H01,D08|애가 정조와 사망·관객 슬픔 확정 구분
145|proxy|H02,H03|죽음 도상과 실제 사망·위협 분리
146|proxy|H02|정물 전통과 부패·세계 종말 구분
147|sequence|B12,G12|여행 소품과 여러 계층을 거치는 서사 형식 구분
148|sequence|D10,G12|동시 대비와 장엄함이 사소함으로 바뀌는 전환 구분
149|sequence|G12|위험 앞 미소가 농담의 텍스트·효과를 증명하지 않음
150|critical|D02,G12|낯선 식기와 낯설게 하기의 문학적 효과 구분
'''
