#!/usr/bin/env python3
"""Post-render diagnostics only; no new pack, prompt, profile activation or corpus edit."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'skills/photo-prompt-image-generator/scripts'))
import prompt_generator as pg

CASES = [
    ('sca_h05', 'Two side ponytails coil repeatedly and become thinner toward their ends.'),
    ('sca_x10', 'A separate silver ribbon winds around the coils of the dark hair.'),
    ('sca_g01', '몸통 옷과 팔소매 사이로 맨팔 구간이 드러나는 분리 소매.'),
    ('sca_g20', 'The neckline and sleeve hems carry narrow coral trim along their edges.'),
    ('hime_cut', '턱 부근에서 반듯하게 끝난 양옆 머리보다 뒷머리가 훨씬 길다.'),
    ('sca_x01', 'A curved hair band carries two triangular cloth ears above the head.'),
    ('sca_g08', 'A white gathered underskirt extends below the burgundy outer skirt and supports its volume.'),
    ('clt_ct055_v1', '옷 앞쪽 양편의 아일렛을 끈이 여러 번 X자로 통과하며 여민다.'),
    ('sca_h13', '머리 앞 가닥이 한 눈을 가리고 반대 눈은 드러난다.'),
    ('sca_h01', 'A single curved lock of hair rises from the crown.'),
    ('sca_g14', '구리 손 보호구가 팔뚝과 손목을 지나 손등까지 이어진다.'),
    ('y2kr_mesh', '실 가닥으로 된 그물 소매의 마름모 구멍 너머로 팔 피부가 보인다.'),
]


def main():
    assets = ROOT / 'skills/photo-prompt-image-generator/assets'
    data = pg.load_json(assets / 'photo_prompt_tags.json')
    index = pg.load_semantic_index_payload(assets / 'photo_prompt_semantic_index.json')
    pg.validate_semantic_index_metadata(index, data)
    bm25 = pg.semantic_bm25f_payload_from_index(index)
    rows = []
    for entry_id, query in CASES:
        expected = [f'slot:{slot}:{entry_id}' for slot, entries in data['slots'].items()
                    if any(entry['id'] == entry_id for entry in entries)]
        assert expected, entry_id
        ranked = pg.rank_bm25f(bm25, {'active_request': query}, limit=20)
        ranks = {row['document_id']: i for i, row in enumerate(ranked, 1)}
        positions = [ranks[key] for key in expected if key in ranks]
        rows.append({'entry_id': entry_id, 'query': query, 'expected_documents': expected,
                     'rank_in_top_20': min(positions) if positions else None,
                     'top_5': [row['document_id'] for row in ranked[:5]]})
    record = {'scope': 'post-render read-only BM25F candidate diagnostic',
              'candidate_pack_generated': False, 'corpus_changed': False,
              'profile_hard_activation_claimed': False, 'causal_render_improvement_claimed': False,
              'qualification_holdout_claimed': False,
              'limitation': 'Analyst-authored diagnostic after rendering; global lexical rank is not the integrated pack ranking, eligibility, slot allocation or adoption.',
              'semantic_index_manifest_sha256': hashlib.sha256((assets / 'photo_prompt_semantic_index.json').read_bytes()).hexdigest(),
              'top_5_target_count': sum(r['rank_in_top_20'] is not None and r['rank_in_top_20'] <= 5 for r in rows),
              'top_20_target_count': sum(r['rank_in_top_20'] is not None for r in rows),
              'cases': rows}
    (HERE / 'READ-ONLY-RETRIEVAL-DIAGNOSTIC.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in record.items() if k != 'cases'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
