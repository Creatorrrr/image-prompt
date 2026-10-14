"""Independent readonly prototype01 probes. False manual disjoint cannot waive known path overlap.
PR case deliberately demonstrates the disclosed supplement boundary, not an external-pin forgery.
"""
import copy,sys,json,hashlib,dataclasses,datetime
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');P=(R/'permission-envelope-prototype-01').resolve();O=R/'permission-envelope-review11870-01'
sys.path.insert(0,str(P))
from fixtures import make,repin,refresh,native,w,PRIMITIVES,EREFS
from envelope import compare,digest,IndependentPins
def run(f):return compare(f['bound'],core=f['core'],resolved_view=f['view'],inventory=f['inventory'],assessment=f['assessment'],expected=f['pins'],primitives=PRIMITIVES)
def observe(name,f,semantic_expected,category):
 try:r=run(f);allowed=r['permission_only_pass'];reasons=r['reasons']
 except ValueError as e:r=None;allowed=False;reasons=[str(e)]
 return {'name':name,'category':category,'manual_expected_permission_only':semantic_expected,'actual_permission_only':allowed,'matches_expectation':allowed==semantic_expected,'reasons':reasons,'fixture_digest':digest({k:v for k,v in f.items()if k not in ['bound','pins']}),'source_bindings':f['pins'].source_bindings,'original_E_and_Rx_unchanged':r is None or r['original_expanded_effects']==[e for n in f['view']['nodes']for e in n['expanded_facts']if e['mode']=='effect'],'native_B2_or_consumer_executed':False}
cases=[];examples=[]
# Each independent source2 selects a literal ancestor/descendant property on a
# same owner or actual receiver/alias/ancestor. Original1299 E3 stays byte-equal.
for name,target,prop,receiver in [
 ('same_image_parent_shot','I','shot',None),('same_image_child_shot','I','shot.scale.detail',None),
 ('same_image_parent_framing','I','framing',None),('same_image_child_coverage','I','framing.coverage.detail',None),
 ('same_item_action_parent','X','action.interaction',None),('actual_face_alias_parent','F1_alt','framing',None),
 ('actual_hand_carrier_ancestor','U','action.interaction',None),('other_source_receiver_face_parent','Z','framing','F1')]:
 f=make(joint={'target':target,'property':prop,'value':'independent_selected_state',**({'receiver':receiver}if receiver else{})},joint_impact='disjoint')
 c=observe(name,f,False,'known_joint_property_path_overlap')
 # Permission primitive already defines exactly this overlap; do not add aliases.
 left=next(e for e in f['view']['nodes'][0]['expanded_facts']if e['fact_id']==('exchangeApp'if prop.startswith('action')else 'macroApp'if prop.startswith('shot')else 'coverageApp'))
 right=next(e for e in f['view']['nodes'][1]['expanded_facts']if e['mode']=='effect')
 targets=lambda e:sorted({e['target']['canonical_owner_id'],*e['canonical_receivers']})
 lock={'contract_version':'photo-intent-lock/v2','semantic_anchors':[{'dimension':right['dimension'],'target':t,'property':right['property']}for t in targets(right)]}
 es=[{'dimension':left['dimension'],'target':t,'property':left['property']}for t in targets(left)]
 c['frozen_primitive_allows_same_actual_pair']=PRIMITIVES['property_effects_allowed'](lock,[left['dimension']],es,owner_graph=f['view']['permission_scope']['owner_graph'])
 cases.append(c)
 if name in ['same_image_parent_shot','other_source_receiver_face_parent']:examples.append({'name':name,'core':f['core'],'projection':f['projection'],'view':f['view'],'inventory':f['inventory'],'assessment':f['assessment'],'source_contexts':f['contexts'],'independent_pins':dataclasses.asdict(f['pins'])})
for name,target,prop in [('same_image_unrelated','I','custom.unrelated_palette'),('related_carrier_unrelated','U','custom.surface_finish'),('disjoint_Z_parent','Z','shot'),('substring_not_alias','I','not_shot.scale_copy')]:
 f=make(joint={'target':target,'property':prop,'value':'independent_selected_state'},joint_impact='disjoint');cases.append(observe(name,f,True,'independently_reviewed_unrelated_control'))
