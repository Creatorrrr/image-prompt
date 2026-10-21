"""Current example-free authoring and explicit historical catalog replay."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / 'precore'))
import photo_feature_selection as features


def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


def fixture(legacy=False):
    catalog = json.loads(features.CANONICAL_CATALOG_FILE.read_bytes())
    if legacy:
        catalog['schema_version'] = features.LEGACY_CATALOG_VERSION
        for row in catalog['categories']:
            key = 'source_examples' if row['source_number'] is not None else 'added_examples'
            row[key] = ['archived-value-' + row['id']]
    raw = encode(catalog)
    request = 'Requested photographic content'
    baseline = ' '.join('authored_value_' + str(i) for i in range(6))
    envelope = {'contract_version': 'photo-request-envelope/v1', 'provenance': 'requesting_user',
                'request_id': 'example-free-regression', 'request_text': request,
                'request_sha256': hashlib.sha256(request.encode()).hexdigest(),
                'active_spans': [{'span_id': 'topic', 'start': 0, 'end': len(request), 'text': request}]}
    core = {'contract_version': 'photo-authorial-core/v3', 'provenance': 'agent_prepack',
            'source_request': request, 'baseline_prompt_en': baseline,
            'user_definitions': [], 'semantic_assertions': [], 'intent_lock': {'semantic_anchors': []}}
    digest = hashlib.sha256(baseline.encode()).hexdigest()
    review = {'contract_version': 'photo-embodiment-review/v1', 'provenance': 'agent_prepack',
              'prompt_sha256': digest}
    selected = [{'category_id': row['id'], 'basis': 'explicit_request', 'source_span_ids': ['topic'],
                 'source_text': request, 'derivation': None, 'reason': 'Recorded decision ' + str(i),
                 'baseline_evidence': 'authored_value_' + str(i)}
                for i, row in enumerate(catalog['categories'][:6])]
    selection = {'contract_version': features.SELECTION_VERSION, 'request_id': envelope['request_id'],
                 'active_span_ids': ['topic'], 'catalog_path': features.CATALOG_PATH,
                 'catalog_schema_version': catalog['schema_version'],
                 'catalog_sha256': hashlib.sha256(raw).hexdigest(),
                 'request_sha256': envelope['request_sha256'], 'baseline_prompt_sha256': digest,
                 'selected': selected}
    return catalog, raw, selection, envelope, core, review


class ExampleFreeCatalog(unittest.TestCase):
    def test_current_catalog_keeps_categories_without_visual_values(self):
        catalog, raw, selection, envelope, core, review = fixture()
        self.assertTrue(all(not r['source_examples'] and not r['added_examples']
                            for r in catalog['categories']))
        result = features.validate_selection(catalog, raw, selection, envelope, core, review)
        self.assertTrue(result['valid'])
        self.assertEqual(result['selected_count'], 6)

    def test_current_catalog_rejects_visual_examples_even_in_historical_mode(self):
        for index in (0, -1):
            for field in ('source_examples', 'added_examples'):
                for historical in (False, True):
                    with self.subTest(index=index, field=field, historical=historical):
                        catalog = fixture()[0]
                        catalog['categories'][index][field] = ['unrequested-visual-value']
                        with self.assertRaises(features.SelectionValidationError):
                            features.validate_catalog(catalog, historical_catalog=historical)

    def test_legacy_is_available_only_for_explicit_historical_replay(self):
        args = fixture(legacy=True)
        with self.assertRaises(features.SelectionValidationError):
            features.validate_selection(*args)
        self.assertTrue(features.validate_selection(*args, historical_catalog=True)['valid'])

    def test_historical_replay_still_checks_source_provenance(self):
        catalog = fixture(legacy=True)[0]
        catalog['categories'][0]['source_examples'] = []
        with self.assertRaises(features.SelectionValidationError):
            features.validate_catalog(catalog, historical_catalog=True)
        catalog = fixture(legacy=True)[0]
        catalog['categories'][0]['source_number'] = 46
        with self.assertRaises(features.SelectionValidationError):
            features.validate_catalog(catalog, historical_catalog=True)

    def test_historical_replay_rejects_unknown_schema_and_mixed_bindings(self):
        args = list(fixture(legacy=True))
        args[2]['catalog_schema_version'] = features.CATALOG_VERSION
        with self.assertRaises(features.SelectionValidationError):
            features.validate_selection(*args, historical_catalog=True)
        catalog = fixture(legacy=True)[0]
        catalog['schema_version'] = 'photo-precore-feature-catalog/unknown'
        with self.assertRaises(features.SelectionValidationError):
            features.validate_catalog(catalog, historical_catalog=True)

    def test_payload_cannot_borrow_different_catalog_bytes(self):
        args = list(fixture())
        changed = copy.deepcopy(args[0])
        changed['categories'][0]['name_en'] += ' changed'
        args[1] = encode(changed)
        args[2]['catalog_sha256'] = hashlib.sha256(args[1]).hexdigest()
        with self.assertRaises(features.SelectionValidationError):
            features.validate_selection(*args)

    def test_historical_replay_does_not_relax_hash_or_literal_evidence(self):
        changes = [lambda a: a[2].update(catalog_sha256='0' * 64),
                   lambda a: a[2].update(request_sha256='0' * 64),
                   lambda a: a[2].update(baseline_prompt_sha256='0' * 64),
                   lambda a: a[5].update(prompt_sha256='0' * 64),
                   lambda a: a[2]['selected'][0].update(baseline_evidence='absent-value')]
        for legacy in (False, True):
            for change in changes:
                with self.subTest(legacy=legacy, change=change):
                    args = list(fixture(legacy=legacy))
                    change(args)
                    with self.assertRaises(features.SelectionValidationError):
                        features.validate_selection(*args, historical_catalog=legacy)

    def test_five_to_ten_selection_rule_is_unchanged(self):
        for count in (4, 11):
            args = list(fixture())
            args[2]['selected'] = (args[2]['selected'] * 2)[:count]
            with self.assertRaises(features.SelectionValidationError):
                features.validate_selection(*args)

    def test_agent_choice_cannot_be_promoted_to_requester_ownership(self):
        args = list(fixture())
        row = args[2]['selected'][0]
        row.update(basis='agent_visual_choice', source_span_ids=[], source_text=None, derivation=None)
        args[4]['intent_lock']['semantic_anchors'] = [{'prompt_evidence': row['baseline_evidence']}]
        with self.assertRaises(features.SelectionValidationError):
            features.validate_selection(*args)

    def test_cli_distinguishes_current_authoring_from_historical_verification(self):
        for legacy, historical, expected in ((False, False, 0), (True, False, 2), (True, True, 0)):
            with self.subTest(legacy=legacy, historical=historical), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                args = fixture(legacy=legacy)
                names = ('catalog', 'selection', 'envelope', 'core', 'review')
                values = (args[0], args[2], args[3], args[4], args[5])
                for name, value in zip(names, values):
                    (root / (name + '.json')).write_bytes(encode(value))
                command = [sys.executable, str(SKILL / 'scripts/validate_precore_feature_selection.py'),
                           '--catalog', str(root / 'catalog.json'), '--selection', str(root / 'selection.json'),
                           '--request-envelope', str(root / 'envelope.json'), '--authorial-core', str(root / 'core.json'),
                           '--embodiment-review', str(root / 'review.json')]
                if historical:
                    command.append('--historical-catalog')
                env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
                result = subprocess.run(command, capture_output=True, text=True, env=env)
                self.assertEqual(result.returncode, expected, result.stderr)
                if expected == 0:
                    self.assertEqual(json.loads(result.stdout)['catalog_mode'], 'historical' if historical else 'current')


if __name__ == '__main__':
    unittest.main()
