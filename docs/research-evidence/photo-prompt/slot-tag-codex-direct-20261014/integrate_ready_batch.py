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
from review_state import ACCEPTED, PENDING, correction_counts, coverage


def git(*args):
    return subprocess.check_output(['git', *args], cwd=review.ROOT).decode().strip()


def write_current():
    progress = json.loads((review.HERE / 'PROGRESS.json').read_text())
    rows = []
    for path in sorted((review.HERE / 'decisions').glob('*.json')):
        rows.extend(json.loads(path.read_text())['decisions'])
    order = json.loads((review.HERE / 'ORDER.json').read_text())
    state = coverage(order, rows)
    accepted = list(state['accepted'].values())
    if (len(accepted) != progress['direct_approved_records']
            or len(state['pending']) != progress['pending_decisions']
            or state['unreviewed_source_records'] != progress['unreviewed_records']):
        raise ValueError('current report differs from verified source judgement counts')
    methods = Counter(row['review_method'] for row in accepted)
    kinds = Counter(row['recommended_kind'] for row in accepted)
    roles = Counter(role['slot_id'] for row in accepted for role in row['roles'])
    changes = correction_counts(accepted)
    report = {
        'schema': 'photo-codex-current-source-review/v1',
        'registered_decisions': len(accepted), 'total_records': len(order),
        'registered_source_judgements': len(rows),
        'accepted_source_judgements': len(accepted),
        'review_methods': dict(methods), 'recommended_kinds': dict(kinds),
        'role_proposals': sum(roles.values()), 'role_distribution': dict(sorted(roles.items())),
        'records_with_text_corrections': changes['text_records'],
        'text_field_corrections': changes['text_fields'],
        'records_with_structured_corrections': changes['structured_records'],
        'structured_source_value_corrections': changes['structured_values'],
        'unreviewed_records': progress['unreviewed_records'],
        'pending_decisions': progress['pending_decisions'],
        'first_unreviewed_order_offset': state['first_unreviewed_order_offset'],
        'first_unfinished_order_offset': state['first_unfinished_order_offset'],
        'native_changes_applied': False, 'native_qualification_complete': False,
        'stage05_complete': False, 'stages06_08_complete': False,
        'gemini_calls_in_this_run': 0, 'local_embedding_inferences_in_this_run': 0,
        'root_personally_read_all_worker_sources_claimed': False,
        'independent_human_or_pixel_verification': False,
    }
    review.write(review.HERE / 'CURRENT.json', report)
    text = f'''# 직접 검토 최신 등록 현황

현재 승인·원문 결합 검증을 통과한 판정은 **{len(accepted):,}/{len(order):,}개**다. 보류를 포함해 등록한 직접 원문 판정은 {len(rows):,}개다. 주 에이전트 직접 승인 판정 {methods['codex_direct_source_read']:,}개와 명시 승인된 gpt-6.1-sol/high 서브에이전트 직접 승인 판정 {methods['codex_subagent_direct_source_read']:,}개를 구분한다. 주 에이전트가 worker의 모든 원문을 직접 읽었다고 주장하지 않는다.

승인 판정의 역할 제안 {sum(roles.values()):,}개, 텍스트 보정 제안 {report['records_with_text_corrections']:,}개 후보/{report['text_field_corrections']:,}개 필드, 명시적 구조 보정 제안 {changes['structured_records']:,}개 후보/{changes['structured_values']:,}개 값이다. 이는 native 채택 수나 의미 정확도 점수가 아니다. 미검토 {progress['unreviewed_records']:,}개·미해결 판정 {progress['pending_decisions']:,}개이며, 작업 순서의 첫 미검토 위치는 {report['first_unreviewed_order_offset']:,}번, 보류를 포함한 첫 미완료 위치는 {report['first_unfinished_order_offset']:,}번이다. 병렬로 끝난 뒤쪽 범위를 앞쪽 미검토 완료로 합산하지 않는다. 보류가 있는 배치는 체크포인트이며 완료 배치가 아니다.

원문·참조·catalog·긍정 인용·소유자/속성 계약·실현 분기·작성 항목 및 worker task/model/effort·배정 범위·note hash를 기계 검증했다. 기계 검사는 실제 의미 정확도나 독립 사람/전문가/이미지 픽셀 검증을 대신하지 않는다. 직접 의미 판정과 혼동 경계는 각 authored 판정·worker note에 남아 있다. 같은 모델 계열의 분업 결과를 독립 평가로 표시하지 않는다.

**5B 전수 검토·5C native 자격화와 역검색·6~8단계는 미완료다.** 운영 본문·종류·태그·기존 binding·로컬 index/space는 아직 바꾸지 않았다. 최종 적용 전에는 조건·소유자·실현/번역 일치·참조를 별도로 해결하고 검증한다. Gemini 신규 호출과 이번 실행의 로컬 임베딩 추론은 0건이다.

단계·배치별 상세 기록은 [REPORT.ko.md](REPORT.ko.md), 최신 수치의 기계 대장은 [CURRENT.json](CURRENT.json), source-bound 원문 판정은 `decisions/`를 참고한다. 단계 완료를 표시하지 않은 중간 커밋이다.
'''
    (review.HERE / 'CURRENT.ko.md').write_text(text)
    return report


