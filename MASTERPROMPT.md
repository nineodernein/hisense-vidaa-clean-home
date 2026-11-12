# Masterprompt: native Hisense VIDAA dock for an owned TV

You are a coding agent with filesystem and terminal access on the owner's computer.
Implement the native dock using this repository. Read this entire file, AGENTS.md,
AGENT-START.md, COMPATIBILITY.md and RECOVERY.md before changing a TV. This document is a procedure,
not proof of authorization for a device or a license to bypass platform safety rules.

"Use this" plus the repository link is the entry request. Begin the local work,
reuse existing device facts and follow through the statuses in AGENT-START.md.
Read WORKED-EXAMPLE.md for the complete original technical handoff. For a device
that differs from the reference, read PORTING.md and develop its own reviewed
integration; do not treat a hash mismatch as the end of the owner's task.

## The requested result

A native replacement for the stock /Launcher component, with the floating
horizontal app dock, soft edge fades, an active focus ring, Apps / Inputs / TV
tabs, long-OK favorite editing and the real App Store at the right. Home must return
through the vendor home engine. Preserve streaming apps, parental checks,
authentication, DRM, firmware updates and native settings.

Optional: add the owner's animated video wallpaper and manual video screensaver.
Optional and separate: TV-scoped DNS rules for home promotional endpoints.
“Remove from home” must only edit favorites, never uninstall system packages.

Do not replace this request with a browser watcher unless the owner knowingly
accepts that fallback after native compatibility cannot be established.

## 1. Get the project and run offline checks

Repository: https://github.com/nineodernein/hisense-vidaa-clean-home
Download a tagged/source ZIP, or clone it. Pin the revision you actually use and
record it locally. Read files before running them; do not pipe a remote script
into a shell. Download only from the named project/upstream sources.

For an owner request to set up this repository, begin the executable local
workflow after inspecting its source. Do not stop at advice or ask the owner to
run every command. Run from the extracted folder:

```sh
python3 agent.py start --json
```

This command runs the offline runtime, bundle, simulation and privacy checks,
then creates blank private device/UI templates and a session manifest. Re-running
it preserves existing templates. Read its JSON status and follow AGENT-START.md.
For simulation only, use `python3 agent.py simulate --json` and never contact a TV.
Do not install missing software automatically.
Use an existing Python 3.10+ and Node 18+ where available; explain a missing
prerequisite once and use official vendor/package-manager sources if authorized.
FFmpeg is optional until a video is requested.

The startup command creates `.private/` with restrictive permissions. If making
it manually, use `mkdir -m 700 .private`. Keep configuration, IPs, SSH keys, firmware bundles,
logs and backups there, never in Git-tracked source. Do not copy the author's
device data or media; none is required or distributed.

## 2. Identify the actual device and choose the correct route

Use the owner-provided IP or existing authorized inventory. No subnet scanning.
Record marketing model, internal model, SoC, full firmware string and OS.
Verify VIDAA rather than inferring it from the Hisense brand. Distinguish the TV's
browser from the native Cobalt home renderer.

Use VIDAA-MODELS.md only to identify documented OS families. Manufacturer VIDAA
listings and upstream access reports are not this project's support matrix.
Do not label a Toshiba, Loewe, MEDION or another Hisense model supported until
this dock's exact integration has separate device evidence. Keep the reference
profile and its hash guard unchanged during a documentation-only update.

The reference family is in compatibility.json. Exact original launcher/saver
SHA-256 values are decisive for the reference build; a similar model name is insufficient.
The native source expects _V_M_, _V_SDK_, /Launcher and /ScreenSaver/ScreenMode.

If those requirements do not match, stop the reference native write path. Run
`python3 agent.py research --json` and follow PORTING.md: investigate a documented
access route, inspect the device's own SDK, create its private port draft, adapt
the source and test a candidate locally. Only stop dependent live steps when
their actual prerequisites are unresolved. A browser bridge rejection does not
rule out every service, and a successful root report does not validate Home.
Do not weaken the fixed hash check or paste another model's memory offsets,
ownership IDs or boot hooks. Offer DNS or an agreed browser fallback if no native
route can be established; do not silently substitute that for the native goal.

## 3. Establish a bounded, authorized maintenance path

Read NATIVE-ACCESS.md. Prefer an existing authorized root shell. If absent, match
the exact model/firmware against alvidaa's model documentation and explain the
specific proposed access method before installation or privilege changes.
A browser bootstrap used once to establish access is not a browser-based Home UI.

On the reference firmware, the working route was a browser-exposed file/service
bridge and a one-time local package whose postinst ran as root. It then used a
source-restricted, key-only, time-limited SSH maintenance channel. Do not infer
this works on every VIDAA release. No universal exploit or prebuilt root package
is shipped here. No default password or foreign private key is supplied.

No open root listeners, wildcard LAN access, permanent startup hooks or firmware
flashing. Keep the authorized access duration and close it after the test.
Never silently extend it. Do not make the maintenance channel public.

## 4. Back up and prove recovery before replacing Home

Read RECOVERY.md. Copy the original native Home and Saver modules from the owner's
TV to .private/stock/home.js and .private/stock/saver.js. Compute hashes on both
sides and compare to compatibility.json. Save file ownership/modes and the
actual engine/cache locations privately. Do not publish these copies.

Keep an independent shell/recovery path working while testing. Verify that the
documented engine restart mechanism matches this firmware; do not kill processes
by a broad name pattern. Native GUI restart can interrupt Netflix and other apps.
Schedule a test while the owner is not watching.

