"""Fresh146V5 direct review; canonical selected facts and manual one-hop references.

No previous proof is loaded or converted. Literal repetition covers the two
individually reread actual choices; it performs no semantic classification.
"""
import copy, hashlib, json, sys
from pathlib import Path

R=Path(__file__).resolve().parents[1]
FROZEN=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/2ad7b2bfd3f4d730985c23ed89e3513a326a0a2ceea22aecfe28cb5d05c98ac9')
sys.path[:0]=[str(FROZEN/'scripts'),str(FROZEN/'precore'),str(R)]
import photo_candidate_corpus as c
import photo_candidate_realizations as rr
import photo_semantic_evidence as s
import native_reviews as nr
sys.path[:0]=[str(FROZEN/'scripts'),str(FROZEN/'precore')]
assert Path(s.__file__).is_relative_to(FROZEN)
assert hashlib.sha256(Path(s.__file__).read_bytes()).hexdigest()=='0f4a974435f7cb9e71a23a726f092bff73d0dd61bb9deb3df2537f59d5be15e4'
P=R/'native-inputs/prepared/review08250-11128-05';O=R/'native_batches/review08250-11128-05'
I=json.loads((P/'INPUT.json').read_text());ASS=json.loads((P/'ASSIGNMENT.json').read_text());PACK=json.loads((P/'PREPARED-PACKET.json').read_text());CID=ASS['ids'][0]
BEFORE=PACK['original_records'][CID];AFTER=PACK['current_records'][CID];CAT=I['catalog_review']['after'];OLD=PACK['historical_compiled_rows'][CID]
assert c.digest(CAT)=='3655a006e69500662987c829361711a7194c3e297bfc4c408297bcf94f35d645'
F=[];U=[];M={}

def fact(rid,key,p,q,d,prop,mode,value,requires):
    row={'id':rid+'_'+key,'realization_id':rid,'pointer':p,'quote':q,'dimension':d,
         'target':'main_subject','property':prop,'mode':mode,
         'value':{'type':prop+'/v1','value':value},'requires':requires}
    if mode=='effect':row.update(operation='set_value',receivers=[])
    assert q in s.positive_string(AFTER,p,realization_id=rid)
    F.append(row);return row['id']

def normal(rid,p,refs):
    U.append({'realization_id':rid,'pointer':p,'quote':s.positive_string(AFTER,p,realization_id=rid),
              'fact_refs':refs,'disposition':'semantic' if refs else 'nonsemantic'})

def reference(rid,p,refs,relation,rationale):
    U.append({'realization_id':rid,'pointer':p,'quote':s.positive_string(AFTER,p,realization_id=rid),
              'fact_refs':refs,'disposition':'semantic_reference','reference_relation':relation,
              'retained_constraint_rationale':rationale})

# Explicit values/quotes after each actual source/RID was read. Neither the
# common OR phrase nor another language supplies a missing canonical qualifier.
choices=[('standing','natural standing posture','자연스럽게 서 있는 자세','natural_standing'),
         ('walking','natural walking posture','자연스럽게 걷는 자세','natural_walking')]
