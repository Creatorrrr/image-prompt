"""Append V33 validation and delegate sealed V32 tests to their exact source."""
from pathlib import Path
import hashlib
import json

E=Path(__file__).resolve().parent
W=E.parents[3]
I=Path('skills/subculture-illustration-image-generator')
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

proof=E/'V33-PALETTE-DATA-PROOF.json';parent=E/'V32-PARENT-SOURCE.json'
helper=W/'tests/photo_palette_history.py';text=helper.read_text()
for marker,value in [('PROOF_SHA256_PLACEHOLDER',sha(proof)),('PARENT_SHA256_PLACEHOLDER',sha(parent)),('PARENT_TREE_PLACEHOLDER',read(parent)['source_tree'])]:
    assert text.count(marker)==1,marker;text=text.replace(marker,value)
helper.write_text(text);support_sha=sha(helper)

fixtures=W/'tests/photo_prompt_fixtures.py';text=fixtures.read_text()
support=f'''

# V33 authenticates a bounded optional palette addition while retaining V32.
PALETTE_HISTORY_SUPPORT_SHA256 = "{support_sha}"


def _v33_palette_context(source_root):
    base = Path("docs/research-evidence/photo-prompt/color-palette-main-merge-20261007")
    return any((source_root / name).exists() or (source_root / name).is_symlink()
               for name in (base / "V33-PALETTE-DATA-PROOF.json", base / "V32-PARENT-SOURCE.json",
                            Path("skills/subculture-illustration-image-generator/assets/photo_regression_baseline_v33.json")))


def _v33_palette_support(source_root):
    path = _v24_regular_path(source_root, "tests/photo_palette_history.py")
    if hashlib.sha256(path.read_bytes()).hexdigest() != PALETTE_HISTORY_SUPPORT_SHA256:
        raise AssertionError("Frozen V33 palette support code drift")
    from tests import photo_palette_history
    if hashlib.sha256(Path(photo_palette_history.__file__).read_bytes()).hexdigest() != PALETTE_HISTORY_SUPPORT_SHA256:
        raise AssertionError("Frozen V33 loaded support code drift")
    return photo_palette_history
'''
needle='def _v32_require_after_payload(source_root: Path, name: str, current: bytes) -> None:\n'
assert text.count(needle)==1
text=text.replace(needle,needle+'    if _v33_palette_context(source_root):\n        current = _v33_palette_support(source_root).previous_payload(source_root, name, current)\n')
needle='    """Recover four sealed robe/index edits, then follow the authenticated history."""\n'
assert text.count(needle)==1
text=text.replace(needle,needle+'    if _v33_palette_context(source_root):\n        support = _v33_palette_support(source_root)\n        preserved = support.preserved_payload(source_root, row, current)\n        if preserved is not None:\n            return preserved\n        current = support.previous_payload(source_root, row["path"], current)\n')
fixtures.write_text(text+support)

