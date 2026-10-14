"""Freeze fresh manual05 judgement after full selected-source review and checks.

Historical204 occurrences are exact provenance only; no old proof is loaded.
The explicit new05 fact/unit literals were separately read and checked.
"""
import copy,hashlib,json,runpy,sys
from pathlib import Path
M=runpy.run_path(str(Path(__file__).with_name('native_fresh_08250_17437_05_author.py')))
R=M['R'];s=M['s'];c=M['c'];CID=M['CID'];P=M['P'];I=M['I'];ASS=M['ASS'];T=M['T'];BEFORE=M['BEFORE'];GEN=M['GEN'];CAT=M['CAT']
sys.path[:0]=[str(GEN/'scripts'),str(GEN/'precore'),str(R)]
import native_reviews as nr
assert Path(nr.native.__file__).resolve().is_relative_to(GEN)
CHECK=json.loads((R/'authored/native_fresh_08250_17437_05_checks.json').read_text())
assert CHECK['source_units']==786 and CHECK['scalar_facts']==483 and CHECK['guard_supports']==18
PROOF=copy.deepcopy(M['PROOF'])
PROOF['review']['basis']='Fresh formal05 original/current/complete exact5B/item188/empty ownbindings and candidate/binding closure; all18 whole selected bodies and actual modes/value/owner/requirements/effects/guards/profile contracts directly reviewed. All204 historical precision occurrences individually addressed with exact-repeat and RID-prefix display factoring; fresh483 scalar facts and786 units were read by actual RID using reversible exact display normalization and duplicate antecedents. No claim of483 ungrouped raw repetitions or historical3633 raw-fact reread. Canonical normal full-field/substring anchors retain full values; local partial/output/owner constraints are explicit one-hop references without new facts. Existing face part_of actor uses exact source guard support, no scalar identity invention. Independent frozen188c full/compact/admission/property+dimension+receiver/ancestor lock/profile/guard/role checks completed separately. This worker source judgement is not root acceptance or operating qualification.'
PROOF['review']['native_review']['native_contract_sha256']=s.native_contract_sha256(PROOF)
by_id={f['id']:f for f in PROOF['facts']}
hp=R/'authored/native_resolution_08250_17437_field_local_reanchor_design_01.json';H=json.loads(hp.read_text())
POLICIES=[
(0,6,'A1_cheek_gate_anaphora','cheek_color','The bounded-cue gate retains locality/ownership/exclusions through same-RID selected-output reference to the instruction full visible warm-color E and cheek P. No heat/makeup/health/private emotion or duplicate state E.'),
(6,60,'A2_rival_only_paraphrases','role','Rival-only local descriptors remain partial restatements; exact already-declared adult peer-rival role P is anchored at the selected common instruction. Outward descriptor C remains separate, without new person or private personality.'),
(60,96,'A3_canonical_expression_from_anatomy_gate','expression','Selected common gate3 exactly states haughty smug poised baseline and supplies canonical full expression E. Anatomy gate1 retains named part P and readability/owner references. Exact face part_of actor is separately supported by source-guard provenance and anatomical_connection role; no scalar identity or new geometry E.'),
(96,153,'A4_face_age_from_optional_baseline','keep_face','Full adult-face preservation stays at selected common instruction; narrow optional eye/baseline fragments retain only continuing selected baseline/readability references. Whole EN/KO repeat bodies retain their own whole clauses. No local eye phrase is an independent whole-face-age witness or incoming haughty-eye P.'),
(153,189,'A5_fresh_only_styling_gate','style','Full fresh youthful adult styling E stays at exact selected instruction; shorter fresh-only gate is a partial selected-output constraint. Separate youthful-adult age E remains actual age permission scope, never a style or adult-allowed substitute.'),
(189,198,'A6_generic_recovery_gate_goal','recovery_expression','Canonical selected instruction requires visible attempt to restore superior smirk OR poised composure. Generic gate retains attempt/readability and continuing baseline through reference, with independent prior-disruption P. No completed recovery or forced selected setback/help/warmth.'),
(198,204,'A7_mouth_gate_brief_qualifier','mouth_warmth','Brief local mouth-corner softening is directly anchored at exact selected instruction. Narrow gate retains local softening/readable selected adult haughty baseline through reference; no gratitude/global smile/cheek color/extra duration or eye-state P.')]
LEDGER=[]
for lo,hi,issue,key,reason in POLICIES:
 for index in range(lo,hi):
  old=H['exact_occurrence_designs'][index];b=old['before'];rid=b['realization_id'];pointer=b['pointer'];assert old['issue_id']==issue
  local=s.positive_string(T,pointer,realization_id=rid);assert b['quote'] in local
  f=by_id['g05_'+rid+'_'+key]
  normal=[u for u in PROOF['source_units'] if u['realization_id']==rid and u['pointer']==f['pointer'] and u['disposition']=='semantic' and f['id'] in u['fact_refs']];assert len(normal)==1
  refs=[u for u in PROOF['source_units'] if u['realization_id']==rid and u['pointer']==pointer and u['disposition']=='semantic_reference'];assert len(refs)==1
  LEDGER.append(dict(reviewed_occurrence_index=index,issue_id=issue,historical_fact_id=old['original_fact_id'],historical_fact_sha256=old['original_fact_sha256'],historical_narrow_fact=b,realization_id=rid,exact_local_pointer=pointer,exact_local_full_text=local,manual_disposition=reason,fresh_canonical_fact=f,fresh_normal_anchor=normal[0],fresh_local_reference=refs[0],source_after_edited=False))
