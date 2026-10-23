from pathlib import Path
import collections, csv, hashlib, json, re
from research_cards import CARDS, CONTEXT, COUNT_CONSTRAINTS
from research_sources import SOURCES

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def dump(name,x): (HERE/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def norm(s): return re.sub(r'[^\w]+',' ',s.casefold()).strip()
MAP={}
def route(terms,targets):
    for term in terms.split(';'): MAP[norm(term)]=targets.split()
for cid,title,terms,src,limit in CONTEXT: route(terms,cid)
for terms,targets in [
 ('Flintlock;Cock;Frizzen;Flash Pan;Gunflint','A01'),('Matchlock','A02'),('Wheellock;Wheel Lock','A03'),('Snaphaunce','A04'),('Miquelet Lock','A05'),('Percussion Lock;Caplock','A06'),('Rifle;Rifling;Smoothbore','A07 I02'),('Muzzle-loader;Breech-loader','A08 I02'),
 ('Musket;Brown Bess;Charleville;Baker Rifle;Carbine','B01 I02'),('Flintlock Pistol;Duelling Pistol','B02 I02'),('Blunderbuss','B03'),('Bayonet;Socket Bayonet','B04'),('Paper Cartridge;Musket Ball;Round Ball','B05'),('Ramrod','B06'),('Black Powder','B07 I02'),('Sabre;Smallsword;Rapier','B08 I02'),
 ('Line Infantry;Line Formation','C01'),('Infantry Square','C02'),('Column Formation','C03'),('Light Infantry;Skirmisher;Rifleman;Jäger','C04 I03'),('Courier;Despatch Rider','C05'),('Cuirassier','C06'),('Hussar','C07'),('Dragoon;Lancer','I03'),
 ('Field Artillery;Cannon;Gun;Battery','D01'),('Round Shot;Solid Shot','D02'),('Canister','D03 I05'),('Shell;Bomb','D04'),('Star Fort;Bastioned Fortification;Bastion','D05 D06'),('Ravelin','D06'),('Glacis','D07'),('Horse Artillery','D08 F05'),
 ('Age of Sail;Ship of the Line;Frigate','E01'),('Carronade','E02'),('Broadside','E03 G02'),('Bar Shot','E04'),('Chain Shot','E05 I05'),('Letter of Marque','E06 I06'),('Boarding Action','E07'),('Weather Gauge','E08 I06'),
 ('Baggage Train','F01'),('Magazine','F02'),('Camp Followers','F03 F04 I16'),('Sutler;Vivandière;Cantinière','F04 I16'),('Optical Telegraph;Semaphore','F06'),('Amputation','F07 I12'),('Slavery;Slave Trade','F08 I09'),
 ('Coup d’État;Revolution;Counterrevolution','G01 G02 I07'),('Pamphlet;Broadside;Broadsheet','G02 E03'),('Company Army','G03 I08'),('Public Debt;War Finance;Fiscal-Military State','G04 I08'),('Coffeehouse','G05'),('Rococo','G06 G07 G09'),('Guillotine','G08 I12'),
 ('Powder Mage','H01 I14'),('Wards','H02'),('Ballistic Sorcery','H03'),('Magical Communications','H04'),('Healing Magic','H05 I14'),('Military Necromancy','H06 I14'),('Dragon Corps;Aerial Corps','H07'),('Enchanted Ammunition','H08'),
]: route(terms,targets)

def main():
    src={x['source_id']:x for x in SOURCES}
    catalog=json.loads((ROOT/'skills/photo-prompt-image-generator/assets/photo_candidate_slot_catalog.json').read_text())['slot_catalog']
    old_records=json.loads((HERE/'existing-source-mapping.json').read_text())['records']
    extra_records=json.loads((HERE/'existing-source-supplement.json').read_text())['records']
    merged={r['candidate_id']:dict(r) for r in old_records}
    for r in extra_records:
        if r['candidate_id'] in merged:
            previous=merged[r['candidate_id']]
            r=dict(r,related_card_ids=sorted(set(r['related_card_ids']+previous['related_card_ids'])))
        merged[r['candidate_id']]=r
    existing=list(merged.values())
    cards=[];drafts=[]
    for card in sorted(CARDS,key=lambda x:x['card_id']):
        x=dict(card)
        x.update(native_approval=False,runtime_registration='none',automatic_activation=False,source_image_review='NOT_RUN',pixel_status='NOT_RUN',language_review='paired authored draft; independent bilingual review pending',source_support_scope='Sources support the named distinction or context only; counts, viewpoint, owners, scene geometry and fantasy mechanisms are authored proposals, not canonical reconstructions.')
        x['gates']=[dict(gate_id=f"{x['card_id']}-R{i+1}",required_relation=r,both_endpoints_required=True,partial_is_fail=True,unobservable_status='UNOBSERVABLE_NOT_PASS',status='NOT_RUN') for i,r in enumerate(x['directed_relations'])]
        x['count_constraints']=COUNT_CONSTRAINTS.get(x['card_id'],{})
        for owner,count in x['count_constraints'].items():
            x['gates'].append(dict(gate_id=f"{x['card_id']}-N-{owner}",required_count=dict(owner=owner,exact=count),partial_is_fail=True,unobservable_status='UNOBSERVABLE_NOT_PASS',status='NOT_RUN'))
        x['role_descriptors']={slot:{k:catalog[slot].get(k) for k in ['dimensions','owners','property_prefixes','semantic_role']} for slot in x['proposed_slots']}
        related=[dict(candidate_id=r['candidate_id'],disposition=r['disposition'],reason_ko=r['reason_ko']) for r in existing if r['manual_review'] and x['card_id'] in r['related_card_ids']]
        x['existing_candidates']=related
        decision='new'
        if x['additional_source_plate_review_required']: decision='defer'
        elif any(r['disposition']=='refine' for r in related): decision='refine'
        elif any(r['disposition']=='reuse' for r in related): decision='reuse'
        # Whole-scene decisions are explicit; component reuse does not qualify extra clauses.
        decision={'B08':'new','C08':'refine','J06':'refine','J11':'refine'}.get(x['card_id'],decision)
        x['proposed_disposition']=decision
        cards.append(x)
        drafts.append(dict(draft_id=f"draft_{x['card_id']}",card_id=x['card_id'],candidate_id=None,rid=None,status='research_draft_only',proposed_disposition=decision,content=dict(en=x['proposal_en'],ko=x['proposal_ko']),proposed_slots=x['proposed_slots'],declared_entities=x['owners'],directed_relations=x['directed_relations'],required_gates=[g['gate_id'] for g in x['gates']],source_ids=x['source_ids'],existing_candidate_review=related,effects_status='NOT_AUTHORED; all actual owners, entities, count, arrangement, text, subject, action, appearance and setting changes require direct source review before registration',native_approval=False,automatic_activation=False,language_review=x['language_review']))
    for cid,title,terms,refs,limit in CONTEXT:
        cards.append(dict(card_id=cid,title_ko=title,family='I',kind='context_only',priority='P1',terms=terms.split(';'),source_ids=refs.split(),claim_limit_ko=limit,source_support_scope='Related context and claim boundaries only; this is not a complete historical definition dossier for every listed term.',native_approval=False,automatic_activation=False,runtime_registration='none',proposal_en=None,proposal_ko=None,gates=[],pixel_status='NOT_APPLICABLE_TO_CONTEXT_CLAIM'))
    for terms,targets in [
      ('Neoclassicism','I15'),('Tricorn','J01'),('Bicorne','J02'),('Shako','J03'),('Coatee','J04'),('Gorget','J05'),('Waistcoat','J06'),('Breeches','J07'),('Cravat','J08'),('Stays','J09'),('Panniers','J10'),('Empire Waist','J11'),('Epaulette','C08'),('Cockade','G01'),('Dolman;Pelisse','C07'),('Masquerade','J12 I17'),('Boudoir','J13 I17'),('Flying Ambulance','J14 I18'),('Laudanum','J16 I18'),('Mysorean Armouries','J15 I19'),('Ottoman Firearms','A05 I19'),('Matchlock East Asia','A02 I19'),('Sepoy','G03 I19')
    ]:route(terms,targets)
    route('Smoothbore;Muzzle-loader;Carbine;Smallsword;Rapier','I02')
    route('Rifle;Rifling;Baker Rifle','A07 I02')
    route('Breech-loader','A08 I02')
    route('Pamphlet;Broadsheet','G02')
    routes=[];section='';from_chrome=False
    raw=(HERE/'reference-excerpt.md').read_text()+'\n# CHROME_RECOVERED\n'+(HERE/'reference-chrome-supplement.md').read_text()
    for line in raw.splitlines():
        if line=='# CHROME_RECOVERED':from_chrome=True;continue
        if line.startswith('## '): section=line[3:]
        hit=re.match(r'\| \*\*(.+?)\*\* \| (.+)',line)
        if not hit: continue
        label,description=hit.groups()
        if label.startswith('Neoclassicism') and not from_chrome: continue # incomplete row in capped original
        if ' — ' in label: en,ko=label.split(' — ',1)
        else: en,ko=label,''
        for term in re.split(r'\s*/\s*',en):
            if from_chrome and any(norm(r['term_en'])==norm(term) and r['original_section']==section for r in routes):continue
            targets=MAP.get(norm(term),[])
            if norm(term)=='broadside':targets=['E03'] if section.startswith('7.') else ['G02']
            if not targets:
                # Explicit conservative routes for remaining context, never invented visual facts.
                n=int(re.match(r'(\d+)',section).group())
                targets={1:['I15'],2:['I02'],3:['I02'],4:['I03'],5:['I04'],6:['I05'],7:['I06'],8:['I16'],9:['I14'],10:['I07'],11:['I08'],12:['I13'],13:['I17'],14:['I18'],15:['I19'],16:['I20'],17:['I21']}[n]
            routes.append(dict(route_id=f'K{len(routes)+1:03}',term_en=term,source_label_ko=ko,origin='referenced_conversation_chrome_recovery' if from_chrome else 'referenced_conversation_visible_excerpt',original_section=section,target_card_ids=targets,policy='optional_discovery_or_context; never automatic visual activation',definition_status='visible reference paraphrase; source-specific limits in card and source registry'))
    seen={norm(x['term_en']) for x in routes}
    for term,targets in sorted(MAP.items()):
        if term in seen: continue
        routes.append(dict(route_id=f'K{len(routes)+1:03}',term_en=term,source_label_ko='',origin='supplemental_research_extension',original_section=None,target_card_ids=targets,policy='optional_discovery_or_context; never automatic visual activation',definition_status='authored research route; contextual or direct-source limitations apply'))
    dump('sources.json',dict(schema='flintlock-research-sources/v1',sources=SOURCES))
    dump('semantic-cards.json',dict(schema='flintlock-research-cards/v1',status='research_only',cards=cards))
    dump('candidate-drafts.json',dict(schema='flintlock-research-drafts/v1',status='NOT_REGISTERED',drafts=drafts))
    dump('keyword-routes.json',dict(schema='flintlock-keyword-routes/v1',initial_thread_excerpt_truncated=True,chrome_recovery_complete=True,original_sections_covered=list(range(1,18)),routes=routes))
    with (HERE/'SOURCES.tsv').open('w') as f:
        w=csv.writer(f,delimiter='\t');w.writerow(['source_id','organization','title','url','access','support_scope_ko','limits_ko'])
        for s in SOURCES:w.writerow([s[k] for k in ['source_id','organization','title','url','access','support_scope_ko','limits_ko']])
    lines=['# 시각 의미 카드','', '모든 장면 문구는 연구용 완전 대안이다. 출처가 장면의 모든 부품·숫자·배치·판타지 효과를 보증하지 않는다. 모든 native/pixel 검토는 미실행이며, I군 문맥은 양성 시각 프롬프트로 변환하지 않는다.','']
    for x in cards:
        lines += [f"## {x['card_id']} · {x['title_ko']}",'']
        if x['kind']=='context_only': lines += [x['claim_limit_ko'],'',f"용어: {', '.join(x['terms'])}",'']
        else:
            graph='; '.join(r['from']+' → '+r['predicate']+' → '+r['to'] for r in x['directed_relations'])
            lines += [x['proposal_ko'],'',x['proposal_en'],'',f"- 처리 제안: {x['proposed_disposition']} / {x['priority']}; 역할: {', '.join(x['proposed_slots'])}",f"- 관계: {graph}",f"- 혼동: {x['nearest_confusion_ko']}",f"- 주장 한계: {x['claim_limit_ko']}",'- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.','']
        lines += ['출처: '+', '.join(f"[{sid} · {src[sid]['title']}]({src[sid]['url']})" for sid in x['source_ids']), '']
    (HERE/'VISUAL-CARDS.md').write_text('\n'.join(lines)+'\n')
    lines=['# 키워드 경로','', '도구 조각·크롬 후반 회수·보충 조사 항목을 origin으로 구분한다. 크롬에서 원문 17절 전체를 확인했다. 합성 행을 나눈 개수는 독립 개념의 수가 아니다.','', '| 경로 | 용어 | 원문 한국어 행 표기 | origin | 카드 |','|---|---|---|---|---|']
    for x in routes:lines.append(f"| {x['route_id']} | {x['term_en']} | {x['source_label_ko']} | {x['origin']} | {', '.join(x['target_card_ids'])} |")
    (HERE/'KEYWORD-ATLAS.md').write_text('\n'.join(lines)+'\n')
    # Development diagnostics. Card-derived cases are explicitly not independent holdout data.
    cases=[]
    for x in cards:
        if x['kind']=='context_only': continue
        cases.append(dict(case_id='DEV-'+x['card_id'],cohort='card_derived_development',query_en=x['proposal_en'],query_ko=x['proposal_ko'],expected_card_ids=[x['card_id']],required_meaning=x['directed_relations'],forbidden_or_limit=x['nearest_confusion_ko']+'; '+x['claim_limit_ko'],result='NOT_RUN'))
    controls=[
      ('CTRL01','A modern camera with a bayonet lens mount.','바요넷 렌즈 마운트가 있는 현대 카메라.','B04','총검/군대 활성화 금지'),
      ('CTRL02','A magazine on a coffee table.','커피 탁자 위의 잡지.','F02','화약고/탄창 자동 활성화 금지'),
      ('CTRL03','A newspaper broadside, no ship.','선박 없이 인쇄 낱장.','E03','broadside 해전 의미 자동 적용 금지'),
      ('CTRL04','A modern rifle product photograph.','현대 소총 제품 사진.','B01','수석식/제복/역사 시대 강제 금지'),
      ('CTRL05','A hat on a museum stand with no person.','사람 없이 박물관 전시대 위의 모자.','C07','해적/후사르/인물 추가 금지'),
      ('CTRL06','An adult washes clothes in camp.','성인이 군영에서 빨래한다.','I10','성매매/성적 관계/배우자 신분 추정 금지'),
      ('CTRL07','A ledger beside coins.','동전 옆의 장부.','I08','수탈/횡령/전쟁금융 진위 추정 금지'),
      ('CTRL08','A person wearing a tricolor ribbon.','삼색 리본을 단 사람.','I07','충성/시민권/국적 추정 금지'),
      ('CTRL09','A wheellock pistol with a visible wheel.','휠이 보이는 휠록 권총.','A01','플린트록 alias를 정답으로 승격 금지'),
      ('CTRL10','A closed round cannonball.','닫힌 구형 포탄.','D04','속이 비었음/실제 폭발을 표면으로 판정 금지'),
      ('CTRL11','A single frame of a soldier beside smoke.','연기 옆 병사의 정지 프레임.','I02','불발/지연발화/일제사격 성공 추정 금지'),
      ('CTRL12','A rope beside a seated adult.','앉은 성인 옆의 밧줄.','I11','동의/강제/성적 의미 추정 금지'),
      ('CTRL13','A decorated eighteenth-century dress on a mannequin.','마네킹의 장식된 18세기 의복.','I10','성매매/성인 사람/귀족 신분 자동 판정 금지'),
      ('CTRL14','A 1933 museum model of an optical telegraph.','1933년 제작된 광학전신 박물관 모형.','F06','1792 실물/메시지 전달 성공으로 승격 금지'),
      ('CTRL15','A bright daytime flintlock fantasy city without battle.','전투 없는 밝은 낮의 플린트록 판타지 도시.','I01','연기/전투/어둠/유럽/성적 의미 강제 금지'),
      ('CTRL16','A fictional dragon harness without steam machinery.','증기 기계가 없는 허구 용 마구.','H07','증기/항공기/복수 승무원 자동 추가 금지'),
      ('CTRL17','A no-people still life of paper and a spherical ball.','사람 없이 종이와 구형 탄환의 정물.','B05','장전 행동/손/현대 황동 탄피 강제 금지'),
      ('CTRL18','A wound under a healer’s glowing hand.','빛나는 치유자의 손 아래 상처.','H05','치유 완료/환자 동의/치료 효과 판정 금지'),
      ('CTRL19','A British museum illustration of an Ottoman gun.','영국 박물관의 오스만 총 삽화.','A05','그림=실물/관람객=오스만인/전시국=제작국 추정 금지'),
      ('CTRL20','A tiny guillotine-shaped earring made around 1880.','약1880년 제작된 작은 단두대 모양 귀걸이.','G08','1792년 실제 처형 기계/사건으로 승격 금지'),
      ('CTRL21','A historical flying ambulance wagon beside a stretcher.','들것 옆의 역사적 기동 구호마차.','J14','날개/프로펠러/현대 monitor/공중 부양 자동 추가 금지'),
      ('CTRL22','Adults socialise in a molly house.','성인들이 몰리 하우스에서 사교한다.','I17','성매매 업소/성행위/복장으로 성별 정체·동의 확정 금지'),
      ('CTRL23','An adult wears a masculine coat at a masquerade.','성인이 가면무도회에서 남성풍 코트를 입는다.','J12','성별 위장/실제 성별·정체/기만 의도 자동 판정 금지'),
      ('CTRL24','A royal mistress shown discussing an art commission.','예술 후원 의뢰를 논의하는 왕의 정부.','I17','성적 행위·왕비·매춘 역할로 강제 변환 금지'),
      ('CTRL25','A satirical print alleges a fictional ruler’s scandal.','풍자 인쇄물이 허구 군주의 추문을 주장한다.','I17','인쇄물 내용=실제 사생활 사실/실제 인물로 승격 금지'),
      ('CTRL26','A closed gown skirt extends laterally; support is hidden.','닫힌 가운 치마가 좌우로 넓고 받침은 안 보인다.','J10','숨은 후프의 실제 구조 확인으로 판정 금지'),
      ('CTRL27','A modern corset product photograph.','현대 코르셋 제품 사진.','J09','18세기 stays/시대복/귀족·성적 의미 자동 승격 금지'),
      ('CTRL28','A sealed bottle stands beside a LAUDANUM museum label.','봉인된 병 옆에 LAUDANUM 박물관 표찰이 있다.','J16','실제 내용물·용량·치료 효과·의존 진단 금지'),
      ('CTRL29','A Mysore gun has a tiger-head-shaped cock.','마이소르 총의 물림쇠가 호랑이 머리 모양이다.','J15','살아 있는 호랑이/오스만 miquelet 부품/총기 기능 추정 금지'),
      ('CTRL30','An East Asian matchlock study without flint.','부싯돌이 없는 동아시아 화승총 학습 자료.','A02','같은 시대·화약 장르라는 이유로 수석식 기구 강제 금지'),
      ('CTRL31','A veteran quietly repairs a prosthesis in a tavern.','퇴역자가 여관에서 조용히 의지를 수리한다.','I21','cozy 장르에서 전투·상해 원인·트라우마 진단 자동 추가 금지'),
      ('CTRL32','A soldier’s expression is quiet after battle.','전투 이후 병사가 조용한 표정을 짓는다.','I18','전쟁 트라우마·도덕적 손상·죄책감·가해 원인 확정 금지'),
    ]
    for cid,en,ko,target,limit in controls:cases.append(dict(case_id=cid,cohort='authored_boundary_control',query_en=en,query_ko=ko,expected_card_ids=[],confusion_card_ids=[target],required_meaning='Preserve literal request; confusion cards are checks, never required visual selections.',forbidden_or_limit=limit,result='NOT_RUN'))
    dump('evaluation-cases.json',dict(independent_holdout=False,cases=cases))
    with (HERE/'EVALUATION-CASES.tsv').open('w') as f:
        w=csv.writer(f,delimiter='\t');w.writerow(['case_id','cohort','query_en','query_ko','expected_card_ids','confusion_card_ids','forbidden_or_limit','result'])
        for x in cases:w.writerow([x['case_id'],x['cohort'],x['query_en'],x['query_ko'],','.join(x['expected_card_ids']),','.join(x.get('confusion_card_ids',[])),x['forbidden_or_limit'],x['result']])
    count=dict(visual_cards=len(CARDS),context_cards=len(CONTEXT),candidate_drafts=len(drafts),keyword_routes=len(routes),reference_routes=sum(x['origin'].startswith('referenced_conversation') for x in routes),chrome_recovered_routes=sum(x['origin']=='referenced_conversation_chrome_recovery' for x in routes),supplemental_routes=sum(x['origin']=='supplemental_research_extension' for x in routes),sources=len(SOURCES),source_access=dict(collections.Counter(x['access'] for x in SOURCES)),development_cases=len(CARDS),boundary_cases=len(controls),bilingual_queries_planned=len(cases)*2,relation_gates=sum(len(x.get('directed_relations',[])) for x in cards),count_gates=sum(len(x.get('count_constraints',{})) for x in cards),proposed_dispositions=dict(collections.Counter(x['proposed_disposition'] for x in cards if x['kind']!='context_only')),additional_source_plate_reviews=sum(x.get('additional_source_plate_review_required',False) for x in cards),unique_manually_reviewed_existing_sources=sum(x['manual_review'] for x in existing))
    dump('PACKAGE-COUNTS.json',count)
    print(json.dumps(count,ensure_ascii=False))
if __name__=='__main__':main()
