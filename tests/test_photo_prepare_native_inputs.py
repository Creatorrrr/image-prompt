"""Mechanical root-authored input fixtures; no semantic classification or models."""
import copy
import hashlib
import gzip
import json
from pathlib import Path
import sys
import tempfile
import unittest

RUN=Path(__file__).resolve().parents[1]/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
sys.path.insert(0,str(RUN))
import prepare_native_inputs as prep
import native_reviews as reviews
from tests import test_photo_direct_native_reviews as fixtures
from tests.test_photo_candidate_corpus import A,B


class PrepareNativeInputsTests(unittest.TestCase):
    def fixture(self,directory,*,pair=False):
        helper=fixtures.NativeReviewsTests()
        if pair:
            v,manifest,final,bid=helper.paired_latest_fixture(directory,reference=True)
            assignment=reviews.artifact(v['root'],manifest['batches'][0]['assignment'])
            v['inp']=reviews.artifact(v['root'],assignment['input']); v['current']=final
        else: v=helper.fixture(directory)
        root=v['root']; original=v['original']; current=v['current']
        catalog={'schema':prep.CATALOG,'actor':'/root','status':'final_approved',
            'catalog':helper.put(root,'run/root-final-catalog.json',current['slot_catalog']),
            'catalog_count':len(current['slot_catalog']),'catalog_ids':sorted(current['slot_catalog']),
            'catalog_sha256':prep.c.digest(current['slot_catalog']),'review':copy.deepcopy(v['inp']['catalog_review']),
            'reason':'Explicit fixture root approval of the entire final catalog.'}
        source={'schema':prep.SOURCE,'actor':'/root','original_source_sha256':prep.c.digest(original),
            'current_source_sha256':prep.c.digest(current),'changes':[],'binding_changes':[],'policy_change':None,
            'reason':'Explicit complete root fixture source proposal, not native approval.'}
        memo=helper.put(root,'run/root-proposal-memo.json',{'reason':'Directly authored fixture proposal approved for input preparation.'})
        if pair:
            source['changes']=[dict(candidate_id=B,before=copy.deepcopy(original['candidates'][B]),after=copy.deepcopy(current['candidates'][B]),
                delta=[dict(pointer='/conditions',before_exists=True,before={},after_exists=True,after={'for_any':['human']},reason='Explicit B fixture proposal.')],
                reason='Explicit complete B fixture source proposal.',provenance=[memo])]
        selection={'schema':prep.SELECTION,'actor':'/root','original_source_sha256':prep.c.digest(original),
            'records':{A:{'locator':copy.deepcopy(v['inp']['original_decisions'][A]),'packet':copy.deepcopy(v['inp']['original_packets'][A]),
                'reason':'Explicit exact selected historical compiled item.'}},'reason':'Root selects this original without changing its status.'}
        plan={'schema':prep.PLAN,'actor':'/root','original_snapshot':copy.deepcopy(v['inp']['original_snapshot']),
            'current_proposal':{},'order':copy.deepcopy(v['inp']['order']),'catalog_approval':{},'source_approval':{},'original_selection':{},
            'assignment':{'task_name':'/root/native_test_worker','model':'gpt-6.1-sol','reasoning_effort':'high','start':0,'end':1,'ids':[A]},
            'required_revisions':{},'reason':'Explicit fixture root assignment and exact approved source/catalog input set.'}
        v.update(helper=helper,catalog=catalog,source_approval=source,selection=selection,plan=plan,memo=memo)
        self.persist(v); return v

    def persist(self,v):
        helper=v['helper']; root=v['root']; plan=v['plan']
        plan['current_proposal']=helper.put(root,'run/root-current-proposal.json',v['current'])
        v['source_approval']['current_source_sha256']=prep.c.digest(v['current'])
        plan['catalog_approval']=helper.put(root,'run/root-catalog-approval.json',v['catalog'])
        plan['source_approval']=helper.put(root,'run/root-source-approval.json',v['source_approval'])
        plan['original_selection']=helper.put(root,'run/root-original-selection.json',v['selection'])
        v['plan_ref']=helper.put(root,'run/root-preparation-plan.json',plan)

    def build(self,v):
        return prep.prepare(v['plan_ref'],'isolated-input',actor='/root',root=v['root'],here=v['here'],expected_count=len(v['original']['candidates']))

    def write(self,v):
        return prep.write_inputs(v['plan_ref'],'isolated-input',actor='/root',root=v['root'],here=v['here'],expected_count=len(v['original']['candidates']))

    def test_pure_deterministic_preparation_preserves_history_and_has_zero_actual_reads(self):
        with tempfile.TemporaryDirectory() as directory:
            v=self.fixture(directory); before={p:p.read_bytes() for p in v['root'].rglob('*') if p.is_file()}
            output,docs=self.build(v); self.assertEqual((output,docs),self.build(v)); self.assertFalse(output.exists())
            self.assertEqual(before,{p:p.read_bytes() for p in v['root'].rglob('*') if p.is_file()})
            self.assertEqual(set(docs),{'INPUT.json','ASSIGNMENT.json','PREPARED-PACKET.json','PREPARATION.json'})
            receipt=docs['PREPARATION.json']; self.assertEqual((receipt['prepared_count'],receipt['actual_read_count']),(1,0))
            self.assertEqual(receipt['operational_native_qualified_count'],0); self.assertFalse(receipt['production_count_gate'])
            packet=docs['PREPARED-PACKET.json']; self.assertEqual(packet['historical_statuses'][A],'needs_boundary_review')
            self.assertEqual(packet['historical_compiled_rows'][A],v['old'])
            self.assertTrue(packet['original_compiled_artifacts'][A].endswith('#item=1'))
            self.assertEqual(docs['INPUT.json']['original_decisions'][A],v['selection']['records'][A]['locator'])
            self.assertEqual(docs['INPUT.json']['current_snapshot'],v['plan']['current_proposal'])
            self.assertNotIn('proof',docs['ASSIGNMENT.json']); self.assertNotIn('status',docs['ASSIGNMENT.json'])

    def test_immutable_writer_only_adds_input_bundle_and_actual_artifact_hashes_match(self):
        with tempfile.TemporaryDirectory() as directory:
            v=self.fixture(directory); before={p:p.read_bytes() for p in v['root'].rglob('*') if p.is_file()}
            output,receipt=self.write(v); self.assertEqual(output,v['here']/'native-inputs/prepared/isolated-input')
            self.assertEqual(before,{p:p.read_bytes() for p in before})
            for ref in receipt['documents'].values(): reviews.artifact(v['root'],ref)
            assignment=reviews.read_json(output/'ASSIGNMENT.json'); reviews.artifact(v['root'],assignment['input'])
            with self.assertRaisesRegex(ValueError,'new immutable'): self.write(v)
            with self.assertRaises(ValueError): prep.prepare(v['plan_ref'],'../escape',actor='/root',root=v['root'],here=v['here'],expected_count=1)

    def test_emitted_input_assignment_is_consumable_without_fabricating_worker_review(self):
        with tempfile.TemporaryDirectory() as directory:
            v=self.fixture(directory); output,receipt=self.write(v); assignment=reviews.read_json(output/'ASSIGNMENT.json')
            # This is a separately authored positive synthetic worker fixture,
            # not produced by the preparer. Only fixture bookkeeping is rebound.
            batch=copy.deepcopy(v['batch']); note=copy.deepcopy(v['note'])
            for doc in (batch,note): doc.update(assignment_sha256=prep.c.digest(assignment),input_sha256=assignment['input']['sha256'])
            batch_ref=v['helper'].put(v['root'],'run/authored/separate-worker-review.json',batch)
            note['batch_sha256']=prep.c.digest(batch); note_ref=v['helper'].put(v['root'],'run/separate-worker-note.json',note)
            checked=reviews.verify_batch(str((output/'ASSIGNMENT.json').relative_to(v['root'])),batch_ref['file'],note_ref['file'],root=v['root'],here=v['here'])
            self.assertTrue(checked['shape_valid']); self.assertEqual(checked['actual_read_count'],1)
            self.assertEqual(receipt['actual_read_count'],0); self.assertFalse(receipt['worker_read_attestation_written'])

    def test_full_transitive_guard_closure_is_only_copied_and_never_qualified(self):
        with tempfile.TemporaryDirectory() as directory:
            v=self.fixture(directory,pair=True); _,docs=self.build(v); packet=docs['PREPARED-PACKET.json']
            self.assertEqual(set(packet['references'][A]),{B}); self.assertEqual(packet['references'][A][B],v['current']['candidates'][B])
            bid=next(iter(packet['reference_bindings'][A])); self.assertEqual(packet['reference_bindings'][A][bid],v['current']['slot_bindings'][bid])
            self.assertNotIn('role_evidence',packet['references'][A][B]['content'])
            self.assertEqual(packet['actual_read_count'],0)

    def test_provisional_or_mismatched_catalog_approval_is_rejected_without_fixed_role_count(self):
        for defect in ('provisional','actor','count','bool_count','ids','hash','artifact','review'):
            with self.subTest(defect=defect),tempfile.TemporaryDirectory() as directory:
                v=self.fixture(directory); catalog=v['catalog']
                if defect=='provisional': catalog['status']='provisional'
                elif defect=='actor': catalog['actor']='/root/worker'
                elif defect=='count': catalog['catalog_count']+=1
                elif defect=='bool_count': catalog['catalog_count']=True
                elif defect=='ids': catalog['catalog_ids']=[]
                elif defect=='hash': catalog['catalog_sha256']='0'*64
                elif defect=='artifact': catalog['catalog']['sha256']='0'*64
                else: catalog['review']['whole_catalog_reviewed']=False
                self.persist(v)
                with self.assertRaises(ValueError): self.build(v)
        # This synthetic catalog is deliberately neither141 nor142. Only its
        # explicit exact root identity/count/hash approval controls preparation.
        with tempfile.TemporaryDirectory() as directory:
            v=self.fixture(directory); self.assertNotIn(v['catalog']['catalog_count'],(141,142)); self.build(v)

    def test_root_actor_assignment_range_count_and_exact_plan_hash_are_required(self):
        for defect in ('actor','model','effort','start_bool','range','ids','unknown','selection'):
            with self.subTest(defect=defect),tempfile.TemporaryDirectory() as directory:
                v=self.fixture(directory)
                if defect=='actor': v['plan']['actor']='/root/worker'
                elif defect=='model': v['plan']['assignment']['model']='other'
                elif defect=='effort': v['plan']['assignment']['reasoning_effort']='low'
                elif defect=='start_bool': v['plan']['assignment']['start']=False
                elif defect=='range': v['plan']['assignment']['end']=2
                elif defect=='ids': v['plan']['assignment']['ids']=[B]
                elif defect=='unknown': v['plan']['source_guess']=[]
                else: v['selection']['records']={}
                self.persist(v)
                with self.assertRaises(ValueError): self.build(v)
        with tempfile.TemporaryDirectory() as directory:
            v=self.fixture(directory)
            with self.assertRaisesRegex(ValueError,'full18250'): prep.prepare(v['plan_ref'],'production',actor='/root',root=v['root'],here=v['here'])
            with self.assertRaisesRegex(ValueError,'root-only'): prep.prepare(v['plan_ref'],'x',actor='/root/worker',root=v['root'],here=v['here'],expected_count=1)
            v['plan_ref']['file_sha256']='0'*64
            with self.assertRaisesRegex(ValueError,'artifact bytes'): self.build(v)

    def exact_source_change(self,v):
        before=copy.deepcopy(v['original']['candidates'][A]); after=copy.deepcopy(before); after['conditions']={'for_any':['human']}
        v['current']['candidates'][A]=after
        change=dict(candidate_id=A,before=before,after=copy.deepcopy(after),delta=[dict(pointer='/conditions',before_exists=True,before={},
            after_exists=True,after=after['conditions'],reason='An explicit authored existing fixture correction.')],
            reason='Root selected this complete existing correction for preparation only.',provenance=[v['memo']])
        v['source_approval']['changes']=[change]; self.persist(v); return change

    def test_only_root_exact_complete_source_corrections_are_copied_and_pending_remains_pending(self):
        with tempfile.TemporaryDirectory() as directory:
            v=self.fixture(directory); self.exact_source_change(v); _,docs=self.build(v)
            self.assertEqual(docs['PREPARED-PACKET.json']['current_records'][A]['conditions'],{'for_any':['human']})
            self.assertEqual(docs['PREPARED-PACKET.json']['historical_statuses'][A],'needs_boundary_review')
            self.assertFalse(docs['PREPARATION.json']['native_proof_written'])
        for defect in ('missing','before','after','delta','provenance','identity','status'):
            with self.subTest(defect=defect),tempfile.TemporaryDirectory() as directory:
                v=self.fixture(directory); change=self.exact_source_change(v)
                if defect=='missing': v['source_approval']['changes']=[]
                elif defect=='before': change['before']['conditions']={'for_any':['object']}
                elif defect=='after': change['after']['conditions']={}
                elif defect=='delta': change['delta']=[]
                elif defect=='provenance': change['provenance']=[]
                elif defect=='identity': v['current']['candidates'][A]['id']=B
                else: change['native_status']='approved'
                self.persist(v)
                with self.assertRaises(ValueError): self.build(v)

    def test_historical_recommended_kind_and_corrections_are_not_automatically_applied(self):
        with tempfile.TemporaryDirectory() as directory:
            v=self.fixture(directory); old=copy.deepcopy(v['old']); old['recommended_kind']='visual_profile'
            old['corrections']=[dict(pointer='/conditions',before={},after={'for_any':['human']},reason='Historical unresolved fixture correction.')]
            authored=reviews.read_json(v['root']/old['authored_decision']['file']); decision=authored['decisions'][0]
            decision.update(recommended_kind=old['recommended_kind'],corrections=old['corrections'])
            v['helper'].put(v['root'],old['authored_decision']['file'],authored); old['authored_decision']['sha256']=prep.c.digest(decision)
            loc=v['selection']['records'][A]['locator']; ref=v['helper'].put(v['root'],loc['file'],{'decisions':[old]})
            loc.update(file_sha256=ref['file_sha256'],row_sha256=prep.c.digest(old)); self.persist(v)
            _,docs=self.build(v); after=docs['PREPARED-PACKET.json']['current_records'][A]
            self.assertEqual(after,v['original']['candidates'][A]); self.assertNotEqual(after['record_kind'],'visual_profile')
            self.assertEqual(docs['PREPARED-PACKET.json']['historical_compiled_rows'][A],old)

    def test_native_proof_creation_or_reviewer_resigning_is_rejected_even_inside_root_source_proposal(self):
        with tempfile.TemporaryDirectory() as directory:
            v=self.fixture(directory); before=copy.deepcopy(v['original']['candidates'][A]); after=copy.deepcopy(before)
            after['content']['role_evidence']=copy.deepcopy(v['batch']['records'][0]['proof']); v['current']['candidates'][A]=after
            v['source_approval']['changes']=[dict(candidate_id=A,before=before,after=after,
                delta=[dict(pointer='/content/role_evidence',before_exists=False,before=None,after_exists=True,after=after['content']['role_evidence'],reason='Unsupported proof installation.')],
                reason='This remains forbidden in input preparation.',provenance=[v['memo']])]
            self.persist(v)
            with self.assertRaisesRegex(ValueError,'create, convert or re-sign'): self.build(v)

    def test_explicit_archived_compiled_history_uses_original_declared_locator_and_status(self):
        with tempfile.TemporaryDirectory() as directory:
            v=self.fixture(directory); v['helper'].archive_fixture(v)
            v['selection']['records'][A]['locator']=copy.deepcopy(v['batch']['records'][0]['original_compiled']); self.persist(v)
            _,docs=self.build(v); loc=v['selection']['records'][A]['locator']
            self.assertEqual(docs['INPUT.json']['original_decisions'][A],loc)
            self.assertEqual(docs['PREPARED-PACKET.json']['original_compiled_artifacts'][A],loc['file']+'#item=1')
            self.assertEqual(docs['PREPARED-PACKET.json']['historical_statuses'][A],'needs_boundary_review')
            live=reviews.read_json(v['root']/loc['file']); self.assertEqual(live['decisions'][0]['status'],'approved')
            loc['archive']['artifact']['file']='run/authored/decision.json'; self.persist(v)
            with self.assertRaises(ValueError): self.build(v)

    def test_pending_revision_and_frozen_legacy_strings_are_preserved_without_conversion(self):
        with tempfile.TemporaryDirectory() as directory:
            v=self.fixture(directory); prior={'records':[{'status':'pending','reviewer':'/root/old_pilot-suffix',
                'proof':{'artifact':'run/decisions/old-pilot.json#1','literal':'frozen old pilot bytes'}}]}
            prior_ref=v['helper'].put(v['root'],'run/authored/frozen-legacy-pilot.json',prior)
            memo_ref=v['helper'].put(v['root'],'run/pending-reread-memo.json',{'candidate_id':A,'status':'pending','reason':'Explicit future reread required.'})
            requirement=dict(prior_review=dict(artifact=prior_ref,pointer='/records/0',sha256=prep.c.digest(prior['records'][0])),memo_artifacts=[memo_ref],reason='Root requires a separate actual worker revision.')
            v['plan']['required_revisions']={A:requirement}; self.persist(v)
            before=(v['root']/prior_ref['file']).read_bytes(); _,docs=self.build(v)
            self.assertEqual((v['root']/prior_ref['file']).read_bytes(),before)
            self.assertEqual(docs['INPUT.json']['required_revisions'],{A:requirement})
            self.assertEqual(docs['PREPARATION.json']['actual_read_count'],0)
            v['plan']['required_revisions'][A]['prior_review']['sha256']='0'*64; self.persist(v)
            with self.assertRaisesRegex(ValueError,'prior judgement digest'): self.build(v)

    def test_explicit_catalog_addition_uses_approved_roster_count_and_never_adds_candidate_roles(self):
        with tempfile.TemporaryDirectory() as directory:
            v=self.fixture(directory); catalog=v['current']['slot_catalog']
            added=copy.deepcopy(catalog['surface_material']); added['id']='reviewed_new_pattern'
            catalog['reviewed_new_pattern']=added
            approval=v['catalog']; approval.update(catalog_count=len(catalog),catalog_ids=sorted(catalog),catalog_sha256=prep.c.digest(catalog),
                catalog=v['helper'].put(v['root'],'run/root-final-catalog.json',catalog))
            approval['review']['after']=copy.deepcopy(catalog)
            approval['review']['changes']=[dict(pointer='/reviewed_new_pattern',before_exists=False,before=None,after_exists=True,
                after=added,reason='Explicitly authored synthetic root final new-role spec.')]
            self.persist(v); _,docs=self.build(v)
            self.assertEqual(docs['INPUT.json']['catalog_review']['after'],catalog)
            self.assertEqual(docs['PREPARED-PACKET.json']['current_records'][A],v['original']['candidates'][A])
            self.assertNotIn('role_evidence',docs['PREPARED-PACKET.json']['current_records'][A]['content'])

    def test_binding_and_policy_proposals_require_exact_complete_root_approval(self):
        for defect in ('binding_missing','binding_before','binding_provenance','policy_missing','policy_before','policy_provenance'):
            with self.subTest(defect=defect),tempfile.TemporaryDirectory() as directory:
                v=self.fixture(directory); before=copy.deepcopy(next(iter(v['original']['slot_bindings'].values())))
                after=copy.deepcopy(before); after['weight']=0.6; v['current']['slot_bindings'][after['id']]=after
                v['current']['policies']['explicit_fixture_policy']={'enabled':True}
                changes=[dict(binding_id=after['id'],before=before,after=after,reason='Exact root-authored fixture weight proposal.',provenance=[v['memo']])]
                policy=dict(before=copy.deepcopy(v['original']['policies']),after=copy.deepcopy(v['current']['policies']),reason='Exact root-authored whole policy proposal.',provenance=[v['memo']])
                v['source_approval'].update(binding_changes=changes,policy_change=policy); self.persist(v)
                _,docs=self.build(v); self.assertEqual(docs['PREPARATION.json']['actual_read_count'],0)
                if defect=='binding_missing': v['source_approval']['binding_changes']=[]
                elif defect=='binding_before': changes[0]['before']['weight']=0.2
                elif defect=='binding_provenance': changes[0]['provenance']=[]
                elif defect=='policy_missing': v['source_approval']['policy_change']=None
                elif defect=='policy_before': policy['before']={'guessed':True}
                else: policy['provenance']=[]
                self.persist(v)
                with self.assertRaises(ValueError): self.build(v)

    def test_compressed_original_snapshot_raw_bytes_and_ref_are_not_rewritten(self):
        with tempfile.TemporaryDirectory() as directory:
            v=self.fixture(directory); raw=gzip.compress(prep.c.canonical_bytes(v['original']),mtime=0)
            path=v['root']/'run/frozen-original.json.gz'; path.write_bytes(raw)
            ref=dict(file=str(path.relative_to(v['root'])),file_sha256=hashlib.sha256(raw).hexdigest(),sha256=prep.c.digest(v['original']))
            v['plan']['original_snapshot']=ref; self.persist(v); output,receipt=self.write(v)
            inp=reviews.read_json(output/'INPUT.json'); self.assertEqual(inp['original_snapshot'],ref)
            self.assertEqual(path.read_bytes(),raw); self.assertEqual(reviews.artifact(v['root'],ref),v['original'])
            self.assertEqual(receipt['actual_read_count'],0)


if __name__=='__main__': unittest.main()
