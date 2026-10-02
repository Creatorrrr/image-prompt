#!/usr/bin/env python3
"""Exact Korean active-use edit with current external maintenance binding. Dry-run by default; never calls an API."""
import argparse
import fcntl
import os
from cycle_common import E, R, W, g, A, git, guard_window, load_freeze, raw_proposal, require, sha, states_from_freeze


def run(apply):
    frozen = load_freeze()
    source = R / frozen['source_file']
    before = (E / 'baseline-raw-extension.json').read_bytes()
    after = raw_proposal(frozen)
    require(source.read_bytes() == before,'Source no longer equals frozen baseline')
    require(git('rev-parse','HEAD').decode().strip() == frozen['baseline_commit'],'HEAD changed before apply; review freeze')
    require(g.load_json(A / 'photo_prompt_tags.json') == states_from_freeze(frozen)['baseline'],'Complete current merged data differs from frozen baseline')
    if apply:
        guard_window(frozen)
        revision = frozen['maintenance_revision']
        record_path = R / revision['new_record_file']
        record_bytes = (E / revision['new_record_snapshot']).read_bytes()
        if record_path.exists():
            require(record_path.read_bytes() == record_bytes,'Versioned maintenance record conflicts')
        else:
            with record_path.open('xb') as handle:
                handle.write(record_bytes)
                handle.flush()
                os.fsync(handle.fileno())
            fd = os.open(record_path.parent,os.O_DIRECTORY)
            try:
                os.fsync(fd)
            finally:
                os.close(fd)
        require(record_path.read_bytes() == record_bytes,'New maintenance record verification failed')
        guard_window(frozen)
        temporary = source.with_name(source.name + '.liminal-use-ko.tmp')
        with temporary.open('wb') as handle:
            handle.write(after)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary,source)
        fd = os.open(source.parent,os.O_DIRECTORY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
        require(source.read_bytes() == after,'Source write verification failed')
    print(('APPLIED' if apply else 'DRY RUN') + ': one action Korean active-use clause and planned maintenance reference corrected; sha256=' + sha(after))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply',action='store_true')
    args = parser.parse_args()
    if args.apply:
        with (W / '.data-evaluation.lock').open('a') as lock:
            fcntl.flock(lock,fcntl.LOCK_EX | fcntl.LOCK_NB)
            run(True)
    else:
        run(False)


if __name__ == '__main__':
    main()
