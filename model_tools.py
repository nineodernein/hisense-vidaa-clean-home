"""Offline research routing and private, evidence-bound port candidates.

No transport or installer. The observations are supplied by the owner's agent;
hash checks establish consistency, not truth or physical-device compatibility.
"""
import datetime as dt
import json
import re
import shutil
import subprocess

IDENTITY = ('internalModel', 'soc', 'os', 'reportedNativeVersion')
REVIEWS = ('nativeRegistry', 'launcherRoute', 'sdkContract', 'localAssetMapping',
           'appInventory', 'independentRecovery', 'engineRestart', 'rollbackPlan')
FLAGS = ('nativeContractsVerified', 'independentRecoveryAvailable',
         'engineRestartVerified', 'rollbackPlanReviewed')
ADAPTERS = ('current-show-apps-v1', 'app-list-v1')


def normalized(value):
    return re.sub(r'[^A-Z0-9]', '', value.upper()) if isinstance(value, str) else ''


def research(device, catalog):
    models = {normalized(device.get(k)) for k in ('marketingModel', 'internalModel')} - {''}
    version = device.get('reportedNativeVersion')
    soc = normalized(device.get('soc'))
    matches, related = [], []
    for report in catalog['reports']:
        item = dict(report)
        if models.intersection(normalized(m) for m in report['models']):
            item['match'] = ('model_and_reported_firmware' if version in report['firmwares'] else 'model_only')
            matches.append(item)
        elif soc and soc == normalized(report['soc']):
            item['match'] = 'chip_only_not_device_compatibility'
            related.append(item)
    observations = []
    for report in catalog.get('communityObservations', []):
        if models.intersection(normalized(m) for m in report['models']):
            item = dict(report)
            item['match'] = ('model_and_reported_firmware' if version in report['firmwares'] else 'model_only')
            observations.append(item)
    return {'status': 'research_leads' if matches or observations else 'needs_exact_device_research',
            'exactModelReports': matches, 'relatedChipReports': related,
            'communityObservations': observations,
            'accessResearch': catalog['accessResearch'],
            'upstreamRevision': catalog['upstreamRevision'], 'inventory': catalog['inventory'],
            'installationApproved': False, 'hardwareVerifiedByThisProject': False,
            'next': ['Follow ACCESS-RESEARCH.md, PORTING.md and WORKED-EXAMPLE.md; keep the reference profile unchanged.',
                     'Read the linked primary sources and current upstream reports; pin every source used.',
                     'Reuse known identity and permissions. Keep owner-reported observations separate from upstream results and this project\'s hardware acceptance.',
                     'Use the accessResearch capability sequence and private hypothesis/result ledger; prepare concrete diagnostics instead of stopping at a missing exact guide.',
                     'Keep access, native Home, video and DNS evidence separate. A blocked browser write is not proof all routes are blocked.',
                     'Continue authorized source analysis while a live dependency is pending. Request only genuinely new scope with the exact effects and cleanup ready.',
                     'With authorized originals available, run agent.py port; continue local adaptation without forcing reference prepare.']}


def observed_identity(api, device):
    if device.get('schemaVersion') != 1:
        raise api.Stop('Unknown device evidence schema')
    result = {}
    for key in IDENTITY:
        value = device.get(key)
        if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9_. -]{1,120}', value):
            raise api.Stop('Port draft needs observed ' + key)
        result[key] = value
    if 'VIDAA' not in result['os'].upper():
        raise api.Stop('This native kit requires observed VIDAA OS, not a Hisense brand inference')
    return result


