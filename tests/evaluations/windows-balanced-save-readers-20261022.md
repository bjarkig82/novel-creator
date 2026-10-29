# Balanced save readers: external candidate, not adopted

2026-10-22, T149 continuation. Production remains unchanged at
`9b9092130ff0ee2768ba739cdb9ae28613010ed82b4a9eeb70bb9b342b080ffc` with serial save history/first-guard hashing and four final hash readers.
The [verified source report](windows-history-read-20261022.md) records both
138-test suites and full Windows read/save p95 1.787683800s/9.219870400s.
Reads pass; saves miss the unchanged 1s gate. Novice evaluations stay deferred.

A current ordinary-layout profile shows history/first-guard durations about
2.9–3.7s, nearly completely overlapped, and a final guard about 1.9–2.3s.
The external candidate changes only save history workers one→two and first-guard
full-byte workers one→two. Final hashing stays four. Every actual blob, metadata,
path, root, live-index, full-byte, candidate, authority, CAS and recovery check
stays active. It calls existing production implementations with alternate
parameters; production source and runtime policy are unchanged.

Eight fresh-worker complete saves, balanced ABBA/ABBA, use the full ordinary
100-session/5,000-exchange/10,000-assertion/26,215,716-byte fixture and opt-in
external private cache key. Public payload preparation remains unchanged and
outside the timer; its history is retained. Four samples per policy measure
median 5.669104200s baseline versus 4.856166300s candidate (14.34% lower).
Baseline range 4.263866800–7.429309900s; candidate range
4.512843800–5.886827900s. All saves at sequences 5001–5008
succeed without cleanup, with 25/27 Git calls. This small variable diagnostic
supports integration testing, not p95 compliance or a portable speedup claim.

Independent read-only review found no fundamental safeguard blocker, provided
all nested workers join, ordered framing/fallback remains, and first-guard
errors are observed at the original post-validation position. Before adoption,
production-path regressions must cover both two-worker policies simultaneously:
large/small/non-Windows/bootstrap/retry/public selection; malformed-history and
later worker/nonzero failure versus a failing first guard; first-guard process,
count and thread-start failures; root redirection and same-stat byte tampering;
post-first-guard edits caught by the final guard; restoration and unchanged
retry with one publication and no duplicated decisions. Retain two-worker
chunk-boundary fallback coverage. No production adoption or fresh p95 claimed.

[Raw samples](windows-balanced-save-readers-20261022.txt),
[executed source](windows-balanced-save-readers-source-20261022.txt),
[artifact hashes](windows-balanced-save-readers-manifest-20261022.json).
The diagnostic handle exited0; no provider call, commit or push occurred.
T149 stays unchecked; other host/human/language/release gates stay open.
