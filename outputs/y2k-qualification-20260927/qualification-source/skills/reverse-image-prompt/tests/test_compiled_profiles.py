#!/usr/bin/env python3

from __future__ import annotations

from contextlib import redirect_stdout
import io
from pathlib import Path
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

from compile_skill import compile_skill, default_modules  # noqa: E402
from module_metadata import ROOT, load_manifest  # noqa: E402


PROFILE_OUTPUTS = {
    "core": "SKILL.compiled.core.md",
    "all": "SKILL.compiled.all.md",
    "portrait": "SKILL.compiled.portrait.md",
    "product": "SKILL.compiled.product.md",
    "screenshot": "SKILL.compiled.screenshot.md",
}


class CompiledProfileTests(unittest.TestCase):
    def test_checked_in_profiles_match_current_sources(self) -> None:
        manifest = load_manifest(ROOT)
        with tempfile.TemporaryDirectory() as temp_dir:
            for profile, filename in PROFILE_OUTPUTS.items():
                with self.subTest(profile=profile):
                    output = Path(temp_dir) / filename
                    modules = default_modules(manifest, profile, [])
                    with redirect_stdout(io.StringIO()):
                        compile_skill(modules, output)
                    self.assertEqual(
                        output.read_text(encoding="utf-8"),
                        (ROOT / filename).read_text(encoding="utf-8"),
                    )

    def test_profiles_include_only_applicable_lane_contracts(self) -> None:
        manifest = load_manifest(ROOT)
        expectations = {
            "core": {"lane.global-composition"},
            "portrait": {
                "lane.global-composition",
                "lane.spatial-topology",
                "lane.subject-appearance",
                "lane.color-light-material",
                "lane.medium-aesthetic-capture",
            },
            "product": {
                "lane.global-composition",
                "lane.spatial-topology",
                "lane.subject-appearance",
                "lane.color-light-material",
                "lane.medium-aesthetic-capture",
                "lane.information-layout",
            },
            "screenshot": {
                "lane.global-composition",
                "lane.spatial-topology",
                "lane.subject-appearance",
                "lane.color-light-material",
                "lane.medium-aesthetic-capture",
                "lane.information-layout",
            },
            "all": {lane["id"] for lane in manifest.get("analysis_lanes", [])},
        }
        all_lane_ids = {lane["id"] for lane in manifest.get("analysis_lanes", [])}
        with tempfile.TemporaryDirectory() as temp_dir:
            for profile, expected in expectations.items():
                with self.subTest(profile=profile):
                    output = Path(temp_dir) / f"{profile}.md"
                    with redirect_stdout(io.StringIO()):
                        compile_skill(default_modules(manifest, profile, []), output)
                    text = output.read_text(encoding="utf-8")
                    present = {
                        lane_id
                        for lane_id in all_lane_ids
                        if f"# Included analysis lane: `{lane_id}`" in text
                    }
                    self.assertEqual(present, expected)


if __name__ == "__main__":
    unittest.main()
