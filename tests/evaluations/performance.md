# Performance — reference targets passed; Windows save limit remains

Measured on 2026-10-21 against the complete fixture: 100 sessions, 5,000
exchanges, 10,000 active assertions and 26,215,716 UTF-8 JSON bytes. Each result
contains 30 warm read and 30 validation/local-save samples; p95 uses nearest rank.
Targets are <=2 seconds for reads and <=1 second for validation/local save.

| Configuration | First read (s) | Read p95 (s) | Save p95 (s) | Both targets |
|---|---:|---:|---:|---|
| [Linux/WSL2, full validation](linux-performance-scale-30.json) | 1.692 | 1.695 | 2.011 | UNMET |
| [Linux/WSL2, opt-in authenticated cache](linux-performance-trusted-cache-30.json) | 1.616 | 0.826 | 0.982 | PASS |
| [Windows, full validation](windows-performance-scale-30.json) | 2.439 | 2.683 | 8.650 | UNMET |
| [Windows, opt-in authenticated cache](windows-performance-trusted-cache-30.json) | 2.517 | 1.745 | 6.771 | UNMET |

The **Ubuntu/WSL2 reference run with the opt-in cache passes both targets**.
Windows reads pass with that cache; its save target remains unmet. Full validation
without the optional cache remains correct and has the separate timings above.
These results establish the planned reference measurement, not uniform performance
across all operating systems or macOS support.

## Reference hardware and environments

[Observed hardware](performance-reference-hardware.json): LENOVO 22AWS00800,
33,847,832,576 bytes physical RAM, eight logical CPUs. Windows 11 build
10.0.26300 used Python 3.13.13 and Git 2.53.0.windows.3. Ubuntu 24.04.4 LTS
under WSL2 kernel 6.6.87.2-microsoft-standard-WSL2 used Python 3.12.3,
Git 2.43.0 and ext4 for the source copy and disposable fixtures. This is WSL2
structural evidence; physical power-loss guarantees have not been measured.

## Reproduction and measurement boundary

```powershell
.venv/Scripts/python.exe -B -m tests.performance.benchmark_records --runs 30 --progress --output tests/evaluations/performance-local.json
# Full-validation comparison:
.venv/Scripts/python.exe -B -m tests.performance.benchmark_records --runs 30 --no-validation-cache --output tests/evaluations/performance-uncached-local.json
```

On Linux use the local virtual environment's `python`. Fixtures must be on a
writable filesystem outside every Git repository. Normal filesystem access is
needed where Windows sandbox policy denies hard-link publication. The harness
creates only disposable repositories and local test identities. Threshold failure
returns exit 1 while retaining every actual sample or explicit timeout.

Successful operation timers exclude interpreter imports and model latency. Save
payload preparation is outside its timer; the save's own committed-history read,
validation, file/index guards, local Git publication and cleanup are included.
Each operation uses a fresh subprocess. The first read is separate and is not a
controlled OS page-cache flush. Each warm save appends one exchange, so later
samples have a slightly larger history. Timeout deadlines include worker startup;
partial sets have null p95 values and never become a passing measurement.

## Optional cache and trust boundary

Caching requires `NOVEL_CREATOR_VALIDATION_KEY_FILE` to identify an existing
private 32-byte cache key at an absolute path outside the novel. The application
only reads this explicit runtime configuration. It never creates/modifies that
key or writes outside novel-local managed paths. The benchmark creates/removes
its own private key in a separate temporary directory. Product caching is off
until an operator supplies trusted configuration.

Ignored `.novel-creator/local/cache/validation.json` contains an HMAC-authenticated
proof bound to Git HEAD, journal paths/modes/object IDs, schemas and runtime.
It contains no story records. Warm reads fetch every blob from Git, verify its
actual Git object hash and reconstruct current record indexes. Every new exchange
receives full schema/source/authority/hold/transition validation. Missing keys,
novel-provided keys, changed HEAD/schema/runtime, forged or tracked proofs and
cache deletion cause full validation. Cache failures do not change read/save
outcomes. Structural proof does not establish creative acceptance meaning,
literary consistency, language quality or human approval.

## Changes and verification

Profiling identified repeated prefix folding/deepcopy, per-exchange/per-file Git
processes, interpreted schema validation, Python file-open overhead and repeated
path processing. Changes use incremental indexes, batched Git reads/hashes,
compiled checks of the same Draft 2020-12 schemas, complete path-component checks
with fewer temporary objects and the optional authenticated proof. The reference
validator remains for detailed failures and backend parity tests across all nine
record kinds. No model runtime, database or story-state cache was introduced.

Real-Git regressions cover cache deletion/rebuild, forged/tracked proofs, actual
installed-schema changes, changed Git object bytes under the same object ID,
novel-supplied keys, current canon authorization, both Git object formats,
same-size/same-timestamp edits and existing publication/recovery fault windows.
[Linux full-suite evidence](linux-trusted-cache-final-tests.txt) and the final
Windows suite record structural outcomes separately from host/human judgments.

The [initial timeout](performance-scale.json), profiling logs and uncached runs
are retained as prior evidence. `linux-performance-local-key-prototype-30.json`
is an early experiment excluded from the delivered trust design. The final
external-key result is `linux-performance-trusted-cache-30.json`.

T062/T063/T081/T096/T109/T122/T132 complete the measured reference scope.
Windows save latency remains an explicit platform limitation. T125-T130/T133
retain actual-host, human, bilingual, Linux/Windows and overall release obligations.
macOS support and verification are deferred from the current release.
