---
category: python
---
Calling a C routine from python, the easy way
=============================================

I think it may be interesting for others to see how to call easily a C
routine from python, without implementing a python module. What you need
is the ctypes module. Remeber however that apparently the use of this
module is generally frowned upon, at least according to a note I found
in [PEP 399](http://www.python.org/dev/peps/pep-0399/):

*Usage of \`\`ctypes\`\` to provide an API for a C library will continue
to be frowned upon as \`\`ctypes\`\` lacks compiler guarantees that C
code typically relies upon to prevent certain errors from occurring
(e.g., API changes).*

although to be honest, it may be in the context of the PEP itself, and
not as a general recommendation.

Nevertheless, suppose you want to call the function

```c
double pow(double, double)
```

in the standard math library.

The first thing to do is to define the prototype of the function. You
achieve this via the following:

```python
prototype=ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double, ctypes.c_double)
```

The call to ctypes.CFUNCTYPE creates a prototype object for a C function
that returns a double (the first argument) and accepts two double (the
second and third arguments).

Now you have a prototype. This entity is a class

```python
>>> prototype
<class 'ctypes.CFunctionType'>
```

and you can bind this prototype to the actual function in the math
library with the following. First you create an object representing the
library

```python
>>> dll=ctypes.cdll.LoadLibrary("libm.dylib") # on Mac. Linux use libm.so
```

and then you bind to the actual function

```python
>>> pow = prototype(("pow", dll)
>>> pow(3,4)
81.0
```

This just brushes the surface, but I wanted to make a simple
introductory post.
