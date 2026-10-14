"""Explicit manual final precision edits after all50 full-source/after readings."""
import json,runpy
from pathlib import Path
R=Path(__file__).resolve().parents[1];p=R/'authored/native_05250_05250_06250.05950_06000.literals.py';D=runpy.run_path(str(p))['D'];P=json.loads((R/'authored/native_05250_05250_06250.05950_06000.packet.json').read_text());m='/content/embedding_text';e='/content/en';k='/content/ko'
def anchor(o,ident,q,path=None):
 a=D[o]['anchors'];idx=next(i for i,x in enumerate(a) if x[0]==ident);old=a[idx];a[idx]=(old[0],path or old[1],old[2],q)
def claim(o,key,**vals):
 names=['dimension','target','property','mode','type','value','requires','operation','receivers'];v=list(D[o]['claims'][key])
 for n,value in vals.items():v[names.index(n)]=value
 D[o]['claims'][key]=tuple(v)
# Original Kpositive straight antenna is vertical; retain precise Ksource prerequisite, not keyword inference.
D[5954]['claims']['vertical']=('appearance','straight_antenna','object.geometry.axis','prerequisite','object.geometry.axis/v1','vertical_straight_antenna',[],None,None)
D[5954]['anchors'].append(('k_vertical',k,'vertical','수직 안테나'))
D[5954]['owner_issue']+=' Exact Korean vertical straight-antenna geometry independently retained as prerequisite k_vertical; no automatic antenna creation or axis inference from English straight.'
# Phase coexistence is explicit EN; Mphase-nuclei/growth scope is a different literal statement.
claim(5973,'stage',value='parent_phase_nuclei_and_growing_new_phase_belong_same_material_system')
D[5973]['claims']['coexist']=('timing','specimen','transformation.coexistence','effect','transformation.coexistence/v1','single_specimen_parent_and_emerging_phases_coexist',[],'set_value',['specimen'])
D[5973]['anchors'].append(('e_coexist',e,'coexist','single bounded specimen containing both parent and emerging phases'))
D[5973]['roles']['transformation_stage'][0].append('e_coexist')
# The ENalignment fragment has no named actor: retain it as generic context and ground actual hunter operation in M.
D[5975]['claims']['generic']=('action','alignment','action.align_clues.context','context','action.align_clues.context/v1','weathered_map_compass_bearing_distant_ruin_alignment',[],None,None)
idx=next(i for i,a in enumerate(D[5975]['anchors']) if a[0]=='e_align');fid,path,key,q=D[5975]['anchors'][idx];D[5975]['anchors'][idx]=(fid,path,'generic',q)
D[5975]['anchors'].append(('m_align',m,'align',P['records'][25]['after_existing5B']['content']['embedding_text']))
D[5975]['roles']['action']=(['m_align'],['effect'])
# Apparatus motion is coupled to image succession; its trajectory is not specified along the optical path.
after='In this translucent-screen and sequential-replacement variant, the visible lantern lens and operator produce a succession of projected spectral images on a translucent screen. Sequential replacement is tied to actual apparatus movement; the projections follow the lantern optical path to that screen. The images remain represented projections, not external ghosts; no smoke/haze receiver, additional scale-shift requirement or exact apparatus trajectory is selected.'
D[5993]['text_corrections'][0]['after']=after
D[5993]['text_corrections'][0]['reason']='Select translucent-screen/sequential-replacement alternatives, retain visiblelens/operator production and sequence tied to actual apparatusmovement. Klantern optical path belongs to projections toward selected screen; do not invent apparatus trajectory along that path.'
anchor(5993,'m_path','the projections follow the lantern optical path to that screen')
D[5993]['owner_issue']='Lantern/operator/screen/projection/optics/production/sequence/apparatusmovement permissions pending. Exact spectralcontours/receiverregion bounds/nativepattern precision absent, fine light_shape held. Final manual audit removes unsupported apparatus motion along optical path while keeping both actual movement and Kprojection-path relation. Selected screen/sequence harmonization unapproved.'
# Individually chosen full-source quote expansions resolve antecedents/ownership/property components.
for o,ids in [(5953,['m_sparks','m_scorch']),(5954,['m_hands','m_arms','m_fields','m_gap','m_visible']),(5956,['m_geometry','m_guard']),(5959,['m_result','m_joints']),(5961,['m_connection']),(5968,['m_legible','m_access']),(5972,['e_material']),(5973,['m_stage','m_growth']),(5974,['m_entry','m_features','m_position','m_visible']),(5977,['k_v']),(5979,['m_view','m_visible']),(5980,['m_position','m_visible']),(5982,['m_garment']),(5984,['m_structure','m_axis','m_alignment','m_visible']),(5986,['m_cloth','m_optics','m_structure','m_layers','m_undershirt','m_underoptics','m_visible']),(5992,['m_body','m_visible']),(5993,['m_apparatus','m_role','m_projection','m_sequence','m_motion','m_path']),(5994,['m_visible']),(5995,['m_jacket','m_shirt','m_lower','m_footwear','m_use']),(5997,['m_terminal','m_visible']),(5998,['m_glove','m_tool','m_backpack','m_tether','m_contact','m_interaction'])]:
 for ident in ids:
  old=next(x for x in D[o]['anchors'] if x[0]==ident);path=old[1]
  source=next((x['after'] for x in D[o]['text_corrections'] if x['pointer']==path),None)
  if source is None:
   source=P['records'][o-5950]['after_existing5B']
   for part in path[1:].split('/'):source=source[int(part)] if isinstance(source,list) else source[part]
  anchor(o,ident,source)
for o,a in D.items():
 units={}
 for fid,path,key,q in a['anchors']:units.setdefault(path,[]).append(fid)
 a['units']=units;a['effects']=sorted({(v[0],v[1],v[2]) for v in a['claims'].values() if v[3]=='effect'})
with p.open('w') as f:
 f.write('"""Explicit manually authored native meaning/fact cells; final manual audit applied."""\nD={}\n')
 for o,a in D.items():f.write('D['+str(o)+']='+repr(a)+'\n')
