#!/usr/bin/env python3
"""Check research references and compile templates in memory; no active writes."""
from __future__ import annotations
import copy
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'skills/photo-prompt-image-generator/scripts'))
import photo_candidate_semantics as pcs
from visual_profile_contracts import compile_visual_profile

def read(name):
    return json.loads((HERE/name).read_text())
def write(name,value):
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

failures=[]
checks=Counter()
def check(condition,label):
    checks['total']+=1
    if not condition:failures.append(label)
def attempt(label,func):
    checks['total']+=1
    try:return func()
    except Exception as exc:
        failures.append(label+': '+str(exc));return None

reference=read('REFERENCE-KEYWORDS.json')
terms=read('TERM-RESEARCH.json')
sources=read('SOURCES.json')
inventory=read('CURRENT-INVENTORY.json')
audit=read('CURRENT-DATA-AUDIT.json')
snapshot=read('SOURCE-SNAPSHOT.json')
cd=read('CANDIDATE-DRAFTS.json')
pd=read('PROFILE-DRAFTS.json')
bd=read('BUNDLE-DRAFTS.json')
reg=read('REGRESSION-PLAN.json')
pixel=read('PIXEL-QUALIFICATION-PLAN.json')
summary=read('PACKAGE-SUMMARY.json')
oldkeys=set(inventory['candidate_keys']); oldprofiles=set(inventory['profile_ids'])
sourceids={s['id'] for s in sources['sources']}
knownnumbers=set(range(1,121))
allowed_dims={d for dims in snapshot['slot_dimensions'].values() for d in dims}
newkeys={d['slot']+'.'+d['candidate_entry_template']['id'] for d in cd['new_candidate_proposals']}
allkeys=oldkeys | newkeys

check(len(reference['rows'])==len(terms['terms'])==len(audit['rows'])==120,'120 terms in all ledgers')
check([r['number'] for r in reference['rows']]==list(range(1,121)),'original numbers contiguous')
check([r['number'] for r in terms['terms']]==list(range(1,121)),'research numbers contiguous')
check(len(sources['sources'])==len(sourceids)==39,'39 distinct sources')
check(set(terms['interpretive_terms'])==set(range(1,15))|{33},'15 interpretation terms')
check(set(terms['explicit_temporal_terms'])=={24,25,26,27,28,35,81,107,108},'9 temporal terms')
check(not (newkeys & oldkeys),'new candidate keys do not collide with snapshot keys')
check(len(newkeys)==14,'14 distinct new candidate proposals')
for r in terms['terms']:
    n=r['number'];check(r['term']==reference['rows'][n-1]['term'],f'term {n} retained')
    check(bool(r['observables_or_optional_examples_ko'] and r['ownership_and_relations_ko'] and r['confusion_boundaries_ko'] and r['observability_gate_ko']),f'term {n} has four visual evidence fields')
    check(set(r['existing_candidate_keys'])<=oldkeys,f'term {n} known candidate keys')
    check(set(r['existing_profile_ids'])<=oldprofiles,f'term {n} known profile ids')
    check(bool(r['source_ids']) and set(r['source_ids'])<=sourceids,f'term {n} known sources')
    check(r['runtime_status']=='research_only_not_installed',f'term {n} nonruntime status')
    if n in terms['interpretive_terms']:
        check(r['component_policy']=='optional_examples_not_a_hard_recipe',f'term {n} optional interpretation')
for s in sources['sources']:
    check(s['url'].startswith('https://'),s['id']+' HTTPS source')
    check(bool(s['supported_claim'] and s['limitations'] and s['access_method']),s['id']+' evidence scope')
    check(s['quotes_verbatim'] is False,s['id']+' paraphrased source')

template_slots=defaultdict(list)
for draft in cd['new_candidate_proposals']:
    e=draft['candidate_entry_template'];k=draft['slot']+'.'+e['id']
    template_slots[draft['slot']].append(copy.deepcopy(e))
    check(set(e)<= {'id','ko','en','weight','tags','for_any','aliases','keywords','embedding_text','concept_units','relations','affected_dimensions','affected_properties','paraphrases'},k+' supported draft fields')
    check(bool(e['concept_units'] and e['relations'] and e['affected_dimensions'] and e['affected_properties']),k+' units relations and effects')
    check(bool(draft['effect_mapping_status'] and draft['required_core_bindings_ko'] and draft['dedup_review_ko']),k+' mapping blockers preserved')
    check(set(draft['source_ids'])<=sourceids,k+' sources')
    check(not re.search(r'https?://|Merriam|Peter Hurley|research_|source_sha|BM25|embedding model',e['embedding_text'],re.I),k+' no provenance in positive embedding text')
    check(not re.search(r'\b(?:not|no|without|never|forbidden|excluded)\b',e['embedding_text'],re.I),k+' negative boundaries outside positive embedding text')
    check('frozen' not in e['embedding_text'],k+' orchestration word outside positive embedding text')
