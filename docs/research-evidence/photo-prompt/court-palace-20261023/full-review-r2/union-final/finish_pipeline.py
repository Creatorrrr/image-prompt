from pathlib import Path
import time,subprocess,json
O=Path(__file__).resolve().parent;py='/opt/homebrew/bin/python3';end=time.monotonic()+1800
while not (O/'successor.json').exists():
 if time.monotonic()>end:raise RuntimeError('union build deadline')
 time.sleep(5)
b=json.loads((O/'before.json').read_text());s=json.loads((O/'successor.json').read_text());source=Path(s['store'])/'generations'/s['native_generation_id'];m=json.loads((source/'manifest.json').read_text());base=json.loads((Path(b['native'])/'manifest.json').read_text());assert m['source']['environment']==base['source']['environment']=={'implementation':'cpython','python':[3,14,3],'unicode':'16.0.0'}
for f in ['install_release.py','qualify_release.py']:
 print('RUN',f,flush=True);subprocess.run([py,str(O/f)],check=True)
root=Path('/Users/chasoik/Projects/image-prompt');current=json.loads((root/'skills/photo-prompt-image-generator/retrieval-runtime.json').read_text())
if current==b['config']:
 print('ACTIVATE CAS',flush=True);subprocess.run([py,str(O/'install_release.py'),'--activate'],check=True)
else:
 (O/'activation-concurrent-change.json').write_text(json.dumps({'status':'not_overwritten','current':current,'base':b['config']},indent=2)+'\n');print('CURRENT advanced; preserve and inspect',flush=True)
print('UNION PIPELINE COMPLETE',flush=True)
