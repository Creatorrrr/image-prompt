"""Explicit manual quote precision/meaning audit; no classifier."""
import runpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];p=R/'authored/native_05250_05250_06250.05700_05750.literals.py';D=runpy.run_path(str(p))['D'];P=json.loads((R/'authored/native_05250_05250_06250.05700_05750.packet.json').read_text());M='/content/embedding_text'
def text(o):
 cs=[x for x in D[o]['text_corrections'] if x['pointer']==M]
 return cs[0]['after'] if cs else P['records'][o-5700]['after_existing5B']['content']['embedding_text']
def change(o,s,reason):
 cs=[x for x in D[o]['text_corrections'] if x['pointer']==M]
 if cs:cs[0]['after']=s;cs[0]['reason']+=' '+reason
 else:D[o]['text_corrections'].append(dict(pointer=M,before=text(o),after=s,reason=reason))
def anchor(o,fid,q):
 D[o]['anchors']=[(i,path,key,q if i==fid else old) for i,path,key,old in D[o]['anchors']]
def value(o,key,v):
 c=list(D[o]['claims'][key]);c[5]=v;D[o]['claims'][key]=tuple(c)
def fact(o,key,claim,ident,path,q,role=None):
 D[o]['claims'][key]=claim;D[o]['anchors'].append((ident,path,key,q))
 if role:D[o]['roles'][role]=([ident],[claim[3]])
C=lambda d,t,p,m,v,req=[],op=None,recv=None,typ=None:(d,t,p,m,typ or p+'/v1',v,req,op,recv)
anchor(5703,'k_fit','오버사이즈 스포츠 저지')
value(5708,'form','dress_form')
fact(5708,'neutral',C('concept','dress_form','concept.presentation.context','context','neutral_unspecified_presentation'),'m_neutral',M,'neutral dress form')
anchor(5708,'e_construction','a dress form carrying a basted toile with pins, balance lines, and visible internal support layers')
change(5708,text(5708).replace('internal structure','internal support layers'),'Harmonize explicit ENinternal support layers with Mgeneric internal structure; neutral remains unspecified presentation context rather than an ENunsupported neutral form type.')
anchor(5708,'m_construction','basting pins balance lines tulle and internal support layers')
anchor(5710,'m_fan',text(5710))
anchor(5711,'m_gaze',text(5711))
change(5713,text(5713).replace('is left there, with','is left there as consequences of that repeated action, with'),'Make ENexplicit left-by-ghost causal relationship explicit in Mwithout inventing key-press technique.')
anchor(5713,'m_physics',text(5713));anchor(5713,'m_dust',text(5713))
anchor(5716,'m_texture',text(5716))
anchor(5719,'m_synchrony',text(5719));anchor(5719,'m_physics',text(5719));anchor(5719,'m_interaction',text(5719))
change(5723,text(5723).replace('keep the asymmetric overlap and broad sash readable','the asymmetric overlap and broad sash are readable'),'Remove keep grammar that could falsely imply prior-state preservation; original Krequests actual readable overlap/sash.')
anchor(5723,'m_visible','the asymmetric overlap and broad sash are readable')
anchor(5728,'m_contact',text(5728));anchor(5728,'m_interaction',text(5728))
anchor(5731,'m_galaxies',text(5731))
anchor(5733,'m_origin',text(5733));anchor(5733,'m_inspect',text(5733))
anchor(5734,'m_clearance',text(5734));anchor(5734,'m_visible',text(5734))
D[5736]['roles'].pop('transformation_stage')
D[5736]['boundary']+=' Selected current erosion/deposition building is not a separately identified observable transformation stage; actual building E remains, fine transformation_stage withheld.'
D[5736]['owner_issue']+=' Root must resolve exact process-stage meaning; role withholding does not delete building E.'
change(5739,text(5739).replace('its ice is flowing as stated in the Korean source','its ice is flowing'),'Remove source-commentary phrase from actual positive cue while retaining literal ice flow. Separate generic active-valley subject from Mcontinuous extent and Kjoint-visibility constraints.')
value(5739,'subject','active_valley_glacier')
fact(5739,'continuous',C('setting','glacier','environment.detail.continuity','effect','continuous_glacier',[],'set_value',['glacier']),'m_continuous',M,'active continuous valley glacier')
D[5739]['roles']['environment_detail'][0].append('m_continuous')
fact(5739,'visible',C('framing','glacier_structures','framing.joint_visibility','effect','ice_crevasses_glacial_valley_moraines_jointly_visible',[],'set_value',['ice','glacier','valley','moraines']),'k_visible','/content/ko','흐르는 빙체·크레바스·빙식곡·빙퇴석이 함께 보이는',role='subject_framing')
# Explicit Msoft pneumatic care robot: softness is declared for the robot, no invented body material adjective.
D[5742]['claims']['soft']=C('material','robot','surface.material.softness','effect','soft',[],'set_value',['robot'])
D[5742]['anchors']=[a for a in D[5742]['anchors'] if a[0]!='m_generic']
# Frame legibility is actual source, clinical sound results excluded; no exact instrument chosen.
# Whole-source binding quotations retain all named endpoints rather than isolated generic verbs.
anchor(5740,'m_visible',text(5740));anchor(5740,'m_light',text(5740))
anchor(5744,'m_structure',text(5744));anchor(5744,'m_frame',text(5744))
anchor(5746,'m_paths',text(5746));anchor(5746,'m_contact',text(5746));anchor(5746,'m_visible',text(5746))
anchor(5749,'m_pattern',text(5749));anchor(5749,'m_color',text(5749));anchor(5749,'m_visible',text(5749));anchor(5749,'m_strength',text(5749))
for o,a in D.items():
 a['units']={}
 for ident,path,key,q in a['anchors']:a['units'].setdefault(path,[]).append(ident)
 a['effects']=sorted({(v[0],v[1],v[2]) for v in a['claims'].values() if v[3]=='effect'})
with p.open('w') as f:
 f.write('"""Explicit manually authored meaning/fact cells; no semantic inference code."""\nD={}\n')
 for o,a in D.items():f.write('D['+str(o)+']='+repr(a)+'\n')
# New reread artifact, old checkpoint JSON unchanged.
b=R/'authored/native_05250_05250_06250.05700_05750.build.py'
s=b.read_text().replace('05700_05745.draft_before_reread','05700_05750.draft_before_reread').replace("out=R/f'authored/native_05250_05250_06250.05700_{stop:05d}.draft_before_reread.json'","out=R/'authored/native_05250_05250_06250.05700_05750.reread01.json'")
q=R/'authored/native_05250_05250_06250.05700_05750.reread.py'
with q.open('x') as f:f.write(s)
