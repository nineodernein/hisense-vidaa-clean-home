#!/usr/bin/env python3
"""Behavioral access experiments and persistent learning; no device transport."""
import ast
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import socket
import tempfile
import unittest
from unittest.mock import patch
import vidaa_lab as lab

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('lab_entry', ROOT / 'agent.py')
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)


def run(changes=None, memory=None):
    tv = lab.VirtualTV(changes or {})
    result = lab.Explorer(tv, memory).run()
    return tv, result


def actions(result):
    return [s['action'] for s in result['trace']]


class EnvelopeTests(unittest.TestCase):
    def test_returned_source_words_do_not_become_denials(self):
        for text in ('permission denied error', '{"ret":false,"code":"EPERM"}', 'unicode: \u00e4\U0001f327'):
            response = {'ret': True, 'data': text}
            self.assertEqual(lab.classify_read(response), 'read')
            self.assertEqual(lab.classify_read(json.dumps(response)), 'read')

    def test_structured_errors_have_distinct_meanings(self):
        self.assertEqual(lab.classify_read({'ret': False, 'code': 'ENOENT'}), 'missing_path')
        self.assertEqual(lab.classify_read({'ret': False, 'error': {'code': 'EACCES'}}), 'denied')
        self.assertEqual(lab.classify_read({'ret': False, 'code': 'PAGE_CSP'}), 'context_error')
        self.assertEqual(lab.classify_read({'ret': False, 'code': 'BAD_ARGUMENT'}), 'argument_error')

    def test_ambiguous_envelopes_do_not_pass(self):
        for response in (None, [], 'false', 'not-json', {'ret': 'false', 'data': 'x'},
                         {'ret': 'true', 'data': 'x'}, {'ret': 1, 'data': 'x'},
                         {'ret': True}, {'ret': True, 'data': 'x', 'code': 'EACCES'}):
            self.assertEqual(lab.classify_read(response), 'inconclusive')


