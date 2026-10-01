from pathlib import Path
import copy,hashlib,json,sys,datetime
from unittest import mock
base=Path(sys.argv[1]);fixture=Path(sys.argv[2]);ids=json.loads(sys.argv[3])
skill=base if (base/'scripts/prompt_generator.py').is_file() else base/'skills/photo-prompt-image-generator'
scripts=skill/'scripts';registry_path=skill/'assets/photo_prompt_visual_obligations.json'
sys.path.insert(0,str(scripts));import prompt_generator as g
main=scripts/'prompt_generator.py';h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before={'prompt_generator_sha256':h(main),'registry_main_file_sha256':h(registry_path)}
registry=g.load_visual_obligation_registry(registry_path)
registry_hash=g.visual_profile_registry_sha256(registry)
index=g.build_visual_profile_index_payload(registry)
def generated_index(registry,**kwargs):
 assert not kwargs,kwargs
 assert g.visual_profile_registry_sha256(registry)==registry_hash
 return copy.deepcopy(index)
rows=[]
cases=[json.loads(line) for line in fixture.read_text().splitlines() if line.strip()]
with mock.patch.object(g,'build_visual_profile_index_payload',side_effect=generated_index):
 for case in cases:
  if case['id'] not in ids:continue
  sources=[{'source':'concept_lock','text':case['text'],'polarity':'required','priority':'critical','mandatory':True}]
  hard=g.candidate_pack_auto_visual_obligation_matches(registry,sources)
  optional=g.candidate_pack_auto_visual_concept_matches(registry,sources)
  actual_hard=sorted(hard);actual_optional=sorted(optional)
  expected_hard=sorted(case['expected_profile_ids']);expected_optional=sorted(case['expected_candidate_profile_ids'])
  rows.append({'id':case['id'],'text':case['text'],'expected_hard_profile_ids':expected_hard,'expected_optional_profile_ids':expected_optional,'actual_hard_profile_ids':actual_hard,'actual_optional_profile_ids':actual_optional,'hard_expected_pass':actual_hard==expected_hard,'optional_expected_pass':actual_optional==expected_optional,'direct_expected_pass':actual_hard==expected_hard and actual_optional==expected_optional})
after={'prompt_generator_sha256':h(main),'registry_main_file_sha256':h(registry_path)}
assert before==after
assert g.visual_profile_registry_sha256(g.load_visual_obligation_registry(registry_path))==registry_hash
print(json.dumps({'base_path':str(base),'generator_module_path':g.__file__,'registry_path':str(registry_path),'registry_canonical_sha256':registry_hash,'registry_profile_count':len(registry['profiles']),'source_file_hashes':before,'source_unchanged_during_probe':before==after,'fixture_path':str(fixture),'fixture_sha256':h(fixture),'tested_case_count':len(rows),'method':'Same direct hard and optional matching calls as tests/test_photo_visual_obligations.py lines 153-174, with its one-registry-built-index mock pattern. No candidate pack or image generation; no embedding/API call.','rows':rows},ensure_ascii=False,indent=2))
