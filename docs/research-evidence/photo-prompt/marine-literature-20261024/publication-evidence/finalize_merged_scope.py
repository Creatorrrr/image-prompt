"""Qualify and explicitly stage the final source/index after upstream merges."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess

ROOT = Path.cwd()
Q = Path('docs/research-evidence/photo-prompt/marine-literature-20261024')
P = Q / 'publication-evidence'
S = Path('skills/photo-prompt-image-generator')
A = S / 'assets'


def git(*args, **kwargs):
    return subprocess.check_output(['git', *args], **kwargs)


def read(path):
    return json.loads(path.read_bytes())


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


parent = git('rev-parse', 'origin/main', text=True).strip()
manifest = read(A / 'photo_candidate_corpus_manifest.json')
upstream = json.loads(git('show', parent + ':' + str(A / 'photo_candidate_corpus_manifest.json')))
assert manifest['modules'][:len(upstream['modules'])] == upstream['modules']
assert len(manifest['modules']) == len(upstream['modules']) + 2
paths = [str(A / row['file']) for row in upstream['modules']]
expected = {}
for row in git('ls-tree', '-r', '-z', parent, '--', *paths).split(b'\0'):
    if row:
        meta, name = row.split(b'\t', 1)
        expected[name.decode()] = meta.decode().split()[2]
actual = git('hash-object', '--stdin-paths', input='\n'.join(paths) + '\n', text=True).splitlines()
assert len(actual) == len(paths)
assert all(blob == expected[name] for name, blob in zip(paths, actual))
assert git('diff', parent, '--', str(S / 'scripts'), str(S / 'precore')) == b''
write(P / 'merged-parent-source-preservation.json', {
    'status': 'pass', 'parent': parent, 'remote_modules_exact': len(paths),
    'blob_ids': dict(zip(paths, actual)), 'final_module_count': len(manifest['modules']),
    'upstream_scripts_and_precore_byte_preserved': True,
})

for name, digest in read(P / 'source-scope.json')['copied_files'].items():
    assert sha(Path(name)) == digest, name
report = read(Path('generated/marine-publication-cache/BUILD-REPORT.json'))
descriptor = read(A / 'photo_candidate_search.json')
assert report['layout_id'] == descriptor['layout_id'] and report['verification']['verified']
shutil.copyfile('generated/marine-publication-cache/BUILD-REPORT.json', P / 'index-build.json')
validation = read(P / 'dictionary-validation.json')
assert not validation['errors']
test_counts = {}
for name in ['semantic-tests.log', 'topic-sealed-tests.log', 'query-ownership-sealed-tests.log']:
    text = (P / name).read_text()
    assert text.rstrip().endswith('OK'), name
    test_counts[name] = int(re.findall(r'Ran (\d+) tests?', text)[-1])
assert test_counts['topic-sealed-tests.log'] == 3 and test_counts['query-ownership-sealed-tests.log'] == 10
assert (S / 'tests/test_topic_title_discovery_scope.py').read_bytes() == (P / 'runtime-dependent-regression/test_topic_title_discovery_scope.py').read_bytes()

retired = []
for old_report in P.glob('before-*.index-build.json'):
    old = read(old_report)['layout_id']
    if old == report['layout_id']:
        continue
    files = list(filter(None, git('ls-files', '-z', '--', str(A / 'photo_candidate_search_shards' / old)).decode().split('\0')))
    for offset in range(0, len(files), 128):
        subprocess.run(['git', 'rm', '-q', '--', *files[offset:offset + 128]], check=True)
    retired.append({'layout': old, 'removed_current_tree_members': len(files)})
write(P / 'retired-intermediate-layouts.json', {'status': 'pass', 'task_owned_layouts': retired,
                                               'unrelated_layouts_removed': 0, 'history_preserved': True})

members = {}


def walk(value):
    if isinstance(value, dict):
        if 'path' in value and 'sha256' in value:
            members[value['path']] = value['sha256']
        for child in value.values():
            walk(child)
    elif isinstance(value, list):
        for child in value:
            walk(child)


walk(descriptor)
assert all(sha(A / name) == digest for name, digest in members.items())
write(P / 'publication-qualification.json', {
    'status': 'pass', 'layout_id': report['layout_id'], 'full_dictionary': validation,
    'positive_records': report['records'], 'verified_active_derived_members': len(members),
    'latest_remote_parent': parent, 'latest_remote_modules_exact': len(paths),
    'test_counts': test_counts, 'source_semantic_tests': test_counts['semantic-tests.log'],
    'sealed_query_tests': 13, 'sealed_test_native_generation': '047b1e251359abd3bde2f8b089a5aefa72a08c49e1ea1393a0272a40f3bc9492',
    'new_positive_records': 87, 'new_diagnostics_excluded': 247,
    'runtime_config_changed_by_this_task': False, 'native_pixel_approval_changed': False,
    'source_tree_probe_limit': 'Raw H-F2 facades need generated modules absent from the working source. Two direct-source probes failed import and are retained as unsupported probes; query tests were run against the exact sealed image-test kernel instead.',
})
(P / 'PUBLISHING.md').write_text(f'''# 해병문학 데이터 main 발행 검증

소스 커밋 후 `git pull --no-rebase origin main`을 실행했다. 검증 중 추가된 영지경영·캠퍼스·메카 발행도 다시 pull하여 합쳤다. 후보 목록은 파일명·종류로 합치고 두 안내문의 추가 내용을 보존했으며 검색 인덱스를 합본 소스에서 재구축했다.

최신 원격 `{parent}`의 모듈 {len(paths)}개와 scripts/precore는 동일 바이트로 보존했다. 해병문학 모듈 두 개를 추가했으며 시각 87개·진단 247개·바인딩 166개와 의미 sidecar를 포함한다. 복사한 연구·재시험 증거 및 생성 원본 6장의 바이트는 유지했다. 입력 사진은 로컬에 보존하며 기존 증거의 줄바꿈·후행 공백도 해시 유지를 위해 보존했다.

후보 {validation['native_candidates']:,}개, 바인딩 {validation['bindings']:,}개, 긍정 레코드 {report['records']:,}개의 최종 사전 오류는 0건이다. 의미 회귀 {test_counts['semantic-tests.log']}개 및 봉인 커널의 주제·소유권 회귀 13개가 통과했다. 원시 source facade는 생성 모듈 없이 직접 실행할 수 없으므로 해당 import 실패 probe와 실제 봉인 커널 검증을 구분했다. 기본 설치 런타임 선택은 바꾸지 않았다. 이미지 재생성이나 과거 실패의 합격 승격은 없다.

최종 인덱스는 `{report['layout_id']}`다. 작업 중 만든 과거 임시 인덱스는 현재 트리에서 제거하고 커밋 이력을 보존했다. 이번 주제 회귀는 upstream의 기존 봉인 커널 테스트 관례에 맞춰 canonical tests에도 포함했다. source-tree-only 검사라고 주장하지 않는다.

이 문서는 푸시 전 검증 기록이다. 실제 push, 로컬/tracking/live 원격 SHA 대조, 워크트리 제거 및 캐시 정리 결과는 `generated/publication-receipts/marine-literature-20261024/`에 별도로 기록한다. 최종 원본·프롬프트·보고서, 입력 사진, 설치된 공용 런타임과 활성 인덱스, 다른 작업의 변경은 정리에서 보호한다.
''')
reference = S / 'references/marine-literature-semantics.md'
text = reference.read_text()
text = text.replace('The regression and\nits runtime-dependent source snapshot remain in the research evidence. That\nnewer kernel and independent unpublished neutral-authoring code are not part of\nthis data-only publication; the selected runtime configuration is preserved.',
                    'The regression and its original snapshot remain in the research evidence.\nThe upstream requester-query implementation is preserved in this merge; the\ncanonical topic regression follows the existing explicit sealed-kernel test\nconvention. The selected runtime configuration is preserved.')
# Preserve a clear post-upstream note even if historical paragraph wrapping differs.
if 'Post-upstream publication:' not in text:
    text += '\nPost-upstream publication: requester-query source fixes from main are preserved.\nThe canonical topic regression uses the same explicit sealed-kernel convention\nas the upstream query/ownership tests; actual pixels remain the previous three\nrecorded image calls. No source-tree facade execution is claimed.\n'
reference.write_text(text)

staged_before = set(filter(None, git('diff', '--cached', '--no-renames', '--name-only', '-z').decode().split('\0')))
allowed_prefix = str(A / 'photo_candidate_search_shards') + '/'
assert all(name.startswith(allowed_prefix) and not Path(name).exists() for name in staged_before)
changed = set(git('diff', '--no-renames', '--name-only', text=True).splitlines())
untracked = set(git('ls-files', '--others', '--exclude-standard', text=True).splitlines())
permitted_files = {str(A / 'photo_candidate_search.json'), str(reference), str(S / 'tests/test_topic_title_discovery_scope.py')}
assert all(name.startswith(str(P) + '/') or name.startswith(allowed_prefix) or name in permitted_files for name in changed | untracked)
names = {str(A / name) for name in members} | changed | untracked
names = {name for name in names if Path(name).is_file()}
scope = set(filter(None, git('ls-files', '-z', '--', str(Q)).decode().split('\0'))) | names
scope |= {str(S / 'SKILL.md'), str(S / 'references/maintenance.md'), str(S / 'tests/test_marine_literature_semantics.py'),
          str(A / 'photo_candidate_corpus_manifest.json'), str(A / 'photo_candidate_marine_literature_20261024.json'),
          str(A / 'photo_candidate_marine_literature_bindings_20261024.json'), str(A / 'photo_marine_literature_semantics_20261024.json')}
scope = {name for name in scope if Path(name).is_file() and not name.endswith(('SHA256SUMS.PUBLISHED', 'publication-staged-verification.json'))}
(P / 'SHA256SUMS.PUBLISHED').write_text(''.join(sha(Path(name)) + '  ' + name + '\n' for name in sorted(scope)))
names.add(str(P / 'SHA256SUMS.PUBLISHED'))
for offset in range(0, len(names), 128):
    subprocess.run(['git', 'add', '--', *sorted(names)[offset:offset + 128]], check=True)
actual_staged = set(filter(None, git('diff', '--cached', '--no-renames', '--name-only', '-z').decode().split('\0')))
assert actual_staged <= names | staged_before
assert staged_before <= actual_staged
blobs = {}
for row in git('ls-files', '-s', '-z').split(b'\0'):
    if not row:
        continue
    meta, encoded_name = row.split(b'\t', 1)
    name = encoded_name.decode()
    if name in actual_staged:
        data = Path(name).read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        assert blob == meta.decode().split()[1], name
        blobs[name] = blob
proof = P / 'publication-staged-verification.json'
write(proof, {'status': 'pass', 'actual_staged_files_before_own_receipt': sorted(actual_staged),
              'current_blob_ids': blobs, 'explicit_deletions': sorted(staged_before),
              'own_receipt_path': str(proof), 'checksum_members': len(scope)})
subprocess.run(['git', 'add', '--', str(proof)], check=True)
assert set(filter(None, git('diff', '--cached', '--no-renames', '--name-only', '-z').decode().split('\0'))) == actual_staged | {str(proof)}
print(json.dumps({'status': 'pass', 'layout': report['layout_id'], 'source_tests': test_counts['semantic-tests.log'],
                  'sealed_tests': 13, 'parent_modules_exact': len(paths), 'staged_files': len(actual_staged | {str(proof)})}), flush=True)
