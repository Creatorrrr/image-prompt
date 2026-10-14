"""Literal manually authored formal03 facts; helpers only serialize and bind metadata."""
import json,gzip,hashlib,sys,copy
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');D=R/'native-inputs/prepared/review11870-01250-01300-03';G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/534cde26ba2156cf1760542d5be3a36e82b5457972d85f69d2a2fa8a7c0d50d2')
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c
# Load read-only research helper with frozen corpus already pinned, then restore paths before every late import.
sys.path.insert(0,str(R));import direct_review as direct
sys.path=[x for x in sys.path if x not in [str(Path('skills/photo-prompt-image-generator/scripts').resolve()),str(G/'scripts'),str(G/'precore')]]
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_semantic_evidence as n
import photo_candidate_realizations as real
I=json.loads((D/'INPUT.json').read_text());A=json.loads((D/'ASSIGNMENT.json').read_text());P=json.loads((D/'PREPARED-PACKET.json').read_text());S=json.loads(gzip.decompress(Path(I['current_snapshot']['file']).read_bytes()));CAT=I['catalog_review']['after'];CH=c.digest(CAT)
assert CH=='5bc5f6d185b6ef6e2d8d3a2bf6e4aa02d73e22143b0529a233fd5f98ddbed908'
assert c.digest(I)=='db1f809df8dc01e11f9855d4c9554a767e5a1dcb2a1e60a7dfc0eb196c20630a'
ROWS=[];CHECKS=[]
def F(fid,ptr,q,d,t,p,mode,vt,value,requires,operation=None,receivers=None):
 f={'id':fid,'realization_id':'base','pointer':'/content/'+ptr,'quote':q,'dimension':d,'target':t,'property':p,'mode':mode,'value':{'type':vt,'value':value},'requires':requires}
 if mode=='effect':assert operation is not None and receivers is not None;f.update(operation=operation,receivers=receivers)
 return f
def unit(ptr,refs):return (ptr,refs)
def delta(before,after,reason):
 # Identity diff only: author already chose the exact complete assigned after source.
 changes=[]
 for field in ['content','conditions','effects','provenance','record_kind']:
  if before[field]!=after[field]:changes.append({'pointer':'/'+field,'before_exists':True,'before':before[field],'after_exists':True,'after':after[field],'reason':reason})
 return changes
def row(ordinal,status,rationale,facts=None,roles=None,owners=None,units=None):
 cid=A['ids'][ordinal-1250];before=P['original_records'][cid];after=P['current_records'][cid];old=P['historical_compiled_rows'][cid];revision=I['required_revisions'][cid]
 proof=None
 if status=='approved':
  assert facts is not None and roles is not None and owners is not None and units is not None
  proof={'schema':n.SCHEMA,'meaning_sha256':n.meaning_sha256(after),'catalog_sha256':CH,'complete':True,'facts':facts,'roles':{tag:{'spec_sha256':c.digest(CAT[tag]),'scope':'whole_record','realization_ids':['base'],'fact_refs':refs,'support_modes':modes} for tag,refs,modes in roles},'owner_maps':{'base':owners if isinstance(owners,dict) else {'schema':'photo-native-owner-bindings/v2','bindings':[{'target':target,'core_role':role,'origin':'existing','introduced_by':None} for target,role in owners]}},'source_units':[{'realization_id':'base','pointer':'/content/'+ptr,'quote':after['content'][ptr],'fact_refs':refs,'disposition':'semantic'} for ptr,refs in units],'effect_sets':{'base':{'dimensions':sorted(after['effects']['dimensions']),'properties':sorted(after['effects']['properties'],key=n.property_key)}},'dependencies':{'base':[]},'reference_sha256':{},'guard_sets':{'base':{'source_conditions':[after['conditions'],{}],'member_conditions':{}}},'profile_contracts':{'base':None},'review':{'basis':rationale,'whole_source_reviewed':True,'source_correction':None if n.meaning_sha256(before)==n.meaning_sha256(after) else {'before_sha256':n.meaning_sha256(before),'after_sha256':n.meaning_sha256(after),'rationale':'Fresh whole assigned source correction reread, including exact owner/application and complete actual effects; exact root-selected formal03 input only. '+rationale},'original_review':{'candidate_id':cid,'source_record_sha256':old['source_record_sha256'],'catalog_sha256':old['catalog_sha256'],'decision_sha256':I['original_decisions'][cid]['row_sha256'],'artifact':I['original_decisions'][cid]['file']+'#item='+str(I['original_decisions'][cid]['item'])},'native_review':{'reviewer':'/root/review_11870_12250','method':'codex_subagent_direct_source_read','native_contract_sha256':''}}}
  proof['review']['native_review']['native_contract_sha256']=n.native_contract_sha256(proof)
  record=copy.deepcopy(after);record['content']['role_evidence']=proof
  n.validate(record,CAT,catalog_sha256=CH,corpus=S)
  CHECKS.append({'ordinal':ordinal,'full_source_validation':True,'proof_sha256':c.digest(proof),'native_signature':proof['review']['native_review']['native_contract_sha256']})
 ROWS.append({'candidate_id':cid,'ordinal':ordinal,'status':status,'rationale':rationale,'source_before':before,'source_after':after,'delta':delta(before,after,'Exact assigned INPUT original-to-current correction, freshly whole-source reviewed. '+rationale),'original_compiled':I['original_decisions'][cid],'proof':proof,'dependency_records':{},'reference_bindings':{},'source_reread_complete':True,'reference_reread_complete':True,'revision':{'prior_review':revision['prior_review'],'memo_artifacts':revision['memo_artifacts'],'rationale':'Fresh formal03 whole-source/native-namespace/owner/effect review. '+rationale}})


