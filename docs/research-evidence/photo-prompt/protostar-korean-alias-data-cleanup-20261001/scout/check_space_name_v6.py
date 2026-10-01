"""Read-only named-alias scout. No source edits, network or query measurements."""
import copy, hashlib, json, random, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode=True
R=Path('/workspace/scratch/ce8f20680f5a/image-prompt')
O=R.parent/'daylong-progress/space-name-scout'
A=R/'skills/photo-prompt-image-generator/assets'; S=A.parent/'scripts'
sys.path[:0]=[str(R),str(S)]
import prompt_generator as g
import photo_candidate_semantics as sem
import compose_pack_view as v
from tests import photo_prompt_fixtures as f
from tests.test_photo_authorial_core_v6 import PhotoAuthorialCoreV6Tests
sha=lambda b:hashlib.sha256(b).hexdigest()
objsha=lambda x:sha(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def save(n,x): (O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
SRC=A/'photo_prompt_space_extension.json'; SLOT='subject'; ID='embedded_protostar_observation_subject'; CID=f'slot:{SLOT}:{ID}'
raw_source=json.loads(SRC.read_text()); before=next(r for r in raw_source['slots'][SLOT] if r['id']==ID)
after=copy.deepcopy(before);after['aliases'].append('원시성 원반 분출계')
assert {k:v for k,v in before.items() if k!='aliases'}=={k:v for k,v in after.items() if k!='aliases'}
tracked=[SRC,S/'prompt_generator.py',S/'photo_candidate_semantics.py',S/'compose_pack_view.py',A/'photo_prompt_quality_layers.json',A/'photo_prompt_visual_obligations.json']
snapshot={str(p.relative_to(R)):sha(p.read_bytes()) for p in tracked}
queries=[
 {'id':'p01_en','language':'en','kind':'positive','query':'A protostar buried in a dark cloud drives two jets away from its surrounding disk'},
 {'id':'p01_ko','language':'ko','kind':'positive','query':'어두운 구름에 묻힌 원시성이 주변 원반의 양쪽으로 제트를 내뿜는다'},
 {'id':'p02_en','language':'en','kind':'positive','query':'An infant star and a flattened dusty disk seen between opposed outflow cavities'},
 {'id':'p02_ko','language':'ko','kind':'positive','query':'서로 반대쪽으로 열린 공동 사이에 갓 태어난 원시성과 납작한 먼지 원반이 보인다'},
 {'id':'n01_en','language':'en','kind':'near_miss_mature_debris_disk','query':'A mature star surrounded by a debris belt with no jets'},
 {'id':'n01_ko','language':'ko','kind':'near_miss_mature_debris_disk','query':'제트 없이 잔해 띠로 둘러싸인 성숙한 별'},
 {'id':'n02_en','language':'en','kind':'near_miss_bipolar_planetary_nebula','query':'An aging star sheds a bipolar planetary nebula shaped like an hourglass'},
 {'id':'n02_ko','language':'ko','kind':'near_miss_bipolar_planetary_nebula','query':'늙은 별이 물질을 내보내며 만든 모래시계 모양의 양극 행성상성운'},
]
freeze={'status':'unmeasured_one_alias_proposal','candidate_id':CID,'source_path':str(SRC.relative_to(R)), 'source_line':28,
 'before':before,'proposed':after,'exact_delta':{'field':'aliases','operation':'append','value':'원시성 원반 분출계'},
 'before_row_sha256':objsha(before),'proposed_row_sha256':objsha(after),
 'queries':[{**q,'query_sha256':sha(q['query'].encode())} for q in queries],
 'query_measurement_status':'unmeasured','query_retrieval_executions':0,'paid_calls':0,
 'evidence':[
 {'kind':'original_project_evidence','path':'docs/research-evidence/photo-prompt/space-visual-semantics-20260901/evidence.jsonl','record_id':'space_nasa_protostar_disks'},
 {'kind':'original_primary_source','url':'https://science.nasa.gov/missions/hubble/hubbles-album-of-planet-forming-disks/','section':'protostar image descriptions','support':'Hidden newly developing stars with dark planet-forming disks and bipolar gas jets; individual viewing geometries vary.'},
 {'kind':'official_korean_term_equivalence','organization':'Korea Astronomy and Space Science Institute','url':'https://astro.kasi.re.kr/kor/post/stellarObjects/71429','section':'원시성','support':'KASI explicitly equates 원시성 with 원시별.'},
 {'kind':'official_korean_research_description','organization':'Korea Astronomy and Space Science Institute','url':'https://www.kasi.re.kr/kor/publication/post/notice/5575?cPage=18','section':'8. 권우진 교수','support':'KASI pairs 원시성(protostars), 양축분출(bipolar outflows), circumstellar envelopes and circumstellar disks. Search-index text retrieved; direct opening returned an internal fetch error.'}],
 'alias_rationale':'The established named concept 원시성 is absent from all inspected runtime asset text. Substitute only this official synonym in the already authored alias 원시별 원반 분출계. The full qualified alias is not claimed as a verbatim official term. It keeps the existing disk/outflow qualifier; no bare term is attached across rows.',
 'unchanged_scope':['embedded young source','dust envelope','flattened disk','opposed outflows','perpendicular disk-outflow geometry','advisory candidate only'],
 'repository_snapshot':snapshot,'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),
 'limits':['No claim that all protostars display the candidate morphology.','No natural retrieval, dense-score, final-adoption or image-quality claim.','Promotion requires meaningful named lexical gain with no unjustified dense or near-miss loss.']}
save('frozen-proposal-and-unmeasured-probes.json',freeze)
frozen_sha=sha((O/'frozen-proposal-and-unmeasured-probes.json').read_bytes()); (O/'freeze-sha256.txt').write_text(frozen_sha+'\n')
print('FROZEN',frozen_sha,flush=True)
D=PhotoAuthorialCoreV6Tests().runtime_data();D.pop(g.SEMANTIC_INDEX_DATA_KEY,None)
assert next(r for r in D['slots'][SLOT] if r['id']==ID)==before
request='An astronomical observation of a distant celestial environment.'
baseline=('A distant celestial environment fills an astronomical observation frame. Fine clouds of luminous matter and darker obscuring regions remain distinguishable across the field. Small points of light establish depth without overwhelming the larger structure. The observation keeps delicate brightness differences and faint outer material visible, with an uncluttered border around the principal region. The photographic presentation preserves the appearance of a measured astronomical image rather than a sharply fabricated physical model.')
raw=f.core(request,interpreted_intent='A restrained astronomical observation of a distant celestial environment',subject='a distant celestial environment',setting='a distant astronomical field',event='A distant celestial environment fills an astronomical observation frame',visual_priorities=('fine luminous structure','darker obscuring regions','faint outer material'),baseline_prompt_en=baseline,locked_dimensions=('concept','subject','event'),open_dimensions=('framing','composition','lighting','camera','color','material','atmosphere','relationship'))
core=g.normalize_authorial_core(raw,request_envelope=g.normalize_request_envelope(f.envelope(request)))
result=f.generate_once(D,random.Random(17),None,['en'],True,12,True,selection_mode='rule',include_trace=True,concept_locks=[request],seed=17,creativity=0,authorial_core=core,fixture_context={'subject_category':'nonhuman'})
save('synthetic-rule-contract-result.json',result)
fixed_core=copy.deepcopy(result['provenance']['authorial_core']); states={}
# Alternatives are existing environment-kind astronomy subjects, not invented rows.
# A broad celestial-environment diagnostic core admits both as optional candidates.
pool_ids=[ID,'interacting_galaxy_pair_subject']
for state,row in [('before',before),('proposed',after)]:
 data={**D,'slots':{**D['slots'],SLOT:[copy.deepcopy(row) if r['id']==ID else r for r in D['slots'][SLOT]]}}
 sem.validate_candidate_entries(data,g.AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS)
 subject=next(r for r in data['slots'][SLOT] if r['id']==ID)
 source_pool=[next(r for r in data['slots'][SLOT] if r['id']==eid) for eid in pool_ids]
 assert g.compatible_with_picked(source_pool,{'subject':subject},forced=False,slot=SLOT,source=data)==source_pool
 # Show the unchanged narrow cluster has a real subject-bearing path too.
 dependent=next(r for r in data['slots']['location'] if r['id']=='dusty_protostar_envelope_location')
 assert g.compatible_with_picked([dependent],{'subject':subject},forced=False,slot='location',source=data)==[dependent]
 fixture=copy.deepcopy(result);fixture['choices']={'subject':copy.deepcopy(subject)};fixture['preset_id']=None
 contract=fixture['semantic_trace']['generation_contract']
 normalized=g.candidate_pack_normalized_slot_contract(data,fixed_core,contract)
 for option in source_pool:
  assert not g.entry_block_reason(option,SLOT,normalized),g.entry_block_reason(option,SLOT,normalized)
 trace=fixture['semantic_trace'];trace['slot_scores']=[{'slot':SLOT,'selected':ID,'candidate_count':len(source_pool),'top':[{'id':r['id'],'weight':r['weight'],'score':1.,'applicability_status':'eligible','applicability_source':'controlled_source_compatible_fixture'} for r in source_pool]}];trace['preset_scores']=[]
 contract['candidate_pool_trace']={SLOT:{'eligible_ids':pool_ids,'weights':{r['id']:r['weight'] for r in source_pool},'forced':False}}
 pack=g.build_candidate_pack(fixture,data,'v6'); save(state+'-actual-v6-full-pack.json',pack)
 candidate=next((r for r in pack.get('slots',{}).get(SLOT,{}).get('candidates',[]) if r['id']==CID),None)
 assert candidate,(state,'not_exposed')
 overview=v.build_view(pack);v.verify_view(pack,overview)
 detail=v.build_view(pack,[CID]);v.verify_view(pack,detail)
 assert pack['authorial_core']==fixed_core
 assert pack['negative_intent_guard']==result['negative_intent_guard']
 assert contract['soft_anchor_policy']==result['semantic_trace']['generation_contract']['soft_anchor_policy']
 save(state+'-verified-detail.json',detail);save(state+'-verified-overview.json',overview)
 states[state]={'candidate':candidate,'full_pack':pack,'detail':detail,'overview':overview}
 print(state,'EXPOSED',pack['pack_id'],flush=True)
b,a=states['before'],states['proposed']
checks={'append_only_one_field':True,'both_exposed':bool(b['candidate'] and a['candidate']),'candidate_equal':b['candidate']==a['candidate'],'full_pack_equal':b['full_pack']==a['full_pack'],'detail_equal':b['detail']==a['detail'],'overview_equal':b['overview']==a['overview'],'real_source_subject_compatibility_without_force':True,'narrow_location_compatibility_without_force':True,'generated_soft_policy_preserved':True,'negative_guard_preserved':True,'frozen_core_preserved':True,'frozen_probes_unchanged':sha((O/'frozen-proposal-and-unmeasured-probes.json').read_bytes())==frozen_sha,'tracked_source_runtime_guard_bytes_unchanged':all(sha((R/p).read_bytes())==h for p,h in snapshot.items())}
save('actual-v6-preservation-report.json',{'status':'pass' if all(checks.values()) else 'inspect','checks':checks,'scope':'Production V6 full pack, overview and detail under a controlled two-alternative source-compatible diagnostic exposure. This is output preservation only, not retrieval improvement.','controlled_pool_ids':pool_ids,'genuine_subject_id':ID,'dependent_location_id':dependent['id'],'paid_calls':0,'retrieval_probe_executions':0,'repository_files_written':[],'freeze_sha256':frozen_sha})
assert all(checks.values()),checks
print('PASS_ALL_PRESERVATION_CHECKS',flush=True)
