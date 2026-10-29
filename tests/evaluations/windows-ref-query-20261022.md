# Combined branch/OID query — 2026-10-22

T149 continuation. Novice evaluations remain deferred/unverified. The unchanged
read/save goals are 2s/1s p95. Earlier path-allocation source measurements remain
in [their source-specific report](windows-allocation-investigation-20261022.md);
critical-path experiments remain [separate diagnostics](windows-save-critical-path-20261022.md).

## Narrow retained change

A private _branch_head helper queries Git for the checked-out local branch and
its object ID in one process. It replaces only the initial branch/head pair and
the postpublication branch/head pair before index cleanup. The existing fresh branch
check in the final publication phase remains, as do both complete file guards and every
full-content hash, live-index/path/root check, private candidate index,
candidate verification, authority/hold check, conditional publication, durable
receipt and recovery step. No guard sampling phase is moved or cached.

The format uses Git's HEAD marker, full refname and full objectname separated by
NUL bytes. This follows the documented [Git ref-format fields](https://git-scm.com/docs/git-for-each-ref#_field_names).
Valid [Git ref names](https://git-scm.com/docs/git-check-ref-format) cannot contain
the control delimiters used here. Exactly
one marked local branch and a complete 40/64-character lowercase hexadecimal
OID are required. Failed queries, missing or ambiguous marked records, and malformed or
undecodable selected records use the existing branch/head queries. Detached, unborn and symbolic
references retain their tested fallback/rejection behavior. No dependency,
reference-backend file parser, format/schema change, root binding, machine Git
selector or background process is introduced.

One process does not make the reference read an atomic snapshot. External Git
operations can still race the reads. The existing branch check before the final guard,
conditional update of the captured ref and postpublication verification remain
necessary. Both before_ref and after_ref branch-switch regressions deliberately
use another branch at the same OID, proving that commit identity alone is not
accepted as branch identity. Before publication, the captured branch is not
advanced. After publication, saved-with-cleanup is returned before index sync.
Both cases preserve the user index and release the writer lock, in SHA-1 and
SHA-256 repositories.

An independent final diff review found no actionable safety defect in the source
or new tests. It explicitly retained the non-atomic/race qualification above and
warned that enumerating all local refs can cost more in repositories with many
branches. No universal speedup or branch-count bound is claimed.

## Baseline, focused verification and limited timing

The public same-OID branch-switch regression passes the prior source (one test,
11.911s). New helper compatibility/fallback tests fail that prior source with
missing-helper AttributeErrors, as expected for the new private helper; this is
not evidence of an old authority defect. After implementation, all three new
tests pass in 24.872s. Permanent coverage includes normal, detached, unborn,
packed, recursive alias, alias-to-tag rejection, Unicode/delimiter-like names,
another branch at the same OID, and failed/malformed/duplicate/undecodable output.

[Baseline race test](windows-ref-query-baseline-20261022.txt),
[missing-helper red result](windows-ref-query-red-20261022.txt),
[focused green result](windows-ref-query-green-20261022.txt).

The separate disposable query matrix confirms equivalent branch/OID results
for SHA-1/SHA-256 states above. Eight balanced small-query samples per variant
record medians 0.088914950s -> 0.038358600s (SHA-1) and 0.072220300s ->
0.033599700s (SHA-256). These are query-only medians, not save or p95 results.
[Query samples](windows-ref-query-diagnostic-20261022.txt) and
[executed query script](windows-ref-query-diagnostic-source-20261022.txt).

A matched full-fixture comparison uses 100 sessions, 5,000 exchanges, 10,000
active assertions and 26,215,716 JSON bytes, fully validated before timing.
Packing is explicit disposable setup only. Four save samples per variant in
ABBA/ABBA order retain the preparation history equally for both variants.
Median save is 2.762793500s before / 2.336735950s after (15.4% lower), with
visible sample variation. Each baseline save uses 24 Git processes; each retained
save uses 22, including two combined ref queries. Both variants retain four
hash-object calls, four fresh ls-files queries and two cat-file requests; the two
complete managed-file byte hashes remain. These small matched results do not
establish p95 compliance or attribute differences between independent runs.
[Matched raw saves](windows-ref-query-comparison-20261022.txt) and
[executed comparison](windows-ref-query-comparison-source-20261022.txt).

## Frozen source and reproduction

Baseline storage SHA-256:
69ff00ee3e3a864a458f8c26074e241932911f58c654551afb1b22285eba3035.
The [baseline bytes](windows-path-allocation-retained-source-20261022.txt) are
preserved from the prior investigation. Current storage SHA-256:
47c6eac0122d1076a91f21caeb253bf6721678f4e626fc0630ab069557e55304.
[Exact current source](windows-ref-query-retained-source-20261022.txt).
The benchmark harness remains SHA-256
7f69593cbee6330af1cb67261f662db8d186cc6d00787d3710d002a8430650f2.
Historical experiments require those pinned sources in a disposable source copy;
do not replace current user code to replay them. The comparison script loads
the pinned baseline as a separate module. No provider call or real novel is used.

## Final-source verification and 30-run result

Final-source Windows suite: 129 tests in 457.064s, 127 passed and two
explicit real-symlink privilege skips, exit 0. Linux/WSL2: all 129 pass in
85.357s, zero skips, exit 0. Windows before/after runtime/test/harness/helper
fingerprints match across final verification and measurement.

Current-source ordinary-layout Windows PowerShell, optional authenticated cache:
first read 4.237690400s; read p95 5.106631200s; validation/local-save p95
3.612526000s. All 30 reads and 30 saves succeed without operation errors or
timeouts. Read misses the 2s target; save misses the 1s target. Exit 1
records unmet thresholds. No explicit Git packing/maintenance is requested.
This is the default fixture layout; prior packed/native-Git results describe
their own source and configuration, not this source. Linux performance has not
been remeasured for this source; historical Linux/earlier Windows data is kept.

Environment: Windows-11-10.0.26300-SP0, Python 3.13.13, git version 2.53.0.windows.3.
Git executable: C:\Program Files\Git\cmd\git.EXE. Disposable fixtures and external trusted
key are on canonical Windows NTFS paths; the temporary key is removed.
[Hardware inventory](windows-performance-hardware-20261022.json). Cold means
first fixture read, not a guaranteed OS cache flush. Interpreter/model latency
is excluded as stated by the unchanged harness; worker deadlines include imports.

Raw evidence: [Windows full suite](windows-ref-query-full-tests-20261022.txt),
[Linux full suite](linux-ref-query-full-tests-20261022.txt),
[30-run samples](windows-ref-query-default-30-20261022.json),
[progress](windows-ref-query-default-progress-20261022.txt),
[Windows frozen-source manifest](windows-ref-query-verification-20261022.json),
[Linux manifest](linux-ref-query-verification-20261022.json).

T149 stays unchecked; current performance remains unmet. This is no host,
novice, semantic bilingual or release approval. No safeguards, thresholds,
dependency, schema, machine setting, actual novel or manuscript are changed.
Independent runs differ in source/runtime/layout and cannot isolate a speedup
or regression. The small matched comparison evaluates this local change;
it is insufficient for a p95 claim.

## Sample audit

Nearest-rank p95 was independently recomputed from all 30 raw samples and
matches the harness. No samples are excluded or replaced. Read median is
1.841458400s; samples 10 and 11 are 6.963569300s and 5.106631200s, which make
rank 29 read p95=5.106631200s. Save median is 2.897798650s, maximum 4.635249000s
and rank 29 p95=3.612526000s. These slow read observations are not explained by
the present data. No causal claim about filesystem, antivirus, load, cache
misses or this ref-query change is made. Both current performance gates remain
unmet even though every operation succeeded and the small matched comparison
favoured the change.
