"""Fresh manual literal review of exact formal 11128 source; no old-proof conversion."""
import copy,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[3]
FROZEN=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/1871bafa0e008e186ccce4e92908f2b177529b215c22e2fb46d07f0b28679bfd')
sys.path[:0]=[str(R),str(FROZEN/'scripts')]
import photo_candidate_corpus as c
import photo_candidate_realizations as rr
import photo_semantic_evidence as s
import native_reviews as nr
sys.path[:0]=[str(FROZEN/'scripts'),str(FROZEN/'precore')]
P=R/'native-inputs/prepared/review08250-11128-02';O=R/'native_batches/review08250-11128-02'
I=json.loads((P/'INPUT.json').read_text());ASS=json.loads((P/'ASSIGNMENT.json').read_text());PACK=json.loads((P/'PREPARED-PACKET.json').read_text());CID=ASS['ids'][0]
BEFORE=PACK['original_records'][CID];AFTER=PACK['current_records'][CID];CAT=I['catalog_review']['after'];OLD=PACK['historical_compiled_rows'][CID]
F=[];U=[];M={}
def f(rid,key,p,q,d,prop,mode,typ,v,req):
 row=dict(id=rid+'_'+key,realization_id=rid,pointer=p,quote=q,dimension=d,target='main_subject',property=prop,mode=mode,value={'type':typ,'value':v},requires=req)
 if mode=='effect':row.update(operation='set_value',receivers=[])
 assert q in s.positive_string(AFTER,p,realization_id=rid)
 F.append(row);return row['id']
for rid in ['standing','walking']:
 root='/content/realization_content/'+rid
 presence=f(rid,'present','/content/relations/0/subject','the established adult subject','subject','entity.presence','prerequisite','entity.presence/v1','present',[])
 adult=f(rid,'adult','/content/en','adult','age','age.declared','prerequisite','age.declared/v1','adult',[presence])
 req=[presence,adult]
 # Each tuple explicitly identifies its own language's actual clauses. The
 # root OR is scoped to the actual chosen RID, never a union of both effects.
 passages=[('/content/concept_units/0','adult','wearing a pencil skirt','natural standing or walking posture',True),('/content/en','adult','wearing a pencil skirt','natural standing or walking posture',True),('/content/ko','성인','펜슬 스커트 차림','서 있거나 걷는 전체 자세',False),('/content/relations/0/object','adult','wearing a pencil skirt','natural standing or walking posture',True),
 (root+'/concept_units/0','adult','wearing a pencil skirt','natural '+rid+' posture',True),(root+'/embedding_text','adult','wearing a pencil skirt','natural '+rid+' posture',True),(root+'/en','adult','wearing a pencil skirt','natural '+rid+' posture',True),(root+'/ko','성인','펜슬 스커트 차림','자연스럽게 서 있는 자세' if rid=='standing' else '자연스럽게 걷는 자세',True)]
 for n,(p,aq,wq,pq,natural) in enumerate(passages):
  f(rid,f'p{n}_age',p,aq,'age','age.declared','prerequisite','age.declared/v1','adult',[presence])
  f(rid,f'p{n}_wardrobe',p,wq,'appearance','wardrobe.ensemble','effect','wardrobe.ensemble/v1','pencil_skirt',req)
  f(rid,f'p{n}_pose',p,pq,'pose','body.pose','effect','body.pose/v1','natural_'+rid,req)
  if rid=='walking':f(rid,f'p{n}_walking',p,'걷는' if p.endswith('/ko') else 'walking','action','action.walking','effect','action.walking/v1','walking',req)
 # Original common Korean posture quote anchors selected standing/walking only.
 # The exact full selected EN/KO bodies independently supply naturalness; the
 # one canonical same-RID body.pose assignment retains that complete meaning.
 # This shorter quote is not standalone entailment of the natural modifier.
 f(rid,'root_owner_age','/content/relations/0/subject','adult','age','age.declared','prerequisite','age.declared/v1','adult',[presence])
 f(rid,'branch_owner',root+'/relations/0/subject','the established adult subject','subject','entity.presence','prerequisite','entity.presence/v1','present',[])
 f(rid,'branch_age',root+'/relations/0/subject','adult','age','age.declared','prerequisite','age.declared/v1','adult',[presence])
 f(rid,'branch_wardrobe',root+'/relations/0/object','wearing a pencil skirt','appearance','wardrobe.ensemble','effect','wardrobe.ensemble/v1','pencil_skirt',req)
 f(rid,'branch_pose',root+'/relations/0/object','natural '+rid+' posture','pose','body.pose','effect','body.pose/v1','natural_'+rid,req)
 if rid=='walking':f(rid,'branch_walking',root+'/relations/0/object','walking','action','action.walking','effect','action.walking/v1','walking',req)
 # Scope preservation is conditional guard evidence, not an always-present
 # reference/identity fact or a positive contextual role. Its full text remains
 # in the unchanged reviewed source and exact guard_sets below.
 paths=['/content/concept_units/0','/content/en','/content/ko','/content/relations/0/object','/content/relations/0/subject','/content/relations/0/type',root+'/concept_units/0',root+'/embedding_text',root+'/en',root+'/ko',root+'/relations/0/object',root+'/relations/0/subject',root+'/relations/0/type']
 assert set(paths)==s.primary_paths(AFTER,rid)
 for p in paths:
  refs=[x['id'] for x in F if x['realization_id']==rid and x['pointer']==p]
  assert refs or p.endswith('/type')
  U.append(dict(realization_id=rid,pointer=p,quote=s.positive_string(AFTER,p,realization_id=rid),fact_refs=refs,disposition='semantic' if refs else 'nonsemantic'))
 M[rid]={'schema':s.OWNER_SCHEMA,'bindings':[{'target':'main_subject','core_role':'main_subject','origin':'existing','introduced_by':None}]}
