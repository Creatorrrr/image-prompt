"""Destructive GC boundaries, reference closure, clock and rollback scenarios."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[1] / "tools/runtime_gc.py"
spec = importlib.util.spec_from_file_location("runtime_gc", MODULE)
gc = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = gc
spec.loader.exec_module(gc)


class FakeEnvironment:
    def __init__(self, fixture):
        self.f = fixture
        self.handles = []
        self.processes = b""
        self.busy = False
        self.garbage = set()
        self.smokes = 0
        self.hook = None

    def worktrees(self):
        return [self.f.repo]

    def git_dir(self):
        return self.f.repo / ".git"

    def usage(self):
        return self.handles, self.processes

    def git_busy(self, processes):
        return self.busy

    def git_garbage(self):
        return self.garbage

    def git_identity(self):
        return {"head": "preserved", "packs": "preserved", "staging": "preserved"}

    def smoke(self):
        self.smokes += 1
        if self.hook:
            self.hook(self.smokes)


class Collection(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name).resolve()
        self.repo = root / "repo"
        self.store = root / "cache/photo-shared-runtime"
        self.state = root / "cache/runtime-cleanup"
        self.evidence = root / "evidence"
        self.evidence.mkdir()
        self.skill = self.repo / "skills/photo-prompt-image-generator"
        (self.skill / "scripts").mkdir(parents=True)
        (self.repo / ".git/objects/pack").mkdir(parents=True)
        self.store.mkdir(parents=True)
        self.policy = gc.Policy(self.repo, self.store, self.state, (self.evidence,))
        self.now = 200 * gc.DAY
        self.old_time = self.now - 10 * gc.DAY
        self.env = FakeEnvironment(self)
        self.pairs = [self.pair(i) for i in range(5)]
        # Oldest two are collection candidates; newest two are rollback copies.
        self.current(*self.pairs[-1])
        self.sentinel = self.repo / "generated/reactorprompt-export/preserve.tmp"
        self.sentinel.parent.mkdir(parents=True)
        self.sentinel.write_text("user data")
        self.official = self.repo / ".git/objects/pack/pack-official.pack"
        self.official.write_bytes(b"not a temp")
        self.skill_sentinel = self.skill / "keep.partial"
        self.skill_sentinel.write_bytes(b"skill must not be collected")

    def old(self, path, offset=0):
        when = self.old_time + offset
        os.utime(path, (when, when))

    def generation(self, group, label, native=None, offset=0):
        data = ("sealed-" + label).encode()
        m = {"schema": "photo-h-f2-generation/v1" if group == "h-f2-generations" else "photo-runtime-generation/v3",
             "label": label, "files" if group == "h-f2-generations" else "members": {
                 "data.bin": gc.hashlib.sha256(data).hexdigest()}}
        if native:
            m["native_generation_id"] = native.name
        gid = gc.digest(m)
        p = self.store / "h-f2-installed" / group / gid
        p.mkdir(parents=True)
        (p / "data.bin").write_bytes(data)
        (p / "manifest.json").write_bytes(gc.canonical(m))
        # Tests simulate immutable old file identities without changing the host clock.
        self.old(p, offset)
        for q in p.iterdir():
            self.old(q, offset)
        return p

    def pair(self, i):
        native = self.generation("generations", "native-" + str(i), offset=i)
        hf = self.generation("h-f2-generations", "hf-" + str(i), native, offset=i)
        return hf, native

    def current(self, hf, native):
        (self.skill / "retrieval-runtime.json").write_bytes(gc.canonical({
            "schema": "photo-installed-h-f2/v1", "store_subdirectory": "h-f2-installed",
            "generation_id": hf.name, "native_generation_id": native.name}))

    def workflow(self, pair, phase="pack_bound", *, operations=None):
        p = self.repo / "generated/photo-runs/run/workflow.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        hf, native = pair
        p.write_bytes(gc.canonical({"schema_version": "photo-workflow-run/v2", "phase": phase,
            "operations": operations or [], "artifacts": {},
            "h_f2_binding": {"store": str(hf.parent.parent), "generation_id": hf.name},
            "source_binding": {"runtime_store": str(native.parent.parent), "generation_id": native.name}}))
        return p

    def collector(self, days=0):
        # ctime cannot be set by user code; fake inventories keep all other
        # production reference/path/checksum behavior and model elapsed days.
        class Historical(gc.Collector):
            def nodes(inner):
                nodes = super().nodes()
                for path, row in nodes.items():
                    row["latest"] = (Path(path) / "manifest.json").stat().st_mtime
                return nodes

            def temps(inner):
                temps = super().temps()
                for row in temps.values():
                    row["latest"] = self.old_time
                return temps
        return Historical(self.policy, self.env, self.now + days * gc.DAY)

    def observed(self):
        return self.collector().plan({})["observations"]

    def mature(self):
        return self.collector(2).plan(self.observed())

    def assert_sentinels(self):
        self.assertEqual(self.sentinel.read_text(), "user data")
        self.assertEqual(self.skill_sentinel.read_bytes(), b"skill must not be collected")
        self.assertEqual(self.official.read_bytes(), b"not a temp")
        self.assertTrue(all(p.exists() for p in self.pairs[-1]))

    def test_current_and_recent_rollback_pairs_preserved(self):
        plan = self.mature()
        for pair in self.pairs[-2:]:
            self.assertTrue(all(str(p) in plan["pins"] for p in pair))
        self.assertTrue(all(str(p) in plan["eligible"] for p in self.pairs[0]))

    def retire(self, path, kind):
        self.state.mkdir(parents=True, exist_ok=True)
        (self.state / 'retired-references.json').write_bytes(gc.canonical({
            'schema': 'image-prompt-retired-references/v1', 'entries': [{
                'kind': kind, 'path': str(path), 'sha256': gc.sha(path)}]}))

    def test_retired_workflow_stops_pinning_only_unchanged_bytes(self):
        workflow = self.workflow(self.pairs[0])
        self.retire(workflow, 'workflow')
        self.assertTrue(all(str(p) not in self.collector().plan({})['pins'] for p in self.pairs[0]))
        self.env.processes = ('123 python photo_workflow.py --run ' + str(workflow.parent)).encode()
        with self.assertRaises(gc.Deferred):
            self.collector().plan({})
        self.env.processes = b''
        workflow.write_bytes(workflow.read_bytes() + b' ')
        self.assertTrue(all(str(p) in self.collector().plan({})['pins'] for p in self.pairs[0]))

    def test_retired_script_only_exempts_exact_content_and_running_script_defers(self):
        script = self.repo / 'generated' / 'old' / 'historical.py'
        script.parent.mkdir(parents=True)
        script.write_text('GENERATION = "' + self.pairs[0][0].name + '"\n')
        self.retire(script, 'historical_script')
        self.assertNotIn(str(self.pairs[0][0]), self.collector().plan({})['pins'])
        self.env.processes = ('123 python ' + str(script)).encode()
        with self.assertRaises(gc.Deferred):
            self.collector().plan({})
        self.env.processes = b''
        script.write_text(script.read_text() + '# new work\n')
        self.assertIn(str(self.pairs[0][0]), self.collector().plan({})['pins'])

    def test_retirement_manifest_cannot_target_files_outside_worktrees(self):
        outside = self.evidence / 'workflow.json'
        outside.write_text('{}')
        self.retire(outside, 'workflow')
        with self.assertRaises(gc.Unsafe):
            self.collector().plan({})

    def test_explicit_runtime_wait_exception_requires_prior_unchanged_observation(self):
        collector = self.collector()
        collector.waive_runtime_observation_wait = True
        first = collector.plan({})
        self.assertNotIn(str(self.pairs[0][0]), first['eligible'])
        second = collector.plan(first['observations'])
        self.assertTrue(all(str(p) in second['eligible'] for p in self.pairs[0]))
        self.assertTrue(all(str(p) in second['pins'] for p in self.pairs[-1]))
        self.workflow(self.pairs[0])
        third = collector.plan(first['observations'])
        self.assertTrue(all(str(p) in third['pins'] for p in self.pairs[0]))

    def test_explicit_runtime_wait_exception_does_not_apply_to_git_temps(self):
        temp = self.repo / '.git/objects/pack/tmp_pack_test'
        temp.write_bytes(b'git temporary')
        self.env.garbage.add(temp)
        collector = self.collector()
        collector.waive_runtime_observation_wait = True
        first = collector.plan({})
        self.assertNotIn(str(temp), collector.plan(first['observations'])['eligible'])

    def test_nonterminal_unknown_and_prompt_delivered_preserve_pair(self):
        for phase in ("pack_bound", "prompt_delivered", "future_phase"):
            self.workflow(self.pairs[0], phase)
            plan = self.mature()
            self.assertTrue(all(str(p) in plan["pins"] for p in self.pairs[0]))

    def test_reactor_named_real_workflows_pin_both_generations(self):
        original = self.workflow(self.pairs[0], "invocation_reserved")
        content = original.read_bytes()
        original.unlink()
        for relative in ("generated/photo-runs/reactorprompt-case/run/workflow.json",
                         "docs/research-evidence/reactorprompt-study/run/workflow.json"):
            path = self.repo / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
            plan = self.mature()
            self.assertTrue(all(str(p) in plan["pins"] for p in self.pairs[0]))
            self.assertFalse(any(str(p) in plan["eligible"] for p in self.pairs[0]))
            path.unlink()

    def test_reactor_raw_fixture_workflow_is_not_a_live_reference(self):
        path = self.repo / "generated/trend-scout/raw/reactorprompt-corpus/fixtures/workflow.json"
        path.parent.mkdir(parents=True)
        path.write_text("not a live workflow")
        self.assertIn(str(self.pairs[0][0]), self.mature()["eligible"])

    def test_terminal_review_does_not_release_pending_operation(self):
        self.workflow(self.pairs[0], "review_record_validated", operations=[{"status": "execution_unknown"}])
        self.assertNotIn(str(self.pairs[0][0]), self.mature()["eligible"])
        self.workflow(self.pairs[0], "review_record_validated", operations=[{"status": "complete", "last_event": {"terminal": True}}])
        self.assertIn(str(self.pairs[0][0]), self.mature()["eligible"])

    def test_old_precore_copy_missing_prose_is_not_a_runtime_reference(self):
        p = self.workflow(self.pairs[1])
        v = json.loads(p.read_bytes())
        v["h_f2_binding"] = v["source_binding"] = None
        v["artifacts"] = {"request_raw": {"path": str(p.parent / "missing.json")}}
        p.write_bytes(gc.canonical(v))
        self.assertIn(str(self.pairs[0][0]), self.mature()["eligible"])

    def test_dry_run_never_creates_state_and_clock_needs_multiple_passes(self):
        report = self.collector().run()
        self.assertFalse(report["eligible"])
        self.assertFalse(self.state.exists())
        first = self.observed()
        self.assertFalse(self.collector(0.1).plan(first)["eligible"])
        self.assertTrue(self.collector(2).plan(first)["eligible"])

    def test_reference_resets_unused_clock(self):
        old = self.observed()
        p = self.workflow(self.pairs[0])
        observed = self.collector(2).plan(old)["observations"]
        self.assertNotIn(str(self.pairs[0][0]), observed)
        p.unlink()
        self.assertNotIn(str(self.pairs[0][0]), self.collector(3).plan(observed)["eligible"])

    def test_open_mapping_and_process_id_pin_whole_pair(self):
        self.env.handles = [("123", "Python", "mem", self.pairs[0][0] / "data.bin")]
        self.env.processes = self.pairs[1][0].name.encode()
        plan = self.mature()
        for pair in self.pairs[:2]:
            self.assertTrue(all(str(p) in plan["pins"] for p in pair))

    def test_external_hardlink_and_symlink_preserve_dependency(self):
        alias = self.repo / "preserve-link"
        os.link(self.pairs[0][0] / "data.bin", alias)
        (self.skill / "pinned-release").symlink_to(self.pairs[1][0], target_is_directory=True)
        plan = self.mature()
        for pair in self.pairs[:2]:
            self.assertTrue(all(str(p) in plan["pins"] for p in pair))

    def test_broken_selector_and_malformed_workflow_abort(self):
        p = self.workflow(self.pairs[0])
        p.write_text("{broken")
        with self.assertRaises(ValueError):
            self.mature()
        p.unlink()
        c = self.skill / "retrieval-runtime.json"
        c.write_text("{}")
        with self.assertRaises(gc.Unsafe):
            self.mature()

    def test_active_source_revision_aborts(self):
        p = self.store / "local/test/SOURCE.json"
        p.parent.mkdir(parents=True)
        p.write_text('{"editing":"active","epoch":1}')
        with self.assertRaises(gc.Unsafe):
            self.mature()

    def test_only_confirmed_git_garbage_collected_when_git_idle(self):
        p = self.repo / ".git/objects/pack/tmp_pack_abandoned"
        p.write_bytes(b"abandoned pack")
        self.old(p)
        self.assertNotIn(str(p), self.mature()["eligible"])
        self.env.garbage.add(p)
        self.env.busy = True
        self.assertNotIn(str(p), self.mature()["eligible"])
        self.env.busy = False
        self.assertIn(str(p), self.mature()["eligible"])

    def test_unused_staging_collected_but_referenced_staging_preserved(self):
        p = self.store / ".generation-old"
        p.mkdir()
        (p / "staged.bin").write_bytes(b"staging")
        self.assertIn(str(p), self.mature()["eligible"])
        w = self.workflow(self.pairs[0])
        v = json.loads(w.read_bytes())
        v["source_binding"]["runtime_store"] = str(p)
        w.write_bytes(gc.canonical(v))
        self.assertNotIn(str(p), self.mature()["eligible"])

    def test_fresh_generation_not_eligible_even_with_old_observation(self):
        observed = self.observed()
        class Young(gc.Collector):
            def nodes(inner):
                rows = super().nodes()
                for row in rows.values():
                    row["latest"] = self.now + 1.9 * gc.DAY
                return rows
        c = Young(self.policy, self.env, self.now + 2 * gc.DAY)
        self.assertFalse(c.plan(observed)["eligible"])

    def test_candidate_mutation_restarts_unused_observation(self):
        old = self.observed()
        p = self.pairs[0][0] / "new-unsealed-cache"
        p.write_bytes(b"a producer used this release")
        self.assertNotIn(str(self.pairs[0][0]), self.collector(2).plan(old)["eligible"])

    def test_corrupted_sealed_member_prevents_any_deletion(self):
        p = self.pairs[0][0] / "data.bin"
        p.write_bytes(b"altered source")
        plan = self.mature()
        with gc.collector_lock(self.state), self.assertRaises(gc.Unsafe):
            self.collector(2).collect(plan)
        self.assertTrue(all(q.exists() for pair in self.pairs for q in pair))
        self.assert_sentinels()

    def test_batch_limit_cannot_unlink_other_batch_hardlink(self):
        a = self.store / ".generation-a"
        b = self.store / ".generation-b"
        a.mkdir(); b.mkdir()
        (a / "data").write_bytes(b"same inode")
        os.link(a / "data", b / "data")
        self.policy = gc.Policy(self.repo, self.store, self.state, (self.evidence,), batch=1)
        plan = self.mature()
        self.assertFalse(plan["eligible"])

    def test_producer_process_preserves_releases_and_staging(self):
        p = self.store / ".generation-old"
        p.mkdir()
        self.env.processes = b"123 python install_photo_h_f2_runtime.py"
        plan = self.mature()
        self.assertFalse(plan["eligible"])

    def test_explicit_pin_preserves_hf_and_native(self):
        self.state.mkdir()
        (self.state / "pins.json").write_bytes(gc.canonical([self.pairs[0][0].name]))
        self.assertTrue(all(str(p) in self.mature()["pins"] for p in self.pairs[0]))

    def test_local_and_remote_current_preserve_generic_generation(self):
        p = self.generation("generations", "generic-current")
        target = self.store / "generations" / p.name
        target.parent.mkdir()
        p.rename(target)
        for kind in ("local", "remote"):
            q = self.store / kind / "namespace/CURRENT.json"
            q.parent.mkdir(parents=True)
            q.write_bytes(gc.canonical({"schema": "photo-runtime-current/v3", "generation_id": target.name}))
        self.assertIn(str(target), self.mature()["pins"])

    def test_missing_runtime_artifact_blocks_instead_of_guessing(self):
        p = self.workflow(self.pairs[0])
        v = json.loads(p.read_bytes())
        v["artifacts"] = {"runtime_receipt": {"path": str(p.parent / "missing.json")}}
        p.write_bytes(gc.canonical(v))
        with self.assertRaises(gc.Unsafe):
            self.mature()

    def test_git_temp_crash_rename_is_recoverable(self):
        p = self.repo / ".git/objects/pack/tmp_pack_recover"
        p.write_bytes(b"pack temp")
        q = p.with_name(".runtime-gc-test-" + p.name)
        p.rename(q)
        c = self.collector()
        record = {"schema": gc.SCHEMA, "scope": c.scope(), "phase": "quarantine",
                  "moves": [{"kind": "git-temp", "original": str(p), "hidden": str(q)}]}
        gc.atomic_json(self.state / "transaction.json", record)
        c.recover()
        self.assertEqual(p.read_bytes(), b"pack temp")

    def test_generation_and_git_temp_deleted_without_touching_sentinels(self):
        p = self.repo / ".git/objects/pack/tmp_pack_abandoned"
        p.write_bytes(b"abandoned pack")
        self.env.garbage.add(p)
        plan = self.mature()
        c = self.collector(2)
        with gc.collector_lock(self.state):
            deleted = c.collect(plan)
        self.assertIn(str(p), deleted)
        self.assertFalse(p.exists())
        self.assertTrue(all(not Path(p).exists() for p in deleted))
        self.assertEqual(self.env.smokes, 3)
        self.assert_sentinels()
        self.assertFalse(list(self.store.rglob(".runtime-gc-*")))

    def test_new_reference_after_quarantine_restores_all_candidates(self):
        plan = self.mature()
        def change_reference(number):
            if number == 2:
                self.workflow(self.pairs[0])
        self.env.hook = change_reference
        with gc.collector_lock(self.state), self.assertRaises(gc.Unsafe):
            self.collector(2).collect(plan)
        self.assertTrue(all(p.exists() for pair in self.pairs for p in pair))
        self.assertFalse((self.state / "transaction.json").exists())
        self.assert_sentinels()

    def test_failed_installed_smoke_rolls_back_quarantine(self):
        plan = self.mature()
        def fail(number):
            if number == 2:
                raise gc.Unsafe("runtime failed")
        self.env.hook = fail
        with gc.collector_lock(self.state), self.assertRaises(gc.Unsafe):
            self.collector(2).collect(plan)
        self.assertTrue(all(p.exists() for pair in self.pairs for p in pair))

    def test_new_generation_dependency_rolls_back_quarantine(self):
        plan = self.mature()
        def publish(number):
            if number == 2:
                self.generation("h-f2-generations", "new-published", self.pairs[-1][1])
        self.env.hook = publish
        with gc.collector_lock(self.state), self.assertRaises(gc.Deferred):
            self.collector(2).collect(plan)
        self.assertTrue(all(p.exists() for pair in self.pairs for p in pair))

    def test_rollback_collision_keeps_both_copies(self):
        plan = self.mature()
        p = Path(plan["eligible"][0])
        def collision(number):
            if number == 2:
                p.mkdir()
                (p / "new-producer-data").write_bytes(b"preserve this too")
        self.env.hook = collision
        with gc.collector_lock(self.state), self.assertRaises(gc.Unsafe):
            self.collector(2).collect(plan)
        self.assertEqual((p / "new-producer-data").read_bytes(), b"preserve this too")
        self.assertTrue((self.state / "transaction.json").exists())
        self.assertTrue(list(p.parent.glob(".runtime-gc-*-" + p.name)))

    def test_collector_lock_excludes_another_process(self):
        program = "import fcntl,sys;f=open(sys.argv[1],'rb');fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)"
        with gc.collector_lock(self.state):
            result = subprocess.run([sys.executable, "-c", program, str(self.state / "LOCK")], capture_output=True)
        self.assertNotEqual(result.returncode, 0)

    def test_crash_recovery_restores_quarantine_but_never_partial_deletion(self):
        p = self.pairs[0][0]
        q = p.with_name(".runtime-gc-test-" + p.name)
        p.rename(q)
        c = self.collector()
        record = {"schema": gc.SCHEMA, "scope": c.scope(), "phase": "quarantine",
                  "moves": [{"kind": "runtime", "original": str(p), "hidden": str(q)}]}
        gc.atomic_json(self.state / "transaction.json", record)
        c.recover()
        self.assertTrue(p.exists())
        p.rename(q)
        record["phase"] = "deleting"
        gc.atomic_json(self.state / "transaction.json", record)
        with self.assertRaises(gc.Unsafe):
            c.recover()
        self.assertTrue(q.exists())
        self.assertFalse(p.exists())

    def test_symlink_store_and_unsafe_retention_rejected(self):
        alias = self.store.parent / "alias"
        alias.symlink_to(self.store, target_is_directory=True)
        with self.assertRaises(gc.Unsafe):
            gc.Policy(self.repo, alias, self.state).validate()
        with self.assertRaises(gc.Unsafe):
            gc.Policy(self.repo, self.store, self.state, runtime_age=0).validate()
        with self.assertRaises(gc.Unsafe):
            gc.Policy(self.repo, self.store, self.repo.parent).validate()


if __name__ == "__main__":
    unittest.main()
