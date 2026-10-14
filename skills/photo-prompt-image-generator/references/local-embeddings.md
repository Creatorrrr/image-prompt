# 스킬 내장 로컬 임베딩

EmbeddingGemma 2의 텍스트 구성(271,002,624 parameters)을 스킬 전용 Python에서 실행한다. HTTP 서버·Ollama·LM Studio·임베딩 API 키를 사용하지 않는다. 공개 CLI는 설치 설정에 따라 스킬 전용 Python을 선택하고 모델을 같은 프로세스에서 지연 로드한다. 다른 Python 환경에서 직접 호출할 때는 CLI가 소유하는 파이프 worker를 사용하며 종료 시 정리된다. 최초 모델 로드와 실제 추론은 명시적인 post-core 단계에서만 발생한다.

## 설치와 확인

```sh
.venv/bin/python skills/photo-prompt-image-generator/scripts/setup_local_embeddings.py prepare --device mps
.venv/bin/python skills/photo-prompt-image-generator/scripts/setup_local_embeddings.py check
```

`prepare`만 고정된 의존성과 공식 모델 revision을 다운로드한다. CPU 설치에는 `--device cpu`를 사용한다. 기존 프로젝트 가상환경은 수정하지 않는다. 준비된 모델은 `.runtime/embeddinggemma2/<revision>/`, 전용 Python은 `.runtime/embedding-python/`에 있다. 파일 해시·모델 revision·토크나이저/모델 구성·라이브러리 버전·장치·정밀도는 `embedding-runtime.lock.json`으로 고정한다. 공식 원본의 불필요한 modality encoder를 제외해 저장하고 원본과 출력 동등성을 검사한다.

현재 검증 장비는 Mac arm64/Python 3.14.3/MPS FP32다. 기본 출력은 L2 정규화한 768차원이며 FP16을 사용하지 않는다. 8,192 token 한도를 초과하면 오류를 내며 입력을 조용히 자르지 않는다. 문서에는 `title: none | text: `, 질의에는 `task: search result | query: `를 별도로 적용한다. 모델·입력 recipe·정밀도/장치가 바뀌면 새 공간과 전체 재임베딩으로 검증한다.

## 별도 인덱스 생성과 검증

```sh
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_shared_candidate_index.py \
  --backend embeddinggemma2-local --output-assets /absolute/candidate/assets \
  --cache /absolute/build-cache --batch-size 32
```

`--output-assets`는 기존 manifest와 모든 Gemini shard를 유지한다. 재개 시에는 같은 authored corpus와 모델 공간의 checkpoint만 재사용한다. 모델 파일 누락·변조, cache binding 불일치, 잘못된 실행 증거는 오류다. Gemini로의 자동 우회나 암묵적인 keyword 검색은 없다.

실제 검색 질의는 활성 인덱스의 공간을 사용한다. `SPACE` 상수는 과거 Gemini fixture 호환용이며 실행 기본값이 아니다. 일반 provider와 새 빌더의 기본값은 `embedding-default.json`을 따른다. 다른 모델 공간의 질의·문서·실행 증거를 섞을 수 없다.

## 오프라인 배포

```sh
.venv/bin/python skills/photo-prompt-image-generator/scripts/setup_local_embeddings.py bundle --output /absolute/offline-bundle
.venv/bin/python /absolute/new-skill/scripts/setup_local_embeddings.py install-bundle --bundle /absolute/offline-bundle
```

오프라인 묶음은 모델, 스킬 코드, 고정된 Python wheel과 설치 메타데이터를 포함한다. Python 버전·OS·CPU architecture가 맞아야 한다. 새 스킬 경로에 코드부터 복사한 뒤 `install-bundle`을 실행한다. 사용 중인 설치를 덮어쓰지 않는다. 후보 source/index는 별도 유지되는 자산이며 함께 배포할 때 해당 완전한 closure를 추가한다. 모델의 Apache-2.0 라이선스 전문은 `embeddinggemma2-LICENSE.txt`에 있다. 원본: https://huggingface.co/google/embeddinggemma-2/tree/914f7f89142e33e77833254d9c9b90c3cef7303b

## 채택과 복구

```sh
.venv/bin/python skills/photo-prompt-image-generator/scripts/activate_local_embeddings.py activate \
  --assets /absolute/candidate/assets --qualification /absolute/qualification --backup /absolute/activation-backup
.venv/bin/python skills/photo-prompt-image-generator/scripts/activate_local_embeddings.py rollback --backup /absolute/activation-backup
```

채택은 현재 소스와 일치하는 품질·회귀·오프라인 검증 보고서가 통과한 경우에만 가능하다. 새 shard의 checksum과 전체 문서 실행 증거를 확인하고, 기존 manifest·기본값·CURRENT를 백업한 뒤 유지보수 revision 안에서 전환·publication한다. rollback은 보존한 Gemini manifest와 현재 authored corpus가 일치할 때만 실행된다. 기존 Gemini shard를 삭제하지 않는다.

query/context, candidate pack, generation, receipt, 독립 감사의 결합을 유지한다. 모든 요청·모델 비교는 현재 source와 명확히 연결해야 하며, 검색 지표나 합성 회귀 사례의 성공을 이미지 품질·실사용 선호의 성공으로 확대하지 않는다.
