#!/usr/bin/env python3

from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

from profile_context import (  # noqa: E402
    SCHEMA,
    VERSION,
    main,
    read_profile_files,
    render_profile_text,
)


SCRIPT = TOOLS / "profile_context.py"
SOURCE = (
    "Shared first.\n"
    "<!-- profile:prompt -->\n"
    "Compact instructions.\n"
    "<!-- /profile -->\n"
    "Shared middle.\n"
    "<!-- profile:audited -->\n"
    "Audited instructions.\n"
    "<!-- /profile -->\n"
    "Shared last."
)
PROMPT_VIEW = "Shared first.\nCompact instructions.\nShared middle.\nShared last."
AUDITED_VIEW = "Shared first.\nShared middle.\nAudited instructions.\nShared last."


class RenderProfileTextTests(unittest.TestCase):
    def test_distinct_views_preserve_shared_text_in_source_order(self) -> None:
        self.assertEqual(render_profile_text(SOURCE, "prompt"), PROMPT_VIEW)
        self.assertEqual(render_profile_text(SOURCE, "audited"), AUDITED_VIEW)

    def test_shared_prose_is_never_heuristically_filtered(self) -> None:
        text = (
            "The audited profile still needs this shared sentence.\n"
            "prompt profile:audited /profile profile:prompt\n"
            "<!-- ordinary comment about profile:audited -->\n"
            "  # 공유 문장\r\n\t* Keep all spacing.  \n\nend"
        )
        for profile in ("prompt", "audited", "combined"):
            with self.subTest(profile=profile):
                self.assertEqual(render_profile_text(text, profile), text)

    def test_combined_keeps_both_blocks_in_source_order_without_markers(self) -> None:
        self.assertEqual(
            render_profile_text(SOURCE, "combined"),
            "Shared first.\nCompact instructions.\nShared middle.\nAudited instructions.\nShared last.",
        )

    def test_preserves_line_endings_and_whitespace_around_content(self) -> None:
        source = (
            "공유  \r\n"
            "\t<!-- profile:prompt -->  \r\n"
            "  Keep\tthis.\r\n"
            " <!-- /profile -->\r\n"
            "<!-- profile:audited -->\n"
            "omit\n"
            "<!-- /profile -->\n"
            "tail"
        )
        self.assertEqual(render_profile_text(source, "prompt"), "공유  \r\n  Keep\tthis.\r\ntail")

    def test_repeated_adjacent_and_empty_blocks_are_valid(self) -> None:
        source = (
            "<!-- profile:prompt -->\n"
            "<!-- /profile -->\n"
            "<!-- profile:prompt -->\n"
            "first\n"
            "<!-- /profile -->\n"
            "<!-- profile:prompt -->\n"
            "second\n"
            "<!-- /profile -->"
        )
        self.assertEqual(render_profile_text(source, "prompt"), "first\nsecond\n")
        self.assertEqual(render_profile_text(source, "audited"), "")

    def test_empty_shared_text_is_valid(self) -> None:
        self.assertEqual(render_profile_text("", "prompt"), "")

    def test_unknown_profiles_fail_before_returning_shared_text(self) -> None:
        for profile in ("", "Prompt", "full", None):
            with self.subTest(profile=profile), self.assertRaises(ValueError):
                render_profile_text("shared", profile)

    def test_unknown_and_malformed_markers_fail_closed(self) -> None:
        markers = (
            "<!-- profile:unknown -->",
            "<!-- profile:combined -->",
            "<!-- profile -->",
            "<!-- profile :prompt -->",
            "<!--profile:prompt-->",
            "<!-- profile:prompt --> trailing text",
            "inline <!-- profile:prompt -->",
            "<!-- profile:prompt --> <!-- /profile -->",
            "<!-- profile:prompt",
            "<!-- /profile",
            "<!-- PROFILE:prompt -->",
            "<!-- / profile -->",
            "<!-- /profile:audited -->",
            "<!--\nprofile:prompt\n-->",
            "<!--\n/profile\n-->",
            "<!-- profile:prompt --!>",
            "<! -- profile:prompt -->",
            "<!- profile:prompt -->",
            "<-- profile:prompt -->",
            "<!--- profile:prompt -->",
            "< !-- /profile -->",
        )
        for marker in markers:
            for profile in ("prompt", "audited", "combined"):
                with self.subTest(marker=marker, profile=profile), self.assertRaises(ValueError):
                    render_profile_text(f"shared\n{marker}\nmore shared\n", profile)

    def test_unbalanced_markers_fail_even_for_excluded_profile(self) -> None:
        sources = (
            "<!-- /profile -->\n",
            "<!-- profile:prompt -->\ncontent",
            "<!-- profile:audited -->\ncontent",
            "<!-- profile:prompt -->\n<!-- /profile -->\n<!-- /profile -->\n",
        )
        for source in sources:
            for profile in ("prompt", "audited", "combined"):
                with self.subTest(source=source, profile=profile), self.assertRaises(ValueError):
                    render_profile_text(source, profile)

    def test_nested_blocks_fail_regardless_of_profile_selection(self) -> None:
        for outer in ("prompt", "audited"):
            for inner in ("prompt", "audited"):
                source = (
                    f"<!-- profile:{outer} -->\n"
                    f"<!-- profile:{inner} -->\n"
                    "content\n<!-- /profile -->\n<!-- /profile -->\n"
                )
                for profile in ("prompt", "audited", "combined"):
                    with self.subTest(outer=outer, inner=inner, profile=profile):
                        with self.assertRaisesRegex(ValueError, "nested"):
                            render_profile_text(source, profile)

    def test_invalid_marker_in_excluded_block_still_fails(self) -> None:
        source = "<!-- profile:audited -->\n<!-- profile:unknown -->\n<!-- /profile -->\n"
        with self.assertRaisesRegex(ValueError, "line 2"):
            render_profile_text(source, "prompt")


class ProfileContextCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.root = self.base / "skill"
        (self.root / "modules").mkdir(parents=True)
        self.file = self.root / "modules" / "fixture.md"
        self.file.write_bytes(SOURCE.encode("utf-8"))

    def run_cli(self, *args: str, script: Path = SCRIPT) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(script), *args],
            cwd=self.base,
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )

    def request(self, *files: str, profile: str = "prompt") -> subprocess.CompletedProcess[str]:
        return self.run_cli("--analysis-profile", profile, "--root", str(self.root), "--files", *files)

    def assert_failed_without_output(self, result: subprocess.CompletedProcess[str]) -> None:
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("error:", result.stderr)

    def test_cli_returns_complete_ordered_bundle_and_hashes(self) -> None:
        second = self.root / "other.md"
        second.write_bytes("둘째 파일\r\n".encode("utf-8"))
        result = self.request("other.md", "modules/./fixture.md")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        bundle = json.loads(result.stdout)
        self.assertEqual(bundle["schema"], SCHEMA)
        self.assertEqual(bundle["version"], VERSION)
        self.assertEqual(bundle["profile"], "prompt")
        self.assertEqual([item["path"] for item in bundle["files"]], ["other.md", "modules/fixture.md"])
        self.assertEqual(bundle["files"][0]["content"], "둘째 파일\r\n")
        fixture = bundle["files"][1]
        self.assertEqual(fixture["content"], PROMPT_VIEW)
        self.assertEqual(fixture["source_sha256"], hashlib.sha256(self.file.read_bytes()).hexdigest())
        self.assertEqual(fixture["view_sha256"], hashlib.sha256(PROMPT_VIEW.encode("utf-8")).hexdigest())
        self.assertEqual(fixture["source_words"], len(SOURCE.split()))
        self.assertEqual(fixture["view_words"], len(PROMPT_VIEW.split()))
        self.assertEqual(self.file.read_bytes(), SOURCE.encode("utf-8"))

    def test_audited_cli_selects_audited_block(self) -> None:
        result = self.request("modules/fixture.md", profile="audited")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["files"][0]["content"], AUDITED_VIEW)

    def test_source_and_view_hashes_preserve_raw_utf8_and_crlf(self) -> None:
        source = SOURCE.replace("\n", "\r\n").replace("Shared first.", "공유 문장.").encode("utf-8")
        self.file.write_bytes(source)
        entry = read_profile_files([self.file], "prompt", self.root)["files"][0]
        expected = PROMPT_VIEW.replace("\n", "\r\n").replace("Shared first.", "공유 문장.")
        self.assertEqual(entry["content"], expected)
        self.assertEqual(entry["source_sha256"], hashlib.sha256(source).hexdigest())
        self.assertEqual(entry["view_sha256"], hashlib.sha256(expected.encode("utf-8")).hexdigest())

    def test_excluded_content_changes_source_hash_but_not_view_hash(self) -> None:
        before = read_profile_files([self.file], "prompt", self.root)["files"][0]
        self.file.write_text(SOURCE.replace("Audited instructions.", "Updated audited obligations."), encoding="utf-8")
        after = read_profile_files([self.file], "prompt", self.root)["files"][0]
        self.assertNotEqual(before["source_sha256"], after["source_sha256"])
        self.assertEqual(before["view_sha256"], after["view_sha256"])

    def test_invalid_later_file_never_emits_partial_bundle(self) -> None:
        invalid = self.root / "invalid.md"
        for contents in (b"<!-- profile:audited -->\nunclosed", b"invalid utf-8: \xff"):
            with self.subTest(contents=contents):
                invalid.write_bytes(contents)
                self.assert_failed_without_output(self.request("modules/fixture.md", "invalid.md"))

    def test_missing_later_file_and_directory_fail_without_output(self) -> None:
        for bad_path in ("missing.md", "modules"):
            with self.subTest(path=bad_path):
                self.assert_failed_without_output(self.request("modules/fixture.md", bad_path))

    def test_unreadable_later_file_fails_without_output(self) -> None:
        unreadable = self.root / "unreadable.md"
        unreadable.write_text("private", encoding="utf-8")
        original_read = Path.read_bytes

        def read_bytes(path: Path) -> bytes:
            if path == unreadable.resolve():
                raise PermissionError("fixture denied")
            return original_read(path)

        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.object(Path, "read_bytes", read_bytes), redirect_stdout(stdout), redirect_stderr(stderr):
            with self.assertRaises(SystemExit) as error:
                main(["--analysis-profile", "prompt", "--root", str(self.root), "--files", "modules/fixture.md", "unreadable.md"])
        self.assertNotEqual(error.exception.code, 0)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("fixture denied", stderr.getvalue())

    def test_traversal_absolute_escape_and_symlink_escape_are_rejected(self) -> None:
        outside = self.base / "outside.md"
        outside.write_text("outside instructions", encoding="utf-8")
        (self.root / "linked.md").symlink_to(outside)
        for escaped in ("../outside.md", str(outside), "linked.md"):
            with self.subTest(path=escaped):
                result = self.request("modules/fixture.md", escaped)
                self.assert_failed_without_output(result)
                self.assertIn("escapes skill root", result.stderr)

    def test_default_root_comes_from_tool_location_instead_of_cwd(self) -> None:
        tools = self.root / "tools"
        tools.mkdir()
        copied_script = tools / SCRIPT.name
        shutil.copyfile(SCRIPT, copied_script)
        result = self.run_cli("--analysis-profile", "prompt", "--files", "modules/fixture.md", script=copied_script)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["files"][0]["content"], PROMPT_VIEW)

    def test_combined_is_not_an_analysis_profile(self) -> None:
        self.assert_failed_without_output(self.request("modules/fixture.md", profile="combined"))
        with self.assertRaises(ValueError):
            read_profile_files([self.file], "combined", self.root)

    def test_empty_files_and_invalid_root_fail_without_output(self) -> None:
        self.assert_failed_without_output(self.request())
        for root in (self.file, self.root / "missing-root"):
            with self.subTest(root=root):
                self.assert_failed_without_output(
                    self.run_cli("--analysis-profile", "prompt", "--root", str(root), "--files", "fixture.md")
                )
        with self.assertRaises(ValueError):
            read_profile_files([], "prompt", self.root)


if __name__ == "__main__":
    unittest.main()
