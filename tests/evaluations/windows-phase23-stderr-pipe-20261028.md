# T174 checked-Git stderr-pipe investigation — 2026-10-28

The prototype is not retained. Small-command resource savings do not establish
a complete-save improvement in the matched full-scale comparison. Production
runtime, workflows, resources, dependencies, benchmark policy and safeguards are
unchanged. T174 and dependent T175 remain unchecked, as do T172/T173.

## Hypothesis and controlled change

The current save traces contain 29 Git invocations, many with substantial elapsed
time. `storage.git` captures both stdout and stderr even for checked calls, whose
contract returns only stdout and sanitizes nonzero exits as ToolError 5. On
Windows, capturing both streams requires Python subprocess reader threads.
The source-free prototype directs only checked-call stderr to DEVNULL; unchecked
calls retain their complete result, including captured stderr. It changes no
Git arguments, environment filtering, input bytes, return-code handling or save
ordering. The current storage source is SHA-256
`40c7c1ef61af98e9c1e04292d2befc963bd48bbd45196ce8cbf91576f3ee771b`.

The runner compiles a separate in-memory module from that source, with exactly
one subprocess stream-selection replacement. It does not overwrite storage.py.
This is an unqualified diagnostic prototype, not a delivered product change.

Real Git checks in SHA-1 and SHA-256 repositories verify exact checked stdout,
binary stdin, sanitized checked failures and retained unchecked diagnostics.
These execute in both the component and full-scale comparisons. The first
component attempt incorrectly expected one reader thread per single-pipe call;
it stopped at that diagnostic assertion. Python's no-stdin/single-stream fast
path instead uses the caller thread, with zero reader threads. The original
failed attempt remains in the `component-assumption` artifacts and is not a
product failure or a passing measurement.

## Observations

| Comparison | Current median (s) | Prototype median (s) | Scope |
|---|---:|---:|---|
| Eight checked rev-parse commands per batch | 0.602102700 | 0.538249500 | Eight batches per variant, ABBA four times |
| Complete validation/local save | 6.261266500 | 6.255118250 | Four saves per variant, ABBA twice |

Every current eight-command batch starts 16 reader threads; the single-stream
prototype starts none. Component CPU windows range from 27.36–88.48% for current
capture and 32.72–65.06% for the prototype. This confirms a resource reduction
and a component-level observation, not an end-to-end or qualification pass.

The full-scale fixture has 100 sessions, 5,000 exchanges, 10,000 active assertions
and 26,215,716 JSON bytes, with full initial validation. No packing/maintenance is
requested. The optional private validation key is temporary and outside the
disposable novel. Each save uses a fresh worker with the normal 30-second whole-
worker deadline, installed Git and unchanged history/hash-reader counts. Imports
and payload preparation stay outside the save timer as in the existing harness.
Every save retains two complete guards, full history and object/byte hashes,
root/path/reparse/live-index checks, private-candidate verification, fresh
branch/CAS, writer/worker lifetime, receipts/fsync, cache, cleanup and recovery.
For saved sequence N, the runner checks 2*N bulk file hashes and batch objects;
the batch count includes the preparation read and candidate verification.

All eight normal-access saves succeed without timeouts or cleanup warnings.
Current save times range from 3.650258100–10.006145000s; prototype times from
4.688200400–15.132966300s. CPU windows cover the whole worker operation, including
payload preparation, rather than exactly the timed save. They range from
79.27–99.69% and 89.56–99.95%, respectively. These variable conditions and nearly
equal medians establish no basis to retain the change. No causal regression or
stable low-load speedup is claimed. No further runtime fix or 30-run candidate
qualification is justified by these samples.

The original sandbox full-scale attempt fails at the first `os.link` with
WinError 5. Its source, fixture and failure outputs remain preserved separately.
The successful rerun uses scoped normal filesystem access on fresh disposable
data; no lock, hard-link publication check or failure is bypassed. Disposable
fixtures and their private keys are cleaned up by their context managers.

## Reproduction and verification

From the repository root, use Python from `.venv/Scripts/python.exe`, `-B`,
`PYTHONPATH=src` and a writable temporary directory; the successful normal-access
run uses ignored `.tools/t174-pipe-temp/` for TEMP/TMP. On this sandbox, hard-link
publication needs normal scoped filesystem access.

```powershell
.venv/Scripts/python.exe -B tests/evaluations/phase23-stderr-pipe-20261028.py
.venv/Scripts/python.exe -B tests/evaluations/phase23-stderr-pipe-20261028.py --full-scale
.venv/Scripts/python.exe -B tests/evaluations/verify-phase23-stderr-pipe-20261028.py
```

[Executed runner](phase23-stderr-pipe-20261028.py),
[component observations](windows-phase23-stderr-component-20261028.jsonl),
[full-scale observations](windows-phase23-stderr-save-normal-20261028.jsonl),
[read-only independent verifier](verify-phase23-stderr-pipe-20261028.py),
[verified arithmetic/source/artifact identities](windows-phase23-stderr-verification-20261028.json).
The successful component, normal-access full-scale runner and verifier exit 0;
successful runner stderr files are empty. The verifier checks source hashes,
exact orders, fixture dimensions, sequences, guard/hash/object counts, correctness
results and the retained 30-run p95 arithmetic. It also confirms the original
sandbox and diagnostic-assumption failures remain visible.

The retained ordinary-layout qualification remains read p95 1.028736700s
(<=2s passes), save p95 3.067419500s (<=1s unmet), with all 30 reads/30 saves
successful. No fresh 30-run benchmark, broad suite, wheel or native-host outcome
is inferred from these diagnostics. Current runtime/resource identity still
matches the retained independent wheel, so prior source-specific product evidence
is not invalidated. The POC remains usable; broader qualification is incomplete.
No novice/manual prerequisite, threshold relaxation, provider call, global
configuration change, real-novel edit, framework commit or push is introduced.
