"""Reproduce pre-existing failures with authenticated pre-integration main DATA."""
from pathlib import Path
from unittest import mock
import json,sys,unittest,io,hashlib,tempfile
ROOT=Path.cwd();OUT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT))
from tests import test_photo_candidate_semantics as candidate
from tests import test_photo_character_appearance_100 as character
from tests import test_photo_liminal_active_use_korean_data_cleanup as liminal
import photo_source_manifest as sources
manifest=json.loads((OUT/'V26-PARENT-SOURCE.json').read_bytes());prefix='skills/photo-prompt-image-generator/assets/'
with tempfile.TemporaryDirectory(prefix='sealed-main-data-baseline-',dir='/private/tmp/harry-appearance-main-merge-tests') as tmp:
 assets=Path(tmp)/'assets';assets.mkdir()
 for row in manifest['members']:
  if row['path'].startswith(prefix) and len(Path(row['path']).parts)==4:
   raw=(ROOT/row['source_path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==row['sha256'];(assets/Path(row['path']).name).write_bytes(raw)
 p=assets/'photo_prompt_source_manifest.json';required=sources.required_files
 with mock.patch.object(candidate,'ASSETS',assets),mock.patch.object(character,'ASSETS',assets),mock.patch.object(liminal,'ASSETS',assets),mock.patch.object(candidate.generator,'RESEARCH_EXTENSION_FILENAMES',sources.extension_files('candidate',p)),mock.patch.object(character.pg,'VISUAL_OBLIGATION_EXTENSION_FILENAMES',sources.extension_files('visual_profile',p)),mock.patch.object(sources,'required_files',side_effect=lambda kind:required(kind,p)):
  for module,name,expected in [(character,'test_all_previous_profiles_keep_meaning_activation_effects_and_native_gates',11),(candidate,'test_maintenance_prose_is_external_and_hash_bound',1),(liminal,'test_complete_merged_state_and_twenty_one_keeps_remain_exact',1)]:
   cls=module.CharacterAppearance100Tests if module is character else module.PhotoCandidateSemanticsTests if module is candidate else module.LiminalActiveUseKoreanDataCleanupTests
   log=io.StringIO();result=unittest.TextTestRunner(stream=log,verbosity=2).run(unittest.TestSuite([cls(name)]))
   domain='CHARACTER' if module is character else 'MAINTENANCE' if module is candidate else 'LIMINAL'
   (OUT/f'MAIN-BASELINE-{domain}-FAILURE.log').write_text(log.getvalue())
   payload={'status':'FAILURE_REPRODUCED_ON_SEALED_MAIN_DATA','main_commit':manifest['source_pin'],'test':cls.__module__+'.'+cls.__name__+'.'+name,'failed_subcases':[str(t) for t,_ in result.failures],'failure_count':len(result.failures),'error_count':len(result.errors),'historical_expected_values_unchanged':True}
   (OUT/f'MAIN-BASELINE-{domain}-FAILURE.json').write_text(json.dumps(payload,indent=2)+'\n')
   assert len(result.failures)+len(result.errors)==expected,payload
   if module is liminal:assert 'glass_near_contact_reflected_fringes' in log.getvalue()
   if module is candidate:assert "KeyError: 'maintenance_only'" in log.getvalue()
   print(domain,payload['failure_count'],'failures',payload['error_count'],'errors')
