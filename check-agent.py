#!/usr/bin/env python3
"""Synthetic offline guard tests. Never imports a network or SSH transport."""
import importlib.util
import json
import tempfile
import unittest
from types import SimpleNamespace
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('entry', Path(__file__).with_name('agent.py'))
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)


def fixture():
    stock = {'home': b'/* synthetic home; not OEM code */',
             'saver': b'/* synthetic saver; not OEM code */'}
    profile = {'id': 'synthetic-offline-fixture', 'internalModel': 'SIMULATED-DEVICE', 'soc': 'SIMULATED-SOC',
               'os': 'SIMULATED-OS', 'reportedNativeVersion': 'SIMULATED-FIRMWARE',
               'stock': {k: entry.digest(v) for k, v in stock.items()},
               'paths': {'home': '/fixture/home.js', 'saver': '/fixture/saver.js'}}
    device = {'schemaVersion': 1, **{k: profile[k] for k in
              ('internalModel', 'soc', 'os', 'reportedNativeVersion')},
              'freeBytes': entry.RESERVE * 2, 'storeAppId': '164',
              'modules': {k: {'path': profile['paths'][k], 'remoteSha256': profile['stock'][k],
                              'uid': 0, 'gid': 0, 'mode': '0644'} for k in stock},
              'checks': {k: True for k in ('nativeContractsVerified', 'independentRecoveryAvailable',
                                          'engineRestartVerified', 'rollbackPlanReviewed')}}
    return device, profile, stock, {'storeAppId': '164'}


class EvidenceTests(unittest.TestCase):
    def test_complete_synthetic_evidence(self):
        entry.validate_evidence(*fixture())

    def test_each_identity_mismatch_stops(self):
        for key in ('internalModel', 'soc', 'os', 'reportedNativeVersion'):
            with self.subTest(key=key):
                d, p, s, c = fixture(); d[key] = 'OTHER'
                with self.assertRaises(entry.Stop): entry.validate_evidence(d, p, s, c)

    def test_blank_template_cannot_pass(self):
        d = json.loads(Path(__file__).with_name('device.example.json').read_text())
        _, p, s, c = fixture()
        with self.assertRaises(entry.Stop): entry.validate_evidence(d, p, s, c)

    def test_malformed_evidence_stops_cleanly(self):
        for key in ('modules', 'checks'):
            for bad in (None, [], 'yes'):
                d, p, s, c = fixture(); d[key] = bad
                with self.assertRaises(entry.Stop): entry.validate_evidence(d, p, s, c)
        d, p, s, c = fixture(); d['modules']['home'] = None
        with self.assertRaises(entry.Stop): entry.validate_evidence(d, p, s, c)

    def test_synthetic_fixture_cannot_pass_production_profile(self):
        d, _, s, c = fixture()
        p = json.loads(Path(__file__).with_name('compatibility.json').read_text())
        with self.assertRaises(entry.Stop): entry.validate_evidence(d, p, s, c)

    def test_each_missing_recovery_check_stops(self):
        for key in fixture()[0]['checks']:
            with self.subTest(key=key):
                d, p, s, c = fixture(); d['checks'][key] = False
                with self.assertRaises(entry.Stop): entry.validate_evidence(d, p, s, c)

    def test_truthy_string_is_not_verification(self):
        d, p, s, c = fixture(); d['checks']['independentRecoveryAvailable'] = 'true'
        with self.assertRaises(entry.Stop): entry.validate_evidence(d, p, s, c)

    def test_corrupt_backup_or_transfer_stops(self):
        for key in ('home', 'saver'):
            d, p, s, c = fixture(); s[key] += b'corrupt'
            with self.assertRaises(entry.Stop): entry.validate_evidence(d, p, s, c)
            d, p, s, c = fixture(); d['modules'][key]['remoteSha256'] = '0' * 64
            with self.assertRaises(entry.Stop): entry.validate_evidence(d, p, s, c)

    def test_missing_metadata_and_foreign_paths_stop(self):
        for key, bad in [('path', '/other/home.js'), ('uid', None), ('gid', -1),
                         ('uid', True), ('mode', '07777'), ('mode', None)]:
            d, p, s, c = fixture(); d['modules']['home'][key] = bad
            with self.assertRaises(entry.Stop): entry.validate_evidence(d, p, s, c)

    def test_disk_reserve_and_store_inventory(self):
        for free in (None, 0, entry.RESERVE - 1, True):
            d, p, s, c = fixture(); d['freeBytes'] = free
            with self.assertRaises(entry.Stop): entry.validate_evidence(d, p, s, c)
        d, p, s, c = fixture(); c['storeAppId'] = '999'
        with self.assertRaises(entry.Stop): entry.validate_evidence(d, p, s, c)

    def test_report_distinguishes_missing_from_mismatch(self):
        d, p, _, _ = fixture()
        self.assertEqual(entry.compatibility_report(d, p)['status'], 'reference_identity_reported')
        d['reportedNativeVersion'] = None
        self.assertEqual(entry.compatibility_report(d, p)['status'], 'needs_more_evidence')
        d['internalModel'] = 'DIFFERENT-MODEL'
        report = entry.compatibility_report(d, p)
        self.assertEqual(report['status'], 'needs_model_research')
        self.assertFalse(report['installationApproved'])

    def test_report_omits_private_fields(self):
        d, p, _, _ = fixture()
        d['account'] = 'DO-NOT-EXPORT-ACCOUNT';d['sshKey'] = 'DO-NOT-EXPORT-KEY'
        d['reportedNativeVersion'] = '192.0.2.10'
        d['modules']['home']['remoteSha256'] = 'DO-NOT-ECHO-ARBITRARY-HASH-FIELD'
        result = json.dumps(entry.compatibility_report(d, p))
        self.assertNotIn('DO-NOT-', result)
        self.assertNotIn('192.0.2.10', result)
        self.assertIn('redacted', result)


class PrivateFileTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='vidaa-offline-')
        self.root = Path(self.temp.name)
        self.patches = [patch.object(entry, 'ROOT', self.root),
                        patch.object(entry, 'PRIVATE', self.root / '.private')]
        for p in self.patches: p.start()

    def tearDown(self):
        for p in reversed(self.patches): p.stop()
        self.temp.cleanup()

    def test_private_write_and_no_overwrite(self):
        file = '.private/stock/home.js'
        entry.write_private(file, b'fixture')
        self.assertEqual((self.root / file).read_bytes(), b'fixture')
        with self.assertRaises(FileExistsError): entry.write_private(file, b'replace')

    def test_traversal_and_public_output_rejected(self):
        for name in ('public.js', '.private/../public.js', str(self.root / 'public.js')):
            with self.assertRaises(entry.Stop): entry.private_path(name)
        self.assertFalse((self.root / 'public.js').exists())

    def test_symlink_root_and_parent_rejected(self):
        outside = self.root / 'outside'; outside.mkdir()
        (self.root / '.private').symlink_to(outside, target_is_directory=True)
        with self.assertRaises(entry.Stop): entry.write_private('.private/home.js', b'x')
        (self.root / '.private').unlink(); (self.root / '.private').mkdir()
        (self.root / '.private/link').symlink_to(outside, target_is_directory=True)
        with self.assertRaises(entry.Stop): entry.write_private('.private/link/home.js', b'x')
        self.assertEqual(list(outside.iterdir()), [])

    def test_dangling_symlink_rejected(self):
        (self.root / '.private').mkdir()
        (self.root / '.private/link').symlink_to(self.root / 'missing', target_is_directory=True)
        with self.assertRaises(entry.Stop): entry.write_private('.private/link/home.js', b'x')

    def test_manifest_detects_corruption(self):
        entry.write_private('.private/home.js', b'fixture')
        files = {'.private/home.js': entry.digest(b'fixture')}
        entry.verify_files(files)
        (self.root / '.private/home.js').write_bytes(b'changed')
        with self.assertRaises(entry.Stop): entry.verify_files(files)

    def test_manifest_refuses_public_paths(self):
        with self.assertRaises(entry.Stop): entry.verify_files({'public.js': 'a' * 64})
        with self.assertRaises(entry.Stop): entry.verify_files({})

    def test_prepare_orchestration_and_plan_integrity(self):
        # Mock only the subprocess/fixture profile. The real assembler has its
        # own full-bundle test; the production CLI never accepts this profile.
        device, profile, stock, _ = fixture()
        (self.root / 'compatibility.json').write_text(json.dumps(profile))
        entry.write_private('.private/session.json', {'sourceSha256': 'a' * 64, 'offlineChecksPassed': True})
        entry.write_private('.private/device.json', device)
        entry.write_private('.private/ui.json', {'storeAppId': '164'})
        for name, data in stock.items(): entry.write_private('.private/stock/' + name + '.js', data)
        def fake_builder(command, **kwargs):
            out = Path(command[command.index('--out') + 1]);out.mkdir(parents=True)
            recovery = Path(command[command.index('--stock-home') + 1])
            self.assertEqual(recovery.read_bytes(), stock['home'])
            self.assertIn('recovery', recovery.parts)
            payload = b'/* assembled fixture */';(out / 'home.js').write_bytes(payload)
            (out / 'manifest.json').write_text(json.dumps({'files': {'home.js': entry.digest(payload)}}))
            return SimpleNamespace(returncode=0, stderr='')
        with patch.object(entry, 'source_digest', return_value='a' * 64), \
             patch.object(entry, 'doctor', return_value={'ok': True}), \
             patch.object(entry.shutil, 'which', return_value='node'), \
             patch.object(entry.subprocess, 'run', side_effect=fake_builder):
            result = entry.prepare('.private/device.json')
            self.assertEqual(result['status'], 'ready_for_local_review')
            self.assertFalse(result['tvContacted'])
            self.assertFalse(result['installationAuthorized'])
            self.assertEqual(entry.verify_plan(result['plan'])['status'], 'local_artifacts_unchanged')
            (self.root / result['build'] / 'home.js').write_bytes(b'corrupt candidate')
            with self.assertRaises(entry.Stop): entry.verify_plan(result['plan'])
        self.assertEqual((self.root / result['recovery'] / 'home.js').read_bytes(), stock['home'])

    def test_changed_source_invalidates_session_before_preparation(self):
        entry.write_private('.private/session.json', {'sourceSha256': 'a' * 64, 'offlineChecksPassed': True})
        with patch.object(entry, 'source_digest', return_value='b' * 64):
            with self.assertRaises(entry.Stop): entry.prepare('.private/device.json')
        self.assertFalse((self.root / '.private/recovery').exists())

    def test_failed_simulated_trial_preserves_original_bytes(self):
        # Local contract model, NOT a TV restart/rollback implementation.
        d, p, stock, c = fixture(); entry.validate_evidence(d, p, stock, c)
        for name, data in stock.items():
            entry.write_private('.private/recovery/' + name + '.js', data)
        original = self.root / '.private/mock-home.js'
        original.write_bytes(stock['home'])
        candidate = b'/* simulated faulty candidate */'
        staged = original.with_suffix('.pending'); staged.write_bytes(candidate); staged.replace(original)
        self.assertEqual(original.read_bytes(), candidate)
        backup = (self.root / '.private/recovery/home.js').read_bytes()
        self.assertEqual(entry.digest(backup), p['stock']['home'])
        staged.write_bytes(backup); staged.replace(original)
        self.assertEqual(original.read_bytes(), stock['home'])
        self.assertEqual((self.root / '.private/recovery/saver.js').read_bytes(), stock['saver'])

if __name__ == '__main__':
    unittest.main()
