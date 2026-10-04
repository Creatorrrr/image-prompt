Arm B는 한 번의 네이티브 이미지 생성과 원본 픽셀 검증까지 완료했다. 최종 all-of 결과는 **FAIL**이다. 독립 평가 9개 중 4 PASS, 4 FAIL, 1 UNOBSERVABLE이며, UNOBSERVABLE도 실패로 계산했다. 원래 프롬프트나 평가 기준을 결과에 맞추어 바꾸지 않았다.

독립 무작위 장면은 성인 무대 의상 수선사가 동료 망토의 끊어진 금색 braid를 자신의 앞치마에서 분리하는 순간이다. 장소·역할·사건·손 접점·면 방향·시선·프레이밍은 agent-owned 테스트 설계다. 공통 requester bytes와 coordinator envelope만 requester 출처로 사용했고, 이 설계는 사용자 정의나 required semantic assertion으로 relabel하지 않았다. 다른 arm, 이전 프롬프트, 유지보수 리서치와 fixture는 읽지 않았다.

| 증거 층 | 실제 결과 |
| --- | --- |
| 데이터 존재 | `se_small_garment_fold_pinch`와 보강된 `pv_side_eye` 대체 표현이 존재한다. 자기 라펠 접촉은 상대 망토 끈 접촉과 별개다. |
| 정상 팩 노출 | 작은 fold pinch는 contact_point에 노출되지 않았다. `se_edge_on_hand_to_camera`는 노출됐지만 손바닥·손등 정면 방향과 다르다. 새 se 시각 프로필은 0개 노출됐다. |
| 후보 선택 | `slot:gaze_engagement:pv_side_eye` 1개 선택. edge-on 후보는 형태 불일치로 거절했다. counterorientation 후보는 선언된 source effects가 비어 필수 감사에서 실패하여 선택에서 제거했다. 실패 감사와 당시 composed를 보존했다. |
| 하드 의무 | se 시각 프로필 의무는 활성화되지 않았다. 기존 embodiment 5개 게이트가 적용됐다. 독립 9개 테스트 게이트는 별도 평가다. |
| 프롬프트·런타임 | 325-word baseline을 바이트 그대로 유지했다. 최종 compose PASS, runtime PASS이며 원본 첨부 1개의 경로·해시를 실제 native args에 바인딩했다. |
| 네이티브 호출 | `image_gen.imagegen`, 1회, 이미지 반환 성공. 관찰되지 않은 image model 이름은 기록하지 않았다. 원본은 1536×1024이고 저장 복사본과 해시가 같다. |
| 원본 픽셀 | 두 손의 소유와 자기/상대 옷 접점은 상당 부분 읽히지만 카메라를 향하는 손의 면은 두 손 모두 반대로 생성됐다. 상대 braid 아래 검지 hook은 관찰 불충분이다. |
| 사용자 판단 | 직접 수락·비교 선호는 아직 받지 않았다. |

| 독립 게이트 | 결과 | 원본 관찰 |
| --- | --- | --- |
| 얼굴·머리 참고 | PASS | 검은 턱 길이 bob, 나뉜 앞머리, 어두운 눈, 턱선·입술의 보이는 형태가 새 작업실 사진에 반영된다. 정체성 일치 판단은 아니다. |
| 성인 작업실 장면 | PASS | 성인 두 명, 의상 작업대·실·의상 랙과 수선 맥락이 보인다. 수치 나이는 픽셀로 확인할 수 없다. |
| 자기 apron 집기 | PASS | 주인공 오른손 엄지·검지가 자신의 apron 위쪽 가장자리와 국소 주름을 집는다. |
| 오른손 palm-to-camera | FAIL | 자기 apron을 잡는 손은 손등·손마디가 카메라를 향한다. |
| 상대 braid 아래 검지 | UNOBSERVABLE | 상대 cape에 연결된 금색 끈을 손가락으로 잡지만 검지가 그 아래로 걸린 메커니즘을 별도로 분명히 볼 수 없다. |
| 왼손 dorsum-to-camera | FAIL | 상대 끈을 잡는 왼손은 손바닥이 카메라를 향한다. |
| 고개 회전 + lens glance | PASS | 오른쪽 동료 방향으로 약하게 돌아선 고개와 카메라를 향한 눈 방향이 함께 보인다. |
| brooch 아래 두 frayed ends | FAIL | frayed 부분은 손 쪽 라펠에 있고 star brooch는 반대편 장식 끈에 있다. 같은 brooch 아래 두 짧은 끝의 관계가 성립하지 않는다. |
| 양 머리·upper-hip framing | FAIL | 손목·전완과 접점은 보이지만 남성의 정수리가 상단 경계에서 잘렸다. 부분 충족은 실패다. |

기존 embodiment 검사는 소유·관절 연결·지지 3개 PASS, 접촉 메커니즘·투영 2개 FAIL이다. 리뷰 기록의 schema failures는 0이고 `technical_qualified=false`다. 사진 전체의 따뜻한 작업실 분위기, 관객을 돌아보는 시선과 옷 재질은 의도한 사진 방향을 잘 지지하지만 손 방향과 엄격한 상호작용 fidelity 실패를 대신할 수 없다.

작은 fold pinch와 시선 형태가 픽셀에 나타났다는 사실은 반영한 데이터가 그 결과를 유발했다는 증거가 아니다. 전자는 해당 후보가 정상 팩에 노출되지 않았고, 두 형태 모두 retrieval 이전의 독립 baseline에 이미 있었다. 반영 전·후 이미지 비교가 없으므로 통합의 인과 개선이나 새 시각 프로필 전체 PASS는 주장하지 않는다.

원본 이미지: [original.png](generated_images/backstage-snapped-braid-native-1/original.png). 주요 기록: [프롬프트](final_prompt.txt), [후보·노출·선택](retrieval_exposure_selection.json), [런타임 감사](runtime_audit.json), [독립 픽셀 평가](independent_pixel_review.json), [embodiment 평가 감사](render_review_audit.json), [run manifest](run_manifest.json), [요약](qualification_summary.json).

Pack `ac476ded4e547dab`; baseline SHA-256 `4292bdb541e749e65bd8fef694e6fff246082f0baa4ae9b727b78f95d87ac536`; 원본 이미지 SHA-256 `821532369caf4d10cb3500dcafb373aafd5f671fe28c302f7d6894129aa7deda`.
