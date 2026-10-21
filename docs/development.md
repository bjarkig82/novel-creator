# Development

Requires Python 3.11 or newer and external Git 2.39 or newer. Use a local
virtual environment; no model credentials, server or AI runtime are needed.

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-lock.txt
python -m pip install -e '.[test]'
python -m novel_creator --help
python -m unittest discover -v
bash tests/speckit-smoke.sh
```

On Windows activate `.venv\Scripts\Activate.ps1`. The test extra uses Python's
standard unittest runner. `requirements-lock.txt` records exact runtime resolution;
packaging declares the compatible range. Tests use temporary Git repositories,
local disposable identities, and automatic fixture cleanup. They never configure
a global identity. Interrupted fixtures may be removed only after confirming
they are disposable test directories.

Structural tests do not establish literary consistency or native-host support.
Each claimed Codex host/model/version needs separate actual capture evidence in
`tests/evaluations/host-capture.md`. No host is yet verified; story implementation
must wait for the foundation gate.

## Foundation status and hard gate

Foundation packaging, complete shared schemas, structural transition validation,
atomic exchange-save and an independent disposable host-spike fixture are
implemented. `init`, session operations, production context/inspection/validation
and `recover` are command placeholders returning an explicit unavailable error.
The fixture's context helper is test-only. Pending retries use the exact original
`exchange save` payload. Published cleanup failures return saved/cleanup_required;
further writes remain paused because safe cleanup recovery is later T034 work.
Never manually reset history to clear this pause.

New decisions must cite the current conversation's actual user message;
historical messages may remain provenance but cannot authorize a new change.
Malformed committed envelopes and recovery receipts return structured
unavailable-context errors with the affected path, rather than tracebacks.
Journal failures retain the last validated prefix and its historical Git
checkpoint when verifiable; a null `git_head` means no matching valid historical
snapshot could be confirmed. An unsafe journal never permits further saves.
Stale-write conflicts include `error.expected_git_head` and
`error.actual_git_head`, alongside the last confirmed checkpoint and pending ID.
Held writer locks also report the attempted exchange ID and an independently
verified committed checkpoint when available. Inspection reads a captured Git
snapshot without taking over the lock; unborn or unreadable history does not
produce an invented checkpoint. The existing lock and pending files are retained.

Before dependent implementation, the actual host still needs real automatic
subsequent turns, fresh-chat recovery and controlled save/display interruption
evidence. Reading thread summaries or running subprocess fixtures does not
establish those behaviors. Foundation remediation does not pass this gate.

**T013 decision: BLOCKED. T012 actual Codex host evidence is unverified.** See
[host-capture evaluation](../tests/evaluations/host-capture.md). No available host
control can create genuine subsequent turns, a fresh chat or display interruption
here. T014+ remains unimplemented. A subprocess fixture or prompt compliance
cannot waive that gate. Return to actual-host evaluation/adapter planning before
continuing; no supported-host claim, manuscript feature or release is implied.
