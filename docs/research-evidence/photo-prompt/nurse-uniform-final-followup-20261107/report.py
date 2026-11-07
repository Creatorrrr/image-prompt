import json
from pathlib import Path
R=Path('/Users/chasoik/Projects/image-prompt');A=R/'skills/photo-prompt-image-generator/assets';O=Path(__file__).parent
r=json.loads((A/'photo_nurse_uniform_final_followup_review_20261107.json').read_text())['rows'];sem=json.loads((A/'photo_nurse_uniform_final_followup_semantics_20261107.json').read_text());cards={x['candidate_id']:x['id'] for x in sem['cards']};cards.update({v:'진단 D'+k for k,v in sem['diagnostic_ids'].items()});cards['cand_1cc1ddabe95952d992cb345b76a8cf4f']='기존 진단 D285';out=['# 간호복 미확인 36개와 시각 보류 1개 후속 조사','','2026-11-07. 직전 조사에서 새 외부 출처가 없던 36개 및 그 밖의 보류 285행 1개를 대조했다. 37행 모두 관련된 새 자료를 하나 이상 기록했다. 사전 뜻이나 특정 제작·상품·사진 사례, 포즈의 한 요소만을 뒷받침하는 부분 자료가 많다. 복합 의미 전체가 검증됐다는 뜻이 아니다.','', '연구 전용 맥락 37개와 시각 의미 카드 25개, 새 선택 후보 25개, 진단 후보 3개, binding 25개, 원본 결합 양성 검색 뷰 50개를 작성했다. 기존 후보 7개를 8개 행에서 부분적으로 재사용한다. 262·263·264·285는 이번에 새 양성 후보를 추가하지 않은 연구 맥락 전용이다. 285의 이전 앞치마 단독 후보는 표현 전체와 다르다.','', '285의 용어 정의는 일본어 사전으로 추가 확인했지만 단일 사진에서 가려진 의복의 부재나 나이는 확인할 수 없어 전신 의미에 대한 시각 보류를 유지한다. 용어 정의 확인은 성인 인증이나 사진 증거가 아니다.','', '## 행별 근거와 연결','', '| 행 | 출처가 뒷받침하는 범위 | 후보 연결 |','|---|---|---|']
for x in r:
 src=x['additional_sources'][0];a='['+src['title']+']('+src['url']+') — '+src['supported_scope_ko'];c=[]
 for cid in x['linked_candidate_ids']:c.append(cards.get(cid,'기존 '+cid))
 if x['source_row_id']=='NURSE-ROW-285':c.append('보류; 기존 앞치마 단독 형태만 별도')
 out.append('| '+x['source_row_id'][-3:]+' '+x['source_term_label'].replace('|','/')+' | '+a.replace('|','/')+' | '+(', '.join(c) if c else '연구 맥락 전용')+' |')
out += ['', '## 검증과 한계','','선택 후보는 요청의 의도·범위에 맞을 때만 검토하는 독립적인 한 가지 시각 실현이며 출처 자체가 후보의 전체 형태나 native 채택을 승인하지 않는다. 기존 후보 재사용은 일부 의미의 연결이고 완전 동등성은 보장하지 않는다. 특히 정지 이미지에서 움직임의 전후, 실제 의도·감정·연령·동의·직업이나 보이지 않는 재료는 확정하지 않는다. 코스프레와 실제 간호복도 구분한다.','', '자동 검사: 관련 테스트 22개 통과, 12개 스킵, 하위 검사 4개 통과. 인덱스 검증과 설치 결과는 완료 후 기록한다. 이미지 생성과 픽셀 검증은 수행하지 않았다.']
(O/'README.md').write_text('\n'.join(out)+'\n')
