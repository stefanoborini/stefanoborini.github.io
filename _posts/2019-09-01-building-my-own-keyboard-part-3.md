---
category: hardware
title: Building my own keyboard - Part 3 (in progress)
---

After the initial exploration, let's start small. The first step is to create a small 2x2 matrix 
and have arduino push out i2c data for the scan codes.

I am following the [excellent guide from the bald engineer](https://www.baldengineer.com/arduino-keyboard-matrix-tutorial.html)
and I managed to create this.

![pic](https://raw.githubusercontent.com/stefanoborini/keymine/master/pics/20190920_184318.jpg)


# Communication between the arduinos and the RasPi

To connect the two arduinos to the raspberry pi I will use I2C. It's a simple
bus that needs a very limited number of pins. By design, I2C requires that the
master is always initiating the communication, and the slave receives that
communication and optionally replies. No problem, I thought: the two arduinos
will be masters, and the RasPi a slave, and I2C supports multimaster
configuration. 

Unfortunately it's not that simple: [I opened a question on Raspberry PI](https://raspberrypi.stackexchange.com/questions/102162/i2c-communication-between-two-arduino-masters-sending-events-and-one-raspberry-p)
stackexchange, and apparently I can really only have one master. Most
importantly, [the raspberry Pi kernel does not support slave mode](https://github.com/qriozum/kernel/blob/master/Documentation/i2c/summary).
This is also confirmed [here](https://raspberrypi.stackexchange.com/questions/5584/i2c-raspberri-pi-as-a-slave).
As a result, the only option I have is the following:

- set the Raspberry Pi as master
- set the two arduinos as slaves, each on a different bus (for practical reasons).
- When a keypress is issued, the arduino firmware will
  1. trigger an interrupt line to the pi to warn that there is data to read.
  2. the pi interrupt handler sets the pi to master receive mode.
  3. the arduino uses the Wire library to send data about the keystroke, with the payload being the scan code.

This dance seems complicated, and it is, but it becomes even more complicated by the following problems:

1. the pi might be busy when the arduino is ready to send.
2. there is a time delay from when the interrupt pin is enabled to when the arduino enters slave send mode.
3. the pi might have to respond to a second interrupt while it's still in the interrupt handler (e.g. if the other half of the keyboard also wants to send a keypress)
4. the pi or the arduino might crash, hang or run out of resources.

Now, it's a keyboard, not a nuclear reactor, but still I find it interesting to
play with these kind of problems. There's a lot to learn.

In any case, my final design will be as depicted in the picture below

![schematics](https://raw.githubusercontent.com/stefanoborini/keymine/master/schematics/schema-0.1.png)

