"""Selected source meanings must survive the single-query material view."""
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

SKILL = Path(__file__).resolve().parents[1]
NATIVE = os.environ.get('PHOTO_H_F2_TEST_NATIVE')
if NATIVE:
    sys.path.insert(0, str(Path(NATIVE) / 'scripts'))
    sys.path.insert(0, str(SKILL / 'runtime-overlays/age-neutral-compact-v4/scripts'))
    import photo_h_f2_workflow as workflow
    import photo_h_f2_receipts as receipts
    import photo_candidate_realizations as realizations
    import compose_pack_view


@unittest.skipUnless(NATIVE, 'requires installed H-F2 dependencies')
class CompleteMeaningTest(unittest.TestCase):
    def project(self, native, units, *, conditions=None, effects=None, rid='base'):
        source = {'conditions': conditions or {}, 'effects': effects or {'dimensions': [], 'properties': []}}
        with patch.object(workflow.canonical, 'native', return_value=native), \
             patch.object(workflow.canonical, 'units', return_value=units):
            return workflow.compact_material(source, {'cid': 'cand_x', 'rid': rid})

    def test_short_label_never_hides_complete_definition(self):
        units = {'/content/en': 'Shadow pedestal — shadow owner',
                 '/content/definition': 'A three-footed object casts a branching tower shadow.',
                 '/content/application_contract': 'Preserve the entire definition.'}
        row = self.project({'application_contract': 'Preserve the entire definition.'}, units)
        self.assertIn(units['/content/en'], row['meaning'])
        self.assertIn(units['/content/definition'], row['meaning'])
        self.assertEqual(row['application_contract'], units['/content/application_contract'])

    def test_components_and_relation_endpoints_are_kept_with_their_roles(self):
        units = {'/content/en': 'sorting clothes before a wash',
                 '/content/ko': '세탁 전 옷 정리',
                 '/content/concept_units/0': 'A person sorts garments into two laundry groups.',
                 '/content/concept_units/1': 'A machine or basket marks the next step.',
                 '/content/relations/0/subject': 'person',
                 '/content/relations/0/type': 'sorts_into',
                 '/content/relations/0/object': 'two laundry groups'}
        out = self.project({}, units)['meaning']
        for value in units.values():self.assertIn(value, out)
        self.assertIn('[relations/0/subject] person', out)
        self.assertIn('[relations/0/type] sorts_into', out)
        self.assertIn('[relations/0/object] two laundry groups', out)

    def test_preserves_evidence_context_without_promoting_search_hints(self):
        units = {'/content/en': 'A subject.', '/content/embedding_text': 'lookup tokens',
                 '/content/paraphrases/0': 'search-only alternate',
                 '/content/authored_components/obligations/0/evidence/0/requirement/must_not_contain/0': 'girl'}
        out = self.project({}, units)['meaning']
        self.assertNotIn('lookup tokens', out)
        self.assertNotIn('search-only alternate', out)
        self.assertIn('[authored_components/obligations/0/evidence/0/requirement/must_not_contain/0] girl', out)

    def test_selected_branch_does_not_emit_other_branch(self):
        dress = 'A pink inner sheath belongs to the dress.'
        bustier = 'A nude jersey layer belongs to the bustier.'
        effects = {'dimensions': [], 'properties': [], 'realizations': {'mode': 'one', 'branches': [
            {'id': 'dress', 'component_units': {'garment': [dress]}, 'conditions': {}},
            {'id': 'bustier', 'component_units': {'garment': [bustier]}, 'conditions': {}}]}}
        units = {'/content/components/0/concept_units/0': dress,
                 '/content/components/0/concept_units/1': bustier,
                 '/content/relations/0/subject': 'one selected garment'}
        out = self.project({}, units, effects=effects, rid='dress')['meaning']
        self.assertIn(dress, out)
        self.assertNotIn(bustier, out)
        self.assertIn('one selected garment', out)

    def test_selected_branch_appends_its_specific_units(self):
        effects = {'dimensions': [], 'properties': [], 'realizations': {'mode': 'optional', 'branches': [
            {'id': 'playback', 'concept_units': ['Signal dropout appears in the playback image.'], 'conditions': {}}]}}
        out = self.project({}, {'/content/en': 'Physical tape is stretched.'}, effects=effects, rid='playback')['meaning']
        self.assertIn('Physical tape is stretched.', out)
        self.assertIn('Signal dropout appears in the playback image.', out)

    def test_base_does_not_lose_a_unit_shared_with_an_optional_branch(self):
        shared = 'The physical tape carrier has visible stretch.'
        effects = {'dimensions': [], 'properties': [], 'realizations': {'mode': 'optional', 'branches': [
            {'id': 'playback', 'concept_units': [shared, 'Dropout is shown in playback.'], 'conditions': {}}]}}
        out = self.project({}, {'/content/concept_units/0': shared}, effects=effects)['meaning']
        self.assertIn(shared, out)
        self.assertNotIn('Dropout is shown in playback.', out)

    def test_selected_branch_conditions_fail_closed_instead_of_disappearing(self):
        effects = {'dimensions': [], 'properties': [], 'realizations': {'mode': 'one', 'branches': [
            {'id': 'branch', 'concept_units': ['One scene.'], 'conditions': {'for_any': ['human']}}]}}
        with self.assertRaises(ValueError):
            self.project({}, {'/content/en': 'One scene.'}, effects=effects, rid='branch')

    def test_authored_realization_projection_supplies_only_selected_content(self):
        effects = {'dimensions': [], 'properties': [], 'realizations': {'mode': 'one', 'branches': [
            {'id': 'a', 'concept_units': ['A selected scene.'], 'conditions': {}},
            {'id': 'b', 'concept_units': ['A different scene.'], 'conditions': {}}]}}
        projected = {'en': 'A selected scene.', 'ko': '선택된 장면.',
                     'concept_units': ['A selected scene.'], 'relations': []}
        with patch.object(realizations, 'project_content', return_value=projected):
            out = self.project({'realization_content': {'a': {}, 'b': {}}},
                               {'/content/en': 'Parent describes both alternatives.'},
                               effects=effects, rid='a')['meaning']
        self.assertIn('A selected scene.', out)
        self.assertIn('선택된 장면.', out)
        self.assertNotIn('A different scene.', out)
        self.assertNotIn('Parent describes both alternatives.', out)

    def test_research_visual_relations_are_labeled_as_non_native_metadata(self):
        research = {'owners': [{'id': 'drummer', 'visible_component_en': 'one adult with a hand drum'}],
                    'relations': [{'subject': 'drummer', 'predicate': 'faces', 'object': 'dancers'}],
                    'source_refs': [{'url': 'https://example.invalid/source'}], 'native_approval': False}
        out = self.project({'research_semantics': research}, {'/content/en': 'A drummer faces dancers.'})['meaning']
        self.assertIn('one adult with a hand drum', out)
        self.assertIn('"predicate":"faces"', out)
        self.assertIn('optional review metadata, not native adoption authority', out)
        self.assertNotIn('https://example.invalid', out)

    def test_research_metadata_does_not_leak_unbound_sibling_branches(self):
        effects = {'dimensions': [], 'properties': [], 'realizations': {'mode': 'one', 'branches': [
            {'id': 'branch', 'concept_units': ['One scene.'], 'conditions': {}}]}}
        with self.assertRaises(ValueError):
            self.project({'research_semantics': {'positive_en': 'Possibly another alternative.'}},
                         {'/content/en': 'One scene.'}, effects=effects, rid='branch')

    def test_mixed_sibling_literal_fails_closed(self):
        effects = {'dimensions': [], 'properties': [], 'realizations': {'mode': 'one', 'branches': [
            {'id': 'a', 'concept_units': ['red dress'], 'conditions': {}},
            {'id': 'b', 'concept_units': ['blue dress'], 'conditions': {}}]}}
        with self.assertRaises(ValueError):
            self.project({}, {'/content/en': 'Choose a red dress or a blue dress.'}, effects=effects, rid='a')

    def test_view_keeps_conditions_and_contract_and_no_extra_search(self):
        source = {'conditions': {'requires_adult_context': True}, 'effects': {'dimensions': [], 'properties': []}}
        packet = {'goals': {'topic': {'candidates': [{'cid': 'cand_x', 'rid': 'base'}]}},
                  'sources': {'cand_x': source}, 'query_set': {'query_scopes': {'topic': 'slot'}}}
        with patch.object(receipts, 'verify_bound', return_value=packet), \
             patch.object(workflow.canonical, 'native', return_value={'application_contract':'Keep it.'}), \
             patch.object(workflow.canonical, 'units', return_value={'/content/en':'An adult.', '/content/definition':'An adult faces a group.'}), \
             patch.object(workflow, 'value', return_value={'contract_version':'photo-validation-context/v1'}), \
             patch.object(compose_pack_view, 'build_view', return_value={}):
            out = workflow.view({})
        row = out['materials']['topic'][0]
        self.assertEqual(out['schema'], 'photo-h-f2-compact-material-view/v3')
        self.assertIn('An adult faces a group.', row['meaning'])
        self.assertEqual(row['conditions'], source['conditions'])
        self.assertEqual(row['application_contract'], 'Keep it.')
        self.assertEqual(out['additional_search_calls'], 0)


if __name__ == '__main__':unittest.main()
