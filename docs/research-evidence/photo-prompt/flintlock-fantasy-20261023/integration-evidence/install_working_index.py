"""Install only an already fully verified, source-identical local index closure."""
from pathlib import Path
import datetime, hashlib, json, shutil, sys

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'skills/photo-prompt-image-generator/scripts'))
import photo_candidate_corpus as corpus

ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
STAGE = OUT / 'working-index-current/assets'
REPORT = OUT / 'working-index-cache/BUILD-REPORT.json'
MANIFEST = 'photo_candidate_search.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    report = json.loads(REPORT.read_bytes())
    staged = json.loads((STAGE / MANIFEST).read_bytes())
    assert report['verification']['verified']
    assert report['layout_id'] == staged['layout_id']
    source_digest = corpus.digest(corpus.load(ASSETS))
    assert source_digest == corpus.digest(corpus.load(STAGE)), 'Working source advanced; do not install mismatched index'
    assert staged['corpus_sha256'] == source_digest
    previous_hash = sha(ASSETS / MANIFEST)
    closure = Path('photo_candidate_search_shards') / staged['layout_id']
    src, dst = STAGE / closure, ASSETS / closure
    hashes = {str(p.relative_to(src)): sha(p) for p in src.rglob('*') if p.is_file()}
    if dst.exists():
        assert {str(p.relative_to(dst)): sha(p) for p in dst.rglob('*') if p.is_file()} == hashes
    else:
        shutil.copytree(src, dst)
    assert {str(p.relative_to(dst)): sha(p) for p in dst.rglob('*') if p.is_file()} == hashes
    assert corpus.digest(corpus.load(ASSETS)) == source_digest, 'Working source advanced during copy'
    assert sha(ASSETS / MANIFEST) == previous_hash, 'Concurrent index writer advanced pointer'
    temporary = ASSETS / 'photo_candidate_search.flintlock-install.tmp'
    temporary.write_bytes((STAGE / MANIFEST).read_bytes())
    temporary.replace(ASSETS / MANIFEST)
    result = {'status': 'pass', 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'layout_id': staged['layout_id'], 'corpus_sha256': source_digest,
              'files_copied_and_byte_verified': len(hashes), 'previous_manifest_sha256': previous_hash,
              'installed_manifest_sha256': sha(ASSETS / MANIFEST), 'complete_build_report': report,
              'retained_old_shards': True, 'runtime_default_activation': False}
    (OUT / 'working-index-install.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'complete_build_report'}))


if __name__ == '__main__':
    main()
