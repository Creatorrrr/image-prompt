"""Verify research references and protected source bytes, not runtime quality."""
from __future__ import annotations
import hashlib
import importlib.util
import json
import pathlib
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
def read(name): return json.loads((HERE / name).read_text())
def save(name, obj): (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')

checks = []
def check(label, condition, detail=None):
    checks.append({'check':label, 'status':'PASS' if condition else 'FAIL', 'detail':detail})

cards = read('SEMANTIC-CARDS.json')['cards']
card_map = {c['id']:c for c in cards}
sources = read('SOURCES.json')['sources']
source_ids = {s['id'] for s in sources}
drafts = read('CANDIDATE-DRAFTS.json')['items']
bundles = read('BUNDLE-DRAFTS.json')['items']
keywords = read('KEYWORD-COVERAGE.json')['items']
seeds = read('SEED-KEYWORDS.json')['items']
mapping = read('RUNTIME-MAPPING.json')['entries']
evaluation = read('EVALUATION-PLAN.json')
check('unique_card_ids', len(card_map)==len(cards)==70)
check('unique_source_ids', len(source_ids)==len(sources))
check('unique_candidate_draft_ids', len({d['draft_id'] for d in drafts})==len(drafts))
check('all_source_references_exist', all(set(c['source_ids'])<=source_ids for c in cards))
check('card_owners_and_directed_relations_present', all(c['owners'] and c['observable_components'] and c['directed_relations'] and all(r.get('owner_binding') for r in c['directed_relations']) for c in cards))
check('all_confusion_boundaries_present', all(len(c['confusion_boundaries'])>=2 for c in cards))
check('existing_ids_resolved_in_raw_sources', all(len(c['existing_references'])>=len(c['integration']['existing_ids']) for c in cards))
check('candidate_slots_exist_in_raw_sources', all(r['slot_exists_in_raw_authored_sources'] for r in mapping))
check('drafts_are_not_runtime_records', all(d['is_runtime_record'] is False and d['status']=='PROPOSED_NOT_INTEGRATED' for d in drafts))
check('candidate_card_references', all(d['semantic_card_id'] in card_map for d in drafts))
check('bundle_card_and_candidate_references', all(set(b['card_ids'])<=set(card_map) and set(b['candidate_draft_refs'])<={d['draft_id'] for d in drafts} for b in bundles))
check('visible_keyword_preservation', len(seeds)==len(keywords)==350 and [s['id'] for s in seeds]==[k['seed_id'] for k in keywords] and all(s['en']==k['en'] and s['ko']==k['ko'] for s,k in zip(seeds,keywords)))
check('keyword_routes_do_not_claim_semantic_coverage', all(not k['is_semantic_equivalence_or_runtime_coverage'] and set(k['research_card_routes'])<=set(card_map) for k in keywords))
check('20_palette_role_drafts', len(read('PALETTE-ROLE-DRAFTS.json')['items'])==20)
check('90_regression_design_cases_not_run', sum(len(g['cases']) for g in evaluation['deterministic_case_groups'])==90 and all(g['status']=='PLANNED_NOT_RUN' for g in evaluation['deterministic_case_groups']))
check('pixel_plan_only', len(evaluation['pixel_groups'])==6 and all(g['status']=='PLANNED_NOT_RUN' for g in evaluation['pixel_groups']))

module_path = ROOT/'skills/photo-prompt-image-generator/scripts/visual_profile_contracts.py'
spec = importlib.util.spec_from_file_location('research_visual_profile_contracts', module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
prototypes = []
for cid in ['EG07','EG53','EG60']:
    c = card_map[cid]
    profile = {'id':'egr_prototype_'+cid.lower(), 'category':'research_prototype_only', 'semantics':{'definition':'; '.join(c['observable_components'])}, 'authored_components':{'contract_version':'photo-authored-visual-components/v1','components':[]}}
    for idx, phrase in enumerate(c['observable_components'],1):
        profile['authored_components']['components'].append({'id':f'component_{idx}','match_terms':[phrase],'evidence_field':f'component_{idx}_phrase','evidence_terms':[phrase],'min_content_words':3,'instruction':'Keep the explicitly declared owner and realize this selected component: '+phrase,'render_gate':{'id':f'vo_egr_{cid.lower()}_{idx}','review_scale':'native','description':'Inspect the original pixels on the declared owner for this entire relation: '+phrase}})
    compiled = module.compile_visual_profile(profile)
    check('component_projection_'+cid, len(compiled['required_evidence_fields'])==len(c['observable_components'])==len(compiled['render_gates']))
    prototypes.append({'card_id':cid,'status':'COMPONENT_PROJECTION_ONLY','is_complete_runtime_profile':False,'source_profile':profile,'compiled_profile':compiled,'unverified':['property scope','runtime owner resolution','hard activation matcher','candidate pack exposure','prompt audit','native pixels']})
save('PROFILE-PROTOTYPES.json', {'schema_version':'research-profile-prototypes/v1','items':prototypes})

snapshot = read('CHECKOUT-SNAPSHOT.json')
changes = []
for field in ['protected_files','index_manifests']:
    for relative, before in snapshot[field].items():
        path = ROOT/relative
        after = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
        if after != before: changes.append({'path':relative,'before':before,'after':after})
check('protected_sources_scripts_and_index_manifests_unchanged', not changes, {'checked_files':len(snapshot['protected_files'])+len(snapshot['index_manifests']),'changed':changes})
current_status = subprocess.check_output(['git','status','--porcelain=v1','-uall'],cwd=ROOT,text=True)
prefix = str(HERE.relative_to(ROOT))+'/'
filter_status = lambda text: sorted(line for line in text.splitlines() if prefix not in line)
before_status = filter_status(snapshot['git_status'])
after_status = filter_status(current_status)
check('unrelated_dirty_and_untracked_status_preserved', before_status==after_status, {'removed':sorted(set(before_status)-set(after_status)),'added':sorted(set(after_status)-set(before_status))})
check('head_unchanged', subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==snapshot['head'])

all_json = []
for path in sorted(HERE.glob('*.json')):
    json.loads(path.read_text()); all_json.append(path.name)
check('research_json_parse', True, all_json)
result = {'schema_version':'research-package-validation/v1','status':'PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL','scope':'Research document structure, references, simple authored-component projection and source preservation only. No production dictionary/index/runtime tests or image evaluations.','checks':checks,'counts':read('PACKAGE-SUMMARY.json'),'production_implementation':'NOT_RUN','index_rebuild':'NOT_RUN','embedding_calls':0,'candidate_pack_runs':0,'image_generation_calls':0,'native_pixel_evaluation':'NOT_RUN','user_acceptance':'NOT_ASSESSED'}
save('VALIDATION.json',result)
print(json.dumps({'status':result['status'],'checks':len(checks),'failed':[c for c in checks if c['status']=='FAIL'],'scope':result['scope']},ensure_ascii=False))
raise SystemExit(0 if result['status']=='PASS' else 1)
