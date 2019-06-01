---
category: databases
title: MySQL enumeration, strict mode and the troubles of debugging
---

Suppose you have a MySQL table containing an enum column. The
enumeration allows the values \"FOO\", \"BAR\" and \"BAZ\". This is a
production database, hooked up by a quite huge amount of programs
inserting and deleting rows into that table.

Now suppose that, for some reason, one of these programs tries to insert
the value \"HELLO\" into the enumeration column. You would expect an
error, wouldn\'t you? Unfortunately not in MySQL: when you try to insert
a value not defined in the enumeration group, it will insert instead a
special value \'\' (empty string) which is always present in any
enumeration, and associated with the index 0. You just obtain a warning.

``` {.sql}
mysql> insert into test (my_enum) values ("FOO");
Query OK, 1 row affected (0.00 sec)
```

``` {.sql}
mysql> insert into test (my_enum) values ("HELLO");
Query OK, 1 row affected, 1 warning (0.00 sec)
```

``` {.sql}
mysql> select * from test;
+---------+
| my_enum |
+---------+
| FOO     |
|         |
+---------+
2 rows in set (0.00 sec)
```

This means that you will get non-expected entries in the column (not
within your enum expected values). Moreover, you have no way of tracing
back who performed the wrong insertion, and what value he stored.
Imagine there\'s just a mistyped \"FO\" instead of \"FOO\" somewhere: it
will produce an empty column entry.

So, what can you do if you really want the enum values enforced? You
switch on Strict mode, which, unfortunately, is server wise. Not table
wise, not even database wise. It\'s server wise. Meaning that if your
server is dealing with hundreds of databases, all of them will be under
strict mode. Argh!

Glad to be proven wrong!
