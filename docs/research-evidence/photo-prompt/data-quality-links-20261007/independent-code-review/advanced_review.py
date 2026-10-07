from __future__ import annotations

import argparse
import copy
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from unittest.mock import patch

QA = Path('/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/code-review')
PROJECT = Path('/Users/chasoik/.codex/worktrees/photo-data-quality-links/image-prompt')
ROOT = PROJECT / 'skills/photo-prompt-image-generator'
BASESTORE = QA.parents[1] / 'runtime-base'
sys.path.insert(0, str(QA/'frozen-project-v2'))
from tools.photo_data_maintenance.common import canonical, decode, digest, sha, code_binding, RECIPES
import tools.photo_data_maintenance.corpus as corpus_api
corpus_api.DEFAULT_ROOT = ROOT
import tools.photo_data_maintenance.report as report_api
from tools.photo_data_maintenance.links import build_links, path_key, query
from tools.photo_data_maintenance.reviews import review_states, load_reviews
from tools.photo_data_maintenance.quality import analyze

REPORT = QA / 'v2/baseline-report'
PATH_NODES = ['slot:light_shape:lit_clean_vertical_catchlight_pair',
              'bundle:clean_beauty_clamshell', 'profile:clamshell_dual_source_portrait_light']


def record(name, value):
    value['code_binding'] = code_binding()
    (QA/(name+'-results.json')).write_bytes(canonical(value))
    print(json.dumps(value, ensure_ascii=False, indent=2), flush=True)


def revised_manifest(directory, changes=None):
    manifest = decode((directory/'manifest.json').read_bytes())
    if changes:
        changes(manifest)
    for name in manifest['files']:
        manifest['files'][name] = sha((directory/name).read_bytes())
    manifest['report_id'] = digest({key:value for key,value in manifest.items() if key != 'report_id'})
    (directory/'manifest.json').write_bytes(canonical(manifest))
    return manifest


def runtime_copy(name):
    target = QA/name/'runtime'
    shutil.copytree(BASESTORE, target)
    return target


def review_for(inventory):
    return {'record_id':'unsubstantiated-review', 'finding_or_path_key':path_key(PATH_NODES),
            'input_entity_hashes':{row['id']:row['entity_sha256'] for row in inventory['nodes'] if row['id'] in PATH_NODES},
            'recipe_versions':RECIPES, 'decision':'retain', 'rationale':'Evidence deliberately omitted',
            'support_level':'full_support'}


def tamper():
    directory = QA/'tamper/report'
    shutil.copytree(REPORT,directory)
    old = report_api.load_report(directory,require_links=True)
    forged_review = review_for(old['inventory'])
    # Deliberately omit mandatory reviewed_at and evidence_refs.
    review_body = {'records':[forged_review],
                  'states':review_states([forged_review],old['inventory'],[],old['links'])}
    (directory/'reviews.json').write_bytes(canonical(review_body))
    (directory/'findings.json').write_bytes(canonical({'schema':'photo-data-findings/v1','findings':[]}))
    (directory/'inputs/photo_prompt_tags.json').write_bytes(b'{}')
    def change_binding(manifest):
        manifest['binding']['source_manifest_sha256'] = '1'*64
        manifest['binding']['runtime_algorithm_sha256'] = '2'*64
        manifest['findings_count'] = {'error':0,'review':0,'info':0}
    rewritten = revised_manifest(directory,change_binding)
    reviewed = report_api.load_report(directory,require_links=True)
    store = runtime_copy('tamper')
    report_api.require_current(reviewed,ROOT,store)
    result = query(reviewed['inventory'],reviewed['links'],PATH_NODES[0],reviewed['reviews'])
    path = next(row for row in result['paths'] if row['nodes']==PATH_NODES)
    candidate_input_archive = decode((directory/'inputs/photo_prompt_tags.json').read_bytes())
    reviewfile = QA/'tamper/forged-review.ndjson'
    reviewfile.write_bytes(canonical(forged_review)+b'\n')
    try:
        load_reviews(reviewfile)
        strict_review_error = None
    except ValueError as exc:
        strict_review_error = str(exc)
    record('tamper',{
        'report_load_accepted':True,'require_current_accepted':True,
        'wrong_runtime_algorithm_sha256':rewritten['binding']['runtime_algorithm_sha256'],
        'wrong_source_manifest_sha256':rewritten['binding']['source_manifest_sha256'],
        'source_input_archive':candidate_input_archive, 'original_review_findings':len(old['findings']),
        'rewritten_review_findings':len(reviewed['findings']), 'returned_review':path['review'],
        'mandatory_review_loader_rejects':strict_review_error,
        'report_directory':str(directory)})
    pinned = QA/'tamper/pinned-wrong-authority'
    shutil.copytree(REPORT,pinned)
    def wrong_authority(manifest):
        manifest['binding'].update(source_root=str(QA/'unrelated-root'),generation_id='f'*64,source_fingerprint='a'*64)
    revised_manifest(pinned,wrong_authority)
    allowed = report_api.load_report(pinned,require_links=True)
    query(allowed['inventory'],allowed['links'],PATH_NODES[0],allowed['reviews'])
    record('pinned-wrong-authority',{
        'accepted':True, 'binding':allowed['manifest']['binding'], 'report_directory':str(pinned)})


