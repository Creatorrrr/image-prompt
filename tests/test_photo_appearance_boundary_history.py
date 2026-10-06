"""The additive appearance transition preserves V26 and all scene duties."""
from pathlib import Path
from contextlib import contextmanager
from unittest import mock
import copy,hashlib,json,subprocess,sys,tempfile,unittest
from tests import photo_prompt_fixtures as fixtures
ROOT=Path(__file__).resolve().parents[1]
ILLUSTRATION=ROOT/'skills/subculture-illustration-image-generator'
EVIDENCE=Path('docs/research-evidence/photo-prompt/harry-potter-integration-20261006/main-merge')
sys.path.insert(0,str(ILLUSTRATION/'scripts'))
import validate_illustration_assets as validator

class AppearanceBoundaryHistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proof=json.loads((ROOT/EVIDENCE/'V27-APPEARANCE-DATA-PROOF.json').read_bytes())
        cls.parent=json.loads((ROOT/EVIDENCE/'V26-PARENT-SOURCE.json').read_bytes())
        cls.baseline=json.loads((ILLUSTRATION/'assets/photo_regression_baseline_v27.json').read_bytes())
        cls.raw=(ILLUSTRATION/'assets/photo_regression_baseline_v27_pack.json').read_bytes()
        cls.pack=json.loads(cls.raw)[0]
        cls.historical_directory=tempfile.TemporaryDirectory(prefix='original-v27-validator-')
        cls.addClassCleanup(cls.historical_directory.cleanup)
        cls.historical_root=Path(cls.historical_directory.name).resolve()/'tree'
        cls.historical_validator=fixtures.archived_v27_validator(cls.historical_root)

    def setUp(self):
        temporary=tempfile.TemporaryDirectory(prefix='v27-appearance-boundary-');self.addCleanup(temporary.cleanup)
        self.repo=Path(temporary.name);self.assets=self.repo/ILLUSTRATION.relative_to(ROOT)/'assets'
        paths={r['source_path'] for r in self.parent['members']}
        paths.update(self.proof['source_files_after']);paths.update(self.proof['active_shards_after'])
        paths.update({str(EVIDENCE/'V27-APPEARANCE-DATA-PROOF.json'),str(EVIDENCE/'V26-PARENT-SOURCE.json')})
        paths.update(str(p.relative_to(ROOT)) for p in (ILLUSTRATION/'assets').glob('photo_regression_baseline_v*.json'))
        paths.add(str((ILLUSTRATION/'assets/universal_scene_baseline_v2.json').relative_to(ROOT)))
        for name in paths:
            original=self.historical_root/name
            p=self.repo/name;p.parent.mkdir(parents=True,exist_ok=True);p.symlink_to(original if original.is_file() else ROOT/name)

    def validate(self,pack=None,raw=None):
        try:
            self.historical_validator._validate_v27_appearance_data_successor(self.assets,self.repo,self.baseline,
                self.pack if pack is None else pack,self.raw if raw is None else raw)
        except self.historical_validator.ValidationFailure as exc:
            raise validator.ValidationFailure(str(exc)) from exc

    @contextmanager
    def changed(self,name,raw):
        p=self.repo/name;original=p.readlink();p.unlink()
        if raw is not None:p.write_bytes(raw)
        try:yield
        finally:p.unlink(missing_ok=True);p.symlink_to(original)

    def test_original_real_command_reproduces_v27_and_v26_scene_remains_exact(self):
        result=validator.validate_photo_regression_baseline(ILLUSTRATION/'assets',baseline_version=27)
        self.assertEqual(result['schema'],'photo_regression_baseline/v27')
        self.assertEqual(result['sha256'],self.proof['current_pack_sha256'])
        previous=json.loads((ILLUSTRATION/'assets/photo_regression_baseline_v26_pack.json').read_bytes())[0]
        for name in ('slots','authorial_core','authorial_composition','creative_controls','embodiment_preflight','negative_en','visual_concept_candidates'):
            self.assertEqual(previous[name],self.pack[name],name)
        self.assertEqual(64,validator._public_photo_candidate_count(self.pack))
        self.assertEqual(5,len(self.proof['reviewed_pack_delta']))

    def test_explicit_original_boundary_is_registered(self):
        def frozen(command,**kwargs):
            Path(command[command.index('--output-file')+1]).write_bytes(self.raw)
            return subprocess.CompletedProcess(command,0,'','')
        with mock.patch.object(validator.subprocess,'run',side_effect=frozen):
            for version in (27,):
                result=validator.validate_photo_regression_baseline(ILLUSTRATION/'assets',baseline_version=version)
                self.assertEqual(result['schema'],'photo_regression_baseline/v27')
        with self.assertRaisesRegex(validator.ValidationFailure,'unsupported photo baseline version'):
            validator.validate_photo_regression_baseline(self.assets,baseline_version=29)

    def test_rehashed_candidate_order_meaning_controls_negative_and_budget_are_rejected(self):
        for key in ('candidate','order','core','controls','negative','budget'):
            changed=copy.deepcopy(self.pack)
            rows=next(r['candidates'] for r in changed['slots'].values() if len(r['candidates'])>1)
            if key=='candidate':rows[0]['concept_terms'][0]+=' changed'
            if key=='order':rows.reverse()
            if key=='core':changed['authorial_core']['subject']+=' changed'
            if key=='controls':changed['creative_controls']['extra']=True
            if key=='negative':changed['negative_en']+=', changed'
            if key=='budget':changed['authorial_composition']['prompt_budget']['absolute_maximum_words']+=1
            changed['pack_id']=validator._canonical_photo_pack_id(changed)
            raw=(json.dumps([changed],ensure_ascii=False,indent=2)+'\n').encode()
            with self.subTest(mutation=key),self.assertRaises(validator.ValidationFailure):self.validate(changed,raw)

    def test_current_sources_and_active_index_shards_are_bound(self):
        names=[next(p for p in self.proof['source_files_after'] if p.endswith('photo_prompt_character_appearance_extension.json')),next(iter(self.proof['active_shards_after']))]
        for name in names:
            with self.subTest(path=name),self.changed(name,(ROOT/name).read_bytes()+b'\n'):
                with self.assertRaises(validator.ValidationFailure):self.validate()

    def test_parent_manifest_and_proof_cannot_be_rehashed_to_weaker_claims(self):
        for name in ('V26-PARENT-SOURCE.json','V27-APPEARANCE-DATA-PROOF.json'):
            path=str(EVIDENCE/name)
            with self.subTest(path=name),self.changed(path,(ROOT/path).read_bytes()+b'\n'):
                with self.assertRaises(validator.ValidationFailure):self.validate()

    def test_historical_payload_recovery_rejects_unsealed_live_tampering(self):
        row=next(r for r in self.parent['members'] if r['path'].endswith('/photo_prompt_semantic_index.json') and '/assets/' in r['path'] and '/parent-source' not in r['path'])
        historical=dict(row,source_path=row['path'])
        self.assertEqual(fixtures._v24_verified_payload(ROOT,historical),(ROOT/row['source_path']).read_bytes())
        with self.changed(row['path'],(ROOT/row['path']).read_bytes()+b'\n'):
            with self.assertRaises(AssertionError):fixtures._v24_verified_payload(self.repo,historical)

    def test_missing_or_rehashed_parent_cannot_fall_back_to_git_or_network(self):
        name=str(EVIDENCE/'V26-PARENT-SOURCE.json')
        for raw in (None,(ROOT/name).read_bytes()+b'\n'):
            with self.changed(name,raw),tempfile.TemporaryDirectory() as tmp:
                with mock.patch('subprocess.Popen',side_effect=AssertionError('historical fallback invoked subprocess')):
                    with self.assertRaises(AssertionError):fixtures.materialize_v26_parent_source(Path(tmp)/'tree',source_root=self.repo)

if __name__=='__main__':unittest.main()
