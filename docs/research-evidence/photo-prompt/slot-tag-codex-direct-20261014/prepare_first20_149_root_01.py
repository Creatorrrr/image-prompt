"""Freeze new direct-review input only; no semantic decisions or proofs are produced."""
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
D=R/'native-inputs/first20-catalog149-recheck-plan-15';D.mkdir(exist_ok=False)
parent=R/'native-inputs/root-hands-exchange-source-plan-14';current=read(parent/'CURRENT-PROPOSAL.json.gz')
assert c.digest(current)=='8acdd741cdb846c8bb33b53ded16471363ece5747280b5b4893c25acdeed302d'
oldplan=read(R/'native-inputs/root-00000-00020-plan-01/PLAN.json');prior=R/'native_batches/root-00000-00020-01/BATCH.json';batch=read(prior)
assert len(batch['records'])==20
memo={'schema':'photo-root-native-semantic-reopen/v1','actor':'/root','prior_batch':ref(prior),
 'reason':'Fresh first20 direct semantic/native review on exact149V6 and frozen50fd92 engine. Historical7 approvals and13 pending remain historical; no status transfer.',
 'requirements':['Read full original/current/exact5B/ownbindings/closure and all actual positive fields before comparing tags; read each used149 fullspec and actual neighbor boundaries.',
 'Write fresh source-bound facts/units, actual effects and complete receivers, typed prerequisites/owner guards, all matching roles. Do not re-sign a historical144 proof or treat metadata as positive evidence.',
 'Preserve original canonical actual effect properties/owners/conditions. Do not rename properties for slot-prefix fit; same-fact manual role views may be explicitly justified after full effect review.',
 'For ambiguous or coarse lighting/capture/theme sources, write exact before/after source proposals and reasons after full source reading. No source choice is authorized by input preparation; root must select changes before a new prepared input.',
 'No invented light/person/pet/food/anatomical owner, fixed total count or existing desired value from candidate text. Preserve lab/travel/pet/food/interior qualifiers and all literal meanings; no diagnostic conversion for mere ambiguity.',
 'No discarded E or ordinary-field coverage, false stronger quotes, shadow effects, automatic fallback, compatibility shortcuts or model calls.',
 'Use independently authored controlled actual-source full/compact tests including original properties, aliases, ancestor/property/whole locks and actual binding conditions. Distinguish fixtures from real request/runtime/pixels.',
 'Leave unresolved rows pending with exact source/contract gap. No operating source/code/runtime/Git/model/network changes.'],
 'input_preparation_semantic_reads_claimed':0,'native_proofs_created':0,'operating_changes':0,'Gemini_calls':0}
save(D/'ROOT-REVIEW-REQUIREMENTS.json',memo)
plan=copy.deepcopy(oldplan);plan['assignment']={'task_name':'/root/review_06250_07250','model':'gpt-6.1-sol','reasoning_effort':'high','start':0,'end':20,'ids':oldplan['assignment']['ids']}
plan['catalog_approval']=ref(R/'NATIVE-CATALOG-APPROVAL-149-V6.json');plan['current_proposal']=ref(parent/'CURRENT-PROPOSAL.json.gz');plan['source_approval']=ref(parent/'SOURCE-APPROVAL.json');plan['reason']=memo['reason']
plan['required_revisions']={row['candidate_id']:{'prior_review':{'artifact':ref(prior),'pointer':'/records/'+str(i),'sha256':c.digest(row)},'memo_artifacts':[ref(D/'ROOT-REVIEW-REQUIREMENTS.json')],'reason':memo['reason']}for i,row in enumerate(batch['records'])}
save(D/'PLAN.json',plan);out,receipt=prep.write_inputs(ref(D/'PLAN.json'),'review06250-00000-00020-149-02',actor='/root',root=ROOT,here=R)
report={'schema':'photo-root149-input-preparation/v1','plan':ref(D/'PLAN.json'),'current_source':ref(parent/'CURRENT-PROPOSAL.json.gz'),'prepared':str(out.relative_to(ROOT)),'records':20,'source_changes_created':0,'actual_new_semantic_reads':0,'native_proofs_created':0,'operating_changes':0,'Gemini_calls':0,'frozen_engine':str(G),'photo_module_paths':{k:str(Path(v.__file__).resolve())for k,v in sys.modules.items()if k.startswith('photo_')and getattr(v,'__file__',None)}}
assert all(Path(v).is_relative_to(G) for v in report['photo_module_paths'].values());save(D/'ROOT-PREPARATION-VERIFICATION.json',report)
print(json.dumps({k:report[k]for k in ['prepared','records','source_changes_created','native_proofs_created','operating_changes','Gemini_calls']}))
