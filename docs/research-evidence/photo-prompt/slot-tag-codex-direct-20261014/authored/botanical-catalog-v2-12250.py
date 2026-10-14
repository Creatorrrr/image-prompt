"""Directly authored bounded botanical clarification of2 existing roles; proposal only."""
import sys,json,copy,datetime,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));import direct_review as d;import native_reviews as nr;import photo_slot_semantics as slots
FINAL_SHA='e7ad376ae1e195ada8268259015b29751f33a24f47e23899c7b7e9329b4a3e28'
BEFORE=json.loads((R/'CATALOG-FINAL-142.json').read_text());assert d.c.digest(BEFORE)==FINAL_SHA
AFTER=copy.deepcopy(BEFORE)
AFTER['body_form'].update(
 description='Owned non-facial anatomical contour, regional volume or visible muscle and tendon form of a declared biological subject, including a plant or declared botanical part. Explicitly depicted anatomy remains owned by its representation. Independent of connection topology, relative proportions, pose, garment fit and non-anatomical artifact construction.',
 description_ko='선언된 생물 주체의 얼굴 이외 해부학적 윤곽·국소 부피·근육·힘줄 형태이며, 식물 또는 명시된 식물 부위의 기관 형태도 포함한다. 명시된 해부학적 묘사는 그 표현물의 소유 범위에 머문다. 연결 구조·상대 비율·자세·의복 부피·비해부학적 물건 구조와 구별하며 생존 상태·종·건강·능력·정체성을 추정하지 않는다.',
 owners=['actor','plant','representation'],
 evidence_terms=['muscle','tendon','contour','body build','body form','vein contour','botanical organ form','bloom form','leaf contour','근육','힘줄','윤곽','꽃 기관 형태','잎 윤곽'],
 includes=[
  'Restrained visible muscle planes on a declared human or other animal; a localized neck vein contour or gluteal-thigh surface fold.',
  'Large distinct floral segments forming an open cup on the declared botanical bloom; broad bounded leaf form or layered flower-organ form on its own declared plant owner. Plant form is not a claim of physiological life, growth capacity or species identification.',
  'Explicitly depicted biological anatomy, including represented botanical organ form, stays on its declared representation. The source must actually describe anatomical form, not merely a floral style, motif or generic craft part.',
  'A biological flower and a fabric rosette may occur in the same record, but anatomical form is assessed only on the declared biological flower or explicit anatomical depiction; cloth-fold form remains on the garment/craft owner.'
 ],
 excludes=[
  'Body/plant region names, biological class words or connection topology alone without an independently stated anatomical contour or regional form.',
  'Relative proportions, pose, facial geometry, garment fit or non-anatomical object/garment construction alone.',
  'Floral graphic paths, repeating vegetal ornament, branch-shaped hardware or fabric/paper/lace flower parts do not become biological anatomy from resemblance or petal/stem labels. An explicitly declared anatomical depiction may describe represented organs only; its physical carrier remains an artifact.',
  'A represented or artificial anatomical form does not alter or add a living actor/plant, and does not establish that its carrier is alive or that any depicted species exists physically.',
  'Body weight, health, strength, biological age, origin, species, growth capacity, material chemistry or fabrication inferred from form.',
  'Source owner, positive form and actual application scope must be explicit; metadata, source effects, an optional member/profile or an actor/plant/representation role word alone is not a form fact.'
 ],
 neighbors=['anatomical_connection','body_pose','body_region','facial_geometry','garment_fit','silhouette_proportion','skin_finish','texture','object_structure','surface_pattern'])
