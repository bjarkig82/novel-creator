# Distribution and Getting-Started Contract

## Distribution

Production source: PyPI. Intended distribution/console name: novel-creator. Name ownership/availability is unverified; check before claiming installability. Any required distribution rename is maintainer-approved and recorded throughout metadata/docs/evidence; console spelling can stay.

Canonical acquisition: Python/pip in a separate user-owned venv, then `python -m pip install novel-creator`. Production acceptance pins the published version and uses the production index without local wheels, checkout, caches or inherited dependency paths. Editable installs are not writer onboarding evidence.

Publish wheel/sdist with readme/content type, truthful Python/dependency metadata, project/source/documentation URLs, version and maintainer-approved licensing. If license intent is absent, resolve it with the maintainer before release rather than choosing a license incidentally. Verify sdist contents and the rebuilt wheel. Guide/bundle hashes correspond to the release source.

Proposed workflow: explicit manual release selection → build/hash → Windows/Linux candidate checks → protected PyPI publish of those artifacts → named production installs. Trusted publisher binds repository/workflow/environment; configure through maintainer account. Do not store credentials in commits, logs or novels. Planning performs no account/network mutations or publication.

Artifact handoff: the workflow has separate manual `candidate` and `publish` modes. Candidate mode checks out an immutable source commit, builds the release wheel/sdist once, and uploads them with a manifest in an immutable workflow artifact. Record repository, candidate workflow run ID and run attempt, source commit, artifact ID, distribution/version, filenames and SHA-256 hashes. Candidate tests and host walkthroughs consume that artifact's bytes and record its identity. Any wheel rebuilt from sdist is a separate verification output, never a replacement release wheel.

Publish mode accepts that exact candidate run/attempt and artifact ID, downloads the stored artifact without a build step, and verifies all identity fields and file hashes before upload. Required test/host evidence must bind to this candidate; mismatched, expired, missing or changed artifacts/evidence fail closed. A new build or source change creates a new candidate and invalidates affected verification; never substitute a fresh build under an old approval. Record the publishing run separately. Repository workflow availability and candidate dispatch are explicitly authorized execution steps, not consequences of generating this plan.

## Guide discovery and content

Canonical source: workflows/getting-started.md; package through existing workflow resources; install at .novel-creator/workflows/getting-started.md for new novels. README links to source; command help points to installed package copy; new-novel completion points to novel-local copy. Check all three routes to identical guide bytes for the same release. PyPI README uses absolute repository documentation links pinned to the released tag; relative repository links alone do not establish index-page usability.

Recognized older novels: prefer their verified pinned guide when present. If their original manifest has no guide, continuation output links to the verified current installed-package guide and labels it as a package-guide fallback; do not copy it into the novel or change its manifest/history/resources. Explain that current-package installation instructions do not upgrade the older novel and continuation uses its installed workflows. Readiness is checked against that novel's own verified manifest, not the current release's resource set. A missing fallback produces an actionable documentation diagnostic rather than a fabricated path. Test an actual pre-feature bundle without a guide, snapshot all novel bytes/history, repeat shorthand init, and verify a working fallback with unchanged novel state. Legacy machine output remains unchanged.

Clearly distinguish the minimal route from optional reference material:

1. Explain product purpose, single-writer/Codex/Windows/Linux scope and initialization results.
2. Check Python, Git, Codex and Git identity; explain external dependency acquisition and safe parent folders outside repositories. No model API key required.
3. Create/activate a reusable user-owned venv outside novels; install the public named package and verify version/help. Explain activation scope, explicit-interpreter alternative and command-not-found recovery. Never require weakening PowerShell execution policy.
4. Run one name-only init command, show expected saved/ready result and locate the independent project.
5. Open that folder in Codex, provide the printed interpreter, invoke $novel-init, and give a sample no-idea request: 'I have no story idea yet. Guide me with one question at a time.' Explain unknowns and optional brainstorming.
6. Recognize confirmed save, inspect state, and later use $novel-resume instead of init.

Optional examples cover destination, title different from name, en/is, spaces/Unicode, and correct PowerShell/Bash quoting. Essential instructions are text and copyable commands, with where-to-run, replacement values and expected results. Distinguish terminal commands from Codex prompts. Link option reference and safe recovery details.

Six troubleshooting entries: command unavailable; prerequisite unavailable; Git identity missing; unsafe destination; permission failure; interrupted initialization. Each includes diagnostic, safe corrective action and preservation boundary. No automatic global Git/security-policy changes. Recovery retains receipts and unchanged request/expected head.

Reconcile README, docs/poc-quickstart.md and docs/development.md: writers reach the package route; contributor and historical fixture instructions stay labeled. Do not rewrite historical evaluation results as new evidence.

## Verification evidence

Record release version, source/artifact hashes, OS/shell/Python/Git, resolved dependencies and source, stdout/stderr/exits, and cases/skips. Candidate checks and public-install checks are separate. Verify published metadata/hashes and named-install identity; local pyproject.toml cannot prove owner control.

Guide command checks are automated; Codex current-input/save/display/inspection/resume is actual labeled host evidence. Structural fixtures cannot substitute for host use or human approval. No novice/manual prerequisite, latency gate, or subjective quality claim is added. Feature completion still requires public named installs and required platform/host evidence.
