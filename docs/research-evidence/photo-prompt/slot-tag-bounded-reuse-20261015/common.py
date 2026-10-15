"""Read-only inputs and non-overwriting evidence helpers for the bounded run."""
import hashlib
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
SKILL = ROOT / 'skills/photo-prompt-image-generator'
RESEARCH = HERE.parent / 'slot-tag-codex-direct-20261014'
PILOT = HERE.parent / 'slot-tag-pilot-20261013'
BASELINE = HERE.parent / 'slot-tag-bounded-reuse-plan-20261015/BASELINE.json'
sys.path[:0] = [str(SKILL / 'scripts'), str(RESEARCH)]
for key in ('GEMINI_API_KEY', 'GOOGLE_API_KEY', 'OPENAI_API_KEY', 'ANTHROPIC_API_KEY'):
    os.environ.pop(key, None)
os.environ['HF_HUB_OFFLINE'] = os.environ['TRANSFORMERS_OFFLINE'] = '1'
os.environ['PHOTO_EMBEDDING_BACKEND'] = 'embeddinggemma2-local'
import photo_candidate_corpus as c


def read(path):
    return json.loads(Path(path).read_text())


def save(name, value):
    path = HERE / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as handle:
        handle.write(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    return path


def artifact(path):
    path = Path(path)
    return {'file': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def source():
    value = c.load(SKILL / 'assets')
    assert c.digest(value) == read(BASELINE)['operating']['corpus_sha256']
    return value
