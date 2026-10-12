"""Stage only incoming main, qualified source repairs, active shards and compact evidence."""
import ast
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

OUT = Path(__file__).resolve().parent
ROOT = Path('/Users/chasoik/.codex/worktrees/slot-retrieval-stage07-integration/image-prompt')
REL = 'docs/research-evidence/photo-prompt/slot-retrieval-stage07-20261012/main-publication'
ASSETS = 'skills/photo-prompt-image-generator/assets'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(name, obj):
    (OUT/name).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')


def main():
    validation = json.loads((OUT/'FINAL-MERGE-VALIDATION.json').read_text())
    assert validation['all_latest_selectors_pass'] and validation['all_current_critical_audits_pass']
    assert validation['public_entrypoint_cases'] == 40
    stage = git('rev-parse', 'HEAD').decode().strip()
    remote = git('rev-parse', 'MERGE_HEAD').decode().strip()
    assert stage == '47d535d12ab80f1ae99c2f443af3f2846a891b6e'
    assert remote == '0b33ae2c18a26060b918436c38d6d77eb2385306'
    unchanged = [
        '.gitignore',
        ASSETS+'/photo_prompt_autumn_fashion_extension.json',
        ASSETS+'/photo_prompt_portrait_composition_extension.json',
        ASSETS+'/photo_prompt_tags.json',
        'skills/photo-prompt-image-generator/references/maintenance.md',
        'skills/photo-prompt-image-generator/scripts/build_semantic_index.py',
        'skills/photo-prompt-image-generator/scripts/prompt_generator.py',
        'tests/test_photo_semantic_attempt_records.py',
        'docs/research-evidence/photo-prompt/extension-maintenance/korean-label-correction-20261012-photo_prompt_autumn_fashion_extension.json',
        'docs/research-evidence/photo-prompt/extension-maintenance/korean-label-correction-20261012-photo_prompt_portrait_composition_extension.json',
    ]
    for name in unchanged:
        assert (ROOT/name).read_bytes() == git('show', remote+':'+name), name
    golem = ASSETS+'/photo_prompt_visual_obligations.json'
    assert (ROOT/golem).read_bytes() == git('show', stage+':'+golem)
    # Apart from the three reviewed prerequisites, both source files remain exact main bytes.
    repairs = json.loads((OUT/'ANIMAL-SCOPE-REPAIR.json').read_text())
    repaired_ids = {'soil_e077', 'soil_e078', 'electric_eel_freshwater_visible_form'}
    repaired_files = ['photo_prompt_soil_earth_extension.json', 'photo_prompt_electrical_relations_extension.json']
    compared = []
    for filename in repaired_files:
        name = ASSETS+'/'+filename
        old = json.loads(git('show', remote+':'+name))
        new = json.loads((ROOT/name).read_text())
        found = []
        for entries in new['slots'].values():
            for entry in entries:
                if entry['id'] in repaired_ids:
                    found.append(dict(id=entry['id'], primary_context_alternatives=entry.pop('primary_context_alternatives')))
        assert new == old, name
        compared.extend(found)
    assert {r['id'] for r in compared} == repaired_ids
    animal = 'tests/test_photo_animal_subject_retrieval.py'
    previous = ast.parse(git('show', remote+':'+animal))
    current = ast.parse((ROOT/animal).read_text())
    new_class = next(n for n in ast.walk(current) if isinstance(n, ast.ClassDef))
    old_class = next(n for n in ast.walk(previous) if isinstance(n, ast.ClassDef))
    for old in old_class.body:
        equivalent = next(n for n in new_class.body if getattr(n, 'name', None) == getattr(old, 'name', None))
        assert ast.dump(old) == ast.dump(equivalent)
    manifest_name = ASSETS+'/photo_prompt_semantic_index.json'
    manifest = json.loads((ROOT/manifest_name).read_text())
    active = []
    for row in manifest['shards']:
        name = ASSETS+'/'+row['path']
        raw = (ROOT/name).read_bytes()
        assert sha(raw) == row['sha256'], name
        active.append(dict(path=name, sha256=sha(raw), size=len(raw)))
    assert len(active) == 16
    parent_paths = set(git('ls-tree', '-r', '--name-only', stage).decode().splitlines())
    parent_paths.update(git('ls-tree', '-r', '--name-only', remote).decode().splitlines())
    staged = git('diff', '--cached', '--name-only').decode().splitlines()
    inactive = [name for name in staged if '/photo_prompt_semantic_index_shards/' in name
                and name not in parent_paths and name not in {r['path'] for r in active}]
    if inactive:
        subprocess.run(['git', 'restore', '--staged', '--source=HEAD', '--', *inactive], cwd=ROOT, check=True)
    previous_intent = OUT/'MERGE-INTENT-VERIFICATION.json'
    if previous_intent.exists():
        inactive = sorted(set(inactive) | set(json.loads(previous_intent.read_text()).get('intermediate_shards_excluded_from_commit', [])))
    save('MERGE-INTENT-VERIFICATION.json', dict(
        stage07_commit=stage, remote_commit=remote, remote_authored_files_preserved=unchanged,
        remote_animal_positive_and_printed_tests_preserved=True,
        remote_animal_category_overrides_preserved=True, stage07_golem_source_preserved=golem,
        source_only_repairs=compared, source_repair_evidence=repairs,
        merged_semantic_manifest_sha256=sha((ROOT/manifest_name).read_bytes()),
        active_semantic_shards=active, intermediate_shards_excluded_from_commit=inactive,
        runtime=validation['runtime'], embedding_api_calls=0))
    files = [
        'FINAL-MERGE-VALIDATION.json', 'MERGE-INTENT-VERIFICATION.json', 'ANIMAL-SCOPE-REPAIR.json',
        'REPAIRED-RETRIEVAL-INVARIANCE.json', 'REPAIRED-RUNTIME.json', 'REPAIRED-PUBLICATION.json',
        'REPAIRED-COMPOSITION-VALIDATION.json', 'REPAIRED-COMPOSITION-INPUTS.json',
        'REPAIRED-COMPOSITION-ALL-INPUTS.json', 'PULL-RESULT.json', 'MERGE-SOURCE-PREFLIGHT.json',
        'merge-focused-tests.json', 'merge-focused-tests.log', 'repaired-animal-context-tests.json',
        'repaired-animal-context-tests.log', 'repaired-bird-negative-recheck-tests.json',
        'repaired-bird-negative-recheck-tests.log', 'scope-repaired-index-summary.json',
        'scope-repaired-semantic-build.log', 'scope-repaired-dictionary.log', 'scope-repaired-visual-check.log',
        'scope-repaired-visual-vector-preflight.json', 'merged-exact/exact-recall-summary.json',
        'merged-exact/runtime-acquisition.json', 'ADOPTION-AUTHORING.json', 'GOLEM-COMPOSITION-AUTHORING.json',
        'qualify_final_merge.py', 'replay_public_worker.py', 'verify_repaired_compositions.py',
        'prepare_merge_commit.py',
    ] + ['REPAIRED-PUBLIC-ENTRYPOINTS-'+str(i)+'.json' for i in range(4)]
    report = '''# 7단계와 origin/main 통합 검증

7단계 커밋 `47d535d12ab80f1ae99c2f443af3f2846a891b6e`에 origin/main `0b33ae2c18a26060b918436c38d6d77eb2385306`을 pull하여 통합했다. 원격의 한글 라벨, 동물 분류, 임베딩 요청/응답 기록 기능과 7단계의 슬롯 검증 및 골렘 의미 데이터를 보존했다. 파생 semantic index 충돌은 합쳐진 source를 기준으로 재생성했다.

통합 중 참새 장면에 지렁이 subject 후보가 들어오는 회귀를 발견했다. 지렁이·개미·전기뱀장어 3개 source에 기존 primary context prerequisite 형식을 추가했다. 원격의 실제 동물 EN/KO 양성 검사와 인쇄물 음성 검사를 유지하고, 참새 EN/KO 음성 검사를 추가했다. source의 나머지 필드와 기존 테스트 메서드는 그대로다.

- 최종 generation: `5ef4af21887c41b6e890a84ed99da85b0ea5a10f7811202b0ad28656bb91f9ff`.
- 공개 후보 생성·뷰·원본 재계산 40건 통과. 후보 누락 변조 40건 탐지. native 표기 양성 10/10, 인접·제외 문맥 오탐 0/10.
- 필요한 후보 13/13 노출, 채택 가능 12/13. 초기 7단계의 subject 의미, authorial core, creative controls, negative, 후보 cap 유지.
- 최종 source에서 실제 receipt를 검증한 composed/runtime 감사 9건 통과. 48개 최종 프롬프트·negative·선택 ID는 7단계 검증본과 동일하다. 이전 generation의 전체 48건 감사는 역사적 증거이며 최종 source에서 48건을 다시 감사했다는 뜻은 아니다.
- 관련 테스트 60개 고유 selector의 마지막 실행 통과. 추가한 참새 테스트의 초기 setting 입력 오류 2건과 수정 후 통과 결과를 모두 보존했다.
- 합친 원본의 exact 조회 40,380/40,380, 슬롯 cap 내 40,148/40,380. prerequisite 수정 전후 문서·벡터·검색 metadata·코드가 모두 같음을 확인하여 전수 결과를 재사용했다.
- 임베딩 API와 이미지 생성 호출 0. 전체 테스트 suite와 실제 이미지 생성은 실행하지 않았다.

이 파일은 머지 커밋 직전의 통합 검증 기록이다. 푸시와 원본 checkout 보존의 최종 상태는 로컬 `DELIVERY.md`/`DELIVERY.json`에서 별도로 검증한다. 여기에는 요약·해시·로그를 담았고, 실제 candidate-pack/receipt/runtime-store 및 원본 백업은 로컬 검증 디렉터리에 보존했다.
'''
    (OUT/'REPORT.md').write_text(report)
    files.append('REPORT.md')
    evidence = []
    copies = []
    for filename in files:
        source = OUT/filename
        target = ROOT/REL/filename
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        assert source.read_bytes() == target.read_bytes()
        raw = source.read_bytes()
        if source.suffix == '.log':
            # Retain raw terminal output locally; remove trailing spaces in the Git text copy.
            target.write_text('\n'.join(line.rstrip() for line in source.read_text().splitlines())+'\n')
        copies.append(dict(path=REL+'/'+filename, source_sha256=sha(raw),
                           committed_sha256=sha(target.read_bytes()),
                           terminal_trailing_whitespace_normalized=raw != target.read_bytes()))
        evidence.append(REL+'/'+filename)
    save('EVIDENCE-COPY.json', copies)
    shutil.copy2(OUT/'EVIDENCE-COPY.json', ROOT/REL/'EVIDENCE-COPY.json')
    evidence.append(REL+'/EVIDENCE-COPY.json')
    source_paths = [manifest_name, *[ASSETS+'/'+f for f in repaired_files], animal]
    stage_paths = [*source_paths, *[r['path'] for r in active], *evidence]
    subprocess.run(['git', 'add', '--', *stage_paths], cwd=ROOT, check=True)
    subprocess.run(['git', 'diff', '--cached', '--check'], cwd=ROOT, check=True)
    assert not git('ls-files', '-u').strip()
    final_staged = git('diff', '--cached', '--name-only').decode().splitlines()
    unexpected = set(final_staged)-set(staged)-set(stage_paths)
    assert not unexpected, unexpected
    save('MERGE-STAGING.json', dict(reviewed_paths=final_staged,
        added_evidence_count=len(evidence), excluded_intermediate_shards=inactive,
        active_shard_count=len(active), unmerged_paths=[], diff_check_pass=True))
    print(json.dumps(dict(staged_paths=len(final_staged), evidence_files=len(evidence),
                         active_shards=len(active), inactive_shards_excluded=len(inactive))))


if __name__ == '__main__':
    main()
