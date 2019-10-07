---
category: hardware
title: Building my own keyboard - Part 5 (in progress)
---

# Baseplate and new (larger) prototype matrix

I managed to get my hands on the 1.5 mm acrylic and build a double layered 3mm thick baseplate.
It was horribly expensive, and unfortunately only available in transparent. I
say unfortunately because LEDs are no longer an option, as they would shine
through the baseplate and not illuminate precisely one key.  Aluminum is still
an option I am considering, but for now LEDs are not my top priority.

I created the baseplate by cutting two layers: the first layer as normal, and the second by 
enlarging slightly the holes for the switches. I just used the laser cutter software to do it.
Then, I used cyanoacrylate glue to stick the two layers together. This creates a 3mm sandwich that 
has lips in each switch hole. On these lips the Cherry switch locks perfectly.

The main problem with this method is that cyanoacrylate is very fast curing. I
need a slower curing glue for the bigger baseplates. The most appropriate glue
for this task seems to be [Tensol
12](https://www.amazon.co.uk/gp/product/B07G4Z1PFT/ref=ox_sc_act_title_1?smid=A1ODUIM79K8PMU&psc=1)
which has an initial setting time of 3 hours and a final setting time of 24
hours. Not perfect, but I can deal with it.

I then decided it's time to move forward to a larger matrix from the current
2x2 I have on the prototype breadboard, so I used the small baseplate, added the switches
I had laying around, a handful of 1n4148 diodes and here it is:

![newmatrix](https://raw.githubusercontent.com/stefanoborini/keymine/master/pics/IMG-20191006-WA0004.jpg)


# Connecting Arduino with the Raspberry Pi

- Use the new matrix to verify the firmware
- send actual scancodes using Wire.

# PCB

- wait for the PCB
- order all the parts.
- test it.


# The keycaps

- edit the thingiverse spacebar
- 3d print one
- try acetone smoothing

