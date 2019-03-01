---
category: fortran
---
Undefined symbols for Fortran module variables in static library on OSX. Problem (and solution)
===============================================================================================

If you program in Fortran on the Mac, you might meet this odd problem.
You have a module test.f90 containing nothing but public variables

``` {.fortran}
module Test
    implicit none
    integer :: value
end module
```

and a program

``` {.fortran}
program main
    use Test
    implicit none

    value = 5
    print *, value
end program
```

If you try and compile as follows, you have no problems

``` {.console}
ifort -c test.f90
ifort -c main.f90
ifort main.o test.o
./a.out
```

However, if you package the test.o in a test.a static library

``` {.console}
ar cru test.a test.o
ranlib test.a
ifort main.o test.a
```

You will get an undefined symbol error for the value symbol. What gives?
Well, the problem has to do with how ranlib on Mac works. You have two
solutions to this problem:

> -   either you add a module procedure to the test module
> -   or you use ranlib -c instead of plain ranlib.

I thank [Drew McCormack for figuring this
out](http://lists.apple.com/archives/fortran-dev/2006/May/msg00026.html)
and [going back to post the solution](https://xkcd.com/979/).
