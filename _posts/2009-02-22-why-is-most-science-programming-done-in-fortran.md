---
category: fortran
title: Why is most science programming done in fortran?
---

I found this interesting question in the referral logs.
Why is most science programming done in Fortran (77 or 95)?

After some thought, I can fill the following reasons:

- Fortran is simple to understand. Not the code itself maybe, but the
  style. The learning curve for doing something in Fortran is very
  low, and after you manage the basic concepts, read and write, you
  can be proficient enough to write even complex computational
  application. Most scientists are not programmers, and they would be
  overwhelmed with the intricacies of C and C++. I would strongly
  prefer a non-programmer to code Fortran than, say, perl. In other
  words, Fortran just fits the need computational scientists have:
  read numbers, do a calculation, write the result, and everything can
  be taught to a profane in a standard semester course.
- Fortran is computationally efficient. I will not go into the age old
  debate about \"is Fortran really faster than C?\", for which I have
  a rather articulate opinion I won\'t delve in. Instead, I will just
  present the fact that is indeed one of the languages whose compilers
  and computational libraries have been beaten to death for
  computational efficiency, being their marketing value.
- Fortran is old. This has the effect of producing a huge amount of
  legacy code that have to be maintained or reused. Rewriting this
  code is normally not possible: who should do it? Even if this task
  requires just one man month in three years of Ph.D. contract, it
  will probably not produce a scientific publication, so nobody want
  the task. Moreover, the rewriting will likely ruin interfacing with
  other codes, programs and libraries, as well as the group knowledge
  (if any) of the code, so this move will almost always be opposed.
- Fortran has a slow release cycle. Backward compatibility has been
  kept into account. Knowing that the code you wrote in the 80s will
  still compile today (or eventually you will have to add some
  compiler switch) make everyone happier. I am not sure you can run a
  perl or python program written 10 years ago and have it running
  today. I have no experience with C and C++ and old codes, so I am
  not completely sure about this point, and I welcome being proven
  wrong.

There are for sure many other reasons, but I won\'t go further.

Let\'s see instead why and when Fortran should not be used. My head goes
to python for most comparison:

- Fortran has very reduced expressivity. You need a lot of code, often
  redundant, to code something. In some cases, you need to put stuff
  in temporary variables to pass the information to a subroutine,
  introducing more variables (difficult to maintain) or recycling old
  ones (bad).
- Fortran (77, things are better in 95) makes very difficult to
  perform modular programming. Namespace pollution can be dramatic on
  large programs, especially considering the short identifier limit
  (not an issue on modern compilers, but in violation of the
  standard). Fortran 95 modules are a step ahead, but you can\'t group
  modules into submodules.
- Fortran (95) does not allow storage of function or subroutine
  pointers, making callback-oriented programming very hard.
- Fortran (95) does not allow inheritance. [Smart workarounds exist](http://www.macresearch.org/advanced_fortran_90_callbacks_with_the_transfer_function),
  but they require some skills and the base class develops a
  dependency towards derived ones.
- Fortran has no polymorphism nor templating, making very painful to
  work on generic data types. Again, [workarounds exist, but they require external tools](http://www.macresearch.org/advanced_fortran_polymorphism_and_generic_programming).
- Fortran makes very difficult to keep loose coupling. A very strong
  dependency network arises. For large programs, the number of modules
  USEd (or the amount of code in them) may increase considerably.
  Compare with python, where a module does not need to be imported if
  you have to call a method on an object inside that module, or with
  C++, where you have forward declarations.
- Fortran (95) does not have object orientation, it is very difficult,
  if not impossible, to use traditional design patterns.
- Fortran does not have exceptions (F2003 will, but not custom ones,
  as far as I know).
- Fortran has IMPLICIT. (Edit: yes, it has `IMPLICIT NONE`, but the
  existence of implicit declaration is unfortunately abused still
  today. It should have been deprecated.)
- Fortran (77) does not have aggregated data types and dynamic memory
  allocation (in the standard)
- Fortran strings are not dynamic in length (unless, if I remember
  correctly, if you do very weird hacks). A string of Length 100 and
  another of Length 101 are like being two different datatypes (say an
  int and a string), unless you use the LEN=\* in routine calls, but
  you cannot make more room to an allocated string if needed.
- Fortran did not have clear interfacing with C, and every compiler
  did as it pleased. Apparently this is no longer true with the
  introduction of `BIND`.
- No effective tools exist for documenting the code or easily perform
  Test Driven Development.
- Libraries out there are targeted at computational tasks. I haven\'t
  seen any good library for GUI programming, networking, db access,
  and even if you could, would you ?
- Fortran is full of unusual pitfalls for anyone used to a different
  language. While pitfalls exist in any language, Fortran has pitfalls
  coming from compatibility towards older improper use (e.g. automatic
  SAVE in assignment at declaration). In some other cases though,
  pitfalls are due to the highly optimized nature of the language.
  These pitfalls are in general a strong deviation from the behavior
  of any other language using the similar constructs.
- Most of the code out there uses old code. Even if the language
  progressed, you will still find ancient remains of code written when
  the main writing method was a stick on a clay table. This code will
  most likely be impossible to refactor.

This is just out of the top of my head, and I am sure there is a lot
more. In any case, Fortran 2003 seems to alleviate most of the problems
outlined above. In particular, it will have object oriented programming,
and function/subroutine pointers. A considerable step forward.

Please note that I wasn\'t a Fortran fan, but with time I became
tolerant to it. It should be used sparingly and only where the need
exist, or if a real reason exists: use high level programming languages
with good expressivity first, such as Python. Then eventually optimize
where needed, sometimes with a drop of Fortran, but only if you really,
really (yes, I mean **really**) need it.
