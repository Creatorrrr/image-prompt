"""Accumulate only missing exact-text vectors, then resume the official builder.

No runtime recipe, provider, model, dimensions or semantic ownership is changed.
The ordinary builder independently checks every cached text before publication.
"""
from pathlib import Path
import json
import sys
import hashlib

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "skills/photo-prompt-image-generator/scripts"))
import prompt_generator as pg
import build_semantic_index as builder


def main():
    builder.load_project_env()
    source = ROOT / "skills/photo-prompt-image-generator/assets/photo_prompt_tags.json"
    data = pg.load_json(source)
    prior = json.loads((HERE / "semantic-cache-preserved.json").read_text())
    expected = builder.base_payload(data, pg.SEMANTIC_PROVIDER, pg.SEMANTIC_MODEL_ID,
                                    pg.DEFAULT_SEMANTIC_DIMENSIONS)
    assert builder.metadata_matches(prior, expected)
    rows = pg.iter_semantic_entries(data)
    entries = prior["entries"]
    delta_path = HERE / "semantic-delta-checkpoint.json"
    delta = builder.base_payload(data, pg.SEMANTIC_PROVIDER, pg.SEMANTIC_MODEL_ID,
                                 pg.DEFAULT_SEMANTIC_DIMENSIONS)
    if delta_path.exists():
        previous_delta = json.loads(delta_path.read_text())
        assert builder.metadata_matches(previous_delta, expected)
        delta["entries"] = previous_delta["entries"]
        entries.update(delta["entries"])
    pending = []
    for key, kind, entry, slot in rows:
        text = pg.semantic_text_for_entry(entry, slot, kind=kind)
        cached = entries.get(key)
        if cached and cached.get("text") == text and len(cached.get("vector", [])) == expected["embedding_dimensions"]:
            continue
        pending.append((key, kind, entry, slot, text))
    print(f"Verified compatible exact-text cache; {len(pending)} entries remain; batch size 1", flush=True)
    for i, (key, kind, entry, slot, text) in enumerate(pending, 1):
        vectors = pg.embed_texts_with_gemini([text], model=expected["embedding_model"],
            dimensions=expected["embedding_dimensions"], retry_attempts=4, retry_initial_delay=15.0)
        assert len(vectors) == 1 and len(vectors[0]) == expected["embedding_dimensions"]
        delta["entries"][key] = dict(kind=kind, slot=slot, id=entry.get("id"), text=text, vector=vectors[0])
        builder.write_payload(delta_path, delta, compact=True)
        if i % 25 == 0 or i == len(pending):
            print(f"Embedded delta {i}/{len(pending)} entries", flush=True)
    entries.update(delta["entries"])
    expected["entries"] = entries
    output = HERE / "semantic-combined-checkpoint.json"
    builder.write_payload(output, expected, compact=True)
    record = dict(provider=expected["provider"], embedding_model=expected["embedding_model"],
        embedding_dimensions=expected["embedding_dimensions"], batch_size=1,
        source_dictionary_sha256=expected["dictionary_hash"], existing_compatible_entries=len(rows)-len(pending),
        newly_embedded_in_delta=len(pending), expected_total=len(rows),
        combined_checkpoint_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
        validation="Final official build_semantic_index.py must recheck every row and build BM25F before use.")
    builder.write_payload(HERE / "embedding-delta-completion.json", record)
    print("Combined exact-text checkpoint ready for the official builder", flush=True)


if __name__ == "__main__":
    main()
