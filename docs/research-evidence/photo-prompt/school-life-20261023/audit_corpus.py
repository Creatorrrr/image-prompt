"""Read-only, one-shot corpus evidence. Refuses to overwrite the saved snapshot."""
import collections
import hashlib
import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parents[3]
ASSETS = REPO / 'skills/photo-prompt-image-generator/assets'
OUT = ROOT / 'corpus-snapshot.json'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def primary_fields(value, path='content'):
    """Search positive en/ko/phrase fields, not aliases, examples, or research notes."""
    found = []
    if isinstance(value, dict):
        for k, v in value.items():
            p = path + '/' + k
            if k in {'en', 'ko', 'phrase_en', 'phrase_ko'} and isinstance(v, str):
                found.append((p, v))
            elif k in {'realizations', 'branches', 'selected', 'options'}:
                found.extend(primary_fields(v, p))
    elif isinstance(value, list):
        for i, v in enumerate(value):
            found.extend(primary_fields(v, path + '/' + str(i)))
    return found

def main():
    if OUT.exists():
        raise SystemExit('Snapshot already exists. Use a separate stage directory after integration.')
    manifest_bytes = (ASSETS / 'photo_candidate_corpus_manifest.json').read_bytes()
    manifest = json.loads(manifest_bytes)
    modules, candidates, bindings = {}, {}, []
    for m in manifest['modules']:
        raw = (ASSETS / m['file']).read_bytes()
        d = json.loads(raw)
        modules[m['file']] = sha(raw)
        if m['kind'] == 'candidates':
            for cid, record in d['candidates'].items():
                if cid in candidates:
                    raise AssertionError('Duplicate CID ' + cid)
                candidates[cid] = {'module': m['file'], 'record': record}
        if m['kind'] == 'slot_bindings':
            bindings.extend(d['slot_bindings'].values())
    patterns = {
        'school': r'\bschool\b|학교|학원물',
        'classroom': r'\bclassroom\b|교실',
        'uniform': r'\bgakuran\b|\bsailor\b|school.uniform|교복|세일러복',
        'boarding': r'\bboarding.school\b|\bdormitor\w*\b|기숙',
        'council': r'\bstudent.council\b|학생회',
        'cultural_festival': r'\bbunkasai\b|\bschool.festival\b|문화제',
        'school_club': r'\bschool.club\b|\bclubroom\b|동아리',
        'exam': r'\bexam(?:ination|s)?\b|\bentrance.test\b|입시|수능|모의고사',
        'prom': r'\bprom\b|\bhomecoming\b|홈커밍',
        'bullying': r'\bbullying\b|\bhazing\b|이지메|왕따',
        'dark_academia': r'\bdark.academia\b|다크 아카데미아',
        'gyaru': r'\bgyaru\b|갸루',
    }
    lexical = {}
    for label, pattern in patterns.items():
        matches = []
        for cid, row in candidates.items():
            fields = [(p, t) for p, t in primary_fields(row['record']['content'])
                      if re.search(pattern, t, re.I)]
            if fields:
                matches.append({'candidate_id': cid, 'module': row['module'], 'fields': fields})
        lexical[label] = {'count': len(matches), 'matches': matches}
    decisions = [
        ('cand_564ee719d63f5899909f03532490e2b1', 'separate_context', ['C03','W01','W02','W03'], '성인 교복 코스프레 인물. 실제 학생이나 일반 교복 구조 후보로 재분류하지 않는다. adult 명칭과 실제 조건의 일치도 추후 native 심사한다.'),
        ('cand_0df22ad2652f5d239338e75226f22c52', 'reuse_review', ['W01','W02','W03'], '교복 체계 일반 문맥은 재사용 검토. 특정 칼라/입깃/레이어 전체가 기존 원문에 있다는 뜻은 아니다. attire_context의 contextual binding 유지.'),
        ('cand_ac61ab4384135edbb8a909b1ec0c8dbe', 'reuse_review', ['S01'], '일반 교실 위치의 기존 선택지. 앞 칠판·책상·통로 구조는 원문에 없으므로 새 의무로 간주하지 않는다.'),
        ('cand_98a65f70c792575ea2f5f0c767ca52b9', 'refine_review', ['S01','C02'], '2000년대 한국이라는 고증 주장이 있으나 물리 성분이 없다. 시대 실물 자료 보강 전 범용 교실의 증거로 사용하지 않는다.'),
        ('cand_455838fef14a5caba8aa45911dc42aae', 'reuse_review', ['S10','C01'], '오크 서가 도서관을 선택한 경우 재사용 검토. 학교 장르에 자동 부여하지 않는다.'),
        ('cand_c65e606e900d508aac906a5b71291cb2', 'separate_context', ['C04'], '성인 갸루 실천·styling 문맥. 학생/불량/성적 행동으로 확대하지 않으며 requires_primary_any_tags를 유지한다.'),
        ('cand_ed0409b561f759cfaa90fd00877e4889', 'refine_review', ['A04','A14'], '책·행·주석·시선·양손의 완전 관계와 effects 유지. 원문의 구체 관계보다 짧은 한글 label을 전체 의미로 오인하지 않는다. 새로운 공동학습과는 별개.'),
        ('cand_17e89ecffe7e5634b84e66e15af751f4', 'reuse_review', ['W03'], '교복 부품 일관성을 점검하는 동작. 착용 의복 자체를 공급하는 후보와 구별.'),
        ('cand_a853ef841c6c5b6c86e6f6b9f5f58ae4', 'reuse_review', ['S01','A14'], '교실 천장 형광등이라는 광원. 2000년대 고증·학교급·번아웃 의미는 없다.'),
        ('cand_58771df5cae55656b194e4946a19e36d', 'reuse_review', ['C03','W08'], '한쪽 어깨 검은 백팩은 소품·접촉 원문으로만 재사용. 학생 신원과 등교 목적을 입증하지 않는다.'),
    ]
    existing = []
    for cid, decision, cards, reason in decisions:
        row = candidates[cid]
        bs = [b for b in bindings if b['candidate_id'] == cid]
        existing.append({'candidate_id': cid, 'decision_proposal': decision, 'card_ids': cards,
                         'reason': reason, 'module': row['module'], 'source_record': row['record'],
                         'record_sha256': sha(json.dumps(row['record'], sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()),
                         'bindings': bs, 'native_approval': False})
    index_raw = (ASSETS / 'photo_candidate_search.json').read_bytes()
    index = json.loads(index_raw)
    catalog = json.loads((ASSETS / 'photo_candidate_slot_catalog.json').read_text())
    stable = (ASSETS / 'photo_candidate_corpus_manifest.json').read_bytes() == manifest_bytes
    drift = [n for n,h in modules.items() if sha((ASSETS/n).read_bytes()) != h]
    report = {
        'schema': 'school-life-corpus-research/v1', 'head': subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),
        'manifest_sha256': sha(manifest_bytes), 'module_sha256': modules,
        'counts': {'modules':len(modules),'candidates':len(candidates),'slot_bindings':len(bindings),'catalog_slots':len(catalog['slot_catalog'])},
        'catalog_slots': sorted(catalog['slot_catalog']), 'lexical_field_policy': 'Positive en/ko/phrase fields only; no alias/metadata/example claim of absence.',
        'lexical_scan': lexical, 'existing_source_triage': existing,
        'index_observation': {'sha256':sha(index_raw),'schema':index.get('schema'),'layout_id':index.get('layout_id'),'space':index.get('space'),'metadata_count':index.get('metadata',{}).get('count'), 'corpus_sha256':index.get('corpus_sha256')},
        'read_consistency': {'manifest_stable':stable,'changed_modules':drift},
        'not_run': ['native qualification','source validation','retrieval','embedding','index verification','image generation','pixel review','commit','push'],
    }
    OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'counts':report['counts'],'lexical':{k:v['count'] for k,v in lexical.items()},'stable':stable and not drift},ensure_ascii=False))

if __name__ == '__main__':
    main()
