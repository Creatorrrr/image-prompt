# 럭셔리 시각 의미 5-arm 독립 렌더 테스트

## 결론

- 재현 랜덤 시드: `868462607`
- 조합 프롬프트 감사: `5/5 PASS`
- 정확한 렌더 요청 감사: `5/5 PASS`
- built-in imagegen 생성: `5/5 성공`, 팔별 `1회`, 재시도 `0회`
- 픽셀 하드 게이트: `23/25 PASS`
- 팔 단위 기술 통과: `3/5`
- 전체 스위트: `FAIL` — 모든 팔이 5/5여야 한다는 사전 규칙을 적용함
- 사용자 미학 판단: 아직 받지 않았으며 기술 판정과 별도임

## 팔별 결과

| Arm | 랜덤 복합 컨셉 | 대상 프로필 | 픽셀 결과 | 판정 |
|---|---|---|---:|---|
| 01 | 우천 궤도 페리 터미널의 외교용 케이스 공개 | conspicuous original house code | 5/5 | PASS |
| 02 | 고산 전파 관측소의 조약 방송 전 긴급 피팅 | bespoke tailoring individual pattern | 4/5 | FAIL |
| 03 | 침수 도시 위 보존 살롱의 지도 케이스 복원 상담 | private client service interaction | 4/5 | FAIL |
| 04 | 심해 잠수정의 조석 항법 브로치 세팅 | high jewelry setting integration | 5/5 | PASS |
| 05 | 폐관 플라네타리움의 무중력 공연 토일 피팅 | couture atelier individual construction | 5/5 | PASS |

## 실패 진단

1. **비스포크 손캔버스 내부**: 재킷 외부 베이스팅과 어깨 수정은 명확하지만, 뒤집힌 라펠 안쪽의 캔버스층이나 확실한 패드 스티치 면이 픽셀에 남지 않았다.
2. **프라이빗 서비스 애프터케어**: 세 가지 소재, 고객의 손상 지시, 장갑 낀 취급은 명확하지만, 빈 노트는 복원·수리·관리의 후속 기록임을 스스로 증명하지 못했다.

후보팩 강화 시에는 작은 내부 공정에 전용 초점 영역을 배정하고, 개인정보 없는 애프터케어를 `빈 문서`가 아니라 기능이 보이는 도식·체크리스트·매칭 샘플·기록 동작으로 표현하는 편이 적합하다. 이 테스트에서는 진단만 수행했으며 공유 스킬 데이터는 수정하지 않았다.

## 증거 경계

- 프롬프트 감사 PASS는 문구와 계약이 보존됐다는 뜻이지 픽셀 PASS가 아니다.
- 렌더 요청 감사 PASS는 실제 프롬프트·네거티브·참조 파일 바이트가 일치한다는 뜻이지 이미지 품질을 증명하지 않는다.
- 픽셀 판정은 각 이미지 원본, 320px 썸네일, 필요한 상세 크롭을 사용했다. 부분 반영은 실패로 처리했다.
- 참조 초상은 일반적인 성인 가상 인물의 헤어·얼굴 외형 연속성에만 사용했다. 동일인, 생체, 인종, 국적, 매력, 건강, 성격 판정은 하지 않았다.

## 재현 산출물

- 테스트 정의: `coordination/test_cases.json`
- 코디네이터 픽셀 검토: `coordination/coordinator_pixel_review.json`
- 개선 판단 기록: `coordination/iteration_record.json`
- 각 팔: `request_envelope.json`, `authorial_core.json`, `visual_intent.json`, `candidate_pack.json`, `composed_prompt.json`, `render_request.json`, `result.png`, `pixel_review.json`, `run_manifest.json`, `agent_result.json`
