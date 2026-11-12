# 츤데레 원문 맥락 H-F2 overlay (비활성 실험물)

이 폴더는 설치된 코드나 세대를 변경하지 않는다. `build_index.py`는 표 346행과 원문 본문 70개·추출 표현 21개를 총 437행으로 보존하여 BM25F 인덱스를 별도 디렉터리에 만든다. 본문 빈 항목도 원문 단위로 보관한다. 질의 임베딩과 후보 인덱스는 건드리지 않는다. 결과는 연구 맥락이며 원문 대화는 정의의 독립적 검증, 후보 발급, 사진의 가시성, 인물의 나이·동의 또는 네이티브 승인 근거가 아니다.

## 빌드 및 검증

```sh
python3 skills/photo-prompt-image-generator/runtime-overlays/tsundere-context-20261112/build_index.py --output /tmp/tsundere-context-new-build
python3 -m pytest -q skills/photo-prompt-image-generator/runtime-overlays/tsundere-context-20261112/tests/test_context_overlay.py skills/photo-prompt-image-generator/tests/test_hf2_research_context_lane.py
```

빌드는 출력 디렉터리가 존재하지 않아야 하고 설치 저장소 내부 출력을 금지한다. Git에 포함된 `source-snapshots/`의 원문 표 및 본문 스냅샷 해시와 각 셀·본문 위치를 확인하고, 현재 설치 기반 세대와 과거 페티시 맥락 인덱스의 임베딩 binding 및 파일 해시를 확인한다. 109개 `followup_review`는 대응 검토 레코드의 해시, 내용, 원문 셀 및 승인 경계와 대조하고 검색 결과에 유지한다. `build-lock.json`은 두 인덱스, 원문 뷰·스냅샷, 검토 파일, overlay 코드의 해시를 기록하며 봉인·활성화 증거가 아니다. 빌드에는 설치된 H-F2의 Python 의존성이 필요하다.

## 향후 통합 시 필요한 작업

- 설치 기준 H-F2 `763c9e9032cdb8969fa1c1650697ccb24aaf1962798bf527ad980d39ade27bb7`, native `8498a19bf5cdf0226849c269a9b9f9ad2b130390c36b5d7bf1fea83cb4cc4b8d`. 이 세대는 검색 및 감사 훅은 있으나 `research_context` descriptor가 없다.
- 신규 코드 세대에 이 overlay의 `scripts/photo_h_f2_research_context.py`를 적용하고 나머지 workflow·receipt 코드를 유지한다. 기준 native의 동일 파일 원본 SHA-256은 `c94733b41dea47b6d5d68ca09a89baba52b6da79b4a4673d43b1e3f09188f379`이다. 결합 대상이 바뀌면 직접 비교·재검토해야 한다.
- 28행 페티시 맥락을 복원할 때 과거 `adbfbd2bedaf0be8948fc802305a5112b854ebf9d9143993cb1065ef533d391e`의 원본 descriptor 및 `research-context-index.json.gz`를 사용한다. 해당 파일 SHA-256은 `fdbb29d99d7a26f77b810678c8408ef07479b4caa7b8722a794fc50a81ed9755`이고 binding은 기준 세대와 같다. 파일 해시·원본 descriptor·내부 데이터·binding을 검증하고 새 세대 manifest의 `files`와 `research_context`에 함께 반영해야 한다. 기존 세대는 건드리지 않는다.
- 빌드 산출물의 `tsundere-research-context-index.json.gz`를 새 세대에 넣고 `files`에 실제 파일 해시를, `tsundere_research_context`에 `schema: photo-h-f2-tsundere-research-context-index/v1`, `file`, `rows: 437`, `canonical_sha256`을 lock 값으로 기록한다. 새 코드·데이터, 원문 해시, 현재 대상 후보 세대 및 binding을 재검증한 후 별도 절차로 봉인한다. 이 폴더는 봉인·활성화 도구가 아니다.
- 봉인된 스테이징 환경에서 실제 `search_material`과 `audit_packet`을 사용해 기존 후보 ID·순위·영수증이 기준과 일치하는지, 두 맥락의 반환과 출력 변조 거부가 작동하는지 비교해야 한다. 현재 테스트는 모의 generation 객체에 실데이터를 넣은 lane 및 audit 단위 검증이며 전체 관리형 경로 검증은 아니다.

## 검색 경계

기존 28행 검색을 먼저 그대로 수행하고 츤데레 맥락을 별도 최대 `limit`개 덧붙인다. 따라서 기존 결과의 순위는 그대로이며 후보 검색에는 영향을 주지 않도록 설계했다. 츤데레 lane의 성인 표시 행과 본문에 명시적인 성인 맥락이 들어 있는 행은 질의에 구체적인 성인 맥락 표현이 있어야 제공한다. `fetish=3` 같은 제어값, 복식, 브랫 또는 츤데레만으로 성인 맥락을 추론하지 않는다. 일부 부정 표현이 있으면 츤데레 lane 전체를 억제한다. 부정 및 성인 표현 인식은 유한한 규칙으로 모든 언어·문장에 대해 완전하지 않다. 원문을 수정하거나 비성인 행의 사람을 성인으로 간주하지 않는다.

일반 사진 질의의 흔한 단어가 원문 본문과 겹쳐 무관한 맥락이 반환되지 않도록, 츤데레 주제 표지가 있거나 질의 전체가 원문 표제·대체 표기·추출 표현·명시적 부분검색 표현과 정확히 일치해야 신규 lane이 열린다. 성인 맥락 표지만 제거한 나머지 질의가 정확히 일치하는 경우도 허용한다. 주제 표지가 없는 정확 질의는 해당 표현이 속한 행만 반환한다. 관련 검색 예시나 본문 단어의 단순 겹침은 진입 근거가 아니다. 이 보수적 조건 때문에 주제 표지가 없는 자유로운 문장 형태의 관련 질의는 누락될 수 있다.

검색 결과는 원문 소스 URL, 스냅샷·뷰 해시, 행의 출처 및 권한 필드, 점수와 성인 조회 여부를 포함한다. 점수는 관련도일 뿐 의미의 동등성 또는 사실의 신뢰도를 나타내지 않는다. `audit`은 결과를 다시 계산하여 수정이나 누락을 거부한다.

원본 봉인 세대와 로컬 임베딩 런타임은 Git에 포함되지 않는다. 해당 세대가 설치되지 않은 환경에서는 통합 테스트를 건너뛰며, 스냅샷과 자산만으로 설치된 인덱스나 검색 품질의 재현을 주장하지 않는다.
