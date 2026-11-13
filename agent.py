#!/usr/bin/env python3
"""Offline agent entry point. No network, SSH, TV writes, or dependency installs."""
import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PRIVATE = ROOT / '.private'
RESERVE = 64 * 1024 * 1024


class Stop(RuntimeError):
    pass


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load_json(path):
    try:
        value = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as error:
        raise Stop('Cannot read valid JSON from ' + path.name) from error
    if not isinstance(value, dict):
        raise Stop('Expected a JSON object in ' + path.name)
    return value


def private_path(path):
    """Reject traversal and symlink ancestors, including .private itself."""
    raw = Path(path)
    if '..' in raw.parts:
        raise Stop('Parent traversal is not allowed')
    absolute = Path(os.path.abspath(str(raw if raw.is_absolute() else ROOT / raw)))
    try:
        relative = absolute.relative_to(PRIVATE)
    except ValueError as error:
        raise Stop('Device files must stay below .private/') from error
    current = PRIVATE
    if current.is_symlink():
        raise Stop('.private must not be a symlink')
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise Stop('Symlinks are not allowed in private paths')
    return absolute


def write_private(path, value):
    path = private_path(path)
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    data = (json.dumps(value, indent=2) + '\n').encode() if isinstance(value, dict) else value
    # Exclusive creation also prevents an unnoticed overwrite of previous evidence.
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'wb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def source_digest():
    spec = importlib.util.spec_from_file_location('public_files', ROOT / 'privacy-check.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    h = hashlib.sha256()
    for name in sorted(module.ALLOWED):
        path = ROOT / name
        if not path.is_file() or path.is_symlink():
            raise Stop('Missing or unsafe public source: ' + name)
        h.update(name.encode() + b'\0' + path.read_bytes() + b'\0')
    return h.hexdigest()


def doctor():
    node = shutil.which('node')
    node_version = None
    if node:
        try:
            version = subprocess.run([node, '--version'], capture_output=True,
                                     text=True, timeout=10, check=True).stdout.strip()
            match = re.fullmatch(r'v(\d+)\.\d+\.\d+', version)
            if match:
                node_version = int(match.group(1))
        except (OSError, subprocess.SubprocessError):
            pass
    missing = []
    if sys.version_info < (3, 10):
        missing.append('Python 3.10+ (use an existing supported interpreter)')
    if node_version is None or node_version < 18:
        missing.append('Node.js 18+')
    return {'ok': not missing, 'python': '.'.join(map(str, sys.version_info[:3])),
            'nodeMajor': node_version, 'missing': missing,
            'tvContacted': False, 'networkUsed': False, 'softwareInstalled': False}


def offline_checks():
    environment = doctor()
    if not environment['ok']:
        return {'status': 'needs_runtime', 'environment': environment,
                'next': 'Use existing prerequisites or ask once before installing from official sources.'}
    checks = []
    for command in ([shutil.which('node'), 'check.mjs'],
                    [shutil.which('node'), 'check-bundle.mjs'],
                    [sys.executable, 'check.py'],
                    [sys.executable, 'check-agent.py'],
                    [sys.executable, 'check-port.py'],
                    [sys.executable, 'check-lab.py'],
                    [sys.executable, 'privacy-check.py']):
        try:
            result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                                    timeout=120, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
        except (OSError, subprocess.SubprocessError) as error:
            raise Stop('Offline check could not finish: ' + command[1]) from error
        checks.append({'name': command[1], 'passed': result.returncode == 0})
        if result.returncode:
            # The checked scripts contain synthetic/public data, never TV logs.
            sys.stderr.write(result.stdout + result.stderr)
            return {'status': 'checks_failed', 'checks': checks,
                    'next': 'Resolve the failing check before contacting any TV.'}
    return {'status': 'offline_pass', 'checks': checks, 'sourceSha256': source_digest(),
            'simulationScope': 'Synthetic modules, mock SDK/player, local files only; no firmware/hardware emulation.'}


def start():
    result = offline_checks()
    if result['status'] != 'offline_pass':
        return result
    private_path(PRIVATE)
    PRIVATE.mkdir(mode=0o700, exist_ok=True)
    if os.name == 'posix' and PRIVATE.stat().st_mode & 0o077:
        raise Stop('Restrict .private permissions to owner-only before storing device data')
    for name, source in [('device.json', 'device.example.json'), ('ui.json', 'config.example.json')]:
        target = private_path(PRIVATE / name)
        if not target.exists():
            write_private(target, (ROOT / source).read_bytes())
    session = private_path(PRIVATE / 'session.json')
    state = {'schemaVersion': 1, 'sourceSha256': result['sourceSha256'], 'offlineChecksPassed': True}
    if session.exists():
        if load_json(session) != state:
            raise Stop('Source changed since the last session. Preserve old session.json under a new private name, then start again.')
    else:
        write_private(session, state)
    import vidaa_lab
    lab = vidaa_lab.campaign(sys.modules[__name__])
    result['simulationMemory'] = {key: lab[key] for key in
                                 ('report', 'memory', 'worlds', 'memoryHits', 'newMemories')}
    result.update(status='needs_device_evidence', next=[
        'Read MASTERPROMPT.md, COMPATIBILITY.md, NATIVE-ACCESS.md and RECOVERY.md.',
        'Use existing owner-supplied facts first. Ask once only for missing TV identity/address and access authorization.',
        'With authorized read-only access, fill .private/device.json from actual observations and copy original modules to .private/stock/.',
        'Never fill evidence with example/profile values. A mismatch stops reference writes, not further authorized source research.',
        'Run python3 agent.py research --json. Follow ACCESS-RESEARCH.md for concrete access hypotheses and WORKED-EXAMPLE.md for original successes and failures.',
        'Read python3 agent.py lab-memory --json and the saved lab report. Reuse matching simulated routes as test-design hypotheses, never as real device evidence.',
        'Exact reference: agent.py prepare. Other devices: PORTING.md, agent.py port, then reviewed agent.py prepare-port.',
        'Read AGENT-START.md for the separate model-specific TV trial. No TV writes are performed by this tool.'
    ])
    return result


def validate_evidence(device, profile, stock, config, required_bytes=RESERVE):
    if device.get('schemaVersion') != 1:
        raise Stop('Unsupported device evidence schema')
    if not isinstance(device.get('modules'), dict) or not isinstance(device.get('checks'), dict):
        raise Stop('Module and recovery evidence must be JSON objects')
    for field in ('internalModel', 'soc', 'os', 'reportedNativeVersion'):
        if device.get(field) != profile.get(field) or not device.get(field):
            raise Stop('Unsupported or unobserved ' + field + '; do not alter compatibility.json to force a match')
    for name in ('home', 'saver'):
        expected = profile['stock'][name]
        if digest(stock[name]) != expected:
            raise Stop('Original ' + name + ' backup does not match the reference hash')
        evidence = device.get('modules', {}).get(name, {})
        if not isinstance(evidence, dict):
            raise Stop('Invalid module evidence for ' + name)
        if evidence.get('remoteSha256') != expected:
            raise Stop('Remote/local ' + name + ' hashes do not match')
        if evidence.get('path') != profile['paths'][name]:
            raise Stop('Unverified ' + name + ' module path')
        for key in ('uid', 'gid'):
            if type(evidence.get(key)) is not int or evidence[key] < 0:
                raise Stop('Missing ownership for ' + name)
        if not re.fullmatch(r'0[0-7]{3}', str(evidence.get('mode', ''))):
            raise Stop('Missing original file mode for ' + name)
    flags = device.get('checks', {})
    for key in ('nativeContractsVerified', 'independentRecoveryAvailable',
                'engineRestartVerified', 'rollbackPlanReviewed'):
        if flags.get(key) is not True:
            raise Stop('Required observation not confirmed: ' + key)
    if device.get('storeAppId') != config.get('storeAppId') or not device.get('storeAppId'):
        raise Stop('Validate the Store app ID against the actual inventory')
    free = device.get('freeBytes')
    if type(free) is not int or free < required_bytes:
        raise Stop('Insufficient or unobserved free space, including rollback/cache reserve')


def compatibility_report(device, profile):
    """Allowlisted facts and verdicts only; never echo the private device object."""
    checks = []
    def public_value(value):
        if value is None or value == '':
            return None
        if (not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9_. -]{1,120}', value)
                or re.search(r'(?:\d{1,3}\.){3}\d{1,3}', value)):
            return '[redacted: unexpected format]'
        return value
    for key in ('internalModel', 'soc', 'os', 'reportedNativeVersion'):
        observed = device.get(key)
        checks.append({'field': key, 'state': 'missing' if not observed else
                       'matches' if observed == profile[key] else 'differs',
                       'observed': public_value(observed), 'reference': profile[key]})
    modules = device.get('modules') if isinstance(device.get('modules'), dict) else {}
    for name in ('home', 'saver'):
        info = modules.get(name) if isinstance(modules.get(name), dict) else {}
        observed = info.get('remoteSha256')
        checks.append({'field': name + '.remoteSha256', 'state': 'missing' if not observed else
                       'matches' if observed == profile['stock'][name] else 'differs'})
    differs = any(c['state'] == 'differs' for c in checks)
    missing = any(c['state'] == 'missing' for c in checks)
    status = 'needs_model_research' if differs else 'needs_more_evidence' if missing else 'reference_identity_reported'
    return {'schemaVersion': 1, 'status': status, 'referenceProfile': profile['id'],
            'checks': checks, 'installationApproved': False, 'tvContacted': False,
            'meaning': 'A mismatch means this exact build is unverified for the device, not that a native port is impossible.',
            'next': 'Use exact-model primary/upstream research and redacted facts; never change expected hashes just to force this build.'}


