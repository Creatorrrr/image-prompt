"""Literal manually authored formal02 facts; helpers only serialize and bind metadata."""
import json,gzip,hashlib,sys,copy
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');D=R/'native-inputs/prepared/review11870-01250-01300-02';G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/1871bafa0e008e186ccce4e92908f2b177529b215c22e2fb46d07f0b28679bfd')
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_semantic_evidence as n
import photo_candidate_corpus as c
import photo_candidate_realizations as real
I=json.loads((D/'INPUT.json').read_text());A=json.loads((D/'ASSIGNMENT.json').read_text());P=json.loads((D/'PREPARED-PACKET.json').read_text());S=json.loads(gzip.decompress(Path(I['current_snapshot']['file']).read_bytes()));CAT=I['catalog_review']['after'];CH=c.digest(CAT)
assert CH=='0d7cab7b4add7279b0faa629bb5df72829da0c756adc6db21dcd7c09d56b971f'
assert c.digest(I)=='9167593b02863b305d44ee026d769b48d9e02e4554e3f47f5707239131faad19'
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
  proof={'schema':n.SCHEMA,'meaning_sha256':n.meaning_sha256(after),'catalog_sha256':CH,'complete':True,'facts':facts,'roles':{tag:{'spec_sha256':c.digest(CAT[tag]),'scope':'whole_record','realization_ids':['base'],'fact_refs':refs,'support_modes':modes} for tag,refs,modes in roles},'owner_maps':{'base':{'schema':'photo-native-owner-bindings/v2','bindings':[{'target':target,'core_role':role,'origin':'existing','introduced_by':None} for target,role in owners]}},'source_units':[{'realization_id':'base','pointer':'/content/'+ptr,'quote':after['content'][ptr],'fact_refs':refs,'disposition':'semantic'} for ptr,refs in units],'effect_sets':{'base':{'dimensions':sorted(after['effects']['dimensions']),'properties':sorted(after['effects']['properties'],key=n.property_key)}},'dependencies':{'base':[]},'reference_sha256':{},'guard_sets':{'base':{'source_conditions':[after['conditions'],{}],'member_conditions':{}}},'profile_contracts':{'base':None},'review':{'basis':rationale,'whole_source_reviewed':True,'source_correction':None if n.meaning_sha256(before)==n.meaning_sha256(after) else {'before_sha256':n.meaning_sha256(before),'after_sha256':n.meaning_sha256(after),'rationale':'Fresh whole assigned source correction reread, including exact owner/application and complete actual effects; no pending18 proposals applied. '+rationale},'original_review':{'candidate_id':cid,'source_record_sha256':old['source_record_sha256'],'catalog_sha256':old['catalog_sha256'],'decision_sha256':I['original_decisions'][cid]['row_sha256'],'artifact':I['original_decisions'][cid]['file']+'#item='+str(I['original_decisions'][cid]['item'])},'native_review':{'reviewer':'/root/review_11870_12250','method':'codex_subagent_direct_source_read','native_contract_sha256':''}}}
  proof['review']['native_review']['native_contract_sha256']=n.native_contract_sha256(proof)
  record=copy.deepcopy(after);record['content']['role_evidence']=proof
  n.validate(record,CAT,catalog_sha256=CH,corpus=S)
  CHECKS.append({'ordinal':ordinal,'full_source_validation':True,'proof_sha256':c.digest(proof),'native_signature':proof['review']['native_review']['native_contract_sha256']})
 ROWS.append({'candidate_id':cid,'ordinal':ordinal,'status':status,'rationale':rationale,'source_before':before,'source_after':after,'delta':delta(before,after,'Exact assigned INPUT original-to-current correction, freshly whole-source reviewed. '+rationale),'original_compiled':I['original_decisions'][cid],'proof':proof,'dependency_records':{},'reference_bindings':{},'source_reread_complete':True,'reference_reread_complete':True,'revision':{'prior_review':revision['prior_review'],'memo_artifacts':revision['memo_artifacts'],'rationale':'Fresh formal02 whole-source/native-namespace/owner/effect review. '+rationale}})
row(1290,'approved','Fresh whole original/current/full5B/memo/own binding and weather fullspec read. Explicit current existing scene uses common subject/entity P; sticky tropical heat is selected declared-weather effect, not measured temperature/humidity, body sweat, country or summer date. Qualitative heat remains exact weather meaning under this source contract, no sensory-proxy substitution. All strings same E assignment. Source conditions empty; unrestricted weather .56 display-only.',[
 F('sceneP','application_contract','independently declared scene','subject','scene','entity.presence','prerequisite','entity.presence/v1','present',[]),
 F('weatherEn','en','sticky tropical heat','atmosphere','scene','weather.declared','effect','weather.declared/v1','sticky_tropical_heat',['sceneP'],'set_value',[]),
 F('weatherKo','ko','끈적한 열대성 더위','atmosphere','scene','weather.declared','effect','weather.declared/v1','sticky_tropical_heat',['sceneP'],'set_value',[]),
 F('weatherEmb','embedding_text','sticky tropical heat','atmosphere','scene','weather.declared','effect','weather.declared/v1','sticky_tropical_heat',['sceneP'],'set_value',[]),
 F('weatherApp','application_contract','Apply the stated sticky tropical heat as declared weather','atmosphere','scene','weather.declared','effect','weather.declared/v1','sticky_tropical_heat',['sceneP'],'set_value',[])],[('weather',['weatherEn','weatherKo','weatherEmb','weatherApp'],['effect'])],[('scene','scene')],[unit('en',['weatherEn']),unit('ko',['weatherKo']),unit('embedding_text',['weatherEmb']),unit('application_contract',['sceneP','weatherApp'])])
