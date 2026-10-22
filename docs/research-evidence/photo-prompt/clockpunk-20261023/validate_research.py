"""Validate research referential integrity and protection evidence, never native truth."""
import collections,csv,hashlib,json,pathlib,re,subprocess,sys
HERE=pathlib.Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def read(n):return json.loads((HERE/n).read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def main():
    errors=[];checks=[];observations=[]
    def check(label,ok,detail=None):
        checks.append(dict(check=label,status='PASS' if ok else 'FAIL',detail=detail))
        if not ok:errors.append(label)
    def observe(label,unchanged,detail):
        observations.append(dict(observation=label,status='UNCHANGED' if unchanged else 'DRIFT_OBSERVED',detail=detail))
    dom=read('reference-dom.json');routes=read('keyword-routes.json')['routes'];cards=read('semantic-cards.json')['cards'];drafts=read('candidate-drafts.json')['drafts'];sources=read('sources.json')['sources'];counts=read('PACKAGE-COUNTS.json');mapping=read('existing-source-mapping.json');baseline=read('BASELINE.json')
    cids={c['card_id'] for c in cards};sids={s['source_id'] for s in sources};byid={c['card_id']:c for c in cards}
    check('reference_table_rows_exactly_routed',len(routes)==sum(len(t)-1 for t in dom['tables'])==213)
    exact=all(r['original_cells']==dom['tables'][r['table']-1][r['row']] for r in routes)
    positions=[(r['table'],r['row']) for r in routes]
    check('reference_rows_byte_equivalent_and_unique',exact and len(positions)==len(set(positions)))
    check('unique_card_source_draft_ids',len(cards)==len(cids) and len(sources)==len(sids) and len(drafts)==len({d['draft_id'] for d in drafts}))
    check('all_route_targets_and_source_refs_exist',all(set(r['card_ids'])<=cids and set(r['source_ids'])<=sids for r in routes))
    check('all_cards_are_routed',cids=={x for r in routes for x in r['card_ids']})
    check('all_graph_endpoints_owned',all(e['from'] in c['owners'] and e['to'] in c['owners'] for c in cards for e in c['directed_relations']))
    check('no_disconnected_declared_owner',all(set(c['owners'])=={e[k] for e in c['directed_relations'] for k in ('from','to')} for c in cards))
    check('gate_identity_and_context_layer',all(len(c['gates'])==len(c['directed_relations']) and all(g['required_relation']==e and g['both_endpoints_required'] and not g['unobservable_is_pass'] and g['partial_is_fail'] and (g['claim_layer']=='declared_context_only')==(c['observability']=='context_only') for g,e in zip(c['gates'],c['directed_relations'])) for c in cards))
    check('sources_resolve_and_claim_limits_nonempty',all(set(c['source_ids'])<=sids and c['claim_limit_ko'].strip() and c['nearest_confusion_ko'].strip() for c in cards))
    check('all_drafts_bilingual_nonidentical',all(d['proposal_en'].strip() and d['proposal_ko'].strip() and d['proposal_en']!=d['proposal_ko'] for d in drafts))
    check('drafts_exact_visual_subset', {d['card_id'] for d in drafts}=={c['card_id'] for c in cards if c['observability']!='context_only'})
    check('no_context_only_card_in_positive_routes',all(all(byid[x]['observability']!='context_only' for x in r['optional_visual_card_ids']) for r in routes))
    check('no_runtime_import_or_native_approval_claim',not read('semantic-cards.json')['runtime_import_allowed'] and not read('candidate-drafts.json')['runtime_import_allowed'] and all(c['native_approval'] is False and c['runtime_registration']=='none' and not c['automatic_activation'] for c in cards) and all(d['runtime_schema_compatible'] is False and d['native_effects']=='UNKNOWN_PENDING_FULL_SOURCE_REVIEW' for d in drafts))
    A=ROOT/'skills/photo-prompt-image-generator/assets';catalog_bytes=(A/'photo_candidate_slot_catalog.json').read_bytes();catalog=json.loads(catalog_bytes)['slot_catalog']
    check('slot_catalog_snapshot_still_matches',sha(catalog_bytes)==read('semantic-cards.json')['catalog_sha256'])
    check('all_proposed_slots_exist',all(set(c['proposed_slots'])<=set(catalog) for c in cards))
    check('all_sources_explicit_read_scopes',all(s['read_scope'] and s['limitation_ko'] and s['url'].startswith('https://') and s['full_work_read'] is False and s['image_inspection']=='not_performed' for s in sources))
    with (HERE/'EVALUATION-CASES.tsv').open() as f:cases=list(csv.DictReader(f,delimiter='\t'))
    check('evaluation_inventory_and_not_run',len(cases)==counts['evaluation_cases'] and len(cases)*2==counts['evaluation_queries'] and all(r['query_en'] and r['query_ko'] and r['status']=='NOT_RUN' for r in cases))
    check('package_counts_consistent',counts['cards']==len(cards) and counts['optional_visual_drafts']==len(drafts) and counts['sources']==len(sources) and counts['reference_entries']==len(routes) and counts['card_modes']==dict(collections.Counter(c['observability'] for c in cards)))
    check('read_scope_counts_consistent',counts['source_access']==dict(collections.Counter(s['access_status'] for s in sources)))
    module_drift=[name for name,h in mapping['module_sha256'].items() if not (A/name).exists() or sha((A/name).read_bytes())!=h]
    check('authored_source_modules_unchanged_since_snapshot',not module_drift,module_drift)
    check('source_manifest_snapshot_still_matches',sha((A/'photo_candidate_corpus_manifest.json').read_bytes())==mapping['source_manifest_sha256'])
    check('record_snapshot_hashes_and_binding_owners',all(sha(canonical(r['record']))==r['record_sha256'] and r['record']['id']==r['candidate_id'] and all(b['candidate_id']==r['candidate_id'] for b in r['bindings']) for r in mapping['records']))
    drift=[]
    for name,h in baseline['tracked_hashes'].items():
        p=ROOT/name
        if not p.is_file() or sha(p.read_bytes())!=h:drift.append(name)
    observe('preexisting_tracked_bytes',not drift,{'tracked_files':len(baseline['tracked_hashes']),'drift':drift,'limit':'Drift is not attributed by the hash. All mutations performed by this task were confined to its new research folder.'})
    current_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()
    observe('head',current_head==baseline['head'],{'start':baseline['head'],'end':current_head})
    old_status=set(baseline['git_status_porcelain']);current_status=subprocess.check_output(['git','status','--porcelain=v1','-uall'],cwd=ROOT).decode().splitlines()
    owned_prefix='docs/research-evidence/photo-prompt/clockpunk-20261023/'
    outside=[r for r in current_status if r not in old_status and not r[3:].startswith(owned_prefix)]
    observe('new_git_status_outside_research_folder',not outside,outside)
    runtime_targets=['photo_clockpunk_semantics_20261023.json','photo_candidate_clockpunk_20261023.json','photo_candidate_clockpunk_bindings_20261023.json']
    check('planned_operating_modules_not_created',not any((A/n).exists() for n in runtime_targets))
    # Local document targets only. External URLs and hashes are not fetched here.
    missing=[]
    for p in HERE.glob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            if '://' not in target and not target.startswith('#') and target not in ('VALIDATION.json','SHA256SUMS') and not (p.parent/target.split('#')[0]).exists():missing.append([p.name,target])
    check('local_document_links_resolve',not missing,missing)
    workspace_drift=any(o['status']=='DRIFT_OBSERVED' for o in observations)
    result=dict(status='FAIL' if errors else 'PASS_WITH_WORKSPACE_DRIFT' if workspace_drift else 'PASS',research_structure_status='FAIL' if errors else 'PASS',workspace_status='DRIFT_OBSERVED' if workspace_drift else 'UNCHANGED',scope='Research structure, references and authored source snapshot integrity only. Workspace-wide preservation observations are separate; no automatic natural-language, engineering, native, retrieval or image truth verification.',checks=checks,workspace_observations=observations,errors=errors,
      counts=counts,gate_count=sum(len(c['gates']) for c in cards),baseline_head=baseline['head'],
      untouched_untracked_limit='Initial untracked names were recorded; they were not all hashed. Tracked bytes and all authored source module bytes were independently compared.',
      execution={'operating_source_changes':'NOT_RUN','native_qualification':'NOT_RUN','index_embedding_retrieval':'NOT_RUN','installed_activation':'NOT_RUN','source_image_inspection':'NOT_RUN','image_generation_pixel_review':'NOT_RUN','user_acceptance':'NOT_RUN','commit_push':'NOT_RUN'})
    (HERE/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    sums=[]
    for p in sorted(HERE.rglob('*')):
        if p.is_file() and p.name!='SHA256SUMS' and '__pycache__' not in p.parts:sums.append(f'{sha(p.read_bytes())}  {p.relative_to(HERE)}')
    (HERE/'SHA256SUMS').write_text('\n'.join(sums)+'\n')
    print(json.dumps({'status':result['status'],'checks':len(checks),'errors':errors,'gate_count':result['gate_count'],'tracked_files_checked':len(baseline['tracked_hashes']),'files_hashed':len(sums)},ensure_ascii=False,indent=2))
    return 0 if not errors else 1
if __name__=='__main__':sys.exit(main())
