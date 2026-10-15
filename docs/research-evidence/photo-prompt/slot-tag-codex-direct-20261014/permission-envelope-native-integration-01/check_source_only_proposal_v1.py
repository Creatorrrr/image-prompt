"""Pure actual full-snapshot schema check of unselected execution opt-in proposal."""
import copy,gzip,hashlib,json,sys
from pathlib import Path
sys.path[:0]=[str(Path.cwd()/'skills/photo-prompt-image-generator/scripts')]
import photo_candidate_corpus as c,photo_semantic_evidence as n
O=Path(__file__).parent;proposal=json.loads((O/'SOURCE-OPTIN-PROPOSAL-v1.json').read_text());p=Path(proposal['current_snapshot']['file']);raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==proposal['current_snapshot']['file_sha256'];data=json.loads(gzip.decompress(raw));assert c.digest(data)==proposal['current_snapshot']['sha256'];cid=proposal['candidate_id'];assert data['candidates'][cid]==proposal['before'];data['candidates'][cid]=copy.deepcopy(proposal['after']);c.validate(data)
x={'schema':'photo-native-permission-source-only-proposal-check/v1','candidate_id':cid,'source_snapshot_before_sha256':proposal['current_snapshot']['sha256'],
 'proposal_after_sha256':c.digest(proposal['after']),'whole_snapshot_proposal_sha256':c.digest(data),'full_schema_validation':'PASS',
 'native_status':n.native_status(data['candidates'][cid]),'source_only_approval':False,'root_selection':False,'native_proof':None,
 'boundary':'Actual full current source snapshot plus unselected literal proposal was validated in memory. Source-only opt-in syntax is compatible with Stage5C preparation; original effect-address declaration and ordinary pointers checked. No future fact values/roles/actual scope semantics proven, no snapshot saved, no operating/source/runtime change.',
 'module_pins':{str(Path(m.__file__)):hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest()for m in [c,n]},'network_denied':True,'model_calls':0}
p=O/'SOURCE-ONLY-PROPOSAL-CHECK-v1.json';assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');print(c.digest(x));print(x['native_status'])
