import json, hashlib, subprocess
from pathlib import Path
R=Path('/workspace/scratch/ce8f20680f5a/image-prompt'); P=R.parent/'daylong-progress'; O=P/'boundary-transition-source-scout'; A=R/'skills/photo-prompt-image-generator/assets'; B=R/'docs/research-evidence/photo-prompt'; S=B/'angle-motion-20260927/dynamic_composition/source_snapshot/assets'
sha=lambda b:hashlib.sha256(b).hexdigest()
digest=lambda o:sha(json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
manifest={}
def tracked(p):
 manifest[str(p.relative_to(R.parent))]=sha(p.read_bytes());return json.loads(p.read_text())
def save(n,o):(O/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
coverage=tracked(P/'review-coverage-map/id-coverage.json'); excluded={r['entry_id'] for r in coverage['rows']}
def ids(v):
 if isinstance(v,dict):
  for k,x in v.items():
   if k in {'id','entry_id','candidate_id'} and isinstance(x,str):yield x.split(':')[-1]
   yield from ids(x)
 elif isinstance(v,list):
  for x in v:yield from ids(x)
names={'source-inventory-and-decisions.json','selected-row-evidence.json','row-decisions.json','decisions.json','source-decisions.json','evidence.json','report.json'}
exfiles=[]
for p in sorted(P.glob('*scout*/*.json')):
 if p.parent==O or p.name not in names:continue
 excluded.update(ids(tracked(p)));exfiles.append(str(p.relative_to(R.parent)))
for p in sorted(B.glob('*cleanup*/frozen-inventory*.json')):
 d=tracked(p)
 for st in d if isinstance(d,list) else [d]:
  excluded.update(r['id'] for r in st.get('inventory',[]) if r.get('id'))
unknown={cid for f in tracked(P/'review-coverage-map/source-coverage.json') for cid in f['no_explicit_review_ids']}
boundary=tracked(A/'photo_prompt_boundary_transition_extension.json'); br=[r for rs in boundary['slots'].values() for r in rs]
assert len(br)==36 and all(r['id'] in excluded for r in br)
save('prior-exclusions.json',{'boundary_extension_total_rows':36,'boundary_extension_all_previously_reviewed':True,'boundary_rows':[r for r in coverage['rows'] if r['entry_id'] in {x['id'] for x in br}],'later_structured_inventories_checked':exfiles,'conservative_exclusion_ids':sorted(excluded),'note':'Generated whole-pool contracts and other scouts exclusion manifests alone do not establish individual row decisions.'})
reason={
'waiting_in_between_use_space':'Pending independent adjudication: Korean without traces of use may deny the temporal residue explicitly retained by the authored liminal profile, whereas English and embedding only suspend expected active use. Snapshot identity does not resolve this authored bilingual question.',
'between_use_transit_interior':'The maintained transit interior retains route and use cues while expected occupants and destination activity are absent. Both languages preserve suspended use; cleanliness and maintenance do not assert abandonment or erase possible operational residue.',
'liminal_expected_route_depth_frame':'The same route recedes through repeated maintained cues toward an unresolved endpoint. Korean withholding arrival function agrees with English missing destination use; no reversed route or forced horror interpretation.',
'between_use_liminal_suspension':'The place retains recognizable passage and timing cues while expected activity is deferred. Korean suspended use before/after operation matches the English between-use relation, without claiming irreversibility.',
'undergoing_contiguous_visible_metamorphosis':'One body owns source, intermediate and target forms simultaneously. Korean and English maintain the same transition direction and material/anatomical continuity; the fictional transformation is intentional.',
'full_bridge_metamorphosis_frame':'All three source/intermediate/target regions stay on one subject in one frame. Neither language turns them into independent before/after people or discrete panels.',
'single_subject_contiguous_metamorphosis':'Source-to-target transformation runs through a contiguous intermediate zone on one subject. The topology/material gradient is authored fiction, not a factual material process to normalize.',
'metamorphosis_contiguous_topology_gradient':'Surface, joints, silhouette and material progressively join source and target regions through the same unbroken intermediate bridge. Korean and English preserve that ownership and sequence.',
'contiguous_source_target_mid_metamorphosis':'The middle stage retains source features and emerging target features connected through one body. Before/after forms coexist rather than implying that the target has already replaced the source entirely.',
'metamorphosis_source_residue_trace':'Residue belongs to the source form and follows the same transition path into the emerging target surface. Neither language reverses source and target or assigns the fragments to a second subject.',
'mythic_apotheosis_aesthetic':'A former mortal retains a mortal-state anchor while receiving divine investiture. Korean explicit divine acceptance and English retained identity agree with the authored conferred-status event.',
'apotheosis_same_mortal_subject':'The recipient remains the same former mortal through elevation; the earthly token anchors previous status. No new deity replaces the subject and no worshipper/recipient role swap occurs.',
'apotheosis_divine_investiture_action':'The divine order grants the same formerly mortal subject a new place and attribute while mortal evidence survives. Korean explicitly names the granting actor; English is a compatible action phrase, not self-coronation.',
'mortal_divine_threshold_location':'The authored lower earthly zone leads through one visible transition to the higher receiving divine order. This spatial specialization intentionally expresses status change and is not generalized to all traditions.',
'mortal_token_divine_regalia_prop':'The mortal token and newly bestowed attribute share one owner. The ordinary token can remain behind while still evidencing that same subject; neither language transfers it to a different person.',
'apotheosis_continuity_composition':'One subject joins the retained mortal anchor, transition and active divine reception. Before-state evidence and granted status coexist in a compressed scene without reversing temporal direction.',
'katabasis_underworld_aesthetic':'The traveler remains living while moving from the world above into a governed underworld for one objective. It does not convert the traveler into a dead soul escorted by a psychopomp.',
'katabasis_living_traveler_subject':'The living traveler carries a source-appropriate purpose across a downward threshold and stays distinct from underworld dead inhabitants. Both languages preserve actor state and destination.',
'katabasis_threshold_descent_action':'The same living traveler leaves upper-world traces behind and crosses downward toward the underworld objective. The event is descent, not ascent or a completed return.',
'living_to_underworld_gate_location':'The gate connects retained upper-world origin cues to the underworld below. A traceable path back toward the living world is spatial origin evidence, not a guarantee of successful return or a forced irreversible crossing.',
'katabasis_objective_token_prop':'The purpose token travels with the living visitor from upper-world origin toward the underworld target. Korean continuity before/after descent and English directed carriage preserve the same owner and objective.',
'katabasis_directional_composition':'The composition traces upper-world origin through the downward gate to the underworld ruler or objective. Both languages keep the living traveler on that directionally continuous path.'}
profiles=tracked(A/'photo_prompt_visual_obligations.json'); profile_ids={'liminal_space':'liminal_transition_use_gap','metamorphosis':'continuous_metamorphosis_source_target_bridge','mythic_apotheosis':'mythic_apotheosis_mortal_divine_transition','katabasis_underworld':'katabasis_living_underworld_descent'}
profile_records={p['id']:(i,p) for i,p in enumerate(profiles['profiles']) if p['id'] in profile_ids.values()}
evfiles=[B/'imaginal-visual-semantics-20260901/evidence.jsonl',B/'research_evidence.jsonl']; evidence=[]
for p in evfiles:
 manifest[str(p.relative_to(R.parent))]=sha(p.read_bytes())
 for i,line in enumerate(p.read_text().splitlines(),1):
  if line.strip():evidence.append((p,i,json.loads(line)))
for p in [R/'GOAL_PLAN.md',B/'boundary-transition-visual-semantics-20260901/source-research.md',B/'imaginal-visual-semantics-20260901/source-research.md',B/'mythology-visual-semantics-20260901/source-research.md']:
 manifest[str(p.relative_to(R.parent))]=sha(p.read_bytes())
rows=[]; selected=set();bindings=[]
for family in ['imaginal','mythology']:
 p=A/f'photo_prompt_{family}_extension.json';d=tracked(p); sp=S/p.name; old=tracked(sp); lookup={r['id']:(s,i,r) for s,rs in old['slots'].items() for i,r in enumerate(rs)}
 mp=B/'extension-maintenance'/(d['maintenance_ref']['record_id']+'.json');maintenance=tracked(mp)
 binding={'source':str(p.relative_to(R)),'maintenance':str(mp.relative_to(R)),'maintenance_ref_hash_matches':digest(maintenance)==d['maintenance_ref']['sha256']}
 bindings.append(binding)
 for slot,rs in d['slots'].items():
  for i,r in enumerate(rs):
   keys=[k for k in profile_ids if k in r.get('tags',[])]
   if not keys:continue
   eid=r['id'];cid=f'slot:{slot}:{eid}';assert eid not in excluded and cid in unknown;selected.add(eid); os,oi,orr=lookup[eid]; assert r==orr and slot==os
   profile_id=profile_ids[keys[0]]; profile_i,pr=profile_records[profile_id]
   refs=[{'path':str(ep.relative_to(R)),'jsonl_line':li,'record':ev} for ep,li,ev in evidence if eid in ev.get('candidate_ids',[])]
   assert refs
   rows.append({'candidate_id':cid,'entry_id':eid,'slot':slot,'family':family,'chain_id':profile_id,'source':str(p.relative_to(R)),'source_pointer':f'/slots/{slot}/{i}','source_row_sha256':digest(r),'source_row':r,'original_snapshot':{'path':str(sp.relative_to(R)),'pointer':f'/slots/{os}/{oi}','full_row_equal':True},'authored_research_evidence':refs,'authored_profile_pointer':{'path':str((A/'photo_prompt_visual_obligations.json').relative_to(R)),'pointer':f'/profiles/{profile_i}'},'decision':'pending_independent_adjudication' if eid=='waiting_in_between_use_space' else 'keep_authored_meaning','reason':reason[eid]})
assert len(rows)==22
mentions=[]
for p in P.rglob('*.json'):
 if O in p.parents:continue
 txt=p.read_text(); hit=[i for i in sorted(selected) if '"'+i+'"' in txt]
 if hit:mentions.append({'path':str(p.relative_to(R.parent)),'ids':hit,'classification':'incidental_generated_whole_pool_contract_or_external_exclusion_manifest; no individual decision'})
inv={'scope':'22 individually unreviewed adjacent threshold/before-after rows after excluding all 36 boundary extension rows. Read-only source audit; no repository mutation or ranking measurement.','observed_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'selection':{'rows':22,'liminal':4,'metamorphosis':6,'apotheosis':6,'katabasis':6,'all_in_review_map_no_explicit_review':True,'later_individual_scout_overlap':[]},'rows':rows,'authored_chains':[{'profile_id':eid,'source_pointer':f'/profiles/{i}','record':r} for eid,(i,r) in profile_records.items()],'maintenance_bindings':bindings,'incidental_prior_mentions':mentions,'qualified_defects':0,'unresolved_candidates':['waiting_in_between_use_space'],'proposals':[],'limits':['Full earlier-source equality establishes preservation, not semantic correctness.','Authored fictional and liminal specializations are retained.','The katabasis profile single one-way wording was read as directional descent; the slot chain never claims successful return or irreversible path loss. No profile-policy change proposed.','No probes, final consumer gate, runtime tests, retrieval ranks, paid API calls, repository edits, commits or pushes performed at this checkpoint.']}
save('source-inventory-and-decisions.json',inv);save('evidence-manifest.json',manifest)
print(json.dumps({'rows':len(rows),'keeps':21,'pending':1,'bindings':bindings,'artifact':str(O/'source-inventory-and-decisions.json')},indent=2))
