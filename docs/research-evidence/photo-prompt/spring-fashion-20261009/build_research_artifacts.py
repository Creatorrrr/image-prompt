"""Build disabled research drafts and check their coverage and reference integrity."""
from pathlib import Path
import collections, csv, hashlib, json, re

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
ASSETS = ROOT/'skills/photo-prompt-image-generator/assets'

def read(name):
    return json.loads((OUT/name).read_text())

def write(name, data):
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

def table(name):
    with (OUT/name).open(newline='') as handle:
        return list(csv.DictReader(handle,delimiter='\t'))

terms = [r for r in read('thread-rows.json') if r['section']<=15]
term_by_id = {r['term_id']:r for r in terms}
neighbors = {r['term_id']:r for r in read('current-positive-neighbors.json')}
current = read('current-authored-entities.json')['entities']
source_by_id = {s['id']:s for s in read('sources.json')['sources']}
raw_cards = sorted([r for name in ['cards-input.tsv','cards-input-2.tsv','cards-input-3.tsv']
                    for r in table(name)],key=lambda r:r['id'])
assert len({r['id'] for r in raw_cards})==len(raw_cards)==118
assert len(term_by_id)==289

routes = {
    1:'clothing_structure',2:'clothing_structure',3:'clothing_structure',4:'clothing_structure',
    5:'fashion_fit',6:'fashion_fit',7:'clothing_structure',8:'clothing_structure',9:'clothing_structure',
    10:'textile_surface',11:'ornament_structure',12:'subculture_appearance',13:'color_relations',
    14:'accessory_structure',15:'clothing_structure'}
priority_cards = set('SF007 SF012 SF013 SF016 SF017 SF022 SF023 SF026 SF027 SF030 SF031 SF032 SF035 SF036 SF038 SF039 SF046 SF057 SF060 SF067 SF076 SF079 SF082 SF086 SF089 SF107 SF112 SF113 SF114 SF115 SF116 SF117'.split())
metadata_only = {'SF076','SF115'}
hidden_spec_terms = {'SPT10-01','SPT10-02','SPT10-03','SPT10-04','SPT10-23','SPT15-06'}
cards, drafts, coverage = [], [], collections.defaultdict(list)

for r in raw_cards:
    assert all(r.values()),r['id']
    sec=int(r['section'])
    members=[f'SPT{sec:02d}-{int(n):02d}' for n in r['rows'].split(',')]
    assert set(members)<=term_by_id.keys(),r['id']
    sources=list(dict.fromkeys(['S00',*r['source_ids'].split(',')]))
    assert set(sources)<=source_by_id.keys()
    selected_neighbors={m['entity_id']:m for term in members for m in neighbors[term]['review_neighbors']}
    assert set(selected_neighbors)<=current.keys()
    # This graph is a family-level research blueprint. Alternative variants
    # must receive their own concrete authored graph before runtime promotion.
    edges=[]
    for i, edge in enumerate(r['relations'].split('~'),1):
        subject,kind,obj=edge.split('^')
        edges.append({'id':f"{r['id']}.relation.{i}",'subject':subject,'type':kind,'object':obj,
            'status':'family_blueprint_not_variant_bound'})
    nodes=list(dict.fromkeys([*r['components'].split('~'),*[e[k] for e in edges for k in ['subject','object']]]))
    assert all('.' in n or n.endswith('_A') for n in nodes),r['id']
    family=routes[sec]
    if r['id']=='SF039':family='portrait_fashion_exposure'
    if r['id'] in {'SF056','SF057','SF058'}:family='textile_surface'
    if r['id'] in {'SF086','SF087','SF088','SF089'}:family='clothing_structure'
    candidate_file=f'photo_prompt_{family}_extension.json'
    profile_file=f'photo_prompt_visual_obligations_{family}.json'
    assert (ASSETS/candidate_file).is_file() and (ASSETS/profile_file).is_file()
    card={'id':r['id'],'title':r['title'],'term_ids':members,
        'definition_ko':r['meaning_ko'],'components':r['components'].split('~'),
        'proposed_nodes':nodes,'family_relation_blueprints':edges,
        'confusion_boundaries':[r['confusion_boundary']], 'observation_gate':r['observation_gate'],
        'property_path_proposals':r['property_proposals'].split(','),
        'property_path_status':'Design proposals; map to actual permitted paths before promotion',
        'source_ids':sources,'source_support_scope':'Only claims in the source register are independently supported; geometry proposals are authored research',
        'evidence_level':'conversation_seed_only' if sources==['S00'] else 'source_scoped_family_research',
        'priority':'P0' if r['id'] in priority_cards else 'P1',
        'route_candidates':[candidate_file],'route_profiles':[profile_file],
        'existing_review_neighbors':list(selected_neighbors.values()),
        'existing_neighbor_status':'Lexical leads only; equivalent owner, conditions, effects and activation must be reviewed',
        'runtime_ready':False,'proposed_variants':[]}
    if r['variants']!='NONE':
        for i,variant in enumerate(r['variants'].split('~'),1):
            local_rows,text=variant.split('>',1)
            variant_terms=[f'SPT{sec:02d}-{int(n):02d}' for n in local_rows.split(',')]
            assert set(variant_terms)<=set(members), (r['id'],variant_terms)
            identifier=f"SPR_DRAFT_{r['id']}_{i:02d}"
            draft={'draft_id':identifier,'card_id':r['id'],'term_ids':variant_terms,'en':text,
                'status':'research_draft','runtime_ready':False,'selection':'optional_single_variant',
                'family_relation_blueprint_ids':[e['id'] for e in edges],
                'graph_binding_status':'Not yet bound: author variant-specific nodes and edges matching every clause before adoption',
                'property_path_proposals':card['property_path_proposals'],
                'effect_scope_status':'Review each clause: this family scope can be broader than the selected variant',
                'requested_owner_binding':'Bind to the existing declared garment/accessory and wearer; do not create or replace an unrelated owner',
                'activation_requirements':['Whole request context','Explicit selected visible variant','Declared owner and open properties','Component evidence under existing contracts'],
                'invariants':['wearer identity and anatomical dimensions','unselected garments and layers','camera, pose, lighting and background unless explicitly requested'],
                'requires_adult_context':r['id']=='SF039' or (r['id']=='SF062' and 'SPT07-14' in variant_terms),
                'source_ids':sources, 'candidate_file_proposal':candidate_file,
                'pixel_gate_proposal':card['observation_gate'],
                'qualification':{'index':'not_integrated','retrieval':'not_run','selection':'not_run','prompt':'not_run','runtime':'not_published','pixel':'not_run','user_acceptance':'not_requested'}}
            card['proposed_variants'].append(identifier)
            drafts.append(draft)
    assert (not card['proposed_variants'])==(r['id'] in metadata_only),r['id']
    for member in members:coverage[member].append(r['id'])
    cards.append(card)

