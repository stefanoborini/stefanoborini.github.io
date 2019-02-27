Is SVN slow?
============

date

:   2008-07-03 20:40

author

:   Stefano

category

:   Version Control

slug

:   is-svn-slow

I am using SVN to manage my current development repository. As the
project grew, the operations became slower and slower. Things like
updating or committing could require minutes.

I ran some strace, and apparently SVN takes a lot of time in walking
through the repository tree, probably checking for differences between
the previous copy (in .svn) and the current copy. Also, it walks through
the tree to remove all the lock files it created. These operations grow
with the number of subdirectories involved during the operation, so if
you don\'t want to spend your time staring at the ceiling while
committing or updating, either you keep the number of subdirs to an
acceptable low amount, or you invoke operations involving a low amount
of directories (like, committing only a subtree).

My situation is maybe quite extreme, as my repository has 2000
directories (I have lots of small applications to keep track of). I
could check out a part of the repository, or split the repository into
smaller, independent ones, but I don\'t want to risk: it could prove
potentially dangerous right now, where I have to work on other issues
with a quite tight schedule.

Despite this, I like SVN, but I am considering taking a look at
[git](http://git.or.cz/).
