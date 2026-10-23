from pathlib import Path
import json,subprocess,time
O=Path(__file__).resolve().parent;S=O.parents[4]/'skills/photo-prompt-image-generator'
started=time.monotonic()
while not (O/'successor.json').is_file():
 if time.monotonic()-started>1800:raise SystemExit('Timed out waiting for qualified source generation; no install attempted')
 time.sleep(5)
release=json.loads((O/'successor.json').read_bytes());base=json.loads((O/'sealed-base.json').read_bytes());current=json.loads((S/'retrieval-runtime.json').read_bytes())
activate=current==base['config']
cmd=[str(S/'.runtime/embedding-python/bin/python'),str(S/'scripts/install_photo_h_f2_runtime.py'),'--source-store',release['store'],'--generation-id',release['generation_id']]
if not activate:cmd.append('--no-activate')
result=subprocess.run(cmd,capture_output=True,text=True)
(O/'install.stdout.log').write_text(result.stdout);(O/'install.stderr.log').write_text(result.stderr)
if result.returncode:raise SystemExit(result.returncode)
report=json.loads(result.stdout);report['default_activation_requested']=activate;report['base_config_matched_at_start']=activate
(O/'install-result.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report),flush=True)
