"""Working entry fix against frozen B2 dependencies and actual bounded source proof."""
import copy,gzip,hashlib,importlib.util,json,sys,unittest
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014';O=R/'native_batches/review11870-01264-06'
GEN=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/694ba2cc064e0eae2ae0d24603f37250577122cd4a700ae10f6e379ec9057609')
sys.dont_write_bytecode=True
namespace={'__file__':str(O/'fixture_v1.py'),'__name__':'root_isolated_fixture'}
code=(O/'fixture_v1.py').read_text().replace('188c56270ebc2c973defd3307d8fa43df60e55701baa30c45367a4e2e3efe2bb',GEN.name)
exec(compile(code,str(O/'fixture_v1.py'),'exec'),namespace)
sys.path=[str(GEN/'scripts'),str(GEN/'precore')]+[p for p in sys.path if 'image-generator/scripts' not in p]
prompt=ROOT/'skills/photo-prompt-image-generator/scripts/prompt_generator.py'
spec=importlib.util.spec_from_file_location('root_working_prompt',prompt);generator=importlib.util.module_from_spec(spec);sys.modules[spec.name]=generator;spec.loader.exec_module(generator)
sys.path.insert(0,str(ROOT));import tests.test_photo_entry_domain_override as unit
unit.generator=generator
result=unittest.TestResult();unittest.defaultTestLoader.loadTestsFromModule(unit).run(result);assert result.wasSuccessful(),(result.failures,result.errors)
c,n=namespace['c'],namespace['n'];row=json.loads((O/'BATCH.json').read_bytes())['records'][0];cid=row['candidate_id'];I=json.loads((O/'INPUT.json').read_bytes());S=json.loads(gzip.decompress((ROOT/I['current_snapshot']['file']).read_bytes()));rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=row['proof'];S['candidates'][cid]=rec;n.validate(rec,S['slot_catalog'],corpus=S)
base=namespace['core']();ent,select,contract,picked=(namespace[x] for x in ['ent','select','contract','picked']);runs=[]
def check(label,k,want,*,category='object',domains=('visual_structure',),choose=True,extra=None):
 for view in ['full','compact']:
  entry=ent(S,cid,True,view)
  if choose:entry,kk=select(entry,k,row['proof'])
  else:kk=k
  ct=contract(category,list(domains))
  if extra:ct.update(extra)
  got=generator.core_entry_eligible(S,kk,ct,picked(category),'aftermath_trace',entry)
  assert got==want,(label,view,got,want)
  runs.append({'case':label,'view':view,'expected':want,'allowed':got,'entry_reason':generator.entry_block_reason(entry,'aftermath_trace',ct,catalog=S['slot_catalog'])})
check('actual_originalbinding_object_visual_structure',base,True)
check('actual_originalbinding_human',base,True,category='human',domains=())
for domains in [(),('product',),('visual_structure','product'),('visual_structure','jewelry'),('visual_structure','food'),('visual_structure','wildlife')]:check('independent_oldbinding_policy_'+str(domains),base,False,domains=domains)
check('missing_selection',base,False,choose=False)
for aid in ['chair_type','seat_type','chair_presence','seat_presence','actual_seat_of_same_chair']:
 check('missing_'+aid,namespace['delete'](base,aid),False)
check('wrong_part_of',namespace['alter'](base,'actual_seat_of_same_chair',left='C',right='S'),False)
for dimension,target,prop in [('pose','C','prop.orientation'),('role','S','prop.state.disturbed'),('timing','S','trace.recent_disturbance'),('role','C','prop.state.disturbed'),('timing','C','trace.recent_disturbance')]:
 k=copy.deepcopy(base);k['intent_lock']['semantic_anchors'].append({'dimension':dimension,'target':target,'property':prop});check('actual_property_lock_'+str((dimension,target,prop)),k,False)
for dimension in ['pose','role','timing']:
 k=copy.deepcopy(base);k['intent_lock']['open_dimensions'].remove(dimension);k['intent_lock']['locked_dimensions'].append(dimension);check('whole_dimension_lock_'+dimension,k,False)
ct=contract('object',['visual_structure']);ct['intent_constraints']['no_people']=True
check('explicit_no_people_routing_tag_retained',base,False,extra={'intent_constraints':ct['intent_constraints']})
modules=namespace['modules']();modules.pop('prompt_generator',None)
for name,mod in sys.modules.copy().items():
 if name.startswith('photo_') and getattr(mod,'__file__',None):assert Path(mod.__file__).resolve().is_relative_to(GEN),(name,mod.__file__)
report={'schema':'photo-root-entry-domain-override-check/v1','unit_tests':result.testsRun,'unit_failures':len(result.failures),'unit_errors':len(result.errors),'actual_bounded_source_candidate_id':cid,'batch_sha256':c.digest(json.loads((O/'BATCH.json').read_bytes())),'working_prompt_sha256':hashlib.sha256(prompt.read_bytes()).hexdigest(),'dependency_generation':str(GEN),'dependency_modules':modules,'full_compact_actual_source_oldbinding_checks':runs,'new_source_approval':False,'operating_qualified':0,'inference_and_Gemini_calls':0,'actual_runtime_request_or_pixels':False}
out=R/'ROOT-ENTRY-DOMAIN-OVERRIDE-CHECK-01.json';assert not out.exists();out.write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print('PASS',result.testsRun,'unit tests',len(runs),'actual full/compact checks',report['working_prompt_sha256'])
