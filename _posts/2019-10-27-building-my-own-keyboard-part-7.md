---
category: hardware
title: Building my own keyboard - Part 7 (in progress)
---

# USB Controller

I decided to put the firmware on hold for a while and just rely on
the Holtek chip. It's a single solution and while I won't be able to achieve
what I want in the long run, I can starte designing other things and get a functional
keyboard quickly. I designed the PCB, ordered the components, and soldered them

![image](https://raw.githubusercontent.com/stefanoborini/keymine/master/pcb/PCB_holtek-v1_20191115214619.png)

This first iteration of the board does not connect all pins, but the routing was quite challenging and
I stayed simple for now. The bill of material required mostly passive components that are easily
available, a USB connector, a board connector, and a 6MHz oscillator.

![image](https://raw.githubusercontent.com/stefanoborini/keymine/master/pics/20191208_125910.jpg)

And... it works. Sort of. The problem is that when I designed the matrix connection in my keyboard,
I didn't consider the Holtek chip yet, and I did not plan to comply woth any matrix other than my own
preference. But by using the Holtek, I need a PCB for the matrix that respects what the chip expects.
This is in the [Datasheet](http://www.farnell.com/datasheets/79209.pdf) ad it's kind of odd.

You can see the consequences of this odd wiring in this video I made

<iframe width="560" height="315" src="https://www.youtube.com/embed/UdCWe9osWNg" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

# Keycaps

I ordered 2.75 spacebar keycaps and costar stabilizers. 

# Body


- create new baseplate and design the screw setup
- keep searching 3u spacebar DCS.
- search the DCS keycaps for the rest of the keyboard.

- USB vendor and product id?

[USB specifications](https://www.beyondlogic.org/usbnutshell/usb1.shtml)