# Fresh literal full-source modes, roles, carrier scopes; not old facts conversion.
row(1290,'approved','Fresh03 entire original/current/5B/prior02/self binding/root approval41/independent memo against full current weather/thermal_state/sensory_cue. Existing scene common entity.presence P. Sticky tropical heat remains complete qualitative declared-weather E, not numeric temperature/humidity certification, sweat, country or summer date. Physical heat weather meaning is retained in whole weather value, never replaced by color or sensory proxy; source does not separately identify object/air temperature carrier or a thermal process and current effect is weather.declared atmosphere, so no fabricated material/thermal.state property or extra role. Root should assess this exact weather-vs-local-thermal boundary independently. All4 strings same selected E. Original optional direct weather .56 unrestricted binding and empty intrinsic conditions preserved.',[
 F('sceneP','application_contract','independently declared scene','subject','scene','entity.presence','prerequisite','entity.presence/v1','present',[]),
 F('heatEn','en','sticky tropical heat','atmosphere','scene','weather.declared','effect','weather.declared/v1','sticky_tropical_heat',['sceneP'],'set_value',[]),
 F('heatKo','ko','끈적한 열대성 더위','atmosphere','scene','weather.declared','effect','weather.declared/v1','sticky_tropical_heat',['sceneP'],'set_value',[]),
 F('heatEmb','embedding_text','sticky tropical heat','atmosphere','scene','weather.declared','effect','weather.declared/v1','sticky_tropical_heat',['sceneP'],'set_value',[]),
 F('heatApp','application_contract','Apply the stated sticky tropical heat as declared weather','atmosphere','scene','weather.declared','effect','weather.declared/v1','sticky_tropical_heat',['sceneP'],'set_value',[])],[('weather',['heatEn','heatKo','heatEmb','heatApp'],['effect'])],[('scene','scene')],[unit('en',['heatEn']),unit('ko',['heatKo']),unit('embedding_text',['heatEmb']),unit('application_contract',['sceneP','heatApp'])])
row(1291,'approved','Fresh03 whole original/current/5B/prior02/self binding/root approval42/independent memo against full current presentation_style. Independently existing person main_subject uses common entity.presence P. Fresh campus-student-like styling is selected appearance E in3 fields, no actual enrollment/age/location or garment specifics. Human source intrinsic preserved. Original optional direct .7 presentation human and documentary/craft/wildlife/product/jewelry/food deny remains independent role gate, no new unconstrained bypass.',[
 F('personP','application_contract','independently declared existing person','subject','person','entity.presence','prerequisite','entity.presence/v1','present',[]),
 F('styleEn','en','fresh campus-student styling','appearance','person','presentation.style','effect','presentation.style/v1','fresh_campus_student_like',['personP'],'set_value',[]),
 F('styleKo','ko','대학생 같은 산뜻한 스타일','appearance','person','presentation.style','effect','presentation.style/v1','fresh_campus_student_like',['personP'],'set_value',[]),
 F('styleApp','application_contract','Select fresh campus-student-like styling','appearance','person','presentation.style','effect','presentation.style/v1','fresh_campus_student_like',['personP'],'set_value',[])],[('presentation_style',['styleEn','styleKo','styleApp'],['effect'])],[('person','main_subject')],[unit('en',['styleEn']),unit('ko',['styleKo']),unit('application_contract',['personP','styleApp'])])
