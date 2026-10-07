#!/usr/bin/env python3
"""Merge only this task's additive authored fields into the dirty primary."""
import hashlib,json,shutil,sys,datetime
from pathlib import Path

WORK=Path(__file__).resolve().parents[4]
PRIMARY=Path('/Users/chasoik/Projects/image-prompt')
SKILL='skills/photo-prompt-image-generator'
OUT=PRIMARY/SKILL/'data/runs/vel-alternatives-integration-20261007/primary_adoption'
EVIDENCE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def unique(a):return list(dict.fromkeys(a))

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 if (OUT/'AUTHORED-MERGE.json').exists():raise RuntimeError('already applied; inspect the saved merge instead of repeating it')
 record=read(EVIDENCE/'ADOPTION.json');summary=read(EVIDENCE/'IMPLEMENTATION-SUMMARY.json')
 targets=set(summary['changed_profile_files'])|{'photo_prompt_source_manifest.json'}
 before={f:read(PRIMARY/SKILL/'assets'/f) for f in targets}
 hashes={f:sha(PRIMARY/SKILL/'assets'/f) for f in targets}
 for f in targets:
  (OUT/'backup/assets').mkdir(parents=True,exist_ok=True)
  shutil.copy2(PRIMARY/SKILL/'assets'/f,OUT/'backup/assets'/f)
 after=json.loads(json.dumps(before))
 for row in record['existing_profile_delta']:
  p=next(p for p in after[row['file']]['profiles'] if p['id']==row['profile_id'])
  source=next(p for p in read(WORK/SKILL/'assets'/row['file'])['profiles'] if p['id']==row['profile_id'])
  if p['semantics']['definition']!=source['semantics']['definition']:
   raise RuntimeError('definition changed concurrently; review before adding alternatives: '+row['profile_id'])
  p['semantics']['paraphrase_examples']=unique(p['semantics']['paraphrase_examples']+row['paraphrases'])
  p['concept_candidate']['concept_terms']=unique(p['concept_candidate']['concept_terms']+row['paraphrases'])
 manifest=after['photo_prompt_source_manifest.json']
 additions=[]
 for f,kind in zip(summary['new_files'],['candidate','visual_profile']):
  if (PRIMARY/SKILL/'assets'/f).exists():raise RuntimeError('new authored file already exists: '+f)
  if any(r['file']==f for r in manifest['sources']):raise RuntimeError('already registered: '+f)
  r={'file':f,'kind':kind,'required':True,'load_order':max(r['load_order'] for r in manifest['sources'] if r['kind']==kind)+1}
  manifest['sources'].append(r);additions.append(r)
 # Cooperative revision keeps live requests from reading a half-written source.
 sys.path.insert(0,str(PRIMARY/SKILL/'scripts'))
 from photo_runtime_sources import source_update
 with source_update(PRIMARY/SKILL):
  if any(sha(PRIMARY/SKILL/'assets'/f)!=hashes[f] for f in targets):raise RuntimeError('primary changed during review; no merge applied')
  for f in summary['new_files']:shutil.copy2(WORK/SKILL/'assets'/f,PRIMARY/SKILL/'assets'/f)
  dest=PRIMARY/'docs/research-evidence/photo-prompt/extension-maintenance/vel-alternatives-20261007.json'
  if dest.exists():raise RuntimeError('maintenance record already exists')
  shutil.copy2(WORK/'docs/research-evidence/photo-prompt/extension-maintenance/vel-alternatives-20261007.json',dest)
  for f,d in after.items():write(PRIMARY/SKILL/'assets'/f,d)
 # Remove only owned additions from the new JSON views and verify prior semantics.
 restored=json.loads(json.dumps(after))
 for row in record['existing_profile_delta']:
  original=next(p for p in before[row['file']]['profiles'] if p['id']==row['profile_id'])
  current=next(p for p in restored[row['file']]['profiles'] if p['id']==row['profile_id'])
  current['semantics']['paraphrase_examples']=original['semantics']['paraphrase_examples']
  current['concept_candidate']['concept_terms']=original['concept_candidate']['concept_terms']
 restored['photo_prompt_source_manifest.json']['sources']=before['photo_prompt_source_manifest.json']['sources']
 assert restored==before,'unexpected non-owned authored-data mutation'
 result={'status':'PASS_ADDITIVE_AUTHORED_MERGE','captured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'before_sha256':hashes,'after_sha256':{f:sha(PRIMARY/SKILL/'assets'/f) for f in targets},'manifest_additions':additions,'existing_profile_ids':[r['profile_id'] for r in record['existing_profile_delta']],'all_prior_authored_json_preserved':True,'generated_indexes':'pending rebuild from combined primary data'}
 write(OUT/'AUTHORED-MERGE.json',result)
 print(json.dumps({'status':result['status'],'prior_authored_json_preserved':True,'primary_manifest_additions':additions},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