def mutate_manifest(directory):
    def update(manifest):
        manifest['created_at'] = '2026-10-07T00:00:00+00:00'
    result = revised_manifest(Path(directory),update)
    print(json.dumps({'new_report_id':result['report_id']}),flush=True)


def publication_copy_race():
    directory = QA/'publication-copy-race/report'
    shutil.copytree(REPORT,directory)
    original = report_api.load_report(directory,require_links=True)
    store = runtime_copy('publication-copy-race')
    report_store = QA/'publication-copy-race/management'
    original_copy = report_api.shutil.copytree
    triggered = []
    def copy_after_change(src,dst,*args,**kwargs):
        if Path(src)==directory and not triggered:
            edit = subprocess.run([sys.executable,str(Path(__file__)), 'mutate-manifest', str(directory)],
                                  check=True,capture_output=True,text=True)
            triggered.append(decode(edit.stdout.encode()))
        return original_copy(src,dst,*args,**kwargs)
    with patch.object(report_api.shutil,'copytree',side_effect=copy_after_change):
        pointer = report_api.activate(directory,report_store,ROOT,store,None)
    destination = report_store/'reports'/pointer['report_id']
    actual = report_api.load_report(destination,require_links=True)
    try:
        report_api.current_report(report_store,ROOT)
        current_error = None
    except ValueError as exc:
        current_error = str(exc)
    record('publication-copy-race',{
        'activate_returned_success':True, 'report_changed_after_initial_validation':bool(triggered),
        'initial_report_id':original['manifest']['report_id'],'pointer_report_id':pointer['report_id'],
        'copied_report_id':actual['manifest']['report_id'], 'pointer_matches_copied_report':pointer['report_id']==actual['manifest']['report_id'],
        'current_report_error':current_error, 'pointer':pointer,'report_store':str(report_store)})


def source_edit_worker(store, ready, stop):
    runtime,_,_ = corpus_api.runtime(ROOT)
    with runtime.source_update(ROOT,Path(store)):
        Path(ready).write_text('cooperative source edit started')
        deadline=time.monotonic()+45
        while not Path(stop).exists():
            if time.monotonic()>deadline:
                raise RuntimeError('QA writer timeout')
            time.sleep(.05)


