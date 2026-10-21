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

**T013 decision: BLOCKED. T012 actual Codex host evidence is unverified.** See
[host-capture evaluation](../tests/evaluations/host-capture.md). No available host
control can create genuine subsequent turns, a fresh chat or display interruption
here. T014+ remains unimplemented. A subprocess fixture or prompt compliance
cannot waive that gate. Return to actual-host evaluation/adapter planning before
continuing; no supported-host claim, manuscript feature or release is implied.
