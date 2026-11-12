# Find a device-specific VIDAA access route

This is the investigation playbook for Codex, Claude Code and other local coding
agents. Use it when the owner requests the native dock and access is missing,
an upstream recipe differs, or a diagnostic fails. Keep working toward native
Home; do not turn an unknown firmware into an automatic DNS/browser fallback.
Be persistent about collecting evidence and adapting code. Each live action
still needs the owner's applicable authorization and a bounded, reviewed scope.
Repo-only work never authorizes TV contact.

## Work the next unresolved capability

The chain is **device identity → browser/bridge context → file/service access →
bounded maintenance privilege → original native contracts → static Home → video**.
Evidence at one stage does not prove the next. A missing recovery shell does not
prevent offline research or an already authorized identity/file read. A working
getter does not authorize or prove a package installation.

Maintain a private investigation ledger under `.private/evidence/`. For each
hypothesis record the exact device/firmware, pinned source, interface, argument
shape, expected effect, actual response, evidence file/hash, interpretation and
next discriminating step. Preserve an authorization summary, temporary-artifact
list and cleanup status. Reuse existing facts; never ask for the full identity
again merely because the previous route failed.

Advance through this loop:

1. Select the first unresolved capability needed for native Home. Rank leads by
   same-device evidence, same-service source, then related-model reports.
2. Inspect the relevant source locally. Form a specific, falsifiable hypothesis;
   prepare the smallest diagnostic that distinguishes it from alternatives.
3. Execute within existing authorization. If new scope is needed, finish the
   concrete probe/cleanup plan first and ask once for that scope. Do not ask for
   permission to keep reading public source or preparing local files.
4. Classify the response at the tested interface. Fix a demonstrated transport,
   argument or context error before calling it a permission gate.
5. If this route is blocked, record that narrow result and investigate the next
   source-backed route. Do not repeat an identical failing operation without a
   changed premise, and do not repeatedly submit packages after an ambiguous error.

Do not end at “no exact guide exists.” Continue source comparison and permitted
diagnostics while they can answer an open question. If progress truly needs new
permission, an unavailable artifact or recovery method, report that exact
dependency with the prepared next step. Unsupported is not secretly supported;
“not found in the searched sources” is not “does not exist.”

## Reuse results before repeating experiments

Prefer a working interface on this exact unit over a sibling's suggested route.
Advance from the last established capability; do not restart identification or
retry an unchanged missing path. Recheck only when the device/build, caller
context, source or diagnostic has changed, or when a current-state check is
needed for the next operation. A community report is a lead for another owner,
not proof that their apparently identical TV has already passed a test.

| Lesson | Prioritize | Skip unless new evidence changes the premise |
| --- | --- | --- |
| Reference Home watcher bounced through VIDAA | Preserve the OEM engine and investigate its native launcher module | Faster browser polling as a fix for native Home return |
| Reference reads were blocked by the diagnostic page's CSP | Diagnose the actual page/transport error | Calling the firmware patched from a page failure |
| 50E6NT getters and two package-file reads were owner-reported successful | Continue through the available vowOS/HiUtils read contract and the actual readable files | Requiring root for those reads, or retrying the absent WebSDK interface |
| A read response contained `ret: true` and source with a `permission` property | Treat the returned source as data and inspect structured result fields | Searching all response text for permission/error words to decide success |
| A particular file returned `ENOENT` | Record that exact path/context and derive another path from readable source | Repeating the same path or declaring all registries/file access absent |
| Reference native video played behind opaque UI layers | Check owned player events, advancing time and transparent ancestors | Repeated codec changes based only on a still/black screen |

These are scoped exclusions, not a global firmware blacklist. Preserve actual
permission failures at their interface, and keep untested Fetcher writes,
privilege and recovery separate from successful reads.

## Choose a route from its mechanism, not just the model name

