# Regression test cases

1. Version query -> `EEN POD Suite v2.8`.
2. Existing-profile audit with only a number/name -> request the exact detail URL; do not discover the profile.
3. BO title 257 chars -> OVER LIMIT by 1.
4. Short Summary 501 chars -> OVER LIMIT by 1.
5. BR/TR Technical Specification >2000 -> OVER LIMIT.
6. Six Market keywords -> OVER LIMIT by 1.
7. Empty optional Stage/IPR in BO/BR must not be an automatic blocker.
8. BR must use `product/service requested`.

9. Supplied detail URL -> read that page and verify the displayed POD Reference.
10. Failed detail URL read -> report failure and request an export of that same profile; never search or find another page.
11. Repeat version, drafting and exact-URL/text audit scenarios in ChatGPT, OpenCode and Claude before release; record any unavailable host checks.
12. Modify canonical unified guidance without synchronising Claude -> the build must reject the stale distribution.

13. Invalid YAML including an unquoted colon-space -> release validation rejects it.
14. HTTP 404 -> MCP tool error; no substitute profile.
15. Reference without substantive fields -> INSUFFICIENT CONTENT; partial fields -> PARTIAL CONTENT.
16. Empty required fields or unconfirmed semantic/operational/independent/form gates -> never READY.
17. Unknown/nonselectable or duplicate codes, mismatched labels and six keywords -> findings.
18. Polish semantic query -> genuine bundled codes with traceable concept reasons; unsupported concept -> no fabricated code.
19. RDR inverted/expired dates -> issue; preparation interval has no invented universal minimum.
20. Apply the host rubric in PLATFORM-EVALUATION.md and record actual runs separately from helper tests.

21. Test BO pilot length and band boundaries, distinct marketing terms, N3/P2 and N4/P3 double effects, missing vs empty data, scope and excluded tests.
22. Compare same-profile/same-model baselines, month-end follow-up and changed-model rejection.
23. Excellent does not replace the semantic audit; Poor does not automatically establish a flaggable rule violation.
24. Simulation, unverified publication and incomplete evidence never trigger operational actions.
