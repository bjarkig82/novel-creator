# English/Icelandic evidence

Structural tests preserve English and Icelandic titles, Þ/þ/Ð/ð and exact source
text, explicit unknowns and language tags including is-IS. Context selects en.md
or is.md using the configured primary tag without changing the manuscript setting.
Shared instructions honor explicit interaction-language requests and mixed input.

Paired authored acceptance and continuity fixtures share IDs, selected proposition
expectations and revision cases. They include speculation, negative acceptance,
quoted dialogue, ambiguous references, partial selection and intentional narrative
techniques. Their translations and literary judgments have not received human
semantic review or actual product host execution. These are prepared test inputs,
not proof of bilingual parity. T055/T059/T060 and T120 remain incomplete where
meaning, false-friend coverage or actual host evidence is required.

## Authored pitfall corpus continuation — 2026-10-21

Added eight paired [English](../fixtures/en/language-pitfalls.json) and
[Icelandic](../fixtures/is/language-pitfalls.json) inputs covering setup, guidance,
capture, acceptance and continuity. Cases distinguish eventúellt/possibly from
eventually, gift/married from an English present, and gas/gaseous fuel from petrol.
Mixed-language requests cover manuscript versus interaction language, fewer
suggestions, topic changes and partial acceptance; quoted dialogue and negation
must not establish author truth. Expected source quotes and Unicode code-point
spans are explicit. These are authored expectations, not observed host outcomes.

An agent review identified two existing translation mismatches: English brass
seal was rendered as copper seal in Icelandic A07/O01. Both now use
látúnsinnsigli, and A07's source span was updated. This is an agent assessment;
no fluent human review or actual product-host execution is claimed.

New fixture contracts check unique/matching IDs, outcome and selected-proposition
parity, revision expectations, all six continuity categories/intervention rules,
workflow/challenge coverage and exact source quote ranges. The initial run found
the absent pitfall corpus; after authoring it, the fixture and existing portability
contracts pass **six tests on Windows and six on Linux/WSL2**, zero skips/errors.
See [Windows log](windows-language-fixture-tests.txt) and
[Linux log](linux-language-fixture-tests.txt). These checks cannot judge translation
meaning or literary significance. No production code or dependency changed;
full host/human/bilingual tasks T055/T060/T130 remain open.

Focused command on both platforms: `python -B -m unittest
tests.contract.test_language_fixtures tests.contract.test_portability -v`.
Windows used `.venv/Scripts/python.exe` with PYTHONUTF8=1. Linux used the existing
Python 3.12.3 WSL environment with PYTHONPATH=src and UTF-8/bytecode-disabled
execution against this checkout. No dependencies were installed or updated.

Installed source and resources operate without importing the framework's product
modules in an isolated interpreter. This establishes local portability of the
tested paths, not Linux/macOS or spoken-output support.
