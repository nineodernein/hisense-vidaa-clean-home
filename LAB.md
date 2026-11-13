# Persistent offline access lab

Run `python3 agent.py lab --matrix --json` to explore named cases and 1,536 systematic combinations. Inspect retained learning with `python3 agent.py lab-memory --json`. `agent.py start` runs and remembers the named cases automatically.

Device files, services and diagnostic packages are in-memory Python values. The lab has no network transport, shell, firmware interpreter or executable package generator.

Successful routes, failed routes, conditions and steps persist in `.private/lab/memory/`. Detailed reports persist in `.private/lab/runs/`. Matching conditions prioritize the successful route on subsequent runs. Changed assumptions or model source use separate memory namespaces; old records remain. Checksums detect accidental edits.

Read the returned report and use matching outcomes to prioritize the next hypothesis. These are behavioral simulations, not real hardware evidence or success probabilities. Never populate device.json or compatibility.json with simulated outcomes. Share generalized lessons and synthetic regressions, not private memory or OEM captures.

For the community case run `python3 agent.py lab --profile community-50e6nt --json`. Its unresolved conditions are enumerated as hypothetical worlds, not declared supported hardware.
