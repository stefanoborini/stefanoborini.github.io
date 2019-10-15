---
category: python
title: Why 0.1 + 0.2 is not equal to 0.3 in python
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
A binary number only allows the digits 0 and 1, so a binary value like 110.01 means:

    0b110.01 = 1 * 2^2 + 1 * 2^1 + 0 * 2^0 + 0 * 2^-1 + 1 * 2^-2

which, if you do the math, is 6.25 in decimal.

What about 0.2? in decimal, it's easy and non-repeating: 2 * 10^-1, but in
binary you will find out that it is repeating, and its first ten digits
are 0.0011001100... 

Like in our example with truncated tau value, if we stop at ten binary digits,
we cannot represent any value that lies between 0.0011001100, which is
0.19921875 in decimal, a bit less than 0.2, and 0.0011001101, which 
is 0.2001953125, a bit more than 0.2.

The decimal value 0.2 lies in this interval, and because its value in binary is
infinite, a computer cannot exactly hold decimal 0.2 in memory. It will always
hold a very close approximation, but never exactly 0.2. Every time you tell the
computer you want to handle 0.2, the computer will not store 0.2. It will
store something very close to it. How close, depends on how many binary digits
it uses to represent the number. This also happens for other values, and it is
the reason why this difference emerges occasionally. 

Python is not wrong. It is just exposing the hard truth: **mathematics with
floating point numbers is inexact by design**, because some values cannot be
represented exactly and are truncated. The error between the represented value
and the mathematically correct value, known as round-off error, can have
dramatic effects on the final result of a series of operations.  It also means
that the order of operations or the precision of intermediate values can change
the result.

# Floating point in-memory representation: IEEE 754

Until now, we discussed the general issue with representing numbers that are 
finite in decimal base, but infinite in binary base, and how truncation affects
the final precision. We said nothing about how floating point numbers actually 
represented in a computer memory.

Converting a concept, in this case a floating point number, into a bit pattern is
called an **encoding**. There's a standard known as IEEE 754 that specifies
exactly how floating point values should be represented in memory (and disk).
Note that this is not the only encoding possible (in fact, I had to work with
non IEEE encodings in my career), but it is by far the most universal standard
in modern computing.

*Be warned*: What I am giving here is an extremely simplified description of IEEE 754.
If you want the full details, this is not the right place, but it will give you a basic
understanding of how it works.

A generic floating point number is fully represented by three entities: the sign,
the exponent and the mantissa. The final result is meant to represent something like

    sign mantissa * 2^exponent

such as
    
    - 0b1.0010 * 2^(-5)

When we have to store this value, IEEE-754 uses the following tricks:

- the exponent is represented as an integer, but shifted so that a value of zero
  means the highest representable negative exponent.
- the mantissa is represented as a sequence of binary digits, representing a
  base 2 fractionary number as in the example I gave above. However,
  the value is normalised, which means that it will be written so that the first
  digit is never zero. This may require a change in the value for the exponent,
  of course.  In other words, binary 110.01 will be rewritten as binary 1.1001,
  and binary 0.0011010 will be rewritten as binary 1.1010. With this
  trick, the first digit will always inevitably be 1, so it can be omitted
  from the in-memory representation and considered implicit.

The standard defines a single precision floating point to be stored using 32 bits, or four bytes.
These 32 bits are allocated as follows:

- 1 bit for the sign: represents if the value is positive (0) or negative (1)
- 8 bits represent the exponent.
- 23 bits to represent the mantissa.

To understand how a floating point number is stored in memory we will use the
``struct`` module to extract the byte representation of data. The following line
does a lot of magic

```python
print(" ".join(reversed(list(map(lambda x: bin(x)[2:].zfill(8), struct.pack('@f', 0.5))))))
```

and basically shows the binary representation of the value 0.5 according to IEEE-754 on
a little endian machine. The result is the following:

    00111111 00000000 00000000 00000000                                                     

If we divide the bits according to the rules given above


    sign exp-127  mantissa                                                                  
    0    01111110 00000000000000000000000                                                   

We see that the exponent is, after removing the shift:

    0b01111110 - 127 = 126-127 = -1

and the mantissa is the implicit one followed by all zeros. The result is therefore

    + 1 * 2^(-1) = 0.5 in decimal

IEEE 754 also defines some special combinations of bits to represent some
extremely useful information for floating point math, such as plus or minus
infinite, positive and negative zero, and an entity called Not a Number (NaN).
There's an interesting gotcha about NaN that needs some explanation NaN is not
equal to itself.

To reduce build up of errors, the standard also specifies an extended double
precision (80 bits, 10 bytes).  This mode is for example used internally by x86
processors while doing multiple operations one after another. 

## Alternative encodings

IEEE 754 is today _the_ way to represent a floating point value, but it wasn't
always the only one.  Before 1985 every platform had its own way of encoding
floating point values, and in some extremely rare cases they
are still supported today. For example, I personally witnessed two: VAX and
MBF. Two bits of trivia on these:

- VAX floating point representation was quite similar to IEEE, but the
  information was stored as middle endian.

- Commodore 64 had no in-processor operations to perform floating point
  operations.  All floating point operations were done in-software by the
  KERNAL. This made floating point operations extremely slow, but these routines
  just applied MBF enconding.

