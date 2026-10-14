"""Controlled independently authored research fixtures; never real user requests.
See SPEC-v1.md written before implementation for literal expectations.
"""
import copy
import hashlib
import json
import sys
from pathlib import Path
from envelope import digest, bind_source, source_binding, anchors_from_core, IndependentPins

G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
P=Path(__file__).resolve().parent;R=P.parent
PINNED={
'scripts/photo_native_owner_resolution.py':'cc1407f2ccfa3f00e3d6f2c73d964f934c4e33f501628b2c3c228aabbc04107f',
'scripts/photo_contracts.py':'0601699a58dbaa12376fa8439fbdda852b3dc4f069a82a4909f5711419eaa866',
'precore/photo_semantic_witnesses.py':'cc9bfca271ae1650c28a08b379bc84030b38a5cbcf9918c18d55d50a93094a58',
'scripts/photo_semantic_role_views.py':'74a1b412453766de85aef2c9a22f927f5b9b23de3ea4b3bd0358d1a69ae765f4'}
for rel,expected in PINNED.items():
 assert hashlib.sha256((G/rel).read_bytes()).hexdigest()==expected
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_native_owner_resolution as b1
import photo_contracts as contracts
w=b1.witnesses
assert Path(b1.__file__).resolve()==G/'scripts/photo_native_owner_resolution.py'
assert Path(contracts.__file__).resolve()==G/'scripts/photo_contracts.py'
assert Path(w.__file__).resolve()==G/'precore/photo_semantic_witnesses.py'
PRIMITIVES={'property_effects_allowed':contracts.property_effects_allowed,'owner_relation':w.owner_relation}
B=R/'native_batches/review11870-01299-149-06'
OLD=json.load(open(B/'FOOTPRINT-COUNTEREXAMPLE-v2.json'))
ASSESS=json.load(open(B/'SOURCE-ASSESSMENT-v1.json'))
CID=ASSESS['candidate_id'];CID2='cand_'+'e'*32
EREFS=['macroApp','coverageApp','exchangeApp']
PREFS=['initiatingPresence','otherPresence','initiatingType','otherType','itemPresence','itemKind','framePresence','itemVisiblePreservation']


def native(assertion_id, axes, dimension='subject'):
 return {'assertion_id':assertion_id,'dimension':dimension,'affected_dimensions':[dimension],'axes':{'native_schema':'photo-frozen-semantics/v1',**axes},'polarity':'required','source_span_ids':['scope'],'evidence':{'meaning':'Controlled independent request'}}


def core_pin(core):
 core['canonical_sha256']=digest({k:v for k,v in core.items() if k not in {'canonical_sha256','core_id'}})


def refresh(core, projection):
 # Test transport recomputation, never source semantics or inventory completeness.
 core_pin(core)
 frozen=w.read(core['semantic_assertions'],core['request_binding']['active_spans'],core['baseline_prompt_en'],intent_lock=core['intent_lock'],request_binding=core['request_binding'])
 scopes={s['scope_id']:s for s in frozen['member_scopes']}
 for n in projection['nodes']:
  for b in n['bindings']:
   if b['selection']['kind']=='existing_member_scope':b['selection']['scope_sha256']=digest(scopes[b['selection']['scope_id']])
  n['projection_sha256']=b1.node_digest(n)
 projection.update(core_sha256=core['canonical_sha256'],owner_graph_sha256=digest(frozen['graph']),member_scopes_sha256=digest(frozen['member_scopes']))
 return b1.resolve_selected_contracts(core,projection)


def full_source_context():
 facts=copy.deepcopy(ASSESS['literal_fact_sketch'])
 return {'candidate_id':CID,'realization_id':'base','source_snapshot_sha256':'8acdd741cdb846c8bb33b53ded16471363ece5747280b5b4893c25acdeed302d',
 'catalog_sha256':'d9f4db418e1b63cd100b4c7a9fbff4c8401e00dffeffd22e299a0b5087a82b15',
 'source_record':copy.deepcopy(ASSESS['whole_current_after']),'facts':facts,
 'source_units':copy.deepcopy(ASSESS['whole_unit_sketch']),
 'positive_fields':[{'realization_id':'base','pointer':'/content/'+p,'text':ASSESS['whole_current_after']['content'][p]} for p in ['en','ko','application_contract']],
 'ownbindings':copy.deepcopy(ASSESS['whole_ownbindings']),
 'closure_snapshot':{'selected_rids':['base'],'guards':copy.deepcopy(ASSESS['whole_current_after']['conditions']), 'CID_closure':{},'binding_closure':{},'profiles':{},'reference_sha256':{}},
 'canonical_effect_refs':EREFS.copy(),'required_preservation_refs':['itemVisiblePreservation']}


def contract(ctx):
 return {'schema':'research-permission-envelope-contract/v1','candidate_id':ctx['candidate_id'],'realization_id':'base',
 'basis':[{'fact_ref':e,'unit_pointer':next(f['pointer'] for f in ctx['facts'] if f['id']==e),'rationale':'Manually selected ordinary App fact; unchanged canonical target, property, operation, value, all Rx and requires.'} for e in ctx['canonical_effect_refs']]}


