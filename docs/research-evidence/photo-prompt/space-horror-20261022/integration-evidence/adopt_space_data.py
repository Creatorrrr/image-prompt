"""Register whole optional space-horror sources, preserving every old record."""
import copy,hashlib,json,sys,uuid
from pathlib import Path
ROOT=Path('/Users/chasoik/Projects/image-prompt');S=ROOT/'skills/photo-prompt-image-generator';A=S/'assets';Q=Path(__file__).resolve().parents[1];O=Path(__file__).resolve().parent
sys.path.insert(0,str(S/'scripts'))
import photo_candidate_corpus as corpus
from photo_runtime_sources import source_update
from photo_installed_h_f2 import default_store,release
def read(p):return json.loads(p.read_bytes())
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def fsha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
# Whole-source footprint reviewed from the bilingual scene, not slot aliases.
FOOTPRINTS='''V01:subject count appearance pose setting composition relationship
V02:subject appearance pose action setting composition relationship body_geometry text
V03:setting material body_geometry composition relationship
V04:setting material body_geometry composition relationship
V05:setting material body_geometry composition relationship
V06:subject appearance pose action setting lighting composition relationship
V07:setting material body_geometry composition relationship
V08:setting material body_geometry composition relationship lighting
V09:subject count appearance pose setting composition relationship
V10:setting material body_geometry composition relationship
V11:subject appearance pose action setting composition relationship
V12:subject pose setting composition relationship text
V13:setting lighting composition relationship text
V15:subject count appearance body_geometry pose setting composition relationship
V17:material appearance body_geometry composition relationship
V18:setting material body_geometry composition relationship lighting
V19:setting material body_geometry composition relationship
V20:subject pose setting composition relationship
V21:subject appearance count pose setting composition relationship
V22:setting material composition relationship appearance text
V23:setting material composition relationship
V24:setting material body_geometry composition relationship
V25:setting material body_geometry composition relationship
V26:subject setting count body_geometry composition relationship
V27:setting material body_geometry composition relationship text
V28:setting material body_geometry composition relationship
V29:subject pose setting composition relationship text
V30:subject count species body_geometry appearance composition relationship
V32:subject count species body_geometry appearance composition relationship action
V33:subject count species body_geometry material composition relationship
V34:setting species material body_geometry composition relationship
V35:setting material body_geometry composition relationship action
V36:setting material body_geometry composition relationship
V37:subject appearance body_geometry action pose setting composition relationship
V38:subject count body_geometry appearance composition relationship
V39:subject body_geometry material appearance composition relationship
V40:subject pose body_geometry setting composition relationship action
V42:subject species body_geometry material setting composition relationship
V43:subject species body_geometry count action pose composition relationship
V46:subject species body_geometry setting composition relationship action
V48:subject species body_geometry appearance material composition relationship
V49:subject age count body_geometry pose action setting composition relationship
V50:subject count appearance pose setting composition relationship
V51:subject age appearance body_geometry pose setting composition relationship
V52:setting material body_geometry composition relationship text
V53:subject count pose action body_geometry setting composition relationship text
V54:subject pose action setting composition relationship text
V58:setting body_geometry composition relationship
V59:subject count body_geometry material pose action setting composition relationship
V60:subject count pose action body_geometry setting composition relationship
V62:setting material body_geometry appearance composition relationship
V63:subject pose action body_geometry setting composition relationship
V64:subject count pose setting lighting composition relationship'''
EFFECTS={k:v.split() for k,v in (line.split(':') for line in FOOTPRINTS.splitlines())}
REUSE={'V14':'cand_7b74028598cd503abdcd5256886084e5','V16':'cand_49652d62206e522fb28ad2b5d4c2bc43','V31':'cand_4c2a218da12358c2ab9e8ae53951adc4','V44':'cand_ee6b62e77e9357b69cd2ae19b63a3677','V55':'cand_d1d1920147855b41a40559368ae95ea0'}
DEFER={'V41','V45','V47','V56','V57','V61'}
APP='One complete optional authored visual realization. Preserve the whole English and Korean proposition, every stated owner, count, part, layer, material, displayed field, state and directed relationship together. Use only where compatible with the independently frozen requester meaning and all affected dimensions and properties; do not invent an owner, erase a source condition or reverse an endpoint to force a fit. Titles and narrative clues do not prove diagnosis, cause, consciousness, consent, kinship, personal identity, history, time, physical measurement or a work-specific canonical design. A displayed value is a depicted claim, not its truth. Every distinguishing endpoint must be observable together; partial or hidden required evidence cannot pass. Sources and research graphs are review metadata and grant no native facts, roles, guards, effect permissions or source qualification.'
def main():
 original=corpus.load(A);cfg=read(S/'retrieval-runtime.json');native,hm,nm=release(default_store(),cfg['generation_id'])
 before=dict(config=cfg,store=str(default_store()),native=str(native),corpus_sha256=corpus.digest(original),candidate_count=len(original['candidates']),binding_count=len(original['slot_bindings']),manifest_sha256=fsha(A/corpus.MANIFEST_NAME),module_sha256={m['file']:fsha(A/m['file']) for m in read(A/corpus.MANIFEST_NAME)['modules']},research_sha256={p.name:fsha(p) for p in Q.iterdir() if p.is_file()},code_sha256=nm['source']['code'])
 write(O/'before.json',before)
 cards=read(Q/'semantic-cards.json')['cards'];contexts=read(Q/'context-records.json')['records'];routes=read(Q/'keyword-routes.json')['routes'];sources={s['source_id']:s for s in read(Q/'sources.json')['sources']}
 assert set(EFFECTS)|set(REUSE)|DEFER=={c['card_id'] for c in cards}
 assert not(set(EFFECTS)&set(REUSE) or set(EFFECTS)&DEFER or set(REUSE)&DEFER)
 assert all(cid in original['candidates'] for cid in REUSE.values())
 records={};bindings={};registry=[];decisions=[];lookup={}
 for card in cards:
  key=card['card_id'];positive=key in EFFECTS
  cid=REUSE.get(key,'cand_'+uuid.uuid5(uuid.NAMESPACE_URL,'image-prompt/space-horror/20261022/'+key).hex);lookup[key]=cid
  meta={**copy.deepcopy(card),'schema':'photo-space-horror-visual-semantics/v1','candidate_id':cid,'registration_status':'existing_source_reference' if key in REUSE else 'authored_optional_source' if positive else 'deferred_context_diagnostic','source_details':[sources[s] for s in card['source_ids']],'native_qualification':'not_qualified','graph_scope':'Advisory authored research graph, not typed native facts or permission. Existing-source reuse preserves the actual old proposition, not an assertion that every illustrative staging detail is source-equivalent.'}
  registry.append(meta)
  if key in REUSE:
   decisions.append(dict(card_id=key,candidate_id=cid,decision='reuse_existing_without_mutation',existing_source_sha256=corpus.digest(original['candidates'][cid]),research_staging_not_promoted_to_existing_source_fact=True,native_approval=False));continue
  assert cid not in original['candidates']
  en=card['proposal_en'] if positive else f"Context-only research for {card['title']}. "+card['claim_limit']
  ko=card['proposal_ko'] if positive else card['title']+'。'+card['claim_limit']
  records[cid]={'id':cid,'record_kind':'visual_option' if positive else 'diagnostic','content':{'en':en,'ko':ko,'definition':('Complete optional authored visual realization: '+en) if positive else 'Deferred/context diagnostic excluded from positive material retrieval.','aliases':[card['title']],'application_contract':APP if positive else 'Context only. Preserve the distinction, missing evidence and deferred review. Do not prescribe a still-image shape or infer a diagnosis, cause, consciousness, coercion, kinship or physical proof.','research_semantics':meta},'conditions':{},'effects':{'dimensions':sorted(set(EFFECTS[key])) if positive else [],'properties':[]},'provenance':[{'source':sources[s]['url'],'sha256':fsha(Q/'semantic-cards.json')} for s in card['source_ids']]}
  for slot in card['proposed_slots'] if positive else []:
   assert slot in original['slot_catalog'];bid='bind_'+uuid.uuid5(uuid.NAMESPACE_URL,cid+'/'+slot).hex
   bindings[bid]={'id':bid,'candidate_id':cid,'slot_id':slot,'role':'optional','semantic_role':original['slot_catalog'][slot]['semantic_role'],'conditions':{'subject_applicability':{}},'weight':2}
  decisions.append(dict(card_id=key,candidate_id=cid,decision='new_complete_optional_variant' if positive else 'context_defer',novelty_scope='Reviewed relation-specific optional proposition; exhaustive semantic novelty is not claimed. All old records/guards/effects remain intact.',native_approval=False))
 for ctx in contexts:
  key=ctx['context_id'];cid='cand_'+uuid.uuid5(uuid.NAMESPACE_URL,'image-prompt/space-horror/20261022/context/'+key).hex;lookup[key]=cid;assert cid not in original['candidates']
  records[cid]={'id':cid,'record_kind':'diagnostic','content':{'en':ctx['distinction']+' '+ctx['not_established'],'ko':ctx['distinction']+' '+ctx['not_established'],'definition':'Context-only distinction excluded from positive material retrieval.','aliases':[key+' space-horror semantic distinction'],'application_contract':'Keep this as contextual interpretation and proof limits. No fixed image recipe, automatic hard profile or native permission.','research_semantics':copy.deepcopy(ctx)},'conditions':{},'effects':{'dimensions':[],'properties':[]},'provenance':[{'source':sources[s]['url'],'sha256':fsha(Q/'context-records.json')} for s in ctx['source_ids']]}
 proposed=copy.deepcopy(original);proposed['candidates'].update(records);proposed['slot_bindings'].update(bindings);corpus.validate(proposed)
 cm='photo_candidate_space_horror_20261022.json';bm='photo_candidate_space_horror_bindings_20261022.json'
 with source_update(S):
  assert corpus.digest(corpus.load(A))==corpus.digest(original),'Concurrent source drift; rebase rather than overwrite'
  manifest=read(A/corpus.MANIFEST_NAME);assert not any(m['file'] in [cm,bm] for m in manifest['modules'])
  write(A/cm,{'schema':corpus.MODULE_SCHEMAS['candidates'],'candidates':records});write(A/bm,{'schema':corpus.MODULE_SCHEMAS['slot_bindings'],'slot_bindings':bindings})
  manifest['modules'] += [{'file':cm,'kind':'candidates'},{'file':bm,'kind':'slot_bindings'}];write(A/corpus.MANIFEST_NAME,manifest)
  actual=corpus.load(A);assert actual==proposed
 assert all(actual['candidates'][cid]==r for cid,r in original['candidates'].items())
 assert all(actual['slot_bindings'][bid]==r for bid,r in original['slot_bindings'].items())
 assert all(actual[k]==original[k] for k in ['slot_catalog','policies'])
 result={'schema':'photo-space-horror-semantic-registry/v1','cards':registry,'contexts':contexts,'keyword_routes':[{**r,'candidate_ids':list(dict.fromkeys([lookup[k] for k in r['visual_card_ids']+r['context_ids']]))} for r in routes],'decisions':decisions,'counts':{'visual_cards':len(cards),'reused_visual_sources':len(REUSE),'new_visual_options':len(EFFECTS),'deferred_card_diagnostics':len(DEFER),'context_diagnostics':len(contexts),'new_bindings':len(bindings),'keyword_routes':len(routes)},'native_approval':False,'source_provenance':'Research specification hashes, not remote page hashes.'}
 write(A/'photo_space_horror_semantics_20261022.json',result);write(O/'data-integration.json',result);write(O/'new-native-records.json',records);write(O/'changed-native-records.json',{})
 write(O/'source-preservation.json',{'status':'pass','old_candidates_preserved':len(original['candidates']),'old_bindings_preserved':len(original['slot_bindings']),'catalog_policies_preserved':True,'old_module_bytes_preserved':all(fsha(A/f)==h for f,h in before['module_sha256'].items()),'total_candidates':len(actual['candidates']),'total_bindings':len(actual['slot_bindings']),**result['counts']})
 print(json.dumps(read(O/'source-preservation.json')),flush=True)
if __name__=='__main__':main()
