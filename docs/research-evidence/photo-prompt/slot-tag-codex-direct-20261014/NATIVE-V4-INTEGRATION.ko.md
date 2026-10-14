# Native v4 조건·프로필 통합 검증

후보의 원본 조건, 선택 분기, 표시 관계, 실제 선택한 의존 후보의 조건을 함께 검사하도록 보강했다. 참조 외형과 요청자 정체성은 명시적 입력·범위 대장에 결합하며, 이미 정해진 값의 보존과 새 변경 효과를 구별한다. 조건부 프로필은 실제 선택한 RID의 본문·의무·최종 render gate만 사용한다. 일반 후보의 소유자를 임의로 주인공이나 전경으로 정하는 기능은 추가하지 않았다.

루트는 변경 코드를 검토하고 별도 새 프로세스에서 293회 실행, 고유 테스트 263개, 하위 사례 570개를 확인했다. 실패·오류·skip은 0건이다. OS에서 네트워크를 차단하고 provider 키를 제거했다. 스킬 quick_validate, 변경 18파일·유지 11파일의 worker hash 대조와 Python AST 검사도 통과했다. worker의 이전 동시 편집 중 `runtime_restart_required` 오류와 이후 새 프로세스 통과 기록은 인계 문서에 보존했다.

실제 원본 18,250개, positive 18,180개, 운영 catalog 139개를 그대로 유지한 상태에서 전체 인덱스를 다시 구성했다. provider의 embed/embed_many를 호출 즉시 실패하도록 고정했고, 같은 로컬 공간의 벡터 18,180개를 모두 재사용했다. 새 임베딩 입력·provider 시도·Gemini 호출은 모두 0건이다. 전체 shard 폐쇄 검증 후 generation `1871bafa0e008e186ccce4e92908f2b177529b215c22e2fb46d07f0b28679bfd`를 발행하고 실제 acquire 및 원본 payload 일치를 확인했다. 인덱스 layout은 `f82ab43bc2a5a141ad1aedcc1f415b68737b9e5867af829a6c88d6750f27a285`로 동일하다.

이 커밋의 완료 범위는 실행 계약, fixture 회귀와 실제 인덱스·runtime 통합이다. 운영 후보 native 자격화는 여전히 0개이며, 최종 142개 catalog 적용, 실제 frozen-core 전체 슬롯 질의, 전수 최신 의미 승인 및 단계 6–8 완료는 포함하지 않는다. 연구용 실제 후보 판정은 별도의 입력·증빙·루트 승인으로 기록한다. 입력의 완전성과 의미 판정은 작성자의 주장이고, 문자/hash 검사는 이미지 픽셀이나 전문가 정답을 증명하지 않는다.

실행값은 `NATIVE-V4-ROOT-TEST-VERIFICATION.json`, `native-v4-runtime-01/PREFLIGHT.json`, `native-v4-runtime-01/VERIFICATION.json`에 보존했다. 재실행 도구는 `root_verify_native_v4.py`, 정확한 worker 계약·변경 목록은 `worker-notes/native-v4-final-handoff-20261014.md`와 같은 이름의 JSON이다. 부모 세션의 모델·effort는 확인되지 않은 값으로 기록하고, 실제 배정한 하위 작업자의 gpt-6.1-sol/high 선언과 구별한다.
