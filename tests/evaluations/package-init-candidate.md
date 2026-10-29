# Remote candidate verification

Date: 2026-10-29. Distribution/version: novel-creator 0.1.0, provisional pending name control and release metadata. Candidate execution is authorized; publication is not authorized by that decision. The maintainer now reports PyPI account bjarkig82; pending trusted publishing is configured, the source repository is now public, and final name control/public release remain unverified.

## Superseded first candidate

- Repository: bjarkig82/novel-creator.
- Source: ed91ca48ff2ca0ecfee9aa6cf2720cffe5f9aa77.
- [Run 40881175659](https://github.com/bjarkig82/novel-creator/actions/runs/40881175659), attempt 1; artifact 12900133550, candidate-40881175659-1.
- Wheel: novel_creator-0.1.0-py3-none-any.whl, SHA-256 6a94ac9c314cabc756e74dd447225f623daff4222b4bd13e4ee6c08a222bf1ac.
- Source: novel_creator-0.1.0.tar.gz, SHA-256 a3ebf93b7af992c0c9190a10925371c22a5d597930257378a00a5512e73f7103.

The build/metadata and Linux candidate jobs passed. Linux CPython 3.13.17 on Ubuntu 26.04.1 ran 208 source tests in 40.615s, with three Windows-only skips, followed by wheel source/resource/pinned save/reopen and clean-install acceptance. Its check artifact is 12899249381. [Retained Linux result](package-init-remote-linux/candidate-check.json), [job log](package-init-remote-linux-job.txt).

Downloaded candidate bytes matched their manifest. Windows metadata and exact-source wheel verification passed; the latter checked 27 source/resource files and pinned save/reopen. [Wheel result](package-init-remote-wheel-windows.json). A separate source-distribution rebuild and clean rebuilt-wheel install passed; its verification wheel is kept outside the immutable release directory. [Build](package-init-remote-sdist-build.txt), [install](package-init-remote-sdist-install.json).

The literal PowerShell guide uncovered a missing py-launcher prerequisite. Corrected shell commands passed locally, but the shipped-guide change requires new candidate bytes. The superseded run was cancelled to release the workflow concurrency slot; its incomplete Windows job is not a pass. No publication occurred.

## Replacement candidate

[Run 40882235905](https://github.com/bjarkig82/novel-creator/actions/runs/40882235905) completed successfully against source 1d6d6632c81ca8402ff60ca05a7ec832a0dea802 on codex/package-novel-init, including the corrected Python command in the PowerShell guide. Attempt 1; artifact 12901057415, candidate-40882235905-1. Archive SHA-256 5d2dace52a0e6c333fff379c682dcfd3772807e0310c835d403c34420c38519e; expires 2026-11-28T13:29:56Z.

- Wheel novel_creator-0.1.0-py3-none-any.whl: ff1a617f55d863ccc173c416d3c0f12c75876b029056f112361f34cc911b678b.
- Source novel_creator-0.1.0.tar.gz: cd740503228a1a8feed9d9807f6b5e01b0d840100d9dda2c194f2bf153d214e2.

Windows passed all 208 source tests, exact-source wheel/pinned save/reopen and clean-install checks. Linux completed 208 source tests with three Windows-only skips, then the same wheel/clean checks. [Windows](package-init-candidate-windows.md), [Linux](package-init-candidate-linux.md). Their result artifacts are 12901132705 and 12900872945 respectively. Both clean outputs identify the approved wheel hash and no dependency inheritance. Publication/public-check jobs were skipped.

Downloaded file/manifest identity and metadata checks passed. Local byte comparison covered 27 source/resource files plus required source-archive inputs: [identity](package-init-final-remote-source.json). The remote source archive rebuilt into a separate directory and its verification wheel passed clean installed default/optional/refusal checks: [build](package-init-final-remote-sdist-build.txt), [install](package-init-final-remote-sdist-install.json). Original candidate bytes were never replaced. The corrected Windows guide command slice passed against this candidate: [guide](package-init-guide-windows.md). Native Codex host behavior is not inferred from any of these checks.

## Remaining delivery gates

Actual Codex setup/first conversational save/inspection/resume on both platforms is unverified. Literal Linux guide and all-six-category troubleshooting completion remain open. Public name control, account/publisher setup, public release documentation access and production installation are unverified. A successful candidate is not a public release, and missing gates remain unchecked.
