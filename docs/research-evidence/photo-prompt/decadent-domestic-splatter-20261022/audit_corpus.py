"""Read source; write snapshots only in this research directory. No inference."""
import collections,hashlib,json,pathlib,re,subprocess,datetime
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[3]
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
def sha(x):return hashlib.sha256(x).hexdigest()
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
PATTERNS={
 'decadence_names':r'decaden|퇴폐|유미주의|aestheticism',
 'control_names':r'coercive|gaslight|강압적 통제|가스라이팅|DARVO',
 'access_names':r'enfilade|앙필라드|service corridor|하인 복도|keyhole|열쇠구멍',
 'collection_anatomy_names':r'wunderkammer|anatomical venus|écorché|anthropoderm|분더카머|해부학적 비너스|에코르셰|인피 장정',
 'body_damage_names':r'dismember|flaying|eviscer|mutilat|신체 절단|박피|적출',
 'textile_names':r'damask|brocade|새틴|satin|patina|고색|벨벳',
 'vanitas_mourning_names':r'vanitas|바니타스|mourning|애도 장신구|hair.*locket',
 'giallo_guignol_names':r'giallo|지알로|guignol|기뇰',
}
# Dispositions are research recommendations, pending complete source qualification.
SELECTED={
 'cand_b8ea917907aa5ba7b3f86dc4b1c1aafb':('refine','E08,F10','공연 프레임은 재사용 가능성이 있으나 실제 보철 접착 경계는 원문에 구체적이지 않다.'),
 'cand_ad31ba5a8a43517cab27883121598b0a':('refine','C04','불완전 목격의 기존 관계를 보존하며 시야·가림·행위자 끝점을 더 명확히 검토한다.'),
 'cand_aa2452faf3f0562aa153d6dadcba23db':('reuse','A03,D01','파일 방향·압박 반응 자체는 기존 의미를 우선 재사용. 의복 소유자가 의자에 그대로 전용될 수는 없다.'),
 'cand_3606cfccad1a5ed5b4982c8d9569a773':('refine','A03,A05','그을음은 파일 마모·먼지와 다르므로 표면 원인과 소유자를 분리한다.'),
 'cand_d4559d47b9a85aa3a002287216e3e843':('refine','A01,A02','tarnished gold-leaf라는 짧은 명칭을 순금 부식으로 확장하지 않게 기재·손실·부착물 구분 필요.'),
 'cand_0319d46abb0753fd80ede0a2a7c34c67':('refine','F01,F03','원문은 분리된 부분과 신체 간격이다. Evisceration은 내부 구조/공동 관계가 필요하므로 동의어 합산 금지.'),
 'cand_03674dc910e55de58a74f6cbec6b10e8':('refine','F03,F04','공동·외부화·분리 상태를 실제 원문과 대조해 적출과 돌출을 구분한다.'),
 'cand_4fdbddb05d8e551cbd5bb77caeb96732':('refine','F02,D06,G06','피부·직물·모형 패널을 구별하고 같은 몸의 경계를 유지해야 한다.'),
 'cand_1e347f2d50bf5bf58c6682c7a4246d73':('refine','B02,B03','기존 crime-tag 선행조건이 있는 공간. 가정 통제 의미를 위해 그 guard를 우회해선 안 된다.'),
 'cand_0cf82fd67fdb52448da27bd8314dfd00':('context','H08','거부·철회·강압의 선언 의미를 유지하되 비성적 출입 제한의 일반 재료로 자동 전용하지 않는다.'),
 'cand_3fcbad4793095196924a064c29ed78ad':('reuse','B08','공적/직원 구역 분리의 기존 의미는 검토 후 재사용; 역사적 하인·공모는 새 사실이다.'),
 'cand_3387ca0978a65fbc8539c2d9edbe4864':('refine','C02','비네트는 물리적 문과 열쇠구멍의 깊이/경계를 충족하지 않는다.'),
 'cand_d463e45a07805a509f35e518769b343e':('reject_neighbor','C02','이 키홀은 의복 목선 아래의 구멍이다. 문/관음 의미에 부적합하다.'),
 'cand_509be0e782ac5916aefd52e4124f62f8':('refine','C01','거울로 대상을 보는 의미는 있으나 실물-반사 대응과 프레임 경계를 보완 검토한다.'),
 'cand_2d636a13fb4d5e20ae728f5f9c8c5311':('reuse','C01,B12','반사 공간의 소유자 관계를 검토 후 재사용. 셀피폰을 타 장면에 강제하지 않는다.'),
 'cand_2376c7d9fc995f969f8177440f2e7c1a':('refine','C01','시점 라벨만으로 어느 반사가 누구인지 확정하지 않는다.'),
 'cand_14bcc760a5bd562abb1f847b2a8caa80':('refine','C08,B05','집안 기록·계보·열쇠는 존재하지만 수정 전후나 혈통 진위를 증명하지 않는다.'),
 'cand_a3a40af2673e5d0c8ddfd704534b61b2':('reuse','B01,B03','특정 자원 출입장치와 키 권한의 연결은 우선 검토. 법적 권력·가족 폭력으로 확장하지 않는다.'),
 'cand_19669cd1b116565eb8316bfcb47a112a':('refine','A01,A03,E03','faded luxury residue는 어느 물건의 어느 표면인지 추가로 명확해야 한다.'),
 'cand_3044467fb69652dfbba296cc69578e7c':('refine','F05,F06','잔해 변색·구조 변화와 살아 있는 몸의 괴사 진단은 다르다.'),
 'cand_b13d77701e8f56f6860fefee02304549':('reuse','D06','의복 섬유·같은 천의 경계는 재사용 우선. 아래 피부의 상태까지 자동 지원하지 않는다.'),
 'cand_c7c3eae3d2b95445ab7dd0c5bda35228':('refine','E03,E06','붉은 얼룩·의자·가방은 사건 단서. 실제 피·피해자·스플래터의 온전한 대체 아님.'),
 'cand_57f134b9ba7056caa69ab466b10a2277':('reuse','E01,A07','빈 의자·시든 꽃·그릇은 이미 존재하는 관계. 부재자의 사망·추방을 붙이지 않는다.'),
 'cand_eb165802b276591084b42c4285daa130':('refine','G10','새 음식·시든 꽃·꺼진 촛불이 있으므로 vanitas 어휘 0건을 의미 부재로 해석하면 안 된다.'),
 'cand_9d5d5004e35a5a8396b88df1b49d099b':('reuse','G11','기념함 위 꽃의 접촉은 재사용 가능성이 있으나 실제 시신·성적 의미·유품함 내부는 지원 안 됨.'),
 'cand_207c5ff457c75a92affdf62476a17231':('refine','D09','도자기 인형 관절이라는 기존 의미에 진열 받침/별도 신체 소유자를 검토한다.'),
 'cand_244633c6683c50248bf9c404272b552c':('reuse','E02','식기 자체는 재사용 우선. 물건 하나가 식사 통제·고급 요리·식인을 뜻하지 않는다.'),
 'cand_6d54ff31448d5479928903bc0fb60692':('reject_neighbor','A01','종교 아이콘 금박 패널과 세속 액자의 박락은 다른 의미/물건이다.'),
}

