"""Isolate source-only replay from network, credentials and unrelated processes."""
import json, os, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).parent
SAFE_KEYS = {'PATH','LC_ALL','LC_CTYPE','PYTHONPATH','PYTHONDONTWRITEBYTECODE',
             'GEMINI_API_KEY','GOOGLE_API_KEY','V28_GUARD_LOG','COLUMNS','LINES',
             'LANGUAGE','PYTHON_COLORS','NO_COLOR','FORCE_COLOR','TERM'}
ALLOWED = ['.venv/bin/python','skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py',
           '--seed','910000','--authorial-core-json','tests/fixtures/photo_prompt/current_boundary/core.json',
           '--request-envelope-json','tests/fixtures/photo_prompt/current_boundary/envelope.json',
           '--creative-controls-json','tests/fixtures/photo_prompt/current_boundary/controls.json',
           '--embodiment-review-json','tests/fixtures/photo_prompt/current_boundary/review.json','--output-file']

def install():
    tempfile.tempdir = '/tmp'
    original = dict(os.environ)
    assert set(original) <= SAFE_KEYS, 'Unexpected environment keys'
    assert not original.get('GEMINI_API_KEY') and not original.get('GOOGLE_API_KEY')
    log = Path(original['V28_GUARD_LOG'])
    testing = False
    def record(event, status):
        with log.open('a') as stream:
            stream.write(json.dumps({'pid':os.getpid(),'event':event,'status':status,'self_test':testing})+'\n')
    def deny(event):
        record(event, 'blocked')
        raise PermissionError('Offline guard: '+event)
    def guard(event,args):
        if event.startswith('socket.') or event in {'os.system','os.posix_spawn','os.exec','os.fork','os.forkpty','ctypes.dlopen','ctypes.dlsym'}:
            deny(event)
        if event == 'import' and args and str(args[0]).split('.')[0] in {'requests','httpx','google','openai','dotenv','ctypes'}:
            deny('provider import')
        if event == 'open' and args and isinstance(args[0],(str,bytes,os.PathLike)):
            path = Path(os.path.abspath(os.fsdecode(args[0])))
            parts = {p.lower() for p in path.parts}
            name = path.name.lower()
            if name == '.env' or name.startswith('.env.') or name in {'credentials','credentials.json','application_default_credentials.json','id_rsa','id_ed25519'} or parts & {'.aws','.ssh','.config','.codex','private-inputs'} or path == Path('/root') or Path('/root') in path.parents:
                deny('credential/private read')
        if event == 'subprocess.Popen':
            command=args[1]
            if not isinstance(command,list) or command[:-1] != ALLOWED or len(command)!=len(ALLOWED)+1:
                deny('unapproved subprocess')
            output=Path(command[-1])
            if not output.is_absolute() or Path('/tmp') not in output.parents:
                deny('unapproved generator output')
            environment=args[3]
            if not environment or set(environment)-SAFE_KEYS or environment.get('PYTHONPATH')!=str(HERE) or environment.get('V28_GUARD_LOG')!=str(log):
                deny('unguarded generator subprocess')
            record('exact frozen generator subprocess','allowed')
    sys.addaudithook(guard)
    class SafeEnvironment(dict):
        def __getitem__(self,key):
            if key not in SAFE_KEYS: deny('environment credential access')
            return super().__getitem__(key)
        def get(self,key,default=None):
            if key not in SAFE_KEYS or key in {'GEMINI_API_KEY','GOOGLE_API_KEY'}: deny('environment credential access')
            return super().get(key,default)
        def __contains__(self,key):
            if key not in SAFE_KEYS: deny('environment credential access')
            return super().__contains__(key)
    os.environ=SafeEnvironment(original)
    os.environb={}
    testing=True
    for event,args in [('socket.__new__',(None,2,1,0)),('subprocess.Popen',('forbidden',[],None,None)),('open',('/root/never-opened','r',0))]:
        try: sys.audit(event,*args)
        except PermissionError: pass
        else: raise AssertionError('Offline guard self-test failed')
    try: os.environ.get('GEMINI_API_KEY')
    except PermissionError: pass
    else: raise AssertionError('Environment guard self-test failed')
    testing=False
    record('guard installed','pass')
