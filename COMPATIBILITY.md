# Hisense VIDAA compatibility

This project targets a native VIDAA/Cobalt Home component. It does not target
Android TV/Google TV, Roku TV, Fire TV or a generic Linux desktop.

Last reviewed: 2026-11-15. **One reference unit has confirmed native integration.
A separate 55U7Q owner reports a successful setup and supplied a photo of the
custom dock; feature-by-feature acceptance remains open.** A TV using VIDAA is
a research candidate, not an installation approval.

## Support levels

| Evidence | Meaning | Can the native build be installed on that basis alone? |
| --- | --- | --- |
| Reference integration verified | The original project ran on the exact profile below; owner confirmed the listed behaviors | No: the public package still needs its own controlled trial, matching hashes and recovery checks |
| Public package tested offline | Source checks and build behavior pass on a computer | No physical-TV claim |
| Upstream model/firmware report | Another project reports access or a launcher on a specific device | No: this dock's integration must be checked separately |
| Manufacturer confirms VIDAA | Official product data identifies the operating system | No: access, native APIs, module layout and video support remain unknown |
| Community reports information getters | Owner reports model/chip/region queries working | No: file access, root and native Home are separate, unverified stages |
| Community reports file reads | Owner reports structured read success at specific paths | No: source visibility, writes, cleanup, privilege and native Home are separate stages |
| Community reports setup success with a dock photo | Owner reports success; the supplied photo shows the custom dock | No: native Home return, tested revision, persistence and recovery still need separate evidence |

[VIDAA-MODELS.md](VIDAA-MODELS.md) lists sourced Hisense examples and other VIDAA
brands. It is an OS directory, not a supported-install list. The sole native build
reference profile remains [compatibility.json](compatibility.json).

Other devices now have a separate [porting workflow](PORTING.md), with an offline
research router, private original-file draft and experimental static-Home builder.
It includes two explicit SDK adapters. This removes the single-profile dead end
from the agent workflow; it does **not** add hardware support claims. The
[research catalog](model-research.json) separates exact-model and chip-only leads.
It also returns a concrete [access research playbook](ACCESS-RESEARCH.md) even
when no model matches. Community observations are listed separately from project
hardware acceptance. The 50E6NT Q0707 owner now reports verified source transfer,
two marker write/readback/removal runs and a later diagnostic postinst UID 0
proof. Diagnostic-package cleanup completion, active maintenance access, recovery
and native Home remain unconfirmed in the shared report. This does not approve
installation on that unit or establish another unit's compatibility.

## Reference evidence

| Item | Observed reference |
| --- | --- |
| Internal model | 43A53FEVS_0004 |
| SoC | MTK9602 |
| OS | VIDAA U9 |
| Native firmware getter | V0000.09.09F.P0930 |
| Marketing model | Not conclusively verified; do not use a presumed 43A6CG label as a compatibility check |
| Home renderer | Native Cobalt; 1920×1080 UI, not proof of native 4K UI |
| Required factories | _V_M_.launcher, _V_M_['screen-saver'], _V_SDK_ |
| Reference original hashes | compatibility.json |

The browser's Chromium version and resolution are not the native renderer's
capabilities. Canvas/WebGL effects that work in the browser may fail in Cobalt.

## Verified in the original project

Native app dock, direct Home return, app launches, long-OK favorite editing,
App Store access, input navigation, a native looping local video and a manual
video saver returning to Home were confirmed by the owner.

## Not verified

The offline agent workflow and assembled-bundle simulations are described in
[SIMULATION.md](SIMULATION.md). They exercise synthetic SDK/player/file behavior;
passing them does not add another supported TV or prove physical recovery.

- This generalized public source build on a physical TV.
- The packaged shared media chooser on a physical TV.
- Automatic Home saver after a real ten-minute idle test.
- A custom saver over a paused Netflix movie and session-preserving return.
- Cold boot/standby persistence across all firmware or future updates.
- Full feature acceptance on other model/firmware families, including the
  separately reported 55U7Q dock success below.

A same-family TV still needs original hashes, app/service contracts and recovery
checks. Unknown hash means stop the reference write path, not “update the
expected hash and try”. Continue authorized port research with that device's
originals and separate evidence rather than forcing the fixed build.

For other devices consult the [alvidaa model catalog](https://github.com/carteakey/alvidaa/tree/main/docs/models)
and [native implementations](https://github.com/carteakey/alvidaa/tree/main/tools/launcher-host).
Those are upstream references, not automatic authorization to run their commands.

## Why one VIDAA device does not validate every other one

The full firmware, SoC, native renderer, module hashes, app/service contracts and
available maintenance path must match. Screen size, series name, a shared VIDAA
major version or the ability to launch a browser is insufficient. The same retail
family can differ by country, model suffix and update. Root access alone does not
prove that the dock or the native video background works.

DNS filtering is a separate route: it does not require this native build profile,
but each candidate domain still needs client-scoped observation and streaming tests.
An ad-blocking success is not evidence of native Home compatibility.

To add confirmed support, submit the redacted feature results described in
[CONTRIBUTING.md](CONTRIBUTING.md). Preserve the exact firmware and original-file
hash checks; do not add an entire retail series from one successful test.

## Later optional integrations on the original unit

The original unit's separate Jellyfin app integration was owner-confirmed.
Private Continue Watching cards were accepted for Netflix (title/artwork/action),
Prime (also season/episode), and Disney+ (also remaining time/progress and correct
episode action). Netflix episode/remaining-time and Prime remaining-time remain
open. The YouTube trial was not accepted; other provider cards remain unverified.
These adapters are not included in the public source build. See the full
[provider matrix](CONTINUE-WATCHING.md) and [project abstract](PROJECT-ABSTRACT.md).

## Community case: 55U7Q

An anonymous owner followed up on the earlier enquiry with a successful setup
report and a photograph showing the custom dock. The model and firmware below
come from the owner's original identity message; the success report refers back
to that message.

| Item | Reported evidence |
| --- | --- |
| Retail model | 55U7Q |
| Full software version | V0000.09.60A.Q0602 |
| Extended version | X0003.W01.Y01.J01 |
| Setup outcome | Owner reports that it worked |
| Visible result | Custom dock shown in the supplied TV photo |
| Tested project revision, internal model, SoC and original hashes | Not supplied |
| Native launcher integration and physical Home return | Not established by the photo/message |
| Reboot/standby persistence and independent recovery | Not reported |
| Video, screensaver, editing, inputs and provider previews | Not separately reported |

This **replaces the previous identity-only status** with a positive community
result. It is not an independently reproduced port or a new reference profile.
The private message, photograph and account identifier are not redistributed.
The [machine-readable observation](model-research.json) preserves this distinction.

On that working unit, resume from the retained private setup evidence and collect
only missing acceptance results. A concise follow-up can report the tested
revision, app → physical Home return, and an owner-scheduled restart. Do not
repeat installation or privilege tests merely to complete the public catalog.
For another 55U7Q, the report is a useful lead; use that unit's own originals,
contracts and recovery checks. Similar firmware strings do not prove equal
permissions or an identical build.

The separate V01.09.60G.Q0612 enquiry was identified by its owner as a 32-inch
E5ST and still has no reported setup result.
