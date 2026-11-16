# Hisense VIDAA Clean Home
## Native app dock, custom home screen and animated wallpapers

[Deutsch](README.de.md) · [Start with your coding agent](AGENT-START.md) · [Download & setup](START-HERE.md) · [Compatibility](COMPATIBILITY.md) · [Offline simulation](SIMULATION.md) · [VIDAA brands & models](VIDAA-MODELS.md)

Replace the sponsored Hisense VIDAA home screen with a local, native app dock.
Keep your real installed apps, HDMI inputs and TV settings. Long-press OK to
reorder favorites or remove them from the home screen. Add your own animated
wallpapers and video screensavers.

![Hisense VIDAA custom home screen with a floating app dock, native Apps and Inputs tabs, and an animated night-scene wallpaper](preview.jpg)

*Example from the reference project. The screenshot is a design preview, not a
live screen capture. Its custom icon pack and wallpaper video are not bundled.
The default build uses the TV's cached icons or text tiles.*

### Start with Codex (recommended)

```text
Use this: https://github.com/nineodernein/hisense-vidaa-clean-home
```

The [agent instructions](AGENT-START.md) give a concrete goal and executable
workflow. They include [the successful techniques and failed approaches from
the original project](WORKED-EXAMPLE.md), plus [per-device porting](PORTING.md)
when another TV does not match the reference. A mismatch starts research and
adaptation; it is not automatically the end of the task.
The [access investigation playbook](ACCESS-RESEARCH.md) supplies concrete read
contracts, separate HiUtils/Fetcher routes and corrected false negatives. Agents
must keep an evidence ledger and pursue the next source-backed hypothesis when
one interface fails. Community observations remain separate from verified ports.

