"""Independent read/identity audit and bounded actual-admission checks. No writes outside own peer artifacts."""
import ast,copy,gzip,hashlib,json,pathlib,sys
ROOT=pathlib.Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
G=pathlib.Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
O=R/'native_batches/review06250-00000-00020-149-04';D=R/'native-inputs/prepared/review06250-00000-00020-149-04'
def H(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def read(p):return json.loads(pathlib.Path(p).read_text())
def raw(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def rel(p):
 try:return str(pathlib.Path(p).relative_to(ROOT))
 except ValueError:return str(p)
def ref(p,x=None):return {'file':rel(p),'file_sha256':raw(p),'sha256':H(read(p) if x is None else x)}
assert raw(O/'BATCH.json')=='7d38bd7e01b91bec137238c7e5870785239f50b88f45d120e2e8b848ab2da5f5'
assert raw(O/'NOTE.json')=='8b30d48ca7acf34a56d4277af11f1add48aad264bcc4bef51d19c8e4da2eb934'
B=read(O/'BATCH.json');I=read(D/'INPUT.json');A=read(D/'ASSIGNMENT.json');P=read(D/'PREPARED-PACKET.json')
currentpath=ROOT/I['current_snapshot']['file'];S=json.loads(gzip.decompress(currentpath.read_bytes()))
originalpath=ROOT/I['original_snapshot']['file'];original=json.loads(gzip.decompress(originalpath.read_bytes()))
assert H(S)=='a3ac73e618b4443855c9cba07a0b0f9977c65cd19d0dcb92188ea2b208fddec7'
catalog=I['catalog_review']['after'];assert H(catalog)==H(S['slot_catalog'])=='d9f4db418e1b63cd100b4c7a9fbff4c8401e00dffeffd22e299a0b5087a82b15'
assert B['assignment_sha256']==H(A) and B['input_sha256']==H(I)
previouspath=R/'native_batches/review06250-00000-00020-149-03/BATCH.json';previous=read(previouspath)
stage2path=R/'native_batches/review06250-00000-00020-149-02/BATCH.json';stage2=read(stage2path)
REUSED=[3,4,5,8,9,10,13,14,15,16,17,18,19];FIRST7=[3,4,5,9,16,17,18];GENRE6=[8,10,13,14,15,19];LIGHT7=[0,1,2,6,7,11,12]

# Extract actual raw JSON value substrings, not only reserialized canonical bytes.
decoder=json.JSONDecoder()
def member_text(text,key):
 pos=0
 while text[pos].isspace():pos+=1
 assert text[pos]=='{';pos+=1
 while True:
  while text[pos].isspace() or text[pos]==',':pos+=1
  if text[pos]=='}':raise KeyError(key)
  k,end=decoder.raw_decode(text,pos);pos=end
  while text[pos].isspace():pos+=1
  assert text[pos]==':';pos+=1
  while text[pos].isspace():pos+=1
  start=pos;_,pos=decoder.raw_decode(text,pos)
  if k==key:return text[start:pos]
def array_texts(text):
 assert text[0]=='[';pos=1;result=[]
 while True:
  while text[pos].isspace() or text[pos]==',':pos+=1
  if text[pos]==']':return result
  start=pos;_,pos=decoder.raw_decode(text,pos);result.append(text[start:pos])
newtexts=array_texts(member_text((O/'BATCH.json').read_text(),'records'))
oldtexts=array_texts(member_text(previouspath.read_text(),'records'))
stage2texts=array_texts(member_text(stage2path.read_text(),'records'))
reuse=[]
for n in REUSED:
 a,b=member_text(newtexts[n],'proof'),member_text(oldtexts[n],'proof')
 assert a.encode()==b.encode() and B['records'][n]['proof']==previous['records'][n]['proof']
 assert all(B['records'][n][k]==previous['records'][n][k] for k in ['source_after','dependency_records','reference_bindings'])
 if n in FIRST7:assert a.encode()==member_text(stage2texts[n],'proof').encode()
 reuse.append({'ordinal':n,'proof_raw_value_sha256':hashlib.sha256(a.encode()).hexdigest(),'proof_canonical_sha256':H(B['records'][n]['proof']),
  'raw_proof_bytes_identical_03_04':True,'raw_proof_bytes_identical_02_04':n in FIRST7,'new_writer_signature':False,'new_writer_read_credit':0})

manual={
0:('agree_conditional_source_native','Neon source type is E. App supports existing selected illumination and all receiving members, not a sign/color/new light; complete-scope and relation restrictions remain mandatory. All normal fact values are supported locally.'),
1:('agree_conditional_source_native','LED remains E while laboratory-use designation is independently frozen P on that same actual source. Lab is not dropped and does not create a lab room/worker. Exact source guard and P retain designated laboratory-use context.'),
2:('agree_conditional_source_native','Softbox is a source modifier E on existing illumination with full Rx. No softness, shape, measured shadow transition, new box/support/window or device count is inferred.'),
3:('agree_conditional_source_native','Fantasy is a selected image genre E, not a proven fictional world, magical event or added entity. KO partial reference retains the complete same genre.'),
4:('agree_conditional_source_native','Fine-art genre E retains the complete named category; gallery tag creates no gallery, substrate or art movement.'),
5:('agree_conditional_source_native','Recorded motion blur E has image-plane scope; no actor motion, panning, speed, direction, duration or exposure is inferred. Missing original camera effect was explicitly repaired in selected current source.'),
6:('agree_conditional_source_native','Flash source type AND hard received quality remain distinct E, each with every actual receiver. No frontal direction/power/numeric extent or complete lighting setup is supplied.'),
7:('agree_conditional_source_native','Fluorescent-source illumination is the disclosed bounded original-label interpretation; no fluorescent dye/material, green cast, flicker, medical place or new lamp is inferred.'),
8:('agree_conditional_source_native','Complete travel_photograph genre value retains travel conventions. Root-selected App expressly avoids claiming a journey/history or creating a traveler/destination. It is not a generic photography value that drops travel.'),
9:('agree_conditional_source_native','50mm and named standard class are both E on the recording camera. Numeric spelling50 is normalization of50mm, without sensor-format/FOV/aperture/distance/focus claims.'),
10:('agree_conditional_source_native','Complete pet_photography E and independently pet-theme-compatible image P retain the pet qualifier without inventing an animal, species, count, owner or identity.'),
11:('agree_conditional_source_native','Actual same-scene golden-hour timing E AND natural-golden-hour illumination-treatment E both remain. Existing source/receivers are guarded to that actual scene. No desired golden-hour value is P and no sunset/sunrise/hue/weather is inferred. Retained lighting E receives no unsupported light_type/quality/setup role.'),
12:('agree_conditional_source_native','Window source-route E AND soft received-quality E remain, with actual existing path/type/window-route P and retained path-source/receiver-via PR. Source guard binds path/source/allRx to actual IDs. Existing path-window-route P does not replace source-route E or waive its locks. No geometry/window creation.'),
13:('agree_conditional_source_native','Food_photography E retains food theme; exact independently food-theme-compatible image P is required. No dish/tableware/cooking/stillness/physical medium is inferred.'),
14:('agree_conditional_source_native','Dieselpunk aesthetic is one actual canonical setting/image/setting.aesthetic_reading E. Manual aesthetic role view uses that same fact and exact facet without a shadow style E, property rename, world rules or private mood inference; original setting locks remain.'),
15:('agree_conditional_source_native','Street_photography remains complete genre E, with disclosed App limiting adoption to conventions rather than changing a street/city, adding people or asserting candid capture.'),
16:('agree_conditional_source_native','Focused scene atmosphere E is clarified by current EN and KO, not optical focus, a work actor/action or proven psychology.'),
17:('agree_conditional_source_native','24mm and named wide-angle class are both recording-camera E; neither invents sensor size, approach/angle, distorted body geometry, aperture or selected focus.'),
18:('agree_conditional_source_native','Laboratory is a location E on the independently declared scene address, not a research worker, experiment, equipment, sterility or actual lab designation for some separate light.'),
19:('agree_conditional_source_native','Interior_photography E retains full interior-space theme, with exact independent theme-compatibility P. It does not introduce or select room/furniture/architecture/lens/physical medium.')}

rows=[]
for row in B['records']:
 n=row['ordinal'];cid=row['candidate_id'];proof=row['proof']
 assert row['source_before']==original['candidates'][cid]==P['original_records'][cid]
 assert row['source_after']==S['candidates'][cid]==P['current_records'][cid]
 loc=row['original_compiled'];r=read(ROOT/loc['file'])['decisions'][loc['item']-1]
 assert raw(ROOT/loc['file'])==loc['file_sha256'] and H(r)==loc['row_sha256'] and r==P['historical_compiled_rows'][cid]
 own={k:v for k,v in S['slot_bindings'].items() if v['candidate_id']==cid};assert len(own)==1
 assert own=={k:v for k,v in original['slot_bindings'].items() if v['candidate_id']==cid}
 assert row['dependency_records']==row['reference_bindings']=={}
 assert proof['dependencies']=={'base':[]} and proof['reference_sha256']=={} and proof['profile_contracts']=={'base':None}
 assert proof['effect_sets']=={'base':row['source_after']['effects']}
 assert proof['guard_sets']=={'base':{'source_conditions':[row['source_after']['conditions'],{}],'member_conditions':{}}}
 assert set(row['source_before']['effects']['dimensions'])<=set(row['source_after']['effects']['dimensions'])
 for slot,role in proof['roles'].items():assert role['spec_sha256']==H(catalog[slot])
 for f in proof['facts']:
  x=row['source_after']
  for k in f['pointer'].split('/')[1:]:x=x[int(k)] if isinstance(x,list) else x[k]
  assert f['quote'] in x
 rows.append({'ordinal':n,'candidate_id':cid,'peer_disposition':manual[n][0],'individual_semantic_reason':manual[n][1],
  'original_sha256':H(row['source_before']),'current_sha256':H(row['source_after']),'proof_sha256':H(proof),'actual_native_contract_sha256':proof['review']['native_review']['native_contract_sha256'],
  'original_compiled_locator':loc,'own_bindings_whole':own,'required_closure':{},'read_full_facts_source_units_modes_values_ops_requires_receivers_roles_owner_maps_conditions':True,
  'writer_history_group':'previous_accepted7' if n in FIRST7 else 'new03_genre_aesthetic6' if n in GENRE6 else 'new04_lighting7',
  'source_native_semantic_agreement_is_conditional':True,'root_acceptance':False})

# Read fixture source functions without executing their writer loops/output code.
# These are explicitly reused controlled fixtures, not newly independent fixtures
# or proof of an actual requester. Run real pinned admission, not diagnostic flags.
assert raw(G/'scripts/photo_semantic_evidence.py')=='f74a5ef91bc07048c8bf312b66680c5b92b3b7b388f31f1890f31c8578609dee'
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_semantic_evidence as e
import photo_candidate_corpus as c
import photo_search_layout as layout
assert pathlib.Path(e.__file__).resolve()==G/'scripts/photo_semantic_evidence.py'
def functions(path,names,env):
 tree=ast.parse(path.read_text());nodes=[node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name in names]
 assert {node.name for node in nodes}==set(names)
 exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),env)
 return env
