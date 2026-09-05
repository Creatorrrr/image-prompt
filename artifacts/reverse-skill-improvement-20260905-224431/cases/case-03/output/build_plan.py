from pathlib import Path
import json,hashlib,datetime,sys
ROOT=Path(__file__).resolve().parent
ROUTE=json.loads((ROOT/'route.json').read_text())
C={'mode':'appearance-led','perceptual_proposition':'Close low-angle photographic adult figure in an asymmetric fitted top, in front of an oversized softer illustration.','invariants':[],'flexible_dimensions':[],'major_regions':[],'component_relations':[],'placement_closures':[],'candidate_claims':[],'aggregate_effects':[],'emitted_controls':[],'prior_clusters':[]}
P={'schema_version':'reverse-image-salience-plan/v1','direct_appeal_read':'The image is dominated by upward perspective and a large dark-clad foreground silhouette against an enlarged drawn face. No attractiveness or personality judgment is used.','routing':{'analysis_profile':'audited','route_fingerprint':ROUTE['route_fingerprint'],'resolved_non_core_modules':[x for x in ROUTE['resolved_modules'] if not x.startswith('core.') and x!='concept.primary-relationship']},'source_sha256':'a3e2b2dcf5d8aa7b8d78e564452f48c60e579db1282e090bd3dcaa9015e83aa9','render_contract':C}
ordered=[]
def region(id,role,area,attention,evidence,anchor=None):
 d={'id':id,'role':role,'relative_area':area,'attention':attention,'source_evidence':[evidence]}
 if anchor:d['prompt_anchor']=anchor
 C['major_regions'].append(d)
def relation(id,kind,subject,reference,observation,role='primary',frame=False,**kw):
 d={'id':id,'kind':kind,'subject_region_id':subject,'observation':observation,'role':role,'source_evidence':[observation],**kw}
 d['frame_reference' if frame else 'reference_region_id']=reference;C['component_relations'].append(d);return id

def add(id,text,axis,owner,origin,regions,evidence,role='primary',strength='moderate',rels=None,kind='generic',color_axis=None,layer=None,light_axis=None,ref=None):
 inv={'id':id,'axis':axis,'role':role,'observation':evidence,'causal_origin':origin,'target_strength':strength,'source_evidence':[evidence],'clause_owner':owner,'source_obligation_ids':[]}
 claim={'id':'claim-'+id,'semantic_slot':id,'owner':owner,'role':role,'polarity':'affirmative','target_strength':strength,'source_kind':'visible-evidence','source_evidence':[evidence],'emit':True}
 effect={'id':'effect-'+id,'direction':evidence,'role':role,'target_strength':strength,'claim_ids':[claim['id']],'source_supported':True,'source_evidence':[evidence]}
 control={'id':'control-'+id,'prompt_excerpt':text,'claim_id':claim['id'],'aggregate_effect_ids':[effect['id']]}
 if kind=='generic':
  effect.update(axis=axis,region_ids=regions,relation_ids=rels or [])
  claim['salience_effects']=[{'aggregate_effect_id':effect['id'],'source_evidence':[evidence]}];control['owner']=owner
  C['aggregate_effects'].append(effect);C['emitted_controls'].append(control)
 elif kind=='color':
  effect.update(axis=color_axis,region_id=regions[0]);claim['perceptual_effects']=[{'aggregate_effect_id':effect['id'],'causal_layer':layer,'confidence':'medium','source_evidence':[evidence]}]
  control.update(causal_layer=layer,control_role='axis-control',region_id=regions[0],axis=color_axis)
  CT['aggregate_effects'].append(effect);CT['claim_ids'].append(claim['id']);CT['emitted_controls'].append(control)
 elif kind=='light':
  effect.update(axis=light_axis,region_id=regions[0]);control['owner']=light_axis
  if ref:effect['reference_region_id']=ref
  claim['lighting_effects']=[{'aggregate_effect_id':effect['id'],'confidence':'medium','source_evidence':[evidence]}]
  LF['aggregate_effects'].append(effect);LF['claim_ids'].append(claim['id']);LF['emitted_controls'].append(control)
 C['invariants'].append(inv);C['candidate_claims'].append(claim);ordered.append(control)
 return inv,claim,effect,control

