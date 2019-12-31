---
category: hardware
title: Building my own keyboard - Part 7 (in progress)
---

# USB Controller and board

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

This means that I will have to redesign the board, and I will hopefully take the chance
of isolating the 3x5 part from the rest. This will give me better reuse, because I can use the
same board both on the left and on the right. I will however be careful with the wiring, because
the right part actually associates to live keys that the Holtek controller monitors, and the left part
is programmable and will stay silent until I can write the firmware to replace the Holtek.

This means that my firmware will have to be compatible with the Holtek matrix.
Not a big deal, but something to keep in mind.

# Keycaps

I ordered [2.75 spacebar keycaps](https://www.amazon.co.uk/gp/product/B07953BXY1/ref=ppx_yo_dt_b_asin_title_o03_s00?ie=UTF8&psc=1) and 
[costar stabilizers](https://www.amazon.co.uk/gp/product/B07K8FFDYJ/ref=ppx_yo_dt_b_asin_title_o03_s00?ie=UTF8&psc=1) from amazon.

# Body

I made the body out of multiple horizontal layers of green acrylic. It's a
quick and dirty solution but it is not going to be the final structure. I
decided to take a different approach and do the slicing vertically, rather than
horizontally, resulting in a lot of 3mm thick shapes that will stack side by side.
This solution gives me a lot more freedom in the final shape, but I will have
to use glue, and do a lot of polishing. I also found out that the best option for a long
setting glue is not Tensol 12, which is fast acting and good for joints, but Tensol 80, 
which is a two components glue for surfaces. 
