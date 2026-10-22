"""Integrity validation for this research package; never qualifies native data."""
import ast,copy,csv,hashlib,json,pathlib,re,subprocess,datetime
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[3]
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
def read(name):return json.loads((HERE/name).read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def ensure(ok,message):
    if not ok:raise ValueError(message)
def validate_graph(sem,draft,kw,sources,catalog):
    cards=sem['cards'];byid={c['card_id']:c for c in cards};source_by_id={s['source_id']:s for s in sources}
    ensure(len(byid)==len(cards),'duplicate_card_id')
    ensure(sem['runtime_registration']=='none','research_registered_as_runtime')
    for c in cards:
        ensure(c['native_approval'] is False,'native_approval_not_false')
        ensure(c['semantic_authority']=='research_only','wrong_semantic_authority')
        ensure(c['proposal_en'] and c['proposal_ko'] and c['claim_limit'] and c['nearest_confusion'],'empty_card_field')
        ensure(set(c['source_ids'])<=set(source_by_id),'unknown_source')
        ensure(all(source_by_id[s]['review_status']=='targeted_passages_reviewed' for s in c['source_ids']),'unreviewed_source_used')
        ensure(set(c['proposed_slots'])<=set(catalog),'unknown_slot')
        for r in c['directed_relations']:
            ensure(set(r)=={'from','relation','to'},'bad_relation_shape')
            ensure(r['from'] in c['owners'] and r['to'] in c['owners'],'unbound_owner_endpoint')
        if c['observability'] in ('still','proxy','versioned'):
            ensure(c['owners'] and c['directed_relations'],'visual_without_visible_contract')
        for g in c['review_gates']:
            ensure(g['pixel_status']=='NOT_RUN','invented_pixel_execution')
            ensure(g['partial_is_fail'] is True and g['unobservable_is_pass'] is False,'partial_or_unobservable_promoted_to_pass')
    ensure('reality_anchor' not in byid['R01']['proposed_slots'],'SRA_slot_name_collision')
    ensure('anatomical_connection' not in byid['G07']['proposed_slots'],'robot_joint_as_biological_anatomy')
    ensure('apparatus_pov' not in byid['T04']['proposed_slots'],'device_photo_as_apparatus_view')
    ensure('reflection_logic' not in byid['N02']['proposed_slots'],'screen_recursion_as_mirror')
    visual_ids={c['card_id'] for c in cards if c['observability'] in ('still','proxy','versioned')}
    ensure(draft['runtime_import_allowed'] is False,'runtime_import_enabled')
    ensure(len({d['draft_id'] for d in draft['drafts']})==len(draft['drafts']),'duplicate_draft_id')
    ensure({d['card_id'] for d in draft['drafts']}==visual_ids,'draft_set_mismatch_or_context_export')
    for d in draft['drafts']:
        c=byid[d['card_id']]
        ensure(c['observability'] in ('still','proxy','versioned'),'context_exported_to_visual')
        ensure(d['proposal_en']==c['proposal_en'] and d['proposal_ko']==c['proposal_ko'],'draft_text_drift')
        ensure(d['owners']==c['owners'] and d['directed_relations']==c['directed_relations'],'draft_owner_or_relation_drift')
        ensure(d['native_approval'] is False and d['runtime_schema_compatible'] is False,'native_status_invented')
        ensure(d['effects_status']=='UNKNOWN_PENDING_FULL_SOURCE_REVIEW','unreviewed_effects_claimed')
        ensure(d['registration_status']=='not_in_operating_manifest' and d['evaluation_status']=='NOT_RUN','execution_status_invented')
    ensure(len({r['seed_id'] for r in kw['routes']})==len(kw['routes']),'duplicate_seed_id')
    for r in kw['routes']:
        ensure(set(r['card_ids'])<=set(byid),'unknown_route_card')
        ensure(set(r['optional_visual_card_ids'])<=visual_ids,'nonvisual_route_marked_visual')
        ensure(r['automatic_hard_obligation'] is False,'automatic_hard_activation')
    return True

def main():
    sem=read('semantic-cards.json');draft=read('candidate-drafts.json');kw=read('keyword-routes.json');sources=read('sources.json')
    catalog=json.loads((ASSETS/'photo_candidate_slot_catalog.json').read_text())['slot_catalog']
    validate_graph(sem,draft,kw,sources,catalog)
    reference=read('reference-glossary.json');expected=[]
    for table in reference['tables']:
        n=int(table['section'].split('.')[0])
        expected.extend((n,row[1] if n==4 else row[0],row) for row in table['rows'])
    ensure([(r['section'],r['term'],r['original_row']) for r in kw['routes']]==expected,'reference_coverage_or_order')
    ensure(len(expected)==268 and len(reference['tables'])==24 and {r['section'] for r in kw['routes']}==set(range(1,21)),'reference_count')
    ensure(len(sem['cards'])==103 and len(draft['drafts'])==70,'package_count_mismatch')
    ensure(sem['catalog_sha256']==sha((ASSETS/'photo_candidate_slot_catalog.json').read_bytes()),'catalog_changed_since_build')
    counts=read('PACKAGE-COUNTS.json')
    ensure(counts['targeted_sources']==sum(s['review_status']=='targeted_passages_reviewed' for s in sources),'source_count')
    snapshots=read('existing-source-mapping.json');ensure(len(snapshots)==15,'mapping_count')
    for s in snapshots:
        ensure(s['record']['id']==s['candidate_id'],'snapshot_id')
        ensure(sha(json.dumps(s['record'],sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())==s['source_sha256'],'snapshot_content_hash')
        ensure(all(b['candidate_id']==s['candidate_id'] for b in s['bindings']),'snapshot_binding_owner')
        ensure(s['native_adoption']=='not_run','snapshot_adoption_invented')
    audit=read('CORPUS-LEXICAL-AUDIT.json');ensure(not audit['selected_missing_ids'],'missing_existing_source')
    ensure(not audit['snapshot_changed_during_read'],'mixed_snapshot_during_read')
    with (HERE/'EVALUATION-CASES.tsv').open() as f:cases=list(csv.DictReader(f,delimiter='\t'))
    ensure(len(cases)==78 and len({c['case_id'] for c in cases})==78,'evaluation_count')
    ensure(all(c['status']=='NOT_RUN' and c['query_en'] and c['query_ko'] for c in cases),'evaluation_execution_or_missing_query')
    ensure(all(not re.search('[가-힣]',c['query_en']) for c in cases),'untranslated_english_query')
    manifest=json.loads((ASSETS/'photo_candidate_corpus_manifest.json').read_text())
    ensure(not any('photo_candidate_scp_20261022' in m['file'] for m in manifest['modules']),'research_registered_in_manifest')
    for p in HERE.glob('*.py'):ast.parse(p.read_text(),filename=p.name)
    for p in HERE.glob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            if '://' in target or target.startswith('#'):continue
            ensure((p.parent/target.split('#')[0]).exists(),f'broken_local_link:{p.name}:{target}')
    mutations=[
      ('missing_owner',lambda s,d,k,z:s['cards'][0]['owners'].pop('researcher')),
      ('foreign_endpoint',lambda s,d,k,z:s['cards'][0]['directed_relations'][0].update(to='unbound_other_body')),
      ('unknown_slot',lambda s,d,k,z:s['cards'][0]['proposed_slots'].append('invented_scp_slot')),
      ('foreign_source',lambda s,d,k,z:s['cards'][0]['source_ids'].append('S999')),
      ('native_approval',lambda s,d,k,z:s['cards'][0].update(native_approval=True)),
      ('unknown_keyword_target',lambda s,d,k,z:k['routes'][0]['card_ids'].append('NO_SUCH_CARD')),
      ('automatic_activation',lambda s,d,k,z:k['routes'][0].update(automatic_hard_obligation=True)),
      ('draft_text_drift',lambda s,d,k,z:d['drafts'][0].update(proposal_en='unrelated replacement text')),
      ('unreviewed_effects',lambda s,d,k,z:d['drafts'][0].update(effects_status='NO_EFFECTS')),
      ('partial_pass',lambda s,d,k,z:s['cards'][0]['review_gates'][0].update(partial_is_fail=False)),
      ('unobservable_pass',lambda s,d,k,z:s['cards'][0]['review_gates'][0].update(unobservable_is_pass=True)),
      ('runtime_import',lambda s,d,k,z:d.update(runtime_import_allowed=True)),
      ('context_visual_export',lambda s,d,k,z:d['drafts'][0].update(card_id='N01')),
      ('unreviewed_source_authority',lambda s,d,k,z:z[0].update(review_status='collected_not_substantively_reviewed')),
    ]
    rejected=[]
    for name,mutation in mutations:
        s,d,k,z=copy.deepcopy((sem,draft,kw,sources));mutation(s,d,k,z)
        try:validate_graph(s,d,k,z,catalog)
        except (ValueError,KeyError) as e:rejected.append({'mutation':name,'rejected':True,'reason':str(e)})
        else:raise ValueError('mutation_was_accepted:'+name)
    baseline=read('BASELINE.json');changed=[];missing=[]
    for f,h in baseline['tracked_sha256'].items():
        q=ROOT/f
        if not q.is_file():missing.append(f)
        elif sha(q.read_bytes())!=h:changed.append(f)
    audit_drift=[f for f,h in audit['source_module_sha256'].items() if not (ASSETS/f).is_file() or sha((ASSETS/f).read_bytes())!=h]
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    drift={'date':'2026-10-22','baseline_head':baseline['head'],'current_head':head,'head_changed':head!=baseline['head'],
      'tracked_files_changed_from_baseline':changed,'tracked_files_missing':missing,'corpus_modules_changed_since_snapshot':audit_drift,
      'manifest_changed_since_snapshot':sha((ASSETS/'photo_candidate_corpus_manifest.json').read_bytes())!=audit['manifest_sha256'],
      'scope_note':'This task writes research files only; observed concurrent checkout changes are preserved. Rebaseline before implementation.'}
    (HERE/'SOURCE-DRIFT.json').write_text(json.dumps(drift,ensure_ascii=False,indent=2)+'\n')
    members=[p for p in HERE.iterdir() if p.is_file() and p.name not in ('VALIDATION.json','SHA256SUMS')]
    lines=[sha(p.read_bytes())+'  '+p.name for p in sorted(members)]
    (HERE/'SHA256SUMS').write_text('\n'.join(lines)+'\n')
    has_drift=bool(changed or missing or audit_drift or drift['head_changed'] or drift['manifest_changed_since_snapshot'])
    result={'date':'2026-10-22','status':'STRUCTURE_PASS_REBASELINE_REQUIRED' if has_drift else 'STRUCTURE_PASS',
      'research_structure_pass':True,'counts':counts,'reference_coverage':{'tables':24,'entries':268,'sections':20},
      'existing_source_snapshots':len(snapshots),'snapshot_content_hashes':'pass','corpus_read_atomicity':'pass',
      'catalog_slot_existence':'pass','specific_slot_collision_checks':'pass','local_links':'pass','python_syntax':'pass',
      'mutation_rejections':rejected,'checksum_members':len(members),'checksum_file_sha256':sha((HERE/'SHA256SUMS').read_bytes()),
      'concurrent_changed_tracked_files':len(changed),'corpus_modules_changed_after_snapshot':audit_drift,
      'runtime_registration':'NOT_RUN','embedding_calls':0,'image_calls':0,'retrieval_execution':'NOT_RUN','native_qualification':'NOT_RUN','pixel_review':'NOT_RUN','installation':'NOT_RUN','commit_push':'NOT_RUN','user_judgment':'not_yet_received',
      'limit':'Integrity/graph/coverage checks only. Not independent semantic verification, native source admission, retrieval quality, generated-pixel success or user acceptance.'}
    (HERE/'VALIDATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'counts':counts,'mutations_rejected':len(rejected),'checksummed_files':len(members),'changed_tracked_files':len(changed),'corpus_drift':audit_drift},ensure_ascii=False))
if __name__=='__main__':main()
