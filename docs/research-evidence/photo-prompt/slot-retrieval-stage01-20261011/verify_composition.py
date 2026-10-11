"""Maintenance composition evidence, with real public receipt-bound audits.

These are authored prose/contract reviews. They make no native-image claim.
The retained baselines are reviewed again as the final proposed scene.
"""
import argparse
import copy
import json
import subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent
PYTHON = Path('/Users/chasoik/Projects/image-prompt/.venv/bin/python')
CASES = {
    'holdout-01-graduation-ko': 'graduation_after_ceremony',
    'holdout-02-workshop-en': 'workshop_class_session',
    'holdout-05-world-treaty-en': 'diegetic_larp_world_checkpoint_occasion',
    'holdout-06-isekai-ko': 'isekai_frontier_guild_frontier_occasion',
    'holdout-07-cup-ko': None,
}
FACTS = {
    'diegetic_larp_world_checkpoint_occasion': ['roleplaying', 'world', 'treaty'],
    'isekai_frontier_guild_frontier_occasion': ['isekai', 'frontier', 'guild'],
}


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def composition(pack, fixture, target):
    core = pack['authorial_core']; lock = core['intent_lock']
    prompt = core['baseline_prompt_en']
    review = copy.deepcopy(fixture['embodiment_review'])
    review['provenance'] = 'agent_postcomposition'
    review['summary'] = 'Reviewed the final proposed prompt again; the retained scene keeps the support, reach, contact and visibility described in the baseline. ' + review['summary']
    composed = dict(
        pack_id=pack['pack_id'], prompt_en=prompt, negative_en=pack['negative_en'],
        core_retrieval_sha256=pack['core_retrieval']['canonical_sha256'],
        composer='agent', chosen_candidate_ids=[], chosen_visual_concept_ids=[],
        candidate_interpretations=[],
        embodiment_review=dict(source_contract_sha256=pack['embodiment_preflight']['canonical_sha256'], review=review),
        authorial_core_binding=dict(source_authorial_core_sha256=core['canonical_sha256'],
            source_intent_lock_sha256=lock['canonical_sha256'],
            preserved_anchor_ids=[r['anchor_id'] for r in lock['semantic_anchors']],
            preserved_evidence=[], authorial_decisions=[]),
        semantic_clarification_decisions=[dict(clarification_id=r['id'],
            decision='applied' if r.get('required_in_final_prompt') else 'rejected',
            rationale='The final proposed scene retains the frozen requester meaning in the independently authored baseline.',
            prompt_evidence=lock['semantic_anchors'][0]['prompt_evidence'])
            for r in pack['semantic_clarification']['candidates']],
        creative_augmentation_brief=dict(decisions=[dict(candidate_id=r['id'],
            decision='rejected', rationale='The retained baseline already develops this request; this optional addition is declined.')
            for r in pack['creative_augmentation']['candidates']]),
    )
    if pack.get('semantic_assertion_obligations'):
        contract = pack['semantic_assertion_obligations']
        composed['semantic_assertion_evidence'] = dict(source_contract_sha256=contract['canonical_sha256'],
            evidence={r['assertion_id']: r['frozen_evidence'] for r in contract['obligations']})
    if target:
        candidate = next(r for r in pack['slots']['occasion_context']['candidates'] if r['entry_id'] == target)
        evidence = prompt.split('. ')[0].rstrip('.')
        row = dict(candidate_id=candidate['id'], realization='baseline',
            artistic_interpretation='Use the occasion as the chronological context of the already developed photographic scene.',
            transformation='Retain the independently authored actor, action and setting rather than paste the candidate label as a new scene.',
            prompt_evidence=evidence, affected_properties=candidate['affected_properties'])
        if target in FACTS:
            row['context_review'] = dict(requirement_evidence=[dict(requirement_id='entry:primary_any',
                fact=fact, state='present', prompt_evidence=evidence,
                reason='The retained sentence explicitly locates the participants and their activity in this primary scene.',
                origin='retained', affected_dimensions=[], affected_properties=[]) for fact in FACTS[target]])
        composed['chosen_candidate_ids'] = [candidate['id']]
        sampled = next((r for r in composed['creative_augmentation_brief']['decisions']
                        if r['candidate_id'] == candidate['id']), None)
        if sampled is None:
            composed['candidate_interpretations'] = [row]
        else:
            sampled.clear(); sampled.update(row, decision='transformed',
                rationale='Interpret the already-authored event phase through the open timing property; actors and requested activity remain retained.',
                affected_dimensions=['timing'],
                affected_properties=[r for r in candidate['affected_properties'] if r['dimension']=='timing'])
    return composed


def main():
    p = argparse.ArgumentParser(); p.add_argument('--root', type=Path, required=True); p.add_argument('--lane', default='after')
    p.add_argument('--only', action='append')
    args = p.parse_args(); skill = args.root/'skills/photo-prompt-image-generator'
    results = []
    for key, target in CASES.items():
        if args.only and key not in args.only: continue
        directory = OUT/args.lane/key
        pack = json.loads((directory/'candidate-pack.json').read_text())[0]
        fixture = json.loads((args.root/'tests/fixtures/photo_prompt/slot_retrieval_natural_v1'/key/'fixture.json').read_text())
        chosen = composition(pack, fixture, target)
        modes = [('adopted' if target else 'zero-candidates', chosen, True)]
        if target:
            modes.append(('zero-candidates', composition(pack, fixture, None), True))
        if target in FACTS:
            missing = copy.deepcopy(chosen)
            row = next(r for r in missing['candidate_interpretations'] + missing['creative_augmentation_brief']['decisions']
                       if 'context_review' in r)
            row['context_review']['requirement_evidence'].pop()
            modes.append(('missing-context-fact', missing, False))
        for label, composed, expected in modes:
            path = directory/(label+'-composed.json'); save(path, composed)
            command = [str(PYTHON), str(skill/'scripts/audit_composed_prompt.py'), '--pack', str(directory/'candidate-pack.json'),
                '--composed', str(path), '--runtime-store', str(OUT/(args.lane+'-runtime-store')),
                '--runtime-receipt', str(directory/'candidate-pack.json.runtime-receipt.json')]
            result = subprocess.run(command, cwd=args.root, capture_output=True, text=True)
            (directory/(label+'-audit.log')).write_text(result.stdout+result.stderr)
            try: report=json.loads(result.stdout)
            except ValueError: report=dict(status='tool_error', error=result.stderr)
            save(directory/(label+'-audit.json'), report)
            actual = result.returncode == 0 and report.get('status') == 'pass'
            record = dict(key=key, mode=label, expected_pass=expected, actual_pass=actual,
                          matched=actual == expected, checks=[r.get('check') for r in report.get('failures',[])])
            results.append(record); print(json.dumps(record), flush=True)
            save(OUT/(args.lane+'-composition-summary.json'), results)
    if not all(row['matched'] for row in results): raise SystemExit(1)


if __name__ == '__main__': main()
