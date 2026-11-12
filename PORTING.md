# Port the native dock to another VIDAA device

For the owner's local coding agent. The objective is a native Home with the same
dock and editing behavior, followed by separately validated local video. A
different model or original-file hash starts this workflow; it does not mean
"VIDAA cannot be customized". Keep the fixed reference profile unchanged.

This is a source-level development workflow, not a universal exploit/installer.
The owner should not have to discover these steps or paste every command. Continue
the authorized local research and coding yourself. Never present another owner's
hardware result as a test of this owner's device.

## 1. Route from observed facts

Start with `python3 agent.py start --json`. Fill `.private/device.json` with actual
marketing/internal model, SoC, full native firmware and OS. Unknown fields remain
null. Use existing authorized inventory first; do not scan the household.

```sh
python3 agent.py compatibility --json
python3 agent.py research --json
```

`research` is offline: it searches [model-research.json](model-research.json), a
pinned, curated upstream evidence catalog. It returns exact-model reports and
separate chip-only leads. It does not probe a TV or authorize installation.
Read the linked primary sources and check newer upstream research as needed;
record its revision. Firmware letters and region variants matter. In particular:

- An A7GQ with MTK9603 is not established compatible. MTK9603 research includes
  both a successful access route and a blocked route on different firmware.
- `V01.09.60G.Q0612` is not the `09.60W.Q0612` report just because Q0612 matches.
- A 55E7NQ PRO report does not cover a 58E7NQ, nor every E7NQ.
- An upstream working web launcher does not establish native Home replacement.

## 2. Investigate the maintenance path separately

Read [NATIVE-ACCESS.md](NATIVE-ACCESS.md) and the actual source linked by the
research result. Inspect capabilities before proposing writes: native file
bridge, app identity restrictions, service/fetcher behavior, package manager,
architecture/userland, installation destination and available independent
recovery. A browser bridge failure is evidence about that bridge, not every
service. Distinguish a permission error, missing path and unsupported API.

Prefer an already authorized maintenance channel. A newly needed privileged
bootstrap requires a concrete, owner-approved scope, reviewed code and cleanup.
Do not run a model recipe merely because the chipset matches. Keep access
time-limited, authenticated and restricted to the owner's computer. Do not copy
upstream default passwords, permanent access hooks, broad firewall openings or
update-disabling steps. No brute-force offsets, destructive probing or firmware
flash. If no evidenced route exists, explain the exact unresolved capability;
continue offline analysis of owner-supplied sources where useful.

## 3. Preserve this device's original Home

Once authorized access exists, copy its original native Home module to
`.private/stock/home.js`. Fill `device.json.modules.home` with the actual module
path, remote SHA-256, UID, GID and mode. Compare the local hash. Keep OEM SDK
sources and observations in `.private/evidence/`; never upload them.

```sh
python3 agent.py port --json
```

This creates an exclusive private backup, an observation snapshot and a draft
`port.json` in a new `.private/ports/…/` directory. It does not change
`compatibility.json`. The draft has no selected adapter and all reviews are
false. Token matches in the original bundle are hints, not contract evidence.

## 4. Review and adapt the actual native contracts

Inspect the original launcher, SDK and route lifecycle. Record the following in
the generated private profile. Every review needs `confirmed: true`, an actual
explanation in `note`, and `evidence` mapping private artifact paths to SHA-256.
The checks validate consistency of those records; they cannot prove their truth.
Do not manufacture notes or mark a review passed because a build needs it.

| Review | Evidence required |
| --- | --- |
| nativeRegistry | Existing `_V_M_.launcher` factory and SDK construction; retain the vendor registry |
| launcherRoute | Actual `/Launcher` route, Vue/lifecycle and key event contract |
| sdkContract | Observed app-list/detail/APC, source and settings contracts for the chosen adapter |
| localAssetMapping | Actual renderer `file:///…/` URL mapped to the writable asset destination; not another TV's path |
| appInventory | Real apps, icon fields, Store ID or confirmed absence; no copied personal app list |
| independentRecovery | Recovery independent of the replaced Home, including availability after UI failure |
| engineRestart | Exact executable/process/cache/start mechanism and private saved environment |
| rollbackPlan | Reviewed apply/restore artifacts, hashes, ownership, deadline and cleanup |

Two source-reviewed adapter contracts are included:

| Adapter | App inventory/detail | App start | Settings |
| --- | --- | --- | --- |
| `current-show-apps-v1` | `getCurrentShowApps("Launcher")` / `getAppInfoByAppId` | APC `REMOTECONTROL` | `open("settings", {vk:"T"})` |
| `app-list-v1` | `getAppList({sceneCode:"launcher"})` / `getAppInfo` | APC `LAUNCHER_RECOMMEND` from the SDK | `open("settings")` |

