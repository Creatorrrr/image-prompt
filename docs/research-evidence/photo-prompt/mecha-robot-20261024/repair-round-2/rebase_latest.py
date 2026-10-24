"""Reseal the exact new data union against a concurrently advanced current kernel."""
from pathlib import Path
import gc, json, sys, shutil, hashlib
gc.disable()
O=Path(__file__).resolve().parent
ROOT=Path('/Users/chasoik/Projects/image-prompt')
S=ROOT/'skills/photo-prompt-image-generator'
read=lambda p:json.loads(p.read_bytes())
old=read(O/'before.json'); current=read(S/'retrieval-runtime.json')
store=Path(old['store']); native=store/'generations'/current['native_generation_id']
first=read(O/'successor.json'); stage=O/'successor-skill'; out=O/'rebase-1'
out.mkdir(exist_ok=True)
before={'config':current,'store':str(store),'native':str(native),'h_f2':str(store/'h-f2-generations'/current['generation_id'])}
(out/'before.json').write_text(json.dumps(before,indent=2)+'\n')
assert current != old['config'], 'No rebase required.'
# This rebase is admissible only because all baseline candidate/source assets are byte-identical.
prior=Path(old['native'])
original={str(p.relative_to(prior/'assets')):hashlib.sha256(p.read_bytes()).hexdigest() for p in (prior/'assets').rglob('*') if p.is_file()}
latest={str(p.relative_to(native/'assets')):hashlib.sha256(p.read_bytes()).hexdigest() for p in (native/'assets').rglob('*') if p.is_file()}
assert original==latest, 'Concurrent source data changed: require a complete source union rebuild.'
manifest=read(native/'manifest.json'); changes=[]
for rel, sha in manifest['source']['code'].items():
 src=native/rel; dst=stage/rel
 assert hashlib.sha256(src.read_bytes()).hexdigest()==sha
 if not dst.exists() or dst.read_bytes()!=src.read_bytes():changes.append(rel)
 dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
sys.path.insert(0,str(stage/'scripts'))
from photo_runtime_sources import SnapshotPublisher
from photo_h_f2_generation import stage as seal
import photo_candidate_corpus as corpus
base=corpus.load(native/'assets'); merged=corpus.load(stage/'assets')
assert all(merged['candidates'][k]==v for k,v in base['candidates'].items())
assert set(merged['candidates'])-set(base['candidates'])==set(read(O/'new-native-records.json'))
assert all(merged['slot_bindings'][k]==v for k,v in base['slot_bindings'].items())
publication=SnapshotPublisher(stage,O/'successor-store').stage()
print('latest native staged',publication['generation_id'],flush=True)
g=Path(first['store'])/'h-f2-generations'/first['generation_id']
binding=read(g/'manifest.json')['binding']
inputs={'generation':str(g),'documents':str(g/'documents.json.gz'),'field_documents':str(g/'field-documents.json.gz'),'fields':str(g/'fields.json.gz'),'proofs':str(g/'document-proofs.json.gz'),'vectors':str(g/'vectors.f64'),'binding':binding,'native_generation_id':publication['generation_id']}
gid=seal(O/'successor-store',inputs)
result={**first,'generation_id':gid,'native_generation_id':publication['generation_id'],'latest_code_overlay_members':changes,'latest_code_already_present_in_current_default':True,'rebased_from':first['generation_id'],'baseline_assets_byte_identical':True,'reembedded_documents':0,'code_sha256':current['code_sha256']}
(out/'successor.json').write_text(json.dumps(result,indent=2)+'\n')
(out/'source-union-validation.json').write_text(json.dumps({'status':'pass','all_current_baseline_records_preserved':True,'all_current_baseline_bindings_preserved':True,'baseline_assets_byte_identical':True,'new_records':len(read(O/'new-native-records.json')),'kernel_from_current_default':current['code_sha256'],'kernel_code_authored':False,'CURRENT_writes':0},indent=2)+'\n')
print(json.dumps(result),flush=True)
