"""Fresh live consumer and local-scope check, with preserved-reference disclosure."""
import ast,collections,json,sys,textwrap
from pathlib import Path
import run
from history_state import new
ROOT=run.ROOT;E=run.E;skill=run.SKILL
counts=collections.Counter();samples=collections.defaultdict(list);scanned=collections.Counter();failures=[];functions={};targets=collections.defaultdict(set)
for r in run.CONSTANTS:targets[r['module']].add(r['name'])
resolver=ROOT/'docs/research-evidence/photo-prompt/runtime-remaining-after-seventeen-20261019/review.py'
selected=[n for n in ast.parse(resolver.read_bytes()).body if isinstance(n,ast.FunctionDef) and n.name in {'hit','inspect','scan','references'}]
exec(compile(ast.Module(body=selected,type_ignores=[]),str(resolver),'exec'),globals())
paths=[*(skill/'scripts').glob('*.py'),*(skill/'precore').glob('*.py'),*(ROOT/'tests').glob('*.py')]
for p in paths:scan(str(p),p.read_bytes(),'live')
rows=[]
for row in run.CONSTANTS:
    t=ast.parse((ROOT/row['path']).read_bytes());loads=[n.lineno for n in ast.walk(t) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load) and n.id==row['name']]
    consumers=[r for r in samples[(row['module']+'.'+row['name'],'live')] if r.get('requested','named') is not None]
    assert not loads and not consumers,(row['name'],loads,consumers)
    rows.append({'name':row['name'],'module':row['module'],'local_loads':loads,'current_named_consumers':consumers,
        'preserved_references_kept':row['references']})
for row in run.IMPORTS:
    t=ast.parse((ROOT/row['path']).read_bytes());fn=next(n for n in ast.walk(t) if isinstance(n,ast.FunctionDef) and n.name==row['owner'])
    assert not any(isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load) and n.id==row['binding'] for n in ast.walk(fn))
# This historical comparison snapshots vars(auditor), then executes a specific HEAD function.
# Its actual free-name loads do not refer to the removed tables; all callable code is retained.
historical=ROOT/'docs/research-evidence/photo-prompt/restrained-divinity-run-review-20261015/verify.py'
source=run.state.git(ROOT,'show','HEAD:skills/photo-prompt-image-generator/scripts/audit_composed_prompt.py')
fn=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='audit_adult_appeal_dimension_scope')
removed={r['name'] for r in run.CONSTANTS if r['module']=='audit_composed_prompt'}
assert not removed&{n.id for n in ast.walk(fn) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load)}
new(E/'REFERENCE-CHECK.json',{'status':'PASS','scanned':dict(scanned),'parse_failures':failures,'constants':rows,'local_imports_no_local_load':6,
 'historical_namespace_comparison':{'path':str(historical),'sha256':run.state.sha(historical),'HEAD_function_removed_name_loads':[],
 'all_nontarget_AST_unchanged_gate':'TARGETS.json'},'analysis_inventory_sha256':run.state.sha(E/'INPUT-INVENTORY.json'),
 'unknown_external_reflection_absence_claimed':False,'frozen_implementations_untouched':True,'Gemini_calls':0,'CURRENT_writes':0})
print('fresh consumer checks PASS:',len(rows),'constants, 6 function-local imports;',dict(scanned),flush=True)
