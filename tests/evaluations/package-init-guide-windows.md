# Windows guide verification

Date: 2026-10-29. Status: partial; candidate-bound shell walkthrough and actual Codex continuation remain separate checks.

The literal installation block first failed at `py -3 -m venv` because this Python-equipped Windows environment has no `py` launcher. [Initial output](package-init-guide-windows-initial.txt) retains that failure. The guide was corrected to use `python -m venv`, check its version and allow a full interpreter path.

The corrected command route was exercised in a new temporary root with a disposable process-scoped Git identity. Its only acquisition substitution was the verified prepublication wheel, as allowed by the guide's release-status note; explicit executable paths followed the documented activation alternative. Default `My Novel`, context/session/inspection commands, separate destination/title/Icelandic example and interpreter verification succeeded. [Command output](package-init-guide-windows-commands.txt).

This preliminary run consumed artifact 12900133550 from run 40881175659/attempt 1, source ed91ca48ff2ca0ecfee9aa6cf2720cffe5f9aa77; wheel SHA-256 6a94ac9c314cabc756e74dd447225f623daff4222b4bd13e4ee6c08a222bf1ac. It establishes the corrected shell command behavior, not the corrected guide's packaged identity. A replacement candidate is required because the guide changed. No actual fresh Codex conversation, native input capture, first conversational save or resume was performed. All-six-category troubleshooting completion and final candidate binding remain open.
