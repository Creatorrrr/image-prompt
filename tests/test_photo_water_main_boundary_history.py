"""Water's V30 qualification cannot overwrite V29 or unrelated DATA."""
from __future__ import annotations
import contextlib
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
ILL=ROOT/'skills/subculture-illustration-image-generator'
sys.path.insert(0,str(ILL/'scripts'))
import validate_illustration_assets as validator
from tests import photo_prompt_fixtures as fixtures


class WaterMainBoundaryHistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proof,cls.parent=fixtures._v30_transition(ROOT)
        original=tempfile.TemporaryDirectory(prefix='v30-original-source-')
        cls.addClassCleanup(original.cleanup)
        cls.original_root=Path(original.name).resolve()/'tree'
        cls.original_validator=fixtures.archived_v30_validator(cls.original_root)
        cls.baseline=json.loads((ILL/'assets/photo_regression_baseline_v30.json').read_bytes())
        cls.raw=(ILL/'assets/photo_regression_baseline_v30_pack.json').read_bytes()
        cls.pack=json.loads(cls.raw)[0]

    def setUp(self):
        temporary=tempfile.TemporaryDirectory(prefix='water-v30-boundary-')
        self.addCleanup(temporary.cleanup)
        self.repo=Path(temporary.name)
        self.assets=self.repo/ILL.relative_to(ROOT)/'assets'
        paths=set(self.proof['source_files_after'])|set(self.proof['active_shards_after'])
        paths.update(row['source_path'] for row in self.parent['members'])
        paths.update([str(fixtures.V30_WATER_PROOF),str(fixtures.V29_PARENT_SOURCE),str(fixtures.V29_RUNTIME_PROOF)])
        paths.update(str(p.relative_to(self.original_root)) for p in (self.original_root/ILL.relative_to(ROOT)/'assets').glob('photo_regression_baseline_v*.json'))
        paths.add(str((ILL/'assets/universal_scene_baseline_v2.json').relative_to(ROOT)))
        for name in paths:
            path=self.repo/name;path.parent.mkdir(parents=True,exist_ok=True)
            path.symlink_to(self.original_root/name)

    def validate(self,pack=None,raw=None):
        try:
            self.original_validator._validate_v30_water_main_successor(self.assets,self.repo,self.baseline,
                self.pack if pack is None else pack,self.raw if raw is None else raw)
        except self.original_validator.ValidationFailure as exc:
            raise validator.ValidationFailure(str(exc)) from exc

    @contextlib.contextmanager
    def changed(self,name,raw,mode=None):
        path=self.repo/name;original=path.readlink();path.unlink()
        if raw is not None:
            path.write_bytes(raw)
            if mode is not None:path.chmod(mode)
        try:yield
        finally:
            path.unlink(missing_ok=True);path.symlink_to(original)

    def test_original_cli_receipt_and_reviewed_delta_are_qualified(self):
        result=validator.validate_photo_regression_baseline(ILL/'assets',baseline_version=30)
        self.assertEqual(result['schema'],'photo_regression_baseline/v30')
        self.assertEqual(result['sha256'],self.proof['current_pack_sha256'])
        self.assertEqual(64,validator._public_photo_candidate_count(self.pack))
        self.assertEqual(22,len(self.proof['reviewed_pack_delta']))

    def test_sealed_current_sources_and_original_parent_pass(self):
        self.validate()
        self.assertEqual(1253,self.parent['member_count'])

    def test_unreviewed_meaning_order_core_budget_or_negative_cannot_be_rehashed(self):
        for kind in ('meaning','order','core','budget','negative','age_policy'):
            pack=copy.deepcopy(self.pack)
            if kind=='meaning':pack['slots']['texture']['candidates'][1]['concept_terms'][0]+=' changed'
            if kind=='order':pack['slots']['texture']['candidates'].reverse()
            if kind=='core':pack['authorial_core']['subject']+=' changed'
            if kind=='budget':pack['authorial_composition']['prompt_budget']['absolute_maximum_words']+=1
            if kind=='negative':pack['negative_en']+=', changed'
            if kind=='age_policy':pack['adult_appeal']['composition_requirements']['adult_subject_phrase_required']=True
            pack['pack_id']=validator._canonical_photo_pack_id(pack)
            raw=(json.dumps([pack],ensure_ascii=False,indent=2)+'\n').encode()
            with self.subTest(kind=kind),self.assertRaises(validator.ValidationFailure):self.validate(pack,raw)

    def test_water_runtime_unrelated_data_and_active_shards_remain_bound(self):
        names=['skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_water_relations.json',
               'skills/photo-prompt-image-generator/assets/photo_prompt_tags.json',
               'skills/photo-prompt-image-generator/scripts/photo_runtime_sources.py',
               next(iter(self.proof['active_shards_after']))]
        for name in names:
            with self.subTest(path=name),self.changed(name,(ROOT/name).read_bytes()+b'\n'):
                with self.assertRaises(validator.ValidationFailure):self.validate()

    def test_undeclared_source_cannot_enter_the_qualified_inventory(self):
        path=self.repo/'skills/photo-prompt-image-generator/assets/photo_prompt_unrelated_extension.json'
        path.write_text('{}')
        with self.assertRaises(validator.ValidationFailure):self.validate()

    def test_missing_rehashed_proof_or_original_parent_fail(self):
        for name in (str(fixtures.V30_WATER_PROOF),str(fixtures.V29_PARENT_SOURCE)):
            for raw in (None,(ROOT/name).read_bytes()+b'\n'):
                with self.subTest(path=name,missing=raw is None),self.changed(name,raw):
                    with self.assertRaises((validator.ValidationFailure,OSError)):self.validate()

    def test_original_parent_source_bytes_and_mode_cannot_drift(self):
        row=next(row for row in self.parent['members'] if row['path']=='tests/photo_prompt_fixtures.py')
        name=row['source_path'];raw=(ROOT/name).read_bytes()
        for payload,mode in ((raw+b'\n',0o644),(raw,0o600)):
            with self.subTest(mode=mode),self.changed(name,payload,mode):
                with self.assertRaises(validator.ValidationFailure):self.validate()


if __name__=='__main__':unittest.main()