# Source-derived clauses and the audited ledgers are filled below after the lane wave.
region('person','dominant','large','primary','One photographic adult person spans most of the frame.')
region('head','dominant','small','primary','Head is high near center, whole crown and facial features visible.')
region('torso','dominant','large','secondary','Large curved upper torso occupies most of the lower field.')
region('garment','dominant','large','secondary','The opaque fitted top dominates the lower field.')
region('hair','supporting','large','secondary','Long straight hair surrounds face and falls along torso.')
region('shoulder','supporting','medium','secondary','Broad bare viewer-right shoulder lies near right edge.','exposed shoulder')
region('illustration','low-legibility','large','background','Enormous drawn face and hair surround the foreground silhouette.')
relation('r-person-frame','frame-zone','person','image frame','The full crown and face are high near center; torso fills lower frame.',frame=True,placement_axes=['frame-position','frame-share'])
relation('r-crop','partial-visibility','person','image frame','Lower crop ends at the shirt hem with only a narrow midriff and lower garment fragment.',frame=True,visible_fragments=['Full crown and face','Torso and top hem','Thin midriff strip'],hidden_or_cropped=['Hands','Legs','Lower body'],completion_risk='high')
relation('r-arm-edge','edge-contact','person','right image edge','Viewer-right sleeve and arm exit through the right frame edge.',frame=True,edge_contacts=['right'])
relation('r-low','viewpoint','person','viewer position','View looks strongly upward at nose and chin underplanes.',frame=True)
relation('r-near','viewpoint','person','viewer position','Near torso is broad below the more distant head.',frame=True)
relation('r-chin','part-whole-orientation','person','torso','Head is lifted with extended front neck.')
relation('r-head-yaw','part-whole-orientation','person','torso','Face turns mildly viewer-left relative to chest projection.')
relation('r-shoulder','part-whole-orientation','person','torso','Shoulder image line rises toward viewer-right.')
relation('r-gaze','attention-direction','person','low viewing position','Eyes aim down toward camera.',frame=True)
relation('r-illustration-frame','frame-zone','illustration','image frame','Giant illustrated head is cropped by top edge; illustration fills exposed background.',frame=True,placement_axes=['frame-position','frame-share'])
relation('r-overlap','overlap','person','illustration','Photographic head, hair and torso occlude the illustrated center, with broad side fragments.',placement_axes=['overlap','visibility-budget'])
relation('r-direction','cross-component-orientation','person','illustration','Illustrated smiling mouth remains above and viewer-left of foreground head.',placement_axes=['direction','overlap','visibility-budget'],degenerate_satisfaction_risk='high',degeneracy_rationale='Above-left can remain true after the giant face is displaced almost out of frame.',placement_closure_id='closure-illustration')
relation('r-garment','partial-visibility','garment','person','A low asymmetric neckline exposes viewer-right shoulder while sleeves cover arms.',visible_fragments=['Bare viewer-right shoulder','Sleeves and top hem','Diagonal band'],hidden_or_cropped=['Hidden garment behind long hair','Lower outfit'],completion_risk='high')
relation('r-band','overlap','garment','person','Separate diagonal band passes over upper chest above the low neckline.')
relation('r-contour','contact','garment','torso','The fitted opaque fabric follows the broad curved chest and narrower lower torso.')
C['placement_closures']=[{'id':'closure-illustration','subject_region_id':'person','reference_region_id':'illustration','subject_frame_relation_id':'r-person-frame','reference_frame_relation_id':'r-illustration-frame','inter_region_relation_ids':['r-direction','r-overlap'],'protected_axes':['frame-position','frame-share','direction','overlap','visibility-budget'],'degenerate_satisfaction_check':{'tested_change':'Move the illustrated face far upward-left while preserving direction alone.','held_fixed_axes':['direction'],'changed_axes':['overlap','visibility-budget'],'verdict':'material-drift','source_evidence':['The giant smiling mouth is close above-left of the crown; drawn hair and garment remain broad beside the person.']}}]
add('medium','A vertical photographic portrait of one adult woman against an enormous flat anime-style illustration.','surface','concept.primary-relationship','processing',['person','illustration'],'Photographic foreground and flat drawn backdrop are visibly different media.',strength='strong')
add('aspect','Use a portrait frame close to 3:4.','hierarchy','core.frame-coordinates','layout',['person'],'Source dimensions 969 by 1280 give a near-3:4 portrait frame.',strength='strong')
add('view-low','The camera looks strongly upward from below her face, showing the underside of her nose and chin.','form','core.frame-coordinates','perspective',['person'],'Nose and chin underplanes are exposed above the viewing position.',strength='strong',rels=['r-low'])
add('view-near','At this close distance, the clothed torso projects much wider than the smaller, more distant head.','form','core.frame-coordinates','perspective',['person','torso','head'],'Near torso is broad beneath the smaller high head.',strength='strong',rels=['r-near'])
add('placement','Her complete crown and face sit high near the center, with a small strip of illustrated backdrop above her hair and her torso filling most of the lower image.','hierarchy','core.frame-coordinates','layout',['person','head','torso'],'Full head and shallow headroom remain over the large torso.',strength='strong',rels=['r-person-frame'])
add('crop','The lower crop ends just below the top hem, showing only a narrow midriff strip and a sliver of the lower waistband.','hierarchy','core.frame-coordinates','layout',['person'],'Source cuts just beneath the top with narrow skin and lower-clothing fragments.',rels=['r-crop'])
add('arm-crop','Her viewer-right sleeve and upper arm cross the right edge; both hands and the legs are outside the frame.','topology','core.frame-coordinates','layout',['person'],'Right sleeve intersects edge; no hands or legs are visible.',rels=['r-arm-edge','r-crop'])
add('chin','Her chin is lifted and the front of her neck is extended above the chest.','form','subject.human','pose-deformation',['person'],'Chin lift and extended neck remain material with viewpoint held.',rels=['r-chin'])
add('head-yaw','Her face turns a little toward viewer-left relative to the chest.','form','subject.human','pose-deformation',['person'],'Nose and face project mildly viewer-left relative to chest.',rels=['r-head-yaw'])
add('shoulder-slope','The shoulder line rises toward viewer-right.','form','subject.human','pose-deformation',['person'],'Viewer-right shoulder is higher in the image.',rels=['r-shoulder'])
add('gaze','Her eyes look downward toward the low camera.','form','subject.human','pose-deformation',['person'],'The eyes look down toward the low viewing position.',rels=['r-gaze'])
add('overlap','Her head, hair and torso hide the center of the illustration; its giant smiling mouth is visible above and to viewer-left of her head, with broad drawn hair and clothing fragments surviving beside her silhouette.','topology','concept.mixed-media-illusion','spatial-relation',['person','illustration'],'Foreground silhouette occludes the giant illustrated figure while mouth and broad side fragments survive.',strength='strong',rels=['r-overlap','r-direction','r-person-frame'])
add('illustration-scale','The illustrated head is much larger than her head and is cut off by the top edge; the illustration fills the entire exposed background.','hierarchy','core.frame-coordinates','layout',['illustration'],'The large illustrated head extends beyond the frame.',rels=['r-illustration-frame'])
add('face','Her oval face narrows through the jaw to a tapered chin, with elongated eyes, pronounced upper eyeliner, a narrow projecting nose and softly parted full lips.','form','detail.human-face-likeness','intrinsic',['head'],'Oval tapered facial outline, elongated lined eyes, narrow nose and full separated lips are readable.',role='supporting')
add('hair-form','Dense blunt bangs cover the forehead while leaving the eyes visible; long straight hair falls along both cheeks and down both sides of the torso to the low crop.','form','subject.human','intrinsic',['hair','head','torso'],'Blunt fringe and long straight side masses delimit face and torso.',role='supporting')
add('body-contour','The fitted opaque long-sleeve top follows a broad rounded chest contour that narrows toward the lower torso.','form','detail.human-body-form','material-interaction',['torso','garment'],'The fitted fabric follows a broad curved chest above a narrower lower torso; perspective remains separately owned.',rels=['r-contour'])
add('garment-coverage','Its low asymmetric neckline leaves the viewer-right shoulder bare while the sleeve stays around the upper arm.','topology','detail.clothing-fashion','material-interaction',['person','garment'],'Distinct bare shoulder, low neckline and sleeve boundary are visible.',rels=['r-garment'])
add('band','A separate diagonal band crosses the upper chest toward the base of the neck, leaving a triangular opening between the band and the lower neckline.','topology','detail.clothing-fashion','material-interaction',['person','garment'],'A separate diagonal band and low neckline bound an exposed triangular opening.',rels=['r-band'])
LF={'importance':'primary','observation_scope':'source-visible','observed_result':{'global_tonal_range':'Bright face/shoulder against very dark hair and top; exact exposure unknown.','local_form_contrast':'moderate','bright_plane_coverage':'mixed','gradient_character':'Broad gentle garment gradient with more distinct face-to-neck transition.','gradient_extent':'mixed','background_spill_relation':'uncertain','largest_bright_masses':['Face','Exposed shoulder','Illustrated pale face and garment'],'largest_dark_masses':['Hair lengths','Lower shirt'],'source_evidence':['Face planes, bare shoulder and crown catch illumination while jaw/neck and lower garment are shaded.']},'source_hypothesis':{'model_type':'uncertain','source_count':'uncertain','camera_axis_offset':'uncertain','elevation':'uncertain','front_side_back_relation':'Multiple rigs could reproduce the visible pattern.','apparent_angular_size':'uncertain','fill_structure':'uncertain','confidence':'low','actuation':'result-space-only','source_evidence':['A single image exposes only the visible light distribution.']},'regions':[{'id':'face-plane','parent_region_id':'head','prompt_anchor':'nose and cheek planes','role':'major-plane','source_evidence':['Nose and cheeks catch light.']},{'id':'neck-shadow','parent_region_id':'person','prompt_anchor':'jaw underside and neck','role':'shadow-zone','source_evidence':['Jaw underside transitions into neck shadow.']}],'region_effects':[],'shadow_events':[{'id':'jaw-shadow','region_id':'neck-shadow','owner':'mixed','footprint':'Under jaw across front/side neck','edge_character':'Defined but softened transition','confidence':'medium','source_evidence':['Jaw and neck are darker than nose and cheek planes.']},{'id':'brow-shadow','region_id':'head','owner':'cast','footprint':'Brow and upper eye region under bangs','edge_character':'Soft dark band','confidence':'medium','source_evidence':['Bangs border a shaded brow/eye area.']}],'material_responses':[{'region_id':'hair','response':'glossy','highlight_width':'Narrow streaks on crown strands','highlight_strength':'Distinct on crown only','black_level_behavior':'Side lengths stay dark','source_evidence':['Crown has streaked sheen over dark lengths.']},{'region_id':'garment','response':'mixed','highlight_width':'Broad upper-chest gradient','highlight_strength':'Subtle','black_level_behavior':'Lower shirt stays dark','source_evidence':['Upper fabric curves carry gentle gradients, lower cloth low detail.']}],'pose_light_dependency':{'geometry_dependency':'pose-bound','preserved_result':'Raised head exposes jaw underside and neck transition under the brighter face planes.','flexible_effects':[],'source_evidence':['Visible underplanes depend on raised chin and low camera.']},'claim_ids':[],'aggregate_effects':[],'emitted_controls':[]}
C['light_form_contract']=LF
add('face-neck-light','The nose and cheek planes are more illuminated than the jaw underside and neck.','light-to-form','detail.light-form-fidelity','lighting-shadow',['face-plane'],'Face planes stand above darker jaw and neck in the displayed light pattern.',kind='light',light_axis='local-form-contrast',ref='neck-shadow')
add('shoulder-light','The exposed shoulder forms one broad illuminated plane.','light-to-form','detail.light-form-fidelity','lighting-shadow',['shoulder'],'Bare shoulder is a broad continuous bright plane.',kind='light',light_axis='bright-plane-coverage')
add('brow-shadow','The bangs shade the eye area without hiding the eyes.','light-to-form','detail.light-form-fidelity','lighting-shadow',['head'],'Bangs shade the brow and upper eye region.',role='primary',kind='light',light_axis='shadow-topology')
add('hair-sheen','Narrow sheen streaks pick out strands at the hair crown, while the side lengths read as a dark mass.','light-to-form','detail.light-form-fidelity','material-interaction',['hair'],'Crown streaks articulate hair more than the dark side lengths.',role='supporting',kind='light',light_axis='material-response')
add('shirt-gradient','The shirt has a broad shallow shading gradient across the curved upper chest.','light-to-form','detail.light-form-fidelity','lighting-shadow',['garment'],'Upper chest has a broad shallow gradient over fabric curve.',role='supporting',kind='light',light_axis='gradient-extent')
for id,reg,ref,role,obs in [('face-neck-light','face-plane','neck-shadow','gradient','Nose and cheek planes brighter than jaw underside and neck.'),('shoulder-light','shoulder',None,'broad-plane','Exposed shoulder forms broad light plane.'),('brow-shadow','head',None,'shadow','Bangs shade eye area.'),('hair-sheen','hair',None,'highlight','Narrow crown streaks over dark lengths.'),('shirt-gradient','garment',None,'gradient','Broad shallow chest shading gradient.')]:
 e={'id':'observed-'+id,'region_id':reg,'role':role,'value_relation':obs,'gradient_strength':'moderate','edge_character':'Softly resolved','source_evidence':[obs]}
 if ref:e['reference_region_id']=ref
 LF['region_effects'].append(e)
