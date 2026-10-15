from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] /
                       'skills/photo-prompt-image-generator/scripts'))
import photo_candidate_corpus as c
import photo_scoped_slot_adoption as scoped
from tests.photo_native_schema import slot

A = 'cand_' + 'a' * 32
B = 'cand_' + 'b' * 32
X = scoped.binding_id(A, 'role_000')
Y = scoped.binding_id(A, 'role_001')


def fixture():
    candidate = {'id': A, 'record_kind': 'visual_option',
        'content': {'en': 'a glossy fabric surface'}, 'conditions': {},
        'effects': {'dimensions': ['style'], 'properties': []},
        'provenance': [{'source': 'authored test', 'sha256': 'a' * 64}]}
    row = {'id': X, 'candidate_id': A, 'slot_id': 'role_000', 'role': 'optional',
           'semantic_role': 'direct', 'conditions': {'subject_applicability': {}}, 'weight': 1}
    return {'schema': c.SCHEMA, 'candidates': {A: candidate},
        'slot_catalog': {'role_%03d' % n: slot('role_%03d' % n, ['style']) for n in range(149)},
        'slot_bindings': {X: row, Y: {**copy.deepcopy(row), 'id': Y, 'slot_id': 'role_001'}},
        'policies': {'original': {'preserve': 'exactly'}}}


def manifest(source, *, changed=False):
    catalog = copy.deepcopy(source['slot_catalog'])
    if changed:
        catalog['role_000']['description'] += ' with a reviewed boundary'
    return {'schema': scoped.SCHEMA, 'source_sha256': c.digest(source),
        'source_catalog_sha256': c.digest(source['slot_catalog']),
        'reviewed_catalog_sha256': c.digest(catalog), 'catalog': catalog,
        'catalog_reason': 'Reviewed boundaries for this bounded catalog',
        'catalog_source_citation': 'authored/catalog.json#/role_000', 'binding_decisions': []}


def decision(source, action='retain', bid=X):
    before = copy.deepcopy(source['slot_bindings'][bid])
    return {'action': action, 'before': before,
        'after': None if action == 'remove' else copy.deepcopy(before),
        'reason': 'Reviewed visible garment relation' if action == 'retain' else
                  'Ambiguous carrier deferred without a semantic approval',
        'source_citation': 'authored/review.json#' + bid}


def write_assets(path, source):
    modules = []
    for field, schema in c.MODULE_SCHEMAS.items():
        name = field + '.json'
        # Deliberately noncanonical formatting exercises byte preservation.
        raw = json.dumps({'schema': schema, field: source[field]}, ensure_ascii=False, indent=3) + '\n'
        (path / name).write_text(raw, encoding='utf-8')
        modules.append({'file': name, 'kind': field})
    (path / c.MANIFEST_NAME).write_text(json.dumps({'schema': c.MANIFEST_SCHEMA,
                                                  'modules': modules}), encoding='utf-8')