row(1292,'approved','Fresh03 complete original/current/5B/prior02/self binding/root approval43/independent memo against current prop/prop_state/narrative_clue. Same existing paper crane primary_prop independently needs precise props.type paper_crane P, no generic presence substitute or live bird/new object. Folded state AND left-behind disposition AND authored signal-token function are actual role/concept E across3 strings. Narrative contextual role cannot make newly selected signal purpose free C. No sender/recipient/group, delivery/decoding success or current leaving actor invented. Corrected Korean preserves left behind. Source human for_any and optional direct unrestricted prop .85 retained; narrative clue independent unrestricted spec. Concept E remains required-locked, actual consumer must deny.',[
 F('craneP','application_contract','independently declared existing paper crane','subject','crane','props.type','prerequisite','props.type/v1','paper_crane',[]),
 F('craneEn','en','paper crane','subject','crane','props.type','prerequisite','props.type/v1','paper_crane',[]),
 F('foldEn','en','folded','role','crane','prop.state','effect','prop.state/v1','folded',['craneP'],'set_value',[]),
 F('leftEn','en','left behind','role','crane','prop.state.disposition','effect','prop.state.disposition/v1','left_behind',['craneP'],'set_value',[]),
 F('signalEn','en','as a signal token','concept','crane','narrative.clue.function','effect','narrative.clue.function/v1','signal_token',['craneP'],'set_value',[]),
 F('craneKo','ko','종이학','subject','crane','props.type','prerequisite','props.type/v1','paper_crane',[]),
 F('foldKo','ko','접힌','role','crane','prop.state','effect','prop.state/v1','folded',['craneP'],'set_value',[]),
 F('leftKo','ko','남겨진','role','crane','prop.state.disposition','effect','prop.state.disposition/v1','left_behind',['craneP'],'set_value',[]),
 F('signalKo','ko','신호 토큰으로','concept','crane','narrative.clue.function','effect','narrative.clue.function/v1','signal_token',['craneP'],'set_value',[]),
 F('foldApp','application_contract','Select its folded state','role','crane','prop.state','effect','prop.state/v1','folded',['craneP'],'set_value',[]),
 F('leftApp','application_contract','left-behind disposition','role','crane','prop.state.disposition','effect','prop.state.disposition/v1','left_behind',['craneP'],'set_value',[]),
 F('signalApp','application_contract','as a signal token','concept','crane','narrative.clue.function','effect','narrative.clue.function/v1','signal_token',['craneP'],'set_value',[])],[('prop',['craneP','craneEn','craneKo'],['prerequisite']),('prop_state',['foldEn','leftEn','foldKo','leftKo','foldApp','leftApp'],['effect']),('narrative_clue',['signalEn','signalKo','signalApp'],['effect'])],[('crane','primary_prop')],[unit('en',['craneEn','foldEn','leftEn','signalEn']),unit('ko',['craneKo','foldKo','leftKo','signalKo']),unit('application_contract',['craneP','foldApp','leftApp','signalApp'])])
