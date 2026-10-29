# Git blob identity checks - 2026-10-23

Candidate verification and uncached history reads accepted a corrupt loose Git
blob stored under its original object ID when its replacement bytes parsed to
the same exchange. Canonical payload validation cannot authenticate the raw Git
object: compact and pretty JSON can describe the same record. Git cat-file does
not itself establish this raw identity for these reads.

The candidate verifier now hashes the raw blob header and bytes using the
repository's SHA-1 or SHA-256 format before parsing. History reads perform the
same existing identity check regardless of validation-cache certification,
before parsing, accepting an exchange or creating a proof. No extra Git calls,
filesystem reads, dependencies or authority sources were introduced.

Real-object regressions cover both formats. The candidate tests reject a
corrupt object, preserve HEAD/index/history and pending work, then publish the
restored pending exchange exactly once. The history test covers disabled,
missing, invalid and certified proofs, preserves the last verified checkpoint,
HEAD/index/proof, and reopens the restored history. The test helper restores
the original object bytes and permissions.

Before the fixes, candidate tests failed four subcases and the history test
failed six (three uncertified policies in both formats). The already-certified
path rejected corruption before this change. After both fixes, all 12 focused
candidate/cache tests pass on Windows (43.235s) and Linux (3.707s).

Intermediate candidate-only full suites: Windows 157 tests in 462.427s, two
explicit symlink-privilege skips; Linux 157 tests in 47.344s, three Windows-only
skips. Both exited zero. These are intermediate-source evidence, not final
history-fix verification. The final Linux suite passes 158 tests in 753.914s
with three Windows-only skips. The final Windows suite passes 158 tests in
32783.725s with two explicit real-symlink privilege skips. Both suite exits are
zero. The Windows job spanned an unusually long elapsed verification interval;
its duration supplies no product-performance or before/after timing evidence.
Both independent wheel checks pass, compare all 25 source/resource files, and
exercise pinned isolated installation, save/reopen, recovery and Unicode output.
The common wheel SHA-256 is
`a8be8f63cd77ef958e0e4307a686eae1f78c4360017a869ad6237efda22488e6`.
Test-suite durations are elapsed verification times, not product benchmarks.
The accompanying manifest verifies both final suites, wheel results and pinned
runtime/test source hashes. It can be regenerated with
`python tests/evaluations/verify-git-blob-integrity-evidence-20261023.py` from
the repository root.

Read-only review found no actionable defect in either fix. A separate tree
corruption probe was rejected by Git ls-tree on the tested Git versions; it
does not justify a tree-handling change or a broader portability claim.

This repair does not complete T151-T158. Genuine novice observations, native
product-host and bilingual evaluation, the Windows one-second save target and
dependent release approval remain open. Earlier performance results are tied
to their earlier source. No commit, push or publication was performed.
