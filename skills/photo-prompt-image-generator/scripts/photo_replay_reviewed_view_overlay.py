"""Replay reviewed search views and registered follow-ups into an isolated module.

The overlay records exact candidate hashes and reviewed view records.  This
does not infer new meanings, build embeddings, or activate a runtime.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path

import photo_candidate_corpus as corpus
import photo_candidate_retrieval_views as views

ROOT = Path(__file__).resolve().parents[3]
FOLLOWUPS = Path(__file__).with_name('photo_reviewed_view_replay_manifest.json')


def apply(module, records, overlay):
    if overlay.get('schema') != 'photo-reviewed-view-overlay/v1':
        raise ValueError('unsupported reviewed view overlay')
    result = copy.deepcopy(module)
    existing = {row['id']: row for row in result['views']}
    if len(existing) != len(result['views']):
        raise ValueError('duplicate existing view')
    actions = []
    seen = set()
    for item in overlay['items']:
        cid = item['candidate_id']
        if cid in seen or cid not in records or views.digest(records[cid]) != item['source_record_sha256']:
            raise ValueError('overlay candidate missing, duplicated or changed')
        seen.add(cid)
        for view in item['views']:
            if view['candidate_id'] != cid or view['source_record_sha256'] != item['source_record_sha256']:
                raise ValueError('overlay view source mismatch')
            previous = existing.get(view['id'])
            if previous is not None:
                if previous != view:
                    raise ValueError('existing view differs from overlay')
                actions.append({'id': view['id'], 'status': 'already_present'})
                continue
            result['views'].append(copy.deepcopy(view))
            existing[view['id']] = view
            actions.append({'id': view['id'], 'status': 'added'})
    views.validate(result, records, require_complete=False)
    return result, actions


def apply_registered(module, records, raw, expected_sha256, *, root=ROOT, manifest=FOLLOWUPS,
                     followups=True):
    """Apply the requested overlay and any registered later overlays, in order.

    A known overlay identifies a suffix of the reviewed sequence. Each input
    is independently checked before any output is written; changed candidates
    still require review rather than silently dropping an enrichment.
    """
    digest = hashlib.sha256(raw).hexdigest()
    if digest != expected_sha256:
        raise ValueError('overlay hash mismatch')
    inputs = [(digest, raw)]
    if followups:
        registry = json.loads(Path(manifest).read_bytes())
        if registry.get('schema') != 'photo-reviewed-view-replay-sequence/v1':
            raise ValueError('unsupported reviewed view replay sequence')
        entries = registry['overlays']
        hashes = [row['sha256'] for row in entries]
        if len(hashes) != len(set(hashes)):
            raise ValueError('duplicate overlay in replay sequence')
        if digest in hashes:
            base = Path(root).resolve()
            for entry in entries[hashes.index(digest) + 1:]:
                path = (base / entry['path']).resolve()
                if not path.is_relative_to(base):
                    raise ValueError('overlay path outside repository')
                content = path.read_bytes()
                if hashlib.sha256(content).hexdigest() != entry['sha256']:
                    raise ValueError('registered overlay hash mismatch: ' + entry['path'])
                inputs.append((entry['sha256'], content))
    result = module
    stages = []
    for overlay_sha256, content in inputs:
        result, actions = apply(result, records, json.loads(content))
        stages.append({'overlay_sha256': overlay_sha256, 'views': len(actions),
                       'added': sum(x['status'] == 'added' for x in actions),
                       'already_present': sum(x['status'] == 'already_present' for x in actions)})
    return result, stages


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--assets', type=Path, required=True)
    p.add_argument('--input', type=Path, required=True)
    p.add_argument('--overlay', type=Path, help='start at this reviewed overlay; defaults to the registered first')
    p.add_argument('--overlay-sha256', help='required when --overlay is specified')
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--no-followups', action='store_true',
                   help='replay only the requested overlay, for historical inspection')
    args = p.parse_args()
    if args.output.exists() or args.output.resolve() == args.input.resolve():
        raise ValueError('output must be a new file')
    if (args.overlay is None) != (args.overlay_sha256 is None):
        p.error('--overlay and --overlay-sha256 must be specified together')
    if args.overlay is None:
        registry = json.loads(FOLLOWUPS.read_bytes())
        if registry.get('schema') != 'photo-reviewed-view-replay-sequence/v1' or not registry.get('overlays'):
            raise ValueError('missing reviewed view replay sequence')
        first = registry['overlays'][0]
        path = (ROOT / first['path']).resolve()
        if not path.is_relative_to(ROOT):
            raise ValueError('overlay path outside repository')
        raw, expected_sha256 = path.read_bytes(), first['sha256']
    else:
        raw, expected_sha256 = args.overlay.read_bytes(), args.overlay_sha256
    records = corpus.load(args.assets)['candidates']
    result, stages = apply_registered(json.loads(args.input.read_bytes()), records, raw,
                                      expected_sha256, followups=not args.no_followups)
    legacy = None
    if not args.no_followups:
        registry = json.loads(FOLLOWUPS.read_bytes())
        if any(s['overlay_sha256'] == registry['overlays'][-1]['sha256'] for s in stages):
            # Source records keep their historical provenance. Verify it from
            # preserved evidence rather than opening the retired search release.
            import photo_archived_legacy_evidence
            legacy = photo_archived_legacy_evidence.verify(records)
    with args.output.open('x', encoding='utf-8') as output:
        output.write(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'views': sum(s['views'] for s in stages),
                      'added': sum(s['added'] for s in stages),
                      'already_present': sum(s['already_present'] for s in stages),
                      'stages': stages, 'legacy_evidence': legacy,
                      'runtime_activation': 'unchanged'}))


if __name__ == '__main__':
    main()