def publication_epoch_race():
    name='publication-epoch-race'
    store = runtime_copy(name)
    report_store = QA/name/'management'
    ready = QA/name/'worker-ready'
    stop = QA/name/'worker-stop'
    original_capture = report_api.capture_generation
    calls=[]
    worker=None
    def capture_with_writer(*args,**kwargs):
        nonlocal worker
        calls.append(len(calls)+1)
        if len(calls)==2:
            worker=subprocess.Popen([sys.executable,str(Path(__file__)),'source-edit-worker',str(store),str(ready),str(stop)],
                                    stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
            deadline=time.monotonic()+20
            while not ready.exists():
                if worker.poll() is not None or time.monotonic()>deadline:
                    raise RuntimeError('QA cooperative writer failed to enter source_update')
                time.sleep(.05)
        return original_capture(*args,**kwargs)
    try:
        with patch.object(report_api,'capture_generation',side_effect=capture_with_writer):
            pointer=report_api.activate(REPORT,report_store,ROOT,store,None)
        source_revision=decode(next(store.glob('local/*/SOURCE.json')).read_bytes())
        selected=report_api.current_report(report_store,ROOT)
        try:
            report_api.require_current(report_api.load_report(selected,require_links=True),ROOT,store)
            current_error=None
        except ValueError as exc:
            current_error=str(exc)
        record(name,{
            'activate_returned_success':True, 'editing_pending_at_activation_return':bool(source_revision.get('editing')),
            'source_revision':source_revision, 'subsequent_require_current_error':current_error,
            'pointer':pointer,'report_store':str(report_store),'reprojection_calls':len(calls)})
    finally:
        stop.write_text('release QA writer')
        if worker is not None:
            worker.communicate(timeout=15)


def bundle_description_stale():
    name='bundle-description-stale'
    root=QA/name/'skill'
    assets=root/'assets'
    assets.mkdir(parents=True)
    declaration=decode((ROOT/'assets/photo_prompt_source_manifest.json').read_bytes())
    names=set(corpus_api.BASE)|{'photo_prompt_source_manifest.json'}|{row['file'] for row in declaration['sources']}
    for filename in names:
        source=ROOT/'assets'/filename
        if source.is_file():
            shutil.copyfile(source,assets/filename)
    before=corpus_api.capture_draft(root,runtime_store=QA/name/'runtime')
    row=review_for(before['inventory'])
    row.update(reviewed_at='2026-10-07T00:00:00Z',evidence_refs=['previous exact bundle description review'],support_level='partial_support')
    source_file=None
    before_description=None
    for filename in names:
        path=assets/filename
        if not path.is_file(): continue
        value=decode(path.read_bytes())
        for bundle in value.get('visual_semantics') or []:
            if bundle['id']=='clean_beauty_clamshell':
                before_description=bundle.get('primary_visual_proposition')
                bundle['primary_visual_proposition']='TODO: A single lateral source produces exactly one catchlight, with no lower frontal fill.'
                path.write_bytes(canonical(value))
                source_file=filename
    assert source_file is not None
    after=corpus_api.capture_draft(root,runtime_store=QA/name/'runtime')
    old_hashes={node['id']:node['entity_sha256'] for node in before['inventory']['nodes']}
    new_hashes={node['id']:node['entity_sha256'] for node in after['inventory']['nodes']}
    review=review_states([row],after['inventory'],analyze(after['inventory']),build_links(after['inventory']))
    record(name,{
        'source_fingerprint_changed':before['binding']['source_fingerprint']!=after['binding']['source_fingerprint'],
        'bundle_description_before':before_description, 'bundle_description_after':'TODO: A single lateral source produces exactly one catchlight, with no lower frontal fill.',
        'bundle_hash_before':old_hashes['bundle:clean_beauty_clamshell'],
        'bundle_hash_after':new_hashes['bundle:clean_beauty_clamshell'],
        'changed_entity_count':sum(old_hashes[key]!=new_hashes[key] for key in old_hashes.keys()&new_hashes.keys()),
        'effective_old_review':review[row['finding_or_path_key']],
        'unfinished_description_finding_for_bundle':any(row['rule']=='unfinished_description' and 'bundle:clean_beauty_clamshell' in row['entity_ids'] for row in analyze(after['inventory'])),
        'source_file':source_file})


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('mode',choices=['tamper','publication-copy-race','publication-epoch-race','bundle-description-stale','mutate-manifest','source-edit-worker'])
    parser.add_argument('extra',nargs='*')
    args=parser.parse_args()
    if args.mode=='mutate-manifest': mutate_manifest(*args.extra)
    elif args.mode=='source-edit-worker': source_edit_worker(*args.extra)
    else:
        {'tamper':tamper,'publication-copy-race':publication_copy_race,
         'publication-epoch-race':publication_epoch_race,'bundle-description-stale':bundle_description_stale}[args.mode]()