def main():
    raw=(ASSETS/'photo_candidate_corpus_manifest.json').read_bytes();manifest=json.loads(raw)
    rows=[];bindings=collections.defaultdict(list);hashes={}
    for m in manifest['modules']:
        b=(ASSETS/m['file']).read_bytes();hashes[m['file']]=sha(b);data=json.loads(b)
        if m['kind']=='candidates':rows.extend((cid,r,m['file']) for cid,r in data['candidates'].items())
        elif m['kind']=='slot_bindings':
            for binding in data['slot_bindings'].values():bindings[binding['candidate_id']].append(binding)
    by_id={cid:(r,f) for cid,r,f in rows};patterns={}
    for key,pat in PATTERNS.items():
        hits=[]
        for cid,r,f in rows:
            c=r['content'];fields=[k for k in ('en','ko','additional_details') if re.search(pat,str(c.get(k,'')),re.I)]
            if fields:hits.append({'candidate_id':cid,'module':f,'record_kind':r['record_kind'],'matched_fields':fields,'en':c.get('en',''),'ko':c.get('ko','')})
        patterns[key]={'regex':pat,'count':len(hits),'matches':hits}
    selected=[]
    for cid,(disposition,cards,why) in SELECTED.items():
        r,f=by_id[cid]
        selected.append({'candidate_id':cid,'module':f,'record':r,'record_sha256':sha(canonical(r)),'module_sha256':hashes[f],'bindings':bindings[cid],'related_cards':cards.split(','),'proposed_disposition':disposition,'rationale_ko':why,'native_source_qualification':'NOT_RUN','actual_rank':None,'role_adoption':'NOT_RUN'})
    kinds=dict(collections.Counter(r['record_kind'] for _,r,_ in rows))
    drift=[f for f,h in hashes.items() if sha((ASSETS/f).read_bytes())!=h]
    audit={'schema':'decadent-domestic-splatter-corpus-audit/v1','captured_at_kst':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat(),'candidate_count':len(rows),'positive_count':len(rows)-kinds.get('diagnostic',0),'record_kinds':kinds,'binding_count':sum(map(len,bindings.values())),'module_count':len(manifest['modules']),'source_manifest_sha256':sha(raw),'source_module_sha256':hashes,'changed_during_read':drift,'fields':['content.en','content.ko','content.additional_details'],'excluded_fields':['aliases','definition','embedding_text','tags','conditions','research_semantics','native_proof'],'patterns':patterns,'limit':'Lexical scan only. Zero is not semantic absence; matches are not retrieval exposure or semantic qualification.'}
    (HERE/'CORPUS-LEXICAL-AUDIT.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
    (HERE/'existing-source-mapping.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2)+'\n')
    check=subprocess.run(['python3',str(ROOT/'skills/photo-prompt-image-generator/scripts/photo_installed_h_f2.py'),'--check-runtime'],cwd=ROOT,text=True,capture_output=True)
    observation={'read_only_installed_check':json.loads(check.stdout) if check.returncode==0 else {'exit_code':check.returncode,'output':check.stdout,'stderr':check.stderr},'retrieval_runtime':json.loads((ROOT/'skills/photo-prompt-image-generator/retrieval-runtime.json').read_text()),'limit':'Existing release import/dependency observation only; no research source activation or retrieval.'}
    (HERE/'RUNTIME-OBSERVATION.json').write_text(json.dumps(observation,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'records':len(rows),'kinds':kinds,'modules':len(hashes),'snapshots':len(selected),'counts':{k:v['count'] for k,v in patterns.items()},'changed_during_read':drift},ensure_ascii=False))
if __name__=='__main__':main()
