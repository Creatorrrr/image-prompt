"""Isolated, manually declared synthetic admission witnesses; never production core retrofit."""
import json,gzip,copy,hashlib,sys
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/1871bafa0e008e186ccce4e92908f2b177529b215c22e2fb46d07f0b28679bfd');sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
D=R/'native-inputs/prepared/review11870-01250-01300-02';I=json.loads((D/'INPUT.json').read_text());S=json.loads(gzip.decompress(Path(I['current_snapshot']['file']).read_bytes()));A=json.loads((D/'ASSIGNMENT.json').read_text());P=json.loads((D/'PREPARED-PACKET.json').read_text());CAT=I['catalog_review']['after'];CH=c.digest(CAT);ROWS=[];CPS=[]
for start in range(1250,1300,5):
 cp=R/('authored/native_11870_formal02_checkpoint_%05d_%05d.json'%(start,start+5));j=json.loads(cp.read_text());ROWS.extend(j['records']);CPS.append({'file':str(cp),'sha256':c.digest(j),'file_sha256':hashlib.sha256(cp.read_bytes()).hexdigest()})
def assertion(aid,kind,dimension='subject',**axes):return {'assertion_id':aid,'dimension':dimension,'polarity':'required','source_span_ids':['fixture_request'],'affected_dimensions':[dimension],'axes':{'native_schema':'photo-frozen-semantics/v1','kind':kind,**axes},'evidence':{'meaning':'Independently declared existing face F, photograph I, and charm C where explicitly selected in this synthetic fixture.'}}
def core(roles,values,opendims):
 text='Independently declared existing face F, photograph I, and charm C where explicitly selected in this synthetic fixture.'
 rows=[]
 for idx,(role,owner) in enumerate(roles):rows.extend([assertion('o'+str(idx),'owner',owner=owner,owner_kind='entity'),assertion('r'+str(idx),'role',owner=owner,role=role)])
 for idx,(dim,owner,prop,typ,val) in enumerate(values):rows.append(assertion('f'+str(idx),'fact',dimension=dim,owner=owner,property=prop,value_type=typ,value=val))
 return {'contract_version':'photo-authorial-core/v3','subject':text,'baseline_prompt_en':text,'request_binding':{'active_spans':[{'source_span_id':'fixture_request','text':text}]},'semantic_assertions':rows,'user_exclusions':[],'intent_lock':{'contract_version':'photo-intent-lock/v2','locked_dimensions':['age','concept','count','event','identity','subject'],'open_dimensions':opendims,'semantic_anchors':[]}}

# Literal independently declared synthetic requests. No values generated from proof P facts.
# Tuple: ordinal, explicit core roles, exact frozen witness facts.
def ep(owner):return ('subject',owner,'entity.presence','entity.presence/v1','present')
def ap(owner,part):return ('subject',owner,'anatomy.'+part+'.presence','anatomy.'+part+'.presence/v1','present')
def pt(owner,value):return ('subject',owner,'props.type','props.type/v1',value)
F=ap('F','face');E=ep('I');SC=ep('S');PE=ep('P')
FIXTURES=[
 (1250,[('primary_face','F')],[F]),
 (1251,[('image','I'),('primary_face','F')],[E,F]),
 (1252,[('primary_face','F')],[F]),
 (1254,[('primary_prop','C')],[pt('C','thread_charm')]),
 (1257,[('scene','S')],[SC]),
 (1259,[('primary_prop','C')],[pt('C','tarot_card_set')]),
 (1260,[('main_subject','P')],[PE]),
 (1261,[('scene','S')],[SC]),
 (1262,[('main_subject','P'),('primary_prop','G')],[PE,pt('G','gavel')]),
 (1263,[('primary_face','F')],[F,ap('F','eyes'),ap('F','mouth')]),
 (1266,[('main_subject','P'),('primary_prop','W'),('scene','S')],[PE,pt('W','magic_wand_prop'),SC]),
 (1268,[('main_subject','P')],[PE,('subject','P','entity.type','entity.type/v1','human')]),
 (1269,[('primary_face','F')],[F,ap('F','mouth'),ap('F','lips')]),
 (1270,[('light_source','L'),('image','I')],[('lighting','L','lighting.source.type','lighting.source.type/v1','fairy_lights'),E]),
 (1271,[('primary_prop','Q'),('primary_hands','H')],[pt('Q','polaroid_print_set'),('body_geometry','H','body.part.presence','body.part.presence/v1','hand')]),
 (1274,[('light_receiver','A'),('scene','S')],[('atmosphere','A','air.presence','air.presence/v1','air_volume'),SC]),
 (1276,[('recording_camera','K'),('image','I'),('primary_prop','R')],[ep('K'),E,pt('R','railing')]),
 (1277,[('main_subject','P')],[PE]),
 (1279,[('scene','S')],[SC]),
 (1281,[('scene','S')],[SC]),
 (1282,[('scene','S')],[SC]),
 (1283,[('recording_camera','K'),('image','I'),('secondary_subject','C'),('scene','S')],[ep('K'),E,('subject','C','entity.type','entity.type/v1','crowd'),SC]),
 (1288,[('recording_camera','K'),('image','I'),('main_subject','P')],[ep('K'),E,PE]),
 (1289,[('scene','S')],[SC]),
 (1290,[('scene','S')],[SC]),
 (1291,[('main_subject','P')],[PE]),
 (1292,[('primary_prop','C')],[pt('C','paper_crane')]),
 (1293,[('primary_hair','H')],[ap('H','hair')]),
 (1294,[('scene','S')],[SC]),
 (1297,[('primary_prop','O')],[ep('O')]),
 (1298,[('primary_prop','B')],[pt('B','florist_delivery_box')])]
