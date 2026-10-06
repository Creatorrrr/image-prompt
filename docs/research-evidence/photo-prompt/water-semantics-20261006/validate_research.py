"""Validate research links, scope boundaries and reproducible compiler format."""
import collections
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode=True
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
errors=[]

def require(ok,message):
    if not ok: errors.append(message)

def read(name):
    return json.loads((OUT/name).read_text())

parsed=[]
for p in sorted(OUT.glob('*.json')):
    try: json.loads(p.read_text());parsed.append(p.name)
    except Exception as e: errors.append(f'{p.name}: {e}')

seeds=read('SEED-INVENTORY.json')['rows']
units=read('SEMANTIC-UNITS.json')['units']
candidates=read('CANDIDATE-DRAFTS.json')['candidates']
sources=read('SOURCES.json')['sources']
coverage=read('SEED-COVERAGE.json')['rows']
mappings=read('RUNTIME-MAPPING.json')['mappings']
prototypes=read('PROFILE-PROTOTYPES.json')
bundles=read('BUNDLE-DRAFTS.json')['bundles']
regressions=read('REGRESSION-PLAN.json')['case_groups']
pixels=read('PIXEL-QUALIFICATION-PLAN.json')['groups']
seed_ids={r['seed_id'] for r in seeds};unit_ids={r['id'] for r in units};source_ids={r['id'] for r in sources}
require(len(seeds)==len(seed_ids)==345,'345 unique original rows required')
require({r['section'] for r in seeds}==set(range(1,25)),'all 24 sections required')
require(len(units)==len(unit_ids)==192,'192 unique units required')
require(len(source_ids)==len(sources)==45,'45 unique sources required')
for r in sources: require(r['url'].startswith('https://') and bool(r['supported_scope']),r['id']+': source URL/scope missing')
require({r['seed_id'] for r in coverage}==seed_ids,'coverage identity mismatch')
for r in coverage:
    require(bool(r['unit_refs']) and set(r['unit_refs'])<=unit_ids,r['seed_id']+': unassigned or missing unit')
for u in units:
    require(set(u['seed_refs'])<=seed_ids,u['id']+': unknown seed')
    require(set(u['public_source_refs'])<=source_ids,u['id']+': unknown public source')
    require(len(u['observable_components_proposal'])>=3,u['id']+': incomplete observation proposal')
    require(u['qualification']=='PROPOSED_NOT_RUN',u['id']+': invalid evidence promotion')
    require(bool(u['confusion_boundary']),u['id']+': missing confusion boundary')
    for r in u['relations_proposal']:
        b=r.get('owner_binding',{})
        require(b.get('scene')==u['id'] and b.get('subject_ref')==u['id']+':'+r['subject'] and b.get('object_ref')==u['id']+':'+r['object'],u['id']+': unbound relation')

visual={r['id'] for r in units if r['mode']=='visual'}
require(len(candidates)==117 and {r['unit_id'] for r in candidates}==visual,'visual-only candidate projection mismatch')
require(len({r['id'] for r in candidates})==117,'duplicate candidate IDs')
for c in candidates:
    require(not c['eligible_for_hard_activation'] and c['property_status']=='NOT_MAPPED_DO_NOT_ADOPT',c['id']+': false runtime eligibility')
    require(c['qualification']=='PROPOSED_NOT_RUN',c['id']+': draft evidence boundary missing')
    text=c['positive_retrieval_text_proposal']
    require(not any(x in text for x in ['https://','PROPOSED_NOT_RUN','water_research_']),c['id']+': research provenance in retrieval text')
    require(not c['affected_properties_proposal'],c['id']+': unverified property effects present')
require({m['unit_id'] for m in mappings}==unit_ids,'missing runtime mapping')
for m in mappings: require(not m['missing_lookup_ids'],m['unit_id']+': missing current ID reference')
for b in bundles: require(set(b['unit_refs'])<=unit_ids,b['id']+': missing bundle members')
require(len(regressions)==len(pixels)==16,'16 planned regression/pixel groups required')
for p in regressions+pixels:
    require(p['unit_id'] in unit_ids and p['qualification']=='PROPOSED_NOT_RUN',p['id']+': invalid qualification or unit')

path=ROOT/'skills/photo-prompt-image-generator/scripts/visual_profile_contracts.py'
require(prototypes['compiler_source_sha256']==hashlib.sha256(path.read_bytes()).hexdigest(),'compiler source drift since prototype build')
spec=importlib.util.spec_from_file_location('water_validation_contract',path)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
format_checks=[]
for p in prototypes['profiles']:
    compiled=module.compile_visual_profile(p['source_prototype'])
    for k,v in p['compiled_format_preview'].items(): require(compiled[k]==v,p['unit_id']+': mismatched compiler projection '+k)
    fields=compiled['required_evidence_fields'];gates=compiled['render_gates']
    require(len(fields)==len(set(fields))==len(gates)==3,p['unit_id']+': missing or duplicated component projection')
    format_checks.append({'unit_id':p['unit_id'],'components':3,'evidence_fields':len(fields),'gates':len(gates),'status':'COMPILER_FORMAT_ONLY'})

local_links=[]
for p in OUT.glob('*.md'):
    for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
        if re.match(r'^[a-z][a-z0-9+.-]*:',target,re.I) or target.startswith('#'): continue
        target=target.split('#')[0]
        if target=='VALIDATION.json': continue
        require((p.parent/target).exists(),f'{p.name}: broken local link {target}')
        local_links.append((p.name,target))

result={'schema':'water-research-validation/v1','status':'PASS_RESEARCH_STRUCTURE' if not errors else 'FAIL','errors':errors,'json_files_parsed':parsed,'local_links_checked':len(local_links),'counts':{'seeds':len(seeds),'units':len(units),'candidates':len(candidates),'family':sum(u['mode']=='family' for u in units),'context':sum(u['mode']=='context' for u in units),'sources':len(sources),'bundles':len(bundles),'planned_regression_groups':len(regressions),'planned_pixel_groups':len(pixels)},'source_verification_counts':dict(collections.Counter(s['verification'] for s in sources)),'visual_cards_awaiting_primary_source':[u['id'] for u in units if u['mode']=='visual' and not u['public_source_refs']],'compiler_format_checks':format_checks,'proof_boundary':'JSON/link/coverage/owner-binding integrity and existing compiler projection only. No public source claim completion, active data validation, real index/retrieval, candidate exposure/selection, runtime or native image test.'}
(OUT/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
stats=read('RESEARCH-STATS.json');stats['research_status']=result['status'];(OUT/'RESEARCH-STATS.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
