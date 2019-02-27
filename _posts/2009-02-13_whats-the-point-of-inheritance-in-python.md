What\'s the point of inheritance in python ?
============================================

author

:   Stefano

category

:   C/C++, Design, Python

Python is a fascinating language. It makes you think. Sometimes it can
destroy your beliefs. Sometimes it makes you understand new concepts in
a natural way, specifically Generic Programming.

My background is in statically typed languages. I came from C++, camped
there for a while, then moved to python. I also explored Java recently.

I would like to present my case by remembering the three pillars of
object oriented programming:

1.  Encapsulation
2.  Inheritance
3.  Polymorphism

In particular, I would like to go into the details of two of them:
inheritance and polymorphism.

Inheritance is a strategy that allows you to define a new class
(hereafter called NEW) as derived of an old one (OLD). The new class
gets access to all methods and attributes of the old one, and according
to the [substitution
principle](http://en.wikipedia.org/wiki/Substitutability), you can
replace objects of type OLD with object of type NEW without altering the
properties of the program. For example, suppose you have the following
situation

``` {.c++}
#include <iostream>

class Animal {
public:
    virtual void speak() = 0;
};

class Dog : public Animal {
    void speak() { std::cout << "woff!" <<std::endl; }
};

class Cat : public Animal {
    void speak() { std::cout << "meow!" <<std::endl; }
};

void makeSpeak(Animal &a) {
    a.speak();
}

int main() {
    Dog d;
    Cat c;
    makeSpeak(d);
    makeSpeak(c);
}
```

As you can see, `makeSpeak` is a routine that accepts a generic `Animal`
object. In this case, `Animal` is quite similar to a java interface, as
it contains only a pure virtual method. makeSpeak does not know the
nature of the `Animal` it gets passed. It just sends it the signal
\"speak\" and leaves the late binding to take care of which method to
call: either `Cat::speak()` or `Dog::speak()`. This means that, as far
as `makeSpeak` is concerned, the knowledge of which subclass is actually
passed is irrelevant.

But what about python? Let\'s see the code for the same case in python.
Please note that I try to be as similar as possible to the C++ case for
a moment:

``` {.python}
class Animal(object):
    def speak(self):
        raise NotImplementedError()

class Dog(Animal):
    def speak(self):
        print "woff!"

class Cat(Animal):
    def speak(self):
        print "meow"

def makeSpeak(a):
    a.speak()

d=Dog()
c=Cat()
makeSpeak(d)
makeSpeak(c)
```

Now, in this example you see the same strategy. You use inheritance to
leverage the hierarchical concept of both `Dogs` and `Cats` being
`Animals`. Here is the nice thing: in python, there\'s no need for this
hierarchy. This works equally well

``` {.python}
class Dog:
    def speak(self):
        print "woff!"

class Cat:
    def speak(self):
        print "meow"

def makeSpeak(a):
    a.speak()

d=Dog()
c=Cat()
makeSpeak(d)
makeSpeak(c)
```

In python, this kind of inheritance application is irrelevant because
there\'s no concern of the type. you can send the signal \"speak\" to
any object you want. If the object is able to deal with it, it will be
executed, otherwise it will raise an exception. Suppose you add a class
`Airplane` to both codes, and submit an `Airplane` object to
`makeSpeak`. In the C++ case, it won\'t compile, as `Airplane` is not a
derived class of `Animal`. In the python case, it will raise an
exception at runtime, which could even be an expected behavior.

On the other side, suppose you add a `MouthOfTruth` class with a method
`speak()`. In the C++ case, either you will have to refactor your
hierarchy, or you will have to define a different makeSpeak method to
accept `MouthOfTruth` objects\... or in java you could extract the
behavior into a `CanSpeakIface` and implement the interface for each
\... There are many solutions, but I wont\' go into this direction.

What I\'d like to point out is that I haven\'t found a single reason yet
to use inheritance in python: you don\'t need to implement a
base-derived hierarchy to perform polymorphically. See also [this post
which points out a similar point of
view](http://forums.devshed.com/python-programming-11/does-interface-only-inheritance-make-sense-in-python-82822.html).

So, if interface-only inheritance has no meaning, maybe it could be ok
for implementation-based inheritance? What about recycling the code and
the data of a base class? You can accomplish the same through a
containment relationship, with the added benefit that you can alter it
at runtime, and you clearly define the interface of the contained,
without risking unintended side effects.

But yes, there\'s a natural case where a class hierarchy is indeed
useful: Exceptions. Suppose your code is like this

``` {.python}
class ServiceException(Exception): pass
class TrivialException(Exception): pass

class OutOfPaperException(TrivialException): pass
class OutOfTonerException(TrivialException): pass
class BrokenCircuitryException(ServiceException): pass

def usePrinter():
    raise OutOfTonerException()

def writeLocalAdmin():
    print "writing to local admin"
def writeServiceShop():
    print "writing to service shop"

try:
    usePrinter()
except TrivialException:
    writeLocalAdmin()
except ServiceException:
    writeServiceShop()
```

Now, in this case, you actually gain something. Suppose the printer
raises `OutOfTonerException`. This exception will be caught by the
`try/except`, and by virtue of this exception being hierarchically a
`TrivialException`, it will write the local admin that something is
wrong.

What I have written is the essence and the reason for the existence of
Generic Programming in statically typed languages such as C++. As you
can see, both approaches, OOP and Generic Programming are natural and
smooth in Python.
