"""Manual source references never replace direct facts or mutation obligations."""
import copy
import unittest
from unittest import mock

from tests.test_photo_semantic_evidence import (
    A, c, e, g, layout, core, fact, source, seal, reattest, owner_map, slot,
)


def reference(pointer, quote, refs, *, rid='base', relation='selected_output_constraint'):
    return {'realization_id': rid, 'pointer': pointer, 'quote': quote,
            'fact_refs': refs, 'disposition': 'semantic_reference',
            'reference_relation': relation,
            'retained_constraint_rationale':
                'The local clause retains readability on this selected face; '
                'the full illumination value is directly grounded in the named primary field.'}


def referenced_source(*, local_fact=False):
    # These are independently authored meanings, not a converter from old proofs.
    text = 'The existing face is illuminated from below.'
    gate = 'Keep this selected illumination readable on the same face.'
    rows = [fact('face', 'subject', 'face', 'anatomy.face.presence', 'prerequisite',
                 'present', [], quote='existing face'),
            fact('underlight', 'lighting', 'face', 'lighting.direction', 'effect',
                 'below', ['face'], quote='illuminated from below',
                 operation='set_value', receivers=[])]
    if local_fact:
        rows.append(fact('local_face', 'subject', 'face', 'anatomy.face.presence',
                         'prerequisite', 'present', [], quote='same face',
                         pointer='/content/render_gates/0'))
    data = source(text, rows, {'light_direction': slot('light_direction', ['lighting'],
                  property_prefixes=['lighting.direction'])},
                  {'base': owner_map(('face', 'primary_face'))})
    record = data['candidates'][A]
    record['content']['render_gates'] = [gate]
    seal(data, {'light_direction': ['underlight']})
    proof = record['content']['role_evidence']
    if not local_fact:
        proof['source_units'] = [u for u in proof['source_units']
                                 if u['pointer'] != '/content/render_gates/0']
    proof['source_units'].append(reference('/content/render_gates/0', gate, ['underlight']))
    reattest(data)
    return data


def proof_of(data):
    return data['candidates'][A]['content']['role_evidence']


def ref_of(data):
    return next(u for u in proof_of(data)['source_units']
                if u['disposition'] == 'semantic_reference')


def direct_of(data):
    return next(u for u in proof_of(data)['source_units'] if u['pointer'] == '/content/en')


