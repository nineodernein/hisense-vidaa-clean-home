# When a coding agent stops

[Start](AGENT-START.md) · [Masterprompt](MASTERPROMPT.md) · [Remote and browser setup](REMOTE-AND-BROWSER.md)

The goal is concrete progress on the owner's authorized TV project. Reuse facts,
working interfaces and valid permissions. Do not restart onboarding or end the
entire task because one native-install prerequisite is missing.

A repository prompt cannot force execution, grant ownership, replace missing
tools or override a model's safety policy. This guide resolves avoidable stalls
and mistaken assumptions; it is not a jailbreak or an instruction to conceal
what an operation does.

## Identify the actual stopping condition

Ask for the exact failure or refusal text only when it is not already available.
Do not ask the owner to repeat the TV identity or whole chat. Separate:

| Condition | Concrete next action |
| --- | --- |
| Agent summarizes the repo but does not start | Read AGENT-START.md and execute the reviewed offline checks in a local coding environment. |
| No terminal, browser integration or LAN route | State the missing capability. Prepare local artifacts with available tools; explain the required local environment once. |
| Tool permission or network policy denied a call | Report the exact blocked tool/action and rule source if exposed. Let the owner review the intended narrowly scoped permission through the tool's normal controls; continue independent allowed work. |
| Agent assumes unknown firmware means impossible | Point to existing same-unit evidence and ACCESS-RESEARCH.md. Distinguish untested from rejected and prepare the next bounded diagnostic. |
| Agent demands root before preparing any read diagnostic | Inspect the actual read contract and existing source. Prepare non-privileged work where possible; keep later installation requirements separate. |
| Agent repeats permission questions within an active scope | Reuse the actual grant and deadline. Bundle only genuinely new scope into a concrete, reviewable request. |
| Agent lacks screen feedback | Reuse an authorized paired remote and result receiver; ask for one visible check where observation is still missing. Do not guess destructive confirmations. |
| Model explicitly refuses an operation on safety-policy grounds | Respect that boundary. Briefly explain which action cannot proceed and continue independently permitted diagnostics, documentation or local tests. Do not disguise or reroute the refused action. |
| A technical probe returns an error | Record raw private evidence; distinguish transport, arguments, permission, path, lifecycle and result interpretation. Change the tested premise before retrying. |

A missing recovery path stops the dependent native modification. It does not
automatically stop reading public source, reviewing existing private evidence,
preparing backups or testing an offline renderer. Conversely, a passing mock
cannot authorize a real TV write.

## Claude Code: instructions and tool access are different

Claude's documented project instructions guide behavior; permission settings
control tool use. Check the installed version's normal permission UI with
`/permissions` when an actual tool-access error occurs. Explain the minimum
needed action and target; do not silently alter managed settings, deny rules,
hooks or global access. Keep any owner-approved machine-specific settings
local and out of version control.

Use [Claude Code's permission documentation](https://code.claude.com/docs/en/permissions)
and [project instruction documentation](https://code.claude.com/docs/en/memory)
for the installed environment. CLAUDE.md does not grant tool access or outrank
platform policy. A remote web chat also does not acquire LAN access merely
because the prompt contains a repository URL.

Do not suggest disabling all permission checks as the solution to a refusal.
Do not relabel a real device action as a simulation, hide its privilege effects,
fabricate authorization or use a different tool to evade a denied operation.
Truthful scope and evidence can resolve a misunderstanding; they cannot
guarantee that every model will perform every step.

## A concise owner prompt

Use this in the existing project conversation so its evidence and permissions
remain available. In a new chat, first provide the private local handoff path,
without copying credentials or raw device data into a public issue.

> Continue my own authorized VIDAA project from this repository and the private handoff. Read AGENT-START.md, MASTERPROMPT.md and REMOTE-AND-BROWSER.md. Reuse confirmed results and my still-valid permissions. Complete the next concrete permitted step rather than repeating the whole plan. Use a paired remote and a local TV-browser page where supported to reduce manual clicks and source screenshots. If something blocks a step, identify whether it is missing tools, missing owner scope, a permission denial, a technical failure or a model-policy limit. Stop only the dependent action and continue independent permitted work. Prepare one specific next action with its expected evidence and cleanup. Do not invent success, change my access scope or bypass tool or model safeguards.

The prompt refers to permissions already granted; it does not create them. If
the current task is repo-only or simulation-only, the agent must stay offline
with respect to the TV.

## Progress receipt

Keep the private handoff short and update it after meaningful progress:

- current source revision and validated local artifacts;
- specific authorized target, allowed actions and any expiry;
- established same-unit results and private evidence locations;
- current remote/browser/maintenance state and owned cleanup obligations;
- next unresolved boundary, one proposed test and its expected observation.

Public reports should contain only a sanitized capability/result summary. No
pairing codes, private host details, raw logs, accounts or chat screenshots.
