# Host capture run — partial, gate remains BLOCKED

Disposable installed fixture: `/workspace/host-capture-spike-5321347ef6`.

Observed Codex CLI version: 0.163.0. A native `codex exec` attempt failed before
any model turn: `failed to initialize in-process app-server client: Read-only
file system (os error 30)`. No credentials or host state configuration were changed.
See environment.json and cli-attempt.json for exact input, runtime and diagnostics.
No CLI response, continuation, fresh chat or interruption evidence exists.

The user authorized the experiment in the current desktop/voice chat. The current
utterance and prepared assistant reply were saved through the installed fixture,
then read back exactly; an unchanged retry returned the original checkpoint.
The realtime [COMPLETE] transport marker is excluded from the prepared response
body. This is one actual prepared turn, not evidence of two subsequent automatic
turns, native-host support or an observed display event. The assistant will emit
the prepared body after the successful save; independent display observation,
host/model versions and exact rendered-text comparison remain unverified.

Next: accept two real user turns without reinvoking an entry, save each before
emitting its exact prepared response, then perform genuine fresh-chat recovery,
controlled interruption and visible failed-save handling in a controllable host.
The current session cannot launch or control those separate host conversations.
No T012/T069/T089 pass or dependent story implementation is authorized by this run.

Live turn 02: actual typed user message `Next`, without skill reinvocation,
saved with its exact prepared response and verified by committed readback.
Receipt: live-turn-02-receipt.json. This is the first automatic follow-up;
one further real turn and the remaining host checks are still outstanding.
Voice rendering of the first response paraphrased its prepared text according
to the archival transcript; exact spoken-output matching is not established.
The typed follow-up is recorded separately. The full gate remains BLOCKED.

Live turn 03: second actual typed `Next` follow-up without skill reinvocation,
saved with its exact prepared response and verified by committed readback.
Both requested follow-up saves now have real user-turn evidence. The second
reply has not yet been independently observed on screen. Fresh-chat recovery,
controlled interruption, visible failure disclosure and full host/model/version
evidence remain unverified; the full host gate remains BLOCKED.
