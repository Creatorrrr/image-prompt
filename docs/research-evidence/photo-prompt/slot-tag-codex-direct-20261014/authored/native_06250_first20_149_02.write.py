"""Serialize seven fresh manual judgements and thirteen explicit pending rows.
No semantic inference from historical facts/tags, no source or runtime mutation.
"""
import sys,json,gzip,copy,hashlib
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
raw=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert raw(G/'scripts/photo_semantic_evidence.py')=='f74a5ef91bc07048c8bf312b66680c5b92b3b7b388f31f1890f31c8578609dee'
sys.path[:0]=[str(G/'scripts'),str(G/'precore'),str(R)]
import photo_semantic_evidence as e
import photo_candidate_corpus as c
import photo_candidate_realizations as z
import native_reviews as nr
sys.path[:]=[str(G/'scripts'),str(G/'precore')]+[p for p in sys.path if p not in {str(ROOT/'skills/photo-prompt-image-generator/scripts'),str(G/'scripts'),str(G/'precore')}]
P=R/'native-inputs/prepared/review06250-00000-00020-149-02'
A=json.loads((P/'ASSIGNMENT.json').read_text());I=nr.artifact(ROOT,A['input']);K=json.loads((P/'PREPARED-PACKET.json').read_text())
S=nr.artifact(ROOT,I['current_snapshot'])
assert c.digest(S)=='8acdd741cdb846c8bb33b53ded16471363ece5747280b5b4893c25acdeed302d'
assert c.digest(S['slot_catalog'])=='d9f4db418e1b63cd100b4c7a9fbff4c8401e00dffeffd22e299a0b5087a82b15'

# Each tuple is an independently chosen source-local fact, after whole source reading.
# id, exact EN quote, dimension, target, canonical property, typed-value type/value.
MANUAL={
3:('genre','image','image',[
 ('fantasy_genre','fantasy','style','image','genre.selection','genre.selection/v1','fantasy')],
 'Fantasy selects an image genre/convention. It changes stylistic interpretation, without adding magic, beings, world systems or historical facts. The root-selected existing genre.selection/image property remains exact.'),
4:('genre','image','image',[
 ('fine_art_genre','fine art','style','image','genre.selection','genre.selection/v1','fine_art')],
 'Fine art selects the declared photographic genre/purpose of the image. This is an actual stylistic selection, not a no-op context label. It does not supply a gallery, physical print, named art movement or capture apparatus.'),
5:('motion_rendering','image','image',[
 ('recorded_motion_blur','motion blur','camera','image','image.motion.rendering','image.motion.rendering/v1','motion_blur')],
 'Motion blur selects recorded image-plane motion rendering. No actor motion, camera movement, speed, direction or exposure is separately asserted. The complete actual camera effect stays image.motion.rendering/image.'),
9:('lens','camera','recording_camera',[
 ('lens_50mm','50mm','camera','camera','lens.focal_length_mm','lens.focal_length_mm/v1','50'),
 ('lens_standard','standard','camera','camera','lens.named_class','lens.named_class/v1','standard')],
 'The recording lens is expressly 50mm and named standard. Both choices are actual camera effects. Standard is the source-declared class, not a universal sensor-format field-of-view claim. No aperture, distance, depth of field, body or distortion is added.'),
16:('mood','scene','scene',[
 ('focused_reading','focused atmosphere','atmosphere','scene','mood.proposed_reading','mood.proposed_reading/v1','focused')],
 'The current English and Korean declare a focused scene atmosphere. This changes proposed affective interpretation; it is not optical focus, an invented person, work action, profession, facial expression or a proven private mental state. Original mood.proposed_reading/scene is preserved.'),
17:('lens','camera','recording_camera',[
 ('lens_24mm','24mm','camera','camera','lens.focal_length_mm','lens.focal_length_mm/v1','24'),
 ('lens_wide_angle','wide-angle','camera','camera','lens.named_class','lens.named_class/v1','wide_angle')],
 'The declared recording lens is 24mm and named wide-angle. Both exact effects remain. No approach, low angle, sensor format, enlarged anatomy, barrel distortion, aperture or chosen focus is supplied by that lens name.'),
18:('location','scene','scene',[
 ('laboratory_place','a laboratory','setting','scene','setting.location.kind','setting.location.kind/v1','laboratory')],
 'The scene location is selected as a laboratory. Its actual location effect is retained. No researcher, experiment, medical purpose, sterility, equipment, lighting or visible text follows from the laboratory noun or the excluded science/interior metadata.')}
