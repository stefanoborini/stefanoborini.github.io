Global includes
===============

author

:   Stefano

category

:   Computer Science

Sometimes in my programmer career I did this mistake: a big global
header file that gets included by most, if not all the files in my
project. This file normally contains one or more of the following:
global variables, general defines or enums, other includes. I have also
found this mistake in other\'s codes as well, when I had to maintain or
change these codes.

The apparent advantages of this approach are:

-   You have a central, unique place where to look for global variables,
    and they are instantly accessible just by including the this header
    file.
-   You save typing, because by having `global.h` include other files,
    you save the need to specify these files explicitly every time.
-   You have application-wide settings clearly partitioned and
    accessible.

The main reasons why I consider this practice a mistake are three. First
of all, with a global include file, all the files in the project gain a
dependency toward this file. This dependency is related only to the
layout of the code, not on the conceptual entities you are working with
and how they interact in your design. If the language is compiled, this
potentially leads to an application-wide recompile when the `global.h`
is changed, even for those files that are not actively dependent on the
part that changed. If the language is interpreted, you slow down the
execution because you are potentially parsing sections of the code that
are not used for the invoked task.

The second problem is that if you are using the global include to
further include other headers, so to make your typing life easier (by
including all of them with a single `#include <global.h>`), you are
effectively making your future maintainer life more difficult: you lose
information about what is really used by the code and what is not.
Compare for example:

``` {.c}
globals.h:

#include <foo.h>
#include <bar.h>
#include <baz.h>

file.c:

#include <global.h>

<other code using only foo.h>
```

With the more communicative

``` {.c}
file.c:

#include <foo.h>

<other code using only foo.h>
```

In the second example, `bar.h` and `baz.h` are not included. This
explicitly states to a maintainer that `file.c` only uses `foo.h`, an
information that was more complex to devise in the first example, in
particular if the code is complex and no namespacing is used. This
highly simplifies many refactorings and code auditing.

Finally, the global file tends to become a catch-all for the bad
practice of global variables, mainly with the justification of keeping
consistency. Instead, the file keeps becoming more complex and difficult
to maintain as many conceptually unrelated entities are aggregated.

A situation where a global include is instead useful is when you develop
a library. The global include makes the library interface available.
This is fine, because in general a library user needs to import the
interface as a whole, or eventually a conceptually whole subpart of it.
Check out, for example, `#include <gl/gl.h>` and `#include <gl/glut.h>`
in openGL.

References:

-   [If (global header files are bad) then
    ...?](http://groups.google.com/group/microsoft.public.vc.mfc/browse_thread/thread/f522d2e61e2acfd6/d71a6fad505053a2)
-   [global header
    file](http://groups.google.com/group/microsoft.public.vc.mfc/browse_thread/thread/91ecec41f230d7de/69eb355fe2513253)
