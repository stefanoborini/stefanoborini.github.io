---
category: hardware
title: Building my own keyboard - Part 2
---

# Overall design

The two halves have 53 keys the left hand side and 52 the right hand side.
It is clear that, to drive so many switches, I will need a matrix, as there's no
chance I can have that many IO pins. This is a [typical and well-established trick](https://www.baldengineer.com/arduino-keyboard-matrix-tutorial.html).
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

# The arduino

To control a 8x8 matrix I will need 16 pins. Plus, I will need some pins to
speak I2C.  Additionally, I really want to have independent RGB LEDs under each
key, so we'll also need one cable to drive neopixels.

An arduino micro has 18 digital pins (including the analog ones that can go digital):
D2-13, A0-5. (A6 and A7 can't go digital according to the docs). For I2C,
Arduino uses A4 and A5. This leaves D2-13 and A0-3, for a total of 16 pins.
Just what I need for the matrix, but not for the LEDs.  I could reduce the
matrix to 8x7 (which would still be able to handle all buttons) freeing one
cable for the LEDs, but it feels really constrained. 

Therefore, I could bring out the big guns: tge Atmega2560. 
Initially I thought one Atmega2560 to serve both keyboard sides.
The problem is, however, that we'll need to send 16 wires to the other side,
plus the power, ground, a wire for the neopixels. Additional wires may be
needed to drive the LCD.  let's say 20 wires. That's a lot of copper, and
that's a thick cable, so this is also not a solution. The Atmega is also quite
big, and I would have to make my own PCB (which is not a big deal) and solder the 
Atmel (close to impossible but I might learn).

Keyboard controllers such as the
[SK5221](http://www.sprintek.com/en/products/keyboard_ic/SK5221.aspx) handle
8x16 or 8x20 matrixes, driving up to 160 buttons with 28 pins. Unfortunately, I
could not find any place where these controllers can actually be bought.
I could use the [HT82K628A](https://www.holtek.com/productdetail/-/vg/82k628a) but I am not
sure how I would then convert the data out into an I2C transmission.

So I decided to overengineer the hell out of this thing: one Atmega2560 per each side.

# PCB

I will need a custom PCB for this project, and custom PCBs are expensive.
Why custom? Because I am not using a standard layout. The vast majority of self-made
keyboards out there use standard layouts, or, in some cases, they use the ortholinear layout.
Not my thing. 

So, yeah, I will make my own PCB, and it will be an adventure in itself.

# Baseplate 

The baseplate is another issue. Cherry type keys need to lock into position,
and to do so, they need a baseplate. This plate must be 1.5 mm thick to lock
the key. I initially thought of using Acrylic, but 1.5 mm acrylic is very
bendy. I will create an initial prototype using acrylic as I have the laser
cutter for it, but in the end I will have to use aluminium and ask for a
professional cut.

One possibility is that the acrylic might be enough, as the split keyboard is
shorter and thus the plate won't bend that much. I am also planning to use hot
swap key contacts, so any stress on the key won't end up breaking the solder.

# Links

Here are a few links that gave me some relevant knowledge:

- https://www.toptal.com/embedded/from-the-ground-up-how-i-built-the-developers-dream-keybooard
- https://lcsc.com
- https://jlcpcb.com
- https://docs.qmk.fm
- https://ultimatehackingkeyboard.com/layout-and-keycaps