def make(same=False, anchor=None, impacts=None, joint=None, joint_impact='unknown'):
 old=OLD['actual_property_gap_counterexamples'][4 if same else 0]
 core=copy.deepcopy(old['core']);projection=copy.deepcopy(old['input_projection']);ctx=full_source_context()
 # Explicit request additions are independent fixture text, not candidate inference.
 addition=' Separately existing background object Z remains visible in I and is explicitly disjoint from I and each affected owner H1,H2,H3,X,U,F1,F2,R1,R2'+('' if same else ',V')+'. F1_alt is an explicitly declared alternative ID for exactly F1, not another face. X visibility is independently linked to image I. The event remains the selected physical item handoff while its moment and framing are open. The desired macro/hands-only result is not a frozen input fact.'
 core['baseline_prompt_en']+=addition;core['source_request']=core['baseline_prompt_en'];rb=core['request_binding'];rb['request_sha256']=hashlib.sha256(core['source_request'].encode()).hexdigest();rb['active_spans'][0].update(text=core['source_request'],end=len(core['source_request']));rb['input_inventory']['items'][0]['sha256']=rb['request_sha256']
 a=core['semantic_assertions'];a.extend([native('ownerZ',{'kind':'owner','owner':'Z','owner_kind':'entity'}),native('presenceZ',{'kind':'fact','owner':'Z','property':'entity.presence','value_type':'entity.presence/v1','value':'present'}),native('ownerAlias',{'kind':'owner','owner':'F1_alt','owner_kind':'entity'}),native('aliasFace',{'kind':'equivalent','left':'F1_alt','right':'F1'})])
 for owner in ['I','H1','H2','H3','X','U','F1','F2','R1','R2']+([] if same else ['V']):a.append(native('disjointZ_'+owner,{'kind':'disjoint','left':'Z','right':owner}))
 for row in a:
  if row['axes']['kind']=='existing_member_scope':
   inv=json.loads(row['axes']['inventory']);inv['input_binding']=w.input_binding(rb);row['axes']['inventory']=w.canonical(inv)
 if anchor:
  if anchor.get('kind')=='whole_dimension':
   core['intent_lock']['locked_dimensions'].append(anchor['dimension']);core['intent_lock']['open_dimensions']=[d for d in core['intent_lock']['open_dimensions'] if d!=anchor['dimension']]
  else:core['intent_lock']['semantic_anchors'].append({k:anchor[k] for k in ['dimension','target','property']})
 # Actual normalized canonical projection uses only the three App E, no duplicate EN/KO facts.
 projection['nodes'][0]['facts']=[{k:v for k,v in f.items() if k not in ['pointer','quote']} for f in ctx['facts'] if f['id'] in PREFS+EREFS]
 contexts=[ctx]
 if joint:
  target,prop=joint['target'],joint['property'];dim=joint.get('dimension','framing');val=joint.get('value','visible')
  phrase=f'Controlled other source selects {prop}={val} on exactly its independently declared object; every stated receiver remains actual.'
  f={'id':'otherE','realization_id':'base','pointer':'/content/en','quote':phrase,'mode':'effect','operation':'set_value','dimension':dim,'target':'other','property':prop,'value':{'type':prop+'/v1','value':val},'receivers':['also'] if joint.get('receiver') else [],'requires':['otherP']}
  pf={'id':'otherP','realization_id':'base','pointer':'/content/en','quote':'independently declared object','mode':'prerequisite','dimension':'subject','target':'other','property':'entity.presence','value':{'type':'entity.presence/v1','value':'present'},'requires':[]}
  source={'id':CID2,'conditions':{},'effects':{'dimensions':[dim],'properties':[{'dimension':dim,'target':'other','property':prop}]},'content':{'en':phrase},'record_kind':'visual_option'}
  c2={'candidate_id':CID2,'realization_id':'base','source_snapshot_sha256':digest(source),'catalog_sha256':ctx['catalog_sha256'],'source_record':source,'facts':[pf,f],'source_units':[{'disposition':'semantic','realization_id':'base','pointer':'/content/en','quote':phrase,'fact_refs':['otherP','otherE']}],'positive_fields':[{'realization_id':'base','pointer':'/content/en','text':phrase}],'ownbindings':{},'closure_snapshot':{'selected_rids':['base'],'guards':{},'CID_closure':{},'binding_closure':{},'profiles':{},'reference_sha256':{}},'canonical_effect_refs':['otherE'],'required_preservation_refs':[]}
  contexts.append(c2);bindings=[{'target':'other','origin':'existing','selection':{'kind':'selected_existing_owner','owner_id':target}}]
  if joint.get('receiver'):bindings.append({'target':'also','origin':'existing','selection':{'kind':'selected_existing_owner','owner_id':joint['receiver']}})
  n={'candidate_id':CID2,'realization_id':'base','meaning_sha256':digest(source),'qualification_sha256':digest({'synthetic-not-qualified':source}),'projection_sha256':'0'*64,'facts':[{k:v for k,v in q.items() if k not in ['pointer','quote']} for q in [pf,f]],'bindings':bindings,'guard_only_targets':[],'selected_children':[]};projection['nodes'].append(n);projection['roots'].append({'candidate_id':CID2,'realization_id':'base'})
 view=refresh(core,projection);bound=[bind_source(c,contract(c)) for c in contexts]
 source_pins={source_binding(b)['candidate_id']:source_binding(b) for b in bound}
 graph=view['permission_scope']['owner_graph'];members={b['selection']['scope_id']:[m['owner_id'] for m in b['members']] for n in view['nodes'] for b in n['bindings'] if b['selector_kind']=='existing_member_scope'}
 inv={'schema':'research-independent-permission-inventory/v1','phase':'before_discovery','core_sha256':core['canonical_sha256'],'core_payload_sha256':digest(core),'input_binding':view['context']['input_binding'],'topology_sha256':digest(graph),'owners':list(graph['owners']),'scope_members':members,'anchors':anchors_from_core(core),'reviewed_input_ids':['request'],'reviewed_span_ids':['scope'],'complete':True,'state':'known','reviewer':'controlled-independent-fixture-author','reason':'All actual synthetic request owners, explicit topology, input and scopes were written and manually reviewed before candidate discovery; no invisible input exists in this fixture.','witnesses':[{'candidate_id':CID,'source_fact_ref':'itemVisiblePreservation','target':'X','image':'I','dimension':'framing','property':'subject.visibility','value':{'type':'subject.visibility/v1','value':'visible'},'assertion_id':'item_visible','input_ids':['request'],'span_ids':['scope'],'frozen':True}]}
 review={'schema':'research-source-anchor-impact-review/v1','inventory_sha256':digest(inv),'resolved_view_sha256':digest(view),'source_bindings_sha256':digest(source_pins),'reviewer':'controlled-independent-manual-semantic-review','anchors':[],'joint':[]}
 effects={digest({k:f[k] for k in ['candidate_id','realization_id','fact_id','expansion_index','target']}):f for n in view['nodes'] for f in n['expanded_facts'] if f['mode']=='effect'}
 # Literal per-source semantic decisions. No keyword/property classifier is used.
 whole_reasons={
 'macroApp':'Macro shot-scale selection changes framing, not the already declared subject inventory, identity, age, fixed handoff event, count or concept.',
 'coverageApp':'Hands-only participant-anatomy coverage changes inclusion, while the original declared owners, identity, age, count and underlying handoff event remain present.',
 'exchangeApp':'The selected physical handoff instant changes the item action, while fixed entity identity, age, count, topology and the already selected handoff-event meaning remain unchanged.',
 'otherE':'The independently selected other-source local property change does not create entities, alter age/count/identity or replace the declared event.'}
 for ek,f in effects.items():
  for lock in inv['anchors']:
   state='disjoint';pr=None;reason=whole_reasons[f['fact_id']]
   if lock['kind']=='property':
    if lock['target']=='X' and lock['property']=='subject.visibility':
     reason='The same existing item X stays visibly present in the same active image I; exact independently frozen visibility PR is required, not physical presence.';pr='itemVisiblePreservation'
    else:
     # Tests provide explicit manual intended semantics for each case, never inferred from the property spelling.
     state=(impacts or {}).get(f['fact_id'],'unknown');reason='Independent manual reading of the selected source and this actual protected anchor: '+state+'. '+(anchor or {}).get('reason','No default semantic equivalence is asserted.')
   review['anchors'].append({'effect_key':ek,'anchor_key':digest(lock),'impact':state,'reason':reason,'input_ids':['request'],'span_ids':['scope'],'preservation_ref':pr})
 seen=set()
 for a,fa in effects.items():
  for b,fb in effects.items():
   if fa['candidate_id']==fb['candidate_id']:continue
   pair=tuple(sorted((a,b)))
   if pair in seen:continue
   seen.add(pair);review['joint'].append({'effect_keys':list(pair),'impact':joint_impact,'reason':'Independent joint manual judgment: '+joint_impact+'. Compare complete actual target and all receiver scopes, not role labels or new shadow E.','input_ids':['request'],'span_ids':['scope']})
 pins=IndependentPins(source_pins,digest(view),digest(inv),digest(review))
 return {'core':core,'projection':projection,'view':view,'inventory':inv,'assessment':review,'bound':bound,'contexts':contexts,'pins':pins}


def repin(f, inventory=False, assessment=False, view=False):
 """Only a test-author trust-root update; never expose as candidate self-approval."""
 p=f['pins'];f['pins']=IndependentPins(p.source_bindings,digest(f['view']) if view else p.resolved_view_sha256,digest(f['inventory']) if inventory else p.inventory_sha256,digest(f['assessment']) if assessment else p.assessment_sha256)
