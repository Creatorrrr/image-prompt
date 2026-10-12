"""Preserved owner, garment topology, hard activation and native pixel contracts."""
from pathlib import Path
import sys,unittest,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/photo-prompt-image-generator/scripts'))
import photo_candidate_corpus as c
import prompt_generator as pg
from photo_contracts import property_effects_allowed
class NativeWardrobeOwnerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source=c.load(ROOT/'skills/photo-prompt-image-generator/assets')
        cls.profiles={cid:c.entry(source,cid) for cid in PROFILE_IDS}
        cls.registry={'profiles':list(cls.profiles.values())}
        cls.index={'exact_lookup':pg.visual_profile_exact_term_rows(cls.registry)}
        bindings={b['candidate_id']:bid for bid,b in source['slot_bindings'].items()}
        cls.entries={cid:c.entry(source,cid,bindings[cid]) for cid in ENTRY_IDS}
    def hard(self, text, source='concept_lock', polarity='required'):
        hits = pg.resolve_visual_profile_hits(self.registry, [{'source': source, 'text': text, 'polarity': polarity, 'priority': 'critical', 'mandatory': polarity == 'required'}], visual_profile_index=self.index, adult_context=True)
        return {r['profile_id'] for r in hits['hits'] if r.get('hard_eligible')}
    def test_complete_relation_has_one_owner_and_no_sibling_obligation(self):
        for pid, profile in self.profiles.items():
            with self.subTest(profile=pid):
                text = profile['activation']['exact_terms'][0]
                self.assertEqual(self.hard(text), {pid})
                self.assertNotIn(pid, self.hard('not ' + text))
                self.assertNotIn(pid, self.hard(text, 'authorial_core_interpretation', 'advisory'))
    def test_family_labels_and_incomplete_layers_do_not_harden(self):
        for text in ['baby tee', 'button-down', 'bandeau', 'balletcore', 'gothic', 'satin', 'silk', 'cream', 'detached sleeves', 'tray handoff', 'a pendant', 'Mary Jane shoes', 'kimono inspired', 'a dark blazer', 'a red dress', 'a red light', 'blue background and ivory paint', 'shirt front buttons']:
            with self.subTest(text=text):
                self.assertEqual(self.hard(text), set())
        pid = 'cand_22123819e8d151c59ef3c937552ec7a4'
        p = self.profiles[pid]
        self.assertEqual(len(p['authored_components']['components']), 2)
        for component in p['authored_components']['components']:
            self.assertIsNone(pg.candidate_pack_visual_component_match(p, component['evidence_terms'][0]))
    def test_selected_sleeve_does_not_merge_bodice_transmission_or_neck_support(self):
        detached = self.entries['cand_df55314065395a5caff72df8ee7283e0']
        joined = self.entries['cand_a483404df3f256439cb355f526c69a5d']
        self.assertIn('upper-arm band', detached['en'])
        self.assertIn('gap from the bodice', detached['en'])
        self.assertIn('joining boundary', joined['en'])
        self.assertNotEqual(detached['relations'], joined['relations'])
        self.assertIn('material', detached['affected_dimensions'])
        for entry in [detached, joined]:
            lock = {'contract_version': 'photo-intent-lock/v2', 'semantic_anchors': [{'dimension': 'material', 'target': 'main_subject', 'property': 'wardrobe.material.transmission'}]}
            self.assertFalse(property_effects_allowed(lock, entry['affected_dimensions'], entry['affected_properties']))
        halter = self.entries['cand_3e8ea4a1ece456e7bf8687fb6fab8be9']
        spaghetti = self.entries['cand_275026d5bf9e53ae91a2e4d59a4e79d1']
        self.assertIn('neck', halter['relations'][0]['object'])
        self.assertIn('shoulders', spaghetti['relations'][0]['object'])
        self.assertNotEqual(halter['relations'], spaghetti['relations'])
    def test_natural_discovery_keeps_partial_parts_optional_and_distinct(self):
        examples = {'cand_dd6843817f2e56cd8f78986b05575fde': 'black velvet bodice and sheer organza sleeves', 'cand_b284f5e6816d54daabc814305953a659': 'a chain draped between two brooches', 'cand_a9f62a6881965a5490844ca125d0f0e9': 'compressed folds of a seated skirt on a bench seat'}
        for pid, text in examples.items():
            with self.subTest(profile=pid):
                self.assertEqual(pg.candidate_pack_visual_component_match(self.profiles[pid], text), 'component_semantics')
                self.assertFalse(self.hard(text))
                profile = self.profiles[pid]
                self.assertTrue(all((g['review_scale'] == 'native' for g in profile['render_gates'])))
        layered = self.profiles['cand_22123819e8d151c59ef3c937552ec7a4']
        for partial in ['a ribbed top', 'rolled sleeves']:
            self.assertIsNone(pg.candidate_pack_visual_component_match(layered, partial))
        complete = 'a ribbed top beneath an open shirt with rolled sleeves'
        self.assertEqual(pg.candidate_pack_visual_component_match(layered, complete), 'component_semantics')
        self.assertFalse(self.hard(complete))
        self.assertIsNone(pg.candidate_pack_visual_component_match(self.profiles['cand_3b5bed00e718562499b48475729d0ec4'], 'crew neck'))
        self.assertIsNone(pg.candidate_pack_visual_component_match(self.profiles['cand_7272ccaa048b51cca3739454cafa3fb1'], 'spaghetti straps'))
    def test_single_accent_print_and_camera_effects_preserve_cross_carrier_locks(self):
        accent = self.entries['cand_f269dbef117b5ad19c834ea0501d1bd8']
        lock = {'contract_version': 'photo-intent-lock/v2', 'semantic_anchors': [{'dimension': 'appearance', 'target': 'main_subject', 'property': 'wardrobe.color'}]}
        self.assertFalse(property_effects_allowed(lock, accent['affected_dimensions'], accent['affected_properties']))
        self.assertIn('One saturated red fabric plane', accent['en'])
        self.assertIn('remaining garment panels stay black', accent['en'])
        jersey = self.entries['cand_24f728c13e4c5459b726b5f6d56ccd52']
        self.assertIn('text', jersey['affected_dimensions'])
        self.assertIn('front panel', jersey['en'])
        camera = self.entries['cand_c94686f979015e2098604428dbd2195c']
        lock['semantic_anchors'] = [{'dimension': 'camera', 'target': 'camera', 'property': 'viewpoint'}]
        self.assertFalse(property_effects_allowed(lock, camera['affected_dimensions'], camera['affected_properties']))
    def test_nonworn_and_two_actor_states_are_not_worn_or_single_hand_substitutes(self):
        blazer = self.entries['cand_019bedae3fd25e608170ee286d40818c']
        self.assertEqual(blazer['relations'][0]['type'], 'rests_on')
        self.assertIn('bedside surface', blazer['en'])
        self.assertIn('worn blouse remains separate', blazer['en'])
        tray = self.entries['cand_55ede615dee15cd9b5a14955aef4c612']
        self.assertEqual(len(tray['relations']), 2)
        self.assertEqual(tray['relations'][0]['subject'], 'one tray')
        self.assertEqual(tray['relations'][1]['subject'], 'same tray opposite edge')
        self.assertIn('giver', tray['relations'][0]['object'])
        self.assertIn('receiver', tray['relations'][1]['object'])
        self.assertIn('two distinct permitted human actors', json.dumps(tray['contextual_usage']))
        self.assertNotIn('count', tray['affected_dimensions'])
        hem = self.entries['cand_936e2ddb7a575f18a314f83aa654a272']
        self.assertIn('pinch_and_pull_down', [r['type'] for r in hem['relations']])
        self.assertIn('material', hem['affected_dimensions'])
        self.assertNotIn('relationship', hem['affected_dimensions'])

