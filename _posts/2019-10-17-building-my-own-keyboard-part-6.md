---
category: hardware
title: Building my own keyboard - Part 6 (in progress)
---

# Baseplate 

I laser cut the complete baseplate. Laser files provided. Link.

screwed the screw space. Need rework.

To verify the strength of the Tensol 12 bond, I applied a small amount on two scrap strips of acrylic.
I let them cure for 24 hours, and then tried to separate them. It was much stronger than I could even remotely
think. I tried to shear separate them by using pliers and pulling in opposite directions with the help of another person.
The acrylic snapped first

![tensol](https://raw.githubusercontent.com/stefanoborini/keymine/master/pics/20191019_174234.jpg)

So it is safe to say that tensol 12 is indeed an excellent bonding agent for acrylic, and
it's perfectly transparent too.  Unfortunately, I also realised that the actual
time from application to solid is in the order of 15-20 seconds, not hours as I
believed. Longer than cyanoacrylate, but still very small to allow for proper
gluing and setting of the two halves of the baseplate. My first attempt was far
from perfect, as you will see soon, but I will come up with a solution for
rapid application at a later stage.

- create new baseplate and design the screw setup


# PCB

Soldering the PCB components took me a whole day, but I found myself strangely absorbed at the zen-like activity of soldering
with a microscope. I thought it was much harder, but with a steady hand, a good technique with the solder, iron, and tweezers,
and some good tune, I managed to solder all the diodes and the kailh hot-plugs.

![first-pair](https://raw.githubusercontent.com/stefanoborini/keymine/master/pics/20191019_130412.jpg)

It is of particular importance to keep close attention to the diode directionality, indicated by a small yellow band.
Keep into account that these diodes are the size of a sesame seed, and the contacts are the size of a grain of sand.

![diode](https://raw.githubusercontent.com/stefanoborini/keymine/master/pics/20191019_130540.jpg)

The final result is very pleasing:

![solder-complete](https://raw.githubusercontent.com/stefanoborini/keymine/master/pics/20191019_172654.jpg)

That said, I doubt I will use the kailh hot-plugs in the final model. They were
hard to find, and they provide little advantage for the final product, besides
the ability to replace a switch easily. But seriously, I don't think I'll ever
replace switches in the finished model. I do however want to keep this option
for the current prototypes, so I can reuse the switches in later prototypes and
finished product. The result is that I will have to rework the final PCB to
just provide through-hole solder pads for the switches.

After adding the baseplate and the switches, it's now time to do the final assembly of
the left side prototype:

![final-left-side](https://raw.githubusercontent.com/stefanoborini/keymine/master/pics/20191023_200650.jpg)

Note how the baseplate tensol application was far from perfect, but despite this I am pleased with the result.

# Debugging arduino/raspi connection woes

I realised I have made a pretty large whoopsie with the connection. I am not
sure if this is the source of my current issues with the I2C, but it certainly
needs fixing. The arduino mega2560 is operating at 5 volts. The raspberry pi at
3.3v, and its pins are _not_ 5v resistant.  There's a chance that I might have
destroyed the raspberry pi GPIO, so I decided to replace it, and add a level shifter
in between.



- check kernel i2c driver.

# The keycaps

Ordered keycaps from [the keyboard company](http://keyboardco.com), the only
company based in the UK with a reasonable set of keys. I ordered two sets: one
with US layout, and the other with blank keycaps. 


- keep searching 3u spacebar DCS.
- search the DCS keycaps for the rest of the keyboard.
- order keycaps and costar stabilizers
- refine acetone process

