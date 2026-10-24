from pathlib import Path
import json,subprocess,sys
r=Path('/Users/chasoik/Projects/image-prompt/generated/photo-runs/mecha-20261024-repair2-transport-a');p=json.load(open(r/'recorder-provenance.prepared.json'))
argv=['/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/.runtime/embedding-python/bin/python','/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/mecha-robot-20261024/repair-round-2/run_sealed.py','/Users/chasoik/.cache/image-prompt/photo-shared-runtime/h-f2-installed/generations/578fd501437e5f3e4927330cf8c1a7f319a1aafb05f7f8627d09f10b23ccb7a9/scripts/photo_workflow.py','native-result','--run',str(r),'--ledger',p['ledger'],'--result',str(r/'native-observed-result.json'),'--arm-id',p['arm_id'],'--worktree-id',p['worktree_id'],'--skill-sha256',p['skill_sha256'],'--source-ref',p['source_ref'],'--independent-no-cross-arm-inputs','--manifest',p['manifest'],'--image-call-count','1']
(r/'native-result.argv.json').write_text(json.dumps(argv,indent=2)+'\n')
with (r/'native-result.command-output.json').open('x') as out:
 result=subprocess.run(argv,stdout=out,stderr=subprocess.STDOUT)
print(json.dumps({'exit_code':result.returncode,'output_path':str(r/'native-result.command-output.json')}));sys.exit(result.returncode)