CT={'importance':'primary','observation_scope':'source-visible','global':{'cast_or_palette_shift':'Uncertain; regional warm skin and muted pink backdrop do not establish a global white balance.','exposure_behavior':'Uneven displayed brightness with dark lower shirt.','contrast_and_tone_curve':'Bright face and shoulder over deep black masses.','processing_shift':'Modest detail softness; exact pipeline unknown.','source_evidence':['Dark hair and clothing coexist with light face and shoulder and muted background.']},'regions':[],'neutral_anchor_status':'uncertain','neutral_anchors':[],'uncertainty_note':'No calibrated neutral or scene-referred reference exists. Displayed image targets only.','displayed_tone_response':[],'claim_ids':[],'aggregate_effects':[],'emitted_controls':[]}
C['color_tone_contract']=CT
color_specs=[
('hair-value','Her hair is near-black in value.','hair','value','intrinsic','Near-black displayed hair value.','primary'),
('hair-chroma','The hair has very little visible chroma.','hair','chroma','intrinsic','Very low displayed hair chroma.','primary'),
('shirt-value','The top is near-black in value.','garment','value','intrinsic','Near-black displayed garment value.','primary'),
('shirt-chroma','The top has very little visible chroma.','garment','chroma','intrinsic','Very low displayed garment chroma.','primary'),
('skin-value','Her exposed skin is light in displayed value.','skin','value','intrinsic','Exposed skin midtone is light relative to hair and top.','supporting'),
('skin-chroma','The exposed skin has subdued chroma.','skin','chroma','intrinsic','Exposed skin midtone chroma is subdued.','supporting'),
('skin-hue','The exposed skin midtones are warm beige.','skin','hue','intrinsic','Exposed skin has warm beige midtones under captured illumination.','supporting'),
('lip-hue','The lips are a subdued rose.','lips','hue','intrinsic','Lips display subdued rose hue.','supporting'),
('poster-hue','The illustrated hair is dusty pink-mauve.','illustrated-hair','hue','intrinsic','Illustrated hair is dusty pink-mauve.','supporting'),
('poster-chroma','The illustrated hair remains muted in chroma.','illustrated-hair','chroma','intrinsic','Illustrated hair is muted rather than saturated.','supporting'),
('gray-value','The illustrated clothing is pale.','illustrated-clothing','value','intrinsic','Pale displayed illustrated garment.','supporting'),
('gray-chroma','The illustrated clothing is nearly achromatic gray.','illustrated-clothing','chroma','intrinsic','Low chroma illustrated garment reads gray.','supporting'),
('shirt-floor','The lower shirt stays deep in shadow, with only faint fold detail.','lower-shirt','shadow-floor','processing','Deep lower-shirt floor preserves only faint folds.','supporting'),
('skin-rolloff','Highlights on the exposed skin retain tonal modeling without flat white clipping.','skin','highlight-rolloff','exposure','Skin highlights retain gradation rather than appearing flat white.','supporting')]
for id,txt,reg,ax,layer,ev,role in color_specs:
 add(id,txt,'color','detail.color-tone-fidelity','intrinsic' if layer=='intrinsic' else 'processing',[reg],ev,role=role,kind='color',color_axis=ax,layer=layer)