light_script=R/'authored/native_06250_first20_149_04.lighting-check.py'
reuse_script=R/'authored/native_06250_first20_149_04.reused-check.py'
lv=functions(light_script,['fixture','choices'],{'e':e,'c':c,'hashlib':hashlib,'B':B})
tv=functions(reuse_script,['fixture'],{'e':e,'THEME':None})
checks=[]
for n in LIGHT7+[10,13,19]:
 row=B['records'][n];cid=row['candidate_id'];rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=row['proof']
 data={**S,'candidates':{**S['candidates'],cid:rec}}
 e.validate(rec,catalog,corpus=data)
 islight=n in LIGHT7
 if not islight:tv['THEME']={10:'pet_theme_compatible',13:'food_theme_compatible',19:'interior_space_theme_compatible'}[n]
 defects=([None,'source_kind_missing','receiver_presence_missing','last_relation_wrong']+
          (['lab_designation_missing'] if n==1 else [])+
          (['scene_relation_wrong'] if n==11 else [])+
          (['path_route_wrong','path_source_wrong','last_via_wrong'] if n==12 else [])) if islight else [None,'missing_theme','wrong_theme','theme_on_other']
 for label,view in [('full',data),('compact',{**data,'candidates':{**data['candidates'],cid:layout.guard_record(rec,data)}})]:
  for defect in defects:
   core=lv['fixture'](n,defect=defect) if islight else tv['fixture']('style','image',**({defect:True} if defect else {}))
   admission_called=False
   try:
    mapping=lv['choices'](rec,core) if islight else None
    entry=c.entry(view,cid,realization_id='base',**({'owner_selections':mapping} if mapping else {}))
    admission_called=True;receipt=e.admission(entry,core)
   except (ValueError,KeyError) as error:
    assert defect is not None
    receipt={'allowed':False,'phase':'frozen_inventory_or_selection_validation_before_admission','error_type':type(error).__name__,'error':str(error)}
   assert bool(receipt['allowed'])==(defect is None),(n,label,defect,receipt)
   if defect is None:
    expected_count=({0:6,1:7,2:6,6:6,7:6,11:8,12:12}[n] if islight else 1)
    assert len(receipt['resolved_frozen_facts'])==expected_count,(n,receipt)
    assert all(x['core_assertion_id'] for x in receipt['resolved_frozen_facts'])
    assert not receipt.get('search_only')
   checks.append({'ordinal':n,'view':label,'defect':defect,'expected_allowed':defect is None,'admission_called':admission_called,'actual_receipt':receipt})

