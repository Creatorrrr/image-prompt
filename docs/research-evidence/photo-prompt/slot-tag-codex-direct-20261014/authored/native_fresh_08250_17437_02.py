"""Fresh current17437 formal read remains pending: proposed color footprint needs new root input."""
import copy,json,sys,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
FROZEN=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/e54254ce78fde43d717a5c6e1670a0ffa5b50050fdafcf4b813930e42ecd0a7f')
sys.path[:0]=[str(FROZEN/'scripts'),str(FROZEN/'precore'),str(R)]
import photo_candidate_corpus as c
import photo_semantic_evidence as native
import native_reviews as nr
sys.path[:0]=[str(FROZEN/'scripts'),str(FROZEN/'precore')]
P=R/'native-inputs/prepared/review08250-17437-02';O=R/'native_batches/review08250-17437-02'
I=json.loads((P/'INPUT.json').read_text());ASS=json.loads((P/'ASSIGNMENT.json').read_text());PACK=json.loads((P/'PREPARED-PACKET.json').read_text());CID=ASS['ids'][0]
def delta(a,b,p=''):
 if c.canonical_bytes(a)==c.canonical_bytes(b):return []
 if isinstance(a,dict) and isinstance(b,dict):
  out=[]
  for k in sorted(set(a)|set(b)):
   path=p+'/'+k.replace('~','~0').replace('/','~1')
   if k not in a:out.append(dict(pointer=path,before_exists=False,before=None,after_exists=True,after=b[k],reason='Exact root-provided formal current source, directly reread.'))
   elif k not in b:out.append(dict(pointer=path,before_exists=True,before=a[k],after_exists=False,after=None,reason='Exact root-provided formal current source, directly reread.'))
   else:out.extend(delta(a[k],b[k],path))
  return out
 return [dict(pointer=p,before_exists=True,before=a,after_exists=True,after=b,reason='Exact root-provided formal current source, directly reread.')]
BEFORE=PACK['original_records'][CID];AFTER=PACK['current_records'][CID]
ROW=dict(candidate_id=CID,ordinal=17437,status='pending',rationale='Fresh full original/current18-RID/profile/conditions/own-binding(empty)/reference(empty)/compiled item188 and144V4 used-spec review confirms primary actor peer-rival prerequisite fits the updated participant_role without an invented counterpart. Required youthful-adult age E and adult/body/face preservation, selected helper distinctness and independent warmth/recovery remain. Direct source names retained eyes, owned eyelids/brow/mouth; explicit atomic existing-anatomy prerequisites need new fact anchors and negative fixtures rather than face-category inheritance. New skin_tone spec independently covers the selected bounded visible local cheek color; current skin.state footprint cannot automatically become a skin.color fact or support an out-of-prefix role. A separate exact source-only color-facet proposal is frozen for root whole-source review and a new formal INPUT. Current source_after stays exact assigned source. No new proof or semantic approval is claimed.',source_before=BEFORE,source_after=AFTER,delta=delta(BEFORE,AFTER),original_compiled=I['original_decisions'][CID],proof=None,dependency_records={},reference_bindings={},source_reread_complete=True,reference_reread_complete=True,revision=dict(prior_review=I['required_revisions'][CID]['prior_review'],memo_artifacts=I['required_revisions'][CID]['memo_artifacts'],rationale='Fresh144V4 whole-source review, not an automatic conversion or promotion of the old142V2 proof. Current formal source remains immutable; unresolved complete source/property/role representation is explicitly pending with null proof.'))
BATCH=dict(schema=nr.BATCH,task_name=ASS['task_name'],model=ASS['model'],reasoning_effort=ASS['reasoning_effort'],assignment_sha256=c.digest(ASS),input_sha256=c.digest(I),prepared_count=1,actual_read_count=1,records=[ROW])
NOTE=dict(schema=nr.NOTE,task_name=ASS['task_name'],model=ASS['model'],reasoning_effort=ASS['reasoning_effort'],assignment_sha256=c.digest(ASS),input_sha256=c.digest(I),batch_sha256=c.digest(BATCH),prepared_count=1,actual_read_count=1,whole_source_read_ids=[CID],whole_dependency_read_ids=[CID])
if __name__=='__main__':
 O.mkdir(exist_ok=True,parents=True)
 for n,v in [('BATCH.json',BATCH),('NOTE.json',NOTE)]:
  p=O/n;assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
 result=nr.verify_batch(str(P/'ASSIGNMENT.json'),str(O/'BATCH.json'),str(O/'NOTE.json'))
 proposal=json.loads((R/'authored/native_resolution_08250_17437_144v4_source_proposal_01.json').read_text())
 assert nr.apply_delta(proposal['source_before'],proposal['native_review_delta'])==proposal['source_after']
 c.validate_effects(proposal['source_after']['effects'],CID)
 for branch in proposal['source_after']['effects']['realizations']['branches']:c.validate_conditions(branch['conditions'],CID)
 modules={n:dict(file=str(Path(m.__file__)),sha256=hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest()) for n,m in sys.modules.items() if getattr(m,'__file__',None) and (n.startswith('photo_') or n in ['native_reviews','direct_review'])}
 assert not {n:v for n,v in modules.items() if n.startswith('photo_') and not Path(v['file']).is_relative_to(FROZEN)}
 result.pop('records',None);out=dict(verification=result,production_modules=modules,source_only_proposal_shape_valid=True,full_compact_admission_not_run=True,reason='Current formal row is pending with proof null; no alternate source is smuggled into a positive fixture.',operating_native_qualified_count=0)
 path=R/'authored/native_fresh_08250_17437_02_checks.json';assert not path.exists();path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(dict(batch=c.digest(BATCH),note=c.digest(NOTE),checks_sha256=hashlib.sha256(path.read_bytes()).hexdigest())))
