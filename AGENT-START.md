# Start from one link: Codex or Claude Code

Paste this into your local Codex or Claude Code:

> Use this: https://github.com/nineodernein/hisense-vidaa-clean-home

**Agent instruction:** treat "Use this" with this repository as a request to
begin this workflow for the owner's TV, not just summarize the README. Your
target is the native floating dock, editable favorites and direct physical Home
return, then optional animated wallpaper/manual saver. If the device differs,
research and adapt it through PORTING.md. Do not stop merely at a reference
profile mismatch or replace the target with a browser watcher without agreement.
Establish the specific authorized target before contacting a TV. Respect any
explicit repo-only/simulation-only scope in the conversation.

Give your local coding agent this repository link with the request to set it up
for your own TV. The agent should begin the local checks, not merely describe a
plan or ask you to copy every command. A cloud-only chat cannot reach your home
network; use an agent with terminal access on your computer.

If an agent only summarizes the link, this is the short, explicit request:

> Set up https://github.com/nineodernein/hisense-vidaa-clean-home for my own TV. Follow AGENT-START.md and MASTERPROMPT.md, begin the offline checks now, and ask only for missing device information or genuinely new permissions. Stop native installation if compatibility or recovery cannot be verified.

## Coding-agent procedure

1. Read this file and the root AGENTS.md / CLAUDE.md. Obtain a clean checkout or
   source ZIP from this repository; record the exact commit locally. Review the
   scripts before execution. Never pipe a download into a shell.
2. In the repository, run `python3 agent.py start --json` using Python 3.10+.
   This runs the offline checks and creates blank private device/UI templates.
   It does not contact the TV, change DNS, install packages, obtain root or write
   system files. Node 18+ is needed for the JS tests/build. On Windows use a
   supported `python`/`py -3` interpreter; the workflow is the same.
3. Read the JSON status and act on it:

| Status | Agent action |
| --- | --- |
| `needs_runtime` | Find an existing supported runtime first. Ask once before installing anything missing from an official source. |
| `checks_failed` / `stopped` | Explain the concrete failed check. Fix local issues; do not attempt native writes or weaken compatibility. |
| `needs_device_evidence` | Read MASTERPROMPT.md, COMPATIBILITY.md, NATIVE-ACCESS.md and RECOVERY.md. Collect only genuinely missing facts. |
| `needs_more_evidence` | Collect the missing model/hash facts through already authorized read-only access; do not treat missing data as an incompatibility finding. |
| `needs_model_research` | Stop native writes; continue exact-model documentation research and produce a redacted report. Do not claim the TV is technically impossible to customize. |
| `research_leads` / `needs_exact_device_research` | Follow the pinned primary sources, record actual capabilities, and continue PORTING.md. Chip-only results never approve installation. |
| `port_draft_needs_contract_review` | Inspect the owner's private OEM/SDK sources and populate the draft's evidence-backed reviews; do not just set flags to true. |
| `experimental_candidate_for_review` | A private static Home port was assembled. Prepare its separate live preflight/atomic apply/rollback; no device was tested by this command. |
| `reference_identity_reported` | The supplied identity/hashes match the reference; local originals, recovery and current live state still require verification. |
| `ready_for_local_review` | Review the prepared private artifacts and model-specific apply/rollback plan. This is not TV installation approval. |
| `local_artifacts_unchanged` | The local files still match; recheck live TV state before any separately authorized trial. |

4. Reuse the owner's existing information and authorization. Ask one concise,
   bundled question for anything still missing: the specific TV address/model,
   full firmware, whether it is currently in use, and authorized access if needed.
   Do not ask for streaming passwords, serial numbers, router passwords or a
   general network scan. If current scope is simulation only, STOP HERE.
5. Once read-only TV access is authorized, identify the actual device and original
   files. Fill `.private/device.json` with observed values; the template is
   deliberately blank. Copy originals to `.private/stock/home.js` and `saver.js`.
   Never copy expected values from compatibility.json and call them observations.
   Record remote hashes, ownership, modes, free space, native contracts, actual
   Store ID and the independently verified recovery/restart plan.
6. Run `python3 agent.py compatibility --json` for an allowlisted diagnostic
   summary. It separates missing observations from actual differences. Review the
   summary before sharing it; never attach the full device.json, SSH logs or OEM
   files. With a matching profile, run `python3 agent.py prepare --json`. Unknown firmware, corrupt backups,
   insufficient space or incomplete recovery evidence stop preparation. On a
   match it retains another set of private original copies, invokes the real
   guarded build and emits a private review manifest. No connection is made.
   For a mismatch, run `python3 agent.py research --json`, read PORTING.md and
   WORKED-EXAMPLE.md, then use `agent.py port` and `agent.py prepare-port` once
   device-specific original files and contract/recovery evidence are available.
   Do not stop all useful work simply because reference `prepare` cannot pass.
7. Before a TV trial run `python3 agent.py verify-plan --plan .private/plans/<id>.json`.
   This checks source/artifact integrity only; evidence fields are observations
   supplied by the agent, not remote measurements made by this tool. Recheck the
   live files, available space, maintenance deadline and independent recovery.
8. Follow MASTERPROMPT.md sections 3–6 and RECOVERY.md for the reviewed,
   firmware-specific apply/rollback procedure. Respect permissions already given;
   obtain authorization for genuinely new privilege/install scope. Preserve
   parental controls, DRM, authentication, updates and the vendor shell. A TV
   restart must not interrupt someone watching without authorization.
9. Confirm visible Home → app → physical Home and the requested features with
   the owner. Accept/cancel any trial watchdog before normal watching resumes.
   Close temporary access. Keep all backups, logs and generated bundles private.

## What “one link” does and does not mean

The link supplies a complete agent handoff plus executable checks and private
build preparation. It is not a trigger that can force an LLM to execute commands,
and it cannot manufacture permissions or compatibility. If an agent lacks local
tools, prerequisites or a verified access method, it must say what is missing.

There is deliberately no universal remote `apply` command or root payload. A
model-specific native modification still requires a reviewed access/recovery path.
The simulator cannot validate a TV's bootloader, actual SDK, video decoder, DRM,
power-loss behavior or firmware updates. See [simulation scope](SIMULATION.md).

No app accounts, manufacturer bundles, keys, IP addresses or media from the
original author are needed. The dock begins with the current TV's installed app
inventory and a static background. Custom video is a separate optional step.

## When another VIDAA model does not match

Do not end with “VIDAA confirmed, installation impossible.” State exactly which
facts are missing and which differ. With the owner's permission for read-only
research, consult the manufacturer's exact model documentation and alvidaa's
model catalog. Report whether a documented access route exists and which native
SDK/module/recovery contracts still need investigation. Do not scan a subnet,
install a diagnostic payload, patch offsets or modify native files as part of
this research. A new privileged access method requires its own reviewed scope.

A new device is a separate development path with its own original hashes,
implementation, recovery plan and hardware acceptance. The agent should do that
work within the owner's authorized scope; the owner need not invent it.
[PORTING.md](PORTING.md) supplies the executable private draft/build procedure,
two explicit SDK adapters, review criteria and the trial sequence.
[WORKED-EXAMPLE.md](WORKED-EXAMPLE.md) records the successful original techniques
and failed approaches. Keep the reference build stopped; continue the port.
Simulation cannot create hardware evidence or open a firmware with no known path.
