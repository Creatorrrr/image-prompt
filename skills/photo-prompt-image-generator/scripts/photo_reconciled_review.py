"""Run the maintained review boundary with an original run's sealed audits.

Historical sealed code remains untouched. The maintained review adds explicit
native-reconciliation evidence checking before invoking its bound audit.
"""
import argparse, importlib.util, json, sys
from pathlib import Path

p=argparse.ArgumentParser();p.add_argument('command',choices=('shape','audit'));p.add_argument('--run',type=Path,required=True);p.add_argument('--image',type=Path);p.add_argument('--visual-review',type=Path);p.add_argument('--generic-review',type=Path);p.add_argument('--baseline-available',choices=('yes','no'))
a=p.parse_args(); meta=json.loads((a.run/'workflow.json').read_bytes()); binding=meta.get('h_f2_binding') or {}
from photo_installed_h_f2 import release
import photo_native_preview_reconcile
native,manifest,_=release(Path(binding['store']),binding['generation_id'])
if manifest['native_generation_id'] != meta['source_binding']['generation_id']:raise ValueError('native_generation_mismatch')
sys.path.insert(0,str(native/'scripts'))
import photo_workflow_worker
path=Path(__file__).resolve().with_name('photo_workflow_reviews.py')
spec=importlib.util.spec_from_file_location('maintained_reconciled_review',path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
try:
 out=mod.review_shape(a) if a.command=='shape' else mod.review_audit(a)
 print(json.dumps(out,ensure_ascii=False))
except (ValueError,OSError,KeyError,TypeError) as err:
 print(json.dumps({'status':'error','code':str(err)},ensure_ascii=False),file=sys.stderr);raise SystemExit(2)
