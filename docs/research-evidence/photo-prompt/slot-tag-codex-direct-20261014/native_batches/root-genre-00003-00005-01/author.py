"""Serialize the root's two individual genre judgements; no corpus inference.

Both complete sources, their historical rows, own bindings and final genre
specification were read by /root. All semantic values below are literal root
choices. Hash/locator extraction does not supply a new semantic judgement.
This writes research proofs and read notes only, never an operating source.
"""
from __future__ import annotations
import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
HERE = ROOT / 'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
sys.path[:0] = [str(HERE), str(ROOT / 'skills/photo-prompt-image-generator/scripts')]
import direct_review as dr
import native_reviews as reviews
import photo_semantic_evidence as native

OUT = Path(__file__).resolve().parent
PREPARED = HERE / 'native-inputs/prepared/root-genre-00003-00005-01'
assignment = reviews.read_json(PREPARED / 'ASSIGNMENT.json')
inp = reviews.artifact(ROOT, assignment['input'])
packet = reviews.read_json(PREPARED / 'PREPARED-PACKET.json')
catalog = reviews.read_json(HERE / 'CATALOG-FINAL-142-V2.json')
source_proposal = reviews.read_json(HERE / 'native-inputs/root-genre-00003-00005-plan/SOURCE-PROPOSAL.json')
proposals = {row['candidate_id']: row for row in source_proposal['records']}

# Literal decisions, including the whole source-unit dispositions and owners,
# were authored and reread by root before this serialization. This is neither
# a tag-to-fact converter nor an automatic approval loop over the data pool.
JUDGEMENTS = [
    ('cand_d0ea20c766a9599eaa25c91f363105fc', 3, 'fantasy', '판타지', 'fantasy',
     '장르 선택 fantasy/판타지를 이미지의 실제 style 효과로 심사했다. 판타지 생물·마법 사건·세계 법칙·시대·장소를 추가하지 않는다. stylized 태그는 긍정 사실로 사용하지 않는다.'),
    ('cand_d5529cc10da55534835653d5936f4f56', 4, 'fine art', '파인아트', 'fine_art',
     '장르 선택 fine art/파인아트를 이미지의 실제 style 효과로 심사했다. gallery 태그로 화랑 장소·전시 이력·인쇄 매체·특정 미술 운동을 생성하지 않는다.'),
]
rows = []
for cid, ordinal, english, korean, genre_value, rationale in JUDGEMENTS:
    before = packet['original_records'][cid]
    after = packet['current_records'][cid]
    assert after['content']['en'] == english and after['content']['ko'] == korean
    assert packet['references'][cid] == {} and packet['reference_bindings'][cid] == {}
    old = packet['historical_compiled_rows'][cid]
    loc = inp['original_decisions'][cid]
    facts = [
        {'id': 'en_genre', 'realization_id': 'base', 'pointer': '/content/en',
         'quote': english, 'dimension': 'style', 'target': 'image',
         'property': 'genre.selection', 'mode': 'effect',
         'value': {'type': 'photo.genre/v1', 'value': genre_value},
         'operation': 'set_value', 'receivers': [], 'requires': []},
        {'id': 'ko_genre', 'realization_id': 'base', 'pointer': '/content/ko',
         'quote': korean, 'dimension': 'style', 'target': 'image',
         'property': 'genre.selection', 'mode': 'effect',
         'value': {'type': 'photo.genre/v1', 'value': genre_value},
         'operation': 'set_value', 'receivers': [], 'requires': []},
    ]
    proof = {
        'schema': 'photo-candidate-role-evidence/v4',
        'meaning_sha256': native.meaning_sha256(after),
        'catalog_sha256': dr.c.digest(catalog), 'complete': True,
        'facts': facts,
        'roles': {'genre': {
            'spec_sha256': dr.c.digest(catalog['genre']), 'scope': 'whole_record',
            'realization_ids': ['base'], 'fact_refs': ['en_genre', 'ko_genre'],
            'support_modes': ['effect']}},
        'owner_maps': {'base': {'schema': 'photo-native-owner-bindings/v2',
            'bindings': [{'target': 'image', 'core_role': 'image',
                          'origin': 'existing', 'introduced_by': None}]}},
        'source_units': [
            {'realization_id': 'base', 'pointer': '/content/en', 'quote': english,
             'fact_refs': ['en_genre'], 'disposition': 'semantic'},
            {'realization_id': 'base', 'pointer': '/content/ko', 'quote': korean,
             'fact_refs': ['ko_genre'], 'disposition': 'semantic'},
        ],
        'effect_sets': {'base': {'dimensions': ['style'], 'properties': [
            {'dimension': 'style', 'target': 'image', 'property': 'genre.selection'}]}},
        'dependencies': {'base': []}, 'reference_sha256': {},
        'guard_sets': {'base': {'source_conditions': [{}, {}], 'member_conditions': {}}},
        'profile_contracts': {'base': None},
        'review': {
            'basis': rationale,
            'whole_source_reviewed': True,
            'source_correction': {
                'before_sha256': native.meaning_sha256(before),
                'after_sha256': native.meaning_sha256(after),
                'rationale': proposals[cid]['individual_reason']},
            'original_review': {
                'candidate_id': cid, 'source_record_sha256': old['source_record_sha256'],
                'catalog_sha256': old['catalog_sha256'], 'decision_sha256': loc['row_sha256'],
                'artifact': loc['file'] + '#item=' + str(loc['item'])},
            'native_review': {'reviewer': '/root', 'method': 'codex_direct_source_read',
                              'native_contract_sha256': ''},
        },
    }
    proof['review']['native_review']['native_contract_sha256'] = native.native_contract_sha256(proof)
    rows.append({
        'candidate_id': cid, 'ordinal': ordinal, 'status': 'approved',
        'rationale': rationale, 'source_before': before, 'source_after': after,
        'delta': proposals[cid]['delta'], 'original_compiled': loc, 'proof': proof,
        'dependency_records': {}, 'reference_bindings': {},
        'source_reread_complete': True, 'reference_reread_complete': True,
        'revision': None,
    })

assert [row['candidate_id'] for row in rows] == assignment['ids']
batch = {
    'schema': reviews.BATCH, 'task_name': '/root', 'model': 'gpt-6.1-sol',
    'reasoning_effort': 'high', 'assignment_sha256': dr.c.digest(assignment),
    'input_sha256': assignment['input']['sha256'],
    'prepared_count': 2, 'actual_read_count': 2, 'records': rows,
}
note = {
    'schema': reviews.NOTE, 'task_name': '/root', 'model': 'gpt-6.1-sol',
    'reasoning_effort': 'high', 'assignment_sha256': dr.c.digest(assignment),
    'input_sha256': assignment['input']['sha256'], 'batch_sha256': dr.c.digest(batch),
    'prepared_count': 2, 'actual_read_count': 2,
    'whole_source_read_ids': assignment['ids'],
    'whole_dependency_read_ids': assignment['ids'],
}
for name, value in [('BATCH.json', batch), ('NOTE.json', note)]:
    path = OUT / name
    if path.exists():
        raise ValueError('preserve immutable existing proof: ' + str(path))
    path.write_bytes(dr.c.canonical_bytes(value) + b'\n')
print(json.dumps({'prepared': 2, 'root_direct_whole_read': 2,
                  'research_proofs_written': 2, 'operating_mutations': 0,
                  'batch_sha256': dr.c.digest(batch), 'note_sha256': dr.c.digest(note)}))
