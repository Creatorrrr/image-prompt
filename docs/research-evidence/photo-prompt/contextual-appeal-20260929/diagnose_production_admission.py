#!/usr/bin/env python3
"""Recompute admission only from frozen production artifacts, without API calls."""
import json,sys,collections,pathlib
root=pathlib.Path(__file__).resolve().parents[4];sys.path.insert(0,str(root/'skills/photo-prompt-image-generator/scripts'))
import prompt_generator as g
D=g.load_json(root/'skills/photo-prompt-image-generator/assets/photo_prompt_tags.json')
D[g.QUALITY_LAYERS_DATA_KEY]=g.load_json(root/'skills/photo-prompt-image-generator/assets/photo_prompt_quality_layers.json')
P=g.candidate_pack_hybrid_policy(D)['adult_appeal']
new={e['id'] for rows in json.loads((root/'skills/photo-prompt-image-generator/assets/photo_prompt_contextual_appeal_extension.json').read_text())['slots'].values() for e in rows}
identity={'subject','appearance_type','age','species','species_morphology','face','body_type','person_origin'}
report={'schema_version':'contextual-appeal-production-admission-diagnostic/v1','method':'Read-only replay of admission predicates against saved production packs; no new candidate packs, queries or image calls.','arms':{}}
for arm in ['craft','sensory','mirror']:
 p=root/'artifacts/photo-prompt-runs/research-integration-20260929'/arm
 pack=json.loads((p/'candidate_pack.json').read_text()); pack=pack[0] if isinstance(pack,list) else pack
 core=pack['authorial_core']; snapshot=pack['creative_controls']; contract=pack['adult_appeal'];lock=core['intent_lock']
 constraints={'subject_category':snapshot['context']['subject_category'],'preset_domains':[],'adult_allowed':contract['eligibility']['status']=='eligible','intent_constraints':g.authorial_core_generation_constraints(core)}
 exclusions=[g.candidate_pack_v5_relevance_tokens(v) for v in core.get('user_exclusions',[])]
 axis_results={}
 for axis in ['sensual_editorial','fetish_fashion']:
  allowed=set(contract['dimension_scope']['axis_allowed_dimensions'][axis]); admitted=[];blocked=[];total=0
  for slot,entries in D['slots'].items():
   for entry in entries:
    key=f"{slot}:{entry['id']}";dims=sorted(set(entry.get('affected_dimensions',[]))|set(P.get('entry_dimensions',{}).get(key,[])))
    dims=dims or g.photo_candidate_semantics.slot_dimensions(slot,D.get('candidate_semantic_policy'))
    reasons=[]
    if slot in identity:reasons.append('identity_slot')
    if r:=g.slot_block_reason(D,slot,constraints):reasons.append('slot_guard:'+str(r))
    if not dims or not set(dims)<=allowed:reasons.append('outside_dimensions:'+','.join(sorted(set(dims)-allowed)))
    if not g.property_effects_allowed(lock,dims,entry.get('affected_properties',[])):reasons.append('property_lock')
    if r:=g.entry_block_reason(entry,slot,constraints):reasons.append('entry_guard:'+str(r))
    if not g.compatible_with_facet_guards(entry,{},{}):reasons.append('facet_guard')
    fields=g.semantic_bm25f_fields_for_entry(entry,slot,kind='slot');tokens=g.candidate_pack_v5_relevance_tokens(' '.join(str(v) for values in fields.values() for v in values))
    if any(group and group<=tokens for group in exclusions):reasons.append('user_exclusion')
    if not reasons:total+=1
    if entry['id'] in new:
     (blocked if reasons else admitted).append({'source_candidate_id':'slot:'+key,'reasons':reasons})
  returned=contract['axes'][axis]['candidate_inventory']
  axis_results[axis]={'all_admitted_count':total,'saved_pack_eligible_count':contract['contextual_retrieval']['axes'][axis]['eligible_corpus_count'],'new_admitted_count':len(admitted),'new_blocked_count':len(blocked),'new_returned_count':sum(r['entry_id'] in new for r in returned),'new_admitted_ids':[r['source_candidate_id'] for r in admitted],'new_blocked':blocked,'block_reasons':dict(collections.Counter(r for row in blocked for r in row['reasons']))}
 report['arms'][arm]=axis_results
out=root/'docs/research-evidence/photo-prompt/contextual-appeal-20260929/production-admission-diagnostic.json';out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({arm:{axis:{k:v for k,v in row.items() if k not in ['new_admitted_ids','new_blocked']} for axis,row in axes.items()} for arm,axes in report['arms'].items()},ensure_ascii=False,indent=2))
