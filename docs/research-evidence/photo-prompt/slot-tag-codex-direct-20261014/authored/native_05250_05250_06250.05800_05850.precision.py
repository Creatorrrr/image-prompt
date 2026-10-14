"""Explicit manual quote/owner precision audit; no automated semantic approval."""
import runpy
from pathlib import Path
R=Path(__file__).resolve().parents[1];p=R/'authored/native_05250_05250_06250.05800_05850.literals.py';D=runpy.run_path(str(p))['D']
def value(o,key,val):
 a=list(D[o]['claims'][key]);a[5]=val;D[o]['claims'][key]=tuple(a)
def quote(o,fid,q):
 D[o]['anchors']=[(i,path,key,q if i==fid else old) for i,path,key,old in D[o]['anchors']]
def after(o):return next(a['after'] for a in D[o]['text_corrections'] if a['pointer']=='/content/embedding_text')
value(5800,'place','reef_system')
quote(5804,'e_leather','woven-leather sample panel')
D[5804]['owner_issue']=D[5804]['owner_issue'].replace(' Mguard facts need separate unbranded/exclusion typed claims in precision audit.',' Separate exact unbranded and printed/embossed-exclusion claims audited; no shared misleading quote.')
quote(5807,'m_trim',after(5807).split(' Their stated')[0]);quote(5807,'m_optics',after(5807).split(' Their stated')[0])
for key in ['trim','generic']:
 a=list(D[5807]['claims'][key]);a[1]='garment_surface';
 if key=='trim':a[8]=['garment_surface']
 D[5807]['claims'][key]=tuple(a)
quote(5815,'m_consequence',after(5815).split(' The operator')[0])
quote(5816,'m_detail',after(5816).split('; no specific')[0])
c=D[5818]['text_corrections'][0];c['after']=c['after'].replace('summoned entity moves back','summoned entity is released and moves back');c['reason']+=' Explicit release wording also harmonizes positive EN/K, not inferred from a return-variant label.'
quote(5818,'m_return','summoned entity is released and moves back through the same existing complete bounded threshold');quote(5818,'m_release','summoned entity is released');quote(5818,'m_close',after(5818).split(' The gesture')[0])
quote(5821,'m_placement',after(5821).split(' The current')[0]);quote(5822,'m_view',after(5822).split(' The exact')[0])
value(5823,'realism','optical_realism_appearance');value(5825,'hands','owned_hands')
value(5829,'upland','drier_upland');quote(5829,'m_upland','drier upland')
quote(5831,'m_step',after(5831).split(' The exact')[0]);quote(5836,'m_structure',D[5836]['anchors'][1][3]+' in an editorial portrait, with the specific structure and contact relation visible')
D[5836]['owner_issue']=D[5836]['owner_issue'].replace(' Structure visibility fragment interpreted within full M weapon antecedent, final precision anchor full M.',' Structure visibility anchor now includes exact full weapon/presentation antecedent in M.')
# One physical material token owns the actual strips; independent EN exact phrase lacks strip antecedent.
D[5804]['anchors']=[(i,'/content/embedding_text' if i=='e_leather' else path,key,'separate leather strips' if i=='e_leather' else q) for i,path,key,q in D[5804]['anchors']]
# Rebind only the manually moved exact material anchor unit; retain all existing positive strings.
D[5804]['units']['/content/en'].remove('e_leather');D[5804]['units']['/content/embedding_text'].append('e_leather')
for o in [5807]:D[o]['effects']=sorted({(v[0],v[1],v[2]) for v in D[o]['claims'].values() if v[3]=='effect'})
with p.open('w') as f:
 f.write('"""Explicit manually authored meaning/fact cells; no semantic inference code."""\nD={}\n')
 for o,a in D.items():f.write('D['+str(o)+']='+repr(a)+'\n')
print('Manually audited exact anchors/owners/typed values; no formal or semantic qualification claimed.')
