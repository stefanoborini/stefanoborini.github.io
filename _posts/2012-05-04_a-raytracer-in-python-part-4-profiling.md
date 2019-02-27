A raytracer in python -- part 4: profiling
==========================================

author

:   Stefano

category

:   Python, Raytracing

After having finally obtained a raytracer which produces antialiasing,
it is now time to take a look at performance. We already saw some
numbers in the last post. Rendering a 200x200 image with 16 samples per
pixels (a grand total of 640.000 rays) takes definitely too much. I want
to perform some profiling with python, find the hotspots in the code,
and eventually devise a strategy to optimize them.

General profiling with cProfile
-------------------------------

To perform basic profiling, I used the cProfile program provided in the
standard library. It appears that the longest processing time is in the
hit() function

``` {.text}
$ python -m cProfile -s time test3.py
 Ordered by: internal time

 ncalls  tottime  percall  cumtime  percall filename:lineno(function)
 2560000  85.329    0.000  108.486    0.000 Sphere.py:12(hit)
 1960020  30.157    0.000   30.157    0.000 {numpy.core.multiarray.array}
 7680000  23.115    0.000   23.115    0.000 {numpy.core._dotblas.dot}
 1        19.589   19.589  195.476  195.476 World.py:25(render)
 2560000   7.968    0.000  116.454    0.000 World.py:62(f)
 640000    6.710    0.000  133.563    0.000 World.py:61(hit_bare_bones_object)
 640025    4.438    0.000  120.902    0.000 {map}
 640000    3.347    0.000  136.910    0.000 Tracer.py:5(trace_ray)
 640000    3.009    0.000    3.009    0.000 {numpy.core.multiarray.zeros}
 640000    2.596    0.000    2.613    0.000 {sorted}
 640000    2.502    0.000    3.347    0.000 {filter}
 640000    1.835    0.000   16.784    0.000 Ray.py:4(__init__)
```

This does not surprise me, as the main computation a raytracer performs
is to test each ray for intersection on the objects in the scene, in
this case multiple Sphere objects.

Profiling line by line for hot spots
------------------------------------

