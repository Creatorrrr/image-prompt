"""Skill-owned offline inference. Lazy, bounded pipe worker; no daemon or HTTP."""
from __future__ import annotations

import atexit
import copy
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import threading
import time

ROOT = Path(__file__).resolve().parents[1]
MODEL_ID = 'google/embeddinggemma-2'
REVISION = '914f7f89142e33e77833254d9c9b90c3cef7303b'
PREFIXES = {'query': 'task: search result | query: ', 'document': 'title: none | text: '}
PACKAGES = ('torch', 'transformers', 'sentence-transformers', 'tokenizers', 'safetensors', 'numpy', 'pillow', 'torchvision')
_VERIFIED = {}
_INSTALLATIONS = {}
_WORKER = None
_DIRECT_RUNNER = None
_LOCK = threading.RLock()


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',', ':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()


def runtime_lock(root=ROOT, *, verify=True):
    root=Path(root).resolve()
    path=root/'embedding-runtime.lock.json'
    try:
        st=path.stat();stamp=(st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns,st.st_ctime_ns)
        cached=_INSTALLATIONS.get(str(root))
        if cached and cached[0]==stamp:
            lock=copy.deepcopy(cached[1]);package=cached[2];paths=cached[3]
        else:
            lock=json.loads(path.read_bytes());package=root/lock['package']
            if package.is_symlink() or root not in package.resolve().parents:raise ValueError('unsafe local model package')
            paths={name:package/name for name in lock['files']}
            for name,p in paths.items():
                if p.is_symlink() or package.resolve() not in p.resolve().parents:raise ValueError('unsafe local model file: '+name)
            _INSTALLATIONS[str(root)]=(stamp,copy.deepcopy(lock),package,paths)
    except FileNotFoundError: raise RuntimeError('local_embedding_not_installed: run setup_local_embeddings.py') from None
    if lock.get('schema')!='photo-local-embedding-installation/v1' or lock['space'].get('model')!=MODEL_ID:
        raise ValueError('invalid local embedding installation')
    if package.is_symlink() or root not in package.resolve().parents:
        raise ValueError('unsafe local model package')
    if lock['space']['model_package_sha256']!=digest(lock['files']):
        raise ValueError('model package manifest mismatch')
    if verify:
        for name,row in lock['files'].items():
            path=paths[name]
            # Parent-directory links are rejected even when bytes are cached.
            if path.is_symlink() or path.parent.is_symlink() or not path.is_file():
                raise RuntimeError('local_model_missing_or_unsafe: '+name)
            stat=path.stat();identity=(stat.st_dev,stat.st_ino,stat.st_size,stat.st_mtime_ns,stat.st_ctime_ns)
            if _VERIFIED.get(str(path))!=identity:
                sha=hashlib.sha256(path.read_bytes()).hexdigest()
                if sha!=row['sha256'] or stat.st_size!=row['bytes']:
                    raise ValueError('local model checksum mismatch: '+name)
                after=path.stat()
                if (after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns)!=identity:raise ValueError('model changed during verification')
                _VERIFIED[str(path)]=identity
    return lock


def space(root=ROOT):
    return dict(runtime_lock(root)['space'])


def numpy_runtime():
    """Use the pinned numeric library only after explicit post-core retrieval."""
    lock=runtime_lock()
    import site
    version=f'python{sys.version_info.major}.{sys.version_info.minor}'
    directory=ROOT/'.runtime/embedding-python/lib'/version/'site-packages'
    if not directory.is_dir():raise RuntimeError('local numerical runtime Python ABI mismatch')
    if str(directory) not in sys.path:site.addsitedir(str(directory))
    import numpy
    if numpy.__version__!=lock['runtime']['packages']['numpy']:raise ValueError('local numeric dependency version mismatch')
    return numpy


def installed_binding(root=ROOT):
    lock=runtime_lock(root)
    command='import importlib.metadata,json;print(json.dumps({n:importlib.metadata.version(n) for n in '+repr(PACKAGES)+'}))'
    actual=json.loads(subprocess.check_output([str(Path(root)/lock['python']),'-c',command],text=True))
    if actual!=lock['runtime']['packages']:raise ValueError('local inference dependency versions changed')
    return {'space':lock['space'],'runtime':lock['runtime'],'lock_sha256':digest(lock)}


def model_inputs(texts, kind):
    if kind not in PREFIXES:raise ValueError('embedding kind must be query or document')
    if any(not isinstance(text,str) or not text.strip() for text in texts):raise ValueError('nonempty embedding text required')
    return [PREFIXES[kind]+text for text in texts]


def close_worker():
    global _WORKER
    with _LOCK:
        if _WORKER is not None:
            process=_WORKER[1]
            if process.stdin:process.stdin.close()
            try:process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.terminate()
                try:process.wait(timeout=5)
                except subprocess.TimeoutExpired:process.kill();process.wait()
            _WORKER=None


atexit.register(close_worker)


