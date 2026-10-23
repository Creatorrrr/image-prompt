from pathlib import Path
import time,subprocess,json
O=Path(__file__).resolve().parent;py='/opt/homebrew/bin/python3';end=time.monotonic()+1800
while not (O/'successor.json').exists():
 if time.monotonic()>end:raise RuntimeError('build did not finish before pipeline deadline')
 time.sleep(5)
for file in ['reseal_environment.py','install_release.py','qualify_release.py']:
 print('RUN',file,flush=True);subprocess.run([py,str(O/file)],check=True)
root=Path('/Users/chasoik/Projects/image-prompt');before=json.loads((O/'before.json').read_text());current=json.loads((root/'skills/photo-prompt-image-generator/retrieval-runtime.json').read_text())
if current==before['config']:
 print('ACTIVATE CAS baseline unchanged',flush=True);subprocess.run([py,str(O/'install_release.py'),'--activate'],check=True)
else:
 (O/'activation-concurrent-change.json').write_text(json.dumps({'status':'not_overwritten','current':current,'base':before['config']},indent=2)+'\n');print('CURRENT advanced; union verification or rebase needed',flush=True)
print('PIPELINE COMPLETE',flush=True)
