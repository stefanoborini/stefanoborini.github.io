A raytracer in python - part 1: basic functionality
===================================================

Some time ago I visited Sydney, and I made a tragic mistake: I entered
the University bookshop. Why a mistake, you say? I am book maniac. As
soon as I enter a book shop (live or on web) I end up spending up to a
thousands euro every time. This time, it was not the credit card, but
the limit of 20 kg on my luggage to put a limit on what I could buy.
Needless to say I got really good stuff, in particular this 761 pages of
pure awesomeness: [\"Ray tracing from the ground
up\"](http://www.amazon.com/Ray-Tracing-Ground-Kevin-Suffern/dp/1568812728).
This book teaches you how to write a raytracer, step by step from a
first basic skeleton to incredibly complex optic effects. It also
provides code, available for download under GPL. I haven\'t downloaded
it, but according to the book it\'s in C++. Since I want to keep myself
fresh with python, I will write my own version in this language.

The first objection I may hear is performance. Native python is much
slower than C++. I agree, and I do it on purpose. My objective is in
fact not only to write a raytracer for fun (and the world is full of
[already awesome
raytracers](http://en.wikipedia.org/wiki/List_of_ray_tracing_software)),
but also to perform some infrequent python exercises: interfacing with
C, parallelization and, hopefully, some OpenCL programming. This is my
hope, at least. I will try to spend some time on it and see how far I
can get.

What is raytracing and how does it work ?
-----------------------------------------

Raytracing is a technique to produce a photorealistic image. It works by
projecting rays from the observer to the scene, and coloring pixels on a
viewplane for every ray that intersects an object.

![image](http://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Ray_trace_diagram.svg/500px-Ray_trace_diagram.svg.png){.align-center
width="400px"}

This mechanism resembles how vision works, although in the opposite
direction. Light rays from a lamp hit objects and their reflection
happens to scatter around. Some of these reflections will enter our eyes
and allow us to see the world around us. Doing the opposite, tracing
from the observer, is clearly more efficient as we don\'t care about the
rays not hitting the observer (at least in its basic implementation),
only those who do.

Performing raytracing (or to be more accurate, for now just its basic
form [raycasting](http://en.wikipedia.org/wiki/Ray_casting)) involves
the following steps:

1.  define a geometric object in space, like for example a sphere
2.  define a view panel made of pixels
3.  shoot one straight line (ray) from the center of each pixel
4.  if the ray intersects the object, mark the pixel colored, otherwise
    mark it with the background color

That\'s it. Basically, it\'s an exercise in geometry: finding
intersections between lines and 3D objects in 3D space. This first
program,
[ray.py](http://forthescience.org/blog/wp-content/uploads/2011/05/ray.py_.txt),
does exactly that. You will need to install the Python Imaging Library,
pygame and numpy. The result is intriguing:

![image](http://forthescience.org/blog/wp-content/uploads/2011/05/render.png){.align-center
width="400px"}

Ok, I have a very loose definition of \"intriguing\", but it\'s a start.
