"""Use the recognized whole positive application-contract field, preserving noise semantics."""
import copy, gzip, hashlib, json, sys
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
sys.dont_write_bytecode=True;sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c, photo_semantic_evidence as n
sys.path.insert(0,str(R));import prepare_native_inputs as prep
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
def read(p):return json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def save(p,v):
 with p.open('xb')as f:f.write(c.canonical_bytes(v)+b'\n')
def ref(p):return {'file':str(p.relative_to(ROOT)),'file_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'sha256':c.digest(read(p))}
parent=R/'native-inputs/root-noise-canonical-source-plan-12';current=read(parent/'CURRENT-PROPOSAL.json.gz');original=read(R/'SOURCE.json.gz')
assert c.digest(current)=='a72e46dcc1830046dd6f12ad31465c0de2c2e548bc1e199791b613c594f7a8bb'
cid='cand_f1251d5df8735a3d83381e34a2d70b34';before=copy.deepcopy(current['candidates'][cid]);after=copy.deepcopy(before)
after['content']['application_contract']=after['content'].pop('application_scope')
assert after['effects']==before['effects']==original['candidates'][cid]['effects']
reason='Fresh native manual-role-view validation rejects an ordinary unit on application_scope, which is not a recognized primary positive field. Move the exact unchanged, individually read application text into the native application_contract field. Preserve every literal statement, actual original rendering.noise/image_plane effect, condition, provenance and source ID. No validation relaxation or engine edit.'
D=R/'native-inputs/root-noise-contract-source-plan-13';D.mkdir(exist_ok=False)
memo={'schema':'photo-root-native-input-field-repair/v1','actor':'/root','candidate_id':cid,'reason':reason,'before_source':before,'after_source':after,
 'failed_script':'review_noise_canonical_root_02.py','failed_script_raw_sha256':hashlib.sha256((R/'review_noise_canonical_root_02.py').read_bytes()).hexdigest(),
 'error':'ValueError: ordinary unit must be the exact full positive field','native_proof_written':False,'production_changes':0,'operating_changes':0,'Gemini_calls':0}
save(D/'ROOT-FIELD-REPAIR.json',memo);current['candidates'][cid]=after
approval=read(parent/'SOURCE-APPROVAL.json');choice=next(row for row in approval['changes']if row['candidate_id']==cid)
choice['after']=after;choice['reason']+=' '+reason;choice['provenance'].append(ref(D/'ROOT-FIELD-REPAIR.json'))
choice['delta']=[{'pointer':'/content','before_exists':True,'before':choice['before']['content'],'after_exists':True,'after':after['content'],'reason':choice['reason']}]
approval['current_source_sha256']=c.digest(current);approval['reason']+=' Exact noise application text uses the native whole-positive application_contract field; no semantic or proof conversion.'
prep.approve_source(ROOT,original,current,approval);c.validate(current)
with (D/'CURRENT-PROPOSAL.json.gz').open('xb')as f:f.write(gzip.compress(c.canonical_bytes(current),mtime=0))
save(D/'SOURCE-APPROVAL.json',approval)
plan=read(parent/'PLAN-03169.json');plan['current_proposal']=ref(D/'CURRENT-PROPOSAL.json.gz');plan['source_approval']=ref(D/'SOURCE-APPROVAL.json')
plan['required_revisions'][cid]['memo_artifacts'].append(ref(D/'ROOT-FIELD-REPAIR.json'));plan['required_revisions'][cid]['reason']+=' '+reason;plan['reason']+=' '+reason
save(D/'PLAN-03169.json',plan);out,receipt=prep.write_inputs(ref(D/'PLAN-03169.json'),'root-03169-149-03',actor='/root',root=ROOT,here=R)
save(D/'ROOT-PREPARATION-VERIFICATION.json',{'current_proposal':ref(D/'CURRENT-PROPOSAL.json.gz'),'source_approval':ref(D/'SOURCE-APPROVAL.json'),
 'exact_application_text_unchanged':before['content']['application_scope']==after['content']['application_contract'],'original_noise_effects_preserved':True,
 'source_changes_total':len(approval['changes']),'prepared':str(out.relative_to(ROOT)),'native_proofs_created':0,'operating_changes':0,'Gemini_calls':0})
print(json.dumps({'prepared':str(out),'source_sha256':c.digest(current),'native_proofs_created':0}))
