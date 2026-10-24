# surreal=3 재시험

현재 실제 사용자 요청은 `surreal 3 으로 테스트해줘.`다. 같은 사진 참고 범위로 새 독립 컨셉 세 개를 시험한다. 현재 실제 요청 원문·span과 이전 실제 사용자 요청(사진 활용·서로 다른 세 컨셉)의 문맥만 제공한다. 이전 이미지·프롬프트·후보 pack·다른 arm·유지보수 예시는 새 독립 초안의 재료가 아니다.

- 실행별 override는 `surreal: 3`만 둔다. 전역 저장 기본값을 변경하지 않는다. 다른 control은 기존 저장값을 사용한다.
- 강도 3은 초현실 관계가 사진의 주된 인상과 방향을 이끈다는 저술 지침이다. 이상한 소품 수, 문장 길이, 필수 디테일 수로 성공을 판정하지 않는다.
- 세 fresh author는 coordinator가 먼저 고정한 실제 current request envelope, 실제 이전 사용자 문맥, 제공된 reference와 허용된 현재 neutral precore만 보고 initial core(request_lineage=null)를 확정한다. 그 후 같은 설치 H-F2에서 source를 전체 검토하고 compose/native input 감사를 거쳐 각각 1장 생성한다.
- 이전 원본·실패·ledger는 보존하고 새 child run에 기록한다. 기존 사진을 다시 출력하거나 이전 prompt 끝에 `surreal 3`만 붙여 이번 설정의 실행으로 간주하지 않는다.
- 실제 reference bytes·역할·범위는 닫힌 context의 transport를 그대로 사용한다. 얼굴·헤어 외관 참고를 신원·실제 나이·성격 증거로 확대하지 않는다.
- 초현실 관계의 화면 내 주도성, 관측 가능한 접점·경계·소유 관계, reference 외관을 분리해 검토한다. 부분 구현과 관측 불가는 완전 관계 pass가 아니다.
- 이전 surreal=0 시험도 명시 surreal 주제를 보존해 강한 비현실 장면을 이미 포함했다. 저술과 확률적 생성이 다시 이루어지는 이번 시험은 설정 변경의 인과 효과를 정량적으로 추정하는 통제된 A/B 실험이 아니다. 실제 새 snapshot=3 바인딩과 결과의 주도성을 직접 확인하는 시험이다.

## 준비 경로 기록

처음에는 이전 실행과 연결하는 retry projection을 준비했다. 요청 근거 범위와 local-axis 형식을 고친 뒤 A projection은 representable이었으나, 생성된 execution_scope.preserved_controls는 이전 surreal=0을 담았다. 해당 준비는 이번3시험에 사용하지 않았다. 원본과 unused projection을 보존하고 이미지를 호출하지 않은 채 준비 프로세스만 종료했다. 이는 기존 픽셀 수정을 새 요청으로 위장한 것이 아니라, 사용자가 실제로 명시한 설정3을 처음부터 적용하는 새로운 독립 저술 시험이다. 기존 시나리오와 같은 장면의 A/B 비교는 수행하지 않는다.