def prepare(device_file):
    session = load_json(private_path(PRIVATE / 'session.json'))
    if session.get('sourceSha256') != source_digest() or session.get('offlineChecksPassed') is not True:
        raise Stop('Run start and pass all offline checks with this exact source first')
    if not doctor()['ok']:
        raise Stop('Supported Python and Node are required')
    device = load_json(private_path(device_file))
    profile = load_json(ROOT / 'compatibility.json')
    config_path = private_path(PRIVATE / 'ui.json')
    config = load_json(config_path)
    stock = {name: private_path(PRIVATE / 'stock' / (name + '.js')).read_bytes()
             for name in ('home', 'saver')}
    validate_evidence(device, profile, stock, config,
                      RESERVE + 2 * sum(map(len, stock.values())))
    # Keep immutable recovery copies even if a later local build fails.
    tag = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    recovery = PRIVATE / 'recovery' / tag
    for name, data in stock.items():
        write_private(recovery / (name + '.js'), data)
    write_private(recovery / 'evidence.json', device)
    out = PRIVATE / 'builds' / tag
    built = subprocess.run([shutil.which('node'), str(ROOT / 'build.mjs'),
                            '--stock-home', str(recovery / 'home.js'),
                            '--stock-saver', str(recovery / 'saver.js'),
                            '--config', str(config_path), '--out', str(out)],
                           cwd=ROOT, capture_output=True, text=True, timeout=120)
    if built.returncode:
        raise Stop('Local build refused the inputs. Recovery copies retained. ' + built.stderr.strip())
    manifest = load_json(out / 'manifest.json')
    total = sum((out / name).stat().st_size for name in manifest['files'])
    validate_evidence(device, profile, stock, config,
                      RESERVE + 2 * (total + sum(map(len, stock.values()))))
    files = {str((out / name).relative_to(ROOT)): value for name, value in manifest['files'].items()}
    for name, data in stock.items():
        files[str((recovery / (name + '.js')).relative_to(ROOT))] = digest(data)
    files[str((recovery / 'evidence.json').relative_to(ROOT))] = digest((recovery / 'evidence.json').read_bytes())
    plan = {'schemaVersion': 1, 'status': 'local_review_only', 'profile': profile['id'],
            'sourceSha256': source_digest(), 'files': files,
            'tvContacted': False, 'installationAuthorized': False,
            'liveEvidenceIndependentlyVerifiedByTool': False,
            'next': ['Review the exact model-specific apply and rollback scripts.',
                     'Recheck live hashes, free space, maintenance deadline and recovery immediately before a trial.',
                     'Obtain new approval only when existing authorization does not cover the concrete changes.',
                     'Follow RECOVERY.md; verify visible Home/app/Home behavior before accepting the trial.']}
    plan_path = PRIVATE / 'plans' / (tag + '.json')
    write_private(plan_path, plan)
    return {'status': 'ready_for_local_review', 'plan': str(plan_path.relative_to(ROOT)),
            'build': str(out.relative_to(ROOT)), 'recovery': str(recovery.relative_to(ROOT)),
            'installationAuthorized': False, 'tvContacted': False}