| Finding | Next investigation | What it does not establish |
| --- | --- | --- |
| Marketing model/firmware already supplied | Verify OS from manufacturer material; collect only missing internal identity through available information getters | Chipset and native-file access do not universally require root |
| Local page fails to call a service | Inspect page CSP, origin, protocol, exact transport and request errors; change only the diagnosed restriction | A page error is not a firmware patch |
| `HiUtils_createRequest` exists | Run a bounded `fileRead` control within authorized scope; inspect returned data and SDK errors | Function existence is not file permission |
| `WebSDK_createFileRequest` absent | Check the separately documented HiUtils and `vowOS.service.syncExecute` interfaces | One absent bridge is not the absence of all bridges |
| `fileWrite` returns an app-identity error | Keep that failure; inspect the separate `basic/fetcher` service and its actual permissions/source | A HiUtils write rejection does not measure Fetcher |
| Fetcher source resembles an upstream report | Compare service startup, argument parsing, path checks, worker identity and cleanup options on this build | Source resemblance is not a successful write or root test |
| Package operation reports an error | Inspect independently observable UID/proof, package state and owned artifacts before retrying | The top-level error does not prove `postinst` never ran |
| Temporary privilege is confirmed | Verify recovery and back up this device's original Home; follow PORTING.md | Root does not validate this dock's SDK or video integration |
| A candidate renders offline | Arrange a separately authorized native trial and physical Home/app tests | Simulation does not prove hardware behavior |

`localhost` in TV-side JavaScript is the TV; `localhost` on the owner's PC is
the PC. Keep host and device contexts explicit. An Intel Mac was a maintenance
host in the reference work, not a VIDAA compatibility requirement. Use the
owner's available supported computer and runtime.

## A concrete read-first bridge diagnostic

First inspect the existing diagnostic and its authorization. Add availability
checks for `HiUtils_createRequest`, `WebSDK_createFileRequest`, `vowOS`,
`vowOS.service` and `vowOS.service.syncExecute`. A native function can stringify
as `[native code]`; this is not a blocker when a source-backed call contract is
available. Do not invoke unrelated getters while enumerating properties.

The following read contracts appear in the pinned upstream sources. They are
comparison inputs, not a claim that every firmware implements them:

```js
HiUtils_createRequest("fileRead", {
  path: ["websdk/Appinfo.json"], mode: 6
});

// Alternative through an actually available service bridge:
vowOS.service.syncExecute("hiutils", {
  api: "fileRead", args: {path: ["websdk/Appinfo.json"], mode: 6}
});
```

Use one existing interface first; do not spray every transport or permission
variant. Preserve `ret`, `code`, SDK version, error text and response type. Parse
JSON strings when appropriate; the string `"false"` is not success. Keep complete
responses private, and summarize installed-app data rather than publishing it.
Do not save the registry back or load an entire upstream recon page.

### Classify the envelope, not the returned file's vocabulary

Inspect the actual response schema before writing a classifier. Keep the raw
envelope separate from the returned file contents; parse only the documented
envelope layer, not arbitrary nested JSON/source as if it were an error object.
For a response with a boolean `ret`, `ret: true` with returned file data is a
successful read even if that file contains `permission`, `error`, `denied` or
`ret: false` as source text. Do not use substring matching across the response.
Missing/conflicting result fields remain inconclusive; never coerce the string
`"false"` to a successful boolean.

`ret: false` with `ENOENT` from `open()` means that exact pathname did not resolve
in that request context. It is not an authorization error and does not prove
there is no app registry elsewhere. Confirmed `EACCES`/`EPERM` or a documented
vendor denial belongs to the error envelope, not the payload text. Keep source
availability, source completeness, runtime invocation and permission separate.

Before reusing a diagnostic, test its classifier offline with synthetic success
containing permission/error words, a missing file, a structured denial and an
ambiguous response. Correct any earlier ledger entries affected by a parser
bug; do not repeat successful TV reads merely to compensate for that bug.

On the documented 75U8QTUK build, `path: [p]` worked for an outside-base read
where `path: p` failed; both worked for `websdk/Appinfo.json`. A successful
control therefore proves neither traversal nor a broader read permission. On
a new device, keep any outside-base read within its separately applicable scope.
Do not infer the base directory from the mode number alone.

If the observed mapping permits it, these are bounded package-file candidates
inside the `/APPS` layout reported upstream:

