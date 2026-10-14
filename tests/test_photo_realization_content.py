"""An explicitly selected primitive alternative cannot render another body."""
import copy
import unittest

from tests.test_photo_candidate_corpus import fixture, A
import photo_candidate_corpus as c
import photo_candidate_realizations as r
import photo_global_index as index
import photo_search_layout as layout
import prompt_generator as g


def source():
    data = fixture();record = data['candidates'][A]
    record['content'] = {'en': 'standing or walking', 'ko': '서 있거나 걷는',
        'embedding_text': 'standing or walking', 'aliases': ['standing or walking'],
        'keywords': ['walking'], 'concept_units': ['standing or walking'],
        'realization_content': {rid: {'en': en, 'ko': ko, 'embedding_text': en,
            'concept_units': [en], 'relations': []}
            for rid, en, ko in [('standing', 'a standing adult', '서 있는 성인'),
                               ('walking', 'a walking adult', '걷는 성인')]}}
    record['effects'] = {'dimensions': [], 'properties': [],
        'realizations': {'mode': 'one', 'branches': [
            {'id': rid, 'conditions': {}, 'context_terms': [],
             'effects': {'dimensions': ['pose'], 'properties': [
                 {'dimension': 'pose', 'target': 'main_subject', 'property': 'body.pose.' + rid}]}}
            for rid in ['standing', 'walking']]}}
    return data


class RealizationContentTests(unittest.TestCase):
    def test_selected_text_and_properties_exclude_the_other_primitive_choice(self):
        data = source();before = copy.deepcopy(data);c.validate(data)
        entry = c.entry(data, A, realization_id='standing')
        self.assertEqual(entry['en'], 'a standing adult')
        self.assertEqual(entry['ko'], '서 있는 성인')
        self.assertEqual(entry['concept_units'], ['a standing adult'])
        self.assertNotIn('walking', g.candidate_pack_entry_blob(entry, [entry['embedding_text']]))
        self.assertEqual(entry['affected_properties'][0]['property'], 'body.pose.standing')
        self.assertNotIn('realization_content', entry)
        self.assertEqual(data, before)

    def test_projection_does_not_add_or_duplicate_a_search_document_or_ranking_text(self):
        data = source();without = copy.deepcopy(data)
        without['candidates'][A]['content'].pop('realization_content')
        self.assertEqual(index.documents(data), index.documents(without))
        self.assertEqual(index.text(data['candidates'][A]), index.text(without['candidates'][A]))

    def test_lazy_guard_and_payload_select_identical_positive_text(self):
        data = source();record = data['candidates'][A]
        lazy = {**data, 'candidates': {A: layout.guard_record(record)}}
        for rid in r.ids(record):
            full, compact = c.entry(data, A, realization_id=rid), c.entry(lazy, A, realization_id=rid)
            self.assertEqual(g.candidate_pack_entry_blob(full, [full['embedding_text']]),
                             g.candidate_pack_entry_blob(compact, [compact['embedding_text']]))

    def test_foreign_missing_or_guard_overriding_primitive_text_is_rejected(self):
        for defect in ['missing', 'foreign', 'guard', 'identity', 'empty', 'unconditional']:
            data = source();record = data['candidates'][A];choices = record['content']['realization_content']
            if defect == 'missing':
                choices.pop('walking')
            elif defect == 'foreign':
                choices['invented'] = copy.deepcopy(choices['walking'])
            elif defect == 'guard':
                choices['standing']['conditions'] = {}
            elif defect == 'identity':
                choices['standing']['id'] = 'another-candidate'
            elif defect == 'empty':
                choices['standing']['concept_units'] = []
            else:
                record['effects'].pop('realizations')
            with self.subTest(defect=defect), self.assertRaises(ValueError):
                c.validate(data)


def mechanism_source():
    """An isolated projection fixture from the fully read 12165 definition.

    This does not amend or approve the frozen candidate or supply native effects.
    """
    data = fixture(); record = data['candidates'][A]
    definition = ('Subtle practical makeup or motivated reflected color appears on the cheeks '
                  'while other social-action evidence remains visible.')
    record['record_kind'] = 'relationship_mechanism'
    record['conditions'] = {'requires_adult_context': True}
    record['content'] = {'definition': definition, 'family_ids': ['affect_expression_gaze'],
        'priority_dimension': 'observable_action', 'role': 'visual_atom',
        'topic_ids': ['expression_manga_symbol_translation']}
    definitions = {
        'practical_makeup': ('Subtle practical makeup appears on the cheeks while other '
                             'social-action evidence remains visible.'),
        'reflected_color': ('Motivated reflected color appears on the cheeks while other '
                            'social-action evidence remains visible.')}
    korean = {'practical_makeup': '다른 사회적 행동 증거가 보이는 동안 볼에 미묘한 실용적 화장이 나타난다.',
              'reflected_color': '다른 사회적 행동 증거가 보이는 동안 볼에 동기가 있는 반사색이 나타난다.'}
    record['content']['realization_content'] = {rid: {'en': text, 'ko': korean[rid],
        'embedding_text': text, 'concept_units': [text], 'relations': [], 'definition': text}
        for rid, text in definitions.items()}
    record['effects'] = {'dimensions': [], 'properties': [], 'realizations': {'mode': 'one',
        'branches': [{'id': rid, 'conditions': {}, 'context_terms': [],
                      'effects': {'dimensions': [], 'properties': []}} for rid in definitions]}}
    return data