anchors={'hair':'hair','garment':'top','skin':'exposed skin','lips':'lips','illustrated-hair':'illustrated hair','illustrated-clothing':'illustrated clothing','lower-shirt':'lower shirt'}
for reg,anchor in anchors.items():
 spec={'id':reg,'role':'dominant' if reg in {'hair','garment'} else 'supporting','prompt_anchor':anchor,'source_evidence':[next(ev for _,_,rr,_,_,ev,_ in color_specs if rr==reg)],'intrinsic_axes':[],'tone_zones':[{'zone':'midtone','observation':'Displayed region midtone is considered independently from highlight and shadow response.','confidence':'medium','source_evidence':[next(ev for _,_,rr,_,_,ev,_ in color_specs if rr==reg)]}],'relative_relations':['Hair and top are much darker than exposed skin and illustrated clothing.']}
 for ax in ['value','chroma','hue']:
  found=next((row for row in color_specs if row[2]==reg and row[3]==ax),None)
  ar={'axis':ax,'observation':found[5] if found else 'No separate reliable or material intrinsic '+ax+' target is emitted.','confidence':'medium' if found else 'low','source_evidence':spec['source_evidence'],'role':found[6] if found else 'supporting','evidence_scope':'midtone','emission':'required' if found else 'diagnostic-only'}
  if found:ar['aggregate_effect_id']='effect-'+found[0]
  else:ar['non_emission_reason']='Low chroma, shadows or subordinate region scale do not support an independent '+ax+' direction.'
  spec['intrinsic_axes'].append(ar)
 CT['regions'].append(spec)
