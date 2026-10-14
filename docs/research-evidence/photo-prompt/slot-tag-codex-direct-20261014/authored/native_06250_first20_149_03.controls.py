"""Source coverage/provenance/signature controls only; no semantic classifier."""
import sys,json,copy,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=Path.cwd();G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839');sys.path[:0]=[str(G/'scripts'),str(G/'precore'),str(R)]
import photo_semantic_evidence as e
import photo_candidate_corpus as c
import native_reviews as nr
sys.path[:]=[str(G/'scripts'),str(G/'precore')]+[p for p in sys.path if p not in {str(ROOT/'skills/photo-prompt-image-generator/scripts'),str(G/'scripts'),str(G/'precore')}]
raw=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert raw(Path(e.__file__))=='f74a5ef91bc07048c8bf312b66680c5b92b3b7b388f31f1890f31c8578609dee'
P=R/'native-inputs/prepared/review06250-00000-00020-149-03';O=R/'native_batches/review06250-00000-00020-149-03';I=json.load(open(P/'INPUT.json'));S=nr.artifact(ROOT,I['current_snapshot']);B=json.load(open(O/'BATCH.json'));OLD=json.load(open(R/'native_batches/review06250-00000-00020-149-02/BATCH.json'));checks=[]
for n in [3,4,5,9,16,17,18]:
 assert c.canonical_bytes(B['records'][n]['proof'])==c.canonical_bytes(OLD['records'][n]['proof'])
 checks.append({'ordinal':n,'prior_proof_exact_bytes':True,'proof_sha256':c.digest(B['records'][n]['proof']),'new_read_credit':0})
for n in [8,10,13,14,15,19]:
 row=B['records'][n];cid=row['candidate_id'];rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=copy.deepcopy(row['proof']);data={**S,'candidates':{**S['candidates'],cid:rec}}
 assert rec['effects']==S['candidates'][cid]['effects'] and row['source_after']==S['candidates'][cid]
 rejected=[]
 for defect in ['missing_app','app_reference_without_normal_anchor','metadata_fact','new_unknown_positive_anchor','unsigned_fact_change']+(['prefix_rename'] if n==14 else []):
  bad=copy.deepcopy(rec);p=bad['content']['role_evidence']
  if defect=='missing_app':p['source_units']=[u for u in p['source_units'] if u['pointer']!='/content/application_contract']
  elif defect=='app_reference_without_normal_anchor':
   u=p['source_units'][0];u.update(disposition='semantic_reference',reference_relation='partial_restatement',retained_constraint_rationale='Intentional invalid self-reference control; not a real semantic judgement.')
  elif defect=='metadata_fact':p['facts'][-1]['pointer']='/content/tags/0';p['facts'][-1]['quote']=bad['content']['tags'][0]
  elif defect=='new_unknown_positive_anchor':
   bad['content']['unknown_extra']='invented extra positive wording';p['facts'][-1]['pointer']='/content/unknown_extra';p['facts'][-1]['quote']='invented extra positive wording';p['meaning_sha256']=e.meaning_sha256(bad)
  elif defect=='unsigned_fact_change':p['facts'][-1]['value']['value']='tampered_value'
  else:p['facts'][-1]['dimension']='style';p['facts'][-1]['property']='style.aesthetic.dieselpunk'
  if defect!='unsigned_fact_change':p['review']['native_review']['native_contract_sha256']=e.native_contract_sha256(p)
  try:e.validate(bad,S['slot_catalog'],corpus={**data,'candidates':{**data['candidates'],cid:bad}})
  except ValueError:rejected.append(defect)
  else:raise AssertionError((n,defect,'unexpected acceptance'))
 checks.append({'ordinal':n,'exact_current_source_and_canonical_effects':True,'rejected_controls':rejected,'native_contract_sha256':row['proof']['review']['native_review']['native_contract_sha256']})
mods={}
for name,m in sorted(sys.modules.items()):
 if name.startswith(('photo_','photo_precore_')) and getattr(m,'__file__',None):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G),(name,p);mods[name]={'file':str(p),'raw_sha256':raw(p)}
out={'schema':'photo-first20-source03-controls/v1','checks':checks,'actual_modules':mods,'manual_boundary':'These tests reject malformed evidence and footprint changes; they do not semantically approve new source or prove a user request, pixels or root acceptance. Only six manually reviewed new source03 proofs and seven byte-identical historical proofs are exercised. Seven unselected guard afters remain separate pending source proposals.'};q=O/'CONTROLS.json';assert not q.exists();q.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('PASS13',raw(q))
