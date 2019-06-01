---
category: c++
title: libstdc++ dependencies notes
---

Imagine you have a big C++ program, such as Firefox, and you want to compile
it, link it, package it, and distribute it in binary form. You want to use a
recent version of g++ (for example, 4.6.3) because it has some nice things and
bugfixes that make your life easy as a programmer, such as better compliance to
the C++ standard. Now you ship it to your users, and some of them start
reporting error messages such as this one

```
/usr/lib/libstdc++.so.6: version `GLIBCXX_3.4.9' not found
```

What's going on? and how can you fix it?

## The g++/libstdc++ pair

You just entered a world of pain. The problem is complex, and it is due to how
g++ and the standard C++ library interact. If you start digging into this
problem, the first confusion you have to address is in terms of version
numbers, API and ABI.

libstdc++ is a library that provides a bunch of classes, routines and
templates. This set is provided to source client code in terms of an API, which
is versioned according to the changes the developers introduced in each new
release. The development team takes particular care in providing changes that
do not disrupt the API, which means that, as long as they add new things (new
classes, new routines etc) there's no problem, as long as the API is concerned:
the old API is still intact, and the new API is an extension of the old one.

When the stdc++ library is compiled with a specific compiler version, the
compiled entity now introduces another magical acronym: the ABI (application
binary interface). The ABI is decided both by how the API and the compiler
organize compiled code in the final object file. The final, compiled object you
link against provides you a set of entry points and conventions your objects
link against, against its ABI.

Every new release of g++ (for example, 4.2.0) is associated to a specific
version of libstdc++ (for 4.2.0, version number is libstdc++.so.6.0.9). Note
however, that also g++ 4.2.1 and 4.2.2 are associated to the same version of
libstdc++ 6.0.9. <a
href="http://gcc.gnu.org/onlinedocs/libstdc++/manual/abi.html">You can find the
associations at this page</a>. Given the compiler/library association, and the
fact that ABI=API+compiler, it follows that every version of libstdc++ is
associated to a specific ABI version. The ABI version is extremely important
and the core problem of the error above.

How do other projects address this issue? I did some searching, and apparently
what they do is to trick or allow the compiler not to use the problematic
symbols. I found <a href="http://glandium.org/blog/?p=1901">this post for
mozilla</a>,

In this case, <a
href="https://bug559964.bugzilla.mozilla.org/attachment.cgi?id=518130">the
patch is relatively small</a>,

## problems with libc

Unfortunately, libstdc++ is not the only problem. There's also the problem with
libc. libc.so.6 is normally a link to a specific libc library (f.ex.
lib64/libc-2.15.so) and it also has symbol versions, so if you compile against
lib64/libc-2.15.so and try to run on lib64/libc-2.9.so, it is likely it won't
work with errors like

```
/lib64/libc.so.6: version GLIBC_2.14 not found (required by ....)
```

I assumed the C library came with the compiler, but this is not the case. When
you install a new compiler, there is no new version of the C library waiting
for you.

To add to the trouble, libc works in concert with the kernel, so there is a
dependency of the compiled libc against a specific kernel version.

- <a href="http://stackoverflow.com/questions/10815453/compile-with-older-libc-version-glibc-2-14-not-found">http://stackoverflow.com/questions/10815453/compile-with-older-libc-version-glibc-2-14-not-found</a>
- <a href="http://stackoverflow.com/questions/10830650/how-do-i-fix-a-version-glibc-2-14-not-found-error">http://stackoverflow.com/questions/10830650/how-do-i-fix-a-version-glibc-2-14-not-found-error</a>
- <a href="http://stackoverflow.com/questions/8657908/deploying-yesod-to-heroku-cant-build-statically/8658468#8658468">http://stackoverflow.com/questions/8657908/deploying-yesod-to-heroku-cant-build-statically/8658468#8658468</a>
- <a href="https://github.com/yesodweb/yesod/wiki/Deploying-Yesod-Apps-to-Heroku">https://github.com/yesodweb/yesod/wiki/Deploying-Yesod-Apps-to-Heroku</a>
- <a href="http://stackoverflow.com/questions/4099013/link-to-provided-glibc">http://stackoverflow.com/questions/4099013/link-to-provided-glibc</a>
- libc does not like being linked statically (unsupported) <a
href="http://gcc.gnu.org/ml/gcc/2009-07/msg00299.html">http://gcc.gnu.org/ml/gcc/2009-07/msg00299.html</a>
- <a href="http://www.akkadia.org/drepper/no_static_linking.html">http://www.akkadia.org/drepper/no_static_linking.html</a>
- <a href="http://stackoverflow.com/questions/6941332/anticipate-kernel-too-old-errors-between-2-6-16-and-2-6-26-kernel-versions">http://stackoverflow.com/questions/6941332/anticipate-kernel-too-old-errors-between-2-6-16-and-2-6-26-kernel-versions</a>

So, how do others solve this problem? <a
href="https://bugzilla.mozilla.org/show_bug.cgi?id=526868">Mozilla apparently
hacks its code so not to trigger the inclusion of the new symbols</a>, or they
<a href="https://bugzilla.mozilla.org/show_bug.cgi?id=643690">just link dummy
routines so that the dependency is satisfied locally</a> (instead of toward the
library). <a
href="https://bug643690.bugzilla.mozilla.org/attachment.cgi?id=526012">Here you
can see an example of Mozilla implementing these strategies</a> by checking
`__GNUC__` and `__GNUC__MINOR__` (the compiler version) for preprocessing
purposes. Both these solution assume that your code is relatively self
contained and the dependencies are not hard to workaround. If you have a
complex runtime with a lot of C++ libraries, the dependencies might creep in
from the runtime, forcing you to patch not only your code, but also someone
else's code. It is also not necessarily possible to achieve complete removal of
the symbols. If, for example, you generate swig interfaces, the compiled
wrapper might depend on these symbols, and patching the swig product is close
to insanity. Occasionally, the mozilla team went as far as <a
href="https://bugzilla.mozilla.org/show_bug.cgi?id=561236">patching the stdc++
library</a>, something you can of course do only if you compile the compiler as
part of your development runtime.

The backward compatibility might, in the end, <a
href="https://bugzilla.mozilla.org/show_bug.cgi?id=561236#c2">arise from pure
luck</a>.

See also <a href="http://tldp.org/HOWTO/Program-Library-HOWTO/index.html">http://tldp.org/HOWTO/Program-Library-HOWTO/index.html</a>
