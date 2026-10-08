# 병합본 전체 검사 결과

224개 모듈 중 202개 통과, 22개 실패. 발견 2,031개 / 실제 보고 1,947개. 84개 발견 사례는 class setup 중단으로 실행되지 않았다.

불/후보/transport/capture 관련 검사 35개는 별도 통과했다. 전체 검사를 통과로 표기하지 않는다. 기존 source 보존 증거는 byte 보존을 입증하며 모든 실패의 기존 발생 여부를 입증하지는 않는다. 과거 기대값을 새 current 결과로 교체하지 않았다.

| 모듈 | 분류 | 확인된 오류 |
|---|---|---|
| `test_photo_appearance_boundary_history` | sealed_skill_and_refreshed_index | AssertionError: Frozen V24 historical source payload drift: skills/photo-prompt-image-generator/SKILL.md; AssertionError: Frozen V35 retained live source payload or mode drift: skills/photo-prompt-image-generator/assets/photo_prompt_visual_profile_index.json |
| `test_photo_character_appearance_100` | sealed_existing_source | AssertionError: Frozen V35 retained live source payload or mode drift: skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json |
| `test_photo_ct073_back_band_data` | sealed_existing_source | AssertionError: Frozen V24 historical source payload drift: skills/photo-prompt-image-generator/assets/photo_prompt_character_moe_extension.json |
| `test_photo_ct073_boundary_history` | sealed_existing_source | AssertionError: Frozen V24 historical source payload drift: skills/photo-prompt-image-generator/assets/photo_prompt_character_moe_extension.json |
| `test_photo_cute_visual_forms` | curated_inventory_missing_dependency | ValueError: context extension references unknown entry texture.vg_faille_crossgrain_ribs |
| `test_photo_data_scope_boundary_history` | sealed_existing_source | AssertionError: Frozen V35 original source payload or mode drift: skills/photo-prompt-image-generator/SKILL.md |
| `test_photo_data_scope_v34_boundary_history` | sealed_existing_source | AssertionError: Frozen V35 original source payload or mode drift: skills/photo-prompt-image-generator/SKILL.md |
| `test_photo_ethereal_gothic_scene` | curated_inventory_missing_dependency | ValueError: context extension references unknown entry texture.vg_faille_crossgrain_ribs |
| `test_photo_horror_main_boundary_history` | sealed_existing_source | AssertionError: Frozen V24 historical source payload drift: skills/photo-prompt-image-generator/SKILL.md |
| `test_photo_krummholz_korean_alias_data_cleanup` | historical_bundle_metadata | AssertionError: Lists differ: [{'id[532808 chars]인', '초점 영역의 채도가 주변만큼 높아져 채도 차이가 사라짐'], 'relati[703605 chars]ly'}] != [{'id[532808 chars]인', '배경도 함께 선명해짐'], 'relations': [], 'adoption[703586 chars]ly'}] |
| `test_photo_muted_color_boundary_history` | sealed_existing_source | AssertionError: Frozen V24 historical source payload drift: skills/photo-prompt-image-generator/SKILL.md |
| `test_photo_palette_boundary_history` | sealed_existing_source | AssertionError: Frozen V35 original source payload or mode drift: skills/photo-prompt-image-generator/SKILL.md |
| `test_photo_portrait_fashion_exposure` | existing_profile_projection | AssertionError: {'id'[1443 chars]uous']}, 'runtime_expression': {'default_mode'[2429 chars]}}]}} != {'id'[1443 chars]uous', '성인의 한 어깨에만 연결된 의복 지지가 있고 반대 어깨는 연속된 비대[2804 chars]}}]}} |
| `test_photo_protostar_korean_alias_data_cleanup` | historical_bundle_metadata | AssertionError: Lists differ: [{'id[532808 chars]인', '초점 영역의 채도가 주변만큼 높아져 채도 차이가 사라짐'], 'relati[703605 chars]ly'}] != [{'id[532808 chars]인', '배경도 함께 선명해짐'], 'relations': [], 'adoption[703586 chars]ly'}] |
| `test_photo_robe_source_boundary_history` | sealed_existing_source | AssertionError: Frozen V35 original source payload or mode drift: skills/photo-prompt-image-generator/SKILL.md |
| `test_photo_runtime_boundary_history` | sealed_existing_source | AssertionError: Frozen V24 historical source payload drift: skills/photo-prompt-image-generator/assets/photo_prompt_character_moe_extension.json |
| `test_photo_scene_budget_boundary_history` | sealed_existing_source | AssertionError: Frozen V24 historical source payload drift: skills/photo-prompt-image-generator/SKILL.md; AssertionError: Frozen V24 historical source payload drift: skills/photo-prompt-image-generator/assets/photo_prompt_character_moe_extension.json |
| `test_photo_shelf_return_korean_state_data_cleanup` | historical_bundle_metadata | AssertionError: Lists differ: [{'id[532808 chars]인', '초점 영역의 채도가 주변만큼 높아져 채도 차이가 사라짐'], 'relati[703605 chars]ly'}] != [{'id[532808 chars]인', '배경도 함께 선명해짐'], 'relations': [], 'adoption[703586 chars]ly'}] |
| `test_photo_structure_maintenance` | exact_registration_list | AssertionError: Lists differ: ['pho[2721 chars]json', 'photo_prompt_vel_appearance_relations_[57 chars]son'] != ['pho[2721 chars]json'] |
| `test_photo_water_main_boundary_history` | sealed_existing_source | AssertionError: Frozen V24 historical source payload drift: skills/photo-prompt-image-generator/SKILL.md |
| `test_subculture_illustration_contract_v1` | current_pack_exact_byte_replay | validate_illustration_assets.ValidationFailure: current photo baseline candidate-pack bytes drift |
| `test_subculture_illustration_universal_scene_v3` | current_pack_exact_byte_replay | validate_illustration_assets.ValidationFailure: current photo baseline candidate-pack bytes drift |
