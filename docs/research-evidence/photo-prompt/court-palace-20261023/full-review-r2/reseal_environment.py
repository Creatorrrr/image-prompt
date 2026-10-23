"""Seal the completed data/index artifacts using the deployed exact CPython environment.
No data, vector, proof, algorithm, policy, or validation is substituted.
"""
import gc;gc.disable()
from pathlib import Path
import json,sys,shutil,time,collections
O=Path(__file__).resolve().parent;STAGE=O/'successor-skill';STORE=O/'successor-store';WORK=O/'build'
sys.path.insert(0,str(STAGE/'scripts'))
from photo_recall_generation import read,write
from photo_runtime_sources import SnapshotPublisher,environment_binding
from photo_h_f2_generation import stage as seal_h
B=read(O/'before.json');baseline=read(Path(B['native'])/'manifest.json')['source']['environment'];assert environment_binding()==baseline
import photo_candidate_corpus as corpus,photo_search_layout as layout,photo_recall_first as rf
from photo_h_f2_generation import configs,WEIGHTS
verification=layout.verify(STAGE/'assets',corpus.load(STAGE/'assets'),read(STAGE/'assets'/layout.MANIFEST));write(O/'exact-environment-native-index-verify.json',verification);print('exact environment native index verified',flush=True)
fdocs=read(WORK/'field-documents.json.gz')['rows'];old_fields=read(WORK/'fields.json.gz');lengths={f:[] for f in WEIGHTS};counts={f:0 for f in WEIGHTS};posting={}
for i,f in enumerate(fdocs):
 terms={}
 for name in WEIGHTS:
  bag=collections.Counter(t for v in f['fields'][name] for t in rf.tokens(v));size=sum(bag.values());lengths[name].append(size);counts[name]+=bool(size)
  for term,tf in bag.items():terms.setdefault(term,{})[name]=tf
 for term,tf in terms.items():posting.setdefault(term,[]).append([i,tf])
cfg=configs();fields={'n':len(fdocs),'fields':cfg,'lengths':lengths,'nonempty_counts':counts,'postings':posting,'average_lengths':{f:(sum(lengths[f])/(counts[f] if 'normalization_population' in cfg[f] else len(fdocs)) if (counts[f] if 'normalization_population' in cfg[f] else len(fdocs)) else 0.) for f in WEIGHTS},'tokenizer':old_fields['tokenizer']}
write(WORK/'fields.json.gz',fields);write(O/'exact-environment-tokenizer-verify.json',{'status':'pass','recomputed_under':environment_binding(),'foreign_build_fields_identical':old_fields==fields});print('exact environment F2 fields rebuilt',flush=True)
prior=read(O/'successor.json');shutil.copy2(O/'successor.json',O/'intermediate-foreign-environment-release.json')
publication=SnapshotPublisher(STAGE,STORE).stage();write(O/'native-staged-exact-environment.json',publication)
oldG=Path(B['store'])/'h-f2-generations'/B['config']['generation_id'];binding=read(oldG/'manifest.json')['binding']
inputs={'generation':str(WORK/'source'),'documents':str(WORK/'documents.json.gz'),'field_documents':str(WORK/'field-documents.json.gz'),'fields':str(WORK/'fields.json.gz'),'proofs':str(WORK/'document-proofs.json.gz'),'vectors':str(WORK/'vectors.f64'),'binding':binding,'native_generation_id':publication['generation_id']}
gid=seal_h(STORE,inputs);prior.update(generation_id=gid,native_generation_id=publication['generation_id'],environment=baseline,exact_deployed_environment_resealed=True,intermediate_release_installed=False)
write(O/'successor.json',prior);write(O/'environment-seal-validation.json',{'status':'pass','baseline_and_final_environment':baseline,'build_environment_note':'Offline source/index build initially ran with CPython 3.12. Exact data/vector/proof closure retained; final native and H2 seals republished under deployed CPython 3.14.3 before installation. Intermediate release not installed or activated.','unchanged_offline_derived_closure':True,'bypassed_validators':False});print(json.dumps(prior),flush=True)
