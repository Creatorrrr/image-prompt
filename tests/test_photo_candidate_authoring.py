import copy
import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'skills/photo-prompt-image-generator/scripts'))
from photo_candidate_authoring import digest
from photo_candidate_review import validate, SCHEMA
from photo_candidate_documents import project, field_index


def fixture():
    record = {'id': 'cand_'+'a'*32, 'meaning': {'primary': {'base': {'/visible': 'u'}},
        'literals': {'u': 'a narrow line follows the rear surface of the stocking'}, 'retrieval_class': 'positive'}}
    anchor = {'pointer': '/visible', 'quote': record['meaning']['literals']['u']}
    row = {'schema': SCHEMA, 'candidate_id': record['id'], 'source_sha256': digest(record),
        'decision': 'enrich', 'rationale': 'Make the visible surface relation readable.',
        'realizations': {'base': {'summary_en': 'A stocking has a narrow line running along its rear surface.',
            'summary_ko': '스타킹의 뒤 표면을 따라 가는 선이 이어진다.', 'anchors': [anchor],
            'facets': [{'kind': 'relation', 'text_en': 'The line follows the stocking surface.', 'anchors': [anchor]}],
            'search_aliases': [], 'unknowns': ['The source does not establish physical stitching.']}},
        'slot_tags': [], 'review': {'author': 'gpt-6-luna', 'effort': 'max', 'source_only': True, 'native_approval': False}}
    return record, row


class SourceReview(unittest.TestCase):
    def test_source_and_anchors_are_bound(self):
        record, row = fixture();self.assertIs(validate(row, record, {}), row)
        for path in ['source', 'quote', 'rid', 'authority']:
            bad = copy.deepcopy(row)
            if path == 'source': bad['source_sha256'] = 'b'*64
            elif path == 'quote': bad['realizations']['base']['anchors'][0]['quote'] = 'a stitched seam'
            elif path == 'rid': bad['realizations']['other'] = bad['realizations'].pop('base')
            else: bad['review']['native_approval'] = True
            with self.assertRaises(ValueError): validate(bad, record, {})

    def test_unknown_discovery_slot_rejected(self):
        record, row = fixture();row['slot_tags'] = [{'slot_id': 'invented', 'realization_id': 'base',
            'rationale': 'test', 'anchors': row['realizations']['base']['anchors']}]
        with self.assertRaises(ValueError): validate(row, record, {})

    def test_original_D_is_exact_prefix_and_native_record_is_unchanged(self):
        record, row = fixture();before = copy.deepcopy(record)
        fields = {'labels': ['original cue'], 'core_meaning': [], 'aliases': []}
        result = project('original cue', fields, record, 'base', {'parts': []},
                         arm='C', selected=True, review=row, catalog={})
        self.assertTrue(result['text'].startswith('original cue\n'))
        self.assertIn(row['realizations']['base']['summary_en'], result['fields']['core_meaning'])
        self.assertEqual(record, before);self.assertEqual(fields['core_meaning'], [])

    def test_unselected_and_deferred_sources_keep_original_input(self):
        record, row = fixture();fields = {'labels': ['cue'], 'core_meaning': [], 'aliases': []}
        for selected, decision in [(False, 'enrich'), (True, 'defer'), (True, 'needs_semantic_edit'), (True, 'retain')]:
            row['decision'] = decision
            result = project('cue', fields, record, 'base', {'parts': []}, arm='C', selected=selected, review=row, catalog={})
            self.assertEqual(result['text'], 'cue')

    def test_existing_manifestation_needs_exact_primary_ground(self):
        record, _ = fixture();value = record['meaning']['literals']['u']
        parts = {'parts': [{'text': value, 'sources': [{'role': 'source_manifestations'}]},
                           {'text': 'unproved physical seam', 'sources': [{'role': 'source_manifestations'}]}]}
        fields = {'labels': ['cue'], 'core_meaning': [], 'aliases': []}
        result = project('cue', fields, record, 'base', parts, arm='B', selected=True)
        self.assertEqual(result['fields']['core_meaning'], [value])

    def test_global_DF_lengths_and_nonempty_population(self):
        configs = {'labels': {'weight': 3, 'b': .75}, 'core_meaning': {'weight': 2, 'b': .75, 'normalization_population': 'nonempty_documents'}}
        documents = [{'fields': {'labels': ['one'], 'core_meaning': ['same same']}},
                     {'fields': {'labels': ['two'], 'core_meaning': []}},
                     {'fields': {'labels': ['same'], 'core_meaning': []}}]
        index = field_index(documents, configs)
        self.assertEqual(index['n'], 3);self.assertEqual(index['average_lengths']['core_meaning'], 2)
        self.assertEqual(len(index['postings']['same']), 2)
        self.assertEqual(index['nonempty_counts']['core_meaning'], 1)

    def test_diagnostic_cannot_become_positive_by_annotation(self):
        record, row = fixture();record['meaning']['retrieval_class'] = 'diagnostic';row['source_sha256'] = digest(record)
        with self.assertRaises(ValueError): validate(row, record, {})

if __name__ == '__main__': unittest.main()
