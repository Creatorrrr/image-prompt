"""Root-approved property spelling only; all previous proposals immutable."""
import copy,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(Path.cwd()/'skills/photo-prompt-image-generator/scripts'))
import photo_candidate_corpus as c
import photo_semantic_evidence as s
J=json.loads((R/'authored/native_resolution_08250_revision3_sources.json').read_text())
cid='cand_d15b4c6334a45b61a7407a022a2cc8e0';before=J['resolution_proposed_records'][cid];after=copy.deepcopy(before);deltas=[]
for bi,branch in enumerate(after['effects']['realizations']['branches']):
 for pi,p in enumerate(branch['effects']['properties']):
  if p['property']=='event.small_setback':
   ptr=f'/effects/realizations/branches/{bi}/effects/properties/{pi}/property'
   deltas.append({'pointer':ptr,'before':'event.small_setback','after':'situation.small_setback','reason':'Root approved exact spelling correction for the same concrete local small setback under final142 situation_context property prefix. No content, dimension, mode, owner, typed value or selected-RID scope change.'});p['property']='situation.small_setback'
assert len(deltas)==6
out=copy.deepcopy(J);out['schema']='native-resolution-semantic-revision/v4';out['supersedes_proposal_file']=str(R/'authored/native_resolution_08250_revision3_sources.json');out['supersedes_record_sha256']=c.digest(before);out['resolution_proposed_records'][cid]=after;out['exact_corrections']={cid:deltas};out['proposed_meaning_sha256']=s.meaning_sha256(after);out['status']='prepared_revision4_not_yet_reread_or_native_approved';out['root_adjudication']['small_setback_property_spelling']='Approved event.small_setback -> situation.small_setback with meaning/mode/conditions/owner/typed value/scope unchanged.'
(R/'authored/native_resolution_08250_revision4_sources.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'exact_property_corrections':len(deltas),'meaning_sha256':out['proposed_meaning_sha256'],'content_conditions_and_effect_dimensions_unchanged':after['content']==before['content'] and after['conditions']==before['conditions'] and after['effects']['dimensions']==before['effects']['dimensions']}))
