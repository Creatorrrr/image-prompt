"""Negative checks against real qualified packs, receipts and final prose."""
import copy
import hashlib
import json
from pathlib import Path
import sys

OUT = Path(__file__).resolve().parent
meta = json.loads((OUT/'QUALIFIED-RUNTIME.json').read_text())
sys.path.insert(0, str(Path(meta['sealed_root'])/'scripts'))
import audit_composed_prompt as ca
import audit_image_render_request as ra
from photo_runtime_sources import RuntimeSnapshotProvider, FreshnessError, json_digest, pack_bindings

provider = RuntimeSnapshotProvider(Path(meta['sealed_root']), Path(meta['store']))
results = []


def save(name, value):
    (OUT/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')


def case(name):
    pack_path = OUT/'qualified-public-natural'/name/'candidate-pack.json'
    folder = OUT/'qualified-composition'/name/'reject-all'
    return (json.loads(pack_path.read_text())[0],
            json.loads(Path(str(pack_path)+'.runtime-receipt.json').read_text()),
            json.loads((folder/'FINAL-COMPOSED.json').read_text()),
            json.loads((folder/'RENDER-REQUEST.json').read_text()))


def record(name, failures, inputs):
    assert failures, name
    results.append(dict(name=name, rejected=True, failures=failures,
                        input_sha256={k:json_digest(v) for k,v in inputs.items()}))
    save('TAMPER-VALIDATION.json', dict(generation_id=meta['generation_id'],
        source_fingerprint=meta['source_fingerprint'], negative_cases=len(results),
        rejection_count=len(results), cases=results, image_calls=0))
    print(json.dumps(dict(name=name,rejected=True,checks=[r['check'] for r in failures])), flush=True)


def forged_receipt(pack, original):
    receipt = copy.deepcopy(original)
    receipt['pack_sha256'] = json_digest(pack)
    receipt['bindings'] = pack_bindings(pack)
    receipt['canonical_sha256'] = json_digest({k:v for k,v in receipt.items() if k!='canonical_sha256'})
    return receipt


def receipt_rejection(name, pack, receipt):
    try:
        provider.from_receipt(pack, receipt)
    except FreshnessError as exc:
        record(name, [dict(check='receipt_source_recomputation', reason=str(exc))],
               dict(pack=pack,receipt=receipt))
    else:
        raise AssertionError(name+' was accepted')


def main():
    cup, cup_receipt, cup_final, cup_request = case('dev-02-blue-cup-en')
    snapshot = provider.from_receipt(cup, cup_receipt)
    assert ca.audit_composed_prompt(cup,cup_final,source_data=snapshot.data)['status']=='pass'
    assert ra.audit_image_render_request(cup,cup_final,cup_request)['status']=='pass'
    for mutation in ('delete_ordinary_candidate','substitute_source_id','forge_candidate_terms'):
        pack = copy.deepcopy(cup)
        candidates = pack['slots']['subject']['candidates']
        if mutation=='delete_ordinary_candidate':
            candidates.pop()
        elif mutation=='substitute_source_id':
            candidates[0]['id']='slot:subject:unregistered_impostor'
        else:
            candidates[0]['concept_terms']=['a walking mechanical actor instead of the requested cup']
            candidates[0]['concept_units']=candidates[0]['concept_terms'][:]
        receipt_rejection(mutation,pack,forged_receipt(pack,cup_receipt))
    pack=copy.deepcopy(cup)
    pack['core_retrieval']['slot_corpus_sha256']='0'*64
    receipt_rejection('forged_source_corpus_hash',pack,forged_receipt(pack,cup_receipt))
    for field,name in [('source_fingerprint','forged_receipt_source_hash'),('algorithm_sha256','stale_receipt_code_binding')]:
        receipt=copy.deepcopy(cup_receipt);receipt[field]='0'*64
        receipt['canonical_sha256']=json_digest({k:v for k,v in receipt.items() if k!='canonical_sha256'})
        receipt_rejection(name,cup,receipt)
    leaf, leaf_receipt, final, request = case('dev-07-dew-leaf-ko')
    leaf_snapshot=provider.from_receipt(leaf,leaf_receipt)
    candidate=next(c for slot in leaf['slots'].values() for c in slot['candidates'] if c['id']=='slot:light_direction:backlight')
    assert candidate['applicability']['status']=='ineligible'
    forced=copy.deepcopy(final);forced['chosen_candidate_ids']=[candidate['id']]
    phrase='Backlight from behind the subject remains on the same dew-covered leaf.'
    forced['prompt_en']+=' '+phrase
    forced['embodiment_review']['review']['prompt_sha256']=hashlib.sha256(forced['prompt_en'].encode()).hexdigest()
    forced['candidate_interpretations']=[dict(candidate_id=candidate['id'],artistic_interpretation='Keep the stated backlight.',
        transformation='Retain the existing leaf view.',prompt_evidence=phrase,
        affected_dimensions=candidate['affected_dimensions'],affected_properties=candidate.get('affected_properties',[]))]
    audit=ca.audit_composed_prompt(leaf,forced,source_data=leaf_snapshot.data)
    record('force_ineligible_locked_lighting_candidate',audit['failures'],dict(pack=leaf,composed=forced))
    assert any('applicability' in row['check'] or 'property' in row['check'] for row in audit['failures']),audit['failures']
    golem, golem_receipt, final, request=case('holdout-10-fantasy-ko')
    golem_snapshot=provider.from_receipt(golem,golem_receipt)
    missing=copy.deepcopy(final)
    del missing['visual_obligation_evidence']['golem_constructed_material_agency']['task_phrase']
    record('missing_required_golem_task_component',ca.audit_composed_prompt(golem,missing,source_data=golem_snapshot.data)['failures'],dict(pack=golem,composed=missing))
    stale=copy.deepcopy(final);stale['prompt_en']+=' A soft highlight follows an existing stone seam.'
    failures=ca.photo_embodiment.audit_composed(golem,stale)
    record('stale_postcomposition_embodiment_review',failures,dict(pack=golem,composed=stale))
    for name in ('runtime_only_new_action','runtime_negative_byte_drift','runtime_retrieval_hash_drift'):
        modified=copy.deepcopy(request)
        if name=='runtime_only_new_action':modified['runtime_prompt_en']+=' The golem lifts a new heavy load.'
        elif name=='runtime_negative_byte_drift':modified['runtime_negative_en']=(modified['runtime_negative_en'] or '')+' '
        else:modified['core_retrieval_sha256']='0'*64
        record(name,ra.audit_image_render_request(golem,final,modified)['failures'],dict(pack=golem,composed=final,request=modified))
    assert len(results)==12


if __name__=='__main__':
    main()
