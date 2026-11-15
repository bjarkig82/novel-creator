# Immutable historical release inputs

These are public Novel Creator wheels, retained unchanged for offline historical
book compatibility tests. They are test inputs, never updater targets or rebuilt
substitutes. Fixtures verify the exact hashes before extraction.

| Version | Wheel SHA-256 | Existing release evidence |
| --- | --- | --- |
| 0.1.0 | `cc8645556f74190dee9ac7527c3e66c0bc71574913b5bbae5ddff7516b8817a8` | `tests/evaluations/package-init-release-manifest.json` |
| 0.2.0 | `9872b3aa9a4a1629d4b6c50a1672f5acbd376130f08f9c7edcd0492381c632fa` | `tests/evaluations/automatic-retrospectives-release.md` |

`historical_book(version, wheel=...)` also accepts an explicit external archive,
but it must match the same approved release digest. Tests use only disposable
repositories and existing runtime dependencies; they do not download packages,
read a real book, create credentials or contact GitHub.

The 0.10.0 and 0.10.1 public wheels are retained byte-for-byte for offline issue
setup and installed-package upgrade checks. `tests/release_fixtures.py` verifies
their pinned SHA-256 values before use; no machine-local release folder is needed.

- 0.10.0: `097e9d093424a04fdf0d50fcfbc47c3ed7fd0e6d4d081167b3a78cda497ce4d6` (public PyPI release wheel).
- 0.10.1: `6721c5a527f1b7e567743f2760ec5e13aec2d0394f520913e98589ac54b8b11a` (public PyPI release wheel).
