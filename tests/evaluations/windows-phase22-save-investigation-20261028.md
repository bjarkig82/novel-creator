# T172 save scheduling investigation — 2026-10-28

T172 remains unmet and dependent T173 remains unchecked. No runtime optimization
is adopted: three source-free alternatives fail to demonstrate an improvement.
Existing work, production source, dependencies, safeguards and performance
targets are preserved. The usable single-user POC remains separate.

The recorded [stage profile](windows-phase22-performance-20261028.md) identifies
full history and the first complete guard overlapping, with native metadata
queries competing with Python decoding, followed by a substantial second guard.
Earlier parser, metadata-thread, GIL, native-binding and hashing experiments
were reviewed before these tests. Neither receipt/fsync removal nor omitted
validation or byte checks is justified by these profiles.

## Full-scale matched diagnostics

Each comparison uses an ordinary-layout disposable repository with 100 sessions,
5,000 exchanges, 10,000 active assertions and 26,215,716 JSON bytes, fully
validated before measurement. No Git packing/maintenance is requested. An opt-in
temporary private validation key is outside the novel. Windows 11 build 26300,
Python 3.13.13 and Git 2.53.0.windows.3 use the unchanged
`C:/Program Files/Git/cmd/git.EXE` selection and C: NTFS; the same-day
[hardware inventory](windows-phase22-hardware-20261028.json) records the laptop.

Every save uses a fresh Python subprocess with a 30-second deadline. Public
payload preparation and imports remain outside the operation timer, as in the
existing benchmark. The final guard always retains four hash readers. Counts
include both payload-preparation and save-time history reads; they do not claim
that either history read was removed. Ambient machine activity is uncontrolled.

| Comparison | Policy | Four-save median (s) | Disposition |
|---|---|---:|---|
| Balanced ABC/CBA twice | Current: four history/two initial hash readers | 3.052792150 | Control |
| Same fixture/order | One save-history/two initial hash readers | 4.330007750 | Reject |
| Same fixture/order | Four history/one initial hash reader | 3.224343650 | Reject |
| Separate ABBA/ABBA fixture | Current overlapping first guard | 3.087430600 | Control |
| Same fixture/order | Complete history before first guard | 3.309358300 | Reject |

The first comparison tests resource contention by reducing reader concurrency.
The second tests whether eliminating history/metadata overlap outweighs losing
parallel work. Its diagnostic-only deferred executor runs the complete first
guard at the existing await point, before pending writes, and drains queued work
on exit inside the writer lock. This changes initial sampling timing; it is not
represented as a production-ready implementation or comprehensive failure-path
qualification. The original executor continues to govern production.

All 20 saves succeed without timeouts or cleanup warnings. Each asserts two
completed guards, explicit real-root worktree binding for bulk hashes and total
managed-file and object counts. For saved sequence N, bulk hashes cover 2*N
files and batch reads cover 2*N objects (including the candidate's two objects).
Both actual guard implementations, metadata-before-hash ordering, complete
history/object hashes, private candidate verification, live-index checks,
branch/CAS, receipts, fsync, cache and recovery paths execute unchanged.
These small balanced comparisons are diagnostic medians, not 30-run p95s,
universal speed estimates, atomic filesystem snapshots or release evidence.

[Concurrency samples](windows-phase22-save-balance-normal-20261028.jsonl),
[scheduling samples](windows-phase22-save-schedule-20261028.jsonl),
[replay runner](phase22-save-balance-20261028.py).
The runner gained its optional scheduling mode after the first comparison;
that comparison's original rows therefore omit the optional `defer_guard` field.
Its counting and default execution behavior are unchanged in the final runner.
Both normal-access diagnostic processes exit 0 with empty stderr files.

The initial sandbox attempt fails creating the temporary key before fixture
generation or any save. Its [original error](windows-phase22-save-balance-stderr-20261028.txt)
is preserved. Scoped normal-access execution with TEMP/TMP pointing at the
ordinary user temporary directory succeeds; the test helper cleans up its
disposable repositories and keys. No global environment or Git setting changes.

## Qualification and verification

The independent ordinary-layout 30-read/30-save run remains authoritative:
first read 1.740510000s, read p95 1.028736700s passes <=2s, save p95
3.067419500s misses <=1s. All 60 operations succeeded. Its raw timings are
preserved unchanged and independently recomputed, rather than replaced with
these smaller comparisons. No new 30-run candidate benchmark is warranted
because no candidate improves the matched diagnostic or is retained.

Storage remains SHA-256
`40c7c1ef61af98e9c1e04292d2befc963bd48bbd45196ce8cbf91576f3ee771b`.
Both diagnostic headers and the verifier confirm matching current storage,
context, validation and benchmark hashes. No runtime, schema, dependency,
resource, test or harness edits invalidate prior source-specific platform/wheel
evidence; broad suites and wheel builds are not repeated for evidence-only files.

[Verifier](verify-phase22-save-investigation-20261028.py), exit 0, independently
checks fixture sizes, exact balanced orders, sequences, read/hash/guard counts,
all medians, current source identity and nearest-rank p95s from all original
30 samples. [Verification output and artifact hashes](windows-phase22-save-investigation-verification-20261028.json).

T172 and T173 remain open. The existing
[provisional release assessment](phase22-release-assessment-20261028.md) remains
provisional, with no unknown semantic/native/platform outcome promoted to pass.
Further work needs a separately justified bottleneck change and matched
full-scale evidence; this result supplies no basis to weaken safeguards or
change the read/save targets.