validator=W/I/'scripts/validate_illustration_assets.py';text=validator.read_text()
text=text.replace('version for version in (32, 31, 30,','version for version in (33, 32, 31, 30,',1)
text=text.replace('30, 31, 32}, "unsupported photo baseline version")','30, 31, 32, 33}, "unsupported photo baseline version")',1)
support_validator=f'''

PHOTO_PALETTE_HISTORY_SUPPORT_SHA256 = "{support_sha}"


def _palette_history_support(repo_root):
    path = _photo_v28_regular_path(repo_root, "tests/photo_palette_history.py")
    _require(_sha256(path) == PHOTO_PALETTE_HISTORY_SUPPORT_SHA256,
             "photo V33 palette support code drift")
    from tests import photo_palette_history
    _require(_sha256(Path(photo_palette_history.__file__)) == PHOTO_PALETTE_HISTORY_SUPPORT_SHA256,
             "photo V33 loaded palette support code drift")
    return photo_palette_history
'''
needle='def validate_photo_regression_baseline(\n'
assert text.count(needle)==1;text=text.replace(needle,support_validator+'\n\n'+needle)
needle='    if baseline_version == 31 and (asset_dir / "photo_regression_baseline_v32.json").is_file():\n'
dispatch='''    if baseline_version == 32 and (asset_dir / "photo_regression_baseline_v33.json").is_file():
        support = _palette_history_support(repo_root)
        with tempfile.TemporaryDirectory(prefix="photo-v32-original-") as temporary:
            tree = Path(temporary).resolve() / "tree"
            support.materialize_v32_parent_source(tree, source_root=repo_root)
            (tree / ".venv").symlink_to(Path(sys.executable).parent.parent, target_is_directory=True)
            code = (
                "import json,sys; from pathlib import Path; "
                "sys.path.insert(0,'skills/photo-prompt-image-generator/scripts'); "
                "from photo_runtime_sources import SnapshotPublisher; SnapshotPublisher().publish(); "
                "sys.path.insert(0,'skills/subculture-illustration-image-generator/scripts'); "
                "import validate_illustration_assets as v; "
                "print(json.dumps(v.validate_photo_regression_baseline("
                "Path('skills/subculture-illustration-image-generator/assets'),baseline_version=32)))"
            )
            environment = os.environ.copy()
            environment["PHOTO_RUNTIME_STORE"] = str(Path(temporary).resolve() / "runtime-store")
            environment["GEMINI_API_KEY"] = ""; environment["GOOGLE_API_KEY"] = ""
            completed = subprocess.run([sys.executable, "-c", code], cwd=tree,
                                       env=environment, capture_output=True, text=True, timeout=300)
            _require(completed.returncode == 0,
                     "original V32 replay failed: " + (completed.stderr or completed.stdout))
            return json.loads(completed.stdout.strip().splitlines()[-1])
'''
assert text.count(needle)==1;text=text.replace(needle,dispatch+needle)
text=text.replace('if baseline_version in (29, 30, 32):','if baseline_version in (29, 30, 32, 33):',1)
needle='        _validate_v32_robe_source_successor(asset_dir, repo_root, baseline, pack, raw, receipt)\n'
assert text.count(needle)==1
text=text.replace(needle,needle+'    if baseline_version == 33:\n        _palette_history_support(repo_root).qualify_current(\n            sys.modules[__name__], asset_dir, repo_root, baseline, pack, raw, receipt)\n')
validator.write_text(text)

robe=W/'tests/test_photo_robe_source_boundary_history.py';text=robe.read_text()
needle='import validate_illustration_assets as validator\n'
setup='''
# Current DATA is V33; these unchanged V32 assertions use exact original bytes.
if (ROOT / ILLUSTRATION / 'assets/photo_regression_baseline_v33.json').is_file():
    import atexit
    _live_root = ROOT
    _v32_temporary = tempfile.TemporaryDirectory(prefix='.palette-v32-robe-tests-', dir=ROOT)
    _v32_root = Path(_v32_temporary.name) / 'tree'
    _v32_support = fixtures._v33_palette_support(ROOT)
    _v32_support.materialize_v32_parent_source(_v32_root, source_root=ROOT, link_verified=True)
    (_v32_root / '.venv').symlink_to(Path(sys.executable).parent.parent, target_is_directory=True)
    validator = _v32_support.pinned_v32_validator(_v32_root, source_root=ROOT)
    ROOT = _v32_root
    atexit.register(_v32_temporary.cleanup)
'''
assert text.count(needle)==1;robe.write_text(text.replace(needle,needle+setup))

descriptor=W/I/'assets/universal_scene_baseline_v2.json'
original=(E/'v32-parent-source-files'/I/'assets/universal_scene_baseline_v2.json').read_bytes()
old=read(proof)['previous_validator_sha256'].encode('ascii');assert original.count(old)==1
descriptor.write_bytes(original.replace(old,sha(validator).encode('ascii'),1))
(E/'BOUNDARY-IMPLEMENTATION.json').write_text(json.dumps({'schema':'palette-boundary-implementation/v1','support_sha256':support_sha,'validator_sha256':sha(validator),'fixtures_sha256':sha(fixtures),'universal_descriptor_sha256':sha(descriptor),'v32_test_assertions_unchanged':True},indent=2)+'\n')
print(json.dumps({'support_sha256':support_sha,'validator_sha256':sha(validator),'v33_version_added':True}))
