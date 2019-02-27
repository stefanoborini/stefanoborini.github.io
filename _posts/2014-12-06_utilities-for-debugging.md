Utilities for debugging
=======================

category

:   Linux, MacOSX, Windows

Part of my daily job involves getting dirty at the assembler level,
generally to debug segfaults, FPE, deadlocks and similar stuff. It\'s a
fascinating challenge which makes me feel extremely powerful and in
control of the hard, low-level technicalities of the OS, libraries and
hardware I use. Most of my effort, however, would be impossible without
a few tools I learned to appreciate and love through hours of solid
dependency. I\'m posting them here, and while the list is certainly not
exhaustive, it\'s a starting kit for the hardcore debugger.

Linux
-----

### c++filt

This nifty utility converts C++ mangled symbols into the unmangled form.
A simple example is the following

``` {.console}
$ c++filt _ZNK3MPI4File19Get_position_sharedEv
MPI::File::Get_position_shared() const
```

More complex symbols can become unreadable in the mangled form,
especially when they arise from template instantiation. A quick pass
with `c++filt` will make everything much clearer.

### pmap

Another nifty utility in the Linux arsenal, this easy program reports
the VM layout of a running process.

``` {.console}
$ pmap  21102
21102:   cat
0000000000400000     44K r-x--  /bin/cat
000000000060a000      4K r----  /bin/cat
000000000060b000      4K rw---  /bin/cat
0000000001969000    132K rw---    [ anon ]
00007f3b98aa9000   7068K r----  /usr/lib/locale/locale-archive
00007f3b99190000   1748K r-x--  /lib/x86_64-linux-gnu/libc-2.15.so
00007f3b99345000   2048K -----  /lib/x86_64-linux-gnu/libc-2.15.so
00007f3b99545000     16K r----  /lib/x86_64-linux-gnu/libc-2.15.so
00007f3b99549000      8K rw---  /lib/x86_64-linux-gnu/libc-2.15.so
00007f3b9954b000     20K rw---    [ anon ]
00007f3b99550000    136K r-x--  /lib/x86_64-linux-gnu/ld-2.15.so
00007f3b99749000     12K rw---    [ anon ]
00007f3b99770000      8K rw---    [ anon ]
00007f3b99772000      4K r----  /lib/x86_64-linux-gnu/ld-2.15.so
00007f3b99773000      8K rw---  /lib/x86_64-linux-gnu/ld-2.15.so
00007fff18ae9000    136K rw---    [ stack ]
00007fff18bff000      4K r-x--    [ anon ]
ffffffffff600000      4K r-x--    [ anon ]
 total            11404K
```

To achieve the same with a post-mortem core file, the gdb commands
\"info files\" and \"maintenance info sections\" are your friends. When
running, \"info proc mappings\" can achieve the same.

### lddtree

`lddtree` is like `ldd`, but it traverses the full hierarchy, building a
tree diagram of all dependencies. It is available on Ubuntu in the
package pax-utils.

``` {.console}
$ lddtree /bin/ls
ls => /bin/ls (interpreter => /lib64/ld-linux-x86-64.so.2)
    libselinux.so.1 => /lib/i386-linux-gnu/libselinux.so.1
        libdl.so.2 => /lib/i386-linux-gnu/libdl.so.2
        ld-linux.so.2 => /lib/i386-linux-gnu/ld-linux.so.2
    librt.so.1 => /lib/i386-linux-gnu/librt.so.1
        libpthread.so.0 => /lib/i386-linux-gnu/libpthread.so.0
    libacl.so.1 => /lib/x86_64-linux-gnu/libacl.so.1
        libattr.so.1 => /lib/x86_64-linux-gnu/libattr.so.1
    libc.so.6 => /lib/i386-linux-gnu/libc.so.6
```

Windows
-------

I am not a Windows person, but I build and debug on it rather often.
With time, I gathered a few essential tools to understand the source of
your problems during build, deployment and execution.

### [Process monitor](http://technet.microsoft.com/en-us/sysinternals/bb896645.aspx)

Reports events of different nature from all the processes in your
system, such as disk access, registry access, and so on. I found this
utility fundamental to track a strange crash that occurred in a third
party closed-source library. The problem turned out to be an attempt to
write to a directory that was not writable. From the website:

> Process Monitor is an advanced monitoring tool for Windows that shows
> real-time file system, Registry and process/thread activity. It
> combines the features of two legacy Sysinternals utilities, Filemon
> and Regmon, and adds an extensive list of enhancements including rich
> and non-destructive filtering, comprehensive event properties such
> session IDs and user names, reliable process information, full thread
> stacks with integrated symbol support for each operation, simultaneous
> logging to a file, and much more. Its uniquely powerful features will
> make Process Monitor a core utility in your system troubleshooting and
> malware hunting toolkit.

### [Process Explorer](http://technet.microsoft.com/en-us/sysinternals/bb896653.aspx)

An equivalent of `fuser` on Linux. From the website:

> Ever wondered which program has a particular file or directory open?
> Now you can find out. Process Explorer shows you information about
> which handles and DLLs processes have opened or loaded.

### [VMMap](http://technet.microsoft.com/en-us/sysinternals/dd535533.aspx)

Extremely useful tool to see the Virtual Memory layout. It is precious
to check potential fragmentation scenarios that could lead to invalid
allocations.

From the website:

> VMMap is a process virtual and physical memory analysis utility. It
> shows a breakdown of a process\'s committed virtual memory types as
> well as the amount of physical memory (working set) assigned by the
> operating system to those types. Besides graphical representations of
> memory usage, VMMap also shows summary information and a detailed
> process memory map.

### [Dependency walker](http://www.dependencywalker.com/)

Performs more or less the task of `lddtree` on Linux and `otool` on Mac.
It\'s invaluable to figure our which libraries or symbols are
unresolved. I soon discovered that Windows is not very verbose when it
comes to unresolved dependencies at startup. From the website:

> Dependency Walker is a free utility that scans any 32-bit or 64-bit
> Windows module (exe, dll, ocx, sys, etc.) and builds a hierarchical
> tree diagram of all dependent modules. For each module found, it lists
> all the functions that are exported by that module, and which of those
> functions are actually being called by other modules. Another view
> displays the minimum set of required files, along with detailed
> information about each file including a full path to the file, base
> address, version numbers, machine type, debug information, and more.

### [Event Viewer](http://windows.microsoft.com/en-us/windows/open-event-viewer#1TC=windows-7)

Provided on a standard windows 7 installation. Another invaluable tool
to understand what\'s going on in your program, reports error and
anomalous conditions that prevent an application to start, and much
more.
