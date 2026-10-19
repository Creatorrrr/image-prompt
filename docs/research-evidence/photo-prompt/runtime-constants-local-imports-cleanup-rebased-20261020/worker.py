"""Changed-source contract runner, with active guard and algorithm checks."""
import ast,hashlib,importlib,inspect,json,os,sys,unittest
from pathlib import Path
project=Path(sys.argv[1]).resolve();removed=sys.argv[2]=='1';config=json.loads((Path(__file__).parent/'TARGETS.json').read_bytes())
os.chdir(project);skill=project/'skills/photo-prompt-image-generator';sys.path[:0]=[str(project),str(skill/'scripts'),str(skill/'precore')]
order=['prompt_generator','audit_composed_prompt','photo_runtime_sources','photo_contextual_appeal','compose_pack_view','photo_candidate_realizations','photo_candidate_semantics','photo_native_permission','photo_workflow','photo_contracts','photo_authoring_wire']
mods={name:importlib.import_module(name) for name in order}
for row in config['constants']:assert hasattr(mods[row['module']],row['name'])!=removed,row
for row in config['local_imports']:
    tree=ast.parse(Path(mods[row['module']].__file__).read_bytes());fn=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name==row['owner'])
    present=any(isinstance(n,(ast.Import,ast.ImportFrom)) and any((a.asname or a.name.split('.')[0])==row['binding'] for a in n.names) for n in ast.walk(fn));assert present!=removed,row
loaded={}
for name,m in mods.items():
    path=Path(m.__file__).resolve();assert path.is_relative_to(project),path
    loaded[name]={'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
g=mods['prompt_generator'];runtime=mods['photo_runtime_sources'];permission=mods['photo_native_permission'];ctx=mods['photo_contextual_appeal']
assert len(runtime.LOADED_CODE)==76
values=[runtime.algorithm_binding(x) for x in (g,None,{})];assert all(v==values[0] for v in values)
runtime._require_implementation({'code':runtime.LOADED_CODE,'environment':runtime.LOADED_ENVIRONMENT},None)
try:runtime._require_implementation({'code':{**runtime.LOADED_CODE,'scripts/foreign.py':'bad'},'environment':runtime.LOADED_ENVIRONMENT},None)
except runtime.FreshnessError:pass
else:raise AssertionError('implementation guard weakened')
assert g.candidate_pack_contract_version('v9')=='photo-candidate-pack/v10'
assert g.character_response_relation_signature({'operator':'contrasts','left':'baseline','right':'visible_response'})
assert permission.validate_declaration({'content':{}},{}) is None
assert permission.enforce({'nodes':[],'entries':{}},[],{}) is None
assert ctx.allowed_dimensions({'open_dimensions':[],'locked_dimensions':[]})==set(ctx.DIMENSIONS)
for name in ('CHARACTER_RESPONSE_RELATION_MEMBERS','CHARACTER_RESPONSE_REQUIRED_AXES','CHARACTER_RESPONSE_REQUIRED_EVIDENCE'):
    assert getattr(mods['photo_contracts'],name)==getattr(mods['photo_authoring_wire'],name)==getattr(mods['audit_composed_prompt'],name)
result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(sys.argv[3:]))
print(json.dumps({'status':'PASS' if result.wasSuccessful() and not result.skipped else 'FAIL','tests':result.testsRun,'skipped':len(result.skipped),
    'loaded_modules':loaded,'code_files':len(runtime.LOADED_CODE),'implementation_guard_preserved':True,
    'algorithm_without_code':{k:v for k,v in values[0].items() if k!='code'},'algorithm_binding_signature':str(inspect.signature(runtime.algorithm_binding)),
    'active_contract_checks':{'provider_constants':True,'permission':True,'allowed_dimensions':True,'relation_signature':True,'v9_alias':True},
    'failures':[(t.id(),x.replace(str(project),'<project>')) for t,x in result.failures],'errors':[(t.id(),x.replace(str(project),'<project>')) for t,x in result.errors]}))
sys.exit(not result.wasSuccessful() or bool(result.skipped))
