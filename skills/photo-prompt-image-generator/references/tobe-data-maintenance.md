# TO-BE 후보 데이터와 검색본 유지보수

정식 후보 원본은 이 스킬의 `assets/`에 있다. 현재 후보는 27,077개이며, 정식 검색 뷰는 25,551개다. 검토한 뷰의 기준본은 `assets/photo_candidate_retrieval_views_calibration_20261027.json`, 추가 보강 오버레이와 검증에 필요한 근거는 `data/reviewed-views/`와 `data/provenance/`에 있다. 진단 전용 후보와 뷰가 없는 일부 실현 항목은 이 수치에 별도로 반영되어 있다.

## 뷰 재생성

새 뷰 모듈을 만든 후, 임베딩이나 검색 인덱스를 만들기 전에 다음 명령으로 검토된 기준 뷰와 보강 내용을 준비한다.

```sh
python3 skills/photo-prompt-image-generator/scripts/photo_prepare_reviewed_views.py \
  --input /absolute/new-views.json --output /absolute/prepared-views.json
```

기준본에 있던 뷰를 빠짐없이 복원하고 등록된 오버레이를 적용하며 출처 인용과 기존 근거를 확인한다. 같은 ID의 다른 내용, 바뀌거나 빠진 후보 원본은 검토 없이 덮어쓰지 않고 오류로 알린다. 입력이나 정식 자산을 덮어쓰거나 실행 중인 검색본을 전환하지 않는다. 새 후보나 원본 변경을 반영할 때는 오류를 검토해 기준본을 갱신한 후 다시 실행한다. 이 명령을 거치지 않는 저수준 뷰 생성 호출에 보강 내용이 자동 적용되는 것은 아니다.

Git의 과거 커밋을 가리키는 인용도 `data/provenance/reviewed-git-sources.json.gz`에 원문과 원래 커밋·트리의 증명을 보존한다. 재생성 시 압축 파일과 원문의 해시, 원문이 해당 Git 커밋의 경로에 속했다는 증명, JSON 경로와 인용문을 확인하므로 해당 과거 커밋이 없는 환경에서도 검증할 수 있다.

준비한 결과는 후속 다중 뷰 임베딩과 H-only+F2 검색본 생성 및 검증에 입력해야 한다. `build_shared_candidate_index.py`는 후보 원본의 별도 인덱스를 만들며 H-only+F2 다중 뷰 검색본 전체를 재생성하지 않는다. 현재 임의의 새 후보 원본에서 H-only+F2 검색본까지 한 번에 만드는 통합 명령은 제공하지 않는다.

## 검증된 현재 검색본 복원

현재 고정된 검색본과 별도 후보 원본 인덱스는 크기 때문에 Git에 포함하지 않는다. `data/tobe-release-lock.json`에 기록된 해시와 일치하는 두 파일을 별도로 보관하고 옮겨야 한다. 기존 모델 설치가 없다면 먼저 [로컬 임베딩 설치](local-embeddings.md)를 완료한다. 그다음 저장소 루트에서 실행한다.

```sh
python3 skills/photo-prompt-image-generator/scripts/install_photo_tobe_bundle.py \
  --bundle /absolute/tobe-data-and-runtime.tar.zst \
  --source-index /absolute/tobe-source-index.tar.zst
```

설치 도구는 원본 후보와 인덱스 manifest가 고정된 릴리스와 일치하는지, 압축 묶음과 각 인덱스 조각의 해시가 맞는지, 검색본의 구성 파일이 완전한지 확인한다. 별도 위치에서 활성화 없이 시험할 때는 `--destination /absolute/test-store --no-activate`를 추가한다. 이 명령은 기존 보강 데이터를 재임베딩하지 않고 이미 검증된 검색본을 복원한다. 묶음은 자동 다운로드되지 않으며, 모델과 두 묶음 없이는 Git만으로 검색본을 설치할 수 없다.

기존 검색본은 현재 고정된 원본에만 대응한다. 후보 내용을 바꾼 뒤에는 이전 인덱스를 그대로 설치하지 말고, 새 원본에 맞는 인덱스와 검색본을 만들어 검증해야 한다.
