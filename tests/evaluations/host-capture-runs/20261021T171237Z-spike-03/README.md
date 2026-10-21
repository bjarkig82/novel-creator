# Actual Desktop capture gate: PASS — 2026-10-21

The focused spike-03 turn resolves spike-02's exact-user-text blocker. Native
userMessage JSON, prepared payload and committed user text match without
normalization, including the ending LF. The displayed assistant final exactly
matches the committed reply: `Native capture is ready.` The successful native
save event precedes the final display. See [independent comparisons](exact-parity.json),
[public native observations](native-host-observations.json) and [manifest](manifest.json).

Checkpoint: sequence 2, exchange `1e9054a1-f963-4a15-9b8e-35e0d32fe837`, commit
`bc7318a0d534b8e21600cedc669d67661e8daf34`. All 13 pinned checksums verify,
cleanup_required is false and the fixture Git status is clean.

Capture source files belong under `.novel-creator/local/evidence/`: placing the
source directly in local/ initially collided with receipt discovery. Moving
that source to evidence/ resolved the failure without changing the payload.
A subsequent sandbox hard-link denial required an unchanged scoped filesystem
retry, which succeeded. Both failures and recovery remain in the observations.

Together with [spike-02](../20261021T161928Z-spike-02/README.md), this completes
automatic follow-ups, identical retry without duplication, saved-but-interrupted
display, genuine fresh-chat recovery, visible failed-save pause and unchanged
retry. Spike-02's original LF mismatches remain preserved as historical evidence;
the revised native-input adapter supersedes its manual here-string boundary.

Scope: Windows Desktop package OpenAI.Codex 26.1016.6573.0, user-visible
GPT-6.1 Sol Medium selector, native read_thread/current-thread availability,
single typed text input and scoped filesystem approval when required. Underlying
model revision is unavailable. Unattended default-sandbox capture, voice,
multi-input capture, other platforms, physical power-loss durability, semantic
bilingual quality and the unfinished story features are not established here.

T012/T069/T089/T103/T116 are satisfied within this tested scope; T013's latest
decision is PASS. This capability gate permits dependent implementation to begin;
it does not establish feature or release completion. No prior fixture was rewritten.
