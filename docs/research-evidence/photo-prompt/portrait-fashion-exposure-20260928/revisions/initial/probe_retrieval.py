"""Read-only diagnostic of real registry/index retrieval with cached query vectors."""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
SKILL = ROOT / "skills/photo-prompt-image-generator"
sys.path.insert(0, str(SKILL / "scripts"))
import prompt_generator as pg
from build_visual_profile_index import load_project_env


def main():
    load_project_env()
    fixture_path = HERE / "retrieval_probes.json"
    fixture = json.loads(fixture_path.read_text())
    registry = pg.load_visual_obligation_registry(SKILL / "assets/photo_prompt_visual_obligations.json")
    index = pg.load_visual_profile_index(SKILL / "assets/photo_prompt_visual_profile_index.json", registry)
    cache_path = HERE / "query_vectors.json"
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    rows = []
    for case in fixture["cases"]:
        q = case["query"]
        key = hashlib.sha256(q.encode()).hexdigest()
        if key not in cache:
            cache[key] = pg.embed_texts_with_gemini([q], model=pg.SEMANTIC_MODEL_ID, dimensions=768)[0]
            cache_path.write_text(json.dumps(cache, separators=(",", ":")) + "\n")
        resolved = pg.resolve_visual_profile_hits(registry,
            [{"source": "authorial_core_interpretation", "text": q, "polarity": "advisory"}],
            visual_profile_index=index, query_text=q, query_fields={"interpreted_intent": q},
            query_vector=cache[key], adult_context=True)
        hits = [{"profile_id": h["profile_id"], "match_basis": h["match_basis"],
                 "hard_eligible": h.get("hard_eligible"), "optional_eligible": h.get("optional_eligible")}
                for h in resolved["hits"]]
        expected = case.get("expected_profile")
        rows.append({**case, "expected_discovered": any(h["profile_id"] == expected for h in hits) if expected else None,
                     "new_optional_hits": [h for h in hits if h["profile_id"].startswith("pfe_")],
                     "any_new_hard_hit": any(h["profile_id"].startswith("pfe_") and h["hard_eligible"] for h in hits)})
        print(case["id"], rows[-1]["expected_discovered"], flush=True)
    report = {"fixture_sha256": hashlib.sha256(fixture_path.read_bytes()).hexdigest(),
              "registry_sha256": index["registry_sha256"], "provider": index["provider"],
              "embedding_model": index["embedding_model"], "dimensions": 768, "cases": rows,
              "limitations": "Discoverability and authority diagnostics only; optional adjacent hits are not false hard activation or automatic candidate selection. No image was generated."}
    (HERE / "retrieval-results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
