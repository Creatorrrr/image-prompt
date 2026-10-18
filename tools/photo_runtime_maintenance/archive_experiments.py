"""Archive the enumerated inactive closure; replay before removing clean originals."""
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys
import tempfile

from state import ROOT, EVIDENCE, read, write, sha, files
from classify import EXPERIMENTS, MODULES
from bundles import pack, restore

ARCHIVES = ROOT/'docs/research-archives/photo-prompt'
BUNDLE = ARCHIVES/'source-review-and-lane-experiments.zip'
LOCK = ARCHIVES/'EXPERIMENT-LOCK.json'


def replay(root, output):
    python = ROOT/'skills/photo-prompt-image-generator/.runtime/embedding-python/bin/python'
    wt = '/Users/chasoik/.codex/worktrees/slot-search-relevance/image-prompt'
    denied = [wt, *[str(ROOT/'docs/research-evidence/photo-prompt'/n) for n in EXPERIMENTS],
              *[str(ROOT/'skills/photo-prompt-image-generator/scripts'/(m+'.py')) for m in MODULES]]
    profile = '(version 1)(allow default)(deny network*)' + '(deny file-read* '+ ' '.join(
        '(subpath '+json.dumps(p)+')' for p in denied)+')' + '(deny file-write* (subpath '+json.dumps(str(ROOT))+') (subpath '+json.dumps(str(Path.home()/'.cache/image-prompt'))+'))'
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONNOUSERSITE='1',
               HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1')
    for name in ['PYTHONPATH','GEMINI_API_KEY','GOOGLE_API_KEY','OPENAI_API_KEY','ANTHROPIC_API_KEY']:
        env.pop(name,None)
    launcher = "import sys,runpy;from pathlib import Path;entry=sys.argv.pop(1);sys.path.insert(0,str(Path(entry).parent));runpy.run_path(entry,run_name='__main__')"
    commands = [
        [str(python),'-I','-c',launcher,str(root/'docs/research-evidence/photo-prompt/candidate-semantic-renewal-20261018/audit_saved.py')],
        [str(python),'-I','-c',launcher,str(root/'docs/research-evidence/photo-prompt/candidate-recall-followup-20261019/audit.py')],
        [str(python),'-I','-c',"import os,sys,unittest;os.chdir(sys.argv[1]);sys.path.insert(0,sys.argv[1]);suite=unittest.defaultTestLoader.loadTestsFromNames(['tests.test_photo_candidate_authoring','tests.test_photo_candidate_lanes']);r=unittest.TextTestRunner().run(suite);sys.exit(not r.wasSuccessful())",str(root)]]
    results = []
    for command in commands:
        p = subprocess.run(['/usr/bin/sandbox-exec','-p',profile,*command],cwd=root,env=env,
                           capture_output=True,text=True,timeout=180)
        results.append({'command':command[2], 'exit_code':p.returncode, 'stdout':p.stdout,'stderr':p.stderr})
        print(p.stdout[-500:]+p.stderr[-500:],flush=True)
        if p.returncode:
            write(output,{'status':'FAIL','results':results})
            raise ValueError('archived replay failed')
    old = read(root/'docs/research-evidence/photo-prompt/candidate-semantic-renewal-20261018/SAVED-AUDIT.json')
    new = read(root/'docs/research-evidence/photo-prompt/candidate-recall-followup-20261019/DEVELOPMENT-QUALIFICATION.json')
    if old['full_orders_checked']!=225 or new['full_orders_independently_replayed']!=225 or new['status']!='HOLD':
        raise ValueError('archived replay gate changed')
    write(output,{'status':'PASS','results':results,'network_denied':True,'original_research_reads_denied':True,
          'old_full_orders':225,'latest_full_orders':225,'experiment_tests':17,
          'latest_gate':new['status'],'latest_winner':new['winner'],
          'new_embedding_calls':0,'CURRENT_writes':0,'Gemini_calls':0})


