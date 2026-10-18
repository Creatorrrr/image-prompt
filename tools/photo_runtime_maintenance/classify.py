"""Conservative cleanup actions from explicit sources, seals and existing work."""
from pathlib import Path
import ast
import subprocess

from state import ROOT, SHARED, EVIDENCE, read, write, sha, stamp, files, worktrees

EXPERIMENTS = ('candidate-semantic-renewal-20261018',
               'candidate-recall-followup-20261019', 'recall-improvement-consult-20261018')
MODULES = tuple('photo_candidate_'+n for n in
                ('authoring','review','documents','evaluation','lane_documents','lane_generation'))
TESTS = ('tests/test_photo_candidate_authoring.py','tests/test_photo_candidate_lanes.py')


def main():
    if (EVIDENCE/'STAGE03.json').exists():
        raise ValueError('classification already sealed; do not replace the cleanup action list')
    b = read(EVIDENCE/'BASELINE.json.gz')
    dirty = b['repositories'][str(ROOT)]['status']
    exp_files = [p for name in EXPERIMENTS for p in files(ROOT/'docs/research-evidence/photo-prompt'/name)]
    requested = [str(p.relative_to(ROOT)) for p in exp_files]
    requested += ['skills/photo-prompt-image-generator/scripts/'+m+'.py' for m in MODULES]
    requested += list(TESTS)
    requested = sorted(set(requested))
    module_refs = []
    for root in worktrees():
        skill = root/'skills/photo-prompt-image-generator'
        for p in [*skill.glob('scripts/*.py'), *skill.glob('precore/*.py'), *root.glob('tests/*.py')]:
            tree = ast.parse(p.read_text())
            for node in ast.walk(tree):
                names = ([a.name for a in node.names] if isinstance(node,ast.Import) else
                         [node.module or ''] if isinstance(node,ast.ImportFrom) else [])
                for name in names:
                    if name.split('.')[0] in MODULES or name in ('tests.test_photo_candidate_authoring','tests.test_photo_candidate_lanes'):
                        module_refs.append({'file':str(p),'import':name})
    # Include literal CLI/dynamic references outside ordinary imports. No provider is loaded.
    pattern = '|'.join(MODULES+('test_photo_candidate_authoring','test_photo_candidate_lanes'))
    external_stores = [SHARED.parent/n for n in ('candidate-semantic-renewal-20261018','candidate-recall-followup-20261019')]
    command = ['rg','--files-with-matches','--no-ignore','-g','*.py','-g','*.json','-g','*.md',
               '-g','!**/.git/**','-g','!**/.runtime/**','-g','!**/.venv/**','-g','!**/__pycache__/**',
               pattern,*map(str,[*worktrees(),SHARED,*external_stores])]
    result = subprocess.run(command,capture_output=True,text=True)
    if result.returncode not in (0,1):
        raise ValueError('reference scan incomplete: '+result.stderr[:500])
    text_refs = sorted(set(result.stdout.splitlines()))
    supplementary = {str(p):stamp(p) for p in files(SHARED.parent)
                     if p.name=='CURRENT.json' and str(p) not in b['files']}
    for store in external_stores:
        for p in files(store):
            if p.suffix=='.py' or p.name=='manifest.json':
                supplementary[str(p)] = stamp(p)
    write(EVIDENCE/'ADDITIONAL-PROTECTED.json.gz',supplementary)
    actions = []
    for rel in requested:
        p = ROOT/rel
        if '__pycache__' in p.parts or p.suffix=='.pyc':
            continue  # Caches are considered separately, never captured as source.
        reason = 'closed inactive source-review/lane experiment; exact relative tree retained offline'
        action = 'ARCHIVE_EXPERIMENT'
        if rel in dirty:
            action, reason = 'DEFER', 'original uncommitted work'
        if not p.is_file() or p.is_symlink():
            action, reason = 'DEFER', 'nonregular or absent original'
        actions.append({'path':rel,'action':action,'reason':reason,'sha256':sha(p) if p.is_file() else None,
                        'bytes':p.stat().st_size if p.is_file() else 0})
    outside_imports = [r for r in module_refs if r['file'].startswith(str(ROOT)+'/')
                       and str(Path(r['file']).relative_to(ROOT)) not in requested]
    if outside_imports:
        raise ValueError('operating/test import outside archive closure: '+str(outside_imports))
    # Do not infer unreferenced status from just the current source manifest.
    skill = ROOT/'skills/photo-prompt-image-generator'
    active = read(skill/'assets/photo_candidate_search.json')['layout_id']
    shard_rows = []
    for p in sorted((skill/'assets/photo_candidate_search_shards').iterdir()):
        if p.is_dir():
            members = list(files(p))
            shard_rows.append({'path':str(p.relative_to(ROOT)), 'action':'KEEP_RUNTIME' if p.name==active else 'DEFER',
               'reason':'current native source manifest' if p.name==active else 'historical frozen manifests/receipts and other worktree references not fully discharged',
               'files':len(members),'logical_bytes':sum(f.stat().st_size for f in members)})
    # Whole sealed snapshots and old root code remain protected, even when not default.
    kept = [{'path':'skills/photo-prompt-image-generator/scripts/photo_workflow.py','action':'KEEP_RUNTIME'},
            {'path':'skills/photo-prompt-image-generator/scripts/photo_installed_h_f2.py','action':'KEEP_RUNTIME'},
            {'path':'skills/photo-prompt-image-generator/candidate-authoring/v1','action':'KEEP_MAINTENANCE'},
            {'path':'tests/photo_slot_oracle.py','action':'KEEP_MAINTENANCE'},
            {'path':'all existing sealed generations, receipts, models and CURRENT pointers','action':'KEEP_REPLAY'},
            *[{'path':str(p),'action':'KEEP_REPLAY','reason':'self-contained inactive generations retained; archive replay does not remove cache'} for p in external_stores]]
    write(EVIDENCE/'REFERENCE-GRAPH.json.gz',{'imports':module_refs,'literal_reference_files':text_refs,
          'dynamic_and_hash_rule':'frozen experiment files retained byte-identically in the restored original tree',
          'opaque_archives_and_unresolved_external_references':'DEFER; never garbage-collect sealed stores'})
    write(EVIDENCE/'ACTION-LIST.json',{'schema':'photo-cleanup-actions/v1','archive':actions,
          'shards':shard_rows,'keep':kept,'all_original_dirty_paths':'DEFER/PRESERVE',
          'all_other_historical_evidence':'DEFER unless a separately verified closed bundle is enumerated',
          'retained_worktree':'codex/slot-search-relevance'})
    write(EVIDENCE/'STAGE03.json',{'status':'PASS','archive_files':sum(r['action']=='ARCHIVE_EXPERIMENT' for r in actions),
          'deferred_archive_files':sum(r['action']=='DEFER' for r in actions),
          'static_import_edges':len(module_refs),'literal_reference_files':len(text_refs),
          'outside_operating_imports':outside_imports,'deferred_old_shard_generations':len(shard_rows)-1,
          'unresolved_run_references':len(read(EVIDENCE/'RUN-BINDINGS.json.gz')['unresolved']),
          'additional_protected_metadata_files':len(supplementary),
          'Gemini_calls':0,'CURRENT_writes':0})
    print('classification PASS',len(actions),'archive paths;',len(text_refs),'literal reference files')


if __name__ == '__main__':
    main()