modules={}
for name,m in sorted(sys.modules.items()):
 if name.startswith(('photo_','photo_precore_')) and getattr(m,'__file__',None):
  p=pathlib.Path(m.__file__).resolve();assert p.is_relative_to(G),(name,p)
  modules[name]={'file':str(p),'file_sha256':raw(p)}
admission_calls=sum(x['admission_called'] for x in checks)
technical={'schema':'photo-independent-first20-peer04-admission-samples/v1','task':'/root/review_05250_06250','model':'gpt-6.1-sol','reasoning_effort':'high',
 'batch':ref(O/'BATCH.json',B),'actual_modules':modules,'fixture_functions_reused':[ref(light_script,{'kind':'python-source'}),ref(reuse_script,{'kind':'python-source'})],
 'fixture_boundary':'Reused the directly read writer-controlled fixture function bodies through AST function-only extraction. No writer loop or frozen output artifact is executed/rewritten. These are synthetic controlled request assertions, not independent real-request evidence or proof that an inventory is semantically complete.',
 'actual_check_cases':len(checks),'actual_admission_calls':admission_calls,'pre_admission_fail_closed_cases':len(checks)-admission_calls,'passed_check_cases':len(checks),'sampled_source_records':10,'checks':checks,
 'harness_history':'First attempt stopped on the deliberately missing receiver presence before admission: frozen inventory validation correctly raised. No output artifact was written. Harness instrumentation now distinguishes those early structural rejections from actual admission calls; this is not a runtime defect or a waived check.',
 'whole_consumer_reruns':0,'new_proofs_or_signatures':0,'operating_changes':0}
