"""Fresh current consumers plus unchanged evidence reuse, no arbitrary API claim."""
import ast,collections,json,sys,textwrap
from pathlib import Path
import run
from history_state import new

ROOT=run.ROOT;targets=collections.defaultdict(set)
for row in run.ROWS:targets[row['module']].add(row['binding'])
functions={};counts=collections.Counter();samples=collections.defaultdict(list);scanned=collections.Counter();failures=[]
resolver=ROOT/'docs/research-evidence/photo-prompt/runtime-remaining-after-seventeen-20261019/review.py'
defs=[n for n in ast.parse(resolver.read_bytes()).body if isinstance(n,ast.FunctionDef) and n.name in {'hit','inspect','scan','references'}]
exec(compile(ast.Module(body=defs,type_ignores=[]),str(resolver),'exec'),globals())
b=run.baseline();old=run.state.read(run.ANALYSIS/'PRESERVATION.json');analyzed=run.state.read(old['baseline_path'])
live=[*(run.SKILL/'scripts').glob('*.py'),*(run.SKILL/'precore').glob('*.py'),*(ROOT/'tests').glob('*.py')]
for p in live:scan(str(p),p.read_bytes(),'live')
changed=[];unchanged=0
for p,row in b['files'].items():
    if Path(p).suffix!='.py' or row['kind']!='file' or Path(p) in live:continue
    prior=analyzed['files'].get(p)
    if prior and prior.get('sha256')==row['sha256']:unchanged+=1;continue
    # Existing analysis/cleanup hypotheses are evidence, not operating consumers.
    kind='analysis_hypothesis' if Path(p).is_relative_to(run.ANALYSIS) else 'new_preserved'
    changed.append({'path':p,'kind':kind});scan(p,Path(p).read_bytes(),kind)
assert not failures,failures
rows=[]
for row in run.ROWS:
    refs=references(row['module']+'.'+row['binding'])
    assert not refs.get('live') and not counts[(row['module']+'.'+row['binding'],'new_preserved')],refs
    rows.append({**row,'fresh_current_references':refs,'new_preserved_named_or_dynamic_references':counts[(row['module']+'.'+row['binding'],'new_preserved')],
        'decision':'QUALIFY_REMOVAL','provider_remains_imported':True})
assert all(run.state.sha(ROOT/r['path'])==r['source_sha256'] for r in run.ROWS)
new(run.E/'REFERENCE-CHECK.json',{'status':'PASS','rows':rows,'fresh_scanned':dict(scanned),'analyzed_preserved_Python_hashes_unchanged':unchanged,
    'new_or_changed_Python':changed,'parse_failures':failures,'prior_inventory_sha256':run.state.sha(run.ANALYSIS/'INVENTORY.json'),
    'known_preserved_reflection_review':'Report prose, whole namespace copying of a function not loading these names, bounded CHARACTER_* checks. No removed provider definitions.',
    'unknown_external_reflection_absence_claimed':False,'Gemini_calls':0,'CURRENT_writes':0})
print('5 reference checks PASS;',len(live),'current Python;',unchanged,'unchanged preserved Python',flush=True)