PENDING={
0:'Bare neon plus a coarse lighting effect does not specify the actual light owner, receiver scope or whether a source device is to be added. Neon emission/type cannot be replaced by pink color, signage or city context. Explicit source application/refinement is needed before effect-mode proof.',
1:'Lab led must retain both LED and the laboratory-use qualifier. A bare qualifier cannot silently become a laboratory scene, researcher or medical role, and cannot be deleted as metadata. Coarse lighting effects and unresolved actual source/receiver application require root clarification.',
2:'Softbox is a source modifier/device, not a guaranteed soft-shadow measurement. The coarse lighting effect still needs an exact application owner and receivers. No new device or universal light quality is inferred from the short noun.',
6:'Hard flash expressly contains both flash source and hard light quality. Dropping hard or calling the cue context would erase an actual lighting selection. Actual source/receiver application and both complete effects need an explicit source correction.',
7:'Fluorescent is not enough to disambiguate source mechanism/application from fluorescent surface emission in this bare bilingual source. Historical metadata and 5B role cannot supply positive missing application wording. The coarse lighting effect remains pending.',
8:'Travel photograph retains travel as a photographic genre subject/context qualifier. The physical medium is not declared merely by photograph; no journey, destination, actor or new scene is authorized. Coarse style effects need a complete genre application refinement that preserves the qualifier.',
10:'Pet photography retains its pet subject-matter theme. A genre role does not create a pet, and neither species nor count is supplied. Current coarse style effects and actual independent theme/carrier applicability remain unresolved; no candidate-desired pet value is manufactured as a frozen witness.',
11:'Golden hour may identify an actual natural-light day phase or an imitated lighting treatment. Current bare source/coarse lighting does not choose between them, and the 149 specifications expressly exclude deriving source type/quality/day phase from an ambiguous label. Preserve the lighting E; request editorial source clarification.',
12:'Soft window names window-mediated illumination and explicitly soft quality. It does not supply a room, curtain, window location or direction. Actual source/window route and receiver application plus both precise lighting effects need root-selected source clarification.',
13:'Food photography retains its food subject-matter genre theme without automatically adding food, tableware or cooking. Current coarse style effect and independent applicability are not completed merely by a genre tag. Clarify the bounded genre application before proof.',
14:'Dieselpunk mood/디젤펑크 감성 positively selects aesthetic interpretation, not a persistent world system and not a context no-op. Current source still declares setting E. Replacing it with a style E changes the actual effect contract and requires explicit root-selected correction plus original setting-lock comparison; no prefix-driven automatic rename.',
15:'Street photography retains the street-photography convention; it does not choose a city, replace location, add a crowd or assert candid capture. The coarse style effect requires precise genre selection with the full qualifier retained and independently compatible scene content.',
19:'Interior photography retains its interior-space photographic theme, without selecting a particular room, furniture, architecture or wide lens. The coarse style effect needs exact genre application and actual compatible subject-matter carrier; no generated interior or existing-only interpretation is inferred automatically.'}