def module_observation(api, device, name, data):
    modules = device.get('modules')
    item = modules.get(name) if isinstance(modules, dict) else None
    if not isinstance(item, dict):
        raise api.Stop('Missing module evidence: ' + name)
    path = item.get('path')
    if not isinstance(path, str) or not re.fullmatch(r'/[A-Za-z0-9_./-]+\.js', path) or '..' in path.split('/'):
        raise api.Stop('Unobserved or unsafe module path: ' + name)
    if item.get('remoteSha256') != api.digest(data):
        raise api.Stop('Remote/local original hash mismatch: ' + name)
    if any(type(item.get(k)) is not int or item[k] < 0 for k in ('uid', 'gid')):
        raise api.Stop('Unobserved original module ownership: ' + name)
    if not re.fullmatch(r'0[0-7]{3}', str(item.get('mode', ''))):
        raise api.Stop('Unobserved original module mode: ' + name)
    return {k: item[k] for k in ('path', 'remoteSha256', 'uid', 'gid', 'mode')}


def require_session(api):
    session = api.load_json(api.private_path(api.PRIVATE / 'session.json'))
    if session.get('sourceSha256') != api.source_digest() or session.get('offlineChecksPassed') is not True:
        raise api.Stop('Run start with this exact source before preparing a port')


def draft(api, device_file):
    require_session(api)
    device = api.load_json(api.private_path(device_file))
    identity = observed_identity(api, device)
    home = api.private_path('.private/stock/home.js').read_bytes()
    observation = module_observation(api, device, 'home', home)
    tag = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    directory = api.PRIVATE / 'ports' / tag
    backup = directory / 'original-home.js'
    api.write_private(backup, home)
    api.write_private(directory / 'observations.json', device)
    hints = [name for name, token in [('current-show-apps-v1', b'getCurrentShowApps'),
                                     ('app-list-v1', b'getAppList')] if token in home]
    profile = {'schemaVersion': 1, 'kind': 'experimental_device_port',
               'sourceSha256': api.source_digest(), 'identity': identity,
               'originalHome': {'file': str(backup.relative_to(api.ROOT)), **observation},
               'adapterHintsOnly': hints, 'adapter': None, 'assetBase': None,
               'assetDestination': None, 'excludedAppIds': [],
               'reviews': {key: {'confirmed': False, 'note': '', 'evidence': {}} for key in REVIEWS},
               'hardwareVerified': False, 'installationAuthorized': False}
    destination = directory / 'port.json'
    api.write_private(destination, profile)
    return {'status': 'port_draft_needs_contract_review', 'port': str(destination.relative_to(api.ROOT)),
            'adapterHintsOnly': hints, 'installationAuthorized': False,
            'next': 'Inspect actual local OEM/SDK sources and recovery evidence as described in PORTING.md; hints are not a verified adapter selection.'}


