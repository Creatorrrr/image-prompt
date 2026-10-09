"""Read authored sources and produce research evidence; no runtime publication."""
from pathlib import Path
import collections
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib
import json
import re
import subprocess
import sys
import unicodedata

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
ASSETS = SKILL / 'assets'
sys.path.insert(0, str(SKILL / 'scripts'))

def dump(name, value):
    (HERE/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')

def norm(s):
    s=unicodedata.normalize('NFKD',str(s)).casefold()
    s=''.join(x for x in s if not unicodedata.combining(x))
    return ' '.join(re.sub(r'[^\w]+',' ',s).split())

def snap(paths):
    return {str(p.relative_to(ROOT)):{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
            'bytes':p.stat().st_size,'mode':p.stat().st_mode & 0o777}
            for p in sorted(set(paths)) if p.is_file()}

def seeds():
    groups=[]; terms=[]
    for line in (HERE/'seed-terms.txt').read_text().splitlines():
        if not line or line.startswith('#'):continue
        if line.startswith('@'):
            key,title=line[1:].split('|',1)
            group={'id':key,'title':title,'term_ids':[]};groups.append(group)
        else:
            for raw in line.split(';'):
                ko,en=raw.split(' — ',1)
                variants=[ko,en]+re.split(r' / |·',ko)+en.split(' / ')
                if ' / ' in en and en.endswith(' neck'):variants.append(en.split(' / ')[0]+' neck')
                t={'id':f'WIN{len(terms)+1:03d}','group':group['id'],'source_term':raw,
                   'ko':ko,'en':en,'query_variants':list(dict.fromkeys(variants))}
                terms.append(t);group['term_ids'].append(t['id'])
    assert len(terms)==304,len(terms)
    assert len(groups)==18,len(groups)
    return groups,terms

def main():
    import prompt_generator as pg
    start=datetime.now(ZoneInfo('Asia/Seoul')).isoformat()
    manifest=json.loads((ASSETS/'photo_prompt_source_manifest.json').read_text())
    paths=[ASSETS/s['file'] for s in manifest['sources']]
    paths += [ASSETS/n for n in ['photo_prompt_source_manifest.json','photo_prompt_tags.json',
                               'photo_prompt_visual_obligations.json','photo_prompt_semantic_index.json',
                               'photo_prompt_visual_profile_index.json']]
    paths += list((SKILL/'scripts').glob('*.py'))
    before=snap(paths)
    status=subprocess.check_output(['git','status','--porcelain=v1','-z'],cwd=ROOT).decode().split('\0')
    status=[x for x in status if x and 'winter-fashion-20261009' not in x]
    dirty_paths=[ROOT/x[3:] for x in status if not x.startswith('??')]
    dirty=snap(dirty_paths)
    data=pg.load_json(ASSETS/'photo_prompt_tags.json')
    registry=pg.load_visual_obligation_registry(ASSETS/'photo_prompt_visual_obligations.json')
    candidates=[]
    for slot,entries in data['slots'].items():
        for e in entries:
            fields=pg.semantic_bm25f_fields_for_entry(e,slot)
            text=norm(' '.join(v for k,vs in fields.items() if k!='slot_context' for v in vs))
            candidates.append({'id':e['id'],'slot':slot,'ko':e.get('ko'),'en':e.get('en'),'text':text,
                               'concept_units':e.get('concept_units',[]),'relations':e.get('relations',[]),
                               'affected_properties':e.get('affected_properties',[])})
    profiles=[{'id':p['id'],'category':p.get('category'),'definition':p.get('semantics',{}).get('definition'),
               'text':norm(pg.positive_visual_profile_text(p)),'activation':p.get('activation'),
               'affected_properties':p.get('concept_candidate',{}).get('affected_properties',[])}
              for p in registry['profiles']]
    groups,terms=seeds()
    for t in terms:
        hits={}
        for kind,rows in [('candidates',candidates),('profiles',profiles)]:
            hits[kind]=[]
            for row in rows:
                matched=[v for v in t['query_variants'] if norm(v) and f' {norm(v)} ' in f" {row['text']} "]
                if matched:hits[kind].append({'id':row['id'],'slot':row.get('slot'),'matched':matched})
        t['positive_field_mentions']=hits
        t['coverage_claim']='lexical_mentions_only; not equivalence, retrieval, selection, or pixels'
    after=snap(paths)
    changed=[p for p in before if before[p]!=after.get(p)]
    dump('source-snapshot.json',{'started_at_kst':start,'completed_at_kst':datetime.now(ZoneInfo('Asia/Seoul')).isoformat(),
         'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
         'scope':'Working tree includes preexisting dirty data; read-only loaders, no source validation/publication.',
         'manifest_source_counts':dict(collections.Counter(s['kind'] for s in manifest['sources'])),
         'source_files':before,'changed_during_load':changed,'preexisting_git_status':status,
         'tracked_dirty_files':dirty,'compiled_counts':{'slots':len(data['slots']),'candidates':len(candidates),
         'semantic_documents':len(list(pg.iter_semantic_entries(data))),'profiles':len(profiles),
         'bundles':len(data.get('candidate_bundles',[]))},'runtime_dispatch_executed':False,
         'embedding_calls':0,'image_calls':0,'index_rebuild_executed':False})
    dump('term-inventory.json',{'origin':{'conversation_id':'6ac7dd5d-c74c-83ec-9d21-4b1ee66066c9',
         'title':'겨울 패션 용어 조사','read_thread_body_cap':20000,'full_official_dom_read':True,
         'vocabulary_sections':15,'vocabulary_tables':18,'vocabulary_rows':304,
         'body_region_index_rows':15,'combination_rows':10,'rendered_response_text_length':25053,
         'extraction':'First-column term labels; aliases within one row count once. Supplementary tables counted separately.'},
         'groups':groups,'terms':terms})
    selected={kind:{h['id'] for t in terms if len(t['positive_field_mentions'][kind])<=20
                    for h in t['positive_field_mentions'][kind]} for kind in ['candidates','profiles']}
    dump('current-positive-records.json',{kind:[{k:v for k,v in r.items() if k!='text'}
         for r in rows if r['id'] in selected[kind]] for kind,rows in [('candidates',candidates),('profiles',profiles)]})
    dump('current-record-ids.json',{'candidates':[r['id'] for r in candidates],
                                  'profiles':[r['id'] for r in profiles]})
    print(json.dumps({'counts':{'terms':len(terms),'candidates':len(candidates),'profiles':len(profiles)},
        'changed_during_load':changed,'terms_with_candidate_mentions':sum(bool(t['positive_field_mentions']['candidates']) for t in terms),
        'terms_with_profile_mentions':sum(bool(t['positive_field_mentions']['profiles']) for t in terms)},ensure_ascii=False))
    if changed:raise SystemExit('Source changed during load; snapshot needs a bounded refresh.')

if __name__=='__main__':main()
