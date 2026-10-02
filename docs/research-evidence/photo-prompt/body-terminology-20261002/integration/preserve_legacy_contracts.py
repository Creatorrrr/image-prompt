"""Preserve legacy authored meanings; add equivalent context through its allowed overlay.

This is a recorded correction of the initial integration, not a golden update.
Historical test sources, expected values and acceptance records are untouched.
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[4]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
RECEIPT = OUT / 'LEGACY-CONTRACT-REPAIR.json'
if RECEIPT.exists():
    raise SystemExit('This recorded correction already ran.')

def historical(name):
    return subprocess.check_output(['git', 'show', 'HEAD:' + str((ASSETS / name).relative_to(ROOT))], cwd=ROOT)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def object_span(raw, ident):
    decoder = json.JSONDecoder()
    match = re.search(r'"id"\s*:\s*' + re.escape(json.dumps(ident)), raw)
    assert match
    start = raw.rfind('{', 0, match.start())
    obj, end = decoder.raw_decode(raw, start)
    assert obj['id'] == ident
    return start, end, obj

candidate_name = 'photo_prompt_portrait_fashion_exposure_extension.json'
candidate_before = (ASSETS / candidate_name).read_bytes()
candidate_old = historical(candidate_name)
before = json.loads(candidate_before)
original = json.loads(candidate_old)
overlay_path = ASSETS / 'photo_prompt_body_morphology_extension.json'
overlay = json.loads(overlay_path.read_text())
contexts = overlay.setdefault('existing_slot_context_extensions', {})
changed = []
for slot, rows in original['slots'].items():
    live = {row['id']: row for row in before['slots'][slot]}
    for row in rows:
        current = live[row['id']]
        if row == current:
            continue
        original_phrases = row.get('paraphrases', [])
        assert current['paraphrases'][:len(original_phrases)] == original_phrases
        phrases = current['paraphrases'][len(original_phrases):]
        assert phrases
        contexts.setdefault(slot, {})[row['id']] = {'paraphrases': phrases}
        changed.append(dict(slot=slot, id=row['id'], equivalent_paraphrases=phrases,
                            original=row, first_integration=current))
assert len(changed) == 4
overlay_path.write_text(json.dumps(overlay, ensure_ascii=False, indent=2) + '\n')
(ASSETS / candidate_name).write_bytes(candidate_old)

profile_name = 'photo_prompt_visual_obligations_portrait_fashion_exposure.json'
profile_before = (ASSETS / profile_name).read_bytes()
profile_old = historical(profile_name)
(ASSETS / profile_name).write_bytes(profile_old)

main_name = 'photo_prompt_visual_obligations.json'
main_before = (ASSETS / main_name).read_text()
main_old = historical(main_name).decode()
ident = 'inner_thigh_negative_space'
start, end, prior = object_span(main_before, ident)
old_start, old_end, legacy = object_span(main_old, ident)
assert prior != legacy
main_after = main_before[:start] + main_old[old_start:old_end] + main_before[end:]
json.loads(main_after)
(ASSETS / main_name).write_text(main_after)

# A build-only cache carries original vectors with the original text and space.
# The runtime index is rebuilt by the standard generator, never patched by hand.
old_index = json.loads(historical('photo_prompt_visual_profile_index.json'))
restored = [ident, 'pfe_cleavage', 'pfe_midriff', 'pfe_lateral_chest', 'pfe_lower_chest']
cache = {key: old_index[key] for key in ('schema_version', 'provider', 'embedding_model', 'embedding_dimensions')}
cache['entries'] = {key: old_index['entries'][key] for key in restored}
(OUT / 'legacy-vector-cache.json').write_text(json.dumps(cache, ensure_ascii=False, indent=2) + '\n')
receipt = dict(schema_version='body-morphology-legacy-contract-repair/v1',
    status='CORRECTED_SOURCE_REQUIRES_INDEX_REBUILD', golden_updates=0,
    historical_candidate_source_sha256=sha(candidate_old), first_candidate_source_sha256=sha(candidate_before),
    historical_profile_source_sha256=sha(profile_old), first_profile_source_sha256=sha(profile_before),
    restored_profiles=restored, candidate_context_overlays=changed,
    restored_inner_thigh_original=legacy, first_inner_thigh_integration=prior,
    boundary='Equivalent candidate paraphrases use the existing allowed overlay. Original bundle meanings, maintenance receipts and authored profile contracts remain exact.')
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({key:receipt[key] for key in ('status','golden_updates','restored_profiles','historical_candidate_source_sha256')}, ensure_ascii=False))
