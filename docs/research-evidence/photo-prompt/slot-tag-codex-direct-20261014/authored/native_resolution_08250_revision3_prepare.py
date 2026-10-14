"""Explicitly approved visible youthful-adult age effect; no operating writes."""
import copy,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(Path.cwd()/'skills/photo-prompt-image-generator/scripts'))
import photo_candidate_corpus as c
import photo_semantic_evidence as s
J=json.loads((R/'authored/native_resolution_08250_revision2_sources.json').read_text())
cid='cand_d15b4c6334a45b61a7407a022a2cc8e0';before=J['resolution_proposed_records'][cid];after=copy.deepcopy(before)
AGE='Render a visibly youthful-adult age presentation on the already adult actor; this changes visible age presentation only, without changing declared adulthood or claiming biological age, a numeric age, or child or teen morphology.'
repls=[
 ('Preserve unmistakably adult body and face presentation.','Preserve unmistakably adult body and face presentation. '+AGE),
 ('몸과 얼굴의 명백한 성인 표현을 보존하고','몸과 얼굴의 명백한 성인 표현을 보존한다. 기존 성인 인물의 외관상 연령 표현을 앳돼 보이는 성인으로 나타내되 선언된 성인 여부·생물학적 나이·수치 나이·아동이나 청소년의 체형을 바꾸거나 추론하지 않는다. 이어서'),
 ('The declared peer rival is already unmistakably adult in body and face presentation; this cue changes no age or requester-owned identity.','The declared peer rival is already unmistakably adult in body and face presentation. Render visibly youthful-adult age presentation within that adult range, preserving declared adulthood and requester-owned identity without claiming biological age, a numeric age, or child or teen morphology.'),
 ('poised bearing and fresh youthful adult styling. The already declared peer-rival role','poised bearing and fresh youthful adult styling. '+AGE+' The already declared peer-rival role'),
 ('The common adult peer, haughty smug poised baseline and fresh styling remain mandatory.','The common adult peer, haughty smug poised baseline, fresh styling and visibly youthful-adult age presentation remain mandatory.')]
deltas=[];counts=[0]*len(repls)
def walk(v,p):
 if isinstance(v,dict):return {k:walk(x,p+'/'+k.replace('~','~0').replace('/','~1')) for k,x in v.items()}
 if isinstance(v,list):return [walk(x,p+'/'+str(i)) for i,x in enumerate(v)]
 if not isinstance(v,str):return v
 start=v
 for i,(a,b) in enumerate(repls):
  if a in v:counts[i]+=v.count(a);v=v.replace(a,b)
 if start!=v:deltas.append({'pointer':p,'before':start,'after':v,'reason':'Root-approved preservation of original youthful-adult visible age meaning as an actual age effect, distinct from fresh styling and pre-existing adult declaration. No biological/numeric age or minor morphology claim.'})
 return v
after['content']=walk(after['content'],'/content')
old=copy.deepcopy(after['effects']);after['effects']['dimensions'].append('age');after['effects']['properties'].append({'dimension':'age','target':'actor','property':'age.presentation.youthful_adult'})
deltas.append({'pointer':'/effects','before':old,'after':copy.deepcopy(after['effects']),'reason':'Root explicitly approved common actual visible youthful-adult age presentation effect. Keep adult prerequisites/preservation and all original styling/face/pose/selected effects. This effect requires age mutation permission; equal age values cannot bypass locks.'})
assert all(counts),counts
out=copy.deepcopy(J);out['schema']='native-resolution-semantic-revision/v3';out['supersedes_proposal_file']=str(R/'authored/native_resolution_08250_revision2_sources.json');out['supersedes_record_sha256']=c.digest(before);out['resolution_proposed_records'][cid]=after;out['exact_corrections']={cid:deltas};out['root_adjudication']['youthful_adult_age_effect']='approved common actual visible age effect; adulthood remains a separate existing prerequisite/preservation';out['proposed_meaning_sha256']=s.meaning_sha256(after);out['status']='prepared_revision3_not_yet_reread_or_native_approved';out['age_effect_literal']=AGE
(R/'authored/native_resolution_08250_revision3_sources.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'field_deltas':len(deltas),'literal_occurrences':counts,'meaning_sha256':out['proposed_meaning_sha256'],'prepared_only':True}))
