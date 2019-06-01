---
category: python
title: A Raytracer in Python - Part 2 - Rendering Multiple Objects
---

A quick addition needed to the raytracer is providing freedom to add
more objects to the rendering scene. In Part 1, the design was such that
only one object, a sphere, could be drawn. The new code allows much more
flexibility. I added a Plane object, introduced assignment of colors to
the objects, divided the source into multiple files, and fixed a bug
relative to rendering direction. Let\'s see more specifically.

The class World is the main interface to user programming of the
raytracer. This small program creates and renders a scene containing
four spheres, a white one in the origin, the others along the axes, each
with different colors.

```python
import raytrace
from raytrace import objects

w=raytrace.World()
w.add_object(objects.Sphere(center=(0.0,0.0,0.0),
                            radius=10.0,
                            color=(1.0,1.0,1.0)
                           )
            )
w.add_object(objects.Sphere(center=(50.0,0.0,0.0),
                            radius=10.0,
                            color=(1.0,0.0,0.0)
                           )
            )
w.add_object(objects.Sphere(center=(0.0,50.0,0.0),
                            radius=10.0,
                            color=(0.0,1.0,0.0)
                           )
            )
w.add_object(objects.Sphere(center=(0.0,0.0,50.0),
                            radius=10.0,
                            color=(0.0,0.0,1.0)
                            )
            )
w.render()
```

The resulting image is the following

![image]({{ site.url }}/assets/images/2011/05/render1.png)

Clearly, the white sphere is not visible, as it\'s hidden by the blue
sphere. This test allowed me to discover a problem with orientation: the
green sphere was on the wrong side. I therefore had to analyze a bit the
orientation and the different coordinate systems into play here

1.  The measure of the screen is given in pixels. We are used to this
    when it comes to screen size, for example. An image which is 320x200
    means that it\'s 320 pixels wide (horizontal resolution) and 200
    pixel high (vertical resolution). Don\'t fall into \"thinking
    matrix\", where NxM means N rows x M columns. It is the exact
    opposite.
2.  The geometry uses the cartesian system, which has the origin in the
    center of the picture. The x axis is oriented towards the right, the
    y axis towards the top, and the z axis towards the observer. This is
    not different from a traditional cartesian layout: for the z=0
    plane, the top left pixel correspond to a (-,+) coordinate, the
    bottom right to a (+,-) coordinate. Points closer to the observer
    have positive z, honoring the [right hand
    system](http://en.wikipedia.org/wiki/Right-hand_rule). The camera in
    the above picture is at z=+100.0
3.  The raytracer uses pixel coordinates for the viewplane. Pixel 0,0 is
    at the bottom left. Changing the first index moves horizontally
    (along the row) from left to right. Changing the second index moves
    vertically (along the column) from bottom to top. As a consequence,
    the point at the bottom right is (hres-1,0), and at the top left is
    (o, vres-1). Note that this is equivalent to a cartesian (x,y)
    system with origin on the bottom left corner. Not a surprise, since
    there is a direct mapping between the pixels and the rays\' origins.
4.  Finally, the pixel image indexing of pygame and PIL. For them, pixel
    0,0 is top left. Like the case above, incrementing the first index
    also moves along the row from left to right. However, incrementing
    the second index moves vertically from top to bottom, which is the
    opposite of the raytracing index. Bottom left is (0, vres-1) and the
    bottom right is (hres-1, vres-1).

A remapping is therefore needed from the pixel coordinate of the
rendering and the pixel coordinate of the display (e.g. pygame). The
transformation is trivial, of course, but it must be kept into account,
otherwise pics will be flipped horizontally.

Another interesting fact is that, according to \"Ray Tracing from the
ground up\" it\'s useful to perform the raytracing operation starting
from the bottom and working our way up, rendering pixels from left to
right. According to them this is for coding symmetry and future
convenience, so we stick to it.

Finding the foremost object
---------------------------

In the book, finding the foremost object is made more complex by the
language used, C++. In python, you can use functional programming style
to obtain the same in a very concise statement. The idea is to cast a
ray, then go through all objects in the world to find the intersection
point (if any) between the ray and the object. If more than one object
is hit, the one with the intersection point closer to the observer
commands the pixel color, since it\'s in front.

I achieve this with the following code

```python
def hit_bare_bones_object(self,ray):
   def f(o):
     shadeRec = o.hit(ray)
     if shadeRec:
       return (shadeRec.parameter, o)
     else:
       return None

   try:
     foremost=sorted( \
                filter(lambda x: x is not None, \
                  map(f, self.objects)
                ), key=lambda x: x[0]
              )[0][1]
   except IndexError:
     return None

   return foremost
```

What does this code do ? I defined a simple internal function f which
accepts an object, performs the hit and returns a tuple containing the
hit point position (as a parameter of the ray, so it\'s a single number,
not a xyz coordinate) and the object.

Now, I use this function to map all the objects defined in the world. I
will obtain a list with one entry per each object, either a None (not
hit) or a 2-tuple containing the parameter and the hit object. I filter
out the None entries, leaving only the 2-tuples and then sort according
to their first element. The 2-tuple with the lowest parameter is now at
index 0, and the \[1\] element of this tuple is the foremost object. At
any time, the list may be empty (such as if you don\'t have any object,
or no object is hit. In that case, a IndexError will be raised and that
will indicate that the ray hit nothing. I may rework on this function
later on, but for this second round, it suits my needs.

It\'s now time to move on to samplers. Given that the code is growing in
size, [I created a git repository you can clone from](https://github.com/stefanoborini/python-raytrace). 
The [release of this post is available here](https://github.com/stefanoborini/python-raytrace/tree/74521b39d6ebba01b7446b7353c9a7868407513b).
The code is under BSD license.
