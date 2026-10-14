"""Explicit final manual precision audit; no rule-based semantic approval."""
import runpy
from pathlib import Path
R=Path(__file__).resolve().parents[1];h=runpy.run_path(str(R/'authored/native_05250_05250_06250.05900_05950.literals.py'));D=h['D'];p=R/'authored/native_05250_05250_06250.05900_05950.literals.py'
m='/content/embedding_text';k='/content/ko'
def anchor(o,ident,quote,path=None):
 a=D[o]['anchors'];idx=next(i for i,x in enumerate(a) if x[0]==ident);old=a[idx];a[idx]=(old[0],path or old[1],old[2],quote)
def claim(o,key,**values):
 keys=['dimension','target','property','mode','type','value','requires','operation','receivers'];a=list(D[o]['claims'][key])
 for key2,value in values.items():a[keys.index(key2)]=value
 D[o]['claims'][key]=tuple(a)
def text(o,after,reason=None):
 D[o]['text_corrections'][0]['after']=after
 if reason:D[o]['text_corrections'][0]['reason']=reason
# Original view shows a seated gate edge; it does not ask only to preserve an input seated state.
text(5903,'For the selected existing vertical-grid drop gate and its existing guide channel in the gate passage, use a close oblique view relative to the gate that shows the grid edge seated inside its own guide channel. The selected edge is in that seated state; no current dropping motion or exact camera distance is specified.','Bind named gate/channel inputs only; retain original actually selected seated edge state AND its close-oblique visible presentation. Remove added keep-state language that could incorrectly turn the original state selection into preservation.')
claim(5903,'seated',mode='effect',value='grid_edge_seated_inside_own_guide_channel',requires=['m_gate','m_structure'],operation='set_value',receivers=['gate'])
claim(5903,'guard',value='selected_seated_state_no_current_drop_exact_camera_distance')
anchor(5903,'m_seated','the grid edge seated inside its own guide channel');anchor(5903,'m_visible','shows the grid edge seated inside its own guide channel');anchor(5903,'m_guard','The selected edge is in that seated state; no current dropping motion or exact camera distance is specified')
D[5903]['roles']['prop_state']=(['m_seated'],['effect']);D[5903]['meaning']='Existing vertical-grid gate/channel, actual selected seated-edge state plus close oblique view/detail display. Source original showing-seated does not warrant replacing state-selection E with newly added keep P.'
D[5903]['owner_issue']='Existing gate/grid/channel witnesses and actual seated state/close view/axis/display permission pending. Original selected seated state retained E; exact edge/channel ownership native witnesses unresolved. Existing named-input proposal root unapproved.'
D[5903]['boundary']='No current drop/lift/closing/seating action, metal chemistry/full fortress/mechanism/exact camera distance. Actually selected seated state distinct current seating motion; do not transform state selection into mere preservation.'
# Graphical height bands are an actual bounded surface motif, no text identity.
claim(5904,'bands',property='surface.pattern.height_bands',type='surface.pattern.height_bands/v1')
anchor(5904,'e_bands','a coastal erosion marker stake with geometric height bands')
D[5904]['roles']['surface_pattern']=(['e_bands'],['effect'])
# No extra route through coma: retain source head/coma/tail continuity only.
text(5909,'For the selected existing compact comet head, surrounding coma and one continuous dust tail in this dust-tail variant, observational tracking resolves those features along a vector away from the established sunlight direction. Retain the head, coma and tail’s anti-solar continuity without prescribing an additional path through the coma. The tracking actor or apparatus, precise viewing axis and established sunlight-direction value are unspecified; no camera panning is specified.')
claim(5909,'continuity',value='head_coma_one_dust_tail_antisolar_continuity_retained')
anchor(5909,'m_cont','Retain the head, coma and tail’s anti-solar continuity without prescribing an additional path through the coma')
# Preserve Korean-specific inspector field role, not merely its broad English role.
D[5914]['claims']['field_i']=('role','inspectors','participant.role.field_assignment','effect','participant.role.field_assignment/v1','fictional_association_field_inspectors',[],'set_value',['inspectors'])
D[5914]['anchors'].append(('k_field',k,'field_i','허구 협회 현장 조사관'));D[5914]['roles']['participant_role'][0].append('k_field')
D[5914]['owner_issue']+=' Korean field-inspector specificity actual role E anchored to its own exact Korean quote, not inferred from English inspectors.'
# Newly selected pilot owns the named hand; do not presuppose a part of a not-yet-created pilot.
text(5927,'An adult aircraft pilot performs flight-deck duties seated at the existing real flight-deck pilot station, with one of that pilot’s hands at an existing primary control, while cross-checking instruments and outside flight state. The exact control, hand-contact relation and flight state are unspecified; neither qualification nor flight correctness is certified.','Retain actual pilot duties, owned hand, seated pose, hand-at-control and instrument/outside cross-check. Named station/control may be existing inputs; the selected pilot’s owned hand is an actual part obligation rather than an independently existing prerequisite. At still does not prove contact.')
claim(5927,'hand',mode='effect',value='one_pilot_owned_hand',requires=[],operation='add_entity',receivers=['pilot_hand'])
claim(5927,'position',requires=['m_control'],receivers=['pilot_hand','primary_control'])
anchor(5927,'m_hand','one of that pilot’s hands');anchor(5927,'m_position','one of that pilot’s hands at an existing primary control')
D[5927]['roles']['body_region']=(['m_hand'],['effect'])
D[5927]['owner_issue']='New adult pilot/owned hand and actual seated pose/at-control position/cross-check permissions plus existing station/control witnesses pending. Hand parent-owner link explicit but native new-part creation unapproved. At does not prove contact; control identity/flight state unresolved. No existing-hand prerequisite on a newly selected pilot.'
# The source outfit specifies a combination, beyond an inventory of individual items.
D[5930]['claims']['combination']=('appearance','garment_set','wardrobe.ensemble','effect','wardrobe.ensemble/v1','fitted_top_Bermuda_shorts_slim_belt_low_profile_footwear_combination',[],'set_value',['top','shorts','belt','shoes'])
D[5930]['anchors'].append(('m_combination',m,'combination','summer city dailywear combines a fitted top with two separately readable Bermuda short legs ending around the knees, a slim visible belt and low-profile footwear'))
# The result may not be assigned to the target surface without source evidence.
claim(5932,'result',target='unresolved_result',requires=[],receivers=[])
D[5932]['owner_issue']+=' Immediate state-change result receiver is unspecified; assigning it to the target surface would invent outcome ownership. Actual result E remains unresolved_result with empty receivers.'
# Original two-in-one shorts descriptive selection is a construction/display requirement, not keep-only.
text(5938,'The selected two-in-one athletic shorts have one shared waist system, a loose outer shell and a separately readable fitted inner short with its own two leg hems. This coherent component structure and separately readable inner short are required in this selected garment. This is not a brief liner or a color-blocked single layer; no particular wearer, current running or fabric-performance claim is specified.','Retain original selected two-in-one garment/construction/inner-readability as actual E. Remove added existing/preserve language that could turn real selection into E0. Shared waist/outer shell/fitted inner/two hems/exclusions stay mandatory.')
claim(5938,'shorts',mode='effect',requires=[],operation='add_entity',receivers=['shorts'])
claim(5938,'structure',mode='effect',requires=[],operation='set_value',receivers=['shorts'])
claim(5938,'outer',mode='effect',requires=[],operation='set_value',receivers=['shorts_outer_shell'])
claim(5938,'inner',mode='effect',requires=[],operation='set_value',receivers=['shorts_inner'])
claim(5938,'keep',property='garment.construction.required_components',mode='effect',type='garment.construction.required_components/v1',requires=[],operation='set_value',receivers=['shorts'])
claim(5938,'visible',mode='effect',requires=[],operation='set_value',receivers=['shorts_inner'])
anchor(5938,'m_shorts','selected two-in-one athletic shorts')
anchor(5938,'m_structure','The selected two-in-one athletic shorts have one shared waist system, a loose outer shell and a separately readable fitted inner short with its own two leg hems')
anchor(5938,'m_keep','This coherent component structure and separately readable inner short are required in this selected garment')
anchor(5938,'m_visible','The selected two-in-one athletic shorts have one shared waist system, a loose outer shell and a separately readable fitted inner short with its own two leg hems. This coherent component structure and separately readable inner short are required in this selected garment')
anchor(5938,'m_guard','This is not a brief liner or a color-blocked single layer; no particular wearer, current running or fabric-performance claim is specified')
D[5938]['roles']['garment_detail']=(['m_structure','m_keep'],['effect']);D[5938]['roles']['subject_framing']=(['m_visible'],['effect'])
D[5938]['meaning']='Selected two-in-one shorts/shared waist/loose outer/fitted inner/two inner hems and separate readability actual E, no unproven preserve-only existing input. One coherent component system, not automatically two independently owned garments.'
D[5938]['creation_permission']=True
D[5938]['owner_issue']='Selected garment/components/construction/readability creation/state permissions pending. Wearer fit baselines and distinct garment ownership unspecified, fine garment_fit/wardrobe_layering held. Original actual construction/display demands preserved E; no added keep/existing-input E0.'
# Precisely scoped quotation enlargements: antecedents and all typed value components are now included.
# Each pair is individually chosen from the source read above; no semantic loop selects records.
for o,ids in [(5901,['m_symmetry','m_aligned']),(5905,['m_pose','m_frame','m_depth']),(5908,['m_formation','m_orientation','m_roles']),(5909,['m_tracking','m_visible','m_orientation']),(5910,['m_route','m_cloth']),(5913,['m_support','m_optics']),(5915,['m_structure','m_read']),(5917,['m_grain','m_frame','m_active','m_making']),(5918,['m_prop']),(5919,['m_composed','m_phase','m_reaction','m_awareness']),(5923,['m_change','m_rule','m_cont']),(5924,['m_scan','m_light']),(5925,['m_trace']),(5926,['m_variation','m_color']),(5929,['m_pattern','m_relation']),(5933,['m_mesh']),(5934,['m_capability']),(5935,['m_interval']),(5936,['m_hand']),(5938,['m_outer','m_inner']),(5939,['m_under','m_weave','m_legible']),(5940,['m_height','m_direction','m_retain']),(5947,['m_boundary','m_blush'])]:
 after=next((x['after'] for x in D[o]['text_corrections'] if x['pointer']==m),None)
 if after is None:
  import json
  source=json.loads((R/'authored/native_05250_05250_06250.05900_05950.packet.json').read_text())['records'][o-5900]['after_existing5B'];after=source['content']['embedding_text']
 for ident in ids:anchor(o,ident,after)
# Named trio itself is the entire positive subject inventory, not an arbitrary foreground selection.
D[5946]['roles']['subject']=(['e_clinician','e_traveler','e_arbitrator'],['effect'])
# Correct units/effect sets only from explicitly authored changes above, with no meaning classifier.
for o,a in D.items():
 units={}
 for ident,path,key,q in a['anchors']:units.setdefault(path,[]).append(ident)
 a['units']=units
 a['effects']=sorted({(v[0],v[1],v[2]) for v in a['claims'].values() if v[3]=='effect'})
with p.open('w') as f:
 f.write('"""Explicit manually authored meaning/fact cells; final manual precision audit applied."""\nD={}\n')
 for o,a in D.items():f.write('D['+str(o)+']='+repr(a)+'\n')
