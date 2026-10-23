"""Authored DEVELOPMENT probes. These are plans, not executed retrieval evidence."""
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
ROWS='''
P01	셋이 연습실 거울을 보면서 테이프에 발 맞추는 장면	Three trainees finding their floor marks in front of a rehearsal mirror	I001	N02
P02	심사하는 둘 앞에서 혼자 평가 받는 연습생	One trainee performing in front of two seated evaluators	I002	N02
P03	녹음하는 멤버와 유리 너머 엔지니어	A vocalist in the booth with the engineer behind the glass	I003	N06
P04	동료한테 물을 내밀지만 아직 받기 전	Backstage, a bandmate offers water just before the other takes it	I008	N15,N41
P05	다섯 명 무대, 중앙 한 명만 조금 앞	Five members on stage with one slightly forward in the middle	I011	N07
P06	한쪽 무릎은 바닥, 뒤에는 서 있는 둘	A low front pose with one knee down and two members standing behind	I013	N26
P07	들어 올리는 파트너의 손과 바닥 발이 보이는 순간	A partner lift with the supporting hands and grounded feet visible	I016	N26
P08	팬이 앞에 있고 열린 앨범에 사인하는 가수	An artist signing an open album across the table from a fan	I021	N17
P09	영통 팬싸, 화면 속 가수한테 손 흔드는 팬	A fan waving to an artist on a video fan call	I022	N17
P10	카드 슬리브에 포카 넣고 옆에 바인더	A collector sleeving a portrait card beside a pocket binder	I026	N19
P11	재킷 길이는 다르지만 세 명 어깨 장식은 같은 팀	Three members with different jacket lengths sharing one shoulder motif	I059	N23
P12	겉치마와 옆 쇼츠 입구가 함께 보이는 무대 스코트	A stage skort showing the outer skirt panel and the shorts openings	I063	N23
P13	성인 무대복의 아일릿에 교차 끈이 있는 몸판	An adult stage costume with crossed eyelet lacing on its bodice	I068	N23
P14	성인 하네스가 셔츠 위에서 등과 허리에 연결	An adult fashion harness routed over the shirt to the back and waist	I075	N23,N32
P15	허리벨트 끈이 스타킹 윗단 집게에 닿는 성인 의상	An adult costume with suspender straps clipped to the stocking tops	I076	N23
P16	오른손 엄지랑 검지를 교차한 작은 하트	A tiny heart made by crossing the right thumb and index finger	I083	N25
P17	왼눈만 감고 카메라를 보는 클로즈업	A close-up wink with only the left eye shut toward the camera	I088	N25
P18	귀 안 이어피스에서 뒤 허리 팩까지 선이 보이게	An in-ear earpiece with the cable visible down to the back-waist pack	I109	N30
P19	손은 비워 두고 입 옆에 작은 마이크 캡슐	A hands-free stage shot with a small microphone capsule beside the mouth	I110	N30
P20	마커 입은 사람 옆 화면에만 아바타가 있는 제작실	A capture-room performer beside a screen that contains the avatar	I113	N21
'''
NEG='''
C01	아이돌 스타일의 두상	N01,N07	종교적 우상·괴물 조각을 연예인과 혼동하지 않음
C02	우리 반 아이돌 같은 인기 많은 학생	N01,N22	실제 가수·성인·무대·팬덤을 자동 추가하지 않음
C03	정가운데 선 멤버	N07	리더·최연장자·최고 인기라는 직책 추론 금지
C04	연습생 오디션	N02	데뷔 확정·미성년·교복으로 자동 변경 금지
C05	청순한 콘셉트 사진	N22	순결·성경험·실제 나이 추정 금지
C06	걸크러시 룩	N22	성적 지향·성정체성·폭력성 추론 금지
C07	지뢰계 리본 의상	N22	정신질환·자해 성향을 추가하지 않음
C08	지쳐 보이는 무대 얼굴	N28,N41	화장·땀에서 번아웃·약물·과로 원인을 진단하지 않음
C09	유닛 멤버끼리 손잡기	N15	실제 연애·성적 지향·팬 합의를 추정하지 않음
C10	카메라 든 홈마	N17,N34	사생·스토킹·무허가 판정은 장비 외형에서 만들지 않음
C11	성인 하네스 무대복	N23,N32	구속·강압·노출 강요를 자동 추가하지 않음
C12	반짝이는 검은 의상	N24	레더·라텍스·PVC 성분을 단정하지 않음
C13	가터 없는 허벅지 밴드	N23	허리벨트·스트랩·집게를 새로 추가하지 않음
C14	헤드셋 쓴 가수	N30	귀 안 모니터·라이브 가창·립싱크를 자동 판정하지 않음
C15	트로피 들고 우는 멤버	N12	첫 1위·재기 성공·정산 완료를 확정하지 않음
C16	꺼진 응원봉이 보이는 공연장	N18	블랙오션·불매 의도를 자동 판정하지 않음
C17	모니터의 같은 포즈 아바타	N21	실제 인원 중복 계산·실시간 연결·동일 신원을 추정하지 않음
C18	회귀한 아이돌	N04	거울·시계·복제 얼굴을 필수로 강제하지 않음
C19	한 명이 손에 마이크 들고 있는 요청	N25,N30	마이크를 든 손에 양손 하트를 강제해 손·물체를 늘리지 않음
C20	실제 무대와 다른 표정의 앨범 사진	N01,N28	인쇄 얼굴 표정을 실제 현장 몸에 이전하지 않음
'''
TEMP='''
T01	센터 교대	N26	최소 전후 인물 위치와 인계 순서	I011
T02	리플·캐논	N26	세 시점에서 순차 시작을 구분; 팔 높이 차이만으로 대체 금지	I012
T03	바디롤·힙롤·트월킹	N26,N44	몸통·골반·무릎의 시간 경로와 지지점; 용어별 전문가 자료	I050
T04	손키스 완료	N25	입 앞 출발과 손의 바깥 이동을 순서로 제시	I089
T05	군무의 정밀 타이밍	N26	연속 프레임·박자 비교; 순간 정렬만으로 통과 금지	I012
T06	원테이크·무빙캠	N29	연속 촬영과 편집 이력; 정지 구도로 증명 불가	I033
T07	립싱크·백킹 트랙	N30	오디오와 입 모양의 시간적 관계; 장비 사진은 부족	I110
T08	스토킹·그루밍·반복 괴롭힘	N33,N34,N40	반복·권한·원치 않음·경과를 명시한 서사; 사진 한 장으로 판정 불가	I117
'''
COMBO='''
M01	세 명 거울 연습 + 멤버별 같은 어깨 모티프	I001,I059	실물 셋과 거울상, 별도 의복 소유를 함께 보존
M02	한 손 마이크 + 다른 손 작은 하트	I083,I096	두 카드 모두 오른손이므로 그대로 동시 채택하면 충돌. 손을 임의 변경해 같은 literal 채택으로 기록하지 않고 적합한 다른 대안을 선택하거나 별도 전체 소스를 검토
M03	성인 새틴 상의 + 장식 하네스 + 뒤 허리 팩	I050,I075,I109	의복 스트랩과 장비 케이블을 따로 유지; 필수 종점이 가리면 실패
M04	팬사인 테이블 + 촬영 구역의 카메라	I021,I030	사인 대기열·지정 촬영 구역을 행사 문맥에 맞게 분리
M05	모션캡처 실물 + 모니터 얼굴 + 무대 LED	I040,I113,I114	세 매체 경계와 인원 계산; 표시 인물이 실제 거인으로 변하지 않음
M06	후렴 전신 구도 + 눈 아래 젬	I033,I105	원거리 장면에서 작은 젬을 실제로 식별 가능한지 별도 판정
M07	리프트 + 긴 프린지 소매	I016,I079	허리 지지 손과 장식 가닥을 섞지 않고 접점이 보이는지 검토
M08	트로피 반응 + 소등 객석	I020,I119	보이는 소품과 표정을 이력·관객 의도의 증거로 과장하지 않음
'''

