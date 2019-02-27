Doing nothing in bash
=====================

date

:   2007-09-22 06:41

author

:   Stefano

category

:   Bash

slug

:   doing-nothing-in-bash

Today I had to \"do nothing\" in bash. In python you have \"pass\" for
this task. In C, you can use \";\". I found [this
post](http://ynniv.com/blog/2005/04/doing-nothing-in-bash.html) from
someone having the same issue. He proposes either \"sleep 0\" or
\"A=0\". However, looks like this is even nicer: from the bash manual

> : \[arguments\]
>
> :   No effect; the command does nothing beyond expanding arguments and
>     performing any specified redirections. A zero exit code is
>     returned.
>
So, a simple \":\" will do the trick.
