---
category: c++
---
# T considered harmful in template programming

As I use more and more C++ generic programming, I come to realize one general
problem of books and tutorials: the use of typename T in template programming.

Generic programming allows compile-time check for types to comply with a
required interface, and freeing the burden of providing multiple definitions
for the same function for different types. For example

```
template &lt;typename T&gt;
T max(T x, T y)
{
return x &lt; y ? y : x;
}
```

satisfies the need to define a max() routine, provided that the generic type T
supports operator&lt;. With only one definition, we cover every possible type,
in this case from native ones to user-defined ones. The compiler will examine
our needs, and instantiate the proper definition according to them, so if one
writes

```
int i = 1;
int j = 2;
int maxval = max(i,j);
`````````

the following template instance will be created for us
```
template &lt;&gt;
int max(int x, int y)
{
return x &lt; y ? y : x;
}
```

This is common knowledge for C++ programmers using templates, and I won't delve
into it. What I want to delve in is the template argument naming convention,
the T.

The problem is that, for simple cases as this one, it does not matter much, but
for more complicated cases with multiple template parameters, there's the
danger that the convention goes on, and symbols such as T, V, and U are used,
or other similar names, like T1, T2 and so on. When you encounter a class
template in a real case scenario, these template argument names give absolutely
no hint on what they are supposed to represent, unless you look into the code.
Delegating the task of pointing out the error to the compiler is not an option,
when C++ provides error messages the size of a novel.

I think it should be made best practice to use more meaningful names for
template parameters. Given that what a template parameter represents is a
protocol a type is supposed to define (a protocol that goes beyond its type, as
in the case of OOP style programming), I think a better practice should be
something like

```
template &lt;typename ComparableProto&gt;
ComparableProto max(ComparableProto x, ComparableProto y)
{
return x &lt; y ? y : x;
}
```

or simply Comparable. This makes clearer that the expected type will be
inquired by the function body for comparability. It still does not communicate
fully, but it's a huge improvement over a generic name such as T, that says
very little. I restate that this case is trivial, but for more complex code,
defining a shared terminology in the development team through protocol names
documents better the intent of a templated class or
method.

