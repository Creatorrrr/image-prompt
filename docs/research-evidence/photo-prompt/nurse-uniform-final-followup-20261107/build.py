from pathlib import Path
import hashlib,json,sys,uuid,csv
R=Path('/Users/chasoik/Projects/image-prompt');A=R/'skills/photo-prompt-image-generator/assets';O=Path(__file__).parent;sys.path.insert(0,str(R/'skills/photo-prompt-image-generator/scripts'))
import photo_candidate_corpus as cc,photo_candidate_retrieval_views as rv
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):
 if p.exists():raise RuntimeError('refusing overwrite '+str(p))
 p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
prior=A/'photo_nurse_uniform_external_review_20261107.json';old=json.loads(prior.read_text())['rows'];covered=set()
for name in ['photo_nurse_uniform_external_source_supplement_20261107.json','photo_nurse_uniform_external_source_supplement2_20261107.json']:
 covered.update(x['source_row_id'] for x in json.loads((A/name).read_text())['rows'])
targets=[v for v in old if (not v['new_external_sources'] and v['source_row_id'] not in covered) or v['source_row_id']=='NURSE-ROW-285'];assert len(targets)==37
mapping=json.loads((O/'source-map.json').read_text());ids={v['source_row_id'] for v in targets};assert set(mapping)==ids
raw=list(csv.reader((O/'visual-options.tsv').open(),delimiter='\t'));assert len(raw)==25 and all(len(x)==7 for x in raw)
n=uuid.UUID('1ca7ed2b-7f7f-4bf9-b081-49d0e7cf2dc3');uid=lambda pre,s:pre+uuid.uuid5(n,s).hex
opts=[];links={}
for pid,num,label,slot,dims,en,ko in raw:
 rid='NURSE-ROW-'+num;assert rid in ids
 x={'id':pid,'source_row_id':rid,'name_ko':label,'slot':slot,'effect_dimensions':dims.split(','),'en':en,'ko':ko};opts.append(x);links.setdefault(rid,[]).append(uid('cand_',pid))
reuse={'237':'cand_feb931de1a0153ccb0bf7d08371f7a35','346':'cand_feb931de1a0153ccb0bf7d08371f7a35','327':'cand_bfb03c750544524e8288b3911a1892e6','328':'cand_9a3543a6184859b5a650b60417ba0136','329':'cand_8fa5241af02a5aa3be9bc42f8938a2dc','342':'cand_7833b4ed80545dbbbdf70eb972ad0e13','365':'cand_2eaff84c80a658239718b077db8a3520','378':'cand_3ad500fd77be5a3ca13b6bc8a4275947'}
for num,cid in reuse.items(): links.setdefault('NURSE-ROW-'+num,[]).append(cid)
diag_defs={'262':('Cleavage refers to the visible area between the breasts, often framed by a garment neckline.','클리비지는 의복의 목선 사이로 보이는 양쪽 가슴 사이 부분을 뜻한다.',['cleavage','클리비지']), '263':('Underboob refers to the lower portion of a breast, including when a cropped garment leaves it visible.','언더붑은 짧은 상의 등 아래로 드러날 수 있는 가슴 아랫부분을 뜻한다.',['underboob','언더붑']), '264':('Sideboob refers to the side portion of a breast, including when a low-cut armhole or side of a garment leaves it visible.','사이드붑은 낮은 암홀이나 옆선으로 드러날 수 있는 가슴 옆부분을 뜻한다.',['sideboob','사이드붑'])}
diagids={num:uid('cand_','D'+num) for num in diag_defs}
for num,cid in diagids.items():links.setdefault('NURSE-ROW-'+num,[]).append(cid)
links['NURSE-ROW-285']=['cand_1cc1ddabe95952d992cb345b76a8cf4f']
review=A/'photo_nurse_uniform_final_followup_review_20261107.json';ctx=A/'photo_nurse_uniform_final_followup_context_views_20261107.json';rows=[]
for v in targets:
 rid=v['source_row_id'];i=old.index(v);hold=rid=='NURSE-ROW-285';src=mapping[rid]
 boundary=('용어의 정의는 사전에서 확인되었으나 단일 사진에서 가려진 부위의 의복 부재와 연령은 확인할 수 없다. 전신 의미의 양성 구현은 계속 보류한다.' if hold else '출처는 명시된 일부 단서·용례만 뒷받침한다. 원문 전체나 후보의 완전 동등성, 가려진 부분, 나이·의도·행동의 이력은 증명하지 않는다.')
 rows.append({'source_row_id':rid,'source_term_label':v['source_term_label'],'source_definition_ko':v['source_definition_ko'],'previous_review_file':prior.name,'previous_review_sha256':sha(prior),'previous_review_pointer':f'/rows/{i}','previous_status':v['source_status'],'additional_sources':src,'source_status':'meaning_verified_visual_hold' if hold else 'new_scoped_source','linked_candidate_ids':links.get(rid,[]),'unresolved_ko':boundary,'native_approval':False})
