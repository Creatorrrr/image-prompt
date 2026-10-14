#!/usr/bin/env python3
"""Prepare/check/export a pinned skill-owned embedding installation."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import venv
from photo_local_embedding import ROOT, MODEL_ID, REVISION, PACKAGES, digest, runtime_lock


def atomic(path,value):
    from photo_embedding_provider import atomic as write
    write(path,value)


def install_python(*,offline=None):
    python=ROOT/'.runtime/embedding-python/bin/python'
    if not python.exists():venv.EnvBuilder(with_pip=True).create(python.parents[1])
    uv=shutil.which('uv')
    if uv:command=[uv,'pip','install','--python',str(python)]
    else:
        subprocess.run([str(python),'-m','ensurepip'],check=True)
        command=[str(python),'-m','pip','install']
    requirement=ROOT/'requirements-local-embeddings.txt'
    if offline:command+=['--no-index','--find-links',str(Path(offline)/'wheelhouse')]
    subprocess.run(command+['-r',str(requirement)],check=True)
    return python


def export_model(device='cpu'):
    """Runs in the isolated runtime after dependency installation."""
    import importlib.metadata
    import os
    os.environ['HF_HUB_DISABLE_TELEMETRY']='1'
    from huggingface_hub import snapshot_download
    import torch
    from sentence_transformers import SentenceTransformer
    source=ROOT/'.runtime/source-embeddinggemma2'/REVISION
    package=ROOT/'.runtime/embeddinggemma2'/REVISION
    snapshot_download(MODEL_ID,revision=REVISION,local_dir=source,ignore_patterns=['README.md','.gitattributes'])
    model=SentenceTransformer(str(source),device='cpu',local_files_only=True,config_kwargs={'vision_config':None,'audio_config':None},model_kwargs={'torch_dtype':torch.float32})
    probes=['task: search result | query: 왼쪽 자연광','title: none | text: natural light from the left']
    model.max_seq_length=8192
    before=model.encode(probes,prompt='',normalize_embeddings=True)
    model.save_pretrained(str(package))
    reloaded=SentenceTransformer(str(package),device='cpu',local_files_only=True,model_kwargs={'torch_dtype':torch.float32})
    after=reloaded.encode(probes,prompt='',normalize_embeddings=True)
    if float(abs(before-after).max())>1e-6:raise ValueError('text-only package differs from reference')
    parameters=sum(p.numel() for p in reloaded.parameters())
    if parameters>300_000_000:raise ValueError('unused modality encoders were not removed')
    files={str(p.relative_to(package)):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(package.rglob('*')) if p.is_file()}
    runtime={'engine':'sentence-transformers','device':device,'dtype':'float32','threads':4,'batch_size':32,
             'packages':{name:importlib.metadata.version(name) for name in PACKAGES}}
    space={'provider':'embeddinggemma2-local','model':MODEL_ID,'revision':REVISION,'dimensions':768,
           'model_package_sha256':digest(files),'recipe':'embeddinggemma2-retrieval/v1','normalization':'l2','inference':runtime}
    lock={'schema':'photo-local-embedding-installation/v1','space':space,'runtime':runtime,'package':str(package.relative_to(ROOT)),
          'python':'.runtime/embedding-python/bin/python','files':files,'parameters':parameters,
          'reference_export_max_abs_error':float(abs(before-after).max()),'license':'Apache-2.0',
          'source':'https://huggingface.co/google/embeddinggemma-2/tree/'+REVISION}
    atomic(ROOT/'embedding-runtime.lock.json',lock)
    print(json.dumps({'installed':True,'parameters':parameters,'package_bytes':sum(r['bytes'] for r in files.values()),'space':space}))


def check():
    from photo_local_embedding import installed_binding,infer
    lock=runtime_lock();rows=infer(['오프라인 실행 확인'], 'query',lock['space'])
    print(json.dumps({'verified':True,'binding':installed_binding(),'dimensions':len(rows[0]['vector']),'execution':rows[0]['execution']}))


def bundle(destination):
    lock=runtime_lock();destination=Path(destination).resolve()
    if destination.exists():raise ValueError('bundle destination already exists')
    destination.mkdir(parents=True)
    for name in ('scripts','precore','references'):
        shutil.copytree(ROOT/name,destination/'skill'/name,ignore=shutil.ignore_patterns('__pycache__'))
    for name in ('SKILL.md','embedding-runtime.lock.json','requirements-local-embeddings.txt'):
        shutil.copy2(ROOT/name,destination/'skill'/name)
    shutil.copytree(ROOT/lock['package'],destination/'skill'/lock['package'])
    # Interpreter-specific wheels; this bundle declares its architecture/version.
    python=ROOT/lock['python'];subprocess.run([str(python),'-m','ensurepip'],check=True)
    frozen=subprocess.check_output([str(python),'-m','pip','freeze'],text=True)
    (destination/'requirements.lock.txt').write_text(frozen)
    subprocess.run([str(python),'-m','pip','download','--only-binary=:all:','--dest',str(destination/'wheelhouse'),'-r',str(destination/'requirements.lock.txt')],check=True)
    atomic(destination/'BUNDLE.json',{'schema':'photo-embedding-offline-bundle/v1','space':lock['space'],
        'python':list(sys.version_info[:2]),'platform':sys.platform,'architecture':__import__('platform').machine(),
        'note':'Includes embedding runtime and model. Candidate index/source are distributed separately.'})
    print(json.dumps({'bundle':str(destination)}))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    commands=p.add_subparsers(dest='command',required=True)
    prep=commands.add_parser('prepare');prep.add_argument('--device',choices=['cpu','mps'],default='cpu')
    commands.add_parser('check')
    exp=commands.add_parser('bundle');exp.add_argument('--output',type=Path,required=True)
    install=commands.add_parser('install-bundle');install.add_argument('--bundle',type=Path,required=True)
    internal=commands.add_parser('_export-model');internal.add_argument('--device',default='cpu')
    a=p.parse_args()
    if a.command=='prepare':
        python=install_python();subprocess.run([str(python),str(Path(__file__).resolve()),'_export-model','--device',a.device],check=True)
    elif a.command=='_export-model':export_model(a.device)
    elif a.command=='check':check()
    elif a.command=='bundle':bundle(a.output)
    elif a.command=='install-bundle':
        info=json.loads((a.bundle/'BUNDLE.json').read_bytes())
        import platform
        if info['architecture']!=platform.machine() or info['platform']!=sys.platform or info['python']!=list(sys.version_info[:2]):
            raise ValueError('offline bundle architecture/Python version mismatch')
        src=a.bundle/'skill';lock=json.loads((src/'embedding-runtime.lock.json').read_bytes())
        if (ROOT/lock['package']).exists():raise ValueError('preserve existing installation; use a new skill directory')
        shutil.copytree(src/lock['package'],ROOT/lock['package'])
        shutil.copy2(src/'embedding-runtime.lock.json',ROOT/'embedding-runtime.lock.json')
        # Locked complete dependencies, without an online package lookup.
        shutil.copy2(a.bundle/'requirements.lock.txt',ROOT/'requirements-local-embeddings.txt')
        install_python(offline=a.bundle);check()


if __name__=='__main__':main()
