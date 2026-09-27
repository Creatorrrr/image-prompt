"""Resume the normal builder using its existing compact JSON writer for checkpoints.

Embedding inputs, batch size, source metadata, cache admission, and final index
construction are unchanged. Disposable checkpoints are compact and saved after
each sixteen single-text requests; the final index always includes every row.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skills/photo-prompt-image-generator/scripts"))
import build_semantic_index as builder

original_write = builder.write_payload
checkpoint_writes = 0


def compact_checkpoint(path, payload, *, compact=False):
    global checkpoint_writes
    is_checkpoint = Path(path).suffix == ".partial"
    if is_checkpoint:
        checkpoint_writes += 1
        if checkpoint_writes % 16:
            return
    return original_write(path, payload, compact=compact or is_checkpoint)


builder.write_payload = compact_checkpoint
raise SystemExit(builder.main())
