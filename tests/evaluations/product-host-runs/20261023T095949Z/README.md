# Delegated product-host input probes — 2026-10-23

**Observed boundary: task-driven native capture is unavailable. No creative
evaluation passed or failed.** Both tasks followed the required stop rule before
installation or conversation saving. The prior direct typed-input capability result is not
revoked or broadened by these probes.

The user explicitly authorized the [prepared four-task run plan](../../product-host-run-plan-20261023.md).
Two initial local projectless tasks were created using the configured default
model. The fresh resumption tasks depended on the capture gate and were not
created after it could not pass. Both initial tasks remain available for direct
user interaction; neither was archived or repurposed.

| Task title | Thread ID | Intended manuscript language |
|---|---|---|
| Novel host evaluation English | 01a16833-e1cf-79d2-bee0-80a6ca973e3c | en |
| Novel host evaluation Icelandic | 01a16833-fa8e-7ec1-9c69-53dc7eaec197 | is |

These are actual Codex task/input observations, not installed creative-workflow
outcomes. Novel repositories were not initialized; language labels describe the
intended configuration only. Native thread metadata identifies Codex on host
`local`; exact model selector/revision and package version were unavailable and
are not inferred from historical tests or the parent's model.

## Four observed probes

| Intended language | Input route | Native current userMessage count | Actual source | Outcome |
|---|---|---:|---|---|
| English | create_thread | 0 | functionCallOutput / codex_delegation | Capture unavailable; stopped |
| English | send_message_to_thread | 0 | functionCallOutput / codex_delegation | Capture unavailable; stopped |
| Icelandic | create_thread | 0 | functionCallOutput / codex_delegation | Capture unavailable; stopped |
| Icelandic | send_message_to_thread | 0 | functionCallOutput / codex_delegation | Capture unavailable; stopped |

Native `read_thread` exposes the actual current turn. In all four probes its
administrative input is a `functionCallOutput`, with the parent thread ID and
input text in a `codex_delegation` envelope. The public delegation input matches
the driver's submitted text exactly; that establishes delivery, not the required
native userMessage boundary. Previews, delegated input fields and older messages
were not substituted. Follow-up prompts include Icelandic, Japanese, an emoji and
a final LF; none of that changes the event's source type.

The product entry requires one complete current native userMessage with one text
input. Both tasks disclosed the missing input, wrote unavailable reports and
stopped. Scoped workspace inventories contain only administrative output/work
directories and the two reports per task, with no Git/novel/story installation.
Zero semantic cases, conversation exchanges, novice ratings or human observations
were produced. No fresh-resumption test was claimed.

Initial overlarge read_thread requests (30,000/50,000 characters) were rejected;
20,000-character requests succeeded. The successful public observations, rather
than those rejected calls, establish the source-type result. An unrelated
wait_threads request also failed; completed status was verified using read_thread.
No transcript files or hidden reasoning were read to reconstruct missing input.
The exported observations exclude reasoning items entirely.

## Reproducible evidence

- [Run metadata, explicit authorization and initial driver prompts](run.json)
- Public native creation observations: [English](en-creation-native.json), [Icelandic](is-creation-native.json)
- Public native follow-up observations: [English](en-followup-native.json), [Icelandic](is-followup-native.json)
- Task-produced reports: [English creation](en-creation-gate-report.json), [English follow-up](en-followup-gate-report.json), [Icelandic creation](is-creation-gate-report.json), [Icelandic follow-up](is-followup-gate-report.json)
- [Independent boundary verification and artifact hashes](capture-boundary-verification.json)

Run `.venv/Scripts/python.exe -B tests/evaluations/product-host-runs/20261023T095949Z/verify_capture_boundary.py`
from the framework root. The verifier checks completed turn/thread identity,
source type, absent native user messages, exact delegated delivery, task reports,
workspace inventories and absence of reasoning in exported events. Its
`verification_ok: true` means that the boundary evidence is consistent;
`native_capture_gate_passed` remains **false**. It does not execute a creative case.

## Instruction clarification and verification

`workflows/entry.md` and the Codex adapter fragment now explicitly identify
delegation events and previews as insufficient substitutes for native input.
This clarifies the existing stop rule; no new source role, approval path, runtime,
schema or authority rule is introduced. Development guidance records the observed
automation limit. Existing novels and pinned earlier spike artifacts are unchanged.

Fourteen installation/portable-install/initialization tests pass on each platform:
Windows in 54.724s and Linux/WSL in 4.466s, zero skips/failures/errors, exits 0.
See [Windows log](windows-resource-tests.txt) and [Linux log](linux-resource-tests.txt).
The command is `python -B -m unittest tests.integration.test_install tests.integration.test_portable_install tests.contract.test_initialize -v`
with the existing configured environments, UTF-8/bytecode-disabled execution,
PYTHONPATH=src and normal filesystem access for disposable Windows publication.
Linux uses its existing WSL verification environment and `/tmp` fixtures.

The updated wheel is built offline with the existing bundled setuptools backend
under `dist/delegation-boundary-20261023/`, preserving earlier artifacts. Independent
wheel verification passes on Windows and Linux using the same wheel, SHA-256
`db8f9aa8def1b9338d337bbcc9fd65d46a718f05646233c90ee657d041fa035b`.
Both verifiers compare 25 source/resource files, isolated product module origins,
unknown/Icelandic initialization, pinned save/reopen, recovery and UTF-8 errors.
See [Windows wheel result](windows-wheel-verification.json) and
[Linux wheel result](linux-wheel-verification.json). Both exit 0.
No runtime Python or schema change invalidates the prior 155-test full-suite
results. Full suites and performance are not redundantly rerun for this text-only
clarification. Source/artifact fingerprints are recorded in [manifest.json](manifest.json).

Read-only independent review found no actionable issue in the public boundary
evidence or instruction clarification. It distinguished consistency checks on
exported events from independent verification of the host's provenance.

## Input needed to proceed

The current task APIs cannot generate the native userMessage needed for these
product-host conversations. A supported input route must provide that actual
current-turn item. The previously verified route is a message entered directly
in a Codex chat; one must still verify it in this particular task/host instance.

For an initial direct-input check, open either named evaluation task in Codex and
send this as an actual chat message:

```text
Continue the native capture gate from the original instructions using this message as the current input. Preserve the earlier unavailable reports.
```

That checks only native capture and the first installed save. Subsequent semantic
cases also require actual supported current inputs; one direct message does not
convert future cross-task delegation events into user messages. If the evaluation
route remains exclusively task-to-task messaging, leave the cases unavailable.
Do not relax the adapter or relabel sources to make this test plan appear complete.

T151–T158 remain incomplete, including the independent Windows save-performance
gate and the genuine novice/human criteria. The API route limitation does not
establish guidance quality, authority recognition, continuity judgments, bilingual
parity, fresh resumption or release approval. No provider API, external messages
to people, dependency change, real-novel mutation, commit, push or publication
was performed. The authorized Codex tasks used normal account task execution.