def role(tag,rids,ids,modes,scope='whole_record'):
 return dict(spec_sha256=c.digest(CAT[tag]),scope=scope,realization_ids=rids,fact_refs=ids,support_modes=modes)
roles={'age_presentation':role('age_presentation',['standing','walking'],['standing_adult','walking_adult'],['prerequisite']),
 'wardrobe_style':role('wardrobe_style',['standing','walking'],['standing_p1_wardrobe','walking_p1_wardrobe'],['effect']),
 'body_pose':role('body_pose',['standing','walking'],['standing_p1_pose','walking_p1_pose'],['effect']),
 'action':role('action',['walking'],['walking_branch_walking'],['effect'],'positive_alternative')}
for rid in ['standing','walking']:
 assignments={}
 for fact in F:
  if fact['realization_id']!=rid or fact['mode']!='effect':continue
  key=s.property_key(fact);value=c.canonical_bytes({k:fact[k] for k in ['value','operation','receivers']})
  assert key not in assignments or assignments[key]==value
  assignments[key]=value
LOC=I['original_decisions'][CID]
PROOF={'schema':s.SCHEMA,'meaning_sha256':s.meaning_sha256(AFTER),'catalog_sha256':c.digest(CAT),'complete':True,'facts':F,'roles':roles,'owner_maps':M,'source_units':U,'effect_sets':{rid:s.effect_set(AFTER,rid) for rid in ['standing','walking']},'dependencies':{'standing':[],'walking':[]},'reference_sha256':{},'guard_sets':{rid:{'source_conditions':[copy.deepcopy(AFTER['conditions']),{}],'member_conditions':{}} for rid in ['standing','walking']},'profile_contracts':{'standing':None,'walking':None},'review':{'basis':'Fresh revision02 full exact formal INPUT source/original compiled judgement/current source/spec/own-binding/condition/two-RID/reference reread after root single-assignment correction request. Each clause mode/value/owner/requires is explicitly reviewed. Conditional preservation is exact v4 source guard, not an unconditional reference prerequisite.','whole_source_reviewed':True,'source_correction':{'before_sha256':s.meaning_sha256(BEFORE),'after_sha256':s.meaning_sha256(AFTER),'rationale':'Explicit selected standing/walking bodies and complete wardrobe/pose/walking footprint; existing adulthood is a prerequisite rather than an age mutation. Preserve reference/identity only when independently established, with unknown state requiring review.'},'original_review':{'candidate_id':CID,'source_record_sha256':OLD['source_record_sha256'],'catalog_sha256':OLD['catalog_sha256'],'decision_sha256':LOC['row_sha256'],'artifact':LOC['file']+'#item='+str(LOC['item'])},'native_review':{'reviewer':'/root/review_08250_09250','method':'codex_subagent_direct_source_read','native_contract_sha256':''}}}
PROOF['review']['native_review']['native_contract_sha256']=s.native_contract_sha256(PROOF)
def delta(before,after,p=''):
 # Mechanical exact tree difference only, after authored source is fixed.
 if c.canonical_bytes(before)==c.canonical_bytes(after):return []
 if isinstance(before,dict) and isinstance(after,dict):
  out=[]
  for k in sorted(set(before)|set(after)):
   path=p+'/'+k.replace('~','~0').replace('/','~1')
   if k not in before:out.append({'pointer':path,'before_exists':False,'before':None,'after_exists':True,'after':after[k],'reason':'Exact root-selected source correction; complete repaired source reread.'})
   elif k not in after:out.append({'pointer':path,'before_exists':True,'before':before[k],'after_exists':False,'after':None,'reason':'Exact root-selected source correction; complete repaired source reread.'})
   else:out+=delta(before[k],after[k],path)
  return out
 return [{'pointer':p,'before_exists':True,'before':before,'after_exists':True,'after':after,'reason':'Exact root-selected source correction; complete repaired source reread.'}]
