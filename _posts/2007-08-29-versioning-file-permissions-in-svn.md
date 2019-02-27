Versioning file permissions in svn
==================================

date

:   2007-08-29 08:32

author

:   Stefano

category

:   Computer Science

slug

:   versioning-file-permissions-in-svn

There can be cases when it\'s important to version file permissions. One
case I have at hand is to have a cache directory for automatically
generated images in a web application. The cache must be open for
writing by the webserver, because the images are generated via a PHP
script.

Unfortunately, subversion does not perform versioning of the file
permissions. As a result, when the cache directory is checked out, the
permissions are restricted to the user who checks out, and the webserver
cannot write content in the cache. There are some solutions to this
problem:

1.  create a script that has to be run every time the tree is freshly
    checked out. The script checks the permission of critical
    directories and files, and put them correct. Advantages: quick to
    implement. Disadvantages: easy to forget, must be maintained for
    changes.
2.  Use the [asvn
    wrapper](http://svn.collab.net/repos/svn/trunk/contrib/client-side/asvn)
    to enhance subversion so that it can handle permissions via
    properties. Advantages: cleaner approach. Disadvantages: apparently
    none.
3.  Let the webserver user check out the tree. Advantages: conceptually
    simple. Disadvantages: You have to have access to the webserver
    user, and if a security flaw is available, the webserver can
    potentially alter any file or write in any directory.

I\'m sure there are other solutions, but I\'m not aware of them at the
moment. My personal choice is for the first solution, mainly because I
don\'t want to bring asvn into the system right now. The script scales
appropriately for my current needs.
