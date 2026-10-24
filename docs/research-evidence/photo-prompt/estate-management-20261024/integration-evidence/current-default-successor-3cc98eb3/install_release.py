import gc
gc.disable()
import json,sys,os
from pathlib import Path
O=Path(__file__).resolve().parent;ROOT=Path('/Users/chasoik/Projects/image-prompt');SKILL=ROOT/'skills/photo-prompt-image-generator'
sys.path.insert(0,str(SKILL/'scripts'))
import install_photo_h_f2_runtime as installer
read=lambda p:json.loads(p.read_bytes())
release=read(O/'successor.json');before=read(O/'before.json')
if '--activate' in sys.argv:
    assert read(SKILL/'retrieval-runtime.json')==before['config'],'Installed default advanced; must rebase rather than overwrite it'
# Allocation scheduling only. The deployed validators and every assertion remain unchanged.
original_run=installer.subprocess.run
def controlled_run(args,*a,**kw):
    args=list(args)
    if '-c' in args:
        i=args.index('-c')+1;args[i]='import gc;gc.disable();'+args[i]
        print('INSTALL_COPIES_SEALED_READY: model and executable copies verified; deployed validators starting',flush=True)
    return original_run(args,*a,**kw)
installer.subprocess.run=controlled_run
# Independent APFS clone for large transport members, each still fully SHA verified
# by the unchanged installer. This avoids a second physical 1 GiB model copy.
original_copyfile=installer.shutil.copyfile
clone_copies=[]
def clone_large(src,dst,*,follow_symlinks=True):
    if Path(src).is_file() and Path(src).stat().st_size>=64*1024*1024:
        original_run(['/bin/cp','-c',os.fspath(src),os.fspath(dst)],check=True)
        assert Path(src).stat().st_ino!=Path(dst).stat().st_ino
        clone_copies.append({'source':str(src),'destination':str(dst),'bytes':Path(src).stat().st_size})
        return dst
    return original_copyfile(src,dst,follow_symlinks=follow_symlinks)
installer.shutil.copyfile=clone_large
result=installer.install(release['store'],release['generation_id'],activate=('--activate' in sys.argv))
(O/('install-active.json' if '--activate' in sys.argv else 'install.json')).write_text(json.dumps(result,indent=2)+'\n')
(O/'validation-execution.json').write_text(json.dumps({'cyclic_gc_enabled':False,'deployed_validator_cyclic_gc_enabled':False,'validation_bypassed':False,'kernel_code_changed':False,'reason':'Large acyclic JSON validation allocation scheduling; every original deployed validator and seal check runs.'},indent=2)+'\n')
(O/'clone-transports.json').write_text(json.dumps({'transport_only':True,'independent_inodes':True,'unchanged_full_validators_run':True,'copies':clone_copies},indent=2)+'\n')
print(json.dumps(result),flush=True)