write(review,{'schema':'nurse-uniform-final-followup-review/v1','scope':'36 rows without newly external sources plus distinct prior visual hold 285; 37 total','previous_review_file':prior.name,'previous_review_sha256':sha(prior),'source_map_sha256':sha(O/'source-map.json'),'rows':rows,'native_approval':False})
context=[]
for i,row in enumerate(rows):
 context.append({'id':'nurse-final-context-'+row['source_row_id'],'term_id':row['source_row_id'],'source_term_label':row['source_term_label'],'source_definition_ko':row['source_definition_ko'],'review_file':review.name,'review_sha256':sha(review),'review_pointer':f'/rows/{i}','additional_sources':row['additional_sources'],'linked_candidate_ids':row['linked_candidate_ids'],'positive_candidate_ids':[x for x in row['linked_candidate_ids'] if x not in set(diagids.values())|{'cand_1cc1ddabe95952d992cb345b76a8cf4f'}],'boundary_ko':row['unresolved_ko'],'context_only':True,'native_approval':False})
write(ctx,{'schema':'nurse-uniform-final-followup-context/v1','review_file':review.name,'review_sha256':sha(review),'search_scope':'Research-only; not a positive retrieval view or permission.','views':context,'native_approval':False})
contract='Apply only as one complete optional visual realization to independently identified owners and permitted changes. Preserve stated parts, counts, owners and relations. Do not infer age, identity, occupation, consent, intent, real treatment, material chemistry or events outside the frame. Source evidence supports only its stated scope. Research metadata does not grant native qualification or automatic selection.'
candidates={};bindings={};cards=[]
for p in opts:
 cid=uid('cand_',p['id']);bid=uid('bind_',p['id']+':'+p['slot']);rid=p['source_row_id'];row=next(x for x in rows if x['source_row_id']==rid)
 card={'id':p['id'],'candidate_id':cid,'source_row_id':rid,'source_review_file':review.name,'source_review_sha256':sha(review),'positive_en':p['en'],'positive_ko':p['ko'],'source_evidence':mapping[rid],'boundary_ko':row['unresolved_ko'],'scope':'One optional authored visual example; source evidence may cover only a component and does not establish equivalence, native admission or pixel quality.','native_approval':False,'pixel_status':'NOT_RUN'}
 if p['id']=='F295':card['boundary_ko']+=' 코스프레 출처는 Demon Nurse 용례만 확인하며 뿔 장식은 별도로 작성한 가상 예다.'
 rec={'id':cid,'record_kind':'visual_option','content':{'en':p['en'],'ko':p['ko'],'definition':'Complete optional nurse follow-up visual realization: '+p['en'],'aliases':[p['name_ko']],'application_contract':contract,'research_semantics':card},'conditions':{},'effects':{'dimensions':p['effect_dimensions'],'properties':[]},'provenance':[{'source':'authored-research:'+review.name+'#'+p['id'],'sha256':sha(review)}]};candidates[cid]=rec;bindings[bid]={'id':bid,'candidate_id':cid,'slot_id':p['slot'],'role':'optional','semantic_role':'direct','conditions':{'subject_applicability':{}},'weight':1.0};cards.append(card)
