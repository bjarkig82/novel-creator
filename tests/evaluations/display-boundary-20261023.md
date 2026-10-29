# Save-before-display boundary: observed commentary defect

Phase 22's installed English/Icelandic capture runs exposed a host workflow
failure beyond final-response equality. Both CAPTURE3 tasks emitted creative
conclusions in commentary before the matching successful save. Their final
responses matched committed assistant messages, but that alone did not prove
the full save-before-display contract. An earlier English administrative gate
also emitted two extra trailing newlines; a separate retry passed.

Original public observations, committed failed exchanges, exact commentary and
separate agent classifications remain under
[the original run](phase22-runs/20261023T225457Z/README.md). They are not rewritten
or counted as successful full-boundary observations. Determining whether text is
story content is an explicitly recorded agent judgment. The ordering comparison
against the public successful-save event is deterministic.

## Cause and narrow change

The shared entry workflow described the prepared reply and final display without
explicitly covering story-bearing progress commentary. The host followed general
progress-update instructions while revealing unsaved creative conclusions. The
storage transaction cannot prevent text the host emits before invoking it.

workflows/entry.md now applies the boundary to all creative display channels.
Neutral operational updates remain possible; creative content is prepared and
saved before display. Failure disclosures retain their exception. Exact delivery
includes leading/trailing whitespace. No runtime, schema, dependency, authority,
provenance, hash/path/index/lock/CAS or recovery behavior changes. No existing
novel's pinned bundle is replaced.

## Verification

The evidence verifier first accepted a matching final despite an agent-classified
story comment before save. A behavioral regression test failed with
`ValueError not raised`; the corrected verifier rejects that chronology and
unreviewed/changed commentary. It requires complete separately recorded commentary
classifications when a case opts into full-channel assessment. Tests do not
classify literary content by English keywords or equate schema checks with meaning.

Twenty-two affected checks pass on each platform: Windows 169.228s; Linux 14.087s.
They cover verifier evidence corruption, initialization/install, guidance,
three-session structural recovery, portability, languages and installed input
source labels. These are fresh affected runs, not a fresh full-suite claim.

The new offline wheel independently verifies on Windows and Linux against all
26 source/resource files and isolated pinned save/reopen checks. SHA-256:
`003c938689ca6121488884fe3d0a2e53bd9a04a06688cc7d3c3abed798898514`.
Artifact: dist/phase22-20261023/novel_creator-0.1.0-py3-none-any.whl.
Historical wheels and POC evidence remain unchanged.

Current installed-host regressions are retained under
phase22-runs/20261023T231406Z/. Both refreshed gates, all three capture sessions
and both correction/checkpoint responses pass exact input, saved/displayed final,
save order, current bundle identity and separately reviewed commentary checks.
The repeated third-session scenario no longer discloses creative conclusions in
pre-save commentary in either language. This is scoped host regression evidence,
not a guarantee of arbitrary future host adherence. Fresh recovery and complete
task qualification are recorded separately. POC readiness remains distinct from
broader qualification; no novice/manual prerequisite is reinstated.
