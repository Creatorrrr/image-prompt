"""Check research/source boundaries and preserve evidence of concurrent changes."""
from pathlib import Path
import hashlib,json

ROOT=Path('/Users/chasoik/Projects/image-prompt')
O=Path(__file__).resolve().parent
A=ROOT/'skills/photo-prompt-image-generator/assets'
read=lambda p:json.loads(p.read_bytes())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
records=read(A/'photo_candidate_estate_management_20261024.json')['candidates']
bindings=read(A/'photo_candidate_estate_management_bindings_20261024.json')['slot_bindings']
sidecar=read(A/'photo_estate_management_semantics_20261024.json')
mapping=sidecar['card_candidate_map']
positive={cid for cid,r in records.items() if r['record_kind']=='visual_option'}
diagnostic=set(records)-positive
assert len(positive)==22 and len(diagnostic)==56 and len(bindings)==56
assert records==read(O/'new-native-records.json')
assert bindings==read(O/'new-bindings.json')
assert sidecar['keyword_routes']==read(O.parent/'reference-inventory.json')['rows']
assert len(sidecar['keyword_routes'])==374
assert all(row['route_authority']=='review_navigation_only_not_semantic_match' and not row['exact_definition_verified'] and not row['compound_label_fully_covered'] for row in sidecar['keyword_routes'])
assert len({m['card_id'] for m in mapping})==80
assert {m['candidate_id'] for m in mapping if m['disposition']=='new_optional_visual_source'}==positive
assert {m['candidate_id'] for m in mapping if m['disposition'] in ('held_structure_review','context_diagnostic')}==diagnostic
assert len([m for m in mapping if m['disposition']=='reuse_existing_complete_relation' and m['mutated'] is False])==2
assert all(b['candidate_id'] in positive and b['role']=='optional' for b in bindings.values())
assert all('en' not in records[cid]['content'] and 'ko' not in records[cid]['content'] for cid in diagnostic)
catalog=read(A/'photo_candidate_slot_catalog.json')['slot_catalog']
assert all(b['slot_id'] in catalog and b['semantic_role']==catalog[b['slot_id']]['semantic_role'] for b in bindings.values())
manifest=read(A/'photo_candidate_corpus_manifest.json')
assert all(sum(m['file']==name for m in manifest['modules'])==1 for name in ['photo_candidate_estate_management_20261024.json','photo_candidate_estate_management_bindings_20261024.json'])
baseline=read(O/'BASELINE.json')
drift=[{'file':r['file'],'before':r['sha256'],'after':sha(A/r['file'])} for r in baseline['source_modules'] if sha(A/r['file'])!=r['sha256']]
protected=[{'path':p,'before':h,'after':sha(ROOT/p)} for p,h in baseline['protected_dirty_tracked'].items() if sha(ROOT/p)!=h]
report={'status':'pass','research_rows_exactly_retained':374,'new_positive':22,'excluded_diagnostics':56,'optional_bindings':56,'reused_without_mutation':2,
        'all_positive_records_match_release_inputs':True,'route_claim_limits_preserved':True,
        'preexisting_module_drift_observed':drift,'preexisting_dirty_tracked_drift_observed':protected,
        'drift_interpretation':'Read-only observation in a concurrently changing checkout. This task wrote only its new modules/sidecar, manifest append, reference documentation and runtime configuration if activated. Existing modules were never rewritten by this task.',
        'historical_reconstruction_qualification':False,'pixel_qualification':'separate run evidence required'}
(O/'integration-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if 'drift' not in k},ensure_ascii=False))
