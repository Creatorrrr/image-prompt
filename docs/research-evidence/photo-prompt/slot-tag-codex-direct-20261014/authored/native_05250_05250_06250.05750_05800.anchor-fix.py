"""Exact quote follow-through after explicit 7/8 harmonization."""
import runpy
from pathlib import Path
p=Path(__file__).resolve().with_name('native_05250_05250_06250.05750_05800.literals.py');D=runpy.run_path(str(p))['D'];D[5760]['anchors']=[(i,path,key,'fitted seven-eighth leggings' if i=='m_fit' else q) for i,path,key,q in D[5760]['anchors']]
with p.open('w') as f:
 f.write('"""Explicit manually authored meaning/fact cells; no semantic inference code."""\nD={}\n')
 for o,a in D.items():f.write('D['+str(o)+']='+repr(a)+'\n')
