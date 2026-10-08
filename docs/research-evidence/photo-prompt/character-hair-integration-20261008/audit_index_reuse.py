"""Compare frozen pre-application vectors with the new exact text corpus."""
import gc,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
sys.path.insert(0,str(ASSETS.parent/'scripts'))
import prompt_generator as pg

def main():
    reports={}
    for kind,filename,loader in [('candidate','photo_prompt_semantic_index.json',pg.load_semantic_index_payload),
                                 ('profile','photo_prompt_visual_profile_index.json',pg.load_visual_profile_index_payload)]:
        old=json.loads((HERE/'before'/filename).read_text())
        new=loader(ASSETS/filename)
        for field in ['provider','embedding_model','embedding_dimensions','semantic_text_recipe']:
            assert old[field]==new[field],('vector-space change',kind,field)
        old_rows={}
        for shard in old['shards']:
            path=ASSETS/shard['path'];assert hashlib.sha256(path.read_bytes()).hexdigest()==shard['sha256']
            entries=json.loads(path.read_text())['entries']
            old_rows.update(entries)
        unchanged=changed=added=0
        for key,row in new['entries'].items():
            previous=old_rows.get(key)
            if previous is None:added+=1
            elif previous['text']==row['text']:
                assert previous['vector']==row['vector'],('Identical text received a different vector',kind,key)
                unchanged+=1
            else:changed+=1
        reports[kind]={'total':len(new['entries']),'unchanged_text_identical_vector':unchanged,
                       'changed_text':changed,'new_text':added,'removed_ids':len(set(old_rows)-set(new['entries'])),
                       'provider':new['provider'],'model':new['embedding_model'],'dimensions':new['embedding_dimensions'],
                       'semantic_text_recipe':new['semantic_text_recipe']}
        del old_rows,new;gc.collect()
    (HERE/'INDEX-REUSE-AUDIT.json').write_text(json.dumps(reports,indent=2)+'\n')
    print(json.dumps(reports,indent=2))

if __name__=='__main__':main()
