# TV remote control and browser-assisted setup

[Agent entry point](AGENT-START.md) · [Masterprompt](MASTERPROMPT.md) · [Access research](ACCESS-RESEARCH.md) · [Agent troubleshooting](AGENT-TROUBLESHOOTING.md)

Use the owner's computer to operate their paired TV when that reduces manual
work. Remote navigation and a temporary TV-browser diagnostic page were useful
in the reference project. They are legitimate parts of the workflow even when
the final Home component runs natively.

**Scope:** this is an implementation playbook, not a bundled universal remote
driver or a new hardware-compatibility claim. This documentation update did not
contact any TV. A remote-control connection does not establish root access.

## Three independent capabilities

| Capability | What it establishes | What it does not establish |
| --- | --- | --- |
| Paired local remote | Accepted keys, app inventory/launch or text entry, where implemented | File access, installation privileges, a screen capture or native Home compatibility |
| A local page opened in the TV browser | The page loads in the TV's actual browser context; permitted probes can run there | That the computer browser has the same bridges, or that every VIDAA build permits them |
| Native maintenance and Home integration | Only the separately observed device contracts and authorized changes | Permission to expand remote scope or keep access open indefinitely |

Keep these results separate in the private handoff. A working remote does not
need to be rediscovered just because a file bridge or installation path fails.

## 1. Establish control with minimal owner effort

1. Read the private handoff and reuse a still-valid pairing before creating one.
   Record the specific TV, host computer, allowed navigation and session scope.
   Repo-only or simulation-only work must not contact the TV.
2. Use the owner-supplied TV address or existing authorized inventory. Check
   only that target and the documented service; do not discover an entire subnet.
   The original host's CPU brand was not an access requirement. The relevant
   requirement is a computer able to reach the TV with the necessary tools.
3. Review the exact model's mobile-remote documentation and the selected client
   implementation. VIDAA MQTT implementations vary in transport, client identity,
   certificates, pairing and topic contracts. Do not assume one fixed credential,
   port configuration or certificate works on all releases.
4. Prefer an existing approved local client. For a new client, pin and review
   its source and dependencies, select explicit-host mode and inspect whether
   startup performs discovery, power changes or writes. Do not install a whole
   home-automation stack just to send a few keys. Apply the project's existing
   software-install authorization.
5. When needed, perform the TV's normal owner-visible pairing flow. Ask for
   the current on-screen code once; submit it without recording it in public
   output. Report a rejected/expired code accurately before requesting another.
   Pairing needs owner participation; do not guess codes or bypass its checks.
6. Keep resulting keys, certificates, client identifiers and pairing state
   private with restrictive permissions. Never distribute the original owner's
   pairing files or include credentials copied from an upstream example.
7. Confirm the session with an available read/status query. Then, while the
   owner has authorized navigation, test one reversible navigation action with
   feedback. A successful MQTT publish acknowledges transport, not a visible
   focus change. If no screen/status feedback exists, ask one focused question
   before proceeding through state-dependent actions.

Some official remote features may require model-specific settings or consent.
Explain a genuinely required change before making it. Do not enable unrelated
content sharing, account features, advertising consent, wake-on-network or
router rules simply because an upstream tutorial includes them.

## 2. Drive the interface, not the owner

For an authorized setup session, carry out routine navigation yourself when
the client supports it: select the browser, enter the diagnostic URL, follow
its focus order and activate the exact prepared action. The owner should not
have to transcribe source code or perform every arrow press.

Use an existing matched implementation or a small reviewed adapter exposing
only the capabilities actually available:

- connection/pairing state and a clean disconnect;
- installed-app inventory and launch by verified app identifier;
- one key event with an explicit completion/feedback check;
- text or URL entry, only if the client and current screen support it;
- request/reply correlation with timeouts and no blind mutation retries.

These are suggested adapter responsibilities, **not names of vendor APIs**.
Derive actual topics, payloads and response handling from the reviewed client
and the TV's observed behavior. Do not hardcode the reference TV's app IDs.

Keep one controller active at a time. Subscribe to the required response before
sending its request; correlate replies to the current session. Avoid duplicate
event handlers and repeated button events after reconnects. Distinguish a short
OK from long OK and release held keys when stopping. Do not replay a queued
confirmation after a timeout.

Navigate in short, observable segments. Prefer a verified app launch or URL
command over a long sequence of guessed coordinates. Browser focus, keyboard
layout and current page state can differ. If the session is blind, stop the
dependent click and obtain minimal feedback rather than repeatedly pressing OK.

Remote control is not screen capture: MQTT status and app lists alone cannot
show rendered pixels. Use an available, separately authorized capture mechanism
or owner confirmation for visual acceptance. Do not install screen mirroring
or start camera/audio recording merely to avoid asking a short question.

## 3. Use the TV browser as a temporary setup tool

