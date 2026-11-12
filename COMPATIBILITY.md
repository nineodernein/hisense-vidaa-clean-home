# Hisense VIDAA compatibility

This project targets a native VIDAA/Cobalt Home component. It does not target
Android TV/Google TV, Roku TV, Fire TV or a generic Linux desktop.

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

- This generalized public source build on a physical TV.
- The packaged shared media chooser on a physical TV.
- Automatic Home saver after a real ten-minute idle test.
- A custom saver over a paused Netflix movie and session-preserving return.
- Cold boot/standby persistence across all firmware or future updates.
- Other model/firmware families.

A same-family TV still needs original hashes, app/service contracts and recovery
checks. Unknown hash means stop, not “update the expected hash and try”.

For other devices consult the [alvidaa model catalog](https://github.com/carteakey/alvidaa/tree/main/docs/models)
and [native implementations](https://github.com/carteakey/alvidaa/tree/main/tools/launcher-host).
Those are upstream references, not automatic authorization to run their commands.