for rid,pose_en,pose_ko,pose_value in choices:
    root='/content/realization_content/'+rid
    present=fact(rid,'present',root+'/relations/0/subject','the established adult subject',
                 'subject','entity.presence','prerequisite','present',[])
    adult=fact(rid,'adult',root+'/en','adult','age','age.declared','prerequisite','adult',[present])
    required=[present,adult]
    wardrobe=fact(rid,'wardrobe',root+'/en','wearing a pencil skirt','appearance','wardrobe.ensemble','effect','pencil_skirt',required)
    pose=fact(rid,'pose_en',root+'/en',pose_en,'pose','body.pose','effect',pose_value,required)
    ko_pose=fact(rid,'pose_ko',root+'/ko',pose_ko,'pose','body.pose','effect',pose_value,required)
    activity=[];ko_activity=[]
    if rid=='walking':
        activity=[fact(rid,'walking_en',root+'/en','walking','action','action.walking','effect','walking',required)]
        ko_activity=[fact(rid,'walking_ko',root+'/ko','걷는','action','action.walking','effect','walking',required)]
    canonical=[adult,wardrobe,pose]+activity
    normal(rid,root+'/en',canonical)
    normal(rid,root+'/ko',[ko_pose]+ko_activity)
    reference(rid,root+'/ko',[adult,wardrobe],'selected_output_constraint',
              'This selected Korean body explicitly says 성인이 and 펜슬 스커트 차림; it constrains the same adult wearer/outfit. Its own natural posture (and walking activity when selected) has direct Korean facts at this field, not a borrowed English qualifier.')
    normal(rid,root+'/relations/0/subject',[present])
    reference(rid,root+'/relations/0/subject',[adult],'same_selected_owner',
              'The established adult subject is the same already frozen wearer named by this selected body. This local adult-owner phrase does not add a person, establish identity from appearance or authorize an age mutation.')
    for p in ['/content/concept_units/0','/content/en','/content/ko','/content/relations/0/object']:
        reference(rid,p,canonical,'partial_restatement',
                  'The common source explicitly gives adult, pencil skirt and natural standing OR walking. It permits only the actual selected '+rid+' alternative here, rather than independently forcing both poses or claiming that the common OR field alone fixes one canonical assignment. Common Korean itself includes 자연스럽게. The same selected owner, outfit and allowed natural posture remain required; only selected walking carries walking activity.')
    reference(rid,'/content/relations/0/subject',[present,adult],'same_selected_owner',
              'The common relation names the established adult subject and scene elements. It refers to this same frozen wearer; every other actually mentioned element outside the declared changes must already be established under the retained application guard. It creates no additional scene object/place/person and no compulsory reference image or fixed identity.')
    for p in [root+'/concept_units/0',root+'/embedding_text']:
        reference(rid,p,canonical,'selected_output_constraint',
                  'This complete selected positive body repeats exactly the adult wearer, pencil-skirt outfit and natural '+rid+' posture of the canonical selected English body. It retains those actual output constraints without adding another effect assignment or borrowing an unselected sibling.')
    reference(rid,root+'/relations/0/object',[wardrobe,pose]+activity,'selected_output_constraint',
              'The selected relation object explicitly says wearing a pencil skirt in a natural '+rid+' posture. It constrains that same selected visible configuration; adulthood and presence belong to the separately named established owner, and standing never acquires walking activity.')
    normal(rid,'/content/relations/0/type',[])
    normal(rid,root+'/relations/0/type',[])
    M[rid]={'schema':s.OWNER_SCHEMA,'bindings':[{'target':'main_subject','core_role':'main_subject','origin':'existing','introduced_by':None}]}
    assert {u['pointer'] for u in U if u['realization_id']==rid}==s.primary_paths(AFTER,rid)

def role(tag,rids,refs,modes,scope='whole_record'):
    return {'spec_sha256':c.digest(CAT[tag]),'scope':scope,'realization_ids':rids,'fact_refs':refs,'support_modes':modes}

ROLES={'age_presentation':role('age_presentation',['standing','walking'],['standing_adult','walking_adult'],['prerequisite']),
       'wardrobe_style':role('wardrobe_style',['standing','walking'],['standing_wardrobe','walking_wardrobe'],['effect']),
       'body_pose':role('body_pose',['standing','walking'],['standing_pose_en','standing_pose_ko','walking_pose_en','walking_pose_ko'],['effect']),
       'action':role('action',['walking'],['walking_walking_en','walking_walking_ko'],['effect'],'positive_alternative')}
LOC=I['original_decisions'][CID]
PROOF={'schema':s.SCHEMA,'meaning_sha256':s.meaning_sha256(AFTER),'catalog_sha256':c.digest(CAT),
       'complete':True,'facts':F,'roles':ROLES,'owner_maps':M,'source_units':U,
       'effect_sets':{rid:s.effect_set(AFTER,rid) for rid in ['standing','walking']},
       'dependencies':{'standing':[],'walking':[]},'reference_sha256':{},
       'guard_sets':{rid:{'source_conditions':[copy.deepcopy(AFTER['conditions']),{}],'member_conditions':{}} for rid in ['standing','walking']},
       'profile_contracts':{'standing':None,'walking':None},
       'review':{'basis':'Fresh146V5 direct reread of original/current whole source, both selected bodies, exact historical compiled row, own binding and empty closure, prior71 facts/26 units and root acceptance reason. Each new canonical fact and each local reference was manually judged. Full canonical posture is directly quoted in selected EN and naturalness-explicit selected KO; common OR is an explicit selected-scope reference. No prior proof is copied or re-signed.',
                 'whole_source_reviewed':True,
                 'source_correction':{'before_sha256':s.meaning_sha256(BEFORE),'after_sha256':s.meaning_sha256(AFTER),'rationale':'Exact root-selected source retains existing adulthood as P, actual wardrobe/posture and walking-only action E, explicit natural Korean and conditional established reference/identity preservation. No reviewer source change.'},
                 'original_review':{'candidate_id':CID,'source_record_sha256':OLD['source_record_sha256'],'catalog_sha256':OLD['catalog_sha256'],'decision_sha256':LOC['row_sha256'],'artifact':LOC['file']+'#item='+str(LOC['item'])},
                 'native_review':{'reviewer':'/root/review_08250_09250','method':'codex_subagent_direct_source_read','native_contract_sha256':''}}}
