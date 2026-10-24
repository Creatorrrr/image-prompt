"""Rebase only this extension when another qualified default wins the CAS.

Every attempt uses the unchanged native/H-F2 builders, full installer validators
and compare-before-select guard. No other candidate record is overwritten.
"""
from pathlib import Path
import json,subprocess,sys,shutil,datetime
ROOT=Path('/Users/chasoik/Projects/image-prompt');O=Path(__file__).resolve().parent;S=ROOT/'skills/photo-prompt-image-generator';STORE=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/h-f2-installed')
read=lambda p:json.loads(p.read_bytes())
write=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
for attempt in range(1,9):
 config=read(S/'retrieval-runtime.json');n=STORE/'generations'/config['native_generation_id']
 assert config['code_sha256']=='ec29f441dbfc26930e7f4fb71ced759bf5ae271e672176110b21d2a7f6c846ef','Kernel changed; inspect before another publication'
 modules=read(n/'assets/photo_candidate_corpus_manifest.json')['modules'];assert not any(m['file']=='photo_candidate_estate_management_20261024.json' for m in modules),'Estate already present in newer default; qualify that release instead of replacing it'
 folder=O/('current-default-successor-'+config['generation_id'][:8]);assert not folder.exists(),'Do not overwrite an earlier attempt'
 folder.mkdir();cache=Path('/Users/chasoik/.cache/image-prompt/estate-management-20261024')/folder.name;cache.mkdir()
 for fn in ('build_release.py','install_release.py','probe_runtime.py','new-native-records.json','changed-native-records.json','new-bindings.json','card-candidate-map.json'):shutil.copyfile(O/fn,folder/fn)
 subprocess.run(['/bin/cp','-cR',str(n),str(cache/'successor-skill')],check=True)
 for p in (cache/'successor-skill').rglob('*'):
  if p.is_file() and not p.is_symlink():p.chmod(p.stat().st_mode|0o200)
 write(folder/'before.json',{'config':config,'store':str(STORE),'native':str(n),'build_cache':str(cache),'reason':'Preserve all currently selected qualified source records and add only the exact estate delta.'})
 prior=read(O/'DEFAULT-PUBLICATION-TARGET.json');prior_folder=Path(prior['folder'])
 if not (prior_folder/'SUPERSEDED.json').exists():write(prior_folder/'SUPERSEDED.json',{'reason':'Default advanced before selection; this earlier build never selected a default.','latest_config':config,'CURRENT_writes':0,'default_selected':False,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
 write(O/'DEFAULT-PUBLICATION-TARGET.json',{'folder':str(folder),'baseline_config':config,'status':'building_latest_default_successor'})
 print(json.dumps({'attempt':attempt,'baseline':config['generation_id'],'folder':str(folder)}),flush=True)
 subprocess.run([sys.executable,str(folder/'build_release.py')],check=True)
 install=subprocess.run([sys.executable,str(folder/'install_release.py'),'--activate'])
 if install.returncode:
  if read(S/'retrieval-runtime.json')!=config:
   print('A newer default won the guard; preserving it and rebasing the estate-only delta.',flush=True);continue
  raise RuntimeError('Installation failed without default drift; inspect the validation failure')
 subprocess.run([sys.executable,str(folder/'probe_runtime.py')],check=True)
 release=read(folder/'successor.json')
 assert read(S/'retrieval-runtime.json')['generation_id']==release['generation_id'],'Default changed after selection; inspect inclusion before further work'
 print('FINAL_CURRENT_DEFAULT_PUBLICATION_PASS',flush=True)
 break
else:raise RuntimeError('Eight newer qualified releases advanced consecutively; preserve all and reassess')
