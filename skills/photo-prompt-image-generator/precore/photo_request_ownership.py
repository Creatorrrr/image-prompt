"""Candidate-free review of requester anchors and atomic authorial detail."""
from __future__ import annotations
import hashlib
import re

VERSION = 'photo-requester-ownership-review/v1'

def contains(text, phrase):
    text, phrase = (' '.join(v.split()).casefold() for v in (text, phrase))
    return re.search(r'(?<!\w)' + re.escape(phrase) + r'(?!\w)', text) is not None

def validate(review, core, selection, envelope, required_evidence):
    if not isinstance(review, dict) or set(review) != {
            'contract_version', 'request_sha256', 'baseline_prompt_sha256',
            'anchors', 'authorial_details'}:
        raise ValueError('requester ownership review fields are incomplete or unsupported')
    baseline = core['baseline_prompt_en']
    if (review['contract_version'] != VERSION
            or review['request_sha256'] != envelope['request_sha256']
            or review['baseline_prompt_sha256'] != hashlib.sha256(baseline.encode()).hexdigest()):
        raise ValueError('requester ownership review input binding mismatch')
    anchors = {a['anchor_id']: a for a in core['intent_lock']['semantic_anchors']}
    rows = review['anchors']
    if not isinstance(rows, list) or len(rows) != len(anchors):
        raise ValueError('requester ownership review must cover every anchor exactly once')
    seen = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != {
                'anchor_id', 'source_text', 'prompt_evidence', 'requester_meaning', 'reason'}:
            raise ValueError('requester ownership anchor review fields are invalid')
        key = row['anchor_id']
        if key not in anchors or key in seen:
            raise ValueError('requester ownership review has missing or duplicate anchors')
        seen.add(key)
        if any(row[f] != anchors[key][f] for f in ('source_text', 'prompt_evidence')):
            raise ValueError('requester ownership review changed an anchor')
        if any(not isinstance(row[f], str) or not row[f].strip()
               for f in ('requester_meaning', 'reason')):
            raise ValueError('requester ownership anchor needs semantic review')
    authored = {r['category_id']: r for r in selection['selected']
                if r['basis'] == 'agent_visual_choice'}
    details = review['authorial_details']
    if not isinstance(details, list) or len(details) != len(authored):
        raise ValueError('ownership review must cover every authorial feature category')
    seen = set()
    for row in details:
        if not isinstance(row, dict) or set(row) != {'category_id', 'literals', 'reason'}:
            raise ValueError('authorial detail review fields are invalid')
        key = row['category_id']
        if key not in authored or key in seen:
            raise ValueError('authorial detail categories must be exact and distinct')
        seen.add(key)
        literals = row['literals']
        if (not isinstance(literals, list) or not 1 <= len(literals) <= 8
                or not isinstance(row['reason'], str) or not row['reason'].strip()):
            raise ValueError('authorial feature needs one to eight reviewed atomic literals')
        if any(not isinstance(v, str) for v in literals):
            raise ValueError('authorial detail literals must be text')
        if len(set(literals)) != len(literals):
            raise ValueError('duplicate authorial detail literal')
        for literal in literals:
            if (not isinstance(literal, str) or not literal.strip()
                    or not re.search(r'\w', literal)
                    or literal not in authored[key]['baseline_evidence']):
                raise ValueError('authorial detail must be an exact part of its feature evidence')
            for path, required in required_evidence:
                if contains(required, literal):
                    raise ValueError('authorial detail is locked by requester evidence: '
                                     + key + ' / ' + literal + ' / ' + path)
    return {'valid': True, 'contract_version': VERSION,
            'reviewed_anchor_count': len(anchors), 'reviewed_authorial_categories': len(authored),
            'limit': 'Exact atomic overlap and complete review binding; natural-language ownership still needs semantic judgment.'}
