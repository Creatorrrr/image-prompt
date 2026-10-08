"""Check research integrity and pure contracts; never publish runtime data."""
from __future__ import annotations
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
sys.path.insert(0,str(ROOT/'skills/photo-prompt-image-generator/scripts'))
from photo_candidate_semantics import validate_candidate_entries, validate_relations
from photo_contracts import INTENT_LOCK_DIMENSIONS, property_effects_allowed
from visual_profile_contracts import compile_visual_profile, validate_visual_profile_source, validate_hard_activation

def read(name): return json.loads((OUT/name).read_text())
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def normal(s): return re.sub(r'[^\w]+',' ',str(s).casefold()).strip()

def main():
    units=read('research-units.json')['units']; proposals=read('candidate-proposals.json')['proposals']
    profiles=read('visual-profile-proposals.json')['proposals'];routing=read('keyword-routing.json')['routing']
    sources=read('sources.json')['sources'];seed=read('original-keywords.json');inv=read('existing-inventory.json')
    before=read('workspace-before.json');case_plan=read('validation-case-plan.json')
    errors=[];unit_ids={u['id']for u in units};source_ids={s['id']for s in sources}
    if len(unit_ids)!=180 or [u['seed_number']for u in units]!=list(range(1,181)): errors.append('numbered seed coverage mismatch')
    if set(Counter(u['group']for u in units).values())!={10}: errors.append('each of 18 groups must preserve 10 seed rows')
    if len(source_ids)!=len(sources):errors.append('duplicate source ID')
    for u in units:
        if not set(u['source_ids'])<=source_ids:errors.append('broken source reference '+u['id'])
        if len(u['components'])<3 or any(not c['owner']or not c['visible_phrase_en']for c in u['components']):errors.append('unowned or insufficient form '+u['id'])
        if not u['confusion_boundary_ko']or not u['observability_ko']or not u['capture_policy']:errors.append('missing boundary/observability '+u['id'])
        validate_relations(u['relations'],u['id'])
    seed_ids={r['id']for r in seed['numbered_rows']+seed['summary_rows']}
    if len(routing)!=200 or {r['seed_id']for r in routing}!=seed_ids:errors.append('routing must preserve 180 numbered plus 20 summary rows')
    for r in routing:
        if not r['research_unit_ids']or not set(r['research_unit_ids'])<=unit_ids:errors.append('broken routing '+r['seed_id'])
    slots={};by_unit={};proposal_ids=set()
    real_slots={r['slot']for r in inv['records']if r['kind']=='candidate'}
    for p in proposals:
        c=p['candidate_draft'];slots.setdefault(p['suggested_slot'],[]).append(c);by_unit.setdefault(p['research_unit_id'],[]).append(c)
        if p['suggested_slot']not in real_slots:errors.append('unregistered proposed slot '+p['suggested_slot'])
        if c['id']in proposal_ids:errors.append('duplicate candidate '+c['id'])
        proposal_ids.add(c['id'])
        if p['research_unit_id']not in unit_ids:errors.append('broken candidate link')
    validate_candidate_entries({'slots':slots},set(INTENT_LOCK_DIMENSIONS))
    compiled_gates=0;profile_ids=set();paired_candidate_ids=set();korean_components=0
    for p in profiles:
        prof=p['profile_draft'];validate_visual_profile_source(prof);validate_hard_activation(prof['activation']['hard_activation'])
        compiled=compile_visual_profile(prof);compiled_gates+=len(compiled['render_gates'])
        if len(compiled['render_gates'])!=len(prof['authored_components']['components']):errors.append('compiler lost a component '+prof['id'])
        if prof['id']in profile_ids:errors.append('duplicate profile '+prof['id'])
        profile_ids.add(prof['id']);paired_candidate_ids.add(p['candidate_id'])
        korean_components+=sum(any(re.search('[가-힣]',t)for t in c['match_terms'])for c in prof['authored_components']['components'])
        if p['candidate_id']not in proposal_ids:errors.append('broken paired candidate '+prof['id'])
        if p['research_unit_id']=='SF056'and any('cat heart' in t.casefold()or'고양이 하트'in t for t in prof['activation']['exact_terms']):errors.append('unverified name hard activation')
    if paired_candidate_ids!=proposal_ids:errors.append('candidate/profile pairing mismatch')
    lock_results=[]
    for case in case_plan['regression_cases']:
        if not set(case['research_unit_ids'])<=unit_ids:errors.append('broken planned test reference')
        if case['type']!='property_lock':continue
        uid=case['research_unit_ids'][0];lock={'contract_version':'photo-intent-lock/v2','semantic_anchors':[case['locked_anchor']]}
        for c in by_unit[uid]:
            actual=property_effects_allowed(lock,c['affected_dimensions'],c['affected_properties'])
            lock_results.append({'case_id':case['id'],'candidate_id':c['id'],'expected':case['candidate_allowed_expected'],'actual':actual})
            if actual!=case['candidate_allowed_expected']:errors.append('property lock failure '+c['id'])
    for case in case_plan['render_scenario_families']:
        if not set(case['research_unit_ids'])<=unit_ids:errors.append('broken planned render reference')
    reused=read('reuse-plan.json')['reuse'];reuse_refs=0
    saved_refs={(r['file'],r.get('slot'),r['id'])for r in inv['records']if r['kind']=='candidate'}
    for r in reused:
        for ref in r['existing_refs']:
            reuse_refs+=1
            if(ref['file'],ref['slot'],ref['id'])not in saved_refs:errors.append('reuse identity missing '+ref['id'])
    # Snapshot lexical matches are review hints, not a quality score or proof of
    # equivalent shape. Search only positive names/terms, never contrast prose.
    positive_name_index={}
    for r in inv['records']:
        terms=([r.get('ko','')]+r.get('aliases',[])+r.get('keywords',[]))if r['kind']=='candidate'else r.get('terms',[])
        for term in {normal(t)for t in terms}:
            if term:positive_name_index.setdefault(term,[]).append(r)
    audit=[]
    for u in units:
        probes={normal(u['label_ko']),normal(u['label_en'])}
        if u['seed_number']==8:probes.update({'fish gape','parted lips'})
        hints=[]
        seen=set()
        for probe in sorted(probes):
            for r in positive_name_index.get(probe,[]):
                key=(r['kind'],r['file'],r.get('slot'),r['id'])
                if key not in seen:
                    seen.add(key)
                    hints.append({'kind':r['kind'],'id':r['id'],'slot':r.get('slot'),'file':r['file']})
        audit.append({'research_unit_id':u['id'],'positive_name_match_hints':hints,
                      'meaning':'Names match only; component semantics, ownership and applicability need review.'})
    (OUT/'current-data-audit.json').write_text(json.dumps({'source_file_count':len(inv['files']),
        'raw_candidate_rows':sum(r['kind']=='candidate'for r in inv['records']),
        'raw_profile_rows':sum(r['kind']=='profile'for r in inv['records']),
        'counts_are_not_live_loader_counts':True,'audit':audit,
        'specific_findings':[
            {'id':'smize_mouth_constraint','candidate':'ae_smize','finding':'Existing source requires mouth-corner rise; SF004 near-neutral lip variant must not silently alias it.'},
            {'id':'mirror_age_count_scope','profile':'mirror_selfie_reflection_device_topology','finding':'Current base profile assumes one adult and physical reflection. Neutral capture geometry and multi-actor variants need scoped review.'},
            {'id':'no_finger_heart_name_hint','finding':'Initial positive-name scan did not find Finger heart as a candidate; this is not proof that all thumb-index geometry is absent.'},
            {'id':'bambi_scope','finding':'Existing pose tests exclude bare bambi activation. Preserve heel-sit component data without claiming a newly verified named convention.'},
            {'id':'projection_and_roll_reuse','finding':'Existing ultrawide_near_far_scale_expansion, pv_head_tilt and camera-roll components are component reuse references; do not duplicate or impose their broader context.'},
        ]},ensure_ascii=False,indent=2)+'\n')
    drift=[f['path']for f in inv['files']if not(ROOT/f['path']).is_file()or sha(ROOT/f['path'])!=f['sha256']]
    protected_drift=[p for p,r in before['protected_files'].items()if not(ROOT/p).is_file()or sha(ROOT/p)!=r['sha256']]
    result={'status':'pass'if not errors else'fail','errors':errors,'numbered_seed_rows_checked':180,'summary_rows_checked':20,
            'research_units':len(units),'owned_observation_proposals':sum(len(u['components'])for u in units),
            'candidate_drafts_contract_checked':len(proposals),'profile_drafts_source_compiler_checked':len(profiles),
            'compiled_gate_count':compiled_gates,'profile_components_with_positive_korean_equivalents':korean_components,
            'sources':len(sources),'source_evidence_statuses':dict(Counter(s['evidence_status']for s in sources)),
            'reuse_references_checked':reuse_refs,'planned_regression_cases':len(case_plan['regression_cases']),
            'planned_render_families':len(case_plan['render_scenario_families']),
            'pure_property_lock_checks':lock_results,'source_files_checked':len(inv['files']),
            'working_source_drift':drift,'protected_files_checked':len(before['protected_files']),'protected_file_drift':protected_drift,
            'preservation_status':'baseline_drift_observed'if protected_drift else'baseline_hashes_identical',
            'preservation_boundary':'Only captured authored-source JSON and modified tracked files were fingerprinted. Drift does not attribute another actor changes. All authored writes for this research are confined to this directory.',
            'proof_boundary':'Research reference integrity, snapshot reuse identities, pure candidate/profile compiler contracts and pure property locks. No live activation/ranking/selection, prompt audit, render, native pixels, user acceptance or publication tested.'}
    (OUT/'research-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()if k!='pure_property_lock_checks'},ensure_ascii=False,indent=2))
    if errors:raise SystemExit(1)

if __name__=='__main__':main()
