"""Current, actually audited API inputs; provider calls are never needed."""
import atexit
import copy
import json
from pathlib import Path
import tempfile

from tests import photo_prompt_fixtures as fixtures
from tests.test_photo_authorship_policy import PhotoAuthorshipPolicyTests
import prompt_generator as pg
from photo_runtime_sources import RuntimeSnapshotProvider

_temporary = None
_template = None
_verified = None
_original_from_receipt = RuntimeSnapshotProvider.from_receipt


def write_valid_inputs(directory: Path) -> dict:
    global _temporary, _template, _verified
    if _template is None:
        _temporary = tempfile.TemporaryDirectory(prefix="photo-api-source-")
        atexit.register(_temporary.cleanup)
        store = Path(_temporary.name) / "runtime"
        provider = RuntimeSnapshotProvider(store=store)
        snapshot = provider.acquire()
        raw = fixtures.core("A blue porcelain teacup on a rainlit kitchen counter.")
        controls = pg.creative_controls.resolve(raw["source_request"],
            overrides={"sensual": 0, "fetish": 0, "surreal": 0, "creativity": 0}, seed=7)
        raw["creative_controls_sha256"] = controls["canonical_sha256"]
        core = pg.normalize_authorial_core(raw, request_envelope=pg.normalize_request_envelope(fixtures.envelope(raw["source_request"])),
            creative_control_snapshot=controls)
        pack = pg.generate_candidate_pack(snapshot.data, core, controls, fixtures.review(core["baseline_prompt_en"]), seed=7)
        composed = PhotoAuthorshipPolicyTests.composed(pack)
        request = {"schema_version": "photo-image-render-request/v2", "pack_id": pack["pack_id"],
            "core_retrieval_sha256": pack["core_retrieval"]["canonical_sha256"],
            "source_intent_lock_sha256": core["intent_lock"]["canonical_sha256"],
            "source_embodiment_preflight_sha256": pack["embodiment_preflight"]["canonical_sha256"],
            "runtime_prompt_en": composed["prompt_en"] + ("\n\nAvoid: " + pack["negative_en"] if pack["negative_en"] is not None else ""),
            "runtime_negative_en": pack["negative_en"], "references": [],
            "audit_boundary": {"composed_prompt_audit_status": "pass", "runtime_prompt_audit_status": "not_run", "inherits_composed_prompt_pass": False}}
        _template = {"pack": pack, "composed": composed, "request": request,
            "receipt": provider.receipt(snapshot, pack), "store": str(store)}
        _verified = _original_from_receipt(provider, pack, _template["receipt"])
    result = {"runtime_store": Path(_template["store"])}
    for key in ("pack", "receipt", "composed", "request"):
        path = directory / f"{key}.json"
        path.write_text(json.dumps(copy.deepcopy(_template[key]), ensure_ascii=False, indent=2), encoding="utf-8")
        result[key + "_file"] = path
    return result


def verified_fixture_receipt(provider, pack, receipt=None):
    """Reuse only the exact independently verified immutable test template.

    Actual composed/runtime audits still run. Changed pack/receipt inputs use
    the real resolver. Generation corruption is exercised by freshness tests,
    which do not install this fixture optimization.
    """
    if (_template is not None and provider.publisher.store == Path(_template["store"]).resolve()
            and json.dumps(pack, sort_keys=True, ensure_ascii=False) == json.dumps(_template["pack"], sort_keys=True, ensure_ascii=False)
            and receipt == _template["receipt"]):
        return _verified
    return _original_from_receipt(provider, pack, receipt)