row(1293,'approved','Fresh whole03 source/5B/prior02/self binding/root approval0/independent memo directly read against full V4 hair_style/hair_color and common neutral hair protocol. Existing owned hair primary_hair independently needs subject/anatomy.hair.presence present; no wearer/head/biological/wig origin or body region inference. Actual length long, form wavy, local color black and naturally flowing arrangement remain4 appearance E. Arrangement positive only Korean/application, not borrowed into shorter English. No actual wind/movement, extra hair, identity/ethnicity or global grading. Human for_any source and original hair_style optional direct1 human+product/jewelry/food/wildlife deny binding remain; broader current specs do not waive intrinsic/old binding and each new role independently scoped.',[
 F('hairP','application_contract','independently declared existing owned hair','subject','hair','anatomy.hair.presence','prerequisite','anatomy.hair.presence/v1','present',[]),
 F('lengthEn','en','long','appearance','hair','hair.length','effect','hair.length/v1','long',['hairP'],'set_value',[]),
 F('waveEn','en','wavy','appearance','hair','hair.style','effect','hair.style/v1','wavy',['hairP'],'set_value',[]),
 F('blackEn','en','black hair','appearance','hair','hair.color','effect','hair.color/v1','black',['hairP'],'set_value',[]),
 F('lengthKo','ko','긴','appearance','hair','hair.length','effect','hair.length/v1','long',['hairP'],'set_value',[]),
 F('waveKo','ko','웨이브','appearance','hair','hair.style','effect','hair.style/v1','wavy',['hairP'],'set_value',[]),
 F('blackKo','ko','블랙 헤어','appearance','hair','hair.color','effect','hair.color/v1','black',['hairP'],'set_value',[]),
 F('flowKo','ko','자연스럽게 흐르는','appearance','hair','hair.strands.arrangement','effect','hair.strands.arrangement/v1','naturally_flowing',['hairP'],'set_value',[]),
 F('lengthApp','application_contract','Select long length','appearance','hair','hair.length','effect','hair.length/v1','long',['hairP'],'set_value',[]),
 F('waveApp','application_contract','wavy form','appearance','hair','hair.style','effect','hair.style/v1','wavy',['hairP'],'set_value',[]),
 F('blackApp','application_contract','black local hair color','appearance','hair','hair.color','effect','hair.color/v1','black',['hairP'],'set_value',[]),
 F('flowApp','application_contract','naturally flowing visual arrangement','appearance','hair','hair.strands.arrangement','effect','hair.strands.arrangement/v1','naturally_flowing',['hairP'],'set_value',[])],[('hair_style',['lengthEn','waveEn','lengthKo','waveKo','flowKo','lengthApp','waveApp','flowApp'],['effect']),('hair_color',['blackEn','blackKo','blackApp'],['effect'])],[('hair','primary_hair')],[unit('en',['lengthEn','waveEn','blackEn']),unit('ko',['lengthKo','waveKo','blackKo','flowKo']),unit('application_contract',['hairP','lengthApp','waveApp','blackApp','flowApp'])])
row(1294,'approved','Fresh full03 source/5B/prior02/self binding/root approval2/independent memo against current complete location. Existing scene common entity.presence P. Selected apartment door threshold setting E in4 fields, not entire unseen apartment interior, resident or entry/exit action. Empty source intrinsic, optional direct unrestricted location .58 retained.',[
 F('sceneP','application_contract','independently declared scene','subject','scene','entity.presence','prerequisite','entity.presence/v1','present',[]),
 F('doorEn','en','apartment door threshold','setting','scene','setting.location','effect','setting.location/v1','apartment_door_threshold',['sceneP'],'set_value',[]),
 F('doorKo','ko','아파트 현관 문턱','setting','scene','setting.location','effect','setting.location/v1','apartment_door_threshold',['sceneP'],'set_value',[]),
 F('doorEmb','embedding_text','apartment door threshold','setting','scene','setting.location','effect','setting.location/v1','apartment_door_threshold',['sceneP'],'set_value',[]),
 F('doorApp','application_contract','Select the apartment-door threshold','setting','scene','setting.location','effect','setting.location/v1','apartment_door_threshold',['sceneP'],'set_value',[])],[('location',['doorEn','doorKo','doorEmb','doorApp'],['effect'])],[('scene','scene')],[unit('en',['doorEn']),unit('ko',['doorKo']),unit('embedding_text',['doorEmb']),unit('application_contract',['sceneP','doorApp'])])
if __name__=='__main__':
 assert [r['ordinal']for r in ROWS]==list(range(1290,1295))
 modules={k:{'path':v.__file__,'sha256':hashlib.sha256(Path(v.__file__).read_bytes()).hexdigest()}for k,v in sys.modules.items()if k.startswith('photo_')and getattr(v,'__file__',None)};assert all(Path(v['path']).is_relative_to(G)for v in modules.values()),modules
 out=R/'authored/native_11870_formal03_checkpoint_01290_01295.json';assert not out.exists();payload={'schema':'photo-native-manual-review-small-checkpoint/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','assignment_sha256':c.digest(A),'input_sha256':c.digest(I),'actual_read_count':5,'records':ROWS,'full_source_checks':CHECKS,'frozen_generation':str(G),'loaded_photo_module_paths_sha256':modules,'boundary':'Fresh5 only/5 worker source proofs; not50, root acceptance0.1292 concept E remains locked;1290 whole qualitative declared weather not thermal proxy or measured value.'};out.write_text(json.dumps(payload,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(str(out),c.digest(payload),hashlib.sha256(out.read_bytes()).hexdigest());print('5 source proofs validated; no admission yet')
