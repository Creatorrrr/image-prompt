# CAPRI 독립 렌더 평가

- 컨셉: 비가 갠 서울 옥상 온실의 코발트 블루아워 패션 사진
- 외형 참조 범위: 첨부 초상에서 관찰되는 성인 머리·눈·메이크업·차분한 표정만 참고. 신원, 동일인, 생체정보, 보호 특성, 성격은 추론하지 않음.
- 후보팩: v6, seed `26090131`, pack `a039fc89da641d86`
- 후보팩 보강: 온실의 수렴하는 화분열·지붕 골조 구도, 온실 지붕의 확산광과 따뜻한 밑단 윤곽광
- 국내 여름 요소: 리브드 핏 탱크, 얇은 스트라이프 오버셔츠, 블랙 카프리 팬츠, 로우프로파일 포인티드 발레 플랫, 레몬 미니백
- 호출: built-in imagegen 1회, 재시도 없음
- 보존 이미지: `generated_capri.png` (`1023x1537`, SHA-256 `dd03e2df1921d8cc0d37e3dc4c571c92428de34e34d51ffc356cada24ac2afb3`)

## 증거 레이어

- Candidate pack 생성: PASS
- Composed prompt audit: PASS (`uncovered_intent` 3건은 코어 문구가 프롬프트에 그대로 보존되었다는 비차단 경고)
- Runtime request audit: PASS
- Generation delivery: SUCCESS, concrete local PNG 보존
- Rendered-pixel review: 5/5 PASS
- 사용자 취향 판정: PENDING (`not_yet_received`)

## 하드 게이트

| Gate | Scale | 판정 | 픽셀 근거 |
|---|---|---|---|
| `vo_summer_capri_two_trouser_legs` | thumbnail | PASS | 축소본에서도 가랑이부터 보행 간격까지 검은 하의가 두 바지통으로 분리되어 읽힘 |
| `vo_summer_capri_paired_below_knee_hems` | both | PASS | 양쪽 실제 밑단이 각각 무릎 아래 종아리 부근에서 끝남 |
| `vo_summer_capri_clear_ankle_gaps` | both | PASS | 두 밑단에서 두 발목까지 맨다리 구간이 각각 연속적으로 보임 |
| `vo_summer_capri_landmarks_unobstructed` | native | PASS | 양쪽 무릎 위치, 밑단, 발목, 포인티드 플랫이 원본에서 동시에 추적 가능함 |
| `vo_summer_capri_not_bermuda_or_ankle_crop` | native | PASS | 무릎보다 충분히 아래인 밑단과 긴 종아리-발목 노출이 함께 보여 버뮤다·발목 크롭·풀렝스·카메라 절단이 아님 |

## 결론

`visual_technical_qualified_user_judgment_pending`. 프롬프트와 런타임 통과를 픽셀 통과로 대체하지 않았으며, thumbnail/native 실제 검사에서 다섯 구성 관계가 한 이미지 안에 모두 확인됐다. 이 한 장의 성공은 CAPRI 프로필의 보편적 렌더 성공이나 사용자 선호를 증명하지 않는다.