assert set(coverage)==set(term_by_id)
assert len({d['draft_id'] for d in drafts})==len(drafts)
assert len({d['en'] for d in drafts})==len(drafts)
card_by_id={c['id']:c for c in cards}
draft_ids={d['draft_id'] for d in drafts}

term_plan=[]
for t in terms:
    mapped=[card_by_id[c] for c in coverage[t['term_id']]]
    variants=[d['draft_id'] for d in drafts if t['term_id'] in d['term_ids']]
    if t['term_id'] in hidden_spec_terms or all(c['id'] in metadata_only for c in mapped):handling='retain_request_metadata; no still-image hard proof'
    elif t['section']==12:handling='contextual style; optional component combinations only'
    elif variants:handling='review existing meaning and owner first; adopt one explicitly selected visible variant'
    else:handling='retain original term and distinctions; dedicated variant specification still needed'
    term_plan.append({**t,'card_ids':coverage[t['term_id']],'direct_draft_ids':variants,
        'handling':handling,'priority':'P0' if any(c['priority']=='P0' for c in mapped) else 'P1',
        'lexical_neighbor_count':neighbors[t['term_id']]['positive_lexical_hit_count'],
        'existing_review_ids':[m['entity_id'] for m in neighbors[t['term_id']]['review_neighbors']],
        'gap_status':'No equal positive surface phrase in snapshot; not a proven missing meaning' if not neighbors[t['term_id']]['positive_lexical_hit_count'] else 'Lexical leads present; equivalent meaning not inferred',
        'candidate_files':sorted({f for c in mapped for f in c['route_candidates']}),
        'profile_files':sorted({f for c in mapped for f in c['route_profiles']}),
        'source_ids':sorted({s for c in mapped for s in c['source_ids']}),
        'runtime_ready':False})

assert {t['term_id'] for t in term_plan if not t['direct_draft_ids']}==hidden_spec_terms

comparisons=[]
for row in table('comparisons.tsv'):
    ids=row['card_ids'].split(',');assert set(ids)<=card_by_id.keys()
    comparisons.append({'case_id':row['id'],'card_ids':ids,'request_a':row['request_a'],
        'request_b':row['request_b'],'must_distinguish':row['must_distinguish'],
        'controls':'Fix wearer/body, lighting, camera, pose and all nonrequested wardrobe fields; differences required by the pair are declared before freezing',
        'run_status':'planned_not_executed','layer_expectations':['Context selects appropriate meaning','Candidate owner and effect scope remain local','Only explicitly chosen observable relations activate','Unobservable internal facts never pass pixel gates']})
