# What actually worked, and the dead ends to skip

This is the technical handoff from the original owner's project. It is a
sanitized account of the accepted native Home and manual video saver, checked
against the retained development notes. Those notes, device backups, credentials,
original firmware, private icons and videos are not distributed. Paths/API names
below describe observed contracts, not values to force onto another device.

Read this before starting a new port. [MASTERPROMPT.md](MASTERPROMPT.md) sets
the task; [PORTING.md](PORTING.md) turns another device's evidence into a local
candidate. The exact original reference hashes remain in `compatibility.json`.

## 1. From browser workaround to the real Home

The early RemoteNow/MQTT route could pair, open apps and navigate the browser.
A local web page produced a custom launcher, and a watcher detected stock Home
then reopened that page. This worked but visibly bounced through VIDAA, required
the host service, and reloaded the UI. Repeated `hisense://debug` attempts did not
expose the expected installer on this firmware. Neither approach changed native
Home; reducing the polling interval could not make it a real replacement.

The successful change kept the original Home engine and its module registry.
The native Home bundle exposed `_V_M_.launcher`; its result had a `/Launcher`
Vue component. We kept the vendor bundle and appended wrappers, then substituted
that one component. The physical Home key therefore returned through the
existing native engine directly. No browser polling, firmware flash, Android
ADB, bootloader change or replacement OS was needed for this reference device.

Implementation: `native-entry.js` + `native-platform.js` + `native-core.js` +
`native-dock.js` + `native-actions.js`. The wrapper returns stock Home when the
required registry/SDK interface is missing. This is a defensive fallback, not
a substitute for preflight and recovery.

## 2. How temporary maintenance access was established

The native module was not initially readable through the browser context.
An exposed service/file bridge was useful for identifying firmware and paths;
our own page's CSP initially blocked its local service calls. Fixing that
specific diagnostic CSP mistake enabled the reads. A page/network error was not
proof of a closed firmware API. Revert diagnostic permissions after the probe.

The reference's reviewed package/service route staged a one-time local IPK.
Its `postinst` ran with UID 0, independently confirmed with a diagnostic artifact.
The package manager still returned an update error. That taught us to inspect
UID, artifacts and cleanup separately from the top-level install result; do not
assume an error means nothing ran or blindly retry a write.

From that authorized test we established a bounded, key-only SSH maintenance
channel restricted to the owner's maintenance computer. A wrong key was rejected;
the lease expired and had no boot autostart. We backed up originals, recorded
ownership/modes and verified the actual engine restart before editing Home.
The original `index.html`, vendor registry and update configuration remained.

Primary sources used for this investigation:

