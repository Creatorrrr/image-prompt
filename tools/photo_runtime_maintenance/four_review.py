"""Recheck four known candidates, retaining the hash-bound prior archive review."""
import ast
from collections import Counter, defaultdict
from pathlib import Path

import four_state as scope
import state
from history_state import new


def run():
    previous = scope.ROOT/'docs/research-evidence/photo-prompt/runtime-legacy-followup-20261019'
    old = state.read(previous/'FUNCTION-REVIEW.json')
    targets = state.read(scope.E/'TARGETS.json')['targets']
    names = set(scope.FUNCTIONS);references = defaultdict(list)
    paths = [*(scope.SKILL/'scripts').glob('*.py'),*(scope.SKILL/'precore').glob('*.py'),
             *(scope.ROOT/'tests').glob('*.py')]
    for p in paths:
        tree = ast.parse(p.read_bytes(),filename=str(p))
        for node in ast.walk(tree):
            name = node.id if isinstance(node,ast.Name) and isinstance(node.ctx,ast.Load) else (
                node.attr if isinstance(node,ast.Attribute) and isinstance(node.ctx,ast.Load) else None)
            if name in names:references[name].append({'path':str(p),'line':node.lineno,'kind':'load'})
            if isinstance(node,ast.ImportFrom):
                for alias in node.names:
                    if alias.name in names:references[alias.name].append({'path':str(p),'line':node.lineno,
                        'kind':'import','asname':alias.asname})
            if isinstance(node,ast.Constant) and isinstance(node.value,str):
                for name in names:
                    if name in node.value:references[name].append({'path':str(p),'line':node.lineno,'kind':'literal'})
    before = scope.baseline();prior_rows = {r['name']:r for r in old['candidates']}
    rows = []
    for target in targets:
        name = target['name'];p = scope.ROOT/target['path'];prior = prior_rows[name]
        if state.sha(p)!=target['source_sha256'] or prior['source_sha256']!=target['source_sha256']:
            raise ValueError('target changed since original review')
        rows.append({**target,'current_references':references[name],
            'retained_historical_reference_counts':prior['reference_counts'],
            'retained_historical_sources':sorted({r['path'] for values in prior['references'].values() for r in values}),
            'decision':'DEFER_CURRENT_REFERENCE' if references[name] else 'REMOVE_CANDIDATE',
            'scope':'working source only; all historical copies remain protected'})
    docs = state.read(previous/'TEXT-REFERENCES.json')
    mentions = [r for r in docs['references'] if set(r['names']) & names]
    # Reuse only immutable baseline-bound evidence, never a missing scratch source.
    for p in [previous/'FUNCTION-REVIEW.json',previous/'TEXT-REFERENCES.json',
              scope.ROOT/'docs/research-archives/photo-prompt/SOURCE-LOCK.json',
              scope.ROOT/'docs/research-archives/photo-prompt/EXPERIMENT-LOCK.json']:
        if state.stamp(p)!=before['files'][str(p)]:raise ValueError('review evidence changed')
    new(scope.E/'REFERENCE-REVIEW.json',{'schema':'photo-four-reference-review/v1','rows':rows,
        'current_source_tests':len(paths),'prior_source_and_archive_review':old['scanned'],
        'prior_document_references':mentions,'unknown_external_callers_proved_absent':False,
        'public_routes':{'new_and_bound_H_F2':'installed sealed implementation selected by config/run binding',
            'bound_native':'existing public native route unchanged; explicit replay validates original sealed code',
            'working_generation_mismatch':'existing 77-vs-74 difference retained; not relabeled as a new regression'},
        'prior_evidence_sha256':{'FUNCTION-REVIEW':state.sha(previous/'FUNCTION-REVIEW.json'),
            'TEXT-REFERENCES':state.sha(previous/'TEXT-REFERENCES.json')},'Gemini_calls':0})
    new(scope.E/'STAGE02.json',{'status':'PASS' if all(not references[n] for n in names) else 'PASS_WITH_DEFER',
        'functions':4,'decisions':dict(Counter(r['decision'] for r in rows)),
        'scanned_current_files':len(paths),'historical_copies_retained':True,
        'additional_functions':0,'source_changes':0,'Gemini_calls':0,'CURRENT_writes':0})
    print('review:',[(r['name'],r['decision']) for r in rows],flush=True)


if __name__=='__main__':run()
