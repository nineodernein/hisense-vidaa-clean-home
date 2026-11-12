# Native Home recovery and acceptance

Prepare recovery before any write. A nice-looking preview is not a recovery plan.
Match that plan to the action: a bounded diagnostic artifact needs its own
collision/cleanup and failure review; replacing Home needs the full independent
recovery contract below. These write requirements do not prevent offline source
analysis or already authorized read-only diagnostics. See ACCESS-RESEARCH.md.

## Private backup

`agent.py prepare` validates supplied device evidence against the fixed profile,
retains additional private original copies, and produces a local artifact/hash
plan. `verify-plan` detects changes to those local artifacts. Neither command
contacts the TV or verifies that a live recovery channel works; check that
separately. See AGENT-START.md for the automated local handoff.

For another device, `port` retains its own original Home and `prepare-port`
validates the separate private reviews before creating a static candidate.
The same live recovery contract applies; those local commands do not verify
recovery on real hardware. First ports preserve the OEM saver. See PORTING.md.

Use the exact module paths from compatibility.json only after verifying the
device. Save both original modules on the owner's computer and on an appropriate
private TV release directory. Verify SHA-256 on both sides and preserve ownership
and mode. Never rely on somebody else's downloadable firmware backup.

Also record the verified UI engine executable identity, current process ID,
environment needed to restart it, and cache paths. Keep these records private.
Do not include environment files in bug reports or GitHub uploads.

## Apply contract

The agent prepares an explicit script for the known firmware:
- recheck current module hashes before writing;
- verify backup and candidate hashes;
- check disk reserve and acquire a single update lock;
- identify the exact UI engine by executable identity, not a broad process name;
- stop the engine gracefully and fail if it does not stop;
- copy a candidate to an adjacent temporary file, set verified owner/mode, rename;
- move aside only the relevant compiled_js/uncompiled_js caches;
- restart through the verified vendor mechanism with the saved private environment;
- verify one intended engine instance, module hashes and visible UI behavior.

This repo's build performs no remote apply. Do not execute a borrowed restart
script without verifying it matches the current firmware.

## Rollback contract

Restore the exact previous module after checking that the current file is either
the expected candidate or the expected original. Refuse an unknown third version.
Rebuild caches from the actual restored module set. Restoring a whole old cache
can silently roll back another module too.

Do not delete system packages, format partitions or factory-reset as a routine
rollback. Leave old assets until the restored UI works. Remove only your own
known temporary files afterward, using an explicit manifest.

## Trial deadline

A test may have a bounded automatic rollback. Its deadline must be visible to
the owner. Accept or cancel that guard before allowing normal movie watching.
The reference project learned that an automatic UI rollback can interrupt Netflix.
Do not leave a “successful” test with a rollback still scheduled.

After visual acceptance, test app → physical Home with independent recovery
still available. Record which checks actually passed. Close maintenance at the
authorized deadline; no silent renewal or autostart.

## Updates

An OTA update can replace modules, close an access path or change SDK contracts.
Keep updates enabled. After an update, back up and reassess; do not blindly reinstall
an old patched bundle.
