# T149 corrected history reader: verification pending

2026-10-22. Current storage SHA-256:
`9b9092130ff0ee2768ba739cdb9ae28613010ed82b4a9eeb70bb9b342b080ffc`.
This working implementation supersedes the initial unretained prototype.
It is not fully verified or established as satisfying T149.

Large public Windows snapshot reads partition immutable captured blob OIDs
into at most four contiguous requests at 1,024 exchanges. All workers join
before parsing or returning. Successful outputs form one original-order binary
stream. A worker/submission exception or any nonzero child status triggers one
complete original serial request, preserving partial stdout, earlier damaged
history, error paths and verified-prefix checkpoint behavior. The fallback is
outside the retry handler. Small histories and non-Windows runtime stay serial.

Save history reads remain serial. All existing file metadata, path, symlink,
index, root-bound complete byte hashing, candidate, authority, digest, CAS,
locking and recovery checks remain in place. The previously retained parallel
final-byte guard is unchanged.

## Diagnostic measurements

Four fresh-worker samples per configuration on the ordinary Windows fixture
(100 sessions, 5,000 exchanges, 10,000 assertions, 26,215,716 JSON bytes)
measured context-read medians of 2.052871050s serial, 1.586789600s with two
requests and 1.432398200s with four. Complete-save medians were 4.529989250s,
4.567219250s and 5.588813600s respectively. All operations succeeded. These
small balanced diagnostics support exploring public reads only; they establish
neither complete-save improvement nor p95 compliance.

The threshold diagnostic measured serial/four-request context-read medians
0.312642000s/0.320206100s at 256 exchanges and
0.648670600s/0.565530500s at 1,024 exchanges (four samples each).
The external diagnostic candidate was ab6ba8f4... against baseline 6ec58b45...;
it predates the additional nonzero chunk-boundary fallback correction below.
Its valid-data timings are not a benchmark of the current production source.

## Regression evidence and limitations

Five current focused methods pass in 31.152s, exit 0:
[final focused retry](windows-history-partition-production-final-focused-space-retry-20261022.txt).
They cover SHA-1/SHA-256 cached/uncached equality, captured snapshots after HEAD
advances, missing/header/truncated objects, trailing framing, nonzero complete
and partial output, earlier damaged history versus later worker/guard failures,
partial submission cleanup, small-read fallback and serial save policy.
Review found nonzero partial stdout at a chunk boundary could silently continue;
its explicit red test failed six cases before the correction, and those cases
are included in the passing final suite. Final read-only review found no
remaining actionable issue; this does not replace runtime verification.

An editing helper briefly recoded existing Unicode fixtures. The original test
body was restored and reconstructed baseline SHA-256 verified exactly as
7536bdfbba465f85f8113cadf5aa674e2893a33cb28a053aa6be8c20a468cf1e.
No fixture language change is intended.

The first final-focused attempt hit OSError 28, No space left on device;
its failed log is preserved separately from the successful retry. C: has
repeatedly reached zero free bytes. Full Windows/Linux suites and a fresh
30-read/30-save ordinary-layout benchmark for this source have NOT run.
The earlier 133-test results and read/save p95 5.110137800s/6.566394800s belong
to source 6ec58b45... and cannot verify this implementation. Avoid broad tests
until disk space is available. No live verification process remains.

Raw diagnostics, executed scripts, pending source snapshots and red/green logs
are hashed in [the pending manifest](windows-history-partition-pending-manifest-20261022.json).
T149 remains unchecked. Novice evaluations remain deferred/unverified;
host, bilingual semantic and final release gates remain open.
