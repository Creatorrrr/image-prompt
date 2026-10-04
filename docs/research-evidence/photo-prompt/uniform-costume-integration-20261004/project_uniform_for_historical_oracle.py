"""Retain the older lexical oracle after verified additive uniform rows."""
from __future__ import annotations
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]

PROJECTION = '''        # Undo only the independently sealed uniform overlay before the
        # older Vocaloid/body projections. The historical oracle stays exact.
        uniform = ROOT / 'docs/research-evidence/photo-prompt/uniform-costume-integration-20261004'
        delta_path = uniform / 'authored-candidate-delta.json'
        self.assertEqual(common.sha(delta_path.read_bytes()),
                         '531c31e6602b378228bba0005cd4dcaf8703ddfd2d1de8f4d06034a4516a4cb1')
        delta = json.loads(delta_path.read_text())
        uniform_rows = {(item['slot'], item['id']): item for item in delta['rows']
                        if item['file'] == 'photo_prompt_tags.json' or item['file'] in filenames}
        seen_uniform = set()
        for slot, rows in historical_current['slots'].items():
            retained = []
            for row in rows:
                key = (slot, row['id'])
                change = uniform_rows.get(key)
                if change is None:
                    retained.append(row)
                    continue
                self.assertEqual(row, change['after'])
                self.assertEqual(change['before'] is None, change['new'])
                if not change['new']:
                    self.assertEqual({k: v for k, v in row.items()
                                      if k not in {'paraphrases', 'keywords', 'embedding_text'}},
                                     {k: v for k, v in change['before'].items()
                                      if k not in {'paraphrases', 'keywords', 'embedding_text'}})
                    retained.append(copy.deepcopy(change['before']))
                seen_uniform.add(key)
            rows[:] = retained
        self.assertEqual(seen_uniform, set(uniform_rows))
'''

def main():
    path = ROOT / 'tests/test_photo_liminal_active_use_korean_data_cleanup.py'
    before = path.read_text()
    marker = '        # Project only the declared later Vocaloid additions.'
    assert before.count(marker) == 1
    assert 'seen_uniform' not in before
    (HERE / 'test_photo_liminal_active_use_korean_data_cleanup.before-uniform.py').write_bytes(path.read_bytes())
    path.write_text(before.replace(marker, PROJECTION + marker))
    print('Added exact hash-bound reverse projection; all historical assertions unchanged.')

if __name__ == '__main__':
    main()
