# Native access: what actually changed

The successful route replaced the /Launcher Vue component inside the existing
VIDAA home engine. It did not flash another OS or set a browser page as the default.
The original module registry, settings, app-control and input services remained.

Read [WORKED-EXAMPLE.md](WORKED-EXAMPLE.md) for the full sanitized development
handoff: access, native Home, cache/recovery mistakes, dock rendering and native
video. For a different device use [PORTING.md](PORTING.md) and
`python3 agent.py research --json`. The curated research catalog includes a newer
pinned upstream revision and distinguishes blocked browser writes from other
documented service paths. It does not execute or approve those paths.

[ACCESS-RESEARCH.md](ACCESS-RESEARCH.md) is the next-step playbook when access is
missing. It gives concrete HiUtils/vowOS read contracts, the separate Fetcher
route, error classification and an evidence ledger. Keep progressing through
source-backed hypotheses instead of requiring a completed exact-firmware guide
before doing any useful investigation. Live writes retain their own review.

## Known working architecture

1. Use an authorized, model-matched local maintenance channel.
2. Back up the original launcher and screen-saver modules.
3. Append the local adapter/core/dock wrappers to the unmodified vendor bundle.
4. Wrap _V_M_.launcher and replace only the component at /Launcher.
5. Let the native app-control layer launch real apps with its normal checks.
6. Replace only the native saver view for the optional local video.
7. Rebuild the relevant renderer caches and restart the existing UI with its own
   saved environment. Keep that environment private; it may contain secrets.

On the reference build, a browser-exposed native service/file bridge could stage
a one-time local IPK whose postinst ran with UID 0. This enabled a temporary,
key-only maintenance connection limited to the owner's computer. A package manager
error code did not by itself prove the postinst failed. UID, exit result, artifacts
and cleanup were verified separately.

## Start from the published, model-specific research

[alvidaa](https://github.com/carteakey/alvidaa) documents access paths and native
launcher integration. The reference work used revision
4bbf060aa7bc1532478517d5cd4d1484bd28ad97 as research input.
Use its [model catalog](https://github.com/carteakey/alvidaa/tree/4bbf060aa7bc1532478517d5cd4d1484bd28ad97/docs/models)
and inspect the exact recipe before execution.

A similar P0930 model with a different full firmware string is **not** a confirmed
match. This repository intentionally ships no prebuilt privileged package, no
foreign key/certificate, no default root password and no persistent boot hook.
Access setup remains a reviewed per-device step. Do not hide it behind “one click”.

## Facts that saved time

- hisense://debug did not expose the expected installer on the reference unit.
  Repeating that URL did not establish native access.
- A RemoteNow/MQTT remote can control apps without replacing Home.
- A watcher that reopens a browser causes a visible VIDAA bounce.
- Root access and a native module replacement are separate steps.
- The native SDK/renderer differs from the TV browser.
- A UI restart can interrupt a movie, even if the Netflix process stays alive.
- A native video PLAYING event is not proof it is visible through the UI layers.

Preserve secure boot, system partitions and security update functionality.
Do not publish OEM bundles or private recovery state.
