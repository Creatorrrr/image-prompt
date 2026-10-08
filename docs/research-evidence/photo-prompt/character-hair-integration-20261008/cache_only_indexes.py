"""Rebuild maintained indexes while rejecting any new embedding request."""
from pathlib import Path
import runpy,sys
ROOT=Path(__file__).resolve().parents[4]
SCRIPTS=ROOT/'skills/photo-prompt-image-generator/scripts'
sys.path.insert(0,str(SCRIPTS))
import prompt_generator as pg

def reject_network_embedding(*args,**kwargs):
    raise RuntimeError('Metadata-only finalization must reuse every exact-text vector; embedding request refused.')

pg.embed_texts_with_gemini=reject_network_embedding
name={'candidate':'build_semantic_index.py','profile':'build_visual_profile_index.py'}[sys.argv[1]]
sys.argv=[str(SCRIPTS/name),'--no-runtime-publication']
if name=='build_semantic_index.py':sys.argv.append('--progress')
runpy.run_path(str(SCRIPTS/name),run_name='__main__')
