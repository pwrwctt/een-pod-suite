# Regression test cases

1. Version query -> `EEN POD Suite v2.4`.
2. Existing-profile audit with only a number/name -> request the exact detail URL; do not discover the profile.
3. BO title 257 chars -> OVER LIMIT by 1.
4. Short Summary 501 chars -> OVER LIMIT by 1.
5. BR/TR Technical Specification >2000 -> OVER LIMIT.
6. Six Market keywords -> OVER LIMIT by 1.
7. Empty optional Stage/IPR in BO/BR must not be an automatic blocker.
8. BR must use `product/service requested`.

9. Supplied detail URL -> read that page and verify the displayed POD Reference.
10. Failed detail URL read -> report failure and request an export of that same profile; never search or scan API pages.
