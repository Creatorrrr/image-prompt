"""Record the actual old/new candidate population without changing a fixture."""
import json
import sys
from pathlib import Path

source = Path(sys.argv[1]).resolve()
output = Path(sys.argv[2])
assets = source / "skills/photo-prompt-image-generator/assets"
sys.path.insert(0, str(assets.parent / "scripts"))
import prompt_generator as generator

registry = generator.load_visual_obligation_registry(assets / "photo_prompt_visual_obligations.json")
index = generator.load_visual_profile_index(assets / "photo_prompt_visual_profile_index.json", registry)
text = "A modern bodycon dress with a Mandarin collar"
source_rows = [{"source": "concept_lock", "text": text, "polarity": "required", "priority": "critical", "mandatory": True}]
resolution = generator.resolve_visual_profile_hits(registry, source_rows, visual_profile_index=index, adult_context=True)
hard_matches = generator.candidate_pack_auto_visual_obligation_matches(registry, source_rows)
optional_matches = generator.candidate_pack_auto_visual_concept_matches(registry, source_rows)
result = {"source_root": str(source), "text": text, "source_rows": source_rows, "hard_profile_ids": [row["profile_id"] for row in resolution["hits"] if row.get("hard_eligible")],
          "optional_profile_ids": [row["profile_id"] for row in resolution["hits"] if row.get("optional_eligible") and not row.get("hard_eligible")],
          "frozen_fixture_compatibility_wrapper": {"hard_profile_ids": sorted(hard_matches), "optional_profile_ids": sorted(optional_matches), "optional_match_records": optional_matches},
          "qipao_hard_activated": any("qipao" in row["profile_id"] and row.get("hard_eligible") for row in resolution["hits"]),
          "claim_limit": "Text-only diagnostic. The frozen fixture uses compatibility projections with component fallback; the typed resolver is reported separately. No fixture expectation was changed."}
output.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result))
