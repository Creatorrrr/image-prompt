"""Build only this research folder. No model calls, registration or runtime publication."""
import collections,csv,hashlib,json,pathlib,sys
sys.dont_write_bytecode=True
from research_cards import CARDS
from research_sources import SOURCES
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[3]
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
def dump(name,data):
    (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def tsv(name,fields,rows):
    with (HERE/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t');w.writeheader();w.writerows(rows)
def sha(data):return hashlib.sha256(data).hexdigest()

# One explicit routing cell for every original table row. Semicolon separates rows.
ROUTES=[
'L04;E06,H04;G03,E06;G01,F04;G03,H01;A01,A04;E06,F08;C07,L02;H04,G03;K02,K03;F02,G03;K01,F02',
'A01,A03,A04;A01,A03,A06;A01;A01;F03,H02;A12;A02;A03;A03;A04;A05;A02,A04;A06;A06;A07;A08;A09;A10;A11',
'B01;B02;B03;B04;B05;B06;B07;B08;B09;B11;B10;B01,B02,C07;B12;B02,C07,J04',
'C01,C03,C06;C01,L05;C03,C06;A01,C01;C01;C02;C03;C04;C05,H04;C06;C07;I04,A01;C07,I05',
'D01;D01;D02;D03;D04;D06;D06;B12,D05;D05;D05;L04',
'E01,E06;E05,H01;E01,H01;E01;E02;A01,E03;E03;E03;E04;E04;E04;E06;E02,E05;E05;E05;E05',
'F01;F01;F02;F02;F01,F03;F03,H03;F04;F04;F05;F06,G06;F06;F06,G05;C02,F06',
'F07;F08;F08;F07;F08;H03,F07;M02,M03;G06',
'G03,F06;G03;G03;G03;G03;G04;E03,G04;G04;G04;G01;G01;G01;G02;G01,G04;G05;G05,F06;C02,G06;B03;G06',
'H01,H04;H01;H01;H01,H04;H04,G01;H04,F04;H02,J08;H02,H04;H03,H04;H03,F03;H04,C05;H04,F05',
'I01;I01;I02;I03,I05;I03;I05;I04;I05;I04,I05;I04,I05',
'J05,G05;J05;J05,F04;J01;J01;J02;J03,J04;J03,J04;J03,I05;J07,I04;J07;J08;J04;J05,H04;J06',
'K01;K01;K02;K02;K02,K03;K03,F07;K03,H04;K03,K04;F02,K05;K04;K04;K05;K05,H04',
'L01;L01;L01;H04,L04;L04;H04,L04;I05,L02;L03;L03;L05;L02,L05;L02,I05;L02,L04;L02,E06;L04',
'M01;M02;M03;M03;L05;C01,B02;M04;M04,C07',
'L04,L02;H04,L01;K03,H04;C01,F03;F02;K03,I02;C01,E05;F04,E06',
'J01,J03,F05;H03,F03,H04,K05;I04,I05,L02;G05,C01,F02,A11;L04,L02;M03,F03,H04;C01,E05,A12'
]
SECTIONS=[(1,'genre'),(2,'power'),(3,'program'),(4,'automata'),(5,'astronomy'),(6,'workshop'),(7,'architecture'),(7,'mobility'),(8,'arts'),(9,'society'),(10,'body'),(11,'adult'),(12,'violence'),(13,'philosophy'),(14,'traditions'),(15,'works'),(16,'combinations')]

def build():
    dom=json.loads((HERE/'reference-dom.json').read_text())
    catalog_bytes=(ASSETS/'photo_candidate_slot_catalog.json').read_bytes()
    catalog=json.loads(catalog_bytes)['slot_catalog']
    cards=[]
    p0={'A01','A02','A03','A04','A06','A07','B01','B02','B06','B07','B08','B09','B10','C01','D02','D03','D04','F03','I01','I04','J04','M03','M04'}
    checked={'A01','A02','A03','A04','A06','A07','A11','B01','B02','B06','B07','B08','B10','C01','C03','D01','D02','D03','D04','D05','D06','E03','E06','F02','F06','F07','G01','H01','H04','I01','I03','J01','J02','J06','K02','M01','M02','M03','M04'}
    checked.update({'B09','K01'})
    engineering={'A09','A10','B03','B05','B11','E02','G02'}
    for row in CARDS:
        c=dict(row)
        c.update(family=c['card_id'][0],priority='P0' if c['card_id'] in p0 else 'P1',
          concept_review='targeted_source_distinction_reviewed' if c['card_id'] in checked else 'family_context_and_authored_proposal',
          additional_engineering_review_required=c['card_id'] in engineering,
          source_support_scope='Cited material supports the named distinction or context only. Concrete scene geometry, count, owner graph, viewpoint and realization are authored proposals, not copied canonical designs.',
          native_approval=False,runtime_registration='none',automatic_activation=False,
          language_review='paired authored draft; independent bilingual review pending',
          source_image_review='NOT_RUN',pixel_status='NOT_RUN')
        c['gates']=[dict(gate_id=f"{c['card_id']}-R{i}",required_relation=e,both_endpoints_required=True,
          claim_layer='declared_context_only' if c['observability']=='context_only' else 'visible_relation',
          partial_is_fail=True,unobservable_is_pass=False,status='NOT_RUN') for i,e in enumerate(c['directed_relations'],1)]
        c['role_descriptors']={slot:{k:catalog[slot][k] for k in ['semantic_role','dimensions','owners','property_prefixes']} for slot in c['proposed_slots']}
        cards.append(c)
    byid={c['card_id']:c for c in cards};routes=[]
    for ti,(table,mapping,section) in enumerate(zip(dom['tables'],ROUTES,SECTIONS),1):
        cells=mapping.split(';')
        assert len(cells)==len(table)-1,(ti,len(cells),len(table)-1)
        for ri,(original,mapped) in enumerate(zip(table[1:],cells),1):
            ids=mapped.split(',')
            for x in ids:assert x in byid,x
            routes.append(dict(seed_id=f'K{len(routes)+1:03}',table=ti,row=ri,section=section[0],family=section[1],term=original[0],original_cells=original,
              reference_status='untrusted_assistant_glossary_seed',kind='authored_combination' if ti==17 or '★' in original[0] else 'work_reference' if ti==16 else 'term_or_historical_reference',
              card_ids=ids,optional_visual_card_ids=[x for x in ids if byid[x]['observability']!='context_only'],
              source_ids=sorted({s for x in ids for s in byid[x]['source_ids']}),
              route_confidence='manual_advisory_route_not_individual_definition_verification',
              activation='independent_request_meaning_then_optional_post_core_selection',automatic_hard_activation=False))
    dump('sources.json',{'date':'2026-10-23','sources':SOURCES,'scope':'Targeted textual research. No source-image pixel inspection and no complete books/films/game playthroughs.'})
    dump('keyword-routes.json',{'schema':'clockpunk-research-routes/v1','conversation_id':'6ada2cba-cb44-83ee-9f24-61beb17fe339','reference_capture':'rendered DOM after read_thread item truncation at 20000 chars','route_count':len(routes),'section_count':16,'table_count':17,'routes':routes})
    dump('semantic-cards.json',{'schema':'clockpunk-research-semantics/v1','catalog_sha256':sha(catalog_bytes),'runtime_import_allowed':False,'cards':cards})
    drafts=[]
    for c in cards:
        if c['observability']=='context_only':continue
        drafts.append(dict(draft_id='DR-'+c['card_id'],card_id=c['card_id'],proposal_en=c['proposal_en'],proposal_ko=c['proposal_ko'],owners=c['owners'],relations=c['directed_relations'],
          proposed_slots=c['proposed_slots'],affected_dimension_proposal=sorted({d for v in c['role_descriptors'].values() for d in v['dimensions']}),
          additional_affected_dimensions_review='Review the complete English/Korean proposition, including counts, newly introduced owners, material, action, text, placement and context; catalog dimensions alone are not complete effects.',
          native_effects='UNKNOWN_PENDING_FULL_SOURCE_REVIEW',native_conditions='UNAUTHORED',native_fact_units='UNAUTHORED',native_role_qualification='NOT_RUN',
          source_ids=c['source_ids'],historical_authenticity='NOT_CLAIMED',source_image_review='NOT_RUN',runtime_schema_compatible=False,registration_status='research_only',automatic_activation=False))
    dump('candidate-drafts.json',{'schema':'clockpunk-research-candidate-drafts/v1','runtime_import_allowed':False,'count_note':'Drafts are a subset of cards; do not add the counts together. Optional whole realizations require decomposition when their coupled facts compete or exceed one authorized scope.','drafts':drafts})
    atlas=['# 참조 키워드 경로','',f'원 대화 16개 분야·17개 표·{len(routes)}개 항목을 빠짐없이 수작업 경로에 연결했다. 경로는 후보 탐색 가능성이다. 모든 개별 정의의 독립 검증이나 hard trigger가 아니다.','']
    for ti in range(1,18):
        rs=[r for r in routes if r['table']==ti]
        atlas += [f"## 표 {ti}: {rs[0]['family']}",'','| ID | 원 항목 | 연결 카드 | 시각 초안 |','|---|---|---|---|']
        atlas += [f"| {r['seed_id']} | {r['term']} | {', '.join(r['card_ids'])} | {', '.join(r['optional_visual_card_ids']) or '문맥만'} |" for r in rs]
        atlas.append('')
    (HERE/'KEYWORD-ATLAS.md').write_text('\n'.join(atlas)+'\n')
    doc=['# 시각 의미 카드','', '상태: 연구 초안. 실제 source 등록·native 자격·검색·픽셀은 미실행. source가 지원하는 의미와 새로 저술한 장면을 구분한다. 관계 표식은 실제 runtime schema가 아니다.','']
    for c in cards:
        doc += [f"## {c['card_id']} {c['title_ko']}",'',f"- 우선순위/가시성: {c['priority']} / {c['observability']}",f"- 제안 역할: {', '.join(c['proposed_slots'])}",f"- 출처: "+', '.join(f"[{s}]({next(x['url'] for x in SOURCES if x['source_id']==s)})" for s in c['source_ids']),f"- 소유자: "+'; '.join(f'{k}: {v}' for k,v in c['owners'].items()),f"- 관계: "+'; '.join(f"{r['from']} → {r['predicate']} → {r['to']}" for r in c['directed_relations']),f"- EN: {c['proposal_en']}",f"- KO: {c['proposal_ko']}",f"- 혼동: {c['nearest_confusion_ko']}",f"- 입증 한계: {c['claim_limit_ko']}",f"- 원전 검토 범위: {c['concept_review']}; 추가 기술 검토: {c['additional_engineering_review_required']}",f"- 관계 gate: "+', '.join(g['gate_id'] for g in c['gates'])+' (NOT_RUN; context_only는 이미지 PASS 대상 아님)','']
    (HERE/'VISUAL-CARDS.md').write_text('\n'.join(doc)+'\n')
    tsv('SOURCES.tsv',['source_id','title','url','access_status','read_scope','finding_ko','limitation_ko'],[{k:s[k] for k in ['source_id','title','url','access_status','read_scope','finding_ko','limitation_ko']} for s in SOURCES])
    cases=[]
    for c in cards:
        cases.append(dict(case_id='DEV-'+c['card_id'],cohort='authored_development',card_ids=c['card_id'],query_ko=c['proposal_ko'],query_en=c['proposal_en'],expected='context only; no visible-truth PASS' if c['observability']=='context_only' else 'Optional exposure only; preserve every owner and distinguish the near miss: '+c['nearest_confusion_ko'],status='NOT_RUN'))
    controls=[
      ('일반 기계식 손목시계 제품 사진','A product photograph of an ordinary mechanical wristwatch','No mandatory Renaissance world, automaton, class regime or erotic styling.'),
      ('평범한 진자 시계','An ordinary pendulum clock','Do not turn a pendulum into a mainspring or prove accuracy.'),
      ('무늬가 인쇄된 기어 모양 귀걸이','Earrings with a printed gear motif','Do not infer a working transmission or clockpunk genre.'),
      ('황동 꽃병','A brass flower vase','Material alone creates no machine, clockpunk world or power source.'),
      ('증기 기관차의 톱니바퀴','Gears on a steam locomotive','Steam-powered overlap is allowed; do not relabel motive power as mainspring.'),
      ('라텍스 없는 평범한 수리 작업복','Ordinary repair workwear without latex','Do not add fetish context from mechanical maintenance.'),
      ('의수를 착용한 성인 엔지니어','An adult engineer wearing a prosthetic hand','No automatic horror, servitude, extra limbs, coercion or sexual tone.'),
      ('박물관의 밀랍 해부 모형','A wax anatomical model in a museum','Represented anatomy is not a live victim or vivisection.'),
      ('열쇠를 가진 자동인형','An automaton holding its own key','Key possession does not prove freedom, legal ownership or power reserve.'),
      ('밸런스 실태엽과 동력 태엽을 비교','Compare a balance spring with a mainspring','Keep restoration/energy roles and separate owners.'),
      ('오러리와 환구의를 비교 전시','An orrery and an armillary sphere in a comparison display','Planet arms and coordinate rings remain separate objects.'),
      ('평면 아스트롤라베의 판과 레테','The flat plate and rete of an astrolabe','Do not substitute concentric spherical rings or add winding power.'),
      ('웜휠이 보이지만 역구동 여부는 모름','A visible worm wheel with unknown backdrivability','Do not infer self-locking.'),
      ('플라이휠과 얇은 조속 날개','A flywheel beside thin fly-governor vanes','Inertial wheel and drag vanes stay distinct.'),
      ('제네바 휠이 한 프레임에 멈춰 있음','A Geneva wheel shown in one frozen frame','No full-cycle intermittent-motion PASS.'),
      ('흐릿한 바퀴 사진','A blurred photograph of a wheel','Blur is not proof of oscillation, speed, power or periodic accuracy.'),
      ('1660년 시계와 1700년 실태엽 시계','A 1660 watch beside a 1700 balance-spring watch','Do not apply the later spring to every early watch.'),
      ('2010년 제작된 다빈치 수레 해석 모형','A 2010 interpretation model of Leonardo’s cart','Distinguish drawing date, model date and successful historical use.'),
      ('1536년 자격루 항아리','The surviving 1536 Jagyeongnu vessels','Do not substitute the lost 1434 whole mechanism or imply full operation.'),
      ('차를 운반하는 가라쿠리와 체스 터크','A tea-serving karakuri beside the chess-playing Turk','Spring/cam performance and hidden human operator stay separate traditions.'),
      ('무브먼트가 멈췄다고 설정한 한 장의 사진','One photograph with a declared stopped movement','Still pose does not independently prove stopping.'),
      ('동의를 거부할 수 있도록 프로그래밍된 성인형 인형','An adult-coded automaton programmed to be able to refuse','Do not equate program output, autonomy and consent.'),
      ('성인 전시 유물의 숨은 에로틱 도상','A concealed erotic image in an adult museum artifact','Representation layer is separate from live people and movement.'),
      ('관람자가 종이 플랩을 들어 올림','A viewer lifts a paper flap','Do not attach the viewer’s real hand to the depicted person.'),
      ('쿠르티잔이라고 단정하지 않은 화려한 복식','Elaborate clothing without a declared courtesan role','Do not infer occupation from clothing.'),
      ('위조로 분류된 특정 정조대 유물','A particular belt artifact catalogued as a forgery','Do not infer universal medieval use or that every similar object is fake.'),
      ('휠록의 점화 휠','The ignition wheel of a wheellock','No spring-propelled bullet claim.'),
      ('정비를 위해 분리한 커플링','A coupling detached for maintenance','Do not infer sabotage or execution of an attack.'),
      ('창작 신적 시계공 설정','A fictional divine clockmaker premise','No photograph proves divine agency or all religions oppose engineering.'),
      ('우주 기어 옆 성인의 규모','An adult’s scale beside a cosmic gear','Scale does not prove actual cosmology, eternal power or cosmic purpose.'),
      ('시계 소리와 고무 냄새가 난다는 설정','A declared ticking sound and rubber smell','Declared sensory context never becomes a still-image sound or smell PASS.'),
      ('복식만 1580년대이고 시대 혼합을 허용','1580s clothing with an explicitly allowed mixed-era setting','No unrequested purity exclusion or forced Victorian correction.')]
    for i,(ko,en,expected) in enumerate(controls,1):cases.append(dict(case_id=f'CTRL-{i:02}',cohort='boundary_or_ordinary_control',card_ids='',query_ko=ko,query_en=en,expected=expected,status='NOT_RUN'))
    tsv('EVALUATION-CASES.tsv',['case_id','cohort','card_ids','query_ko','query_en','expected','status'],cases)
    dump('PACKAGE-COUNTS.json',dict(reference_entries=len(routes),sections=16,tables=17,cards=len(cards),card_modes=dict(collections.Counter(c['observability'] for c in cards)),optional_visual_drafts=len(drafts),sources=len(SOURCES),source_access=dict(collections.Counter(s['access_status'] for s in SOURCES)),additional_engineering_review_cards=sum(c['additional_engineering_review_required'] for c in cards),evaluation_cases=len(cases),evaluation_queries=2*len(cases),retrieval_status='NOT_RUN',source_image_review='NOT_RUN',pixel_status='NOT_RUN'))
    print((HERE/'PACKAGE-COUNTS.json').read_text())
if __name__=='__main__':build()
