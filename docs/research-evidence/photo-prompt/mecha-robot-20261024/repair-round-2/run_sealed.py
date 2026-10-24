"""Scheduling-only wrapper: execute the unchanged named sealed CLI and validators."""
import gc,runpy,sys
from pathlib import Path
gc.disable()
target=sys.argv.pop(1)
sys.argv[0]=target
sys.path.insert(0,str(Path(target).parent))
runpy.run_path(target,run_name='__main__')
