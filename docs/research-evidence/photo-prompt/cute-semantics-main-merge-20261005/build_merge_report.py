"""Write the current merge receipt without relabeling historical pixel evidence."""
import hashlib
import json
import subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
index=json.loads((HERE/'INDEX-REBUILD.json').read_text())
preserved=json.loads((HERE/'MERGE-PRESERVATION.json').read_text())
result_path=HERE/'FINAL-REGRESSION-RESULT.json'
result=json.loads(result_path.read_text()) if result_path.exists() else None
tests=f"전체 {result['test_count']:,}개 검사 {'PASS' if result['all_pass'] else '미통과'}" if result else '전체 1,529개 검사 진행 중'
def link(label,name):return f'[{label}]({HERE/name})'
report=f'''최신 main의 기존 의도와 이번 귀여움 대체 표현·후보 데이터의 의도를 함께 보존해 통합했다. 기존 main authored JSON 83개는 바이트가 동일하며, 기존 후보 67개의 label·정의·효과·소유·전제 조건을 유지한 채 한국어·영어 동등 표현 134개를 추가했다. 좁은 신규 후보 15개, 프로필·선택형 묶음 각각 26개와 기존 프로필 11개 보강을 유지했다.

main pull 당시 원격과 작업 기준은 `98ca92a070a6127a2e03877ec8a5d3f0dfda0467`로 같았다. 다른 연구의 미커밋 파일은 이번 배포 범위에서 제외하고 분리된 작업트리에서 검증했다. 데이터 통합 커밋은 `cfa68762b9eeda8f09f6e485bf2665492fe53584`다.

| 확인 대상 | 결과 |
|---|---|
| 기존 main authored JSON | 83개 바이트 보존 |
| 보강한 기존 후보 | 67개 기존 의미·효과·전제 조건 보존 |
| 후보 인덱스 | {index['semantic_entries']:,}개, main 9,933개 + 이번 작업 82개의 정확히 같은 텍스트·벡터 재사용 |
| 시각 프로필 인덱스 | {index['visual_profiles']:,}개, 호환 캐시에서 재생성 |
| 새 임베딩 API 호출 | 0회 |
| V1–V16 manifest와 pack | 원본 25개 바이트 보존 |
| V17 동결 회귀 장면 | PASS; 후보 객체·순서·core·controls·composition·negative·privacy 보존 |
| V17 실제 pack 변화 | DATA 결합 해시 5개만 변경 |
| 기존 이력 검사 | 30개 PASS; V16은 원래 실행 코드와 DATA로 재검사 |
| 새 V17 공격성 검사 | 5개 PASS; 후보·순서·core·controls·negative의 동시 재해시를 거부 |
| 전체 회귀 검사 | {tests} |

새 DATA는 V17 `photo-cute-equivalent-language-inventory-transition/v17`로 등록했다. V16의 기준이나 증거를 다시 해시해 새 결과로 취급하지 않는다. V16 원본 코드·DATA 147개 파일은 SHA-256으로 결합된 원본 archive에 보존했고, 이전 테스트의 예상 의미와 실패 기준은 유지한다. 현재 V17의 새 proof도 validator 상수로 고정해 후보와 manifest를 함께 바꾸는 방식의 재기준화를 거부한다.

{link('양쪽 작성 의도 보존','MERGE-PRESERVATION.json')} · {link('인덱스 생성 근거','INDEX-REBUILD.json')} · {link('V17 변경 명세','V17-CUTE-DATA-PROOF.json')} · {link('실제 V17 검증','V17-VALIDATION.json')} · {link('전체 검사 결과','FINAL-REGRESSION-RESULT.json')}

전체 검사는 8개의 표준 unittest 프로세스로 모든 메서드를 실행했다. 처음에는 분리 작업트리에 Git ignored 과거 실험 기록이 없어 makeup 2개 메서드와 poverty 1개 메서드의 3개 subtest가 실패했다. main에 게시되어 있던 복원 기록의 SHA-256으로 원본 의존 파일 15개를 확인해 복사한 뒤, 해당 모듈과 같은 의존 관계의 rare-photo 모듈을 다시 검사한 28개가 PASS였다.

새 V17 helper의 구체적인 sibling skill 경로 참조도 기존 photo/illustration 소스 분리 검사 1개에 걸렸다. 기존 V14–V16과 같은 방식으로 동결 회귀 명세에서 외부 DATA 경로를 읽도록 수정하고 validator의 descriptor hash 결합만 갱신했다. 관련 모듈 분리·V17·기존 이력·현재 snapshot·universal contract 검사를 다시 실행하고 실제 V17 명령도 재검증했다. DATA, pack, 테스트 소스, 기대 결과는 변경하지 않았다. 초기 전체 로그, 원본 의존 파일 재검사와 경로 수정 뒤 재검사 로그를 모두 보존한다. 최종 통과는 전체 실행과 두 재검사 결과를 합친 결과이며 모든 메서드는 실행되었다.

원래의 독립 이미지 테스트와 판정은 그대로 보존했다. 공방 PASS, 등불 축제 BLOCKED_UNSCORED, 박물관 FAIL이며 사용자 수락은 pending이다. 이번 main 통합 과정에서 새 이미지를 생성하지 않았고, 원본 픽셀 결과를 현재 통합 DATA의 품질 향상이나 사용자 수락 증거로 확대하지 않았다.

캐시 작업 파일과 원래 작업 폴더의 다른 연구 변경은 이 배포에 포함하지 않는다. 원래 main을 동기화할 때는 먼저 이번 작업 파일과 working index를 별도 검증 backup으로 보존하고, 이미 게시한 경로만 정리한 뒤 fast-forward한다. 기존 미커밋 authored DATA는 유지하고 그 DATA에 맞는 working index를 보존한다. 배포 검증은 분리된 깨끗한 main 상태의 결과다.
'''
(HERE/'REPORT.md').write_text(report)
print(tests)
