#!/usr/bin/env python3
"""Gated local activation and explicit Gemini rollback, preserving all shards."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import photo_candidate_corpus as c
import photo_search_layout as layout
from photo_embedding_provider import atomic,GEMINI_SPACE
from photo_local_embedding import ROOT,space as local_space
from photo_runtime_sources import source_update,SnapshotPublisher


def activate(assets,qualification,backup,store=None):
    """Only a complete, frozen, qualified same-source candidate can become active."""
    assets=Path(assets);qualification=Path(qualification);backup=Path(backup)
    decision=json.loads((qualification/'ADOPTION.json').read_bytes())
    if decision.get('schema')!='photo-local-embedding-adoption/v1' or decision.get('passed') is not True:
        raise ValueError('local model did not pass all required qualification gates')
    for name,sha in decision['evidence_sha256'].items():
        if hashlib.sha256((qualification/name).read_bytes()).hexdigest()!=sha:raise ValueError('qualification evidence changed')
    report=json.loads((qualification/'vector-summary.json').read_bytes())
    if not report.get('vector_quality_pass') or any(r['recall5_delta']<-.02-1e-12 for r in report['languages'].values()):
        raise ValueError('vector quality gate failed')
    hybrid=json.loads((qualification/'hybrid-summary.json').read_bytes())
    if hybrid.get('forbidden_adoptions')!=0 or hybrid.get('audit_pass') is not True or any(v['positive_hits']!=v['positive_cases'] for v in hybrid['languages'].values()):
        raise ValueError('hybrid regression gate failed')
    offline=json.loads((qualification/'offline-public.json').read_bytes())
    if len(offline['results'])!=2 or any(r['exit_code']!=0 or r['seconds']>60 or r['max_child_rss_bytes']>4*1024**3 for r in offline['results']):
        raise ValueError('offline/performance gate failed')
    current=c.load(ROOT/'assets');candidate=c.load(assets)
    if c.digest(current)!=c.digest(candidate) or decision['corpus_sha256']!=c.digest(current):raise ValueError('current source differs from qualified source')
    manifest=json.loads((assets/layout.MANIFEST).read_bytes())
    if manifest['space']!=local_space() or manifest['layout_id']!=report['local_layout_id']:raise ValueError('qualified model/layout differs')
    layout.verify(assets,candidate,manifest)
    backup.mkdir(parents=True,exist_ok=False)
    old_manifest=(ROOT/'assets'/layout.MANIFEST).read_bytes()
    (backup/layout.MANIFEST).write_bytes(old_manifest)
    default=ROOT/'embedding-default.json'
    if default.exists():(backup/'embedding-default.json').write_bytes(default.read_bytes())
    old_pointer=SnapshotPublisher(ROOT,store).directory/'CURRENT.json'
    if old_pointer.exists():(backup/'CURRENT.json').write_bytes(old_pointer.read_bytes())
    try:
        with source_update(ROOT,store):
            for row in manifest['shards']+[manifest['metadata']]:
                src=assets/row['path'];dest=ROOT/'assets'/row['path']
                if src.is_symlink() or assets.resolve() not in src.resolve().parents:raise ValueError('unsafe qualified shard')
                if dest.exists():
                    if hashlib.sha256(dest.read_bytes()).hexdigest()!=row['sha256']:raise ValueError('protected shard collision')
                else:dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
            atomic(ROOT/'assets'/layout.MANIFEST,manifest)
            atomic(default,{'schema':'photo-embedding-default/v1','provider':'embeddinggemma2-local','space':manifest['space'],
                            'qualification_sha256':hashlib.sha256((qualification/'ADOPTION.json').read_bytes()).hexdigest()})
        pointer=SnapshotPublisher(ROOT,store).publish()
    except Exception:
        # Leave original Gemini bytes recoverable even if publication fails.
        with source_update(ROOT,store):
            atomic(ROOT/'assets'/layout.MANIFEST,json.loads(old_manifest))
            if (backup/'embedding-default.json').exists():atomic(default,json.loads((backup/'embedding-default.json').read_bytes()))
            elif default.exists():default.unlink()
        SnapshotPublisher(ROOT,store).publish()
        raise
    atomic(backup/'ACTIVATION.json',{'schema':'photo-local-activation/v1','local_layout_id':manifest['layout_id'],'publication':pointer})
    return pointer


def rollback(backup,store=None):
    backup=Path(backup);manifest=json.loads((backup/layout.MANIFEST).read_bytes())
    if manifest['space']!=GEMINI_SPACE:raise ValueError('rollback backup must contain the preserved Gemini layout')
    layout.verify(ROOT/'assets',c.load(ROOT/'assets'),manifest)
    with source_update(ROOT,store):
        atomic(ROOT/'assets'/layout.MANIFEST,manifest)
        atomic(ROOT/'embedding-default.json',{'schema':'photo-embedding-default/v1','provider':'gemini'})
    return SnapshotPublisher(ROOT,store).publish()


def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    a=sub.add_parser('activate');a.add_argument('--assets',type=Path,required=True);a.add_argument('--qualification',type=Path,required=True);a.add_argument('--backup',type=Path,required=True)
    r=sub.add_parser('rollback');r.add_argument('--backup',type=Path,required=True)
    for cmd in (a,r):cmd.add_argument('--runtime-store',type=Path)
    args=p.parse_args()
    result=activate(args.assets,args.qualification,args.backup,args.runtime_store) if args.command=='activate' else rollback(args.backup,args.runtime_store)
    print(json.dumps(result))


if __name__=='__main__':main()
