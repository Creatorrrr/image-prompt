"""Run real current installed CLI against only a disposable pinned closure."""
from pathlib import Path
import sys
import run
from history_state import new
import managed_smoke

label=sys.argv[1];b=run.baseline();cfg=b['installed']['config'];store=Path(b['installed']['store']).resolve()
projects=run.state.read(run.E/'PRIVATE-PROJECTS.json')['projects']
original_root=managed_smoke.ROOT;original_profile=managed_smoke.profile;original_copy=managed_smoke.shutil.copytree
original_read=managed_smoke.read;original_fixture=managed_smoke.FIXTURE
managed_smoke.FIXTURE=Path(b['fixture']);clones=0;excluded={}
def selected_read(path):
    if Path(path).resolve()==(run.state.EVIDENCE/'BASELINE.json.gz').resolve():return {'installed':b['installed']}
    return original_read(path)
def scoped_copy(source,destination,*args,**kwargs):
    global clones
    if Path(source).resolve()==store:
        clones+=1;previous=kwargs.get('ignore')
        def ignore(directory,names):
            omit=set(previous(directory,names) if previous else [])
            for branch,gid in {'generations':cfg['native_generation_id'],'h-f2-generations':cfg['generation_id']}.items():
                if Path(directory).resolve()==store/branch:
                    extra=set(names)-{gid};omit.update(extra);excluded[branch]=sorted(extra)
            return omit
        kwargs['ignore']=ignore
    return original_copy(source,destination,*args,**kwargs)
managed_smoke.read=selected_read;managed_smoke.shutil.copytree=scoped_copy
managed_smoke.ROOT=run.ROOT if label=='applied' else Path(projects[label])
managed_smoke.profile=lambda:(run.checks.profile() if label=='applied' else run.four_patch.policy())+'(deny file-read* (regex "/site-packages/torch(/|$)"))'
output=run.E/('MANAGED-'+label+'.json')
try:managed_smoke.main(output)
finally:
    managed_smoke.ROOT=original_root;managed_smoke.profile=original_profile;managed_smoke.shutil.copytree=original_copy;managed_smoke.read=original_read;managed_smoke.FIXTURE=original_fixture
result=run.state.read(output);assert result['status']=='PASS' and len(result['commands'])==5 and clones==1
new(run.E/('MANAGED-'+label+'-CLOSURE.json'),{'status':'PASS','config':cfg,'pinned_generations_only':True,'excluded_inactive_generations':excluded,
    'store_clones':clones,'result_sha256':run.state.sha(output),'operating_manifest_or_generation_modified':False,'Gemini_calls':0,'CURRENT_writes':0})
