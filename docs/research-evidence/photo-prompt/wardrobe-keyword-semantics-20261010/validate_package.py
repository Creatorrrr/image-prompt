"""Research-package integrity checks; no runtime, embedding or image calls."""
from pathlib import Path
import collections
import csv
import hashlib
import json
import re
import subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]

def read(name):return json.loads((HERE/name).read_text())
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def unique(rows,key='id'):
 values=[r[key] for r in rows]
 assert len(values)==len(set(values)),f'duplicate {key}'
 return set(values)

def main():
 original=read('inputs/wardrobe_keyword_catalog.json')
 counts=read('RESEARCH-COUNTS.json')
 coverage=read('KEYWORD-COVERAGE.json')['rows']
 cards=read('SEMANTIC-CARDS.json')['cards']
 drafts=read('CANDIDATE-BLUEPRINTS.json')['drafts']
 recipes=read('COMBINATION-ANALYSIS.json')['recipes']
 boundaries=read('CONTEXT-BOUNDARIES.json')['exclusions']
 public=read('SOURCES.json')['sources']
 regressions=read('REGRESSION-PLAN.json')['cases']
 native=read('NATIVE-VALIDATION-PLAN.json')
 keyword_ids=unique(original['keywords']);card_ids=unique(cards);source_ids=unique(public)
 assert len(keyword_ids)==503 and len(original['sources'])==45
 assert len(set(r['category'] for r in original['keywords']))==21
 assert dict(collections.Counter(r['usage_status'] for r in original['keywords']))==original['counts']['usage_status']
 assert unique(coverage)==keyword_ids
 assert len(cards)==125 and len(drafts)==150 and len(recipes)==20 and len(boundaries)==23 and len(public)==26
 assert len(regressions)==48 and len(native['arms'])==8 and native['images_generated']==0
 unique(drafts);unique(recipes);unique(boundaries);unique(regressions);unique(native['arms'])
 for c in cards:
  assert set(c['seed_keyword_ids'])<=keyword_ids
  assert set(c['public_source_ids'])<=source_ids
  assert set(c['catalog_source_ids'])<=set(original['sources'])
  assert c['owner'] and c['counterpart'] and c['relations'] and c['confusion_boundaries_ko']
  assert not c['runtime_ready'] and not c['effects_verified'] and not c['native_pixels_verified']
  if c['suggested_slot'] is None:assert c['pixel_gate_proposal'] is None
 for r in coverage:
  assert r['research_card_ids'] and set(r['research_card_ids'])<=card_ids
  old=next(k for k in original['keywords'] if k['id']==r['id'])
  for k,v in old.items():assert r[k]==v,f'original keyword modified: {r["id"]}.{k}'
  assert r['meaning_support']=='not_inferred' and not r['runtime_verified'] and not r['native_pixels_verified']
 for d in drafts:
  assert d['card_id'] in card_ids and d['concept_units'] and d['affected_properties']
  assert d['candidate_only'] and not d['automatic_hard_activation'] and not d['source_keyword_ids_are_aliases']
  assert not d['runtime_ready'] and not d['effects_verified'] and not d['native_pixels_verified']
 for r in recipes+regressions+native['arms']:
  assert set(r.get('research_card_ids',r.get('card_ids',[])))<=card_ids
 for r in recipes:assert r['always_optional_recipe'] and not r['hard_activation_from_style_label']
 for r in boundaries:assert not r['current_request_default'] and r['source_scope_required']
 for s in public:
  p=HERE/s['evidence_file'];assert p.is_file(),s['id']
  assert s['url'] in p.read_text(),f'source URL absent from retained tool evidence: {s["id"]}'
 for n in ['KEYWORD-COVERAGE.csv','KEYWORD-RESEARCH-ROUTING.csv']:
  with (HERE/n).open() as f:assert len(list(csv.DictReader(f)))==503
 links=0
 for name in ['RESEARCH.md','IMPLEMENTATION-PLAN.md','CARD-CATALOG.md','README.md']:
  p=HERE/name
  if not p.exists():continue
  for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text()):
   if target.startswith(('https://','http://')):continue
   if target.startswith('#'):continue
   local=target.split('#')[0]
   assert (HERE/local).exists() or local in {'PACKAGE-VALIDATION.json','MANIFEST.json'},(name,target)
   links+=1
 provenance=read('inputs/import-provenance.json')
 assert digest(HERE/'inputs/wardrobe_keyword_catalog.json')==provenance['source_sha256']
 inventory=read('CURRENT-INVENTORY.json')
 source_drift=[]
 for r in inventory['source_files']:
  if not r['present']:continue
  p=ROOT/'skills/photo-prompt-image-generator/assets'/r['file']
  if not p.exists() or digest(p)!=r['sha256']:source_drift.append(r['file'])
 protected=read('validation/task-start-preservation.json')
 changed=[];files_checked=0;directories_checked=0
 for r in protected['paths']:
  p=ROOT/r['path']
  if 'sha256' in r:
   files_checked+=1
   if not p.is_file() or digest(p)!=r['sha256']:changed.append(r['path'])
  else:
   directories_checked+=1
   if not p.exists():changed.append(r['path'])
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()
 report={'schema_version':'wardrobe-research-package-validation/v1','checked_date_kst':'2026-10-10',
  'research_package_checks':'PASS','counts':counts,'planned_regressions':48,'planned_native_arms':8,
  'checked_local_links':links,'original_catalog_sha256':provenance['source_sha256'],
  'snapshot_reference':{'head_at_start':inventory['head'],'head_at_finish':head,
                        'authored_source_files_changed_since_lexical_audit':source_drift},
  'preservation':{'existing_file_hashes_checked':files_checked,'existing_directory_presence_checked':directories_checked,
                  'initial_dirty_entries':len(protected['paths']),'changed_paths':changed,
                  'directory_presence_is_not_recursive_byte_integrity':True,
                  'changes_outside_task_scope_are_not_reset_or_attributed_to_this_task':True},
  'runtime_sources_edited_by_task':False,'runtime_integrated':False,'indexes_rebuilt':False,
  'runtime_pack_tests_executed':False,'behavior_regressions_executed':False,
  'embedding_calls':0,'image_calls':0,'images_generated':0,'native_pixels_verified':False,
  'user_acceptance':'pending','commit_created':False,'push_performed':False,
  'limits':['Structural reference checks do not prove complete semantic equivalence, retrieval, pixel quality or user acceptance.',
            'Original library citations are preserved from the recovered catalog, not newly reopened.',
            'Some candidate variants retain endpoint/effect review before runtime export.',
            'Working-tree source drift, if listed, needs a new snapshot before implementation.']}
 (HERE/'PACKAGE-VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 files=[]
 for p in sorted(HERE.rglob('*')):
  if p.is_file() and p.name!='MANIFEST.json' and '__pycache__' not in p.parts:
   files.append({'path':str(p.relative_to(HERE)),'bytes':p.stat().st_size,'sha256':digest(p)})
 (HERE/'MANIFEST.json').write_text(json.dumps({'schema_version':'wardrobe-research-manifest/v1','files':files},ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'research_package_checks':'PASS','files_hashed':len(files),'counts':counts,
                   'source_drift':source_drift,'protected_changed_paths':changed},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
