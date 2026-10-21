# Storage and Transaction Contract v1

## Novel repository layout and ownership

```text
<independent-novel-root>/
├── .git/
├── .gitignore
├── .gitattributes
├── AGENTS.md                         # existing content preserved
├── .agents/skills/novel-*/SKILL.md    # installed thin Codex entry points
├── .novel-creator/
│   ├── manifest.json                 # novel ID, bundle/schema versions and hashes
│   ├── run.py                        # local launcher
│   ├── src/, schemas/, workflows/, languages/
│   └── local/                        # ignored locks, preparation, disposable caches
└── story/exchanges/
    └── 000001-<uuid>.json             # subsequent sequences use same format
```

Exchange bundles own all creative records and user-visible conversation. Current
canon/brief/session state is a deterministic fold, not an editable second source.
The manifest owns installation metadata only. The Git committed chain owns
confirmed saves. Working-tree changes and prepared bundles are pending work until
validated and committed. Independent readers use committed bundles in sequence
and the documented data model; no original host or prose extraction is required.
Generated summaries must include `derived: true`, source refs and checkpoint.
Ignore caches, locks, temporary payload files and environment dependencies; never
ignore authoritative bundles. Use LF for JSON/Markdown and preserve Unicode text.

## Per-exchange protocol

1. Read the confirmed checkpoint and applicable records. Allocate exchange and
   message UUIDs before preparing response or retry; retain them through retries.
2. Prepare exact visible assistant text, typed new record versions and continuity
   assessment. Include expected Git HEAD, predecessor ID/digest and next sequence.
3. Acquire an exclusive novel-local lock using atomic directory creation. Record
   owner/process information. A held lock returns conflict; stale locks require
   explicit recovery inspection, never silent theft.
4. Recheck HEAD, journal/manifest hashes and relevant input versions under the
   lock. Detect working-tree modifications of managed records and incompatible
   staged changes; surface conflicts rather than overwrite. Unrelated unstaged
   files are preserved. An externally advancing HEAD causes a stale-write result.
5. Validate schema, IDs, sources, state transitions, dependency holds and managed
   write allowlist. Reject invalid canon mutations before publishing any changes.
6. Serialize the entire bundle, flush and fsync a temporary file on the same
   filesystem, then atomically publish its unique final filename. Verify absence
   of a competing payload. Readers do not treat this uncommitted file as confirmed.
   Use platform-appropriate directory flush where supported; validate crash
   behavior on each claimed filesystem/OS and disclose unsupported durability.
7. Build the candidate tree in a private temporary Git index seeded from the
   expected HEAD. Add only the new bundle with explicit paths; create an
   unreferenced commit using `git commit-tree` with exactly the expected parent.
   For an unborn bootstrap, use an empty tree and no parent; include only managed
   setup paths. Verify the tree delta, parent and bundle digest before publication.
   Never touch the user's index while constructing the candidate.
8. Publish by compare-and-swap: `git update-ref <branch-ref> <candidate> <expected>`.
   The target is the captured local branch ref, never a remote ref. Bootstrap
   requires the ref still be absent (the null object ID). A moved branch causes
   failure without changing it; the candidate remains non-authoritative pending
   work. Verify the checked-out branch identity has not changed; concurrent
   checkout/branch switching is unsupported and blocks further tool operations.
9. Successful ref update is the commit point. Return that committed ID, exchange
   ID/digest and sequence; only then may the adapter emit the response. Synchronize
   only managed index entries, under Git's index lock and only if their prior
   contents still match the captured baseline. Preserve unrelated index/worktree
   changes. If synchronization fails, report saved-with-cleanup-needed and pause
   writes until recovery; do not call an already published exchange unsaved.
   Release the novel lock in cleanup. Lost receipts are resolved by committed
   exchange ID/digest, not by creating another decision.

The novel lock serializes tool writers. The conditional ref update protects
against external commits between validation and publication: a rejected save
never enters authoritative branch history. Unreferenced objects and uncommitted
files are not authority. Integration tests must advance the branch immediately
before update-ref and verify the competing HEAD and index remain unchanged, with
no candidate exchange visible to committed readers. Recovery never force-updates
refs, resets unrelated work, amends history, or pushes. Concurrent checkouts or
external history rewriting are outside the supported single-director workflow;
report conflicts and preserve evidence rather than guessing how to merge them.

## Recovery and idempotency

| Failure window | Authoritative state | Required behavior |
|---|---|---|
| Before publication | Prior checkpoint | Ignore incomplete temp; disclose unsaved exchange; retry same ID |
| File/candidate prepared, ref update failed/interrupted | Existing authoritative branch checkpoint | Preserve pending payload; inspect ref and exchange ID before explicit retry; reject stale parent |
| Ref published, index cleanup interrupted | New committed exchange | Report saved-with-cleanup-needed; recover managed index safely without replaying decisions |
| Ref publication completed, receipt lost | New committed exchange | Same ID/digest returns original success without a duplicate decision |
| Saved, display interrupted | New committed exchange | Offer exact saved response on resume; do not infer user saw/accepted it |
| Same ID, changed contents | Original committed/pending payload | Reject conflict; never replace original |
| Stale expected parent | Existing checkpoint | Return both expected/actual heads; reload and reconcile before a new attempt |
| Record unreadable/unsupported | Last verifiable checkpoint and explicit gaps | Proposals only if chain can safely extend; hold affected canon, or all canon when scope unknown |

Pending recovery cannot silently regenerate a different payload under the same
ID. If reconciliation changes content, retain the failed attempt for inspection
and allocate a new exchange after explicit conflict resolution. Read commands
never promote pending files. A repository that cannot validate a safe predecessor
cannot accept even proposal writes; the adapter can discuss its failure but cannot
claim the discussion was saved.

## Consumer and compatibility contract

Read versioned envelopes; validate chain/digest and fold full typed revisions by
stable ID. Verify exact previous revision and references before applying an entire
bundle. All-or-nothing application is required. A consumer may expose partial
available information only with an incomplete flag and unavailable references;
it cannot claim complete canon by skipping damaged records. Unsupported schemas
are explicit failures. No ordering by filename alone or timestamps. Source text
and captured records are separate; only recorded decisions authorize canon.

Migrations require a preserved Git checkpoint, documented version map, reference
validation and recovery guide. No automatic incompatible migration or destructive
rollback is part of v1. Remote pushes/backups remain explicit user operations.