Both use actual `getAllInputsData` results and `changeSourceTo`. APC retains the
vendor's parental/EULA/app checks. No bypass flags or guessed command constants
are sent. Select an adapter using actual contracts, not chip or model names.
The second adapter is derived from the pinned upstream 75U8QTUK implementation;
it is offline-tested here, not hardware-certified on every modern VIDAA TV.

Set `adapter`, `assetBase`, `assetDestination` and `excludedAppIds` in the draft.
The first two paths describe renderer URL and actual storage respectively;
they need not be identical. `excludedAppIds` defaults to empty, so another
device does not inherit the reference owner's hidden app. Set the actual Store
ID in both device/UI files; use JSON `null` if no Store has been confirmed.

If neither adapter fits, implement a new narrow adapter against those observed
contracts in a local branch. Add an actual assembled-bundle fixture for its API
shapes, errors, app/Home lifecycle and recovery behavior. Do not turn one adapter
into a guessing loop. Re-run `agent.py simulate`, preserve the old private
session, run `start` again and make a new source-bound draft. Updating an adapter
is legitimate port development; changing a reference hash to silence a guard is
not. Keep real OEM bytes in private files, never test fixtures.

## 5. Build a static candidate first

The first port intentionally preserves the original screensaver and uses the
native inventory icons. Keep `media: []`, `icons: {}` and both defaults null.
Verify device free space and the four recovery/SDK observations in `device.json`.

```sh
python3 agent.py prepare-port --port .private/ports/YOUR-DRAFT/port.json --json
python3 agent.py verify-plan --plan .private/port-builds/YOUR-BUILD/plan.json --json
```

Use the actual paths returned by the commands. The agent substitutes them; do
not ask the owner to find those paths. Output contains private OEM Home plus our
wrappers and the two local focus atlases. It contains no saver replacement,
remote apply script, root package or boot hook. The plan includes exact local
artifact hashes, copied review records and `hardwareVerified: false`.

This separate experimental builder accepts a reviewed device's own original;
`build.mjs` and `agent.py prepare` still enforce the fixed reference hashes.
`prepare-port` validates supplied evidence, not a live TV. Its success is not
installation approval or evidence that recovery works physically.

## 6. Prepare a device-specific live trial

Follow [RECOVERY.md](RECOVERY.md). Before any transfer, use the authorized channel
to recheck identity, current original hash, actual free space, asset mapping,
maintenance deadline and independent recovery. Prepare the exact atomic apply
and rollback scripts locally for those observations, including a single lock,
refusal of an unknown current file, preserved modes, targeted cache handling,
and the verified UI restart. The repo deliberately does not invent those shell
commands for an unobserved firmware.

If the owner has authorized this concrete change, proceed within that scope.
Otherwise request the missing permission once with the actual prepared change.
Keep trial rollback independent of the Home UI and visible to the owner. Accept
or restore before the owner resumes normal viewing. Verify Home, apps, physical
Home return, inputs, settings and long-OK move/remove. Preserve the original
screensaver and stop if any core action fails. A rendered preview is not a pass.

## 7. Add the optional look and video separately

Once the static Home has passed its physical acceptance, follow
[WORKED-EXAMPLE.md](WORKED-EXAMPLE.md) and [ANIMATED-WALLPAPERS.md](ANIMATED-WALLPAPERS.md).
The dock source is already shared; do not rebuild it as a browser page.

Animated media on a new device is a second porting step. Inspect its own native
DMP/file/session APIs, URL mapping and video-plane transparency before enabling
`native-video.js`. Adapt only the observed differences in a local branch and add
tests. The initial `prepare-port` command deliberately rejects media; do not
remove that guard just to make an unverified video build. A media-capable port
needs its own reviewed builder/manifest with the same backup/hash/space gates,
Home-player ownership tests and visible loop acceptance. The source and complete
reference contract are supplied; unsupported firmware is still development work.

For a custom saver, additionally back up that device's original saver, inspect
its module factory and `/ScreenSaver/ScreenMode` lifecycle, and validate manual
entry/Back independently. Never replace a paused streaming app based solely on
keyboard inactivity. Home background and saver selection are independent; a
shared local clip is stored once.

## Completion and sharing

Keep a private result matrix: static Home, app/Home return, editing, inputs,
settings, video loops, manual saver, standby/cold boot and recovery. Mark only
observed results passed. Close maintenance and remove only owned temporary
artifacts. Report exact unresolved steps if a capability is blocked; do not call
that a successful installation. Public reports contain redacted model/firmware,
source revision, hashes and feature results only. Never publish originals,
private keys, network addresses or personal media.
