# Project abstract and complete agent handoff

[Deutsch](PROJECT-ABSTRACT.de.md) · [Masterprompt](MASTERPROMPT.md) · [Evidence and compatibility](COMPATIBILITY.md)

Status recorded: **2026-11-14**. This is a sanitized synthesis of the original
project and community reports. It contains reusable mechanisms, research sources,
failed assumptions and acceptance criteria. Private device files, accounts,
network details and viewing history are deliberately excluded.

## 1. Objective and actual result

The original project changed the native VIDAA Home component into a floating,
editable app dock. Physical Home returns through the existing vendor engine,
without reopening a browser launcher. Streaming apps and their authentication,
native settings, parental controls, DRM and update configuration remain part of
the existing system.

The reference is one **MTK9602 / VIDAA U9 / V0000.09.09F.P0930** unit, internal
model **43A53FEVS_0004**. Its marketing name is not conclusively established.
A retail series, chipset or VIDAA version alone does not establish compatibility.

| Capability | Evidence at this snapshot |
| --- | --- |
| Native dock; app → physical Home; favorite editing; Store; input grid | Confirmed on the original unit |
| Local animated wallpaper; manual video saver and Back | Confirmed on the original unit |
| Jellyfin app tile connected to the owner's local server | Confirmed on the original unit; separate integration |
| Netflix preview artwork/title and native resume action | Confirmed; reliable episode and remaining-time fields still open |
| Prime Video preview artwork/title, season/episode and native action | Confirmed; remaining time still open |
| Disney+ preview artwork, season/episode, remaining time, progress and episode action | Owner confirmed on the original unit; private integration |
| YouTube last-watched preview | Experimental; owner reported missing or wrong card; not accepted |
| ARD, ZDF, RTL+, MagentaTV and HBO Max personal resume cards | Not accepted/verified |
| Shared wallpaper/saver chooser | Prepared and tested offline; deployed acceptance not established |
| Automatic saver after ten Home-idle minutes | Real timeout test not completed |
| Custom saver over paused Netflix with reliable return | Not solved |
| Generalized public build | Tested offline; not separately accepted as a new physical-TV build |
| Every VIDAA model or firmware update | Not established |

The public native source kit does **not** include the private Continue Watching
adapters or the owner's Jellyfin/server configuration. This update documents
those lessons; it does not silently promote prototypes to shipped features.

## 2. Why native Home worked

The initial browser launcher, controlled through paired remote commands and a
watcher, visibly bounced through stock Home and reloaded assets. Faster polling
could not fix the architectural problem. The reference device's debug URL also
did not expose the expected installer.

The successful route retained the OEM engine, bundle and module registry.
Wrappers around `_V_M_.launcher` and the existing `_V_SDK_` replaced the
`/Launcher` component. Native Home therefore remained the Home key's destination.
The saver was adapted separately through its own factory and route.

A browser-exposed file/service interface helped establish a reviewed one-shot
package test. Its diagnostic `postinst` produced independent UID 0 evidence.
The top-level package result was not sufficient to determine whether execution
had occurred. A time-limited, key-only, source-restricted maintenance connection
then enabled backups and the native integration. No replacement OS or Android
ADB was required on this unit.

**The Intel Mac was an orchestration/build/server computer, not the reason the
firmware permitted access.** Another computer can perform those roles with
appropriate tools. The decisive differences are the TV's firmware, service
permissions, module contracts and recovery options.

See [the detailed worked example](WORKED-EXAMPLE.md),
[access research](ACCESS-RESEARCH.md) and [porting](PORTING.md).

## 3. Lessons from the second reported device

An owner of a 50E6NT reported firmware `V0002.09.60A.Q0707`, internal model
`50A60LEVS_0002` and MTK9603. These are model/build facts, not serial numbers.
The progression was information getters → file reads → verified source transfer
→ two inert write/readback/removal trials → reported one-shot UID 0 execution.

Important corrections:

- A missing WebSDK wrapper did not rule out the available vowOS/HiUtils bridge.
- A successful source response containing the word `permission` was incorrectly
  classified as denial. Inspect the structured response, not arbitrary content.
- `ENOENT` concerned a specific path, not all file access or all app registries.
- Photograph transcription changed source bytes. Direct private transfer with
  consistent UTF-16 length, UTF-8 byte count and checksum removed that ambiguity.
  Use SHA-256 for retained originals/build integrity; FNV is only a transfer check.
- The complete dispatcher resolved the object-versus-JSON-string question.
  Partial function source alone had not established the full call contract.
- Source plus the successful runs established one-shot service dispatch without
  an explicit start. Do not generalize that lifecycle to every service/build.
