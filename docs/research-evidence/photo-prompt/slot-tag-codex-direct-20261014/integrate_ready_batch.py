"""Integrate an explicitly selected final-ready worker batch, then commit it.

This is mechanical bookkeeping, never semantic classification or approval.
Only root runs it after the worker reports the concrete authored batch ready.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import direct_review as review
from summarize_batch import summarize


def git(*args):
    return subprocess.check_output(['git', *args], cwd=review.ROOT).decode().strip()


def write_current():
    progress = json.loads((review.HERE / 'PROGRESS.json').read_text())
    rows = []
    for path in sorted((review.HERE / 'decisions').glob('*.json')):
        rows.extend(json.loads(path.read_text())['decisions'])
    methods = Counter(row['review_method'] for row in rows)
    kinds = Counter(row['recommended_kind'] for row in rows)
    roles = Counter(role['slot_id'] for row in rows for role in row['roles'])
    reviewed = {row['candidate_id'] for row in rows}
    order = json.loads((review.HERE / 'ORDER.json').read_text())
    missing = [n for n, cid in enumerate(order) if cid not in reviewed]
    report = {
        'schema': 'photo-codex-current-source-review/v1',
        'registered_decisions': len(rows), 'total_records': len(order),
        'review_methods': dict(methods), 'recommended_kinds': dict(kinds),
        'role_proposals': sum(roles.values()), 'role_distribution': dict(sorted(roles.items())),
        'records_with_text_corrections': sum(bool(row['corrections']) for row in rows),
        'text_field_corrections': sum(len(row['corrections']) for row in rows),
        'unreviewed_records': progress['unreviewed_records'],
        'pending_decisions': progress['pending_decisions'],
        'first_unreviewed_order_offset': missing[0] if missing else len(order),
        'native_changes_applied': False, 'native_qualification_complete': False,
        'stage05_complete': False, 'stages06_08_complete': False,
        'gemini_calls_in_this_run': 0, 'local_embedding_inferences_in_this_run': 0,
        'root_personally_read_all_worker_sources_claimed': False,
        'independent_human_or_pixel_verification': False,
    }
    review.write(review.HERE / 'CURRENT.json', report)
    text = f'''# 직접 검토 최신 등록 현황

현재 등록·원문 결합 검증을 통과한 판정은 **{len(rows):,}/{len(order):,}개**다. 주 에이전트 직접 판정 {methods['codex_direct_source_read']:,}개와 명시 승인된 gpt-6.1-sol/high 서브에이전트 직접 판정 {methods['codex_subagent_direct_source_read']:,}개를 구분한다. 주 에이전트가 worker의 모든 원문을 직접 읽었다고 주장하지 않는다.

역할 제안 {sum(roles.values()):,}개, 텍스트 보정 제안 {report['records_with_text_corrections']:,}개 후보/{report['text_field_corrections']:,}개 필드다. 이는 native 채택 수나 의미 정확도 점수가 아니다. 미검토 {progress['unreviewed_records']:,}개·미해결 판정 {progress['pending_decisions']:,}개이며, 작업 순서의 첫 미검토 위치는 {report['first_unreviewed_order_offset']:,}번이다. 병렬로 끝난 뒤쪽 범위를 앞쪽 미검토 완료로 합산하지 않는다.

원문·참조·catalog·긍정 인용·소유자/속성 계약·실현 분기·작성 항목 및 worker task/model/effort·배정 범위·note hash를 기계 검증했다. 기계 검사는 실제 의미 정확도나 독립 사람/전문가/이미지 픽셀 검증을 대신하지 않는다. 직접 의미 판정과 혼동 경계는 각 authored 판정·worker note에 남아 있다. 같은 모델 계열의 분업 결과를 독립 평가로 표시하지 않는다.

**5B 전수 검토·5C native 자격화와 역검색·6~8단계는 미완료다.** 운영 본문·종류·태그·기존 binding·로컬 index/space는 아직 바꾸지 않았다. 최종 적용 전에는 조건·소유자·실현/번역 일치·참조를 별도로 해결하고 검증한다. Gemini 신규 호출과 이번 실행의 로컬 임베딩 추론은 0건이다.

단계·배치별 상세 기록은 [REPORT.ko.md](REPORT.ko.md), 최신 수치의 기계 대장은 [CURRENT.json](CURRENT.json), source-bound 원문 판정은 `decisions/`를 참고한다. 단계 완료를 표시하지 않은 중간 커밋이다.
'''
    (review.HERE / 'CURRENT.ko.md').write_text(text)
    return report


def integrate(job):
    if git('diff', '--cached', '--name-only'):
        raise ValueError('the staging area is not empty')
    note_path = review.run_path(job['note'], 'worker-notes')
    authored_path = review.run_path(job['authored'], 'authored')
    for path, key in [(note_path, 'note_sha256'), (authored_path, 'authored_sha256')]:
        if hashlib.sha256(path.read_bytes()).hexdigest() != job[key]:
            raise ValueError('final-ready file changed after root selected it')
    supporting = []
    for item in job.get('supporting_files', []):
        path = review.run_path(item['file'], 'authored')
        if hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
            raise ValueError('declared authoring source changed after root selected it')
        supporting.append(path)
    note = json.loads(note_path.read_text())
    start, stop = note['start'], note['stop']
    authored = json.loads(authored_path.read_text())
    order = json.loads((review.HERE / 'ORDER.json').read_text())
    if (len(authored['decisions']) != stop - start
            or {row['candidate_id'] for row in authored['decisions']} != set(order[start:stop])
            or note['unresolved_ordinals']
            or any(row['status'] not in {'approved', 'diagnostic_reviewed'} for row in authored['decisions'])):
        raise ValueError('the explicitly selected management batch is not complete')
    packets = [review.run_path(value, 'packets') for value in note['packet_paths']]
    declared_json = [review.run_path(value, 'authored') for value in note['authored_paths']
                     if value.endswith('.json')]
    if len(packets) != 1 or declared_json != [authored_path]:
        raise ValueError('this integration command requires one complete management packet/document')
    stem = f'{start:05d}-{stop:05d}'
    if (review.HERE / 'decisions' / authored_path.name).exists():
        raise ValueError('already registered; never silently revise an existing batch')
    result = review.register(packets[0], authored_path, note_path)
    review.write(review.HERE / f'DELEGATED-{stem}-REGISTER.json', result)
    summary = summarize(start, stop, result['direct_approved_records'], allow_sparse=True)
    current = write_current()
    acceptance = {'schema': 'photo-codex-root-integration/v1', **job,
        'start': start, 'stop': stop, 'worker_task': note['task_name'],
        'root_acceptance_scope': 'Source-bound integration of worker-authored semantic judgements.',
        'root_all_source_read_claimed': False, 'registered_count': result['direct_approved_records'],
        'stage05_complete': False}
    acceptance_path = review.HERE / 'root-integrations' / f'{stem}.json'
    review.write(acceptance_path, acceptance)
    paths = [note_path, authored_path, *packets, *supporting,
        review.HERE / 'decisions' / authored_path.name, acceptance_path,
        review.HERE / f'DELEGATED-{stem}-REGISTER.json',
        review.HERE / f'BATCH-{stem}-SUMMARY.json',
        review.HERE / f'BATCH-{stem}-CHANGE-PROPOSALS.json',
        review.HERE / f'STAGE05B-{stem}-VERIFICATION.json',
        review.HERE / 'PROGRESS.json', review.HERE / 'CURRENT.json', review.HERE / 'CURRENT.ko.md']
    paths.extend(review.ROOT / path for path in job.get('extra_files', []))
    relative = [str(path.relative_to(review.ROOT)) for path in paths]
    subprocess.run(['git', 'add', '--', *relative], cwd=review.ROOT, check=True)
    staged = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only', '-z'],
                                        cwd=review.ROOT).decode().strip('\0').split('\0'))
    if staged != set(relative):
        raise ValueError('staged paths differ from the explicitly selected review batch')
    subprocess.run(['git', 'diff', '--cached', '--check'], cwd=review.ROOT, check=True)
    subprocess.run(['git', 'commit', '-m', f'feat(photo): integrate direct review {start} through {stop - 1}'],
                   cwd=review.ROOT, check=True)
    print(json.dumps({'commit': git('rev-parse', 'HEAD'), 'range': [start, stop],
        'registered': current['registered_decisions'], 'roles_in_batch': summary['role_proposals'],
        'stage05_complete': False}), flush=True)


if __name__ == '__main__':
    jobs = json.loads(Path(sys.argv[1]).read_text())
    for job in jobs:
        integrate(job)
