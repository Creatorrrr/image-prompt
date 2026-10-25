from pathlib import Path
import gc,json,sys
gc.disable();P=Path(__file__).resolve().parent;ROOT=P.parents[4];S=ROOT/'skills/photo-prompt-image-generator';sys.path.insert(0,str(S/'scripts'))
from build_shared_candidate_index import build
cache=Path('/Users/chasoik/.cache/image-prompt/investigative-publication-01a1723b-20261025');space=json.loads((S/'embedding-runtime.lock.json').read_bytes())['space']
result=build(S/'assets',cache,space=space)
(P/'index-build.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False),flush=True)
