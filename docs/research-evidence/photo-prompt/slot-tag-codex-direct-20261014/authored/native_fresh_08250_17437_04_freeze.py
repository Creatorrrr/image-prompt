"""Serialize individually read precision cases and explicit pending disposition.

Old facts are provenance only. They never generate new proof facts/roles/units.
The new proof was authored independently in the adjacent draft module.
"""
import copy,hashlib,json,runpy
from pathlib import Path
M=runpy.run_path(str(Path(__file__).with_name('native_fresh_08250_17437_04_draft.py')))
R=M['R'];s=M['s'];c=M['c'];nr=M['nr'];CID=M['CID'];P=M['P'];I=M['I'];ASS=M['ASS'];PROOF=M['PROOF'];T=M['T'];BEFORE=M['BEFORE']
history_path=R/'authored/native_resolution_08250_17437_field_local_reanchor_design_01.json'
history=json.loads(history_path.read_text())
by_id={f['id']:f for f in PROOF['facts']}
# Explicit manually reviewed index spans and dispositions, after every actual
# quote/target/property/value/mode and its full current field was displayed.
POLICIES=[
 (0,6,'A1_cheek_gate_anaphora','cheek_color',['cheek_color','cheek'],
  'Keep gate owner/local bounded-cue and exclusions as a selected-output reference to exact selected warm-color E and named cheek P. No literal heat, cosmetic pigment, private emotion or duplicate state E.'),
 (6,60,'A2_rival_only_paraphrases','role',['role','adult','expression'],
  'Keep this actual adult/rival outward descriptor as a short partial restatement of the exactly declared peer-rival canonical role. Rival alone is never a direct peer-rival scalar witness, nor permission for another person. Local outward context remains a separate directly supported C fact.'),
 (60,96,'A3_canonical_expression_from_anatomy_gate','expression',['expression','eye_effect','pose'],
  'Use exact haughty smug poised baseline in selected common gate3 as full E anchor. Gate1 retains directly named eyelid/brow/mouth P plus explicit owner/readability reference. No full expression from part names. Face part_of actor guard stays exact; its additional anatomical_connection tag remains technically uncertified.'),
 (96,153,'A4_face_age_from_optional_baseline','keep_face',['eye_effect','expression'],
  'Whole-face adult preservation remains directly anchored at selected common instruction. The optional-only eye/baseline fragment is a continuing-selected-baseline condition, never an independent whole-face-age preservation witness or incoming haughty-eye P. Full EN/KO repeat bodies retain their own explicit whole-face clause by same-selected-output reference; local optional instructions/gates keep only their actual narrower readable baseline constraints.'),
 (153,189,'A5_fresh_only_styling_gate','style',['style','expression','age_effect'],
  'Fresh-only local gate remains a partial selected styling constraint with full youthful-adult styling at exact selected instruction. Do not borrow youthful styling from age E. Gate3 also independently anchors full facial E, and explicit optionality/morphology/reference exclusions remain.'),
 (189,198,'A6_generic_recovery_gate_goal','recovery_expression',['recovery_expression','recovery_phase','expression'],
  'Canonical goal is exactly superior smirk OR poised composure at this same selected recovery instruction. Generic gate preserves visible attempt/readability and continuing baseline via reference, not a complete independent goal witness. Existing prior disruption P stays separate from current optional events, and success/elapsed sequence/hidden suppression remain excluded.'),
 (198,204,'A7_mouth_gate_brief_qualifier','mouth_warmth',['mouth_warmth','eye_effect','expression'],
  'Keep brief local mouth-corner softening at exact selected positive instruction; the local gate refers to its readable local softening and selected adult haughty eye baseline. It adds no duration, gratitude, cheek color, global smile or incoming haughty-eye condition.')]
LEDGER=[]
for lo,hi,issue,key,local_keys,reason in POLICIES:
    for index in range(lo,hi):
        old=history['exact_occurrence_designs'][index]
        assert old['issue_id']==issue
        before=old['before'];rid=before['realization_id'];pointer=before['pointer']
        # Exact source checks are bookkeeping after manual judgement, not a
        # semantic classifier or proof transformation.
        local=s.positive_string(T,pointer,realization_id=rid)
        assert before['quote'] in local
        canonical=by_id[rid+'_'+key]
        assert canonical['quote'] in s.positive_string(T,canonical['pointer'],realization_id=rid)
        normals=[u for u in PROOF['source_units'] if u['realization_id']==rid and u['pointer']==canonical['pointer'] and u['disposition']=='semantic' and canonical['id'] in u['fact_refs']]
        assert len(normals)==1
        refs=[u for u in PROOF['source_units'] if u['realization_id']==rid and u['pointer']==pointer and u['disposition']=='semantic_reference']
        assert len(refs)==1
        LEDGER.append({'reviewed_occurrence_index':index,'issue_id':issue,'historical_fact_id':old['original_fact_id'],'historical_fact_sha256':old['original_fact_sha256'],'realization_id':rid,'exact_local_pointer':pointer,'exact_local_quote':local,'historical_narrow_quote':before['quote'],'historical_mode':before['mode'],'historical_target':before['target'],'historical_property':before['property'],'historical_typed_value':before['value'],'manual_disposition':reason,'fresh_canonical_fact':canonical,'fresh_normal_anchor_unit':normals[0],'fresh_local_reference_unit':refs[0],'local_constraint_fact_ids':[rid+'_'+x for x in local_keys],'local_read_distinct_from_full_canonical_witness':True,'source_after_edited':False})
