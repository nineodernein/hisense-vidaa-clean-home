#!/usr/bin/env python3
"""Real offline port assembly with invented OEM/SDK evidence; no TV transport."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import model_tools as ports

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('port_entry', ROOT / 'agent.py')
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)
pspec = importlib.util.spec_from_file_location('public', ROOT / 'privacy-check.py')
public = importlib.util.module_from_spec(pspec)
pspec.loader.exec_module(public)


class ResearchTests(unittest.TestCase):
    def setUp(self):
        self.catalog = json.loads((ROOT / 'model-research.json').read_text())

    def test_shared_chip_is_not_a_device_match(self):
        result = ports.research({'marketingModel': 'A7GQ', 'soc': 'MTK9603'}, self.catalog)
        self.assertFalse(result['exactModelReports'])
        self.assertEqual({r['access'] for r in result['relatedChipReports']},
                         {'upstream_blocked', 'upstream_root_reported', 'upstream_root_not_attempted'})
        self.assertFalse(result['installationApproved'])
        self.assertNotIn('A7GQ', json.dumps(result['exactModelReports']))

    def test_similar_retail_or_firmware_names_are_not_matches(self):
        for model in ('58E7NQ', '65U87GQ', '55E7NQ'):
            result = ports.research({'marketingModel': model}, self.catalog)
            self.assertFalse(result['exactModelReports'])
        result = ports.research({'internalModel': '43Q60SEVS_02',
                                'reportedNativeVersion': 'V01.09.60G.Q0612'}, self.catalog)
        self.assertEqual(result['exactModelReports'][0]['match'], 'model_only')

    def test_primary_report_never_becomes_our_support_claim(self):
        result = ports.research({'marketingModel': '75U8QTUK',
                                'reportedNativeVersion': 'V0000.09.60I.Q0813'}, self.catalog)
        self.assertEqual(result['exactModelReports'][0]['adapter'], 'app-list-v1')
        self.assertEqual(result['exactModelReports'][0]['match'], 'model_and_reported_firmware')
        self.assertFalse(result['hardwareVerifiedByThisProject'])
        self.assertFalse(result['installationApproved'])

    def test_private_extra_fields_not_echoed(self):
        result = ports.research({'credentials': 'private-marker', 'marketingModel': 'private-marker'}, self.catalog)
        self.assertNotIn('private-marker', json.dumps(result))

    def test_unknown_device_still_receives_research_path_without_approval(self):
        result = ports.research({'internalModel': 'UNLISTED-DEVICE', 'soc': 'UNLISTED-CHIP'}, self.catalog)
        self.assertEqual(result['status'], 'needs_exact_device_research')
        self.assertFalse(result['exactModelReports'])
        self.assertFalse(result['relatedChipReports'])
        self.assertFalse(result['communityObservations'])
        self.assertTrue((ROOT / result['accessResearch']['guide']).is_file())
        self.assertGreater(len(result['accessResearch']['nextCapabilities']), 0)
        self.assertFalse(result['installationApproved'])

    def test_community_read_success_is_never_promoted_to_root_or_native_support(self):
        result = ports.research({'marketingModel': '50E6NT', 'soc': 'MTK9603',
                                'reportedNativeVersion': 'V0002.09.60A.Q0707'}, self.catalog)
        self.assertEqual(result['status'], 'research_leads')
        self.assertFalse(result['exactModelReports'])
        observation = result['communityObservations'][0]
        self.assertEqual(observation['match'], 'model_and_reported_firmware')
        self.assertEqual(observation['evidenceLevel'], 'owner_reported_information_getters')
        self.assertEqual(observation['access'], 'file_and_root_access_unverified')
        self.assertEqual(observation['nativeHome'], 'not_verified')
        sibling = next(r for r in result['relatedChipReports'] if r['id'] == '43a5le-q0707')
        self.assertEqual(sibling['match'], 'chip_only_not_device_compatibility')
        self.assertFalse(result['hardwareVerifiedByThisProject'])
        self.assertFalse(result['installationApproved'])
        changed = ports.research({'internalModel': '50A60LEVS_0002',
                                 'reportedNativeVersion': 'DIFFERENT-FIRMWARE'}, self.catalog)
        self.assertEqual(changed['communityObservations'][0]['match'], 'model_only')


class PortTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='vidaa-port-test-')
        self.root = Path(self.temp.name)
        for name in public.ALLOWED:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, path)
        self.patch = patch.multiple(entry, ROOT=self.root, PRIVATE=self.root / '.private')
        self.patch.start()
        self.home = b"self._V_M_={launcher:function(){return {route:[{path:'/Launcher',component:{name:'OEM'}}]};}};"
        self.device = {'schemaVersion': 1, 'internalModel': 'SYNTHETIC-TV', 'soc': 'SYNTHETIC-CHIP',
                       'os': 'VIDAA SYNTHETIC', 'reportedNativeVersion': 'SYNTHETIC-FIRMWARE',
                       'freeBytes': entry.RESERVE * 4, 'storeAppId': None,
                       'modules': {'home': {'path': '/fixture/launcher/app.js',
                                           'remoteSha256': entry.digest(self.home), 'uid': 123, 'gid': 123, 'mode': '0644'}},
                       'checks': {key: True for key in ports.FLAGS}}
        self.config = {'version': 1, 'storeAppId': None, 'icons': {}, 'media': [], 'defaults': {'home': None, 'saver': None}}
        entry.write_private('.private/session.json', {'sourceSha256': entry.source_digest(), 'offlineChecksPassed': True})
        entry.write_private('.private/device.json', self.device)
        entry.write_private('.private/ui.json', self.config)
        entry.write_private('.private/stock/home.js', self.home)
        self.result = ports.draft(entry, '.private/device.json')
        self.port_file = entry.private_path(self.result['port'])
        self.port = entry.load_json(self.port_file)

    def tearDown(self):
        self.patch.stop()
        self.temp.cleanup()

    def reviewed(self):
        # Explicit synthetic evidence only. The tool cannot create real-device proof.
        evidence = '.private/evidence/synthetic-sdk-and-recovery.txt'
        text = b'SYNTHETIC fixture: SDK contracts and local rollback are simulated, never hardware-tested.'
        entry.write_private(evidence, text)
        self.port.update(adapter='app-list-v1', assetBase='file:///fixture/assets/', assetDestination='/fixture/assets')
        for review in self.port['reviews'].values():
            review.update(confirmed=True, note='Synthetic contract reviewed for this offline test only.',
                          evidence={evidence: entry.digest(text)})
        return self.port

    def test_draft_preserves_original_and_does_not_approve_itself(self):
        self.assertFalse(self.port['hardwareVerified'])
        self.assertFalse(self.port['installationAuthorized'])
        self.assertIsNone(self.port['adapter'])
        self.assertEqual(entry.private_path(self.port['originalHome']['file']).read_bytes(), self.home)
        with self.assertRaises(entry.Stop): ports.validate(entry, self.port, self.device, self.config)

    def test_each_missing_review_and_string_boolean_stops(self):
        port = self.reviewed()
        for name in ports.REVIEWS:
            for value in (False, 'true'):
                bad = copy.deepcopy(port); bad['reviews'][name]['confirmed'] = value
                with self.assertRaises(entry.Stop): ports.validate(entry, bad, self.device, self.config)

    def test_evidence_requires_real_unchanged_private_artifacts(self):
        port = self.reviewed()
        path = entry.private_path('.private/evidence/synthetic-sdk-and-recovery.txt')
        path.write_text('changed')
        with self.assertRaises(entry.Stop): ports.validate(entry, port, self.device, self.config)
        path.unlink()
        path.symlink_to(self.root / 'README.md')
        with self.assertRaises(entry.Stop): ports.validate(entry, port, self.device, self.config)

    def test_identity_original_or_source_change_stops(self):
        port = self.reviewed()
        bad = copy.deepcopy(self.device); bad['internalModel'] = 'ANOTHER-TV'
        with self.assertRaises(entry.Stop): ports.validate(entry, port, bad, self.config)
        original = entry.private_path(port['originalHome']['file'])
        original.write_bytes(self.home + b'changed')
        with self.assertRaises(entry.Stop): ports.validate(entry, port, self.device, self.config)
        original.write_bytes(self.home)
        (self.root / 'native-platform.js').write_text('source changed')
        with self.assertRaises(entry.Stop): ports.validate(entry, port, self.device, self.config)

    def test_missing_contract_store_space_and_optional_media_stop(self):
        port = self.reviewed()
        for key, value in [('adapter', 'MTK9603'), ('assetBase', 'https://invalid.test/'),
                           ('assetDestination', '/'), ('excludedAppIds', [206])]:
            bad = {**port, key: value}
            with self.assertRaises(entry.Stop): ports.validate(entry, bad, self.device, self.config)
        for key, value in [('storeAppId', '164'), ('freeBytes', 1), ('checks', {})]:
            with self.assertRaises(entry.Stop): ports.validate(entry, port, {**self.device, key: value}, self.config)
        for key, value in [('icons', {'1': 'custom.jpg'}), ('media', [{'id': 'video'}])]:
            with self.assertRaises(entry.Stop): ports.validate(entry, port, self.device, {**self.config, key: value})

    def test_actual_node_build_plan_and_tamper_check(self):
        self.port_file.write_text(json.dumps(self.reviewed()))
        result = ports.prepare(entry, str(self.port_file), '.private/device.json')
        self.assertEqual(result['status'], 'experimental_candidate_for_review')
        self.assertFalse(result['installationAuthorized'])
        self.assertFalse(result['hardwareVerified'])
        output = entry.private_path(result['build'])
        self.assertTrue((output / 'home.js').is_file())
        self.assertFalse((output / 'saver.js').exists())
        self.assertIn(b'self.CleanHomeAdapter="app-list-v1"', (output / 'home.js').read_bytes())
        self.assertIn(self.home, (output / 'home.js').read_bytes())
        self.assertEqual(entry.verify_plan(result['plan'])['status'], 'local_artifacts_unchanged')
        plan = entry.load_json(entry.private_path(result['plan']))
        self.assertIn('OEM screensaver', plan['unchanged'])
        (output / 'home.js').write_text('tampered')
        with self.assertRaises(entry.Stop): entry.verify_plan(result['plan'])

    def test_port_cannot_pass_fixed_reference_builder(self):
        self.reviewed()
        profile = entry.load_json(entry.ROOT / 'compatibility.json')
        with self.assertRaises(entry.Stop):
            entry.validate_evidence(self.device, profile, {'home': self.home, 'saver': b'fake'}, self.config)


if __name__ == '__main__':
    unittest.main()
