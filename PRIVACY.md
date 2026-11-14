# Public repository privacy boundary

The public repository contains the playbook, generic source, a reference firmware
profile, tests, proposed domain rules, licenses and one owner-approved preview.

It must never contain:
- passwords, private keys, tokens, paired MQTT credentials or recovery codes;
- personal email, home IP/MAC addresses, serial numbers, SSIDs or user home paths;
- device logs, browser state, engine environment, packet captures or memory dumps;
- OEM firmware bundles, compiled patched Home/Saver files, backups or IPK packages;
- the owner's wallpaper videos, paid icon collection or iCloud contents.

The preview was explicitly chosen for publication. Its JPEG metadata is stripped;
its visible app labels/time are part of that approved illustration. It does not
distribute the source icon pack or video.

The build uses an allowlisted UI schema and writes only below .private/.
Unknown configuration keys do not enter the TV bundle. Runtime debug-file output
is off by default. No external analytics/CDN is added by the dock. Vendor services
and apps still have their own behavior; this is not a complete privacy claim.

Run privacy-check.py before publishing, and inspect the staged Git diff/archive
manually. A scanner is a useful gate, not proof that arbitrary future additions
are safe. Generated OEM bundles are private even if a secret scan finds nothing.

## Device contents and shared reports

The same boundary covers data read from the owner's devices and other owners'
reports. A VIDAA/vendor file may contain account IDs, session tokens, signed URLs,
network addresses or viewing history. Its vendor origin does not make that data
public. Publish technical behavior and minimal API contracts, not raw private
responses, browser profiles, databases, firmware dumps or chat screenshots.

Use synthetic titles, episode values, content IDs and timestamps in tests.
Keep actual watch history, profile names, refresh credentials and Quick Connect
codes private. Redact private query parameters before sharing any URL. Model
families, firmware versions and generic SDK names may be documented; serial
numbers and unique device/account identifiers may not.

Before release, inspect the exact changed files and commit metadata as well as
running the allowlist scanner. Check added links, images, generated artifacts and
metadata. Do not upload the working directory or .private/ as a troubleshooting
archive. Adding a new public document to the allowlist is not a waiver of its
content review. Public compatibility reports remain anonymous and stage-specific.
