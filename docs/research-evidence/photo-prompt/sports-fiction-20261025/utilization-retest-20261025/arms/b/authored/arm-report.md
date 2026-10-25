# 스포츠 후보 실제 활용 재검증 B

피겨 스케이팅 독립 기준안을 후보 접근 전에 동결한 뒤, 발행된 U03을 실제 프롬프트에 추가해 native image_gen 1회로 테스트했다. 저장 원본에서 U03의 세 부분이 모두 보였고, 관리형 검토 기록의 technical qualification도 PASS다. 사용자 판단은 pending이다.

| 단계 | 결과 |
| --- | --- |
| 독립 baseline | 312 words, 8 features, ownership warning 0 |
| 고정 runtime | f5905cd6954bd25e4d396d58ce7cbb4ceda1ed94e971c1001a5bf849c961a940 |
| 실제 검색 | action / contact_point / narrative_phase + topic + baseline, 총 5 queries |
| 발행 | 40 occurrences / 35 unique sources |
| 보강 세트 발행 | changed 5 + new 2 = 7 unique / 9 occurrences |
| 실제 retained inspiration | U03 1 unique / 1 occurrence |
| native contractual selection | 0; H-F2 material inspiration과 구별 |
| 비교 | baseline + 14개 완성형 대안, 35개 소스 각각 검토 |
| 이미지 호출 | native image_gen 1회, 원본 참조 실제 전달 |
| 프롬프트/실행 입력 감사 | PASS; authored generic anchors 보존에 관한 nonblocking warning 3개 |
| 원본 픽셀 관찰 | U03 3/3 visible PASS; embodiment 5/5 visible PASS |
| 관리형 검토 감사 | record valid, technical qualification PASS |
| 사용자 | pending / not_yet_received; 비교 baseline 렌더 없음 |

실제 사용 소스는 `cand_4f9d675ddaee543b9ad5a6fe777b7a23`, RID `base`, source SHA256 `9fa4151094fb3b6799ee9afa0247d93fa434ac270a17a1dcd4fc9aa2d2c57e9e`다. 기존 white figure skates와 지지 blade라는 일반 표현에 부츠 밑창·높은 굽, 금속 마운트, 하나의 강철 runner, 빙면 접점을 연결한 문구를 추가했다. 정확한 추가 문구는 utilization.json과 final_prompt.txt에 저장했다.

같은 원본에서 밑창과 높은 굽이 마운트 위에 구별되고, 마운트가 같은 부츠를 하나의 날에 연결하며, 날 아래 모서리는 얼음에 닿고 밑창은 떠 있는 것이 보인다. 실제 원본 SHA256은 `dcea6c866e157e0e2c9d88d913c5984f68f254ea6c5b395070fa56e12ef599f5`, 크기는 1237×1272다. 이미지 경로: `/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/sports-fiction-20261025/utilization-retest-20261025/arms/b/original.png`.

작은 차이는 별도 기록했다. 프롬프트의 white boot sole은 흰 부츠 상부와 갈색 밑창/굽으로 표현되었다. U03 소스 자체는 밑창 색을 요구하지 않으며, 세 구조 관계는 보인다. 단순한 연습 드레스에는 반짝이는 장식이 추가되었다. 한 프레임이 앞선 기술 순서, 실제 신원, 기술 수준, 결과를 입증하지는 않는다.

이번 선택은 유효한 데이터 사용 변형의 실제 실행 가능성을 검증하기 위한 것이다. 렌더하지 않은 baseline 대비 미적 향상을 입증했다고 주장하지 않는다. 참조는 얼굴·헤어의 보이는 단서를 안내했고, 실제 신원 동일성을 주장하지 않는다.

실행 ledger는 `image_runs.ndjson`, 독립 manifest는 `run_manifest.json`이다. ledger run ID는 `8f693e60d9a9dc01`이며, tool=`image_gen`, environment=`native_imagegen`, candidate format=`h-f2-v2`, image_call_count=1, cross_arm_inputs_used=false다. skill authored/review SHA는 모두 `d666eb93c9335508f0e5db27efa90b8915e9638eeda694703de05df8a0446957`이고, 최초 읽기 시각을 해시가 독립 증명한다고 주장하지 않는다.
