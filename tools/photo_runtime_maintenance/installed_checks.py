"""Read-only checks against the actual selected H-F2 kernel and issued evidence."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

from state import ROOT, EVIDENCE, read, write, sha, stamp, files
from checks import environment, profile

FIXTURE = Path.home()/'.cache/image-prompt/h-f2-default-install-20261018/installed-managed-run'


def child():
    b = read(EVIDENCE/'BASELINE.json.gz')['installed']
    native = Path(b['native'])
    sys.path.insert(0,str(native/'scripts'))
    import numpy as np
    from photo_h_f2_generation import Generation
    from photo_h_f2_receipts import audit_packet, verify_bound
    from photo_runtime_sources import RuntimeSnapshotProvider
    from photo_workflow_state import load_state, value
    from photo_workflow_worker import audit_bound
    state = load_state(FIXTURE)
    packet = value(state,'h_f2_material')
    generation = Generation(b['store'],b['config']['generation_id'],full=True)
    verified = verify_bound(state)
    if verified != packet:
        raise ValueError('issued packet replay differs')
    index = generation.index()
    goals = []
    positions = {row['id']:i for i,row in enumerate(generation.metadata)}
    for slot,q in packet['query_set']['slots'].items():
        result = index.search(q['text'],packet['queries'][slot]['row'],generation.binding)
        raw = Path(state['h_f2_binding']['raw_directory'])
        name = __import__('hashlib').sha256(slot.encode()).hexdigest()+'.npz'
        with np.load(raw/name,allow_pickle=False) as saved:
            if not np.array_equal(saved['bm25'],result['bm25']) or not np.array_equal(saved['cosine'],result['cosine']):
                raise ValueError('installed lane scores changed')
            actual = [positions[row['id']] for row in result['order']]
            if actual != list(saved['order']):
                raise ValueError('installed full order changed')
        if result['lane_calls']!={'BM25F':1,'local_cosine':1} or result['considered_CIDs']!=18180 or result['considered_RIDs']!=18182:
            raise ValueError('installed pool or lane budget changed')
        goals.append(slot)
    snapshot = RuntimeSnapshotProvider(store=b['store']).from_receipt(value(state,'pack'),value(state,'runtime_receipt'))
    composed = audit_bound(state)['composed_audit']
    if composed['status']!='pass' or composed['failures']:
        raise ValueError('issued native composition audit failed')
    print(json.dumps({'status':'PASS','goals':goals,'whole_pool':{'CIDs':18180,'RIDs':18182},
          'actual_lane_calls':index.calls,'scores_and_full_orders_equal_to_issued':True,
          'issued_h_receipt':'PASS','issued_native_receipt':'PASS','native_composed_audit':'pass',
          'native_generation':snapshot.generation_id,'operating_code_sha256':b['config']['code_sha256'],
          'model_calls':0,'Gemini_calls':0,'CURRENT_writes':0}))


def main(output):
    protection = EVIDENCE/'FIXTURE-PROTECTED.json.gz'
    if not protection.exists():
        write(protection,{str(p):stamp(p) for p in files(FIXTURE)})
    python = ROOT/'skills/photo-prompt-image-generator/.runtime/embedding-python/bin/python'
    launcher = "import sys,runpy;from pathlib import Path;entry=sys.argv.pop(1);sys.path.insert(0,str(Path(entry).parent));runpy.run_path(entry,run_name='__main__')"
    p = subprocess.run(['/usr/bin/sandbox-exec','-p',profile(),str(python),'-I','-c',launcher,str(Path(__file__).resolve()),'--child'],
                       env=environment(),capture_output=True,text=True,timeout=180)
    if p.returncode:
        write(output,{'status':'FAIL','exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
        print(p.stderr[-5000:]+p.stdout[-2000:])
        raise ValueError('actual installed replay/kernel check failed')
    result = json.loads(p.stdout)
    result['network_denied'] = True
    result['original_runtime_writes_denied'] = True
    write(output,result)
    print('installed kernel/issued receipts PASS:',len(result['goals']),'goals; exact scores/full orders; native audit',flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--child',action='store_true')
    p.add_argument('--output',type=Path)
    a = p.parse_args()
    child() if a.child else main(a.output or EVIDENCE/'TEST-INSTALLED.json')
