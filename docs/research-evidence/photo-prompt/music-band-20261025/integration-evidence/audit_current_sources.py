"""Verify the scoped source delta and record concurrent changes without editing them."""
from pathlib import Path
import hashlib, json, sys
O = Path(__file__).resolve().parent
ROOT = O.parents[4]
S = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(S / 'scripts'))
import photo_candidate_corpus as c

def main():
    base = json.loads((O / 'integration-baseline.json').read_bytes())
    corpus = c.load(S / 'assets')
    checks = {
        'candidate_records_preserved': all(cid in corpus['candidates'] and
            c.digest(corpus['candidates'][cid]) == sha for cid, sha in base['candidate_sha256'].items()),
        'binding_records_preserved': all(key in corpus['slot_bindings'] and
            c.digest(corpus['slot_bindings'][key]) == sha for key, sha in base['binding_sha256'].items()),
        'slot_catalog_preserved': c.digest(corpus['slot_catalog']) == base['catalog_sha256'],
        'policies_preserved': c.digest(corpus['policies']) == base['policies_sha256']}
    allowed = {'skills/photo-prompt-image-generator/assets/photo_candidate_corpus_manifest.json',
        'skills/photo-prompt-image-generator/assets/photo_candidate_search.json',
        'skills/photo-prompt-image-generator/retrieval-runtime.json'}
    changes = [name for name, sha in base['protected'].items()
        if not (ROOT / name).exists() or hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != sha]
    checks['unrelated_authored_files_preserved'] = not (set(changes) - allowed)
    report = {'status': 'pass' if all(checks.values()) else 'fail', 'checks': checks,
        'old_candidate_count': len(base['candidate_sha256']),
        'old_binding_count': len(base['binding_sha256']),
        'current_candidate_count': len(corpus['candidates']),
        'current_binding_count': len(corpus['slot_bindings']),
        'current_source_sha256': c.digest(corpus), 'changed_protected_files': changes,
        'authorized_mutation_allowlist': sorted(allowed),
        'source_data_only_no_native_qualification': True}
    (O / 'source-preservation.final.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)
    assert all(checks.values())

if __name__ == '__main__':
    main()
