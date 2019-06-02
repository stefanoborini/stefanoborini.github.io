---
category: c
title: The magic numbers of reboot()
---

Today I learned an interesting piece of Linux trivia. To reboot the
machine, there\'s a system call, reboot(). The funny thing is in its
signature

```c
int reboot(int magic, int magic2, int cmd, void *arg);
```

Of course this routine can only be called by uid 0 (root), but you also
need to pass two \"magic numbers\" for the call to actually work. Why?

Imagine a rogue process with uid 0 gets to screw up and jump at a random
location, and this location happens to be the location of reboot(). It
would trigger a reboot, something rather unpleasant. To prevent this,
magic numbers provide an additional safety net. It\'s unlikely that the
rogue program jumps \_[and]() has the proper magic numbers in the stack
or the registers.

The [comment in the kernel confirm
this](http://lxr.free-electrons.com/source/kernel/reboot.c?v=3.13)

```c
192 * Reboot system call: for obvious reasons only root may call it,
193 * and even root needs to set up some magic numbers in the registers
194 * so that some mistake won't make this reboot the whole machine.
195 * You can also set the meaning of the ctrl-alt-del-key here.
196 *
197 * reboot doesn't sync: do that yourself before calling this.
198 */
```

Another interesting trivia is that the magic2 numbers have a special
meaning. In hex, they are the [birthdates of Torvalds and his
daughters](http://www.nndb.com/people/444/000022378/).

```c
#define LINUX_REBOOT_MAGIC1 0xfee1dead
#define LINUX_REBOOT_MAGIC2 672274793   // 0x28121969
#define LINUX_REBOOT_MAGIC2A 85072278   // 0x05121996
#define LINUX_REBOOT_MAGIC2B 369367448  // 0x16041998
#define LINUX_REBOOT_MAGIC2C 537993216  // 0x20112000
```

Any of these values will be accepted to initiate a reboot

```c
210 /* For safety, we require "magic" arguments. */
211 if (magic1 != LINUX_REBOOT_MAGIC1 ||
212         (magic2 != LINUX_REBOOT_MAGIC2 &
213          magic2 != LINUX_REBOOT_MAGIC2A &
214          magic2 != LINUX_REBOOT_MAGIC2B &
215          magic2 != LINUX_REBOOT_MAGIC2C))
216 return -EINVAL;
```
