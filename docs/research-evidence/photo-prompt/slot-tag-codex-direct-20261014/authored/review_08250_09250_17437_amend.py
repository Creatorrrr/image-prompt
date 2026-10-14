"""One explicitly authored typed amendment; frozen batch and proposal stay unchanged."""
import copy,json,sys,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(R));import direct_review as d
from photo_candidate_realizations import ids
packet=json.loads((R/'packets/17250-250.json').read_text());cid=packet['ids'][187];source=d.source();record=packet['records'][cid]
oldpath=R/'authored/review_08250_09250_17250_17500.json';old=json.loads(oldpath.read_text())['decisions'][187]
assert cid=='cand_d15b4c6334a45b61a7407a022a2cc8e0'
assert d.c.digest(old)=='6b87f610b179b6646bd15affe093a8bd7152c4ded60cc72ad8ebf461426d94f9'
assert old['status']=='needs_source_fix'
proposalpath=R/'authored/review_08250_09250_17437_proposal.json';proposal=json.loads(proposalpath.read_text())
authored=copy.deepcopy(record['content']['authored_components'])
for pointer in ['/content/authored_components/components','/content/authored_components/discovery','/content/authored_components/obligations/0/component_ids']:
 correction=next(c for c in proposal['corrections'] if c['pointer']==pointer)
 keys=pointer.split('/')[3:];parent=authored
 for key in keys[:-1]:parent=parent[int(key)] if isinstance(parent,list) else parent[key]
 key=keys[-1];assert (parent[int(key)] if isinstance(parent,list) else parent[key])==correction['before']
 if isinstance(parent,list):parent[int(key)]=copy.deepcopy(correction['after'])
 else:parent[key]=copy.deepcopy(correction['after'])
# Membership coverage is not activation: compiler only validates refs, discovery controls required groups.
authored['obligations'][0]['component_ids']=[v['id'] for v in authored['components']]
corrections=[{'pointer':'/content/authored_components','before':copy.deepcopy(record['content']['authored_components']),'after':authored,'reason':'Require four explicitly source-supported common baseline groups in discovery; retain all seven known IDs in obligation membership for compiler coverage only. Preserve optional incident definitions, five unchanged baseline evidence requirements, instruction and guards; membership itself does not generate mandatory incident evidence or gates.'}]
corrections+=copy.deepcopy(proposal['corrections'][3:])
assert len(corrections)==5
corrected=d.corrected_record(record,corrections)
assert ids(corrected)==['base'] and corrected['conditions']==record['conditions'] and corrected['effects']==record['effects']
assert list(d.references(corrected))==list(d.references(record)) and packet['references'][cid]=={}
c=corrected['content'];ac=c['authored_components']
assert ac['discovery']=={'minimum_component_groups':4,'required_group_ids':['adult_peer_role','haughty_status_play','smug_poised_bearing','adult_youthful_styling']}
assert c['composition_instruction']==record['content']['composition_instruction']
assert ac['obligations'][0]['instruction']==record['content']['authored_components']['obligations'][0]['instruction']
assert ac['obligations'][0]['evidence']==record['content']['authored_components']['obligations'][0]['evidence']
assert ac['obligations'][0]['render_gates']==c['render_gates']
assert ac['components'][4:]==record['content']['authored_components']['components'][1:]
assert c['required_evidence_fields']==record['content']['required_evidence_fields']
cue=R/'worker-notes/review_08250_09250-17437-corrected-cue.json'
if '--final' not in sys.argv:
 d.write(cue,{'ordinal':17437,'candidate_id':cid,'corrections':corrections,'corrected_source':corrected,'reference_closure':packet['references'][cid],'shape_validation_only':True})
 print('Typed correction shape passed. Read complete corrected_source before --final:',cue)
