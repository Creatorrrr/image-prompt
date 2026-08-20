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


if __name__ == "__main__":
    unittest.main()
