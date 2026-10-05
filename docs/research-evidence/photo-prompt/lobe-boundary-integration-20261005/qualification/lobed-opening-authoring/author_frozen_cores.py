import json, hashlib
from pathlib import Path
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parent

def digest_bytes(value):
 return hashlib.sha256(value).hexdigest()
def canonical(value):
 return digest_bytes(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def save(path,value):
 path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def anchor(aid,source,dimension,evidence,**kw):
 return dict(anchor_id=aid,source_text=source,dimension=dimension,prompt_evidence=evidence,**kw)
def feature(cid,basis,reason,evidence,source=None,derivation=None):
 return dict(category_id=cid,basis=basis,source_span_ids=[] if basis=='agent_visual_choice' else ['topic'],source_text=source,derivation=derivation,reason=reason,baseline_evidence=evidence)
def assertion(aid,dimension,polarity,axes,evidence):
 return dict(assertion_id=aid,dimension=dimension,polarity=polarity,source_span_ids=['topic'],affected_dimensions=[dimension],axes=axes,evidence=evidence)

DATA={
 'three_lobed_stone':{
 'baseline':'An intimate architectural photograph of a small ornamental opening in a stone wall at an old courtyard stairway. Three rounded lobes meet as one continuous open outline; the garden is visible through the opening. The upper curve rises over two lower curves, each edge of the stone reveal catching a soft strip of daylight. Pale leaves and a narrow earth path sit beyond the wall, giving the dark recess a clear depth. A worn stair tread enters the lower corner. Fine pits, softened corners and a little mineral staining give the stone a tactile surface. Cool open-sky light keeps the garden greens quiet and the outline distinct. Frame the wall fragment closely, with the complete opening slightly above centre and a modest margin of stone around it.',
 'subject':'A small ornamental opening in a stone wall',
 'setting':'An old courtyard stairway beside a garden',
 'event':'The garden is visible through a continuous opening with three rounded lobes',
 'priorities':['The three rounded lobes join into a single opening with an uninterrupted silhouette','Garden depth remains visible beyond the stone thickness','The worn stair tread and weathered stone locate the ornament in daily architecture'],
 'resolution':'The requester describes an actual opening with three rounded lobes in one perimeter, not three separate holes. The garden is seen through this opening in the courtyard stairway wall.',
 'anchors':[
  anchor('core_concept','The opening has three rounded lobes joined into one continuous outline','concept','Three rounded lobes meet as one continuous open outline'),
  anchor('core_subject','a small ornamental opening','subject','a small ornamental opening'),
  anchor('core_event','with the garden visible through it','event','the garden is visible through the opening'),
  anchor('core_setting','in the stone wall of an old courtyard stairway','setting','a stone wall at an old courtyard stairway'),
 ],
 'shape_axes':{'outline':'three rounded lobes joined into one continuous outline','surface_state':'opening through a wall'},
 'shape_evidence':{'outline_phrase':'Three rounded lobes meet as one continuous open outline','through_phrase':'the garden is visible through the opening'},
 'features':[
  feature('feature.primary_object','explicit_request','The connected three-part outline identifies the requested ornament.','Three rounded lobes meet as one continuous open outline',source='The opening has three rounded lobes joined into one continuous outline'),
  feature('feature.location','explicit_request','The stairway wall situates the detail as architecture.','a stone wall at an old courtyard stairway',source='in the stone wall of an old courtyard stairway'),
  feature('feature.spatial_depth','request_derived','Visible space behind the wall establishes a real opening.','the garden is visible through the opening',derivation='The request says that the garden is visible through the opening; the baseline places that visible garden beyond the wall.'),
  feature('feature.environmental_details','agent_visual_choice','One stair edge supports the setting without competing with the silhouette.','A worn stair tread enters the lower corner'),
  feature('feature.lighting_source','agent_visual_choice','Open-sky illumination separates stone and garden quietly.','Cool open-sky light'),
  feature('feature.composition','agent_visual_choice','A complete outline in a close wall fragment gives the ornament visual priority.','the complete opening slightly above centre and a modest margin of stone around it')
 ]},
 'four_lobed_timber':{
 'baseline':'A natural architectural detail photograph of a weathered timber gate at a riverside garden. A single decorative opening cuts through the boards, its continuous edge forming four rounded lobes around the centre. Daylight and greenery show through the opening. The rounded parts face up, down, left and right, with the thickness of the timber visible along the inner edge. The gate\'s grey grain and small splits sit against the softer green foliage beyond; a sliver of river glints at the far side. Diffuse morning daylight holds detail in the recess and the worn surface. Compose a medium close view with the complete opening dominant and several board seams still visible, letting the gate remain a recognisable working object.',
 'subject':'A decorative opening in a weathered timber gate',
 'setting':'A riverside garden',
 'event':'Daylight and greenery show through one opening with four rounded lobes',
 'priorities':['One continuous opening has four rounded lobes around its centre','Gate thickness and background greenery establish the void through the timber','The weathered boards remain recognisable around the ornament'],
 'resolution':'The request specifies one decorative opening, whose four rounded lobes form a connected boundary through the timber gate. Light and greenery are visible beyond it.',
 'anchors':[
  anchor('core_concept','formed by four rounded lobes around the centre','concept','its continuous edge forming four rounded lobes around the centre'),
  anchor('core_subject','a single decorative opening','subject','decorative opening cuts through the boards'),
  anchor('core_event','Show daylight and greenery through the opening','event','Daylight and greenery show through the opening'),
  anchor('core_setting','at a riverside garden','setting','at a riverside garden'),
  anchor('core_count','a single decorative opening','count','A single decorative opening'),
  anchor('gate_surface','a weathered timber gate','appearance','a weathered timber gate',target='gate',property='surface.condition'),
  anchor('gate_material','timber gate','material','timber gate',target='gate',property='structure.material')
 ],
 'shape_axes':{'outline':'four rounded lobes around the centre','surface_state':'opening through timber'},
 'shape_evidence':{'outline_phrase':'its continuous edge forming four rounded lobes around the centre','through_phrase':'Daylight and greenery show through the opening'},
 'features':[
  feature('feature.primary_object','explicit_request','The one connected four-part opening is the subject-defining shape.','its continuous edge forming four rounded lobes around the centre',source='formed by four rounded lobes around the centre'),
  feature('feature.location','explicit_request','The riverside garden establishes the requested gate context.','at a riverside garden',source='at a riverside garden'),
  feature('feature.spatial_depth','request_derived','The visible backdrop distinguishes a perforation from a surface pattern.','Daylight and greenery show through the opening',derivation='The requester asks to show daylight and greenery through the opening, so the background remains visible beyond the gate.'),
  feature('feature.environmental_details','agent_visual_choice','A small river highlight quietly supports the riverside setting.','a sliver of river glints at the far side'),
  feature('feature.lighting_source','agent_visual_choice','Soft morning illumination retains the recess and timber surface together.','Diffuse morning daylight'),
  feature('feature.composition','agent_visual_choice','Visible seams retain the gate scale around the dominant ornament.','the complete opening dominant and several board seams still visible')
 ]},
 'painted_solid_panel':{
 'baseline':'A natural detail photograph of a cupboard in a ceramics workshop. A cream motif with four rounded lobes is painted on its solid blue wooden door. The continuous wood surface supports the cream paint across the entire motif, with shallow grain ridges still visible beneath the brushwork. Its four connected curves stand crisply against the blue. A hinge and the edge of the closed door establish the cupboard, while a small section of shelving with matte clay bowls falls softly away beside it. Side light from a high workshop window brings out the layered paint surface and fine brush marks. Frame the door at a comfortable viewing distance with the complete painted shape and a narrow border of blue surrounding it; keep the cream shape the first thing the eye finds.',
 'subject':'A cream painted motif with four rounded lobes on a cupboard door',
 'setting':'A cupboard in a ceramics workshop',
 'event':'Cream paint forms the motif on a continuous solid wooden door surface',
 'priorities':['The four rounded lobes are carried by cream paint across a solid door surface','The uninterrupted grain beneath the brushwork makes the opaque panel legible','Blue paint, a hinge and the door edge maintain the cupboard context'],
 'resolution':'The requester explicitly distinguishes a painted decorative motif from an opening. Its rounded lobes belong to the outline of cream paint on a solid blue wooden cupboard door.',
 'anchors':[
  anchor('core_concept','The motif is painted decoration, not an opening','concept','The continuous wood surface supports the cream paint across the entire motif'),
  anchor('core_subject','a cream motif with four rounded lobes','subject','A cream motif with four rounded lobes'),
  anchor('core_event','painted on its solid blue wooden door','event','is painted on its solid blue wooden door'),
  anchor('core_setting','a cupboard in a ceramics workshop','setting','a cupboard in a ceramics workshop'),
  anchor('motif_color','a cream motif','color','A cream motif',target='motif',property='paint.color'),
  anchor('door_color','blue wooden door','color','blue wooden door',target='cupboard_door',property='paint.color'),
  anchor('door_material','solid blue wooden door','material','solid blue wooden door',target='cupboard_door',property='panel.material')
 ],
 'shape_axes':{'outline':'four rounded lobes','surface_state':'paint on a solid wooden panel'},
 'shape_evidence':{'outline_phrase':'A cream motif with four rounded lobes','solid_surface_phrase':'The continuous wood surface supports the cream paint across the entire motif'},
 'exclusions':['an opening'],
 'features':[
  feature('feature.primary_object','explicit_request','The painted four-part motif defines the requested decorative subject.','A cream motif with four rounded lobes',source='a cream motif with four rounded lobes'),
  feature('feature.location','explicit_request','The working ceramics space explains the cupboard context.','a cupboard in a ceramics workshop',source='a cupboard in a ceramics workshop'),
  feature('feature.situation','request_derived','The continuous surface establishes the stated painted decoration as opaque.','The continuous wood surface supports the cream paint across the entire motif',derivation='The request calls the door solid and says the motif is painted decoration, not an opening; continuous wood carrying the paint realizes that distinction.'),
  feature('feature.environmental_details','agent_visual_choice','A little clay shelving gives a restrained workshop cue.','a small section of shelving with matte clay bowls'),
  feature('feature.lighting_source','agent_visual_choice','Window illumination makes the layered brushwork tangible.','Side light from a high workshop window'),
  feature('feature.composition','agent_visual_choice','A blue border makes the entire painted contour easy to read.','the complete painted shape and a narrow border of blue surrounding it')
 ]},
 'single_round_brick':{
 'baseline':'A quiet architectural photograph of a single round opening in a brick wall at a boathouse. The opening forms a simple circle with smooth edges, and the river is visible through it. A shallow inner reveal gives the wall thickness, while the water beyond carries a low horizontal reflection of the opposite bank. Rough brick faces and pale mortar joints surround the even circular rim. Muted daylight from a cloudy sky balances the cool river view with the warm clay wall. Place the complete circle a little left of centre, viewed nearly square to the wall, with enough masonry around it to show its modest scale. The contrast between the curved boundary, horizontal water and rectangular brickwork supplies the photograph\'s calm rhythm.',
 'subject':'A single round opening in a brick wall',
 'setting':'A quiet boathouse beside a river',
 'event':'The river is visible through a simple circular opening',
 'priorities':['A simple circular outline remains complete and clearly smooth-edged','The river can be seen through the wall thickness','The circular rim contrasts with the rectangular brick pattern'],
 'resolution':'The request describes one ordinary circular opening through a brick wall, with a smooth circular edge and a view of the river. No additional lobes or decorative perimeter are implied.',
 'anchors':[
  anchor('core_concept','a simple circle with smooth edges','concept','The opening forms a simple circle with smooth edges'),
  anchor('core_subject','a single round opening','subject','round opening in a brick wall'),
  anchor('core_event','the river can be seen through it','event','the river is visible through it'),
  anchor('core_setting','in the brick wall of a quiet boathouse','setting','a brick wall at a boathouse'),
  anchor('core_count','a single round opening','count','a single round opening'),
  anchor('quiet_atmosphere','a quiet boathouse','atmosphere','A quiet architectural photograph',target='scene',property='mood.quietness')
 ],
 'shape_axes':{'outline':'simple circle with smooth edges','surface_state':'opening through a wall'},
 'shape_evidence':{'outline_phrase':'The opening forms a simple circle with smooth edges','through_phrase':'the river is visible through it'},
 'features':[
  feature('feature.primary_object','explicit_request','The plain smooth circle is the defining form of the opening.','The opening forms a simple circle with smooth edges',source='a simple circle with smooth edges'),
  feature('feature.location','explicit_request','The boathouse masonry fixes the architectural setting.','a brick wall at a boathouse',source='in the brick wall of a quiet boathouse'),
  feature('feature.spatial_depth','request_derived','The visible river locates a real space beyond the opening.','the river is visible through it',derivation='The request says the river can be seen through the opening; the baseline preserves that visible background relation.'),
  feature('feature.environmental_details','agent_visual_choice','A horizontal reflection supplies a quiet water cue inside the circle.','the water beyond carries a low horizontal reflection of the opposite bank'),
  feature('feature.lighting_source','agent_visual_choice','Cloud light preserves brick and water tones in the same frame.','Muted daylight from a cloudy sky'),
  feature('feature.composition','agent_visual_choice','A slightly off-centre circle creates calm tension against the brick grid.','Place the complete circle a little left of centre')
 ]}
}

for name,data in DATA.items():
 d=ROOT/name
 envelope=json.loads((d/'request_envelope.json').read_text())
 controls=json.loads((d/'creative_controls.json').read_text())
 plan=json.loads((d/'pre_draft_plan.json').read_text())
 baseline=' '.join(data['baseline'].split())
 locked=['concept','subject','event','setting']+(['count'] if name in {'four_lobed_timber','single_round_brick'} else [])
 opened=['appearance','material','color','framing','composition','lighting','camera','timing','atmosphere','style']
 core={'contract_version':'photo-authorial-core/v3','provenance':'agent_prepack','source_request':envelope['request_text'],'creative_controls_sha256':controls['canonical_sha256'],'interpreted_intent':data['resolution']+' Agent-owned direction: '+plan['direction']+' '+plan['independent_alternatives'],'subject':data['subject'],'setting':data['setting'],'event':data['event'],'visual_priorities':data['priorities'],'baseline_prompt_en':baseline,'user_definitions':[],'interpretation_provenance':[{'term':'the requested decorative subject and its surface or opening','source_text':envelope['request_text'],'basis':'request_context','resolution':data['resolution'],'sources':[]}],'unresolved_ambiguities':[],'user_exclusions':data.get('exclusions',[]),'runtime_forbidden_labels':[],'intent_lock':{'contract_version':'photo-intent-lock/v2','priority':'requesting_user','semantic_anchors':data['anchors'],'locked_dimensions':locked,'open_dimensions':opened},'semantic_assertions':[assertion('primary_subject_category','subject','required',{'subject_category':'object'},{'subject_phrase':data['anchors'][1]['prompt_evidence']}),assertion('requested_shape_and_surface','concept','required',data['shape_axes'],data['shape_evidence']),assertion('camera_axis_review','camera','advisory',{'camera_axis_review':'camera_axis_review_v1','capture_owner':'unprescribed','direction_requirement':'open','height_requirement':'open'},{})],'request_lineage':None,'style':{'domain':'architectural detail photography','family':'restrained natural observation','evidence':['ordinary daylight','a complete subject outline in its material setting']},'variation_key':name}
 selection={'contract_version':'photo-precore-feature-selection/v1','request_id':envelope['request_id'],'active_span_ids':['topic'],'catalog_path':'skills/photo-prompt-image-generator/precore/visual_feature_catalog.json','catalog_schema_version':'photo-precore-feature-catalog/v1','catalog_sha256':digest_bytes((d/'visual_feature_catalog.snapshot.json').read_bytes()),'request_sha256':envelope['request_sha256'],'baseline_prompt_sha256':digest_bytes(baseline.encode()),'selected':data['features']}
 embodiment={'contract_version':'photo-embodiment-review/v1','provenance':'agent_prepack','prompt_sha256':digest_bytes(baseline.encode()),'scope':'not_applicable','summary':'This static architectural or cupboard detail contains no body, bodily action, articulated appendage, or bodily load-bearing mechanism. Surface continuity and opening depth were considered in the authorial core.','checks':{}}
 for row in core['intent_lock']['semantic_anchors']:
  assert row['source_text'] in envelope['request_text'],(name,row)
  assert row['prompt_evidence'] in baseline,(name,row)
 for row in selection['selected']:
  assert row['baseline_evidence'] in baseline,(name,row)
  if row['source_text'] is not None:assert row['source_text'] in envelope['request_text'],(name,row)
 assert 48<=len(baseline.split())<=640
 save(d/'authorial_core.json',core)
 (d/'baseline_prompt_en.txt').write_bytes(baseline.encode())
 save(d/'embodiment_review.json',embodiment)
 save(d/'precore_feature_selection.json',selection)
 bindings={'frozen_at_utc':datetime.now(timezone.utc).isoformat(),'hash_method':'SHA-256; object canonical bytes are UTF-8 JSON with ensure_ascii=False, sort_keys=True, separators=(comma,colon); raw and file hashes are exact bytes.','request_sha256':envelope['request_sha256'],'request_envelope_canonical_sha256':canonical(envelope),'authorial_core_canonical_sha256':canonical(core),'intent_lock_canonical_sha256':canonical(core['intent_lock']),'baseline_prompt_sha256':digest_bytes(baseline.encode()),'creative_controls_sha256':controls['canonical_sha256'],'embodiment_review_canonical_sha256':canonical(embodiment),'precore_feature_selection_canonical_sha256':canonical(selection)}
 save(d/'frozen_bindings.json',bindings)
 print(name,len(baseline.split()),bindings['authorial_core_canonical_sha256'])
