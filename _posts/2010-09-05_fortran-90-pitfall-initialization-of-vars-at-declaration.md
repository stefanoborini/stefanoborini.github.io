Fortran 90 pitfall: initialization of vars at declaration
=========================================================

date

:   2010-09-05 14:27

author

:   Stefano

category

:   Fortran

slug

:   fortran-90-pitfall-initialization-of-vars-at-declaration

I am dusting my Fortran 90 skills. One big gotcha that always leaves me
baffled is the following. Suppose you write the following program

``` {.fortran}
program test
  implicit none

  call testsub()
  call testsub()
end program

subroutine testsub()
  implicit none
  integer :: var

  var = 0
  print *, var
  var = 5
  print *, var
end subroutine
```

If you expect the output to be

``` {.text}
0
5
0
5
```

you are right. This is indeed the output you get.

Now consider the following slight different testsub routine

``` {.fortran}
subroutine testsub()
  implicit none
  integer :: var = 0

  print *, var
  var = 5
  print *, var
end subroutine
```

See the difference ? I just coalesced the first assignment of var to the
declaration line. You wouldn\'t expect a big difference right ? Sorry to
bring the news, but that\'s a completely different story. The output you
will obtain is

``` {.text}
0
5
5
5
```

What happened? The fact arises from a very subtle point of the Fortran
standard: local vars with initialization at declaration are
automatically SAVE, so they preserve their content between subsequent
calls (in C terms, they are local static). In other words, this
statement

``` {.fortran}
integer :: var = 0
```

is totally equivalent to

``` {.fortran}
integer, save :: var = 0
```

This is totally counter-intuitive and a huge pitfall if you don\'t know
it. What\'s the rationale behind this practice ? [I asked on
StackOverflow](http://stackoverflow.com/questions/3352741/fortran-assignment-on-declaration-and-save-attribute-gotcha),
and user [kemiisto](http://stackoverflow.com/users/153349/kemiisto)
referred me to [this page where this behavior is explained in rather
detail](http://www.rhinocerus.net/forum/lang-fortran/92384-initialization-local-variables.html).
The reason is due to historical bad practices.

Apparently, initialization during declaration was already possible in
Fortran 77. Usage of this variable without redefinition was allowed
behavior, commonly done when you initialize and assign a parameter, for
example. On the other hand, redefinition within the routine body was a
disallowed practice because, according to the standard, the variable
technically became **undefined** upon reentry.

Before standardization of Fortran 90, the actual internal handling of
initialization during declaration was performed with a lot of freedom by
compilers, as there was nothing specifying for that in the standard.
There were two possible strategies to perform it: static initialization
(doing the assignment only once), and reinitialization at every new
subroutine call (doing it every time). These two solutions are
equivalent, **if** no reassignment is done inside the subroutine, i.e.
the expected practice according to the standard. Compilers were free to
choose which strategy to use, but in practice, most compilers used the
\"initialize once and consider it static\" strategy, probably because
it\'s more efficient (you assign only once), so even if the variable was
technically undefined if reassignment occurred, in practice it behaved
like a static variable.

While the Fortran 90 standard was defined, a lot of code was produced
abusing this behavior. As time passed, forbidding it in the new release
was not feasible, because it would have introduced a lot of trouble with
existing code. This was probably one of those moment in history where
programmers would have learned that **when something is declared
undefined in the standard, it\'s your fault if you abuse it**, and you
eventually pay the consequences. The Fortran committee instead condoned
and ratified this practice, and now it is part of the standard.
Regardless of its status, please follow my advice and stay away from it.
