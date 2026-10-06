"""The additive appearance transition preserves V26 and all scene duties."""
from pathlib import Path
from contextlib import contextmanager
from unittest import mock
import copy,hashlib,json,shutil,subprocess,sys,tempfile,unittest
from tests import photo_prompt_fixtures as fixtures
ROOT=Path(__file__).resolve().parents[1]
ILLUSTRATION=ROOT/'skills/subculture-illustration-image-generator'
EVIDENCE=Path('docs/research-evidence/photo-prompt/harry-potter-integration-20261006/main-merge')

class AppearanceBoundaryHistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        temporary=tempfile.TemporaryDirectory(prefix='sealed-v27-appearance-')
        cls.addClassCleanup(temporary.cleanup)
        cls.source_root=Path(temporary.name).resolve()/'tree'
        with mock.patch('subprocess.Popen',side_effect=AssertionError('historical materialization invoked subprocess')):
            cls.validator=fixtures.archived_v27_validator(cls.source_root)
        interpreter=cls.source_root/'.venv/bin/python'
        interpreter.parent.mkdir(parents=True)
        interpreter.symlink_to(Path(sys.executable).resolve())
        cls.illustration=cls.source_root/ILLUSTRATION.relative_to(ROOT)
        cls.proof=json.loads((cls.source_root/EVIDENCE/'V27-APPEARANCE-DATA-PROOF.json').read_bytes())
        cls.parent=json.loads((cls.source_root/EVIDENCE/'V26-PARENT-SOURCE.json').read_bytes())
        cls.baseline=json.loads((cls.illustration/'assets/photo_regression_baseline_v27.json').read_bytes())
        cls.raw=(cls.illustration/'assets/photo_regression_baseline_v27_pack.json').read_bytes()
        cls.pack=json.loads(cls.raw)[0]

    def setUp(self):
        temporary=tempfile.TemporaryDirectory(prefix='v27-appearance-boundary-');self.addCleanup(temporary.cleanup)
        self.repo=Path(temporary.name).resolve();self.assets=self.repo/ILLUSTRATION.relative_to(ROOT)/'assets'
        paths={r['source_path'] for r in self.parent['members']}
        paths.update(self.proof['source_files_after']);paths.update(self.proof['active_shards_after'])
        paths.update({str(EVIDENCE/'V27-APPEARANCE-DATA-PROOF.json'),str(EVIDENCE/'V26-PARENT-SOURCE.json')})
        paths.update(str(p.relative_to(self.source_root)) for p in (self.illustration/'assets').glob('photo_regression_baseline_v*.json'))
        paths.add(str((ILLUSTRATION/'assets/universal_scene_baseline_v2.json').relative_to(ROOT)))
        for name in paths:
            p=self.repo/name;p.parent.mkdir(parents=True,exist_ok=True);p.symlink_to(self.source_root/name)

    def validate(self,pack=None,raw=None):
        self.validator._validate_v27_appearance_data_successor(self.assets,self.repo,self.baseline,
            self.pack if pack is None else pack,self.raw if raw is None else raw)

    @contextmanager
    def changed(self,name,raw):
        p=self.repo/name;original=p.readlink();p.unlink()
        if raw is not None:p.write_bytes(raw)
        try:yield
        finally:p.unlink(missing_ok=True);p.symlink_to(original)

    def test_archived_real_command_reproduces_v27_and_v26_scene_remains_exact(self):
        result=self.validator.validate_photo_regression_baseline(self.illustration/'assets')
        self.assertEqual(result['schema'],'photo_regression_baseline/v27')
        self.assertEqual(result['sha256'],self.proof['current_pack_sha256'])
        previous=json.loads((self.illustration/'assets/photo_regression_baseline_v26_pack.json').read_bytes())[0]
        for name in ('slots','authorial_core','authorial_composition','creative_controls','embodiment_preflight','negative_en','visual_concept_candidates'):
            self.assertEqual(previous[name],self.pack[name],name)
        self.assertEqual(64,self.validator._public_photo_candidate_count(self.pack))
        self.assertEqual(5,len(self.proof['reviewed_pack_delta']))

    def test_archived_default_and_explicit_v27_boundary_are_registered(self):
        def frozen(command,**kwargs):
            Path(command[command.index('--output-file')+1]).write_bytes(self.raw)
            return subprocess.CompletedProcess(command,0,'','')
        with mock.patch.object(self.validator.subprocess,'run',side_effect=frozen):
            for version in (None,27):
                result=self.validator.validate_photo_regression_baseline(self.illustration/'assets',baseline_version=version)
                self.assertEqual(result['schema'],'photo_regression_baseline/v27')
        with self.assertRaisesRegex(self.validator.ValidationFailure,'unsupported photo baseline version'):
            self.validator.validate_photo_regression_baseline(self.assets,baseline_version=28)

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
            changed['pack_id']=self.validator._canonical_photo_pack_id(changed)
            raw=(json.dumps([changed],ensure_ascii=False,indent=2)+'\n').encode()
            with self.subTest(mutation=key),self.assertRaises(self.validator.ValidationFailure):self.validate(changed,raw)

    def test_current_sources_and_active_index_shards_are_bound(self):
        names=[next(p for p in self.proof['source_files_after'] if p.endswith('photo_prompt_character_appearance_extension.json')),next(iter(self.proof['active_shards_after']))]
        for name in names:
            with self.subTest(path=name),self.changed(name,(self.source_root/name).read_bytes()+b'\n'):
                with self.assertRaises(self.validator.ValidationFailure):self.validate()

    def test_parent_manifest_and_proof_cannot_be_rehashed_to_weaker_claims(self):
        for name in ('V26-PARENT-SOURCE.json','V27-APPEARANCE-DATA-PROOF.json'):
            path=str(EVIDENCE/name)
            with self.subTest(path=name),self.changed(path,(self.source_root/path).read_bytes()+b'\n'):
                with self.assertRaises(self.validator.ValidationFailure):self.validate()

    def test_historical_payload_recovery_rejects_unsealed_live_tampering(self):
        row=next(r for r in self.parent['members'] if r['path'].endswith('/photo_prompt_semantic_index.json') and '/assets/' in r['path'] and '/parent-source' not in r['path'])
        historical=dict(row,source_path=row['path'])
        self.assertEqual(fixtures._v24_verified_payload(self.source_root,historical),(self.source_root/row['source_path']).read_bytes())
        with self.changed(row['path'],(self.source_root/row['path']).read_bytes()+b'\n'):
            with self.assertRaises(AssertionError):fixtures._v24_verified_payload(self.repo,historical)

    def test_missing_or_rehashed_parent_cannot_fall_back_to_git_or_network(self):
        name=str(EVIDENCE/'V26-PARENT-SOURCE.json')
        for raw in (None,(self.source_root/name).read_bytes()+b'\n'):
            with self.changed(name,raw),tempfile.TemporaryDirectory() as tmp:
                with mock.patch('subprocess.Popen',side_effect=AssertionError('historical fallback invoked subprocess')):
                    with self.assertRaises(AssertionError):fixtures.materialize_v26_parent_source(Path(tmp)/'tree',source_root=self.repo)

class AppearanceFixtureRecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.v27=fixtures._v27_parent_manifest()
        cls.v26=fixtures._v26_parent_manifest()
        cls.v27_rows={row['path']:row for row in cls.v27['members']}
        cls.v26_rows={row['path']:row for row in cls.v26['members']}

    def setUp(self):
        temporary=tempfile.TemporaryDirectory(prefix='v28-sealed-recovery-')
        self.addCleanup(temporary.cleanup)
        self.repo=Path(temporary.name).resolve()
        names={fixtures.V27_PARENT_MANIFEST,fixtures.V28_MUTED_COLOR_PROOF,
               fixtures.V26_PARENT_MANIFEST,fixtures.V27_APPEARANCE_PROOF}
        for name in fixtures.V28_MUTED_COLOR_SOURCE_PATHS:
            names.update({Path(name),Path(self.v27_rows[name]['source_path']),
                          Path(self.v26_rows[name]['source_path'])})
        for name in names:
            target=self.repo/name
            target.parent.mkdir(parents=True,exist_ok=True)
            source = (fixtures.v29_source_path(str(name))
                      if str(name) in fixtures.V28_MUTED_COLOR_SOURCE_PATHS else ROOT/name)
            shutil.copy2(source,target)

    @contextmanager
    def changed(self,name,raw):
        path=self.repo/name
        original=path.read_bytes()
        if raw is None:path.unlink()
        else:path.write_bytes(raw)
        try:yield
        finally:path.write_bytes(original)

    def test_sealed_v28_recovery_preserves_exact_v27_and_v26_payloads(self):
        with mock.patch('subprocess.Popen',side_effect=AssertionError('historical fallback invoked subprocess')):
            for name in sorted(fixtures.V28_MUTED_COLOR_SOURCE_PATHS):
                for version,rows in ((27,self.v27_rows),(26,self.v26_rows)):
                    row=rows[name]
                    with self.subTest(path=name,version=version):
                        actual=fixtures._v24_verified_payload(self.repo,dict(row,source_path=name))
                        expected=row['source_path'] if row['source_path']!=name else self.v27_rows[name]['source_path']
                        self.assertEqual(actual,(ROOT/expected).read_bytes())
                        self.assertEqual(hashlib.sha256(actual).hexdigest(),row['sha256'])

    def test_live_drift_cannot_use_the_sealed_successor_recovery(self):
        for name in sorted(fixtures.V28_MUTED_COLOR_SOURCE_PATHS):
            row=dict(self.v27_rows[name],source_path=name)
            with self.subTest(path=name),self.changed(name,(self.repo/name).read_bytes()+b'\n'):
                with self.assertRaisesRegex(AssertionError,'payload drift'):
                    fixtures._v24_verified_payload(self.repo,row)

    def test_v27_index_rollback_cannot_bypass_v28_live_source_binding(self):
        for name in sorted(fixtures.V28_MUTED_COLOR_SOURCE_PATHS):
            if self.v26_rows[name]['sha256']==self.v27_rows[name]['sha256']:continue
            previous=(ROOT/self.v27_rows[name]['source_path']).read_bytes()
            row=dict(self.v26_rows[name],source_path=name)
            with self.subTest(path=name),self.changed(name,previous):
                with self.assertRaisesRegex(AssertionError,'Frozen V28 retained live source payload drift'):
                    fixtures._v24_verified_payload(self.repo,row)

    def test_historical_drift_cannot_use_an_untampered_live_successor(self):
        for name in sorted(fixtures.V28_MUTED_COLOR_SOURCE_PATHS):
            for version,rows in ((27,self.v27_rows),(26,self.v26_rows)):
                row=rows[name]
                if row['source_path']==name:continue
                with self.subTest(path=name,version=version),self.changed(
                        row['source_path'],(self.repo/row['source_path']).read_bytes()+b'\n'):
                    with self.assertRaisesRegex(AssertionError,'payload drift'):
                        fixtures._v24_verified_payload(self.repo,dict(row,source_path=name))

    def test_recovery_requires_both_immutable_transition_manifests_and_proofs(self):
        name='skills/photo-prompt-image-generator/assets/photo_prompt_semantic_index.json'
        row=dict(self.v26_rows[name],source_path=name)
        for path in (fixtures.V27_PARENT_MANIFEST,fixtures.V28_MUTED_COLOR_PROOF,
                     fixtures.V26_PARENT_MANIFEST,fixtures.V27_APPEARANCE_PROOF):
            for raw in (None,(self.repo/path).read_bytes()+b'\n'):
                with self.subTest(path=path,missing=raw is None),self.changed(path,raw):
                    with mock.patch('subprocess.Popen',side_effect=AssertionError('historical fallback invoked subprocess')):
                        with self.assertRaises(AssertionError):
                            fixtures._v24_verified_payload(self.repo,row)

    def test_v27_materialization_rejects_missing_or_rehashed_manifest_before_writing(self):
        path=fixtures.V27_PARENT_MANIFEST
        for raw in (None,(self.repo/path).read_bytes()+b'\n'):
            with self.subTest(missing=raw is None),self.changed(path,raw):
                destination=self.repo/'destination'
                with mock.patch('subprocess.Popen',side_effect=AssertionError('historical fallback invoked subprocess')):
                    with self.assertRaisesRegex(AssertionError,'Missing V24 historical source payload|Frozen V27 parent source manifest drift'):
                        fixtures.materialize_v27_parent_source(destination,source_root=self.repo)
                self.assertFalse(destination.exists())

    def test_all_six_archived_payloads_reject_bytes_mode_symlink_and_missing_file(self):
        for row in self.v27['members']:
            if row['kind']!='archived_parent_source':continue
            path=self.repo/row['source_path']
            path.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(ROOT/row['source_path'],path)
            for mutation in ('bytes','mode','symlink','missing'):
                with self.subTest(path=row['path'],mutation=mutation):
                    if mutation=='bytes':path.write_bytes(path.read_bytes()+b'\n')
                    elif mutation=='mode':path.chmod(0o600)
                    elif mutation=='symlink':
                        path.unlink();path.symlink_to(ROOT/row['source_path'])
                    else:path.unlink()
                    with self.assertRaises(AssertionError):
                        fixtures._v24_verified_payload(self.repo,row)
                    path.unlink(missing_ok=True)
                    shutil.copy2(ROOT/row['source_path'],path)


if __name__=='__main__':unittest.main()
