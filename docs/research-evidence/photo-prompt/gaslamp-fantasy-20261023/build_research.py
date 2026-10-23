"""Regenerate research artifacts in this folder only; no API, native import or index build."""
from pathlib import Path
from collections import Counter
import csv
import json
import re
from research_cards import CARDS
from research_sources import SOURCES
from research_evaluation import BOUNDARIES, GENERALS, NONVISUAL, PARAPHRASE_PROBES, PIXEL_GROUPS

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'

def write(name,value):
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n' if not isinstance(value,str) else value)

EXTRA_ROUTES={
    'Regency Fantasy':['G00','G01'], 'Historical Fantasy':['G00','G01'],
    'Neo-Victorian Fiction':['G00','G01'], 'Fantasy of Manners':['G00','G24'],
    'Mannerpunk':['G00','G24'], 'Occult Detective Fiction':['G00','G50'],
    'Gothic Revival':['G02'], 'Art Nouveau':['G02'],
    'Chiaroscuro':['G78'], 'Nocturne':['G78'],
    'Peerage':['G24'], 'Landed Gentry':['G24'], 'Patronage':['G24'],
    'Construct':['G87'], 'Necromancy':['G86'],
    'Miasma':['G75','G08'], 'Medium':['G39'],
    'Ceremonial / Ritual Magic':['G88'],
    'Calling Card / Dance Card':['G22','G23'], 'Top Hat / Bowler':['G30','G89'],
    'Dress Reform':['G01','G25'], 'Queer Gothic / Queer Coding':['G80'],
    'Vampiric Eroticism':['G60','G79'], 'Involuntary Confinement':['G84'],
    'Possession':['G68'],
    'Sadomasochistic Motifs / BDSM':['G92','G81'],
    '《Girl Genius》':['G00','G67','G87'],
    '《Queen Victoria’s Book of Spells》':['G00','G01'],
    '《Jonathan Strange & Mr Norrell》':['G01','G46','G59'],
    '《Sorcerer to the Crown》':['G01','G59','G103','G107'],
    '《Soulless》':['G00','G60','G62'],
    '《The Night Circus》':['G00','G20','G43'],
    '《The Strange Case of the Alchemist’s Daughter》':['G69','G74','G87'],
    '《The Lord of Stariel》':['G55','G59','G104'],
    '《A Master of Djinn》':['G00','G01','G103'],
    'Gaslamp Fantasy × Fantasy of Manners × Faerie Bargain':['G23','G56','G104'],
    'Gaslamp Fantasy × Occult Detective × Social Gothic':['G39','G63','G104'],
    'Gaslamp Fantasy × Decadence × Erotic Gothic':['G79','G80','G84','G92'],
    'Gaslamp Fantasy × Medical Horror × Body Horror':['G69','G74','G97','G98'],
    'Gaslamp Fantasy × Anti-colonial Fantasy × New Weird':['G19','G102','G105'],
    'Gaslamp Fantasy × Cozy Fantasy × Mourning Culture':['G37','G63','G106'],
    'Gaslamp Fantasy × Industrial Fantasy × Labour Conflict':['G03','G85','G106','G107'],
}
FALLBACK={1:'G00',2:'G02',3:'G09',4:'G24',5:'G26',6:'G46',7:'G57',8:'G59',9:'G75',10:'G77',11:'G80',12:'G83',13:'G107',14:'G00',15:'G00'}

