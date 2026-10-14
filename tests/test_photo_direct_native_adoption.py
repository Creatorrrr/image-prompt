"""Explicit native-v3 fixtures; preview never writes actual source or runtime."""
import copy
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / 'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
sys.path.insert(0, str(RUN))
import direct_review as review
spec = importlib.util.spec_from_file_location('native_adoption', RUN / 'native_adoption.py')
adoption = importlib.util.module_from_spec(spec); spec.loader.exec_module(adoption)
from tests.test_photo_semantic_evidence import reviewed_source, seal
from tests.test_photo_candidate_corpus import A, B
import photo_semantic_evidence as native


class NativeAdoptionTests(unittest.TestCase):
    def fixture(self, directory):
        root = Path(directory).resolve(); here = root / 'run'
        for name in ('authored', 'packets', 'decisions'):
            (here / name).mkdir(parents=True)
        qualified = reviewed_source(); source = copy.deepcopy(qualified)
        proof = qualified['candidates'][A]['content']['role_evidence']
        source['candidates'][A]['content'].pop('role_evidence')
        # Add an old valid pair to prove the ID is preserved rather than regenerated.
        bid = 'bind_' + 'b' * 32
        binding = {'id': bid, 'candidate_id': A, 'slot_id': 'surface_material', 'role': 'optional',
            'semantic_role': source['slot_catalog']['surface_material']['semantic_role'],
            'conditions': {'subject_applicability': {}}, 'weight': 1.0}
        source['slot_bindings'] = {bid: binding}
        fact = {k: proof['facts'][0][k] for k in ('pointer', 'quote', 'dimension', 'target', 'property', 'realization_id')}
        decision = {'candidate_id': A, 'meaning_summary': 'The fixture declares a satin garment surface.',
            'recommended_kind': source['candidates'][A]['record_kind'], 'corrections': [],
            'roles': [{'slot_id': 'surface_material', 'semantic_role': binding['semantic_role'],
                'scope': 'whole_record', 'realization_ids': ['base'], 'rationale': 'Explicit fixture source.',
                'evidence': [fact]}], 'facts': [fact],
            'rejected_boundaries': ['Do not infer a second material or weave.'], 'uncertainties': [],
            'status': 'approved', 'all_roles_considered': True}
        packet = {'ids': [A], 'source_sha256': review.c.digest(source),
            'catalog_sha256': review.c.digest(source['slot_catalog']),
            'records': copy.deepcopy(source['candidates']), 'references': {A: {}}}
        row = {**review.binding(source, A), **decision, 'schema': review.SCHEMA, 'reviewer': 'Codex',
            'review_method': 'codex_direct_source_read', 'independent_human_review': False,
            'authored_decision': {'file': 'run/authored/decision.json', 'item': 1,
                                  'sha256': review.c.digest(decision)}, 'packet_sha256': review.c.digest(packet)}
        baseline = {'source_sha256': review.c.digest(source),
            'catalog_sha256': review.c.digest(source['slot_catalog']), 'candidate_count': 1}
        manual = {'schema': adoption.SCHEMA, 'actor': '/root', 'source_sha256': review.c.digest(source),
            'catalog_sha256': review.c.digest(source['slot_catalog']), 'decisions_sha256': adoption.decision_digest([row]),
            'catalog_updates': [], 'source_updates': [], 'reference_updates': [], 'binding_approvals': [],
            'records': {A: {'source_record_sha256': review.c.digest(source['candidates'][A]),
                'decision_sha256': review.c.digest(row), 'meaning_sha256': native.meaning_sha256(source['candidates'][A]),
                'catalog_sha256': review.c.digest(source['slot_catalog']), 'proof': copy.deepcopy(proof),
                'bindings': {'surface_material': {k: binding[k] for k in adoption.BINDING_SPEC_FIELDS}}}}}
        manual['records'][A]['proof']['review']['original_review'] = {
            'candidate_id': A, 'source_record_sha256': row['source_record_sha256'],
            'catalog_sha256': row['catalog_sha256'], 'decision_sha256': review.c.digest(row),
            'artifact': row['authored_decision']['file']}
        manual['records'][A]['proof']['review']['native_review']['native_contract_sha256'] = native.native_contract_sha256(manual['records'][A]['proof'])
        review.write(here / 'authored/decision.json', {'decisions': [decision]})
        review.write(here / 'packets/source.json', packet)
        return root, here, source, baseline, [A], [row], manual

    def context(self, root, here):
        from contextlib import ExitStack
        stack = ExitStack(); stack.enter_context(patch.object(review, 'ROOT', root))
        stack.enter_context(patch.object(review, 'HERE', here)); return stack

    def build(self, values):
        root, here, source, baseline, order, rows, manual = values
        with self.context(root, here):
            return adoption.build_preview(source, baseline, order, rows, manual, actor='/root', expected_count=1)

    def rebind(self, values):
        root, here, source, baseline, order, rows, manual = values; row = rows[0]
        row.update(review.binding(source, A))
        decision = {k: row[k] for k in {'candidate_id', 'meaning_summary', 'recommended_kind', 'corrections',
            'roles', 'facts', 'rejected_boundaries', 'uncertainties', 'status', 'all_roles_considered'}}
        row['authored_decision']['sha256'] = review.c.digest(decision)
        packet = {'ids': [A], 'source_sha256': review.c.digest(source),
            'catalog_sha256': review.c.digest(source['slot_catalog']),
            'records': copy.deepcopy(source['candidates']), 'references': {A: review.closure(source, A)}}
        row['packet_sha256'] = review.c.digest(packet)
        review.write(here / 'packets/source.json', packet); review.write(here / 'authored/decision.json', {'decisions': [decision]})
        baseline.update(source_sha256=review.c.digest(source), catalog_sha256=review.c.digest(source['slot_catalog']))
        manual.update(source_sha256=review.c.digest(source), catalog_sha256=review.c.digest(source['slot_catalog']),
                      decisions_sha256=adoption.decision_digest(rows))
        manual['records'][A].update(source_record_sha256=review.c.digest(source['candidates'][A]),
                                  decision_sha256=review.c.digest(row))
        manual['records'][A]['proof']['review']['original_review'] = {
            'candidate_id': A, 'source_record_sha256': row['source_record_sha256'],
            'catalog_sha256': row['catalog_sha256'], 'decision_sha256': review.c.digest(row),
            'artifact': row['authored_decision']['file']}
        manual['records'][A]['proof']['review']['native_review']['native_contract_sha256'] = native.native_contract_sha256(manual['records'][A]['proof'])


    def test_deterministic_preview_preserves_existing_binding_and_source_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            values = self.fixture(directory); before = copy.deepcopy(values[2:])
            proposed, ledger = self.build(values); again, again_ledger = self.build(values)
            self.assertEqual(proposed, again); self.assertEqual(ledger, again_ledger)
            self.assertEqual(values[2:], tuple(before))
            self.assertEqual(proposed['slot_bindings'], values[2]['slot_bindings'])
            self.assertEqual(set(proposed['candidates']), {A})
            self.assertEqual(native.native_status(proposed['candidates'][A]), 'qualified')
            self.assertFalse(ledger['native_changes_applied']); self.assertFalse(ledger['stage06_complete'])
            self.assertFalse(ledger['production_count_gate'])

    def test_production_count_and_root_actor_have_no_cli_override(self):
        with tempfile.TemporaryDirectory() as directory:
            root, here, source, baseline, order, rows, manual = self.fixture(directory)
            with self.context(root, here):
                with self.assertRaisesRegex(ValueError, 'full source'):
                    adoption.build_preview(source, baseline, order, rows, manual,
                        actor='/root', expected_count=adoption.PRODUCTION_COUNT)
                with self.assertRaisesRegex(ValueError, 'root-only'):
                    adoption.build_preview(source, baseline, order, rows, manual, actor='/root/worker', expected_count=1)

    def test_missing_pending_duplicate_or_foreign_approval_rejected(self):
        for defect in ('missing', 'pending', 'duplicate', 'foreign'):
            with self.subTest(defect=defect), tempfile.TemporaryDirectory() as directory:
                values = self.fixture(directory); rows = values[5]
                if defect == 'missing': rows.clear()
                elif defect == 'pending': rows[0].update(status='needs_boundary_review', uncertainties=[{'kind': 'fixture', 'detail': 'Pending.'}])
                elif defect == 'duplicate': rows.append(copy.deepcopy(rows[0]))
                else: rows[0]['candidate_id'] = B
                with self.assertRaises(ValueError): self.build(values)

    def test_missing_stale_v2_or_unowned_native_proof_and_role_expansion_rejected(self):
        for defect in ('missing', 'stale', 'v2', 'carrier', 'extra_role', 'missing_role', 'effects', 'source_units', 'closure', 'spec', 'mode', 'value', 'rids', 'catalog'):
            with self.subTest(defect=defect), tempfile.TemporaryDirectory() as directory:
                values = self.fixture(directory); qualification = values[6]['records'][A]; proof = qualification['proof']
                if defect == 'missing': qualification['proof'] = None
                elif defect == 'stale': proof['meaning_sha256'] = '0' * 64
                elif defect == 'v2': proof['schema'] = 'photo-candidate-role-evidence/v2'
                elif defect == 'carrier': proof['owner_maps']['base']['bindings'].clear()
                elif defect == 'extra_role': proof['roles']['texture'] = copy.deepcopy(proof['roles']['surface_material'])
                elif defect == 'missing_role': proof['roles'].clear()
                elif defect == 'effects': proof['effect_sets']['base']['properties'].clear()
                elif defect == 'source_units': proof['source_units'].clear()
                elif defect == 'closure': proof['reference_sha256'][B] = '0' * 64
                elif defect == 'spec': proof['roles']['surface_material']['spec_sha256'] = '0' * 64
                elif defect == 'mode': proof['facts'][0]['mode'] = 'context'
                elif defect == 'value': proof['facts'][0]['value'] = {}
                elif defect == 'rids': proof['owner_maps'].clear()
                else: proof['catalog_sha256'] = '0' * 64
                if isinstance(qualification['proof'], dict):
                    proof['review']['native_review']['native_contract_sha256'] = native.native_contract_sha256(proof)
                with self.assertRaises(ValueError): self.build(values)

    def test_exact_source_corrections_kind_and_provenance_are_enforced(self):
        for defect in ('before', 'kind', 'provenance', 'references'):
            with self.subTest(defect=defect), tempfile.TemporaryDirectory() as directory:
                values = self.fixture(directory); old = values[2]['candidates'][A]; after = copy.deepcopy(old)
                update = {'candidate_id': A, 'decision_sha256': review.c.digest(values[5][0]),
                    'before': copy.deepcopy(old), 'after': after, 'reason': 'Explicit fixture native refinement.'}
                values[6]['source_updates'] = [update]
                if defect == 'before': update['before']['content']['en'] = 'wrong old value'
                elif defect == 'kind': after['record_kind'] = 'visual_profile'
                elif defect == 'provenance': after['provenance'].clear()
                else: after['content']['candidate_ref'] = B
                with self.assertRaises(ValueError): self.build(values)

    def test_binding_condition_changes_need_exact_before_after_manual_approval(self):
        with tempfile.TemporaryDirectory() as directory:
            values = self.fixture(directory); source, rows, manual = values[2], values[5], values[6]
            old = next(iter(source['slot_bindings'].values()))
            spec = manual['records'][A]['bindings']['surface_material']; spec['conditions'] = {'subject_applicability': {'for_any': ['human']}}
            with self.assertRaisesRegex(ValueError, 'explicit approval'): self.build(values)
            after = {**copy.deepcopy(old), **copy.deepcopy(spec)}
            manual['binding_approvals'] = [{'candidate_id': A, 'decision_sha256': review.c.digest(rows[0]),
                'before': copy.deepcopy(old), 'after': after, 'reason': 'Manual role-specific condition review.'}]
            proposed, _ = self.build(values); self.assertEqual(proposed['slot_bindings'][old['id']]['conditions'], spec['conditions'])
            manual['binding_approvals'][0]['before']['conditions'] = {'subject_applicability': {'for_any': ['object']}}
            with self.assertRaisesRegex(ValueError, 'exact before/after'): self.build(values)

    def test_new_pair_id_is_stable_and_requires_explicit_complete_binding_values(self):
        with tempfile.TemporaryDirectory() as directory:
            values = self.fixture(directory); source, rows, manual = values[2], values[5], values[6]
            source['slot_bindings'].clear(); self.rebind(values)
            bid = adoption.binding_id(A, 'surface_material')
            after = {'id': bid, 'candidate_id': A, 'slot_id': 'surface_material',
                     **copy.deepcopy(manual['records'][A]['bindings']['surface_material'])}
            manual['binding_approvals'] = [{'candidate_id': A, 'decision_sha256': review.c.digest(rows[0]),
                'before': None, 'after': after, 'reason': 'Explicit new fixture relation.'}]
            proposed, _ = self.build(values)
            self.assertEqual(set(proposed['slot_bindings']), {bid})
            manual['records'][A]['bindings']['surface_material'].pop('conditions')
            with self.assertRaises(ValueError): self.build(values)

    def test_removed_referenced_binding_never_falls_back_to_a_different_slot(self):
        with tempfile.TemporaryDirectory() as directory:
            values = self.fixture(directory); source, rows, manual = values[2], values[5], values[6]
            old = copy.deepcopy(next(iter(source['slot_bindings'].values())))
            old.update(id='bind_'+'d'*32, slot_id='texture'); source['slot_bindings'][old['id']] = old
            # Reference in source metadata is still a real binding reference: no quiet deletion.
            source['candidates'][A]['content']['reference_for_fixture'] = old['id']; self.rebind(values)
            proof = manual['records'][A]['proof']; proof['meaning_sha256'] = native.meaning_sha256(source['candidates'][A])
            manual['records'][A]['meaning_sha256'] = proof['meaning_sha256']
            manual['binding_approvals'] = [{'candidate_id': A, 'decision_sha256': review.c.digest(rows[0]),
                'before': old, 'after': None, 'reason': 'Explicit removal of an unapproved fixture slot.'}]
            with self.assertRaisesRegex(ValueError, 'removed binding remains referenced'): self.build(values)
            keep = next(b for b in source['slot_bindings'].values() if b['slot_id'] == 'surface_material')
            manual['reference_updates'] = [{'candidate_id': A, 'source_record_sha256': review.c.digest(source['candidates'][A]),
                'decision_sha256': review.c.digest(rows[0]), 'pointer': '/content/reference_for_fixture',
                'before': old['id'], 'after': keep['id'], 'reason': 'Explicit source-bound reference re-review.'}]
            final_record = copy.deepcopy(source['candidates'][A]); final_record['content']['reference_for_fixture'] = keep['id']
            proof['meaning_sha256'] = native.meaning_sha256(final_record)
            proof['reference_sha256'] = native.referenced_records(final_record,source)
            manual['records'][A]['meaning_sha256'] = proof['meaning_sha256']
            proof['review']['source_correction'] = {'before_sha256': native.meaning_sha256(source['candidates'][A]),
                'after_sha256': native.meaning_sha256(final_record), 'rationale': 'Explicit fixture binding reference update.'}
            proof['review']['native_review']['native_contract_sha256'] = native.native_contract_sha256(proof)
            proposed, _ = self.build(values)
            self.assertEqual(proposed['candidates'][A]['content']['reference_for_fixture'], keep['id'])
            manual['reference_updates'][0]['before'] = keep['id']
            with self.assertRaisesRegex(ValueError, 'existing typed reference leaf'): self.build(values)

    def test_explicit_existing_catalog_spec_update_requires_matching_manual_v3_hashes(self):
        with tempfile.TemporaryDirectory() as directory:
            values = self.fixture(directory); source, manual = values[2], values[6]
            before = source['slot_catalog']['surface_material']; after = copy.deepcopy(before)
            after['description'] += ' Explicit reviewed fixture clarification.'
            manual['catalog_updates'] = [{'slot_id': 'surface_material', 'before': copy.deepcopy(before),
                                         'after': after, 'reason': 'Manual existing role-spec review.'}]
            with self.assertRaisesRegex(ValueError, 'meaning/catalog'): self.build(values)
            catalog = copy.deepcopy(source['slot_catalog']); catalog['surface_material'] = after
            qualification = manual['records'][A]; proof = qualification['proof']
            qualification['catalog_sha256'] = review.c.digest(catalog); proof['catalog_sha256'] = review.c.digest(catalog)
            proof['roles']['surface_material']['spec_sha256'] = review.c.digest(after)
            proof['review']['native_review']['native_contract_sha256'] = native.native_contract_sha256(proof)
            proposed, _ = self.build(values); self.assertEqual(proposed['slot_catalog'], catalog)
            manual['catalog_updates'][0]['before']['description'] += ' stale'
            with self.assertRaisesRegex(ValueError, 'exact before'): self.build(values)

    def test_source_guard_refinement_is_explicit_and_never_inferred_from_binding(self):
        with tempfile.TemporaryDirectory() as directory:
            values = self.fixture(directory); source, rows, manual = values[2], values[5], values[6]
            before = source['candidates'][A]; after = copy.deepcopy(before)
            after['conditions'] = {'for_any': ['human']}
            manual['source_updates'] = [{'candidate_id': A, 'decision_sha256': review.c.digest(rows[0]),
                'before': copy.deepcopy(before), 'after': after, 'reason': 'Explicit source intrinsic-guard review.'}]
            qualification = manual['records'][A]; proof = qualification['proof']
            qualification['meaning_sha256'] = native.meaning_sha256(after)
            proof['meaning_sha256'] = qualification['meaning_sha256']
            proof['guard_sets']={rid:native.source_guard_set(after,rid,source) for rid in native.realizations.ids(after)}
            proof['review']['source_correction'] = {'before_sha256': native.meaning_sha256(before),
                'after_sha256': native.meaning_sha256(after), 'rationale': 'Explicit fixture source guard refinement.'}
            proof['review']['native_review']['native_contract_sha256'] = native.native_contract_sha256(proof)
            proposed, _ = self.build(values)
            self.assertEqual(proposed['candidates'][A]['conditions'], {'for_any': ['human']})
            self.assertEqual(next(iter(proposed['slot_bindings'].values()))['conditions'], {'subject_applicability': {}})
            proof['review']['source_correction'] = None
            with self.assertRaisesRegex(ValueError, 'exact original/final meaning'): self.build(values)

    def test_direct_correction_must_match_exact_old_source_value(self):
        with tempfile.TemporaryDirectory() as directory:
            values = self.fixture(directory); row = values[5][0]
            row['corrections'] = [{'pointer': '/content/en', 'before': 'a guessed old surface',
                'after': 'a satin garment surface', 'reason': 'Fixture exact-before rejection.'}]
            self.rebind(values)
            with self.assertRaisesRegex(ValueError, 'exact current text'): self.build(values)

    def test_diagnostic_has_no_roles_facts_effects_or_remaining_bindings(self):
        with tempfile.TemporaryDirectory() as directory:
            values = self.fixture(directory); source, rows, manual = values[2], values[5], values[6]
            old = next(iter(source['slot_bindings'].values())); row = rows[0]
            row.update(recommended_kind='diagnostic', status='diagnostic_reviewed', roles=[], facts=[],
                corrections=[{'pointer': '/effects', 'before': copy.deepcopy(source['candidates'][A]['effects']),
                    'after': {'dimensions': [], 'properties': []}, 'reason': 'Explicit diagnostic fixture effect removal.'}])
            self.rebind(values)
            after = review.corrected_record(source['candidates'][A], row['corrections']); after['record_kind'] = 'diagnostic'
            proof = copy.deepcopy(manual['records'][A]['proof'])
            proof.update(meaning_sha256=native.meaning_sha256(after), facts=[], roles={},
                owner_maps={'base': {'schema': native.OWNER_SCHEMA, 'bindings': []}},
                effect_sets={'base': {'dimensions': [], 'properties': []}})
            proof['source_units'][0].update(fact_refs=[], disposition='nonsemantic')
            proof['review']['source_correction'] = {'before_sha256': native.meaning_sha256(source['candidates'][A]),
                'after_sha256': native.meaning_sha256(after), 'rationale': 'Explicit fixture diagnostic review.'}
            proof['review']['native_review']['native_contract_sha256'] = native.native_contract_sha256(proof)
            manual['records'][A].update(meaning_sha256=native.meaning_sha256(after), proof=proof, bindings={})
            manual['binding_approvals'] = [{'candidate_id': A, 'decision_sha256': review.c.digest(row),
                'before': old, 'after': None, 'reason': 'Explicit removal of diagnostic positive relation.'}]
            proposed, _ = self.build(values)
            self.assertEqual(proposed['candidates'][A]['record_kind'], 'diagnostic')
            self.assertEqual(proposed['slot_bindings'], {})
            proof['roles']['surface_material'] = {}
            with self.assertRaises(ValueError): self.build(values)

    def test_native_original_review_and_immutable_authored_inputs_are_required(self):
        for defect in ('native_original', 'authored', 'packet', 'manual_decisions', 'duplicate_bindings'):
            with self.subTest(defect=defect), tempfile.TemporaryDirectory() as directory:
                values = self.fixture(directory); root, here, source, _, _, rows, manual = values
                if defect == 'native_original': manual['records'][A]['proof']['review']['original_review']['decision_sha256'] = '0' * 64
                elif defect == 'authored':
                    path = here / 'authored/decision.json'; doc = review.c.decode(path.read_bytes())
                    doc['decisions'][0]['meaning_summary'] += ' stale'; review.write(path, doc)
                elif defect == 'packet':
                    path = here / 'packets/source.json'; doc = review.c.decode(path.read_bytes())
                    doc['records'][A]['content']['en'] += ' stale'; review.write(path, doc)
                elif defect == 'manual_decisions': manual['decisions_sha256'] = '0' * 64
                else:
                    extra = copy.deepcopy(next(iter(source['slot_bindings'].values())))
                    extra['id'] = 'bind_'+'e'*32; source['slot_bindings'][extra['id']] = extra
                    self.rebind(values)
                with self.assertRaises((ValueError, KeyError)): self.build(values)

    def test_preview_outputs_are_separate_immutable_and_never_activate(self):
        with tempfile.TemporaryDirectory() as directory:
            values = self.fixture(directory); proposed, ledger = self.build(values)
            root, here, source, baseline, order, rows, manual = values
            with self.context(root, here):
                output = adoption.write_preview('fixture-preview', source, baseline, order, rows, manual, proposed, ledger)
                self.assertTrue(output.is_relative_to(here / 'native-previews'))
                self.assertTrue((output / 'PREVIEW-COMPLETE.json').exists())
                self.assertEqual(review.c.decode((output / 'BEFORE-CORPUS.json').read_bytes()), source)
                self.assertFalse((here / 'PROGRESS.json').exists())
                with self.assertRaises(ValueError): adoption.write_preview('fixture-preview', source, baseline, order, rows, manual, proposed, ledger)
                with self.assertRaises(ValueError): adoption.write_preview('../assets', source, baseline, order, rows, manual, proposed, ledger)

