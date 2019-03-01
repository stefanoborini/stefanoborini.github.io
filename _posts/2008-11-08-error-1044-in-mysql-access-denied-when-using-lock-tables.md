---
category: databases
---
Error 1044 in MySQL: Access denied when using LOCK TABLES
=========================================================

I got an error while using mysqldump

```
*mysqldump: Got error: 1044: Access denied for user x\@y to database z
when using LOCK TABLES*
```

To solve this problem, either ask you administrator to grant you the
lock privileges, or use the following command instead.

```
mysqldump -u username -p database --single-transaction >dump.sql
```

This is the help entry for the keyword

```
    --single-transaction
              Creates a consistent snapshot by dumping all tables in a
              single transaction. Works ONLY for tables stored in
              storage engines which support multiversioning (currently
              only InnoDB does); the dump is NOT guaranteed to be
              consistent for other storage engines. While a
              --single-transaction dump is in process, to ensure a
              valid dump file (correct table contents and binary log
              position), no other connection should use the following
              statements: ALTER TABLE, DROP TABLE, RENAME TABLE,
              TRUNCATE TABLE, as consistent snapshot is not isolated
              from them. Option automatically turns off --lock-tables.
```
