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

# Switches shipment

I just got the shipment of switches. I opted for Gateron as finding Cherry MX turned out to be quite hard.
As far as my experience goes, they are pretty much equivalent in quality, specs, and shape. They are also
cheaper.

The best source for Cherry MX turned out to be [this German shop](https://www.reichelt.de/Tastaturzubehoer/2/index.html?ACTION=2&LA=3&GROUPID=8099)
but I got [104 Gateron for 24 pounds](https://www.amazon.co.uk/dp/B07K7JSRWN/ref=pe_3187911_189395841_TE_3p_dp_1), which is a fourth of the price
of the equivalent Cherry MX set.

While I was looking for places where to buy switches, I also found the following shops

- https://www.switchtop.com/
- http://www.ukkeycaps.co.uk/
- https://candykeys.com


# Connecting Arduino with the Raspberry Pi

With the new matrix soldered and ready, it's now time to stress the firmware and the raspi, including the actual
transmission of data via I2C.
First, I connected the new matrix with the arduino, and the arduino with the
raspberry pi. In the image, I also added a breadboard and a logic analyser, for
reasons that will become clear in a moment

![newmatrix](https://raw.githubusercontent.com/stefanoborini/keymine/master/pics/20191012_200652.jpg)

I then modified the arduino to use the wire library and send 32 bytes of data containing the currently
pressed or released keys, with a simple encoding: the first byte is the scancode, the second is 0x00 if the button has been released
and 0x01 if it has been pressed. This is repeated for 16 times to allow for up to 16 simultaneous events.

Unfortunately, it doesn't work. I think I know why, but first let's see the behavior: occasionally, I get incorrect data
in the stream. This is pretty much guaranteed to happen when multiple keys are pressed. This picture shows what the raspberry pi 
is receiving.

![error](https://raw.githubusercontent.com/stefanoborini/keymine/master/pics/20191012_200613.jpg)

As you can see, there are occasional 0xFF (255) that are sent for no reason. Additionally, sometimes there is an array
that is all zeros 0x00. This is also not possible according to the protocol.
In order to debug the problem, first I wanted to see if that false data was actually in transit, hence the logical analyser.
It turns out that they do indeed go through the wire

![logic-i2c](https://raw.githubusercontent.com/stefanoborini/keymine/master/pics/logic-i2c.png)

So the arduino is sending it. However, I never actually populate the array with those values, and if I print them
to Serial just before they are sent out by the arduino, they are all zero. what gives?

# PCB

- wait for the PCB
- order all the parts.
- test it.

# The keycaps

- order keycaps and costar stabilizers
- edit the thingiverse spacebar
- 3d print one
- try acetone smoothing