AFTER['anatomical_connection'].update(
 description='Ownership and continuity, articulation, attachment or explicitly intended separation of anatomical parts of a declared biological subject, including a plant or declared botanical part. Explicitly depicted anatomy remains owned by its representation; non-anatomical artifact joins remain separate.',
 description_ko='선언된 생물 주체의 해부학적 부위 소유·연속·관절·부착 또는 명시적으로 의도된 분리이며, 식물 또는 명시된 식물 부위의 꽃·잎·자기 줄기 연결도 포함한다. 명시된 해부학적 묘사는 그 표현물의 소유 범위에 머문다. 형태·비율·단순 접촉·비해부학적 공예물 접합과 구별하며 생존·성장·종을 추정하지 않는다.',
 owners=['actor','plant','representation'],
 evidence_terms=['joins','connect','root','emerging','continuous','attached','bloom attached to its own stem','leaf on the same branch','꽃과 자기 줄기 연결','같은 가지의 잎'],
 includes=[
  'Ownership and continuity, articulation or explicitly intended separation of declared human or other animal anatomical parts, retaining each actual owner and endpoint.',
  'The declared botanical bloom remaining attached to its own woody stem; separate blossoms attaching along the same continuous branch; leaves belonging to that same declared plant/branch. Source-stated absence or separation is retained without inventing extra organs.',
  'Explicit anatomical attachment/continuity within a declared representation remains on the represented anatomy. A flat ornament path or assembled craft junction alone does not establish an anatomical relation.',
  'Where a fabric rosette and a separate existing biological flower coexist, their distinct owners remain distinct: the flower own petal/stem relation cannot be donated to the garment, and cloth attachment cannot be recast as plant growth.'
 ],
 excludes=[
  'Anatomical contour, regional volume, relative proportion or part names alone without an actual ownership, continuity, articulation, attachment or intended-separation proposition.',
  'Touching, nearness, overlap or visual alignment of separately owned subjects/objects alone; contact does not merge anatomy or establish a shared biological owner.',
  'Object hinges, hardware branches, textile/lace/paper flower assemblies and floral graphic-path joins alone. Depicted anatomical connection requires an explicitly declared anatomical depiction and remains scoped there, never inferred live continuity.',
  'Continuity/attachment does not prove that an owner is alive, growing, functional, healthy, a particular species or made by a particular process; a cut or depicted botanical part does not gain a hidden whole plant.',
  'An artifact or picture cannot alter/add a living actor or plant merely because its design resembles a biological part. Actor/plant/representation owner labels, source effects and optional members/profiles are not independent anatomical evidence.'
 ],
 neighbors=BEFORE['anatomical_connection']['neighbors']+['body_form','object_structure','surface_pattern'])
