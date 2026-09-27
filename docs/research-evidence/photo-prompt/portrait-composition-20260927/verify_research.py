"""Validate the research draft in memory; never update runtime assets or indexes."""
from __future__ import annotations
import copy
import hashlib
import json
import pathlib
import sys
from collections import Counter

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0,str(SKILL/'scripts'))
import prompt_generator as pg
import photo_candidate_semantics as cs
from visual_profile_contracts import compile_visual_profile

def read(name):return json.loads((HERE/name).read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def verify():
    catalog=read('concept-catalog.json')['concepts']
    sources=read('sources.json')['sources']
    source_ids={s['id'] for s in sources}
    ext=read('candidate-extension.proposed.json')
    proposed=read('visual-profiles.proposed.json')['profiles']
    coverage=read('coverage-audit.json')
    cases=[json.loads(x) for x in (HERE/'regression-cases.jsonl').read_text().splitlines()]
    checks={}
    assert len(catalog)==50 and len({c['id'] for c in catalog})==50
    assert {c['id'] for c in catalog if c['id'].startswith('PC')}=={f'PC{i:02}' for i in range(1,31)}
    assert len(source_ids)==25 and all(set(c['source_ids'])<=source_ids for c in catalog)
    assert len({c['id'] for c in cases})==len(cases)==252
    checks['source_and_concept_references']={'status':'pass','concepts':50,'sources':25,'development_cases':252}
    missing=[r['id'] for row in coverage['concept_coverage'] for r in row['references'] if not r['found']]
    assert not missing,missing
    checks['existing_id_readback']={'status':'pass','resolved_reference_uses':sum(len(x['references']) for x in coverage['concept_coverage']),'claim':'ID existence only; no ranking or rendered coverage inferred'}
    base=pg.load_json(SKILL/'assets/photo_prompt_tags.json')
    registry=pg.load_visual_obligation_registry(SKILL/'assets/photo_prompt_visual_obligations.json')
    compiled=[compile_visual_profile(p) for p in proposed]
    assert len(compiled)==16
    gates=[g['id'] for p in compiled for g in p['render_gates']]
    assert len(gates)==len(set(gates))==64
    assert all(len(p['required_evidence_fields'])==4 for p in compiled)
    assert not ({p['id'] for p in compiled}&{p['id'] for p in registry['profiles']})
    checks['profile_compilation']={'status':'pass','profiles':16,'owner_scoped_gates':64,'runtime_installation':False}
    merged=pg.merge_research_extension(copy.deepcopy(base),copy.deepcopy(ext))
    cs.validate_candidate_entries(merged,pg.AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS)
    cs.validate_bundle_references(merged,[*registry['profiles'],*compiled])
    new=[b for b in merged['candidate_bundles'] if b['id'].startswith('pc_bundle_')]
    atoms=[a for rows in ext['slots'].values() for a in rows]
    assert len(new)==42 and len(atoms)==156
    assert len({a['id'] for a in atoms})==156
    assert all(b['profile_activation']=='independent_request_evidence_only' and b['adoption']=='optional' for b in new)
    assert all(len(a['concept_units'])==1 for a in atoms)
    assert 'http' not in json.dumps(ext) and 'S01' not in json.dumps(ext)
    assert not any('pm0' in a['id'] or 'ps0' in a['id'] for a in atoms)
    checks['candidate_merge_and_authority']={'status':'pass','atoms':156,'bundles':42,'claim':'In-memory compilation only; no live candidate pack or retrieval index updated'}
    # Isolate only proposed profiles. Existing profiles can legitimately match
    # a query without making the new draft a hard match.
    narrow={**registry,'profiles':compiled}
    index=pg.build_visual_profile_index_payload(narrow)
    def hard(text):
        out=pg.resolve_visual_profile_hits(narrow,[{'source':'concept_lock','text':text,'polarity':'required','priority':'critical','mandatory':True}],visual_profile_index=index,adult_context=True)
        return {h['profile_id'] for h in out['hits'] if h.get('match_basis')=='exact' and h.get('hard_eligible') is True}
    route_rows=[]
    for c in cases:
        if c['kind'] not in {'exact_definition','broad_label_no_hard','negated_definition','single_component_no_hard'}:continue
        actual=hard(c['query']); expected=set(c['expected_new_hard_profiles'])
        assert actual==expected,(c['id'],actual,expected)
        route_rows.append({'case_id':c['id'],'kind':c['kind'],'status':'pass','expected':sorted(expected),'actual':sorted(actual)})
    extra_route=0
    for p in proposed:
        for comp in p['authored_components']['components']:
            assert hard(comp['evidence_terms'][0])==set()
            extra_route+=1
    for c in catalog:
        for label in [c['label_ko'],*c['terms_en']]:
            assert not hard(label),(c['id'],label)
            extra_route+=1
    checks['narrow_activation']={'status':'pass','fixture_cases':len(route_rows),'additional_component_and_label_cases':extra_route,
      'fixture_kinds':dict(Counter(x['kind'] for x in route_rows)),'semantic_retrieval':'not_executed; no embedding generalization or exposure claim'}
    positives=missing_mutations=locked_mutations=0
    for b in new:
        pack={'slots':{},'authorial_core':{'intent_lock':{'open_dimensions':sorted({d for m in b['member_candidates'] for d in m['affected_dimensions']})}}}
        for m in b['member_candidates']:
            pack['slots'].setdefault(m['slot'],{'candidates':[]})['candidates'].append({'id':m['id'],'applicability':{'status':'eligible'}})
        subset={**merged,'candidate_bundles':[b]}
        assert len(cs.public_bundles(subset,pack)['candidates'])==1
        positives+=1
        for m in b['member_candidates']:
            bad=copy.deepcopy(pack)
            bad['slots'][m['slot']]['candidates']=[x for x in bad['slots'][m['slot']]['candidates'] if x['id']!=m['id']]
            assert cs.public_bundles(subset,bad)['candidates']==[]
            missing_mutations+=1
        for dim in pack['authorial_core']['intent_lock']['open_dimensions']:
            bad=copy.deepcopy(pack)
            bad['authorial_core']['intent_lock']['open_dimensions'].remove(dim)
            assert cs.public_bundles(subset,bad)['candidates']==[]
            locked_mutations+=1
    checks['bundle_missing_and_locked_dimensions']={'status':'pass','valid_admissions':positives,'missing_member_rejections':missing_mutations,'locked_dimension_rejections':locked_mutations}
    mutation_rejections=0
    for p in proposed:
        bad=copy.deepcopy(p)
        bad['authored_components']['components'][1]['evidence_field']=bad['authored_components']['components'][0]['evidence_field']
        try:compile_visual_profile(bad)
        except ValueError:mutation_rejections+=1
        else:raise AssertionError('duplicate owner evidence was accepted')
    checks['duplicate_evidence_mutations']={'status':'pass','rejections':mutation_rejections}
    changed=[path for path,expected in coverage['input_sha256'].items() if sha(ROOT/path)!=expected]
    checks['runtime_source_hash_readback']={'status':'pass' if not changed else 'concurrent_state_changed','changed_paths':changed,
      'claim':'This verifier writes only its report in the research folder; it does not repair, rebuild or overwrite runtime files.'}
    # These cases need a later semantic experiment, live pack, composed audit,
    # runtime request or native pixel inspection; structural checks cannot pass them.
    checks['unexecuted_layers']={'semantic_paraphrases':50,'pixel_confusion_cases':50,'request_priority_design_cases':20,
      'index_freshness':'not_checked','actual_candidate_exposure':'not_tested','composer_selection':'not_tested',
      'render_calls':0,'saved_images':0,'pixel_qualification':'not_tested','requester_preference':'not_received'}
    report={'schema_version':'portrait-research-verification/v1','checked_on':'2026-09-27','status':'pass_for_executed_structural_checks_only','checks':checks,'route_results':route_rows}
    (HERE/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'checks':checks},ensure_ascii=False,indent=2))

if __name__=='__main__':verify()
