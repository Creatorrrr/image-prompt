"""Independent, source-grounded sparse/dense projections. No native authority."""
import copy
import hashlib
from collections import Counter

from photo_candidate_authoring import digest
from photo_candidate_review import validate
from photo_candidate_documents import tokens

RECIPE = 'photo-independent-candidate-lanes/v2'
ARMS = ('D1', 'D1b')


def project(original, old_fields, record, rid, *, arm, review=None, catalog=None):
    if arm not in ARMS or rid not in record['meaning']['primary']:
        raise ValueError('unknown lane recipe or actual RID')
    if record['meaning']['retrieval_class'] != 'positive':
        raise ValueError('only positive records enter candidate lanes')
    if Counter(tokens(original)) != Counter(t for values in old_fields.values() for text in values for t in tokens(text)):
        raise ValueError('baseline sparse source coverage differs from qualified D')
    source_sha = digest(record)
    sparse = copy.deepcopy(old_fields)
    additions = [];dense_additions = []
    seen = {text for values in sparse.values() for text in values}
    review_sha = None
    if review is not None:
        validate(review, record, catalog)
        if review['decision'] != 'enrich':
            raise ValueError('lane sidecars contain only accepted enrich records')
        review_sha = digest(review)
        value = review['realizations'][rid]
        proposals = [('core_meaning', value['summary_en'], 'summary', value['anchors'])]
        proposals += [('aliases', a['text'], 'alias', a['anchors']) for a in value['search_aliases']]
        for field, text, kind, anchors in proposals:
            if text in seen:
                continue
            sparse[field].append(text);seen.add(text)
            item = {'field':field,'text':text,'kind':kind,'review_sha256':review_sha,
                    'source_sha256':source_sha,'anchors':anchors}
            additions.append(item)
            if arm == 'D1b' and kind == 'summary':
                dense_additions.append(item)
    dense = original + (('\n'+'\n'.join(a['text'] for a in dense_additions)) if dense_additions else '')
    # Sparse owns its own token inventory; dense is not required to repeat aliases.
    expected = Counter(t for values in old_fields.values() for text in values for t in tokens(text))
    expected.update(t for a in additions for t in tokens(a['text']))
    if expected != Counter(t for values in sparse.values() for text in values for t in tokens(text)):
        raise ValueError('sparse token loss or duplicate ownership')
    return {'recipe':RECIPE,'arm':arm,'id':record['id']+'|'+rid,'cid':record['id'],'rid':rid,
            'source_sha256':source_sha,'review_sha256':review_sha,
            'baseline_text_sha256':hashlib.sha256(original.encode()).hexdigest(),
            'baseline_fields_sha256':digest(old_fields),'fields':sparse,'text':dense,
            'text_sha256':hashlib.sha256(dense.encode()).hexdigest(),
            'sparse_additions':additions,'dense_additions':dense_additions}


def verify(actual, original, old_fields, record, rid, *, arm, review=None, catalog=None):
    expected = project(original, old_fields, record, rid, arm=arm, review=review, catalog=catalog)
    if actual != expected:
        raise ValueError('lane projection differs from native parts and approved review')
    return True
