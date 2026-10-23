"""Scoped authored Gaslamp sources; preserves all pre-existing candidate records."""
from pathlib import Path
import copy, hashlib, json, sys, uuid
O=Path(__file__).resolve().parent
R=O.parents[4]; S=R/'skills/photo-prompt-image-generator'; A=S/'assets'; Q=O.parent
sys.path.insert(0,str(S/'scripts'))
import photo_candidate_corpus as corpus
def read(p): return json.loads(p.read_bytes())
def write(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
NS=uuid.UUID('ab37295b-14b7-4b66-a44f-e5318ca7d785')
def ident(prefix,label): return prefix+uuid.uuid5(NS,label).hex
REUSE={
 'G16':('cand_99e57a00d9ed53e0814df0f912633426','Continuous pull–wire–service bell is already explicit; use its exact full source. Spring or lever subtypes are not thereby certified.'),
 'G28':('cand_3671de101025584d832f8dc031a5ec61','Existing bustle volume and its skirt owner are preserved. Its complete wording governs; generic market bustle does not qualify.'),
 'G37':('cand_4375105f2a13508f89054e385d6c9c41','Existing braided-hair locket already preserves hinge and chain and the non-mourning boundary. Glass is not added to that source by this mapping.'),
 'G47':('cand_a65c27b912175fa28ed24b0fec6c3ea1','Existing open bound book has an invented diagram and marginal notes on that same page. Preserve those extra notes when using it.'),
 'G56':('cand_53801d41b5e55a64b1da60297c42198c','Existing human/nonhuman parties share one parchment with separate touched edges. Broad existing effects remain unchanged and grant no native admission.'),
 'G81':('cand_31249a68bccc53fd955a332e036aa6af','Existing seated adult, wrist cuff and chair attachment already form the full connected relation. Consent or imprisonment is not established.')
}
HELD={'G70':'Specific phrenology model divisions need artifact-level source review; retained only as diagnostic context.'}
CONTRACT=('One optional complete authored visual realization. Preserve the complete bilingual proposition, each owner, component, count, representation layer, contact, boundary and directed connection. '
 'Only use within independently frozen requester meaning and all affected dimensions and properties. Genre labels never activate this realization. '
 'All distinguishing endpoints must be simultaneously legible; partial_is_fail; UNOBSERVABLE_NOT_PASS. '
 'Research graphs, references, tags and citations confer no typed native facts, owner permission or native qualification. '
 'A visible proxy does not prove fuel chemistry, material identity, historical authenticity, occupation, class, rights, diagnosis, death, consent, identity, motives, temporal sequence, sound or supernatural cause.')
# These declarations delimit actual changes rather than multiplying every owner by every dimension.
DIMENSIONS={
 'light_type':['lighting','appearance'], 'object_structure':['appearance'],
 'action':['action'], 'contact_point':['action','relationship'], 'location':['setting'],
 'environment_detail':['setting'], 'atmospheric_medium':['atmosphere'], 'spatial_depth':['composition'],
 'space_condition':['setting'], 'relational_action':['action','relationship'], 'proxemics':['relationship','composition'],
 'social_cue':['relationship'], 'prop_placement':['composition'], 'participant_role':['role'],
 'prop':['subject'], 'garment_detail':['appearance'], 'wardrobe_layering':['appearance'],
 'silhouette_proportion':['appearance'], 'wearable_accessory':['appearance'], 'shadow_relation':['lighting'],
 'hand_pose':['pose'], 'wardrobe_style':['appearance'], 'surface_material':['material'],
 'situation_context':['setting'], 'surreal_physics_detail':['appearance'], 'image_artifact':['appearance'],
 'reflection_logic':['appearance','relationship'], 'material_form':['material'], 'visible_text':['text'],
 'gaze_target':['action','relationship'], 'surface_pattern':['appearance'], 'surreal_concept':['concept','appearance'],
 'companion_animal':['subject','relationship'], 'species_marker':['species','appearance'],
 'body_form':['body_geometry'], 'transformation_stage':['appearance'], 'prop_state':['appearance'],
 'subject_count':['count'], 'scale_relation':['composition'], 'anatomical_connection':['body_geometry','relationship'],
 'viewer_position':['camera'], 'narrative_clue':['appearance'], 'body_region':['body_geometry'],
 'aftermath_trace':['appearance'], 'liquid_inclusion':['material']}

def main():
 assert not (O/'data-integration.json').exists(),'Do not overwrite integration history'
 before=corpus.load(A); cards=read(Q/'semantic-cards.json')['cards']; drafts={d['card_id']:d for d in read(Q/'candidate-drafts.json')['drafts']}
 reviewed_aliases=read(O/'discovery-alias-review.json')['aliases']
 neighbors={r['card']:r for r in read(O/'overlap-review-input.json')}
 rows=[];new={};bindings={};enriched=[]
 exact={(v['content'].get('en'),v['content'].get('ko')) for v in before['candidates'].values()}
 for original in cards:
  card=copy.deepcopy(original);k=card['id'];d=drafts.get(k)
  mode='context' if d is None else 'defer' if k in HELD else 'reuse' if k in REUSE else 'new'
  if mode=='reuse':
   cid,reason=REUSE[k];record=before['candidates'][cid]
   review={'candidate_id':cid,'canonical_source_sha256':corpus.digest(record),'complete_source':record,'reason':reason,'mapping_scope':'existing complete realization, not unconditional equivalence to every draft qualifier'}
   rows.append({'card_id':k,'decision':mode,**review});card.update(candidate_ids=[cid],integration_status='existing_source_reused',adoption_review=review)
  else:
   visual=mode=='new';cid=ident('cand_','gaslamp:'+k)
   assert cid not in before['candidates']
   slots=[b['slot_id'] for b in d['proposed_bindings']] if visual else []
   for slot in slots: assert slot in before['slot_catalog'] and slot in DIMENSIONS,slot
   reason=HELD.get(k) if mode=='defer' else ('Nonvisual context is excluded from positive material search.' if mode=='context' else 'Distinct complete relation or component state retained. Nearest lexical sources are comparisons, not evidence of semantic absence; no exact bilingual duplicate found. Full source constraints remain separate.')
   meta={**copy.deepcopy(card),'native_approval':False,'native_qualification':'not_qualified','graph_scope':'research review metadata; no typed native facts or adoption authority','registration_status':'authored_source_module','integration_status':'optional_visual_source' if visual else 'held_diagnostic' if mode=='defer' else 'context_diagnostic','pixel_status':'NOT_RUN_FOR_THIS_SOURCE','candidate_id':cid,'translation_review':'EN/KO named owners and relations manually compared; no independent translator certification'}
   if visual:
    assert (d['positive_en'],d['positive_ko']) not in exact,'Exact duplicate needs reuse'
    content={'en':d['positive_en'],'ko':d['positive_ko'],'definition':'Optional complete authored visual realization: '+d['positive_en'],'aliases':[card['title_ko'],reviewed_aliases[k]],'application_contract':CONTRACT,'research_semantics':meta}
    effects={'dimensions':sorted(set(x for slot in slots for x in DIMENSIONS[slot])),'properties':[]}
   else:
    content={'definition':('Held diagnostic, excluded from positive visual retrieval: ' if mode=='defer' else 'Context-only diagnostic, excluded from positive visual retrieval: ')+card['title_ko']+'. '+card['claim_limit_ko'],'research_semantics':meta};effects={'dimensions':[],'properties':[]}
   record={'id':cid,'record_kind':'visual_option' if visual else 'diagnostic','content':content,'conditions':{},'effects':effects,'provenance':[{'source':'authored research '+str(Q.relative_to(R))+'/semantic-cards.json#'+k+'; context '+ref['url'],'sha256':sha(Q/'semantic-cards.json')} for ref in card['source_refs']]}
   new[cid]=record
   for slot in slots:
    bid=ident('bind_',cid+':'+slot);bindings[bid]={'id':bid,'candidate_id':cid,'slot_id':slot,'role':'optional','semantic_role':before['slot_catalog'][slot]['semantic_role'],'conditions':{'subject_applicability':{}},'weight':2}
   rows.append({'card_id':k,'decision':mode,'candidate_id':cid,'reason':reason,'comparison_candidates':[{'candidate_id':x['cid'],'source_sha256':corpus.digest(x['record']),'complete_source':x['record']} for x in neighbors.get(k,{}).get('nearest',[])],'native_qualification':False,'actual_slots':slots})
   card.update(candidate_ids=[cid],integration_status=meta['integration_status'])
  card.update(native_approval=False,automatic_hard_activation=False,registration_status='authored_registry',decision=mode)
  enriched.append(card)
 assert len(enriched)==113
 candidate_name='photo_candidate_gaslamp_fantasy_20261023.json';binding_name='photo_candidate_gaslamp_fantasy_bindings_20261023.json'
 for name,body in [(candidate_name,{'schema':corpus.MODULE_SCHEMAS['candidates'],'candidates':new}),(binding_name,{'schema':corpus.MODULE_SCHEMAS['slot_bindings'],'slot_bindings':bindings})]:
  assert not (A/name).exists();write(A/name,body)
 manifest=read(A/corpus.MANIFEST_NAME)
 for name,kind in [(candidate_name,'candidates'),(binding_name,'slot_bindings')]:
  assert not any(m['file']==name for m in manifest['modules']);manifest['modules'].append({'file':name,'kind':kind})
 write(A/corpus.MANIFEST_NAME,manifest)
 bycard={c['id']:c['candidate_ids'] for c in enriched}
 routes=read(Q/'keyword-routes.json')['routes']
 for route in routes:route.update(candidate_ids=list(dict.fromkeys(cid for k in route['route_card_ids'] for cid in bycard[k])),automatic_hard_activation=False)
 registry={'schema':'photo-gaslamp-fantasy-visual-semantics/v1','cards':enriched,'keyword_routes':routes,'sources':read(Q/'sources.json'),'native_approval':False,'automatic_hard_activation':False,'source_research_sha256':sha(Q/'semantic-cards.json'),'claim_scope':'Citations support only their recorded access scope; concrete geometry is authored. Context terms never become required visual appearance.'}
 write(A/'photo_gaslamp_fantasy_semantics_20261023.json',registry)
 after=corpus.load(A)
 assert all(after['candidates'][cid]==record for cid,record in before['candidates'].items())
 assert all(after['slot_bindings'][bid]==record for bid,record in before['slot_bindings'].items())
 assert all(after[k]==before[k] for k in ['slot_catalog','policies'])
 write(O/'new-native-records.json',new);write(O/'changed-native-records.json',{})
 write(O/'adoption-review.json',rows)
 summary={'status':'source_integrated','cards':len(enriched),'routes':len(routes),'new_visual_sources':sum(x['record_kind']=='visual_option' for x in new.values()),'new_diagnostics':sum(x['record_kind']=='diagnostic' for x in new.values()),'reused_sources':len(REUSE),'held_cards':list(HELD),'new_bindings':len(bindings),'before_CIDs':len(before['candidates']),'after_CIDs':len(after['candidates']),'existing_records_bindings_catalog_policies_unchanged':True,'native_approval':False,'adoptions':[{k:x[k] for k in ['card_id','decision','candidate_id']} for x in rows]}
 write(O/'data-integration.json',summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
