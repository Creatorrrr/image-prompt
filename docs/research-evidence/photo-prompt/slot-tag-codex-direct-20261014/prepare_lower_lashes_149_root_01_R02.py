"""Select one explicit existing-lash application for fresh review only."""
import copy,gzip,hashlib,json,sys
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014';G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
sys.dont_write_bytecode=True;sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c,photo_semantic_evidence as n
sys.path.insert(0,str(R));import prepare_native_inputs as prep
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
def read(p):return json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def save(p,v):
 with p.open('xb')as f:f.write(c.canonical_bytes(v)+b'\n')
def ref(p):return {'file':str(p.relative_to(ROOT)),'file_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'sha256':c.digest(read(p))}
proposal=R/'authored/native_extra_10250_11250.10350_10375.source_proposals.json';assert hashlib.sha256(proposal.read_bytes()).hexdigest()=='c5783df1e9aafe29dda1c88a1524d554b8982844010e16fd15256c860c76c056';row=read(proposal)['records'][0];assert row['ordinal']==10352
parent=R/'native-inputs/root-hands-exchange-source-plan-14';current=read(parent/'CURRENT-PROPOSAL.json.gz');original=read(R/'SOURCE.json.gz');assert c.digest(current)=='8acdd741cdb846c8bb33b53ded16471363ece5747280b5b4893c25acdeed302d'
cid=row['candidate_id'];before=row['source_before'];after=row['source_after'];assert before==current['candidates'][cid]==original['candidates'][cid]
assert c.digest(after)=='3900d47c518df63bc0c8cca949b0aa0a32edd06fba3734cc08712b543e634a6c';assert before['conditions']==after['conditions'] and before['effects']==after['effects'] and before['provenance']==after['provenance']
assert {k:x for k,x in after['content'].items()if k!='application_contract'}==before['content']
D=R/'native-inputs/root-lower-lashes-source-plan-16-R02';D.mkdir(exist_ok=False)
reason=('Root selects a disclosed narrower application of the actual lower-lash source: lengthen independently existing lower-lash strands on their same independently grounded lower-lid margin, preserving actual root connection. '
 'This excludes creation/false-lash alternatives and does not claim those alternatives never existed in the old short label. '
 'Keep exact appearance/main_subject/face.eyelashes.lower_length and all original and actual receiver locks; retain all old positive relation fields and intrinsic human/domain conditions. '
 'Root has read full original/current/exact5B/ownbinding/emptyclosure and actual provenance entry, the entire proposed App after, full lash/anatomical/hair/makeup and garment neighbor specs. '
 'This selects source text only; native facts, preservation witnesses, possible anatomical-connection role and complete actual receivers must be independently authored and reviewed. '
 'Preservation does not create upper lashes or other parts that are not independently present. No actual desired long length may be prefrozen as a prerequisite.')
memo={'schema':'photo-root-bounded-source-selection/v1','actor':'/root','candidate_id':cid,'ordinal':10352,'proposal':ref(proposal),'decision':'selected_source_literal_for_fresh_review_only','whole_before':before,'whole_after':after,'reason':reason,
 'unselected_other_proposals':[{'ordinal':r['ordinal'],'candidate_id':r['candidate_id'],'decision':'unselected_pending_complete_actual_part_footprint_and_preservation_review'}for r in read(proposal)['records'][1:]],
 'requirements':['Fresh whole-source/current/exact5B/ownbinding/closure/149 fullspec direct semantic review; historical approved5B is not a native proof.',
 'Do not derive lower lashes, lower lid, their root connection, eye shape or face from human category, alias, same-owner label or desired candidate E. Existing rooted-lash carrier and actual parent/part relations require independent typed source-bound witnesses.',
 'Preservation of root association must be an actual equality/protection contract, not discarded as mere context. Consider anatomical_connection only on a genuine source-supported same-fact preservation/witness relation; no shadow E, property rename or fake guard support.',
 'Actual main_subject original property, every lower-lash/lid physical receiver and all ancestor/alias/whole locks remain conjunctive. No relocation to a child owner or synonym E. Unknown actual affected scope keeps pending.',
 'Explicitly show missing/wrong owner or lower lid/root relation, desired long value as fake P, original canonical property lock with child open, child lock with broad owner open, aliases/ancestor/whole locks and unchanged preservation contradictions in full/compact actual-source checks.',
 'No new part creation, source-selected complete anatomy subset, inference/model/Gemini/network, production code, operating source, Git or runtime changes.'],
 'native_proofs_created':0,'operating_changes':0,'Gemini_calls':0}
save(D/'ROOT-SOURCE-SELECTION.json',memo);current['candidates'][cid]=copy.deepcopy(after);approval=read(parent/'SOURCE-APPROVAL.json');approval['changes'].append({'candidate_id':cid,'before':before,'after':after,'delta':[{'pointer':'/content/application_contract','before_exists':False,'before':None,'after_exists':True,'after':after['content']['application_contract'],'reason':reason}],'reason':reason,'provenance':[ref(proposal),ref(D/'ROOT-SOURCE-SELECTION.json')]});approval['current_source_sha256']=c.digest(current);approval['reason']+=' Root explicitly selects existing-lower-lashes application literal only, no native/operating approval.'
prep.approve_source(ROOT,original,current,approval);c.validate(current)
with (D/'CURRENT-PROPOSAL.json.gz').open('xb')as f:f.write(gzip.compress(c.canonical_bytes(current),mtime=0))
save(D/'SOURCE-APPROVAL.json',approval)
packet=R/'packets/10250-250.json';prior=R/'decisions/review_09250_10500_10250_10500.json';oldrow=read(prior)['decisions'][102];assert oldrow['candidate_id']==cid
selection={'schema':prep.SELECTION,'actor':'/root','original_source_sha256':c.digest(original),'records':{cid:{'locator':{'file':str(prior.relative_to(ROOT)),'file_sha256':hashlib.sha256(prior.read_bytes()).hexdigest(),'item':103,'row_sha256':c.digest(oldrow)},'packet':ref(packet),'reason':'Root explicitly selects exact old compiled10352 row and full original10250 packet as historical comparison only.'}},'reason':'Actual original source and exact old5B remain immutable; no historical approval transfer.'};save(D/'ORIGINAL-SELECTION.json',selection)
base=read(R/'native-inputs/root-hands-exchange-source-plan-14/PLAN.json');base.update(current_proposal=ref(D/'CURRENT-PROPOSAL.json.gz'),source_approval=ref(D/'SOURCE-APPROVAL.json'),original_selection=ref(D/'ORIGINAL-SELECTION.json'),assignment={'task_name':'/root/review_05250_06250','model':'gpt-6.1-sol','reasoning_effort':'high','start':10352,'end':10353,'ids':[cid]},required_revisions={cid:{'prior_review':{'artifact':ref(prior),'pointer':'/decisions/102','sha256':c.digest(oldrow)},'memo_artifacts':[ref(D/'ROOT-SOURCE-SELECTION.json')],'reason':reason}},reason=reason);save(D/'PLAN.json',base)
out,receipt=prep.write_inputs(ref(D/'PLAN.json'),'review05250-10352-149-01',actor='/root',root=ROOT,here=R)
save(D/'ROOT-PREPARATION-VERIFICATION.json',{'prepared':str(out.relative_to(ROOT)),'selected':cid,'source':ref(D/'CURRENT-PROPOSAL.json.gz'),'only_changed_from_parent':cid,'source_changes_total':len(approval['changes']),'catalog_changed':False,'bindings_changed':False,'native_proofs_created':0,'operating_changes':0,'Gemini_calls':0})
print(json.dumps({'prepared':str(out),'source_sha256':c.digest(current),'source_changes_total':len(approval['changes']),'native_proofs_created':0}))
