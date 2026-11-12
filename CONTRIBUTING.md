# Contributing

Useful contributions are redacted model/firmware compatibility reports, fixes
with offline tests, accessible remote navigation, and reproducible media handling.

For a model report include internal model, SoC, full firmware string, original
module hashes if appropriate, and separately marked results for Home, App → Home,
inputs, favorite editing, video, standby and recovery. Do not invent “supported”
from a matching product name or an emulator test.

Mark each feature as **passed on device**, **failed**, **not tested** or
**offline only**. Name the exact project revision tested and distinguish a
manufacturer's VIDAA specification, an upstream access report and this project's
native dock running on hardware. Only the last can establish a new dock test
result. Report firmware changes as new observations, not a whole-series promise.

Never submit keys, tokens, email, IP/MAC addresses, serials, Wi-Fi details, OEM
bundles, diagnostics, screenshots of accounts or personal media.
Do not widen a compatibility profile merely to bypass a build error.

Run node check.mjs, python3 check.py and python3 privacy-check.py.
Keep upstream licenses and explain any behavior or compatibility changes.

New original contributions are submitted under PolyForm Noncommercial 1.0.0;
see LICENSE-SCOPE.md. Identify and preserve the licenses of any third-party code.
Do not label the new restricted contributions as MIT or OSI open source.
Use PORTING.md for device-specific development and include actual feature
acceptance separately from upstream reports or simulated success.
