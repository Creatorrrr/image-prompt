"""Post-freeze slot queries plus independent request-topic and baseline queries."""
import hashlib
import photo_slot_expression as expression
import photo_slot_queries as queries
RECIPE='photo-h-f2/v1'
WHOLE_RECIPE='photo-h-f2-whole-scene-query/v2'
REQUEST_TOPIC='__request_topic__'
BASELINE_PROMPT='__baseline_prompt__'
WHOLE_QUERY_IDS=frozenset({REQUEST_TOPIC,BASELINE_PROMPT})


def whole_scene(core,controls,plan):
    """Project frozen positive text, retaining active-arm and exclusion boundaries.

    These are material discovery queries, not new roles or adoption permissions.
    Use the native positive-text projection so explicit exclusions and control
    assignments cannot become positive request-topic search terms. A frozen
    topic_context adds only its reviewed exact prior-user topic quotes, with
    provenance, and never supplies baseline prose or new intent authority.
    """
    from prompt_generator import authorial_core_retrieval_text
    request=core.get('request_binding') or {}
    if not request.get('active_spans'):
        raise ValueError('whole-scene search requires frozen active requester spans')
    rows={}
    for search_id,scope in ((REQUEST_TOPIC,'request_topic'),(BASELINE_PROMPT,'baseline_prompt')):
        projection={key:core[key] for key in ('contract_version','canonical_sha256','source_request','user_exclusions') if key in core}
        if scope=='request_topic':
            projection['request_binding']=request
        else:
            projection['baseline_prompt_en']=core['baseline_prompt_en']
        value,provenance=authorial_core_retrieval_text(projection)
        if not value.strip():
            raise ValueError('empty positive whole-scene query: '+scope)
        binding={'recipe':WHOLE_RECIPE,'search_id':search_id,'scope':scope,
                 'core_sha256':expression.digest(core),'controls_sha256':expression.digest(controls),
                 'expression_plan_sha256':plan['canonical_sha256'],'projection':provenance}
        rows[search_id]={'text':value,'binding':binding,'text_sha256':hashlib.sha256(value.encode()).hexdigest()}
    return rows

def text(role_focus,scene_context):
    if not isinstance(role_focus,str) or not role_focus.strip() or not isinstance(scene_context,str):
        raise ValueError('nonempty authored role focus and scene context required')
    return 'Photographic role: '+role_focus+('\nScene context: '+scene_context if scene_context else '')

def prepare(core,controls,catalog,plan):
    expression.validate(plan,core,controls,catalog)
    rows={}
    for slot,goal in sorted(plan['slots'].items()):
        if goal['status']!='search':continue
        value,fields,binding=queries.inputs(core,controls,catalog,slot,goal['language'],expression_plan=plan,recipe=RECIPE)
        if value!=text(goal['role_focus'],goal['scene_context']):raise ValueError('H query text mismatch')
        rows[slot]={'text':value,'binding':binding,'text_sha256':hashlib.sha256(value.encode()).hexdigest()}
    if WHOLE_QUERY_IDS & (set(catalog)|set(rows)):
        raise ValueError('reserved whole-scene search ID used as a slot')
    scopes={slot:'slot' for slot in rows}
    whole=whole_scene(core,controls,plan)
    rows.update(whole)
    scopes.update({search_id:row['binding']['scope'] for search_id,row in whole.items()})
    return {'recipe':RECIPE,'slots':rows,'query_scopes':scopes,'plan_sha256':plan['canonical_sha256'],
            'core_sha256':expression.digest(core),'controls_sha256':expression.digest(controls)}
