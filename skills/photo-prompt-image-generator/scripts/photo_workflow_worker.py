"""Run current native auditors against the exact pinned v8 generation."""
from pathlib import Path
from photo_workflow_state import WorkflowError,bound_path,read_json

def audit_bound(state,*,runtime=False,reviews=False):
    from photo_runtime_sources import RuntimeSnapshotProvider,default_store
    import audit_composed_prompt as ca
    import audit_image_render_request as ra
    import audit_image_render_review as gr
    import audit_moe_render_review as vr
    import photo_native_pack as n
    store=Path((state.get('source_binding') or {}).get('runtime_store') or default_store()).resolve()
    receipt=read_json(bound_path(state,'runtime_receipt'));raw=read_json(bound_path(state,'pack'));pack=raw[0] if isinstance(raw,list) and len(raw)==1 else raw
    composed=read_json(bound_path(state,'composed'));snapshot=RuntimeSnapshotProvider(store=store).from_receipt(pack,receipt)
    with ca.bound_native_source(snapshot.data,snapshot.query_context):
        first=ca.audit_composed_prompt(pack,composed,source_data=snapshot.data,query_context=snapshot.query_context);result={'composed_audit':first}
        if runtime:
            path=bound_path(state,'render_request');result['runtime_audit']=ra.audit_image_render_request(pack,composed,read_json(path),request_path=path)
        if first['status']=='pass' and not first['failures']:
            token=ca._BOUND_AUDIT_SOURCE.set(snapshot.data);query_token=ca._BOUND_QUERY_CONTEXT.set(snapshot.query_context)
            try:
                pack=n.read_view(pack);effective,failures=ca.derive_effective_visual_obligation_contract(pack,composed)
                character,gates,character_failures=vr.derive_character_response_render_gates(pack,composed)
                embodiment,embodiment_failures=ca.photo_embodiment.render_gate_ids(pack,composed)
                result.update(effective_visual=effective,contract_failures=failures+character_failures+embodiment_failures,repair=ca.expected_render_repair_contract(pack['authorial_core']),character=character,character_gates=gates,embodiment_gates=embodiment)
                if reviews and 'generic_review' in state['artifacts']:
                    path=bound_path(state,'generic_review');result['generic_review_audit']=gr.audit_image_render_review(pack,composed,read_json(path),review_path=path)
                if reviews and 'visual_review' in state['artifacts']:
                    path=bound_path(state,'visual_review');result['visual_review_audit']=vr.audit_moe_render_review(pack,read_json(path),composed=composed,review_path=path)
            finally:ca._BOUND_AUDIT_SOURCE.reset(token);ca._BOUND_QUERY_CONTEXT.reset(query_token)
        return result
