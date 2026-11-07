"""Fail-closed checks use synthetic observations, never a live search."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import photo_h_f2_early_failure_reconcile as reconcile


class EarlyFailureEvidence(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
  self.root=Path(self.tmp.name);self.run=self.root/'generated/magical-girl-tests/arm1/run-v2';self.stage=self.run/'.staging/h-f2';self.stage.mkdir(parents=True)
  self.rid='test-run';self.pid=99999999
  self.pre={'run_id':self.rid,'generation_id':reconcile.GEN,'query_set_sha256':'query','validation_receipt':{'generation_id':reconcile.NATIVE}}
  self.journal={'state':'started','generation_id':reconcile.GEN,'query_set_sha256':'query','preflight_sha256':reconcile.digest(self.pre)}
  self.write(self.stage/'preflight.json',self.pre);self.write(self.stage/'transaction.json',self.journal)
  artifact=self.run/'artifact.json';artifact.write_text('{}')
  self.state={'run_id':self.rid,'phase':'slot_intents_authored','operations':[],'artifacts':{'plan':{'path':str(artifact),'sha256':self.file_sha(artifact)}}}
  self.write(self.run/'workflow.json',self.state)
  event={'pid':self.pid,'stage':'embedding','status':'running','completed_queries':0,'total_queries':5}
  final={**event,'stage':'failed','status':'failed'}
  (self.stage/'progress-events.jsonl').write_text(json.dumps(event)+'\n'+json.dumps(final)+'\n');self.write(self.stage/'progress.json',final)
  self.obs={'schema':'codex-command-observation/v1','source_tool':'mcp__codex_app__read_thread','retrieved_with_outputs':True,
   'execution':{'id':'exec','type':'commandExecution','status':'failed','exitCode':2,
    'command':'retrieve --run generated/magical-girl-tests/arm1/run-v2',
    'output':{'truncated':False,'text':'photo_local_embedding.py\nrunner=ModelRunner(runtime_lock())\nValueError: unsafe local model package'}}}
  self.obspath=self.run.parent/'codex-retrieve-observation.json';self.write(self.obspath,self.obs)
  self.profile=('arm1/run-v2',self.file_sha(self.obspath),'exec',5,{self.pid},None)
  self.bindings=(self.file_sha(self.stage/'transaction.json'),self.file_sha(self.stage/'preflight.json'))
  self.patches=[patch.dict(reconcile.PROFILES,{self.rid:self.profile}),patch.dict(reconcile.ORIGINAL_BINDINGS,{self.rid:self.bindings}),patch.object(reconcile,'CODE',{})]
  for p in self.patches:p.start();self.addCleanup(p.stop)

 @staticmethod
 def file_sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
 @staticmethod
 def write(path,value):path.write_text(json.dumps(value))
 def verify(self):return reconcile.verify(self.root,self.run)

 def test_complete_observations_close_without_modifying_transaction(self):
  before=(self.stage/'transaction.json').read_bytes();self.assertEqual(self.verify()['outcome'],'closed_before_index_search');self.assertEqual(before,(self.stage/'transaction.json').read_bytes())

 def test_refuses_missing_or_altered_evidence(self):
  for name in ('transaction.json','preflight.json'):
   p=self.stage/name;before=p.read_bytes();p.write_bytes(before+b' ')
   with self.subTest(name=name),self.assertRaises(ValueError):self.verify()
   p.write_bytes(before)
  self.obs['execution']['output']['truncated']=True;self.write(self.obspath,self.obs)
  with self.assertRaises(ValueError):self.verify()

 def test_refuses_incomplete_output_even_if_its_hash_is_pinned(self):
  self.obs['execution']['output']['truncated']=True;self.write(self.obspath,self.obs)
  altered=list(self.profile);altered[1]=self.file_sha(self.obspath)
  with patch.dict(reconcile.PROFILES,{self.rid:tuple(altered)}),self.assertRaises(ValueError):self.verify()

 def test_refuses_possible_search_or_material(self):
  extra=self.stage/'raw.npz';extra.write_bytes(b'x')
  with self.assertRaises(ValueError):self.verify()
  extra.unlink();ev={'pid':self.pid,'stage':'searching','status':'running','completed_queries':0,'total_queries':5}
  with (self.stage/'progress-events.jsonl').open('a') as f:f.write(json.dumps(ev)+'\n')
  with self.assertRaises(ValueError):self.verify()

 def test_refuses_live_process_and_changed_run_artifact(self):
  with patch.object(reconcile,'no_live_pid',return_value=False),self.assertRaises(ValueError):self.verify()
  (self.run/'artifact.json').write_text('changed')
  with self.assertRaises(ValueError):self.verify()

 def test_refuses_started_image_operation(self):
  state=copy.deepcopy(self.state);state['operations']=[{'status':'invocation_started'}];self.write(self.run/'workflow.json',state)
  with self.assertRaises(ValueError):self.verify()

if __name__=='__main__':unittest.main()
