"""Shared failure routes; authorization and provider safeguards still apply."""
from photo_workflow_state import WorkflowError

TRANSIENT_HTTP = frozenset({429, 500, 502, 503, 504})
SAME_INPUT_FAILURES = frozenset({"transient_http", "provider_blocked"})
RECOVERY_FAILURES = frozenset({"persistence_failed", "recorder_failed", "execution_unknown", "invalid_review_record", "provider_error"})
REVISION_FAILURES = frozenset({"meaning_rebuild", "agent_spatial_inconsistency", "artistic_revision"})
PIXEL_FAILURES = frozenset({"pixel_realization_mismatch", "unobservable_required_scale"})
FAILURE_CLASSES = SAME_INPUT_FAILURES | RECOVERY_FAILURES | REVISION_FAILURES | PIXEL_FAILURES


def retry_mode(failure_class, *, changed=False):
    if failure_class not in FAILURE_CLASSES:
        raise WorkflowError("invalid_failure_class")
    if failure_class in SAME_INPUT_FAILURES:
        if changed:
            raise WorkflowError("failure_requires_same_input")
        return "same_input"
    if failure_class in RECOVERY_FAILURES:
        if changed:
            raise WorkflowError("failure_requires_recovery")
        return "recovery_only"
    if not changed and failure_class in REVISION_FAILURES:
        raise WorkflowError("content_revision_requires_changed_dimensions")
    return "revised_content" if changed else "same_input"


def observed_failure(status, *, details=None, provider_outcome=None):
    """Use captured evidence, never keywords in the provider's prose."""
    details = details or {}
    if status == "safety_block":
        return "provider_blocked"
    if provider_outcome == "unknown":
        return "execution_unknown"
    if status == "error" and provider_outcome == "returned":
        return "persistence_failed"
    if status == "error" and details.get("http_status") in TRANSIENT_HTTP:
        return "transient_http"
    return "provider_error" if status == "error" else None


def can_repeat_captured(evidence):
    """Only a known rejection can consume an already authorized next call."""
    outcome = evidence["outcome"]
    return evidence.get("provider_outcome") == "rejected" and observed_failure(
        outcome["status"], details=outcome, provider_outcome="rejected") in SAME_INPUT_FAILURES
