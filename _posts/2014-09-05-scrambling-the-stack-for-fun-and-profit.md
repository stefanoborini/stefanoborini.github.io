Scrambling the stack for fun and profit
=======================================

author

:   Stefano

category

:   C/C++

tags

:   

Like any good respected tinkerer, I sometimes like to play with the
madness and intricacies of the hardware and software I use. Recently I
was tracing problems in a software I won\'t name but whose objective is
to prevent tampering attempts, and while dumping stacks and
disassembling routines, I came around this very interesting backtrace

``` {.text}
#0  0x0000003f95e0d654 in __lll_lock_wait () from /lib64/libpthread.so.0
#1  0x0000003f95e08f65 in _L_lock_1127 () from /lib64/libpthread.so.0
#2  0x0000003f95e08e63 in pthread_mutex_lock () from /lib64/libpthread.so.0
#3  0x00002b67cbdeaded in ?? ()
#4  0x000000002d0e9608 in ?? ()
#5  0x00002b67cbd1e1f2 in ?? ()
#6  0x000000000000000b in ?? ()
#7  0x00002aaaca08e410 in ?? ()
#8  0x00002aaab405d558 in ?? ()
#9  0x00002aaaadf65f48 in ?? ()
#10 0x00002aaaadf65fa0 in ?? ()
#11 0x00002aaaadf65fc0 in ?? ()
#12 0x00002aaaadf65f40 in ?? ()
#13 0x00002aaaadf65f50 in ?? ()
#14 0x000000002d0e7460 in ?? ()
#15 0x0000000026014330 in ?? ()
#16 0x00002b67cc1d08b0 in ?? ()
```

Interesting, I said to myself. I had no idea why I didn\'t have any
backtrace information. What\'s interesting is that the addresses
appeared to be incorrect, or not pointing to any code section. Note for
example \#6. I hardly doubt that\'s a correct address. I had no idea why
this happened.

Nevertheless, I eventually found what I was looking for and moved on to
other things, but the weird stack remained in the back of my head. Could
it be that the stack has been scrambled on purpose? Maybe\... or maybe
the library was just stripped? Then why the weird address at frame
\#6? I still don\'t know, but the idea of scrambling the stack was
appealing. So I wrote this trivial program as a proof of concept, just
for fun

``` {.c}
#include <stdio.h>

int routine4() {
    printf("hello\n");
}
int routine3() {
    routine4();
}
int routine2() {
    routine3();
}
int routine1() {
    routine2();
}
int main() {
    routine1();
}
```

then I compiled it with a simple g++ file.cpp, set a breakpoint on
routine4, ran it, and asked for a backtrace

``` {.text}
#0  0x0000000100000e18 in routine4 ()
#1  0x0000000100000e2f in routine3 ()
#2  0x0000000100000e3a in routine2 ()
#3  0x0000000100000e45 in routine1 ()
#4  0x0000000100000e50 in main ()
```

Pretty nice backtrace. We see the full information and all routine
names. If we disassemble routine4, we also see the printf, which is
actually reworked into a puts on OSX 10.6.8 with gcc.

``` {.text}
0x0000000100000e14 <_z8routine4v +0>:    push   %rbp
0x0000000100000e15 <_z8routine4v +1>:    mov    %rsp,%rbp
0x0000000100000e18 <_z8routine4v +4>:    lea    0x45(%rip),%rdi        # 0x100000e64
0x0000000100000e1f <_z8routine4v +11>:   callq  0x100000e5e <dyld_stub_puts>
0x0000000100000e24 <_z8routine4v +16>:   leaveq 
0x0000000100000e25 <_z8routine4v +17>:   retq
```

If I instead strip the binary with strip a.out, I can\'t set a
breakpoint on routine4 anymore, and rightly so

``` {.text}
(gdb) break routine4
Function "routine4" not defined.
Make breakpoint pending on future shared library load? (y or [n]) n
(gdb) break puts
Breakpoint 1 at 0x3126e978c12ef0
```

Thanks to strip, all symbols are gone and the debugger can only refer to
addresses. I can only guess (but not a hard one) where the code is, by
checking at which VM pages they are mapped to, and the entry point