class ScopedAdoptionTests(unittest.TestCase):
    def test_noop_inherits_all_rows_without_native_qualification(self):
        source = fixture()
        frozen = copy.deepcopy(source)
        preview = scoped.build_preview(source, manifest(source))
        self.assertEqual(preview['corpus'], source)
        self.assertEqual(source, frozen)
        self.assertFalse(preview['report']['full_native_qualification'])
        self.assertEqual(preview['report']['inherited_binding_count'], 2)

    def test_changed_spec_requires_every_affected_binding_decision(self):
        source = fixture()
        with self.assertRaisesRegex(ValueError, 'unlisted affected'):
            scoped.build_preview(source, manifest(source, changed=True))

    def test_retain_inherits_candidates_and_original_policies_exactly(self):
        source = fixture()
        m = manifest(source, changed=True)
        m['binding_decisions'] = [decision(source)]
        result = scoped.build_preview(source, m)['corpus']
        self.assertEqual(c.canonical_bytes(result['candidates']), c.canonical_bytes(source['candidates']))
        self.assertEqual(result['policies']['original'], source['policies']['original'])
        self.assertEqual(result['slot_bindings'], source['slot_bindings'])
        self.assertIn(X, result['policies'][scoped.REVIEW_POLICY]['reviewed'])

    def test_defer_preserves_referenced_binding_and_external_exact_decision(self):
        source = fixture()
        source['policies']['original']['binding_id'] = X
        m = manifest(source, changed=True)
        m['binding_decisions'] = [decision(source, 'defer')]
        preview = scoped.build_preview(source, m)
        self.assertEqual(preview['corpus']['slot_bindings'][X], source['slot_bindings'][X])
        policy = preview['corpus']['policies'][scoped.REVIEW_POLICY]
        self.assertIn(X, policy['deferred'])
        self.assertNotIn(X, policy['reviewed'])
        self.assertEqual(preview['deferred_bindings'], m['binding_decisions'])
        self.assertFalse(preview['report']['full_native_qualification'])

    def test_source_catalog_and_reviewed_catalog_hash_mismatch_rejected(self):
        for key in ('source_sha256', 'source_catalog_sha256', 'reviewed_catalog_sha256'):
            source = fixture()
            m = manifest(source)
            m[key] = '0' * 64
            with self.subTest(key=key), self.assertRaises(ValueError):
                scoped.build_preview(source, m)

    def test_full_catalog_count_has_no_override(self):
        source = fixture()
        m = manifest(source)
        del m['catalog']['role_148']
        m['reviewed_catalog_sha256'] = c.digest(m['catalog'])
        with self.assertRaisesRegex(ValueError, '149-slot'):
            scoped.build_preview(source, m)
        m['expected_count'] = 148
        with self.assertRaisesRegex(ValueError, 'exact fields'):
            scoped.build_preview(source, m)

    def test_remove_records_external_exact_before(self):
        source = fixture()
        m = manifest(source, changed=True)
        m['binding_decisions'] = [decision(source, 'remove')]
        preview = scoped.build_preview(source, m)
        self.assertNotIn(X, preview['corpus']['slot_bindings'])
        self.assertEqual(preview['deferred_bindings'][0]['before'], source['slot_bindings'][X])

    def test_referenced_removal_reports_exact_blocker(self):
        source = fixture()
        source['policies']['original']['binding_id'] = X
        m = manifest(source, changed=True)
        m['binding_decisions'] = [decision(source, 'remove')]
        with self.assertRaises(scoped.ReferenceBlocker) as caught:
            scoped.build_preview(source, m)
        self.assertEqual(caught.exception.blockers, [
            {'pointer': '/policies/original/binding_id', 'binding_id': X}])

    def test_original_conditions_weight_and_role_cannot_change(self):
        for key, value in [('conditions', {'subject_applicability': {'deny_domains': ['studio']}}),
                           ('weight', 2), ('role', 'required'), ('candidate_id', B)]:
            source = fixture()
            m = manifest(source)
            d = decision(source, 'update')
            d['after'][key] = value
            m['binding_decisions'] = [d]
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, 'preserve original'):
                scoped.build_preview(source, m)

    def test_exact_before_and_unique_decision_required(self):
        source = fixture()
        m = manifest(source)
        d = decision(source)
        d['before']['weight'] = 2
        m['binding_decisions'] = [d]
        with self.assertRaisesRegex(ValueError, 'exact original before'):
            scoped.build_preview(source, m)
        m['binding_decisions'] = [decision(source), decision(source)]
        with self.assertRaisesRegex(ValueError, 'exact original before'):
            scoped.build_preview(source, m)

    def test_retain_and_defer_cannot_change_original(self):
        for action in ('retain', 'defer'):
            source = fixture()
            m = manifest(source)
            d = decision(source, action)
            d['after']['weight'] = 2
            m['binding_decisions'] = [d]
            with self.subTest(action=action), self.assertRaisesRegex(ValueError, 'preserve exact'):
                scoped.build_preview(source, m)

    def test_add_requires_source_witness_and_rejects_duplicate_pair(self):
        source = fixture()
        m = manifest(source)
        row = copy.deepcopy(source['slot_bindings'][X])
        row.update(slot_id='role_002', id=scoped.binding_id(A, 'role_002'))
        d = {'action': 'add', 'before': None, 'after': row, 'reason': 'Individually reviewed role',
             'source_citation': 'authored/new.json original witness ' + X}
        m['binding_decisions'] = [d]
        self.assertIn(row['id'], scoped.build_preview(source, m)['corpus']['slot_bindings'])
        d['source_citation'] = 'uncited'
        with self.assertRaisesRegex(ValueError, 'witness'):
            scoped.build_preview(source, m)
        d['source_citation'] = X
        row.update(slot_id='role_001', id=Y)
        with self.assertRaisesRegex(ValueError, 'unique deterministic'):
            scoped.build_preview(source, m)

    def test_malformed_after_unknown_slot_is_full_validator_rejected(self):
        source = fixture()
        m = manifest(source)
        d = decision(source, 'update')
        d['after'].update(slot_id='missing', id=scoped.binding_id(A, 'missing'))
        m['binding_decisions'] = [d]
        with self.assertRaisesRegex(ValueError, 'dangling binding'):
            scoped.build_preview(source, m)

    def test_duplicate_pair_with_legacy_identity_is_full_validator_rejected(self):
        source = fixture()
        legacy_id = 'bind_' + 'c' * 32
        source['slot_bindings'][legacy_id] = source['slot_bindings'].pop(Y)
        source['slot_bindings'][legacy_id]['id'] = legacy_id
        m = manifest(source)
        row = copy.deepcopy(source['slot_bindings'][legacy_id])
        row['id'] = Y
        m['binding_decisions'] = [{'action': 'add', 'before': None, 'after': row,
            'reason': 'Individually reviewed', 'source_citation': legacy_id}]
        with self.assertRaisesRegex(ValueError, 'duplicate candidate/tag'):
            scoped.build_preview(source, m)

    def test_existing_review_policy_preserved_except_explicit_decision(self):
        source = fixture()
        source['policies'][scoped.REVIEW_POLICY] = {'schema': scoped.REVIEW_SCHEMA,
            'deferred': {X: {'reason': 'old exact defer', 'source_citation': 'old/record'}},
            'reviewed': {Y: {'reason': 'unchanged review', 'source_citation': 'old/other'}}}
        m = manifest(source)
        m['binding_decisions'] = [decision(source, 'retain')]
        policy = scoped.build_preview(source, m)['corpus']['policies'][scoped.REVIEW_POLICY]
        self.assertNotIn(X, policy['deferred'])
        self.assertIn(X, policy['reviewed'])
        self.assertEqual(policy['reviewed'][Y], source['policies'][scoped.REVIEW_POLICY]['reviewed'][Y])

    def test_catalog_cannot_smuggle_candidate_or_policy_edits(self):
        source = fixture()
        m = manifest(source)
        for field in ('candidates', 'policies', 'source_updates'):
            bad = copy.deepcopy(m)
            bad[field] = {}
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'exact fields'):
                scoped.build_preview(source, bad)

    def test_stage_preserves_source_files_and_untouched_record_bytes(self):
        source = fixture()
        m = manifest(source, changed=True)
        m['binding_decisions'] = [decision(source, 'remove')]
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            assets, staged = base / 'assets', base / 'staged'
            assets.mkdir()
            write_assets(assets, source)
            original = {p.name: p.read_bytes() for p in assets.iterdir()}
            preview = scoped.stage_assets(assets, m, staged)
            self.assertEqual(original, {p.name: p.read_bytes() for p in assets.iterdir()})
            for name in ('candidates.json', 'policies.json', c.MANIFEST_NAME):
                self.assertEqual(original[name], (staged / name).read_bytes())
            before = scoped._map_entries(original['slot_bindings.json'].decode(), 'slot_bindings')
            after = scoped._map_entries((staged / 'slot_bindings.json').read_text(), 'slot_bindings')
            self.assertEqual(before[Y], after[Y])
            self.assertEqual(preview['corpus'], c.load(staged))
            self.assertEqual(preview['report']['changed_files'], ['slot_bindings.json', 'slot_catalog.json'])

    def test_stage_review_policy_preserves_original_policy_value_bytes(self):
        source = fixture()
        m = manifest(source, changed=True)
        m['binding_decisions'] = [decision(source, 'defer')]
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            assets, staged = base / 'assets', base / 'staged'
            assets.mkdir()
            write_assets(assets, source)
            original = (assets / 'policies.json').read_text()
            scoped.stage_assets(assets, m, staged)
            before = scoped._map_entries(original, 'policies')
            after = scoped._map_entries((staged / 'policies.json').read_text(), 'policies')
            self.assertEqual(before['original'], after['original'])
            self.assertEqual((assets / 'slot_bindings.json').read_bytes(),
                             (staged / 'slot_bindings.json').read_bytes())

    def test_stage_refuses_existing_output(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            with self.assertRaisesRegex(ValueError, 'fresh directory'):
                scoped.stage_assets(path, {}, path)


if __name__ == '__main__':
    unittest.main()