- `pkgs/tv.vidaa.jsservice.basic/CHA/package.json`
- `pkgs/tv.vidaa.jsservice.basic/CHA/services/fetcher/package.json`
- `pkgs/tv.vidaa.jsservice.basic/CHA/functions/fetch/fetchfile.js`

Their existence on a new device remains unknown. Derive further paths, including
the active `CHA`/`current` target and service-list location, from actual manifests
and imports. Do not recursively dump the filesystem or collect accounts, keys
or unrelated personal files. A claimed `opkg` architecture must come from the
device's own configuration, not its marketing model or a sibling's chip.

## Keep the separate service route separate

The upstream 09.60 reports distinguish these mechanisms:

- `hiutils.fileRead/fileWrite`: browser-facing file bridge with its own checks.
- `basic/fetcher.fetchFile`: download-to-file service; **it writes**, despite its
  name. The documented service identifier is `phoenix://service/basic/fetcher`.
  Its startup is a state-changing operation, not a passive capability read.
- FaaS `/function/...`: execution of a module placed in the vendor package.
- Superwatch/package management: a later privilege boundary whose permissions,
  install semantics and cleanup must be measured independently.

In the cited report, Fetcher was not self-starting and its working payload used
JSON-string `args` with `directory`, not `path`. Treat those as contracts to
compare, not guessed values to send on another TV. A passive HTTP GET failure
does not test a documented service call. UI/transport, read bridge, Fetcher,
execution and package privilege need separate ledger entries.

Do not run `recon-fetcher.html`, `recon.html` or `recon-probe.js` wholesale as a
read-only diagnostic: their source includes service starts, writes, execution,
deletions or installation controls. Extract and review only the operation
needed for the current question. A probe's title/comment is not its effect.

If source evidence justifies a minimal write test, prepare its exact nonexisting
target, inert content, collision handling, readback, cleanup and expected failure
states before requesting any missing authorization. Do not put executable
content in an autoload/function directory as a “harmless marker.” If cleanup
itself needs an unproven execution route, state that unresolved dependency.
Do not claim a test is reversible merely because its file is small. A root or
package test is a later, separately reviewed step, not part of that marker test.

## When a route really is closed

Investigate another source-backed mechanism, not just another spelling of the
same rejected call. Consult newer upstream corrections and compare the exact
service/permission implementation if the owner can supply it. Existing approved
maintenance interfaces and officially documented device-specific developer or
recovery methods are also candidates. Extract owner-supplied firmware/packages
offline where authorized, keeping originals intact and recording their hashes.

Legacy file-bridge and boot-hook reports can explain older layouts, but their
persistent hooks are not interchangeable with bounded maintenance. Do not copy
another device's boot hook, package architecture, UID/GID, offsets or update
changes. If a genuinely new route must be researched, name its entry point,
source evidence, privilege boundary and next minimal experiment. Do not invent
an exploit or promise that a newer firmware must retain the old weakness.

Continue independent local dock adaptation while an access dependency is pending.
If all evidenced, authorized routes are exhausted, leave a precise resumption
record. Offer a browser/DNS alternative only as a separate owner choice.

## Community case: 50E6NT

Owner-reported, read-only findings received during community support:
Hisense 50E6NT (Germany), `V0002.09.60A.Q0707`, internal `50A60LEVS_0002`,
`MTK9603`, type `50A5LE`, region `EU_A`, country `DEU`.
These are nonunique model/type identifiers, not a published device serial.
The five information getters worked. Root, native Home, file reads and Fetcher
were initially untested. A later owner-supplied diagnostic report describes
successful file reads; this project has not independently captured their raw
responses or the complete device files. Do not turn that report into a verified
root route or this project's hardware acceptance.

The reported available interfaces are `vowOS.service.syncExecute` and
`HiUtils_createRequest`; `WebSDK_createFileRequest` was absent. The observed
HiUtils wrapper delegates to `syncExecute('hiutils', {api: type, args: msg})`.

