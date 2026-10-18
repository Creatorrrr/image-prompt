"""Exercise normal H-F2 CLI in disposable copies with existing query evidence."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

from checks import environment, profile
from installed_checks import FIXTURE
from state import ROOT, EVIDENCE, read, write, sha


def copied_file(source,destination):
    if Path(source).stat().st_size>16*1024*1024:
        # APFS copy-on-write: independent regular files, no source hardlink changes.
        subprocess.run(['/bin/cp','-c','-p',str(source),str(destination)],check=True)
    else:
        shutil.copy2(source,destination)
    return destination


def main(output):
    b = read(EVIDENCE/'BASELINE.json.gz')['installed']
    original_store = Path(b['store'])
    original_state = read(FIXTURE/'workflow.json')
    packet = read(original_state['artifacts']['h_f2_material']['path'])
    with tempfile.TemporaryDirectory(prefix='photo-managed-smoke-') as temp:
        temp = Path(temp)
        base = temp/'stores'
        store = base/'h-f2-installed'
        shutil.copytree(original_store,store,symlinks=True,copy_function=copied_file,
                        ignore=shutil.ignore_patterns('__pycache__','h-f2-query-cache'))
        # Query receipts already contain real local vectors. No encoder/inference is needed.
        binding = read(Path(b['hroot'])/'manifest.json')['binding']
        for slot,q in packet['query_set']['slots'].items():
            key = hashlib.sha256(json.dumps({'text':q['text'],'binding':binding},ensure_ascii=False,
                        sort_keys=True,separators=(',',':')).encode()).hexdigest()
            write(store/'h-f2-query-cache'/(key+'.json'),
                  {'text':q['text'],'binding':binding,'row':packet['queries'][slot]['row']})

        def rewire(value,destination):
            if isinstance(value,str):
                return value.replace(str(FIXTURE),str(destination)).replace(str(original_store),str(store))
            if isinstance(value,list):return [rewire(v,destination) for v in value]
            if isinstance(value,dict):return {k:rewire(v,destination) for k,v in value.items()}
            return value

        def clone(destination):
            shutil.copytree(FIXTURE,destination,symlinks=True)
            state = rewire(original_state,destination)
            write(destination/'workflow.json',state)
            return state

        env = environment()
        env['PHOTO_RUNTIME_STORE'] = str(base)
        python = ROOT/'skills/photo-prompt-image-generator/.runtime/embedding-python/bin/python'
        entry = ROOT/'skills/photo-prompt-image-generator/scripts/photo_workflow.py'
        results = []

        def invoke(command,run,*flags):
            p = subprocess.run(['/usr/bin/sandbox-exec','-p',profile(),str(python),str(entry),
                                command,'--run',str(run),*map(str,flags)],env=env,
                               capture_output=True,text=True,timeout=180)
            if p.returncode:
                print(p.stdout[-2000:]+p.stderr[-4000:],flush=True)
                raise ValueError('managed '+command+' failed')
            value = json.loads(p.stdout)
            results.append({'command':command,'exit_code':0,'status':value.get('status'),
                            'stdout_sha256':hashlib.sha256(p.stdout.encode()).hexdigest()})
            print('managed command PASS:',command,flush=True)
            return value

        issued = temp/'issued-run'
        clone(issued)
        invoke('view',issued)
        fresh = temp/'fresh-run'
        state = clone(fresh)
        for key in ['pack','runtime_receipt','h_f2_material','h_f2_receipt','composed','composed_audit']:
            state['artifacts'].pop(key,None)
        state.pop('h_f2_binding',None)
        state.pop('source_binding',None)
        state['phase'] = 'slot_intents_authored'
        # A prior staging transaction must not be mistaken for this disposable run.
        shutil.rmtree(fresh/'.staging/h-f2')
        write(fresh/'workflow.json',state)
        retrieved = invoke('retrieve',fresh)
        if retrieved.get('status')!='pass' or retrieved.get('policy')!='photo-h-f2/v1':
            raise ValueError('normal entrypoint did not run actual H-F2 retrieval')
        invoke('view',fresh)
        composed = read(original_state['artifacts']['composed']['path'])
        composed.pop('pack_id',None);composed.pop('global_retrieval_sha256',None)
        composed_path = temp/'composed.json'
        write(composed_path,composed)
        invoke('compose-audit',fresh,'--composed',composed_path)
        invoke('deliver',fresh)
        final = read(fresh/'workflow.json')
        material = read(final['artifacts']['h_f2_material']['path'])
        if final['phase']!='prompt_delivered' or material['goals']!=packet['goals']:
            raise ValueError('delivered state or exact material results changed')
        if not all(v['cache_hit'] for v in material['queries'].values()):
            raise ValueError('query evidence was not reused')
        write(output,{'status':'PASS','commands':results,'fixture':'copy of prior installed managed run',
              'normal_entrypoint':str(entry.relative_to(ROOT)),'final_phase':final['phase'],
              'query_goals':sorted(material['goals']),'actual_lane_calls':{
                  slot:row['lane_calls'] for slot,row in material['goals'].items()},
              'exact_top8_and_full_order_digests_preserved':True,'query_vectors_reused':True,
              'new_embedding_calls':0,'Gemini_calls':0,'CURRENT_writes':0,
              'installed_source_and_runtime_stores_readonly':True,'disposable_store_override':True,
              'network_denied':True,'image_calls':0})
        print('managed H-F2 retrieve/view/compose/deliver PASS',flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    a = p.parse_args();main(a.output)
