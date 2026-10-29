# Further Windows save diagnostics — 2026-10-22

T149 remains open; novice evaluations remain deferred/unverified. These
same-process, four-sample comparisons use disposable full-size, fully validated
fixtures and are not p95 evidence. Existing source at the time is SHA-256
`593b46960df2316ea058f03840bb8ac011a716e3c3dd516c8297d0fc91265322`.

Fresh directory-enumeration metadata and queued batch commands were not retained;
their samples/dispositions are appended to the
[history/file-check report](windows-history-guard-optimization-20261022.md).

## Isolated native Git experiment

Installed **only in an external scratch folder**, outside the project's virtual
environment and dependency files: pygit2 1.20.1, libgit2 1.9.7, cffi 2.1.1,
pycparser 3.11. No package/dependency/installation change is retained in the
product. The native prototype is restricted to SHA-1; it is not a supported
backend. The upstream [OID interface](https://www.pygit2.org/oid.html) and
[libgit2 compatibility notes](https://github.com/libgit2/libgit2/blob/main/docs/changelog.md)
do not establish the required SHA-256 compatibility for this pinned experiment.

The prototype reads raw objects from an explicit novel-local object database,
checks each actual object hash, then returns the same binary batch framing to
the existing parser. All 5,000 blobs match the baseline aggregate byte digest.
It also compares global raw-file hashing by absolute path. See upstream
[raw-object API](https://www.pygit2.org/repository.html) and
[raw-file hashing API](https://www.pygit2.org/objects.html).
No ref/index/commit builder or guard pass is replaced. Existing candidate,
authority, hold, cache, live-index, CAS, fsync and recovery code still runs.

| Operation | Existing Git median | Native prototype median |
|---|---:|---:|
| Full bulk-object read | 1.839370550s | 2.044156750s |
| Full-file guard | 1.127681550s | 1.623866750s |
| Whole save | 7.367642750s | 8.981041950s |

The prototype is slower in each measured component and whole-save comparison.
No native binding is retained. Samples are highly variable and cannot be
compared causally against earlier dated p95 runs or used to close a gate.
[Raw samples, versions and source identity](windows-native-objects-diagnostic-20261022.txt).
No actual novel, machine security setting, threshold, schema or dependency file
was changed. No provider call, commit or push occurred.
