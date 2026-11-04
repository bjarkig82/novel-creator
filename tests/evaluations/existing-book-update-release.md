# Existing-book updater: 0.3.0 release

The maintainer authorized PyPI publication on 2026-11-04 after merging PR #4.
**Version 0.3.0 is published and independently verified**, including exact public
archive hashes and clean named production installations on Windows and Linux.
The protected candidate and publication workflows completed successfully.

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
recorded below as observed. Preparation/timeout sections retain their historical
states; the final published-and-verified section records the completed result.

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

## First candidate Windows timeout; not publishable

Run 41823550929's Linux job passed all 372 tests (three Windows-junction skips),
wheel verification, clean wheel/sdist installs and the literal Bash guide.
The Windows job was cancelled by its 45-minute job timeout during the full suite.
Its retained log shows all 20 changed-resource checkpoints and all 12 durable
transition checkpoints recovered, but no final suite result. This is incomplete
Windows evidence, not a test-suite pass, and the candidate must not be published.

The job's hang-protection bound is raised to 90 minutes so the existing functional
matrix can finish. No product code, tests, assertions, discovery or publication
gate is weakened or skipped. There is no performance acceptance target. A new
source commit and immutable candidate are required; the cancelled candidate and
its archive identities above remain historical and will not be republished.

## Replacement candidate; checks pending

Candidate [run 41830297234](https://github.com/bjarkig82/novel-creator/actions/runs/41830297234),
attempt 1, artifact **13322367181**, source
`e895a1a285a118afaf5217d10b3f2fa3aa3734bf` replaces the cancelled candidate:

| Archive | SHA-256 |
| --- | --- |
| `novel_creator-0.3.0-py3-none-any.whl` | `f7eb10ca004a19fd9643800769fc6b31856f1c9da86db1df516eb02638a67d44` |
| `novel_creator-0.3.0.tar.gz` | `9ba6643d9ffd77b9fcc83a796844d8ca53e8c2697b33beba741a61a2ff32f919` |

The fresh download passes manifest verification. All 48 uncompressed wheel
entries, including distribution metadata, match the first candidate exactly;
archive identity is nevertheless distinct and retained. The Windows literal
guide was rerun against this exact wheel and passed all nine command steps and
six troubleshooting cases. The current source/guide JSON records bind these
results to the replacement artifact, preserving the first identity separately.
Full platform checks remain pending; no publication has occurred.

## Replacement candidate qualified

Run 41830297234 completed successfully. Windows passed all **372 tests without
skips**, wheel verification, and clean wheel/sdist installation checks. Linux
passed **372 tests with three Windows-junction skips**, the same archive checks,
and the literal Bash setup guide including all six troubleshooting cases.
Durations (Windows 2480.144s; Linux 438.759s) are informational, not acceptance
targets. The longer job bound allowed the unchanged matrix to finish.

The [candidate check reports](existing-book-update-release-candidate-checks.json)
bind both clean installations to artifact 13322367181 and its wheel hash.
Publication will select exactly this successful run/attempt/artifact/source and
the recorded host/guide scope; the first cancelled candidate remains ineligible.
The runtime/host limitations above remain unchanged. Public named-install
checks must still verify the exact published hashes after upload.

## Published and verified - 2026-11-04

Protected [publication run 41837616353](https://github.com/bjarkig82/novel-creator/actions/runs/41837616353)
uploaded the exact successful replacement candidate without rebuilding. The
wheel was uploaded at 13:24:37 UTC and sdist at 13:24:38 UTC. Direct PyPI JSON
and independent archive downloads confirmed both hashes exactly match artifact
13322367181. Tag `v0.3.0` identifies candidate source
`e895a1a285a118afaf5217d10b3f2fa3aa3734bf`.

Both Windows and Linux clean named installations of `novel-creator==0.3.0`
selected the approved wheel, passed dependency checks, initialized and validated
independent books, and preserved English/Icelandic options. These checks inherit
no development dependencies. See the [public verification record](existing-book-update-release-public.json).

The first Windows public check ran shortly after upload and PyPI's simple index
listed only 0.1.0/0.2.0 there. After directly confirming both 0.3.0 archives were
visible in the simple index, only the failed install job was rerun. It passed;
the publisher was not rerun and no archive was replaced. This transient failure
and the earlier candidate timeout remain documented rather than relabeled green.

Package installation alone does not update pinned books. Use the reviewed
external-controller workflow, retain legacy closed-client requirements and
conservative runtime-fingerprint checks, and preserve the explicitly unverified
direct native-user update input / Linux Codex boundaries. No real book, provider
call, contribution opt-in or contribution publication was part of this release.

