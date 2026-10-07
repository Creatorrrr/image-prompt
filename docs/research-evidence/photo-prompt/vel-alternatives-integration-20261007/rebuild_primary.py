#!/usr/bin/env python3
"""Use canonical builders on the combined primary, with exact compatible reuse."""
import os,sys,json,runpy
from pathlib import Path
WORK=Path(__file__).resolve().parents[4]
PRIMARY=Path('/Users/chasoik/Projects/image-prompt')
SKILL=PRIMARY/'skills/photo-prompt-image-generator'
OUT=SKILL/'data/runs/vel-alternatives-integration-20261007/primary_adoption'
for line in (PRIMARY/'.env').read_text().splitlines():
 if '=' not in line:continue
 k,v=line.split('=',1);k=k.strip()
 if k in {'GEMINI_API_KEY','GOOGLE_API_KEY'}:os.environ.setdefault(k,v.strip().strip('"\''))
sys.path.insert(0,str(SKILL/'scripts'))
import prompt_generator as pg
import build_semantic_index as sem
from prompt_generator import load_semantic_index_payload

data=pg.load_json(SKILL/'assets/photo_prompt_tags.json')
expected=sem.base_payload(data,pg.SEMANTIC_PROVIDER,pg.SEMANTIC_MODEL_ID,pg.DEFAULT_SEMANTIC_DIMENSIONS)
texts={k:pg.semantic_text_for_entry(e,s,kind=kind) for k,kind,e,s in pg.iter_semantic_entries(data)}
entries={}
for path in [SKILL/'assets/photo_prompt_semantic_index.json',WORK/'skills/photo-prompt-image-generator/assets/photo_prompt_semantic_index.json']:
 payload=load_semantic_index_payload(path)
 if not sem.metadata_matches(payload,expected):continue
 for k,row in payload['entries'].items():
  if k in texts and row.get('text')==texts[k] and isinstance(row.get('vector'),list) and len(row['vector'])==pg.DEFAULT_SEMANTIC_DIMENSIONS:entries[k]=row
checkpoint=OUT/'compatible_semantic_cache.partial'
sem.write_payload(checkpoint,{**expected,'entries':entries},compact=True)
print(json.dumps({'primary_semantic_entries':len(texts),'exact_compatible_vectors_reused':len(entries),'pending_embeddings':len(texts)-len(entries)}),flush=True)
sys.argv=['build_semantic_index.py','--checkpoint',str(checkpoint),'--batch-size','1','--progress','--keep-stale-generations','--no-runtime-publication']
try:runpy.run_path(str(SKILL/'scripts/build_semantic_index.py'),run_name='__main__')
except SystemExit as e:
 if e.code:raise
sys.argv=['build_visual_profile_index.py','--cache-index',str(WORK/'skills/photo-prompt-image-generator/assets/photo_prompt_visual_profile_index.json'),'--batch-size','1','--no-runtime-publication']
try:runpy.run_path(str(SKILL/'scripts/build_visual_profile_index.py'),run_name='__main__')
except SystemExit as e:
 if e.code:raise
