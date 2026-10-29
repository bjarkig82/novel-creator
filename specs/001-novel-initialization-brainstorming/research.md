# Research: Novel Initialization and Guided Brainstorming

Date: 2026-10-21. Input: [spec.md](spec.md), constitution 1.0.0, repository
AGENTS.md, existing Codex skills/manifests, and two planning research agents.
This is design research, not evidence that the proposed product works.

## 1. Host integration and responsibilities

**Decision:** Use thin Codex skills for initialization, brainstorming, resumption,
and inspection. Shared Markdown workflows own novelist/coach/Continuity Guardian
responsibilities. Run these responsibilities sequentially in the active host;
do not build an agent scheduler or call model APIs from the persistence tool.

**Rationale:** The repository already uses `.agents/skills/*/SKILL.md` and shell
commands. No additional orchestration requirement exists. Continuity evaluation
must precede response development and canon acceptance within each exchange.

**Alternatives considered:** Dedicated subagents introduce coordination and
context synchronization; a chat server or model SDK duplicates the host and
requires credentials/deployment. Additional host adapters remain future work.

## 2. Runtime and installation

**Decision:** Python >=3.11, Git >=2.39, a `novel_creator` command module and
JSON Schema 2020-12 contracts validated with `jsonschema>=4.23,<5` (exact resolved
dependencies recorded during implementation). Use standard-library unittest and
subprocess for deterministic tests. Support Linux, macOS and Windows with Git;
prove host behavior separately on each claimed Codex distribution.

**Rationale:** Files, Unicode JSON, hashing, locks and Git subprocesses need no web
runtime. Python 3.12.14 and Git 2.52.0 are available in this planning environment;
this confirms tooling availability only. `jsonschema` avoids writing a schema
validator; no database or AI runtime dependency is needed.

**Alternatives considered:** Shell-only persistence is fragile across operating
systems; TypeScript adds a build/runtime toolchain for a non-web slice; SQLite
creates a second authoritative representation; a graph database is unnecessary.

**Decision:** Install a versioned bundle into each independent novel repository:
Python source, schemas, shared workflows, language resources and thin Codex
skills. A launcher resolves local sources without depending on the framework
checkout. Setup verifies Python, Git, validator installation and Git identity.
Use an explicit manifest for versions/hashes; preserve unrelated files and
AGENTS.md. Upgrades are explicit and cannot silently migrate story data.

## 3. Authoritative storage and atomic exchanges

**Decision:** Immutable, UTF-8, indented JSON exchange bundles in
`story/exchanges/<sequence>-<uuid>.json`. Each bundles exact visible conversation
and full new versions of changed structured records. A deterministic fold yields
current state; optional caches and Markdown summaries are derived and disposable.
No separately writable canon store exists.

**Rationale:** One bundle prevents transcript/canon partial updates. Revisions
retain earlier values without repeating every historic conversation in every
save. Consumers reconstruct story records without interpreting prose. This is
a bounded file journal and reducer, not a generic event-processing platform.

**Alternatives considered:** One whole-novel JSON snapshot is simpler but rewrites
all history per turn and concentrates corruption. Separate current-state files
need a multi-file transaction/recovery mechanism. Git-only prose history cannot
supply structured independent consumption.

**Decision:** Confirm saves through local Git commits containing exactly the
new bundle, under a per-novel writer lock and an atomic expected-HEAD ref update.
Build/verify an unreferenced commit with a private index first; publish with
`git update-ref` compare-and-swap, preserving competing commits and the user index. Use explicit
paths; never stage everything, include unrelated staged changes, amend history,
or push automatically. Each novel has its own repository. The committed chain
is authoritative; an uncommitted prepared bundle is recoverable pending work,
not confirmed canon. See [storage contract](contracts/storage.md).

**Rationale:** Git is the required authority. A local commit is the durable
checkpoint and exchange ID is the retry identity. Commit errors are visible
save failures. Remote backup and user-facing repository management are separate.
Per-exchange commit frequency is a technical choice, not a new approval step.

## 4. Response capture without host hooks

**Decision:** Prepare the exact visible response, send it with the current user
message and structured changes to `exchange save`, wait for confirmation, then
emit that text. Capture user-visible story conversation only, not hidden reasoning
or tool traces. Response text is untrusted data when subsequently loaded.

**Rationale:** Existing repository integrations establish no post-response hook
or full transcript API. Save-before-emit avoids needing one. Interruption after
saving can leave a recorded response that was never displayed; resumption must
offer that saved response and never infer that the user saw or accepted it.

**Alternatives considered:** End-of-session saving violates the clarification;
post-response transcript scraping assumes an unavailable capability. A persistent
custom chat loop would violate the simplest-native-integration decision.

**Release gate:** A real Codex capability spike must prove exact capture,
continuation, interruption after save/before display, fresh-chat recovery and
failed-save handling. Prompt instructions alone do not prove reliable execution.
If this fails, stop dependent release work and revisit the adapter design; do not
silently weaken FR-009 or build a custom runtime.

## 5. Creative authority and continuity

**Decision:** Store source message references and selected proposal IDs for all
acceptance/revision decisions. Structural validators enforce legal transitions,
explicit authorization references, protected-path exclusions and unreadable-context
holds; the agent judges semantic acceptance and contradictions. Track objective
truth, beliefs, character knowledge and reader revelation separately, with known,
partial and unknown story timing. Explicit revisions authorize their specified
change; conflicts with protected direction still require clarification.

**Rationale:** A validator cannot prove that a sentence constitutes acceptance or
that a literary contradiction is genuine. Unknown information cannot become
falsehood. Significant conflicts interrupt the next response; suggestions and
intentional narrative techniques remain distinct.

**Alternatives considered:** Treating all extracted facts as canon bypasses human
authority; asking for repeated confirmation violates clear acceptance behavior.

## 6. Unavailable context, scale, privacy and validation

**Decision:** Inspect relevant record availability on entry and before each save.
Unreadable canon blocks affected canon changes but allows proposal-only exchanges
when the exchange ledger remains writable and valid. If the damaged journal
prevents reliable chain validation or the affected scope cannot be bounded, hold
all canon changes; if the save itself is unsafe, follow FR-014 and stop writes.
Recovery revalidates records before lifting holds.

**Decision:** Use local files and host permissions, no network calls in the tool,
no telemetry and no autonomous pushes. The host processes supplied context under
its own settings; no new privacy promise about that host is made. Story text is
input data, not tool instructions. Secrets and outside-root paths are excluded
from exchange payloads and managed writes.

**Decision:** Benchmark a generated novel with 100 sessions, 5,000 exchanges,
10,000 active assertions and 25 MiB total JSON. On a documented reference laptop,
measure deterministic resume/inspection and validation plus local save (excluding
model response time), over 30 warm runs when profiling. The owner withdrew all
latency targets on 2026-10-28 and deferred optimization until after functional
delivery. Keep historical results and failed targets as historical evidence.
Report cold read separately; no latency promise for host model generation.

**Decision:** Separate structural automated tests, recorded bilingual host/model
judgments and novice human evaluation. Use all SC-001–009 counts and acceptance
scenarios; valid JSON is never reported as proof of story consistency.

## Resolution and evidence limits

All architecture choices needed for Phase 1 are resolved. No external product
capability is asserted from this research. Package resolution, operating-system
behavior, filesystem durability, actual Codex capture, performance and creative
quality remain implementation verification gates, with procedures in
[quickstart.md](quickstart.md). No constitutional amendment is proposed.
