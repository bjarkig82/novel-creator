# Writing-agent resource and workflow evidence

Observed November 6, 2026, in the managed Linux checkout. These are focused
development checks on the unpublished 0.4.1 source candidate, not release
qualification, native desktop acceptance or a literary-quality assessment.

## Scope and host boundary

The approved [design](../../docs/writing-agents-design.md) adds six native Codex
agent definitions, shared manuscript/research/review/role workflows and five
focused skills to newly initialized notebooks. The writer explicitly authorized
implementation while target-desktop verification remains pending.

The [host checkpoint](writing-agents-host.md) records the available CLI version,
protocol inspection and a minimal reproducible desktop exercise. Neither a
parseable TOML definition, a valid link nor a manually instructed collaboration
worker proves that Codex loaded the named custom agent. Native discovery,
delegation through these definitions, repeated direct specialist turns and
return to the orchestrator remain unverified in the target desktop.

## Baseline and regression

Before implementation, the existing virtual environment passed:

```sh
.venv/bin/python -m unittest tests.unit.test_notebook_contract -q
.venv/bin/python -m unittest tests.integration.test_notebook_init tests.contract.test_notebook_cli -q
```

Results were 3 and 22 cases, respectively. An initial attempt to run the second
command through system Python failed to import `novel_creator`; using the
existing project virtual environment resolved that setup error without a product
change.

The added real-initialization resource regression was run before initializer or
package edits:

```sh
.venv/bin/python -m unittest tests.integration.test_notebook_init.NotebookInitialization.test_writing_agents_and_guidance_are_installed_unchanged_and_tracked -v
```

Its one case failed in both English and Icelandic because initialized projects
contained no `.codex/agents/*.toml` definitions. It did not fail because of an
import or fixture error.

After integration:

```sh
.venv/bin/python -m unittest tests.integration.test_notebook_init tests.unit.test_notebook_contract tests.contract.test_notebook_cli -q
.venv/bin/python -m unittest tests.integration.test_notebook_package -q
```

Results: **26 focused cases passed**, followed by **1 package case passed**.
These include existing-destination preservation, notebook contracts and direct
legacy resource/export boundaries; they do not represent the complete suite.
The package case was also rebuilt and rerun after final README metadata changes;
both artifacts and all four installed language journeys passed again.

## Distribution and installation checks

The package test builds a real wheel and source distribution, then compares the
source bytes of 26 resources in each artifact: six agent TOMLs, eleven skills,
eight workflows and root project instructions. That is 52 artifact-member
comparisons, covering all newly added product resources and retained guidance.

Each artifact is installed offline into its own disposable environment outside
the checkout. An isolated `-I` origin probe checks that the product module comes
from that environment. Each installed console initializes both English and
Icelandic, producing four independent notebook initialization journeys.

For each initialized notebook, checks cover 26 source-byte comparisons with the
existing LF normalization, tracked resources, six unique exact agent names and
supported nonempty TOML fields, actual local guidance links within the project,
language seeds and clean initial Git history. Initialization creates no empty
manuscript, research or review directories. Direct-script help for the release
verifier still works; the full rebuilt-wheel verifier was not run.

The initial resource-only check independently parsed all six definitions and
resolved 66 Markdown links in their intended installed layout. These structural
checks establish resource integrity, not agent discovery or creative behavior.

## Application evaluations

An application worker initialized disposable English and Icelandic notebooks
through the editable-source CLI, seeded the existing language fixtures, read
the installed guidance and applied explicitly simulated writer requests with
real file/Git tools. Three disposable assertion drivers exited 0. This was not
a native custom-agent loading or conversation-routing test. Python served as a
test driver, not a product conversation controller.

| Scenario | Observed result |
| --- | --- |
| Standalone scene draft | Stable scene/index saved; the sender mystery stayed open, accepted facts unchanged and a new visual detail recorded as proposed. |
| Incorporation into a chapter | Preserved the exact current uncommitted source and index before transfer; retained a simulated writer sentence and one prose owner; old scene retired to a pointer. |
| Narrow revision after a stale read | Detected a writer append, reloaded and preserved exact current prose historically; inverse-replacement equality confirmed only the requested sentence changed. |
| Research without browsing | Consulted an actual local fictional test excerpt, cited its path and scope, disclosed unavailable browsing and real-world uncertainty; all manuscript and notebook hashes stayed unchanged. |
| Seeded interrupted incorporation | In a separate copy, recovered retained source against an incomplete pending destination, then verified one complete insertion and sole owner. This was a seeded state, not an induced filesystem failure. |
| Icelandic scene and chapter | Saved Icelandic headings/prose with stable IDs; original fixture bytes and field tokens survived incorporation. No literary-language assessment is implied. |
| Shared authority and staged work | English six-document and Icelandic five-document notebook subtrees passed the existing format/link checker; sender=open, delivery=resolved, ghost=rejected, occupation=accepted and hope=proposed were retained. The unrelated staged writer note and initial HEAD stayed unchanged. |

The English worker's final chapter SHA-256 was
`396c3ffd81157809a4aac84d1516cb7cae477a8d7a69d02029e9f00962cea750`.
Pre-transfer uncommitted source and its historical recovery copy shared SHA-256
`4f0abbf1d649f96df59881cc7fa9efb0ea13af51bb555b441ca4979d5bf262bb`.
These observations concern the generated disposable test content, not a real novel.

A fresh reviewer context read the installed review workflow, final English prose
and owning notes without the drafter's reasoning/report. It saved a review tied
to the actual untracked prose hash, found no substantiated consistency conflict
in that scope, and verified all fourteen manuscript/notebook file hashes were
unchanged after review. This establishes separate-context application review;
it does not establish host selection of `novel_reviewer` or subjective quality.

Delegated workers did not checkpoint: their installed workflow assigns commits
to the coordinator. Files were saved/read back; later checkpointing remained
pending. No actual save or commit failure was observed. These evaluations do
not establish direct-specialist checkpoint behavior, path-scoped committing under
staged work, OS-error handling, native default routing, persistent direct native
specialist conversations or exhaustive continuity. Source scripts, generated
files and detailed assertion reports were inspected in disposable `/tmp`
scratch; they are not shipped product resources or durable test fixtures.

## Review and delivery limits

Independent requirement-compliance and quality review passed the role/manuscript
resources, installation/package changes, documentation/application evidence and
the host evidence/probe. Overall review found one documentation portability
issue: two source-relative usage-guide links were absent from packaged legacy
layouts. Both references now explicitly identify the guide in the updated source
checkout, without adding notebook resources to legacy novels. Real exported-bundle
bytes and source references passed validation. Independent scoped re-review marked
the finding addressed with no new breakage. There are no open review findings on
the scoped source implementation; native desktop acceptance remains pending.

No full suite, full Windows/Linux release qualification, publication, push,
global configuration change or real-novel edit is established by these checks.
Earlier 0.4.1 release evidence applies to its recorded source and artifact
hashes; it does not qualify these new source changes. Existing notebooks and
legacy novels are not automatically updated or migrated.
