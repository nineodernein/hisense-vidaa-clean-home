"""Offline VIDAA access experiments with persistent, explicitly simulated memory.

All device files, services and packages below are Python values. There is no
transport, shell, firmware interpreter or executable package generator here.
"""
import copy
import hashlib
import itertools
import json
from pathlib import Path

SCHEMA = 1
MODEL_REVISION = 'vidaa-access-model-1'
ROUTES = ('hiutils', 'fetcher')
CONTROL = 'websdk/Appinfo.json'
SOURCE = 'pkgs/tv.vidaa.jsservice.basic/CHA/services/fetcher/package.json'
MARKER = 'lab://owned/marker'
PROOF = 'lab://owned/uid-proof'
MARKER_TEXT = 'inert-simulation-marker'
PROTECTED = {'lab://stock/home': 'original-home',
             'lab://stock/saver': 'original-saver',
             'lab://stock/updates': 'enabled',
             'lab://stock/apps': 'original-app-inventory'}
DEFAULTS = {
    'hiutils': True, 'vowOS': True, 'contextReady': True,
    'fileReadAllowed': True, 'controlExists': False,
    'pathShape': 'array', 'sourceComplete': True,
    'hiutilsWriteAllowed': False, 'fetcherWriteAllowed': True,
    'serviceRunning': False, 'serviceStartAllowed': True,
    'dispatcherArgs': 'both', 'netReady': True, 'wakeReady': True,
    'cleanupMethod': 'http-error', 'httpReject404': True,
    'cleanupAllowed': True, 'cleanupDelay': 2, 'corruptWrite': False,
    'executeAllowed': True, 'architectureKnown': True,
    'installAllowed': True, 'postinstUid': 0, 'installerError': False,
    'proofVariant': 'valid', 'proofCleanupAllowed': True,
}
ENUMS = {'pathShape': ('array', 'string'),
         'dispatcherArgs': ('both', 'object', 'string'),
         'cleanupMethod': ('http-error', 'owned-helper'),
         'proofVariant': ('valid', 'stale-nonce', 'wrong-package', 'string-uid')}
KINDS = ('synthetic', 'reported-mechanism-model', 'unverified-hypothesis-worlds')
SCOPE = {'simulationOnly': True, 'tvContacted': False, 'networkUsed': False,
         'hardwareVerified': False, 'installationApproved': False,
         'realRootEstablished': False}


class LabError(ValueError):
    pass


def stable_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                     ensure_ascii=True).encode()).hexdigest()


def classify_read(response):
    """Classify only this model's explicit envelope; never search file text."""
    if isinstance(response, str):
        try:
            response = json.loads(response)
        except ValueError:
            return 'inconclusive'
    if not isinstance(response, dict):
        return 'inconclusive'
    ret = response.get('ret')
    if ret is True:
        if response.get('error') or response.get('code'):
            return 'inconclusive'
        return 'read' if isinstance(response.get('data'), str) else 'inconclusive'
    if ret is not False:
        return 'inconclusive'
    error = response.get('error')
    code = error.get('code') if isinstance(error, dict) else response.get('code')
    return {'ENOENT': 'missing_path', 'EACCES': 'denied', 'EPERM': 'denied',
            'APP_ID_DENIED': 'denied', 'BAD_ARGUMENT': 'argument_error',
            'PAGE_CSP': 'context_error', 'NO_INTERFACE': 'absent_interface'}.get(code, 'inconclusive')


def validate_world(changes):
    if not isinstance(changes, dict) or set(changes) - set(DEFAULTS):
        raise LabError('Unknown simulation parameter')
    world = {**DEFAULTS, **changes}
    for name, value in world.items():
        if name in ENUMS:
            if value not in ENUMS[name]:
                raise LabError('Unsupported simulation enum: ' + name)
        elif name == 'postinstUid':
            if value is not None and (type(value) is not int or not 0 <= value <= 65535):
                raise LabError('Invalid simulated UID')
        elif name == 'cleanupDelay':
            if type(value) is not int or not 0 <= value <= 12:
                raise LabError('Invalid simulated cleanup delay')
        elif type(value) is not bool:
            raise LabError('Simulation flags must be booleans: ' + name)
    return world


def model_key(world):
    return stable_hash({'revision': MODEL_REVISION, 'world': world})


