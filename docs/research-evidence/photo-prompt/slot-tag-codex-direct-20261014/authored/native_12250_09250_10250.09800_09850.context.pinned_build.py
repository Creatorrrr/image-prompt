"""Fresh-process, frozen-publication prototype checks; no formal proof or approval."""
import sys,hashlib,json,runpy
from pathlib import Path
G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/188c56270ebc2c973defd3307d8fa43df60e55701baa30c45367a4e2e3efe2bb')
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_semantic_evidence as native,photo_candidate_corpus as corpus,photo_precore_bridge as bridge
modules={}
for m in [native,corpus,bridge]:
 p=Path(m.__file__).resolve();assert p.is_relative_to(G);modules[m.__name__]=dict(file=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
assert modules['photo_semantic_evidence']['sha256']=='6833e00c03ee4aa1222ea1a9e7c5304d8a98d62ad1d3d0e3ff6a3d666bb313e9'
x=runpy.run_path(str(Path(__file__).with_name('native_12250_09250_10250.09800_09850.build.py')))
assert x['n'] is native and x['d'].c is corpus and x['nr'].native is native
meta=dict(schema='photo-worker-pinned-prototype-module-boundary/v1',generation=str(G),module_paths_and_raw_sha256=modules,research_helpers={name:dict(file=str(Path(m.__file__).resolve()),sha256=hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest()) for name,m in [('direct_review',x['d']),('native_reviews',x['nr'])]},checked_interval=x['doc']['complete_interval'],formal_signature_count=0,whole_primary_sourceunit_proof=False)
Path(__file__).with_suffix('.modules.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print('PINNED_PROTOTYPE',json.dumps(meta))
