"""Pilot compiler preserving D and cues; F2 weights and search stay unchanged.

B adds already-authored primary visual manifestations. C additionally appends
an explicitly accepted source-grounded review. No native record is modified.
"""
from collections import Counter
import copy
import hashlib
import re
from photo_candidate_authoring import digest
from photo_candidate_review import validate

RECIPE = 'photo-grounded-source-review-document/v1'


def tokens(value):
    return re.findall(r'[^\W_]+', value.casefold(), re.UNICODE)


def project(original, old_fields, record, rid, source_document, *, arm, selected=False,
            review=None, catalog=None):
    if arm not in {'A', 'B', 'C'}:
        raise ValueError('unknown document arm')
    fields = copy.deepcopy(old_fields)
    additions = []
    seen = {value for values in fields.values() for value in values}

    def add(field, value, origin):
        if value not in seen:
            fields[field].append(value)
            additions.append({'field': field, 'text': value, 'origin': origin})
            seen.add(value)

    if selected and arm in {'B', 'C'}:
        positive = {record['meaning']['literals'][uid] for uid in record['meaning']['primary'][rid].values()}
        for part in source_document['parts']:
            if part['text'] in positive and any(s['role'] == 'source_manifestations' for s in part['sources']):
                add('core_meaning', part['text'], 'existing_primary_manifestation')
    if selected and arm == 'C' and review is not None:
        validate(review, record, catalog)
        if review['decision'] == 'enrich':
            realization = review['realizations'][rid]
            add('core_meaning', realization['summary_en'], 'reviewed_summary')
            for alias in realization['search_aliases']:
                add('aliases', alias['text'], 'reviewed_source_alias')
    text = original + (('\n'+'\n'.join(v['text'] for v in additions)) if additions else '')
    if Counter(tokens(text)) != Counter(t for values in fields.values() for v in values for t in tokens(v)):
        raise ValueError('field token loss or duplicate ownership')
    return {'recipe': RECIPE, 'text': text, 'text_sha256': hashlib.sha256(text.encode()).hexdigest(),
            'fields': fields, 'additions': additions, 'source_sha256': digest(record), 'rid': rid}


def field_index(documents, configs):
    """Full-corpus statistics; no selected-subset length/DF normalization."""
    lengths = {f: [] for f in configs}
    counts = {f: 0 for f in configs}
    postings = {}
    for i, document in enumerate(documents):
        if set(document['fields']) != set(configs):
            raise ValueError('field scope mismatch')
        terms = {}
        for field in configs:
            bag = Counter(t for value in document['fields'][field] for t in tokens(value))
            length = sum(bag.values());lengths[field].append(length);counts[field] += bool(length)
            for term, tf in bag.items():
                terms.setdefault(term, {})[field] = tf
        for term, fields in terms.items():
            postings.setdefault(term, []).append([i, fields])
    n = len(documents)
    if not n:
        raise ValueError('empty document corpus')
    average = {}
    for field, config in configs.items():
        denominator = counts[field] if config.get('normalization_population') == 'nonempty_documents' else n
        average[field] = sum(lengths[field])/denominator if denominator else 0.
    return {'n': n, 'fields': configs, 'postings': postings, 'lengths': lengths,
            'nonempty_counts': counts, 'average_lengths': average}