class VirtualTV:
    """An in-memory behavioral model, NOT a TV/SoC or firmware emulator."""
    def __init__(self, world):
        self.world = validate_world(world)
        self.files = dict(PROTECTED)
        self.files[SOURCE] = '{"permission":{},"exampleError":"denied","ret":false}'
        if self.world['controlExists']:
            self.files[CONTROL] = '{"apps":[]}'
        self.initial = dict(self.files)
        self.running = self.world['serviceRunning']
        self.context = self.world['contextReady']
        self.tick = 0
        self.deletion_at = None
        self.write_verified = False
        self.executed = False
        self.packages = []
        self.trace = []
        self.nonce = stable_hash({'model': model_key(self.world), 'session': 'fresh-virtual-instance'})[:24]
        self.package_id = stable_hash({'kind': 'in-memory-uid-probe', 'nonce': self.nonce})

    def request(self, action, **args):
        if len(self.trace) >= 64:
            raise LabError('Simulation exceeded its bounded experiment budget')
        result = self._request(action, args)
        self.trace.append({'sequence': len(self.trace) + 1, 'tick': self.tick,
                           'action': action, 'arguments': copy.deepcopy(args),
                           'result': copy.deepcopy(result), 'evidenceKind': 'simulation'})
        return result

    def _request(self, action, args):
        w = self.world
        if action == 'inspect_interfaces':
            return {'hiutils': w['hiutils'], 'vowOS': w['vowOS']}
        if action == 'fix_page_context':
            self.context = True
            return {'ret': True, 'scope': 'virtual_diagnostic_page_only'}
        if action == 'file_read':
            interface = args.get('interface')
            if interface not in ('hiutils', 'vowOS') or not w[interface]:
                return {'ret': False, 'code': 'NO_INTERFACE'}
            if not self.context:
                return {'ret': False, 'code': 'PAGE_CSP'}
            if not w['fileReadAllowed']:
                return {'ret': False, 'code': 'EACCES'}
            if args.get('shape') != w['pathShape']:
                return {'ret': False, 'code': 'BAD_ARGUMENT'}
            path = args.get('path')
            if path not in self.files:
                return {'ret': False, 'code': 'ENOENT'}
            return {'ret': True, 'data': self.files[path]}
        if action == 'inspect_contract':
            return {'complete': w['sourceComplete'], 'pathShape': w['pathShape'],
                    'dispatcherArgs': w['dispatcherArgs'], 'cleanupMethod': w['cleanupMethod'],
                    'architectureKnown': w['architectureKnown']}
        if action == 'service_status':
            return {'running': self.running}
        if action == 'start_service':
            if not w['serviceStartAllowed']:
                return {'ret': False, 'code': 'EPERM'}
            self.running = True
            return {'ret': True}
        if action == 'restore_service':
            self.running = w['serviceRunning']
            return {'ret': True}
        if action in ('hiutils_write', 'fetcher_write'):
            if args.get('target') != MARKER:
                raise LabError('Simulator refuses a non-owned write target')
            if MARKER in self.files:
                return {'ret': False, 'code': 'COLLISION'}
            route = action.split('_')[0]
            if not w[route + 'WriteAllowed']:
                return {'ret': False, 'code': 'APP_ID_DENIED' if route == 'hiutils' else 'EACCES'}
            if route == 'fetcher':
                if not self.running:
                    return {'ret': False, 'code': 'SERVICE_NOT_RUNNING'}
                if not w['netReady'] or not w['wakeReady']:
                    return {'ret': False, 'code': 'RUNTIME_CONDITION'}
                form = args.get('form')
                if form not in ('object', 'string') or w['dispatcherArgs'] not in ('both', form):
                    return {'ret': False, 'code': 'BAD_ARGUMENT'}
            self.files[MARKER] = 'corrupted-marker' if w['corruptWrite'] else MARKER_TEXT
            return {'ret': True, 'message': 'simulated download finished'}
        if action == 'confirm_marker':
            self.write_verified = self.files.get(MARKER) == MARKER_TEXT
            return {'ret': self.write_verified}
        if action == 'cleanup_marker':
            if args.get('target') != MARKER:
                raise LabError('Simulator refuses a non-owned cleanup target')
            if w['cleanupMethod'] == 'http-error' and not w['httpReject404']:
                self.files[MARKER] = 'simulated HTTP error response body'
                return {'ret': True, 'message': 'HTTP status accepted; file overwritten'}
            if w['cleanupAllowed']:
                self.deletion_at = self.tick + w['cleanupDelay']
                self._delete_due()
            # The modeled async error path reports before unlink completes.
            return {'ret': False, 'code': 'HTTP_ERROR' if w['cleanupMethod'] == 'http-error' else 'CALLBACK_ERROR'}
        if action == 'advance_clock':
            self.tick += 1
            self._delete_due()
            return {'tick': self.tick}
        if action == 'execute_probe':
            if not self.write_verified or MARKER in self.files:
                raise LabError('Execution before verified write/readback/cleanup')
            if not w['executeAllowed']:
                return {'ret': False, 'code': 'EXECUTION_DENIED'}
            self.executed = True
            return {'ret': True, 'uid': 314, 'meaning': 'simulated worker, not root'}
        if action == 'install_uid_probe':
            if not self.executed or not w['architectureKnown']:
                raise LabError('Package trial before execution/source prerequisites')
            package = args.get('package')
            if package != {'kind': 'in-memory-uid-probe', 'nonce': self.nonce, 'id': self.package_id}:
                raise LabError('Unknown virtual diagnostic package')
            self.packages.append(dict(package))
            if not w['installAllowed']:
                return {'ret': False, 'code': 'INSTALL_DENIED'}
            uid = w['postinstUid']
            if uid is not None:
                proof = {'nonce': self.nonce, 'packageId': self.package_id, 'uid': uid}
                if w['proofVariant'] == 'stale-nonce': proof['nonce'] = 'old-session'
                if w['proofVariant'] == 'wrong-package': proof['packageId'] = 'other-package'
                if w['proofVariant'] == 'string-uid': proof['uid'] = str(uid)
                self.files[PROOF] = json.dumps(proof)
            return {'ret': not w['installerError'], 'code': 'PACKAGE_UPDATE_ERROR' if w['installerError'] else None}
        if action == 'read_uid_proof':
            return {'ret': True, 'data': self.files[PROOF]} if PROOF in self.files else {'ret': False, 'code': 'ENOENT'}
        if action == 'cleanup_package':
            if w['proofCleanupAllowed']:
                self.files.pop(PROOF, None)
                self.packages.clear()
            return {'ret': w['proofCleanupAllowed']}
        raise LabError('Unknown simulation action')

    def _delete_due(self):
        if self.deletion_at is not None and self.tick >= self.deletion_at:
            self.files.pop(MARKER, None)
            self.deletion_at = None

    def pristine(self):
        return self.files == self.initial and not self.packages and self.running == self.world['serviceRunning']


