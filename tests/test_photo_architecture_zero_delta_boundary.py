"""V14's exact source-byte transition cannot authorize any pack change.

Fast unit replays mock only the generator subprocess. Real CLI before/after
receipts and final default-dispatch replay are separate production evidence.
"""
from __future__ import annotations
import copy
import hashlib
import json
import zipfile
from pathlib import Path
import shutil
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
ILLUSTRATION = ROOT / 'skills/subculture-illustration-image-generator'
EVIDENCE = Path('docs/research-evidence/photo-prompt/architecture-zero-delta-v14-20261004')
sys.path.insert(0, str(ILLUSTRATION / 'scripts'))
from photo_prompt_fixtures import pinned_v17_validator


class ArchitectureZeroDeltaBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global ROOT, ILLUSTRATION, v
        live_root = ROOT
        cls.source_temp = tempfile.TemporaryDirectory(prefix="immutable-v14-parent-")
        cls.addClassCleanup(cls.source_temp.cleanup)
        source_root = Path(cls.source_temp.name)
        archive = live_root / "docs/research-evidence/photo-prompt/motion-graphics-main-merge-20261004/V14-source-parent.zip"
        if hashlib.sha256(archive.read_bytes()).hexdigest() != "191eba6829139e34f0ad51cce324f6c4a000531eb7ac0c8f03e524781407a47a":
            raise AssertionError("Frozen V14 source archive drift")
        with zipfile.ZipFile(archive) as saved:
            if any(Path(name).is_absolute() or ".." in Path(name).parts for name in saved.namelist()):
                raise AssertionError("Unsafe historical source path")
            saved.extractall(source_root)
        validator_path = source_root / "skills/subculture-illustration-image-generator/scripts/validate_illustration_assets.py"
        validator_path.parent.mkdir(parents=True, exist_ok=True)
        v = pinned_v17_validator(source_root)
        descriptor = source_root / "skills/subculture-illustration-image-generator/assets/universal_scene_baseline_v2.json"
        raw = descriptor.read_bytes()
        old_sha = json.loads(raw)["validator_contract"]["sha256"].encode()
        if raw.count(old_sha) != 1:
            raise AssertionError("Historical descriptive seal is not unique")
        descriptor.write_bytes(raw.replace(old_sha, hashlib.sha256(validator_path.read_bytes()).hexdigest().encode(), 1))
        ROOT = source_root
        ILLUSTRATION = ROOT / "skills/subculture-illustration-image-generator"
        cls.validator_replay_path = validator_path

    def setUp(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.directory = Path(temp.name)
        self.assets = self.directory / 'assets'; self.assets.mkdir()
        for path in (ILLUSTRATION / 'assets').glob('photo_regression_baseline_v*.json'):
            shutil.copyfile(path, self.assets / path.name)
        for name in ('universal_scene_baseline_v1.json', 'universal_scene_baseline_v2.json'):
            shutil.copyfile(ILLUSTRATION / 'assets' / name, self.assets / name)
        self.path = self.assets / 'photo_regression_baseline_v14.json'
        self.baseline = json.loads(self.path.read_bytes())
        self.output = (self.assets / 'photo_regression_baseline_v13_pack.json').read_bytes()
        self.pack = json.loads(self.output)[0]
        self.proof = json.loads((ROOT / EVIDENCE / 'V14-zero-delta-proof.json').read_bytes())

    def validate(self, version=None):
        def replay(command, **kwargs):
            Path(command[command.index('--output-file') + 1]).write_bytes(self.output)
            return SimpleNamespace(returncode=0, stderr='', stdout='')
        with mock.patch.object(v.subprocess, 'run', side_effect=replay), mock.patch.object(v, '__file__', str(self.validator_replay_path)):
            return v.validate_photo_regression_baseline(self.assets, baseline_version=14 if version is None else version)

    def direct(self, *, repo=None, pack=None, raw=None):
        return v._validate_v14_zero_delta_photo_successor(
            self.assets, ROOT if repo is None else repo, self.baseline,
            self.pack if pack is None else pack, self.output if raw is None else raw)

    def sandbox_sources(self):
        repo = self.directory / 'repo'
        shutil.copytree(ROOT / EVIDENCE, repo / EVIDENCE)
        source = Path(self.baseline['command'][1]).parent.parent / 'assets'
        for name in self.proof['source_inventory_after']:
            target = repo / source / name; target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / source / name, target)
        for name in self.proof['immutable_history']:
            target = repo / name; target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        for name in self.proof['active_semantic_shards']:
            target = repo / name; target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        return repo, source

    def test_historical_v14_replay_rejects_unregistered_v17(self):
        self.assertEqual(self.validate()['schema'], 'photo_regression_baseline/v14')
        (self.assets / 'photo_regression_baseline_v17.json').write_text(json.dumps({'schema':'photo_regression_baseline/v17','status':'current'}))
        self.assertEqual(self.validate()['schema'], 'photo_regression_baseline/v14')
        with self.assertRaisesRegex(v.ValidationFailure, 'unsupported'):
            self.validate(18)

    def test_live_v13_rejects_after_source_even_when_its_pack_is_identical(self):
        with self.assertRaisesRegex(v.ValidationFailure, 'DATA source bytes drift'):
            self.validate(13)

    def test_manifest_data_commit_parent_proof_and_source_sets_are_exact(self):
        original = copy.deepcopy(self.baseline)
        for field in ('data_commit','data_parent_commit','previous_data_commit','evidence_sha256','source_files_missing','source_files_extra','source_files_wrong'):
            self.baseline = copy.deepcopy(original); target = self.baseline['zero_pack_delta_transition']
            if field == 'source_files_missing': target['source_files'].pop(next(iter(target['source_files'])))
            elif field == 'source_files_extra': target['source_files']['unexpected.json']='0'*64
            elif field == 'source_files_wrong': target['source_files'][next(iter(target['source_files']))]='0'*64
            else: target[field]='0'*64
            with self.subTest(field=field), self.assertRaisesRegex(v.ValidationFailure,'DATA provenance or source binding'):
                self.direct()

    def test_predecessor_manifest_archive_and_lineage_tampering_fail(self):
        for name in ('photo_regression_baseline_v13.json','photo_regression_baseline_v13_pack.json'):
            path = self.assets/name; raw=path.read_bytes()
            with self.subTest(name=name):
                path.write_bytes(raw+b'\n')
                with self.assertRaises(v.ValidationFailure): self.validate()
                path.write_bytes(raw)
        for predecessor in (None, {}, {'path':self.path.name,'schema':'photo_regression_baseline/v14','sha256':'0'*64}, {'path':'photo_regression_baseline_v10.json','schema':'photo_regression_baseline/v10','sha256':'0'*64}):
            row=copy.deepcopy(self.baseline); row['historical_baseline']=predecessor
            self.path.write_text(json.dumps(row))
            with self.subTest(predecessor=predecessor), self.assertRaisesRegex(v.ValidationFailure,'successor lineage'):
                self.validate()

    def test_candidate_order_scene_controls_embodiment_negative_privacy_and_adoption_changes_fail(self):
        for kind in ('candidate','order','scene','controls','embodiment','composition','negative','privacy','adoption','four_binding_leaves'):
            pack=copy.deepcopy(self.pack)
            slots=[slot for slot in pack['slots'].values() if len(slot['candidates'])>=2]
            if kind=='candidate': slots[0]['candidates'][0]['concept_terms'][0]+=' changed'
            elif kind=='order': slots[0]['candidates'].reverse()
            elif kind=='scene': pack['authorial_core']['subject']+=' changed'
            elif kind=='controls': pack['creative_controls']['unexpected']=True
            elif kind=='embodiment': pack['embodiment_preflight']['baseline_review']['scope']='applicable'
            elif kind=='composition': pack['authorial_composition']['unexpected']=True
            elif kind=='negative': pack['negative_en']+=', changed'
            elif kind=='privacy': pack['provenance']['private_routing_exposed']=True
            elif kind=='adoption': slots[0]['candidates'][0]['adoption_required']=True
            else:
                pack['provenance']['tags_hash']='0'*64
                pack['core_retrieval']['slot_corpus_sha256']='0'*64
                pack['core_retrieval']['canonical_sha256']='0'*64
            pack['pack_id']=v._canonical_photo_pack_id(pack)
            with self.subTest(kind=kind), self.assertRaisesRegex(v.ValidationFailure,'zero changed pack leaves'):
                self.direct(pack=pack)

    def test_recomputed_manifest_and_pack_checksums_do_not_rebaseline_a_candidate(self):
        self.pack['slots'][next(k for k,s in self.pack['slots'].items() if s['candidates'])]['candidates'][0]['concept_terms'][0]+=' changed'
        self.pack['pack_id']=v._canonical_photo_pack_id(self.pack)
        self.output=(json.dumps([self.pack],ensure_ascii=False,indent=2)+'\n').encode()
        self.baseline.update(sha256=hashlib.sha256(self.output).hexdigest(),pack_id=self.pack['pack_id'])
        self.path.write_text(json.dumps(self.baseline))
        with self.assertRaisesRegex(v.ValidationFailure,'zero-delta historical pack binding'): self.validate()

    def test_raw_format_only_pack_change_is_rejected(self):
        with self.assertRaisesRegex(v.ValidationFailure,'historical pack binding'):
            self.direct(raw=self.output+b'\n')

    def test_four_leaf_transition_is_not_permitted_in_v14(self):
        self.baseline['metadata_only_transition']={}
        with self.assertRaisesRegex(v.ValidationFailure,'four-leaf transition'): self.direct()

    def test_coordinated_proof_and_manifest_rehash_is_rejected(self):
        repo=self.directory/'proof-only'; shutil.copytree(ROOT/EVIDENCE,repo/EVIDENCE)
        proof_path=repo/EVIDENCE/'V14-zero-delta-proof.json'
        for field,value in [('data_commit','0'*40),('data_parent_commit','0'*40),('alias_edits',[]),('source_inventory_after',{}),('previous_manifest_sha256','0'*64)]:
            proof=copy.deepcopy(self.proof); proof[field]=value; proof_path.write_text(json.dumps(proof))
            self.baseline['zero_pack_delta_transition']['evidence_sha256']=hashlib.sha256(proof_path.read_bytes()).hexdigest()
            with self.subTest(field=field), self.assertRaisesRegex(v.ValidationFailure,'immutable proof drift'):
                self.direct(repo=repo)

    def test_same_two_alias_scope_cannot_self_authorize_different_wording(self):
        repo,source=self.sandbox_sources()
        proof=copy.deepcopy(self.proof)
        edit=proof['alias_edits'][0]
        palace=repo/source/'photo_prompt_visual_obligations_palace_fortification.json'
        raw=palace.read_bytes()
        old=json.dumps(edit['new_value'],ensure_ascii=False).encode()
        edit['new_value']+='; 추가된 무관한 목재 장식이 보인다'
        new=json.dumps(edit['new_value'],ensure_ascii=False).encode()
        self.assertEqual(raw.count(old),1); palace.write_bytes(raw.replace(old,new,1))
        proof['source_inventory_after'][palace.name]=hashlib.sha256(palace.read_bytes()).hexdigest()
        proposal_path=repo/EVIDENCE/'two-alias-proposal.json'
        proposal=json.loads(proposal_path.read_bytes()); proposal['edits']=proof['alias_edits']
        proposal_path.write_text(json.dumps(proposal,ensure_ascii=False))
        proof['qualification_artifacts'][proposal_path.name]=hashlib.sha256(proposal_path.read_bytes()).hexdigest()
        proof_path=repo/EVIDENCE/'V14-zero-delta-proof.json'; proof_path.write_text(json.dumps(proof,ensure_ascii=False))
        self.baseline['zero_pack_delta_transition']['evidence_sha256']=hashlib.sha256(proof_path.read_bytes()).hexdigest()
        self.path.write_text(json.dumps(self.baseline))
        # The same two profile IDs/field paths do not grant semantic authority.
        self.assertEqual([e['profile_id'] for e in proof['alias_edits']],[e['profile_id'] for e in self.proof['alias_edits']])
        self.assertEqual([e['field'] for e in proof['alias_edits']],[e['field'] for e in self.proof['alias_edits']])
        with self.assertRaisesRegex(v.ValidationFailure,'immutable proof drift'): self.direct(repo=repo)

    def test_coordinated_real_index_vector_and_all_declared_hash_changes_fail(self):
        repo,source=self.sandbox_sources()
        proof=copy.deepcopy(self.proof)
        index_path=repo/source/'photo_prompt_visual_profile_index.json'
        index=json.loads(index_path.read_bytes()); entry=next(iter(index['entries'].values()))
        entry['vector'][0]+=0.125
        index_path.write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n')
        digest=hashlib.sha256(index_path.read_bytes()).hexdigest()
        proof['source_inventory_after'][index_path.name]=digest
        proof['after_source_files'][str(source/index_path.name)]=digest
        receipt_path=repo/EVIDENCE/'production-index-verification.json'
        receipt=json.loads(receipt_path.read_bytes()); receipt['index_sha256']=digest
        receipt_path.write_text(json.dumps(receipt))
        proof['qualification_artifacts'][receipt_path.name]=hashlib.sha256(receipt_path.read_bytes()).hexdigest()
        proof_path=repo/EVIDENCE/'V14-zero-delta-proof.json'; proof_path.write_text(json.dumps(proof,ensure_ascii=False))
        self.baseline['zero_pack_delta_transition']['source_files']=proof['after_source_files']
        self.baseline['zero_pack_delta_transition']['evidence_sha256']=hashlib.sha256(proof_path.read_bytes()).hexdigest()
        self.path.write_text(json.dumps(self.baseline))
        with self.assertRaisesRegex(v.ValidationFailure,'immutable proof drift'): self.direct(repo=repo)

    def test_exact_source_inventory_rejects_unrelated_alias_index_missing_and_extra_files(self):
        repo,source=self.sandbox_sources()
        for name in ('photo_prompt_visual_obligations_palace_fortification.json','photo_prompt_visual_obligations.json','photo_prompt_visual_profile_index.json','photo_prompt_tags.json'):
            path=repo/source/name; raw=path.read_bytes(); path.write_bytes(raw+b'\n')
            with self.subTest(name=name), self.assertRaisesRegex(v.ValidationFailure,'DATA source bytes drift|DATA inventory drift'):
                self.direct(repo=repo)
            path.write_bytes(raw)
        palace=repo/source/'photo_prompt_visual_obligations_palace_fortification.json'
        raw=palace.read_bytes(); data=json.loads(raw)
        profile=next(row for row in data['profiles'] if row['id']=='pf_rib_vault_chapel')
        profile['activation']['exact_terms'].append('undeclared extra alias')
        palace.write_text(json.dumps(data,ensure_ascii=False))
        with self.assertRaisesRegex(v.ValidationFailure,'DATA inventory drift'): self.direct(repo=repo)
        palace.write_bytes(raw)
        path=repo/source/'photo_prompt_visual_obligations.json'; raw=path.read_bytes(); path.unlink()
        with self.assertRaisesRegex(v.ValidationFailure,'DATA inventory drift'): self.direct(repo=repo)
        path.write_bytes(raw)
        (repo/source/'unregistered-alias.json').write_text('{}')
        with self.assertRaisesRegex(v.ValidationFailure,'DATA inventory drift'): self.direct(repo=repo)

    def test_alias_predecessor_and_historical_proof_archives_are_immutable(self):
        repo,source=self.sandbox_sources()
        path=repo/EVIDENCE/'palace-before.json'; raw=path.read_bytes(); path.write_bytes(raw+b'\n')
        with self.assertRaisesRegex(v.ValidationFailure,'alias predecessor bytes drift'): self.direct(repo=repo)
        path.write_bytes(raw)
        old_proof=repo/'docs/research-evidence/photo-prompt/uniform-costume-integration-20261004/main-merge/V13-FOUR-LEAF-PROOF.json'
        old_proof.write_bytes(old_proof.read_bytes()+b'\n')
        with self.assertRaisesRegex(v.ValidationFailure,'immutable historical artifact drift'): self.direct(repo=repo)

    def test_qualification_receipt_bytes_are_bound_by_fixed_proof(self):
        repo,source=self.sandbox_sources()
        path=repo/EVIDENCE/'production-boundary-comparison.json'
        path.write_bytes(path.read_bytes()+b'\n')
        with self.assertRaisesRegex(v.ValidationFailure,'qualification artifact drift'): self.direct(repo=repo)

    def test_universal_v2_has_only_one_permitted_raw_hash_replacement(self):
        old=(ROOT/EVIDENCE/'universal_scene_baseline_v2.before.json').read_bytes()
        before=json.loads(old); after=json.loads((self.assets/'universal_scene_baseline_v2.json').read_bytes())
        digest=hashlib.sha256(Path(v.__file__).read_bytes()).hexdigest()
        before['validator_contract']['sha256']=digest
        self.assertEqual(before,after)
        self.assertEqual((self.assets/'universal_scene_baseline_v2.json').read_bytes(),old.replace(self.proof['previous_validator_sha256'].encode(),digest.encode(),1))
        after['compiled_obligations']['case_count']+=1
        (self.assets/'universal_scene_baseline_v2.json').write_text(json.dumps(after))
        with self.assertRaisesRegex(v.ValidationFailure,'descriptor changed beyond validator hash'): self.direct()

    def test_v10_v11_v12_v13_still_require_nonzero_exact_four_leaf_deltas(self):
        for version in (10,11,12,13):
            baseline=json.loads((self.assets/f'photo_regression_baseline_v{version}.json').read_bytes())
            old=json.loads((self.assets/f'photo_regression_baseline_v{version-1}_pack.json').read_bytes())[0]
            source_hashes=baseline['metadata_only_transition']['source_files']
            def historical_hash(path):
                rel=str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else None
                return source_hashes[rel] if rel in source_hashes else hashlib.sha256(path.read_bytes()).hexdigest()
            with self.subTest(version=version), mock.patch.object(v,'_sha256',side_effect=historical_hash), self.assertRaisesRegex(v.ValidationFailure,'exactly four binding fields'):
                v._validate_metadata_only_photo_successor(self.assets,ROOT,baseline,old,version=version)


    def test_active_semantic_shards_reject_changed_missing_and_extra_bytes(self):
        repo, source = self.sandbox_sources()
        name = next(iter(self.proof['active_semantic_shards']))
        path = repo / name; raw = path.read_bytes()
        path.write_bytes(raw + b'\n')
        with self.assertRaisesRegex(v.ValidationFailure, 'active semantic shard bytes drift'):
            self.direct(repo=repo)
        path.unlink()
        with self.assertRaisesRegex(v.ValidationFailure, 'active semantic shard bytes drift'):
            self.direct(repo=repo)
        path.write_bytes(raw)
        (path.parent / 'shard-999.json').write_text('{}')
        with self.assertRaisesRegex(v.ValidationFailure, 'active semantic shard bytes drift'):
            self.direct(repo=repo)

    def test_coordinated_real_index_policy_and_proof_rehash_cannot_self_authorize(self):
        repo, source = self.sandbox_sources()
        proof = copy.deepcopy(self.proof)
        path = repo / source / 'photo_prompt_visual_profile_index.json'
        index = json.loads(path.read_bytes())
        index['retrieval_policy']['unauthorized_new_policy'] = True
        path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + '\n')
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        proof['source_inventory_after'][path.name] = digest
        proof['after_source_files'][str(source / path.name)] = digest
        receipt_path = repo / EVIDENCE / 'production-index-verification.json'
        receipt = json.loads(receipt_path.read_bytes()); receipt['index_sha256'] = digest
        receipt_path.write_text(json.dumps(receipt))
        proof['qualification_artifacts'][receipt_path.name] = hashlib.sha256(receipt_path.read_bytes()).hexdigest()
        proof_path = repo / EVIDENCE / 'V14-zero-delta-proof.json'
        proof_path.write_text(json.dumps(proof, ensure_ascii=False))
        self.baseline['zero_pack_delta_transition']['source_files'] = proof['after_source_files']
        self.baseline['zero_pack_delta_transition']['evidence_sha256'] = hashlib.sha256(proof_path.read_bytes()).hexdigest()
        with self.assertRaisesRegex(v.ValidationFailure, 'immutable proof drift'):
            self.direct(repo=repo)

    def test_coordinated_candidate_archive_predecessor_and_proof_rehash_fails(self):
        repo, source = self.sandbox_sources()
        pack = copy.deepcopy(self.pack)
        slot = next(value for value in pack['slots'].values() if value['candidates'])
        slot['candidates'][0]['concept_terms'][0] += ' unauthorized'
        pack['pack_id'] = v._canonical_photo_pack_id(pack)
        raw = (json.dumps([pack], ensure_ascii=False, indent=2) + '\n').encode()
        digest = hashlib.sha256(raw).hexdigest()
        proof = copy.deepcopy(self.proof)
        proof['pack_sha256'] = digest; proof['pack_id'] = pack['pack_id']
        predecessor = json.loads((self.assets / 'photo_regression_baseline_v13.json').read_bytes())
        predecessor.update(sha256=digest, pack_id=pack['pack_id'])
        for directory in (self.assets, repo / 'skills/subculture-illustration-image-generator/assets'):
            (directory / 'photo_regression_baseline_v13_pack.json').write_bytes(raw)
            (directory / 'photo_regression_baseline_v13.json').write_text(json.dumps(predecessor))
        for name in ('photo_regression_baseline_v13.json', 'photo_regression_baseline_v13_pack.json'):
            path = 'skills/subculture-illustration-image-generator/assets/' + name
            proof['immutable_history'][path] = hashlib.sha256((repo / path).read_bytes()).hexdigest()
        proof['previous_manifest_sha256'] = hashlib.sha256((self.assets / 'photo_regression_baseline_v13.json').read_bytes()).hexdigest()
        proof_path = repo / EVIDENCE / 'V14-zero-delta-proof.json'
        proof_path.write_text(json.dumps(proof))
        self.baseline.update(sha256=digest, pack_id=pack['pack_id'])
        self.baseline['historical_baseline']['sha256'] = proof['previous_manifest_sha256']
        self.baseline['zero_pack_delta_transition']['evidence_sha256'] = hashlib.sha256(proof_path.read_bytes()).hexdigest()
        with self.assertRaisesRegex(v.ValidationFailure, 'immutable proof drift'):
            self.direct(repo=repo, pack=pack, raw=raw)


if __name__=='__main__': unittest.main()