Prepare and inspect the page locally first. Its initial load should show status
and controls without installing, writing, deleting or invoking a privileged
operation. Separate authorized read diagnostics from any later, separately
reviewed mutation. Browser assistance does not expand the active access scope.

A practical sequence is:

1. Create a private, narrowly scoped directory for the page and a dedicated
   result receiver. Serve only the listed assets, on the host interface reachable
   by the one TV, for a bounded session. Never serve the repository root, private
   backups, credentials or the whole home directory. No router forwarding.
2. Check the page and receiver locally. For direct result transfer, actually test
   the receiver's POST handler with synthetic input. A static file server can
   serve the page while returning HTTP 501 for every result upload.
3. Open the local URL in the **TV browser** through the paired remote if its
   observed launch/text contract allows it. Otherwise ask the owner to open it
   once, then continue from machine-readable results. Opening the same page on
   the computer does not reproduce the TV's vendor bridges.
4. Confirm an actual TV page-load request and session identifier at the receiver.
   Check the page version before an action; an old cached page must not run an
   obsolete probe. Reloading must not repeat staging or other mutations.
5. For a read probe, use the already established same-unit bridge contract from
   ACCESS-RESEARCH.md. Gather only the approved files/fields. Distinguish browser
   policy/CSP/transport errors from a structured device-side permission result.
   A page failure alone is not evidence that the firmware is patched.
6. Send the full result directly to the host. The receiver should accept only
   explicit result names, bounded sizes and the current session, reject path
   traversal and unknown requests, and atomically store accepted data privately.
   Bind to the intended interface and restrict the intended peer. Do not enable
   wildcard cross-origin uploads or expose an unauthenticated file writer.
7. Compare the transmitted character count, UTF-8 byte count and digest with the
   stored copy. UTF-16 length is not UTF-8 byte size. FNV checks can catch a
   transcription/transport mismatch; use SHA-256 for saved artifact manifests.
   If a transfer fails, fix the receiver/transport before repeating TV reads.
8. Present a short structured summary to the owner; retain raw responses locally.
   Screenshots remain useful for UI confirmation, not for reconstructing many
   pages of source. Never publish raw source responses containing private data.

For mutations, resolve uncertain prior results before retrying, give each action
a unique session/action ID and reject duplicate submissions. An HTTP success
only proves that HTTP transaction; it does not prove installation or cleanup.
Follow the separate reviewed access/change plan rather than attaching a generic
installer to every diagnostic page.

## 4. Continue toward the native result

After setup, use the native SDK/maintenance path for the reviewed Home change.
Keep the vendor shell and physical Home behavior. The useful browser bootstrap
does not imply a permanent browser launcher, a Home watcher, a browser restart
loop or remote control left running in the background.

If no native route is established and the owner wants a browser-launcher
alternative, document its limitations and obtain agreement to that different
result. Do not label browser navigation as a successful native installation.

## 5. Close the session

Stop sending keys immediately if the owner resumes watching or asks to stop.
For an authorized session ending normally, return to the agreed screen only
if that navigation remains in scope. Disconnect the controller, release any
held keys and stop the temporary HTTP receiver/server. Verify the owned listener
has closed. Record retained pairing state and how the owner can remove it.

Pairing state and a root maintenance lease are different. Neither extends the
other. Honor each deadline. Do not silently enable a permanent remote daemon
or reopen expired privileged access. Retain only private evidence required to
resume, with its exact unresolved step.

## Primary sources and reference evidence

- [Hisense VIDAA U9 e-manual](https://www.hisense.com.my/wp-content/uploads/2025/08/93041_9603VIDAA_U9_EUEMCO_E-Manual_eng_202502%E5%AE%8C%E6%95%B4%E6%9F%A5%E7%9C%8B%E7%89%88.pdf):
  remote/VIOT services and the Browser and Mobile App sections. Menu paths and
  prerequisites vary by model and region; this is not a universal setting list.
- [Original project's remote/browser experience](WORKED-EXAMPLE.md):
  pairing, browser navigation and app launch worked; a browser Home watcher
  produced an unwanted stock-Home bounce.
- [Krazy998/mqtt-hisensetv, pinned README](https://github.com/Krazy998/mqtt-hisensetv/blob/104d18b238a82447395d9f1d65db71197c7f3254/README.md):
  upstream protocol/client research, including transport-generation differences.
- [adamazad/vidaa-remote, pinned README](https://github.com/adamazad/vidaa-remote/blob/6a868f2a2a040b715d022b717a3ce7a3f18aa9a2/README.md):
  an example CLI client with pairing and key control. Its discovery defaults
  and bundled certificate material are not adopted by this project.

Upstream links are research leads, not endorsements of their defaults or proof
of this project's hardware support. No upstream client code or credentials are
bundled. Review the actual implementation and license before adapting it.