class ExplorerTests(unittest.TestCase):
    def test_missing_control_and_denied_write_reach_separate_fetcher(self):
        tv, result = run()
        self.assertEqual(result['status'], 'simulated_root')
        self.assertEqual(result['successfulWriteRoute'], 'fetcher')
        self.assertEqual(result['closedRoutes'], ['hiutils'])
        self.assertTrue(result['cleanupComplete'])
        reads = [s for s in result['trace'] if s['action'] == 'file_read']
        self.assertEqual(reads[0]['result']['code'], 'ENOENT')
        self.assertEqual(lab.classify_read(reads[1]['result']), 'read')
        self.assertFalse(tv.running)

    def test_context_and_argument_fixes_change_only_the_relevant_premise(self):
        tv, result = run({'contextReady': False, 'pathShape': 'string'})
        self.assertEqual(result['status'], 'simulated_root')
        self.assertEqual(actions(result).count('fix_page_context'), 1)
        self.assertEqual(actions(result).count('fetcher_write'), 1)
        self.assertEqual({k: tv.files[k] for k in lab.PROTECTED}, lab.PROTECTED)

    def test_separate_vowos_bridge_survives_absent_wrapper(self):
        _, result = run({'hiutils': False})
        self.assertEqual(result['status'], 'simulated_root')
        self.assertTrue(all(s['arguments']['interface'] == 'vowOS'
                            for s in result['trace'] if s['action'] == 'file_read'))

    def test_actual_denial_or_absent_bridge_never_starts_write_tests(self):
        for changes in ({'fileReadAllowed': False}, {'hiutils': False, 'vowOS': False}):
            _, result = run(changes)
            self.assertFalse(any(a.endswith('_write') for a in actions(result)))
            self.assertTrue(result['cleanupComplete'])

    def test_source_selects_argument_contract_without_duplicate_writes(self):
        for form in ('object', 'string', 'both'):
            _, result = run({'dispatcherArgs': form})
            writes = [s for s in result['trace'] if s['action'] == 'fetcher_write']
            self.assertEqual(len(writes), 1)
            self.assertEqual(writes[0]['arguments']['form'], 'string' if form == 'string' else 'object')
            self.assertEqual(result['status'], 'simulated_root')

    def test_incomplete_source_remains_a_specific_dependency(self):
        _, result = run({'sourceComplete': False})
        self.assertEqual(result['status'], 'simulated_needs_complete_source')
        self.assertNotIn('hiutils_write', actions(result))

    def test_existing_marker_is_never_overwritten_or_deleted(self):
        tv = lab.VirtualTV({})
        tv.files[lab.MARKER] = 'preexisting-owner-data'
        result = lab.Explorer(tv).run()
        self.assertEqual(result['status'], 'simulated_marker_collision_or_unknown')
        self.assertEqual(tv.files[lab.MARKER], 'preexisting-owner-data')
        self.assertNotIn('cleanup_marker', actions(result))

    def test_async_cleanup_requires_absence_before_execution(self):
        _, result = run({'cleanupDelay': 5})
        self.assertEqual(result['status'], 'simulated_root')
        trace = result['trace']
        execute = next(s['sequence'] for s in trace if s['action'] == 'execute_probe')
        cleanup = next(s['sequence'] for s in trace if s['action'] == 'cleanup_marker')
        absent = [s for s in trace if cleanup < s['sequence'] < execute and
                  s['action'] == 'file_read' and s['arguments']['path'] == lab.MARKER and
                  lab.classify_read(s['result']) == 'missing_path']
        self.assertEqual(len(absent), 1)
        self.assertGreaterEqual(actions(result).count('advance_clock'), 5)

    def test_failed_or_late_cleanup_never_advances_to_privilege(self):
        for changes in ({'cleanupAllowed': False}, {'httpReject404': False}, {'cleanupDelay': 12}):
            _, result = run(changes)
            self.assertEqual(result['status'], 'simulated_cleanup_unresolved')
            self.assertNotIn('execute_probe', actions(result))
            self.assertFalse(result['cleanupComplete'])
            self.assertLess(result['experiments'], 64)

    def test_success_return_requires_actual_marker_contents(self):
        _, result = run({'corruptWrite': True})
        self.assertEqual(result['status'], 'simulated_readback_mismatch')
        self.assertTrue(result['cleanupComplete'])
        self.assertNotIn('install_uid_probe', actions(result))

    def test_initial_service_state_is_restored(self):
        for running in (True, False):
            tv, result = run({'serviceRunning': running})
            self.assertEqual(tv.running, running)
            self.assertEqual(actions(result).count('start_service'), 0 if running else 1)

    def test_installer_error_can_coexist_with_independent_root_proof(self):
        _, result = run({'installerError': True})
        self.assertEqual(result['status'], 'simulated_root')
        package = next(s for s in result['trace'] if s['action'] == 'install_uid_probe')
        self.assertIs(package['result']['ret'], False)
        self.assertEqual(actions(result).count('install_uid_probe'), 1)
        self.assertTrue(result['cleanupComplete'])

    def test_return_success_or_foreign_proof_never_implies_root(self):
        for changes in ({'postinstUid': None}, {'proofVariant': 'stale-nonce'},
                        {'proofVariant': 'wrong-package'}, {'proofVariant': 'string-uid'}):
            _, result = run(changes)
            self.assertEqual(result['status'], 'simulated_uid_unverified')
            self.assertFalse(result['simulatedRoot'])

    def test_non_root_and_incomplete_cleanup_are_separate_results(self):
        _, result = run({'postinstUid': 314})
        self.assertEqual(result['status'], 'simulated_non_root_execution')
        _, result = run({'proofCleanupAllowed': False})
        self.assertEqual(result['status'], 'simulated_root_cleanup_incomplete')
        self.assertTrue(result['simulatedRoot'])
        self.assertFalse(result['cleanupComplete'])

    def test_no_package_without_observed_architecture(self):
        _, result = run({'architectureKnown': False})
        self.assertEqual(result['status'], 'simulated_needs_package_architecture')
        self.assertNotIn('install_uid_probe', actions(result))

    def test_virtual_machine_rejects_foreign_write_and_cleanup_targets(self):
        for action in ('hiutils_write', 'fetcher_write', 'cleanup_marker'):
            tv = lab.VirtualTV({})
            with self.assertRaises(lab.LabError): tv.request(action, target='lab://stock/home')
            self.assertEqual(tv.files['lab://stock/home'], lab.PROTECTED['lab://stock/home'])


class MemoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='vidaa-lab-test-')
        self.root = Path(self.temp.name)
        for name in ('vidaa_lab.py', 'lab-profiles.json'):
            shutil.copyfile(ROOT / name, self.root / name)
        self.patch = patch.multiple(entry, ROOT=self.root, PRIVATE=self.root / '.private')
        self.patch.start()

    def tearDown(self):
        self.patch.stop(); self.temp.cleanup()

    def test_persistent_success_changes_next_run_order_and_reduces_experiments(self):
        first = lab.campaign(entry, 'fetcher-pivot')
        second = lab.campaign(entry, 'fetcher-pivot')
        self.assertEqual(first['outcomes'], second['outcomes'])
        self.assertEqual(first['newMemories'], 1)
        self.assertEqual(second['newMemories'], 0)
        self.assertEqual(second['memoryHits'], 1)
        self.assertLess(second['virtualExperiments'], first['virtualExperiments'])
        report = entry.load_json(entry.private_path(second['report']))
        self.assertNotIn('hiutils_write', actions(report['examples']['simulated_root']))
        self.assertEqual(lab.memory_summary(entry)['records'], 1)
        self.assertTrue(entry.private_path(first['report']).exists())

    def test_changed_conditions_cannot_reuse_an_old_success(self):
        memory = lab.Memory(entry)
        _, result = run()
        world = lab.validate_world({})
        memory.remember(world, result)
        self.assertIsNotNone(memory.lookup(world))
        self.assertIsNone(memory.lookup(lab.validate_world({'fetcherWriteAllowed': False})))

    def test_changed_runner_keeps_old_records_but_starts_a_new_namespace(self):
        first = lab.campaign(entry, 'fetcher-pivot')
        source = self.root / 'vidaa_lab.py'; source.write_text(source.read_text() + '\n# changed model\n')
        second = lab.campaign(entry, 'fetcher-pivot')
        self.assertEqual(second['memoryHits'], 0)
        self.assertNotEqual(first['memory'], second['memory'])
        self.assertTrue(entry.private_path(first['memory']).is_dir())

    def test_modified_memory_is_detected(self):
        result = lab.campaign(entry, 'fetcher-pivot')
        path = next(entry.private_path(result['memory']).glob('*.json'))
        content = json.loads(path.read_text());content['successfulRoute'] = 'hiutils'
        path.write_text(json.dumps(content))
        with self.assertRaises(lab.LabError): lab.campaign(entry, 'fetcher-pivot')

    def test_symlink_memory_root_is_rejected(self):
        outside = self.root / 'outside';outside.mkdir()
        (self.root / '.private').symlink_to(outside, target_is_directory=True)
        with self.assertRaises(entry.Stop): lab.campaign(entry, 'fetcher-pivot')
        self.assertFalse(list(outside.iterdir()))

    def test_complete_matrix_has_no_network_and_preserves_production_gates(self):
        with patch.object(socket, 'socket', side_effect=AssertionError('network forbidden')):
            result = lab.campaign(entry, 'fetcher-pivot', include_matrix=True, remember=False)
        self.assertEqual(result['worlds'], 1537)
        self.assertGreater(len(result['outcomes']), 5)
        self.assertGreater(result['simulatedRootWorlds'], 0)
        for key in ('tvContacted', 'networkUsed', 'hardwareVerified', 'installationApproved', 'realRootEstablished'):
            self.assertIs(result[key], False)
        self.assertFalse((self.root / '.private').exists())

    def test_community_worlds_are_hypotheses_not_device_acceptance(self):
        result = lab.campaign(entry, 'community-50e6nt', remember=False)
        self.assertEqual(result['worlds'], 768)
        self.assertGreater(len(result['profiles'][0]['nextQuestions']), 5)
        self.assertEqual(result['profiles'][0]['kind'], 'unverified-hypothesis-worlds')
        self.assertFalse(result['hardwareVerified'])
        production = json.loads((ROOT / 'compatibility.json').read_text())
        with self.assertRaises(entry.Stop): entry.validate_evidence(result, production, {}, {})

    def test_lab_module_contains_no_live_transport_or_dynamic_execution(self):
        tree = ast.parse((ROOT / 'vidaa_lab.py').read_text())
        modules = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import): modules.update(n.name.split('.')[0] for n in node.names)
            if isinstance(node, ast.ImportFrom): modules.add(node.module.split('.')[0])
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                self.assertNotIn(node.func.id, {'eval', 'exec', '__import__'})
        self.assertLessEqual(modules, {'copy', 'hashlib', 'itertools', 'json', 'pathlib'})


if __name__ == '__main__':
    unittest.main()
