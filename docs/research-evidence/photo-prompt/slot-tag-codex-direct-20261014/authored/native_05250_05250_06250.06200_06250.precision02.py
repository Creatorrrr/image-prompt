"""Four exact quote scopes and footwear value precision, manually selected before freeze."""
import runpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];p=R/'authored/native_05250_05250_06250.06200_06250.literals.py';D=runpy.run_path(str(p))['D'];P=json.loads((R/'authored/native_05250_05250_06250.06200_06250.packet.json').read_text())
for o,fid,q in [(6221,'m_uniform',P['records'][21]['after_existing5B']['content']['embedding_text']),(6230,'m_set',D[6230]['text_corrections'][0]['after']),(6234,'m_state',D[6234]['text_corrections'][0]['after'])]:D[o]['anchors']=[(i,path,key,q if i==fid else oldq) for i,path,key,oldq in D[o]['anchors']]
x=list(D[6222]['claims']['inventory']);x[5]='small_fitted_top_voluminous_harem_trousers_low_profile_footwear';D[6222]['claims']['inventory']=tuple(x)
x=list(D[6222]['claims']['shoes']);x[5]='low_profile';D[6222]['claims']['shoes']=tuple(x)
for o,a in D.items():
 a['units']={}
 for fid,path,key,q in a['anchors']:a['units'].setdefault(path,[]).append(fid)
with p.open('w') as f:
 f.write('"""Explicit manually authored native meaning/fact cells; no semantic inference code."""\nD={}\n')
 for o,a in D.items():f.write('D['+str(o)+']='+repr(a)+'\n')
