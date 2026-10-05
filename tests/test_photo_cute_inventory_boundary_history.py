"""The V17 successor cannot rebaseline a changed scene or candidate object."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
ILLUSTRATION=ROOT/'skills/subculture-illustration-image-generator'
sys.path.insert(0,str(ILLUSTRATION/'scripts'))
import validate_illustration_assets as v


class CuteInventoryBoundaryHistoryTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        self.assets=Path(temp.name)
        for path in (ILLUSTRATION/'assets').glob('photo_regression_baseline_v*.json'):
            shutil.copyfile(path,self.assets/path.name)
        shutil.copyfile(ILLUSTRATION/'assets/universal_scene_baseline_v2.json',
                        self.assets/'universal_scene_baseline_v2.json')
        self.baseline=json.loads((self.assets/'photo_regression_baseline_v17.json').read_text())
        self.raw=(self.assets/'photo_regression_baseline_v17_pack.json').read_bytes()
        self.pack=json.loads(self.raw)[0]

    def validate(self,pack=None,raw=None,repo=ROOT):
        return v._validate_v17_cute_data_successor(self.assets,repo,self.baseline,
            self.pack if pack is None else pack,self.raw if raw is None else raw)

    def test_sealed_successor_preserves_every_frozen_scene_and_candidate_field(self):
        self.validate()
        old=json.loads((self.assets/'photo_regression_baseline_v16_pack.json').read_text())[0]
        for field in ['authorial_core','creative_controls','authorial_composition','negative_en',
                      'negative_intent_guard','slots','candidate_bundles','visual_concept_candidates',
                      'intent_preservation','embodiment_preflight','adult_appeal']:
            with self.subTest(field=field):self.assertEqual(old[field],self.pack[field])

    def test_coordinated_candidate_core_negative_and_control_rehash_is_rejected(self):
        for kind in ['candidate','order','core','negative','controls','adoption']:
            changed=copy.deepcopy(self.pack)
            rows=next(s['candidates'] for s in changed['slots'].values() if len(s['candidates'])>=2)
            if kind=='candidate':rows[0]['concept_terms'][0]+=' altered'
            elif kind=='order':rows.reverse()
            elif kind=='core':changed['authorial_core']['subject']+=' altered'
            elif kind=='negative':changed['negative_en']+=', altered'
            elif kind=='controls':changed['creative_controls']['extra']=True
            else:rows[0]['adoption']='required'
            changed['pack_id']=v._canonical_photo_pack_id(changed)
            raw=(json.dumps([changed],ensure_ascii=False,indent=2)+'\n').encode()
            (self.assets/'photo_regression_baseline_v17_pack.json').write_bytes(raw)
            self.baseline.update(sha256=hashlib.sha256(raw).hexdigest(),pack_id=changed['pack_id'])
            with self.subTest(kind=kind),self.assertRaisesRegex(v.ValidationFailure,'immutable pack binding'):
                self.validate(changed,raw)

    def test_predecessor_manifest_is_immutable(self):
        path=self.assets/'photo_regression_baseline_v16.json'
        path.write_bytes(path.read_bytes()+b'\n')
        with self.assertRaisesRegex(v.ValidationFailure,'pack binding'):
            self.validate()

    def test_transition_cannot_be_reclassified_as_metadata_only(self):
        for field in ['metadata_only_transition','zero_pack_delta_transition',
                      'optional_inventory_transition','authored_metadata_ownership_transition']:
            self.baseline[field]={}
            with self.subTest(field=field),self.assertRaisesRegex(v.ValidationFailure,'cannot relabel'):
                self.validate()
            del self.baseline[field]

    def test_v16_still_rejects_the_live_v17_inventory(self):
        baseline=json.loads((self.assets/'photo_regression_baseline_v16.json').read_text())
        raw=(self.assets/'photo_regression_baseline_v16_pack.json').read_bytes()
        with self.assertRaisesRegex(v.ValidationFailure,'exact DATA inventory'):
            v._validate_v16_seduction_source_successor(self.assets,ROOT,baseline,json.loads(raw)[0],raw)