for id,reg,ax,clas in [('shirt-floor','lower-shirt','shadow-floor','deep'),('skin-rolloff','skin','highlight-rolloff','gradual-unclipped')]:
 ev=next(row[5] for row in color_specs if row[0]==id)
 CT['displayed_tone_response'].append({'region_id':reg,'axis':ax,'class':clas,'role':'supporting','confidence':'medium','source_evidence':[ev],'tone_scope':{'kind':'region','affected_region_ids':[reg],'protected_region_ids':['skin'] if reg=='lower-shirt' else ['lower-shirt'],'prompt_anchor':anchors[reg],'source_evidence':[ev]},'emission':'required','aggregate_effect_id':'effect-'+id})
add('capture','Keep modest photographic fine-detail softness and softly resolved skin texture, without a glossy wet skin finish; the illustrated backdrop is softer and less detailed than the foreground person.','sharpness','medium.photographic-capture','processing',['person','illustration'],'Foreground fine detail is softly resolved and illustration has softer lower legibility.',role='supporting')
# A single capture clause owns both the sharpness result and its displayed texture consequence.
capclaim=next(x for x in C['candidate_claims'] if x['id']=='claim-capture')
capeff={'id':'effect-skin-texture','axis':'surface','direction':'Softly resolved displayed skin texture, without inferred retouching.','role':'supporting','target_strength':'moderate','claim_ids':['claim-capture'],'source_supported':True,'source_evidence':['Skin detail is smooth and softly resolved.'],'region_ids':['person'],'relation_ids':[]}
C['aggregate_effects'].append(capeff);capclaim['salience_effects'].append({'aggregate_effect_id':capeff['id'],'source_evidence':capeff['source_evidence']});next(x for x in C['emitted_controls'] if x['id']=='control-capture')['aggregate_effect_ids'].append(capeff['id'])
add('minor-details','Keep a tiny pale NOIR mark near the lower viewer-right shirt hem and narrow black strips along the far left and right image edges.','information','core.fidelity-discipline','processing',['garment','illustration'],'Tiny pale NOIR lettering and narrow near-black outer strips are visible but secondary.',role='supporting',strength='subtle')
# Incidental lettering and border strips are intentionally omitted at P3, as the global and capture lane counterfactuals allow.
for field in ['invariants','candidate_claims','aggregate_effects','emitted_controls']:
 C[field]=[x for x in C[field] if x.get('id') not in {'minor-details','claim-minor-details','effect-minor-details','control-minor-details'}]
ordered[:]=[x for x in ordered if x['id']!='control-minor-details']
next(x for x in C['emitted_controls'] if x['id']=='control-medium')['prompt_excerpt']='A photographic portrait of one adult woman against an enormous flat anime-style illustration.'
next(x for x in CT['emitted_controls'] if x['id']=='control-lip-hue')['prompt_excerpt']='The lips have a rose hue.'
add('lip-chroma','The lip color is muted.','color','detail.color-tone-fidelity','intrinsic',['lips'],'Lips are rose with subdued displayed chroma.',role='supporting',kind='color',color_axis='chroma',layer='intrinsic')
for rr in CT['regions']:
 if rr['id']=='lips':
  ar=next(x for x in rr['intrinsic_axes'] if x['axis']=='chroma');ar.update(observation='Subdued displayed lip chroma.',confidence='medium',emission='required',aggregate_effect_id='effect-lip-chroma');ar.pop('non_emission_reason',None)
