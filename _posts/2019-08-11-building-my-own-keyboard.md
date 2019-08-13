---
category: hardware
title: Building my own keyboard (in progress)
---

This is a living report of my attempt to build my own keyboard. I am deeply dissatisfied
with the current offer, and I see no other way than to design my own.

Recently I joined Makespace Cambridge. It's a community workshop with a wide availability 
of tools, such as 3d printers, laser cutters, milling machines and so on. The initial motivation
was to gather python enthusiasts interested in exploring more complex topics in the language, but 
this is a story for another time. In any case, with my membership, came the need for a project, 
and I thought I never really had a pleasant experience with keyboards.

# What do I want from a keyboard?

So, what's my Ideal Keyboard (TM)? It must have

- two halves. My wrists demand it. The Kinesis Freestyle is a great model that served me well, but it has its limitations.
- No numeric keypad. It's a waste of space, I never use it, and forces me to move the hand and arm too much to reach the mouse.
- No useless keys. Enough with the caps lock, the print screen, scroll lock, pause.
- Add new keys: I program in R, so I would really love a key that sends the "<-" assignment.
- No split keys for up-down cursor. That thing is pure garbage.
- Programmable displays to show up-to-date information (e.g. build status)
- Fully programmable macro keys on the left hand side. Basically a keybow pimoroni integrated in the keyboard. 
  Bonus point if the keys also have an OLED display (but they are pricey)
- must be pleasant to use in terms of touch ergonomics, but not too noisy.
- must look cool.

# Layout

Basically, this is the layout I want 

![keyboard]({{ site.url }}/assets/images/2019/08/11/keyboard.png)

What is the size of this thing? If we assign 1U for the size of a standard button 
(approx 2 cm), the keyboard has the following sizes:

![keyboard]({{ site.url }}/assets/images/2019/08/11/units-v0.1)

Which is unfortunately incorrect, for a series of reasons:

1. Despite the breakdown of the keyboard in two halves, the total row size must be consistent. 
   In this keyboard it is 15U. Row 0 (the Esc/Fxx row) is not important. Row 1, 2, 3 (123, QWE, ASD) 
   do satisfy this requirement, but not row 4 (ZXC) and row 5, (Ctrl/Win/Alt), which counts at 14.5.
2. Between row 2 and 3 the horizontal offset between Q and A must be 0.25, and between A and Z must be 0.5.
   This is completely not satisfied in my layout.
3. keys that are used with the pinky finger need to be at least 1.25U, 
   as the hand is less accurate with those fingers. This means we can't have two 1U keys to replace 
   the caps lock (which, due to point 2 above, must be 1.75)


This means, I don't really know what to do with the caps lock. I can definitely shorten the Shift key
from the standard 2.25 to 1.25 and obtain an additional key, but for what concerns the Caps Lock the 
situation is more complicated. It must go, it's useless, but it also must be a single 1.75 key. Some 
people map Caps Lock to Esc, but I don't buy it. Moving Esc would just waste space at the top, and I
want to be muscle compatible with general QWERTY as much as possible.

In other words, I want a mix of ANSI and ISO layouts, with short shifts, horizontal Enter, and 
additional keys put to good use.

# Overall design

The two halves have 53 keys the left hand side and 52 the right hand side.
It is clear that, to drive so many switches, I will need a matrix, as there's no
chance I can have that many IO pins. This is a typical and well-established trick.
Standard matrices for keyboards are 8x16 and 8x20 for a full size keyboard. 
In my case, I have two halves, so a 8x8 matrix on each side will give me 64 keys. 
Plenty for my needs.

The idea is to have an arduino on each side scanning this matrix. These arduinos
will send messages, probably via I2C, to the brain of the operation: a raspberry pi.
Why the Pi? Because I need to drive rather complex logic to control the
displays, and the wifi. The intention is to have the display fetch, for example,
information about CI execution, so it needs to get connected to the network.

The RasPi will be hosted on one half of the keyboard, likely the left one, 
which means that I need a I2C cable to drive the right hand display, and the
arduino connected to the right hand matrix.

But let's start small. The first step is to create a small 2x2 matrix and have 
arduino push out i2c data for the scan codes.

# Bill of Materials


# PCB

I will need a custom PCB for this project, and custom PCBs are expensive.
If possible, it's 
# Links

- http://www.sprintek.com/en/products/keyboard_ic/SK5221.aspx
- https://www.toptal.com/embedded/from-the-ground-up-how-i-built-the-developers-dream-keybooard
