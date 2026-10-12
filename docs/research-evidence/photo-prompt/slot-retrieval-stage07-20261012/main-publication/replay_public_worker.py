"""Run unchanged public CLI entrypoints in one matching warm worker."""
import contextlib
import copy
import json
from pathlib import Path
import shutil
import sys

OUT=Path(__file__).resolve().parent
ROOT=Path('/Users/chasoik/.codex/worktrees/slot-retrieval-stage07-integration/image-prompt')
sys.path.insert(0,str(ROOT/'skills/photo-prompt-image-generator/scripts'))
import generate_photo_prompt as public
import compose_pack_view as view
import audit_composed_prompt as audit
from photo_runtime_sources import RuntimeSnapshotProvider

store=OUT/'repaired-runtime-store'
snapshot=RuntimeSnapshotProvider(ROOT/'skills/photo-prompt-image-generator',store).acquire()
shard=int(sys.argv[1]) if len(sys.argv)>1 else 0
results=[]
ordinal=0
for old_lane,lane in [('merged-public-natural','repaired-public-natural'),('merged-public-native','repaired-public-native')]:
    for source in sorted((OUT/old_lane).glob('*/generate-command.json')):
        take=ordinal%4==shard
        ordinal+=1
        if not take:continue
        name=source.parent.name;folder=OUT/lane/name;folder.mkdir(parents=True,exist_ok=True)
        argv=json.loads(source.read_text())[2:]
        for index,value in enumerate(argv):
            if value.startswith(str(source.parent)):
                relative=Path(value).relative_to(source.parent)
                target=folder/relative
                if (source.parent/relative).is_file() and relative.name!='candidate-pack.json':
                    shutil.copy2(source.parent/relative,target)
                argv[index]=str(target)
            if index and argv[index-1]=='--runtime-store':argv[index]=str(store)
        (folder/'generate-command.json').write_text(json.dumps(argv,indent=2)+'\n')
        with (folder/'generate.log').open('w') as log,contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):
            code=public.main(argv)
        assert code==0,(name,code)
        pack_path=folder/'candidate-pack.json';pack=json.loads(pack_path.read_text())[0]
        previous_argv=sys.argv
        try:
            sys.argv=['compose_pack_view.py','--pack',str(pack_path),'--output',str(folder/'composer-view.json')]
            with (folder/'view.log').open('w') as log,contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):
                view_code=view.main()
        finally:sys.argv=previous_argv
        assert view_code==0,name
        issues=audit.audit_core_retrieval(pack,snapshot.data);assert not issues,(name,issues)
        damaged=copy.deepcopy(pack);slot=next(iter(damaged['slots']));damaged['slots'][slot]['candidates'].pop()
        assert audit.audit_core_retrieval(damaged,snapshot.data),name
        result=dict(case=name,lane=lane,cli_exit=code,view_exit=view_code,recomputation_errors=issues,
                    omission_detected=True,generation_id=snapshot.generation_id)
        results.append(result)
        (OUT/('REPAIRED-PUBLIC-ENTRYPOINTS-'+str(shard)+'.json')).write_text(json.dumps(dict(
            cases=results,execution='Unmodified production public.main(argv) and view.main() argument parsers, output files and runtime receipts; one matching warm worker; no mocks.',
            generation_id=snapshot.generation_id,source_fingerprint=snapshot.manifest['source_fingerprint']),indent=2)+'\n')
        print(json.dumps(dict(case=name,cli=code,view=view_code)),flush=True)
assert len(results)==10
