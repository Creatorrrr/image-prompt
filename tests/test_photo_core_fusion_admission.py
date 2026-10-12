"""Whole/focus ties must not spend the finite inventory on an ID ordering."""
from __future__ import annotations

import copy
import json
import unittest
from unittest import mock

from tests import photo_prompt_fixtures as fixtures
import prompt_generator as g
import audit_composed_prompt as auditor


class PhotoCoreFusionAdmissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = g.load_runtime_data()
        cls.fixtures = fixtures.ROOT / 'tests/fixtures/photo_prompt/native_alias_v1'

    def inputs(self, key):
        values = json.loads((self.fixtures / key / 'fixture.json').read_text())
        controls = values['creative_controls']
        core = g.normalize_authorial_core(values['authorial_core_input'],
            request_envelope=g.normalize_request_envelope(values['request_envelope_input']),
            creative_control_snapshot=controls)
        return core, controls

    def test_frozen_english_clothing_targets_survive_the_global_cap(self):
        for key, entry in [('devanagari-sari-positive-en', 'sari_continuous_drape_system'),
                           ('thai-clothing-positive-en', 'thai_chut_thai_regional_ensemble')]:
            with self.subTest(key=key):
                core, controls = self.inputs(key)
                before = copy.deepcopy(core)
                slots, binding, _ = g.retrieve_core_slots(self.data, core, controls)
                self.assertIn(entry, [r['entry_id'] for r in slots['costume_style']['candidates']])
                self.assertLessEqual(sum(len(s['candidates']) for s in slots.values()), 64)
                for slot, info in slots.items():
                    self.assertLessEqual(len(info['candidates']), g.candidate_pack_slot_limit(slot))
                self.assertEqual(core, before)
                self.assertEqual(binding['candidate_adoption'], 'optional')
                self.assertEqual(auditor.audit_core_retrieval(dict(slots=slots, core_retrieval=binding,
                    authorial_core=core, creative_controls=controls), self.data), [])
                public = json.dumps(slots)
                for field in ('"score"', '"rank"', '"matched_terms"', '"representatives"'):
                    self.assertNotIn(field, public)

    def test_printed_alias_and_excluded_clothing_still_fail_before_ranking(self):
        for prefix, entry in [('devanagari-sari', 'sari_continuous_drape_system'),
                              ('thai-clothing', 'thai_chut_thai_regional_ensemble')]:
            for mode in ('printed-en', 'excluded-ko'):
                with self.subTest(case=prefix+'-'+mode):
                    core, controls = self.inputs(prefix+'-'+mode)
                    slots, _, _ = g.retrieve_core_slots(self.data, core, controls)
                    self.assertNotIn(entry, [r['entry_id'] for r in
                        slots.get('costume_style', {}).get('candidates', [])])
                    if mode == 'printed-en':
                        self.assertNotIn('costume_style', slots)

    def test_source_iteration_order_does_not_change_tied_admission(self):
        core, controls = self.inputs('devanagari-sari-positive-en')
        before = g.retrieve_core_slots(self.data, core, controls)
        reversed_data = copy.deepcopy(self.data)
        reversed_data['slots'] = {slot: list(reversed(entries))
                                 for slot, entries in reversed(list(self.data['slots'].items()))}
        after = g.retrieve_core_slots(reversed_data, core, controls)
        self.assertEqual(before[0], after[0])
        self.assertEqual(set(before[1]['active_slots']), set(after[1]['active_slots']))
        for slot in before[1]['active_slots']:
            self.assertEqual(set(before[1]['active_slots'][slot]['source_fields']),
                             set(after[1]['active_slots'][slot]['source_fields']))
        # The receipt still binds changed source bytes even when its inventory is invariant.
        self.assertNotEqual(before[1]['slot_corpus_sha256'], after[1]['slot_corpus_sha256'])

    def test_dense_tie_uses_named_owner_evidence_and_keeps_the_same_budget(self):
        core = {'contract_version': 'photo-authorial-core/v3', 'canonical_sha256': 'f'*64,
            'source_request': 'An adult person wearing a copper lantern costume.',
            'subject': 'An adult person wearing a copper lantern costume',
            'setting': 'a quiet studio', 'event': 'stands for a photograph',
            'baseline_prompt_en': 'An adult person wearing a copper lantern costume in a quiet studio.',
            'visual_priorities': [], 'style': {'domain': 'general_photo'},
            'request_binding': {'active_spans': []}, 'user_exclusions': []}
        controls = g.creative_controls.resolve(core['source_request'], context={'subject_category':'human'},
            overrides={'sensual':0,'fetish':0}, seed=17)
        core['creative_controls_sha256'] = controls['canonical_sha256']
        for needed, incidental in [('z_needed', 'a_incidental'), ('a_needed', 'z_incidental')]:
            for reverse, alias in ((False,'copper lantern'), (True,'copper lantern'),
                                   (False,'quiet studio'), (False,'')):
                with self.subTest(needed=needed, reverse=reverse, alias=alias):
                    entries = [{'id':needed,'en':'copper lantern costume','aliases':[alias] if alias else []},
                               {'id':incidental,'en':'adult wearing a costume','aliases':['unmentioned costume']}]
                    names = ['costume_style'] + [f'detail_{n:03d}' for n in range(64)]
                    data = {'slots': {name:(list(reversed(entries)) if reverse else entries)
                            if name=='costume_style' else [{'id':'supported','en':'copper lantern'}]
                            for name in (list(reversed(names)) if reverse else names)},
                        'candidate_semantic_policy': {'slot_dimensions': {name:['material'] for name in names}}}
                    def rank(index, fields, *, allowed_ids, limit):
                        ids = list(allowed_ids)
                        if ids and ids[0].startswith('slot:costume_style:'):
                            ids = [f'slot:costume_style:{x}' for x in
                                   ([needed,incidental] if 'global_context' in fields else [incidental,needed])]
                        return [{'document_id':doc,'score':2-i,'matched_terms':['copper']}
                                for i,doc in enumerate(ids)]
                    with mock.patch.object(g, 'rank_bm25f', side_effect=rank):
                        slots, binding, _ = g.retrieve_core_slots(data, core, controls)
                    expected = needed if alias == 'copper lantern' else min(needed, incidental)
                    self.assertEqual([r['entry_id'] for r in slots['costume_style']['candidates']], [expected])
                    self.assertEqual(sum(len(s['candidates']) for s in slots.values()), 64)
                    self.assertEqual(len(slots), 64)  # The cap does not invent a quota for all 65 slots.
                    self.assertEqual(binding['candidate_adoption'], 'optional')


if __name__ == '__main__':
    unittest.main()
