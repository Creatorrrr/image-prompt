"""Independent root check: partial discovery contexts cannot grant final reuse."""
from pathlib import Path
import hashlib
import json
import sys
from unittest import mock

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(ROOT), str(ROOT / 'skills/photo-prompt-image-generator/scripts')]
from tests import test_photo_native_member_scope_transport as t
from tests import test_photo_native_existing_member_scope as f
import photo_semantic_evidence as native
import photo_native_owner_resolution as resolver
import photo_embedding_provider as provider


def forbidden(*args, **kwargs): raise AssertionError('No embedding execution in boundary check')


provider.embed = provider.embed_many = forbidden
assert hashlib.sha256(Path(native.__file__).read_bytes()).hexdigest() == '35fbb2b6af1140f914b73fadd6e3833629ad6409efbbcf9c281f2f606b607548'
data = t.MemberScopeClosureTests().compound(True)
core = f.scope_core()
selected = f.choices(data, core)
selected['entries'] += f.choices(data, core, cid=f.B)['entries']
results = []
for entry in f.entries(data, core, mapping=selected, dependency_selections={f.B: 'base'}):
    partial = native._resolve_selected_native_contracts([entry], core, node_only=True)
    partial['discovery_partial'] = True
    assert not partial['nodes'][f.A]['selected_children']
    assert not native._context_covers(partial, [entry], core)
    assert native._context_covers(partial, [entry], core, allow_partial=True)
    token = native._ACTIVE_RESOLUTION.set(partial)
    try:
        with mock.patch.object(resolver, 'resolve_selected_contracts', wraps=resolver.resolve_selected_contracts) as calls:
            with native.bound_selected_resolution([entry], core) as strict:
                assert strict is not partial and not strict.get('discovery_partial')
                assert [row['candidate_id'] for row in strict['nodes'][f.A]['selected_children']] == [f.B]
                assert native.admission(entry, core)['allowed']
                native.permission_scope(entry, core)
            assert calls.call_count == 1
        results.append({'view': 'sealed_compact', 'partial_reused_for_strict': False, 'actual_child_retained': True, 'fresh_B1_calls': 1})
    finally: native._ACTIVE_RESOLUTION.reset(token)
out = HERE / 'ROOT-MEMBER-B2-DISCOVERY-BOUNDARY-01.json'
with out.open('x') as stream:
    json.dump({'schema': 'photo-root-B2-independent-discovery-boundary/v1', 'actor': '/root',
        'cases': results, 'all_passed': True,
        'boundary': 'Explicit isolated synthetic partial context, two independently constructed full/compact entry paths. No operating candidate/source qualification or corpus semantic approval.',
        'model_provider_network_calls': 0, 'Gemini_calls': 0}, stream, sort_keys=True, indent=2)
    stream.write('\n')
print(json.dumps({'cases': len(results), 'strict_fresh_resolution_each': 1, 'all_passed': True}))
