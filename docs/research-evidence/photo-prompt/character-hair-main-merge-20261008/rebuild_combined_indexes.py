"""Rebuild the merged authored corpus using exact-text vectors from both sides."""
from pathlib import Path
import gc,json,runpy,sys
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
SCRIPTS=ROOT/'skills/photo-prompt-image-generator/scripts'
CACHE=Path('/Users/chasoik/.cache/image-prompt/character-hair-main-merge-20261008/vector-cache')
sys.path.insert(0,str(SCRIPTS))
import prompt_generator as pg
import build_semantic_index as bs

def reject_embedding(*args,**kwargs):raise RuntimeError('Unexpected new embedding text in scoped main merge; inspect cache miss before API use.')
def dump(p,j):p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')

def main():
    kind=sys.argv[1];pg.embed_texts_with_gemini=reject_embedding
    if kind=='candidate':
        data=pg.load_json(ROOT/'skills/photo-prompt-image-generator/assets/photo_prompt_tags.json')
        expected=bs.base_payload(data,pg.SEMANTIC_PROVIDER,pg.SEMANTIC_MODEL_ID,pg.DEFAULT_SEMANTIC_DIMENSIONS)
        pools=[]
        for label in ['pulled_main','local_hair']:
            payload=pg.load_semantic_index_payload(CACHE/label/'photo_prompt_semantic_index.json')
            for field in ['provider','embedding_model','embedding_dimensions','semantic_text_recipe']:assert payload[field]==expected[field],(label,field)
            pools.append((label,payload['entries']))
        chosen={};counts={'pulled_main':0,'local_hair':0};missing=[]
        for key,entry_kind,entry,slot in pg.iter_semantic_entries(data):
            text=pg.semantic_text_for_entry(entry,slot,kind=entry_kind)
            matches=[(label,rows[key]) for label,rows in pools if key in rows and rows[key]['text']==text]
            if not matches:missing.append(key);continue
            label,row=matches[-1];assert len(row['vector'])==expected['embedding_dimensions'];chosen[key]=row;counts[label]+=1
        assert not missing,('Unmatched semantic text',missing)
        checkpoint=CACHE/'combined-semantic.partial';dump(checkpoint,dict(expected,entries=chosen));dump(HERE/'CANDIDATE-VECTOR-REUSE.json',{'counts':counts,'total':len(chosen),'missing':missing,'identical_text_and_vector_space_required':True,'new_embedding_requests':0})
        del pools,chosen,data;gc.collect()
        name='build_semantic_index.py';sys.argv=[str(SCRIPTS/name),'--checkpoint',str(checkpoint),'--keep-stale-generations','--progress','--no-runtime-publication']
    else:
        name='build_visual_profile_index.py';sys.argv=[str(SCRIPTS/name),'--cache-index',str(CACHE/'pulled_main/photo_prompt_visual_profile_index.json'),'--cache-index',str(CACHE/'local_hair/photo_prompt_visual_profile_index.json'),'--batch-size','1','--no-runtime-publication']
    runpy.run_path(str(SCRIPTS/name),run_name='__main__')
if __name__=='__main__':main()
