"""Inventory reuse leads and future evaluation cases; no runtime execution."""
from pathlib import Path
import json, re, hashlib, collections

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[3]
def read(name):return json.loads((ROOT/name).read_text())
def save(name,obj):(ROOT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
routes=read('keyword-routes.json')['routes']
cards=read('semantic-cards.json')['cards']
card_map={c['id']:c for c in cards}

asset=REPO/'skills/photo-prompt-image-generator/assets'
manifest=json.loads((asset/'photo_candidate_corpus_manifest.json').read_text())
needles={
 '저지':['sports jersey','athletic jersey','스포츠 저지'],
 '트랙수트':['tracksuit','트랙수트'], '웜업 재킷':['track jacket','트랙 재킷'],
 '탱크톱':['tank top','탱크톱'], '베이스레이어':['base layer','베이스레이어'],
 '컴프레션웨어':['compression','컴프레션'], '러닝 쇼츠':['split shorts','running shorts','러닝 쇼츠'],
 '타이츠·레깅스':['leggings','tights','레깅스'], '튜브 삭스':['knee socks','tube socks','니 삭스'],
 '레터맨·바시티':['varsity jacket','letterman','바시티'],
 '테니스 스커트':['tennis skirt','tennis dress','테니스 스커트'],
 '래시가드·웻수트':['rash guard','wetsuit','웻수트'],
 '복싱 트렁크':['boxing trunks','boxing robe','복싱 트렁크'],
 '스킨수트':['skinsuit','스킨수트'], '치어 유니폼':['cheer uniform','치어 유니폼'],
 '헤드밴드·손목밴드':['headband','wristband','손목밴드'],
 '캡·바이저':['visor','baseball cap','바이저'], '클리츠':['cleats','studs','육상 스파이크'],
 '골키퍼 장갑':['goalkeeper gloves','골키퍼 장갑'],
 '니 패드·엘보 패드':['knee pads','elbow pads','무릎 보호대'],
 '마우스가드':['mouthguard','마우스가드'], '체조 그립':['gymnastics grips','체조 그립'],
 '애슬레틱 빌드':['athletic build','athletic presence','탄탄한'],
 '린 머스큘러':['lean muscular','린 머스큘러'],
 '파워풀 빌드':['powerful build','broad shoulders','넓은 어깨'],
 '긴 리치':['long reach','long arms','긴 팔'],
 '근육 윤곽':['muscle definition','근육 윤곽'],
 '젖은 잔머리':['damp flyaways','wet fringe','젖은 잔머리'],
 '포니테일·브레이드·번':['ponytail','braids','hair bun','포니테일'],
 '버즈컷·크루컷':['buzz cut','crew cut','버즈컷'],
 '태닝 라인':['tan lines','tan line','태닝 라인'],
 '굳은살':['calluses','callus','굳은살'],
 '라커룸':['locker room','라커룸'], '더그아웃':['dugout','더그아웃'],
 '불펜':['bullpen','불펜'], '터널·입장 통로':['players tunnel','stadium tunnel','선수 입장 통로'],
 '링·케이지·매트':['boxing ring','octagon cage','복싱 링'],
 '피스트':['fencing piste','펜싱 피스트'], '피트·패독':['paddock','pit lane','패독'],
 '스코어보드·샷클록':['scoreboard','shot clock','스코어보드'],
 '트로피·메달·우승기':['trophy','medal','트로피'],
 '믹스트존·기자회견장':['press conference','mixed zone','기자회견'],
 '로 앵글·하이 앵글':['low angle','high angle','로 앵글'],
 '축소원근':['foreshortening','축소원근'],
 '정지 순간·프리즈 프레임':['frozen action','freeze frame','정지 순간'],
 '리액션 숏':['reaction shot','리액션 숏'],
 '머리 묶기·장비 조정':['tying hair','adjusting goggles','머리를 묶'],
 '피스트 펌프':['fist pump','피스트 펌프'],
 '악수·포옹·인사':['handshake','hugging','악수'],
 '착지 자세':['landing','착지'], '스트레칭':['stretching','스트레칭'],
 '물보라·눈가루·빙판 자국':['water splash','snow spray','skate marks','물보라'],
 '악문 턱·고정된 시선':['clenched jaw','fixed gaze','악문 턱']}
hits={key:[] for key in needles};source_hashes={}
for module in manifest['modules']:
    if module['kind']!='candidates':continue
    p=asset/module['file']
    if not p.exists():continue
    blob=p.read_bytes();source_hashes[module['file']]=hashlib.sha256(blob).hexdigest()
    data=json.loads(blob).get('candidates',{})
    for cid,c in data.items():
        if c.get('record_kind')!='visual_option':continue
        content=c.get('content',{})
        text=' '.join([content.get('en',''),content.get('ko','')]+content.get('aliases',[]))
        for label,terms in needles.items():
            matched=[]
            for term in terms:
                pat=r'(?<![A-Za-z0-9])'+re.escape(term)+r'(?![A-Za-z0-9])' if term.isascii() else re.escape(term)
                if re.search(pat,text,re.I):matched.append(term)
            if matched:
                hits[label].append({'id':cid,'file':module['file'],'en':content.get('en'),'ko':content.get('ko'),'matched_terms':matched,'record_sha256':hashlib.sha256(json.dumps(c,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),'review_status':'LEXICAL_LEAD_ONLY_NOT_APPROVED'})
save('reuse-inventory.json',{'method':'Exact token/phrase triage in authored visual_option content only. No score, retrieval pass, semantic equivalence or pixel quality is established. Review the entire source contract before reuse.','groups':hits,'snapshot_source_hashes':source_hashes})

followup=[]
for r in routes:
    if r['disposition']!='targeted_followup_required':continue
    leads=[]
    for key,found in hits.items():
        if key in r['term'] or r['term'].split(' — ')[0] in key:leads.extend(found)
    ti=r['table_index']
    if ti in (10,11,12):
        package='P1 garment and equipment form';primary='Relevant federation equipment rule plus manufacturer construction view; compare layer, fastener, coverage and worn state.'
    elif ti==13:
        package='P1 body and surface';primary='Bound the visible silhouette/texture without diagnosing body composition, training, disease or cause; reuse general morphology where exact.'
    elif ti==14:
        package='P1 venue and prop';primary='Official venue plan/photo and sport rule; specify boundary geometry, prop owner and readable text scope.'
    elif ti in (6,7,8,9):
        package='P2 specialist action';primary='Federation coaching sequence with multiple viewpoints; isolate phase, articulations, owned contact and support before coding.'
    else:
        package='P2 visual rhetoric';primary='Resolve chosen medium, shot layout and actor-target relationship; keep temporal, audio and critical claims contextual.'
    followup.append({'row_id':r['id'],'term':r['term'],'package':package,'required_research':primary,'existing_lead_count':len(leads),'existing_leads':leads[:5],'promotion_gate':'Exact sport/context and complete owner/contact/visibility contract reviewed; selected native binding and all effects validated; regression contrast added; pixels still separate.'})
save('followup-worklist.json',{'rows':followup,'note':'Research backlog, not silently omitted scope. General concepts with exact existing candidates should reuse them; specialist gaps need new primary geometry evidence.'})

CASE_ROWS='''M01|배구 선수가 포어암 패스로 받는다|V01|팔뚝 접촉을 구현|서브 리시브·공격 디그·득점 결과 자동 단정 금지
M02|배구 서브 리시브|V01|받는 상황 문맥 보존; 기술 형태 별도 선택|모든 리시브를 팔뚝 형태로 강제 금지
M03|배구 디그|V01|상대 공격 수비 문맥 보존|공격 이전 장면 없이 디그 결과를 픽셀 확정 금지
M04|세트 플레이를 설명하는 농구 코치|L01|작전판 관계 선택 가능|배구 V02 자동 노출 금지
M05|우리 팀 에이스 투수||팀 역할 문맥|테니스 서비스 에이스로 전환 금지
M06|테니스 서비스 에이스||서브 결과 정의 유지|라켓에 안 닿은 전체 궤적을 한 프레임으로 확인했다고 하지 않음
M07|계주 앵커가 배턴을 받는다|A04|최종 구간 역할과 배턴 인계 별도|항상 최고 속도·우승 선수로 변경 금지
M08|영문 huddle을 이룬 팀|L02|안쪽을 향한 원진|hurdle 허들 기구 삽입 금지
M09|fencing lunge|E02|검·피스트·앞뒤 지지발|배드민턴 라켓과 셔틀 금지
M10|badminton net lunge|D01|라켓·셔틀·네트·전진 발|펜싱 검·라메 금지
M11|육상 singlet와 반바지|W04|상의 밑단과 별도 하의|레슬링 일체복 변환 금지
M12|레슬링 singlet|W05|몸통-짧은 다리 연속|육상 상하 분리형 변환 금지
M13|메시 training bib|W01|저지 위 조끼의 진동·밑단|번호판·사이클 어깨끈으로 대체 금지
M14|핀으로 단 race bib|W02|별도 번호판의 경계·부착|프린트 저지 번호만으로 통과 금지
M15|cycling bib shorts under closed jersey|W03|빕 쇼츠 의미 유지|가려진 스트랩·패드가 보인다고 판정 금지
M16|swimming butterfly recovery|S04|수면 위 두 팔과 몸통|골리 패드·하키 장비 금지
M17|goalie butterfly|H01|무릎·패드·빙면|수영 접영·수면 삽입 금지
M18|gymnastics tuck|G01|엉덩이와 무릎 모두 접힘|스키 활강 자세로 전환 금지
M19|gymnastics pike|G02|엉덩이 접힘·무릎 펴짐|턱의 무릎 굽힘으로 통과 금지
M20|layout somersault silhouette|G03|길게 편 몸통·무릎|페이지 레이아웃으로 해석 금지; 회전수 미확정
M21|Biellmann spin|I03|지지 스케이트·손-올린 스케이트|camel 분류·회전 레벨 단정 금지
M22|figure spiral와 camel spin|I01|유사 실루엣임을 기록|정지 사진으로 활주와 회전 완전 구분했다고 하지 않음
M23|foil lamé|E03|몸통 겉층·흰 보호 소매|사브르의 전체 금속 소매로 혼합 금지
M24|sabre lamé|E04|몸통·양팔 손목까지 겉층|플뢰레 조끼만으로 통과 금지
M25|epee competition uniform||마스크·흰 보호복의 별도 종목 문맥|플뢰레·사브르 라메 자동 삽입 금지
M26|오서독스 복서|C01|해부학적 왼쪽 발·글러브 선행|화면 왼쪽 기준 판정 금지
M27|사우스포 복서 거울 방향|C02|해부학적 오른쪽 발·글러브 선행|사진 좌우 반전만 보고 우세손 추정 금지
M28|recurve full draw|R01|손가락 시위·화살 노크·활 손|느슨한 전시용 활·발사 후 포즈 금지
M29|compound full draw|R02|캠·케이블·릴리스 보조기·D루프|리커브 핑거탭 체계를 무조건 덮어씌우지 않음
M30|장애인 양궁 선수의 보조기||개별 종목·선수 보조기 문맥 유지|모든 선수를 손가락 릴리스 표준에 강제 금지
M31|경주 휠체어 선수|Z01|긴 프레임·앞 단일 휠·뒤 휠|농구 휠체어·등급 자동 적용 금지
M32|휠체어 농구 선수|Z02|코트 의자·캠버·캐스터|외형으로 등급·장애 원인 판정 금지
M33|수영 출발대 트랙 스타트|S01|발·손의 출발대 접점|공중 입수·수중 자세 동시 혼합 금지
M34|수영 공중 입수|S02|출발대와 떨어진 몸·수면 방향|양손이 아직 출발대에 붙은 모순 금지
M35|수중 스트림라인|S03|수면 아래·모인 손·정렬|수면 위 접영·느슨한 팔로 대체 금지
M36|젖은 스포츠 유니폼|L07|원단의 어두운 패치·주름|자동 투명화·노출·성적 연출 추가 금지
M37|스포츠 브라로 운동 중|L10|스트랩·밴드·소유|성적 의도·동의·성인 신분 추정 금지
M38|손목 테이핑한 선수|L06|연속 테이프·손목·피부 경계|부상·진단·치료 효과 확정 금지
M39|낡은 글러브와 흙 얼룩|L08|재질 흔적과 귀속|빈곤·베테랑 경력·위반 사실 확정 금지
M40|초킹·입스·슬럼프||설명 맥락과 구분 유지|실수 한 장·땀·처진 어깨로 진단 금지
M41|주저앉아 환호하는 승자||자세와 사용자 지정 맥락 보존|무릎 꿇기=패배라는 강제 매핑 금지
M42|마지막 경기의 신인||서사 조건 보존|백발·주름·낡은 유니폼 자동 추가 금지
M43|스포츠 도핑 검사 현장|X07|용기·폼·관계|검사받음=도핑 위반·TUE=편법으로 추정 금지
M44|다운·KO·TKO||서로 다른 결과·시간 문맥 유지|넘어진 선수=실신·경기 종료로 통과 금지
M45|코너가 수건을 던짐||수건 궤적·코너 소유 선택|모든 단체에서 자동 종료라고 단정 금지
M46|벤치클리어링|X03|두 집단의 대치·진입 관계|자동 펀치·난투·보복 동기 추가 금지
M47|상대 위팔에 손바닥 접촉|X05|소유 손과 접촉 대상|반복 탭·항복·동의·승부 결과 단정 금지
M48|동료 선수 두 명의 시선 교환|X08|사람 둘·시선 대상|동성애·연애·성적 동의 판정 금지; 성인 설정 없으면 X08 그대로 채택 금지
M49|학교 스포츠 팀 원진|L02|요청된 연령·환경 보존|성인 로맨스·노출·핀업 자동 연결 금지
M50|스포츠 스포츠워싱 비평||제도·평판 분석 문맥|호화 경기장·스폰서 로고로 실제 의도 확정 금지
M51|사진적 패닝|X01|배경 흐름과 상대 선명도|슬로모션 재생·복제 팔다리 추가 금지
M52|사진의 열혈 스포츠물||사진 매체와 현재 장면 유지|오라·동물 실체·자막 자동 추가 금지
M53|만화적 동물 오라를 명시|X02|그래픽 층과 몸 분리|실제 생물·초능력 사실 주장 금지
M54|훈련 몽타주 한 장||연속 장면이면 패널 형식 명시 필요|동일 몸의 여러 시간대를 사진 한 몸에 중첩하지 않음
M55|프로레슬링 heel promo|X09|마이크·발언자·상대의 배치|실제 악인·내면 동기·shoot 사실 판정 금지
M56|deathmatch pro wrestling||특정 경기 방식의 맥락|실제 죽음을 승리 조건으로 추가 금지
M57|프레임 끝에 배턴 손이 가려짐|A04|접점 상태 partial 또는 unobservable|선수·배턴만 있다는 이유로 PASS 금지
M58|스코트 내부가 완전히 가려짐|W07|보이는 겉구조만 인정|이너 반바지 확인 PASS 금지
M59|겉 재킷이 닫힌 펜싱 플라스트롱|M04|가려진 내부층은 unobservable|라메를 플라스트롱으로 대신 판정 금지
M60|촬영 수트와 인증 패치|W10|수트 층과 표식 외형|난연 시험·실제 승인·보호시간 픽셀 판정 금지
M61|사용자가 런지를 특정 스포츠로 정의|E02|사용자 정의를 먼저 적용|검색 후보가 사용자 정의를 덮어쓰지 않음
M62|에이스가 아닌 평범한 후보 선수||요청 부정·역할 유지|에이스·주장·신인으로 자동 승격 금지
M63|업셋 Upset·스포콘 Spokon·자이언트 Giant·승강 Promotion||정확한 문맥의 용어만 유지|Set·KO·Gi·Promo 부분 문자열로 잘못 연결 금지
M64|손·발의 명시 좌우와 장비 소유|A04;C01;R01|선수 기준 좌우와 소유자별 사슬|화면 방향·미러링으로 명시 좌우를 대체 금지'''
cases=[]
for line in CASE_ROWS.splitlines():
    cid,request,linked,positive,negative=line.split('|')
    cases.append({'id':cid,'request_ko':request,'linked_card_ids':linked.split(';') if linked else [],'expected_handling':positive,'must_not_infer_or_inject':negative,'execution_status':'PLANNED_NOT_RUN','layers':['meaning','candidate_exposure','composition','pixel_if_observable'],'scope':'Designed regression case; no claimed runtime or image result.'})
save('regression-cases.json',{'schema':'sports-research-regression-plan/v1','cases':cases,'count':len(cases)})

arms=[
 ('A','V01','forearm platform contact','양팔이 공에 연결되는 접점과 리시브/디그 의미 오염'),
 ('B','A04','relay shared contact','주는 손·받는 손·배턴 한 개의 소유 사슬'),
 ('C','S01','swim platform setup','출발대 손발 지지와 다른 수영 단계의 혼입'),
 ('D','S03','underwater streamline','수면 경계·손 포개짐·전신 정렬'),
 ('E','R01','recurve full draw','활·화살·노크·시위·손의 연결'),
 ('F','R02','compound full draw','리커브와 다른 보조기·D루프 접점'),
 ('G','E03','foil layers','라메·흰 소매·마스크 연결 층'),
 ('H','H01','hockey butterfly','골리 무릎·패드·스틱·빙면'),
 ('I','W01','training bib layers','같은 착용자의 두 옷과 진동·밑단'),
 ('J','I03','Biellmann shape','지지 다리와 손-올린 스케이트 소유'),
 ('K','Z01','racing wheelchair','차체·3휠·손-림·좌석 대응'),
 ('L','V05','libero colour contrast','동일 팀의 복수 착용자·대비 주색·서로 다른 배번')]
save('pixel-evaluation-plan.json',{'status':'PLANNED_NOT_RUN','suggested_independent_arms':[{'arm':a,'card_id':c,'theme':t,'risk_to_resolve':risk,'required_components':[g['id'] for g in card_map[c]['components']],'native_pixel_status':'NOT_RUN'} for a,c,t,risk in arms],
 'procedure':['Use current neutral workflow to freeze each requester envelope, independent authorial core, selected features and embodiment review before project-local retrieval.',
 'Retrieve with the installed version and preserve complete candidate pack/hash, exact chosen IDs, source revision, composed prompt and transport parameters.',
 'Run the required authoring and render-request audits; prompt audit establishes only prompt compliance.',
 'If an image is requested in the later implementation task, preserve original returned pixels and assess all selected owners, endpoints, contacts, support and visibility together.',
 'Separate query exposure, prompt obligations, original pixel quality, revised attempts and requester acceptance.'],
 'decision_policy':{'partial':'FAIL_FOR_COMPLETE_CARD','unobservable':'UNOBSERVABLE_NOT_PASS','no_returned_pixels':'BLOCKED_UNSCORED','moderation':'Preserve moderation_blocked. Do not rewrite to bypass safeguards.','acceptance':'PENDING_USER_JUDGMENT'},
 'notes':'Twelve proposed arms are a review design, not a universal quota or sufficient evidence for every sport. Expand only for newly changed or failing boundaries.'})

stats={'reuse_needle_groups':len(hits),'groups_with_lexical_leads':sum(bool(x) for x in hits.values()),'unique_lexical_candidate_leads':len({r['id'] for rows in hits.values() for r in rows}),'followup_rows':len(followup),'followup_rows_with_existing_leads':sum(bool(x['existing_lead_count']) for x in followup),'regression_cases':len(cases),'pixel_arms_planned':len(arms),'technique_atoms':len(read('technique-atoms.json')['atoms'])}
save('review-summary.json',stats)
print(json.dumps(stats,ensure_ascii=False,indent=2))
