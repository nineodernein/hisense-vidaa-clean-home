# Hisense VIDAA compatibility

This project targets a native VIDAA/Cobalt Home component. It does not target
Android TV/Google TV, Roku TV, Fire TV or a generic Linux desktop.

Last reviewed: 2026-11-12. **One reference unit has confirmed native integration;
no other model is claimed as tested with this project's dock.** A TV using VIDAA
is a research candidate, not an installation approval.

## Support levels

| Evidence | Meaning | Can the native build be installed on that basis alone? |
| --- | --- | --- |
| Reference integration verified | The original project ran on the exact profile below; owner confirmed the listed behaviors | No: the public package still needs its own controlled trial, matching hashes and recovery checks |
| Public package tested offline | Source checks and build behavior pass on a computer | No physical-TV claim |
| Upstream model/firmware report | Another project reports access or a launcher on a specific device | No: this dock's integration must be checked separately |
| Manufacturer confirms VIDAA | Official product data identifies the operating system | No: access, native APIs, module layout and video support remain unknown |
| Community reports information getters | Owner reports model/chip/region queries working | No: file access, root and native Home are separate, unverified stages |
| Community reports file reads | Owner reports structured read success at specific paths | No: source visibility, writes, cleanup, privilege and native Home are separate stages |

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
- Other model/firmware families.

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
