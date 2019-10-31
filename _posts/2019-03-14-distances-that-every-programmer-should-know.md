---
category: other
title: Distances that every programmer should know
---

A few days ago, I remembered about a famous collection of 
[numbers that every programmer should know](http://highscalability.com/numbers-everyone-should-know)
about timing of typical computer operations. I realized it would be
interesting to see how much light travels during these times. Without
further ado, here is the table:

```
Operation                              Time              Distance
---------                              ----              --------
3.3 GHz CPU Cycle                      0.3 ns            9 cm
L1 cache reference                     0.5 ns            15 cm
Branch mispredict                      5 ns              1.5 m
L2 cache reference                     7 ns              2.1 m
Mutex lock/unlock                      100 ns            30 m
Main memory reference                  100 ns            30 m
Compress 1K bytes with Zippy           10,000 ns         3 km
Send 2K bytes over 1 Gbps network      20,000 ns         6 km
Read 1 MB sequentially from memory     250,000 ns        75 km
Round trip within same datacenter      500,000 ns        150 km
Disk seek                              10,000,000 ns     3000 km
Read 1 MB sequentially from disk       30,000,000 ns     9000 km
Send packet CA-Netherlands-CA          150,000,000 ns    45000 km
```

This table shows interesting things for latency. It gives an idea of how 
incredibly fast are processors today in executing one instruction: a [Laser
Range Finder](http://en.wikipedia.org/wiki/Laser_rangefinder) using "time of
flight" is able to shoot a bunch of photons, and physically measure the time it
takes for these photons to bounce and come back. In fact, even a simple
[arduino](http://forum.arduino.cc/index.php?topic=110549.0) can count fast
enough to measure distances with a time of flight approach.