# New independently authored two-image request. The actual item visibility row
# is grounded only in I2 span; current native fact tuple has no image axis.
f=make();core=f['core'];oldpins=f['pins'];body=core['baseline_prompt_en'].replace('X remains independently visible in I.','X visibility in active image I is unspecified.').replace('X visibility is independently linked to image I.','').replace('No other participant, hidden carrier, reference image or unreviewed input exists in this synthetic request.','No hidden participant or unreviewed input exists in this synthetic request; two images are explicitly declared.')
clause=' A separately existing image I2 shows item X visibly. This visibility statement concerns I2 only and does not establish X visibility in I.'
body+=clause;core['baseline_prompt_en']=body;core['source_request']=body;rb=core['request_binding'];rb['request_sha256']=hashlib.sha256(body.encode()).hexdigest();rb['active_spans'][0].update(text=body,end=len(body));rb['active_spans'].append({'span_id':'image2','start':len(body)-len(clause),'end':len(body),'text':clause});rb['input_inventory']['items'][0]['sha256']=rb['request_sha256']
core['semantic_assertions'] += [native('image2owner',{'kind':'owner','owner':'I2','owner_kind':'entity'}),native('image2presence',{'kind':'fact','owner':'I2','property':'entity.presence','value_type':'entity.presence/v1','value':'present'})]
visible=next(a for a in core['semantic_assertions']if a['assertion_id']=='item_visible');visible['source_span_ids']=['image2'];visible['evidence']={'meaning':clause.strip()}
for a in core['semantic_assertions']:
 if a['axes']['kind']=='existing_member_scope':
  inv=json.loads(a['axes']['inventory']);inv['input_binding']=w.input_binding(rb);a['axes']['inventory']=w.canonical(inv)
f['view']=refresh(core,f['projection']);v=f['view'];f['inventory'].update(core_sha256=core['canonical_sha256'],core_payload_sha256=digest(core),input_binding=v['context']['input_binding'],topology_sha256=v['context']['owner_graph_sha256'],owners=list(v['permission_scope']['owner_graph']['owners']),reviewed_span_ids=['scope','image2']);f['assessment'].update(inventory_sha256=digest(f['inventory']),resolved_view_sha256=digest(v))
# Holding the original independent roots rejects a rewritten table/view.
cases.append(observe('two_image_rewrite_with_original_retained_pins',f,False,'independent_pin_negative'))
# A deliberately wrong independent annotation is not mechanically checked back
# to I2. This repins trusted test-author evidence; no candidate forged authority.
f['pins']=IndependentPins(oldpins.source_bindings,digest(v),digest(f['inventory']),digest(f['assessment']));cases.append(observe('native_visibility_only_I2_but_supplement_labels_I',f,False,'disclosed_unimplemented_same_image_PR_matching'))
examples.append(copy.deepcopy({'name':'native_visibility_only_I2_but_supplement_labels_I','core':core,'projection':f['projection'],'view':v,'inventory':f['inventory'],'assessment':f['assessment'],'source_contexts':f['contexts'],'independent_pins':dataclasses.asdict(f['pins']),'qualification':'The independently trusted witness annotation is intentionally semantically wrong; shows absent image binding, not a pin authentication bypass.'}))
f['inventory']['witnesses'][0]['image']='I2';f['assessment']['inventory_sha256']=digest(f['inventory']);repin(f,inventory=True,assessment=True);cases.append(observe('honest_I2_supplement_rejected_for_selected_I',f,False,'honest_wrong_image_negative'))
out={'schema':'permission-envelope-independent-counterexamples/v1','task':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'prototype':'01 immutable','cases':cases,'complete_examples':examples,'boundary':'Actual frozen B1 and property primitive only; no native qualification/B2/fullcompact/consumer/image-specific state proof. External pins protect candidate alteration but do not make semantically wrong independent annotations true.','native_proof_count':0,'operating_count':0,'network_denied':True}
p=O/'COUNTEREXAMPLES-v2.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print('cases',len(cases),'joint_holes',sum(not c['matches_expectation']for c in cases if c['category']=='known_joint_property_path_overlap'),'PR_boundary',sum(not c['matches_expectation']for c in cases if c['category'].startswith('disclosed')),'canon',digest(out))
