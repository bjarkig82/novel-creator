# T172 lexical parent-prefix prototype — 2026-10-28

The prototype is rejected for retention: it demonstrates no improvement in the
matched full-scale comparison. No production file, dependency, resource,
benchmark policy, performance target or safeguard changes. T172 and T173 remain
unchecked.

## Distinct hypothesis

The recorded complete guards spend substantial time in `_checked_path`. Earlier
retained work avoided Path parsing/allocation for canonical exchange names; this
experiment does not repeat that change. The new source-free prototype only
avoids rebuilding/walking the two lexical parent prefixes after both exact
parents are already in the existing per-guard checked-directory set. The set is
still fresh for each guard. The first path and any missing cached parent retain
the complete original traversal. Every leaf still receives a fresh native type
query, and all metadata still finishes before bulk byte hashing.

The runner constructs a separate in-memory module from current source with this
one insertion and temporarily uses its path function. It never overwrites
storage.py. Native metadata implementations are identical to the runtime's.
This is an unretained diagnostic prototype, not qualified production behavior or
comprehensive failure-path coverage.

## Matched full-scale result

Eight fresh-worker saves use ABBA/ABBA on the same fully validated ordinary-layout
fixture: 100 sessions, 5,000 exchanges, 10,000 active assertions and 26,215,716
JSON bytes. No packing/maintenance is requested; the optional temporary private
validation key is outside the disposable novel. Every worker has the existing
30-second deadline, with imports/public payload preparation outside the save
timer. Default history/hash reader counts and Git executable remain unchanged.

| Policy | Four-save median (s) | Range (s) |
|---|---:|---:|
| Current runtime | 7.865432450 | 5.790182100–9.256357400 |
| Lexical-prefix prototype | 12.297503250 | 6.011504800–15.872754400 |

All eight saves complete without operation errors, timeouts or cleanup warnings.
For saved sequence N, each worker verifies two complete guards, 2*N bulk file
hashes and batch-read objects, and 2*(N-1) fresh bundle-leaf queries. Candidate
verification, fresh branch/CAS, receipts, fsync, index cleanup/cache/recovery and
ordinary root/path/reparse/index guards execute as before.

The ranges are wide. The contemporaneous [load sample](windows-phase22-components-load-20261028.json)
records 100% CPU use and about 2.8 GiB free physical memory during the preceding
component run. It does not prove the load at every comparison sample or explain
the difference causally. These samples show no basis for retention; they do not
prove that lexical-prefix assembly itself caused the higher median. Do not
repeat this prototype as a demonstrated improvement or substitute these eight
samples for a qualification p95.

[Executed prototype/comparison](phase22-parent-prefix-20261028.py),
[exact samples/source identity](windows-phase22-parent-prefix-20261028.jsonl),
[reproducible verifier](verify-phase22-parent-prefix-20261028.py),
[verified arithmetic and artifact hashes](windows-phase22-parent-prefix-verification-20261028.json).
The diagnostic and verifier exit 0; diagnostic stderr is empty. Runtime and
benchmark hashes match their pre-run identities. No new broad suite/wheel build
is needed for the diagnostic-only files, and no candidate 30-run qualification
is claimed because no promising candidate is retained.

The [deeper native/component investigation](windows-phase22-tree-components-20261028.md)
preserves the measured limits on tree lookup, compression and durability probes.
The unchanged ordinary-layout qualification remains read p95 1.028736700s
(<=2s passes) and save p95 3.067419500s (<=1s unmet). Further optimization needs
a separately justified bottleneck change and stable matched evidence; this pass
does not justify weakening any check or changing the target.