def verify_uid_proof(response, nonce, package_id):
    if classify_read(response) != 'read':
        return None
    try:
        proof = json.loads(response['data'])
    except ValueError:
        return None
    if (not isinstance(proof, dict) or proof.get('nonce') != nonce or
            proof.get('packageId') != package_id or type(proof.get('uid')) is not int or
            not 0 <= proof['uid'] <= 65535):
        return None
    return proof['uid']


class Explorer:
    def __init__(self, tv, memory=None):
        self.tv = tv
        self.memory = memory or {}
        self.closed = set(self.memory.get('closedRoutes', []))
        self.preferred = self.memory.get('successfulRoute')
        self.route = None
        self.interface = None
        self.shape = 'array'
        self.learned = []

    def read(self, path):
        return self.tv.request('file_read', interface=self.interface, shape=self.shape, path=path)

    def run(self):
        status = self._run()
        self.tv.request('restore_service')
        assert all(self.tv.files.get(k) == v for k, v in PROTECTED.items())
        return {'status': status, 'simulatedRoot': status in ('simulated_root', 'simulated_root_cleanup_incomplete'),
                'successfulWriteRoute': self.route, 'closedRoutes': sorted(self.closed),
                'cleanupComplete': self.tv.pristine(), 'experiments': len(self.tv.trace),
                'memoryUsed': bool(self.memory), 'lessons': self.learned,
                'trace': self.tv.trace, **SCOPE}

    def _run(self):
        available = self.tv.request('inspect_interfaces')
        self.interface = 'hiutils' if available['hiutils'] else 'vowOS' if available['vowOS'] else None
        if self.interface is None:
            return 'simulated_no_read_interface'
        # One absent control is followed by the separate source-backed candidate.
        for path in (CONTROL, SOURCE):
            response = self.read(path)
            if classify_read(response) == 'context_error':
                self.tv.request('fix_page_context')
                self.learned.append('Fix the diagnosed diagnostic context before inferring a firmware gate.')
                response = self.read(path)
            if classify_read(response) == 'argument_error':
                self.shape = 'string'
                response = self.read(path)
            kind = classify_read(response)
            if kind == 'read':
                break
            if kind == 'missing_path':
                self.learned.append('ENOENT excludes this path, not the read interface or every registry.')
                continue
            return 'simulated_read_unavailable'
        else:
            return 'simulated_read_unavailable'
        self.learned.append('Classify the response envelope separately from permission/error words in file data.')
        contract = self.tv.request('inspect_contract')
        if not contract['complete']:
            return 'simulated_needs_complete_source'
        order = list(ROUTES)
        if self.preferred in order:
            order.remove(self.preferred); order.insert(0, self.preferred)
        for route in order:
            if route in self.closed:
                continue
            pre = self.read(MARKER)
            if classify_read(pre) != 'missing_path':
                return 'simulated_marker_collision_or_unknown'
            if route == 'fetcher':
                state = self.tv.request('service_status')
                if not state['running']:
                    start = self.tv.request('start_service')
                    if start.get('ret') is not True:
                        self.closed.add(route)
                        continue
            form = 'string' if contract['dispatcherArgs'] == 'string' else 'object'
            response = self.tv.request(route + '_write', target=MARKER, form=form)
            if response.get('ret') is not True:
                if response.get('code') in ('EACCES', 'EPERM', 'APP_ID_DENIED'):
                    self.closed.add(route)
                    self.learned.append('A denied ' + route + ' write does not establish the other route result.')
                    continue
                return 'simulated_runtime_condition_or_argument_gap'
            readback = self.read(MARKER)
            content_ok = classify_read(readback) == 'read' and readback['data'] == MARKER_TEXT
            if content_ok:
                self.tv.request('confirm_marker')
            self.tv.request('cleanup_marker', target=MARKER)
            removed = False
            for _ in range(7):
                verdict = classify_read(self.read(MARKER))
                if verdict == 'missing_path':
                    removed = True; break
                if verdict != 'read':
                    break
                self.tv.request('advance_clock')
            if not removed:
                self.learned.append('Async/error callbacks are not proof of deletion; readback must establish absence.')
                return 'simulated_cleanup_unresolved'
            if not content_ok:
                return 'simulated_readback_mismatch'
            self.route = route
            break
        if self.route is None:
            return 'simulated_write_routes_exhausted'
        if not contract['architectureKnown']:
            return 'simulated_needs_package_architecture'
        executed = self.tv.request('execute_probe')
        if executed.get('ret') is not True:
            return 'simulated_execution_denied'
        package = {'kind': 'in-memory-uid-probe', 'nonce': self.tv.nonce, 'id': self.tv.package_id}
        installed = self.tv.request('install_uid_probe', package=package)
        # Always inspect independently modeled execution evidence, including errors.
        uid = verify_uid_proof(self.tv.request('read_uid_proof'), self.tv.nonce, self.tv.package_id)
        self.tv.request('cleanup_package')
        if uid == 0:
            self.learned.append('UID proof and package return status are independent; do not retry after root proof.')
            return 'simulated_root' if not self.tv.packages and PROOF not in self.tv.files else 'simulated_root_cleanup_incomplete'
        if uid is not None:
            return 'simulated_non_root_execution'
        return 'simulated_install_denied' if installed.get('code') == 'INSTALL_DENIED' else 'simulated_uid_unverified'


