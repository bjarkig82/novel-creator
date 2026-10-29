# Linux guide verification

Date: 2026-10-29. Status: partial. Linux command fixtures and clean installed-package evidence are available; the full literal guide and actual Codex host walkthrough are unverified.

The superseded remote candidate's Ubuntu 26.04.1 / CPython 3.13.17 job passed source tests, exact wheel resources and clean dependency/default/optional/refusal checks. [Candidate details](package-init-candidate.md). It does not establish literal guide execution or actual Codex setup/save/resume.

The existing local WSL Python 3.12.3 environment lacks ensurepip. The guide explicitly requires pip/venv support and points to normal distribution setup when it is missing. Earlier private-pip verification was labeled supporting command evidence, not execution of the literal installation route. No system packages or Python configuration were changed to bypass this prerequisite. Final walkthroughs must use a compatible Linux environment and the replacement immutable candidate.