assert len(LEDGER)==204
precision={'schema':'photo-native-fresh-precision-resolution/v2','task_name':ASS['task_name'],'model':ASS['model'],'reasoning_effort':ASS['reasoning_effort'],'formal_input':'review08250-17437-05','candidate_id':CID,'source_meaning_sha256':s.meaning_sha256(T),'catalog_sha256':c.digest(CAT),'history_file':str(hp),'history_raw_sha256':hashlib.sha256(hp.read_bytes()).hexdigest(),'actual_individually_rejudged_occurrences':204,'read_boundary':'Every index actual RID/quote/property/target/mode/value/canonical anchor/local retained constraint was reviewed. Lossless exact-repeat/RID-prefix display factoring with roundtrip assertions was used; not204 ungrouped raw repeat claims. Old requires were not individually reprinted; new explicit requires were separately authored and reviewed. Old proof never generates new facts or status.','resolutions':LEDGER,'root_accepted':False,'operating_qualified_count':0}
pp=R/'authored/native_fresh_08250_17437_05_precision.json';assert not pp.exists();pp.write_text(json.dumps(precision,ensure_ascii=False,indent=2)+'\n')
def delta(b,a,p=''):
 if c.canonical_bytes(b)==c.canonical_bytes(a):return []
 if isinstance(b,dict) and isinstance(a,dict):
  out=[]
  for k in sorted(set(b)|set(a)):
   q=p+'/'+k.replace('~','~0').replace('/','~1')
   if k not in b or k not in a:out.append(dict(pointer=q,before_exists=k in b,before=b.get(k),after_exists=k in a,after=a.get(k),reason='Exact root-selected formal05 source, after whole original/current reread; no worker source change.'))
   else:out+=delta(b[k],a[k],q)
  return out
 return [dict(pointer=p,before_exists=True,before=b,after_exists=True,after=a,reason='Exact root-selected formal05 source, after whole original/current reread; no worker source change.')]
ROW={'candidate_id':CID,'ordinal':17437,'status':'approved','rationale':'Direct fresh whole-source judgement: explicit four required common components and three independent optional groups retain actual18 selected layouts, declared adult peer-rival/own face, adult body/face prerequisites and preservation, youthful-adult age effect, fresh styling, half-lidded eye effect, haughty-smug-poised baseline and poised bearing. Selected help requires independently present distinct helper and keeps both action owners; setback is a current E, recovery requires independently declared disruption and remains attempt not success, brief mouth softening and bounded visible cheek-color are independent alternatives without heat/private emotion or duplicate skin state. All204 narrow-quote cases retain local constraints through same-RID one-hop references to exact normal full-value anchors. New source-guard supports certify existing face part_of same actor for anatomical_connection without scalar entityID or effect invention. Whole effect set, receiver lists, guards, profile obligations and lock scope are preserved. Worker research approval remains separate from root semantic acceptance and operating activation.','source_before':BEFORE,'source_after':T,'delta':delta(BEFORE,T),'original_compiled':I['original_decisions'][CID],'proof':PROOF,'dependency_records':{},'reference_bindings':{},'source_reread_complete':True,'reference_reread_complete':True,'revision':{'prior_review':I['required_revisions'][CID]['prior_review'],'memo_artifacts':I['required_revisions'][CID]['memo_artifacts'],'rationale':'Fresh formal05 review rather than old04 re-sign: original/current whole source, exact historical5B/item188, empty ownbinding and referenced closure, all18 selected bodies, used/neighbor full146V5 specs, every204 precision entry and new483facts/786units reviewed. Exact sourceguard part_of relation now has frozen188c guard_refs support; no scalar prerequisite fabrication, effect/context conversion or guard weakening. Sourceafter is exact root INPUT; old04 pending/null and unsigned evidence remain unchanged.'}}
B={'schema':nr.BATCH,'task_name':ASS['task_name'],'model':ASS['model'],'reasoning_effort':ASS['reasoning_effort'],'assignment_sha256':c.digest(ASS),'input_sha256':c.digest(I),'prepared_count':1,'actual_read_count':1,'records':[ROW]}
N={'schema':nr.NOTE,'task_name':ASS['task_name'],'model':ASS['model'],'reasoning_effort':ASS['reasoning_effort'],'assignment_sha256':c.digest(ASS),'input_sha256':c.digest(I),'batch_sha256':c.digest(B),'prepared_count':1,'actual_read_count':1,'whole_source_read_ids':[CID],'whole_dependency_read_ids':[CID]}
O=R/'native_batches/review08250-17437-05';O.mkdir(parents=True,exist_ok=True)
for name,obj in [('BATCH.json',B),('NOTE.json',N)]:
 p=O/name;assert not p.exists();p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
v=nr.verify_batch(P/'ASSIGNMENT.json',O/'BATCH.json',O/'NOTE.json');v={k:x for k,x in v.items() if k!='records'}
vp=R/'authored/native_fresh_08250_17437_05_batch_verification.json';assert not vp.exists();vp.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'batch_canonical_sha256':c.digest(B),'batch_raw_sha256':hashlib.sha256((O/'BATCH.json').read_bytes()).hexdigest(),'note_canonical_sha256':c.digest(N),'note_raw_sha256':hashlib.sha256((O/'NOTE.json').read_bytes()).hexdigest(),'precision_raw_sha256':hashlib.sha256(pp.read_bytes()).hexdigest(),'verification':v},ensure_ascii=False))
