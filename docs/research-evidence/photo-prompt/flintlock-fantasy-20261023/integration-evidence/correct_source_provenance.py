"""Apply the F02 erratum without changing visible literals or historical runs."""
from pathlib import Path
import copy, hashlib, json

O=Path(__file__).resolve().parent
R=O.parents[4]
A=R/'skills/photo-prompt-image-generator/assets'

def read(p): return json.loads(p.read_bytes())
def write(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')

def main():
    errata=read(O/'source-correction-F02.json')
    sources=errata['replacement_sources']
    digest=hashlib.sha256((O/'source-correction-F02.json').read_bytes()).hexdigest()
    path=A/'photo_candidate_flintlock_fantasy_20261023.json'
    data=read(path)
    cid=next(k for k,v in data['candidates'].items() if v['content']['research_semantics']['card_id']=='F02')
    old=copy.deepcopy(data['candidates'][cid]);new=data['candidates'][cid]
    meta=new['content']['research_semantics']
    meta.update(source_ids=['S58','S59'],source_refs=sources,source_correction=errata,
                source_support_scope='Context supports powder magazines and barrels only; this exact raised-platform arrangement is authored, not an authenticated storage design.')
    new['provenance']=[{'source':'Authored generic storage literal; correction integration-evidence/source-correction-F02.json; bounded context '+s['url']+'; digest is correction record, not webpage bytes','sha256':digest} for s in sources]
    assert all(old[k]==new[k] for k in ['id','record_kind','conditions','effects'])
    assert all(old['content'][k]==new['content'][k] for k in ['en','ko','definition','aliases'])
    write(path,data);write(O/'corrected-native-records.json',data['candidates'])
    path=A/'photo_flintlock_fantasy_semantics_20261023.json';sidecar=read(path)
    for card in sidecar['cards']:
        if card['card_id']=='F02':
            card.update(source_ids=['S58','S59'],source_correction=errata,source_support_scope=meta['source_support_scope'])
    sidecar['source_refs']=[s for s in sidecar['source_refs'] if s['source_id'] not in ['S58','S59']]+sources
    sidecar['source_corrections']=[errata];write(path,sidecar)
    print(json.dumps({'status':'pass','card':'F02','candidate_id':cid,'visible_literals_changed':False,'immutable_test_release_changed':False}))

if __name__=='__main__': main()
