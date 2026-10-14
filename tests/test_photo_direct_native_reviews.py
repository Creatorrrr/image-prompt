"""Isolated authored fixtures; no production files, acceptance or status is generated."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

RUN = Path(__file__).resolve().parents[1] / 'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
sys.path.insert(0, str(RUN))
import native_reviews as n
import direct_review as dr
import photo_semantic_evidence as native
from tests import test_photo_direct_native_adoption as adoption_fixtures
from tests.test_photo_candidate_corpus import A, B

TASK = '/root/native_test_worker'


class NativeReviewsTests(unittest.TestCase):
    def put(self, root, name, value):
        path = root / name; path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True) + '\n')
        return {'file': name, 'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'sha256': dr.c.digest(value)}

    def fixture(self, directory):
        values = adoption_fixtures.NativeAdoptionTests().fixture(directory)
        root, here, original, baseline, order, old_rows, manual = values
        original = copy.deepcopy(original); current = copy.deepcopy(original)
        old = copy.deepcopy(old_rows[0])
        old['status'] = 'needs_boundary_review'
        old['uncertainties'] = [{'kind': 'history', 'detail': 'Original unresolved semantic scope.'}]
        # Freeze the historical pending authored judgement and its compiled locator separately.
        old_decision = {k:copy.deepcopy(old[k]) for k in ('candidate_id','meaning_summary','recommended_kind','corrections','roles','facts','rejected_boundaries','uncertainties','status','all_roles_considered')}
        self.put(root, old['authored_decision']['file'], {'decisions':[old_decision]})
        old['authored_decision']['sha256'] = dr.c.digest(old_decision)
        packet = json.loads((here/'packets/source.json').read_text())
        original_packet_ref = self.put(root, 'run/packets/history-source.json', packet)
        compiled_ref = self.put(root, 'run/decisions/history.json', {'decisions': [old]})
        locator = {'file': compiled_ref['file'], 'file_sha256': compiled_ref['file_sha256'],
                   'item': 1, 'row_sha256': dr.c.digest(old)}
        proof = copy.deepcopy(manual['records'][A]['proof'])
        proof['review']['original_review'] = {'candidate_id': A,
            'source_record_sha256': old['source_record_sha256'], 'catalog_sha256': old['catalog_sha256'],
            'decision_sha256': dr.c.digest(old), 'artifact': locator['file'] + '#item=1'}
        proof['review']['native_review'].update(reviewer=TASK, method='codex_subagent_direct_source_read')
        proof['review']['native_review']['native_contract_sha256'] = native.native_contract_sha256(proof)
        inp = {'schema': n.INPUT, 'actor': '/root', 'ids': [A],
               'original_snapshot': self.put(root, 'run/input/original.json', original),
               'current_snapshot': self.put(root, 'run/input/current.json', current),
               'order': self.put(root, 'run/input/order.json', order),
               'catalog_review': {'before': copy.deepcopy(original['slot_catalog']),
                   'after': copy.deepcopy(current['slot_catalog']), 'changes': [], 'reviewer': TASK,
                   'whole_catalog_reviewed': True, 'provenance': [self.put(root, 'run/catalog-review-memo.json', {'reviewer': TASK, 'basis': 'Explicit fixture full catalog reread.'})]},
               'original_decisions': {A: locator}, 'original_packets': {A:original_packet_ref}, 'required_revisions': {}}
        assignment = {'schema': n.ASSIGNMENT, 'actor': '/root', 'task_name': TASK, 'model': 'gpt-6.1-sol',
                      'reasoning_effort': 'high', 'ids': [A], 'ordinals': [0], 'input': {}}
        row = {'candidate_id': A, 'ordinal': 0, 'status': 'approved', 'rationale': 'Explicit new fixture judgement.',
               'source_before': copy.deepcopy(original['candidates'][A]), 'source_after': copy.deepcopy(current['candidates'][A]),
               'delta': [], 'original_compiled': locator, 'proof': proof, 'dependency_records': {}, 'reference_bindings': {},
               'source_reread_complete': True, 'reference_reread_complete': True, 'revision': None}
        batch = {'schema': n.BATCH, 'task_name': TASK, 'model': 'gpt-6.1-sol', 'reasoning_effort': 'high',
                 'assignment_sha256': '', 'input_sha256': '', 'prepared_count': 1, 'actual_read_count': 1, 'records': [row]}
        note = {'schema': n.NOTE, 'task_name': TASK, 'model': 'gpt-6.1-sol', 'reasoning_effort': 'high',
                'assignment_sha256': '', 'input_sha256': '', 'batch_sha256': '', 'prepared_count': 1,
                'actual_read_count': 1, 'whole_source_read_ids': [A], 'whole_dependency_read_ids': [A]}
        v = dict(root=root, here=here, original=original, current=current, old=old,
                 inp=inp, assignment=assignment, batch=batch, note=note)
        self.persist(v); return v

    def persist(self, v):
        root = v['root']; inp = v['inp']; assignment = v['assignment']
        # Hash binding only. Semantic values/statuses above are explicit fixture inputs.
        inp['current_snapshot'] = self.put(root, 'run/input/current.json', v['current'])
        assignment['input'] = self.put(root, 'run/input/native.json', inp)
        v['assignment_ref'] = self.put(root, 'run/assignment.json', assignment)
        for doc in (v['batch'], v['note']):
            doc.update(assignment_sha256=dr.c.digest(assignment), input_sha256=dr.c.digest(inp))
        v['batch_ref'] = self.put(root, 'run/authored/native.json', v['batch'])
        v['note']['batch_sha256'] = dr.c.digest(v['batch'])
        v['note_ref'] = self.put(root, 'run/worker-note.json', v['note'])

    def verify(self, v):
        return n.verify_batch('run/assignment.json', 'run/authored/native.json', 'run/worker-note.json', root=v['root'], here=v['here'])

    def attest_proof(self, v):
        p = v['batch']['records'][0]['proof']
        p['review']['native_review']['native_contract_sha256'] = native.native_contract_sha256(p)

    def latest(self, v, *, status=None):
        checked = self.verify(v)
        acceptance = {'schema': n.ACCEPTANCE, 'actor': '/root',
            **{k: checked[k] for k in ('assignment_sha256','input_sha256','batch_sha256','note_sha256')},
            'reviews': {A: {'review_sha256': dr.c.digest(v['batch']['records'][0]),
                            'status': status or v['batch']['records'][0]['status']}},
            'reason': 'Explicit root fixture acceptance, not generated semantic approval.'}
        manifest = {'schema': n.LATEST, 'actor': '/root', 'reason': 'Exact fixture latest set.',
            'original_snapshot': v['inp']['original_snapshot'], 'current_snapshot': v['inp']['current_snapshot'],
            'order': v['inp']['order'], 'batches': [{'assignment': v['assignment_ref'], 'batch': v['batch_ref'],
                'note': v['note_ref'], 'acceptance': self.put(v['root'], 'run/acceptance.json', acceptance)}]}
        self.put(v['root'], 'run/latest.json', manifest)
        return n.verify_latest('run/latest.json', root=v['root'], here=v['here'], expected_count=1)

    def test_read_only_shape_pass_preserves_original_pending_and_has_zero_authority(self):
        with tempfile.TemporaryDirectory() as directory:
            v = self.fixture(directory)
            before = {p: p.read_bytes() for p in v['root'].rglob('*') if p.is_file()}
            first = self.verify(v); self.assertEqual(first, self.verify(v))
            self.assertEqual(first['statuses']['approved'], 1)
            self.assertEqual(v['old']['status'], 'needs_boundary_review')
            self.assertFalse(first['root_accepted']); self.assertEqual(first['operational_native_qualified_count'], 0)
            self.assertEqual(before, {p:p.read_bytes() for p in v['root'].rglob('*') if p.is_file()})

    def test_current_catalog_added_role_and_changed_role_set_are_allowed_only_with_full_review(self):
        with tempfile.TemporaryDirectory() as directory:
            v = self.fixture(directory); catalog = v['current']['slot_catalog']
            new = copy.deepcopy(catalog['surface_material']); new['id'] = 'new_material'
            catalog['new_material'] = new
            v['inp']['catalog_review']['after'] = copy.deepcopy(catalog)
            v['inp']['catalog_review']['changes'] = [{'pointer': '/new_material', 'before_exists': False,
                'before': None, 'after_exists': True, 'after': new, 'reason': 'Explicitly reviewed new native role.'}]
            p = v['batch']['records'][0]['proof']; role = p['roles'].pop('surface_material')
            role['spec_sha256'] = dr.c.digest(new); p['roles']['new_material'] = role
            p['catalog_sha256'] = dr.c.digest(catalog); self.attest_proof(v); self.persist(v)
            result = self.latest(v)
            self.assertTrue(result['root_accepted']); self.assertFalse(result['production_count_gate'])
            self.assertEqual(set(result['records'][A]['proof']['roles']), {'new_material'})
            self.assertEqual(v['old']['roles'][0]['slot_id'], 'surface_material')
            v['inp']['catalog_review']['changes'] = []; self.persist(v)
            with self.assertRaisesRegex(ValueError, 'catalog additions'): self.verify(v)

    def test_pending_is_not_approved_by_shape_or_root_status_rewrite(self):
        with tempfile.TemporaryDirectory() as directory:
            v = self.fixture(directory); v['batch']['records'][0]['status'] = 'pending'; self.persist(v)
            result = self.verify(v); self.assertEqual(result['statuses']['pending'], 1)
            with self.assertRaisesRegex(ValueError, 'exact worker judgement'): self.latest(v, status='approved')
            with self.assertRaisesRegex(ValueError, 'pending0'): self.latest(v)

    def test_separate_root_acceptance_and_full_production_gate_required(self):
        with tempfile.TemporaryDirectory() as directory:
            v = self.fixture(directory); result = self.latest(v)
            self.assertFalse(result['canonical_applied']); self.assertEqual(result['operational_native_qualified_count'], 0)
            with self.assertRaisesRegex(ValueError, 'all18250'):
                n.verify_latest('run/latest.json', root=v['root'], here=v['here'])
            m = json.loads((v['root']/'run/latest.json').read_text()); m['batches'][0]['acceptance']['file'] = 'run/missing.json'
            self.put(v['root'], 'run/latest.json', m)
            with self.assertRaises(FileNotFoundError):
                n.verify_latest('run/latest.json', root=v['root'], here=v['here'], expected_count=1)

    def test_original_compiled_locator_cannot_be_authored_or_rewritten(self):
        for defect in ('authored', 'bytes', 'row_hash', 'catalog_hash', 'proof_locator', 'legacy_item_locator'):
            with self.subTest(defect=defect), tempfile.TemporaryDirectory() as directory:
                v = self.fixture(directory); row = v['batch']['records'][0]; loc = row['original_compiled']
                if defect == 'authored': loc['file'] = 'run/authored/decision.json'
                elif defect == 'bytes': (v['root']/loc['file']).write_text('{}')
                elif defect == 'row_hash': loc['row_sha256'] = '0'*64
                elif defect == 'catalog_hash':
                    old = copy.deepcopy(v['old']); old['catalog_sha256'] = '0'*64
                    ref = self.put(v['root'], loc['file'], {'decisions':[old]}); loc.update(file_sha256=ref['file_sha256'],row_sha256=dr.c.digest(old))
                elif defect == 'legacy_item_locator':
                    row['proof']['review']['original_review']['artifact'] = loc['file']+'#1'
                    self.attest_proof(v)
                else:
                    row['proof']['review']['original_review']['artifact'] = v['old']['authored_decision']['file']
                    self.attest_proof(v)
                self.persist(v)
                with self.assertRaises(ValueError): self.verify(v)

    def test_assignment_input_note_and_counts_fail_closed(self):
        for defect in ('actor','model','effort','task','ordinal','foreign','input_hash','read_count','read_ids','prepared','bool_count'):
            with self.subTest(defect=defect), tempfile.TemporaryDirectory() as directory:
                v = self.fixture(directory)
                if defect == 'actor': v['assignment']['actor'] = TASK
                elif defect == 'model': v['batch']['model'] = 'other'
                elif defect == 'effort': v['note']['reasoning_effort'] = 'low'
                elif defect == 'task': v['note']['task_name'] = '/root/other'
                elif defect == 'ordinal': v['assignment']['ordinals'] = [1]
                elif defect == 'foreign': v['assignment']['ids'] = [B]
                elif defect == 'read_count': v['note']['actual_read_count'] = 0
                elif defect == 'read_ids': v['note']['whole_source_read_ids'] = []
                elif defect == 'prepared': v['batch']['prepared_count'] = 2
                elif defect == 'bool_count': v['batch']['actual_read_count'] = True
                self.persist(v)
                if defect == 'input_hash':
                    a = json.loads((v['root']/'run/assignment.json').read_text()); a['input']['sha256'] = '0'*64; self.put(v['root'],'run/assignment.json',a)
                with self.assertRaises(ValueError): self.verify(v)

    def test_partial_read_pending_stays_distinct_from_prepared(self):
        with tempfile.TemporaryDirectory() as directory:
            v = self.fixture(directory); row = v['batch']['records'][0]
            row.update(status='pending', proof=None, source_reread_complete=False, reference_reread_complete=False)
            v['batch']['actual_read_count'] = 0; v['note'].update(actual_read_count=0,whole_source_read_ids=[],whole_dependency_read_ids=[])
            self.persist(v); result = self.verify(v)
            self.assertEqual((result['prepared_count'],result['actual_read_count']), (1,0))
            row['status'] = 'approved'; self.persist(v)
            with self.assertRaisesRegex(ValueError, 'whole source'): self.verify(v)

    def test_exact_source_delta_and_full_meaning_correction_required(self):
        with tempfile.TemporaryDirectory() as directory:
            v = self.fixture(directory); row = v['batch']['records'][0]
            after = copy.deepcopy(row['source_after']); after['conditions'] = {'for_any':['human']}
            v['current']['candidates'][A] = after; row['source_after'] = copy.deepcopy(after)
            row['delta'] = [{'pointer':'/conditions','before_exists':True,'before':{},'after_exists':True,
                             'after':after['conditions'],'reason':'Explicit intrinsic guard review.'}]
            p = row['proof']; p['meaning_sha256'] = native.meaning_sha256(after)
            p['review']['source_correction'] = {'before_sha256':native.meaning_sha256(row['source_before']),
                'after_sha256':p['meaning_sha256'],'rationale':'The whole corrected guard was read.'}
            self.attest_proof(v); self.persist(v); self.verify(v)
            row['delta'][0]['before'] = {'for_any':['object']}; self.persist(v)
            with self.assertRaisesRegex(ValueError, 'exact before'): self.verify(v)

    def test_source_kind_and_reference_changes_need_explicit_full_delta(self):
        for field, value in [('record_kind','visual_profile'), ('content', {'en':'a satin garment surface','candidate_ref': B})]:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as directory:
                v = self.fixture(directory); row = v['batch']['records'][0]
                row['source_after'][field] = copy.deepcopy(value); v['current']['candidates'][A] = copy.deepcopy(row['source_after'])
                self.persist(v)
                with self.assertRaisesRegex(ValueError, 'before/after/delta'): self.verify(v)

    def test_pending_memo_requires_exact_new_worker_revision_and_root_acceptance(self):
        with tempfile.TemporaryDirectory() as directory:
            v = self.fixture(directory); prior = copy.deepcopy(v['batch']['records'][0])
            prior_ref = self.put(v['root'], 'run/authored/frozen-pilot.json', {'records':[prior]})
            memo_ref = self.put(v['root'], 'run/pending-memo.json', {'candidate_id':A,'status':'pending','reason':'Source intent unresolved.'})
            required = {'prior_review':{'artifact':prior_ref,'pointer':'/records/0','sha256':dr.c.digest(prior)},
                        'memo_artifacts':[memo_ref],'reason':'Root requires exact explicit re-review; no pilot exception.'}
            v['inp']['required_revisions'][A] = required; self.persist(v)
            with self.assertRaisesRegex(ValueError, 'explicit worker revision'): self.verify(v)
            row = v['batch']['records'][0]
            row['revision'] = {'prior_review':copy.deepcopy(required['prior_review']),
                'memo_artifacts':[memo_ref],'rationale':'Worker reread full source and keeps intent pending.'}
            row['status'] = 'pending'; self.persist(v); self.verify(v)
            with self.assertRaisesRegex(ValueError, 'pending0'): self.latest(v)
            row['revision']['prior_review']['sha256'] = '0'*64; self.persist(v)
            with self.assertRaisesRegex(ValueError, 'root-required revision'): self.verify(v)

    def test_native_v3_full_contract_spec_and_reviewer_cannot_be_faked_by_status(self):
        for defect in ('proof','meaning','contract','catalog','spec','whole','reviewer','units','effects','closure'):
            with self.subTest(defect=defect), tempfile.TemporaryDirectory() as directory:
                v = self.fixture(directory); p = v['batch']['records'][0]['proof']
                if defect == 'proof': v['batch']['records'][0]['proof'] = None
                elif defect == 'meaning': p['meaning_sha256'] = '0'*64
                elif defect == 'contract': p['review']['native_review']['native_contract_sha256'] = '0'*64
                elif defect == 'catalog': p['catalog_sha256'] = '0'*64
                elif defect == 'spec': p['roles']['surface_material']['spec_sha256'] = '0'*64
                elif defect == 'whole': p['review']['whole_source_reviewed'] = False
                elif defect == 'reviewer': p['review']['native_review']['reviewer'] = '/root/other'
                elif defect == 'units': p['source_units'] = []
                elif defect == 'effects': p['effect_sets']['base']['properties'] = []
                else: v['batch']['records'][0]['dependency_records'] = {B:copy.deepcopy(v['current']['candidates'][A])}
                if defect not in ('contract','proof'): self.attest_proof(v)
                self.persist(v)
                with self.assertRaises(ValueError): self.verify(v)

    def test_delta_rejects_overlap_missing_parent_and_guess_deletion(self):
        delta = {'pointer':'/content','before_exists':True,'before':{'en':'old'},'after_exists':True,
                 'after':{'en':'new'},'reason':'Exact fixture edit.'}
        for edits in ([delta,delta], [{**delta,'pointer':'/missing/en'}],
                      [{**delta,'pointer':'/absent','before_exists':False,'before':None,'after_exists':False,'after':None}]):
            with self.assertRaises(ValueError): n.apply_delta({'content':{'en':'old'}},edits)

    def test_historical_packet_and_authored_provenance_are_immutable(self):
        for defect in ('packet_bytes', 'packet_source', 'authored'):
            with self.subTest(defect=defect), tempfile.TemporaryDirectory() as directory:
                v = self.fixture(directory)
                if defect == 'packet_bytes':
                    path = v['root']/v['inp']['original_packets'][A]['file']; path.write_text('{}')
                elif defect == 'packet_source':
                    ref = v['inp']['original_packets'][A]; packet = n.artifact(v['root'], ref)
                    packet['source_sha256'] = '0'*64
                    v['inp']['original_packets'][A] = self.put(v['root'], ref['file'], packet)
                else:
                    path = v['root']/v['old']['authored_decision']['file']
                    doc = json.loads(path.read_text()); doc['decisions'][0]['status'] = 'approved'
                    path.write_text(json.dumps(doc))
                self.persist(v)
                with self.assertRaises(ValueError): self.verify(v)

    def test_binding_only_reference_expands_full_candidate_guard_closure(self):
        with tempfile.TemporaryDirectory() as directory:
            v = self.fixture(directory); row = v['batch']['records'][0]
            # Root's historical full snapshot includes B, though the A packet reads only A.
            child = copy.deepcopy(v['original']['candidates'][A]); child['id'] = B
            v['original']['candidates'][B] = copy.deepcopy(child)
            v['current']['candidates'][B] = copy.deepcopy(child)
            v['inp']['original_snapshot'] = self.put(v['root'], 'run/input/original.json', v['original'])
            v['inp']['order'] = self.put(v['root'], 'run/input/order.json', [A,B])
            packet = n.artifact(v['root'], v['inp']['original_packets'][A])
            packet['source_sha256'] = dr.c.digest(v['original'])
            v['inp']['original_packets'][A] = self.put(v['root'], 'run/packets/history-source.json', packet)
            v['old']['packet_sha256'] = dr.c.digest(packet)
            compiled = self.put(v['root'], 'run/decisions/history.json', {'decisions':[v['old']]})
            loc = row['original_compiled']; loc.update(file_sha256=compiled['file_sha256'],row_sha256=dr.c.digest(v['old']))
            bid = 'bind_'+'c'*32
            binding = copy.deepcopy(next(iter(v['current']['slot_bindings'].values())))
            binding.update(id=bid,candidate_id=B); v['current']['slot_bindings'][bid] = binding
            after = copy.deepcopy(row['source_after']); after['content']['explicit_guard_ref'] = bid
            v['current']['candidates'][A] = after; row['source_after'] = copy.deepcopy(after)
            row['delta'] = [{'pointer':'/content/explicit_guard_ref','before_exists':False,'before':None,
                'after_exists':True,'after':bid,'reason':'Root and worker explicitly reviewed this source guard reference.'}]
            row['dependency_records'] = {B:copy.deepcopy(child)}; row['reference_bindings'] = {bid:copy.deepcopy(binding)}
            proof = row['proof']; proof['meaning_sha256'] = native.meaning_sha256(after)
            proof['reference_sha256'] = native.referenced_records(after, v['current'])
            proof['review']['original_review']['decision_sha256'] = dr.c.digest(v['old'])
            proof['review']['source_correction'] = {'before_sha256':native.meaning_sha256(row['source_before']),
                'after_sha256':proof['meaning_sha256'],'rationale':'Whole new guard-reference source reread.'}
            self.attest_proof(v); self.persist(v); self.verify(v)
            row['dependency_records'].clear(); self.persist(v)
            with self.assertRaisesRegex(ValueError, 'reference source closure'): self.verify(v)
            row['dependency_records'] = {B:copy.deepcopy(child)}
            row['reference_bindings'][bid]['conditions'] = {'subject_applicability':{'subject_categories':['human']}}
            self.persist(v)
            with self.assertRaisesRegex(ValueError, 'binding definitions'): self.verify(v)

    def test_diagnostic_status_requires_explicit_diagnostic_source_and_empty_native_roles(self):
        with tempfile.TemporaryDirectory() as directory:
            v = self.fixture(directory); row = v['batch']['records'][0]
            before = row['source_before']; after = copy.deepcopy(before)
            after['record_kind'] = 'diagnostic'; after['effects'] = {'dimensions':[],'properties':[]}
            row['source_after'] = after; v['current']['candidates'][A] = copy.deepcopy(after)
            row['delta'] = [dict(pointer='/'+k,before_exists=True,before=before[k],after_exists=True,
                after=after[k],reason='Explicit diagnostic-only fixture judgement.') for k in ('record_kind','effects')]
            proof = row['proof']; proof.update(meaning_sha256=native.meaning_sha256(after),facts=[],roles={},
                owner_maps={'base':{'schema':native.OWNER_SCHEMA,'bindings':[]}},
                effect_sets={'base':{'dimensions':[],'properties':[]}})
            proof['source_units'] = [{'realization_id':'base','pointer':'/content/en','quote':after['content']['en'],
                                      'fact_refs':[],'disposition':'nonsemantic'}]
            proof['review']['source_correction'] = {'before_sha256':native.meaning_sha256(before),
                'after_sha256':proof['meaning_sha256'],'rationale':'Explicit full diagnostic source qualification.'}
            row['status'] = 'diagnostic_reviewed'; self.attest_proof(v); self.persist(v)
            self.assertEqual(self.verify(v)['statuses']['diagnostic_reviewed'],1)
            row['status'] = 'approved'; self.persist(v)
            with self.assertRaisesRegex(ValueError, 'positive native approval'): self.verify(v)

    def test_legacy_pilot_shape_has_no_implicit_exception_or_auto_conversion(self):
        with tempfile.TemporaryDirectory() as directory:
            v = self.fixture(directory)
            v['assignment']['schema'] = 'photo-codex-native-delegation/v1'; self.persist(v)
            with self.assertRaisesRegex(ValueError, 'root task/model/high'): self.verify(v)

    def test_duplicate_json_keys_and_nonfinite_values_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); path = root/'bad.json'
            for raw in ('{"status":"pending","status":"approved"}', '{"value":NaN}'):
                path.write_text(raw)
                with self.assertRaises(ValueError): n.read_json(path)

    def archive_fixture(self, v):
        row = v['batch']['records'][0]; loc = row['original_compiled']; old = copy.deepcopy(v['old'])
        directory = 'run/revisions/ROOT-NORMALIZE-FIXTURE'
        original_bytes = (v['root']/loc['file']).read_bytes()
        archived_path = v['root']/directory/'history.json'; archived_path.parent.mkdir(parents=True)
        archived_path.write_bytes(original_bytes)
        archive_ref = {'file':str(archived_path.relative_to(v['root'])),
            'file_sha256':hashlib.sha256(original_bytes).hexdigest(),'sha256':dr.c.digest(json.loads(original_bytes))}
        new_decision = {'meaning_summary':'Explicit later sparse fixture amendment.','status':'approved'}
        authored = self.put(v['root'],'run/authored/sparse-amendment.json',{'amendments':[{'decision':new_decision}]})
        note = self.put(v['root'],'run/worker-notes/sparse-worker-note.json',{'task_name':TASK,'reread_count':1})
        after = copy.deepcopy(old); after.update(new_decision)
        after['authored_decision'] = {'file':authored['file'],'item':1,'sha256':dr.c.digest(new_decision)}
        manifest = {'schema':'photo-codex-sparse-amendment-normalization/v1','normalization_author':'/root',
            'worker_attestation':False,'root_all_worker_sources_read_claimed':False,
            'source_sha256':dr.c.digest(v['original']),
            'authored_document':{k:authored[k] for k in ('file','sha256')},
            'worker_note':{k:note[k] for k in ('file','sha256')},
            'replacements':[{'candidate_id':A,'registered_file':loc['file'],'registered_item':1,
                'before_registered_row_sha256':loc['row_sha256'],'previous_authored':old['authored_decision'],
                'decision':new_decision}]}
        manifest_ref = self.put(v['root'],'run/worker-notes/ROOT-NORMALIZE-FIXTURE.json',manifest)
        revision = {'schema':'photo-codex-worker-amendment-revision/v1','root_all_worker_sources_read_claimed':False,
            'normalization_manifest':{k:manifest_ref[k] for k in ('file','sha256')},
            'archive_hashes':{'history.json':loc['file_sha256']},
            'changes':[{'candidate_id':A,'before':old,'after':after,'before_sha256':dr.c.digest(old),'after_sha256':dr.c.digest(after)}],
            'native_changes_applied':False,'stage05_complete':False}
        revision_ref = self.put(v['root'],directory+'/REVISION.json',revision)
        self.put(v['root'],loc['file'],{'decisions':[after]})
        loc['archive'] = {'artifact':archive_ref,'revision':revision_ref,'normalization_manifest':manifest_ref}
        self.persist(v); return manifest, revision

    def test_explicit_actual_archive_survives_later_compiled_amendment(self):
        with tempfile.TemporaryDirectory() as directory:
            v = self.fixture(directory); self.archive_fixture(v)
            original_locator = copy.deepcopy(v['batch']['records'][0]['original_compiled'])
            checked = self.verify(v)
            self.assertTrue(checked['shape_valid'])
            self.assertEqual(checked['records'][A]['proof']['review']['original_review']['artifact'],original_locator['file']+'#item=1')
            self.assertEqual(v['old']['status'],'needs_boundary_review')
            v['batch']['records'][0]['original_compiled'].pop('archive'); self.persist(v)
            with self.assertRaisesRegex(ValueError, 'explicit archive evidence'): self.verify(v)

    def test_archive_wrong_row_file_hash_revision_directory_or_authority_rejected(self):
        for defect in ('row','file','hash','revision','directory','authority','authored_copy'):
            with self.subTest(defect=defect), tempfile.TemporaryDirectory() as directory:
                v = self.fixture(directory); manifest, revision = self.archive_fixture(v)
                loc = v['batch']['records'][0]['original_compiled']; archive = loc['archive']
                if defect == 'row':
                    revision['changes'][0]['before']['meaning_summary'] = 'Wrong preserved original row.'
                    revision['changes'][0]['before_sha256'] = dr.c.digest(revision['changes'][0]['before'])
                elif defect == 'file': manifest['replacements'][0]['registered_file'] = 'run/decisions/foreign.json'
                elif defect == 'hash': loc['file_sha256'] = '0'*64
                elif defect == 'revision': revision['archive_hashes']['history.json'] = '0'*64
                elif defect == 'authority': manifest['normalization_author'] = TASK
                else:
                    value = n.artifact(v['root'], archive['artifact'])
                    name = 'run/revisions/OTHER/history.json' if defect == 'directory' else 'run/authored/history.json'
                    archive['artifact'] = self.put(v['root'],name,value)
                archive['normalization_manifest'] = self.put(v['root'],archive['normalization_manifest']['file'],manifest)
                revision['normalization_manifest'] = {k:archive['normalization_manifest'][k] for k in ('file','sha256')}
                archive['revision'] = self.put(v['root'],archive['revision']['file'],revision)
                self.persist(v)
                with self.assertRaises(ValueError): self.verify(v)

    def paired_latest_fixture(self, directory, *, reference=False):
        v = self.fixture(directory); root = v['root']; original = v['original']
        original['candidates'][B] = copy.deepcopy(original['candidates'][A]); original['candidates'][B]['id'] = B
        bid = 'bind_'+'c'*32
        if reference:
            binding = copy.deepcopy(next(iter(original['slot_bindings'].values())))
            binding.update(id=bid,candidate_id=B); original['slot_bindings'][bid] = binding
            original['candidates'][A]['content']['explicit_guard_ref'] = bid
        v['inp']['original_snapshot'] = self.put(root,'run/input/original-pair.json',original)
        v['inp']['order'] = self.put(root,'run/input/order-pair.json',[A,B])
        rows = {}
        for ordinal, cid in enumerate((A,B)):
            old = copy.deepcopy(v['old']); old['candidate_id'] = cid; old.update(dr.binding(original,cid))
            decision = dr.authored_item(n.read_json(root/v['old']['authored_decision']['file']),1)
            decision['candidate_id'] = cid
            old['authored_decision'] = {'file':'run/authored/old-'+str(ordinal)+'.json','item':1,'sha256':dr.c.digest(decision)}
            self.put(root,old['authored_decision']['file'],{'decisions':[decision]})
            packet = {'ids':[cid],'source_sha256':dr.c.digest(original),'catalog_sha256':dr.c.digest(original['slot_catalog']),
                'records':{cid:original['candidates'][cid]},'references':{cid:dr.closure(original,cid)}}
            packet_ref = self.put(root,'run/packets/pair-'+str(ordinal)+'.json',packet)
            old['packet_sha256'] = dr.c.digest(packet)
            ref = self.put(root,'run/decisions/pair-'+str(ordinal)+'.json',{'decisions':[old]})
            loc = {'file':ref['file'],'file_sha256':ref['file_sha256'],'item':1,'row_sha256':dr.c.digest(old)}
            row = copy.deepcopy(v['batch']['records'][0]); row.update(candidate_id=cid,ordinal=ordinal,
                source_before=copy.deepcopy(original['candidates'][cid]),source_after=copy.deepcopy(original['candidates'][cid]),original_compiled=loc)
            proof = row['proof']; proof['meaning_sha256'] = native.meaning_sha256(row['source_after'])
            proof['reference_sha256'] = native.referenced_records(row['source_after'],original)
            proof['review']['original_review'] = dict(candidate_id=cid,source_record_sha256=old['source_record_sha256'],
                catalog_sha256=old['catalog_sha256'],decision_sha256=dr.c.digest(old),artifact=loc['file']+'#item=1')
            proof['review']['native_review']['native_contract_sha256'] = native.native_contract_sha256(proof)
            rows[cid] = (row,packet_ref)
        # B has a direct new source judgment. A's snapshot intentionally predates
        # this unrelated B correction unless A actually references B.
        final = copy.deepcopy(original); final['candidates'][B]['conditions'] = {'for_any':['human']}
        row = rows[B][0]; row['source_after'] = copy.deepcopy(final['candidates'][B])
        row['delta'] = [dict(pointer='/conditions',before_exists=True,before={},after_exists=True,
            after={'for_any':['human']},reason='Explicit independently read B correction.')]
        proof = row['proof']; proof['meaning_sha256'] = native.meaning_sha256(row['source_after'])
        proof['review']['source_correction'] = dict(before_sha256=native.meaning_sha256(row['source_before']),
            after_sha256=proof['meaning_sha256'],rationale='B full corrected source read.')
        proof['review']['native_review']['native_contract_sha256'] = native.native_contract_sha256(proof)
        entries = []
        for ordinal,cid in enumerate((A,B)):
            row,packet_ref = rows[cid]; current = copy.deepcopy(final if cid==B or reference else original)
            if reference:
                row['dependency_records'] = {B:copy.deepcopy(final['candidates'][B])}
                row['dependency_records'][B]['content']['role_evidence'] = copy.deepcopy(rows[B][0]['proof'])
                row['reference_bindings'] = {bid:copy.deepcopy(final['slot_bindings'][bid])}
                row['proof']['reference_sha256'] = native.referenced_records(row['source_after'],current)
                row['proof']['review']['native_review']['native_contract_sha256'] = native.native_contract_sha256(row['proof'])
            if cid==B: row.update(dependency_records={},reference_bindings={})
            inp = copy.deepcopy(v['inp']); inp.update(ids=[cid],original_decisions={cid:row['original_compiled']},original_packets={cid:packet_ref})
            inp['current_snapshot'] = self.put(root,'run/input/current-'+str(ordinal)+'.json',current)
            assignment = copy.deepcopy(v['assignment']); assignment.update(ids=[cid],ordinals=[ordinal],input=self.put(root,'run/input/native-'+str(ordinal)+'.json',inp))
            assignment_ref = self.put(root,'run/assignment-'+str(ordinal)+'.json',assignment)
            batch = copy.deepcopy(v['batch']); batch.update(records=[row],assignment_sha256=dr.c.digest(assignment),input_sha256=dr.c.digest(inp))
            batch_ref = self.put(root,'run/authored/native-'+str(ordinal)+'.json',batch)
            note = copy.deepcopy(v['note']); note.update(assignment_sha256=dr.c.digest(assignment),input_sha256=dr.c.digest(inp),
                batch_sha256=dr.c.digest(batch),whole_source_read_ids=[cid],whole_dependency_read_ids=[cid])
            note_ref = self.put(root,'run/note-'+str(ordinal)+'.json',note)
            verified = n.verify_batch(assignment_ref['file'],batch_ref['file'],note_ref['file'],root=root,here=v['here'])
            acceptance = {'schema':n.ACCEPTANCE,'actor':'/root',**{k:verified[k] for k in ('assignment_sha256','input_sha256','batch_sha256','note_sha256')},
                'reviews':{cid:{'review_sha256':dr.c.digest(row),'status':'approved'}},'reason':'Explicit independent fixture acceptance.'}
            entries.append(dict(assignment=assignment_ref,batch=batch_ref,note=note_ref,acceptance=self.put(root,'run/acceptance-'+str(ordinal)+'.json',acceptance)))
        manifest = dict(schema=n.LATEST,actor='/root',reason='Two independently reviewed contributing records.',
            original_snapshot=v['inp']['original_snapshot'],current_snapshot=self.put(root,'run/input/final.json',final),order=v['inp']['order'],batches=entries)
        self.put(root,'run/latest-pair.json',manifest)
        return v,manifest,final,bid

    def test_unrelated_cid_correction_reuses_exact_contributions_only_with_own_latest_approval(self):
        with tempfile.TemporaryDirectory() as directory:
            v,m,final,bid = self.paired_latest_fixture(directory)
            checked = n.verify_latest('run/latest-pair.json',root=v['root'],here=v['here'],expected_count=2)
            self.assertEqual(set(checked['records']),{A,B})
            self.assertNotEqual(checked['batch_verifications'][0]['current_source_sha256'],checked['current_source_sha256'])
            self.assertEqual(checked['batch_verifications'][1]['current_source_sha256'],checked['current_source_sha256'])
            m['batches'].pop(); self.put(v['root'],'run/latest-pair.json',m)
            with self.assertRaisesRegex(ValueError,'inventory'):
                n.verify_latest('run/latest-pair.json',root=v['root'],here=v['here'],expected_count=2)

    def test_latest_contributing_cid_reference_binding_policy_catalog_or_child_proof_changes_rejected(self):
        for defect in ('own','reference','binding','policy','catalog','proof'):
            with self.subTest(defect=defect), tempfile.TemporaryDirectory() as directory:
                v,m,final,bid = self.paired_latest_fixture(directory,reference=True)
                n.verify_latest('run/latest-pair.json',root=v['root'],here=v['here'],expected_count=2)
                if defect=='own': final['candidates'][A]['provenance'].append('Unreviewed final-only source provenance.')
                elif defect=='reference': final['candidates'][B]['conditions'] = {'for_any':['object']}
                elif defect=='binding': final['slot_bindings'][bid]['weight'] = 0.8
                elif defect=='policy': final['policies']['unreviewed_policy'] = {'enabled':True}
                elif defect=='catalog': final['slot_catalog']['surface_material']['description'] = 'Unreviewed spec change.'
                else:
                    # Re-author the A batch hashes/acceptance, but deliberately
                    # bind a child proof different from B's accepted latest one.
                    entry=m['batches'][0]; batch=n.artifact(v['root'],entry['batch'])
                    p=batch['records'][0]['dependency_records'][B]['content']['role_evidence']
                    p['review']['basis'] += ' Distinct full reread.'
                    p['review']['native_review']['native_contract_sha256']=native.native_contract_sha256(p)
                    entry['batch']=self.put(v['root'],entry['batch']['file'],batch)
                    note=n.artifact(v['root'],entry['note']); note['batch_sha256']=dr.c.digest(batch)
                    entry['note']=self.put(v['root'],entry['note']['file'],note)
                    acceptance=n.artifact(v['root'],entry['acceptance']); acceptance.update(batch_sha256=dr.c.digest(batch),note_sha256=dr.c.digest(note))
                    acceptance['reviews'][A]['review_sha256']=dr.c.digest(batch['records'][0])
                    entry['acceptance']=self.put(v['root'],entry['acceptance']['file'],acceptance)
                m['current_snapshot']=self.put(v['root'],'run/input/final.json',final); self.put(v['root'],'run/latest-pair.json',m)
                with self.assertRaises(ValueError): n.verify_latest('run/latest-pair.json',root=v['root'],here=v['here'],expected_count=2)



if __name__ == '__main__': unittest.main()
