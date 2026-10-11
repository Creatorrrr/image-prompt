"""Paired full-corpus public CLI evidence from immutable authored fixtures."""
import argparse
import concurrent.futures
import copy
import json
import subprocess
import sys
import time
from pathlib import Path

OUT=Path(__file__).resolve().parent
PYTHON=Path('/Users/chasoik/Projects/image-prompt/.venv/bin/python')


def save(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')


def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--lane',choices=['before','after','primary'],required=True);p.add_argument('--only',action='append');args=p.parse_args()
 skill=args.root/'skills/photo-prompt-image-generator'
 fixtures=args.root/'tests/fixtures/photo_prompt/slot_retrieval_natural_v1'
 frozen=json.loads((OUT/'benchmark-frozen.json').read_text())
 store=OUT/(args.lane+'-runtime-store');dest=OUT/args.lane;dest.mkdir(exist_ok=True)
 selected=[row for row in frozen if not args.only or row['key'] in args.only]
 summary_path=OUT/(args.lane+'-benchmark.json')
 results=[row for row in json.loads(summary_path.read_text()) if row['key'] not in args.only] if args.only and summary_path.exists() else []
 sys.path.insert(0,str(skill/'scripts'))
 import audit_composed_prompt as audit
 from photo_runtime_sources import RuntimeSnapshotProvider
 # Explicit maintenance bootstrap after all core freezes; it prevents two
 # first-use CLI publishers racing on a previously empty evidence store.
 snapshot=RuntimeSnapshotProvider(skill,store).acquire()
 def run(row):
  start=time.monotonic();directory=dest/row['key'];directory.mkdir(exist_ok=True)
  values=json.loads((fixtures/row['key']/'fixture.json').read_text())
  for name,source in [('request-envelope','request_envelope_input'),('authorial-core','authorial_core_input'),('creative-controls','creative_controls'),('embodiment-review','embodiment_review')]:save(directory/(name+'.json'),values[source])
  command=[str(PYTHON),str(skill/'scripts/generate_photo_prompt.py')]
  for name in ['request-envelope','authorial-core','creative-controls','embodiment-review']:command.extend(['--'+name+'-json',str(directory/(name+'.json'))])
  command+=['--new-author-camera-evidence','--seed','17','--runtime-store',str(store),'--output-file',str(directory/'candidate-pack.json')]
  if row['key']=='dev-01-rain-portrait-ko':command+=['--require-camera-evidence','direction','--require-camera-evidence','height']
  save(directory/'generate-command.json',command)
  if (directory/'generate.log').exists():
   index=1
   while (directory/('generate-previous-'+str(index)+'.log')).exists():index+=1
   (directory/('generate-previous-'+str(index)+'.log')).write_bytes((directory/'generate.log').read_bytes())
  result=subprocess.run(command,cwd=args.root,capture_output=True,text=True)
  (directory/'generate.log').write_text(result.stdout+result.stderr)
  summary=dict(key=row['key'],split=row['split'],exit_code=result.returncode,occasion_expected=row['occasion_expected'],seconds=round(time.monotonic()-start,2))
  if result.returncode:summary['error']=result.stderr or result.stdout;return summary
  pack=json.loads((directory/'candidate-pack.json').read_text())[0]
  entries=pack.get('slots',{}).get('occasion_context',{}).get('candidates',[])
  summary.update(slot_count=len(pack['slots']),ordinary_count=sum(len(x['candidates']) for x in pack['slots'].values()),
                 occasion_ids=[x['entry_id'] for x in entries],occasion_candidates=entries,
                 slot_ids={slot:[x['entry_id'] for x in info['candidates']] for slot,info in pack['slots'].items()},
                 authorial_core_sha256=pack['authorial_core']['canonical_sha256'])
  view=subprocess.run([str(PYTHON),str(skill/'scripts/compose_pack_view.py'),'--pack',str(directory/'candidate-pack.json'),'--output',str(directory/'composer-view.json')],cwd=args.root,capture_output=True,text=True)
  (directory/'view.log').write_text(view.stdout+view.stderr);summary['view_exit_code']=view.returncode
  return summary
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
  for row in pool.map(run,selected):
   results.append(row);save(OUT/(args.lane+'-benchmark.json'),results)
   print(json.dumps({k:row[k] for k in ['key','exit_code','occasion_ids'] if k in row}),flush=True)
 selected_keys={row['key'] for row in selected}
 for row in results:
  if row['key'] not in selected_keys:continue
  if row['exit_code']:continue
  pack=json.loads((dest/row['key']/'candidate-pack.json').read_text())[0]
  row['generation_id']=snapshot.generation_id
  row['recomputation_issues']=audit.audit_core_retrieval(pack,snapshot.data)
  tampered=copy.deepcopy(pack);slot=next(iter(tampered['slots']));tampered['slots'][slot]['candidates'].pop()
  row['omission_detected']=bool(audit.audit_core_retrieval(tampered,snapshot.data))
 results.sort(key=lambda row:row['key']);save(OUT/(args.lane+'-benchmark.json'),results)
 save(OUT/(args.lane+'-runtime.json'),dict(generation_id=snapshot.generation_id,source_fingerprint=snapshot.manifest['source_fingerprint']))
 failures=[row['key'] for row in results if row['exit_code'] or row.get('view_exit_code') or row.get('recomputation_issues') or not row.get('omission_detected')]
 print(json.dumps({'cases':len(results),'failures':failures,'generation_id':snapshot.generation_id}),flush=True)
 if failures:raise SystemExit(1)


if __name__=='__main__':main()
