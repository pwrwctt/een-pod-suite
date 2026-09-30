# Regression test cases

1. Version query -> `EEN POD Suite v2.2`.
2. `Zweryfikuj jakość profilu BOCL20240903021` -> exact official lookup before QA.
3. BO title 257 chars -> OVER LIMIT by 1.
4. Short Summary 501 chars -> OVER LIMIT by 1.
5. BR/TR Technical Specification >2000 -> OVER LIMIT.
6. Six Market keywords -> OVER LIMIT by 1.
7. Empty optional Stage/IPR in BO/BR must not be an automatic blocker.
8. BR must use `product/service requested`.
