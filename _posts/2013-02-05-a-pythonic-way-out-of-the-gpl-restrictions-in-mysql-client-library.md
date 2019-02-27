A pythonic way out of the GPL restrictions in MySQL client library
==================================================================

I recently became aware of this native Python package
[PyMySQL](https://github.com/petehunt/PyMySQL). The package has one
important benefit vs. the other solutions to talk to a MySQL server,
such as MySQLdb (AKA
[mysql-python](http://sourceforge.net/projects/mysql-python/)) , namely,
it reimplements the MySQL protocol, instead of binding to the MySQL
connector library (also known as libmysqlclient). Why is this an issue?
Well, because the MySQL connector library is GPL, and you can\'t bind
against GPL code unless your code is under a GPL-compatible license.
This excludes all commercial uses, and makes all derivative works of
libmysqlclient GPL as well, including the Python binding MySQLdb. If you
thought about circumventing the problem using
[unixodbc](http://www.unixodbc.org/), tough luck: the ODBC MySQL
connector is also GPL, thus making unixodbc GPL as well.

Despite the low version number, PyMySQL, seems to be working, has no
dependencies, it\'s pure python, and it is released under the very
liberal MIT license.