for draft in cd['existing_candidate_enrichments']:
    k=draft['candidate_key'];slot,ident=k.split('.',1)
    check(k in oldkeys,k+' enrichment owner exists')
    check(set(draft['source_ids'])<=sourceids,k+' enrichment sources')
    e={'id':ident,**copy.deepcopy(draft['proposed_field_patch'])}
    template_slots[slot].append(e)
    check('requires_' not in ''.join(draft['proposed_field_patch']),k+' no guard mutation in field patch')
check(len(cd['existing_candidate_enrichments'])==22,'22 existing candidate proposals')
minimal_data={'slots':dict(template_slots),'candidate_semantic_policy':{'slot_dimensions':snapshot['slot_dimensions']}}
attempt('candidate template validation with live field validator',lambda:pcs.validate_candidate_entries(minimal_data,allowed_dims))

compiled_profiles=[]
newprofileids=set()
broad_labels={'seductive','flirtatious','coquettish','coy','sultry','smoldering','come-hither','teasing','sensual','languid','provocative','commanding','femme fatale','bedroom eyes','smirk'}
for draft in pd['new_profile_proposals']:
    p=draft['profile_template'];ident=p['id'];newprofileids.add(ident)
    check(ident not in oldprofiles,ident+' not a duplicate profile')
    check(draft['candidate_key'] in newkeys,ident+' new candidate link')
    check(set(draft['source_ids'])<=sourceids,ident+' source refs')
    check(bool(draft['install_blocker'] and draft['required_context_before_activation_ko']),ident+' context blocker')
    check(not broad_labels.intersection(t.casefold() for t in p['activation']['exact_terms']),ident+' no broad hard label')
    cp=attempt(ident+' live authored component projection',lambda p=p:compile_visual_profile(p))
    if cp:
        compiled_profiles.append(cp)
        check(len(cp['render_gates'])==len(p['authored_components']['components']),ident+' all gates projected')
        check(all(g['review_scale']=='native' for g in cp['render_gates']),ident+' native review scale')
        check(len(set(cp['required_evidence_fields']))==len(cp['required_evidence_fields']),ident+' distinct evidence fields')
for draft in pd['existing_profile_enrichments']:
    check(draft['profile_id'] in oldprofiles,draft['profile_id']+' known existing profile')
    check(set(draft['source_ids'])<=sourceids,draft['profile_id']+' existing profile sources')
check(len(newprofileids)==len(compiled_profiles)==12,'12 unique and compiled profile templates')
check(len(pd['existing_profile_enrichments'])==14,'14 existing profile plans')

# In-memory bundle compile uses authored records and proposal templates only.
bundle_keys={k for d in bd['bundles'] for k in d['candidate_keys']}
bundle_slots=defaultdict(list)
source_records={}
for file in snapshot['files']:
    path=ROOT/file['path']
    if path.suffix!='.json':continue
    data=json.loads(path.read_text())
    for slot,values in data.get('slots',{}).items():
        entries=values if isinstance(values,list) else values.get('entries',[])
        for e in entries:
            k=slot+'.'+e['id']
            if k in bundle_keys:source_records[k]=copy.deepcopy(e)
for d in cd['new_candidate_proposals']:
    e=d['candidate_entry_template'];k=d['slot']+'.'+e['id']
    if k in bundle_keys:source_records[k]=copy.deepcopy(e)
for k,e in source_records.items():bundle_slots[k.split('.',1)[0]].append(e)
bundle_data={'slots':dict(bundle_slots),'candidate_semantic_policy':{'slot_dimensions':snapshot['slot_dimensions']}}
for d in bd['bundles']:
    check(set(d['candidate_keys'])<=allkeys,d['proposal_id']+' valid candidate refs')
    check(set(d['source_ids'])<=sourceids,d['proposal_id']+' source refs')
    check(set(d['bundle_entry_template'])<=pcs.BUNDLE_SOURCE_KEYS,d['proposal_id']+' supported source fields')
    check(d['bundle_entry_template']['candidate_only'] is True,d['proposal_id']+' candidate only')
    check(d['bundle_entry_template']['hard_profile_ids']==[],d['proposal_id']+' no broad forced profiles')
attempt('bundle templates compile in memory',lambda:pcs.compile_extension_bundles(bundle_data,{'visual_semantics':[d['bundle_entry_template'] for d in bd['bundles']]}))
compiled_bundles=bundle_data.get('candidate_bundles',[])
check(len(compiled_bundles)==10,'10 bundles compiled')
for b in compiled_bundles:
    check(b['adoption']=='optional',b['id']+' optional adoption')
    check(b['profile_activation']=='independent_request_evidence_only',b['id']+' independent profile activation')

