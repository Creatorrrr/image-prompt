# 최신 main의 기존 블라인드 장면 재검증

`6b9381a0585049cbaca1522dde405b4e6203b295`에서 원래 자격 확인 핀 `6c2cc0f9311ee4c9c6a376781e3ea599d7bb6d14`의 동일한 12사례를 원본·속성 교정 양쪽으로 다시 실행했습니다.

- 공개 CLI 24/24 성공, 고정 입력 96개·원문/런타임 312개 해시 유지
- 4사례의 후보 구성 변경, arm별 합계 749→750개. 모든 팩이64개인 것은 아님
- 교정 arm의 ineligible 22→21은 후보 교체 결과이며 정확도 향상으로 해석하지 않음
- 기존 category·focal query·공유64개 cap·missing affected_properties 문제 유지
- upward view의 worm’s-eye broad rank는5→4지만 focal 교집합에서 여전히 제외
- 공개 순서는 seed 기반 비선호 순서이며 검색 순위가 아님

002의 reflection 후보 교체는 요청하지 않은 별도 반사 행동을 제안하므로 개선으로 보지 않았습니다. 004는 선택 가능한 위치 하나 증가, 010은 교체 전후 모두 부적격, 011은 affected_properties가 없는 gobo가 들어와 적격 수가 늘어난 것으로 guard 개선의 증거가 아닙니다. 실제 production loader와 과거/현재 생산 경로를 비교했고 자세한 순위·교집합·cap 자료는 DETAILS.md와 압축 자료에 보존했습니다.

이 결과는 upstream acting/neutral과 이후 DATA 수정의 합친 변화입니다. 개별 주기의 인과 효과나 자연어 정확도·최종 프롬프트·픽셀 품질·전체 회귀 완료를 주장하지 않습니다. 소스/fixture/런타임 수정·API 호출 없이 실행했습니다. 원래 실패한 입력 작성 이력과 수정된 arm 모두 유지했습니다.

공개 압축은 원본 내보내기의 로컬 경로를 정규화했고 publication-manifest.json이 공개 바이트의 해시를 제공합니다. 원본 패키지 SHA-256은 `dc7896f3d9ec2fa3d6ad2eeb572f9fcc313fa2e027c22a365798cbc591f6794c`입니다.

공개 아카이브 SHA-256: `87382659fac024b0174fc4e4f7062786c7340e2f6367a01e91dcd2a34b306e85`
