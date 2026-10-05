"""Check cross-file research integrity; never claim runtime or pixel validation."""
from __future__ import annotations
import csv, hashlib, json, re, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CHECKS = []

def read(name):
    return json.loads((HERE / name).read_text())

def write(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def check(label, passed, detail=None):
    CHECKS.append({'check': label, 'passed': bool(passed), 'detail': detail})

def main():
    units = read('SEMANTIC-UNITS.json')['units']
    drafts = read('CANDIDATE-DRAFTS.json')['drafts']
    bundles = read('BUNDLE-DRAFTS.json')['bundles']
    adoption = read('ADOPTION-MAP.json')
    plan = read('REGRESSION-PLAN.json')
    counts = read('PACKAGE-COUNTS.json')
    snapshot = read('CHECKOUT-SNAPSHOT.json')
    sources = {s['id']: s for s in read('SOURCES.json')['sources']}
    keyword_rows = read('SOURCE-KEYWORDS.json')['entries']
    inventory = read('AUTHORING-INVENTORY.json')
    source_text = next(it['text'] for turn in read('REFERENCE-CONVERSATION.json')['turns'] for it in turn['items'] if it.get('type') == 'agentMessage' and it.get('truncated'))
    ids = {u['id'] for u in units}
    draft_ids = {c['draft_id'] for c in drafts}
    check('unit_ids_unique', len(ids) == len(units))
    check('source_units_are_all_recovered_rows', {u['source_number'] for u in units if u['source_number'] is not None} == {r['number'] for r in keyword_rows})
    check('supplements_are_explicitly_separate', {u['id'] for u in units if u['source_number'] is None} == {f'GX{i:02}' for i in range(1,21)})
    check('reference_tail_limit_is_retained', read('SOURCE-KEYWORDS.json')['truncated'] is True and counts['source_tail_truncated'] is True)
    for row in keyword_rows:
        check('source_span_' + str(row['number']), source_text[row['source_start']:row['source_end']] == row['source_row'] and row['label'] in row['source_row'])
    for u in units:
        check('unit_fields_' + u['id'], bool(u['meaning_ko'] and u['observable_realization_en'] and u['confusion_boundaries'] and u['claim_limits']))
        check('unit_sources_' + u['id'], set(u['sources']).issubset(sources) and 'S11' not in u['sources'])
        check('unit_draft_boundary_' + u['id'], u['status'] == 'RESEARCH_DRAFT_NOT_RUNTIME_SCHEMA' and 'realization_status' in u and 'hard_activation_plan' in u)
    check('draft_ids_unique', len(draft_ids) == len(drafts))
    slots = {e['slot'] for e in inventory['candidate_catalog']}
    candidate_keys = {(e['file'],e['slot'],e['id']) for e in inventory['candidate_catalog']}
    dimensions = {'composition','appearance','setting','material','style','color','subject','concept','lighting','body_geometry','event','sexual_tone'}
    for c in drafts:
        check('draft_unit_references_' + c['draft_id'], set(c['unit_ids']).issubset(ids))
        check('draft_slot_' + c['draft_id'], c['proposed_slot'] in slots)
        check('draft_relation_owner_' + c['draft_id'], bool(c['owner_binding']) and all(r['source_owner_binding'] == c['owner_binding'] and set(r['targets']).issubset(ids) for r in c['proposed_relations']))
        effects = c['proposed_effects']
        check('draft_effects_' + c['draft_id'], bool(effects) and all(e['dimension'] in dimensions and e['target_binding'] == c['owner_binding'] and e['proposed_property_area'] for e in effects))
        check('draft_mapping_not_runtime_' + c['draft_id'], c['status'] == 'RESEARCH_DRAFT_NOT_RUNTIME_SCHEMA' and c['effect_mapping_status'].startswith('REQUIRES_CURRENT'))
        check('draft_reuse_identities_' + c['draft_id'], all((r['file'],r['slot'],r['id']) in candidate_keys for r in c['current_reuse_records']))
        check('draft_sources_' + c['draft_id'], set(c['sources']).issubset(sources) and 'S11' not in c['sources'])
    for b in bundles:
        check('bundle_refs_and_choice_' + b['id'], set(b['member_draft_ids']).issubset(draft_ids) and b['choice_policy'] and b['status'] == 'RESEARCH_DRAFT_NOT_RUNTIME_SCHEMA')
    check('adoption_has_every_unit_once', len(adoption['units']) == len(ids) and {r['unit_id'] for r in adoption['units']} == ids)
    for r in adoption['units']:
        check('adoption_refs_' + r['unit_id'], set(r['candidate_draft_ids']).issubset(draft_ids) and r['status'] == 'PLANNED_NOT_IMPLEMENTED')
    for p in plan['semantic_probes']:
        check('semantic_probe_' + p['id'], p['status'] == 'PLANNED_NOT_RUN' and set(p.get('unit_ids',[])).issubset(ids) and set(p.get('candidate_review_leads',[])).issubset(draft_ids) and not re.search(r'\b(?:GO\d{3}|GX\d{2}|GD\d{2})\b', p['request_ko']))
    for case in plan['native_cases']:
        check('native_plan_' + case['id'], case['status'] == 'PLANNED_NOT_RUN' and set(case['unit_ids']).issubset(ids) and set(case['candidate_review_leads']).issubset(draft_ids) and len(case['all_of_required_if_bound']) >= 3 and bool(case['claim_boundary']))
    check('pilot_arithmetic', len(plan['pilot']['case_ids']) * len(plan['pilot']['arms']) * plan['pilot']['independent_repeats_per_arm'] == plan['pilot']['planned_image_count'] == counts['pilot_images_planned'])
    check('counts_cross_file', len(units) == counts['semantic_units'] and len(drafts) == counts['candidate_drafts'] and len(bundles) == counts['bundle_drafts'] and len(plan['semantic_probes']) == counts['semantic_probes_planned'] and len(plan['native_cases']) == counts['native_cases_planned'])
    check('runtime_and_pixels_not_misreported', counts['runtime_adopted'] is False and counts['native_images_generated'] == 0 and counts['native_pixel_evaluated'] is False and counts['semantic_probes_executed'] == 0)
    check('failed_followup_not_used', sources['S11']['read_status'] == 'bibliographic_excerpt_only_open_failed_404')
    check('source_ledger_count', len(sources) == counts['source_records'] and sum(s['id'] != 'S11' for s in sources.values()) == counts['retrieved_sources'])

    changed = []
    for file, digest in snapshot['authored_source_sha256'].items():
        path = ROOT / 'skills/photo-prompt-image-generator/assets' / file
        if not path.exists() or sha(path) != digest:
            changed.append(file)
    generator = ROOT / 'skills/photo-prompt-image-generator/scripts/prompt_generator.py'
    generator_changed = sha(generator) != snapshot['generator_sha256']
    current_head = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    currency = {'status': 'REQUIRES_REAUDIT_BEFORE_IMPLEMENTATION' if changed or generator_changed or current_head != snapshot['head'] else 'CAPTURED_INPUTS_STILL_MATCH_AT_VALIDATION', 'snapshot_head': snapshot['head'], 'current_head':current_head, 'changed_authored_files_since_capture':changed, 'generator_changed_since_capture':generator_changed, 'worktree_status_at_validation':subprocess.check_output(['git','status','--porcelain=v1','-z'],cwd=ROOT).decode().split('\0'), 'boundary':'Other work may change this shared checkout. Currency is a read-only observation, not permission to restore or publish files.'}
    write('CHECKOUT-CURRENCY.json',currency)

    generated_self = {'VALIDATION.json','MANIFEST.json'}
    for file in HERE.glob('*.md'):
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',file.read_text()):
            if '://' in target or target.startswith('#'):
                continue
            target = target.split('#',1)[0]
            check('link_' + file.name + '_' + target, target in generated_self or (file.parent / target).exists())
    failures = [c for c in CHECKS if not c['passed']]
    result = {'status':'PASS_RESEARCH_PACKAGE_STRUCTURE_ONLY' if not failures else 'FAIL_RESEARCH_PACKAGE_STRUCTURE', 'checks':len(CHECKS), 'passed':len(CHECKS)-len(failures), 'failed':len(failures), 'failures':failures, 'claims_verified':['Recovered-source spans and units are consistent.','Sources, candidate/probe/bundle/adoption references and draft boundaries are consistent.','Proposed effects and slot identities have explicit authoring scope.','Counts and local document links are consistent.'], 'not_evaluated':['Historical/source-image pixel correctness','Actual fabrication process and authenticity','Runtime schema adoption and exact property mapping','Retrieval eligibility/exposure/selection','Semantic/runtime regression execution','Prompt/tool binding execution','Image generation and native pixels','Moderation outcome','User acceptance'], 'checkout_currency':currency['status']}
    write('VALIDATION.json',result)
    manifest = {'status':'RESEARCH_ARTIFACT_CHECKSUMS_NOT_ACCEPTANCE', 'sha256':{f.name:sha(f) for f in sorted(HERE.iterdir()) if f.is_file() and f.name != 'MANIFEST.json'}, 'boundary':'Hashes establish these saved research bytes only. They are not a runtime or native-pixel proof.'}
    write('MANIFEST.json',manifest)
    print(json.dumps(result,ensure_ascii=False))
    if failures:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
