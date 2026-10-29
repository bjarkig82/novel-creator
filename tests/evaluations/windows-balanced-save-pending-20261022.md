# Balanced save readers: production verification pending

2026-10-22, T149 continuation. Frozen storage SHA-256
`9bbcb0acb6442ef45ce564d4b9980abe5889fbd0373d14acb2387ae429bf2a44`; test SHA-256
`45f49d8b22d6cddd4023769782bef5ffba5ed2370df9edab4e548255c085ff6c`.

The bounded Windows policy now selects two save-history readers and two
first-guard byte readers, retaining four public-history/final-byte readers.
Each existing threshold independently keeps inputs below 1,024 serial;
non-Windows defaults stay one. Every existing metadata-before-hash check,
actual blob/digest validation, root binding, complete byte/index/path guard,
original error/prefix ordering, original first-guard await, lock/worker joins,
private candidate, authority/hold, CAS and recovery stage stays in place.
No check is skipped or moved.

Eight focused methods pass in 85.046s, exit 0. Five new combined production
methods cover forced Windows/non-Windows selection, small bootstrap/retry,
earlier malformed history versus later history launch/nonzero failures and
failed first guard, nested first-guard process/count/thread failures and joins
under the lock, same-stat tampering with a decoy core.worktree, post-first-guard
edits, recoverable pending receipt and unchanged retry publishing exactly once.
Existing framing cases now exercise two and four readers. The initial red run
had 5 tests / 17 missing-feature errors in 27.856s with production unchanged 9b9.
Read-only review found no actionable issue in the minimal delta.

Fresh full Windows/Linux suites are running for this source (expected 143 tests);
a fresh ordinary-layout 30-read/30-save benchmark must follow their successful
completion. Those results are not yet claimed. The preceding verified 9b9 source
passed 138-test suites and read p95 1.787683800s, but missed save p95 9.219870400s.
Those results cannot verify this new source. The external ABBA/ABBA candidate
median 5.669104200s→4.856166300s is a small noisy diagnostic, not p95 compliance;
see [candidate evidence](windows-balanced-save-readers-20261022.md).

[Red run](windows-balanced-save-production-red-20261022.txt),
[focused run](windows-balanced-save-production-focused-20261022.txt),
[pending source/artifact hashes](windows-balanced-save-pending-manifest-20261022.json).
T149 remains unchecked. Novice evaluations remain deferred/unverified; all
other human/host/semantic-language/durability/release gates remain separate.
