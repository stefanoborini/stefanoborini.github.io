Change MySQL config file
========================

date

:   2008-01-28 09:54

author

:   Stefano

category

:   MySQL

slug

:   change-mysql-config-file

It seems trivial, and indeed it is, to specify a different configuration
file for the mysql client, from the standard .my.cnf to a different
file. This is generally needed when you don\'t want the password to be
visible in the process list, but at the same time you don\'t want to use
the standard .my.cnf file.

Despite trivial, I was not able to understand which option was the
correct one, and for some strange reason Google didn\'t help, so this
post is mainly to fix this issue.

So basically you can specify a different file with the option
`--defaults-file=filename`. You can alternatively add the file to the
list with the option `--defaults-extra-file=filename`. In the latter
case, the file will not take precedence on already existent my.cnf
files.
