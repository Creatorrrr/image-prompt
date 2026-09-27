"""Check optional discovery with novel wording and unchanged real vectors."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = HERE / "qualification-source"
ASSETS = SOURCE / "skills/photo-prompt-image-generator/assets"
sys.path.insert(0, str(ASSETS.parent / "scripts"))
import prompt_generator as generator
import build_semantic_index

registry = generator.load_visual_obligation_registry(ASSETS / "photo_prompt_visual_obligations.json")
index = generator.load_visual_profile_index(ASSETS / "photo_prompt_visual_profile_index.json", registry)
queries = {
    "y2kr_spiky_bun": "A tightly gathered hair knot has several straight tips sticking out around its edge.",
    "y2kr_zigzag_part": "The scalp part changes direction repeatedly with alternating left and right angles.",
    "y2kr_low_rise": "The trousers sit below the navel at the upper hips, leaving the natural waist exposed.",
    "y2kr_bootcut": "Denim fits the thighs and knees, then opens modestly around the lower calf to cover boot shafts.",
    "y2kr_butterfly_clips": "Two small butterfly-shaped clips grip the side hair next to the forehead.",
    "y2kr_velour": "The garment shows dense short fuzz with a smooth directional sheen rather than yarn loops.",
    "y2kr_terry": "Dense small upright yarn loops give the top surface a granular towel-like texture.",
    "y2kr_flip_phone": "An open hinged handset has physical keys on one half and a small display on the other.",
}
results = []
for profile_id, query in queries.items():
    vectors = {profile["id"]: [1.0, 0.0] if profile["id"] == profile_id else [0.0, 1.0] for profile in registry["profiles"]}
    fake_index = generator.build_visual_profile_index_payload(registry, vectors=vectors, dimensions=2)
    result = generator.resolve_visual_profile_hits(registry, [{"source": "authorial_core_interpretation", "text": query, "polarity": "advisory"}],
                                                   visual_profile_index=fake_index, query_text=query, query_vector=[1.0, 0.0], adult_context=True)
    expected = next(row for row in result["hits"] if row["profile_id"] == profile_id)
    assert expected["optional_eligible"] and not expected["hard_eligible"]
    results.append({"profile_id": profile_id, "query": query, "fake_vector_optional_boundary": "pass"})
build_semantic_index.PROJECT_ROOT = ROOT
build_semantic_index.load_project_env()
query_vectors = {}
for row in results:
    query = row["query"]
    vector = generator.embed_texts_with_gemini([query], dimensions=768, retry_attempts=0)[0]
    query_vectors[row["profile_id"]] = vector
    result = generator.resolve_visual_profile_hits(registry, [{"source": "authorial_core_interpretation", "text": query, "polarity": "advisory"}],
                                                   visual_profile_index=index, query_text=query, query_vector=vector, adult_context=True)
    hits = {hit["profile_id"]: hit for hit in result["hits"]}
    hit = hits.get(row["profile_id"])
    row["real_index_optional_discovery"] = "pass" if hit and hit["optional_eligible"] and not hit["hard_eligible"] else "not_exposed"
    row["any_hard_activation"] = any(hit.get("hard_eligible") for hit in result["hits"])
    row["optional_y2k_profile_ids"] = [key for key, hit in hits.items() if key.startswith("y2kr_") and hit.get("optional_eligible")]
summary = {"method": "Novel agent-authored wording; fixed full 944-profile index; query embeddings are single-text requests; retrieval is advisory only", "profiles_tested": len(results),
           "fake_vector_optional_boundary_passes": len(results), "real_index_optional_discovery_passes": sum(row["real_index_optional_discovery"] == "pass" for row in results),
           "unexpected_hard_activations": sum(row["any_hard_activation"] for row in results), "results": results,
           "limit": "Focused discovery diagnostics, not representative rendered-image qualification or causal improvement evidence."}
(HERE / "retrieval-probe-query-vectors.json").write_text(json.dumps(query_vectors) + "\n")
(HERE / "retrieval-probe.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps({key: value for key, value in summary.items() if key != "results"}))
