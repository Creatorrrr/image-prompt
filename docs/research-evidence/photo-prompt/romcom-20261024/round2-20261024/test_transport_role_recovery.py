from pathlib import Path
import copy, importlib.util, unittest

spec = importlib.util.spec_from_file_location('role_recovery',Path(__file__).with_name('repair_b_transport_role.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class RecoveryTest(unittest.TestCase):
    def setUp(self):
        self.old = {'runtime_prompt_en':'unchanged prompt','runtime_negative_en':None,'references':[{'path':'same.jpg','sha256':'same','role':'expanded wording'}],'referenced_image_paths':['same.jpg'],'transparent_background':False}
        self.params = {'references':[{'path':'same.jpg','sha256':'same','role':'exact role'}],'referenced_image_paths':['same.jpg'],'transparent_background':False}
        self.expected = [{'role':'exact role','sha256':'same'}]
    def test_only_role_changes_and_old_is_immutable(self):
        prior = copy.deepcopy(self.old)
        result = module.corrected_request(self.old,self.params,self.expected)
        self.assertEqual(self.old,prior)
        result['references'] = prior['references']
        self.assertEqual(result,prior)
    def test_role_must_equal_projection(self):
        self.params['references'][0]['role'] = 'approximate role'
        with self.assertRaises(ValueError): module.corrected_request(self.old,self.params,self.expected)
    def test_ref_path_and_digest_cannot_change(self):
        for field in ['path','sha256']:
            params = copy.deepcopy(self.params);params['references'][0][field] = 'changed'
            with self.assertRaises(ValueError): module.corrected_request(self.old,params,self.expected)
    def test_prompt_and_negative_overrides_rejected(self):
        for field in ['runtime_prompt_en','runtime_negative_en']:
            params = copy.deepcopy(self.params);params[field] = 'changed'
            with self.assertRaises(ValueError): module.corrected_request(self.old,params,self.expected)
    def test_attachment_and_background_cannot_change(self):
        for field, change in [('referenced_image_paths',['other.jpg']),('transparent_background',True)]:
            params = copy.deepcopy(self.params);params[field] = change
            with self.assertRaises(ValueError): module.corrected_request(self.old,params,self.expected)
    def test_extra_reference_rejected(self):
        self.params['references'].append(copy.deepcopy(self.params['references'][0]))
        with self.assertRaises(ValueError): module.corrected_request(self.old,self.params,self.expected)

if __name__ == '__main__': unittest.main()
