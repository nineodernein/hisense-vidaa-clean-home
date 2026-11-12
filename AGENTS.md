# Agent instructions

This repository is an agent playbook and native Home source kit. Start at
MASTERPROMPT.md. Read COMPATIBILITY.md and RECOVERY.md before TV writes.

- Work only on an explicitly owned/authorized target. Respect watch-time pauses.
- Publishing/documentation tasks never authorize contacting or changing a TV.
- Preserve existing authorization; ask only for genuinely new access/scope.
- Match firmware and original-file hashes. Never edit a profile just to force a pass.
- Keep the existing OEM shell, parental checks, app authentication and updates.
- No network scanning, default passwords, permanent root listener or bootloader flash.
- No forced DNS changes to the whole household. Proposed rules are client-scoped.
- Keep private state in .private/; never publish generated OEM bundles, credentials,
  home-network identifiers, device logs, snapshots or personal media.
- Do not store passwords in source, commit messages, configuration examples or tests.
- Run node check.mjs, python3 check.py and python3 privacy-check.py before release.
- Use only official/pinned sources; no curl-to-shell and no unreviewed install scripts.
- Native Home tests require a rollback plan and a verified independent recovery path.
- Cancel/accept trial rollback before the owner resumes watching a film.
- Keep status honest: public packaging/media chooser offline-tested; paused Netflix
  automatic saver and real Home idle timeout unverified.
- No claims of universal compatibility, complete privacy or removal of streaming ads.
- Credit Libraries.dev/metal-fx, alvidaa and Free My TV; retain their licenses.
