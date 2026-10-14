"""Explicit manual quote-owner/mode audit before immutable freeze; no semantic classifier."""
import runpy
from pathlib import Path
R=Path(__file__).resolve().parents[1];p=R/'authored/native_05250_05250_06250.06150_06200.literals.py';D=runpy.run_path(str(p))['D'];e='/content/en';m='/content/embedding_text';k='/content/ko'
def val(o,key,value):
 x=list(D[o]['claims'][key]);x[5]=value;D[o]['claims'][key]=tuple(x)
def anchor(o,fid,path,key,q):D[o]['anchors']=[(fid,path,key,q) if x[0]==fid else x for x in D[o]['anchors']]
def add(o,key,claim,fid,path,q):D[o]['claims'][key]=claim;D[o]['anchors'].append((fid,path,key,q))
# 6150 M lacks zeroing, K explicitly names zero/reference calibration stage.
D[6150]['anchors']=[x for x in D[6150]['anchors'] if x[0]!='m_action']
anchor(6150,'m_step',k,'step','기기 영점과 기준 표적 교정 단계')
# Exact hand tools EN versus embroidery tools M, no invented basting-tool class.
val(6157,'tools','embroidery_tools');add(6157,'handtools',('subject','handtools','prop.type','prerequisite','prop.type/v1','hand_tools',[],None,None),'e_handtools',e,'hand tools');D[6157]['roles']['prop'][0].append('e_handtools')
# 6163 readable literal, no workflow commentary inside proposed prompt.
c=D[6163]['text_corrections'][0];old=c['after'];new='A fictional jianghu handoff post is at the junction of a riverside inn and a ferry landing. No current handoff, ferry arrival or passengers are specified.';c['after']=new
D[6163]['anchors']=[(i,path,key,new if q==old else q) for i,path,key,q in D[6163]['anchors']]
anchor(6163,'m_guard',m,'guard','No current handoff, ferry arrival or passengers are specified')
# 6168 only EN full phrase supports documented regional bunad set/variant.
anchor(6168,'e_variant',e,'variant','a documented region-specific bunad accessory set coordinated with one named variant')
D[6168]['claims']['illustrative']=('concept','accessory_set','concept.illustrative_components.context','context','concept.illustrative_components.context/v1','silverwork_belt_headwear_bag_illustrative_not_mandatory_union',[],None,None)
anchor(6168,'m_set',m,'illustrative','bunad accessories such as documented silverwork belt headwear or bag are selected only for one named regional variant and stay coherent with its garments; generic Nordic jewelry cannot choose the variant')
# Explicit human type is actual source-proposed body scope, not inferred from presence.
add(6176,'human_type',('subject','actor','subject.type','prerequisite','subject.type/v1','human',[],None,None),'m_human_type',m,'existing adult human body');D[6176]['roles']['subject'][0].append('m_human_type')
# K actually requires solar-vector/activity-structure legibility; keep actual E.
add(6178,'readable',('framing','comet','framing.relation_visibility','effect','framing.relation_visibility/v1','solar_direction_and_comet_activity_structure_readable',[],'set_value',['comet']),'k_readable',k,'태양 방향과 혜성 활동 구조가 읽히는 소천체 조우 관측 미학');D[6178]['roles']['subject_framing']=(['k_readable'],['effect'])
# K actually says folding PHONE; EN/M only describe clamshell body.
val(6181,'phone','clamshell_phone');anchor(6181,'e_phone',k,'phone','얇은 금속광 폴더폰')
# M garment-owned does not name leggings; EN legging fabric does.
anchor(6187,'m_garment',e,'garment','a shortened center-back seam channel gathering the legging fabric into repeated ruching')
# Selected surface phrase supports only selected surface; folds PR independently exact.
val(6188,'surface','selected_garment_surface')
# M around same adult, EN personal storage: each exact own field, no quote borrowing.
val(6195,'place','prior_matching_objects_remain_around_same_adult')
add(6195,'storage',('composition','objects','props.placement.storage','preservation','props.placement.storage/v1','same_category_objects_visibly_occupy_personal_storage_space',['m_objects'],None,None),'e_storage',e,'same-category group with no opening or use traces visibly occupying personal storage space');D[6195]['roles']['prop_placement'][0].append('e_storage')
# M complete power/data/output, EN external path; don't merge unsupported scalar.
val(6198,'connections','complete_power_data_output_connections_remain_visibly_traceable')
add(6198,'external_visibility',('framing','equipment','framing.external_path_visibility','preservation','framing.external_path_visibility/v1','antennas_controllers_cables_external_sound_paths_remain_traceable',['e_inventory'],None,None),'e_external',e,'an electronic-instrument studio where antennas, controllers, cables, and external sound paths remain traceable');D[6198]['roles']['subject_framing'][0].append('e_external')
for o,a in D.items():
 a['units']={}
 for fid,path,key,q in a['anchors']:a['units'].setdefault(path,[]).append(fid)
 a['effects']=sorted({(x[0],x[1],x[2]) for x in a['claims'].values() if x[3]=='effect'})
with p.open('w') as f:
 f.write('"""Explicit manually authored native meaning/fact cells; no semantic inference code."""\nD={}\n')
 for o,a in D.items():f.write('D['+str(o)+']='+repr(a)+'\n')
