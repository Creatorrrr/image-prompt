"""Finish this task's source revision after a concurrent-source drift rejection."""
from pathlib import Path
import gc, json, sys
gc.disable()
O = Path(__file__).resolve().parent
S = O.parents[4] / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(S / 'scripts'))
import build_shared_candidate_index as builder
from photo_runtime_sources import SnapshotPublisher, complete_source_update

def main():
    # The preceding writer acquired this token, rejected changed source before
    # activating its layout, and exited. No replacement writer is admitted by
    # source_update while this token remains pending.
    pointer = SnapshotPublisher(S).directory / 'SOURCE.json'
    revision = json.loads(pointer.read_bytes())
    assert revision.get('editing'), 'No pending source revision to repair'
    (O / 'root-index-repair-start.json').write_text(json.dumps({
        'source_revision_path': str(pointer), 'revision': revision,
        'cause': 'source changed before layout activation; original CURRENT preserved'
    }, indent=2) + '\n')
    report = builder.build(S / 'assets', O / 'root-index-cache')
    assert json.loads(pointer.read_bytes()) == revision, 'Source ownership changed'
    complete_source_update(S, token=revision['editing'])
    (O / 'root-index-repair-result.json').write_text(json.dumps({
        'status': 'pass', 'build': report,
        'completed_own_pending_revision': True, 'CURRENT_writes': 0
    }, indent=2) + '\n')
    print(json.dumps(report), flush=True)

if __name__ == '__main__':
    main()
