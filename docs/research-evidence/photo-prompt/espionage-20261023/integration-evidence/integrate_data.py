"""Add scoped espionage sources; retain all existing candidate/guard/binding bytes."""
from pathlib import Path
import collections,copy,hashlib,json,sys,uuid
O=Path(__file__).resolve().parent;R=O.parents[4];S=R/'skills/photo-prompt-image-generator';A=S/'assets';D=O.parent
sys.path.insert(0,str(S/'scripts'))
import photo_candidate_corpus as corpus
read=lambda p:json.loads(p.read_bytes())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
NS=uuid.UUID('b7b02533-6ca8-4d31-b760-f6ae713a25d1')
identity=lambda prefix,label:prefix+uuid.uuid5(NS,label).hex
REUSE={
 'contrapposto':'cand_aa7fc3f7d8ba5421b8d6d8c2afa555bf',
 'crossed_legs':'cand_3693210e9260577fbbcb4db996c45fb9',
 'sideways_glance':'cand_e0d66073bd5757ca9ae29a52cc968e01',
 'notch_lapel':'cand_e0dfcd15b3375892832151b446f1697a',
 'shawl_lapel':'cand_a7a18bd8ad7d53098f1f6e9ed3b57357',
 'three_piece':'cand_1fc72ba8284752e884cf98fa235e987f',
 'pea_coat':'cand_4cfbf7ad25eb586b8f4edbaf25cdf4bf',
 'turtleneck':'cand_3a202991b988538c9a793ece81b39cff',
 'slip_dress':'cand_cf7f5285ee6c50e08136065ee5932646',
 'stocking_support':'cand_ae856dfccef0599eb2db1c6ba565e112',
 'stocking_seam':'cand_847e459987e2500db055c7e89f0272b6',
 'oxford_closure':'cand_f28e4d788db05481bc288ef64f7c29fd',
 'derby_closure':'cand_edec7fe6c6cc5813b2c5074cf449948f',
 'crossbody_bag':'cand_9fc391214cb65f14bfa7629f6f5b502e',
 'glossy_folds':'cand_074c1f23cee455caa3a3284d604c74b7',
 'pinstripe':'cand_c58dc03d876c54d9958c4d38223639d8',
 'blunt_bob':'cand_0bfd7af9c2a4570ba9eb53343831e91d',
}
CONTRACT=('One optional complete authored visual realization. Retain every named actor, object, representation boundary, garment layer, physical support and directed endpoint in the selected English and Korean source. '
 'Apply only within independently frozen requester meaning and all affected dimensions and properties. Do not combine sibling alternatives automatically. '
 'Research cards, graphs, citations and role tags are review metadata and grant no native facts, owner permissions, source qualification or hard activation. '
 'A visible object, pose or surface does not establish identity, allegiance, consent, coercion, cause, chronology, sound, authenticity, chemistry or operational performance. '
 'All consequential contacts and boundaries must be readable together; partial_is_fail; UNOBSERVABLE_NOT_PASS.')
