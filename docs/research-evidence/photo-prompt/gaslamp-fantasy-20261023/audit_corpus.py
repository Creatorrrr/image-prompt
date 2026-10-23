"""Read-only fixed-field corpus audit. Writes only this research directory.

Do not rerun over historical evidence after integration; copy this script to a
new phase directory first. Lexical hits are not retrieval or semantic proof.
"""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
QUERIES = {
    'gaslamp': r'gaslamp|gaslight|가스램프|가스라이트',
    'gas_infrastructure': r'gasworks|gas holder|gasholder|lamplighter|gas.lit|gas lamp|가스등|점등원',
    'crinoline': r'crinoline|크리놀린',
    'bustle': r'\bbustle\b|버슬',
    'corset': r'\bcorset\b|코르셋',
    'chatelaine': r'chatelaine|샤틀렌',
    'mourning_hair': r'mourning jewelry|mourning jewellery|hairwork|hair locket|애도 장신구',
    'hansom': r'\bhansom\b|핸섬 마차',
    'calling_dance_card': r'calling card|dance card|방문 명함|무도회.*카드',
    'conservatory': r'conservatory|유리 온실',
    'seance': r'séance|seance|강령회',
    'planchette': r'planchette|플랑셰트',
    'spirit_photography': r'spirit photograph|심령 사진|이중 노출|double exposure',
    'pepper_ghost': r'pepper.s ghost|페퍼.*고스트',
    'galvanism': r'galvani|갈바니',
    'phrenology': r'phrenolog|골상학',
    'apothecary': r'apothecary|약종상|약제사',
    'laudanum': r'laudanum|아편팅크',
    'gothic_revival': r'gothic revival|고딕 리바이벌',
    'art_nouveau': r'art nouveau|아르누보',
    'faerie_contract': r'faerie bargain|faustian|요정.*계약|파우스트',
    'ward_boundary': r'\bward\b|결계',
    'automaton': r'automaton|자동인형',
    'vampire': r'vampir|흡혈',
    'crypt': r'\bcrypt\b|지하 묘실',
    'workhouse': r'workhouse|구빈원',
    'adult_context': r'demimonde|courtesan|드미몽드|고급 성적 동반자',
}

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()

def main():
    assert not (HERE/'CORPUS-LEXICAL-AUDIT.json').exists(), 'Preserve the first audit snapshot; use a new phase folder.'
    manifest = json.loads((ASSETS/'photo_candidate_corpus_manifest.json').read_text())
    records, origins, bindings, module_hashes = {}, {}, {}, {}
    for item in manifest['modules']:
        path = ASSETS/item['file']
        raw = path.read_bytes()
        module_hashes[item['file']] = hashlib.sha256(raw).hexdigest()
        data = json.loads(raw)
        if item['kind'] == 'candidates':
            for cid,row in data['candidates'].items():
                assert cid not in records, cid
                records[cid],origins[cid] = row,item['file']
        elif item['kind'] == 'slot_bindings':
            bindings.update(data['slot_bindings'])
    fields = ['en','ko','label','definition','description','keywords','tags','aliases','embedding_text']
    texts = {cid:' '.join(json.dumps(row['content'].get(f,''),ensure_ascii=False) for f in fields) for cid,row in records.items()}
    results, snapshots = {}, {}
    for query,pattern in QUERIES.items():
        hits = [cid for cid,text in texts.items() if re.search(pattern,text,re.I)]
        # Short explicit label matches precede matches occurring only in tags or embedding text.
        hits.sort(key=lambda cid:(not bool(re.search(pattern,records[cid]['content'].get('en','')+' '+records[cid]['content'].get('ko',''),re.I)),len(texts[cid]),cid))
        results[query]={'pattern':pattern,'count':len(hits),'hits':[{'id':cid,'module':origins[cid],'en':records[cid]['content'].get('en'),'ko':records[cid]['content'].get('ko')} for cid in hits[:20]],'truncated_at':20 if len(hits)>20 else None}
        for cid in hits[:2]:
            snapshots[cid]={'module':origins[cid],'record':records[cid],'canonical_sha256':hashlib.sha256(canonical(records[cid])).hexdigest(),'bindings':{bid:b for bid,b in bindings.items() if b['candidate_id']==cid},'lexical_queries':[]}
        for cid in hits[:2]:
            snapshots[cid]['lexical_queries'].append(query)
    audit={'schema':'gaslamp-corpus-lexical-audit/v1','candidate_count':len(records),'binding_count':len(bindings),'fields':fields,'module_hashes':module_hashes,'results':results,'limits':['Source lexical inspection only; no retrieval/rank/index/native/pixel claim.','Zero hits do not prove semantic absence.','Only manifest-listed source modules inspected; installed runtime may differ.','Snapshots are first two deterministic lexical witnesses, not representative nearest semantic neighbours.']}
    (HERE/'CORPUS-LEXICAL-AUDIT.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
    (HERE/'existing-source-mapping.json').write_text(json.dumps({'schema':'gaslamp-existing-source-snapshot/v1','records':snapshots},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'candidate_count':len(records),'binding_count':len(bindings),'snapshot_count':len(snapshots),'queries':{q:{'count':v['count'],'first':v['hits'][:1]} for q,v in results.items()}},ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
