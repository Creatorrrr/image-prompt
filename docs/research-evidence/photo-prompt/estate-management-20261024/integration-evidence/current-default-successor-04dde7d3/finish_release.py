"""Select this qualified successor promptly; preserve every baseline/CAS guard."""
import time,sys,subprocess,json
from pathlib import Path
O=Path(__file__).resolve().parent
start=time.monotonic()
while not (O/'successor.json').is_file():
 if time.monotonic()-start>1800: raise TimeoutError('Build did not produce a qualified release in the observation window')
 time.sleep(2)
print('Qualified successor ready; full install validation and unchanged-default CAS starting',flush=True)
result=subprocess.run([sys.executable,str(O/'install_release.py'),'--activate'])
assert result.returncode==0,'Installation did not select the default; inspect output and rebase without replacing newer data'
print('Default activation passed. Running final-generation source and natural-query probes.',flush=True)
result=subprocess.run([sys.executable,str(O/'probe_runtime.py')])
assert result.returncode==0,'Final source/query validation failed'
print('FINISH_RELEASE_PASS',flush=True)