# Place the supporting lip-chroma phrase beside its hue owner without changing the ledger bytes.
lipc=ordered.pop();pos=next(i for i,x in enumerate(ordered) if x['id']=='control-lip-hue');ordered.insert(pos+1,lipc)
# Explicit spatial ownership uses only visible results; unresolved physical axes are not normalized.
sys.path.insert(0,str(ROOT.parent/'skill-v3/tools'))
from salience_plan import SPATIAL_DIMENSION_FAMILIES,SPATIAL_DIMENSION_ALLOWED_ORIGINS,ORIENTATION_SPATIAL_DIMENSIONS,VIEWPOINT_SPATIAL_DIMENSIONS,HUMAN_POSE_GEOMETRY_DIMENSIONS,VALID_APPEARANCE_EFFECT_DIMENSIONS
spatial_report=json.loads((ROOT/'lane.spatial-topology.report.json').read_text())
S={'schema_version':'spatial-orientation/v6','subjects':[{'id':'person','kind':'human','visibility':'readable','region_id':'person','source_evidence':['Full head, torso and parts of both arms are visible.']}],'evidence_cues':[],'decisions':[],'counterfactual_checks':[],'coupled_effects':[],'prompt_effect_audits':[]}
paths={'frame-placement':('placement','r-person-frame'),'viewpoint-elevation':('view-low','r-low'),'viewpoint-distance-foreshortening':('view-near','r-near'),'human-head-body-pitch':('chin','r-chin'),'human-head-body-yaw':('head-yaw','r-head-yaw'),'human-shoulder-image-slope':('shoulder-slope','r-shoulder'),'human-attention-direction':('gaze','r-gaze'),'cross-component-orientation':('overlap','r-direction')}
for record in spatial_report['control_requirements']:
 dim=record['dimension'];disp=record['disposition'];obs=record['observation'];did='sp-'+dim;cid='cue-'+dim
 origin=next(iter(sorted(SPATIAL_DIMENSION_ALLOWED_ORIGINS[dim])))
 fam='perspective' if dim.startswith('viewpoint-') else 'attention' if dim=='human-attention-direction' else 'frame-placement' if dim=='frame-placement' else 'occlusion' if dim=='cross-component-orientation' else 'axis-relation'
 S['evidence_cues'].append({'id':cid,'subject_id':'person','family':fam,'observation':obs,'source_evidence':[obs],'confounders':['Projection, hair, clothing or absent body regions limit physical attribution.'] if disp=='uncertain' else []})
 d={'id':did,'subject_id':'person','dimension':dim,'family':SPATIAL_DIMENSION_FAMILIES[dim],'disposition':disp,'confidence':'low' if disp=='uncertain' else 'medium','causal_origin':origin,'observation':obs,'source_evidence':[obs],'evidence_cue_ids':[cid],'control_axis_id':'axis-'+dim}
 if disp=='invariant':
  iid,rid=paths[dim];inv=next(x for x in C['invariants'] if x['id']==iid);origin=inv['causal_origin'];d['causal_origin']=origin
  d.update(relation_id=rid,invariant_id=iid,claim_id='claim-'+iid,aggregate_effect_id='effect-'+iid,control_id='control-'+iid)
  for collection,key in [(C['aggregate_effects'],'effect-'+iid),(C['emitted_controls'],'control-'+iid)]:
   obj=next(x for x in collection if x['id']==key);obj.update(control_axis_id=d['control_axis_id'],causal_origin=origin)
 elif disp=='uncertain':
  d['visibility_limit']=obs;d['non_emission_reason']='No isolated physical target can be established from the visible projection; no normalization is emitted.'
 else:
  d['non_emission_reason']='Small lateral displacement is subordinate once crop and all neighboring material relations are held.'
  d['neutralization_test']={'test_scope':'single-dimension-with-adjacent-spatial-relations-held','tested_change':'Shift only the head a small horizontal amount; retain camera, high placement, chin lift, gaze and shoulder slope.','verdict':'preserved','preserved_relations':['Low-angle projection, complete head, large torso and illustrated overlap remain.'],'changed_relations':[],'held_fixed_decision_ids':['sp-frame-placement','sp-viewpoint-elevation','sp-viewpoint-distance-foreshortening','sp-human-head-body-pitch','sp-human-shoulder-image-slope'],'evidence_cue_ids':[cid],'confidence':'medium','source_evidence':[obs]}
 S['decisions'].append(d)
ids={x['dimension']:x['id'] for x in S['decisions']}
for scope in ['whole-orientation','residual-alignment']:
 whole=scope=='whole-orientation'
 S['counterfactual_checks'].append({'id':'cf-'+scope,'subject_id':'person','scope':scope,'tested_change':'Replace the low upward view and lifted head with an eye-level neutral portrait.' if whole else 'Hold all camera variables and crop; lower the chin and level the shoulder line.','verdict':'material','changed_relations':['Visible chin/nose underplanes, extended neck and shoulder image slope change.'],'preserved_relations':[],'neutralized_decision_ids':[ids[d] for d in sorted(ORIENTATION_SPATIAL_DIMENSIONS if whole else HUMAN_POSE_GEOMETRY_DIMENSIONS)],'held_fixed_decision_ids':[] if whole else [ids[d] for d in sorted(VIEWPOINT_SPATIAL_DIMENSIONS)],'evidence_cue_ids':['cue-viewpoint-elevation','cue-human-head-body-pitch','cue-human-shoulder-image-slope'],'source_evidence':['Nose/chin underplanes, extended neck and rising viewer-right shoulder are visible.']})
implicit={'view-low':['human-head-body-pitch'],'view-near':['frame-placement'],'placement':['viewpoint-distance-foreshortening'],'chin':['viewpoint-elevation'],'head-yaw':[],'shoulder-slope':[],'gaze':['viewpoint-elevation'],'overlap':['frame-placement']}
for d in S['decisions']:
 if d['disposition']!='invariant':continue
 iid=d['invariant_id'];ctl=next(x for x in C['emitted_controls'] if x['id']==d['control_id'])
 S['prompt_effect_audits'].append({'id':'audit-'+iid,'subject_id':'person','control_id':ctl['id'],'effect_scope':'explicit-and-implicit-spatial-effects','prompt_excerpt':ctl['prompt_excerpt'],'explicit_decision_ids':[d['id']],'implicit_decision_ids':[ids[z] for z in implicit.get(iid,[])],'verdict':'source-consistent','rationale':'Clause preserves the named visible projection or placement. It does not prescribe unresolved torso/camera rotations.','source_evidence':d['source_evidence']})
