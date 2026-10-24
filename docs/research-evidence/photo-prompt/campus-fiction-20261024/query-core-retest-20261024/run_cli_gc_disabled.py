"""Run the unchanged managed CLI, disabling cyclic GC only during this process.

The normal dispatcher, seal checks, assertions, command arguments and artifacts
are unchanged. Its exact subprocess launcher gets the same GC setting; no
installed/source member is modified. This is a run-local allocation setting.
"""
import gc
from pathlib import Path
import runpy
import subprocess
import sys

gc.disable()
LAUNCHER = ("import sys,runpy;from pathlib import Path;"
            "entry=sys.argv.pop(1);sys.path.insert(0,str(Path(entry).parent));"
            "runpy.run_path(entry,run_name='__main__')")
original_run = subprocess.run

def run(args, *positional, **kwargs):
    if (isinstance(args, list) and len(args) >= 5
            and args[1:4] == ['-I', '-c', LAUNCHER]
            and Path(args[4]).name == 'photo_workflow.py'):
        args = list(args)
        args[3] = 'import gc;gc.disable();' + args[3]
    return original_run(args, *positional, **kwargs)

subprocess.run = run
entry = Path(sys.argv.pop(1)).resolve()
sys.path.insert(0, str(entry.parent))
runpy.run_path(str(entry), run_name='__main__')
