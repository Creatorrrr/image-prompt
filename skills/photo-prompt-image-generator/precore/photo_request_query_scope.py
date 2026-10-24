"""Exact requester-text discovery scope; contains no scene examples or candidates."""
from __future__ import annotations
import hashlib
import json

VERSION = 'photo-request-query-scope/v1'
PURPOSES = frozenset({'visual', 'topic_reference', 'reference_use', 'workflow'})

def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()

def normalize(payload, request_text, active_spans, topic_context=None):
    if not isinstance(payload, dict) or set(payload) - {'contract_version', 'segments', 'canonical_sha256'}:
        raise ValueError('request query scope has unsupported fields')
    if payload.get('contract_version') != VERSION:
        raise ValueError('unsupported request query scope')
    rows = payload.get('segments')
    if not isinstance(rows, list) or not 1 <= len(rows) <= 64:
        raise ValueError('request query scope needs one to 64 reviewed segments')
    spans = {r['span_id']: r for r in active_spans}
    coverage = {key: set() for key in spans}
    links = (topic_context or {}).get('links', [])
    out = []
    for row in rows:
        if not isinstance(row, dict) or set(row) != {'active_span_id', 'start', 'end', 'text', 'purpose', 'reason'}:
            raise ValueError('request query segment fields are incomplete or unsupported')
        if not isinstance(row['active_span_id'], str):
            raise ValueError('request query segment needs an active span ID')
        span = spans.get(row['active_span_id'])
        start, end = row['start'], row['end']
        if (span is None or type(start) is not int or type(end) is not int
                or not span['start'] <= start < end <= span['end']
                or request_text[start:end] != row['text']):
            raise ValueError('request query segment is not exact active requester text')
        if (not isinstance(row['purpose'], str) or row['purpose'] not in PURPOSES
                or not isinstance(row['reason'], str) or not row['reason'].strip()):
            raise ValueError('request query segment needs a reviewed purpose')
        positions = set(range(start, end))
        if coverage[row['active_span_id']] & positions:
            raise ValueError('request query segments overlap')
        coverage[row['active_span_id']].update(positions)
        if row['purpose'] == 'topic_reference' and not any(
                link['active_span_id'] == row['active_span_id']
                and start <= link['request_quote']['start'] < link['request_quote']['end'] <= end
                for link in links):
            raise ValueError('topic reference segment has no exact reviewed antecedent')
        out.append(dict(row))
    for key, span in spans.items():
        if any(i not in coverage[key] and not request_text[i].isspace()
               for i in range(span['start'], span['end'])):
            raise ValueError('request query scope leaves active requester text unreviewed')
    result = {'contract_version': VERSION,
              'segments': sorted(out, key=lambda r: (r['start'], r['end']))}
    result['canonical_sha256'] = digest(result)
    if payload.get('canonical_sha256', result['canonical_sha256']) != result['canonical_sha256']:
        raise ValueError('request query scope canonical hash mismatch')
    return result

def retrieval_fields(scope, topic_context=None):
    """Workflow/reference transport is retained in the envelope, not discovery text."""
    fields = []
    links = (topic_context or {}).get('links', [])
    for row in scope['segments']:
        if row['purpose'] == 'visual':
            fields.append(('source_request_visual_scope', row['text']))
        elif row['purpose'] == 'topic_reference':
            fields.extend(('request_topic_context', link['topic_quote']['text'])
                          for link in links
                          if link['active_span_id'] == row['active_span_id']
                          and row['start'] <= link['request_quote']['start']
                          < link['request_quote']['end'] <= row['end'])
    return fields