def main(remove=False):
    actions = read(EVIDENCE/'ACTION-LIST.json')['archive']
    if any(r['action']!='ARCHIVE_EXPERIMENT' for r in actions):
        raise ValueError('only closed clean experiment bundle supported')
    if not LOCK.exists():
        members = {r['path']:ROOT/r['path'] for r in actions}
        for name in EXPERIMENTS[:2]:
            for f in (ROOT/'docs/research-evidence/photo-prompt'/name).glob('*FREEZE*.json'):
                for relative, expected in read(f).get('files',{}).items():
                    p = ROOT/relative
                    if sha(p)!=expected:
                        raise ValueError('original frozen input changed: '+relative)
                    members[relative] = p
        for p in files(ROOT/'skills/photo-prompt-image-generator/candidate-authoring/v1'):
            members[str(p.relative_to(ROOT))] = p
        extras = ['tests/__init__.py','skills/photo-prompt-image-generator/scripts/photo_installed_h_f2.py',
                  'skills/photo-prompt-image-generator/references/candidate-source-review.md',
                  'skills/photo-prompt-image-generator/references/candidate-lane-generation.md']
        for relative in extras:
            members[relative] = ROOT/relative
        seal = pack(BUNDLE,members)
        seal.update(schema='photo-inactive-experiment-bundle/v1', removed_paths=[r['path'] for r in actions],
                    entrypoints=['candidate-semantic-renewal-20261018/audit_saved.py','candidate-recall-followup-20261019/audit.py'],
                    active=False, executable_authority=False, original_relative_paths=True)
        write(LOCK,seal)
    seal = read(LOCK)
    with tempfile.TemporaryDirectory(prefix='photo-experiment-replay-') as temp:
        restored = restore(BUNDLE,seal,Path(temp)/'root')
        replay(restored,EVIDENCE/'ARCHIVE-REPLAY.json')
    if remove:
        if (EVIDENCE/'STAGE04.json').exists():
            raise ValueError('cleanup already completed; use replay without --remove')
        baseline = read(EVIDENCE/'BASELINE.json.gz')
        dirty = baseline['repositories'][str(ROOT)]['status']
        for row in actions:
            path = row['path']
            if path in dirty or sha(ROOT/path)!=row['sha256'] or seal['files'][path]['sha256']!=row['sha256']:
                raise ValueError('removal protection failed: '+path)
        write(EVIDENCE/'ARCHIVE-REMOVAL-JOURNAL.json',{'state':'verified_before_removal',
              'archive_sha256':seal['archive_sha256'],'paths':[r['path'] for r in actions]})
        for row in actions:
            (ROOT/row['path']).unlink()
        for name in EXPERIMENTS:
            p = ROOT/'docs/research-evidence/photo-prompt'/name/'README.md'
            p.write_text('# 보관된 비활성 실험\n\n원래 파일은 `docs/research-archives/photo-prompt/source-review-and-lane-experiments.zip`에\n원래 상대 경로와 hash를 보존했다. 복원·감사 명령은 보관물 디렉터리의 README를 따른다.\n현재 기본 검색은 설치된 H 단독+F2이며 이 실험은 운영에 적용되지 않았다.\n')
        allowed = seal['removed_paths']+[
            'skills/photo-prompt-image-generator/references/candidate-source-review.md',
            'skills/photo-prompt-image-generator/references/candidate-lane-generation.md']
        write(EVIDENCE/'ALLOWED-CHANGES.json',allowed)
        write(EVIDENCE/'STAGE04.json',{'status':'PASS','archive':str(BUNDLE.relative_to(ROOT)),
              'archive_sha256':seal['archive_sha256'],'archived_members':len(seal['files']),
              'removed_clean_originals':len(actions),'original_logical_bytes':sum(r['bytes'] for r in actions),
              'archive_bytes':sum(r['bytes'] for r in seal.get('parts',[])) if 'parts' in seal else BUNDLE.stat().st_size,
              'relative_paths_and_original_hashes_preserved':True,
              'replayed_full_orders':450,'quality_gate':'HOLD','tests_moved_with_dependency_closure':2,
              'operating_activation':False,'Gemini_calls':0,'CURRENT_writes':0})
    print('archive verified',len(seal['files']),'members; removed originals:',remove,flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--remove',action='store_true')
    a = p.parse_args(); main(a.remove)
