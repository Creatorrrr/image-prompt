import datetime, json, os, subprocess
from pathlib import Path

def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(name, value): Path('output/' + name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
regions = []
def patch(name, source, render, role, zone):
    regions.append({'name': name, 'source_bounds': source, 'comparison_bounds': render,
                    'semantic_role': role, 'tone_zone': zone,
                    'purpose': 'intrinsic-displayed-color' if role == 'target' else 'global-cast-and-exposure'})
patch('tank-midtone-a', [.43,.46,.49,.485], [.445,.487,.49,.51], 'target', 'midtone')
patch('tank-midtone-b', [.50,.52,.55,.54], [.50,.535,.55,.555], 'target', 'midtone')
patch('tank-midtone-c', [.57,.565,.61,.585], [.57,.57,.61,.59], 'target', 'midtone')
patch('cardigan-midtone-a', [.77,.425,.805,.455], [.82,.375,.85,.405], 'target', 'midtone')
patch('cardigan-midtone-b', [.797,.515,.827,.54], [.865,.445,.895,.47], 'target', 'midtone')
patch('shorts-midtone-a', [.585,.75,.615,.77], [.455,.735,.48,.755], 'target', 'midtone')
patch('shorts-midtone-b', [.74,.77,.78,.79], [.655,.75,.68,.77], 'target', 'midtone')
patch('wall-context-a', [.02,.25,.09,.29], [.04,.31,.11,.35], 'context', 'flat')
patch('wall-context-b', [.10,.01,.22,.04], [.04,.01,.16,.04], 'context', 'flat')
patch('right-context-a', [.92,.02,.98,.12], [.84,.02,.95,.12], 'context', 'shadow')
patch('right-context-b', [.97,.30,.99,.35], [.97,.20,.99,.27], 'context', 'shadow')
groups=[]
for name, peers, role, zone in [
    ('tank-midtone', ['tank-midtone-a','tank-midtone-b','tank-midtone-c'], 'target','midtone'),
    ('cardigan-midtone', ['cardigan-midtone-a','cardigan-midtone-b'], 'target','midtone'),
    ('shorts-midtone', ['shorts-midtone-a','shorts-midtone-b'], 'target','midtone'),
    ('left-wall-context', ['wall-context-a','wall-context-b'], 'context','flat'),
    ('right-context', ['right-context-a','right-context-b'], 'context','shadow')]:
    groups.append({'name':name,'region_names':peers,'semantic_role':role,'tone_zone':zone,
                   'purpose':'intrinsic-displayed-color' if role=='target' else 'global-cast-and-exposure'})
save('color-sampling-spec.json', {'selected_utc': now(), 'selection':'Analyst manually selected source and render coordinates independently after inspecting delivered pixels; no automatic class detection.',
    'limitations':'Small displayed-color patches; garment fold and knit response may differ. Both files lack embedded ICC profiles; assumed display space only. No calibrated reference or justified acceptance tolerance.',
    'regions':regions,'groups':groups})
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
def run(label, args):
    start=now();r=subprocess.run(['/opt/homebrew/anaconda3/bin/python3',*args],capture_output=True,text=True,env=env)
    save(label+'-execution.json',{'started_utc':start,'ended_utc':now(),'argv':args,'exit_code':r.returncode,'stderr':r.stderr})
    Path('output/'+label+'.json').write_text(r.stdout)
    if r.returncode: raise SystemExit(label+' failed: '+r.stdout+r.stderr)
    return json.loads(r.stdout)
probe=run('color-probe', ['skill-v3/tools/color_probe.py','source.jpg','--spec','output/color-sampling-spec.json','--compare','output/render.png'])
evaluation=run('color-evaluation', ['skill-v3/tools/color_fidelity_eval.py','output/color-probe.json'])
print(json.dumps(evaluation,ensure_ascii=False))