for num,(en,ko,aliases) in diag_defs.items():
 cid=diagids[num];rid='NURSE-ROW-'+num
 candidates[cid]={'id':cid,'record_kind':'diagnostic','content':{'en':en,'ko':ko,'definition':'Context and evidence boundary only; excluded from positive image material retrieval. '+en,'aliases':aliases,'application_contract':'Meaning and observability boundary only; excluded from positive image material retrieval. Do not infer age, identity, consent, unseen anatomy or attire, or promote this diagnostic into a positive instruction.','research_semantics':{'id':'D'+num,'source_row_id':rid,'source_review_file':review.name,'source_review_sha256':sha(review),'source_evidence':mapping[rid],'mode':'context_only','native_approval':False,'pixel_status':'NOT_RUN'}},'conditions':{},'effects':{'dimensions':[],'properties':[]},'provenance':[{'source':'authored-research:'+review.name+'#D'+num,'sha256':sha(review)}]}
cf=A/'photo_candidate_nurse_uniform_final_followup_20261107.json';bf=A/'photo_candidate_nurse_uniform_final_followup_bindings_20261107.json';sf=A/'photo_nurse_uniform_final_followup_semantics_20261107.json';vf=A/'photo_candidate_retrieval_views_nurse_uniform_final_followup_20261107.json';write(cf,{'schema':'photo-candidate-module/v3','candidates':candidates});write(bf,{'schema':'photo-candidate-slot-bindings/v3','slot_bindings':bindings});write(sf,{'schema':'nurse-uniform-final-followup-semantics/v1','source_review_file':review.name,'source_review_sha256':sha(review),'cards':cards,'source_row_to_candidates':links,'context_only_rows':['NURSE-ROW-262','NURSE-ROW-263','NURSE-ROW-264','NURSE-ROW-285'],'diagnostic_ids':diagids,'visual_hold_ids':['NURSE-ROW-285'],'prior_apron_component':'cand_ecc50a3413c95c128e502baa4c3e50b0','native_approval':False,'pixel_qualification':'NOT_RUN'})
views=[]
for cid,rec in sorted(candidates.items()):
 if rec['record_kind']=='diagnostic':continue
 en=rec['content']['en'];ko=rec['content']['ko'];rh=rv.digest(rec);prefix='Complete optional nurse follow-up visual realization: ';label=next(x['source_term_label'] for x in rows if x['source_row_id']==rec['content']['research_semantics']['source_row_id']);parts=label.split(' — ',1);ko_label=parts[0];en_label=parts[-1]
 for kind in ('whole','context'):
  isctx=kind=='context';key=cid+':base:'+kind
  views.append({'id':rv.view_id(cid,'base',key),'candidate_id':cid,'realization_id':'base','key':key,'kind':kind,'source_record_sha256':rh,'text_en':('Optional research topic (component only): '+en_label+'. ' if isctx else '')+en,'text_ko':('선택 연구 주제(일부 예시): '+ko_label+'. ' if isctx else '')+ko,'source_quotes':([{'pointer':'/content/definition','quote':prefix}] if isctx else [])+[{'pointer':'/content/en','quote':en},{'pointer':'/content/ko','quote':ko}],'context_ko':('원문 주제어는 검색용 연구 맥락이며 전체 명제나 필수 조건이 아니다. 실제 선택 의미는 출처 원본의 한영 예시다.' if isctx else '원본의 한영 시각 명제와 명시된 연구 맥락을 보존한다.'),'difference_ko':'전체 예시이며 원문 전체와의 동등성은 별도','native_approval':False})
module={'schema':rv.SCHEMA,'recipe':rv.RECIPE,'source_inventory_id':'nurse-uniform-final-followup-20261107','coverage':{'positive_realizations':len(bindings),'source_module_sha256':sha(cf),'context_views':len(bindings)},'native_approval':False,'views':views};rv.validate(module,candidates);write(vf,module)
m=A/'photo_candidate_corpus_manifest.json';data=json.loads(m.read_text());assert not any(x['file'] in (cf.name,bf.name) for x in data['modules']);data['modules'] += [{'file':cf.name,'kind':'candidates'},{'file':bf.name,'kind':'slot_bindings'}];m.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');loaded=cc.load(A);assert set(candidates)<=set(loaded['candidates']);print(json.dumps({'reviewed':len(rows),'source_rows':len(mapping),'candidate_records':len(bindings),'views':len(views),'candidate_rows':len(links),'context_only_rows':['NURSE-ROW-262','NURSE-ROW-263','NURSE-ROW-264','NURSE-ROW-285'],'diagnostic_ids':diagids,'total_candidates':len(loaded['candidates']),'total_bindings':len(loaded['slot_bindings'])}))