PROFILE_IDS=['cand_0113b93960275541a958bd98ecd7a5b3', 'cand_046afd1c1fbd52fe9e5d9415cf707a11', 'cand_057e3162f31655939939b11d82a3548f', 'cand_07bb0a09411252ed9bf56332e9a9f53e', 'cand_088eb1f2a2355f9baa43b1e561e20b5e', 'cand_0901cbd0cfe657aea6a4020672d59773', 'cand_09c2b3ca875c59c99b55a3474763883e', 'cand_0d0335417ccb525ea569860eaafb1868', 'cand_0d5509a3ac425eeaa6c66e098396968c', 'cand_0da6c38e0a8b5134999c03d1c72c4266', 'cand_0f3d108609b452d880c8fe17109073c9', 'cand_0ffb4705acbd52719a5f04e4a29e0c7a', 'cand_114fce5814e75d80ace4510c0ba4cffd', 'cand_124891a2878b5a7f9483fad4b0cd7a74', 'cand_13f64e2505cc5c859d4845c159763e83', 'cand_15f169088a5353a29138d19577b7dd31', 'cand_16b89991396454bab0a48e58cdbdb300', 'cand_1aa751f2ee275d4696632a8d433573ff', 'cand_1ad4f7fdea9d5decb3a8f54fd7ab72bf', 'cand_1d12642431c350f8b4cbb96bc857ed16', 'cand_21e179b3d3cc5f7e886346a654236df7', 'cand_22123819e8d151c59ef3c937552ec7a4', 'cand_233d8ec281015e5d942a55ca1f8bb3ff', 'cand_29726283d5305daa8e7a0b5ca3880f50', 'cand_2c6d5b61344c5987b4dcb6358c9190e3', 'cand_2cf86781b1fd5f819c055c6d51c101e6', 'cand_34a5f616451051a2a0de69dfc7290c1e', 'cand_3757f8016e505a189709cd445caa3949', 'cand_3b5bed00e718562499b48475729d0ec4', 'cand_3b85ac1fc7925bb1ba9492cb5a08aa7a', 'cand_3d9d09ad8f775c68817238da466a8765', 'cand_3ef5aaa644f95d9895e6939ff415d73b', 'cand_3f3d3d2744025469a8e36ef52c91074e', 'cand_3fab86d764ad5ce686b274fb875d99f9', 'cand_42ba51fad6135a1ab114643d9ba23bcc', 'cand_435324b945f358f4a2440cfec9e260af', 'cand_4387714e3f215e56973d0a1506b9c4b7', 'cand_44b62cbe057051c6817906d93b3ccf83', 'cand_4567b94a447d5f3f82c5a7861ffc44b6', 'cand_460f16abd1f851b6a0fa96a1ec3e6751', 'cand_49e6234b6638535b8d6fad00a35b927b', 'cand_49fd659effd257f098c978b981e17bc1', 'cand_4b78ecdb5b8e57be98099b5d8abc7e85', 'cand_506712cf1d1155918f7655773f3c43f8', 'cand_5104f5dbc8405f3fac5ac374f55a3637', 'cand_5296b45a9e925c5db80e6de76e2e9278', 'cand_532d64a1654f5853b057fd58c7b33b21', 'cand_54862c5056d351328e1ac4d273383777', 'cand_55b79db14fc65230ba8a028f15dc176a', 'cand_56116433f5b6581bbfffa8dad15c37e4', 'cand_5ac0337fa3f35c69b3265b804c2260ef', 'cand_5b79cbd6c521517b97099bbc7a81ffac', 'cand_5c61589f7b1154948111ec96c837a1ec', 'cand_5d59d9751ea95220b4e740b64cff6f02', 'cand_610f1ce3c1f25f0e9d5b7af98d1b925f', 'cand_610f44d3f48d541b9cc1ab12f0854fa2', 'cand_63a044f3e5425ef1b3cd6d973efeefdb', 'cand_663d76fce15a5bd0b5f1362507b6bc5e', 'cand_6684e77a3bd058fc80879226ea14e5db', 'cand_66ff66501c8b57b0bef7c40155474264', 'cand_677863ea887555d4a5e905ed5c970104', 'cand_695008f7106d56fbb75f00940c15343d', 'cand_6aa55832912f57209354c1bfa4eb45f8', 'cand_6b55bfbcea1155389a66bdd90f909842', 'cand_6bf272a47b865381ab3c0b5dae5b5016', 'cand_6c8dd92121e2597888f3965dbe27f5f4', 'cand_6dd274e8c0755dc2bb64b22ab6c3cfde', 'cand_6eea4ba136025446bebd70d93d93fead', 'cand_6f0b3a7bd26a51819cf46cf2ee25b98b', 'cand_6f40094c7adf5158b94cb151a7bfca69', 'cand_708379389ce75d7c83434a1124c46078', 'cand_720745862db25b7eb2fc82438e2c9ba4', 'cand_7272ccaa048b51cca3739454cafa3fb1', 'cand_729323e2c1e75c60a83e48567ed24796', 'cand_7567a4bf58a058808dea7742d079d1c2', 'cand_765c280891d1526a8abf223ac1b50fbc', 'cand_766c341c0b2a57e7937b2f033b25d7e7', 'cand_76d2ea7188005ef595007e632b984092', 'cand_77c1b1db0f3f5075a3c7e05e237e4160', 'cand_7948a633ed0955ec8706fd5b638fd3d6', 'cand_7a84f47995595e30b681d2cfa54c4d93', 'cand_7faa3977fc79592d8af2af3cbcb178aa', 'cand_7fd35064297b57b5834167c068580d20', 'cand_84ec47ccbcda53f781e3b7dcef6e1121', 'cand_878a22374821557ba5b9fc68f3a95ba8', 'cand_87fdcee073205c97bd56a1e299bef967', 'cand_88393a77af7358d2ad123ef4e1a57857', 'cand_88a0c43b456354fdb3e5883e9ab41004', 'cand_892beff7a09a528ea56c97006d4aafea', 'cand_8ec1c16a251b569693234cdd13d619ee', 'cand_93c3035c8f5c5e0eba66327fbc40c46f', 'cand_93ce94636cf557388a5516f6c906b29e', 'cand_99627fc880635b67a7cfddfccf606e91', 'cand_9b84685b7849517ab466a525480ad95c', 'cand_9d99b6912b765216b6df6981f29b7161', 'cand_9f17b35460a256c2b232a6b349eb763f', 'cand_a1e4ac6d9f6f5be1ba285de9e8d6a86d', 'cand_a1f34fce1f305ae996c60b917199b60f', 'cand_a9f62a6881965a5490844ca125d0f0e9', 'cand_ab60a574178856be862bbb5d50572d91', 'cand_b01e846b2fd756a6bd9624cb90160f29', 'cand_b0251c8ab6a556fcb072b41c616f4a1f', 'cand_b0a1a06945965443bc2c6342a7ac8a00', 'cand_b17a1f58ae895801b5a6176b55df4b88', 'cand_b17ff92c17f958e7b45a28af0df9b2bb', 'cand_b284f5e6816d54daabc814305953a659', 'cand_b44c7ef0255355e381709fed5f93dd17', 'cand_b788bb5dc74d579b836bc8b6853bd1eb', 'cand_b9be39b862725942966d49da85a33d76', 'cand_baf53cb2267d5186b04eab1d13850eae', 'cand_bc6648c356ce5a509d6ce9f5b90c306c', 'cand_bcc5287345195842afb14ae2465deba0', 'cand_c18b4160956153ca9fb7efad46949176', 'cand_c2df44d18fe2550d921e09461c8912c1', 'cand_c399b903a196515cb14251475555b4a9', 'cand_c3e0d272503b5e318f90edffc68dc1f3', 'cand_c409dde6d4d45592b2730d822b49963b', 'cand_c445a2b8b7a45347bd2b28046cd2ea87', 'cand_c76453a4c61d55d3b393fb28801d4530', 'cand_ca9cbf3dea035be4aa450ac7d69e9a20', 'cand_cf0ef9b65e1b5ec0bd873ddec5eb866f', 'cand_cfcc1312cc1a58fab9a6ff38a985e2ad', 'cand_d115bf554e1459f188b00918007fb1df', 'cand_d17fcd8ecc7253d4ae8e167c078baa3e', 'cand_d34cb31d288a50a0987cd19ce6aa3b05', 'cand_d5c68090fc6e55e38414d6c937cc71b8', 'cand_d657e148f9a15afb84316552611313d7', 'cand_da0cbaeb737958c8b7020dada90a5c1c', 'cand_da209020b3625784b129a0c46b132beb', 'cand_da32d50aa74d5cc198fd43d995c47404', 'cand_dc7e4b612a64505eb090897954d5633b', 'cand_dd6843817f2e56cd8f78986b05575fde', 'cand_e0c0b3f95e5a5127b58dd6d9f6a7e207', 'cand_e78c9ade4049524f9da0ac94ecf2b75c', 'cand_e9af84b38f4d5ac999f53e985fa1ccd5', 'cand_ea6b0361801f572aa86180f4740dc1ba', 'cand_ea9d405b133c5b56a38189840ccdca66', 'cand_ed2e744866455f55ada36b6e24f875a8', 'cand_edd6f7bbba3056899dd1fd500fd69d85', 'cand_ee6a5a189739516a9e02aa8daf87c0a0', 'cand_eebc136f9bcb598ba49b31482f9bda31', 'cand_f06aa7a839ca555a942550e2b1ec93c9', 'cand_f21a4852e5915a65835c669d09602d5c', 'cand_f687386611a85bd18b6ed66ec13dc13b', 'cand_f84dd50064775c9586ea80d285d06496', 'cand_f88b0e2d030b576f983c83de49dd6ef3', 'cand_fb0cdf7c631b578e8c8bb099f07247fa', 'cand_fb6639261049561b93d276927f995d4a']
ENTRY_IDS=['cand_0009d021fafd583a9f4a315d09e397b4', 'cand_019bedae3fd25e608170ee286d40818c', 'cand_01f1277db67e5ffb8a8a1c59aca70e65', 'cand_0284813e3c465b31a18cec3de7107f41', 'cand_0c7f7fbbf8cd5a929e4bb0282463de97', 'cand_0d36a326530c59888e55b11d8b143752', 'cand_0f04028099a2504a80cbe6ffcd3f64f8', 'cand_117ac513d2bf580ea84f6aaea3a30901', 'cand_11f0ad9b520352a188252543e11b4893', 'cand_1bd08d1ab2275d1d9f6dde915d00484b', 'cand_1c09a24faaa755aab130c4d4096fbba7', 'cand_1ecc394b17fd5195a05e4e913ed75bf7', 'cand_209bf256e7d25c689646efbc390b267c', 'cand_21692b3bf9615d61855e0392a8ef5707', 'cand_234bfc447e655af2a90145b9f64aebed', 'cand_2455af212e0459a8a3193bc89703edc4', 'cand_24a5ae912d3d56fd944c7fbfe6f3be7a', 'cand_24f728c13e4c5459b726b5f6d56ccd52', 'cand_275026d5bf9e53ae91a2e4d59a4e79d1', 'cand_2b4f3b22bc605cfbacde76c81ca5ba26', 'cand_2fd5bce3ffb15fbd8b60b1f44a046eb6', 'cand_3027354dac4954b3a33d043a6c4375e1', 'cand_30a6c5ed722a59deb38ff8ac1d07ffc3', 'cand_34fed182b4a2510eb3b2ed969e600a4c', 'cand_36ce3a08268759c4baa8b61033405e22', 'cand_39ca02a9b7785a24b82f20d902eede35', 'cand_3b3cc18aabe7555ca2ccd2639f00bc76', 'cand_3da7e5c279b95bb4ace5a1bce866e3bd', 'cand_3e8ea4a1ece456e7bf8687fb6fab8be9', 'cand_418d53321d0a5241b47eaf9d6735e4cd', 'cand_41e65a2f6caa5e7f8c7e1b7e66092c43', 'cand_441810bbad33583185246fc4e0839cc6', 'cand_496e38d1b0f954bba3f5a3645d04d87b', 'cand_4a1d8b27d034503bafdae12e06fbc5f7', 'cand_4a781805cbcd51df9ee4edf0dfdf332e', 'cand_51eb32e1175752c9818fb4052c84b81f', 'cand_531cc6f9f2b555a48d35dde4380b0621', 'cand_5404f7a59bbd5e74b9431b1bf25d8623', 'cand_55ede615dee15cd9b5a14955aef4c612', 'cand_57b58247fc5c5b828adc5bda9463ea9c', 'cand_59a159fbc1635ecf9b27bab26b42e766', 'cand_5b6f52a6687e56b19b84880fcb7c2080', 'cand_5d90a5923e24507b959c06489d30a5f9', 'cand_5d9457b199c25c7c8cccfbb6ba23b19b', 'cand_5d945ba752c657da9f5dec0348d06638', 'cand_5e56a521a5d651e7ac0c837465eea9ca', 'cand_64425f18e588555ca8875f87a34f131f', 'cand_672da271182952ff885166214e7f4ab4', 'cand_69452bbfede75b7b9ca7f26ca68d34d9', 'cand_696a0ed291e1533091dfe23b3d302cff', 'cand_6a4d8dd3553a5289ad3a963a1d7d7246', 'cand_6ac2c74fa59f5d599c7ed8287f922013', 'cand_6c3edd509ef5550093350745385d0f40', 'cand_6cd628e075e4584ebe282be6b2ac9c18', 'cand_70f9d91fc87e5a9f993d41d19c69d355', 'cand_728e0529a46e52029dc577daf15b7e55', 'cand_72c9a43065d1544aa91bb4b1deb6a58b', 'cand_73a060d58b8f506da3d3005ea80c9dd4', 'cand_7449812d687f508f9cf03c120c05f28c', 'cand_7536952af07350e19dbadb8efbe6e631', 'cand_78857672866d5627b8369f511e92de41', 'cand_78ab3dd6c5595d7d9e8670a94a2fce97', 'cand_7a3a082635d057dcacd04dc220115030', 'cand_7abe793f80d75643985e1651d8b69537', 'cand_7caf083bd7d4537ba09546c137d73522', 'cand_805f4471153b594b8dbcbb36bba10e8c', 'cand_8720d9a534a359afb573e03b8c667218', 'cand_88a077dffb365bdda3f86c00be9dc62b', 'cand_8954745912585887957f33cc4056bc50', 'cand_8b28e9b4a09f5060bd05e9c4dec361bf', 'cand_8e309577308952afb340eb0a0abf7a00', 'cand_91a2c2774de05eb28f46ea8e88b771d9', 'cand_91c961734c2f57d79499c1c2f6b92713', 'cand_936e2ddb7a575f18a314f83aa654a272', 'cand_9373e64b8341559a9b7d51d41f580d41', 'cand_93e1251e933650099c178f8ab677489d', 'cand_95118948a8fe52e3b92d036f09fbe47d', 'cand_96269ab0306f505baade06b91ddb11b4', 'cand_99c26b6c4a2e52b898a57b4e29bf3919', 'cand_9a773ced2a975bcc863409b5dd666499', 'cand_9d364170fe925e02a18246402c59970a', 'cand_9fe8a5deb48a5fcfb9c026fbc7fd12c7', 'cand_a200c427f46551a08dff48f1add8bbec', 'cand_a2340456694550c99c80073e2b0e00bd', 'cand_a483404df3f256439cb355f526c69a5d', 'cand_a5c1a555b9a95d28b3c4046111d459e9', 'cand_a7e63bebd09f5e74ae9079f486f6973a', 'cand_acdf84a3e69652ea97e4c84b4b6f0cc9', 'cand_ae5c52d160eb53c3b6cb5f3a966b2f6c', 'cand_af6e11e3581f59e48c5a97e79ddd73ce', 'cand_b2ecea11d4d458e59fa77a963c5f406e', 'cand_b4d160fb746553cab6c11aecebde1350', 'cand_b76e52425da653d6a55e7cd10d3fec9c', 'cand_b84594f28aa7509bac220d036c2a625b', 'cand_b9e9bdd0463254809cfe844e17a1d25f', 'cand_bba54b468375533a906d3d98df9855e5', 'cand_bd541569fed65dac86a59c4a7663192f', 'cand_c183c68c2cf3551d9555563e89a2a1b5', 'cand_c23f746c63e65dc68d7b1190221ff684', 'cand_c2b210dd50db5321bc5e312344bb348c', 'cand_c347b2a5737d5ecab8f7a9f37daf1154', 'cand_c3ea3b9ec9145628b9de9f871a830918', 'cand_c4e9308b59a65bbba20e2cab761b364b', 'cand_c94686f979015e2098604428dbd2195c', 'cand_cc10ee8750cf5236bea091fb6c37f18a', 'cand_cd869e8860d655449563c51456262a0d', 'cand_cf4b64d570295fbfa7b3a12314b60cd5', 'cand_cf6cb3df6f8f5aab99ed9a0d549835aa', 'cand_cf78e4414f7254bba4ca30866c4566c0', 'cand_d00045b495115a2b94bce416c4153574', 'cand_d0589f01dab6577d909cfd0032d12cf7', 'cand_d0a4d444a32252d9b4766a08640764ea', 'cand_d21dfd3f6f175cefa28b80c398b8f89e', 'cand_d3e5d1704bf65372874e2cc831eac95b', 'cand_d4065aab370e5fc487ae35017421c5a5', 'cand_d5ebebb18ffc554aa83195751443dc61', 'cand_d66981de7ff05129b8d94a4b112b2cdd', 'cand_d863f4131f0158e793d82a8ffab59df8', 'cand_d8f6734d1cad5912a00865f70c5bdc79', 'cand_df55314065395a5caff72df8ee7283e0', 'cand_e0c8ec9dc974564bb987284a86d80718', 'cand_e121299160cf5acb9f2891f7b0ebc1bb', 'cand_e39f208e22ec533c9d3e15f03829840f', 'cand_e572d0d0976f57ea8d907ee761ebc803', 'cand_e5a4022e64f550fd94b57859b79d5f94', 'cand_e9bca73f36ba55fb8ff9078e2322b78b', 'cand_ea308c02c2fb552b8da55c6750910c78', 'cand_eaa447ec60b35200a9be90254bfd29fa', 'cand_eb56ee76a0655e998fa2889ca3a09f09', 'cand_ec7f78f84fa055f3a9a19d24899d079c', 'cand_ed05f418dc2c5ff68968bd9d22cbdc8f', 'cand_ee75cc84d6e6588d91445e0436fa96c4', 'cand_f0485d66d4a55aaeac5a8f005e2b987f', 'cand_f269dbef117b5ad19c834ea0501d1bd8', 'cand_f487c2ce036c5730946707a8d081aad2', 'cand_f65969a2330651acbb8d19de39cdedfe', 'cand_f91e5ee3a3db54deb606ddde5775b8c7', 'cand_f9a9dcde22a551de903795cb686bd1b7', 'cand_fb5e01c6e0685a7da6c5201a57b63f02', 'cand_fd0c6eb8129651c2ac4d79346be05972', 'cand_fde1c12b62205184b30f60b1dd0707f0', 'cand_fe438f5ac6565a498b7cedc88e0fe0dc', 'cand_fe67eb8a32c4514184dc1de4c242dfec', 'cand_fe893e0b94b35bb2a23a6d29e824b810', 'cand_ff953af3be3955179bb2a406ec4b0a68', 'cand_ff9ab511bc9d5913911ba80c89774745']
