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

Basically, this is the layout I want

![keyboard]({{ site.url }}/assets/images/2019/08/11/keyboard.png)

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



# Links

- http://www.sprintek.com/en/products/keyboard_ic/SK5221.aspx
- https://www.toptal.com/embedded/from-the-ground-up-how-i-built-the-developers-dream-keybooard
