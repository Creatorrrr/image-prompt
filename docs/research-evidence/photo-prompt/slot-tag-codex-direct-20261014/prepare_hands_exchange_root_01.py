"""Select a disclosed bounded handoff application for a fresh review, never a native approval."""
import copy,gzip,hashlib,json,sys
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
sys.dont_write_bytecode=True;sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c,photo_semantic_evidence as n
sys.path.insert(0,str(R));import prepare_native_inputs as prep
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
def read(p):return json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def save(p,v):
 with p.open('xb')as f:f.write(c.canonical_bytes(v)+b'\n')
def ref(p):return {'file':str(p.relative_to(ROOT)),'file_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'sha256':c.digest(read(p))}
parent=R/'native-inputs/root-noise-contract-source-plan-13';current=read(parent/'CURRENT-PROPOSAL.json.gz');original=read(R/'SOURCE.json.gz')
assert c.digest(current)=='b1af3261d4af57d1635f2522ca656b6277dafaa13d238b1cc39a78e1da0f25d5'
path=R/'authored/native_1299_hands_exchange_application_proposal_03.json';proposal=read(path)
assert hashlib.sha256(path.read_bytes()).hexdigest()=='7cadf761e6618b75b66341ce4fa9365687a4eecb92839bc26b53bb36726710e6'
cid=proposal['candidate_id'];before=proposal['whole_before_source'];after=proposal['whole_proposed_after_source']
assert current['candidates'][cid]==original['candidates'][cid]==before
assert c.digest(after)=='e9870bd290b1bd682d9d79001c29a4affa65a4618ce2ed0cd43d46b0d15cfd33'
assert after['provenance']==before['provenance'] and before['conditions']=={} and before['effects']['properties']==[]
D=R/'native-inputs/root-hands-exchange-source-plan-14';D.mkdir(exist_ok=False)
reason=('Root deliberately chooses the disclosed physical-handoff interpretation of the ambiguous hands-only-exchange label for fresh source review. '
 'EN/KO now state that narrower application: one existing physical item and variable plural independently existing hands, with hands-only participant anatomy and macro coverage. '
 'This is an explicit editorial restriction, not a claim that every old exchange interpretation is preserved or uniquely entailed. '
 'No person, common carrier, fixed total hand count, new anatomy or new item is supplied by this source. '
 'A separately selected independently input-bound complete framing-affected-owner inventory must include every actual affected carrier, part, hand, item and other region. '
 'Its semantic completeness requires direct actual-request review; scope hashes and flags do not prove it. '
 'All performed exchange and framing effects remain mutations with full actual receiver unions and locks; unknown completeness remains ineligible. '
 'Only this source choice is selected for new review, not its proposed fact sketch, native approval or operating activation.')
memo={'schema':'photo-root-bounded-source-selection/v1','actor':'/root','candidate_id':cid,'ordinal':1299,'proposal':ref(path),
 'decision':'selected_source_literal_for_fresh_review_only','reason':reason,'whole_before':before,'whole_after':after,
 'root_read_scope':'Whole original/current1299, ownbinding/old04pending, proposal02after/all intents and03after/map; actual native scope/permission implementation and12 relevant149 fullspecs. No claim to have read all original01 alternative specimens.',
 'constraints':['First50-05 remains bound to source09 and must preserve1299 pending; this separate input does not rewrite it.',
 'Freshly read whole original/current/exact5B/ownbinding/closure/149 specs and every actual positive field. Write exact source-local facts/units/guards/roles, not oldproof re-sign.',
 'Choose explicit independent initiating hand plus complete nonempty other-hands scope. No fixed anatomical total, common human carrier, inferred ownership or candidate-created subset.',
 'Freeze and directly review the complete actual affected framing scope from exact request inputs before discovery; include actual owned non-hand regions/carriers when affected. No inventory label/complete flag as semantic proof.',
 'Demonstrate actual different/same carriers, more than one other hand, actual kind/presence, disjoint guards, overlapping receiver-union preservation, missing/stale/incomplete inventory rejection and every receiver/ancestor/property/whole lock.',
 'Use all original canonical properties if present; original1299 has no nonempty property. Do not create shadow E for role prefix or waive actual additional contact/placement/ownership mutations.',
 'Report any remaining complete-scope or applicability gap as pending. No new production code, operating source, runtime, Git or model calls.'],
 'native_proofs_created':0,'operating_changes':0,'Gemini_calls':0}
save(D/'ROOT-SOURCE-SELECTION.json',memo)
current['candidates'][cid]=copy.deepcopy(after);approval=read(parent/'SOURCE-APPROVAL.json')
approval['changes'].append({'candidate_id':cid,'before':before,'after':after,'delta':[{'pointer':'/'+key,'before_exists':True,'before':before[key],'after_exists':True,'after':after[key],'reason':reason}for key in before if before[key]!=after[key]],
 'reason':reason,'provenance':[ref(path),ref(D/'ROOT-SOURCE-SELECTION.json')]})
approval['current_source_sha256']=c.digest(current);approval['reason']+=' Root selects one explicit bounded1299 source application for fresh semantic/native review; previous1299pending unchanged.'
prep.approve_source(ROOT,original,current,approval);c.validate(current)
with (D/'CURRENT-PROPOSAL.json.gz').open('xb')as f:f.write(gzip.compress(c.canonical_bytes(current),mtime=0))
save(D/'SOURCE-APPROVAL.json',approval)
firstplan=read(R/'native-inputs/first50-catalog149-recheck-plan-10/PLAN.json');oldselection=read(ROOT/firstplan['original_selection']['file'])
selection={'schema':prep.SELECTION,'actor':'/root','original_source_sha256':c.digest(original),'records':{cid:copy.deepcopy(oldselection['records'][cid])},'reason':'Exact1299 old original compiled selection remains historical; new bounded literal requires fresh direct review.'}
save(D/'ORIGINAL-SELECTION.json',selection);prior=R/'native_batches/review11870-01250-01300-04/BATCH.json';oldrow=read(prior)['records'][49]
assert oldrow['candidate_id']==cid and oldrow['status']=='pending'
plan={'schema':prep.PLAN,'actor':'/root','original_snapshot':firstplan['original_snapshot'],'current_proposal':ref(D/'CURRENT-PROPOSAL.json.gz'),
 'order':firstplan['order'],'catalog_approval':firstplan['catalog_approval'],'source_approval':ref(D/'SOURCE-APPROVAL.json'),
 'original_selection':ref(D/'ORIGINAL-SELECTION.json'),'assignment':{'task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','start':1299,'end':1300,'ids':[cid]},
 'required_revisions':{cid:{'prior_review':{'artifact':ref(prior),'pointer':'/records/49','sha256':c.digest(oldrow)},'memo_artifacts':[ref(D/'ROOT-SOURCE-SELECTION.json')],'reason':reason}},'reason':reason}
save(D/'PLAN.json',plan);out,receipt=prep.write_inputs(ref(D/'PLAN.json'),'review11870-01299-149-06',actor='/root',root=ROOT,here=R)
save(D/'ROOT-PREPARATION-VERIFICATION.json',{'current_proposal':ref(D/'CURRENT-PROPOSAL.json.gz'),'source_approval':ref(D/'SOURCE-APPROVAL.json'),
 'only_changed_from_parent':cid,'original_source_corrections_total':len(approval['changes']),'prepared':str(out.relative_to(ROOT)),
 'native_proofs_created':0,'catalog_changed':False,'bindings_changed':False,'operating_changes':0,'Gemini_calls':0})
print(json.dumps({'prepared':str(out),'source_sha256':c.digest(current),'source_changes_total':len(approval['changes']),'native_proofs_created':0}))
