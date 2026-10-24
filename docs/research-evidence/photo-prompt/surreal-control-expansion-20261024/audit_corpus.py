#!/usr/bin/env python3
"""Read-only corpus audit; outputs are confined to this research directory.

Lexical screening is a reproducible lead generator, not production H-F2 search,
native qualification, perceptual measurement, or full semantic deduplication.
"""
import collections
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
ASSETS = SKILL / 'assets'


def read(p):
    return json.loads(p.read_text())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def dump(p, value):
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def tokens(text):
    out = []
    for word in re.findall(r'[a-z]+|[가-힣]+', text.lower()):
        if re.fullmatch('[가-힣]+', word):
            out.extend(word[i:i+2] for i in range(max(1, len(word)-1)))
        elif word not in {'a','an','the','of','in','on','at','and','to','with','is','are','its','one'}:
            out.append(word)
    return out


def main():
    manifest_path = ASSETS / 'photo_candidate_corpus_manifest.json'
    manifest = read(manifest_path)
    records, bindings, owners, members = {}, {}, {}, []
    for row in manifest['modules']:
        path = ASSETS / row['file']
        data = read(path)
        members.append({'file':row['file'], 'kind':row['kind'], 'sha256':sha(path)})
        if row['kind'] == 'candidates':
            for cid, candidate in data['candidates'].items():
                assert cid not in records, ('multiple payload owners', cid)
                records[cid] = candidate
                owners[cid] = row['file']
        elif row['kind'] == 'slot_bindings':
            bindings.update(data['slot_bindings'])
    slots = collections.defaultdict(list)
    for bid, binding in bindings.items():
        slots[binding['slot_id']].append(binding['candidate_id'])
    named = ['surreal_concept', 'surreal_physics_detail', 'reality_anchor',
             'reflection_logic', 'shadow_relation', 'scale_relation',
             'transformation_stage', 'object_structure', 'surface_material']
    state = {
        'date_kst':'2026-10-24', 'git_head':subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT,text=True).strip(),
        'manifest_sha256':sha(manifest_path), 'runtime_config':read(SKILL/'retrieval-runtime.json'),
        'source_candidate_count':len(records), 'source_binding_count':len(bindings),
        'record_kind_counts':dict(collections.Counter(c['record_kind'] for c in records.values())),
        'module_count':len(members), 'modules':members,
        'slots':{s:{'binding_count':len(slots[s]), 'unique_candidates':len(set(slots[s])),
                    'candidate_ids':sorted(set(slots[s]))} for s in named},
        'limits':['role tags are neither semantic truth nor native qualification',
                  'root en/ko/phrase fields screening excludes profile internals and nested branches',
                  'no production ranking, embeddings, image calls or runtime/source mutations'],
    }
    selected_modules = ['photo_candidate_surreal_posthuman_science_fantasy_20261022.json',
                        'photo_candidate_liminal_dreamcore_20261022.json',
                        'photo_candidate_liminal_dreamcore_realizations_20261022.json']
    selected_ids = {cid for cid in records if owners[cid] in selected_modules}
    dump(HERE/'evidence/corpus-state.json',state)
    dump(HERE/'evidence/related-source-snapshots.json',
         {'modules':selected_modules, 'records':{cid:records[cid] for cid in sorted(selected_ids)}})
    visual = {cid:c for cid,c in records.items() if c['record_kind']!='diagnostic'}
    texts = {cid:' '.join(c.get('content',{}).get(k,'') for k in ('en','ko','phrase_en','phrase_ko')
                         if isinstance(c.get('content',{}).get(k),str)) for cid,c in visual.items()}
    texts = {cid:text for cid,text in texts.items() if text.strip()}
    bags = {cid:collections.Counter(tokens(text)) for cid,text in texts.items()}
    df = collections.Counter(term for bag in bags.values() for term in bag)
    n=len(bags); avg=sum(sum(b.values()) for b in bags.values())/n
    queries = {c['id']:c['scene']['en']+' '+c['principle_ko'] for c in read(HERE/'input/pro-candidate-draft.json')['candidates']}
    queries.update({
      'reflection_state':'mirror reflection same object branch blossoms flower bare accurate reflected cup 거울 반사 가지 꽃',
      'material_compliance':'stone granite pillow soft dent folds cheek 돌 베개 부드러운 눌림',
      'care_object':'cradle empty wooden chair lap caring holding 빈 의자 무릎 돌봄',
      'functional_inversion':'cup handle attached inside wall loop finger 찻잔 안쪽 손잡이',
      'indoor_weather':'single cloud inside room table ceiling detached 실내 구름 식탁',
      'environment_paradox':'bright daylight sky night dark street continuous 낮 하늘 밤 거리',
      'detached_marking':'paint stripe road cloth folded continuous 흰 줄 도로 접힘',
      'weak_support':'blade grass pebble rests tip weight bends 풀잎 조약돌 지지',
      'domestic_scale':'giant cup adult normal kitchen cleaning large handle 거대 찻잔 부엌',
      'local_gravity':'wall floor chair reading person orientation gravity 벽 바닥 독서 중력',
      'shadow_owner':'shadow attached owner distinct silhouette lit object 그림자 소유자 불일치',
      'negative_volume':'solid empty space cast room vessel negative mold 빈 공간 고형 주형',
      'image_threshold':'painted photograph plane frame boundary real object emerges 그림 사진 경계 사물',
      'fabric_architecture':'sheer fabric doorway room seams transparent architecture 천 건축 문틀',
      'local_season':'single tree snow summer environment weather 계절 눈 여름 경계',
      'container_world':'small landscape horizon inside vessel cup drawer container 용기 풍경 내포',
      'topology':'continuous path ribbon returns impossible connections local perspective 위상 연결 경로',
      'light_exception':'light source lamp dark patch shadow illuminated mismatched 빛 어둠 조명 불일치',
      'recursion':'room model same window interior nested repeated 모형 실제 방 재귀',
      'symbolic_analogy':'tool seed leaf comb roots formal analogy visual poetry 사물 기능 유추',
    })
    proposals=HERE/'candidate-proposals.json'
    if proposals.exists():
        queries.update({c['research_id']:c['proposal_en'] for c in read(proposals)['cards']
                        if c['origin']=='new_research_authored'})
    results={}; shortlisted=set(selected_ids)
    for qid,query in queries.items():
        qt=set(tokens(query)); scored=[]
        for cid,bag in bags.items():
            dl=sum(bag.values());score=0
            for t in qt:
                f=bag.get(t,0)
                if f:
                    idf=math.log(1+(n-df[t]+.5)/(df[t]+.5))
                    score+=idf*f*2.2/(f+1.2*(.25+.75*dl/avg))
            if score:scored.append((score,cid))
        hits=[]
        for score,cid in sorted(scored,reverse=True)[:12]:
            c=records[cid];shortlisted.add(cid)
            hits.append({'candidate_id':cid,'module':owners[cid],'score':round(score,5),
                         'record_kind':c['record_kind'],'primary_text':texts[cid],
                         'conditions':c['conditions'],'effects':c['effects']})
        results[qid]={'query':query,'hits':hits}
    dump(HERE/'evidence/lexical-neighbors.json',{'method':'root-primary BM25 with English words and Hangul bigrams; discovery only',
         'screened_candidate_count':len(bags),'total_positive_candidates':len(visual),'queries':results})
    dump(HERE/'evidence/review-source-snapshots.json',{'records':{cid:records[cid] for cid in sorted(shortlisted)}})
    digest_rows={cid:hashlib.sha256(json.dumps(c,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest() for cid,c in records.items()}
    dump(HERE/'evidence/source-record-digests.json',digest_rows)
    print(json.dumps({'candidates':len(records),'positive':len(visual),'diagnostic':len(records)-len(visual),
                      'root_primary_screened':len(bags),'related_records':len(selected_ids),
                      'shortlisted_unique_records':len(shortlisted),'queries':len(queries)},ensure_ascii=False))


if __name__=='__main__':
    main()