class MechanismRealizationContentTests(unittest.TestCase):
    def test_each_selected_full_definition_and_render_excludes_the_other_choice(self):
        data = mechanism_source(); before = copy.deepcopy(data); c.validate(data)
        for rid, excluded in [('practical_makeup', 'reflected'), ('reflected_color', 'makeup')]:
            entry = c.entry(data, A, realization_id=rid)
            expected = data['candidates'][A]['content']['realization_content'][rid]
            self.assertEqual(entry['definition'], expected['definition'])
            self.assertEqual(entry['en'], expected['en'])
            self.assertEqual(entry['concept_units'], expected['concept_units'])
            self.assertNotIn(excluded, g.candidate_pack_entry_blob(entry, [entry['embedding_text']]))
            positive = index.text({'record_kind': entry['record_kind'], 'content': entry})[1]
            self.assertNotIn(excluded, positive)
            self.assertNotIn(' or ', positive)
            self.assertNotIn('realization_content', entry)
            self.assertEqual(entry['id'], A)
            self.assertEqual(entry['record_kind'], 'relationship_mechanism')
            self.assertTrue(entry['requires_adult_context'])
            self.assertEqual(entry['affected_dimensions'], [])
            self.assertEqual(entry['affected_properties'], [])
        self.assertEqual(data, before)
        self.assertEqual(data['candidates'][A]['provenance'], before['candidates'][A]['provenance'])

    def test_full_search_document_retains_original_or_and_is_not_duplicated(self):
        data = mechanism_source(); without = copy.deepcopy(data)
        without['candidates'][A]['content'].pop('realization_content')
        self.assertEqual(index.documents(data), index.documents(without))
        self.assertEqual(index.text(data['candidates'][A]), index.text(without['candidates'][A]))
        full = index.text(data['candidates'][A])[1]
        self.assertIn('makeup or motivated reflected color', full)
        self.assertEqual(set(index.documents(data)), set(index.documents(without)))
        unselected = c.entry(data, A)
        self.assertEqual(unselected['definition'], data['candidates'][A]['content']['definition'])

    def test_lazy_entry_and_direct_projection_keep_the_same_selected_definition(self):
        data = mechanism_source(); record = data['candidates'][A]
        lazy = {**data, 'candidates': {A: layout.guard_record(record)}}
        for rid in r.ids(record):
            expected = r.project_content(record, rid)
            full, compact = c.entry(data, A, realization_id=rid), c.entry(lazy, A, realization_id=rid)
            self.assertEqual(full['definition'], expected['definition'])
            self.assertEqual(compact['definition'], expected['definition'])
            self.assertEqual(g.candidate_pack_entry_blob(full, [full['embedding_text']]),
                             g.candidate_pack_entry_blob(compact, [compact['embedding_text']]))

    def test_presented_selected_view_overrides_original_or_definition(self):
        data = mechanism_source(); record = data['candidates'][A]
        candidate = {**c.entry(data, A), 'authored_record': record,
            'realization_views': {rid: c.entry(data, A, realization_id=rid) for rid in r.ids(record)}}
        for rid, excluded in [('practical_makeup', 'reflected'), ('reflected_color', 'makeup')]:
            selected = r.selected_view(candidate, {'realization_id': rid})
            self.assertNotIn(excluded, selected['definition'].lower())
            self.assertNotIn(excluded, index.text({'record_kind': selected['record_kind'], 'content': selected})[1])
            self.assertEqual(selected['record_kind'], record['record_kind'])
            self.assertEqual(selected['authored_record'], record)
        self.assertIn('makeup or motivated reflected color', candidate['definition'])

    def test_exact_per_kind_schema_rejects_missing_empty_malformed_or_foreign_fields(self):
        for defect in ('missing_definition', 'empty_definition', 'list_definition', 'foreign_rid',
                       'missing_rid', 'duplicate_rid', 'guard', 'identity', 'kind', 'provenance',
                       'metadata', 'other_kind', 'invalid_concept_units', 'invalid_relations'):
            data = mechanism_source(); record = data['candidates'][A]
            choices = record['content']['realization_content']; selected = choices['practical_makeup']
            if defect == 'missing_definition': selected.pop('definition')
            elif defect == 'empty_definition': selected['definition'] = ' '
            elif defect == 'list_definition': selected['definition'] = ['selected']
            elif defect == 'foreign_rid': choices['invented'] = copy.deepcopy(selected)
            elif defect == 'missing_rid': choices.pop('reflected_color')
            elif defect == 'duplicate_rid': record['effects']['realizations']['branches'][1]['id'] = 'practical_makeup'
            elif defect == 'guard': selected['conditions'] = {'requires_adult_context': False}
            elif defect == 'identity': selected['id'] = A
            elif defect == 'kind': selected['record_kind'] = 'visual_option'
            elif defect == 'provenance': selected['provenance'] = []
            elif defect == 'metadata': selected['family_ids'] = []
            elif defect == 'other_kind': record['record_kind'] = 'visual_bundle'
            elif defect == 'invalid_concept_units': selected['concept_units'] = 'selected'
            else: selected['relations'] = ['untyped relation']
            with self.subTest(defect=defect), self.assertRaises(ValueError):
                c.validate(data)

    def test_unprojected_positive_source_fields_are_rejected_instead_of_hidden(self):
        surfaces = {'ja': 'makeup or reflected color', 'label_en': 'makeup or reflected color',
            'label_ko': '화장 또는 반사색', 'definitions_by_topic': {'test': 'makeup or reflected color'},
            'manifestations': ['makeup or reflected color'],
            'components': [{'id': 'both', 'concept_units': ['makeup or reflected color']}],
            'member_candidates': [{'candidate_id': A}], 'embedding_texts': ['makeup or reflected color'],
            'concept_candidate': {'concept_terms': ['makeup or reflected color']},
            'semantics': {'definition': 'makeup or reflected color'}}
        for key, value in surfaces.items():
            data = mechanism_source(); record = data['candidates'][A]; record['content'][key] = value
            with self.subTest(key=key):
                with self.assertRaisesRegex(ValueError, 'unprojected positive source fields'):
                    r.validate_content(record)
                with self.assertRaisesRegex(ValueError, 'unprojected positive source fields'):
                    c.entry(data, A, realization_id='practical_makeup')

    def test_canonical_discovery_aliases_remain_searchable_but_cannot_leak_to_render(self):
        data = mechanism_source(); record = data['candidates'][A]
        record['content']['semantics'] = {'claim_limits': ['Neither source branch proves private emotion.']}
        for key in ('aliases', 'keywords', 'terms', 'paraphrases', 'concept_terms'):
            record['content'][key] = ['makeup or reflected color']
        c.validate(data)
        self.assertIn('makeup or reflected color', index.text(record)[1])
        entry = c.entry(data, A, realization_id='practical_makeup')
        self.assertEqual(entry['semantics'], record['content']['semantics'])
        for key in ('aliases', 'keywords', 'terms', 'paraphrases', 'concept_terms'):
            self.assertEqual(entry[key], [])
        self.assertNotIn('reflected', index.text({'record_kind': entry['record_kind'], 'content': entry})[1])

    def test_mechanism_quote_cannot_be_borrowed_from_a_sibling_definition(self):
        import photo_semantic_evidence as evidence
        record = mechanism_source()['candidates'][A]
        self.assertEqual(evidence.positive_string(record,
            '/content/realization_content/practical_makeup/definition', realization_id='practical_makeup'),
            record['content']['realization_content']['practical_makeup']['definition'])
        with self.assertRaises(ValueError):
            evidence.positive_string(record, '/content/realization_content/reflected_color/definition',
                                     realization_id='practical_makeup')

    def test_optional_base_is_an_explicit_selected_body_and_guards_remain_separate(self):
        data = mechanism_source(); record = data['candidates'][A]
        record['effects']['realizations']['mode'] = 'optional'
        with self.assertRaises(ValueError): r.validate_content(record)
        record['content']['realization_content']['base'] = {
            'en': 'Other social-action evidence remains visible.', 'ko': '다른 사회적 행동 증거가 보인다.',
            'definition': 'Other social-action evidence remains visible.',
            'embedding_text': 'Other social-action evidence remains visible.',
            'concept_units': ['Other social-action evidence remains visible.'], 'relations': []}
        record['effects']['realizations']['branches'][0]['conditions'] = {'requires_adult_context': True}
        before = copy.deepcopy(record); c.validate(data)
        base = c.entry(data, A, realization_id='base')
        self.assertNotIn('makeup', base['definition']); self.assertNotIn('reflected', base['definition'])
        self.assertTrue(base['requires_adult_context'])
        self.assertEqual(record, before)
        self.assertEqual(r.branch(record, 'practical_makeup')['conditions'], {'requires_adult_context': True})

    def test_existing_visual_option_contract_still_rejects_mechanism_only_definition(self):
        data = source()
        data['candidates'][A]['content']['realization_content']['standing']['definition'] = 'Selected definition.'
        with self.assertRaises(ValueError): c.validate(data)


if __name__ == '__main__':
    unittest.main()
