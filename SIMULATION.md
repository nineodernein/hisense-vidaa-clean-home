# Offline simulation: tested behavior and limits

Run from a fresh checkout with Python 3.10+ and Node 18+:

```sh
python3 agent.py simulate --json
```

No TV, SSH endpoint, DNS server, credentials, manufacturer bundle or original
author's files are used. Fixtures are synthetic and temporary. The production
profile is not weakened: synthetic originals cannot pass its hashes. There is
no simulation flag that allows them into the production CLI build.

## What is exercised

| Test | What it verifies |
| --- | --- |
| `check.mjs` | Native source syntax; config/hash rejection; independent media choices; mock SDK navigation, long OK, favorites, Store and stock fallback. |
| `check-video.cjs` (through check.mjs) | Mock player prepared/play/loop events, session ownership, timeout fallback, listener cleanup, selected-video cycle and still-image behavior. |
| `check-bundle.mjs` | The actual production assembly function with synthetic OEM modules: native Home → app → Home lifecycle, favorites menu, input grid, Store, full bundle load, SDK failure fallback and saver integration. |
| `check-agent.py` | Device identity, original/remote hashes, metadata, free-space and recovery gates; blank evidence and test fixtures rejected; private path traversal/symlinks rejected; overwrite/artifact-corruption checks; redacted compatibility reports distinguish missing facts from mismatches. |
| `check.py` | Client-scoped DNS rendering and video conversion graph validation. |
| `check-port.py` | Exact-model versus chip-only research, no false A7GQ/E7NQ/firmware match, unknown devices retain an investigation path, community file-read reports retain missing-path/incomplete-source limits without becoming write/root/native approval, private original/review evidence, source/identity/hash changes, actual Node experimental build, unchanged saver and artifact verification. |
| `privacy-check.py` | Explicit public-file allowlist, tracked-path checks and known sensitive-data/metadata patterns. |

The Python suite also models a failed trial and atomic restoration of synthetic
files in a temporary directory. This illustrates the recovery contract; it is
**not a test of the TV's restart mechanism or an implemented remote rollback**.
The GitHub workflow runs the same offline entry point on pushes and pull requests.

The fixture SDK returns invented app/input inventories. No Netflix, YouTube or
other streaming app is actually run. No physical remote key, video frame rate,
visual sharpness, power transition or real hardware playback is verified here.

The assembled-bundle tests exercise both `current-show-apps-v1` and `app-list-v1`
against distinct synthetic SDK method shapes. They check actual adapter selection,
APC command use without bypass flags, absent Store handling, app-detail mismatch
rejection, per-device asset mapping and stock Home fallback on missing contracts.
The experimental port path is separate from the fixed reference builder; it
does not grant any new model a tested hardware status.

## Local preparation is a separate step

`agent.py start` runs these checks and initializes `.private/` without overwriting
an existing device template. `prepare` requires actual per-device evidence and
original files; it creates private recovery copies and a real guarded bundle.
`verify-plan` checks the resulting hashes before review. A changed source or
artifact invalidates the prepared plan.

Evidence fields are supplied by the coding agent after authorized observation.
They are not cryptographic proof that an LLM observed the right TV. The tool has
no network transport and cannot independently verify those fields or the user's
permission. That verification belongs to the separately reviewed live procedure.

## Public status

The original custom installation was confirmed on one reference TV. This updated
public package has only been tested offline. No reference TV was contacted or
modified while adding this simulation. A fresh hardware trial, other models,
standby/cold boot, actual recovery and paused-app screensavers remain separate
unverified claims. Passing this suite is **not a zero-brick-risk certificate**.

## Persistent access experiments

See [LAB.md](LAB.md). `check-lab.py` is included in the offline suite and exercises response classification, route pivots, asynchronous cleanup, independent UID proof, the systematic matrix and persistent learning. `agent.py lab --matrix --json` saves modeled outcomes for later runs.