def validate_selected_batch(note, authored, order, *, source_read_checkpoint=False):
    start, stop = note['start'], note['stop']
    rows = authored['decisions']
    if (not 0 <= start < stop <= len(order) or len(rows) != stop - start
            or len({row['candidate_id'] for row in rows}) != len(rows)
            or {row['candidate_id'] for row in rows} != set(order[start:stop])
            or any(row['status'] not in ACCEPTED | PENDING for row in rows)):
        raise ValueError('selected batch must cover its exact canonical range')
    ordinal_by_id = {cid: n for n, cid in enumerate(order)}
    pending = sorted(ordinal_by_id[row['candidate_id']] for row in rows
                     if row['status'] not in ACCEPTED)
    if sorted(note['unresolved_ordinals']) != pending:
        raise ValueError('worker pending attestation differs from explicit judgements')
    if pending and source_read_checkpoint is not True:
        raise ValueError('unresolved source review requires an explicit checkpoint')
    return pending


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
    pending_ordinals = validate_selected_batch(note, authored, order,
        source_read_checkpoint=job.get('source_read_checkpoint', False))
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
    if pending_ordinals:
        checkpoint = {'schema': 'photo-codex-source-review-checkpoint/v1',
            'range': [start, stop], 'complete_source_read': True,
            'direct_source_judgements': stop - start,
            'accepted_source_judgements': stop - start - len(pending_ordinals),
            'pending_ordinals': pending_ordinals,
            'pending_judgements': [row for row in authored['decisions'] if row['status'] not in ACCEPTED],
            'batch_approval_complete': False, 'native_changes_applied': False,
            'stage05_complete': False, 'cumulative_verified_progress': result}
        checkpoint_path = review.HERE / f'CHECKPOINT-{stem}.json'
        review.write(checkpoint_path, checkpoint)
        batch_paths = [checkpoint_path]
        batch_roles = sum(len(row['roles']) for row in authored['decisions'] if row['status'] in ACCEPTED)
    else:
        summary = summarize(start, stop, result['direct_approved_records'], allow_sparse=True)
        batch_paths = [review.HERE / f'BATCH-{stem}-SUMMARY.json',
            review.HERE / f'BATCH-{stem}-CHANGE-PROPOSALS.json',
            review.HERE / f'STAGE05B-{stem}-VERIFICATION.json']
        batch_roles = summary['role_proposals']
    current = write_current()
    acceptance = {'schema': 'photo-codex-root-integration/v1', **job,
        'start': start, 'stop': stop, 'worker_task': note['task_name'],
        'root_acceptance_scope': 'Source-bound integration of worker-authored semantic judgements.',
        'root_all_source_read_claimed': False, 'registered_count': result['direct_approved_records'],
        'stage05_complete': False, 'batch_pending_ordinals': pending_ordinals,
        'batch_approval_complete': not pending_ordinals}
    acceptance_path = review.HERE / 'root-integrations' / f'{stem}.json'
    review.write(acceptance_path, acceptance)
    paths = [note_path, authored_path, *packets, *supporting,
        review.HERE / 'decisions' / authored_path.name, acceptance_path,
        review.HERE / f'DELEGATED-{stem}-REGISTER.json',
        *batch_paths,
        review.HERE / 'PROGRESS.json', review.HERE / 'CURRENT.json', review.HERE / 'CURRENT.ko.md']
    paths.extend(review.ROOT / path for path in job.get('extra_files', []))
    relative = [str(path.relative_to(review.ROOT)) for path in paths]
    subprocess.run(['git', 'add', '--', *relative], cwd=review.ROOT, check=True)
    staged = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only', '-z'],
                                        cwd=review.ROOT).decode().strip('\0').split('\0'))
    if staged != set(relative):
        raise ValueError('staged paths differ from the explicitly selected review batch')
    subprocess.run(['git', 'diff', '--cached', '--check'], cwd=review.ROOT, check=True)
    action = 'checkpoint' if pending_ordinals else 'integrate'
    subprocess.run(['git', 'commit', '-m', f'feat(photo): {action} direct review {start} through {stop - 1}'],
                   cwd=review.ROOT, check=True)
    print(json.dumps({'commit': git('rev-parse', 'HEAD'), 'range': [start, stop],
        'registered': current['registered_decisions'], 'roles_in_batch': batch_roles,
        'batch_approval_complete': not pending_ordinals,
        'stage05_complete': False}), flush=True)


if __name__ == '__main__':
    jobs = json.loads(Path(sys.argv[1]).read_text())
    for job in jobs:
        integrate(job)
