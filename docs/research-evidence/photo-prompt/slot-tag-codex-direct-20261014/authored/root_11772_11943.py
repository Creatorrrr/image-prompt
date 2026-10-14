"""Two explicitly authored root source-placement judgements, no classification."""
import gzip,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(HERE));import direct_review as d
source=json.loads(gzip.decompress((HERE/'SOURCE.json.gz').read_bytes()));order=json.loads((HERE/'ORDER.json').read_text())
def fact(pointer,quote,dimension,target,prop):
 return {'pointer':pointer,'quote':quote,'dimension':dimension,'target':target,'property':prop}
def role(tag,evidence,reason):
 return {'slot_id':tag,'semantic_role':source['slot_catalog'][tag]['semantic_role'],
 'scope':'whole_record','realization_ids':['base'],'rationale':reason,'evidence':[evidence]}
f1=fact('/content/concept_units/0','the declared suspended objects retain a bounded still configuration',
 'action','declared_suspended_objects','motion.still_configuration')
f2=fact('/content/concept_units/2','the exception has a readable spatial boundary against the still region',
 'composition','still_region_and_exception','composition.boundary')
first={'candidate_id':order[11772],'meaning_summary':'The already declared suspended objects form a bounded still region beside a separately declared actor or region continuing its identifiable activity. A visible boundary distinguishes the two. Impossible-scene use is optional context, not an intrinsic positive claim of stopped time.',
 'recommended_kind':'visual_option','corrections':[],
 'roles':[role('physical_motion',f1,'Rest is explicitly owned by the declared suspended objects. No law of time or gravity is inferred.'),
          role('composition',f2,'The positive body requires a legible spatial boundary between existing regions.')],
 'facts':[{**f1,'realization_id':'base'},{**f2,'realization_id':'base'}],
 'rejected_boundaries':['The claim-limit says optional impossible-scene use. Do not turn that contextual possibility into an unconditional surreal_concept or surreal_physics_detail tag. No source correction is needed merely to preserve the legacy surreal slot.',
 'The actor OR region and its unspecified identifiable activity do not supply one concrete action or a universal number of exceptions. Do not add an actor, stopped-time mechanism, levitation support removal or off-frame event.',
 'The spatial boundary is arrangement, not an explicit crop, camera motion, long exposure, elapsed duration or physical proof from a still image.'],
 'uncertainties':[],'status':'approved','all_roles_considered':True}
record=source['candidates'][order[11943]];content=record['content'];corrections=[]
def correction(path,before,after,reason):
 corrections.append({'pointer':path,'before':before,'after':after,'reason':reason})
prefix='An authored impossible material transition follows one continuous artifact path: '
reason='Move the already explicitly authored impossible-material-transition rule from the claim-limit context into ordinary positive content. Preserve all local owners, junctions and the stem-or-lace alternative; this is a fictional artifact rule, not a physical process or a reference-body change.'
for path,before in [('/content/en',content['en']),('/content/embedding_text',content['embedding_text']),
 ('/content/paraphrases/1',content['paraphrases'][1]),('/content/concept_units/0',content['concept_units'][0]),
 ('/content/contextual_usage/contexts/0/observable_interpretation',content['contextual_usage']['contexts'][0]['observable_interpretation'])]:
 correction(path,before,prefix+before,reason)
ko='의도적으로 설정한 불가능한 재료 전이가 하나의 연속된 인공물 경로를 이룬다. 평면 흑연선이 경계가 보이는 종이 표면에 남고, 같은 선이 보이는 종이 접합점 하나에서 실로 솟으며, 실은 입체 꽃의 줄기 또는 레이스 구조로 이어진다. 평면 선·접합점·실·꽃은 하나의 연속 경로를 유지한다.'
correction('/content/ko',content['ko'],ko,reason)
correction('/content/paraphrases/0',content['paraphrases'][0],ko,reason)
new_en=prefix+content['en']
material=fact('/content/en','a flat graphite line remains attached to the bounded paper surface','material','paper_and_graphite_line','surface.material.paper_graphite')
depth=fact('/content/en','that same line rises into a strand at one visible paper junction','composition','flat_line_and_raised_strand','spatial.depth.flat_to_raised')
continuity=fact('/content/en','flat line junction strand and flower remain one continuous path','composition','continuous_artifact_path','composition.continuity')
transition=fact('/content/en',new_en,'timing','depicted_artifact','transformation.material_transition')
concept=fact('/content/en','An authored impossible material transition follows one continuous artifact path','concept','declared_artifact_rule','concept.surreal.material_transition')
physics=fact('/content/en',new_en,'concept','depicted_artifact','surreal.physics.graphite_strand_junction')
artifact=fact('/content/en',new_en,'subject','depicted_artifact','props.paper_strand_flower_artifact')
selected=[('surface_material',material,'Paper and graphite are explicitly declared source materials; no chemistry or performance is inferred.'),
 ('spatial_depth',depth,'The same flat line leaves the paper plane as raised strand at one visible junction.'),
 ('composition',continuity,'Line, junction, strand and flower form a single continuous depicted path.'),
 ('transformation_stage',transition,'The positive body now explicitly selects a fictional material transition, with visible flat and raised stages of the same artifact.'),
 ('surreal_concept',concept,'The already intended departure from ordinary material behavior is now positive selected context.'),
 ('surreal_physics_detail',physics,'The local impossible consequence is the same graphite-line-to-strand junction and continuous raised artifact path.'),
 ('prop',artifact,'A bounded paper/line/strand/raised-flower artifact is expressly identified with its carrier and transition role; it is one depicted artifact, not an additional flower or person.')]
second={'candidate_id':order[11943],'meaning_summary':'A deliberately authored impossible material transition joins a paper-bound graphite line, visible raised strand junction, and raised flower stem or lace in one continuous artifact. This is the depicted artifact rule; no ordinary manufacture, real growth, elapsed process or body transformation is claimed.',
 'recommended_kind':'visual_option','corrections':corrections,
 'roles':[role(tag,f,why) for tag,f,why in selected],
 'facts':[{**f,'realization_id':'base'} for _,f,_ in selected],
 'rejected_boundaries':['The original claim-limit explicitly declares authored impossible material transition. It differs from11772 optional impossible-scene use: preserve this intended rule in both positive languages, without treating a claim-limit as direct evidence.',
 'Stem OR lace are alternative endpoint values of the same continuous artifact property, not simultaneous mandatory separate objects or distinct new role families.',
 'The paper line is not a separate handheld prop or evidence of a new craft worker, tool, hand contact, manufacturing technique, botanical growth or elapsed physical motion.',
 'Graphite/paper are declared material identities, not inferred chemical analysis. Flat-to-raised depth is local artifact geometry, not a change to the photograph medium or a reference body.',
 'Selected source meaning is resolved here; native effect/carrier qualification and actual corpus/index/runtime application remain separate unfinished work.'],
 'uncertainties':[],'status':'approved','all_roles_considered':True}
d.write(HERE/'authored/root_11772_11943.json',{'decisions':[first,second]})
print(json.dumps({'corrected11943':d.corrected_record(record,corrections),'decisions':[first,second]},ensure_ascii=False,indent=2))
