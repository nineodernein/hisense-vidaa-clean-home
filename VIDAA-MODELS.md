# Which TVs use VIDAA, and which work with Clean Home?

Research checked: **2026-11-12**. This page distinguishes the operating system
from compatibility with this particular native dock.

**Confirmed here:** the original integration on one Hisense with internal model
`43A53FEVS_0004`, MTK9602, VIDAA U9 and native firmware
`V0000.09.09F.P0930`. The retail model was not conclusively verified. Do not turn
the previously presumed `43A6CG` name into a supported-model claim.
See [the exact evidence and feature limits](COMPATIBILITY.md). The generalized
public build has offline tests; it has not been freshly deployed to that TV.

**No other model is currently confirmed with this repository's dock.**

## Hisense models officially listed with VIDAA

These are concrete examples from Hisense's German product pages, not an exhaustive
global catalog and not a list of TVs on which Clean Home has been installed.

| Exact example | Regional manufacturer evidence | Clean Home native dock |
| --- | --- | --- |
| Hisense 43A6N | [German 43A6N page: VIDAA Smart OS](https://de.hisense.com/produkte/tv/4k-ultra-hd-tv/TV-SET-43A6N-HSN/p/000000000020014042) | Not tested |
| Hisense 55E7Q | [German 55E7Q page: VIDAA Smart OS](https://de.hisense.com/produkte/tv/qled-tv/TV-SET-55E7Q-HSN/p/000000000020015899) | Not tested |
| Hisense 65U7Q | [German 65U7Q page: VIDAA Smart OS](https://de.hisense.com/produkte/tv/uled-miniled-tv/TV-SET-65U7Q-HSN/p/000000000020015891) | Not tested |
| Hisense 65U8Q | [German 65U8Q page: VIDAA Smart OS](https://de.hisense.com/produkte/tv/uled-miniled-tv/TV-SET-65U8Q-HSN/p/000000000020016068) | Not tested |

Hisense also sells other operating systems. Its [US television catalog](https://www.hisense-usa.com/televisions)
separates smart-TV platforms. A Hisense badge or a similar series name does not
identify the OS. Check the exact regional product page, complete model suffix
and the installed TV firmware; do not extrapolate these examples to every size
or country variant.

## Other brands with documented VIDAA TVs

| Brand | Evidence / examples | Clean Home native dock |
| --- | --- | --- |
| Toshiba | The [manufacturer's catalog](https://toshiba-tv.com/files/Toshiba_TV_Catalog_2025_Low%20size_compressed.pdf) groups VIDAA families including UV23/UV33, UV24/UV34, QV24/QV34 and UV3F; [43UV2363DG datasheet](https://toshiba-tv.com/es-es/pdf/43uv2363dg) gives a concrete example | Not tested |
| Loewe / We. by Loewe | [We. SEE 32 lcd](https://www.loewe.tv/eu/en/tv/tv/we-see-32-lcd/2283661) lists Loewe OS7 based on VIDAA; this branded variant must not be assumed identical to Hisense firmware | Not tested |
| MEDION | [LIFE MD 840102](https://www.medion.com/de/shop/p/performance-tvs-medion-life-md-840102-smart-tv--modell-2026-100-3-cm-40--full-hd-display-pvr-ready-hd-triple-tuner-vidaa-app-store-netflix-disney--dazn-amazon-prime-video-paramount--apple-tv-magenta-tv-hbomax-rtl--joyn-app-30042059A1) explicitly describes VIDAA | Not tested |
| KONKA | [Official VIDAA OS range](https://www.konkaglobal.com/product/televisions/Vidaa_OS/); exact regional model still required | Not tested |

[VIDAA's own platform page](https://www.vidaa.com/vidaa-os/) also names Newsan,
BGH, Element, Schneider, Nordmende, Shinon, Vortex, AKAI, NIKAI, BRUHM and General
Gold, alongside Hisense, Toshiba, Loewe and We by Loewe. That is brand-level OS
evidence only. It does not certify every product from those brands or this mod.

There is no complete, versioned worldwide model-and-firmware support list in the
manufacturer sources reviewed here. This directory deliberately uses sourced
examples instead of claiming to cover every VIDAA television.

## Upstream community evidence is a separate category

[alvidaa's model/firmware catalog](https://github.com/carteakey/alvidaa/blob/main/docs/models/README.md)
reports different outcomes. Selected examples, as reviewed above:

| Upstream model and exact firmware | What upstream reports | This dock |
| --- | --- | --- |
| 32A35HUV — V0000.09.01O.P0814 | Root access on MTK9602 | Not tested |
| 75U8QTUK — V0000.09.60I.Q0813 | Root and an owner-verified native DOM Home | Not tested |
| 50A6Q — V0000.09.61B.Q0721 | Root on a Novatek platform with a different access route | Not tested |
| 43A5LE — V0000.09.60A.Q0707 | Browser launcher/watcher; root not attempted | Not tested |
| 65U7H — V0000.06.29X.P0813 | Some bridge operations; root not achieved in the report | Not tested |

These are attributed upstream reports, not our independent hardware tests or
instructions to reuse their access mechanisms. Root, a browser launcher and a
native dock are different results. A matching firmware suffix alone is not a
match. Check the full model, firmware, platform and original module hashes.

## What your coding agent should do

1. Identify the exact TV, region, internal model, OS, SoC and full firmware.
2. Read [COMPATIBILITY.md](COMPATIBILITY.md) and compare the existing build profile.
3. Verify the original module hashes, required native APIs and recovery path.
4. Treat unknown profiles as unverified; stop native writes rather than changing
   expected hashes merely to make the build accept them.
5. Record feature-by-feature device results before adding a new support claim.

[DNS filtering](DNS.md) can be investigated separately without native root.
Its domain coverage and streaming compatibility still need testing; a cleaned
stock Home does not prove the custom dock is compatible.

Contribute a redacted report via [CONTRIBUTING.md](CONTRIBUTING.md). Do not post
account information, network addresses, serial numbers, keys or OEM bundles.
