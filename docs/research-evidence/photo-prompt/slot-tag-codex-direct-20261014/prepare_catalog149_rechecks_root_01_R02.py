"""New research input only: exact accepted149 catalog plus unchanged62 source choices."""
import copy,gzip,hashlib,json,sys
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014';G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/694ba2cc064e0eae2ae0d24603f37250577122cd4a700ae10f6e379ec9057609')
sys.dont_write_bytecode=True;sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c,photo_semantic_evidence as native
sys.path.insert(0,str(R));import prepare_native_inputs as prep
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
assert Path(prep.reviews.native.__file__).resolve().is_relative_to(G)
def read(p):return json.loads(gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_bytes())
def save(p,v):
 with p.open('xb') as f:f.write(c.canonical_bytes(v)+b'\n')
def ref(p):
 b=p.read_bytes();return {'file':str(p.relative_to(ROOT)),'file_sha256':hashlib.sha256(b).hexdigest(),'sha256':c.digest(read(p))}
D=R/'native-inputs/catalog149-source-pool-plan-09';assert {p.name for p in D.iterdir()} == {'CURRENT-PROPOSAL.json.gz','SOURCE-APPROVAL.json','ROOT-PREPARATION-FAILURE-01.json'}
parent=R/'native-inputs/bare-prop-applications-plan-06';current=read(parent/'CURRENT-PROPOSAL.json.gz');old_catalog=c.digest(current['slot_catalog']);current['slot_catalog']=read(R/'CATALOG-FINAL-149-V6.json');assert c.digest(current['slot_catalog'])=='d9f4db418e1b63cd100b4c7a9fbff4c8401e00dffeffd22e299a0b5087a82b15'
assert (D/'CURRENT-PROPOSAL.json.gz').read_bytes()==gzip.compress(c.canonical_bytes(current),mtime=0)
approval=read(parent/'SOURCE-APPROVAL.json');approval['current_source_sha256']=c.digest(current);approval['reason']+=' New research preparation replaces only146 catalog with separately approved149V6; exact62 source choices, every binding and policy remain byte-identical. No new source meaning/proof/status/operating approval.'
original=read(R/'SOURCE.json.gz');prep.approve_source(ROOT,original,current,approval);c.validate(current);assert read(D/'SOURCE-APPROVAL.json')==approval
prior=R/'native_batches/review08250-17437-05/BATCH.json';batch=read(prior);cid=batch['records'][0]['candidate_id'];proof=batch['records'][0]['proof'];bad=[]
for idx in [174,303,435,565,661,757]:
 u=proof['source_units'][idx];assert 'bounded cheek cue' in u['quote'];assert len(u['fact_refs'])==4
 bad.append({'source_unit_index':idx,'complete_before':u,'proposed_fact_refs':u['fact_refs'][:2],'reason':'Gate states cheek ownership/color/confusion boundary only; eye and expression baseline effects remain in actual full instructions and their separate ordinary/reference source units.'})
memo={'schema':'photo-root-native-semantic-reopen/v1','actor':'/root','prior_batch':ref(prior),'candidate_id':cid,'peer_report':ref(R/'worker-notes/native-09250-special17437-05-peer-20261015.review.json'),'peer_instruction_addendum':ref(R/'worker-notes/native-09250-special17437-05-peer-20261015.cheek-instruction-addendum.json'),'required_repairs':bad,'source_change_selected':False,'requirements':'Fresh direct semantic review on exact149V6 prepared input. Preserve all483 actual facts, all138 effects with their actual modes/targets/Rx, all18 branches/conditions/adult/owners/guard supports. Narrow only these6 overbroad reference fields after re-reading complete actual fields and related full instructions. No automatic proof re-sign or old status change. Optional instrument remains conditional; no mandatory tool invention or claim of tool-bearing runtime qualification. New source approval or operating activation0.'}
save(D/'ROOT-17437-REOPEN.json',memo)
plan=read(R/'native-inputs/guard-support-rechecks-plan-07-R02/PLAN-17437.json');plan['catalog_approval']=ref(R/'NATIVE-CATALOG-APPROVAL-149-V6.json');plan['current_proposal']=ref(D/'CURRENT-PROPOSAL.json.gz');plan['source_approval']=ref(D/'SOURCE-APPROVAL.json');plan['reason']='New direct149V6 source recheck after peer six gate-reference holds; no source/proof/status conversion from preparation.';plan['required_revisions']={cid:{'prior_review':{'artifact':ref(prior),'pointer':'/records/0','sha256':c.digest(batch['records'][0])},'memo_artifacts':[ref(D/'ROOT-17437-REOPEN.json')],'reason':'Fresh entire source/proof review; repair six unsupported baseline references while retaining all actual original effects, guards and qualifiers.'}}
save(D/'PLAN-17437.json',plan);out,receipt=prep.write_inputs(ref(D/'PLAN-17437.json'),'review08250-17437-06',actor='/root',root=ROOT,here=R)
report={'schema':'photo-root149-research-preparation-verification/v1','parent_proposal':ref(parent/'CURRENT-PROPOSAL.json.gz'),'new_proposal':ref(D/'CURRENT-PROPOSAL.json.gz'),'prior_catalog_sha256':old_catalog,'catalog_sha256':c.digest(current['slot_catalog']),'candidates_equal_parent':current['candidates']==read(parent/'CURRENT-PROPOSAL.json.gz')['candidates'],'bindings_equal_parent':current['slot_bindings']==original['slot_bindings'],'policies_equal_parent':current['policies']==original['policies'],'candidate_changes_from_original':len(approval['changes']),'prepared17437':str(out.relative_to(ROOT)),'actual_new_semantic_reads':0,'native_proof_created':False,'operating_changes':0,'model_and_Gemini_calls':0,'frozen_engine':str(G)};assert report['candidates_equal_parent'] and report['bindings_equal_parent'] and report['policies_equal_parent'];save(D/'ROOT-PREPARATION-VERIFICATION.json',report);print(json.dumps(report,ensure_ascii=False))
