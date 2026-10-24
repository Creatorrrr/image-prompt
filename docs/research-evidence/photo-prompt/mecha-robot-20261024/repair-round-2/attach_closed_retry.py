"""Execute the maintained closed attachment contract without CLI version routing."""
import gc,sys,json
from pathlib import Path
from argparse import Namespace
gc.disable()
sys.path.insert(0,str(Path('/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts')))
import prepare_retry_context as coordinator
print(json.dumps(coordinator.attach_child(Namespace(run=Path(sys.argv[1]),proof=Path(sys.argv[2])))),flush=True)