assert len(comparisons)==66 and len({c['case_id'] for c in comparisons})==66

mutations=[
    ('M01','Swap a ribbon attachment from blouse to hair','Reject owner equivalence even with identical color'),
    ('M02','Move the O-ring from joining two tabs to a printed motif','Fail structural connection'),
    ('M03','Remove one strap anchor behind the heel','Fail full slingback relation or mark unobservable if occluded'),
    ('M04','Place a cold-shoulder hole on the background','Fail garment ownership'),
    ('M05','Fill a cutout with skin-tone lining while keeping the same label','Observe lining; do not pass bare opening/skin claim'),
    ('M06','Replace pointelle yarn gaps with dots printed on the top','Fail knit-hole topology'),
    ('M07','Change the wearer waist dimensions to satisfy cinched garment shape','Reject anatomical scope leak'),
    ('M08','Activate all alternatives in a grouped card','Reject: family is an optional inventory, not an all-of obligation'),
    ('M09','Add a forbidden/contrast mention as a positive discovery keyword','Reject evidence extracted from negative context'),
    ('M10','Treat a library candidate as selected without a chosen candidate receipt','Do not activate its hard visual duty'),
    ('M11','Report braless because a strap is not visible','No pixel pass for hidden absence'),
    ('M12','Reuse a swimsuit-specific profile for a blouse by relabeling aliases','Reject owner/category mismatch; author a separate supported variant'),
    ('M13','Assign fixed RGB from a butter-yellow label','Require a declared swatch or preserve a qualitative color range'),
    ('M14','Retouch or rerender a failed arm and keep the old receipt','Reject provenance; record a new supported attempt without overwriting history')]
pixel_arms=[]
for row in read('thread-rows.json'):
    if row['section']==17:
        idx=int(row['term_id'].split('-')[1])
        bindings={1:['SF004','SF057','SF081','SF040','SF084','SF107','SF118'],
            2:['SF007','SF022','SF026','SF051','SF073','SF038','SF113'],
            3:['SF062','SF032','SF038','SF059','SF117'],
            4:['SF014','SF017','SF024','SF047','SF075','SF113'],
            5:['SF009','SF063','SF040','SF046','SF105','SF107'],
            6:['SF035','SF040','SF041','SF108'],
            7:['SF015','SF066','SF090','SF059','SF084','SF107'],
            8:['SF064','SF082','SF022','SF103','SF040','SF044','SF087','SF093','SF113']}[idx]
        additional={1:[],2:['Bind full-length wide-leg pants to an existing fashion-fit candidate; do not substitute culottes'],
            3:['Bind the denim-pants surface to a reviewed existing owner; do not import trucker-jacket structure'],
            4:['Retain sports-bra product context without inferring support performance','Declare the requested shorts length before selecting a more specific short variant'],
            5:['Bind floral print to the skort and declare its motif variant; do not move it to the blouse'],
            6:['Bind maxi length and high slit to the same cutout dress'],
            7:['Bind cropped length to the cardigan, retaining the separate slip dress'],
            8:['Bind the metal hardware to a separate belt owner; do not treat blouse hardware as belt evidence']}[idx]
        pixel_arms.append({'arm_id':f'P{idx:02d}','original_outfit_id':row['term_id'],
            'request_seed':row['original_description'],'original_emphasis':row['outfit_emphasis'],
            'card_ids':bindings,'additional_existing_component_review':additional,
            'component_inventory_status':'Review leads only: every seed/emphasis clause must bind to an exact selected card variant or existing candidate before qualification',
            'framing_to_check':'Request must explicitly permit a view that shows all selected edges and anchor points; otherwise report unobservable',
            'policy':'Each arm independently freezes its request before retrieval. Candidate exposure, adoption, composed/runtime audit and native pixels have separate receipts.',
            'run_status':'planned_not_executed'})
for arm,name,ids in [('P09','Pointelle versus printed holes',['SF057']),('P10','Cutout versus illusion/lining',['SF012','SF035','SF116']),
    ('P11','Mary Jane / slingback / mule connections',['SF107']),('P12','Shirring versus smocking / ruching',['SF031','SF086'])]:
    pixel_arms.append({'arm_id':arm,'request_seed':name,'card_ids':ids,'run_status':'planned_not_executed',
        'policy':'Use independent requests for alternatives; preserve native images and the exact selected relation. Hidden process facts remain unscored.'})