assert len(LEDGER)==204 and {x['reviewed_occurrence_index'] for x in LEDGER}==set(range(204))
precision={'schema':'photo-native-fresh-precision-resolution/v1','task_name':ASS['task_name'],'model':ASS['model'],'reasoning_effort':ASS['reasoning_effort'],'candidate_id':CID,'formal_input':'review08250-17437-04','catalog_sha256':c.digest(M['CAT']),'source_meaning_sha256':s.meaning_sha256(T),'historical_design':{'file':str(history_path),'raw_sha256':hashlib.sha256(history_path.read_bytes()).hexdigest()},'actual_individually_reviewed_occurrences':204,'manual_read_views':[[0,54],[54,105],[105,156],[156,204]],'read_boundary':'Every indexed quote/target/property/value/mode and proposed anchor was individually displayed; complete actual source fields and all18 selected bodies were separately directly read with exact-repeat/delta factoring. Each repeated policy application is a literal reviewed decision, not generated semantic inference. The old204 full requires lists were not newly displayed individually; actual fresh requirements are separately authored and checked from whole selected source. No claim that old3633 raw occurrences were individually reread.','resolutions':LEDGER,'additional_role_gap':M['GAP'],'candidate_status':'pending','formal_proof':None,'native_signature_or_approval_derived_from_this_ledger':False}
out=R/'authored/native_fresh_08250_17437_04_precision.json';assert not out.exists();out.write_text(json.dumps(precision,ensure_ascii=False,indent=2)+'\n')

def delta(before,after,p=''):
    if c.canonical_bytes(before)==c.canonical_bytes(after):return []
    if isinstance(before,dict) and isinstance(after,dict):
        out=[]
        for k in sorted(set(before)|set(after)):
            path=p+'/'+k.replace('~','~0').replace('/','~1')
            if k not in before:out.append(dict(pointer=path,before_exists=False,before=None,after_exists=True,after=after[k],reason='Exact formal root-selected proposal after complete original/current/18RID reread; no worker source change.'))
            elif k not in after:out.append(dict(pointer=path,before_exists=True,before=before[k],after_exists=False,after=None,reason='Exact formal root-selected proposal after complete original/current/18RID reread; no worker source change.'))
            else:out+=delta(before[k],after[k],path)
        return out
    return [dict(pointer=p,before_exists=True,before=before,after_exists=True,after=after,reason='Exact formal root-selected proposal after complete original/current/18RID reread; no worker source change.')]

ROW={'candidate_id':CID,'ordinal':17437,'status':'pending','rationale':'The complete source and all18 choices preserve declared adult peer-rival/owned face, mandatory youthful-adult age/eye/expression/style/bearing effects, adult-range preservation, explicit named anatomy P and independent selected events/helper/local warmth/recovery. All204 historical narrow-anchor cases now have individually reviewed full-value canonical anchors and retained local reference interpretations in separate unsigned research artifacts. A further actual role is justified: face explicitly part_of actor fits146V5 anatomical_connection, but current role fact_refs cannot certify this existing owner_relation guard without fabricating an extra scalar P/value. Candidate approval therefore remains pending this bounded role-evidence technical gap. No source/E/guard/profile/lock was removed or relabeled to obtain approval.','source_before':BEFORE,'source_after':T,'delta':delta(BEFORE,T),'original_compiled':I['original_decisions'][CID],'proof':None,'dependency_records':{},'reference_bindings':{},'source_reread_complete':True,'reference_reread_complete':True,'revision':{'prior_review':I['required_revisions'][CID]['prior_review'],'memo_artifacts':I['required_revisions'][CID]['memo_artifacts'],'rationale':'Fresh146V5 original/current/18RID/compiled item188/empty binding closure/whole specs review. Prior03 worker positive status and root semantic reopen reasons remain immutable. All204 precision cases directly reviewed and separately resolved as research; selected expression full E anchored to gate3 exact haughty smug poised baseline. Additional anatomical ownership role has no current non-scalar guard-evidence route, so this formal04 row is pending/proof null. No automatic old-proof/catalog/status conversion or guard weakening.'}}
B={'schema':nr.BATCH,'task_name':ASS['task_name'],'model':ASS['model'],'reasoning_effort':ASS['reasoning_effort'],'assignment_sha256':c.digest(ASS),'input_sha256':c.digest(I),'prepared_count':1,'actual_read_count':1,'records':[ROW]}
N={'schema':nr.NOTE,'task_name':ASS['task_name'],'model':ASS['model'],'reasoning_effort':ASS['reasoning_effort'],'assignment_sha256':c.digest(ASS),'input_sha256':c.digest(I),'batch_sha256':c.digest(B),'prepared_count':1,'actual_read_count':1,'whole_source_read_ids':[CID],'whole_dependency_read_ids':[CID]}
O=R/'native_batches/review08250-17437-04';O.mkdir(parents=True,exist_ok=True)
for name,obj in [('BATCH.json',B),('NOTE.json',N)]:
    p=O/name;assert not p.exists();p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
v=nr.verify_batch(P/'ASSIGNMENT.json',O/'BATCH.json',O/'NOTE.json')
v={k:x for k,x in v.items() if k!='records'}
check=R/'authored/native_fresh_08250_17437_04_batch_verification.json';assert not check.exists();check.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'precision_raw_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'batch_sha256':c.digest(B),'note_sha256':c.digest(N),'status':'pending','proof':None,'shape_valid':v['shape_valid']}))
