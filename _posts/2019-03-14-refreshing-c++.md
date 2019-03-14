---
category: c++
---
# Refreshing my C++ for fun and profit

It has been a while since I used C++, and now that I regularly do it at work, I
decided to refresh it a bit. I never really dropped it completely in this
fortran-filled hiatus, but now that the new Stroustrup book is out, I decided
to attack the beast again. I am therefore reading with great interest the
latest "C++ programming language", and here are a few new or semi-new things I
found interesting, either because they are new, or because I forgot about them:

## New initialization style

Variables can be initialized with a new style, which Stroustrup recommends
```
int a {3};
```
Which adds to the old style
```
int a = 3;
```
Similar expressions that are also supported are
```
int a = {3};
int a(3);
```
I am a bit disappointed with this addition, but apparently it behaves in a stricter way when conversion is required
```
int main() {
        int a = 40.3; // No error, but truncates
        int a {40.3} // Error
}
```
However, this backfires horribly if you use another addition to the language: auto types
```
int main() {
        auto a = 40; // a is now an int
        auto a {40} // a is now an initializer_list
}
```
So, you should prefer {} over = except when using auto, when the opposite is true. What the hell...

## auto variables

Finally, instead of writing
```
MyClass&lt;MyTemplate, MySecondTemplate&lt;int, string&gt; &gt; \*a = MyClass&lt;MyTemplate, MySecondTemplate&lt;int, string&gt; &gt;("string")
```
We can write
```
auto \*a = MyClass&lt;MyTemplate, MySecondTemplate&lt;int, string&gt; &gt;("string")
```
The compiler knows the type at compile time, and can use this knowledge to save us some typing. auto is cool.

## using instead of typedef

Using, for all purposes, replaces typedef.
```
typedef MyClass * MyClassPointer
using MyClassPointer = (MyClass \*);
```

## Placement new

Albeit not a C++11 feature, I discovered this one only recently. A Placement
new is a form of the new operator that does not allocate memory, but calls the
constructor on previously allocated memory. It is particularly convenient if
you have a memory pool and want to create a new object on it, meaning that it
allows you to separate allocation from construction. An example (<a
href="http://www.devx.com/tips/Tip/12582">taken from here</a>):

```
\#include 
using namespace std;
int main() {
        char *buf  = new char[1000];         // pre-allocated buffer
        string *q = new string("hi");        // ordinary heap allocation. Allocates and call constructor
        delete(q);                           // ordinary heap deallocation. Calls destructor and deallocates.
        string *p = new (buf) string("hi");  // placement new. Executes constructor without allocation
        p-&gt;~string();                        // executes destructor.
        delete[] buf;                        // free the memory of the buffer
}
```

The first new allocates memory and executes the constructor. The first one does
not allocate any memory: it executes the constructor on the pre-allocated
memory provided by the given buffer. Note that the destructor must be called
manually, and that the buffer must be freed independently in a separate
delete[] on the buf itself.

Placement new can also be used on stack memory (usual scope lifespan warnings apply).

## lambda expressions

## inline namespaces

## Final keyword

With the final keyword, you can now prevent derived classes to reimplement
virtual methods of the base class, effectively allowing you to close further
reimplementation.

```
class Base  {
public:
virtual void function() {};

};

class Derived1 : public Base {

public:

void function() final;

}

class Derived2 : public Derived1 {

void function(); // Error. Can't override after final

}
```

## Other little things: nullptr, enum classes, constexpr

The keyword nullptr can now be used in a pointer assignment. This replaces the
NULL or 0 frequently used for the same purpose.

Enum classes are a special kind of enum that is much more type strict than a
traditional C enum. They are strict in namespacing and don't cast to an integer
implicitly.

constexpr are constant expression that are evaluated at compile time, instead
of runtime. They are useful to provide constant values from compile-time
defined information through evaluation of the expression, providing potential
performance benefits.

