"""Task-local artifact assembly helpers; these do not infer evidence or alter validators."""
import json,hashlib
from pathlib import Path


def canonical_sha(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def new_plan(route):
    return {'routing':{'analysis_profile':'audited','route_fingerprint':route['route_fingerprint'],'resolved_non_core_modules':[m for m in route['resolved_modules'] if not m.startswith('core.') and m!='concept.primary-relationship']},'direct_appeal_read':'','render_contract':{'mode':'appearance-led','perceptual_proposition':'','invariants':[],'flexible_dimensions':[],'major_regions':[],'component_relations':[],'placement_closures':[],'candidate_claims':[],'aggregate_effects':[],'emitted_controls':[],'prior_clusters':[]}}


def generic(plan,id,text,axis,owner,origin,evidence,role='primary',strength='moderate',regions=(),relations=(),control_axis=None):
    c=plan['render_contract']; inv={'id':id,'axis':axis,'role':role,'observation':text,'causal_origin':origin,'target_strength':strength,'source_evidence':evidence,'clause_owner':owner,'source_obligation_ids':[]}
    claim={'id':'claim-'+id,'semantic_slot':id,'owner':owner,'role':role,'polarity':'affirmative','target_strength':strength,'source_kind':'translated-causal-control','source_evidence':evidence,'emit':True,'salience_effects':[{'aggregate_effect_id':'effect-'+id,'source_evidence':evidence}]}
    effect={'id':'effect-'+id,'axis':axis,'direction':text,'role':role,'target_strength':strength,'claim_ids':[claim['id']],'region_ids':list(regions),'relation_ids':list(relations),'source_supported':True,'source_evidence':evidence}
    control={'id':'control-'+id,'prompt_excerpt':text,'claim_id':claim['id'],'owner':owner,'aggregate_effect_ids':[effect['id']]}
    if control_axis:
        effect.update(control_axis_id=control_axis,causal_origin=origin); control.update(control_axis_id=control_axis,causal_origin=origin)
    c['invariants'].append(inv); c['candidate_claims'].append(claim); c['aggregate_effects'].append(effect); c['emitted_controls'].append(control)
    return inv,claim,effect,control


def specialized(plan,kind,id,text,axis,region,layer,evidence,role='primary',strength='moderate',origin=None,reference=None):
    c=plan['render_contract']; iscolor=kind=='color'; owner='detail.color-tone-fidelity' if iscolor else 'detail.light-form-fidelity'; key='color_tone_contract' if iscolor else 'light_form_contract'; ledger=c[key]
    inv={'id':id,'axis':'color' if iscolor else 'light-to-form','role':role,'observation':text,'causal_origin':origin or ('intrinsic' if layer=='intrinsic' else 'lighting-shadow'),'target_strength':strength,'source_evidence':evidence,'clause_owner':owner,'source_obligation_ids':[]}
    claim={'id':'claim-'+id,'semantic_slot':id,'owner':owner,'role':role,'polarity':'affirmative','target_strength':strength,'source_kind':'translated-causal-control','source_evidence':evidence,'emit':True}
    contribution={'aggregate_effect_id':'effect-'+id,'confidence':'high','source_evidence':evidence}
    if iscolor: contribution['causal_layer']=layer
    claim['perceptual_effects' if iscolor else 'lighting_effects']=[contribution]
    effect={'id':'effect-'+id,'axis':axis,'region_id':region,'direction':text,'role':role,'target_strength':strength,'claim_ids':[claim['id']],'source_supported':True,'source_evidence':evidence}
    if reference: effect['reference_region_id']=reference
    control={'id':'control-'+id,'prompt_excerpt':text,'claim_id':claim['id'],'aggregate_effect_ids':[effect['id']]}
    if iscolor: control.update(causal_layer=layer,control_role='axis-control',region_id=region,axis=axis,protected_light_effect_ids=[])
    else: control['owner']=axis
    c['invariants'].append(inv); c['candidate_claims'].append(claim); ledger['claim_ids'].append(claim['id']); ledger['aggregate_effects'].append(effect); ledger['emitted_controls'].append(control)
    return inv,claim,effect,control


def save_json(path,value):
    Path(path).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