# These witness classifications, target/property choices and rejections are individually authored.
W=[
(12784,'positive_botanical_form_and_connection','scene_flower',[
 ('/content/components/0/concept_units/0','large distinct floral segments form an open cup-shaped bloom','body_form','appearance','body.form.botanical.open_cup_large_segments','The actual bloom-organ contour is positive, independent of its stem connection. No human body, universal petal count or species/life proof.'),
 ('/content/components/1/concept_units/0','the bloom remains attached to its own woody stem','anatomical_connection','body_geometry','anatomy.connection.botanical.bloom_own_stem','Own biological flower/stem continuity is explicit. Remains attached permits a manually reviewed preservation interpretation only with the exact independently frozen relation, rather than deletion of an actual mutation by mode labeling.')],
 'Parent/option/profile were reread in full. Parent AND requires cup form and own-stem attachment; its optional child stays optional and its primary-any flower/magnolia/branch condition is preserved. Source scene_flower is the botanical owner, not the person. Woody stem is independently declared material context; neither wood nor attachment proves life/growth/species. Native correction/proof remains a separate future full-source review.'),
(13126,'positive_botanical_connection_with_selected_form_limits','scene_branch',[
 ('/content/components/0/concept_units/0','small pale blossoms attach at separated intervals along one continuous woody branch','anatomical_connection','body_geometry','anatomy.connection.botanical.blossoms_same_continuous_branch','The complete botanical attachment relation is explicit on one branch. Small/pale/intervals are independently scoped clauses, not species or genealogy.'),
 ('/content/components/1/concept_units/0','that flowering branch has sparse or absent leaves and readable woody gaps','anatomical_connection','body_geometry','anatomy.connection.botanical.sparse_or_absent_leaves_on_own_branch','The sparse OR absent leaf alternatives remain disjunctive; do not force complete leaflessness or add a fixed leaf count.')],
 'These are botanical parts on the same existing branch. No independent local organ contour beyond small blossoms is forced as body_form here; anatomical_connection addresses actual attachments/declared separation, while pale color/woody material have separate roles. All required groups remain AND, sparse OR absent remains OR. No automatic all-mume five-petal requirement.'),
(13337,'positive_botanical_form_connection_and_distinct_optical_clause','scene_branch',[
 ('/content/components/0/concept_units/0','the larger layered flowers connect to a traceable branching stem','anatomical_connection','body_geometry','anatomy.connection.botanical.layered_flowers_traceable_own_stem','Connection is explicitly traceable; larger/layered flower form remains a distinct form clause on the same botanical owner.'),
 ('/content/components/0/concept_units/0','larger layered flowers','body_form','appearance','body.form.botanical.layered_flower_organ_form','Layered flower-organ form is declared; comparative larger does not invent a separate measured reference owner.'),
 ('/content/components/1/concept_units/0','broad glossy leaves have distinct leaf boundaries on that same branch','body_form','appearance','body.form.botanical.broad_bounded_leaves','Broad bounded botanical leaf form is explicit. Gloss is a separate optical material fact, not an anatomical shape or proof of living tissue.'),
 ('/content/components/1/concept_units/0','on that same branch','anatomical_connection','body_geometry','anatomy.connection.botanical.leaves_same_branch','Same-branch ownership is stated and must not borrow leaves from a different plant.')],
 'Two components and their actual botanical owner remain together. Glossy leaf surface is separately positive for surface_material; species/cultivar and universal petal count remain unproven. Original root appearance/material effects and consumed profile projection are preserved in the witness snapshot, not treated as automatic role evidence or native approval.'),
(13701,'mixed_positive_biological_and_negative_fabric_owners','scene_flower_and_separate_garment_rosette',[
 ('/content/components/0/concept_units/0','the garment rosette consists of gathered or folded fabric with cloth edges','neither_biological_role','appearance','garment.rosette.gathered_or_folded_cloth','Gathered OR folded fabric forms a garment craft rosette; this is local garment construction and declared material, not plant anatomy.'),
 ('/content/components/1/concept_units/0','the separate existing flower retains botanical petals connected to its own stem','anatomical_connection','body_geometry','anatomy.connection.botanical.separate_flower_petals_own_stem','The separate botanical flower has its own petal/stem relation. Retains may support exact preservation only after independently frozen witnesses, and cannot transfer continuity to the cloth rosette.')],
 'This is the strongest real two-owner control. Parent requires both cloth rosette AND separate existing botanical flower; the first component does not become an artificial-to-living transformation. Source intrinsic conditions{}, member optional/requirements{}, old human/deny-domain guard and independent profile activation remain intact. Negative/confusion statements reinforce but do not supply positive biology.'),
(13427,'negative_branch_shaped_artifact','depicted_artifact',[
 ('/content/components/0/concept_units/0','the branch-shaped artifact has a continuous solid object boundary','neither_biological_role','appearance','object.geometry.branch_shaped_solid_boundary','The explicitly artifact-owned boundary is physical non-anatomical geometry, not biological branch continuity.'),
 ('/content/components/1/concept_units/0','metallic-looking reflections remain on that same branch-shaped member','neither_biological_role','material','surface.optical.branch_shaped_member_metallic_look','Metallic-looking optical response stays on the same artifact; it proves neither chemical metal nor plant life.')],
 'A branch-shaped artifact is a declared physical object. Shape/reference tags and botanical nouns do not donate biological anatomy. No living twig becomes metal under gold lighting, and no new plant or growth event follows. Object_structure/material qualification is separate from this botanical spec boundary.'),
(13727,'negative_depicted_craft_transition_with_unselected_flower_or_lace','depicted_artifact',[
 ('/content/components/0/concept_units/0','a flat graphite line remains attached to the bounded paper surface','neither_biological_role','appearance','object.connection.graphite_paper_surface','A source line/paper relation is not biological anatomy.'),
 ('/content/components/2/concept_units/0',"the strand continues into the raised flower's stem or lace structure",'neither_biological_role','appearance','object.connection.raised_strand_flower_or_lace','The flower stem OR lace alternative does not unconditionally declare biological plant anatomy; the parent remains an authored depicted material path.')],
 'All4 source components jointly require flat line→visible paper junction→strand→raised flower-or-lace continuity. They are not a biological germination sequence. The optional child/profile clauses and impossible-material context are preserved; no source effect is reclassified or deleted here. Explicit future represented anatomy would require its own source proposition/owner, not the flower word alone.'),
(12893,'negative_graphic_vegetal_motif','depicted_artifact',[
 ('/content/components/0/concept_units/0','curving stems bifurcate into repeated leaves','neither_biological_role','appearance','surface.pattern.vegetal_branching','Complete source declares artifact ornament, so these are depicted graphic paths rather than own biological organs.'),
 ('/content/components/1/concept_units/0','neighboring vegetal units continue into a repeat','neither_biological_role','appearance','surface.pattern.neighboring_vegetal_repeat','The actual positive relation is artifact-bound motif repetition; surface_pattern does not add a living plant.')],
 'A botanical-looking ornament is not an anatomical illustration merely because it uses stems/leaves. The explicit artifact/design scope and full positive body select decorative repeat. Final142 surface_pattern is the fitting motif proposal after exact source/effect correction; no biological role or actual relief is supplied by native surface_pattern/material effects.')
]

def at(v,p):
 for k in p[1:].split('/'):v=v[int(k)] if isinstance(v,list) else v[k]
 return v