rows=[]
for ordinal,cid in zip(A['ordinals'],A['ids']):
 before=K['original_records'][cid];after=K['current_records'][cid]
 assert after==S['candidates'][cid] and K['references'][cid]==K['reference_bindings'][cid]=={}
 req=I['required_revisions'][cid]
 delta=[]
 if before['content']!=after['content']:
  assert ordinal==16
  delta.append({'pointer':'/content/en','before_exists':True,'before':before['content']['en'],'after_exists':True,'after':after['content']['en'],'reason':'Root-selected focused atmosphere clarifies the English in the same scene-mood sense already stated by Korean; no optical focus or private emotion added.'})
 if before['effects']!=after['effects']:
  delta.append({'pointer':'/effects','before_exists':True,'before':before['effects'],'after_exists':True,'after':after['effects'],'reason':'Exact root-selected current65 precision of the original actual effect dimension; retain every named canonical property and target, with no prefix-driven rename.'})
 proof=None
 if ordinal in MANUAL:
  tag,target,role,tuples,basis=MANUAL[ordinal]
  facts=[{'id':fid,'realization_id':'base','pointer':'/content/en','quote':quote,'dimension':dim,'target':owner,'property':prop,'mode':'effect','value':{'type':vt,'value':value},'requires':[],'operation':'set_value','receivers':[]} for fid,quote,dim,owner,prop,vt,value in tuples]
  refs=[f['id'] for f in facts]
  units=[{'realization_id':'base','pointer':'/content/en','quote':after['content']['en'],'fact_refs':refs,'disposition':'semantic'},
  {'realization_id':'base','pointer':'/content/ko','quote':after['content']['ko'],'fact_refs':refs,'disposition':'semantic_reference','reference_relation':'partial_restatement','retained_constraint_rationale':{'3':'판타지 restates the same fantasy genre, without a world-system assertion.','4':'파인아트 restates the fine-art genre without a substrate or gallery.','5':'모션블러 restates the same recorded motion blur without physical action.','9':'50mm 표준 렌즈 retains both 50mm and the named standard lens class.','16':'집중한 분위기 retains the focused atmosphere, not optical focus or proven psychology.','17':'24mm 광각 렌즈 retains both 24mm and the named wide-angle class.','18':'실험실 restates the laboratory location only; metadata adds no facts.'}[str(ordinal)]}]
  proof={'schema':e.SCHEMA,'meaning_sha256':e.meaning_sha256(after),'catalog_sha256':c.digest(S['slot_catalog']),'complete':True,'facts':facts,'source_units':units,
   'roles':{tag:{'spec_sha256':c.digest(S['slot_catalog'][tag]),'scope':'whole_record','realization_ids':['base'],'fact_refs':refs,'support_modes':['effect']}},
   'owner_maps':{'base':{'schema':e.OWNER_SCHEMA,'bindings':[{'target':target,'origin':'existing','introduced_by':None,'core_role':role}]}},
   'effect_sets':{'base':copy.deepcopy(after['effects'])},'dependencies':{'base':[]},'reference_sha256':{},'guard_sets':{'base':{'source_conditions':[{},{}],'member_conditions':{}}},'profile_contracts':{'base':None},
   'review':{'basis':basis+' Fresh complete original/current/exact 5B row/own binding/empty reference closure and current full used specs reread; every EN/KO positive field receives a direct unit or exact same-RID reference. Metadata is excluded. Receivers are explicitly empty because these image, recording-camera or scene attributes do not declare a separately affected receiver owner.',
    'whole_source_reviewed':True,'source_correction':{'before_sha256':e.meaning_sha256(before),'after_sha256':e.meaning_sha256(after),'rationale':basis+' This proof uses only the already root-selected exact current65 after, not a newly proposed correction.'},
    'original_review':{'candidate_id':cid,'source_record_sha256':K['historical_compiled_rows'][cid]['source_record_sha256'],'catalog_sha256':K['historical_compiled_rows'][cid]['catalog_sha256'],'decision_sha256':I['original_decisions'][cid]['row_sha256'],'artifact':K['original_compiled_artifacts'][cid]},
    'native_review':{'reviewer':'/root/review_06250_07250','method':'codex_subagent_direct_source_read','native_contract_sha256':'pending'}}}
  assert proof['guard_sets']['base']==e.source_guard_set(after,'base',S)
  assert proof['effect_sets']['base']==e.effect_set(after,'base')
  assert z.profile_contract(after,'base') is None
  proof['review']['native_review']['native_contract_sha256']=e.native_contract_sha256(proof)
  record=copy.deepcopy(after);record['content']['role_evidence']=proof
  e.validate(record,S['slot_catalog'],corpus={**S,'candidates':{**S['candidates'],cid:record}})
  rationale=basis
 else:rationale=PENDING[ordinal]
 rows.append({'candidate_id':cid,'ordinal':ordinal,'status':'approved' if proof else 'pending','rationale':rationale,'source_before':before,'source_after':after,'delta':delta,'original_compiled':I['original_decisions'][cid],'proof':proof,'dependency_records':{},'reference_bindings':{},'source_reread_complete':True,'reference_reread_complete':True,'revision':{'prior_review':req['prior_review'],'memo_artifacts':req['memo_artifacts'],'rationale':'Fresh individual 149V6/current65/GEN50fd92 direct rereview; historical seven approved/thirteen pending are retained as history, never mechanically relabeled. '+rationale}})
B={'schema':nr.BATCH,'task_name':A['task_name'],'model':A['model'],'reasoning_effort':A['reasoning_effort'],'assignment_sha256':c.digest(A),'input_sha256':A['input']['sha256'],'prepared_count':20,'actual_read_count':20,'records':rows}
N={'schema':nr.NOTE,'task_name':A['task_name'],'model':A['model'],'reasoning_effort':A['reasoning_effort'],'assignment_sha256':c.digest(A),'input_sha256':A['input']['sha256'],'batch_sha256':c.digest(B),'prepared_count':20,'actual_read_count':20,'whole_source_read_ids':A['ids'],'whole_dependency_read_ids':A['ids']}
O=R/'native_batches/review06250-00000-00020-149-02';O.mkdir(exist_ok=False)
for name,obj in [('BATCH.json',B),('NOTE.json',N)]:
 (O/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print('seven fresh literal proofs validated; thirteen explicit pending; research/root acceptance zero')
print({name:raw(O/name) for name in ['BATCH.json','NOTE.json']})