def load_catalog(root):
    value = json.loads((Path(root) / 'lab-profiles.json').read_text(encoding='utf-8'))
    if value.get('schemaVersion') != SCHEMA or not isinstance(value.get('profiles'), list):
        raise LabError('Unknown lab catalog')
    ids = set()
    for profile in value['profiles']:
        name = profile.get('id')
        if (not isinstance(name, str) or not name or not all(c.islower() or c.isdigit() or c == '-' for c in name)
                or name in ids or profile.get('kind') not in KINDS):
            raise LabError('Invalid/duplicate lab profile')
        ids.add(name)
        validate_world(profile.get('parameters', {}))
        for key, options in profile.get('hypotheses', {}).items():
            if not isinstance(options, list) or not 1 <= len(options) <= 3:
                raise LabError('Invalid hypothesis alternatives')
            for option in options: validate_world({key: option})
    return value


def worlds_for(profile):
    hypotheses = profile.get('hypotheses', {})
    names = sorted(hypotheses)
    count = 1
    for name in names: count *= len(hypotheses[name])
    if count > 4096:
        raise LabError('Too many hypothetical worlds in one profile')
    for values in itertools.product(*(hypotheses[k] for k in names)):
        assumptions = dict(zip(names, values))
        yield assumptions, validate_world({**profile.get('parameters', {}), **assumptions})


