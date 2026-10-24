"""Add only reviewed research sources; retain every unrelated working record."""
from pathlib import Path
import copy, hashlib, json, uuid

O=Path(__file__).resolve().parent
R=O.parents[4]
P=R/'skills/photo-prompt-image-generator'
A=P/'assets'
Q=O.parent
read=lambda p:json.loads(p.read_bytes())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def h(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def cid(s):return 'cand_'+uuid.uuid5(uuid.NAMESPACE_URL,'image-prompt/marine-literature/20261024/'+s).hex

def main():
 cards={c['id']:c for c in read(Q/'semantic-cards.json')}
 drafts=read(Q/'candidate-drafts.json');routes=read(Q/'keyword-routes.json')
 catalog=read(A/'photo_candidate_slot_catalog.json')['slot_catalog']
 manifest_path=A/'photo_candidate_corpus_manifest.json';prior_bytes=manifest_path.read_bytes();manifest=json.loads(prior_bytes)
 records={};bindings={};card_map={};reused={};new_visual=[]
 named={'황근출','황룡','박철곤','무모칠','톤톤정','무톤듀오','견쌍섭','진떡팔','마철두','손수잘','손 으로하는수술은뭐든지잘해','1q2w3e4r!','쾌흥태','말딸필','해병문학','해갤문학'}
 contract=('One optional complete authored visual realization. Preserve every stated owner, part, support, directed endpoint, count, layer, local colour, medium and visible state in the complete English and Korean proposition. Apply only after explicit requester-compatible selection within the frozen meaning and all affected dimensions. A genre, character name or source citation does not impose this realization. Research graphs are review metadata, not native facts or permissions. Human figures in this authored realization are adults; adulthood is not sexual styling. Graphic alternatives require an explicitly selected illustrated/comic medium. A static shape, label or proxy does not establish identity, rank, consent, sexual orientation, intent, chemistry, chronology, sound or real events. Preserve sibling alternatives separately. Every selected required relation must be observable together; partial_is_fail; UNOBSERVABLE_NOT_PASS; BLOCKED_UNSCORED. This source has no native qualification.')
 for d in drafts:
  key=d['research_card_id'];c=cards[key];decision=d['adoption_recommendation']['decision']
  if decision=='reuse':
   refs=d['adoption_recommendation']['existing_ids'];assert len(refs)==1;card_map[key]=refs[0];reused[key]=refs[0];continue
  ident=cid(key);card_map[key]=ident
  aliases=list(dict.fromkeys([c['label']]+[s for s in c['seed_terms'] if s not in named]))
  raw={'id':ident,'record_kind':'visual_option','content':{
   'en':c['proposal_en'],'ko':c['proposal_ko'],'definition':c['proposal_en'],
   'aliases':aliases,'application_contract':contract,
   'research_semantics':{**copy.deepcopy(c),'candidate_id':ident,'integration_status':'optional_visual_source','runtime_registered':True,'native_approval':False,
    'source_support_scope':c['source_scope'],'adoption_note':d['adoption_recommendation']}},
   'conditions':{'for_any':['human']} if any('adult' in n['description'].lower() for n in c['owners']) else {},
   'effects':{'dimensions':sorted({dim for slot in c['planned_slots'] for dim in catalog[slot]['dimensions']}),'properties':[]},
   'provenance':[{'source':'authored research proposition docs/research-evidence/photo-prompt/marine-literature-20261024/semantic-cards.json#'+key,'sha256':h(c)}]}
  records[ident]=raw;new_visual.append(ident)
  for slot in c['planned_slots']:
   bid='bind_'+uuid.uuid5(uuid.NAMESPACE_URL,'image-prompt/marine-literature/'+key+'/'+slot).hex
   bindings[bid]={'id':bid,'candidate_id':ident,'slot_id':slot,'role':'optional','semantic_role':catalog[slot]['semantic_role'],
    'conditions':{'subject_applicability':copy.deepcopy(catalog[slot].get('applicability',{}))},'weight':1}
 diagnostic_ids=[]
 for k in routes:
  ident=cid('context-'+k['id']);diagnostic_ids.append(ident)
  records[ident]={'id':ident,'record_kind':'diagnostic','content':{
   'en':'Contextual research entry for '+k['term']+'. The Korean source definition is retained verbatim as diagnostic context, not a positive visual instruction.',
   'ko':k['original_definition'],'definition':k['original_definition'], 'aliases':[k['term']],
   'application_contract':'Context only. Preserve polysemy, version and claim limits. Do not infer a visual appearance, actual identity, consent, violence, sexual orientation, chemistry, sound or chronology from this label. Never use this diagnostic record as positive image material.',
   'research_semantics':{**copy.deepcopy(k),'integration_status':'context_diagnostic','runtime_registered':True,'native_approval':False}},
   'conditions':{},'effects':{'dimensions':[],'properties':[]},
   'provenance':[{'source':'research seed docs/research-evidence/photo-prompt/marine-literature-20261024/keyword-routes.json#'+k['id'],'sha256':h(k)}]}
 filename='photo_candidate_marine_literature_20261024.json';bfile='photo_candidate_marine_literature_bindings_20261024.json'
 assert not (A/filename).exists() and not (A/bfile).exists(),'avoid overwriting an earlier publication'
 old={}
 for m in manifest['modules']:
  path=A/m['file'];old[m['file']]=hashlib.sha256(path.read_bytes()).hexdigest()
  data=read(path)
  assert not (set(data.get('candidates',{}))&set(records))
 write(O/'protected-source-baseline.json',old)
 write(O/'release-new-native-records.json',records);write(O/'changed-native-records.json',{})
 write(O/'release-bindings.json',{'schema':'photo-candidate-slot-bindings/v3','slot_bindings':bindings})
 write(A/filename,{'schema':'photo-candidate-module/v3','candidates':records});write(A/bfile,{'schema':'photo-candidate-slot-bindings/v3','slot_bindings':bindings})
 assert manifest_path.read_bytes()==prior_bytes,'concurrent source manifest change; rebaseline before append'
 manifest['modules'] += [{'file':filename,'kind':'candidates'},{'file':bfile,'kind':'slot_bindings'}];write(manifest_path,manifest)
 semantic={'schema':'photo-marine-literature-semantics/v1','research_scope':'versioned fiction, real borrowing, observable proposals and diagnostic context remain separate','cards':list(cards.values()),'keyword_routes':routes,'card_candidate_map':card_map,'sources':read(Q/'sources.json'),'qualification':'source registered; no native pixel approval'}
 write(A/'photo_marine_literature_semantics_20261024.json',semantic)
 after={name:hashlib.sha256((A/name).read_bytes()).hexdigest() for name in old}
 assert old==after,'existing source drift; preserve and rebaseline'
 result={'status':'source_registered','new_visual_candidates':len(new_visual),'new_diagnostic_records':len(diagnostic_ids),'new_bindings':len(bindings),'semantic_cards':len(cards),'preserved_seed_rows':len(routes),'reused_existing_ids':reused,'card_candidate_map':card_map,'new_visual_ids':new_visual,'diagnostic_ids':diagnostic_ids,'existing_module_hashes_preserved':True,'native_approval':False}
 write(O/'source-registration.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ['card_candidate_map','new_visual_ids','diagnostic_ids']},ensure_ascii=False))

if __name__=='__main__':main()
