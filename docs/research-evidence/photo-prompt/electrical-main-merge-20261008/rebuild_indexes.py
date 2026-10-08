"""Rebuild merged authored sources with exact compatible vectors; no API calls."""
from __future__ import annotations
import argparse
import gc
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
SKILL=ROOT/'skills/photo-prompt-image-generator'
sys.path.insert(0,str(SKILL/'scripts'))
import prompt_generator as pg
import build_semantic_index as semantic
import build_visual_profile_index as visual
from photo_runtime_sources import source_update,SnapshotPublisher

def denied(*a,**kw): raise AssertionError('Offline rebuild requires exact matching cached vectors')

def main():
    p=argparse.ArgumentParser();p.add_argument('--cache-root',type=Path,action='append',required=True);p.add_argument('--report-name',default='INDEX-REBUILD.json');a=p.parse_args()
    assert Path(a.report_name).name==a.report_name
    semantic.embed_texts_with_gemini=visual.embed_texts_with_gemini=denied
    semantic.load_project_env=visual.load_project_env=lambda:None
    def no_network(event,args):
        if event in {'socket.connect','socket.getaddrinfo'}:raise AssertionError('Offline rebuild attempted network')
    sys.addaudithook(no_network)
    assets=SKILL/'assets';sem=assets/'photo_prompt_semantic_index.json';vis=assets/'photo_prompt_visual_profile_index.json'
    metadata=json.loads(sem.read_text());provider,model,dimensions=[metadata[k] for k in ['provider','embedding_model','embedding_dimensions']]
    data=pg.load_json(assets/'photo_prompt_tags.json');registry=pg.load_visual_obligation_registry(assets/'photo_prompt_visual_obligations.json')
    vectors=visual.reusable_vectors([vis,*[r/'assets'/vis.name for r in a.cache_root]],registry,provider=provider,model=model,dimensions=dimensions)
    assert len(vectors)==len(registry['profiles']), 'Uncached visual profile text'
    wanted={key:pg.semantic_text_for_entry(entry,slot,kind=kind) for key,kind,entry,slot in semantic.iter_semantic_entries(data)}
    expected=semantic.base_payload(data,provider,model,dimensions);compatible={}
    for path in [sem,*[r/'assets'/sem.name for r in a.cache_root]]:
        payload=pg.load_semantic_index_payload(path)
        assert semantic.metadata_matches(payload,expected,require_dictionary_hash=False),'Incompatible vector recipe/model'
        for key,row in payload['entries'].items():
            if key in wanted and row.get('text')==wanted[key] and len(row.get('vector',[]))==dimensions:
                compatible[key]=row
        del payload;gc.collect()
    missing=sorted(set(wanted)-set(compatible));assert not missing,('Uncached semantic text',missing)
    with tempfile.TemporaryDirectory(prefix='electrical-offline-index-') as temp:
        checkpoint=Path(temp)/'current.partial.json';checkpoint.write_text(json.dumps({**expected,'entries':compatible},ensure_ascii=False,separators=(',',':')))
        del compatible;gc.collect()
        payload=semantic.build_resumable_index_payload(data,output=sem,checkpoint=checkpoint,provider=provider,model=model,dimensions=dimensions,batch_size=1,request_interval=0,retry_attempts=1,retry_initial_delay=0)
        with source_update(SKILL):
            visual.write_payload(vis,visual.build_visual_profile_index_payload(registry,vectors=vectors,provider=provider,model=model,dimensions=dimensions))
            semantic.write_sharded_payload(sem,payload,shard_count=16,keep_stale_generations=True)
    pg.validate_semantic_index_metadata(pg.load_semantic_index_payload(sem),data)
    pg.validate_visual_profile_index_metadata(pg.load_visual_profile_index_payload(vis),registry)
    pointer=SnapshotPublisher(SKILL).publish()
    report=dict(semantic_entries=len(wanted),visual_profiles=len(registry['profiles']),embedding_calls=0,provider=provider,model=model,dimensions=dimensions,old_shards_retained=True,cache_rule='identity, full positive text, text hash, provider, model, dimensions and recipe must match',runtime=pointer,semantic_manifest_sha256=hashlib.sha256(sem.read_bytes()).hexdigest(),visual_manifest_sha256=hashlib.sha256(vis.read_bytes()).hexdigest())
    (HERE/a.report_name).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
