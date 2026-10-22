# 작업 중 관찰된 공유 작업 트리 변화

이 연구의 모든 파일 쓰기는 `docs/research-evidence/photo-prompt/clockpunk-20261023/` 안에서 수행했다. 기존 SKILL·후보·인덱스·runtime·maintenance 파일을 이 작업에서 수정하거나 커밋하지 않았다.

시작 HEAD는 `be52bda69010b94bb444e998fe148b2881e20624`였다. 첫 최종 검사에서는 `9b654b631653719774c276148daeadc308c0b50b` (`feat(photo-prompt): add analog horror semantic and candidate data`)로 이동해 있었다. 시작에 hash를 보존한 tracked 파일 15,704개 중 바이트가 다른 파일은 `skills/photo-prompt-image-generator/references/maintenance.md` 한 개였다. Atompunk와 Space Opera의 새 연구 파일들도 status에 나타났다.

이는 같은 작업 트리에서 병행 작업이 진행된 것으로 보이는 관찰이다. hash만으로 그 작업의 작성자나 세부 의도를 증명하지는 않는다. 다른 변경은 되돌리거나 흡수하지 않았다. 시작 baseline을 새 상태로 덮어써서 ‘모두 무변경’으로 보이게 하지 않았다.

조사한 authored source manifest와 그 모든 모듈 hash는 snapshot 이후 동일했다. 따라서 이 연구의 기존 CID·조건·효과 snapshot은 해당 검사 시점에 계속 일치했다. 전체 저장소 무변경, 전체 untracked 파일 바이트 보존, remote SHA는 이 결과가 증명하지 않는다. 초기 untracked 파일은 이름만 기록했으며 전부 hash하지 않았다.

`VALIDATION.json`은 연구 구조 검사와 workspace 관찰을 별도로 기록한다. 공유 작업 트리 drift가 있으면 연구 구조가 통과해도 전체 상태는 `PASS_WITH_WORKSPACE_DRIFT`다. 마지막 검사 시점의 구체 경로·HEAD는 그 JSON을 따른다.
