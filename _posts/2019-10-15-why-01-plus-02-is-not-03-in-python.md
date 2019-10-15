---
category: python
title: Why 0.1 + 0.2 is not equal to 0.3 in python (in progress)
---

This post explain a frequently asked question about python that is nothing new to people who knows their bits and bytes,
but it's unexpected to newcomers. Why this

```python
>>> 0.1+0.2
0.30000000000000004
```

This is not a python bug. This is not a bug. This is expected behavior in any programming language. Those who tell you otherwise
are lying (well, they are probably truncating earlier).

# The floating point type

First of all, what's a floating point number? it's a type that can contain
non-integral values, such as 1.34, or 10 to the minus 20.  In python they are
expressed as the float type.

In mathematics, there are infinite values between any two numbers. Some numbers
repeats forever, like 0.666 and on and on, others don't repeat, but are
infinite, like pi or tau.  However, when you bring computers in, there are
problems, specifically


**Not all real numbers are representable as floating point numbers**

which means we must always truncate them to a given maximum number of digits.

For example, imagine we only have 4 digits available. Tau is mathematically
6.28318.. etc but we cannot express this value with only four digits. We can
express 6.283 or 6.284. Nothing in between.  It's like there's a hole between
them, and any value in that hole, finite or infinite, cannot be expressed.
But, I hear you say, 0.2 should be representable, right? It's not infinite.
Well, no, and to explain this, we need to dig deeper.

Computers don't understand numbers in base ten. They understand numbers in base
two, binary numbers. A number that is finite in one system, may not be finite
in another. Specifically, 0.2 is not finite in binary. Let's see why.

First of all, let's check what it means to be in a given base. A number like 327 can be written as 

    327 = 3 * 100 + 2 * 10 + 7

and if we use powers of ten, we can write

    327 = 3 * 10^2 + 2 * 10^1 + 7 * 10^0

similarly, a number like 0.125 can be rewritten as

    0.125 = 1 * 0.1 + 2 * 0.01 + 5 * 0.001

and again, using powers of ten, as

    0.125 = 1 * 10^-1 + 2*10^-2 + 5 * 10^-3

When we have binary numbers, the rule is the same, only that instead of using 10, we use 2. 
A binary number only allows the digits 0 and 1, so a value like

    110.01<sub>2</sub>

Is equivalent to 

    1 * 2^2 + 1 * 2^1 + 0 * 2^0 + 0 * 2^-1 + 1 * 2^-2

and if you do the math it is 6.25 in decimal.

What about 0.2? in decimal, it's easy, it is 2 * 10^-1. 

But in binary you will find out that it is repeating, and its first ten digits
are 0.0011001100 and on and on. 

Like in our example with truncated tau value, if we stop at ten binary digits,
we cannot represent any value that lies between 0.0011001100, which is
0.19921875 in decimal, a bit less than 0.2, and 0.0011001101, which 
is 0.2001953125, a bit more than 0.2.

The decimal value 0.2 lies in this interval, and because its value in binary is
infinite, a computer cannot exactly hold decimal 0.2 in memory. It will always
hold a very close approximation, but never exactly 0.2. Every time you tell the
computer you want to handle 0.2, the computer will not store 0.2.  It will
store something very close to it. How close, depends on how many binary digits
it uses to represent the number.  This also happens for other values, and it is
the reason why this difference emerges occasionally. 

Python is not wrong. It is just exposing the hard truth: mathematics with
floating point numbers is inexact by design and the error between the
represented value and the mathematically correct value, known as round-off
error, can have dramatic effects on the final result of a series of operations.
It also means that the order of operations or the precision of intermediate
values can change the result.

# Floating point in-memory representation: IEEE 754

How are floating point numbers actually represented in memory?
Converting a concept, in this case a floating point number, into a bit pattern is
called an encoding. There's a standard known as the IEEE 754 that specifies
exactly how floating point values should be represented in memory.
Note that this is not the only encoding possible (in fact, I had to work with
non IEEE encodings in my career), but it is by far the most universal standard
in modern computing.

To understand how a floating point number is stored in memory we will use the struct module.
struct allows us to extract the byte representation of data. We'll then convert this 
representation to bits and I will explain how these bits represent the floating point number. 

When dealing with floating point values, we need to represent three pieces of information: 
the sign, the mantissa and the exponent.

normalised form : we gain one bit.

IEEE 754 also defines some special combinations of bits to represent some extremely useful information for floating point math,
such as plus or minus infinite, and an entity called Not a Number (NaN). There's an interesting gotcha about NaN that needs some explanation
NaN is not equal to itself.


code

slide

    The standard defines four possible sizes for a floating point representation. 
    The two most common are known as single precision and double precision.
    Single precision occupies 32 bits, four bytes, can represent numbers between around 10^-38 and 10^38, both positive and negative, with a precision of around 7 decimal digits. 
    In C on an x86 machine, this is generally referred as "float". (FIXME: check float precision)
    Double precision occupies 64 bits, eight bytes, and can represent numbers between 10^-308 and 10^308, both positive and negative, with a precision of around 16 decimal digits.
    In C on an x86 machine, this is generally referred as "double".
    Both modes also allows to specify special values such as positive and negative infinity, positive and negative zero, a value known as "NaN" or Not a Number with some odd properties,
    and other special properties we will not explore.


    53 bits. But here there are only 52. The reason is, one bit is always for free.

To reduce build up of errors, the standard also specifies an extended double precision (80 bits, 10 bytes). 
This mode is for example used internally by x86 processors while doing multiple operations one after another.

## Alternative encodings

IEEE 754 is today _the_ way to represent a floating point value, but it wasn't always the only one. In fact, many other representations
existed, and some are still in use today on legacy code.  VAX had its own, as well as Microsoft with MBF. 
This format was also used on the venerable Commodore 64.

IEEE 754 was not always the standard. Before 1985 every platform had its own way of encoding floating point values,
and in some extremely rare cases they are still supported today. For example, I personally witness two: VAX and MBF.

Commodore 64 had no in processor operations to perform floating point operations.

One interesting bit of information about VAX is that, floating point representation aside, which was quite similar 
to IEEE, was that the value was stored as middle endian.

VAX-11 Floating Point Representations: "F_Floating" Structure (32 bit "longword"):
313029282726252423222120191817161514131211109876543210
Fraction (second part): bit 16 is the least significantSign BitExponentFraction (first part): bit 6 is the most significant

Cray Floating point representation

signed zero

If the exponent is all ones, then two things can happen. Either the mantissa is all zeros, and in that case the value
represents a zero, or the mantissa is not all zeros, and in that case it represents NaN.

zero is all bits set to zero.


References
----------

http://www.mrob.com/pub/math/floatformats.html