C['spatial_orientation_coverage']=S
C['literal_spatial_audit']=[{'control_id':x['id'],'prompt_excerpt':x['prompt_excerpt'],'status':'source-consistent','rationale':'Frame shape, crop, layer size, hair fall and garment boundaries are literal source-supported controls; no hidden support, completed anatomy or camera-normalization direction is added.','protected_uncertain_axes':[ids[d] for d in ['viewpoint-azimuth','viewpoint-roll','human-torso-yaw','human-torso-pitch','human-torso-roll','human-shoulder-depth-order']]} for x in C['emitted_controls'] if x['id'] in {'control-aspect','control-crop','control-arm-crop','control-illustration-scale','control-hair-form','control-garment-coverage','control-band'}]
C['human_appearance_decisions']=[{'id':'appearance-person','schema_version':'human-appearance/v3','subject_id':'person','face_visibility':'readable','frame_prominence':'primary','fidelity_salience':'supporting','appearance_invariant_ids':['face','hair-form','capture'],'source_evidence':['Readable oval face, blunt bangs, long hair and softly resolved skin.'],'identity_context':{'disposition':'absent','context_use':'none','prompt_disposition':'omit','viewer_priority':'not-material'},'person_prior':{'disposition':'uncertain','confidence':'medium','source_evidence':['Literal face and hair geometry are supported; generator response has not been calibrated.'],'candidate_support':'uncertain','default_drift_risk':'uncertain','local_geometry_sufficiency':'uncertain','geometry_claim_ids':['claim-face','claim-hair-form'],'non_emission_reason':'No extra broad face or demographic-looking prior has reliable source or response support.','omission_counterfactual':{'verdict':'uncertain','source_evidence':['Local geometry is visible but the ability of a broad prior to reduce default face drift is unmeasured.']},'residual_risk':'The model may still produce a generic face despite the literal geometry.'},'appearance_gestalt':{'disposition':'omit','scope':'person-aesthetic','confidence':'medium','candidate_support':'unsupported','viewer_priority':'not-material','default_drift_risk':'low','source_evidence':['Visible form, hair, expression, garment and camera controls state the image without evaluative personality or attractiveness wording.'],'decomposition_control_ids':[],'effect_budget':{'intended_dimensions':[],'protected_dimensions':sorted(VALID_APPEARANCE_EFFECT_DIMENSIONS),'source_evidence':['No aggregate appearance label is emitted; all literal controls have independent owners.']},'omission_counterfactual':{'verdict':'preserved','source_evidence':['Omitting an evaluative label leaves explicit shape, pose, hair and garment constraints intact.']},'non_emission_reason':'No evaluative broad person aesthetic is necessary to express the observable scene.'},'skin_surface':{'disposition':'material','viewer_priority':'P1','observation_scope':'source-visible','semantic_use':'displayed-surface','confidence':'medium','source_evidence':['Face, neck and bare shoulder show light subdued warm beige displayed skin.'],'region_ids':['skin'],'coverage':'exposed','descriptor_disposition':'omit','descriptor_non_emission_reason':'Literal value, chroma and hue are already separate; no friendly or composite skin label is emitted.'}}]
# Protect primary local lighting before overlapping tone controls.
for c in CT['emitted_controls']:
 if c['axis'] in {'value','contrast','displayed-key-level','shadow-floor','microcontrast'}:
  c['protected_light_effect_ids']=[e['id'] for e in LF['aggregate_effects'] if e['role']=='primary' and c['region_id'] in {e.get('region_id'),e.get('reference_region_id')}]

# Explicit integration binding: every source atomic result is retained once in the
# disposition ledger. Decomposed results also name all contributing invariants.
mapping={
'lane.global-composition':{
 'proposition':{'medium-distinction':['medium']},
 'frame-crop':{'aspect':['aspect'],'head-visibility':['placement'],'lower-limit':['crop'],'right-edge':['arm-crop']},
 'upward-view':{'underplanes':['view-low','chin'],'torso-head-scale':['view-near']},
 'region-hierarchy':{'foreground-area':['placement'],'backdrop-visible-share':['illustration-scale','overlap'],'depth-order':['overlap']},
 'backdrop-zones':{'enlargement-and-crop':['illustration-scale'],'spatial-zoning':['overlap'],'displayed-palette':['poster-hue','poster-chroma','gray-value','gray-chroma']},
 'fidelity-ceiling':{'fine-detail':['capture'],'background-legibility':['capture']}},
'lane.spatial-topology':{
 'upward-projection':{'low-view':['view-low'],'scale':['view-near']},
 'pose-residuals':{'chin':['chin'],'head-yaw':['head-yaw'],'gaze':['gaze'],'shoulder-slope':['shoulder-slope']},
 'frame-crop':{'head':['placement'],'torso':['crop'],'arm':['arm-crop']},
 'illustration-overlap':{'depth':['overlap'],'size':['illustration-scale'],'direction':['overlap'],'visibility':['overlap']},
 'completion-boundary':{'limits':['arm-crop','crop','overlap']}},
'lane.subject-appearance':{
 'human-role':{'adult-role':['medium','placement']},
 'face-geometry':{'outline':['face'],'eyes':['face','hair-form','brow-shadow'],'nose':['face']},
 'hair-boundary':{'bangs':['hair-form'],'length':['hair-form']},
 'garment-silhouette':{'contour':['body-contour'],'coverage':['garment-coverage'],'band':['band'],'hem':['crop']},
 'displayed-skin':{'skin':['capture','garment-coverage','chin']}},
'lane.color-light-material':{
 'dark-material-values':{'hair-value':['hair-value'],'shirt-value':['shirt-value'],'dark-chroma':['hair-chroma','shirt-chroma']},
 'skin-color':{'value':['skin-value'],'chroma':['skin-chroma'],'hue':['skin-hue'],'lips':['lip-hue','lip-chroma']},
 'background-palette':{'pink-hue':['poster-hue'],'pink-chroma':['poster-chroma'],'gray':['gray-value','gray-chroma']},
 'facial-and-shoulder-light':{'face-neck':['face-neck-light'],'shoulder':['shoulder-light'],'brow':['brow-shadow']},
 'material-light-response':{'hair-sheen':['hair-sheen'],'shirt-gradient':['shirt-gradient']},
 'displayed-tone':{'shadow-floor':['shirt-floor'],'rolloff':['skin-rolloff']}},
'lane.medium-aesthetic-capture':{
 'medium-separation':{'photo':['medium']},
 'capture-softness':{'foreground':['capture'],'background':['capture']},
 'surface-and-makeup':{'skin-finish':['capture']}}
}
invmap={x['id']:x for x in C['invariants']}
reports=[json.loads((ROOT/(lane+'.report.json')).read_text()) for lane in mapping]
integration={'status':'complete','finding_dispositions':[],'obligation_dispositions':[],'conflicts':[]}
for report in reports:
 lane=report['lane_id']
 for finding in report['findings']:
  key=finding['id'].split(':')[1];targets=[]
  for obligation in finding['atomic_obligations']:
   suffix=obligation['id'].split(':')[2];bound=mapping[lane][key][suffix];iid=bound[0]
   for bid in bound:
    invmap[bid]['source_obligation_ids'].append(obligation['id'])
    if bid not in targets:targets.append(bid)
   integration['obligation_dispositions'].append({'obligation_ids':[obligation['id']],'disposition':'retained','final_invariant_id':iid,'final_role':invmap[iid]['role'],'covered_invariant_ids':bound,'covered_control_ids':['control-'+bid for bid in bound],'preserved_result_direction':obligation['result_direction'],'reason':'The literal result survives in these source-owned controls; additional IDs retain decomposed axes and relations.'})
  iid=targets[0]
  integration['finding_dispositions'].append({'finding_ids':[finding['id']],'disposition':'retained','final_invariant_id':iid,'final_role':invmap[iid]['role'],'covered_invariant_ids':targets,'source_priority':finding.get('priority'),'reason':'All atomic obligations retained through their explicit control bindings; no material result discarded.'})

