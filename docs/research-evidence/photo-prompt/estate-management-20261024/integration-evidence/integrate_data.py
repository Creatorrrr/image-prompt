"""Register reviewed bounded visual sources; preserve held and context records."""
from pathlib import Path
import copy,hashlib,json,sys,uuid
ROOT=Path('/Users/chasoik/Projects/image-prompt')
SKILL=ROOT/'skills/photo-prompt-image-generator';OUT=Path(__file__).resolve().parent;RESEARCH=OUT.parent
sys.path.insert(0,str(SKILL/'scripts'))
import photo_candidate_corpus as corpus
read=lambda p:json.loads(p.read_bytes())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def cid(label):return 'cand_'+uuid.uuid5(uuid.NAMESPACE_URL,'image-prompt/estate-management-20261024/'+label).hex
def bid(label):return 'bind_'+uuid.uuid5(uuid.NAMESPACE_URL,'image-prompt/estate-management-20261024/'+label).hex
data=read(RESEARCH/'semantic-cards.json');inventory=read(RESEARCH/'reference-inventory.json');sources=read(RESEARCH/'sources.json')
catalog=read(SKILL/'assets/photo_candidate_slot_catalog.json')['slot_catalog']
reuse={'D02':'cand_8f33f22aa0de5e3dbb8815b70d686d3e','F07':'cand_a1425f8956985eaeafa7c7a7c954255a'}
# Independently authored, conservative whole-source mutation footprints. These are
# review declarations, not typed native facts or permissions inferred from slots.
effects={
 'A01':['setting','composition'],'A02':['setting','composition'],
 'A07':['setting','composition','action'],'A08':['setting','composition'],
 'B01':['action','pose','relationship','composition'],'B04':['action','pose','relationship','setting'],
 'B05':['action','pose','relationship','setting','composition'],
 'B06':['action','pose','expression','composition'],'B08':['action','composition'],
 'C07':['action','pose','expression','relationship','composition'],
 'D01':['pose','relationship','setting','composition'],'D08':['action','setting','composition'],
 'E01':['pose','relationship'],'E02':['pose','relationship','composition'],
 'E03':['action','pose','relationship'],'E04':['action','pose','expression','relationship','setting'],
 'E05':['action','pose','composition'],'E06':['action','pose','expression','relationship','composition'],
 'E07':['action','pose','relationship','composition'],'F01':['appearance'],
 'F05':['appearance','relationship'],'G04':['appearance','relationship'],
}
application=('One optional complete authored visual realization. Preserve every named actor, object, body part, count, carrier, attachment, contact, boundary and representation layer. '
 'Use only within independently frozen requester meaning and the actual permitted dimensions/properties. Sibling cards and genre labels do not activate one another. '
 'Review all source conditions and complete effects; a role or alias is not an owner choice or adoption permission. '
 'Both endpoints and the complete selected connecting path must be visible together. partial_is_fail; UNOBSERVABLE_NOT_PASS. '
 'Research graphs and citations confer no native typed-fact qualification. A still image does not prove legal ownership, rank, historical authenticity, tax classification, '
 'consent, coercion, motive, identity, loyalty, sound, chronology, actual productivity, material chemistry or supernatural causation.')