check(reg['coverage_probe_count']==len(reg['coverage_probes'])==120,'120 coverage probes')
check(reg['cross_boundary_case_count']==len(reg['cross_boundary_cases'])==45,'45 boundary proposals')
check(len({r['id'] for r in reg['cross_boundary_cases']})==45,'distinct boundary ids')
check(reg['executed_test_count']==0,'no executed runtime regression claim')
check(pixel['scene_family_count']==len(pixel['cases'])==8,'8 pixel scene families')
check(pixel['native_generation_calls_executed']==0,'no native generation claim')
for c in pixel['cases']:
    check(c['status']=='not_generated_not_evaluated',c['id']+' pending pixels')
    check('partial_is_fail' in c['decision_rule'] and 'UNOBSERVABLE' in c['decision_rule'],c['id']+' strict image gate')
    check('exposed_in_pack' in c['attribution_gates'] and 'original_pixel_all_of' in c['attribution_gates'],c['id']+' attribution layers')

check(summary['reference_terms']==120 and summary['sources']==39,'summary term/source counts')
check(summary['new_candidate_proposals']==14 and summary['existing_candidate_enrichment_proposals']==22,'summary candidate counts')
check(summary['new_narrow_profile_proposals']==12 and summary['existing_profile_enrichment_proposals']==14,'summary profile counts')
check(summary['active_asset_edits']==summary['runtime_tests_executed']==summary['native_generations_executed']==0,'summary evidence boundaries')

# Create the eventual report path so local link verification includes it.
write('VALIDATION.json',{'status':'checking_research_package'})
local_links=0
for f in HERE.glob('*.md'):
    content=f.read_text()
    for target in re.findall(r'\]\((/[^)]+)\)',content):
        path=re.sub(r':\d+$','',target)
        check(Path(path).is_file(),f.name+' local link '+target);local_links+=1
    if f.name=='CATALOGUE.md':
        check(len(re.findall(r'^### \d{3}\.',content,re.M))==120,'catalogue 120 headings')
for name in ['RESEARCH.md','IMPLEMENTATION-PLAN.md','README.md']:
    check((HERE/name).stat().st_size>3000,name+' substantive document')

drift=[]
for r in snapshot['files']:
    p=ROOT/r['path'];current=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
    check(current==r['sha256'],'input unchanged '+r['path'])
    if current!=r['sha256']:drift.append({'path':r['path'],'snapshot_sha256':r['sha256'],'current_sha256':current})
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
check(head==snapshot['head'],'repository HEAD unchanged during research')
current_status=subprocess.check_output(['git','status','--porcelain=v1'],cwd=ROOT,text=True).splitlines()
prefix=str(HERE.relative_to(ROOT))
outside=lambda xs:set(x for x in xs if prefix not in x)
status_added=sorted(outside(current_status)-outside(snapshot['status']))
status_removed=sorted(outside(snapshot['status'])-outside(current_status))
check(not status_added and not status_removed,'unrelated git status entries unchanged')

report={'schema_version':'seduction-research-validation/v1',
    'checked_at_kst':datetime.now(timezone(timedelta(hours=9))).isoformat(),
    'status':'PASS' if not failures else 'FAIL','check_count':checks['total'],'failures':failures,
    'scope':'Research records, references, and draft shape/projection checks in memory. No request routing, target/property binding, pack eligibility/exposure/selection, index freshness or native pixels were tested.',
    'template_checks':{'candidate_entries':36,'profile_templates_compiled':len(compiled_profiles),
        'optional_bundles_compiled':len(compiled_bundles),'compiler_files_read_only':True},
    'input_integrity':{'source_files_checked':len(snapshot['files']),'source_hash_mismatches':drift,
        'snapshot_head':snapshot['head'],'current_head':head,
        'unrelated_git_status_added':status_added,'unrelated_git_status_removed':status_removed,
        'boundary':'88 recorded input files were hash checked. Unrelated git-status equality is not a content hash of every file in the worktree.'},
    'local_document_links_checked':local_links,
    'pending_gates':['semantic duplicate review','actual core owner/target/property resolution','executable context guards','positive retrieval text review for final patches','runtime regression and index consistency','candidate-pack exposure and selection','native original-pixel all-of','user acceptance'],
    'active_runtime_assets_edited':False,'native_generation_calls':0,
}
write('VALIDATION.json',report)
manifest=[]
for f in sorted(HERE.iterdir()):
    if f.is_file() and f.name!='MANIFEST.json':
        manifest.append({'path':f.name,'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
write('MANIFEST.json',{'schema_version':'seduction-research-manifest/v1','files':manifest,
    'scope':'Research package file integrity. Excludes this manifest to avoid self-reference.'})
print(json.dumps({'status':report['status'],'checks':checks['total'],'failures':failures,
    'profile_templates':len(compiled_profiles),'optional_bundles':len(compiled_bundles),
    'source_drift_count':len(drift),'local_links':local_links},ensure_ascii=False))
sys.exit(0 if not failures else 1)