for inv in C['invariants']:
 inv['source_obligation_ids']=sorted(set(inv['source_obligation_ids']))
 inv['viewer_priority']='P0' if inv['id'] in {'medium','aspect','view-low','view-near','placement','overlap'} else 'P1' if inv['role']=='primary' else 'P2'
# Tone controls protect the primary light pattern even when a broader skin region
# contains the smaller light-form subregions.
for ctl in CT['emitted_controls']:
 if ctl['region_id']=='skin' and ctl['axis'] in {'value','highlight-rolloff'}:
  ctl['protected_light_effect_ids']=['effect-face-neck-light','effect-shoulder-light','effect-brow-shadow']
next(x for x in C['aggregate_effects'] if x['id']=='effect-skin-texture')['direction']='Softly resolved displayed skin surface without a glossy wet finish; no retouching process is inferred.'
P['production_order']=[x['id'] for x in ordered]
prompt='\n\n'.join(' '.join(c['prompt_excerpt'] for c in ordered[a:b]) for a,b in [(0,13),(13,18),(18,23),(23,len(ordered))])+'\n'
plan_sha=hashlib.sha256(json.dumps(P,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
bundle={'schema_version':'reverse-image-analysis-bundle/v2','request':{'user_request':'이 이미지에서 충실한 독립형 영문 이미지 생성 프롬프트를 추출하고, 그 프롬프트만으로 이미지를 한 장 생성해줘.','intent_mode':'faithful'},'source_artifact':reports[0]['source_artifact'],'route':ROUTE,'execution':{'mode':'mixed','prompt_frozen':False,'independence_claimed':False},'integrated_plan':{'payload':P,'sha256':plan_sha},'lane_reports':reports,'integration':integration,'adjudications':[]}
def write(name,obj):
 (ROOT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
write('plan.json',P);write('analysis-bundle.precritic.json',bundle)
(ROOT/'prompt.integrated-draft.txt').write_text(prompt)
write('integration-decisions.json',{'schema_version':'case-integration-decisions/v1','source_sha256':P['source_sha256'],'plan_canonical_sha256':plan_sha,'status':'awaiting-source-aware-independent-critic','instruction_snapshot':'skill v1, unchanged in v2 and v3','validator_snapshot':'skill-v3','execution_limitation':'One fresh-context lane and four coordinator sequential-fallback lanes; no overall independent-lane claim.','dispositions':integration,'omissions':[{'detail':'Tiny pale hem lettering and narrow outer black edge strips','priority':'P3','basis':'Global/capture omission checks regard these as incidental to the medium, crop, pose and region hierarchy.'}],'uncertainty':['Physical camera azimuth/roll, torso rotations, shoulder depth order, exact lens and light rig remain unresolved.','Broad person-prior utility is uncertain; no demographic or attractiveness prior emitted.','Displayed skin color and tonal targets do not imply measured intrinsic reflectance or a calibrated pipeline.'],'attribution_decision':'Visible nose/chin underplanes have joint camera and head-lift contributors. Camera and residual head controls preserve distinct visible targets with no exact physical angles; full literal clauses remain for source-aware review.','precision_note':'No tests are used as visual evidence. Structure validators do not prove generation fidelity.'})
write('critic-packet.json',{'source_path':str(ROOT.parent/'source.jpg'),'source_sha256':P['source_sha256'],'route_path':str(ROOT/'route.json'),'route_fingerprint':ROUTE['route_fingerprint'],'report_paths':[str(ROOT/(lane+'.report.json')) for lane in mapping],'plan_path':str(ROOT/'plan.json'),'plan_canonical_sha256':plan_sha,'plan_file_sha256':hashlib.sha256((ROOT/'plan.json').read_bytes()).hexdigest(),'draft_prompt_path':str(ROOT/'prompt.integrated-draft.txt'),'draft_prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(),'reviewed_finding_ids_expected':[f['id'] for r in reports for f in r['findings']],'reviewed_obligation_ids_expected':[o['id'] for r in reports for f in r['findings'] for o in f['atomic_obligations']],'reviewed_invariant_ids_expected':list(invmap),'reviewer_context_description':'root, independent of case integrator; shared reviewer across cases; not a fresh empty context','coverage_review_status':'pending; no reviewer response fabricated'})
print(json.dumps({'plan_canonical_sha256':plan_sha,'prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(),'controls':len(ordered),'invariants':len(invmap),'findings':len(integration['finding_dispositions']),'atomic_obligations':len(integration['obligation_dispositions'])},indent=2))
