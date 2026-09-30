from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
sys.path.insert(0, str(ASSETS.parent / 'scripts'))
import prompt_generator as generator
import photo_candidate_semantics as semantics

PROFILE = 'handled_environment_surface_layer'
EXTENSION = 'photo_prompt_tactile_reality_extension.json'
FIXTURE = ROOT / 'tests/fixtures/photo_prompt/tactile_environment_independent_v1.json'
EVIDENCE = ROOT / 'docs/research-evidence/photo-prompt/tactile-reality-20260930'

class PhotoTactileRealitySemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = generator.load_json(ASSETS / 'photo_prompt_tags.json')
        cls.extension = json.loads((ASSETS / EXTENSION).read_text())
        cls.registry = generator.load_visual_obligation_registry(ASSETS / 'photo_prompt_visual_obligations.json')
        cls.profile = next(p for p in cls.registry['profiles'] if p['id'] == PROFILE)
        cls.narrow_registry = {**cls.registry, 'profiles': [cls.profile]}
        cls.fake_index = generator.build_visual_profile_index_payload(cls.narrow_registry, vectors={PROFILE: [1.0, 0.0]}, dimensions=2)
        cls.fixture = json.loads(FIXTURE.read_text())

    def hits(self, text, *, polarity='required'):
        rows=[{'source':'concept_lock','text':text,'polarity':polarity,'priority':'critical','mandatory':True},
              {'source':'authorial_core_interpreted_intent','text':text,'polarity':polarity,'priority':'critical','mandatory':True}]
        return generator.resolve_visual_profile_hits(self.narrow_registry, rows, visual_profile_index=self.fake_index,
                    query_vector=[1.0, 0.0], adult_context=True)['hits']

    def test_registered_ten_candidates_and_four_distinct_optional_bundles(self):
        self.assertIn(EXTENSION, generator.RESEARCH_EXTENSION_FILENAMES)
        self.assertIn(EXTENSION, self.data['candidate_semantic_policy']['required_extensions'])
        self.assertEqual({s:len(v) for s,v in self.extension['slots'].items()}, {'action':4,'surface_material':4,'composition':2})
        ids=[row['id'] for rows in self.extension['slots'].values() for row in rows]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertEqual(len(self.extension['visual_semantics']),4)
        for bundle in self.data['candidate_bundles']:
            if bundle['id'].startswith('tactile_'):
                self.assertEqual(bundle['profile_activation'],'independent_request_evidence_only')
                self.assertEqual(bundle['adoption'],'optional')
        for slot,rows in self.extension['slots'].items():
            for row in rows:
                self.assertTrue(row['concept_units'])
                self.assertTrue(row['relations'])
                self.assertTrue(row['contextual_usage']['contexts'])
                if slot in ('action','surface_material'):
                    self.assertTrue({'action','material'} <= set(row['affected_dimensions']))
                if slot=='action':self.assertIn('pose',row['affected_dimensions'])

    def test_existing_layer_preconditions_survive_normal_semantic_projection(self):
        for slot, rows in self.extension['slots'].items():
            for row in rows:
                projected=semantics.semantic_source(row,slot,self.data['candidate_semantic_policy'])
                text=' '.join(projected['concept_units'])+' '+json.dumps(projected['relations'])
                self.assertTrue('existing' in text or 'established' in text or 'already' in text,row['id'])
                self.assertEqual(projected['affected_dimensions'],row['affected_dimensions'])
        self.assertNotIn('tactile_unzip_contact_action',json.dumps(self.extension))

    def test_precise_exact_labels_are_hard_but_broad_operation_labels_are_not(self):
        for term in self.profile['activation']['exact_terms']:
            self.assertTrue(any(h['profile_id']==PROFILE and h['hard_eligible'] for h in self.hits(term)),term)
        for term in ['surreal','fold','peel','roll','zipper','reality glitch','material logic shift','현실','초현실','접기','벗기기','주름']:
            self.assertFalse(any(h.get('hard_eligible') for h in self.hits(term)),term)

    def test_independent_positive_components_admit_only_optional_discovery(self):
        for case in self.fixture['positive_cases']:
            text=case['synthetic_request']+' '+case['baseline_photographic_prompt']
            self.assertIsNotNone(generator.candidate_pack_visual_component_match(self.profile,text),case['id'])
            hits=self.hits(text)
            self.assertTrue(any(h['profile_id']==PROFILE and h.get('optional_eligible') for h in hits),case['id'])
            self.assertFalse(any(h.get('hard_eligible') for h in hits),case['id'])

    def test_independent_and_adjacent_negatives_cannot_activate_even_with_perfect_vector(self):
        negatives=[r['synthetic_request'] for r in self.fixture['negative_requests']]+[
            'Photograph hands folding a blue sheet beneath the edge of the sky, with the fabric continuous across a bend and its underside visible.',
            'Under the edge of the sky, hands fold a continuous sheet of foil so the underside catches the light.',
            'An adult peels ordinary wallpaper with a hand; the curled flap remains attached, exposing the underside and a contact shadow.',
            'Hands fold an ordinary paper map beneath the sky; the connected fold shows its reverse and thickness.',
            'A person gathers a blanket into hanging folds and looks at its underside.',
            'An adult rolls a rug beside the road surface; hands touch its continuous curled edge and underside.',
            'Hands unzip a jacket with joined teeth ahead and a recessed interior behind the slider.',
            'A cloud-shaped floating fabric sheet hangs over the sea surface, with a curled underside but nobody touching it.',
            'An adult steps through a glowing portal beside a wall.',
            'A body transforms gradually into a bird while its shadow remains on the road.',
            'A collage shows a torn photograph of the sky with a printed shadow.',
        ]
        for text in negatives:
            self.assertFalse(any(h.get('hard_eligible') or h.get('optional_eligible') for h in self.hits(text)),text)
        term=self.profile['activation']['exact_terms'][0]
        self.assertFalse(any(h.get('hard_eligible') for h in self.hits(term,polarity='excluded')))

    def test_unrelated_ordinary_objects_do_not_suppress_a_real_environment_target(self):
        case=self.fixture['positive_cases'][0]
        text=case['synthetic_request']+' '+case['baseline_photographic_prompt']+' A folded blanket and a rolled rug sit far behind the worker.'
        self.assertTrue(any(h.get('optional_eligible') for h in self.hits(text)))

    def test_reviewer_authored_multilingual_component_checks(self):
        # Additional review checks, not the independently authored blind fixture.
        for text in [
            '하늘 자체를 손으로 들어 올리면 표면층이 이어진 채 접히고 어두운 뒷면과 두께가 보인다.',
            '한 사람이 바다 자체를 손바닥으로 잡아 천처럼 모은다. 붙은 경계에서 이어진 주름 아래 뒷면이 보인다.',
            '空そのものを手で持ち上げる。シートの折り目は元の空へつながる。裏面と厚さが見える。',
        ]:
            self.assertIsNotNone(generator.candidate_pack_visual_component_match(self.profile,text),text)
            self.assertTrue(any(h.get('optional_eligible') for h in self.hits(text)),text)

    def test_operation_bundles_do_not_bypass_locked_action_or_material(self):
        for bundle in (b for b in self.data['candidate_bundles'] if b['id'].startswith('tactile_')):
            slots={}
            for member in bundle['member_candidates']:
                slots.setdefault(member['slot'],{'candidates':[]})['candidates'].append({**member,'applicability':{'status':'eligible'}})
            pack={'slots':slots,'authorial_core':{'intent_lock':{'open_dimensions':['action','material','pose']}},'provenance':{'seed':17}}
            scoped={**self.data,'candidate_bundles':[bundle]}
            self.assertTrue(semantics.public_bundles(scoped,pack)['candidates'])
            for locked in ['action','material','pose']:
                altered=copy.deepcopy(pack);altered['authorial_core']['intent_lock']['open_dimensions'].remove(locked)
                self.assertEqual(semantics.public_bundles(scoped,altered)['candidates'],[],(bundle['id'],locked))

    def test_provenance_is_separate_hash_bound_and_sources_resolve(self):
        reference=self.extension['maintenance_ref']
        record=json.loads((ROOT/'docs/research-evidence/photo-prompt/extension-maintenance'/f"{reference['record_id']}.json").read_text())
        self.assertEqual(reference['sha256'],semantics.digest(record))
        self.assertEqual(record['authored_source_sha256'],semantics.digest({k:v for k,v in self.extension.items() if k!='maintenance_ref'}))
        sources=json.loads((EVIDENCE/'source-manifest.json').read_text())
        known={r['id'] for r in sources['primary_sources']}
        decisions=json.loads((EVIDENCE/'integration-decisions.json').read_text())
        for row in decisions['new_candidates']:self.assertLessEqual(set(row['source_ids']),known)
        text=json.dumps(self.extension,ensure_ascii=False)+json.dumps(self.profile,ensure_ascii=False)
        self.assertNotIn('https://',text)
        self.assertNotIn('Goodmanprotocol',text)
        self.assertNotIn('trending',text)

    def test_real_indexes_include_changed_text_in_the_right_vector_space(self):
        visual=generator.load_visual_profile_index(ASSETS/'photo_prompt_visual_profile_index.json',self.registry)
        self.assertEqual(len(visual['entries'][PROFILE]['vector']),768)
        semantic=generator.load_semantic_index_payload(ASSETS/'photo_prompt_semantic_index.json')
        self.assertEqual(semantic['dictionary_hash'],generator.dictionary_hash(self.data))
        for slot,rows in self.extension['slots'].items():
            for row in rows:
                entry=semantic['entries'][f"slot:{slot}:{row['id']}"]
                self.assertEqual(len(entry['vector']),768)
                self.assertEqual(entry['text'],generator.semantic_text_for_entry(row,slot,kind='slot'))

if __name__=='__main__':unittest.main()
