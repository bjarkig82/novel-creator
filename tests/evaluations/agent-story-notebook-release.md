# Story notebook: 0.4.0 release preparation

**Status: source candidate only; not published.** The published stable release
remains 0.3.0. Version 0.4.0 is the next minor release because the published
0.3.0 archives cannot be replaced.

The [notebook evidence ledger](agent-story-notebook.md) records Linux structural
checks and the remaining native-host gaps. The integrated local suite passed
with three skips before this release metadata preparation. These results do not
establish Windows Codex Desktop notebook acceptance. New Windows native notebook
acceptance evidence is required before publication; record the actual journeys,
results, scope, provenance and binding to the candidate source and artifact.
Linux Codex Desktop remains unverified under T028 and is not a new mandatory gate.

The existing package-release workflow builds an immutable wheel and source
archive, runs structural checks on Windows and Linux, and requires candidate-bound
host declarations and the protected PyPI environment for publication. Record the
candidate identity, archive hashes and platform results when available. Publish
only the exact qualified candidate, then verify the public named installations and
archive hashes. No candidate workflow, tag or publication is claimed here.