if __name__=='__main__':
 for tag in ['body_form','anatomical_connection']:slots.validate(tag,AFTER[tag],set(AFTER),d.c.strings)
 changes=[dict(pointer='/'+tag,before_exists=True,before=BEFORE[tag],after_exists=True,after=AFTER[tag],reason='Direct whole botanical and artifact/craft/depicted witness review clarifies biological-owner scope including plants and explicit anatomical representations, while preserving live/depicted ownership, form-versus-continuity and non-anatomical boundaries. No dimension/property-prefix expansion or automatic subject/category inference.') for tag in ['body_form','anatomical_connection']]
 assert nr.exact(nr.apply_delta(BEFORE,changes),AFTER)
 assert len(AFTER)==142 and set(AFTER)==set(BEFORE)
 assert [k for k in BEFORE if BEFORE[k]!=AFTER[k]]==['anatomical_connection','body_form']
 witnesses=[]
 for ordinal,classification,owner,fs,reason in W:
  p=R/f'authored/botanical_catalog_v2_12250_witness_{ordinal}.json';raw=json.loads(p.read_text());facts=[]
  for pointer,quote,role,dim,prop,why in fs:
   assert quote in at(raw['source'],pointer)
   facts.append(dict(realization_id='base',pointer=pointer,quote=quote,role_proposal=role,dimension=dim,target=owner,property=prop,rationale=why))
  witnesses.append(dict(ordinal=ordinal,candidate_id=raw['candidate_id'],classification=classification,owner=owner,facts=facts,rationale=reason,source_snapshot=raw,source_snapshot_sha256=d.c.digest(raw),source_record_sha256=d.c.digest(raw['source']),actual_rids=raw['actual_rids'],all_conditions_and_guards_preserved=True,source_changes_proposed_in_this_catalog_review=[]))
 proposal=dict(schema='photo-botanical-catalog-v2-proposal/v1',status='proposal_not_root_accepted_not_applied',reviewer='/root/review_12250_13000',model='gpt-6.1-sol',reasoning_effort='high',base_catalog_file='CATALOG-FINAL-142.json',base_catalog_sha256=FINAL_SHA,base_catalog_count=142,proposed_catalog_count=142,changed_role_ids=['body_form','anatomical_connection'],before_specs={k:BEFORE[k] for k in ['body_form','anatomical_connection']},after_specs={k:AFTER[k] for k in ['body_form','anatomical_connection']},changes=changes,proposed_full_catalog_sha256=d.c.digest(AFTER),whole142_catalog_reviewed=False,reviewed_final_spec_ids=['body_form','anatomical_connection','object_structure','surface_pattern','subject','surface_material','species_marker'],witnesses=witnesses,owner_protocol='actor/plant/representation are bounded semantic-owner descriptions in these2 specs, not new native common-role names or a candidate-free witness. Actual core owner UUID, neutral protocol role and exact botanical/representation facts must be independently declared. No class tag, botanical word, source effect or source membership can manufacture an owner, anatomy, prerequisite, new entity or life status.',native_modes='These specs do not decide effect/prerequisite/preservation/context. Actual canonical effects must be explicitly corrected/reread before native qualification; remains/retains only permits preservation when source meaning and exact frozen facts support it. Parent own effects, optional children, independently activated profiles, actual RIDs and all condition guards remain separate.',boundary='Existing142 file, all historical judgements, native_pending_12250_draft and canonical source/bindings/runtime/index/Git remain unchanged. This proposal adds0 slots, qualifies0 native records and produces no image/biological-identification evidence.')
 d.write(R/'authored/botanical-catalog-v2-12250.proposal.json',proposal)
 note=dict(task_name='review_12250_13000',model='gpt-6.1-sol',reasoning_effort='high',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),base_catalog_sha256=FINAL_SHA,authored_paths=['authored/botanical-catalog-v2-12250.py','authored/botanical-catalog-v2-12250.proposal.json','authored/botanical_catalog_v2_12250_read.py'],proposal_sha256=d.c.digest(proposal),proposed_full_catalog_sha256=d.c.digest(AFTER),prepared_count=7,actual_read_count=7,full_source_read_ordinals=[w[0] for w in W],read_scope='Original12784 parent, option and profile reread in full; all7 witnesses complete source/positive body/conditions/effects/actual RID/provenance/full transitive CID profiles and explicit guard bindings read without truncation. First3 are botanical positives;13701 deliberately combines actual botanical positive with separate fabric-rosette negative;13427/13727/12893 are artifact/craft/graphic counterexamples. Keyword discovery snippets were not counted as full reading.',final_specs_read=proposal['reviewed_final_spec_ids'],final_catalog_review_and_acceptance_read=True,whole142_catalog_reviewed=False,validation='Pure exact before/after2-spec delta, unchanged142 IDs/count, full schema checks for both proposed specs and exact positive quotes passed. No full-corpus/native validation or signature/registration.',native_qualification_count=0,old_pending9_and_old10draft_unchanged=True,production_or_git_changed=False,network_api_model_calls=False)
 d.write(R/'worker-notes/botanical-catalog-v2-12250.json',note)
 print(json.dumps(dict(proposal=str(R/'authored/botanical-catalog-v2-12250.proposal.json'),changed_specs=2,slot_count=142,witnesses=7,proposed_full_catalog_sha256=d.c.digest(AFTER))))
 print('COMPLETE_PROPOSED_SPECS',json.dumps(proposal['after_specs'],ensure_ascii=False))
