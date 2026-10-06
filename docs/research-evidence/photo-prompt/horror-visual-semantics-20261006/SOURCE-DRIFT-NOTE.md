# 연구 중 기존 파일 변경 감지

2026-10-06 KST. 연구 기준 스냅샷의 792개 기존 skill/tests 파일과 마지막 검증의 해시를 비교했을 때 아래 7개가 달랐다. 785개는 같은 해시였다. 이 작업에서 수행한 파일 작성은 현재 연구 디렉터리 안에 한정되며, 이 차이를 되돌리거나 다른 작업의 변경을 수정하지 않았다.

- `skills/photo-prompt-image-generator/SKILL.md`
- `skills/photo-prompt-image-generator/references/composition-contract.md`
- `skills/photo-prompt-image-generator/references/photographic-methodology.md`
- `skills/photo-prompt-image-generator/scripts/audit_composed_prompt.py`
- `skills/photo-prompt-image-generator/scripts/photo_contracts.py`
- `skills/photo-prompt-image-generator/scripts/prompt_generator.py`
- `tests/test_photo_authorial_core_v6.py`

후속 확인에서는 scene-development/authorial 지침과 core·audit 주변 변경이 보였다. 이 기록은 Git diff 전체를 연구 시작 이후 차이로 단정하지 않는다. 시작 때부터 dirty했던 파일에는 이전 변경도 함께 포함될 수 있다. 시작 시점의 파일 본문을 저장하지 않았으므로 해시 비교가 보여주는 것은 해당 파일의 변화 여부뿐이다.

마지막 구조 검증은 당시 실제 로더와 component compiler로 통과했다. authored data와 generated index 파일은 이번 비교에서 변하지 않았다. 실제 채택 시에는 current skill/contracts와 loader/hash를 다시 확인하고, 연구의 오래된 스냅샷으로 현재 runtime을 덮어쓰지 않는다. 전체 결과는 [VALIDATION.json](VALIDATION.json)에 보존한다.
