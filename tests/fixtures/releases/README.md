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
