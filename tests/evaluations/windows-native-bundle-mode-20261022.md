# Fresh Windows bundle-mode query: external candidate, not adopted

2026-10-22, T149 continuation. Production storage remains unchanged:
`9bbcb0acb6442ef45ce564d4b9980abe5889fbd0373d14acb2387ae429bf2a44`. The [verified balanced-reader report](windows-balanced-save-20261022.md)
records 143-test suites and ordinary Windows read/save p95
2.289081100s/9.240644400s, both unmet. Novice evaluations remain deferred.

## Scope and safeguard review

Only the strict canonical exchange UUID.json final component, with the existing
regular-leaf check requested, uses a fresh GetFileAttributesW call. Ordinary
known attributes yield a regular-file type for the existing caller's type tests.
Every parent and every non-bundle location retains os.lstat. Zero, invalid,
directory, reparse, device and unknown attributes fall through to os.lstat.
This is a narrow ordinary disk-file experiment, not a general lstat replacement;
permission bits are not consumed at this call site. No enumeration, stat-result
cache or reuse between guards is introduced. Root/path/index checks, both full
byte guards, history/authority, private candidate/CAS and recovery stay active.

Microsoft documents that the API queries the named object's attributes, returns
a failure sentinel, and returns a symlink's own attributes:
[GetFileAttributesW](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getfileattributesw).
Review required NORMAL alone, or a nonzero subset of ARCHIVE/READONLY/HIDDEN/
SYSTEM; any NORMAL combination must fall back:
[attribute constants](https://learn.microsoft.com/en-us/windows/win32/fileio/file-attribute-constants).
The first prototype accepted invalid NORMAL combinations. A recorded red
assertion reproduced that missing fallback; the corrected external helper
passes all 16 accepted and 21 fallback combinations before save timing.
CPython additionally distinguishes device kinds, so this may not be broadened
beyond the validated strict bundle/disk-root scope:
[CPython file-type conversion](https://github.com/python/cpython/blob/3.13/Python/fileutils.c).

Actual Unicode-root ordinary/directory/missing cases and synthetic error/unknown/
special-attribute fallbacks pass. Actual Windows symlink behavior remains
unverified because creation requires unavailable privilege (WinError 1314);
the limitation is explicit, not waived. Independent read-only review found no
demonstrated narrow-scope bypass, with the NORMAL correction above required.

## Component and complete-save measurements

The first-prototype component comparison uses four balanced samples per variant
on the complete ordinary fixture. Metadata median: 0.712626850s existing versus
0.151673300s native; complete guard with four full-byte readers: 0.731543150s
versus 0.450599900s. Its normal files use the same native path as the corrected
helper; it predates the invalid-NORMAL correction and is labelled separately.

The corrected helper's eight fresh-worker complete saves, balanced ABBA/ABBA,
use 100 sessions, 5,000 exchanges, 10,000 assertions and 26,215,716 JSON bytes,
fully validated, with an opt-in private key outside the novel. Public payload
preparation stays outside timing with its history retained. Current two-history/
two-initial/four-final reader policy remains the same for controls and candidate.
Four-sample complete-save medians: 4.413188450s existing versus 3.816763250s
native (13.51% lower). Existing range 3.220360700–6.741653400s;
native range 2.748657400–4.758642100s. All saves succeed at
sequences 5001–5008 without cleanup; every save has 27 Git calls and six complete
root-bound hash partitions. The recorded full-guard file count is twice each
sequence (prior journal plus manifest, checked twice); native query count is
twice prior journal length. New-input hashes remain separate and unchanged.
All production and helper fingerprints are unchanged after measurement.

These variable small samples support further integration testing, not p95, a
portable speedup, release approval or an established 1s save result.

## Required before adoption

Add production tests for fresh queries in both guards, parents/non-bundles, all
attribute/error/unknown/NORMAL combinations, fallback exceptions and native
initialization failure, Unicode/long/extended paths, real special/reparse paths
with honest privilege skips, same-stat and staged tampering, final conflicts,
pending receipts and unchanged retry. Bootstrap and non-Windows must preserve
the existing path. Any production implementation must retain lstat when native
initialization/query cannot establish the narrow known ordinary-file result.
Then run appropriate focused checks, full suites and a fresh ordinary 30-read/
30-save benchmark with source fingerprints. No runtime adoption has occurred.

[Component samples](windows-native-bundle-mode-20261022.txt),
[component source](windows-native-bundle-mode-source-20261022.txt),
[complete-save samples](windows-native-bundle-mode-save-comparison-20261022.txt),
[complete-save source](windows-native-bundle-mode-save-comparison-source-20261022.txt),
[corrected helper](windows-native-bundle-mode-candidate-source-20261022.txt),
[artifact hashes](windows-native-bundle-mode-manifest-20261022.json).
Both diagnostic handles exited 0. T149 stays unchecked; novice evaluations
remain deferred/unverified and other host/human/semantic/release gates stay open.
