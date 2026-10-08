"""Coordinator wire boundaries. Live arm audits separately verify pixel runs."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from tests.test_photo_workflow_precore import freeze_fixture, files
from tests.test_photo_workflow_state import workflow
import photo_native_bridge


class TransportBindingTests(unittest.TestCase):
    def prepare_selected(self, directory, *, stored_hash='a'*64, extra=None):
        run,_=freeze_fixture(directory,mode='image')
        pack={'pack_id':'selected-case','core_retrieval':{'canonical_sha256':'b'*64},
              'authorial_core':{'intent_lock':{'canonical_sha256':'c'*64}},
              'embodiment_preflight':{'canonical_sha256':'d'*64}}
        composed={'prompt_en':'A connected fire remains on its own fuel surface.',
                  'negative_en':None,'chosen_visual_concept_ids':['visual-concept:owned-fire']}
        with files.locked_state(run) as state:
            files.commit_stage(run,state,'composition_audited',{
                'pack':files.encode(pack),'composed':files.encode(composed),
                'composed_audit':files.encode({'status':'pass','effective_visual_contract_sha256':stored_hash})})
        parameters=directory/'transport.json';parameters.write_text(json.dumps({'references':[],**(extra or {})}))
        # The worker double represents an independent expected contract; it
        # deliberately rejects stale/missing hashes rather than always passing.
        def independent_worker(state, *, runtime):
            request=files.value(state,'render_request')
            failures=[] if request.get('effective_visual_contract_sha256')=='a'*64 else [{'check':'effective_visual_contract_sha256'}]
            return {'composed_audit':{'status':'pass','failures':[]},
                    'runtime_audit':{'status':'fail' if failures else 'pass','failures':failures}}
        with patch('photo_workflow_worker.audit_bound',side_effect=independent_worker):
            result=workflow.prepare_render(argparse.Namespace(run=run,parameters=parameters,lane='native',model=None,size=None))
        return run,result

    def test_selected_contract_is_bound_from_the_audited_record(self):
        with tempfile.TemporaryDirectory() as temp:
            run,result=self.prepare_selected(Path(temp))
            self.assertEqual(result['status'],'pass')
            state=files.load_state(run)
            self.assertEqual(files.value(state,'render_request')['effective_visual_contract_sha256'],'a'*64)
            self.assertEqual(state['operations'],[])

    def test_stale_or_missing_contract_stays_unadmitted(self):
        for value in [None,'0'*64]:
            with self.subTest(value=value),tempfile.TemporaryDirectory() as temp:
                run,result=self.prepare_selected(Path(temp),stored_hash=value)
                self.assertEqual(result['runtime_audit']['status'],'fail')
                self.assertNotIn('render_request',files.load_state(run)['artifacts'])
                self.assertEqual(files.load_state(run)['operations'],[])

    def test_caller_cannot_override_the_auditor_contract(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(ValueError,'explicit_transport_parameters_required'):
                self.prepare_selected(Path(temp),extra={'effective_visual_contract_sha256':'a'*64})

    @unittest.skipUnless(shutil.which('node'),'Node is needed to execute the actual tool bridge')
    def test_native_bridge_waits_for_exit_and_preserves_json_chunks(self):
        script=photo_native_bridge.BRIDGE_JAVASCRIPT+r'''
const assert = require('node:assert/strict');
(async () => {
  let calls=0, polls=0, commands=0;
  const payload={prompt:'exact audited bytes',transparent_background:false};
  const text=JSON.stringify({operation_id:'observed-operation',payload});
  const tools={
    exec_command:async()=>++commands===1?{session_id:17,output:text.slice(0,19)}:{exit_code:0,output:'{"status":"pass"}'},
    write_stdin:async args=>{assert.equal(args.session_id,17);polls++;return {exit_code:0,output:text.slice(19)};},
    image_gen__imagegen:async args=>{assert.deepEqual(args,payload);calls++;return {actual_path:'/observed/native.png'};}
  };
  await runPhotoNative({tools,run:'/run',workflowScript:'/scripts/photo_workflow.py',python:'/python',ledger:'/ledger',
    observe:async result=>({outcome:'returned',image_path:result.actual_path})});
  assert.equal(polls,1);assert.equal(calls,1);assert.equal(commands,2);
  let blockedCalls=0;
  await assert.rejects(runPhotoNative({tools:{exec_command:async()=>({session_id:19,output:''}),
      write_stdin:async()=>({exit_code:2,output:'failed'}),image_gen__imagegen:async()=>{blockedCalls++;}},
      run:'/run',workflowScript:'/scripts/photo_workflow.py',python:'/python',ledger:'/ledger',observe:async()=>({})}),/native_bridge_command_failed/);
  assert.equal(blockedCalls,0);
})().catch(error=>{console.error(error);process.exitCode=1;});
'''
        result=subprocess.run(['node','-e',script],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)


if __name__=='__main__':unittest.main()
