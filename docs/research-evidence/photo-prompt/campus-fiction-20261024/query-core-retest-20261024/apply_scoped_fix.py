from pathlib import Path
import shutil
R=Path('/Users/chasoik/Projects/image-prompt');S=R/'skills/photo-prompt-image-generator';O=Path(__file__).resolve().parent

def edit(root,rel,old,new):
 p=root/rel;s=p.read_text();assert s.count(old)==1,(str(p),s.count(old));p.write_text(s.replace(old,new))
for root in [S,O/'overlay']:
 if root!=S:
  for n in ['photo_request_query_scope.py','photo_request_ownership.py']:
   shutil.copyfile(S/'precore'/n,root/'precore'/n)
 edit(root,'precore/photo_authoring_wire.py','        "topic_context",\n','        "topic_context",\n        "query_scope",\n')
 edit(root,'precore/photo_authoring_wire.py','    normalized["canonical_sha256"] = canonical_json_sha256(normalized)\n    normalized["envelope_id"]',
 '''    if "query_scope" in payload:
        normalized["query_scope"] = normalize_request_query_scope(
            payload["query_scope"], request_text, spans, normalized.get("topic_context"))
    normalized["canonical_sha256"] = canonical_json_sha256(normalized)
    normalized["envelope_id"]''')
 edit(root,'precore/photo_authoring_wire.py','def normalize_topic_context(payload: Any, request_text: str, active_spans: List[JsonDict]) -> JsonDict:',
 '''def normalize_request_query_scope(payload, request_text, active_spans, topic_context=None):
    import photo_request_query_scope
    return photo_request_query_scope.normalize(payload, request_text, active_spans, topic_context)

def request_query_scope_fields(scope, topic_context=None):
    import photo_request_query_scope
    return photo_request_query_scope.retrieval_fields(scope, topic_context)

def normalize_topic_context(payload: Any, request_text: str, active_spans: List[JsonDict]) -> JsonDict:''')
 edit(root,'precore/photo_authoring_wire.py','    runtime_forbidden_labels = [\n',
 '''    if "query_scope" in request_envelope:
        normalized["request_binding"]["query_scope"] = copy.deepcopy(request_envelope["query_scope"])
    runtime_forbidden_labels = [
''')
 edit(root,'precore/prepare_photo_run.py','    wire.normalize_request_envelope(envelope)\n',
 '''    if getattr(args,"query_scope",None) is not None:
        envelope["query_scope"] = read_json(args.query_scope)
    wire.normalize_request_envelope(envelope)
''')
 edit(root,'precore/prepare_photo_run.py','        selection = read_json(args.selection)\n',
 '''        selection = read_json(args.selection)
        if "ownership_review" not in selection:
            raise WorkflowError("requester_ownership_review_required_for_new_freeze")
''')
 edit(root,'precore/prepare_photo_run.py','    p.add_argument("--topic-context", type=Path, help="reviewed exact prior-user quotes linked to active current spans; discovery only")\n',
 '''    p.add_argument("--topic-context", type=Path, help="reviewed exact prior-user quotes linked to active current spans; discovery only")
    p.add_argument("--query-scope", type=Path, help="exact reviewed visual/topic/reference/workflow segments; discovery only")
''')
 edit(root,'precore/photo_feature_selection.py','            "selected",\n','            "selected",\n            "ownership_review",\n')
 edit(root,'precore/photo_feature_selection.py','    warnings: list[str] = []\n',
 '''    ownership = None
    if "ownership_review" in record:
        import photo_request_ownership
        ownership = photo_request_ownership.validate(record["ownership_review"], authorial_core,
                                                      record, request_envelope, required_evidence)
    warnings: list[str] = []
''')
 edit(root,'precore/photo_feature_selection.py','        "warnings": warnings,\n','        "warnings": warnings,\n        **({"ownership_review": ownership} if ownership is not None else {}),\n')
 old='''        for item in active_spans:
            add("source_request_scope", creative_controls.strip_assignments(str(item.get("text") or "")))
        if "topic_context" in request_binding:
            context = _authoring_wire.normalize_topic_context(request_binding["topic_context"], str(core.get("source_request") or ""), active_spans)
            for link in context["links"]:
                add("request_topic_context", creative_controls.strip_assignments(link["topic_quote"]["text"]))'''
 new='''        context = None
        if "topic_context" in request_binding:
            context = _authoring_wire.normalize_topic_context(request_binding["topic_context"], str(core.get("source_request") or ""), active_spans)
        if "query_scope" in request_binding:
            query_scope = _authoring_wire.normalize_request_query_scope(
                request_binding["query_scope"], str(core.get("source_request") or ""), active_spans, context)
            for field, value in _authoring_wire.request_query_scope_fields(query_scope, context):
                add(field, creative_controls.strip_assignments(value))
        else:
            # Frozen historical requests retain their original projection.
            for item in active_spans:
                add("source_request_scope", creative_controls.strip_assignments(str(item.get("text") or "")))
            if context is not None:
                for link in context["links"]:
                    add("request_topic_context", creative_controls.strip_assignments(link["topic_quote"]["text"]))'''
 edit(root,'scripts/prompt_generator.py',old,new)
 edit(root,'scripts/prompt_generator.py','            provenance["topic_context_sha256"] = context["canonical_sha256"]\n',
 '''            provenance["topic_context_sha256"] = context["canonical_sha256"]
        if "query_scope" in request_binding:
            provenance["request_query_scope_sha256"] = query_scope["canonical_sha256"]
            provenance["request_query_segment_purposes"] = [r["purpose"] for r in query_scope["segments"]]
''')
 edit(root,'scripts/photo_h_f2_queries.py',"WHOLE_RECIPE='photo-h-f2-whole-scene-query/v2'", "WHOLE_RECIPE='photo-h-f2-whole-scene-query/v3'")
print('Scoped working edits and sealed-base overlay completed')
