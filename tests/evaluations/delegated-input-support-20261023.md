# Explicit delegated-input support - 2026-10-23

User decision: add explicitly labeled delegated input while retaining native-input
and novice requirements. No acceptance criterion was relaxed.

The installed `input capture` command selects native_user or delegated explicitly,
requires current thread/turn IDs and exactly one public turn/input event, and
rejects missing, truncated, mixed, stale or malformed captures. Delegation
requires the expected parent, the supported codex_app wrapper/tool, and
evaluation-only opt-in. Its exact UTF-8 text and provenance remain distinct from
native human input. Delimiter collisions inside input are unsupported and rejected.

The command emits one host_input input_artifact for inclusion in the saved
exchange. Conversation validation allows exactly one such artifact, rebuilds
its event-derived labels and exact message binding, and never registers it as a
bootstrap creative source, including certified validation. Existing conversations
without artifacts and initialization artifacts retain their semantics. The
JSON schema fields are unchanged; older installed validators retain their old
behavior and are not silently upgraded. Provenance is not independent host
authentication or creative authority.

Red evidence includes the absent capture module, three missing multi-turn/
truncation rejections and the installed bootstrap-only artifact rejection.
The latter caught an implementation assumption before any host run; the narrow
semantic exception was added and creative-source rejection was tested separately.
The initial broader focused runs preserve this failure; they are not final passes.

Final authority/cache/installed-input regressions: 31 tests pass on Windows
(115.295s) and Linux (59.933s). Final Linux full suite: 165 tests in 97.115s,
three Windows-only skips. Final Windows suite passes 165 tests in 1143.908s with
two explicit real-symlink privilege skips. Both suite exits are zero. Read-only review
found no actionable defects in the parser or the narrower evidence-only rule.

The final wheel passes independent checks on Windows and Linux, comparing all
26 source/resource files and exercising isolated pinned install, save/reopen,
recovery and Unicode output. SHA-256:
`d0bc73c599e9c84449202556a394a0d3ab9a6c2b5790c9241c63159d422289a0`.
Earlier wheel checks are intermediate-source evidence only.

Observed tasks resume under
`product-host-runs/20261023T202447Z/`. The first Icelandic attempt stopped
honestly because the driver requested metadata-only read_thread output. The
corrected request enables public outputs and exports only selected public input,
excluding reasoning. English independently retrieved the public output and
completed its save. Both actual gates now pass independent input/save/display
ordering checks, installed-bundle comparison and fresh CLI reopening with source
artifacts exposed intact. Thirty-two subsequent case observations pass exact
input/save/display checks, and two actual fresh tasks recover all 42 English and
35 Icelandic current records with stable session IDs/modes and no creative record
changes. Scoped agent judgments, unscored setup gaps, capture/citation differences
and four equivalent English evidence timestamp transformations are retained in
the run directory. These remain separate
from structural tests, native-input criteria, novice observations and ratings.

The later [final-source Windows benchmark](windows-delegated-provenance-performance-20261023.md)
fails the read target and times out on save attempt 27 after 26 completed saves;
save p95 remains unavailable. It adds no performance compliance. T151-T158 remain open. No real
novel, manuscript, dependency, global setting, provider API, commit, push or
publication was changed. Authorized disposable tasks use ordinary Codex execution.
