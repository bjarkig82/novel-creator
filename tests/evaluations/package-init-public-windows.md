# Windows production installation

Date: 2026-10-29. Result: pass. [Publication run 40911698155](https://github.com/bjarkig82/novel-creator/actions/runs/40911698155), job 123581592361, succeeded after the protected deployment approved under explicit maintainer authorization.

The checked-out verifier created a fresh isolated environment without dependency inheritance, installed `novel-creator==0.1.0` by name from production PyPI with cache/local links disabled, and resolved declared dependencies. Default/name-only initialization, pinned interpreter validation, guide discovery/hash, distinct destination/title, English/Icelandic/space settings and provenance, unknown creative choices and five invalid-input refusals passed. This command verification does not claim another Codex host walkthrough; that is recorded separately in [Windows host evidence](package-init-host-guide.md).

Pip's actual selected product was `novel-creator` 0.1.0, file `novel_creator-0.1.0-py3-none-any.whl`, SHA-256 `cc8645556f74190dee9ac7527c3e66c0bc71574913b5bbae5ddff7516b8817a8`, from files.pythonhosted.org. Both public distribution hashes match the immutable candidate, not merely a separately downloaded expected file. [Original report](package-init-public-windows/public-check.json), [job log](package-init-public-windows-job.txt), [combined verification](package-init-public-verification.json).

The Windows reporting parent emitted its JSON artifact in CP1252; the installed child commands were verified as UTF-8. Original artifact bytes are retained. The [UTF-8 report view](package-init-public-windows/public-check-utf8.json) decodes CP1252 explicitly and verifies the exact Icelandic title against the Linux report; this is evidence formatting, not a product source change.