Prepare and review the exact apply/rollback actions locally. The new files should
be written to adjacent temporary names and renamed atomically. Restore only the
targeted modules. Cache handling must use the current modules, not a stale cache
from another release. Keep the old assets until recovery is verified.

## 5. Build the dock without OEM redistribution

Default icons come from the TV's local inventory. Do not fabricate installed apps,
hardcode a private app list, request remote icon CDNs or include paid icon packs.
The profile's storeAppId must be checked against the TV inventory.

Use the .private/ui.json created by `start` and add only the owner's chosen
local icon/video files. Use empty media for the static fallback initially.
Fill .private/device.json from actual authorized observations, including remote
hashes, original modes/ownership, free space and recovery checks. Never populate
it by copying the expected profile. Then prepare:

```sh
python3 agent.py prepare --json
```

This retains additional private originals, runs the guarded build and writes a
review manifest. It does not contact the TV or perform a remote installation.
Before transfer run `python3 agent.py verify-plan --plan <reported-private-plan>`.
Live device state and the maintenance deadline must still be checked separately.
For manual local builds, `node build.mjs` remains available under the same hash guard.
The reference build accepts only the exact original module hashes in compatibility.json.
Other devices use the separate reviewed `prepare-port` path in PORTING.md, starting
with a static Home and preserving the OEM saver. Do not force reference `prepare`.
The output deliberately contains the owner's OEM code and is PRIVATE.
Do not upload it as a GitHub Release, artifact, issue attachment or pull request.

The integration order is:
original vendor Home → local config/media/video helpers → native platform adapter
→ native core → dock skin → favorite actions → native entry wrapper.
The wrapper retains the vendor registry and replaces only /Launcher's component.

Do not copy a foreign index.html, remove the shell, rewrite the app store, or
replace system firmware. Disable an old browser Home watcher if the owner has
one, preserving its previous configuration.

## 6. Trial, verify and explicitly accept

Transfer only the reviewed bundles and the listed assets using the authorized
maintenance connection. Compare hashes again after transfer. Check free space
before writing; preserve at least 64 MiB plus room for rollback and cache rebuild.
Large media libraries can exceed the TV's small writable partition.

Use a bounded rollback plan. Tell the owner its deadline. An unaccepted watchdog
must never be left pending while the owner returns to watching a film: its GUI
restart can interrupt playback. After a short successful Home check, explicitly
accept/cancel that trial guard, then perform the app tests with manual recovery
still available. A running process alone is not a visual success.

Verify with the owner:
- Home appears without browser chrome or a polling bounce.
- Left/right changes apps, Up visibly focuses tabs, Down returns to the shelf.
- Holding OK opens move/remove; short OK launches the app only once.
- Canceling a move restores the previous order.
- Removing a favorite does not uninstall its app.
- App Store opens only if present and validated.
- Inputs navigate by row and column, including the last incomplete row.
- Netflix/YouTube or the owner's chosen apps still open.
- Physical Home returns to this native dock.
- Settings and original recovery remain available.
- Test standby/cold boot separately before claiming persistence across either.

Do not mark unobserved checks as passed. Close temporary access and preserve
a concise private change log and hash manifest when done.

## 7. Animated backgrounds and manual video saver

Read ANIMATED-WALLPAPERS.md. Use only owner-supplied/licensed media.
The guide links the example videos' source pages. Do not auto-download media,
install those sites' desktop wallpaper apps, or redistribute the paid icon pack.
Prepare a silent H.264 MP4, 1080p24, JPG poster, known cycle length and two-second
cyclic continuation. Avoid GIFs and 4K canvas decoding on the TV.

The proven native playback contract is:
- a unique owned DMP source/session ending in _NotUpdateLastSource;
- local file URL ending ?video-play-mode=1;
- mpctrl.playMedia(localURL, 4, 'Media', 'null', headers);
- play after the matching PREPARED event;
- use only matching player/session events;
- seek at the cycle boundary before EOF; verify motion and repeated loops;
- stop only the owned player when leaving Home; never stop a different source.

Use native-video.js as the implementation reference. A PLAYING status alone is
not proof that the video is visible; opaque ancestor layers caused black/still
screens in the reference work. Keep a poster fallback and check actual display.

The correct manual saver route is:
`sdk.me.req('screen-saver').open('screenMode', {from:'launcher'})`.
Calling router.push from the launcher with the saver path selected the wrong module.
The saver includes its own video helper so load order is independent.

Shared on-screen media selection is packaged but only offline-tested. Validate
it as a separate change. Keep Home and saver choices independent and store each
clip once. **No automatic takeover of paused Netflix**: DMP can disrupt the DRM
app, global activity isn't proven, and return-to-film behavior remains untested.
Do not include or use fixed Netflix process-memory offsets.

## 8. Optional DNS filtering

Read DNS.md and inspect every rule in dns-candidates.json.
Start with one client-scoped rule and an owner-confirmed cold start.
Keep DNS filtering independent from the native installer. Do not alter router-wide
DNS/DHCP or other household devices to make a single TV work.
Do not disable security update/authentication endpoints or block broad streaming
CDNs. Hostname roles may be inferred; encrypted traffic is not proof of content.

## Finish with evidence

Report what changed, exact tested firmware/revision, verified behaviors, remaining
uncertainty, recovery path, and maintenance closure. Keep raw logs and identifiers
private. For public compatibility reports include only redacted model/firmware,
pass/fail results and relevant hashes; never account/session/network data.

The goal is a reusable, understandable native dock installation, not a boast about
bypassing every VIDAA security mechanism or guaranteed universal ad removal.
