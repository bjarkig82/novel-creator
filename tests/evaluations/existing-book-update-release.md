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

Candidate identity, archive hashes, check outcomes and host evidence binding are
recorded below as observed. Publication and named-install verification remain
pending until their protected workflow gates pass.

## Candidate built; platform checks pending

Candidate [run 41823550929](https://github.com/bjarkig82/novel-creator/actions/runs/41823550929),
attempt 1, artifact **13318445983**, source
`e2fca23e8c29c8a9bca68506c130345fbb343d34` was downloaded and its manifest verified:

| Archive | SHA-256 |
| --- | --- |
| `novel_creator-0.3.0-py3-none-any.whl` | `d0a8b60578df58ecea269935619e9ffbc8457200cfc65d498482f95bf942765a` |
| `novel_creator-0.3.0.tar.gz` | `ccd1c44177008a86e7857686b088dcd25708d073010eae6b1db34b5d55b88704` |

The local Windows literal guide passed against that wheel in a fresh environment
without inherited dependencies or changes to global Git configuration. It covered
the documented executable route, default setup, context/session/inspection,
Icelandic options and all six troubleshooting cases. The permission-denial case
is explicitly injected. See [the bound guide result](existing-book-update-release-windows-guide.json).

[Source comparison](existing-book-update-release-source.json) found 41 unchanged
package resources relative to the actual approved delegated Windows host fixture.
Only `update.py` (the reviewed corrections) and the release setup guide differ.
The original host archive was itself an unpublished controlled 0.3.0 fixture;
its version label is not proof of release-artifact identity. No new conversation
against the release archives is claimed. Host evidence is reused only for the
unchanged creative/adapter components; updater corrections have separate explicit
command-test evidence and must pass the current candidate checks.