else:
 assert json.loads(cue.read_text())['corrected_source']==corrected
 choices=[
 ('age_presentation','actor','unmistakably_adult','/content/semantics/definition'),
 ('participant_role','context','adult_peer_rival','/content/semantics/definition'),
 ('expression','actor_face','haughty_smug_poised_baseline','/content/semantics/definition'),
 ('eye_detail','actor_eyes','haughty_half_lidded_baseline','/content/semantics/definition'),
 ('presentation_style','actor','fresh_youthful_adult_styling','/content/composition_instruction'),
 ]
 meaning='Unmistakably adult peer rival has haughty half-lidded eyes, smug poised bearing and fresh youthful adult styling; one-up, setback, warm crack and recovery incidents remain optional.'
 roles=[];facts=[]
 for tag,owner,tail,pointer in choices:
  spec=source['slot_catalog'][tag];prefix=spec['property_prefixes'][0]
  f={'pointer':pointer,'quote':d.pointer(corrected,pointer,positive=True),'dimension':spec['dimensions'][0],'target':owner,'property':prefix+('' if prefix.endswith('.') else '.')+tail}
  roles.append({'slot_id':tag,'semantic_role':spec['semantic_role'],'scope':'whole_record','realization_ids':['base'],'rationale':meaning+' Exact primary cue supplies '+tail.replace('_',' ')+'.','evidence':[f]})
  facts.append({**f,'realization_id':'base'})
 decision={'candidate_id':cid,'meaning_summary':meaning,'recommended_kind':'visual_profile','corrections':corrections,'roles':roles,'facts':facts,'rejected_boundaries':['No minor-coded role, childlike morphology, twin tails/small face/reference appearance/label as personality proof, generic cuteness, bullying/humiliation, or compulsory one-up/setback/warmth/recovery. No private emotion or real personality truth from pixels.'],'uncertainties':[],'status':'approved','all_roles_considered':True}
 outpath=R/'authored/review_08250_09250_17437_amend.json'
 entry={'ordinal':17437,'candidate_id':cid,'before_authored_file':str(oldpath.relative_to(d.ROOT)),'before_authored_row_sha256':d.c.digest(old),'before_authored_item':188,'before_status':'needs_source_fix','reread_id':'review_08250_09250-17437-typed-r1','model':'gpt-6.1-sol','reasoning_effort':'high','source_record_sha256':d.binding(source,cid)['source_record_sha256'],'source_reread_complete':True,'reference_reread_complete':True,'after_proposal_conditions':corrected['conditions'],'after_proposal_effects':corrected['effects'],'after_proposal_reference_sha256':d.binding(source,cid)['reference_sha256'],'corrected_source_sha256':d.c.digest(corrected),'native_qualification_issues_retained':[{'kind':'obligation_membership_is_not_discovery','detail':'All7 component IDs remain obligation references to satisfy coverage validation. Only common4 discovery groups are required; unchanged5 evidence fields and corrected gates require no optional incident. visual_profile_contracts.py70-74/111 uses component_ids only for known-reference/coverage checks.'}],'reassessment_rationale':'Complete original and complete corrected cue directly reread. Four common adult/haughty/smug-poised/adult-styling components agree with unchanged instruction; all original incidents remain optional. Shape compilation only checks consistency; this approval is the separate Codex semantic judgement.','decision':decision}
 document={'schema':'photo-codex-direct-review-amendment/v1','source_sha256':d.c.digest(source),'catalog_sha256':d.c.digest(source['slot_catalog']),'packet_sha256':d.c.digest(packet),'amendments':[entry]}
 full={**d.binding(source,cid),**decision,'schema':d.SCHEMA,'reviewer':'Codex','review_method':'codex_direct_source_read','independent_human_review':False,'packet_sha256':d.c.digest(packet),'authored_decision':{'file':str(outpath.relative_to(d.ROOT)),'item':1,'sha256':d.c.digest(decision)}}
 d.validate_decision(full,source)
 d.write(outpath,document)
 note={'task_name':'/root/review_08250_09250','agent_id':'/root/review_08250_09250','model':'gpt-6.1-sol','reasoning_effort':'high','start':17437,'stop':17438,'scope':'Sparse full reread of 17437 after typed correction support; original batch and standalone proposal are immutable.','packet_paths':[str((R/'packets/17250-250.json').relative_to(d.ROOT))],'authored_paths':[str(outpath.relative_to(d.ROOT)),str(Path(__file__).relative_to(d.ROOT))],'complete_source_read':True,'directly_reread_count':1,'approved_count':1,'still_pending_count':0,'approved_ordinals':[17437],'unresolved_ordinals':[],'reread_ids':[entry['reread_id']],'source_sha256':d.c.digest(source),'catalog_sha256':d.c.digest(source['slot_catalog']),'packet_sha256':d.c.digest(packet),'source_bindings':d.binding(source,cid),'before_authored_file':entry['before_authored_file'],'before_authored_item':188,'before_authored_row_sha256':entry['before_authored_row_sha256'],'before_status':entry['before_status'],'proposal_link':{'file':str(proposalpath.relative_to(d.ROOT)),'sha256':d.c.digest(proposal)},'corrected_cue_path':str(cue.relative_to(d.ROOT)),'corrected_source_sha256':d.c.digest(corrected),'qualification_issues':[{'detail':'Root and worker read grouped compile path: component_ids only validates known IDs/coverage at visual_profile_contracts.py70-74/111. Compiled obligations derive from explicit evidence/instruction/gates; all7 membership does not require optional incidents. Discovery requires common4/min4 and unchanged5 baseline evidence fields remain. No new optional schema or weakening needed.'}],'final_ready':True,'validation_boundary':'Complete corrected cue semantically reread before approval. Typed compilation and validate_decision shape/hash checks are not semantic-accuracy proof; no canonical/global normalization applied.','authored_file_sha256':{str(p.relative_to(d.ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [outpath,Path(__file__)]}}
 d.write(R/'worker-notes/review_08250_09250-17437-amend.json',note)
 print('17437 approved after complete corrected-source reread; validated in memory:',outpath)