row(1291,'approved','Fresh whole original/current/full5B/memo/own binding and presentation_style fullspec read. Existing person/main_subject common entity P, selected fresh campus-student-like presentation is appearance E; not actual enrollment/age/campus location or specific clothes. Human intrinsic remains; optional/direct presentation .7 human and documentary/craft/wildlife/product/jewelry/food deny is role-only condition, no bypass by new unbound tag.',[
 F('personP','application_contract','independently declared existing person','subject','person','entity.presence','prerequisite','entity.presence/v1','present',[]),
 F('styleEn','en','fresh campus-student styling','appearance','person','presentation.style','effect','presentation.style/v1','fresh_campus_student_like',['personP'],'set_value',[]),
 F('styleKo','ko','대학생 같은 산뜻한 스타일','appearance','person','presentation.style','effect','presentation.style/v1','fresh_campus_student_like',['personP'],'set_value',[]),
 F('styleApp','application_contract','Select fresh campus-student-like styling','appearance','person','presentation.style','effect','presentation.style/v1','fresh_campus_student_like',['personP'],'set_value',[])],[('presentation_style',['styleEn','styleKo','styleApp'],['effect'])],[('person','main_subject')],[unit('en',['styleEn']),unit('ko',['styleKo']),unit('application_contract',['personP','styleApp'])])
row(1292,'approved','Fresh whole original/current/full5B/memo/own binding and prop/prop_state/narrative_clue fullspec read. Same existing paper crane at primary_prop retains exact custom props.type paper_crane P; no live bird or new prop. Folded state, left-behind disposition and authored signal-token clue function remain three actual role/concept effects, including contextual clue role. No actor/group, sending/decoding success or completed communication inferred. Source human intrinsic retained; unrestricted prop .85 display policy. Corrected Korean preserves left behind.',[
 F('craneP','application_contract','independently declared existing paper crane','subject','crane','props.type','prerequisite','props.type/v1','paper_crane',[]),
 F('craneEnP','en','paper crane','subject','crane','props.type','prerequisite','props.type/v1','paper_crane',[]),
 F('foldEn','en','folded','role','crane','prop.state','effect','prop.state/v1','folded',['craneP'],'set_value',[]),
 F('leftEn','en','left behind','role','crane','prop.state.disposition','effect','prop.state.disposition/v1','left_behind',['craneP'],'set_value',[]),
 F('signalEn','en','as a signal token','concept','crane','narrative.clue.function','effect','narrative.clue.function/v1','signal_token',['craneP'],'set_value',[]),
 F('craneKoP','ko','종이학','subject','crane','props.type','prerequisite','props.type/v1','paper_crane',[]),
 F('foldKo','ko','접힌','role','crane','prop.state','effect','prop.state/v1','folded',['craneP'],'set_value',[]),
 F('leftKo','ko','남겨진','role','crane','prop.state.disposition','effect','prop.state.disposition/v1','left_behind',['craneP'],'set_value',[]),
 F('signalKo','ko','신호 토큰으로','concept','crane','narrative.clue.function','effect','narrative.clue.function/v1','signal_token',['craneP'],'set_value',[]),
 F('foldApp','application_contract','Select its folded state','role','crane','prop.state','effect','prop.state/v1','folded',['craneP'],'set_value',[]),
 F('leftApp','application_contract','left-behind disposition','role','crane','prop.state.disposition','effect','prop.state.disposition/v1','left_behind',['craneP'],'set_value',[]),
 F('signalApp','application_contract','as a signal token','concept','crane','narrative.clue.function','effect','narrative.clue.function/v1','signal_token',['craneP'],'set_value',[])],[('prop',['craneEnP','craneKoP','craneP'],['prerequisite']),('prop_state',['foldEn','leftEn','foldKo','leftKo','foldApp','leftApp'],['effect']),('narrative_clue',['signalEn','signalKo','signalApp'],['effect'])],[('crane','primary_prop')],[unit('en',['craneEnP','foldEn','leftEn','signalEn']),unit('ko',['craneKoP','foldKo','leftKo','signalKo']),unit('application_contract',['craneP','foldApp','leftApp','signalApp'])])
