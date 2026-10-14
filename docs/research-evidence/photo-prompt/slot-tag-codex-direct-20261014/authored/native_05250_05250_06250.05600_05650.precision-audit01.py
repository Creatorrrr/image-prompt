"""Manual precision audit: explicit individual corrections, no classification."""
import runpy
from pathlib import Path
R=Path(__file__).resolve().parents[1];p=R/'authored/native_05250_05250_06250.05600_05650.literals.py';D=runpy.run_path(str(p))['D']
def anchor(o,fid,quote):
 a=D[o];a['anchors']=[(f,path,key,quote if f==fid else q) for f,path,key,q in a['anchors']]
def val(o,key,value):
 c=list(D[o]['claims'][key]);c[5]=value;D[o]['claims'][key]=tuple(c)
def claimchange(o,key,**kw):
 c=list(D[o]['claims'][key]);ix=dict(dimension=0,target=1,property=2,mode=3,type=4,value=5,requires=6,operation=7,receivers=8)
 for k,v in kw.items():c[ix[k]]=v
 D[o]['claims'][key]=tuple(c)
def add(o,key,claim,fid,path,quote):
 D[o]['claims'][key]=claim;D[o]['anchors'].append((fid,path,key,quote));D[o]['units'][path].append(fid)
anchor(5618,'m_optics','metallic-foil cosmetic accent has controlled irregular edges and coherent reflective material')
anchor(5619,'m_entity','summoner adjusts a task-directed gesture toward one newly arrived separate entity')
val(5620,'render','several_rendered_motion_phases_preserving_one_existing_fixed_scene_anchor')
# Korean cockpit existence is not visibility or piloted/towering precision.
D[5625]['claims']['kgeneric']=('subject','mecha','subject.type.context.ko','context','subject.type.context.ko/v1','giant_mecha_with_cockpit',[],None,None)
D[5625]['anchors']=[(f,path,'kgeneric' if f in {'k_visible','k_generic'} else key,'조종석이 있는 거대 메카' if f=='k_visible' else q) for f,path,key,q in D[5625]['anchors']]
D[5625]['roles']={t:([x for x in refs if x!='k_visible'],modes) for t,(refs,modes) in D[5625]['roles'].items() if any(x!='k_visible' for x in refs)}
D[5625]['boundary']+=' Korean cockpit existence is context only; visibility uses explicit English and hardware precision uses embedding.'
anchor(5626,'m_drone','single aerial drone with rotors, camera gimbal')
anchor(5627,'m_motion','soluble rock landforms connect a closed sinkhole basin and disappearing surface water to an enlarged underground conduit and spring')
D[5628]['claims']['grole']=D[5628]['claims'].pop('gro le')
D[5628]['anchors']=[(f,path,'grole' if key=='gro le' else key,q) for f,path,key,q in D[5628]['anchors']]
corr=D[5628]['text_corrections'][0];corr['after']=corr['after'].replace('beside the same existing deceased traveler','beside the one same existing deceased traveler');corr['reason']+=' Preserve original one-traveler cardinality explicitly, not total scene count.'
anchor(5628,'m_traveler','one same existing deceased traveler');anchor(5628,'m_same','one same existing deceased traveler');anchor(5628,'m_walk','afterlife guide walks beside the one same existing deceased traveler')
add(5628,'count',('count','traveler','subject.count','prerequisite','subject.count/v1',1,[],None,None),'m_count','/content/embedding_text','one same existing deceased traveler')
D[5628]['roles']['subject_count']=(['m_count'],['prerequisite'])
val(5629,'deck','aircraft_flight_deck')
add(5629,'genericdeck',('setting','deck','setting.generic.context','context','setting.generic.context/v1','realistic_generic_aircraft_flight_deck',[],None,None),'m_genericdeck','/content/embedding_text','realistic generic aircraft flight deck')
anchor(5631,'m_substrate','selected existing rock features remain visibly continuous with their nonface rock substrate')
# EN lacks continuous transition precision explicitly present in embedding; distinct property.
val(5636,'color','highest_inner_center_saturation_outward_fade_toward_vermilion_edge')
add(5636,'continuous',('appearance','lips','lips.color.continuity','effect','lips.color.continuity/v1','continuous_outward_fade',['m_lips'],'set_value',['lips']),'m_continuous','/content/embedding_text','a continuous outward fade')
D[5636]['roles']['lip_color_placement'][0].append('m_continuous')
# Adult describes use classification; do not invent an actual physical size or adult wearer.
D[5640]['text_corrections'][0]['after']=D[5640]['text_corrections'][0]['after'].replace('adult-size','adult-use')
D[5640]['text_corrections'][0]['reason']=D[5640]['text_corrections'][0]['reason'].replace('adult-size','adult-use').replace('scope/size','scope/use')
D[5640]['anchors']=[(f,path,key,q.replace('adult-size','adult-use')) for f,path,key,q in D[5640]['anchors']]
val(5640,'base','adult_use_tailored_opaque_garment')
for k in ['meaning','boundary','owner_issue','binding_intent']:D[5640][k]=D[5640][k].replace('Adult-size','Adult-use').replace('adult-size','adult-use').replace('scope/size','scope/use')
# Visible integration in EN does not independently assert separately readable parts.
val(5644,'construction','internal_shelf_bra_liner_and_underband_attached_inside_tank')
D[5644]['claims']['evisible']=('framing','internal_liner_band','framing.visibility.integration','effect','framing.visibility.integration/v1','internal_liner_and_underband_visibly_integrated',['m_tank','m_type'],'set_value',['internal_liner_band'])
D[5644]['anchors']=[(f,path,'evisible' if f=='e_visible' else key,q) for f,path,key,q in D[5644]['anchors']]
add(5644,'underbust',('appearance','tank','garment.construction.underbust_band','effect','garment.construction.underbust_band/v1','underbust_shelf_band_attached_inside',['m_tank','m_type'],'set_value',['tank']),'m_underbust','/content/embedding_text','inner bust liner and underbust shelf band are attached as an integrated shelf-bra construction')
D[5644]['roles']['garment_detail'][0].append('m_underbust')
for o in [5628,5636,5644]:
 D[o]['effects']=sorted({(v[0],v[1],v[2]) for v in D[o]['claims'].values() if v[3]=='effect'})
with p.open('w') as f:
 f.write('"""Explicit manually authored meaning/fact cells; no semantic inference code."""\nD={}\n')
 for o,a in D.items():f.write('D['+str(o)+']='+repr(a)+'\n')