class NativeAdoptionV2Tests(unittest.TestCase):
    def fixture(self,directory):
        from tests import test_photo_direct_native_reviews as review_fixtures
        helper=review_fixtures.NativeReviewsTests(); v=helper.fixture(directory); latest=helper.latest(v)
        manual=dict(schema=adoption.SCHEMA_V2,actor='/root',latest_manifest_sha256=latest['manifest_sha256'],
            original_source_sha256=latest['original_source_sha256'],current_source_sha256=latest['current_source_sha256'],
            catalog_sha256=latest['catalog_sha256'],member_contract=adoption.MEMBER_CONTRACT,
            records={A:dict(review_sha256=review.c.digest(latest['records'][A]),proof_sha256=review.c.digest(latest['records'][A]['proof']),
                bindings={'surface_material':copy.deepcopy(next(iter(v['current']['slot_bindings'].values())))})},
            source_approvals=[],reference_approvals=[],binding_approvals=[],policy_approval=None,member_guard_migrations=[])
        artifact=helper.put(v['root'],'run/approved-catalog.json',v['current']['slot_catalog'])
        manual['catalog_approval']={'schema':'photo-native-catalog-approval/v1','actor':'/root',
            'artifact':artifact,'catalog_sha256':review.c.digest(v['current']['slot_catalog']),
            'slot_count':len(v['current']['slot_catalog']),'slot_ids':sorted(v['current']['slot_catalog']),
            'reason':'Root explicitly reviewed the complete isolated current catalog.'}
        return helper,v,manual

    def build(self,v,manual):
        return adoption.build_preview_v2('run/latest.json',manual,actor='/root',expected_count=1,root=v['root'],here=v['here'])

    def refresh(self,helper,v,manual):
        helper.attest_proof(v); helper.persist(v); latest=helper.latest(v)
        manual.update(latest_manifest_sha256=latest['manifest_sha256'],current_source_sha256=latest['current_source_sha256'],catalog_sha256=latest['catalog_sha256'])
        manual['records'][A].update(review_sha256=review.c.digest(latest['records'][A]),proof_sha256=review.c.digest(latest['records'][A]['proof']))
        manual['catalog_approval'].update(artifact=helper.put(v['root'],'run/approved-catalog.json',v['current']['slot_catalog']),
            catalog_sha256=review.c.digest(v['current']['slot_catalog']),slot_count=len(v['current']['slot_catalog']),
            slot_ids=sorted(v['current']['slot_catalog']))
        return latest

    def test_v2_uses_new_native_review_despite_historical_pending_and_preserves_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            helper,v,manual=self.fixture(directory); before=copy.deepcopy(v); proposed,ledger=self.build(v,manual)
            again,again_ledger=self.build(v,manual); self.assertEqual(proposed,again); self.assertEqual(ledger,again_ledger)
            self.assertEqual(v,before); self.assertEqual(v['old']['status'],'needs_boundary_review')
            self.assertEqual(proposed['slot_bindings'],v['current']['slot_bindings'])
            self.assertEqual(ledger['original_compiled'][A],v['batch']['records'][0]['original_compiled'])
            self.assertTrue(proposed['candidates'][A]['content']['role_evidence']['review']['original_review']['artifact'].endswith('#item=1'))
            self.assertFalse(ledger['native_changes_applied']); self.assertFalse(ledger['production_count_gate'])
            self.assertFalse(ledger['full_runtime_consumer_integration_verified'])

    def test_v2_current_catalog_approval_binds_exact_artifact_roster_hash_without_magic_count(self):
        with tempfile.TemporaryDirectory() as directory:
            helper,v,manual=self.fixture(directory)
            self.assertNotEqual(len(v['current']['slot_catalog']),141)
            self.assertNotEqual(len(v['current']['slot_catalog']),142)
            self.build(v,manual)
        for defect in ['missing','actor','schema','hash','count','bool','roster','artifact','unknown']:
            with self.subTest(defect=defect),tempfile.TemporaryDirectory() as directory:
                helper,v,manual=self.fixture(directory);approval=manual['catalog_approval']
                if defect=='missing':manual.pop('catalog_approval')
                elif defect=='actor':approval['actor']='/root/worker'
                elif defect=='schema':approval['schema']='guessed'
                elif defect=='hash':approval['catalog_sha256']='0'*64
                elif defect=='count':approval['slot_count']+=1
                elif defect=='bool':approval['slot_count']=True
                elif defect=='roster':approval['slot_ids']+=['invented_role']
                elif defect=='artifact':approval['artifact']=helper.put(v['root'],'run/wrong-catalog.json',{})
                else:approval['automatic_approval']=True
                with self.assertRaises(ValueError):self.build(v,manual)

    def test_v2_requires_exact_schema_root_count_latest_source_and_proof(self):
        for defect in ('schema','actor','manifest','source','catalog','proof','review','unknown','role'):
            with self.subTest(defect=defect),tempfile.TemporaryDirectory() as directory:
                helper,v,manual=self.fixture(directory)
                if defect=='schema': manual['schema']=adoption.SCHEMA
                elif defect=='actor': manual['actor']='/root/worker'
                elif defect=='manifest': manual['latest_manifest_sha256']='0'*64
                elif defect=='source': manual['current_source_sha256']='0'*64
                elif defect=='catalog': manual['catalog_sha256']='0'*64
                elif defect=='proof': manual['records'][A]['proof_sha256']='0'*64
                elif defect=='review': manual['records'][A]['review_sha256']='0'*64
                elif defect=='unknown': manual['guessed_semantics']=[]
                else: manual['records'][A]['bindings'].clear()
                with self.assertRaises(ValueError): self.build(v,manual)
        with tempfile.TemporaryDirectory() as directory:
            helper,v,manual=self.fixture(directory)
            with self.assertRaisesRegex(ValueError,'all18250'):
                adoption.build_preview_v2('run/latest.json',manual,actor='/root',root=v['root'],here=v['here'])
            with self.assertRaisesRegex(ValueError,'root-only'):
                adoption.build_preview_v2('run/latest.json',manual,actor='/root/worker',expected_count=1,root=v['root'],here=v['here'])

    def test_v2_reverifies_latest_artifacts_and_pending_never_creates_preview(self):
        with tempfile.TemporaryDirectory() as directory:
            helper,v,manual=self.fixture(directory)
            v['batch']['records'][0]['status']='pending'; helper.persist(v)
            with self.assertRaises(ValueError):
                adoption.write_preview_v2('must-not-exist','run/latest.json',manual,actor='/root',expected_count=1,root=v['root'],here=v['here'])
            self.assertFalse((v['here']/'native-previews/must-not-exist').exists())

    def test_v2_binding_ids_roles_conditions_weight_are_explicit_and_fully_approved(self):
        for field in ('id','candidate_id','slot_id','role','semantic_role','conditions','weight'):
            with self.subTest(field=field),tempfile.TemporaryDirectory() as directory:
                helper,v,manual=self.fixture(directory); manual['records'][A]['bindings']['surface_material'].pop(field)
                with self.assertRaises(ValueError): self.build(v,manual)
        with tempfile.TemporaryDirectory() as directory:
            helper,v,manual=self.fixture(directory); binding=manual['records'][A]['bindings']['surface_material']
            old=copy.deepcopy(binding); binding.update(id='bind_'+'f'*32,role='secondary',conditions={'subject_applicability':{'subject_categories':['human']}},weight=0.7)
            with self.assertRaisesRegex(ValueError,'binding approval'): self.build(v,manual)
            digest=manual['records'][A]['review_sha256']
            manual['binding_approvals']=[dict(candidate_id=A,review_sha256=digest,before=old,current_before=old,after=None,reason='Explicit deletion of previous binding identity.'),
                dict(candidate_id=A,review_sha256=digest,before=None,current_before=None,after=copy.deepcopy(binding),reason='Explicit new ID, role, conditions and weight.')]
            proposed,ledger=self.build(v,manual); self.assertEqual(proposed['slot_bindings'],{binding['id']:binding})
            self.assertEqual(proposed['candidates'][A]['conditions'],{})
            manual['binding_approvals'][1]['after']['conditions']={}
            with self.assertRaisesRegex(ValueError,'binding approval'): self.build(v,manual)

    def test_v2_new_catalog_and_role_set_require_reviewed_catalog_and_new_binding_approvals(self):
        with tempfile.TemporaryDirectory() as directory:
            helper,v,manual=self.fixture(directory); catalog=v['current']['slot_catalog']
            added=copy.deepcopy(catalog['surface_material']); added['id']='new_material'; catalog['new_material']=added
            v['inp']['catalog_review']['after']=copy.deepcopy(catalog)
            v['inp']['catalog_review']['changes']=[dict(pointer='/new_material',before_exists=False,before=None,after_exists=True,after=added,reason='Complete new native catalog spec review.')]
            p=v['batch']['records'][0]['proof']; role=p['roles'].pop('surface_material'); role['spec_sha256']=review.c.digest(added); p['roles']['new_material']=role
            p['catalog_sha256']=review.c.digest(catalog)
            self.refresh(helper,v,manual)
            old=manual['records'][A]['bindings'].pop('surface_material'); new=copy.deepcopy(old); new.update(id='bind_'+'e'*32,slot_id='new_material')
            manual['records'][A]['bindings']['new_material']=new; digest=manual['records'][A]['review_sha256']
            manual['binding_approvals']=[dict(candidate_id=A,review_sha256=digest,before=old,current_before=old,after=None,reason='Explicit old-role relation removal.'),
                dict(candidate_id=A,review_sha256=digest,before=None,current_before=None,after=new,reason='Explicit current new-role relation.')]
            proposed,_=self.build(v,manual)
            self.assertEqual(set(proposed['candidates'][A]['content']['role_evidence']['roles']),{'new_material'})
            self.assertEqual(v['old']['roles'][0]['slot_id'],'surface_material')

    def test_v2_source_correction_requires_full_direct_delta_and_exact_root_source_approval(self):
        with tempfile.TemporaryDirectory() as directory:
            helper,v,manual=self.fixture(directory); row=v['batch']['records'][0]; before=copy.deepcopy(row['source_before'])
            after=copy.deepcopy(before); after['conditions']={'for_any':['human']}; row['source_after']=after; v['current']['candidates'][A]=copy.deepcopy(after)
            row['delta']=[dict(pointer='/conditions',before_exists=True,before={},after_exists=True,after=after['conditions'],reason='Directly reviewed canonical condition.')]
            p=row['proof']; p['meaning_sha256']=native.meaning_sha256(after)
            p['review']['source_correction']=dict(before_sha256=native.meaning_sha256(before),after_sha256=p['meaning_sha256'],rationale='Full source guard correction directly read.')
            self.refresh(helper,v,manual)
            with self.assertRaisesRegex(ValueError,'source approval'): self.build(v,manual)
            manual['source_approvals']=[dict(candidate_id=A,review_sha256=review.c.digest(row),before=before,after=after,delta=copy.deepcopy(row['delta']),reason='Exact complete root source correction approval.')]
            proposed,_=self.build(v,manual); self.assertEqual(proposed['candidates'][A]['conditions'],after['conditions'])
            self.assertEqual(next(iter(proposed['slot_bindings'].values()))['conditions'],{'subject_applicability':{}})
            manual['source_approvals'][0]['delta']=[]
            with self.assertRaisesRegex(ValueError,'source approval'): self.build(v,manual)

    def test_v2_writes_new_research_preview_only_and_rejects_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            helper,v,manual=self.fixture(directory); before={p:p.read_bytes() for p in v['root'].rglob('*') if p.is_file()}
            output,ledger=adoption.write_preview_v2('explicit-fixture','run/latest.json',manual,actor='/root',expected_count=1,root=v['root'],here=v['here'])
            self.assertEqual(output,v['here']/'native-previews/explicit-fixture')
            self.assertTrue((output/'PREVIEW-COMPLETE.json').exists())
            self.assertEqual(before,{p:p.read_bytes() for p in before})
            with self.assertRaisesRegex(ValueError,'must be new'):
                adoption.write_preview_v2('explicit-fixture','run/latest.json',manual,actor='/root',expected_count=1,root=v['root'],here=v['here'])
            with self.assertRaises(ValueError):
                adoption.write_preview_v2('../escape','run/latest.json',manual,actor='/root',expected_count=1,root=v['root'],here=v['here'])

    def test_member_guard_migration_requires_exact_manual_classification_and_source_condition_target(self):
        helper=NativeAdoptionTests()
        with tempfile.TemporaryDirectory() as directory:
            root,here,original,*_=helper.fixture(directory); original=copy.deepcopy(original)
            bid=next(iter(original['slot_bindings'])); oldbinding=original['slot_bindings'][bid]
            oldbinding['conditions']={'subject_applicability':{'subject_categories':['human']}}
            oldmember={'candidate_id':A,'binding_id':bid,'presentation_role':'surface_material','adoption':'optional','requirements':{}}
            # Pure migration integrity fixture; semantic compound qualification is
            # independently required by the full latest/native validator above.
            original['candidates'][B]=copy.deepcopy(original['candidates'][A]); original['candidates'][B]['id']=B
            original['candidates'][B]['content']['member_candidates']=[oldmember]
            current=copy.deepcopy(original); newmember=copy.deepcopy(oldmember); newmember.pop('binding_id')
            current['candidates'][B]['content']['member_candidates']=[newmember]
            current['candidates'][A]['conditions']={'subject_applicability':{'subject_categories':['human']}}
            rows={A:{'candidate_id':A,'rationale':'Direct child condition reread.'},B:{'candidate_id':B,'rationale':'Direct whole parent reread.'}}
            migration=dict(candidate_id=B,review_sha256=review.c.digest(rows[B]),before_pointer='/content/member_candidates/0',before_member=oldmember,
                before_binding=oldbinding,after_pointer='/content/member_candidates/0',after_member=newmember,
                classification='transferred_to_source_conditions',condition_targets=[dict(candidate_id=A,review_sha256=review.c.digest(rows[A]),
                    before={},after={'subject_applicability':{'subject_categories':['human']}},reason='Manually transferred exact essential subject applicability.')],reason='Explicit final member guard migration review.')
            adoption.verify_member_migrations(original,current,rows,[migration])
            for defect in ('missing','binding','target','classification','retarget','newguard'):
                with self.subTest(defect=defect):
                    edits=[copy.deepcopy(migration)]
                    if defect=='missing': edits=[]
                    elif defect=='binding': edits[0]['before_binding']['weight']=0.2
                    elif defect=='target': edits[0]['condition_targets'][0]['after']={}
                    elif defect=='classification': edits[0]['classification']='copy_all_intrinsic'
                    elif defect=='retarget': edits[0]['after_member']['candidate_id']=B
                    else: edits[0]['after_member']['binding_id']=bid
                    with self.assertRaises(ValueError): adoption.verify_member_migrations(original,current,rows,edits)

    def test_v2_reference_addition_requires_separate_exact_leaf_approval(self):
        with tempfile.TemporaryDirectory() as directory:
            helper,v,manual=self.fixture(directory); row=v['batch']['records'][0]; before=copy.deepcopy(row['source_before'])
            bid=next(iter(v['current']['slot_bindings'])); after=copy.deepcopy(before)
            after['content']['reference_for_fixture']=bid; row['source_after']=after; v['current']['candidates'][A]=copy.deepcopy(after)
            row['delta']=[dict(pointer='/content/reference_for_fixture',before_exists=False,before=None,after_exists=True,after=bid,reason='Explicit actual source guard reference addition.')]
            row['reference_bindings']={bid:copy.deepcopy(v['current']['slot_bindings'][bid])}
            p=row['proof']; p.update(meaning_sha256=native.meaning_sha256(after),reference_sha256=native.referenced_records(after,v['current']))
            p['review']['source_correction']=dict(before_sha256=native.meaning_sha256(before),after_sha256=p['meaning_sha256'],rationale='Complete exact new reference source reread.')
            self.refresh(helper,v,manual); digest=review.c.digest(row)
            manual['source_approvals']=[dict(candidate_id=A,review_sha256=digest,before=before,after=after,delta=row['delta'],reason='Whole reference-bearing source approval.')]
            with self.assertRaisesRegex(ValueError,'reference approval'): self.build(v,manual)
            manual['reference_approvals']=[dict(candidate_id=A,review_sha256=digest,pointer='/content/reference_for_fixture',before_exists=False,before=None,
                after_exists=True,after=bid,reason='Exact independently approved added guard leaf.')]
            proposed,_=self.build(v,manual); self.assertEqual(proposed['candidates'][A]['content']['reference_for_fixture'],bid)
            manual['reference_approvals'][0]['after_exists']=False
            with self.assertRaisesRegex(ValueError,'reference approval'): self.build(v,manual)


    def test_v2_unknown_or_unconsumed_condition_schemas_are_rejected(self):
        for bad in ({'subject_applicability':{'for_any':['human']}},
                    {'subject_applicability':{'require_domain_match':'yes'}},
                    {'subject_applicability':{'subject_categories':'human'}},
                    {'subject_applicability':{'allow_domains':['people','people']}},{}):
            with self.subTest(bad=bad),tempfile.TemporaryDirectory() as directory:
                helper,v,manual=self.fixture(directory)
                manual['records'][A]['bindings']['surface_material']['conditions']=bad
                with self.assertRaises(ValueError): self.build(v,manual)

    def test_v2_cannot_silently_undo_an_unrelated_current_binding_edit_to_historical_value(self):
        with tempfile.TemporaryDirectory() as directory:
            helper,v,manual=self.fixture(directory); bid=next(iter(v['current']['slot_bindings']))
            old=copy.deepcopy(v['original']['slot_bindings'][bid]); v['current']['slot_bindings'][bid]['weight']=0.4
            self.refresh(helper,v,manual)
            with self.assertRaisesRegex(ValueError,'binding approval'): self.build(v,manual)
            manual['binding_approvals']=[dict(candidate_id=A,review_sha256=manual['records'][A]['review_sha256'],before=old,
                current_before=copy.deepcopy(v['current']['slot_bindings'][bid]),after=old,reason='Explicitly reviewed restoring the final weight from the exact current input.')]
            proposed,_=self.build(v,manual); self.assertEqual(proposed['slot_bindings'][bid]['weight'],1.0)
            manual['binding_approvals'][0]['current_before']=old
            with self.assertRaisesRegex(ValueError,'binding approval'): self.build(v,manual)


if __name__ == '__main__': unittest.main()