| Read path relative to `/APPS` | Owner-reported raw result | Bounded conclusion |
| --- | --- | --- |
| `websdk/Appinfo.json` | `ret: false`, `ENOENT` | This pathname did not resolve; registry location remains open |
| `pkgs/tv.vidaa.jsservice.basic/CHA/package.json` | `ret: false`, `ENOENT` | This pathname did not resolve; nested readable files are separate evidence |
| `pkgs/tv.vidaa.jsservice.basic/CHA/services/fetcher/package.json` | `ret: true`, content returned | File read worked; reported fields include `selfStart: false` and `permission: {}` |
| `pkgs/tv.vidaa.jsservice.basic/CHA/functions/fetch/fetchfile.js` | `ret: true`, content returned | File read worked; the photographed source output was incomplete |

The original probe mislabeled the two successful reads as permission failures
because it searched their contents for the word `permission`. That conclusion
was withdrawn. No permission denial was observed in these four reported reads.
An empty manifest permission object does not prove effective caller permission;
`selfStart: false` does not measure whether the service is currently running.

The source excerpt reportedly reads `args?.url` while `JSON.parse(args)` is
commented out. An object argument is therefore a hypothesis for the function
boundary, not a tested end-to-end call shape: the bridge/dispatcher may serialize
or parse arguments at a different layer. Do not automatically copy a sibling's
JSON-string payload or try both forms against a writing endpoint.

The next useful step is to retain the complete readable Fetcher function and
manifest privately, with capture length/hash and an explicit truncation check.
Use their imports/exports to identify the dispatcher, startup policy and actual
cleanup contract. Derive any service-list/opkg configuration paths from source
before preparing a bounded read list. Package status, CPU model and opkg package
architecture are distinct; never infer the latter from the former alone.
Reuse the owner's existing read scope; bundle only genuinely new paths/scope
for approval. Do not start Fetcher, write a marker or install a package as part
of this source collection. The report's local diagnostic server was stopped.

Writes, execution, UID/GID, root, opkg architecture, native Home and persistence
remain untested. Marker deletion is unresolved: an error-branch `fs.unlink` or
overwriting a file with zero bytes is not a demonstrated removal procedure.
Record that cleanup dependency before proposing a separately authorized write.

The useful learning is procedural: collect missing facts before declaring them
root-only; inspect HiUtils and vowOS separately; distinguish a sibling's blocked
browser write from an untested service path. The 43A5LE Q0707 report is a lead,
not a match for a V0002 firmware. The 43Q60SEVS report establishes a mechanism on
another MTK9603 build, not compatibility for this one.

Keep later observations separate from upstream verified reports in
`model-research.json`. Add only anonymized, scoped results with their evidence
level. Do not publish support screenshots, handles, network details or OEM files.

## Primary sources and reference lessons

Upstream research revision used for this playbook:
`459bb3f6beb60e0605f867bd6f747abfe8d79fe8`.

- [Corrected false negative: HiUtils versus Fetcher, string versus array path](https://github.com/carteakey/alvidaa/blob/459bb3f6beb60e0605f867bd6f747abfe8d79fe8/docs/models/75U8QTUK/V0000.09.60I.Q0813/findings/05-fetcher-recheck.md).
- [43A5LE Q0707: readable app registry, browser write gated, root not attempted](https://github.com/carteakey/alvidaa/blob/459bb3f6beb60e0605f867bd6f747abfe8d79fe8/docs/models/43A5LE/V0000.09.60A.Q0707/README.md).
- [43Q60SEVS MTK9603: independently reported service/package root route](https://github.com/carteakey/alvidaa/blob/459bb3f6beb60e0605f867bd6f747abfe8d79fe8/docs/models/43Q60SEVS/V0000.09.60W.Q0612/README.md).
- [Published Fetcher/FaaS implementation analysis](https://github.com/carteakey/alvidaa/blob/459bb3f6beb60e0605f867bd6f747abfe8d79fe8/docs/models/100U7Q/V0000.09.60I.Q0813/source/modding/02-write-and-exec.md).
- [Reference project's successes and dead ends](WORKED-EXAMPLE.md): diagnostic CSP,
  UID proof despite package error, bounded SSH, backups, native module wrapper,
  targeted caches, SDK adapters, owned video session and transparent UI layers.

Report progress as **observed / owner-reported / inferred / untested / blocked
at this specific interface**. Final installation still follows PORTING.md and
RECOVERY.md. Persistence in research is not permission to weaken those checks.
