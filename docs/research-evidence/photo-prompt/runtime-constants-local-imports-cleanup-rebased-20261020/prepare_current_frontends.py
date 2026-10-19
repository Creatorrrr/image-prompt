"""Same eight qualified source bodies with the newly installed external selection."""
from pathlib import Path
import shutil,subprocess
import run
from history_state import new
info=run.state.read(run.E/'PRIVATE-PROJECTS.json');t=run.state.read(run.E/'TARGETS.json');projects={}
for label in ('control','combined'):
    project=Path(info['private_parent'])/('current-front-'+label);skill=run.four_patch.copy_code(project);projects[label]=str(project)
    for rel,row in t['original'].items():assert run.state.sha(project/rel)==row['sha256']
    if label=='combined':
        for rel in run.TARGETS:(project/rel).write_bytes(run.transform((project/rel).read_bytes(),Path(rel).stem))
        assert all(run.state.sha(project/rel)==h for rel,h in t['working'].items())
    subprocess.run(['/bin/cp','-c','-R','-p',str(run.SKILL/'assets'),str(skill/'assets')],check=True)
    lock=run.state.read(run.SKILL/'embedding-runtime.lock.json');package=skill/lock['package'];package.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(['/bin/cp','-c','-R','-p',str(run.SKILL/lock['package']),str(package)],check=True)
    (skill/'.runtime/embedding-python').symlink_to(run.SKILL/'.runtime/embedding-python',target_is_directory=True)
    (project/'docs').symlink_to(run.ROOT/'docs',target_is_directory=True)
    assert run.state.read(skill/'retrieval-runtime.json')==run.state.read(run.SKILL/'retrieval-runtime.json')
new(run.E/'CURRENT-FRONTENDS.json',{'status':'PASS','projects':projects,'cleanup_source_bytes_identical_to_qualified_candidates':True,
    'config':run.state.read(run.SKILL/'retrieval-runtime.json'),'model_and_assets_independent':True,'original_source_changes':0})
print('current-release frontends ready',flush=True)
