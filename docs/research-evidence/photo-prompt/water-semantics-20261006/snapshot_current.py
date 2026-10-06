"""Read-only current authored-source audit; writes only this research directory."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
ASSETS = SKILL / 'assets'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def current_snapshot():
    paths = list(ASSETS.glob('*.json')) + list((SKILL / 'scripts').glob('*.py'))
    paths += [SKILL / 'SKILL.md', SKILL / 'references/maintenance.md']
    return {
        'schema': 'water-research-checkout-snapshot/v1',
        'date_kst': '2026-10-06',
        'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'dirty_status': subprocess.check_output(['git', 'status', '--porcelain=v1', '-uall'], cwd=ROOT, text=True).splitlines(),
        'files': {str(p.relative_to(ROOT)): digest(p) for p in sorted(paths)},
        'boundary': 'Top-level live asset JSON, Python scripts and two instructions only. Not a full backup of shards, images, fixtures or unrelated files.'
    }

def audit():
    if not (OUT / 'CHECKOUT-SNAPSHOT.json').exists():
        save('CHECKOUT-SNAPSHOT.json', current_snapshot())
    manifest = json.loads((ASSETS / 'photo_prompt_source_manifest.json').read_text())
    files = ['photo_prompt_tags.json', 'photo_prompt_visual_obligations.json'] + [x['file'] for x in manifest['sources']]
    records, all_ids, source_hashes = [], [], {}
    english = r'(?<![a-z])(?:water|wet|caustic|snell|meniscus|backscatter|pancake|biofluorescen|halocline|haenyeo|foam|splash|bubble|rippl|submer|hydro|salin|brine|marine|coast|tidal|river|lake|ocean|undersea|underwater|freshwater|saltwater|aquatic|seaweed|seagrass|kelp|coral|jellyfish|estuary|mangrove|shipwreck|scuba|snorkel|wetsuit|drysuit|aquaph)[a-z]*'
    relevant = re.compile(english + r'|테왁|물방울|수중|수면|해안|젖|윤슬|빙하|빙산|해녀|침수|이안류|폭포', re.I)
    def record(file, kind, slot, pointer, value):
        if not isinstance(value, dict) or not value.get('id'): return
        all_ids.append({'file': file, 'kind': kind, 'slot': slot, 'id': value['id']})
        text = json.dumps(value, ensure_ascii=False)
        if relevant.search(text):
            records.append({'file': file, 'kind': kind, 'slot': slot, 'json_pointer': pointer, 'id': value['id'], 'record': value, 'classification': 'LEXICALLY_RELATED_NOT_EQUIVALENCE_PROOF'})
    for file in dict.fromkeys(files):
        raw = (ASSETS / file).read_bytes()
        source_hashes[file] = hashlib.sha256(raw).hexdigest()
        d = json.loads(raw.decode('utf-8'))
        for slot, entries in d.get('slots', {}).items():
            for i, entry in enumerate(entries): record(file, 'candidate', slot, f'/slots/{slot}/{i}', entry)
        profiles = d.get('profiles', [])
        if isinstance(profiles, dict):
            for key, profile in profiles.items(): record(file, 'visual_profile', None, '/profiles/'+key, profile)
        else:
            for i, profile in enumerate(profiles): record(file, 'visual_profile', None, f'/profiles/{i}', profile)
    drift_during_read=[name for name,h in source_hashes.items() if digest(ASSETS/name)!=h]
    save('EXISTING-DATA-CATALOG.json', {'schema':'water-existing-data-catalog/v1','source_manifest':manifest,'audited_file_count':len(set(files)),'all_record_count':len(all_ids),'related_records':records,'all_ids':all_ids,'source_hashes':source_hashes,'files_changed_during_read':drift_during_read,'limits':'Authored-record lexical scan only; no live retrieval, exposure, adoption or pixel quality measured. Catalog binds each source to the exact bytes read; the shared checkout can advance later.'})
    queries = ['caustic','snell','meniscus','backscatter','marine snow','wet_hair','wet_fabric','waterline','rip current','crown splash','pancake','biofluorescence','seaweed','wetsuit','haenyeo','테왁','윤슬','halocline']
    hits = {q: [{'file':r['file'],'slot':r['slot'],'id':r['id']} for r in records if q.lower() in json.dumps(r['record'],ensure_ascii=False).lower()] for q in queries}
    save('LEXICAL-GAP-AUDIT.json', {'method':'Casefold substring scan of authored records, not semantic retrieval. Zero is a research lead, not proven capability absence.','queries':hits})
    print(json.dumps({'audited_files':len(set(files)),'all_records':len(all_ids),'related_records':len(records),'hits':{k:v[:10] for k,v in hits.items()}},ensure_ascii=False,indent=2))

def verify():
    baseline=json.loads((OUT/'CHECKOUT-SNAPSHOT.json').read_text())
    now=current_snapshot()
    changed=[p for p,h in baseline['files'].items() if now['files'].get(p)!=h]
    added=sorted(set(now['files'])-set(baseline['files']))
    prefix=str(OUT.relative_to(ROOT))+'/'
    before=set(x for x in baseline['dirty_status'] if prefix not in x)
    after=set(x for x in now['dirty_status'] if prefix not in x)
    result={'schema':'water-research-preservation/v1','baseline_head':baseline['head'],'current_head':now['head'],'changed_audited_files':changed,'added_live_files':added,'unrelated_status_added':sorted(after-before),'unrelated_status_removed':sorted(before-after),'audited_file_count':len(baseline['files']),'audited_live_inputs_unchanged':not changed and not added and baseline['head']==now['head'],'author_scope':'This research wrote authored outputs only under water-semantics-20261006. Shared live source changes are observed drift and must not be reset or attributed to this research by the hash comparison.','scope':'Hash check covers the enumerated live inputs only; Git status checks path states, not full historical/untracked content. It cannot prove an unchanged shared checkout or identify who changed a file.'}
    save('PRESERVATION-CHECK.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in {'unrelated_status_added','unrelated_status_removed'}},ensure_ascii=False,indent=2))

if __name__=='__main__':
    import sys
    verify() if '--verify' in sys.argv else audit()