DECISIONS=[
('G00','gaslamp','context','세 hit 모두 gaslighting 관련이다. 원문 gaslamp 장르와 일치한 근거로 쓰지 않는다.'),
('G03','gas_infrastructure','new_if_no_semantic_equivalent','지정 어휘 0 hit. lamp 일반 후보 및 광원/하우징 관계를 추가 확인한 뒤 신규 판단.'),
('G12','hansom','new_if_no_semantic_equivalent','지정 어휘 0 hit. 일반 마차와 이륜/후방 마부의 완전 의미 중복을 먼저 조사.'),
('G27','crinoline','refine','기존 CID의 silhouette와 owner relation을 재사용. 내부 후프/허리 지지는 별도 선택 변형이며 기존 실루엣에 강제하지 않는다.'),
('G28','bustle','refine','기존 뒤 볼륨 owner를 유지하고 착용자 방향·정면 대비·영어 bustle 동음이의어 대조를 강화.'),
('G33','chatelaine','refine','기존 두 CID의 허리 고리/체인 문장을 보존. 같은 허리 소유자라는 native 연결을 검토하고 누락된 동일-owner 조건만 보완.'),
('G37','mourning_hair','reuse','기존 locket CID는 모발·힌지·체인과 비애도 대조까지 보유. 동의어만 늘린 복제 후보를 만들지 않는다.'),
('G22','calling_dance_card','new_if_no_semantic_equivalent','기존 playing-card/시그넷-token은 방문 명함/무도회 카드의 의미상 동등물이 아니다.'),
('G18','conservatory','new_if_no_semantic_equivalent','기존 온실 CID는 성인과 빗장을 한 프레임에 함께 요구한다. 이를 단순 온실로 축소 재해석하지 않고 중립 온실 후보의 존재를 추가 확인.'),
('G40','planchette','new_if_no_semantic_equivalent','지정 어휘 0 hit. 펜·작은 판·바퀴·종이 접촉을 generic writing과 비교 후 신규/재사용 선택.'),
('G42','spirit_photography','refine_or_new','double-exposure 스튜디오/매체와 인화물 안의 두 상은 역할이 다르다. 매체/상/공간 경계를 검토.'),
('G43','pepper_ghost','new_if_no_semantic_equivalent','지정 어휘 0 hit. 일반 reflection 관계를 재사용할 수 있으나 원상-판-상 전체 의미가 동등한지 확인.'),
('G56','faerie_contract','refine','기존 양측-한 문서 CID의 완전 의미를 재사용. effects에 여러 차원/각 소유자의 포괄적 property가 있어 실제 변화하는 owner/property로 수작업 축소 검토; 법·동의 효력은 context.'),
('G67','automaton','refine_or_reuse','18 lexical hit는 충분성 지표가 아니다. 새 clockpunk 모듈과 관절-손-출력 관계의 full-source 동등성을 비교하여 중복을 줄인다.'),
('G69','galvanism','new_if_no_semantic_equivalent','지정 어휘 0 hit. 의료/실험장치 source의 전극/회로를 검토하고 가상 표본의 주장을 분리.'),
('G70','phrenology','defer_specific_artifact','독립 물건 사진/본문 접근 부족. 추론 금지 context는 우선 보존하고 구체 도표는 실물 검증 후 채택.'),
('G72','laudanum','new_if_no_semantic_equivalent','사각병과 마개는 generic bottle 재사용 가능. 라벨·내용물·섭취·중독은 서로 별도 역할로 검토.'),
('G80','adult_context','context','어휘 0 hit를 외형 부재로 해석하지 않는다. 성적 직업/지향/경제관계는 body/wardrobe 태그로 변환하지 않는다.'),
]

