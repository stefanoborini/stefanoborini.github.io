New gcc linker behavior leaves me puzzled
=========================================

Today, together with a colleague, I found out this interesting behavior
of the GNU linker. Suppose you define the following trivial (and
incorrect, but who cares) program

``` {.c}
int main() {}
```

if you link it and specify a library (say, libm) it does not depend on,
the final executable does not depend on that library. This is a good
thing, because there\'s no point in having a dependency against a
library if you don\'t use any part of it.

``` {.console}
sbo@NAS:~$ gcc test.c -o test -lm
sbo@NAS:~$ ldd test
    linux-vdso.so.1 =>  (0x00007fff673ff000)
    libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007ff5cc6a4000)
    /lib64/ld-linux-x86-64.so.2 (0x00007ff5cca83000)
```

This was not always the case. In old versions of the linker the result
would have been

``` {.console}
linux-vdso.so.1 =>  (0x00007fff317bc000)
libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007fb5d9d13000)
libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007fb5d9953000)
/lib64/ld-linux-x86-64.so.2 (0x00007fb5da02e000)
```

occasionally resulting in spurious dependencies. The linker would have
added an entry to the ELF dynamic section, regardless of the actual need
for that library.

``` {.console}
sbo@NAS:~$ readelf --dynamic test

Dynamic section at offset 0xe40 contains 21 entries:
  Tag        Type                         Name/Value
 0x0000000000000001 (NEEDED)             Shared library: [libm.so.6]
 0x0000000000000001 (NEEDED)             Shared library: [libc.so.6]
```

To prevent the addition of libraries when no symbols from those
libraries are actually used, a flag \--as-needed was introduced to the
linker. It wasn\'t enabled by default, but in gcc 4.6 it is. In gcc 4.2
it was not. One can always restore the old behavior by issuing
\--no-as-needed

``` {.console}
gcc test.c -o test -Wl,--no-as-needed -lm
```
