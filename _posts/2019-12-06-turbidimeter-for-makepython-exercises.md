---
category: hardware
title: Turbidimeter for MakePython exercises
---

I recently started an initiative at my local Makespace about [advanced python training](http://makepython.org). 
It has been and still is a perfect environment to keep my python fresh and introduce other makers
to the python most obscure and advanced features, as well as the surrounding environment.

In the upcoming meetings I decided to have a little hardware project. We are makespace after all,
and making things is part of the implicit deal. So I started thinking what would make for an 
easy and cheap hardware gimmick that could be both interesting and focused on a real case
problem. I spoke with a friend and we came up with the idea of a turbidimeter.

A turbidimeter is a measuring device generally used in chemical analysis. It evaluates
the amount of light that passes through liquid with partial suspension to
measure the concentration of the agent inducing the suspension. A typical scenario is
to evaluate the bacterial charge of some sludge, as a higher amount of bacteria leads to
a more turbid liquid. From the analytical point of view, the light that passes through is
partially estinguished, and there is a logarithmic relationship (the Lambert-Beer law) that correlates
concentration to light reduction. The same law is used in other spectroscopic measures such as UV/Vis.

Of course, a real turbidimeter is a nice, well behaved instrument. We want some toy that behaves like
a turbidimeter, to measure the concentration of a solution of water and milk (which is readily available
as this is Britain)

## The hardware.

All you need for a turbidimeter is:

- a box that you can close
- a light source 
- a photodetector
- a cuvette, a container that holds the liquid to analyse and defines a precise
  (relatively speaking) path length for the light to traverse.

![image]({{ site.url }}/assets/images/2019/12/IMG-20191129-WA0008.jpeg)
![image]({{ site.url }}/assets/images/2019/12/IMG-20191129-WA0010.jpeg)
![image]({{ site.url }}/assets/images/2019/12/IMG-20191206-WA0001.jpeg)


Those of the readers who know a bit about turbidimetry will have plenty of objections, but remember, it's a toy.