row(1293,'approved','Fresh whole original/current/full5B/memo/own binding and hair_style/hair_color fullspec read. Same explicitly existing owned hair at primary_hair uses exact common subject/anatomy.hair.presence present, no biological/wig origin inference. Long length, wavy form, local black color and naturally flowing arrangement are real appearance effects. Arrangement has positive Korean/application evidence only; do not borrow into shorter English. Same-property assignments identical across strings. No wind/movement/new hair or identity change. Human source intrinsic retained; old hair_style1 human/deny product,jewelry,food,wildlife display gate preserved for presentation; new hair_color support does not bypass source guard.',[
 F('hairP','application_contract','independently declared existing owned hair','subject','hair','anatomy.hair.presence','prerequisite','anatomy.hair.presence/v1','present',[]),
 F('lengthEn','en','long','appearance','hair','hair.length','effect','hair.length/v1','long',['hairP'],'set_value',[]),
 F('styleEn','en','wavy','appearance','hair','hair.style','effect','hair.style/v1','wavy',['hairP'],'set_value',[]),
 F('colorEn','en','black hair','appearance','hair','hair.color','effect','hair.color/v1','black',['hairP'],'set_value',[]),
 F('lengthKo','ko','긴','appearance','hair','hair.length','effect','hair.length/v1','long',['hairP'],'set_value',[]),
 F('styleKo','ko','웨이브','appearance','hair','hair.style','effect','hair.style/v1','wavy',['hairP'],'set_value',[]),
 F('colorKo','ko','블랙 헤어','appearance','hair','hair.color','effect','hair.color/v1','black',['hairP'],'set_value',[]),
 F('flowKo','ko','자연스럽게 흐르는','appearance','hair','hair.strands.arrangement','effect','hair.strands.arrangement/v1','naturally_flowing',['hairP'],'set_value',[]),
 F('lengthApp','application_contract','Select long length','appearance','hair','hair.length','effect','hair.length/v1','long',['hairP'],'set_value',[]),
 F('styleApp','application_contract','wavy form','appearance','hair','hair.style','effect','hair.style/v1','wavy',['hairP'],'set_value',[]),
 F('colorApp','application_contract','black local hair color','appearance','hair','hair.color','effect','hair.color/v1','black',['hairP'],'set_value',[]),
 F('flowApp','application_contract','naturally flowing visual arrangement','appearance','hair','hair.strands.arrangement','effect','hair.strands.arrangement/v1','naturally_flowing',['hairP'],'set_value',[])],[('hair_style',['lengthEn','styleEn','lengthKo','styleKo','flowKo','lengthApp','styleApp','flowApp'],['effect']),('hair_color',['colorEn','colorKo','colorApp'],['effect'])],[('hair','primary_hair')],[unit('en',['lengthEn','styleEn','colorEn']),unit('ko',['lengthKo','styleKo','colorKo','flowKo']),unit('application_contract',['hairP','lengthApp','styleApp','colorApp','flowApp'])])
row(1294,'approved','Fresh whole original/current/full5B/memo/own binding and location fullspec read. Exact existing scene/current scene address uses common subject/entity P. Apartment-door threshold location selected, all en/ko/embedding/application same actual effect; no resident, entry/exit action or whole unseen apartment interior. Conditions empty; location .58 unrestricted display-only.',[
 F('sceneP','application_contract','independently declared scene','subject','scene','entity.presence','prerequisite','entity.presence/v1','present',[]),
 F('locEn','en','apartment door threshold','setting','scene','setting.location','effect','setting.location/v1','apartment_door_threshold',['sceneP'],'set_value',[]),
 F('locKo','ko','아파트 현관 문턱','setting','scene','setting.location','effect','setting.location/v1','apartment_door_threshold',['sceneP'],'set_value',[]),
 F('locEmb','embedding_text','apartment door threshold','setting','scene','setting.location','effect','setting.location/v1','apartment_door_threshold',['sceneP'],'set_value',[]),
 F('locApp','application_contract','Select the apartment-door threshold','setting','scene','setting.location','effect','setting.location/v1','apartment_door_threshold',['sceneP'],'set_value',[])],[('location',['locEn','locKo','locEmb','locApp'],['effect'])],[('scene','scene')],[unit('en',['locEn']),unit('ko',['locKo']),unit('embedding_text',['locEmb']),unit('application_contract',['sceneP','locApp'])])
if __name__=='__main__':
 out=R/'authored/native_11870_formal02_checkpoint_01290_01295.json';assert not out.exists();payload={'schema':'photo-native-manual-review-small-checkpoint/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','assignment_sha256':c.digest(A),'input_sha256':c.digest(I),'actual_read_count':5,'records':ROWS,'full_source_checks':CHECKS,'boundary':'Small checkpoint only; no full50 batch/runtime acceptance.'};out.write_text(json.dumps(payload,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(str(out),c.digest(payload));print('5source proofs validated')
