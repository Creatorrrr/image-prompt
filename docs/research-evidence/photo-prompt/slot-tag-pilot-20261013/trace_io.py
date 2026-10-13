"""Reproducible compressed traces; JSON value hashes survive byte packing."""
import gzip
import json
from pathlib import Path


def read_trace(path):
    return json.loads(gzip.decompress(Path(path).read_bytes()))


def write_trace(path, value):
    body = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    Path(path).write_bytes(gzip.compress(body, mtime=0))
