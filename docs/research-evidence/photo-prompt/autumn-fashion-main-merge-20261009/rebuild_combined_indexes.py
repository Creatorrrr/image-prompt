"""Rebuild the merged authored corpus using exact-text vectors from both sides."""
from pathlib import Path
import gc,json,runpy,sys
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
SCRIPTS=ROOT/'skills/photo-prompt-image-generator/scripts'
CACHE=Path('/Users/chasoik/.cache/image-prompt/autumn-fashion-main-merge-20261009/vector-cache')
sys.path.insert(0,str(SCRIPTS))
import prompt_generator as pg
import build_semantic_index as bs

def reject_embedding(*args,**kwargs):raise RuntimeError('Unexpected new embedding text in scoped main merge; inspect cache miss before API use.')
def dump(p,j):p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')

def main():
    kind=sys.argv[1];real_embedding=pg.embed_texts_with_gemini;pg.embed_texts_with_gemini=reject_embedding
    if kind=='candidate':
        data=pg.load_json(ROOT/'skills/photo-prompt-image-generator/assets/photo_prompt_tags.json')
        expected=bs.base_payload(data,pg.SEMANTIC_PROVIDER,pg.SEMANTIC_MODEL_ID,pg.DEFAULT_SEMANTIC_DIMENSIONS)
        pools=[]
        for label in ['pulled_main','local_autumn','current_primary']:
            payload=pg.load_semantic_index_payload(CACHE/label/'photo_prompt_semantic_index.json')
            for field in ['provider','embedding_model','embedding_dimensions','semantic_text_recipe']:assert payload[field]==expected[field],(label,field)
            pools.append((label,payload['entries']))
        merged_cache=CACHE/'merged-text-vectors.json'
        extra_payload=json.loads(merged_cache.read_text()) if merged_cache.exists() else {}
        space_fields=['provider','embedding_model','embedding_dimensions','semantic_text_recipe']
        if extra_payload:
            for field in space_fields:assert extra_payload[field]==expected[field],('merged_text_cache',field)
        extra=extra_payload.get('entries',{})
        chosen={};counts={label:0 for label in ['pulled_main','local_autumn','current_primary','merged_text_cache','new_merged_text']};missing=[]
        for key,entry_kind,entry,slot in pg.iter_semantic_entries(data):
            text=pg.semantic_text_for_entry(entry,slot,kind=entry_kind)
            matches=[(label,rows[key]) for label,rows in pools if key in rows and rows[key]['text']==text]
            if key in extra and extra[key]['text']==text:matches.append(('merged_text_cache',extra[key]))
            if not matches:missing.append((key,entry_kind,entry,slot,text));continue
            label,row=matches[-1];assert len(row['vector'])==expected['embedding_dimensions'];chosen[key]=row;counts[label]+=1
        allowed={'slot:garment_detail:fit_ff09_v1_candidate','slot:garment_detail:fit_ff52_v1_candidate','slot:garment_detail:fit_ff52_v2_candidate'}
        assert {row[0] for row in missing} <= allowed,('Unexpected merged text', [row[0] for row in missing])
        for key,entry_kind,entry,slot,text in missing:
            vectors=real_embedding([text],model=expected['embedding_model'],dimensions=expected['embedding_dimensions'],retry_attempts=0)
            assert len(vectors)==1 and len(vectors[0])==expected['embedding_dimensions']
            row={'kind':entry_kind,'slot':slot,'id':entry['id'],'text':text,'vector':vectors[0]}
            chosen[key]=row;extra[key]=row;counts['new_merged_text']+=1;dump(merged_cache,{**{k:expected[k] for k in space_fields},'entries':extra})
            print('embedded newly combined text:',key,flush=True)
        checkpoint=CACHE/'combined-semantic.partial';dump(checkpoint,dict(expected,entries=chosen));dump(HERE/'CANDIDATE-VECTOR-REUSE.json',{'counts':counts,'total':len(chosen),'missing':[],'identical_text_and_vector_space_required':True,'new_embedding_requests':len(missing),'newly_combined_text_keys':[row[0] for row in missing],'batch_size':1})
        del pools,chosen,data;gc.collect()
        name='build_semantic_index.py';sys.argv=[str(SCRIPTS/name),'--checkpoint',str(checkpoint),'--keep-stale-generations','--progress','--no-runtime-publication']
    else:
        name='build_visual_profile_index.py';sys.argv=[str(SCRIPTS/name),'--cache-index',str(CACHE/'pulled_main/photo_prompt_visual_profile_index.json'),'--cache-index',str(CACHE/'local_autumn/photo_prompt_visual_profile_index.json'),'--cache-index',str(CACHE/'current_primary/photo_prompt_visual_profile_index.json'),'--batch-size','1','--no-runtime-publication']
    runpy.run_path(str(SCRIPTS/name),run_name='__main__')
if __name__=='__main__':main()
