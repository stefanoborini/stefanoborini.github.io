---
category: python
---
Python and memory fragmentation
===============================

If you use CPython on 32 bit architectures, you may encounter a problem
called memory fragmentation. It is more likely to happen on Windows for
reasons that will soon be clear, but it\'s not a Windows exclusive. It
is also not an exclusive python problem, but tends to occur more often
on CPython due to its intrinsic memory allocation strategy.

When you dynamically allocate memory in C, you do so in a particular
area of the Virtual Memory, the heap. A requirement for this allocation
is that the allocated chunk must be contiguous in virtual memory.
CPython puts extreme stress on the heap: all objects are allocated
dynamically, and when they are freed, a hole is left in the heap. This
hole may be filled by a later allocation, if the requested memory fits
in the hole, but if it doesn\'t, the hole remains until something that
fits is requested. On Linux, you can follow the VM occupation with this
small python script

```python
import sys
import subprocess

mmap = [' ']*(16*256)
out = subprocess.check_output(["/usr/bin/pmap","-x", "%d" % int(sys.argv[1])])
for i in out.splitlines()[2:-2]:
    values = i.split()[0:2]
    start = int("0x"+values[0], 16) / 2**20
    end = start + (int(values[1])*1024)/2**20
    for p in xrange(start, end+1):
        mmap[p] = '*'

for row in xrange(16):
    print hex(row)+" | "+"".join( 
                        mmap[row * 256:(row+1)*256]
                        )+"|"
```

On Windows, the great utility
[VMMap](http://technet.microsoft.com/en-us/sysinternals/dd535533.aspx)
can be used to monitor the same information.

Given the above scenario, the Virtual Memory space can eventually become
extremely fragmented, depending on the size of your objects, their order
of allocation, if your application jumps between dynamically allocating
large chunks of memory and small python objects, and so on. As a result,
you may not be able to perform a large allocation, not because you are
out of memory, but because you are out of **contiguous** memory in your
VM address space. In a recent benchmark I performed on Windows 7, the
largest contiguous chunk of memory available was a meager 32
**megabytes** (ow!), which means that despite the free memory being
around 1 gigabyte, the biggest chunk I could request was only 32
megabytes. Anything bigger would have the malloc fail.

Additional conditions that can make the problem worse are dynamic
libraries binding and excessive threading. The first invades your VM
address space, and the second needs a stack per each thread, putting
additional unmovable barriers throughout the VM and reducing real estate
for contiguous blocks. See for example what happens with 10 threads on
Linux

``` {.text}
(gdb) thread apply all print $esp

Thread 10 (Thread 10606): $5 = (void *) 0x50d7184
Thread 9 (Thread 10607): $6 = (void *) 0x757ce90
Thread 8 (Thread 10608): $7 = (void *) 0x7b69e90
Thread 7 (Thread 10609): $8 = (void *) 0x7d6ae90
Thread 6 (Thread 10618): $9 = (void *) 0x8a4ae90
Thread 5 (Thread 10619): $10 = (void *) 0xb22fee90
Thread 4 (Thread 10620): $11 = (void *) 0xb20fde90
Thread 3 (Thread 10621): $12 = (void *) 0xb1efce90
Thread 2 (Thread 10806): $13 = (void *) 0xb2ea31c4
Thread 1 (Thread 0xb7f6b6c0 (LWP 10593)): $14 = (void *) 0xbffd1f3c
```

Fragmentation is eventually made irrelevant by a 64 bit architecture,
where the VM address space is huge (for now ;) ). Yet, if you have a 32
bit machine and a long running python process that is juggling large and
small allocations, you may eventually run out of contiguous memory and
see malloc() fail.

How to solve? I found [this interesting
article](http://www.mgroeber.de/misc/windows_heap.html) that details the
same issue and provides some mitigation techniques for Windows, because
Windows is kind of special: on Windows, the 4 gigabytes address space is
divided in two parts of 2GB EACH, the first for the process, the second
reserved for the kernel. If you must stay on 32 bits, your best bet is
to give an additional gigabyte of VM with the following recipe (only
valid for Windows-7)

1.  run `bcdedit /set IncreaseUserVa 3072` as administrator, then reboot
    the machine.
2.  mark your executable with
    `EditBin.exe yourprogram.exe /LARGEADDRESSAWARE`

With this command, the VM subdivision is set to 3GB+1GB, granting one
additional gigabyte to your process. This improves the situation, but
sometimes it\'s enough. If it is not, and you still need to work on 32
bit machines then you are in big trouble. You have to change your
allocation strategy and be smarter on handling the fragmentation within
your code.
