---
category: hardware
title: Building my own keyboard - Part 2 (in progress)
---

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

I could bring out the big guns: one Atmega2560 to serve both keyboard sides.
The problem is, however, that we'll need to send 16 wires to the other side,
plus the power, ground, a wire for the neopixels. Additional wires may be
needed to drive the LCD.  let's say 20 wires. That's a lot of copper, and
that's a thick cable, so this is also not a solution. The Atmega is also quite
big, and I would have to make my own PCB (which is not a big deal) and solder the 
Atmel (impossible).

Keyboard controllers such as the
[SK5221](http://www.sprintek.com/en/products/keyboard_ic/SK5221.aspx) handle
8x16 or 8x20 matrixes, driving up to 160 buttons with 28 pins. Unfortunately, I
could not find any place where these controllers can actually be bought.
I could use the [HT82K628A](https://www.holtek.com/productdetail/-/vg/82k628a) but I am not
sure how I would then convert the data out into an I2C transmission.

For now, I'll use the Atmega2560 (I already have one). Later I'll have to find
a cheaper, better alternative.

# PCB

I will need a custom PCB for this project, and custom PCBs are expensive.
If possible, it's 

# Links

- https://www.toptal.com/embedded/from-the-ground-up-how-i-built-the-developers-dream-keybooard