def verify_files(files):
    if not isinstance(files, dict) or not files:
        raise Stop('Missing artifact manifest')
    for name, expected in files.items():
        if not re.fullmatch(r'[a-f0-9]{64}', str(expected)):
            raise Stop('Invalid artifact hash')
        if digest(private_path(name).read_bytes()) != expected:
            raise Stop('Artifact changed since preparation: ' + Path(name).name)


def verify_plan(filename):
    plan = load_json(private_path(filename))
    if plan.get('schemaVersion') != 1 or plan.get('status') != 'local_review_only':
        raise Stop('Unknown plan schema or status')
    if plan.get('sourceSha256') != source_digest():
        raise Stop('Public source changed since preparation')
    verify_files(plan.get('files'))
    return {'status': 'local_artifacts_unchanged', 'liveTVStateVerified': False,
            'next': 'Recheck the actual TV and authorized recovery path separately before any transfer.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command')
    for name in ('doctor', 'start', 'simulate', 'lab', 'lab-memory', 'compatibility', 'research', 'port', 'prepare-port', 'prepare', 'verify-plan'):
        child = commands.add_parser(name)
        child.add_argument('--json', action='store_true', help='Machine-readable output (also the default)')
        if name in ('prepare', 'compatibility', 'research', 'port', 'prepare-port'):
            child.add_argument('--device', default='.private/device.json')
        if name == 'prepare-port':
            child.add_argument('--port', required=True)
        if name == 'verify-plan':
            child.add_argument('--plan', required=True)
        if name == 'lab':
            child.add_argument('--profile', default='all', help='Named lab profile, or all')
            child.add_argument('--matrix', action='store_true', help='Add the exhaustive synthetic parameter matrix')
    args = parser.parse_args()
    try:
        command = args.command or 'start'
        if command == 'doctor':
            result = doctor()
            result['status'] = 'runtime_ready' if result['ok'] else 'needs_runtime'
        elif command == 'start':
            result = start()
        elif command == 'simulate':
            result = offline_checks()
        elif command in ('lab', 'lab-memory'):
            import vidaa_lab
            if command == 'lab':
                result = vidaa_lab.campaign(sys.modules[__name__], args.profile, args.matrix)
            else:
                result = vidaa_lab.memory_summary(sys.modules[__name__])
        elif command == 'prepare':
            result = prepare(args.device)
        elif command == 'compatibility':
            result = compatibility_report(load_json(private_path(args.device)), load_json(ROOT / 'compatibility.json'))
        elif command in ('research', 'port', 'prepare-port'):
            import model_tools
            if command == 'research':
                result = model_tools.research(load_json(private_path(args.device)), load_json(ROOT / 'model-research.json'))
            elif command == 'port':
                result = model_tools.draft(sys.modules[__name__], args.device)
            else:
                result = model_tools.prepare(sys.modules[__name__], args.port, args.device)
        else:
            result = verify_plan(args.plan)
        result.update(tvContacted=False, networkUsed=False)
        print(json.dumps(result, indent=2))
        return 2 if result['status'] in ('needs_runtime', 'checks_failed') else 0
    except (Stop, OSError, ValueError, subprocess.SubprocessError) as error:
        reason = ('Local file operation failed (' + type(error).__name__ + '); inspect the private workspace.'
                  if isinstance(error, OSError) else str(error))
        print(json.dumps({'status': 'stopped', 'reason': reason,
                          'tvContacted': False, 'networkUsed': False}, indent=2))
        return 2


if __name__ == '__main__':
    sys.exit(main())