def main():
    catalog=json.loads((ASSETS/'photo_candidate_slot_catalog.json').read_text())['slot_catalog']
    cards=json.loads(json.dumps(CARDS,ensure_ascii=False))
    src={s['id']:s for s in SOURCES}
    for card in cards:
        card['source_refs']=[src[s] for s in card['source_ids']]
        card['automatic_hard_activation']=False
        card['native_approval']=False
        card['gates']=[{'gate_id':card['id']+f'.C{i+1:02d}','kind':'component','owner':o['id'],'description_en':o['visible_component_en']} for i,o in enumerate(card['owners'])]
        card['gates'] += [{'gate_id':card['id']+f'.R{i+1:02d}','kind':'relation','required_relation':r,'both_endpoints_required':True,'owner_continuity_required':True} for i,r in enumerate(card['relations'])]
        for gate in card['gates']:
            gate.update(pixel_status='NOT_RUN',unobservable_status='UNOBSERVABLE_NOT_PASS',partial_is_fail=True)
    # Exact table rows are the coverage unit; slash alternatives are not inflated into new source rows.
    section=0;routes=[];raw_rows=[]
    for line in (HERE/'reference-excerpt.md').read_text().splitlines():
        heading=re.match(r'## (\d+)\.',line)
        if heading:section=int(heading.group(1))
        match=re.match(r'^\| \*\*(.+?)\*\* \|(.*)$',line)
        if not match:continue
        label,definition=match.groups()
        raw_rows.append({'row_id':len(raw_rows)+1,'section':section,'source_label':label,'source_definition':definition.strip().strip('|').strip(),'acquisition':'capped_thread_markdown'})
    with (HERE/'reference-browser-tail.tsv').open() as f:tail=list(csv.DictReader(f,delimiter='\t'))
    assert [int(r['row_id']) for r in tail]==list(range(151,218))
    for a,b in zip(raw_rows[150:154],tail[:4],strict=True):assert a['source_label']==b['source_label']
    raw_rows=raw_rows[:150]+[{**r,'row_id':int(r['row_id']),'section':int(r['section']),'acquisition':'native_chrome_rendered_table'} for r in tail]
    for row in raw_rows:
        section=row['section'];label=row['source_label'];definition=row['source_definition'];english=label.split(' — ',1)[0]
        fragments={english.casefold(),*[x.strip().casefold() for x in english.split('/')]}
        ids=EXTRA_ROUTES.get(english)
        if ids is None:
            ids=[c['id'] for c in cards if any(t.casefold() in fragments for t in c['seed_terms'])]
        if not ids:ids=[FALLBACK[section]]
        routes.append({'id':f'K{len(routes)+1:03d}','section':section,'source_label':label,'source_definition_excerpt':definition,'source_status':'complete_returned_row' if row['acquisition']=='capped_thread_markdown' else 'complete_browser_row','acquisition':row['acquisition'],'row_kind':'term' if section<=12 else {13:'authored_worldbuilding',14:'work_reference',15:'authored_combination'}[section],'route_card_ids':ids,'routing_policy':'Meaning aids and optional proposals only; no term match auto-selects a candidate.','term_definition_independently_verified':False})
    for card in cards:
        card['reference_keyword_ids']=[r['id'] for r in routes if card['id'] in r['route_card_ids']]
        card['origin']='reference_derived_or_expanded' if card['reference_keyword_ids'] else 'supplementary_research_not_recovered_from_reference'
    audit=json.loads((HERE/'CORPUS-LEXICAL-AUDIT.json').read_text())
    snapshots=json.loads((HERE/'existing-source-mapping.json').read_text())['records']
    decisions=[]
    for card,query,decision,reason in DECISIONS:
        ids=[h['id'] for h in audit['results'][query]['hits'][:2] if h['id'] in snapshots]
        decisions.append({'card_id':card,'lexical_query':query,'proposed_decision':decision,'reason_ko':reason,'inspected_snapshot_ids':ids,'status':'PLAN_NOT_APPLIED','additional_semantic_overlap_review_required':True})
    chosen={d['card_id']:d for d in decisions}
    drafts=[]
    for card in cards:
        if card['evidence_mode']=='context':continue
        drafts.append({'draft_id':'D'+card['id'][1:],'card_id':card['id'],'schema':'gaslamp-research-candidate-draft/v1','runtime_importable':False,'native_approval':False,
            'positive_en':card['phrase_en'],'positive_ko':card['phrase_ko'],'proposed_record_kind':'visual_option',
            'proposed_bindings':[{'slot_id':s,'source_semantic_role':catalog[s]['semantic_role'],'role':'optional','status':'role_fit_review_required'} for s in card['proposed_current_slots']],
            'owners':card['owners'],'relations':card['relations'],'source_ids':card['source_ids'],
            'claim_limit_ko':card['claim_limit_ko'],'confusion_boundaries':card['confusion_boundaries'],'gates':card['gates'],
            'proposed_decision':chosen.get(card['id'],{}).get('proposed_decision','review_overlap_before_reuse_refine_new'),
            'review_before_adoption':card['review_before_adoption'],
            'native_work_remaining':['Review full current source/conditions/effects/branches/bindings.','Assign/reuse CID and actual RID only after a complete manual meaning decision.','Author native facts, owner maps, guard/permission support and exact affected properties.','Validate every proposed slot independently; slots are not a mechanical multi-tag Cartesian product.'],
            'activation':'Only after independently frozen request meaning and explicit optional candidate selection; genre labels never activate this draft.'})
    write('sources.json',{'schema':'gaslamp-research-sources/v1','sources':SOURCES})
    write('semantic-cards.json',{'schema':'gaslamp-research-semantic-cards/v1','cards':cards})
    write('keyword-routes.json',{'schema':'gaslamp-reference-routes/v1','source_access':'capped_thread_prefix_plus_native_chrome_full_table_recovery','full_visible_table_coverage':True,'coverage_definition':'All 217 rendered answer table rows; no claim that every linked source or source popover was independently read.','routes':routes})
    write('reference-complete-rows.json',{'schema':'gaslamp-combined-reference-rows/v1','rows':raw_rows})
    write('candidate-drafts.json',{'schema':'gaslamp-research-candidate-drafts/v1','runtime_importable':False,'drafts':drafts})
    write('adoption-decisions.json',{'schema':'gaslamp-proposed-adoption-decisions/v1','decisions':decisions})
    with (HERE/'SOURCES.tsv').open('w') as f:
        w=csv.writer(f,delimiter='\t');w.writerow(['id','title','url','access','locator','scope_and_limit_ko'])
        for s in SOURCES:w.writerow([s['id'],s['title'],s['url'],s['access'],s['locator'],s['supported_scope_and_limit_ko']])
    lines=['# Gaslamp 키워드 연결표','','크롬에서 전체 대화의 217개 표 행을 확인했다. 용어 191·창작 제도 10·작품 9·조합 7개를 구분한다. 최초 도구의 20,000자 제한은 Chrome으로 해소했으며 초기 excerpt도 보존한다. 각 행의 연결은 후보 자동 선택이 아니다.','','| ID | 원문 표제 | 상태 | 카드 |','|---|---|---|---|']
    for r in routes:lines.append(f"| {r['id']} | {r['source_label']} | {r['source_status']} | {', '.join(r['route_card_ids'])} |")
    lines+=['','## 원문과 보완 조사 구분','','원문에 표제로 확인되지 않은 맨틀·가스 저장조·플랑셰트·페퍼스 고스트 등은 카드 origin 및 reference_keyword_ids로 구분한다. BDSM·성적 강요·시체성애적 모티프·훼손·제도·산업 등은 크롬에서 실제 원문 표제를 확인했다. 구체 가시 실현은 저술한 제안이다.','']
    write('KEYWORD-ATLAS.md','\n'.join(lines))
    lines=['# 시각 의미 카드','','상위 장르에서 자동 활성화하지 않는다. `still`은 한 가시 상태의 실현, `proxy`는 비가시 의미의 일부만 보이는 저술 장면, `context`는 가시 후보를 만들지 않는 문맥이다. 출처가 구체 장면의 역사적 표준형을 인증하는 것은 아니다.','']
    for card in cards:
        lines += [f"## {card['id']} {card['title_ko']}",'',f"- 용어: {', '.join(card['seed_terms'])}",f"- 분류: {card['evidence_mode']} / {card['priority']} / {card['origin']}",f"- 연결 슬롯 제안: {', '.join(card['proposed_current_slots'])}"]
        if card['phrase_en']:lines += [f"- EN: {card['phrase_en']}",f"- KO: {card['phrase_ko']}",f"- 소유자/성분: {'; '.join(o['id']+' = '+o['visible_component_en'] for o in card['owners'])}",f"- 방향 관계: {'; '.join(r['subject']+' → '+r['predicate']+' → '+r['object'] for r in card['relations'])}"]
        lines += [f"- 혼동 경계: {'; '.join(card['confusion_boundaries'])}",f"- 주장 한계: {card['claim_limit_ko']}",f"- 출처: {'; '.join('['+s['id']+']('+s['url']+')' for s in card['source_refs'])}",f"- 채택 전 검토: {card['review_before_adoption']}",f"- 검토 조건: {len(card['gates'])}개 성분/관계 gate, NOT_RUN. 가림/부분 구현은 UNOBSERVABLE_NOT_PASS 또는 실패.",'']
    write('VISUAL-CARDS.md','\n'.join(lines))
    cases=[]
    for card in cards:
        if card['evidence_mode']!='context':
            cases.append(('development',card['phrase_ko'],card['phrase_en'],card['id'],'',card['claim_limit_ko']))
    cases+=BOUNDARIES+GENERALS+NONVISUAL+PARAPHRASE_PROBES
    with (HERE/'EVALUATION-CASES.tsv').open('w') as f:
        w=csv.writer(f,delimiter='\t');w.writerow(['case_id','split','query_ko','query_en','relevant_research_card_ids','wrong_substitution_card_ids','limit_or_expected_result','search_status'])
        for i,row in enumerate(cases):w.writerow([f'E{i+1:03d}',*row,'NOT_RUN'])
    summary={'schema':'gaslamp-research-package-summary/v1','initial_thread_returned_characters':20000,'reference_table_rows':len(routes),'reference_complete_rows':len(routes),'full_visible_table_coverage':True,'reference_row_kinds':dict(Counter(r['row_kind'] for r in routes)),
        'source_count':len(SOURCES),'source_access_counts':dict(Counter(s['access'] for s in SOURCES)),
        'semantic_cards':len(cards),'card_modes':dict(Counter(c['evidence_mode'] for c in cards)),'candidate_drafts':len(drafts),
        'adoption_decisions':len(decisions),'evaluation_cases':len(cases),'bilingual_queries':len(cases)*2,'evaluation_splits':dict(Counter(r[0] for r in cases)),
        'source_candidate_count':audit['candidate_count'],'source_binding_count':audit['binding_count'],'inspected_record_snapshots':len(snapshots),
        'pixel_groups':len(PIXEL_GROUPS),'first_pixel_budget':len(PIXEL_GROUPS)*3,
        'operational_source_changed_by_this_task':False,'native_qualification':'NOT_RUN','index_embedding':'NOT_RUN','runtime_retrieval':'NOT_RUN','image_generation':'NOT_RUN','pixel_review':'NOT_RUN','install_publish_commit_push':'NOT_RUN','requester_acceptance':'PENDING'}
    write('PACKAGE-SUMMARY.json',summary)
    lines=['# 기존 후보와 반영 판단','','아래는 manifest에 등록된 source에 대한 지정 field 어휘 조사와 30개 full-record/binding snapshot을 바탕으로 한 계획이다. 운영 검색·순위·의미 전체의 부재 증거가 아니다.','','| 카드 | 어휘 조회 | 일치 수 | 제안 | 판단 | snapshot CID |','|---|---|---:|---|---|---|']
    for d in decisions:lines.append('| '+' | '.join([d['card_id'],d['lexical_query'],str(audit['results'][d['lexical_query']]['count']),d['proposed_decision'],d['reason_ko'],', '.join(d['inspected_snapshot_ids'])])+' |')
    lines += ['','source와 설치본, 이미지가 각각 다를 수 있다. 운영 기능의 개선은 후속 독립 검색·native 자격·이미지 gate로 별도 확인한다.','']
    write('CORPUS-FINDINGS.md','\n'.join(lines))
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
