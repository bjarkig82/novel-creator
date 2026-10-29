# Native Windows bundle metadata: production verification pending

T149, 2026-10-22. Fresh per-leaf GetFileAttributesW queries classify only ordinary
canonical bundle files. Normal attributes must stand alone; unusual, invalid,
missing or unavailable results fall back to the original lstat. Parents and all
non-bundle checks retain lstat. Full byte hashes, both complete guards, live index,
root binding, candidate verification, conditional publication and recovery remain.
Only the API callable is cached; file metadata is queried anew for every check.

Seven new tests cover API/fallback/type boundaries, Unicode and actual native
extended Windows paths, SHA-1/SHA-256 same-stat tampering, live-index changes,
pending receipts, exact retries and bootstrap/public-read boundaries. Initial
red: 7 tests, 125 missing-feature errors, 4.469s. Final focused verification:
9 tests, 25.960s, all pass, exit 0. Read-only review found no actionable production
issue. The full 150-test Windows/Linux suites and ordinary-layout 30-run Windows
benchmark are pending for this source. Prior 143-test evidence applies to the
balanced-reader source only. No performance gate or release approval is claimed.
Novice evaluations remain deferred and unverified.
