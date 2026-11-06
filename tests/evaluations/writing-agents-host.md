# Native Codex writing-agent host checkpoint

Observed: 2026-11-06, managed Linux workspace. Scope: Task 1 of
[the implementation plan](../../docs/writing-agents-plan.md), against
[the approved design](../../docs/writing-agents-design.md).

**Result: target-desktop acceptance is pending.** This exercise establishes
available documentation, local CLI version, protocol declarations and a minimal
parseable disposable fixture. It does **not** establish custom-agent discovery,
execution in a separate custom-agent context, repeated direct writer turns, or
return to orchestration in the target desktop. None of those four runtime checks
was executed. Their absence here does not establish that Codex cannot support
them. After reviewing this access limitation, the writer explicitly authorized
implementation to continue with desktop acceptance pending. This changes the
implementation checkpoint, not the native-interaction requirement.

## Available host and access

Exact inspected commands:

```sh
/opt/codex/bin/codex --version
/opt/codex/bin/codex --help
/opt/codex/bin/codex app-server --help
/opt/codex/bin/codex agents --help
/opt/codex/bin/codex exec --help
mkdir -p /tmp/novel-writing-agents/schema
/opt/codex/bin/codex app-server generate-json-schema \
  --out /tmp/novel-writing-agents/schema --experimental
```

All exited 0. Version: `codex-cli 0.163.0`. CLI startup also warned:
`WARNING: proceeding, even though we could not create PATH aliases: Read-only file system (os error 30)`.
Schema generation succeeded despite that warning.

`codex agents --help` describes browsing agent sessions on the shared local
app-server daemon. `codex exec --help` exposes `--ephemeral`, but no dedicated
named custom-agent selection option. No CLI model run or app-server session was
started. No authentication files were read, no global configuration was changed,
and no permission or model overrides were introduced.

Enabled-tool metadata was searched for `list_threads`, `read_thread`,
`wait_threads`, `create_thread`, `send_message_to_thread`, `control_browser`,
`browser`, `computer`, and `desktop`. This scoped worker had no matching native
thread/browser/desktop tools. The coordinating chat separately reported native
list/read/wait tools but no create/send tools. Existing collaboration tools can
run separate worker contexts, but their spawn interface does not expose
`agent_type`; this worker's existence is not evidence of discovery or execution
of `.codex/agents` definitions.

A local environment probe reported Linux, no `DISPLAY` or `WAYLAND_DISPLAY`,
`chromium` at `/usr/bin/chromium`, and `playwright` at
`/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/playwright`.
`xdotool` and `wmctrl` were absent. Browser executables alone do not provide
access to the writer's desktop application or its selected agent composer.
No connected desktop UI or target application endpoint was available in these
tools. No user-owned chat was created, and no current chat was modified.

## Official documentation and protocol inspection

