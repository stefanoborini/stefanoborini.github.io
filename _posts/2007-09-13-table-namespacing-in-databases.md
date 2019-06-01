---
category: databases
title: Table namespacing in databases
---

I was trying to find out if some database implements namespacing for
tables, but it looks like google produces no useful results for it. This
is strange. In MySQL, tables are namespaced on a \"database
qualification\" (like in dbname.tablename), but it is not possible, as
far as I am able to see, to define dbname.namespacename.tablename. This
would allow to group related tables into the same namespace, still
keeping all the tables in the same database. This feature could also be
useful during refactoring or handling of different table versions.

I wonder about the rationale behind the lack of this feature. Or maybe
the feature exists but the name is different?

As a fix for the task I am going to do, I will use underscores as
separators. This forces me to use camelcase for namespaces and table
names (eg. NameSpace\_TableName). Not a perfect solution, but at least
it documents itself.
