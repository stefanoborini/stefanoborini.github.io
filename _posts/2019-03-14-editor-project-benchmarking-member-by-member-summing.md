---
category: python
---
# Editor project: benchmarking member-by-member summing

Recently I introduced classes for VRect, VPoint and VSize, to mirror Qt
classes, and replaced all usages of tuples with these classes. Unfortunately,
the code became really, really slow. I expected reduced speed, but not so much
to compromise refresh. I am aware that my refresh strategy can be improved, but
I decided to investigate really how slow the different strategies are. Here is
the code


```
import time
import collections

a=time.time()

b=(2,3)
for i in range(1000000):
    c = (1,1)
    b = (b[0]+c[0], b[1]+c[1])
print("Tuples "+str(time.time()-a-0.07))

############
class C:
    def __init__(self, x,y):
        self._pos = (x,y)
    def __add__(self, other):
        return C(self._pos[0]+other._pos[0], self._pos[1]+other._pos[1])

a=time.time()
b=C(2,3)
for i in range(1000000):
    b = b + C(1,1)
print("Class "+str(time.time()-a-0.07))

#####################
T=collections.namedtuple('T',("x", "y"))

a=time.time()
b=T(2,3)

for i in range(1000000):
    c = T(1,1)
    b = T(b.x+c.x, b.y+c.y)
print("namedtuple "+str(time.time()-a-0.07))

#####################
T=collections.namedtuple('T',("x", "y"))

a=time.time()
b=T(2,3)
for i in range(1000000):
    c = T(1,1)
    b = T(b[0]+c[0], b[0]+c[0])
print("namedtuple index "+str(time.time()-a-0.07))
```

The 0.07 seconds is the time for the empty loop. The results are astonishing

```
$ python3 test.py
Tuples 0.723123960494995
Class 4.2343959140777585
namedtuple 3.7144619750976564
namedtuple index 2.9126908111572267
```

Working with raw tuples beats every other technique hands down. It's quite
clear now why my code has become so sluggish. I won't trash the concept, but I
will definitely not use the high level classes for internal operations.
Unfortunately this has a price in self-documentation: I definitely prefer to
use point.x() or instead of point[0]. An obvious mitigating strategy is to use
a constant to get point[X_INDEX].