PROOF['review']['native_review']['native_contract_sha256']=s.native_contract_sha256(PROOF)

def delta(before,after,p=''):
    # Serialization-only exact difference after source meanings were directly read.
    if c.canonical_bytes(before)==c.canonical_bytes(after):return []
    if isinstance(before,dict) and isinstance(after,dict):
        out=[]
        for k in sorted(set(before)|set(after)):
            pointer=p+'/'+k.replace('~','~0').replace('/','~1')
            if k not in before:out.append(dict(pointer=pointer,before_exists=False,before=None,after_exists=True,after=after[k],reason='Exact root-selected current source; complete after directly reread.'))
            elif k not in after:out.append(dict(pointer=pointer,before_exists=True,before=before[k],after_exists=False,after=None,reason='Exact root-selected current source; complete after directly reread.'))
            else:out+=delta(before[k],after[k],pointer)
        return out
    return [dict(pointer=p,before_exists=True,before=before,after_exists=True,after=after,reason='Exact root-selected current source; complete after directly reread.')]

ROW={'candidate_id':CID,'ordinal':11128,'status':'approved',
     'rationale':'The already established adult wearer adopts a pencil-skirt ensemble and exactly one natural standing/walking posture; only walking supplies activity. Conditional reference/identity scope guards preserve all already established values, permit known absence and deny unknown or overlapping whole effects. No new actor, fixed identity, mandatory reference, profession, office, sensual/fetish classification, material, morphology or frame crop is inferred. Four roles retain distinct P/E support under146V5; references only account for explicit same-RID restatements/output/owner constraints.',
     'source_before':BEFORE,'source_after':AFTER,'delta':delta(BEFORE,AFTER),'original_compiled':LOC,'proof':PROOF,
     'dependency_records':{},'reference_bindings':{},'source_reread_complete':True,'reference_reread_complete':True,
     'revision':{'prior_review':I['required_revisions'][CID]['prior_review'],'memo_artifacts':I['required_revisions'][CID]['memo_artifacts'],
                 'rationale':'Fresh source/spec/mode/owner/quote/selected-RID review under root-published semantic-reference runtime2ad7b2... and exact146V5 research input. Prior04 remains immutable history. Canonical selected EN/KO facts and manually authored one-hop local units replace repetitive field assignments without deleting any source condition, profile/choice, actual E or lock. This is not an automatic conversion or whole-source entailment claim from shape.'}}
BATCH={'schema':nr.BATCH,'task_name':ASS['task_name'],'model':ASS['model'],'reasoning_effort':ASS['reasoning_effort'],'assignment_sha256':c.digest(ASS),'input_sha256':c.digest(I),'prepared_count':1,'actual_read_count':1,'records':[ROW]}
NOTE={'schema':nr.NOTE,'task_name':ASS['task_name'],'model':ASS['model'],'reasoning_effort':ASS['reasoning_effort'],'assignment_sha256':c.digest(ASS),'input_sha256':c.digest(I),'batch_sha256':c.digest(BATCH),'prepared_count':1,'actual_read_count':1,'whole_source_read_ids':[CID],'whole_dependency_read_ids':[CID]}

if __name__=='__main__':
    record=copy.deepcopy(AFTER);record['content']['role_evidence']=PROOF
    s.validate(record,CAT,corpus={'candidates':{CID:record},'slot_bindings':{}})
    O.mkdir(parents=True,exist_ok=True)
    for name,value in [('BATCH.json',BATCH),('NOTE.json',NOTE)]:
        p=O/name;assert not p.exists();p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'facts':len(F),'units':len(U),'semantic_references':sum(u['disposition']=='semantic_reference' for u in U),'batch_sha256':c.digest(BATCH),'note_sha256':c.digest(NOTE)}))