def infer(texts,kind,expected_space):
    """One child owned by this CLI; inherited lifetime, no server or network."""
    global _WORKER, _DIRECT_RUNNER
    if not texts:return []
    lock=runtime_lock()
    if expected_space!=lock['space']:raise ValueError('local model space does not match installed package')
    binding=digest(lock)
    with _LOCK:
        if Path(sys.prefix).resolve()==(ROOT/lock['python']).parents[1].resolve():
            if _DIRECT_RUNNER is None or _DIRECT_RUNNER[0]!=binding:
                _DIRECT_RUNNER=(binding,ModelRunner(lock))
            return _DIRECT_RUNNER[1].run({'texts':texts,'kind':kind,'space':expected_space})
        if _WORKER is not None and (_WORKER[0]!=binding or _WORKER[1].poll() is not None):close_worker()
        if _WORKER is None:
            python=ROOT/lock['python']
            if not python.is_file():raise RuntimeError('local_embedding_python_missing: reinstall the skill runtime')
            env=dict(os.environ,HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',HF_HUB_DISABLE_TELEMETRY='1',TOKENIZERS_PARALLELISM='false')
            for name in ('GEMINI_API_KEY','GOOGLE_API_KEY'):env.pop(name,None)
            process=subprocess.Popen([str(python),str(Path(__file__).resolve()),'--worker'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True,env=env)
            _WORKER=(binding,process)
        process=_WORKER[1]
        request={'texts':texts,'kind':kind,'space':expected_space}
        try:
            process.stdin.write(json.dumps(request,ensure_ascii=False,allow_nan=False)+'\n');process.stdin.flush()
            line=process.stdout.readline()
            if not line:raise RuntimeError('local_inference_worker_failed: '+str(process.poll()))
            result=json.loads(line)
        except (OSError,json.JSONDecodeError):
            close_worker();raise RuntimeError('local_inference_worker_protocol_failed') from None
        if 'error' in result:raise RuntimeError('local_inference_failed: '+result['error'])
        if result.get('request_sha256')!=digest(request) or len(result.get('rows',[]))!=len(texts):
            raise ValueError('local inference response binding/cardinality mismatch')
        return result['rows']


class ModelRunner:
    """Exactly one lazy model per managed CLI or compatibility pipe worker."""
    def __init__(self,lock):
        actual={name:importlib.metadata.version(name) for name in PACKAGES}
        if actual!=lock['runtime']['packages']:raise RuntimeError('local inference dependency versions changed')
        self.lock=lock;self.model=None;self.pending_load_seconds=0.0

    def load(self):
        if self.model is not None:return
        import torch
        from sentence_transformers import SentenceTransformer
        lock=self.lock;torch.set_num_threads(lock['runtime']['threads']);start=time.monotonic()
        self.model=SentenceTransformer(str(ROOT/lock['package']),local_files_only=True,device=lock['runtime']['device'],model_kwargs={'torch_dtype':torch.float32})
        self.model.max_seq_length=8192;self.pending_load_seconds=time.monotonic()-start

    def run(self,request):
        import torch
        from sentence_transformers import SentenceTransformer
        lock=self.lock;load_seconds=0.0
        if request['space']!=lock['space']:raise ValueError('worker space mismatch')
        inputs=model_inputs(request['texts'],request['kind'])
        self.load();load_seconds=self.pending_load_seconds;self.pending_load_seconds=0.0
        runtime_lock()
        lengths=[len(ids) for ids in self.model.tokenizer(inputs,add_special_tokens=True,truncation=False)['input_ids']]
        if any(n>8192 for n in lengths):raise ValueError('embedding token limit exceeded; no silent truncation')
        start=time.monotonic()
        vectors=self.model.encode(inputs,prompt='',batch_size=lock['runtime']['batch_size'],normalize_embeddings=True,convert_to_numpy=True,show_progress_bar=False)
        elapsed=time.monotonic()-start;rows=[]
        for text,encoded,vector,tokens in zip(request['texts'],inputs,vectors,lengths,strict=True):
            values=[float(x) for x in vector]
            if len(values)!=768 or any(not math.isfinite(x) for x in values) or abs(sum(x*x for x in values)-1)>1e-4:raise ValueError('invalid local embedding vector')
            rows.append({'vector':values,'execution':{'schema':'photo-local-inference/v1','provider_executed':True,
                'space':lock['space'],'runtime':lock['runtime'],'installation_sha256':digest(lock),'kind':request['kind'],
                'input_sha256':hashlib.sha256(encoded.encode()).hexdigest(),'vector_sha256':digest(values),
                'tokens':tokens,'elapsed_seconds':elapsed,'load_seconds':load_seconds}})
        return rows


def preload():
    """Explicit post-core preparation, overlapping only independent source IO."""
    global _DIRECT_RUNNER
    lock=runtime_lock();binding=digest(lock)
    with _LOCK:
        if _DIRECT_RUNNER is None or _DIRECT_RUNNER[0]!=binding:_DIRECT_RUNNER=(binding,ModelRunner(lock))
        _DIRECT_RUNNER[1].load()


def worker():
    # Explicit inference entry point only. Nothing loads a model at import.
    runner=ModelRunner(runtime_lock())
    for line in sys.stdin:
        request=json.loads(line)
        try:
            rows=runner.run(request)
            print(json.dumps({'request_sha256':digest(request),'rows':rows},allow_nan=False),flush=True)
        except Exception as error:
            print(json.dumps({'request_sha256':digest(request),'error':type(error).__name__+': '+str(error)[:400]}),flush=True)


if __name__=='__main__':
    if sys.argv[1:]==['--worker']:worker()
    else:raise SystemExit('This is the skill-owned inference worker; use setup_local_embeddings.py.')