**Codex is the maintainer's recommended local coding agent for this project.**
Repeated community reports describe Claude/Claude Code refusals; the previously
documented 50E6NT owner now reports success after switching to Codex. This is
community experience, not a comparative benchmark or a guarantee for every TV.
See [agent choice and troubleshooting](AGENT-TROUBLESHOOTING.md#recommended-coding-agent-codex).

Give the repository link to local Codex with a request to set it up for your own
TV. Other capable local coding agents can follow the same workflow. The agent
should begin the local checks automatically. If it only summarizes the link,
paste this explicit instruction:

> Set up https://github.com/nineodernein/hisense-vidaa-clean-home for my own TV. Follow AGENT-START.md and MASTERPROMPT.md and run the offline checks now. Use ACCESS-RESEARCH.md to investigate missing access and pursue source-backed alternatives after a failed route. Reuse existing facts and permissions; keep backups private and verify recovery before native changes. Do not touch other devices.

The [agent entry point](AGENT-START.md) tells the agent what to execute and how to
handle each result. The [masterprompt](MASTERPROMPT.md) supplies the detailed
procedure. With Python 3.10+ and Node 18+ already available, the first command is:

```sh
python3 agent.py start --json
```

It checks the project, runs offline simulations and prepares blank private files.
It does not contact a TV or install software. The agent then collects missing
device evidence, prepares verified backups and a private build for review.
Use an agent with terminal access on your own computer; a remote web chat usually
cannot reach your TV. This is an
**agent-assisted recipe with source code**, not a universal one-click jailbreak.
An authorized maintenance channel and device-specific compatibility evidence
are prerequisites for native installation, not for beginning source research.
No promise of “a few minutes” on every model.

Two explicit native SDK adapters are included. The private port builder uses
the new device's own original Home and documented contract/recovery evidence;
it does not relax the reference hash guard. Neither adapter selection nor a
passing offline test establishes hardware support. Animated media on a new
firmware follows a successful static-Home trial and its own native-player review.

### Less manual work during setup

The [remote and browser guide](REMOTE-AND-BROWSER.md) explains normal TV pairing,
agent-driven navigation and temporary browser diagnostics with direct result
transfer. These are setup tools; the requested Home component stays native.
No universal remote client or pairing credentials are bundled.
If Claude Code or another agent stops, [troubleshoot the actual blocker](AGENT-TROUBLESHOOTING.md)
and continue permitted work instead of restarting the entire investigation.
The guide does not bypass model policies or permission controls.

### What you get

- A **native VIDAA home component**, not a browser page reopened by a watcher.
- A horizontal app dock with soft edge fades and visible remote-control focus.
- Long OK: move a favorite or remove its tile. This does **not** uninstall the app.
- App Store pinned at the right, where supported by the model's app inventory.
- Apps, inputs and TV settings; normal up/down navigation in the input grid.
- Local MP4 wallpaper playback using the TV's native media player.
- A shared media catalog for background/saver selection; see status below.
- An optional, TV-scoped [DNS ad-blocking guide](DNS.md).
- [Libraries.dev](https://libraries.dev/) Liquid Metal design attribution.
  The TV uses pre-rendered metal-fx frames instead of running React/WebGL.

### Choose your route

| Want | Start here | Access |
| --- | --- | --- |
| Remove VIDAA home ads and recommendations | [DNS filtering](DNS.md) | A DNS filter; no TV root |
| Get the native dock and direct Home return | [Agent masterprompt](MASTERPROMPT.md) | Model-matched maintenance/root access |
| Add animated backgrounds | [Animated wallpapers](ANIMATED-WALLPAPERS.md) | A working native installation; your own clips |
| Understand a browser alternative | [Compatibility](COMPATIBILITY.md) | Broader availability, but Home may bounce through stock VIDAA |

### Consolidated project research

The [complete project abstract](PROJECT-ABSTRACT.md)
([Deutsch](PROJECT-ABSTRACT.de.md)) records the native route, video fixes, community
findings, failed assumptions and next-agent instructions. The
[Continue Watching research](CONTINUE-WATCHING.md) separately records Jellyfin
and provider-specific previews. Those private preview adapters are **not shipped
in this public build**; their acceptance status is explicit.

The masterprompt now directs agents to resolve the next unproven boundary,
reuse confirmed results and pursue source-backed alternatives without repeating
onboarding or ambiguous writes. It does not turn a simulated success or an
unknown firmware into installation approval.

### Tested honestly

**Does this work on every VIDAA TV? No.** VIDAA is also used on selected Toshiba,
Loewe/We. by Loewe, MEDION and other TVs, but using the same OS is not proof that
this native modification works. [Check the sourced brand/model directory](VIDAA-MODELS.md)
and the [project's actual test status](COMPATIBILITY.md) separately. Other Hisense
sets can run Google TV, Roku TV or Fire TV instead.

The original integration was verified on **one MTK9602 / VIDAA U9 / P0930 device**.
Native Home → app → Home, favorite editing, input navigation, a looping local
video and the manual Rainy-style saver/return from Home were confirmed.
The precise [profile and original-file hashes](compatibility.json) are included.

**Community success reports:**

- **50E6NT / V0002.09.60A.Q0707:** the previously documented owner reports
  successful setup and supplied a dock photo after switching to Codex, according
  to the maintainer. See the [50E6NT evidence record](COMPATIBILITY.md#community-case-50e6nt).
- **55U7Q / V0000.09.60A.Q0602** (extended X0003.W01.Y01.J01): another owner
  reports successful setup and supplied a dock photo.
  See the [55U7Q evidence record](COMPATIBILITY.md#community-case-55u7q).

Physical Home return, persistence and optional features were not separately
reported for these follow-ups. These positive owner reports do not change the
reference profile or installation checks.

This public package has been generalized and tested offline. It has **not** been
installed as a new build on the reference TV. Shared on-screen media selection
was prepared and tested offline; it is not a confirmed deployed feature.
The ten-minute Home idle test is still open. A custom saver over **paused
Netflix is not implemented**. Do not claim otherwise or read Netflix memory.

### Does this debloat VIDAA or make every app ad-free?

It cleans the home interface and offers selective DNS filtering. It does not
remove VIDAA, uninstall every preinstalled package, replace the TV operating
system, or remove ads served inside YouTube/Netflix/other streaming content.
DNS filtering is not a complete privacy guarantee. ACR and microphone settings
are separate from launcher customization.

### Download, inspect, recover

Use **Code → Download ZIP**, extract it, then read [START-HERE.md](START-HERE.md).
The tools do not install dependencies, gain root, change DNS, or contact a TV
when you download or build. `build.mjs` refuses unknown original module hashes.
OEM bundles and device backups stay in `.private/` and must never be published.

Read [recovery](RECOVERY.md), [privacy](PRIVACY.md), [security](SECURITY.md) and
[credits/licenses](CREDITS.md) before a native trial.
For supported-model reports, use [CONTRIBUTING.md](CONTRIBUTING.md).

### Noncommercial use

New original maintainer contributions are available under
[PolyForm Noncommercial 1.0.0](LICENSE). Personal use and noncommercial hobby
customization are allowed; commercial use of those contributions requires
separate permission. [License scope](LICENSE-SCOPE.md) explains the retained
upstream MIT rights and earlier MIT releases. This is source-available for
noncommercial use, not a retroactive restriction on previously licensed code.

### Why this exists

VIDAA's stock home screen can be noisy, slow and difficult to personalize.
This project records the path from a browser workaround to a native component
inside the existing home engine, so another coding agent can start with the
working architecture instead of repeating the same dead ends.

Built on [alvidaa](https://github.com/carteakey/alvidaa), its native platform
adapter and the Free My TV design lineage. Independent community project;
not affiliated with Hisense, VIDAA, Netflix, Apple or Libraries.dev.