def validate(api, port, device, config):
    if port.get('schemaVersion') != 1 or port.get('kind') != 'experimental_device_port':
        raise api.Stop('Not an experimental port profile')
    if port.get('sourceSha256') != api.source_digest():
        raise api.Stop('Source changed: create a new port draft and review the changes')
    if port.get('identity') != observed_identity(api, device):
        raise api.Stop('Port identity does not match the observed device')
    original = port.get('originalHome')
    if not isinstance(original, dict):
        raise api.Stop('Missing immutable Home backup')
    data = api.private_path(original.get('file', '')).read_bytes()
    observed = module_observation(api, device, 'home', data)
    if any(original.get(key) != value for key, value in observed.items()):
        raise api.Stop('Device module evidence changed since port draft')
    if port.get('adapter') not in ADAPTERS:
        raise api.Stop('Choose a source-reviewed adapter, or implement and test a new adapter first')
    base, destination = port.get('assetBase'), port.get('assetDestination')
    if not isinstance(base, str) or not re.fullmatch(r'file:///[A-Za-z0-9_/-]+/', base) or '//' in base[8:]:
        raise api.Stop('Review the local renderer asset URL mapping')
    if not isinstance(destination, str) or not re.fullmatch(r'/[A-Za-z0-9_/-]+', destination) or '//' in destination:
        raise api.Stop('Review the actual on-device asset directory')
    excluded = port.get('excludedAppIds')
    if not isinstance(excluded, list) or any(not isinstance(v, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,80}', v) for v in excluded):
        raise api.Stop('Excluded app IDs must be explicitly reviewed strings')
    reviews = port.get('reviews')
    if not isinstance(reviews, dict):
        raise api.Stop('Missing contract review')
    for name in REVIEWS:
        review = reviews.get(name)
        if (not isinstance(review, dict) or review.get('confirmed') is not True or
                not isinstance(review.get('note'), str) or len(review['note'].strip()) < 20):
            raise api.Stop('Missing evidence-backed review: ' + name)
        api.verify_files(review.get('evidence'))
    checks = device.get('checks')
    if not isinstance(checks, dict) or any(checks.get(key) is not True for key in FLAGS):
        raise api.Stop('Actual SDK, independent recovery, engine restart and rollback observations are required')
    if config.get('storeAppId') != device.get('storeAppId'):
        raise api.Stop('Store app ID differs from actual inventory; null means no confirmed Store')
    if config.get('media') or config.get('icons') or any((config.get('defaults') or {}).values()):
        raise api.Stop('First port is static with native inventory icons; validate Home before optional media')
    free = device.get('freeBytes')
    if type(free) is not int or free < api.RESERVE + 2 * len(data):
        raise api.Stop('Insufficient or unobserved device free space')
    return data


def prepare(api, port_file, device_file):
    require_session(api)
    if not api.doctor()['ok']:
        raise api.Stop('Supported Python and Node are required')
    port_path = api.private_path(port_file)
    port = api.load_json(port_path)
    device = api.load_json(api.private_path(device_file))
    config = api.load_json(api.private_path('.private/ui.json'))
    home = validate(api, port, device, config)
    tag = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    directory = api.PRIVATE / 'port-builds' / tag
    # Preserve the exact reviews/evidence/config used, even if the editable draft changes.
    api.write_private(directory / 'reviewed-port.json', port)
    api.write_private(directory / 'device.json', device)
    api.write_private(directory / 'ui.json', config)
    request = {'schemaVersion': 1, 'kind': 'experimental_static_home_only',
               'home': port['originalHome']['file'], 'homeSha256': api.digest(home),
               'adapter': port['adapter'], 'assetBase': port['assetBase'],
               'excludedAppIds': port['excludedAppIds'], 'config': config}
    api.write_private(directory / 'request.json', request)
    out = directory / 'build'
    result = subprocess.run([shutil.which('node'), str(api.ROOT / 'build-port.mjs'),
                             '--request', str(directory / 'request.json'), '--out', str(out)],
                            cwd=api.ROOT, capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise api.Stop('Experimental local assembly failed; originals retained. ' + result.stderr.strip())
    manifest = api.load_json(out / 'manifest.json')
    total = sum((out / name).stat().st_size for name in manifest['files'])
    if device['freeBytes'] < api.RESERVE + 2 * (total + len(home)):
        raise api.Stop('Insufficient space for candidate, original and reserve')
    files = {str((out / name).relative_to(api.ROOT)): value for name, value in manifest['files'].items()}
    files[port['originalHome']['file']] = api.digest(home)
    for review in port['reviews'].values():
        files.update(review['evidence'])
    for path in directory.glob('*.json'):
        files[str(path.relative_to(api.ROOT))] = api.digest(path.read_bytes())
    files[str((out / 'manifest.json').relative_to(api.ROOT))] = api.digest((out / 'manifest.json').read_bytes())
    plan = {'schemaVersion': 1, 'status': 'local_review_only', 'kind': 'experimental_device_port',
            'sourceSha256': api.source_digest(), 'files': files, 'hardwareVerified': False,
            'installationAuthorized': False, 'liveEvidenceIndependentlyVerifiedByTool': False,
            'unchanged': ['OEM screensaver', 'boot configuration', 'firmware', 'DNS'],
            'next': 'Follow PORTING.md for separate live preflight and reversible trial. Local assembly does not verify the TV or authorize transfer.'}
    api.write_private(directory / 'plan.json', plan)
    return {'status': 'experimental_candidate_for_review', 'plan': str((directory / 'plan.json').relative_to(api.ROOT)),
            'build': str(out.relative_to(api.ROOT)), 'hardwareVerified': False,
            'installationAuthorized': False, 'next': plan['next']}