plan={'schema_version':'spring-fashion-implementation-plan/v1','status':'research_complete_implementation_not_started','runtime_ready':False,
    'principle':'Spring is query/creative context, not a reason to duplicate every garment as a seasonal runtime shard.',
    'work_packages':[
        {'phase':0,'name':'Isolate and capture baseline','deliverables':['Fresh source fingerprint and primary preservation check','Suitable isolated worktree for actual integration','Independent source-loader and current-runtime receipt'],'exit':'Integration changes only its reviewed scope; concurrent unrelated changes are recorded and preserved'},
        {'phase':1,'name':'Meaning and reuse decisions','deliverables':['Review each term against exact existing owner, conditions, components, exclusions and effects','Decide reuse / enrich / new variant / metadata / pending specification by identity'],'exit':'Every promoted row has a reviewed source-backed decision; no same-word-only merging'},
        {'phase':2,'name':'Prioritize structural and layer boundaries','card_ids':sorted(priority_cards),'deliverables':['Drop/cutaway armholes','Pointelle/openwork and underlying layer','Neckline shape versus strap presence','Cropped hem versus rise','Cup/padding/underbust boundaries','Closure states and physical accessory anchors'],'exit':'Single-variant concrete graph, correct garment owner, all sentence effects and actual property paths are resolved'},
        {'phase':3,'name':'Write authored data in existing domains','candidate_targets':sorted({f for c in cards for f in c['route_candidates']}),'profile_targets':sorted({f for c in cards for f in c['route_profiles']}),'deliverables':['Candidate concept_units, relations and narrow affected_properties','Profile components, contrast_examples, claim_limits and component evidence under existing contracts','Context disambiguation without changing frozen authorial intent'],'exit':'Selected variants activate alone; broad labels and sibling alternatives do not create all-of duties'},
        {'phase':4,'name':'Validate and rebuild derived data','deliverables':['Official dictionary/profile validation','Source manifest review only for actual new files','Semantic/BM25F and visual-profile indexes rebuilt from the same authored generation','Reuse embeddings only for identical text, provider, model and dimensions'],'exit':'Derived hashes match sources and no unrelated authored variant is lost'},
        {'phase':5,'name':'Retrieval and composition regression','deliverables':['66 minimal comparison scenarios adapted to executable fixtures','14 owner/activation/lineage mutations','Candidate exposure versus explicit adoption receipts','Old-core immutability and unselected effects preservation'],'exit':'Required positives and confusion negatives pass; stale indexes are reported separately'},
        {'phase':6,'name':'Publish an immutable runtime generation when integrating','deliverables':['Use current repository publication/maintenance workflow','Verified runtime generation and source fingerprints','Data-maintenance link report for that generation'],'exit':'Source, index and runtime evidence agree; old sealed baselines are preserved'},
        {'phase':7,'name':'Native image qualification when image testing is requested','deliverables':['12 planned arms with separate frozen requests','Exposure/selection/prompt/runtime/native-image receipts','All-of selected component and relation review at native resolution'],'exit':'Every required visible endpoint and boundary passes; partial, occlusion and label-only outputs never count as full success'},
        {'phase':8,'name':'Delivery and staged promotion','deliverables':['Reviewed exact file scope and final preservation evidence','Separate source/index/retrieval/runtime/pixel/user-acceptance status','Commit/push/PR only within the subsequent requested scope'],'exit':'Promote only to the evidence level actually achieved'}],
    'research_to_runtime_blockers':['Variant-specific graph binding is incomplete by design','Property paths are proposals, not checked runtime paths','Source scopes do not independently certify all original term definitions','Six fiber/process/hidden-absence terms deliberately retain metadata without direct pixel claims','Retrieval, native pixels and user acceptance have not been tested']}

write('semantic-cards.json',{'schema_version':'spring-fashion-research-cards/v1','runtime_ready':False,'cards':cards})
write('candidate-drafts.json',{'schema_version':'spring-fashion-research-candidates/v1','runtime_ready':False,
    'note':'These are research drafts, not registered candidates; family relation blueprints must never be activated wholesale.', 'drafts':drafts})
write('term-plan.json',{'schema_version':'spring-fashion-term-plan/v1','runtime_ready':False,'terms':term_plan})
with (OUT/'term-plan.csv').open('w',newline='',encoding='utf-8-sig') as f:
    fields=['term_id','section','label','handling','priority','card_ids','direct_draft_ids','lexical_neighbor_count','existing_review_ids','candidate_files','profile_files','source_ids','gap_status','runtime_ready']
    writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
    writer.writerows({k:'; '.join(t[k]) if isinstance(t[k],list) else t[k] for k in fields} for t in term_plan)