- [Original research revision / model catalog](https://github.com/carteakey/alvidaa/tree/4bbf060aa7bc1532478517d5cd4d1484bd28ad97/docs/models)
- [50A51HUV native Home findings](https://github.com/carteakey/alvidaa/blob/7f9c9e9f91b5e9982f0af3d515f052b7499b29b4/docs/models/50A51HUV/09.01O.P0813/findings/13-native-home.md)
- [MTK9603 example: gated browser write, different fetcher access route](https://github.com/carteakey/alvidaa/blob/7f9c9e9f91b5e9982f0af3d515f052b7499b29b4/docs/models/43Q60SEVS/V0000.09.60W.Q0612/README.md)
- [Modern native SDK adapter source](https://github.com/carteakey/alvidaa/blob/7f9c9e9f91b5e9982f0af3d515f052b7499b29b4/tools/launcher-host/native-platform-75u8qtuk.js)

These links provide the implementation research, not authorization to execute
every script in it. Resolve exact architecture, paths, package/service semantics
and cleanup against the new device. On the reference, an upstream uninstall
argument form did not match the firmware. Some maintenance package metadata
remained even after payload files were removed; never equate file cleanup with
complete package removal. Do not copy permanent shell, password, boot or OTA
changes from a different report. This repo ships no universal root payload.

## 3. Apply and rollback details that mattered

Compare remote and local originals with SHA-256; retain them separately from
editable working files. Save the exact engine environment privately. Stage a
candidate beside its target, preserve actual owner/mode and rename atomically.
Restart the identified native engine using its verified startup contract.

Compiled and uncompiled UI caches can otherwise serve stale code. Handle only
the relevant caches and rebuild from the actual installed module set. Restoring
an old cache archive wholesale can silently revert a newer, unrelated saver.
The maintenance channel and rollback must survive a broken Home UI.

A timed trial once reverted a working video build because the guard was still
pending. Accept/cancel that guard explicitly after the short Home check, before
normal movie playback. GUI restart can interrupt Netflix even if its process
remains alive. A backup is not a zero-risk guarantee if access to restore it is
lost. Exact apply/rollback requirements are in [RECOVERY.md](RECOVERY.md).

## 4. The dock, focus, icons and sharp text

The native view uses DOM text and a horizontal dock, not a 720p canvas stretched
across the panel. Text and clock remain separate from the video. The reference
native UI was 1920×1080; that does not prove 4K text rendering or lossless
upscaling on every panel. Inspect native viewport/renderer rather than assuming
the TV browser's Chromium version or resolution describes Home.

- Keep a single app row, with focus growth and room around the active outline.
  Let the row extend to the screen edges and mask/fade its edges softly.
- Keep one focus element moving between tabs rather than recreating it on each
  keypress. Give top-tab focus distinct emphasis from a merely selected tab.
- Cache local icon objects; changing Apps/Inputs/TV should not refetch them.
- Native app inventory is authoritative. A hardcoded fallback list produced
  unwanted apps; the public kit uses real inventory and pins only a verified Store.
- Long OK opens editing; suppress the corresponding short-OK launch. Moving and
  removing operate on favorites, not package installation or system files.
- Input navigation is a grid: up/down preserve the column, including incomplete
  final rows; do not require scrolling right through every preceding input.

The requested [Libraries.dev](https://libraries.dev/) Liquid Metal look could
not simply run as a heavy browser/WebGL effect in the native renderer. The final
reference used small pre-rendered metal-fx atlases, not a React runtime. Large
atlases/crossfades caused visible stutter or blinking and were rolled back. The
accepted baseline used 24 frames, forward/backward progression at 200 ms per
frame and a separate 220 ms focus transition. That is a low-cost compromise,
not a claim of shader-quality fluidity. Test on the actual renderer; allow motion
to be disabled. Preserve atlas boundaries and image-cache lifetime.

## 5. Why the video finally became visible

A browser `<video>` or a player `PLAYING` status was not sufficient. We inspected
the reference firmware's own local promotional-video implementation and its
native launcher video class. The public code reimplements the playback contract;
it does not include vendor advertising code or contact an ad service.

The working sequence in `native-video.js`:

1. Register the native source/state callbacks and create a unique owned DMP
   session ending in `_NotUpdateLastSource`.
2. Request DMP with the observed `sourceSwitch` contract. Wait until the current
   source belongs to this session; do not seize or stop an unrelated app player.
3. Resolve the actual local UI file path, append `?video-play-mode=1`, and call
   `mpctrl.playMedia(url, 4, 'Media', 'null', headers)`.
4. Match player events to the expected URL, source/session and player ID.
   After PREPARED, request PLAY and the observed video zoom mode.
5. Keep the native video plane visible through transparent Home ancestors. An
   opaque ancestor can hide a correctly playing video. Inspect the whole chain,
   not only the dock's background. Keep a poster on timeout/playback failure.
6. Observe advancing playback time and actual movement on screen. Stop only
   the owned player and remove listeners when leaving Home.

Validate those APIs and path mappings on each device. A source switch may affect
a streaming app's DRM session; this helper is for Home/manual saver, not a global
Netflix takeover. Do not blindly set global volume or stop every media player.

## 6. Efficient loops and the requested deeper blacks

The accepted reference playback was a silent H.264 MP4 at 1080p/24 fps, prepared
once on the computer from the original 4K clip. It did not decode a GIF or draw
video frames into a canvas on the TV. The Home clip used 90% speed, a short
tail/head crossfade, an 11-second cycle and two seconds of repeated continuation.
Rainy used its own 14-second cycle; these numbers are properties of those exports,
not universal settings for a different clip.

At the known cycle boundary, seek to zero before EOF. The continuation gives the
hardware time to seek without exposing an end-of-file stop. Verify repeated
position resets and visible loops; not just one PLAYING event. Export actual
cycle metadata using `prepare-media.py` and never guess it from the filename.

For deeper blacks, the original export reduced only dark pixel values by up to
about 10%, fading the correction out toward brighter tones. It did not add an
extra full-screen black overlay that also darkened the UI. The portable media
exporter currently handles speed/crossfade/format, not that custom shadow grade;
apply and visually inspect a separate offline grade only if the owner requests
it. Keep the original unchanged and label the result accurately.

## 7. The saver fix and the unfinished parts

Calling `router.push` with a saver-looking path from the launcher opened the
wrong module. The working manual entry was:

```js
sdk.me.req('screen-saver').open('screenMode', {from:'launcher'});
```

The saver bundle needs its own video helper; it cannot assume Home was loaded
first. Wrap the saver factory and replace only `/ScreenSaver/ScreenMode`, with
its lifecycle and Back behavior intact. The owner confirmed the Rainy video
and return to Home. The packaged shared media chooser was prepared/offline-tested
later, not confirmed as deployed. Do not conflate these statuses.

The ten-minute Home idle test was not completed. A paused Netflix saver with
session-preserving return was not solved. Netflix diagnostics had an unstable
session and a native DMP switch can disrupt it. Do not ship fixed process-memory
offsets or call a key-inactivity timer a reliable paused-film detector. Preserve
the OEM/app idle policy until there is separate evidence and acceptance.

## 8. Privacy is a separate result

Replacing Home removes the stock promotional presentation from that view; it
does not prove all tracking stopped or ads inside streaming content disappeared.
DNS filtering, ACR settings and microphone choices have separate requirements.
Use [DNS.md](DNS.md) for client-scoped, reversible rules and compatibility tests.
Do not block broad content/authentication/update domains to force a cosmetic win.

## File map for the next agent

| Task | Reusable implementation |
| --- | --- |
| One-link entry and routing | `AGENT-START.md`, `agent.py`, `model_tools.py` |
| Device-specific candidate and reviews | `PORTING.md`, `build-port.mjs` |
| Native module integration | `native-entry.js`, `native-platform.js` |
| Dock, focus, navigation and editing | `native-core.js`, `native-dock.js`, `native-actions.js` |
| Local video session and loop | `native-video.js`, `prepare-media.py` |
| Shared catalog and manual saver | `native-media.js`, `native-saver.js` |
| Apply/recovery requirements | `RECOVERY.md` |
| Actual offline acceptance tests | `check-bundle.mjs`, `check-video.cjs`, `check-port.py` |

Reuse the proven mechanisms, then verify the differences. Do not copy the
original owner's private values or describe a model-specific research result
as universal compatibility.