def matrix_profile():
    return {'id': 'systematic-matrix', 'kind': 'synthetic',
            'description': 'Exhaustive discrete behavioral combinations, not a sample of real TVs.',
            'parameters': {},
            'hypotheses': {
                'hiutilsWriteAllowed': [False, True], 'fetcherWriteAllowed': [False, True],
                'serviceRunning': [False, True], 'serviceStartAllowed': [False, True],
                'executeAllowed': [False, True], 'installAllowed': [False, True],
                'postinstUid': [None, 314, 0], 'installerError': [False, True],
                'cleanupAllowed': [False, True], 'httpReject404': [False, True]}}


def runner_hash(root):
    return stable_hash({name: hashlib.sha256((Path(root) / name).read_bytes()).hexdigest()
                        for name in ('vidaa_lab.py', 'lab-profiles.json')})


class Memory:
    """Immutable per-world lessons. Exact runner AND assumption matching is required."""
    def __init__(self, api):
        self.api = api
        self.runner = runner_hash(api.ROOT)
        self.base = Path('.private/lab/memory') / self.runner
        self.hits = 0
        self.saved = 0

    def lookup(self, world):
        key = model_key(world)
        path = self.api.private_path(self.base / (key + '.json'))
        if not path.exists(): return None
        value = self.api.load_json(path)
        payload = {k: v for k, v in value.items() if k != 'recordSha256'}
        if (value.get('schemaVersion') != SCHEMA or value.get('kind') != 'simulation' or
                value.get('recordSha256') != stable_hash(payload) or
                value.get('runnerHash') != self.runner or value.get('modelKey') != key or
                value.get('conditions') != world or value.get('hardwareVerified') is not False or
                value.get('installationApproved') is not False or value.get('realRootEstablished') is not False or
                value.get('successfulRoute') not in (*ROUTES, None) or
                not isinstance(value.get('closedRoutes'), list) or
                any(r not in ROUTES for r in value['closedRoutes'])):
            raise LabError('Invalid or stale simulation-memory record')
        self.hits += 1
        return value

    def remember(self, world, result):
        key = model_key(world)
        path = self.base / (key + '.json')
        if self.api.private_path(path).exists(): return
        record = {'schemaVersion': SCHEMA, 'kind': 'simulation', 'runnerHash': self.runner,
                  'modelKey': key, 'conditions': world, 'status': result['status'],
                  'successfulRoute': result['successfulWriteRoute'],
                  'closedRoutes': result['closedRoutes'], 'lessons': result['lessons'],
                  'cleanupComplete': result['cleanupComplete'],
                  'steps': [{'action': step['action'], 'result': step['result']} for step in result['trace']],
                  **SCOPE}
        record['recordSha256'] = stable_hash(record)
        self.api.write_private(path, record)
        self.saved += 1


def next_questions(profile):
    descriptions = {
        'serviceStartAllowed': ('service_lifecycle', 'Resolve the source-backed service status/start contract and its actual caller permission.'),
        'fetcherWriteAllowed': ('bounded_marker', 'Once scope and cleanup are settled, a new inert marker with readback distinguishes actual worker write permission.'),
        'hiutilsWriteAllowed': ('separate_write_bridge', 'Keep a HiUtils write verdict independent of Fetcher; use source evidence before any new write.'),
        'cleanupAllowed': ('cleanup_readback', 'Determine the actual cleanup contract; an async return does not establish removal.'),
        'httpReject404': ('axios_configuration', 'Inspect the resolved Axios defaults and request/instance overrides; a version number alone does not establish validateStatus.'),
        'executeAllowed': ('execution_boundary', 'Compare the actual function loader and caller checks before proposing execution.'),
        'installAllowed': ('package_boundary', 'Resolve package service permission and architecture without borrowing a sibling boot hook.'),
        'postinstUid': ('independent_uid_evidence', 'A source-backed privilege trial needs scoped runtime UID evidence independent of the package result.'),
        'architectureKnown': ('package_architecture', 'Read the actual package architecture configuration, not a marketing model guess.')}
    return [{'parameter': key, 'alternatives': values, 'question': descriptions.get(key, (key, 'Resolve this modeled prerequisite on the actual device.'))[1],
             'capability': descriptions.get(key, (key, ''))[0], 'executedOnTV': False}
            for key, values in profile.get('hypotheses', {}).items()]


