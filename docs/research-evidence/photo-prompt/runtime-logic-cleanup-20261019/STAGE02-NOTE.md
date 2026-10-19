# 참조 분류 보정

초기 REFERENCE-REVIEW는 skills/data/runs 내부 봉인 소스를 working source로 잘못 분류했다.
FINAL은 실제 scripts/precore/tests 188개만 working source로 분류하며 초기 결과를 보존한다.
보호된 과거 소스의 호출은 유지해야 할 의존성으로 기록한다.
기존 literals.py 원문 1개는 파싱되지 않지만 대상 함수명은 없으며 원본은 수정하지 않았다.
9개는 재현 게이트를 통과하기 전까지 제거 승인 대상이 아니다.