- A receiver's HTTP 501 for POST was a PC server implementation error.
- Fetcher error cleanup was asynchronous. Return status did not prove deletion;
  bounded readback confirming absence did.
- Duplicate requests and restaging after reload remained unresolved. Keep probe
  initialization passive, use action correlation and prevent duplicate mutations.
- Root proof ended the need for another root demonstration. It did not establish
  a running maintenance shell, successful cleanup, recovery or a native Home port.

The report is **owner-reported, not independently reproduced here**. Diagnostic
cleanup was described but its outcome was not supplied. Earlier marker cleanup
does not establish later package cleanup. Keep those stages separate.

The latest 55U7Q enquiry reports `V0000.09.60A.Q0602` and extended version
`X0003.W01.Y01.J01`. It supplies identity only: no access, root or Home result.
Other retail-model enquiries likewise remain research leads. Never infer that
a shared 09.60 substring proves the same build or permission boundary.

## 4. Dock and interaction design

Use the actual installed-app inventory and local icons. Do not invent apps from
a static list. Keep one horizontal row with soft edge fades and room around a
slightly enlarged selected tile. Only the selected app and selected top tab have
an outline; the dock itself has no enclosing frame.

A single moving top-tab outline and separate keyboard-focus emphasis make
Apps/Inputs/TV navigation understandable. Long OK opens favorite editing and
suppresses the corresponding short-OK launch. Removing a favorite does not
uninstall an app. The real Store entry is validated from the current inventory.
Input navigation preserves columns on Up/Down, including incomplete rows.

Cache images across sections. Keep text in native DOM rendering, separate from
video, and avoid scaling a low-resolution canvas over the screen. The observed
native viewport was 1920×1080, not evidence of a native 4K UI.

