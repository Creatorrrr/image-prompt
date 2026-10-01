#!/usr/bin/env python3
"""Minimal exact one-row source edit. Dry-run by default; never calls an API."""
import argparse
import os
from cycle_common import A, E, R, git, guard_window, load_freeze, raw_proposal, require, sha


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='Write the separately approved exact source proposal')
    args = parser.parse_args()
    frozen = load_freeze()
    source = R / frozen['source_file']
    before = (E / 'baseline-raw-extension.json').read_bytes()
    after = raw_proposal(frozen)
    require(source.read_bytes() == before, 'Source no longer equals frozen baseline; refuse to overwrite')
    require(git('rev-parse', 'HEAD').decode().strip() == frozen['baseline_commit'], 'HEAD changed before source apply; review/rebase freeze first')
    if args.apply:
        guard_window(frozen)
        # One write, exact replacement bytes; no other rows or index files touched.
        with source.open('wb') as handle:
            handle.write(after)
            handle.flush()
            os.fsync(handle.fileno())
        require(source.read_bytes() == after, 'Source write verification failed')
    print(('APPLIED' if args.apply else 'DRY RUN') + ': one action row; exact en/ko plus concept_units; sha256=' + sha(after))


if __name__ == '__main__':
    main()
