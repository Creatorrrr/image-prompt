"""Runtime selected-existing neutral presence is additional to exact branch identity, never inferred."""
from pathlib import Path
p=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/native_batches/review11870-01250-01300-05/check_01270_01275_v3.py');exec(compile(p.read_text().split('results=[];views=[];extra=[]',1)[0],str(p),'exec'))
checks=[]
for rid,owner in [('small_action_figure','F'),('small_doll','D')]:
 bad=copy.deepcopy(toy);bad['semantic_assertions']=[a for a in bad['semantic_assertions']if not(a['axes']['kind']=='fact'and a['axes']['owner']==owner and a['axes']['property']=='entity.presence')]
 for view in ['full','compact']:
  e,k=choose(1273,rid,bad,owner,view);receipt=n.admission(e,k);assert not receipt['allowed'];assert not generator.core_entry_eligible(S,k,contract('human'),picked('human'),e['_presentation_role'],e);checks.append({'ordinal':1273,'rid':rid,'view':view,'case':'selected_existing_owner_neutral_presence_missing_despite_exact_type_and_owner_node','admission':receipt,'consumer_denied':True})
for o,rid,k,owner,prop,newtype,newval in [(1270,'base',light,None,'lighting.source.type','lighting.source.type/v1','incandescent_lamp'),(1271,'base',hand,None,'entity.type','entity.type/v1','human')]:
 bad=copy.deepcopy(k)
 for a in bad['semantic_assertions']:
  if a['axes']['kind']=='fact'and a['axes']['property']==prop:a['axes']['value_type']=newtype;a['axes']['value']=newval
 for view in ['full','compact']:
  e,k=choose(o,rid,bad,owner,view);receipt=n.admission(e,k);assert not receipt['allowed'];checks.append({'ordinal':o,'rid':rid,'view':view,'case':'different_precise_source_type_not_alias_or_anatomy_inference','admission':receipt})
out={'schema':'photo-selected-owner-neutral-presence-boundary/v1','task_name':'/root/review_11870_12250','input_sha256':c.digest(I),'checkpoint_sha256':c.digest(J),'checks':checks,'case_count':len(checks),'all_passed':True,'source_proof_changes':0,'root_accepted':0,'operating':0,'boundary':'Existing-owner origin/selection runtime consumes independent neutralpresence, beyond precise branch-type sourcefact. Source App explicitly existing, no presence inferred from identity or ownernode. Different source types fail exact P. Synthetic fixture only.'};q=O/'CHECKS-01270-01275-SELECTED-PRESENCE-v1.json';assert not q.exists();q.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(c.digest(out),hashlib.sha256(q.read_bytes()).hexdigest(),len(checks))