class SemanticReferenceUnitTests(unittest.TestCase):
    def assert_rejected(self, data):
        reattest(data)
        with self.assertRaises(ValueError):
            c.validate(data)
        # Both render/search entry routes require full validation before sealing.
        with self.assertRaises(ValueError):
            c.entry(data, A)
        with self.assertRaises(ValueError):
            layout.guard_record(data['candidates'][A], data)

    def test_generic_relations_and_order_independent_single_hop(self):
        for relation in sorted(e.REFERENCE_RELATIONS):
            for reverse in [False, True]:
                with self.subTest(relation=relation, reverse=reverse):
                    data = referenced_source()
                    ref_of(data)['reference_relation'] = relation
                    if reverse:
                        proof_of(data)['source_units'].reverse()
                    reattest(data)
                    c.validate(data)
                    self.assertEqual(len(proof_of(data)['facts']), 2)
                    self.assertEqual(proof_of(data)['roles']['light_direction']['fact_refs'], ['underlight'])

    def test_same_field_direct_local_clause_and_reference_can_coexist(self):
        data = referenced_source(local_fact=True)
        c.validate(data)
        units = [u for u in proof_of(data)['source_units'] if u['pointer'] == '/content/render_gates/0']
        self.assertEqual({u['disposition'] for u in units}, {'semantic', 'semantic_reference'})
        self.assertEqual(next(u for u in units if u['disposition'] == 'semantic')['fact_refs'], ['local_face'])

    def test_full_and_compact_keep_qualification_admission_and_lock_scope(self):
        data = referenced_source()
        record = data['candidates'][A]
        c.validate(data)
        guarded = layout.guard_record(record, data)
        self.assertNotIn('source_units', guarded['_semantic_evidence_guard'])
        self.assertEqual(e.qualification(data['slot_catalog']['light_direction'], record),
                         e.qualification(data['slot_catalog']['light_direction'], guarded))
        present = ('subject', 'face_A', 'anatomy.face.presence', 'present')
        for view in [data, {**data, 'candidates': {A: guarded}}]:
            entry = c.entry(view, A)
            def eligible(frozen):
                return g.core_entry_eligible(view, frozen,
                    {'subject_category': 'object', 'intent_constraints': {'domains': []}},
                    {'subject': {}}, '', entry)
            for frozen, allowed in [
                (core(['face_A'], [present]), True),
                (core(['face_A']), False),
                (core(['face_A', 'face_B'], [('subject', 'face_B', 'anatomy.face.presence', 'present')]), False),
            ]:
                self.assertEqual(e.admission(entry, frozen)['allowed'], allowed)
            locked = core(['face_A'], [present])
            locked['intent_lock']['semantic_anchors'] = [
                {'dimension': 'lighting', 'target': 'face_A', 'property': 'lighting.direction'}]
            self.assertFalse(e.property_scope_allowed(locked, entry['affected_dimensions'],
                             entry['affected_properties'], record=entry))
            self.assertFalse(eligible(locked))
            whole_locked = core(['face_A'], [present])
            self.assertTrue(eligible(whole_locked))
            whole_locked['intent_lock']['open_dimensions'].remove('lighting')
            whole_locked['intent_lock']['locked_dimensions'].append('lighting')
            self.assertFalse(eligible(whole_locked))

    def test_reference_preserves_known_absent_present_unknown_source_guards(self):
        from tests.test_photo_native_v4_guards import guarded, preserve, scoped_core
        data = guarded([preserve()])
        record = data['candidates'][A]
        record['content']['render_gates'] = ['Keep this selected standing pose readable.']
        seal(data, {'test_role': ['effect']})
        p = proof_of(data)
        p['source_units'] = [u for u in p['source_units'] if u['pointer'] != '/content/render_gates/0']
        p['source_units'].append(reference('/content/render_gates/0', record['content']['render_gates'][0], ['effect']))
        reattest(data)
        c.validate(data)
        guards_before = copy.deepcopy(p['guard_sets'])
        for view in [data, {**data, 'candidates': {A: layout.guard_record(record, data)}}]:
            entry = c.entry(view, A)
            for state, allowed in [('known_absent', True), ('known_present', True), ('unknown', False)]:
                frozen = scoped_core(state, has_value=state != 'known_absent')
                self.assertEqual(e.admission(entry, frozen)['allowed'], allowed)
            self.assertEqual(entry['_semantic_evidence_guard']['guard_sets'], guards_before)

    def test_reference_and_rationale_are_bound_by_full_and_compact_fingerprints(self):
        for key, value in [('reference_relation', 'partial_restatement'),
                           ('retained_constraint_rationale', 'A newly reviewed explicit local constraint.')]:
            data = referenced_source()
            record = data['candidates'][A]
            old_hash = e.native_contract_sha256(proof_of(data))
            old_compact = e.compact(record, data)
            ref_of(data)[key] = value
            self.assertNotEqual(e.native_contract_sha256(proof_of(data)), old_hash)
            self.assertEqual(e.qualification(data['slot_catalog']['light_direction'], record)['native_qualification'], 'invalid')
            with self.assertRaises(ValueError):
                e.compact(record, data)
            reattest(data)
            c.validate(data)
            fresh = e.compact(record, data)
            self.assertEqual(fresh['facts'], old_compact['facts'])
            self.assertNotEqual(fresh['qualification_sha256'], old_compact['qualification_sha256'])
            self.assertNotEqual(fresh['compact_sha256'], old_compact['compact_sha256'])

    def test_exact_shape_relation_rationale_and_nonempty_unique_refs(self):
        mutations = [lambda u: u.update(reference_relation='invented_relation'),
                     lambda u: u.update(reference_relation=[]),
                     lambda u: u.update(retained_constraint_rationale=' '),
                     lambda u: u.update(retained_constraint_rationale=3),
                     lambda u: u.pop('retained_constraint_rationale'),
                     lambda u: u.update(candidate_id='cand_' + 'b' * 32),
                     lambda u: u.update(fact_refs=[]),
                     lambda u: u.update(fact_refs=['underlight', 'underlight']),
                     lambda u: u.update(fact_refs=['missing']),
                     lambda u: u.update(quote='selected illumination'),
                     lambda u: u.update(pointer=[])]
        for i, mutate in enumerate(mutations):
            with self.subTest(case=i):
                data = referenced_source()
                mutate(ref_of(data))
                self.assert_rejected(data)

    def test_metadata_and_unenumerated_primary_surfaces_cannot_be_reference_sources(self):
        for key in ['aliases', 'tags', 'provenance', 'unreviewed_extra']:
            data = referenced_source()
            gate = ref_of(data)['quote']
            data['candidates'][A]['content'][key] = [gate]
            ref_of(data)['pointer'] = '/content/' + key + '/0'
            proof_of(data)['meaning_sha256'] = e.meaning_sha256(data['candidates'][A])
            with self.subTest(key=key):
                self.assert_rejected(data)

    def test_metadata_cannot_supply_the_canonical_anchor(self):
        for key in ['aliases', 'unreviewed_extra']:
            data = referenced_source()
            record = data['candidates'][A]
            record['content'][key] = record['content']['en']
            for f in proof_of(data)['facts']:
                f['pointer'] = '/content/' + key
            direct_of(data)['pointer'] = '/content/' + key
            proof_of(data)['meaning_sha256'] = e.meaning_sha256(record)
            with self.subTest(key=key):
                self.assert_rejected(data)

    def test_duplicate_normal_or_reference_units_and_nonsemantic_conflict_reject(self):
        for disposition in ['semantic', 'semantic_reference', 'nonsemantic']:
            data = referenced_source()
            if disposition == 'nonsemantic':
                u = {k: ref_of(data)[k] for k in e.SOURCE_UNIT_FIELDS}
                u.update(disposition='nonsemantic', fact_refs=[])
            else:
                u = copy.deepcopy(ref_of(data) if disposition == 'semantic_reference' else direct_of(data))
            proof_of(data)['source_units'].append(u)
            with self.subTest(disposition=disposition):
                self.assert_rejected(data)

    def test_references_share_existing_unit_budget_and_do_not_extend_it(self):
        data = referenced_source()
        self.assertEqual(len(proof_of(data)['source_units']), 2)
        with mock.patch.object(e, 'MAX_UNITS', 2):
            c.validate(data)
        with mock.patch.object(e, 'MAX_UNITS', 1):
            self.assert_rejected(data)

    def test_self_reference_and_chain_or_cycle_cannot_ground_a_fact(self):
        data = referenced_source()
        ref_of(data).update(pointer='/content/en', quote=data['candidates'][A]['content']['en'])
        self.assert_rejected(data)
        for cycle in [False, True]:
            data = referenced_source()
            p = proof_of(data)
            # The only direct supporting unit is removed. A reference pointing
            # to a fact at another reference field cannot support that fact.
            p['source_units'].remove(direct_of(data))
            p['source_units'].append(reference('/content/en', data['candidates'][A]['content']['en'], ['face']))
            if cycle:
                p['facts'][0].update(pointer='/content/render_gates/0', quote='same face')
            with self.subTest(cycle=cycle):
                self.assert_rejected(data)

    def test_normal_unit_must_directly_cover_every_fact_at_its_own_exact_source(self):
        for defect in ['omitted_fact', 'wrong_pointer', 'short_unit_quote', 'reference_only_orphan']:
            data = referenced_source()
            if defect == 'omitted_fact':
                direct_of(data)['fact_refs'].remove('underlight')
            elif defect == 'wrong_pointer':
                proof_of(data)['facts'][1].update(pointer='/content/render_gates/0', quote='selected illumination')
            elif defect == 'short_unit_quote':
                direct_of(data)['quote'] = 'illuminated from below'
            else:
                ref_of(data)['fact_refs'].append('orphan')
                proof_of(data)['facts'].append(fact('orphan', 'subject', 'face', 'anatomy.face.presence',
                    'prerequisite', 'present', [], pointer='/content/render_gates/0', quote='same face'))
            with self.subTest(defect=defect):
                self.assert_rejected(data)

    def test_reference_does_not_waive_effect_role_owner_or_guard_contracts(self):
        mutations = [lambda p: p['facts'].pop(),
                     lambda p: p['effect_sets']['base'].update(properties=[]),
                     lambda p: p['roles']['light_direction'].update(fact_refs=['missing']),
                     lambda p: p['owner_maps']['base']['bindings'].clear(),
                     lambda p: p['guard_sets']['base'].update(invented=True),
                     lambda p: p['profile_contracts'].update(base={'invented': True})]
        for i, mutate in enumerate(mutations):
            data = referenced_source()
            mutate(proof_of(data))
            with self.subTest(case=i):
                self.assert_rejected(data)

    def test_canonical_fact_id_is_local_to_this_proof_not_an_external_cid(self):
        data = referenced_source()
        ref_of(data)['fact_refs'] = ['cand_' + 'b' * 32 + ':underlight']
        self.assert_rejected(data)

    def test_same_common_field_requires_separate_same_rid_direct_anchors(self):
        data = referenced_source()
        record = data['candidates'][A]
        p = proof_of(data)
        branches = []
        rows = []
        for rid in ['left', 'right']:
            branches.append({'id': rid, 'conditions': {}, 'context_terms': [],
                             'effects': {'dimensions': [], 'properties': []}})
            for old in p['facts']:
                f = copy.deepcopy(old)
                f.update(id=rid + '_' + old['id'], realization_id=rid,
                         requires=[rid + '_' + ref for ref in old['requires']])
                rows.append(f)
        record['effects']['realizations'] = {'mode': 'one', 'branches': branches}
        p['facts'] = rows
        p['owner_maps'] = {rid: owner_map(('face', 'primary_face')) for rid in ['left', 'right']}
        seal(data, {'light_direction': ['left_underlight', 'right_underlight']})
        p['source_units'] = [u for u in p['source_units'] if u['pointer'] != '/content/render_gates/0']
        for rid in ['left', 'right']:
            p['source_units'].append(reference('/content/render_gates/0', record['content']['render_gates'][0],
                                               [rid + '_underlight'], rid=rid))
        reattest(data)
        c.validate(data)
        # A common field is not a permission to borrow a sibling RID's fact.
        ref_of(data)['fact_refs'] = ['right_underlight']
        self.assert_rejected(data)

    def test_unselected_sibling_positive_projection_is_rejected(self):
        # positive_string enforces this boundary before canonical anchor lookup.
        data = referenced_source()
        record = data['candidates'][A]
        record['content']['realization_content'] = {'base': {'en': record['content']['en']},
                                                    'other': {'en': ref_of(data)['quote']}}
        ref_of(data)['pointer'] = '/content/realization_content/other/en'
        proof_of(data)['meaning_sha256'] = e.meaning_sha256(record)
        self.assert_rejected(data)


if __name__ == '__main__':
    unittest.main()