[Libraries.dev](https://libraries.dev/) and its Liquid Metal effect informed the
design. The native implementation used small pre-rendered metal-fx atlases;
React/WebGL components were not drop-in native VIDAA components. The accepted
reference baseline used 24 frames at 200 ms in forward/back progression and a
separate 220 ms focus transition. Large atlases/crossfades caused blinking or
stutter. Preserve the accepted baseline, offer reduced motion and verify it on
the actual renderer. This is a performance compromise, not shader equivalence.

## 5. Video background and saver

The decisive video fix was native player ownership **and a transparent ancestor
chain**. A PLAYING event with a black/still screen did not prove visible playback.
The inspected firmware's own video implementation supplied the native contract;
its proprietary bundles and advertising code are not redistributed.

The reference contract used an owned DMP session, source-switch confirmation,
a local URL with `?video-play-mode=1`, matching PREPARED/PLAY events and cleanup
limited to that session. [WORKED-EXAMPLE.md](WORKED-EXAMPLE.md) and
`native-video.js` describe it. Preserve a poster fallback.

Prepare silent H.264 MP4 on the computer, ordinarily 1080p24 for this reference.
Slight slowing and a short tail/head crossfade were baked into the export.
Known loop metadata plus repeated continuation let the player seek before EOF.
Do not substitute GIF decoding, 4K canvas frame painting or guessed loop timing.
A requested darker black level was an offline shadow adjustment, not a black
layer over the whole picture. That custom grade is not part of the public exporter.

The correct reference manual saver entry was
`sdk.me.req('screen-saver').open('screenMode', {from:'launcher'})`.
A launcher-local router path reached the wrong module. The saver needs its own
video helper and lifecycle, independent of whether Home loaded first.

A key-idle timer is not a reliable paused-stream detector. Native DMP takeover can
disrupt a DRM app. The manual saver result must not become an automatic Netflix
saver claim. Shared media selection should store each clip once and keep Home
and saver choices independent, after free-space and physical-device checks.
See [animated media](ANIMATED-WALLPAPERS.md).

## 6. Jellyfin and Continue Watching

Jellyfin was added as an app entry launching its web client against a local
server. This is not an Android APK. Registration, favorite membership, icon cache
and actual app launch are separate checks. An installer webpage opening the
client did not prove the tile had been registered. An empty library did not prove
network failure. Preserve the existing Home setup when adding one app.

The [upstream Jellyfin installer](https://github.com/theDavidCoen/jellyfin-vidaa-install)
is a research reference, not an instruction to repeat its DNS setup on an already
working native Home. Quick Connect/session state and server settings stay private.
Codec, audio and subtitle combinations still need their own playback tests.

Continue Watching became a small translucent card above the dock. The accepted
layout was 720×190 logical pixels with a 288×162 contained image and padding.
Images needed contain sizing rather than cropping; a CSS background worked in
the native renderer when an image element did not. Metadata must fit the same
card size. Provider-specific adapters, cache lifetimes, profile identity, native
launch actions and real on-screen verification are essential.

Read [CONTINUE-WATCHING.md](CONTINUE-WATCHING.md) for the provider research,
known dead ends, precise status and implementation contract. Never publish the
owner's titles, content IDs, tokens, responses or viewing history as fixtures.

## 7. Deployment, maintenance and validation

Retain originals, SHA-256 values, ownership/modes and exact native restart/cache
contracts privately. Stage adjacent temporary files and rename atomically.
Preserve the OEM shell, settings, parental checks, authentication and updates.
A backup alone does not prove independent recovery.

Handle only relevant caches using the current module set. Restoring an old whole
cache can undo an unrelated newer saver. A GUI restart can interrupt streaming,
even if that app process survives.

Record access expiry, trial deadline and cleanup ownership separately. Give
visible acceptance enough time before access expires. A pending reply is not
acceptance. Cancel/accept a trial guard explicitly before normal watching.
A closed maintenance port does not prove every test package was removed;
an armed rollback does not prove a subsequently read matching hash.

HTTP 200, a running player, a simulation pass and the owner's visible acceptance
are different evidence. A report of a wrong/missing card overrides a backend's
optimistic status. Consolidate diagnostics instead of repeated GUI restarts.

## 8. Privacy, licensing and honest debloating claims

Only generic technical VIDAA findings, model/build facts and sanitized results
belong in the public handoff. Private device contents can be sensitive even when
stored inside a vendor file. Exclude credentials, tokens, serials, network details,
personal paths, signed URLs, history, account IDs, chat screenshots and raw dumps.
See [PRIVACY.md](PRIVACY.md).

The public preview was separately approved. Original videos and paid icon packs
are not bundled; source pages and bring-your-own-media instructions are provided.
New original contributions are noncommercial under the existing
[license scope](LICENSE-SCOPE.md); upstream and earlier MIT rights remain intact.

A clean native Home removes stock promotional presentation from that view.
Selective, client-scoped [DNS filtering](DNS.md) is separate. Neither proves all
tracking stopped, prevents every data sale, removes in-stream ads or replaces
the operating system. One streaming service failing while others work calls for
service/domain-specific diagnosis, not household-wide DNS changes.

## 9. Instructions for the next coding agent

1. Read this handoff, MASTERPROMPT.md, AGENTS.md, COMPATIBILITY.md and RECOVERY.md.
   For an existing project, read its private handoff before repeating onboarding.
2. Review the local scripts. For a new installation request run
   `python3 agent.py start --json`; a repo-only request stays offline.
3. Reuse established device facts, successful probes and current authorization.
   Identify only missing facts. Maintain evidence → hypothesis → next action.
4. Classify the exact failed boundary. An unknown model or reference hash mismatch
   starts device-specific research and PORTING.md, not a universal refusal or a
   forced reference installation.
5. Use the working read contract and complete, verified source. Batch independent
   reads; keep writes sequential and scoped. Never repeat an ambiguous mutation.
6. Once privilege is established, reconcile access/cleanup and move to originals,
   independent recovery and a separate native candidate. Do not keep proving root.
7. Build and test static Home first, then video and optional features separately.
   Preserve unrelated accepted features. Do not turn provider experiments into
   mandatory setup dependencies.
8. Validate the actual screen, correct account/item/action, physical Home return
   and cleanup. Record unresolved behavior precisely.
9. Retain simulation successes and failures for the same modeled conditions,
   separately from hardware evidence. Use the last matching check receipt.
10. Publish only allowlisted, sanitized source/docs and accurate feature status.
    Keep useful authorized work moving; report a concrete resumable dependency
    when the next live action genuinely cannot proceed.

Required release checks: `node check.mjs`, `python3 check.py`,
`python3 privacy-check.py`, and `python3 agent.py simulate --json`.
They do not contact a TV and cannot certify a different firmware.

## Research map

- [Original implementation, native SDK/video contracts and pinned upstream sources](WORKED-EXAMPLE.md)
- [Alternative service paths, community evidence and corrected false negatives](ACCESS-RESEARCH.md)
- [Per-device porting, contracts and recovery](PORTING.md)
- [Provider API/source research and feature acceptance](CONTINUE-WATCHING.md)
- [Manufacturer OS directory, distinct from compatibility](VIDAA-MODELS.md)
- [Offline simulations and retained model results](SIMULATION.md), [LAB.md](LAB.md)
- [Design, upstream projects, media sources and license notices](CREDITS.md)

This is a transferable research and implementation process. It is not evidence
that one exploit, payload or build works on all VIDAA televisions.
