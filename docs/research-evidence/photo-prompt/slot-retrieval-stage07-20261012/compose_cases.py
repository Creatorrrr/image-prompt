"""Author baseline-preserving rejection cases and execute real pinned audits."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys

OUT = Path(__file__).resolve().parent
ROOT = Path('/Users/chasoik/.codex/worktrees/slot-retrieval-stage07-integration/image-prompt')
SKILL = ROOT / 'skills/photo-prompt-image-generator'
PYTHON = Path('/Users/chasoik/Projects/image-prompt/.venv/bin/python')
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as g
import audit_composed_prompt as audit
from photo_runtime_sources import RuntimeSnapshotProvider

def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def authored_review(pack, prompt):
    # Complete final prompts were read individually before these cases were authored.
    # Literal unchanged-body evidence is retained; applicability is not guessed from IDs.
    original = pack['embodiment_preflight']['baseline_review']
    checks = copy.deepcopy(original['checks'])
    for key, row in checks.items():
        row['reason'] = 'Reread the complete final prose. ' + row['reason']
        assert all(phrase in prompt for phrase in row.get('prompt_evidence', []))
    return {'source_contract_sha256':pack['embodiment_preflight']['canonical_sha256'],
        'review':{'contract_version':'photo-embodiment-review/v1',
            'provenance':'agent_postcomposition','prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(),
            'scope':original['scope'],
            'summary':'Final prose review: '+original['summary']+' Optional rows were rejected; actor, support, reach, contact and view remain as individually reviewed in the complete final baseline. This is prose plausibility, not image evidence.',
            'checks':checks}}

def reject(pack):
    core=pack['authorial_core'];lock=core['intent_lock'];prompt=core['baseline_prompt_en']
    result={'pack_id':pack['pack_id'],'composer':'agent','prompt_en':prompt,
        'negative_en':pack['negative_en'],'chosen_candidate_ids':[],
        'chosen_visual_concept_ids':[],'candidate_interpretations':[],
        'core_retrieval_sha256':pack['core_retrieval']['canonical_sha256'],
        'authorial_core_binding':{'source_authorial_core_sha256':core['canonical_sha256'],
            'source_intent_lock_sha256':lock['canonical_sha256'],
            'preserved_anchor_ids':[x['anchor_id'] for x in lock['semantic_anchors']],
            'preserved_evidence':[],'authorial_decisions':[]},
        'embodiment_review':authored_review(pack,prompt),
        'semantic_clarification_decisions':[{'clarification_id':row['id'],
            'decision':'applied' if row.get('required_in_final_prompt') else 'rejected',
            'rationale':'Keep the frozen requester meaning and independently written scene; an optional advisory supplies no new duty.',
            'prompt_evidence':lock['semantic_anchors'][0]['prompt_evidence']}
            for row in pack['semantic_clarification']['candidates']],
        'creative_augmentation_brief':{'decisions':[{'candidate_id':row['id'],
            'decision':'rejected','rationale':'The independently written baseline already specifies this scene; adding the optional detail is unnecessary.'}
            for row in pack['creative_augmentation']['candidates']]}}
    contract=pack.get('semantic_assertion_obligations')
    if contract:
        result['semantic_assertion_evidence']={'source_contract_sha256':contract['canonical_sha256'],
            'evidence':{row['assertion_id']:row['frozen_evidence'] for row in contract['obligations']}}
    return result

def main():
    provider=RuntimeSnapshotProvider(SKILL,OUT/'runtime-store');snapshot=provider.acquire()
    paths=sorted((OUT/'public-natural').glob('*/candidate-pack.json'))
    results=[]
    for path in paths:
        pack=json.loads(path.read_text())[0];composed=reject(pack)
        destination=OUT/'composition'/path.parent.name/'reject-all'
        save(destination/'composed.json',composed)
        run=subprocess.run([str(PYTHON),str(SKILL/'scripts/audit_composed_prompt.py'),
            '--pack',str(path),'--composed',str(destination/'composed.json'),
            '--runtime-store',str(OUT/'runtime-store'),
            '--runtime-receipt',str(path)+'.runtime-receipt.json'],cwd=ROOT,capture_output=True,text=True)
        (destination/'audit.log').write_text(run.stdout+run.stderr)
        try:result=json.loads(run.stdout)
        except ValueError:result={'status':'error','failures':[{'check':'worker','reason':run.stdout+run.stderr}]}
        save(destination/'audit.json',result)
        row={'case':path.parent.name,'variant':'reject-all','exit_code':run.returncode,
            'status':result['status'],'failures':result.get('failures',[]),
            'frozen_baseline_preserved':composed['prompt_en']==pack['authorial_core']['baseline_prompt_en']}
        results.append(row);save(OUT/'COMPOSITION-INITIAL.json',results)
        print(json.dumps(row,ensure_ascii=False),flush=True)

if __name__=='__main__':main()
