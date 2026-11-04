# Existing-book updater: 0.3.0 release

The maintainer authorized PyPI publication on 2026-11-04 after merging PR #4.
Release preparation targets 0.3.0; publication is pending verified candidate gates.

The protected workflow builds an immutable wheel/sdist artifact and checks it on
Windows and Linux. Publication must select that exact successful run, attempt,
source commit and artifact; it must not rebuild or claim unavailable checks.

The [feature qualification](existing-book-update-qualification.md) distinguishes
the earlier full suites, PR-review regressions and fixed-metadata packaged tests.
The [actual host evidence](existing-book-update-host.md) retains delegated input
provenance. Native host evidence may be reused only for explicitly verified
unchanged behavior/components, with candidate identities bound separately.
Direct native-user update input and Linux Codex integration remain unverified.
FUP-001 and conservative runtime-fingerprint refusal remain disclosed limits.

Exact candidate identity, archive hashes, check outcomes, host evidence binding,
publication result and named-install verification will be recorded below as
they are observed. No current candidate or public installation is claimed here.