``` {.text}
(gdb) info file
Symbols from "/Users/sbo/tmp/a.out".
Mac OS X executable:
   /Users/sbo/tmp/a.out, file type mach-o-le.
   Entry point: 0x0000000100000dd8
   0x0000000100000000 - 0x0000000100001000 is LC_SEGMENT.__TEXT in /Users/sbo/tmp/a.out
   0x0000000100000dd8 - 0x0000000100000e57 is LC_SEGMENT.__TEXT.__text in /Users/sbo/tmp/a.out
```

In any case, with the breakpoint at puts I can get to the printf and
issue a backtrace to get to our infamous condition

``` {.text}
#0  0x00007fff86eb0ef0 in puts ()
#1  0x0000000100000e24 in ?? ()
#2  0x0000000100000e2f in ?? ()
#3  0x0000000100000e3a in ?? ()
#4  0x0000000100000e45 in ?? ()
#5  0x0000000100000e50 in ?? ()
#6  0x0000000100000e0c in ?? ()
```

Yet, as you can see, the stack makes sense. I cannot disassemble, but at
least I can dump the contents and they make sense

``` {.text}
(gdb) disas 0x0000000100000e24
No function contains specified address.
(gdb) x/30i  0x0000000100000e24
0x100000e24: leaveq 
0x100000e25: retq   
0x100000e26: push   %rbp
0x100000e27: mov    %rsp,%rbp
0x100000e2a: callq  0x100000e14
0x100000e2f: leaveq 
0x100000e30: retq   
0x100000e31: push   %rbp
0x100000e32: mov    %rsp,%rbp
0x100000e35: callq  0x100000e26
0x100000e3a: leaveq 
0x100000e3b: retq   
0x100000e3c: push   %rbp
0x100000e3d: mov    %rsp,%rbp
0x100000e40: callq  0x100000e31
0x100000e45: leaveq 
0x100000e46: retq   
0x100000e47: push   %rbp
0x100000e48: mov    %rsp,%rbp
0x100000e4b: callq  0x100000e3c
0x100000e50: mov    $0x0,%eax
0x100000e55: leaveq 
0x100000e56: retq
```

In fact, you can see the whole shebang. All the calls of the routines,
the stack pointer changes, and the final setting to zero of eax when
main ends.

Scrambling the return address
-----------------------------