assert [x['ordinal'] for x in ROWS]==list(range(1250,1300))
assert [x['ordinal'] for x in ROWS if x['proof']]==[x[0] for x in FIXTURES]
sourcechecks=[];results=[]
for row in ROWS:
 cid=row['candidate_id'];assert row['source_before']==P['original_records'][cid];assert row['source_after']==P['current_records'][cid];assert row['source_after']==S['candidates'][cid]
 assert row['original_compiled']==I['original_decisions'][cid]
 assert row['revision']['prior_review']==I['required_revisions'][cid]['prior_review'];assert row['revision']['memo_artifacts']==I['required_revisions'][cid]['memo_artifacts']
 assert row['dependency_records']=={} and row['reference_bindings']=={}
 if row['proof'] is None:assert row['status']=='pending';continue
 proof=row['proof'];rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=proof
 n.validate(rec,CAT,catalog_sha256=CH,corpus=S)
 compact=n.compact(rec,corpus=S);assert compact
 assert proof['review']['native_review']['native_contract_sha256']==n.native_contract_sha256(proof)
 assignments={}
 for f in proof['facts']:
  if f['mode']=='effect':assignments.setdefault((f['realization_id'],f['target'],f['dimension'],f['property']),set()).add(c.digest({'value':f['value'],'operation':f['operation'],'receivers':sorted(f['receivers'])}))
 assert all(len(v)==1 for v in assignments.values()),row['ordinal']
 S['candidates'][cid]=rec;entry=c.entry(S,cid,realization_id='base');full=copy.deepcopy(entry);full.pop('_semantic_evidence_guard');short=copy.deepcopy(entry);short.pop('role_evidence',None)
 ordinal,roles,values=next(x for x in FIXTURES if x[0]==row['ordinal'])
 # Only test witnesses, never request freeze, permissions or final render here.
 fixture=core(roles,values,[]);missing=core(roles,values[1:],[])
 for label,k,expected in [('explicit_independent_exact_tuples',fixture,True),('first_actual_prerequisite_absent',missing,False)]:
  for view,en in [('full',full),('compact',short)]:
   adm=n.admission(en,k);assert adm['allowed']==expected,(ordinal,label,view,adm)
   results.append({'ordinal':ordinal,'case':label,'view':view,'core_sha256':c.digest(k),'expected':expected,'admission':adm})
 sourcechecks.append({'ordinal':ordinal,'candidate_id':cid,'proof_sha256':c.digest(proof),'full_source_validation':True,'compact_guard_created':True,'same_actual_E_property_assignments_consistent':True,'source_after_exact_prepared_input':True})
mods={}
for name,m in sorted(sys.modules.items()):
 if getattr(m,'__file__',None) and (name.startswith('photo_') or name=='prompt_generator' or Path(m.__file__).resolve().is_relative_to(G)):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G);mods[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
O=R/'authored/native_11870_formal02_full31_checks.json';assert not O.exists();out={'schema':'photo-native-manual-full-source-qualification-checks/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','input_sha256':c.digest(I),'assignment_sha256':c.digest(A),'catalog_sha256':CH,'checkpoints':CPS,'actual_source_read_count':50,'fresh_fullproof_validated_count':len(sourcechecks),'pending_count':19,'checks':sourcechecks,'synthetic_exact_typed_full_compact_admission_assertions_passed':len(results),'synthetic_admission_results':results,'module_paths_sha256':mods,'frozen_generation':G.name,'os_network_denied':True,'provider_keys_absent':True,'network_model_calls':0,'whole_corpus_or_batch_verification':False,'runtime_retrieval_or_actual_request_freeze_or_final_render_or_pixels_or_operating_checks':False,'boundary':'Source proof validation/compact construction and independently authored synthetic witness consumption only. Every positive synthetic fixture is literal test declaration, never inferred from the proof fact loop or inserted into any real core. Normal effect permission remains separate; none of these 31 admission positives asserts full consumer acceptance.'};O.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(O,c.digest(out),hashlib.sha256(O.read_bytes()).hexdigest());print(len(sourcechecks),'source proofs and compact guards;',len(results),'full/compact synthetic witness assertions passed')