ACTOR_SLUGS=set('direct_handoff suspended_handoff drop_placement pocket_litter analysis_comparison briefing_table threshold_departure cash_envelope kompromat_display earpiece_contact receiver_pose button_lens watch_camera reel_console camera_target window_observer mirror_attention tail_spacing'.split())
def main():
 if (O/'data-integration.json').exists():raise SystemExit('Already integrated; preserve original evidence')
 before=corpus.load(A)
 protected={p.name:sha(p) for p in A.glob('*.json')}
 cards=read(D/'semantic-cards.json');contexts=read(D/'context-distinctions.json');routes=read(D/'keyword-routes.json');sources=read(D/'sources.json')
 fresh={};bindings={};decisions=[];snapshots={}
 for card in cards:
  slug=card['slug'];held=card['source_specific_review'].startswith('HOLD')
  if slug in REUSE:
   cid=REUSE[slug];existing=copy.deepcopy(before['candidates'][cid])
   snapshots[cid]={'record':existing,'bindings':{k:v for k,v in before['slot_bindings'].items() if v['candidate_id']==cid},'record_sha256':corpus.digest(existing)}
   decisions.append({'card_id':card['id'],'slug':slug,'candidate_id':cid,'decision':'reuse','coverage':'one compatible complete existing alternative; preserve its full literal, constraints and effects, not a claim of exhaustive term equivalence','original_unchanged':True})
   continue
  cid=identity('cand_','espionage:'+slug)
  meta={**copy.deepcopy(card),'candidate_id':cid,'integration_status':'held_diagnostic' if held else 'optional_visual_source'}
  if held:
   content={'definition':'Held diagnostic, excluded from positive visual retrieval: '+card['name_ko']+'. '+card['claim_limit'],'research_semantics':meta};effects={'dimensions':[],'properties':[]};conditions={}
  else:
   content={'en':card['visible_en'],'ko':card['visible_ko'],'definition':card['visible_en'],'aliases':[card['name_ko']],'application_contract':CONTRACT,'research_semantics':meta}
   dims=set(d for role in card['proposed_roles'] for d in before['slot_catalog'][role]['dimensions'])
   effects={'dimensions':sorted(dims),'properties':[]}
   human=card['domain'] in ('body_gaze_and_hands','two_person_blocking') or slug in ACTOR_SLUGS or any(x.startswith('A.') for x in card['owners_and_parts'])
   conditions={'for_any':['human']} if human else {}
  fresh[cid]={'id':cid,'record_kind':'diagnostic' if held else 'visual_option','content':content,'conditions':conditions,'effects':effects,'provenance':[{'source':'authored research proposition docs/research-evidence/photo-prompt/espionage-20261023/semantic-cards.json#'+card['id'],'sha256':sha(D/'semantic-cards.json')}]}
  decisions.append({'card_id':card['id'],'slug':slug,'candidate_id':cid,'decision':'defer' if held else 'new','positive':not held,'reason':'specimen/detail equivalence held' if held else 'complete additional owner/endpoint or scene realization; nearby sources have different whole effects or contexts','native_approval':False})
  if not held:
   for role in card['proposed_roles']:
    bid=identity('bind_',cid+':'+role)
    bindings[bid]={'id':bid,'candidate_id':cid,'slot_id':role,'role':'optional','semantic_role':before['slot_catalog'][role]['semantic_role'],'conditions':{'subject_applicability':{}},'weight':1}
 for ctx in contexts:
  cid=identity('cand_','espionage-context:'+ctx['id'])
  fresh[cid]={'id':cid,'record_kind':'diagnostic','content':{'definition':'Context-only diagnostic, excluded from positive visual retrieval: '+ctx['term_ko']+' / '+ctx['term_en']+'. '+ctx['claim_limit'],'research_semantics':copy.deepcopy(ctx)},'conditions':{},'effects':{'dimensions':[],'properties':[]},'provenance':[{'source':'research context docs/research-evidence/photo-prompt/espionage-20261023/context-distinctions.json#'+ctx['id'],'sha256':sha(D/'context-distinctions.json')}]}
 assert set(fresh).isdisjoint(before['candidates'])
 exact={(v.get('content',{}).get('en'),v.get('content',{}).get('ko')) for v in before['candidates'].values() if v['record_kind']!='diagnostic'}
 assert all((v['content']['en'],v['content']['ko']) not in exact for v in fresh.values() if v['record_kind']=='visual_option')
 cm='photo_candidate_espionage_20261023.json';bm='photo_candidate_espionage_bindings_20261023.json';sm='photo_espionage_semantics_20261023.json'
 for name in (cm,bm,sm):assert not (A/name).exists()
 write(A/cm,{'schema':corpus.MODULE_SCHEMAS['candidates'],'candidates':fresh})
 write(A/bm,{'schema':corpus.MODULE_SCHEMAS['slot_bindings'],'slot_bindings':bindings})
 write(A/sm,{'schema':'photo-espionage-research-semantics/v1','cards':cards,'keyword_routes':routes,'context_distinctions':contexts,'sources':sources,'adoption_decisions':decisions,'status':'registered source metadata; not native qualification or pixel proof'})
 manifest=read(A/corpus.MANIFEST_NAME)
 for file,kind in ((cm,'candidates'),(bm,'slot_bindings')):manifest['modules'].append({'file':file,'kind':kind})
 write(A/corpus.MANIFEST_NAME,manifest)
 after=corpus.load(A)
 assert all(after['candidates'][k]==v for k,v in before['candidates'].items())
 assert all(after['slot_bindings'][k]==v for k,v in before['slot_bindings'].items())
 assert after['slot_catalog']==before['slot_catalog'] and after['policies']==before['policies']
 assert all(sha(A/name)==h for name,h in protected.items() if name!=corpus.MANIFEST_NAME)
 write(O/'new-native-records.json',fresh);write(O/'changed-native-records.json',{})
 write(O/'reuse-source-snapshots.json',snapshots)
 write(O/'data-integration.json',{'adoptions':decisions,'new_visual':sum(x['record_kind']=='visual_option' for x in fresh.values()),'new_diagnostics':sum(x['record_kind']=='diagnostic' for x in fresh.values()),'new_bindings':len(bindings),'reuse':len(REUSE),'before_candidates':len(before['candidates']),'after_candidates':len(after['candidates']),'before_bindings':len(before['slot_bindings']),'after_bindings':len(after['slot_bindings']),'existing_records_bindings_catalog_policies_preserved':True,'existing_asset_sha256_preserved_except_appended_manifest':True,'source_files':[cm,bm,sm],'old_alias_or_performance_wording_modified':False,'native_approval':False})
 print(json.dumps({k:v for k,v in read(O/'data-integration.json').items() if k!='adoptions'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