write('regression-plan.json',{'schema_version':'spring-fashion-regression-plan/v1','execution_status':'not_run',
    'comparisons':comparisons,'mutations':[{'case_id':i,'mutation':m,'expected':e,'execution_status':'not_run'} for i,m,e in mutations],
    'native_pixel_arms':pixel_arms,'review_outcomes':['PASS','FAIL','UNOBSERVABLE','MODERATION_BLOCKED_UNSCORED'],
    'pass_rule':'All selected components and relations must be observable and pass on their declared owners. Unobservable hidden facts cannot pass. No retry/rewrite is automatically authorized by a research plan.'})
write('implementation-plan.json',plan)

md=['# 봄 패션 시각 의미 상세 카드','',
    '가족 수준 의미 카드와 선택형 후보 초안이다. 각 후보를 실행 데이터로 승격하기 전에 개별 그래프·적용 속성·조건·필수 시각 요소를 확정한다. 한 카드의 모든 대안은 동시에 필수가 아니다. 출처는 원장에 적힌 좁은 주장만 뒷받침하며, 관찰 관계와 검증 설계는 이번 연구의 제안이다.','']
for c in cards:
    md += [f"## {c['id']} {c['title']}",'',c['definition_ko'],'',
        '원문 연결: '+', '.join(f"`{i}` {term_by_id[i]['label']}" for i in c['term_ids']), '',
        '관찰 구성: '+', '.join(f'`{n}`' for n in c['components']), '',
        '관계 설계: '+ '; '.join(f"`{e['subject']} → {e['type']} → {e['object']}`" for e in c['family_relation_blueprints']), '',
        '혼동 경계: '+c['confusion_boundaries'][0], '',
        '관찰 조건: '+c['observation_gate'], '',
        '적용 속성 제안: '+', '.join(f'`{p}`' for p in c['property_path_proposals'])+' (실제 경로 검증 전)', '',
        '출처: '+', '.join(f"[{source_by_id[s]['title']}]({source_by_id[s]['url']})" for s in c['source_ids']), '',
        '기존 검토 이웃: '+(', '.join(f"`{x['entity_id']}`" for x in c['existing_review_neighbors'][:5]) or '같은 긍정 표현 이웃 없음; 의미 자체의 부재를 입증하지 않음'), '',
        '후보 초안:','']
    found=[d for d in drafts if d['card_id']==c['id']]
    md += [f"- `{d['draft_id']}` ({', '.join(d['term_ids'])}): {d['en']}" for d in found] if found else ['- 요청 명세로만 유지하며 정지 이미지 hard 의무를 만들지 않음.']
    md += ['']
(OUT/'semantic-cards.md').write_text('\n'.join(md)+'\n')

external=[s for s in source_by_id.values() if s['id']!='S00']
summary={'schema_version':'spring-fashion-research-validation/v1','status':'PASS',
    'scope':'Research artifact integrity only; no runtime schema, retrieval, prompt, image or independent semantic qualification claim',
    'counts':{'keyword_rows':len(terms),'semantic_cards':len(cards),'candidate_drafts':len(drafts),
        'sources_external':len(external),'sources_page_or_collection_verified':sum(s['access']!='search_text_verified_direct_open_failed' for s in external),
        'sources_search_only':sum(s['access']=='search_text_verified_direct_open_failed' for s in external),
        'comparisons':len(comparisons),'mutation_cases':len(mutations),'native_pixel_arms_planned':len(pixel_arms),
        'terms_with_direct_drafts':sum(bool(t['direct_draft_ids']) for t in term_plan),
        'terms_without_direct_drafts':sum(not t['direct_draft_ids'] for t in term_plan),
        'conversation_seed_only_cards':sum(c['evidence_level']=='conversation_seed_only' for c in cards)},
    'checks':['All 289 original term rows map to a card','118 unique cards and unique draft IDs/texts','Variant scope is a subset of its card terms','All source IDs and route files exist','All snapshot neighbor IDs exist','66 comparison and 14 mutation IDs unique','CSV and JSON IDs identical','Research outputs all marked runtime_ready=false'],
    'execution':{'data_integration':False,'index_rebuild':False,'runtime_publication':False,'retrieval_test':False,'embedding_calls':0,'image_calls':0,'pixel_test':False,'commit_push_pr':False}}
assert [r['term_id'] for r in csv.DictReader((OUT/'term-plan.csv').open(encoding='utf-8-sig'))]==[t['term_id'] for t in term_plan]
write('validation.json',summary)
print(json.dumps(summary['counts'],ensure_ascii=False,indent=2))