def campaign(api, profile_id='all', include_matrix=False, remember=True):
    catalog = load_catalog(api.ROOT)
    profiles = [p for p in catalog['profiles'] if profile_id == 'all' or p['id'] == profile_id]
    if not profiles: raise LabError('Unknown lab profile')
    if include_matrix: profiles.append(matrix_profile())
    memory = Memory(api) if remember else None
    outcomes, routes, lessons, cases, examples = {}, {}, set(), [], {}
    total, operations, root_count = 0, 0, 0
    for profile in profiles:
        local_outcomes = {}
        for assumptions, world in worlds_for(profile):
            learned = memory.lookup(world) if memory else None
            result = Explorer(VirtualTV(world), learned).run()
            if memory: memory.remember(world, result)
            status = result['status']
            total += 1; operations += result['experiments']; root_count += int(result['simulatedRoot'])
            outcomes[status] = outcomes.get(status, 0) + 1
            local_outcomes[status] = local_outcomes.get(status, 0) + 1
            if result['successfulWriteRoute']:
                route = result['successfulWriteRoute']; routes[route] = routes.get(route, 0) + 1
            lessons.update(result['lessons'])
            if status not in examples:
                examples[status] = {'profile': profile['id'], 'kind': profile['kind'],
                                    'assumptions': assumptions, 'parameters': world, **result}
        cases.append({'id': profile['id'], 'kind': profile['kind'],
                      'worlds': sum(local_outcomes.values()), 'outcomes': local_outcomes,
                      'nextQuestions': next_questions(profile)})
    summary = {'schemaVersion': SCHEMA, 'status': 'offline_lab_complete',
               'modelRevision': MODEL_REVISION, 'runnerHash': runner_hash(api.ROOT),
               'worlds': total, 'virtualExperiments': operations, 'simulatedRootWorlds': root_count,
               'outcomes': outcomes, 'successfulWriteRoutes': routes,
               'memoryHits': memory.hits if memory else 0, 'newMemories': memory.saved if memory else 0,
               'lessons': sorted(lessons), 'profiles': cases,
               'meaning': 'Counts cover invented model combinations, NOT device success rates or hardware compatibility.',
               **SCOPE}
    if remember:
        report = {**summary, 'examples': examples}
        path = Path('.private/lab/runs') / (stable_hash(report) + '.json')
        if not api.private_path(path).exists(): api.write_private(path, report)
        summary['report'] = str(path)
        summary['memory'] = str(memory.base)
    return summary


def memory_summary(api):
    memory = Memory(api)
    base = api.private_path(memory.base)
    statuses, routes, lessons = {}, {}, set()
    records = 0
    if base.exists():
        for path in sorted(base.iterdir()):
            if path.is_symlink() or path.suffix != '.json':
                raise LabError('Unexpected simulation-memory entry')
            record = api.load_json(api.private_path(path))
            world = validate_world(record.get('conditions', {}))
            verified = memory.lookup(world)
            if verified is None or path.stem != model_key(world):
                raise LabError('Simulation-memory identity mismatch')
            records += 1
            status = verified['status']; statuses[status] = statuses.get(status, 0) + 1
            route = verified['successfulRoute']
            if route: routes[route] = routes.get(route, 0) + 1
            lessons.update(verified['lessons'])
    return {'status': 'simulation_memory', 'runnerHash': memory.runner, 'records': records,
            'outcomes': statuses, 'successfulWriteRoutes': routes, 'lessons': sorted(lessons),
            'memory': str(memory.base), 'reuse': 'Exact modeled conditions and runner match; rerun after changed premises.',
            **SCOPE}
