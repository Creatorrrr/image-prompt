"""Read-only lexical audit of manifest source; this is not retrieval evaluation."""
import collections
import hashlib
import json
import pathlib
import re
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
PATTERNS = {
    'genre': r'romantic comedy|romcom|rom-com|screwball|러브코미디|로맨틱 코미디',
    'narrative': r'fake dating|slow burn|friends.to.lovers|enemies.to.lovers|가짜 연애|슬로번|비밀연애',
    'hands': r'interlaced fingers|holding hands|sleeve tug|linking arms|깍지|소매를 잡|팔짱',
    'support': r'bridal carry|piggyback|lap pillow|arm pillow|무릎베개|공주님 안기|업기|팔베개',
    'close_contact': r'kabedon|agokui|almost kiss|forehead|벽쿵|턱 아래|키스 전',
    'shared_objects': r'sharing.*umbrella|shared umbrella|aiaigasa|sharing.*earbud|우산.*함께|같은.*컵',
    'comedy': r'pratfall|spit.take|double.take|harisen|hammerspace|tsukkomi|슬랩스틱|하리센|츳코미',
    'garments': r'cold.shoulder|sweetheart|moe.sleeve|borrowed shirt|garter belt|bustier|babydoll|모에소매|콜드숄더|뷔스티에|가터벨트',
    'context_boundary': r'non.consensual|infidelity|netorare|\bNTR\b|shipping|tsundere|yandere|동의|츤데레|얀데레',
}

def sha(b):
    return hashlib.sha256(b).hexdigest()

def main():
    target = HERE / 'corpus-snapshot.json'
    if target.exists():
        raise SystemExit('Preserve original snapshot; use a different run for a new baseline.')
    manifest_path = ASSETS / 'photo_candidate_corpus_manifest.json'
    manifest_raw = manifest_path.read_bytes()
    manifest = json.loads(manifest_raw)
    records, bindings, modules = {}, collections.defaultdict(list), []
    for mod in manifest['modules']:
        p = ASSETS / mod['file']
        raw = p.read_bytes()
        data = json.loads(raw)
        modules.append({**mod, 'sha256': sha(raw)})
        if mod['kind'] == 'candidates':
            for cid, record in data['candidates'].items():
                assert cid not in records
                records[cid] = (mod['file'], record)
        elif mod['kind'] == 'slot_bindings':
            for bid, binding in data['slot_bindings'].items():
                bindings[binding['candidate_id']].append(binding)
    matches, counts = [], collections.Counter()
    for cid, (module, record) in records.items():
        content = record.get('content', {})
        flat = ' '.join(str(content.get(k, '')) for k in ('en','ko','aliases','keywords','tags'))
        hit = [k for k, pattern in PATTERNS.items() if re.search(pattern, flat, re.I)]
        if hit:
            counts.update(hit)
            matches.append({'candidate_id': cid, 'module': module, 'groups': hit,
                            'record': record, 'bindings': bindings[cid]})
    tracked = subprocess.check_output(['git','status','--porcelain','-uno'],cwd=ROOT,text=True).splitlines()
    scripts = {}
    for filename in ('photo_candidate_corpus.py','build_shared_candidate_index.py','validate_photo_prompt_dictionary.py','photo_installed_h_f2.py'):
        p = ROOT / 'skills/photo-prompt-image-generator/scripts' / filename
        scripts[str(p.relative_to(ROOT))] = sha(p.read_bytes()) if p.exists() else None
    result = {'schema':'romcom-source-audit/v1','captured_date_kst':'2026-10-24',
              'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
              'scope':'Current working-tree manifest closure; lexical matches, not semantic retrieval or novelty proof.',
              'manifest_sha256':sha(manifest_raw),'modules':modules,'script_sha256':scripts,
              'candidate_count':len(records),'binding_count':sum(map(len,bindings.values())),
              'slot_count':len(json.loads((ASSETS/'photo_candidate_slot_catalog.json').read_bytes())['slot_catalog']),
              'tracked_status_counts':dict(collections.Counter(x[:2] for x in tracked)),
              'patterns':PATTERNS,'group_counts':dict(counts),'matches':matches}
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('head','candidate_count','binding_count','slot_count','group_counts')},ensure_ascii=False))
    for group in PATTERNS:
        samples = [m for m in matches if group in m['groups']]
        samples.sort(key=lambda m: ('harem' not in m['module'], len(m['record'].get('content',{}).get('en',''))))
        print(group, [(m['candidate_id'], m['record'].get('content',{}).get('en','')[:155]) for m in samples[:7]])

if __name__ == '__main__':
    main()
