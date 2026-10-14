"""Directly authored142nd-role proposal; no catalog/candidate acceptance or registration."""
import sys,json,datetime,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));import direct_review as d
SPEC={
'id':'surface_pattern','semantic_role':'direct','priority':'support',
'description':'Bounded visible motif geometry and its layout, adjacency or explicitly stated repetition on one declared non-anatomical surface or design field, independent of physical surface microstructure, material identity, local hue and whole-frame composition.',
'description_ko':'선언된 비해부학적 표면·도안 영역 하나에 속한, 경계가 있는 시각 모티프의 형상·배치·인접 관계와 명시된 경우에만 반복. 물리적 미세조직·재질·국소 색상·사진 전체 구도와 구별하며, 반복 없는 한정된 모티프에도 해당한다.',
'dimensions':['appearance'],'owners':['surface'],'property_prefixes':['surface.pattern','surface.motif','surface.design_layout'],
'core_fields':['subject','setting','visual_priorities'],'applicability':{},
'evidence_terms':['motif','pattern','repeat','interlace','graphic tile','printed design','문양','모티프','도안','반복','교차무늬'],
'includes':[
'A figural or vegetal ornamental motif whose line/shape joins belong to the same declared artifact surface or design field; no repetition is required unless separately stated.',
'Hooked teardrop motifs explicitly repeating on one declared garment print; orthogonal equal-width bands forming small checks on one declared fabric surface.',
'Geometric interlace cells with explicitly consistent adjacency on one artifact-bound design; graphic motif contours explicitly continuing across neighboring repeated design-tile boundaries.',
'A separately evidenced visual motif may coexist with physical relief, weave or local color on the same owner, but each role requires its own positive property. A flat print can establish motif geometry without establishing physical relief or a printing process.'
],
'excludes':[
'Physical weave, knit loops, raised ribs, roughness or relief alone without a separately declared visual motif/layout; these belong to texture, with material identity and optical response assessed separately.',
'Uniform local hue, palette, brightness or bounded color placement alone without a motif; color remains separate and no fixed palette follows from a motif name.',
'Whole photographic frame arrangement, negative space, crop or subject placement; a depicted design field remains on its own owner rather than becoming the surrounding photograph layout.',
'Owned anatomy or markings on a body/skin/hair surface, including a depicted body when the clause actually describes its anatomy or marking; use the appropriate anatomical, body_marking or makeup/hair role. An animal-shaped artifact ornament is not a new animal.',
'Garment-specific seam, opening, fold, trim attachment or construction alone; an actual visual print is not automatically garment_detail, and a generic fabric owner is not automatically a garment.',
'Physical object part assembly, hinge, cavity or strap routing alone without a separately stated motif/design relation; object_structure remains distinct.',
'Image grain/compression/lens artifacts, illumination/shadow projections or optical interference alone; a receiving-surface pattern is not inferred solely from lighting or processing.',
'Literal readable text content, symbolic belief, cultural affiliation, biological species, provenance, fabrication process, hidden chemistry or historical identity inferred from a motif.',
'An unbounded style label, metadata keyword, old effect/property name, optional child or render guard cannot supply positive motif geometry, owner identity, repetition or additional actors.'
],
'neighbors':['texture','surface_material','object_structure','composition','color','body_marking','garment_detail','visible_text','makeup_decoration']}
# Each tuple is a manually reviewed actual positive or negative witness, not an automatic slot assignment.
W=[
(12868,True,'depicted_artifact',False,[('/content/components/0/concept_units/0','a figural head joins a scrolling ornamental stem','surface.motif.figural_head_scroll_join'),('/content/components/1/concept_units/0','small animal forms connect into the same decorative framework','surface.motif.animal_forms_same_framework')],
'Figural/animal/scroll topology belongs to the declared artifact design. No repetition is asserted. Physical relief, actual anatomy and raw material remain unproven; native material ornament_relief must be explicitly corrected, not borrowed as support.'),
(12893,True,'depicted_artifact',True,[('/content/components/0/concept_units/0','curving stems bifurcate into repeated leaves','surface.pattern.vegetal_branching'),('/content/components/1/concept_units/0','neighboring vegetal units continue into a repeat','surface.pattern.neighboring_vegetal_repeat')],
'Both botanical-looking branching AND neighboring-unit repeat are explicitly depicted on an artifact, without a live plant or material relief. Native material surface_pattern is not evidence and needs scope correction.'),
(12915,True,'depicted_artifact',True,[('/content/components/0/concept_units/0','bands interlace within a repeating geometric grid','surface.pattern.geometric_interlace_grid'),('/content/components/1/concept_units/0','repeated cells preserve consistent adjacency','surface.design_layout.interlace_cell_adjacency')],
'Graphic grid/interlace AND consistent repeated-cell adjacency are positive. No physical woven over-under strands, raw material, hue or whole-frame grid follows. Adjacency is a selected motif consistency constraint, not permission to relabel an actual effect preservation.'),
(12900,True,'selected_garment_print',True,[('/content/components/0/concept_units/0','Curved teardrop-shaped motifs with hooked tips repeat across the same cloth surface','surface.pattern.hooked_teardrop_repeat')],
'Parent relations explicitly bind this print to the existing wearer garment and cloth surface; the repeated motif has no fixed hue. Historical garment_detail/color routing cannot replace a print-specific fact. Cloth material is a separate positive fact; no manufacturing process or ethnicity follows.'),
(12850,True,'fabric_A',True,[('/content/components/0/concept_units/0','Equal-width horizontal and vertical bands on the fabric cross to form small repeated checks.','surface.pattern.equal_width_orthogonal_small_checks')],
'Parent own fabric_A horizontal/vertical bands cross and repeat. Generic fabric is not automatically a garment. Pattern scale and band width relation are explicitly selected but no numeric millimeters, yarn dyeing or mandatory physical weave follows. Associated profile garment wording/printed-imitation rejection remains independently scoped; it is not promoted into this parent.'),
(13277,True,'displayed_artwork',True,[('/content/components/0/concept_units/0','matching graphic tiles repeat across a visible tiled area','surface.pattern.matching_graphic_tile_repeat'),('/content/components/1/concept_units/0','motif contours continue across neighboring tile boundaries','surface.design_layout.motif_continuity_across_tile_boundaries'),('/content/components/2/concept_units/0','tile borders do not introduce gaps or doubled disconnected motifs','surface.design_layout.no_gaps_or_doubled_disconnected_motifs')],
'Parent applies to displayed artwork. All3 components are AND, including seam continuity and absence of doubled broken motifs; graphic design tiles do not certify ceramic masonry tiles, software or temporal animation loops. Original image_plane composition/layout effects overreach artifact-local design geometry and need explicit source correction.'),
(12943,False,'same_sweater_and_image',False,[('/content/components/0/concept_units/0',"Fine image grain is spread across the frame while the sweater's raised knit ribs stay distinct local textile relief.",'excluded.physical_texture_and_image_grain')],
'Physical raised knit ribs plus independent frame-wide image grain supply texture/grain_profile. No separately stated graphic motif/layout exists. Repetition inherent in physical ribs cannot automatically create surface_pattern.'),
(11970,False,'same_declared_skin_owner',False,[('/content/concept_units/0','a selected line motif lies within one declared skin region','excluded.body_marking'),('/content/concept_units/1','the motif contours remain surface marks on that same skin owner','excluded.body_marking')],
'Explicit human intrinsic condition and same-body skin-plane marks require the specialized body_marking owner scope. A surface_pattern duplicate for this same marking fact would erase that distinction; drawn symbol is not detached artifact or new anatomy. No literal symbol meaning or tattoo process is certified.'),
(12341,False,'top_A',False,[('/content/components/0/concept_units/0','The declared top has a light blue-green color on its textile surface.','excluded.uniform_local_color')],
'Owned blue-green textile color is directly positive, but no motif shape, repeated units or design adjacency is stated. A color-field boundary alone does not force a motif.'),
(4276,False,'image',False,[('/content/en','silhouette outline against negative space','excluded.whole_frame_composition')],
'The photographic negative-space arrangement is image-wide composition, with limited facial detail in embedding prose. No separately declared artifact/design field supports a surface_pattern.'),
(12881,False,'depicted_artifact',False,[('/content/components/0/concept_units/0','shafts gears and linkages occupy a visible apparatus cavity','excluded.object_structure'),('/content/components/1/concept_units/0','the casing boundary defines that exposed cavity','excluded.object_structure')],
'Actual casing-bounded physical part assembly supports object_structure, not a graphic decoration or actual operating event. Hardware source effects are not material evidence.'),
(12933,False,'same_panel',False,[('/content/components/0/concept_units/0','Two inward-facing folds meet at the center of the panel.','excluded.object_fold_geometry'),('/content/components/1/concept_units/0','the joined folds form an inverted box pleat.','excluded.object_fold_geometry')],
'Physical panel fold form supports generic object_structure under proposed141; actual garment-owned version would use garment_detail. No independently stated printed/ornamental motif makes the fold a surface_pattern.'),
(12784,False,'scene_flower',False,[('/content/components/0/concept_units/0','large distinct floral segments form an open cup-shaped bloom','excluded.botanical_anatomical_form'),('/content/components/1/concept_units/0','the bloom remains attached to its own woody stem','excluded.botanical_continuity')],
'Real/declaratively botanical bloom/stem form and continuity are not an artifact floral pattern. Final botanical body/anatomical scopes need review; no generic motif role or biological identification follows.')
]
if __name__=='__main__':
 catalog_doc=json.loads((R/'CATALOG-CORRECTED-PROPOSAL-01.json').read_text());cat=catalog_doc['catalog'];source=d.source();order=json.loads((R/'ORDER.json').read_text());pending=json.loads((R/'authored/native_pending_12250_read_packet.json').read_text());witnesses=[]
 for ordinal,positive,owner,repeat,quotes,judgement in W:
  cid=order[ordinal]
  if str(ordinal) in pending:
   src=pending[str(ordinal)];snapshot=dict(ordinal=ordinal,candidate_id=cid,source=src['source_before'],actual_rids=src['actual_rids'],local_effect_sets=src['effect_sets'],references=src['dependency_records'],bindings=src['reference_bindings'])
  else:snapshot=json.loads((R/f'authored/catalog_surface_pattern_12250_witness_{ordinal}.json').read_text())
  assert snapshot['source']==source['candidates'][cid]
  evidence=[]
  for pointer,quote,prop in quotes:
   val=d.pointer(snapshot['source'],pointer) if hasattr(d,'pointer') else None
   v=snapshot['source']
   for key in pointer[1:].split('/'):v=v[int(key)] if isinstance(v,list) else v[key]
   assert quote in v
   evidence.append(dict(realization_id='base',pointer=pointer,quote=quote,dimension='appearance',target=owner,property=prop))
  witnesses.append(dict(ordinal=ordinal,candidate_id=cid,positive_for_proposed_surface_pattern=positive,explicit_repetition=repeat,owner=owner,evidence=evidence,judgement=judgement,source_snapshot=snapshot,source_sha256=d.c.digest(snapshot['source']),conditions_preserved=snapshot['source']['conditions'],reference_bindings_preserved=snapshot['bindings'],classification_is_manual=True))
 proposal=dict(schema='photo-catalog-surface-pattern-proposal/v1',status='proposed_not_adopted_not_native_qualified',reviewer='/root/review_12250_13000',model='gpt-6.1-sol',reasoning_effort='high',source_sha256=d.c.digest(source),current_proposed_catalog_sha256=d.c.digest(cat),current_slot_count=len(cat),proposed_slot_count=len(cat)+1,exact_new_slot_spec=SPEC,spec_sha256=d.c.digest(SPEC),whole_final_catalog_reviewed=False,final_catalog_refinements_pending=True,witnesses=witnesses,constraints='No source/catalog/binding/registry/index/runtime/Git mutation. All actual sources and complete CID/binding closures were directly read; actual RID base only. Optional choices remain optional; associated profiles require independent activation and never become parent mandatory. A native footprint must be corrected/reviewed explicitly before proof, including separately consumed profile projection. A positive witness is a role-boundary proposal, not existing source or proof approval.',operational_native_qualified_count=0,historical_139_judgements_unchanged=True)
 import photo_slot_semantics
 photo_slot_semantics.validate('surface_pattern',SPEC,set(cat)|{'surface_pattern'},d.c.strings)
 d.write(R/'authored/catalog_surface_pattern_12250.proposal.json',proposal)
 note=dict(task_name='review_12250_13000',model='gpt-6.1-sol',reasoning_effort='high',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),authored_paths=['authored/catalog_surface_pattern_12250.py','authored/catalog_surface_pattern_12250.proposal.json','authored/catalog_surface_pattern_12250_read.py'],proposal_sha256=d.c.digest(proposal),directly_read_positive_witness_ordinals=[w[0] for w in W if w[1]],directly_read_negative_witness_ordinals=[w[0] for w in W if not w[1]],read_scope='Each complete positive/negative witness source, all transitive CID references/associated profiles/conditions/effects/provenance and explicit actual binding definitions were read. Three motif witnesses and plant/assembly witnesses reuse full same-session native_pending snapshots; six additional complete witness snapshots plus frame composition were read separately. No keyword discovery output counted as complete reading.',specs_directly_read=['object_structure','liquid_inclusion','texture','surface_material','composition','color','body_marking','garment_detail','body_form','anatomical_connection','prop','subject','silhouette_proportion','environment_detail'],whole141_catalog_reviewed=False,validation='Exact source quote checks and pure slot spec schema validation passed. No native/full-corpus validation or registration.',prepared_count=len(W),actual_read_count=len(W),status='proposal_only',canonical_changed=False)
 d.write(R/'worker-notes/catalog_surface_pattern_12250.json',note)
 print(json.dumps(dict(proposal=str(R/'authored/catalog_surface_pattern_12250.proposal.json'),positive=6,negative=7,spec_sha256=proposal['spec_sha256'],schema_valid=True)))