Fetched the [official subagent documentation](https://developers.openai.com/codex/subagents)
with:

```sh
curl -Ls --max-time 20 https://developers.openai.com/codex/subagents \
  -o /tmp/codex-subagents.html
```

The retrieved page documents project-scoped `.codex/agents/*.toml`, with required
`name`, `description`, and `developer_instructions`. It says the `name` field
identifies the custom agent and that agents inherit the parent's permissions.
It documents opening an app subagent thread to inspect its work, and CLI
`/subagents` to inspect and switch agent threads. These statements do not
establish that the target desktop permits ongoing direct writer messages in
that thread. No universal top-level custom-agent picker was verified.

Generated schemas were inspected locally using Python `json.loads` and searches
for agent/role fields and method names. Relevant files beneath
`/tmp/novel-writing-agents/schema/`:

- `v2/ThreadStartParams.json`
- `v2/ThreadResumeParams.json`
- `v2/TurnStartParams.json`
- `v2/ThreadStartResponse.json`
- `codex_app_server_protocol.schemas.json`

Observed declarations:

- Methods include `thread/start`, `thread/resume`, `thread/read`, `turn/start`
  and `turn/steer`.
- `turn/start` requires `threadId` and `input`; this declares thread-targeted
  input at the protocol level. It was not sent to a running specialist.
- None of the three inspected request schemas has a dedicated named custom-agent
  selector such as `agentType` or `agentRole`. `multiAgentMode`, present in start
  schemas, is deprecated and ignored; it is not a role selector.
- `Thread.agentRole` has description: “Optional role (agent_role) assigned to an
  AgentControl-spawned sub-agent.” This is response metadata, not proof of a
  custom agent being selected or executed.
- Enumerated method names containing `agent` include external-agent configuration
  imports and `item/agentMessage/delta`; no custom-agent listing/spawning method
  was found in this generated schema. This narrow observation does not rule out
  internal model delegation tools or other native client controls.

Passing `developerInstructions` to a new thread, or instructing the main chat to
act as a specialist, would not establish native custom-agent selection. Protocol
inspection therefore cannot replace the desktop acceptance exercise.

Scratch artifacts include `protocol-summary.txt`, captured help/version output,
`subagents-doc.txt`, generated schemas, and the fixture below under
`/tmp/novel-writing-agents/`. Scratch paths are disposable, not repository assets.

## Minimal reproducible target-desktop exercise

The following single-role fixture was written only under
`/tmp/novel-writing-agents/project/`. Python `tomllib.loads` passed and confirmed
exactly the three required keys. This verifies TOML syntax and fixture shape;
it does not verify host loading. Recreate these two files in a disposable local
project on the writer's machine if this managed workspace is not accessible.

`.codex/agents/novel_scene_writer.toml`:

```toml
name = "novel_scene_writer"
description = "Disposable native-host feasibility specialist for a scene-writing conversation."
developer_instructions = """
You are the disposable scene specialist for a native-host feasibility exercise.
Begin each response with SCENE_SPECIALIST_PROOF.
Keep replies short. Preserve and recall the writer's requested test word across
turns in this agent thread. Do not invent a word when none was provided.
Do not edit files, run tools, create more agents, commit, or push.
"""
```

`AGENTS.md`:

```md
# Disposable native-host feasibility exercise
The main conversation is the orchestration context. In the main conversation
only, begin responses with ORCHESTRATOR_PROOF. Do not adopt the specialist's
marker in the main conversation. A native specialist follows its own role marker.
When the writer explicitly asks, delegate the test to the named native custom
agent novel_scene_writer. If native named-agent delegation is unavailable,
say so; do not simulate it with a persona. Do not edit files, commit, or push.
```

Exercise in the **target desktop**, preserving its ordinary permissions and model:

1. Open the disposable project and start its main conversation. Ask:
   `Let me work with the native custom agent novel_scene_writer. Delegate a short
   scene-writing feasibility test to that named agent, then let me continue
   directly in its own thread. Do not simulate it in this main chat.`
   Capture actual native discovery/delegation evidence naming the selected role
   and the distinct child thread/context. A response marker alone is insufficient.
2. Open the resulting specialist through whatever native control the installed
   desktop actually exposes. Record its label and the observed control. Check
   whether it has an enabled composer or another documented native way to address
   the selected specialist directly. Read-only inspection does not pass.
3. Send directly to that specialist: `Remember the test word amber. Suggest one
   sentence opening a scene at a closed harbor gate.` Then send another direct
   turn: `What test word did I give you? Revise the sentence to include it.`
   Capture both writer inputs, both specialist responses, the same child thread
   identity, and recall of `amber`. Do not relay these turns through an
   orchestrator or switch the main chat's persona.
4. Return through the observed native control to the original main conversation.
   Send: `Return to orchestration and summarize the feasibility result.` Capture
   the main thread identity and orchestration response.
5. Record exact desktop version/platform, role discovery evidence, selected thread
   identity, controls used and any unavailable composer/control. Mark each of the
   four runtime checks separately. If native direct turns fail or cannot be
   exercised, leave that requirement unmet/pending and report the exact step.

CLI `/subagents` may be investigated separately, but CLI success alone does not
verify this target-desktop exercise. No desktop control is claimed to work by
these instructions. A second direct turn and return to orchestration are required
before the delivered feature can claim the agreed interaction is available.

## Verification and remaining gate

Checks performed: CLI/help commands; successful experimental schema generation;
official documentation retrieval; generated-schema inspection; desktop/tool
availability inspection; and TOML parsing of the disposable fixture. No product
files or novels changed, and no code tests, builds, package installs, commits,
pushes, model calls or custom-agent launches were performed for this checkpoint.

Independent review passed the evidence's requirement compliance and probe quality,
including its distinction between documented schema, actual execution and
observed target-desktop interaction. No runtime acceptance was inferred. The precise missing
capability is access to a target-desktop specialist thread that accepts repeated
writer turns, together with observable custom-agent selection and a return to the
main context. The writer explicitly chose to continue implementation with this
desktop verification pending; the pending acceptance remains a delivery limit.
