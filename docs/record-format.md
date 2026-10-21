# Record format v1

Each novel has an independent Git repository. The committed files under
`story/exchanges/` own exact visible conversation and every structured record
revision. Pending working files and ignored preparation evidence are not authority.
The manifest owns only installation identity, schema/bundle versions and pinned
resource checksums. It does not own a second editable creative brief or canon.

An envelope contains schema_version `1.0`, novel/exchange/session UUIDs, sequence,
predecessor exchange ID/digest, expected Git HEAD, recorded UTC time, operation,
messages, original bootstrap input_artifacts, record_versions, continuity_review
and payload_digest. Bootstrap begins at sequence 1 with null predecessor and may
have no conversation. Conversation messages retain exact user/assistant text.
Maintenance cannot introduce canon. Ordering follows validated predecessor/sequence,
not timestamps or filenames alone.

The SHA-256 payload digest excludes payload_digest itself and uses compact JSON,
sorted object keys, UTF-8 Unicode, original array order and no NaN/Infinity.
Strict readers reject duplicate JSON keys, bad UTF-8 and unsupported schemas.
The digest detects accidental changes; it is not an approval signature.

Records have stable id/kind, positive revision, exact previous_revision (null
at creation), created_exchange_id, source_refs and explicit origin. Revisions
are complete new record versions. Fold them by ID only after the entire exchange
validates. Display names and titles never become identity. Retain all historical
versions; exclude rejected/superseded versions from current accepted canon.

Kinds are novel_project, session, idea, story_element, relationship, assertion,
decision, question and finding. Distinguish character/location/event/plot_thread;
directional relationships retain source/target IDs. Assertions retain subject,
predicate/value, status and author_truth/character_knowledge/character_belief/
reader_revelation, with holder or reader audience. Chronology and narrative time
are distinct axes with known/partial/unknown precision, event anchors and explicit
before/after refs. Unknown bounds are null. Absence is not falsehood or ignorance.

Source refs point to an exact message UUID in an exchange, optionally with a
Unicode code-point range [start,end), or a bootstrap artifact plus JSON Pointer.
Artifacts retain original UTF-8 text, parsed JSON and its byte digest. Supplied
preferences preserve original_text separately from interpretation. Skipped answers
are unknown; defaults have explicit system_default origin and no fabricated
source. Original concept provenance is retained after title/settings changes.

Canon changes require an actual current user-message decision and exact accepting
or revising span. target_refs, selected_parts, prior_refs and result_refs explain
the selection/change; affected_refs and review_required_refs identify recorded
impact. Bootstrap artifacts, silence, praise and hypothetical dialogue cannot
authorize canon. A reference is provenance, not proof of acceptance meaning.
Protected creative directions and manuscript boundaries remain mandatory.

Continuity coverage is complete/incomplete/not_applicable for its declared scope,
not a universal literary verdict. Unavailable refs and canon_hold_refs disclose
gaps; '*' holds all canon when scope is unknown. Open/deferred significant
findings hold affected promotion; opportunities are advisory proposals. A damaged
ledger cannot safely accept even proposal writes. Restore and revalidate before
lifting a hold. Inspection returns history, source exchanges and recorded direct
impact, without claiming unrecorded dependencies have been discovered.

`context` and `inspect` are derived views carrying the confirmed checkpoint.
They cannot override records or hide unresolved findings. Saved response display
is unconfirmed; recovery cannot infer that a saved reply was seen or accepted.
Ignored caches can be deleted; the current implementation reads committed records
from its committed source. Current full-scale measurements are in tests/evaluations/performance.md.

The independent test reader reconstructs records, entities, relationships, event
ordering, perspectives, sources, decisions and current/history directly from Git
and JSON, without importing the production reducer or interpreting story prose.
Its passing fixture is structural evidence, not full language/narrative validation.
No dashboard or original host is needed to read these records.

Unsupported versions fail explicitly. No incompatible migration is implemented.
A future migration requires explicit user initiation, a preserved Git checkpoint,
a documented version/reference map, identity/history validation and recovery
instructions. Never automatically reset, amend, coerce unsupported records or
push. Keep the pinned novel-local Python bundle and its Python/jsonschema/jsonschema-rs
dependencies available; framework-path access is unnecessary for installed reads.

## Expanded independent-reader evidence — 2026-10-21

The representative consumer test now covers all nine record kinds, duplicate
Unicode names followed by renaming, known/partial/unknown timing, all four
perspectives and affirmed/denied/unknown truth, superseded/current facts and
sourced decision history. It ignores an invented local cache and produces the
same result after that cache is deleted. Missing bootstrap history, unsupported
versions, dangling record/message references and wrong creation origins fail
explicitly. The reader implements these checks independently of the production
reducer. It remains a test consumer, not a second application authority.

An isolated interpreter imports product modules exclusively from the novel-local
bundle and exercises save, context, session list, validation and history inspection
without importing the framework product modules. Its Python/jsonschema/jsonschema-rs environment
remains a documented prerequisite. This is structural portability evidence for
the tested Windows environment, not bilingual literary or cross-platform proof.

## Optional validation proof cache

Ignored `.novel-creator/local/cache/validation.json` stores derived metadata only:
Git HEAD, a digest of journal paths/modes/object IDs, a schema/runtime fingerprint
and an HMAC. It stores no story records and cannot override committed content.
The key is supplied through explicit trusted runtime configuration outside the
novel; the CLI only reads it. A key supplied by novel files is rejected.

A valid proof permits reuse of completed structural validation for that exact
snapshot. Every blob is fetched from Git, its actual Git object hash is checked
and the current record indexes are reconstructed. New exchanges always undergo
full transition, source, authority and hold validation. The cache does not attest
to acceptance meaning, language quality, literary consistency or human approval.

Changed HEAD/schema/tool/runtime, missing configuration, tracked cache metadata,
corrupt proofs or deletion trigger full validation. Cache write failures do not
change read/save outcomes. The cache is versioned independently of authoritative
record schemas; removing it requires no story migration. No key path or key bytes
are saved in authoritative story records.
