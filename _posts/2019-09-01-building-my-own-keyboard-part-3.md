---
category: hardware
title: Building my own keyboard - Part 3 (in progress)
---

After the initial exploration, let's start small. The first step is to create a small 2x2 matrix 
and have arduino push out i2c data for the scan codes.

I am following the [excellent guide from the bald engineer](https://www.baldengineer.com/arduino-keyboard-matrix-tutorial.html)
and I managed to create this.

# Communication between the arduinos and the RasPi

To connect the two arduinos to the raspberry pi I will use I2C. It's a simple
bus that needs a very limited number of pins. By design, I2C requires that the
master is always initiating the communication, and the slave receives that
communication and optionally replies. For this reason, the two arduinos will be
masters, and the RasPi a slave.  This is not a problem because I2C supports
multimaster configuration. I suspect we will never need arduino to arduino
communication, but in any case there will be a single I2C bus connecting all
three devices.

When a keypress is issued, the arduino firmware will use the Wire library to
send the scan code to the raspberry pi.
