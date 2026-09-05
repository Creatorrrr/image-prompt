"""Case-local authoring helpers. No source conclusions or validator overrides."""
from copy import deepcopy

def make_plan(route):
    return {'routing':{'resolved_non_core_modules':[m for m in route['resolved_modules'] if not m.startswith('core.') and m!='concept.primary-relationship']},'direct_appeal_read':'','render_contract':{'mode':'mixed','perceptual_proposition':'','invariants':[],'flexible_dimensions':[],'major_regions':[],'component_relations':[],'placement_closures':[],'candidate_claims':[],'aggregate_effects':[],'emitted_controls':[],'prior_clusters':[]}}

def generic(plan, id, text, evidence, *, axis='form', owner='subject.human', origin='intrinsic', role='primary', strength='moderate', regions=(), relations=(), spatial_axis=None, appearance=None):
    c=plan['render_contract']; inv={'id':id,'axis':axis,'role':role,'observation':text,'causal_origin':origin,'target_strength':strength,'source_evidence':evidence,'clause_owner':owner,'source_obligation_ids':[]};c['invariants'].append(inv)
    claim={'id':'claim-'+id,'semantic_slot':id,'owner':owner,'role':role,'polarity':'affirmative','target_strength':strength,'source_kind':'visible-evidence','source_evidence':evidence,'emit':True,'salience_effects':[{'aggregate_effect_id':'effect-'+id,'source_evidence':evidence}]};c['candidate_claims'].append(claim)
    effect={'id':'effect-'+id,'axis':axis,'direction':text,'role':role,'target_strength':strength,'source_supported':True,'source_evidence':evidence,'claim_ids':[claim['id']],'region_ids':list(regions),'relation_ids':list(relations),'causal_origin':origin};c['aggregate_effects'].append(effect)
    control={'id':'control-'+id,'prompt_excerpt':text,'claim_id':claim['id'],'owner':owner,'aggregate_effect_ids':[effect['id']],'causal_origin':origin};c['emitted_controls'].append(control)
    if spatial_axis:effect['control_axis_id']=spatial_axis;control['control_axis_id']=spatial_axis
    if appearance:control['appearance_dimension']=appearance
    return inv,claim,effect,control

def relation(plan,id,kind,subject,observation,evidence,*,ref=None,frame=None,role='primary',**extra):
    r={'id':id,'kind':kind,'subject_region_id':subject,'observation':observation,'role':role,'source_evidence':evidence,**extra}
    if ref:r['reference_region_id']=ref
    if frame:r['frame_reference']=frame
    plan['render_contract']['component_relations'].append(r);return r

def color_contract(plan,importance='supporting'):
    c={'importance':importance,'observation_scope':'source-visible','global':{},'regions':[],'region_groups':[],'neutral_anchor_status':'uncertain','uncertainty_note':'No reliable calibrated neutral or scene-referred target is available.','neutral_anchors':[],'displayed_tone_response':[],'aggregate_effects':[],'claim_ids':[],'emitted_controls':[]}
    plan['render_contract']['color_tone_contract']=c;return c

def color(plan,id,text,evidence,*,region,axis,layer='intrinsic',role='supporting',strength='moderate',owner='detail.color-tone-fidelity'):
    c=plan['render_contract'];ct=c['color_tone_contract']
    inv={'id':id,'axis':'color','role':role,'observation':text,'causal_origin': {'intrinsic':'intrinsic','global-cast':'processing','processing':'processing','exposure':'processing','illumination':'lighting-shadow','hierarchy':'layout'}[layer],'target_strength':strength,'source_evidence':evidence,'clause_owner':owner,'source_obligation_ids':[]};c['invariants'].append(inv)
    claim={'id':'claim-'+id,'semantic_slot':id,'owner':owner,'role':role,'polarity':'affirmative','target_strength':strength,'source_kind':'visible-evidence','source_evidence':evidence,'emit':True,'perceptual_effects':[{'aggregate_effect_id':'effect-'+id,'causal_layer':layer,'confidence':'medium','source_evidence':evidence}]};c['candidate_claims'].append(claim)
    effect={'id':'effect-'+id,'axis':axis,'direction':text,'region_id':region,'role':role,'target_strength':strength,'source_supported':True,'source_evidence':evidence,'claim_ids':[claim['id']]};ct['aggregate_effects'].append(effect);ct['claim_ids'].append(claim['id'])
    control={'id':'control-'+id,'prompt_excerpt':text,'claim_id':claim['id'],'causal_layer':layer,'control_role':'axis-control','aggregate_effect_ids':[effect['id']],'region_id':region,'axis':axis};ct['emitted_controls'].append(control)
    return inv,claim,effect,control

def light_contract(plan, *, observed, hypothesis, dependency, importance='supporting'):
    c={'importance':importance,'observation_scope':'source-visible','observed_result':observed,'source_hypothesis':hypothesis,'regions':[],'region_effects':[],'shadow_events':[],'material_responses':[],'pose_light_dependency':dependency,'aggregate_effects':[],'claim_ids':[],'emitted_controls':[]};plan['render_contract']['light_form_contract']=c;return c

def light(plan,id,text,evidence,*,region,axis,role='supporting',strength='moderate',owner='medium.photographic-capture',reference=None):
    c=plan['render_contract'];lc=c['light_form_contract']
    inv={'id':id,'axis':'light-to-form','role':role,'observation':text,'causal_origin':'lighting-shadow','target_strength':strength,'source_evidence':evidence,'clause_owner':owner,'source_obligation_ids':[]};c['invariants'].append(inv)
    claim={'id':'claim-'+id,'semantic_slot':id,'owner':owner,'role':role,'polarity':'affirmative','target_strength':strength,'source_kind':'visible-evidence','source_evidence':evidence,'emit':True,'lighting_effects':[{'aggregate_effect_id':'effect-'+id,'confidence':'medium','source_evidence':evidence}]};c['candidate_claims'].append(claim)
    effect={'id':'effect-'+id,'axis':axis,'direction':text,'region_id':region,'role':role,'target_strength':strength,'source_supported':True,'source_evidence':evidence,'claim_ids':[claim['id']]}
    if reference:effect['reference_region_id']=reference
    lc['aggregate_effects'].append(effect);lc['claim_ids'].append(claim['id'])
    control={'id':'control-'+id,'prompt_excerpt':text,'claim_id':claim['id'],'owner':axis,'aggregate_effect_ids':[effect['id']]};lc['emitted_controls'].append(control)
    return inv,claim,effect,control
