Upgraded my mac to SSD == pure bliss
====================================

author

:   Stefano

category

:   Hardware, MacOSX, Software

![image](http://forthescience.org/blog/wp-content/uploads/2011/02/OWC.jpg){.align-center
width="400px"}

I recently bought this 240 Gigabytes of awesomeness, conveniently packed
into a 2.5\" SATA box. It\'s an [Other World Computing Mercury Extreme
Solid State Hard
Drive](http://eshop.macsales.com/shop/internal_storage/Mercury_Extreme_SSD_Sandforce).
It has no moving parts, it consumes less battery, and it\'s fast. Damn
fast. This thing is so fast it opens applications before you lift your
finger from the touchpad after the click. It\'s also bloody expensive.

I have a MacBook 13\" unibody, the first model, also known as
MacBook5,1. The hard drive is conveniently seriviceable, right under the
large battery lid.

To perform the migration, I needed:

1.  The SSD drive, of course
2.  A smallPhillips screwdriver
3.  A small [Torx](http://en.wikipedia.org/wiki/Torx) screwdriver (I
    managed without one)
4.  A USB-to-SATA external drive case.
5.  [Carbon Copy Cloner](http://www.bombich.com/). The software is free
    but consider making a donation.

I had two or three options to perform the migration. I don\'t have the
original OSX install disk here with me (and I don\'t want to go through
a total reinstall in any case), but I did have the OSX from my iMac,
which may be useful as a safety installation if I screw up. As I quickly
learned, the iMac install DVD does not work on the MacBook, but it
allows, at least, to perform some basic operation, such as disk
partitioning.

My first attempt was based on the assumption that I had to physically
copy the partition, low level. I thought this because I wanted to
transfer the system while not active (you may have troubles), and I
didn\'t know how the boot worked, so I assumed I had to copy the
partition boot record as well\... something I did with Linux once. In
addition, moving stuff via USB takes a long time, and trasferring 160 GB
would have left me with no laptop for a while. So here was the idea:

1.  Disassemble the original disk, and put it in the external case (yes,
    Mac can boot from this disk once in USB, just press \"C\" at boot
    with the USB drive powered and no DVD disk)
2.  Put the OWC disk in the laptop. Partition in two: one with the
    original size of my old disk, the other with the remaining space
3.  Install a bare OSX on the remaining space, and start copying
    low-level from the external drive to the other partition. I thought
    to do this via \"Disk Utility\" restore.
4.  When the system is done copying, boot from the first partition,
    delete the second one (with the bare OSX) and find a way to enlarge
    the partition including the now-free space.

This turned out to be not possible, because the OSX DVD I have does not
allow me to install. I could, however, still use this process, using
Disk Utility from the DVD, which runs. I tried with no luck, as Disk
Utility complains about not being able to allocate memory. In addition,
I could no longer boot from USB after this event. The reason was not
clear. To address this event, I restored the original disk into the
laptop, and proceeded with a different strategy, which is the one I did.

The successful strategy
-----------------------

### 1. Preparing the new disk

I booted my system back with the old disk, and put the OWC SSD in the
USB enclosure. It was clear I had to transfer the system while live, so
I logged in with a new bare account with admin privileges, instead of my
own. This allows not to have active files or mounted FileVaults, which
could give trouble.

I plugged in the SSD in the enclosure, created and formatted a single,
whole partition with Disk Utility, exactly in the same format as my
system partition. Check in either Disk Utility or from the command line,
with the command \"diskutil info /dev/disk0s2\". It should be Journaled
HFS+, because it\'s the one that allows boot. **DO NOT enable
case-sensitive**. You will have a lot of troubles, in particular with
File Vault, (yes, [workarounds exist, but I haven\'t tried
them](http://www.frederico-araujo.com/2008/11/04/getting-filevault-on-a-hfs-case-sensitive-filesystem/)).
I loathe case-preserving/case-insensitive FileSystems, but Mac works
this way. Also check to use Partition Type \"GUID\_partition\_scheme\"
when partitioning.

### 2. Copying the system

Once formatted, I started Carbon Copy Cloner, specified the source as my
system disk, the target as the SSD disk, and ticked \"backup
everything\". The documentation in Carbon Copy Cloner is perfect. Check
also the \"typical usage cases\" shown there, you will find the one you
need. Make sure Carbon Copy Cloner tells you the cloned system partition
will be bootable.

### 3. Swapping the disks

Carbon Copy Cloner will copy your whole system to the external disk,
something that may take many hours. Let it go. When done, I turned off
the computer, flipped it, and opened the battery lid. There\'s a small
Phillips screw keeping the hard drive in place via a simple plastic
brace. I unscrewed this brace and took it away, then pivoted the hard
drive to lift it and unplugged the SATA cable (gently).

Now, I disassembled the SSD drive from the external casing. On the sides
of the old hard drive there are four small Torx screws that provide
support. The plastic brace kept two of these screws pushed down, while
the other two allowed for the pivoting on the side of the battery
compartment. I had to remove these screws to put them in the SSD drive,
but since I didn\'t have a Torx screwdriver, I resorted to pliers both
for removing them and putting them on. I then plugged in the SATA cable
in the SSD, put the disk in the compartment, screwed the brace back and
tried to run the laptop with the new setup. Note: conventional wisdom
says \"first test, then close\", but in this case the
assembly/disassembly was so trivial I preferred to put everything back
in. Also, the battery does not stay in its place without the lid, so you
have to close it anyway, or put the battery aside for a while.

### 4. Booting the new disk

The boot was smooth and uneventful. Not really as fast as I expected,
but notably faster. The real difference is in launching applications and
logging in. It used to take 10-15 seconds to get to work. Now I have the
desktop open in just 2 seconds.

### 5. Conclusion

I now have the old hard drive and an external USB-SATA case. I could
format it and use it as an external disk, or keep it as a safety backup
system. I decided for the latter.