techpath=R/'authored/native_05250_first20-peer04.actual-admission-v1.json'
assert not techpath.exists();techpath.write_text(json.dumps(technical,ensure_ascii=False,sort_keys=True,indent=2)+'\n')

specs=['light_type','light_quality','lighting','time_of_day','capture_configuration','light_direction','light_intensity','light_color','light_shape','genre','aesthetic_trend','medium','capture_context','staging_degree','motion_rendering','camera_movement','exposure','physical_motion','shadow_relation','mood','lens','location','world','focus','depth_of_field']
out={'schema':'photo-independent-native-semantic-peer-review/v1','task':'/root/review_05250_06250','model':'gpt-6.1-sol','reasoning_effort':'high',
 'inputs':{'batch':ref(O/'BATCH.json',B),'note':ref(O/'NOTE.json'),'assignment':ref(D/'ASSIGNMENT.json',A),'input':ref(D/'INPUT.json',I),'prepared_packet':ref(D/'PREPARED-PACKET.json',P),'current_snapshot':{'file':rel(currentpath),'file_sha256':raw(currentpath),'sha256':H(S)},'catalog_sha256':H(catalog)},
 'independent_read_scope':{'whole_original_current_exact5B_ownbindings_empty_closure':20,'all_actual_proofs_facts_source_units_roles_guards_owner_maps':20,'new_unique_bulk_review_credit':0,'new_writer_read_credit_for_reuse13':0,
  'actual_reuse_identity':reuse,'prior_accepted7':FIRST7,'new03_genre_aesthetic6':GENRE6,'new04_lighting7':LIGHT7,
  'duplicate_read_method':'Complete App source unit quote and repeated guard_set source conditions were reused only after exact equality to the directly read complete current field/conditions. Earlier overlong outputs were not counted as complete; all20 were subsequently reread in bounded groups. No semantic string or conditional clause was keyword-compressed.',
  'fullspecs':{k:{'sha256':H(catalog[k]),'full_spec':catalog[k]} for k in specs}},
 'conclusion':'Peer semantic agreement on all20 conditional source-native records under the exact root-selected current04 source. No blocking quote/value/owner/condition/effect omission found in this review. This is independent Codex peer judgement, not root acceptance or actual-user/pixel evidence.',
 'blocking_findings':[],'record_assessments':rows,
 'execution_code_review':{'writer_scripts_read_whole':[ref(light_script,{'kind':'python-source'}),ref(reuse_script,{'kind':'python-source'}),ref(R/'authored/native_06250_first20_149_04.controls.py',{'kind':'python-source'})],
  'frozen_implementation_read':[{'file':str(G/'scripts/photo_semantic_evidence.py'),'file_sha256':raw(G/'scripts/photo_semantic_evidence.py'),'sections':['admission/_admission965-1098','_guard_context selected-node/source-guard framing1860-1918','_evaluate_target_guards1921-2023']}],
  'typed_P_PR_execution':'admission resolves the shared B1 node then compares every expanded prerequisite/preservation fact to one independently frozen actual-owner fact with exact dimension/property/type/value. Preservation same references resolve an actual core assertion. Source target guards resolve that same selected source/path/scene, quantifiers execute every actual inventory member, and guard receipts retain core assertion IDs. No fixture qualified flag waives these checks.',
  'source_full_and_manual_view_boundary':'Full source data is passed into role qualification and full-source validation occurs before compact guard_record construction. The dieselpunk facet is an ordinary App substring of the same canonical E; original target/property/mode/operation/Rx/closure remain unchanged.',
  'actual_sample_rerun':ref(techpath,technical),'actual_check_cases':len(checks),'actual_admission_calls':admission_calls,'whole_consumer_reruns_by_peer':0},
 'limits':['No actual user request was supplied: controlled cores demonstrate conditional matching and permission mechanics only.','Independent inventory completeness, theme-compatibility truth and visible rendering still require actual source/request review; hashes and boolean flags do not prove them.','Writer full/compact/property/whole/alias/ancestor controls were inspected, but their complete matrix was not rerun by this peer. The separate bounded90-case audit distinguishes actual admission calls from pre-admission structural rejection.','Canonical original20 all have empty effect properties; original dimensions remain and selected refined properties/actual Rx are checked. The unrelated3169 original-property-rename issue is not transplanted into this input.','Raw13 proof values are identical across03/04, with original7 also identical to02. This is reuse, no resigning or fresh writer semantic-read claim.','Existing ownbinding records/conditions remain exact historical source; proposed native roles are individually judged and not automatic persistent-binding creation. Root owns integration and operating publication.'],
 'new_proofs':0,'new_signatures':0,'source_changes':0,'root_acceptance':0,'qualified_operating_count':0,'Git':0,'model_calls':0,'network_calls':0}
dest=R/'authored/native_05250_first20-peer04.review-v1.json';assert not dest.exists();dest.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
note={'schema':'photo-independent-peer-worker-note/v1','task_name':'/root/review_05250_06250','model':'gpt-6.1-sol','reasoning_effort':'high','artifact':ref(dest,out),'actual_admission':ref(techpath,technical),'whole_source_and_proof_read_count':20,'semantic_agree_count':20,'blocking_findings':0,'exact_raw_proof_reuse13_verified':True,'new_signatures':0,'root_accepted':False,'operating_changes':0,'consumer_full_matrix_reruns':0,'actual_check_cases':len(checks),'actual_admission_calls':admission_calls,'new_unique_bulk_count':0}
np=R/'worker-notes/native_05250_first20-peer04.note-v1.json';assert not np.exists();np.write_text(json.dumps(note,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
for p in [techpath,dest,np]:print(json.dumps(ref(p),ensure_ascii=False))
print('PASS check cases',len(checks),'actual admission calls',admission_calls,'peer semantic agreement',len(rows))
