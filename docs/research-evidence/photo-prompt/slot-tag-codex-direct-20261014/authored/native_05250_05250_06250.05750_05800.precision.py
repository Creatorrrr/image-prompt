"""Explicit hand-reviewed quote/owner/state precision corrections."""
import runpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];p=R/'authored/native_05250_05250_06250.05750_05800.literals.py';D=runpy.run_path(str(p))['D'];P=json.loads((R/'authored/native_05250_05250_06250.05750_05800.packet.json').read_text());M='/content/embedding_text'
def text(o):
 cs=[x for x in D[o]['text_corrections'] if x['pointer']==M]
 return cs[0]['after'] if cs else P['records'][o-5750]['after_existing5B']['content']['embedding_text']
def change(o,s,why):
 cs=[x for x in D[o]['text_corrections'] if x['pointer']==M]
 if cs:cs[0]['after']=s;cs[0]['reason']+=' '+why
 else:D[o]['text_corrections'].append(dict(pointer=M,before=text(o),after=s,reason=why))
def anchor(o,fid,q):D[o]['anchors']=[(i,path,key,q if i==fid else old) for i,path,key,old in D[o]['anchors']]
def value(o,key,v):
 a=list(D[o]['claims'][key]);a[5]=v;D[o]['claims'][key]=tuple(a)
C=lambda d,t,p,m,v,req=[],op=None,recv=None,typ=None:(d,t,p,m,typ or p+'/v1',v,req,op,recv)
anchor(5750,'m_construct',text(5750));anchor(5750,'m_visible',text(5750))
D[5751]['claims']['kgeneric']=C('appearance','caftan','garment.construction.context.ko','context','Moroccan_caftan_central_trim_fastening_belt_relation')
D[5751]['anchors']=[(i,path,'kgeneric' if i=='k_generic' else key,q) for i,path,key,q in D[5751]['anchors']]
anchor(5753,'m_parts',text(5753))
change(5760,text(5760).replace('fitted leggings ending','fitted seven-eighth leggings ending'),'Harmonize precise EN/K7/8 length into M rather than pretending just-above-ankle alone literally asserts numeric7/8.')
anchor(5760,'m_length','fitted seven-eighth leggings ending just above the ankles');anchor(5760,'m_ensemble',text(5760));anchor(5760,'m_leggings',text(5760))
value(5763,'original','original_prop_unspecified_design')
anchor(5766,'m_construct',text(5766));anchor(5766,'m_attach',text(5766));anchor(5766,'m_load',text(5766))
anchor(5774,'m_visible',text(5774))
D[5777]['anchors'].append(('p3_count','/content/paraphrases/3','pair','한 쌍의 둥근 안경 렌즈'))
anchor(5779,'m_shape',text(5779))
anchor(5782,'m_band',text(5782));anchor(5782,'m_visible',text(5782))
anchor(5783,'m_view',text(5783))
anchor(5784,'m_quality',text(5784));anchor(5784,'m_level',text(5784));anchor(5784,'m_gaps',text(5784))
anchor(5789,'m_state',text(5789))
D[5791]['claims']['kcontext']=C('role','capture','capture.context.ko','context','flat_lay_photography_showing_prop_arrangement')
D[5791]['anchors']=[(i,path,'kcontext' if i=='k_context' else key,q) for i,path,key,q in D[5791]['anchors']]
value(5792,'path','two_shoulder_straps_cross_once_on_back_continue_to_opposite_lower_sides')
anchor(5793,'m_depth',text(5793))
change(5794,text(5794).replace('The sarong boundary below the kebaya remains distinct','The sarong boundary below the kebaya is distinct'),'Original declares distinct lower boundary, not keep/remain. Retain this actual exposure/boundary requirement as E rather than invent prior-state preservation.')
D[5794]['claims']['boundary']=C('appearance','outfit','wardrobe.layers.exposure','effect','separate_sarong_boundary_distinct_below_kebaya',['m_kebaya','m_sarong'],'set_value',['kebaya','sarong'])
anchor(5794,'m_boundary','The sarong boundary below the kebaya is distinct');D[5794]['roles']['wardrobe_layering']=(['m_boundary'],['effect'])
D[5794]['meaning']='Existing kebaya and separate sarong; selected button/scalloped-hem variant. Actual fitted front/fastening/hem and distinct below sarong exposure, no invented preservation or worn owner.'
D[5794]['owner_issue']='Existing kebaya/separate sarong require native frozen witnesses; actual fit/button/hem/state and distinct lower-boundary exposure E permission pending. Earlier partial45 remain-distinct preservation interpretation explicitly corrected before freeze, old artifact retained history.'
D[5794]['binding_intent']='Preserve optional/direct garment_detail weight0.64 intrinsic human and exact human/four-domain binding. Separate sarong actual lower-boundary exposure E, unlike integrated liner. Native owners/permission pending; no original remain guard invented.'
change(5795,'The selected existing one person arrives at a community event; a modest welcome path and independent cameras direct attention toward that person, while familiar reactions support a local-renown reading. The exact people making those reactions and their visible reaction forms are unspecified. No banners, crowns, readable titles or rankings, or pageant staging are selected.','State the source-selected arrival carrier explicitly as the already named one-person attention target, rather than grounding actor action only in event noun. Root source-owner interpretation remains unapproved, no new person/crowd.')
anchor(5795,'m_situation',text(5795));anchor(5795,'m_arrival','The selected existing one person arrives at a community event');anchor(5795,'m_attention',text(5795))
anchor(5799,'m_source',text(5799))
for o,a in D.items():
 a['units']={}
 for ident,path,key,q in a['anchors']:a['units'].setdefault(path,[]).append(ident)
 a['effects']=sorted({(v[0],v[1],v[2]) for v in a['claims'].values() if v[3]=='effect'})
with p.open('w') as f:
 f.write('"""Explicit manually authored meaning/fact cells; no semantic inference code."""\nD={}\n')
 for o,a in D.items():f.write('D['+str(o)+']='+repr(a)+'\n')
b=R/'authored/native_05250_05250_06250.05750_05800.build.py'
s=b.read_text().replace('05750_05795.draft_before_reread','05750_05800.draft_before_reread').replace("out=R/f'authored/native_05250_05250_06250.05750_{stop:05d}.draft_before_reread.json'","out=R/'authored/native_05250_05250_06250.05750_05800.reread01.json'")
with (R/'authored/native_05250_05250_06250.05750_05800.reread.py').open('x') as f:f.write(s)
