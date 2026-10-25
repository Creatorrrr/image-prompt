"""Install reviewed investigative-fiction source data; preserve unrelated work."""
from pathlib import Path
import collections,copy,gc,hashlib,json,os,sys,uuid
gc.disable()
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];S=ROOT/'skills/photo-prompt-image-generator';A=S/'assets';O=HERE/'integration-evidence'
sys.path.insert(0,str(S/'scripts'))
import photo_candidate_corpus as corpus
from photo_runtime_sources import source_update
NS=uuid.UUID('4bf3912a-2544-4d4e-99d8-33b5c23589d4')
def read(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def write(p,x):
 p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_suffix(p.suffix+'.investigation.tmp');tmp.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');os.replace(tmp,p)
def ident(prefix,key):return prefix+uuid.uuid5(NS,'investigative-fiction-20261025:'+key).hex
REUSE={'W01':'cand_5ccf05cc8bd152caaf61d576b37698b8','N01':'cand_33a5a891d9a15891993a3a0c962a5519','V05':'cand_4ff5a93163635a4e976d045fead48f93'}
CONTRACT=('One complete optional authored investigative-fiction-compatible visual realization, not a genre definition, legal status, scientific result or operational instruction. Preserve every English and Korean clause, actual owner, participant count, hand/wrist continuity, tool and target, contact and gap, support, garment layer, document/screen boundary, short fictional label and explicit model/diagram mode. Review all actual effects against independently frozen requester meaning, actual owners and whole-dimension/property locks. A topic, reference portrait, role tag, research graph or source URL supplies no identity, age, owner, prerequisite, permission or native qualification. Do not replace a trace with its marker, actual anatomy with cloth or a model, a screen figure with a real participant, current documentation with a completed sequence, or a realistic board with autonomous magic. Every adopted distinguishing endpoint must read together at useful scale; partial_is_fail; UNOBSERVABLE_NOT_PASS. External appearance alone does not establish identity, credentials, legal power, guilt, truthfulness, consent, coercion, sexual interest, mental state, blood chemistry, DNA source or transfer, cause/manner/time of death, injury mechanism, sterility, protection, recording success, byte integrity, authenticity, historical sequence or supernatural cause. A report, map or display depicts a claim within its carrier. Geometry is an authored option; sources support only their individually listed bounded claims. Material discovery is separate from native approval, actual use and saved-image evidence.')
EFFECTS={
 'A01':'subject count pose setting relationship composition','A02':'appearance setting relationship','A03':'appearance setting relationship text','A04':'appearance setting relationship text','A05':'appearance count setting relationship text','A06':'pose action appearance relationship setting body_geometry','A07':'subject count pose action appearance relationship setting','A08':'appearance material relationship setting','A09':'subject count pose action appearance relationship setting text','A10':'subject count pose action appearance relationship setting',
 'F01':'material appearance setting relationship','F02':'appearance setting relationship format composition','F03':'material appearance count setting relationship','F04':'lighting appearance setting','F05':'subject pose action appearance relationship setting lighting','F06':'appearance count setting relationship text format','F07':'appearance count setting relationship text','F08':'subject pose action appearance relationship setting text format','F09':'appearance count setting relationship','F10':'subject count pose action appearance setting relationship format',
 'D01':'appearance count setting relationship text','D02':'appearance count setting relationship text format','D03':'subject pose action appearance setting relationship text format','D04':'appearance count setting relationship format','D05':'appearance count setting relationship format','D06':'appearance count setting relationship text format','D07':'appearance count setting relationship text format','D08':'appearance setting relationship',
 'I01':'subject count pose action setting relationship','I02':'subject count pose action appearance setting relationship','I03':'subject count pose appearance setting relationship','I04':'appearance count setting relationship','I05':'subject count pose appearance setting relationship lighting composition','I06':'subject count pose action appearance setting relationship','I07':'subject count pose appearance setting relationship composition','I08':'subject count pose action appearance setting relationship',
 'N02':'subject count pose appearance setting relationship composition','N03':'subject pose action appearance setting relationship text','N04':'appearance count setting relationship','N05':'appearance count setting relationship','N06':'subject count pose action appearance setting relationship',
 'W02':'appearance material relationship','W05':'appearance','W06':'appearance relationship','W07':'appearance body_geometry','W08':'appearance relationship','W09':'appearance count relationship','W10':'appearance relationship','W11':'appearance body_geometry relationship color','W12':'appearance relationship material','W13':'appearance relationship','W14':'subject age appearance body_geometry relationship','W15':'subject age appearance body_geometry relationship',
 'V01':'appearance color relationship body_geometry','V02':'appearance relationship body_geometry','V04':'appearance count setting relationship','V07':'subject pose setting relationship','V08':'appearance material setting relationship','V09':'subject count pose appearance setting relationship composition','V10':'appearance setting relationship',
 'L01':'subject lighting relationship setting','L02':'subject count pose appearance setting relationship composition','L03':'appearance setting relationship lighting material','L04':'appearance setting relationship format camera','L05':'subject pose action appearance relationship setting lighting','L06':'subject pose appearance setting relationship composition',
}
def main():
 O.mkdir(exist_ok=True)
 if (O/'data-integration.json').exists():raise SystemExit('Already integrated; preserve evidence.')
 before=corpus.load(A);manifest=read(A/corpus.MANIFEST_NAME)
 protected={str(p.relative_to(ROOT)):sha(p) for p in [S/'SKILL.md',S/'retrieval-runtime.json',*A.glob('*.json')]}
 write(O/'source-before.json',{'protected':protected,'manifest':manifest,'candidates':{cid:digest(r) for cid,r in before['candidates'].items()},'bindings':{bid:digest(r) for bid,r in before['slot_bindings'].items()},'catalog_sha256':digest(before['slot_catalog']),'policies_sha256':digest(before['policies'])})
 config=read(S/'retrieval-runtime.json');store=Path.home()/'.cache/image-prompt/photo-shared-runtime/h-f2-installed';native=store/'generations'/config['native_generation_id']
 write(O/'release-base.json',{'config':config,'store':str(store),'native':str(native),'skill_sha256':sha(S/'SKILL.md'),'scope':'selected sealed code/data plus reviewed investigative delta; unrelated working changes excluded'})
 research=read(HERE/'semantic-cards.json');records={};bindings={};mapping={};decisions=[];registered=[]
 for card in research['visual_cards']:
  key=card['id'];held=card['mode'] in ['defer_visual','diagram_only'];cid=REUSE.get(key) or ident('cand_',key);mapping[key]=cid
  meta=copy.deepcopy(card);meta.update(candidate_id=cid,runtime_registration='REGISTERED_SOURCE_NOT_NATIVE_QUALIFIED',native_approval=False,automatic_hard_activation=False)
  if key in REUSE:
   old=before['candidates'][cid]
   meta.update(registration='reuse_adjacent_complete_existing_source',registered_source_en=old['content']['en'],registered_source_ko=old['content']['ko'],scope_difference={'W01':'Existing complete trench topology reused; original long-hem detail is not additionally guaranteed.','N01':'Existing bolt-to-receiver source reused; all-entry impossibility remains unproved.','V05':'Existing seated-adult cuffs source reused; standing variant is not covered.'}[key])
   decisions.append({'card_id':key,'cid':cid,'decision':meta['registration'],'scope_difference':meta['scope_difference']});registered.append(meta);continue
  if held:
   rec={'id':cid,'record_kind':'diagnostic','content':{'definition':'Held research alternative, excluded from positive retrieval. '+card['label_ko']+'. '+card['claim_limit'],'research_semantics':meta},'conditions':{},'effects':{'dimensions':[],'properties':[]},'provenance':[{'source':'investigative-fiction-20261025 held '+key,'sha256':sha(HERE/'semantic-cards.json')}]};meta['registration']='held_diagnostic'
  else:
   assert key in EFFECTS,key
   meta['registration']='complete_optional_authored_visual'
   rec={'id':cid,'record_kind':'visual_option','content':{'en':card['positive_en'],'ko':card['positive_ko'],'definition':card['positive_en'],'aliases':[card['label_ko']],'application_contract':CONTRACT,'research_semantics':meta},'conditions':{'requires_adult_context':True} if 'adult' in card['positive_en'].lower() else {},'effects':{'dimensions':EFFECTS[key].split(),'properties':[]},'provenance':[{'source':'authored research docs/research-evidence/photo-prompt/investigative-fiction-20261025/semantic-cards.json#'+key,'sha256':sha(HERE/'semantic-cards.json')}]}
   for slot in card['suggested_slots']:
    spec=before['slot_catalog'][slot];bid=ident('bind_',cid+':'+slot)
    bindings[bid]={'id':bid,'candidate_id':cid,'slot_id':slot,'role':'optional','semantic_role':spec['semantic_role'],'conditions':{'subject_applicability':{}},'weight':1}
  records[cid]=rec;registered.append(meta);decisions.append({'card_id':key,'cid':cid,'decision':meta['registration']})
 for row in research['context_cards']:
  key=row['id'];cid=ident('cand_',key);mapping[key]=cid
  records[cid]={'id':cid,'record_kind':'diagnostic','content':{'definition':'Context distinction excluded from positive visual retrieval: '+row['label_ko']+'. '+row['meaning_boundary']+' '+row['integration_action'],'research_semantics':{**copy.deepcopy(row),'candidate_id':cid,'runtime_registration':'diagnostic_context_only','native_approval':False}},'conditions':{},'effects':{'dimensions':[],'properties':[]},'provenance':[{'source':'investigative-fiction-20261025 context '+key,'sha256':sha(HERE/'context-cards.tsv')}]}
 changed={};prior={}
 translations={
 'cand_0537b275d1ae521882cf15be7252c546':'증거 번호 표지 소품',
 'cand_f33ca96f48b15c13af416859d150bbbf':'증거 번호 표지를 살피는',
 'cand_2b800be525185932840b422eb39a7318':'증거 번호 표지가 있는 법과학 근접 구도',
 'cand_1eb3b0a78fe45e6fa7caefdc756de87e':'증거를 살피는 현장감식요원',
 'cand_48c178c2f95e517a9d48c01f263e72d7':'법과학 실험실의 증거 검사 탁자',
 }
 for cid,ko in translations.items():
  prior[cid]=copy.deepcopy(before['candidates'][cid]);r=copy.deepcopy(prior[cid]);r['content']['ko']=ko
  if cid=='cand_48c178c2f95e517a9d48c01f263e72d7':r['content']['phrase_en']='at a forensic laboratory evidence table';r['content']['phrase_ko']='법과학 실험실의 증거 검사 탁자에서'
  changed[cid]=r
  assert all(r[k]==prior[cid][k] for k in ['conditions','effects','provenance'])
 cm='photo_candidate_investigative_fiction_20261025.json';bm='photo_candidate_investigative_fiction_bindings_20261025.json';sm='photo_investigative_fiction_semantics_20261025.json'
 for name in [cm,bm,sm]:assert not (A/name).exists()
 registry={'schema':'photo-investigative-fiction-visual-semantics/v1','visual_cards':registered,'context_cards':research['context_cards'],'keyword_routes':[{**copy.deepcopy(r),'component_candidate_ids':[mapping[x] for x in r['optional_or_adjacent_visual_cards']],'context_candidate_ids':[mapping[x] for x in r['context_cards']],'automatic_hard_activation':False} for r in read(HERE/'keyword-routes.json')],'sources':read(HERE/'sources.json'),'native_approval':False,'automatic_hard_activation':False,'research_sha256':sha(HERE/'semantic-cards.json')}
 assert set(records).isdisjoint(before['candidates']) and set(bindings).isdisjoint(before['slot_bindings'])
 with source_update(S):
  assert sha(A/corpus.MANIFEST_NAME)==protected[str((A/corpus.MANIFEST_NAME).relative_to(ROOT))]
  write(A/cm,{'schema':corpus.MODULE_SCHEMAS['candidates'],'candidates':records});write(A/bm,{'schema':corpus.MODULE_SCHEMAS['slot_bindings'],'slot_bindings':bindings});write(A/sm,registry)
  for mod in manifest['modules']:
   if mod['kind']!='candidates':continue
   path=A/mod['file'];body=read(path);owned=set(body['candidates'])&changed.keys()
   if owned:
    assert sha(path)==protected[str(path.relative_to(ROOT))]
    for cid in owned:body['candidates'][cid]=changed[cid]
    write(path,body)
  manifest['modules'] += [{'file':cm,'kind':'candidates'},{'file':bm,'kind':'slot_bindings'}];write(A/corpus.MANIFEST_NAME,manifest)
 after=corpus.load(A)
 assert all(after['candidates'][cid]==r for cid,r in before['candidates'].items() if cid not in changed)
 assert all(after['slot_bindings'][bid]==r for bid,r in before['slot_bindings'].items())
 assert all(after[k]==before[k] for k in ['slot_catalog','policies'])
 for name,data in [('card-candidate-map.json',mapping),('new-native-records.json',records),('changed-native-records.json',changed),('changed-native-prior.json',prior),('adoption-decisions.json',decisions)]:write(O/name,data)
 report={'status':'authored_source_integrated','positive_new':sum(r['record_kind']=='visual_option' for r in records.values()),'context_and_held_new':sum(r['record_kind']=='diagnostic' for r in records.values()),'reused_adjacent_complete_sources':len(REUSE),'narrow_translation_updates':len(changed),'new_optional_bindings':len(bindings),'before_CIDs':len(before['candidates']),'after_CIDs':len(after['candidates']),'unrelated_CIDs_preserved':len(before['candidates'])-len(changed),'all_existing_bindings_catalog_policies_preserved':True,'native_approval':False,'runtime_retrieval':'not_yet_built','allowlist':[str((A/x).relative_to(ROOT)) for x in [cm,bm,sm,corpus.MANIFEST_NAME]]+sorted({str((A/m['file']).relative_to(ROOT)) for m in manifest['modules'] if m['kind']=='candidates' and any(cid in read(A/m['file'])['candidates'] for cid in changed)})}
 write(O/'data-integration.json',report);print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
