"""Validate the research package and record limits; does not exercise runtime."""
from __future__ import annotations
import ast
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'

def read(name): return json.loads((HERE/name).read_text())
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def write(name,value): (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

def main():
    source=read('SOURCE-KEYWORDS.json')['entries']
    decisions=read('TERM-DECISIONS.json')['decisions']
    units=read('CANDIDATE-DRAFTS.json')['candidates']
    sources=read('SOURCES.json')['sources']
    adoption=read('ADOPTION-MAP.json')['entries']
    probes=read('REGRESSION-PLAN.json')
    inventory=read('AUTHORING-INVENTORY.json')
    snapshot=read('CHECKOUT-SNAPSHOT.json')
    counts=read('PACKAGE-COUNTS.json')
    cov=read('EXISTING-COVERAGE.json')
    checks=[]
    def check(label,condition):
        if not condition: raise ValueError(label)
        checks.append(label)
    expected=list(range(1,141))
    check('source has exactly 140 consecutively numbered entries', [e['number'] for e in source]==expected)
    check('all 140 terms have exactly one research decision', [e['number'] for e in decisions]==expected)
    check('decision labels preserve source labels', all(a['label']==b['source_label'] for a,b in zip(source,decisions)))
    sid={s['id'] for s in sources}
    uid={u['id'] for u in units}
    catalogue={(e['file'],e['slot'],e['id']) for e in inventory['candidate_catalog']}
    check('source identities are unique', len(sid)==len(sources)==46)
    check('source URLs and access limits are explicit',all(s['url'].startswith('https://') and s['access'] and s['limits'] for s in sources))
    check('all decision source references exist', all(set(e['source_ids'])<=sid for e in decisions))
    check('all decision unit references exist',all(set(e['proposed_unit_ids'])<=uid for e in decisions))
    check('unit identities are unique and counted',len(uid)==len(units)==78==counts['proposed_units'])
    check('all units have term lineage and source lineage',all(u['source_term_numbers'] and set(u['source_ids'])<=sid for u in units))
    check('all units have concrete components and directed relations',all(len(u['proposed_concept_units'])>=2 and u['proposed_relations'] for u in units))
    check('all relation endpoints are declared research roles',all({r['subject'] for r in u['proposed_relations']}|{r['object'] for r in u['proposed_relations']}==set(u['proposed_entity_roles']) for u in units))
    check('all research predicates and effect scopes are explicitly non-executable',all(u['status']=='PROPOSED_NOT_INTEGRATED' and u['effect_axes_status']=='UNVALIDATED_NONEXHAUSTIVE_REVIEW_HYPOTHESES' and all(r['status']=='proposed_graph_not_runtime_enum' for r in u['proposed_relations']) for u in units))
    check('adoption map covers exactly the research unit IDs',len(adoption)==len(units) and {a['research_unit_id'] for a in adoption}==uid)
    check('adoption phases are defined in the implementation plan',all(a['priority'] in {'P1','P2','P3','P4'} for a in adoption))
    for d in decisions:
        for reuse in d['reuse']:
            check(f'reuse {d["number"]}:{reuse["id"]} exists in captured authored catalogue',all((e['file'],e['slot'],reuse['id']) in catalogue for e in reuse['records']))
    check('all existing proposed owner files are present or declared new',all((ASSETS/u['proposed_owner_file']).is_file() or u['proposed_owner_file']=='photo_prompt_intellectual_activity_extension.json' for u in units))
    check('research unit IDs do not silently overwrite captured active IDs',not uid&{e['id'] for e in inventory['candidate_catalog']})
    check('83 captured source files and hash provenance exist',len(snapshot['authored_source_sha256'])==83 and all(len(v)==64 for v in snapshot['authored_source_sha256'].values()))
    check('inventory count agrees with the audit snapshot',len(catalogue)==cov['distinct_slot_and_id_count']==9949 and len(inventory['profile_catalog'])==cov['authored_profile_record_count']==1774)
    check('exact inventory metrics are unchanged and labelled as non-coverage',cov['terms_with_exact_candidate_label']==22 and cov['terms_with_exact_profile_label']==0 and 'NOT' in cov['method'])
    cases=probes['semantic_cases']; gates=probes['native_pixel_gates']
    check('82 unique semantic probes remain explicitly unexecuted',len(cases)==len({c['id'] for c in cases})==82 and all(c['status']=='PLANNED_NOT_EXECUTED' for c in cases))
    check('16 unique native gates require all-of and remain unscored',len(gates)==len({g['id'] for g in gates})==16 and all(g['partial_is_fail'] and g['status']=='PLANNED_NOT_GENERATED_NOT_SCORED' for g in gates))
    check('planned cases reference existing research units and source numbers',all(set(c['proposed_unit_ids'])<=uid and set(c['source_term_numbers'])<=set(expected) for c in cases+gates))
    check('all native gates have explicit visible clauses',all(len(g['required_all_of'])>=4 and g['fail_if'] for g in gates))
    for path in HERE.glob('*.py'): ast.parse(path.read_text())
    check('research scripts parse without executing generation',True)
    broken=[]
    for path in HERE.glob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if target.startswith(('https://','http://','chatgpt-conversation://','#')): continue
            target=target.split('#')[0]
            if target in {'VALIDATION.json','MANIFEST.json'}: continue
            if not (path.parent/target).exists(): broken.append(f'{path.name}: {target}')
    check('local Markdown artifact and contract links resolve',not broken)
    changed=[]; missing=[]
    for name,sha in snapshot['authored_source_sha256'].items():
        path=ASSETS/name
        if not path.exists(): missing.append(name)
        elif digest(path)!=sha: changed.append(name)
    generator=ROOT/'skills/photo-prompt-image-generator/scripts/prompt_generator.py'
    validation=dict(schema_version='intellectual-research-validation/v1',
        status='PASS_RESEARCH_PACKAGE_STRUCTURE_ONLY',date_kst='2026-10-05',
        passed_checks=len(checks),checks=checks,
        counts=dict(source_terms=len(source),decisions=len(decisions),sources=len(sources),proposed_units=len(units),
                    reused_candidate_ids=counts['unique_reuse_candidate_ids'],retained_reuse_records=counts['retained_reuse_records'],
                    semantic_probes_planned=len(cases),native_gates_planned=len(gates)),
        source_access_counts=dict(Counter(s['access'] for s in sources)),
        live_snapshot_comparison=dict(changed_authored_files=changed,missing_authored_files=missing,
            generator_changed=digest(generator)!=snapshot['generator_sha256'],
            boundary='Comparison only. Concurrent checkout drift does not invalidate the captured research catalogue; re-audit before implementation.'),
        scope=dict(runtime_assets_modified_by_this_research=False,active_index_rebuilt=False,
                   runtime_tests_executed=False,candidate_pack_exposure_evaluated=False,
                   candidate_selection_evaluated=False,images_generated=0,native_pixels_evaluated=False,
                   user_acceptance_evaluated=False,commit_push_publish_performed=False),
        limitations=['Source reading includes labelled search excerpts and one failed full open.',
                     'No original museum/source-image pixel annotations or live generated-image evaluation.',
                     'Candidate graphs and effect axes are hypotheses, not runtime enums or complete property-effect declarations.',
                     'Temporal, identity and contextual claims cannot be qualified from a single still.',
                     'Historical/tool/language/music/game-content fixtures require the additional checks named in the plan.'])
    write('VALIDATION.json',validation)
    manifest=[]
    for path in sorted(HERE.iterdir()):
        if path.is_file() and path.name!='MANIFEST.json':
            manifest.append(dict(file=path.name,size_bytes=path.stat().st_size,sha256=digest(path)))
    write('MANIFEST.json',dict(schema_version='intellectual-research-manifest/v1',files=manifest,
        boundary='Hashes of this research package only. The manifest does not hash itself.'))
    print(json.dumps(dict(status=validation['status'],checks=len(checks),counts=validation['counts'],
        changed_authored_files=len(changed),missing_authored_files=len(missing),generator_changed=validation['live_snapshot_comparison']['generator_changed']),ensure_ascii=False))

if __name__=='__main__': main()
