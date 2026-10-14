"""Independent bounded controls on immutable simple5 bytes; no writer execution."""
import ast,copy,gzip,hashlib,json,sys
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014';A=R/'authored';G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_semantic_evidence as n
import photo_candidate_corpus as c
import photo_search_layout as layout
import prompt_generator as g
raw=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
read=lambda p:json.loads(Path(p).read_text())
assert raw(n.__file__)=='f74a5ef91bc07048c8bf312b66680c5b92b3b7b388f31f1890f31c8578609dee'
D=R/'native-inputs/prepared/review05250-simple5-149-01';O=R/'native_batches/review05250-simple5-149-01';B=read(O/'BATCH.json');I=read(D/'INPUT.json');S=json.load(gzip.open(ROOT/I['current_snapshot']['file']))
assert raw(ROOT/I['current_snapshot']['file'])==I['current_snapshot']['file_sha256'] and c.digest(S)==I['current_snapshot']['sha256']
# Reuse only explicitly named fixture definitions and literal constants. Never execute
# the writer/checker top-level loop, existing-artifact writes, or author new proofs.
fixturefile=A/'native_05250_simple5-source96.check-v1.py';tree=ast.parse(fixturefile.read_text());selected=[]
for node in tree.body:
 if isinstance(node,ast.FunctionDef) and node.name in ['fixture','contract_for','picked']:selected.append(node)
 if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ['TAGS','EXPECTED'] for t in node.targets):selected.append(node)
assert len(selected)==5
ns={'n':n};exec(compile(ast.Module(body=selected,type_ignores=[]),str(fixturefile),'exec'),ns)
fixture=ns['fixture'];contract=ns['contract_for'];picked=ns['picked'];expected=ns['EXPECTED'];results=[];count=0
for row in B['records']:
 o=row['ordinal'];cid=row['candidate_id'];record=copy.deepcopy(row['source_after']);record['content']['role_evidence']=row['proof'];data={**S,'candidates':{**S['candidates'],cid:record}}
 assert record['content']['role_evidence']==row['proof'];n.validate(record,S['slot_catalog'],corpus=data)
 binds=[k for k,v in S['slot_bindings'].items() if v['candidate_id']==cid];assert len(binds)==1
 for label,viewrecord in [('full',record),('compact',layout.guard_record(record,data))]:
  view={**data,'candidates':{**data['candidates'],cid:viewrecord}};entry=c.entry(view,cid,binds[0],realization_id='base');core=fixture(o)
  receipt=n.admission(entry,core);assert receipt['allowed'] and not receipt.get('search_only');dims,props,_=n.permission_scope(entry,core)
  owner='image_A' if o==6220 else 'scene_A';assert {(x['dimension'],x['property'],x['target']) for x in props}=={(d,p,owner) for d,p in expected[o]};count+=1
  for role in row['proof']['roles']:assert g.core_entry_eligible(view,core,contract(o),picked(o),role,entry);count+=1
  cases=[]
  def deny(name,bad):
   global count
   a=n.admission(entry,bad);consumer=g.core_entry_eligible(view,bad,contract(o),picked(o),next(iter(row['proof']['roles'])),entry)
   assert not a['allowed'] and not consumer,(o,label,name,a,consumer);count+=2;cases.append({'case':name,'admission':a,'actual_consumer_allowed':consumer})
  # Correct same-value facts on an explicitly disjoint owner cannot donate P/PR.
  bad=copy.deepcopy(core)
  for st in bad['semantic_assertions']:
   axes=st['axes']
   if axes.get('kind')=='fact':axes['owner']='other_A'
  deny('disjoint_owner_has_all_correct_typed_facts',bad)
  # A named existing role alone cannot substitute independently typed presence/type.
  for what in ['entity.presence','entity.type']:
   bad=copy.deepcopy(core);bad['semantic_assertions']=[x for x in bad['semantic_assertions'] if x['axes'].get('property')!=what]
   deny('role_without_'+what,bad)
  # Explicitly wrong kind/absent value has no alternate compatible fact fallback.
  for defect in ['wrong_presence','wrong_kind']:deny(defect,fixture(o,defect=defect))
  if o==6220:
   assert row['source_before']['effects']==row['source_after']['effects']=={'dimensions':['style'],'properties':[{'dimension':'style','property':'image.detail','target':'image_plane'}]}
   for defect in ['missing_contours','missing_details','wrong_contours','wrong_details']:deny(defect,fixture(o,defect=defect))
   for prop in ['image.detail','image.contour.continuity','image.small_surface_detail.readability']:
    bad=fixture(o,anchor=('style','image_A',prop))
    if prop=='image.detail':assert not g.core_entry_eligible(view,bad,contract(o),picked(o),'image_detail',entry);count+=1
    else:
     # Direct actual triple control, not a second qualified proof or union admission.
     assert not n.property_scope_allowed(bad,['style'],[{'dimension':'style','target':'image_A','property':prop}]);count+=1
  if o==6214:
   for dim in ['timing','atmosphere']:
    bad=fixture(o,whole=dim);assert not g.core_entry_eligible(view,bad,contract(o),picked(o),'location',entry);count+=1
   assert {(f['dimension'],f['property']) for f in row['proof']['facts'] if f['mode']=='effect'}=={('setting','setting.location'),('timing','timing.event_phase'),('atmosphere','mood.quiet')};count+=1
  if o!=6220:
   bad=fixture(o,anchor=('setting','scene_A','setting.location'));assert not g.core_entry_eligible(view,bad,contract(o),picked(o),'location',entry);count+=1
   assert not g.core_entry_eligible(view,core,contract(o),picked(o,missing=True),'location',entry);count+=1
  results.append({'ordinal':o,'view':label,'binding_id':binds[0],'positive_admission':receipt,'actual_permission_scope':props,'negative_controls':cases})
modules={}
for name,m in sorted(sys.modules.items()):
 if name.startswith(('photo_','photo_precore_')) and getattr(m,'__file__',None):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G),(name,p);modules[name]={'file':str(p),'raw_sha256':raw(p)}
assert Path(g.__file__).resolve().is_relative_to(G);modules['prompt_generator']={'file':str(Path(g.__file__).resolve()),'raw_sha256':raw(g.__file__)}
out={'schema':'photo-simple5-independent-peer-controls/v1','task_name':'/root/review_06250_07250','model':'gpt-6.1-sol','reasoning_effort':'high','batch_raw_sha256':raw(O/'BATCH.json'),'source_canonical_sha256':c.digest(S),'actual_assertion_count':count,'baseline_count':10,'fixture_reuse':{'file':str(fixturefile.relative_to(ROOT)),'raw_sha256':raw(fixturefile),'selected_function_names':['fixture','contract_for','picked'],'literal_constants':['TAGS','EXPECTED'],'boundary':'Existing controlled synthetic request fixture reused after direct read, not independently authored real user/core evidence. This independent run executes new bounded disjoint-owner/type/existence/PR/cross-role lock controls, not the original589 assertions.'},'results':results,'actual_modules':modules,'root_acceptance':0,'operating_qualification':0,'bulk_unique_read_credit':0,'boundary':'In-memory negative cores only. No source/proof/catalog/production/runtime mutation. Fixture negative values may contradict their positive source text and are intentional malformed-witness controls; they are not asserted as valid requester facts. Whole-source semantic judgment is reported separately, not inferred from these assertions.'}
p=A/'native_06250_simple5_peer01.controls.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('PASS',count,'baseline',10,'raw',raw(p))
