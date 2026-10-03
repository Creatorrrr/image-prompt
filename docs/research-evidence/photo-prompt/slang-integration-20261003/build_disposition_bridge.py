"""Link all research work items to reviewed runtime owners or explicit holds."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parent / 'slang-visual-semantics-20261003'
drafts = json.loads((RESEARCH / 'CANDIDATE-DRAFTS.json').read_text())['drafts']
decisions = json.loads((RESEARCH / 'TERM-DECISIONS.json').read_text())
changes = json.loads((HERE / 'authored-change-receipt.json').read_text())
new = {x['draft_id']: x['id'] for x in changes['new_profiles']}
reuse = {'SV04': 'pv_half_lidded', 'SV05': 'ae_deadpan_form', 'SV06': 'pv_parted_lips',
         'SV07': 'ae_slack_jaw', 'SV10': 'pv_double_v', 'SV16': 'pv_wide_stance',
         'SV19': 'ne_regional_soft_volume', 'SV20': 'bm_abdominal_projection',
         'SV21': 'bust_prominence_relation', 'SV28': 'pv_chair_straddle'}
unit_owners = {}
rows = []
for draft in drafts:
    owner = new.get(draft['id'], reuse.get(draft['id']))
    status = 'new_observable_variant' if draft['id'] in new else 'equivalent_existing_owner' if owner else 'held'
    for unit in draft['semantic_unit_ids']:
        if owner: unit_owners.setdefault(unit, []).append(owner)
    rows.append({'research_draft_id': draft['id'], 'status': status, 'runtime_owner': owner,
        'semantic_unit_ids': draft['semantic_unit_ids'], 'source_ids': draft['source_ids'],
        'source_support': 'lexical context and component decomposition; variant details are conservatively authored observations, not universal slang definitions',
        'scope': {'slot': draft['proposed_slot'], 'dimensions': draft['affected_dimensions'], 'properties': draft['affected_properties']},
        'held_reason': draft['held_reason'] if status == 'held' else None,
        'original_slang_spelling_promoted': False})
term_rows = []
for term in decisions['terms']:
    owners = list(dict.fromkeys(owner for unit in term['candidate_effect_recommendation'] for owner in unit_owners.get(unit, [])))
    term_rows.append({'term_id': term['id'], 'term': term['term'], 'decision_group_id': term['decision_group_id'],
        'lexical_evidence_status': term['lexical_evidence_status'],
        'term_specific_source_ids': term['term_specific_source_ids'],
        'research_disposition': term['disposition'], 'related_runtime_observations': owners,
        'new_exact_slang_alias_added': False,
        'limits': 'Related runtime observations are partial visual projections. They do not replace the full original lexical meaning. Unverified spellings and nonvisual role, event, temporal or evaluative meanings remain research-only.'})
output = {'schema_version': 'photo-slang-disposition-bridge/v1',
    'drafts': rows, 'terms': term_rows,
    'counts': {'drafts': len(rows), 'new': sum(x['status']=='new_observable_variant' for x in rows),
        'reuse': sum(x['status']=='equivalent_existing_owner' for x in rows),
        'held': sum(x['status']=='held' for x in rows), 'terms': len(term_rows), 'new_slang_exact_aliases': 0},
    'held_draft_policy': 'SV11 coordinates existing expression and hand owners only; SV13/SV14 need style or carrier review; SV22 needs two-target ownership; SV23/SV25 need temporal paired evidence.'}
assert output['counts'] == {'drafts': 28, 'new': 12, 'reuse': 10, 'held': 6, 'terms': 234, 'new_slang_exact_aliases': 0}
(HERE / 'DISPOSITION-BRIDGE.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(output['counts']))