records={};bindings={};mapping=[]
for card in data['cards']:
    card=copy.deepcopy(card);key=card['id']
    if key in reuse:
        mapping.append({'card_id':key,'candidate_id':reuse[key],'disposition':'reuse_existing_complete_relation','mutated':False,'native_approval':False});continue
    identity=cid(key);held=card['additional_source_plate_review_required']
    card.update(candidate_id=identity,runtime_registration='held_diagnostic' if held else 'registered_optional_visual_source',native_approval=False)
    if held:
        content={'definition':'Held for additional artifact/structure review: '+ ' / '.join(card['terms'])+'. '+card['confusion_boundary_ko'], 'research_semantics':card}
    else:
        content={'en':card['visible_en'],'ko':card['visible_ko'],
            'definition':'Optional bounded estate-management visual realization: '+card['visible_en'],
            'aliases':card['terms'],'application_contract':application,'research_semantics':card}
    dims=[] if held else effects[key]
    props=[{'dimension':'appearance','target':'main_subject','property':'wardrobe'}] if key in ['F01','F05'] else []
    records[identity]={'id':identity,'record_kind':'diagnostic' if held else 'visual_option','content':content,
        'conditions':{},'effects':{'dimensions':dims,'properties':props},
        'provenance':[{'source':'authored research docs/research-evidence/photo-prompt/estate-management-20261024/semantic-cards.json#'+key,
                       'sha256':corpus.digest(card)}]}
    mapping.append({'card_id':key,'candidate_id':identity,'disposition':'held_structure_review' if held else 'new_optional_visual_source','native_approval':False})
    if not held:
        for slot in card['proposed_slots']:
            identity_binding=bid(key+'/'+slot)
            bindings[identity_binding]={'id':identity_binding,'candidate_id':identity,'slot_id':slot,
                'role':'optional','semantic_role':catalog[slot]['semantic_role'],
                'conditions':{'subject_applicability':{}},'weight':2}
for card in data['context_diagnostics']:
    card=copy.deepcopy(card);identity=cid(card['id']);card.update(candidate_id=identity,runtime_registration='context_diagnostic')
    records[identity]={'id':identity,'record_kind':'diagnostic','content':{'definition':card['distinction_ko']+' '+card['not_proven_by_pixels']+' '+card['routing_ko'],'research_semantics':card},
        'conditions':{},'effects':{'dimensions':[],'properties':[]},'provenance':[{'source':'authored estate-management context '+card['id'],'sha256':corpus.digest(card)}]}
    mapping.append({'card_id':card['id'],'candidate_id':identity,'disposition':'context_diagnostic','native_approval':False})
asset=SKILL/'assets';module='photo_candidate_estate_management_20261024.json';binding_module='photo_candidate_estate_management_bindings_20261024.json'
assert not (asset/module).exists() and not (asset/binding_module).exists(),'Refuse overwrite; reconcile a prior attempt first'
write(asset/module,{'schema':'photo-candidate-module/v3','candidates':records})
write(asset/binding_module,{'schema':'photo-candidate-slot-bindings/v3','slot_bindings':bindings})
manifest=read(asset/'photo_candidate_corpus_manifest.json');prior=copy.deepcopy(manifest)
manifest['modules'] += [{'file':module,'kind':'candidates'},{'file':binding_module,'kind':'slot_bindings'}]
write(asset/'photo_candidate_corpus_manifest.json',manifest)
assert manifest['modules'][:-2]==prior['modules']
summary={'schema':'estate-management-integration/v1','semantic_cards':len(data['cards']),
    'context_diagnostics':len(data['context_diagnostics']),'new_positive_candidates':sum(c['record_kind']=='visual_option' for c in records.values()),
    'held_visual_diagnostics':sum(m['disposition']=='held_structure_review' for m in mapping),
    'context_records':len(data['context_diagnostics']),'reused_existing_candidates':len(reuse),'new_bindings':len(bindings),
    'full_native_source_qualification':False,'automatic_hard_activation':False,
    'operating_search_and_images':'PENDING','existing_source_mutations':0,
    'source_support':'Bounded authored optional visual realizations, not certified historical reconstructions. Held details remain nonpositive diagnostics.'}
registry={'schema':'photo-estate-management-semantics/v1',**data,'source_refs':sources['sources'],
    'keyword_routes':inventory['rows'],'card_candidate_map':mapping,'registration':summary}
write(asset/'photo_estate_management_semantics_20261024.json',registry)
write(OUT/'card-candidate-map.json',mapping);write(OUT/'new-native-records.json',records);write(OUT/'changed-native-records.json',{})
write(OUT/'new-bindings.json',bindings);write(OUT/'DATA-INTEGRATION.json',summary)
# Verify declared source shape and preserve the source-only distinction.
loaded=corpus.load(asset);assert set(records)<=set(loaded['candidates'])
assert all(loaded['candidates'][k]==v for k,v in records.items())
print(json.dumps(summary,ensure_ascii=False,indent=2))