Understood that most of the time is spent into hit(), I wanted to
perform line-by-line profiling. This is not possible with the standard
python cProfile module, therefore I searched and found an alternative,
[line\_profiler](http://packages.python.org/line_profiler/):

``` {.console}
$ easy_install-2.7 --prefix=$HOME line_profiler
$ kernprof.py -l test3.py
Wrote profile results to test3.py.lprof
$ python -m line_profiler test3.py.lprof
```

Before running the commands above, I added the \@profile decorator to
the method I am interested in. This decorator is added by line\_profiler
to the \_\_builtin\_\_ module, so no explicit import statement is
needed.

``` {.python}
class Sphere(object):
    <..>
    @profile
    def hit(self, ray):
         <..>
```

The results of this profiling are

``` {.text}
Line # Hits  Time    Per Hit  % Time Line Contents
==============================================================
12                                   @profile
13                                   def hit(self, ray):
14 2560000  27956358  10.9     19.2     temp = ray.origin - self.center
15 2560000  17944912   7.0     12.3     a = numpy.dot(ray.direction, ray.direction)
16 2560000  24132737   9.4     16.5     b = 2.0 * numpy.dot(temp, ray.direction)
17 2560000  37113811  14.5     25.4     c = numpy.dot(temp, temp) \
                                              - self.radius * self.radius
18 2560000  20808930   8.1     14.3     disc = b * b - 4.0 * a * c
19
20 2560000  10963318   4.3      7.5     if (disc < 0.0):
21 2539908   5403624   2.1      3.7         return None
22                                      else:
23   20092     75076   3.7      0.1         e = math.sqrt(disc)
24   20092    104950   5.2      0.1         denom = 2.0 * a
25   20092    115956   5.8      0.1         t = (-b - e) / denom
26   20092     83382   4.2      0.1         if (t > 1.0e-7):
27   20092    525272  26.1      0.4            normal = (temp + t * ray.direction)\
                                                           / self.radius
28   20092    333879  16.6      0.2            hit_point = ray.origin + t * \
                                                              ray.direction
29   20092    299494  14.9      0.2            return ShadeRecord.ShadeRecord(
                                                         normal=normal,
                                                         hit_point=hit_point,
                                                         parameter=t,
                                                         color=self.color)
```

Therefore, it appears that most of the time is spent in this chunk of
code:

``` {.python}
temp = ray.origin - self.center
a = numpy.dot(ray.direction, ray.direction)
b = 2.0 * numpy.dot(temp, ray.direction)
c = numpy.dot(temp, temp) - self.radius * self.radius
disc = b * b - 4.0 * a * c
```

We cannot really optimize much. We could precompute self.radius \*
self.radius, but it does not really have an impact. Something we can
observe is the huge amount of routine calls. Is the routine call
overhead relevant ? Maybe: [Python has a relevant call
overhead](http://wiki.python.org/moin/PythonSpeed/PerformanceTips#Data_Aggregation),
but a very simple program like this

``` {.python}
def main():
    def f():
        return 0
    a=0
    for i in xrange(2560000):
        if f():
            a = a+1

    print a

main()
```

is going to take 0.6 seconds, not small, but definitely not as huge as
the numbers we see. Why is that ? And why is the raytracer so slow for
the same task ? I think the bottleneck is somewhere else.

Finding the problem
-------------------

I decided to profile World.render() to understand what\'s going on: this
is the routine in charge of going through the pixels, shooting the rays,
then delegating the task of finding intersections to Tracer.trace\_ray,
which in turns re-delegates the task to World.hit\_bare\_bone\_object. I
don\'t really like this design, but I stick to the book as much as
possible, mostly because I don\'t know how things will become later on.

The profiling showed two hot spots in World.render(), in the inner loop:

``` {.text}
Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================

    41    640000     18786192     29.4     29.2  ray = Ray.Ray(origin = origin,
                                                               direction = (0.0,0.0,-1.0))
    42
    43    640000     22414265     35.0     34.9  color += numpy.array(tracer.trace_ray(ray))
```

Why is it so slow to perform these two operations? It turns out that
[numpy is incredibly slow at creating
arrays](http://stackoverflow.com/questions/6559463/why-is-numpy-array-so-slow).
This may indeed be the reason why it\'s so slow to instantiate a Ray
object (two numpy.arrays), to add the color (another instantiation) and
to perform operations in the Sphere.hit slow lines. At this point I\'m
not sure I can trust numpy.array, and I decide to remove it completely
replacing arrays with tuples. The result is pleasing

``` {.text}
$ time python test3.py
real    0m31.215s
user    0m29.923s
sys 0m2.355s
```

This is an important point: tuples are much faster than small arrays.
numpy seems to be optimized for large datasets and performs poorly when
handling small ones. This includes not only the creation of the arrays,
but also any operation in numpy that may create numpy arrays as a
consequence, such as calling numpy.dot on two tuples instead of a
trivial implementation such as

``` {.python}
def dot(a,b):
    return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
```

in fact, if I use numpy.dot on tuples in Sphere.hit():

``` {.python}
a = numpy.dot(ray.direction, ray.direction)
b = 2.0 * numpy.dot(temp, ray.direction)
c = numpy.dot(temp, temp) - self.radius * self.radius
```

the total running time goes from 31 seconds to a staggering 316 seconds
(5 minutes). My guess is that they are converted to numpy.arrays
internally, followed by the actual vector-vector operation.

I call myself happy with a runtime of 30 seconds for now, and plan to
optimize further when more complex operations are performed. You can
find the [version for this post at
github](https://github.com/stefanoborini/python-raytrace/commit/2cb6e2b31bc75a21a121ed9c7a46b1a3113fcab0).