cases=[]
for row in ROWS.strip().splitlines():
    cid,ko,en,visual,context=row.split('\t')
    for lang,q in [('ko',ko),('en',en)]:
        cases.append({'id':cid+'_'+lang,'kind':'positive_development','language':lang,'request':q,
                      'relevant_card_ids':visual.split(','),'context_ids':context.split(','),
                      'expectation':'Semantic eligibility and useful optional exposure, never mandatory adoption.'})
for row in NEG.strip().splitlines():
    cid,q,context,forbid=row.split('\t')
    cases.append({'id':cid,'kind':'contrast_development','language':'ko','request':q,
                  'context_ids':context.split(','),'forbidden_inference_ko':forbid})
for row in TEMP.strip().splitlines():
    cid,q,context,required,proxy=row.split('\t')
    cases.append({'id':cid,'kind':'temporal_or_context_development','language':'ko','request':q,
                  'context_ids':context.split(','),'required_evidence_ko':required,
                  'insufficient_static_proxy_card_ids':proxy.split(','),
                  'expectation':'single_frame_not_sufficient'})
for row in COMBO.strip().splitlines():
    cid,q,visual,check=row.split('\t')
    cases.append({'id':cid,'kind':'combination_development','language':'ko','request':q,
                  'relevant_card_ids':visual.split(','),'joint_check_ko':check})
for c in cases:
    c.update(split='development',execution_status='not_run',native_approval=False)
(HERE/'evaluation-cases.json').write_text(json.dumps({
    'schema':'idol-research-evaluation-plan/v1','all_cases_are_authored_development':True,
    'independent_holdout_status':'not_authored_reserve_fresh_queries_before_integration',
    'cases':cases},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'development_cases':len(cases),'executed':0,'blind_holdout':0}))
