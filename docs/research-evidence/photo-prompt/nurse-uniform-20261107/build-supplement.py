from pathlib import Path
import hashlib,json,uuid,sys,shutil
R=Path('/Users/chasoik/Projects/image-prompt');A=R/'skills/photo-prompt-image-generator/assets';O=R/'docs/research-evidence/photo-prompt/nurse-uniform-20261107';sys.path.insert(0,str(R/'skills/photo-prompt-image-generator/scripts'))
import photo_candidate_retrieval_views as rv
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,o):
 if p.exists():raise RuntimeError('refusing overwrite '+str(p))
 p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
reports={}
for letter in 'abc':
 src=R/f'generated/nurse-additions-{letter}.json';dest=A/f'photo_nurse_uniform_supplement_proposals_{letter}_20261107.json';assert not dest.exists();shutil.copyfile(src,dest); reports[letter]=(dest,json.loads(dest.read_text()))
ns=uuid.UUID('2e1908a2-793f-4de3-8ffc-d71b15bb539b');uid=lambda pre,key:pre+uuid.uuid5(ns,key).hex
contract='Apply only as a complete optional visual realization to independently identified owners and permitted changes. Preserve all stated objects, garment parts, owners, count, contacts, spatial relations, conditions and visible endpoint requirements. Hidden elements are unobservable, not a pass. Appearance alone does not establish identity, age, occupation, intent, consent, events, material chemistry or actual protective performance. Research metadata does not confer native qualification or permission.'
candidates={};bindings={};cards=[];links={};held=[]
for letter,(source,report) in reports.items():
 for row in report['rows']:
  if row['classification']!='candidate':held.append({'row_id':row['row_id'],'status':row['classification'],'source':source.name});continue
  proposals=row.get('proposals') if letter=='a' else [row]
  for i,p in enumerate(proposals):
   en=p['visual_proposition_en'] if letter=='a' else p['en']; ko=p['visual_proposition_ko'] if letter=='a' else p['ko']; slot=p['suggested_slot'] if letter=='a' else p['slot'];dims=p['effect_dimensions']; pid=p['proposal_id']; cid=uid('cand_',pid); bid=uid('bind_',pid+':'+slot)
   assert en and ko and len(dims)>0 and cid not in candidates
   code=row['row_id']; name=row['source_term_label'] if letter in 'ab' else row['source_label'];boundary=p['boundary_and_uncertainty'] if letter=='a' else row['boundary']; comparison=p['existing_candidate_comparison'] if letter=='a' else row['existing_comparison']; adult=(letter=='b' and p.get('candidate_conditions',{}).get('requires_adult_context') is True) or code=='NURSE-ROW-280';conditions={'for_any':['human'],'requires_adult_context':True} if adult else {}
   specific=' Explicit adult context must be independently established.' if adult else ''
   card={'id':pid,'source_row_id':code,'candidate_id':cid,'positive_en':en,'positive_ko':ko,'suggested_slot':slot,'source_proposal':source.name,'source_proposal_sha256':sha(source),'source_evidence_scope':'Independent optional visual realization; source row definition does not make this depiction mandatory or establish hidden properties.','boundary':boundary,'existing_comparison':comparison,'observable_gate':en+' Every named endpoint and relation must be visible; hidden means unobservable.','native_approval':False,'pixel_status':'NOT_RUN'}
   rec={'id':cid,'record_kind':'visual_option','content':{'en':en,'ko':ko,'definition':'Complete optional nurse-uniform supplemental visual realization: '+en,'aliases':[name],'application_contract':contract+specific,'research_semantics':card},'conditions':conditions,'effects':{'dimensions':dims,'properties':[]},'provenance':[{'source':'authored-research:'+source.name+'#'+pid,'sha256':sha(source)}]}
   candidates[cid]=rec;bindings[bid]={'id':bid,'candidate_id':cid,'slot_id':slot,'role':'optional','semantic_role':'direct','conditions':{'subject_applicability':{}},'weight':1.0};cards.append(card);links.setdefault(code,[]).append(cid)
cf=A/'photo_candidate_nurse_uniform_supplement_20261107.json';bf=A/'photo_candidate_nurse_uniform_supplement_bindings_20261107.json';sf=A/'photo_nurse_uniform_supplement_semantics_20261107.json';vf=A/'photo_candidate_retrieval_views_nurse_uniform_supplement_20261107.json'; save(cf,{'schema':'photo-candidate-module/v3','candidates':candidates});save(bf,{'schema':'photo-candidate-slot-bindings/v3','slot_bindings':bindings});save(sf,{'schema':'photo-nurse-uniform-supplement-semantics/v1','source_proposals':[{'file':p.name,'sha256':sha(p)} for p,_ in reports.values()],'cards':cards,'source_row_to_candidates':links,'context_or_held':held,'native_approval':False,'pixel_qualification':'NOT_RUN'})
views=[]
for cid,rec in sorted(candidates.items()):
 en=rec['content']['en'];ko=rec['content']['ko'];rh=rv.digest(rec)
 for kind in ['whole','context']:
  key=cid+':base:'+kind;ctx=kind=='context';prefix='Complete optional nurse-uniform supplemental visual realization: '
  views.append({'id':rv.view_id(cid,'base',key),'candidate_id':cid,'realization_id':'base','key':key,'kind':kind,'source_record_sha256':rh,'text_en':('Nurse-uniform supplemental visual option: ' if ctx else '')+en,'text_ko':('간호복 보충 시각 선택지: ' if ctx else '')+ko,'source_quotes':([{'pointer':'/content/definition','quote':prefix}] if ctx else [])+[{'pointer':'/content/en','quote':en},{'pointer':'/content/ko','quote':ko}],'context_ko':'원본의 전체 한영 명제와 명시적 간호복 연구 맥락만 보존한다.','difference_ko':'원본 전체 명제','native_approval':False})
module={'schema':rv.SCHEMA,'recipe':rv.RECIPE,'source_inventory_id':'nurse-uniform-supplement-20261107','coverage':{'positive_realizations':len(candidates),'diagnostics_excluded':0,'source_module_sha256':sha(cf),'context_views':len(candidates)},'native_approval':False,'views':views};rv.validate(module,candidates);save(vf,module)
print(json.dumps({'candidates':len(candidates),'binding':len(bindings),'views':len(views),'rows_with_candidates':len(links),'held_or_context':len(held)}))