ROW={'candidate_id':CID,'ordinal':11128,'status':'approved','rationale':'The existing adult subject adopts the pencil-skirt ensemble and exactly one natural standing or walking posture; only walking adds activity. Both explicit conditional preservation guards retain every established reference/identity scoped value and deny unknown inventory or overlapping whole effects. No mandatory reference, particular scene, occupation, fetish, material, anatomy, count or crop is invented. Owner is the expressly established subject; there are no selected members or referenced records. All source limits remain in exact source.','source_before':BEFORE,'source_after':AFTER,'delta':delta(BEFORE,AFTER),'original_compiled':LOC,'proof':PROOF,'dependency_records':{},'reference_bindings':{},'source_reread_complete':True,'reference_reread_complete':True,'revision':{'prior_review':I['required_revisions'][CID]['prior_review'],'memo_artifacts':I['required_revisions'][CID]['memo_artifacts'],'rationale':'Fresh revision02 full source/spec/compiled/own-binding/guard/selected-RID read explicitly supersedes prior exact BATCH row0. The two generic-Korean posture occurrences now use natural_standing/natural_walking as the single selected canonical assignment, supported by full selected EN and KO. Short common KO alone does not establish naturalness. Source after is unchanged. Independent adult/presence prerequisites and exact conditional scope guards are retained.'}}
BATCH={'schema':nr.BATCH,'task_name':ASS['task_name'],'model':ASS['model'],'reasoning_effort':ASS['reasoning_effort'],'assignment_sha256':c.digest(ASS),'input_sha256':c.digest(I),'prepared_count':1,'actual_read_count':1,'records':[ROW]}
NOTE={'schema':nr.NOTE,'task_name':ASS['task_name'],'model':ASS['model'],'reasoning_effort':ASS['reasoning_effort'],'assignment_sha256':c.digest(ASS),'input_sha256':c.digest(I),'batch_sha256':c.digest(BATCH),'prepared_count':1,'actual_read_count':1,'whole_source_read_ids':[CID],'whole_dependency_read_ids':[CID]}
if __name__=='__main__':
 rec=copy.deepcopy(AFTER);rec['content']['role_evidence']=PROOF;s.validate(rec,CAT,corpus={'candidates':{CID:rec},'slot_bindings':{}})
 O.mkdir(exist_ok=True,parents=True)
 for name,value in [('BATCH.json',BATCH),('NOTE.json',NOTE)]:
  path=O/name;assert not path.exists();path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'facts':len(F),'units':len(U),'batch_sha256':c.digest(BATCH),'note_sha256':c.digest(NOTE)}))
