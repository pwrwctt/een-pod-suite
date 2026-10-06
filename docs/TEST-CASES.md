# Regression test cases

1. Version query -> `EEN POD Suite v2.3`.
2. `Zweryfikuj jakość profilu BOCL20240903021` -> exact official lookup before QA.
3. BO title 257 chars -> OVER LIMIT by 1.
4. Short Summary 501 chars -> OVER LIMIT by 1.
5. BR/TR Technical Specification >2000 -> OVER LIMIT.
6. Six Market keywords -> OVER LIMIT by 1.
7. Empty optional Stage/IPR in BO/BR must not be an automatic blocker.
8. BR must use `product/service requested`.

9. Newly published reference with no external search result -> use an actual direct official URL when supplied; do not infer unavailability.
10. HTTP 403 or unavailable proxy -> report the failed method, try available authorised recovery methods, and preserve the distinction between retrieval failure and profile absence.