Here is the idea: Instead of [smashing the
stack](http://insecure.org/stf/smashstack.html), I will try to scramble
it. What does it mean? Well, let\'s see how the stack is when we are
just about to be calling puts. We select the previous frame

``` {.text}
(gdb) frame 1
#1  0x0000000100000e24 in ?? ()
```

Get the stack pointer at the current frame

``` {.text}
(gdb) info registers
...snip...
rbp            0x7fff5fbff680    0x7fff5fbff680
rsp            0x7fff5fbff680    0x7fff5fbff680
...snip...
```

Then we take a look at what is in there

``` {.text}
(gdb) x/10a 0x7fff5fbff680
0x7fff5fbff680:  0x7fff5fbff690  0x100000e2f
0x7fff5fbff690:  0x7fff5fbff6a0  0x100000e3a
0x7fff5fbff6a0:  0x7fff5fbff6b0  0x100000e45
0x7fff5fbff6b0:  0x7fff5fbff6c0  0x100000e50
0x7fff5fbff6c0:  0x7fff5fbff6d8  0x100000e0c
(gdb) bt
#0  0x00007fff86eb0ef0 in puts ()
#1  0x0000000100000e24 in ?? ()
#2  0x0000000100000e2f in ?? ()
#3  0x0000000100000e3a in ?? ()
#4  0x0000000100000e45 in ?? ()
#5  0x0000000100000e50 in ?? ()
#6  0x0000000100000e0c in ?? ()
```

Nothing unusual, it\'s simply the stack pointer and the return address,
traditional stack contents for a routine call. When the routine returns,
the old return address will be restored to the rip, and the program will
continue where it left off, at the routine call. If we were to change
this address in the stack, the program would jump to a different
location, and that would be bad and likely lead to a crash. Note however
that, in order for the stack to unwind correctly, only the frame below
the current one is needed, and it\'s needed just before the return
occurs.

So, we can technically scramble all the stack, set those addresses to
something else and completely break the backtrace even of a non-stripped
binary, provided that we restore the frame under the current one just
before returning. The process will be:

> 1.  Inside every routine, we will drop at the assembly level and write
>     a prologue section where we alter the underlying frame\'s return
>     address.
> 2.  We do our thing inside the routine
> 3.  Again at the assembly level, we write an epilogue section where we
>     restore the return address, just before issuing the return that
>     needs it.

With this strategy in place, if you break anywhere inside the function
all the frames (except the one your code is currently in) will be
\"scrambled\" and pointing at nonsensical memory areas. Despite the
completely trashed stack, the program will behave correctly because when
those addresses will be needed at return, the right address has been
restored just a few instructions earlier. Let\'s see:

``` {.c}
int routine4() {
    asm("mov 8(%rsp), %rbx"); 
    asm("lea 0xdeeead(,%rbx,), %rbx");
    asm("mov %rbx, 8(%rsp)");
    printf("hello\n");
    asm("mov 8(%rsp), %rbx");
    asm("lea -0xdeeead(,%rbx,), %rbx");
    asm("mov %rbx, 8(%rsp)");
}
```

I altered the routine to perform the prologue and the epilogue. In the
prologue, I extract the content of the stack pointer plus 8, which
happens to be the return address. I put this value in rbx as it seems to
be unused. Then, with lea, I add a fixed offset (oxdeeead) to the
content of rbx. Finally, I write this value back in the stack at %rsp+8.
In the epilogue, I simply perform the opposite operation, subtracting
0xdeeead and restoring the correct return address in the stack. If I
compile and run, the program works correctly.

The gdb session is really nice

``` {.text}
Breakpoint 1, 0x0000000100000df4 in routine4 ()
(gdb) bt
#0  0x0000000100000df4 in routine4 ()
#1  0x0000000100000e2f in routine3 ()
#2  0x0000000100000e3a in routine2 ()
#3  0x0000000100000e45 in routine1 ()
#4  0x0000000100000e50 in main ()
```

Note how the stack is correct, as we haven\'t executed the prologue yet.

``` {.text}
(gdb) disas

Dump of assembler code for function _Z8routine4v:
0x0000000100000df0 <_z8routine4v +0>:    push   %rbp
0x0000000100000df1 <_z8routine4v +1>:    mov    %rsp,%rbp
0x0000000100000df4 <_z8routine4v +4>:    mov    0x8(%rsp),%rbx           # prologue 
0x0000000100000df9 <_z8routine4v +9>:    lea    0xdeeead(,%rbx,1),%rbx   # prologue
0x0000000100000e01 <_z8routine4v +17>:   mov    %rbx,0x8(%rsp)           # prologue
0x0000000100000e06 <_z8routine4v +22>:   lea    0x57(%rip),%rdi          # 0x100000e64
0x0000000100000e0d <_z8routine4v +29>:   callq  0x100000e5e <dyld_stub_puts>
0x0000000100000e12 <_z8routine4v +34>:   mov    0x8(%rsp),%rbx           # epilogue         
0x0000000100000e17 <_z8routine4v +39>:   lea    -0xdeeead(,%rbx,1),%rbx  # epilogue
0x0000000100000e1f <_z8routine4v +47>:   mov    %rbx,0x8(%rsp)           # epilogue
0x0000000100000e24 <_z8routine4v +52>:   leaveq  
0x0000000100000e25 <_z8routine4v +53>:   retq   
End of assembler dump.
```

The current situation looks like this

``` {.text}
(gdb) info register
rbx            0x0   0
rsp            0x7fff5fbff680    0x7fff5fbff680
(gdb) x/10a 0x7fff5fbff680
0x7fff5fbff680:  0x7fff5fbff690  0x100000e2f <_z8routine3v +9>
0x7fff5fbff690:  0x7fff5fbff6a0  0x100000e3a <_z8routine2v +9>
0x7fff5fbff6a0:  0x7fff5fbff6b0  0x100000e45 <_z8routine1v +9>
0x7fff5fbff6b0:  0x7fff5fbff6c0  0x100000e50
```

Stepping instruction after instruction, we can follow the events: first
the rbx register is filled with the return address from the stack

``` {.text}
-> mov    0x8(%rsp),%rbx
(gdb) info register rbx 
rbx 0x100000e2f 4294970927
```

Then, we add `0xdeeead`

``` {.text}
-> lea    0xdeeead(,%rbx,1),%rbx
(gdb) info register rbx
rbx            0x100defcdc   4309581020
```

and finally, we store it back into the stack

``` {.text}
-> mov    %rbx,0x8(%rsp)           # prologue
(gdb) x/10a 0x7fff5fbff680
0x7fff5fbff680:  0x7fff5fbff690  0x100defcdc
0x7fff5fbff690:  0x7fff5fbff6a0  0x100000e3a <_z8routine2v +9>
0x7fff5fbff6a0:  0x7fff5fbff6b0  0x100000e45 <_z8routine1v +9>
0x7fff5fbff6b0:  0x7fff5fbff6c0  0x100000e50
```

Et voila\'. The backtrace is now pointing to neverland

``` {.text}
(gdb) bt
#0  0x0000000100000e06 in routine4 ()
#1  0x0000000100defcdc in ?? ()
#2  0x0000000100000e3a in routine2 ()
#3  0x0000000100000e45 in routine1 ()
#4  0x0000000100000e50 in main ()
```

If we were to return now, a segfault would occur: that return address is
completely invalid. It\'s only by performing the reverse operation that
we can land safely back into `routine3`

``` {.text}
-> mov    0x8(%rsp),%rbx
rbx            0x100defcdc
-> lea    -0xdeeead(,%rbx,1),%rbx  
rbx            0x100000e2f   
-> mov    %rbx,0x8(%rsp)         
Stack 0x7fff5fbff680:    0x7fff5fbff690  0x100000e2f <_z8routine3v +9>
```

Now the backtrace is sane again and we are ready to return

``` {.text}
(gdb) bt
#0  0x0000000100000e24 in routine4 ()
#1  0x0000000100000e2f in routine3 ()
#2  0x0000000100000e3a in routine2 ()
#3  0x0000000100000e45 in routine1 ()
#4  0x0000000100000e50 in main ()
```

Now that we can reliably alter the stack frame, we can apply the same
trick to our complete call hierarchy. Here is the full code:

``` {.c}
#include <stdio.h>

#define scramble() asm("mov 8(%rsp), %rbx"); \
                    asm("lea 0xdead(,%rbx,), %rbx"); \
                    asm("mov %rbx, 8(%rsp)")

#define unscramble() asm("mov 8(%rsp), %rbx"); \
                     asm("lea -0xdead(,%rbx,), %rbx"); \
                     asm("mov %rbx, 8(%rsp)")
int routine4() {
    scramble();
    printf("hello\n");
    unscramble();
}
int routine3() {
    scramble();
    routine4();
    unscramble();
}
int routine2() {
    scramble();
    routine3();
    unscramble();
}
int routine1() {
    scramble();
    routine2();
    unscramble();
}
int main() {
    scramble();
    routine1();
    unscramble();
}
```

If you compile it, it runs

``` {.text}
sbo@sbos-macbook:~/tmp$ g++ test.cpp 
sbo@sbos-macbook:~/tmp$ ./a.out 
hello
```

and if you debug it, break at puts, and backtrace, here is the funny
result

``` {.text}
(gdb) bt
#0  0x00007fff86eb0ef0 in puts ()
#1  0x0000000100000d82 in routine4 ()
#2  0x0000000100defc5e in ?? ()
#3  0x0000000100defc8d in ?? ()
#4  0x0000000100defcbc in ?? ()
#5  0x0000000100defceb in ?? ()
#6  0x0000000100defc05 in ?? ()
(gdb) x/10a 0x0000000100defc8d
0x100defc8d: Cannot access memory at address 0x100defc8d
(gdb) disas 0x0000000100defc8d
No function contains specified address.
(gdb) cont
Continuing.
hello

Program exited normally.
```

Now you can get creative. For example, you can

> -   Scramble your frames according to a random number that you seed
>     differently at every new run.
> -   Scramble the whole frame content, not only the return address
> -   Spread out preamble and epilogue throughout the routine code, so
>     that it\'s harder to find out which opcode is devoted to actual
>     execution, and which one is unscrambling the frame, maybe through
>     tortuous operations full of indirections.

Of course, this stuff is extremely hard to do correctly. You have to
keep into account that some stack content could be needed by callees, so
you may have to unscramble any frame content at any time. It can also
quickly turn into a portability nightmare, as different compilers may
have different strategies to fill the stack with local variables.

Yet, it was fun, and I hope you enjoyed it.
