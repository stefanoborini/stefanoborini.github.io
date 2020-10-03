---
category: r
title: Why R is the new Perl
---

I have the unfortunate experience of having to use R. I say this after more
than a year of fighting against its deeply flawed design, tools, and
documentation. Before I explain why I think it's the new perl, let me introduce you
to what perl is, or better, was.

Perl was a language that started as a substitute for awk and sed, and grew as a
hodgepodge of broken choices, unorganised decisions, and questionable design.
Unfortunately it became the dear little tool of bioinformaticians, and for a
while, if you wanted to do bioinformatics, you were in for the ride with that
garbage dumpster fire. Hey, at least it was not PHP.

Then something happened, probably BioPython, and the bioinformaticians, pretty
much the only ones still keeping the language alive, left in droves.

Today R is in the same situation as Perl. It's a broken, inadequate language
for reliable development that evolved from a limited use case (provide access
to statistical functions) in an extremely wrong direction, and will be replaced
by python within 5 to 10 years. You have been warned. At the moment, R is kept alive
only by statisticians and the company behind its development, RStudio. As soon
as the python world decides to implement all R packages in python (as they did
with [all major libraries during the python 2 to 3
migration](http://chhantyal.net/py3readiness/)), R will be abandoned. 

Strong statement, and here comes the list why I think this is the case, it can
be recapped in different categories:

- problems with the design of the language and its libraries
- problems with its tools and environment
- problem with its licensing

## Problems with the design of the language and its libraries

Before going into detail, let me quote a [brilliant piece of design advice about language design](https://eev.ee/blog/2012/04/09/php-a-fractal-of-bad-design/)

> I assert that the following qualities are important for making a language
> productive and useful [...]:
>
> - A language must be **predictable**. 
>   It’s a medium for expressing human ideas and having a computer execute them, so it’s critical that a human’s understanding of a program actually be correct.
> - A language must be **consistent**. 
>   Similar things should look similar, different things different. Knowing part of the language should aid in learning and understanding the rest.
> - A language must be **concise**. 
>   New languages exist to reduce the boilerplate inherent in old languages. (We could all write machine code.) A language must thus strive to avoid introducing new boilerplate of its own.
> - A language must be **reliable**. 
>   Languages are tools for solving problems; they should minimize any new problems they introduce. Any “gotchas” are massive distractions.
> - A language must be **debuggable**. 
>   When something goes wrong, the programmer has to fix it, and we need all the help we can get.

R fails on all the points above. It is often unpredictable and inconsistent. It
is not concise when you want to program defensively or when you want to use
advanced features such as classes. Has poor reliability in its gotchas and tool
implementations, and has abysmal debuggability information.

The result is that R as a language is completely inadequate for reliable,
professional development that scales. 

Now this is the point where people say "it's just different" and "you have to
learn its behavior", but no. I won't accept this justification when one of the
major R books is literally called ["the R
inferno"](https://www.burns-stat.com/pages/Tutor/R_inferno.pdf). People have
worked in awful, inconsistent, extremely gotcha-prone languages, with rules
making absolutely no sense or too complex to be held in a human brain for
years. Perl and PHP (and for different reasons C++) are notable examples. Heck,
people complained even [against structured programming and claimed that
removing
gotos](https://web.archive.org/web/20090320002214/http://www.ecn.purdue.edu/ParaMount/papers/rubin87goto.pdf) 

> GOTOless programming [...] has caused incalculable harm to the field of 
> programming, which has lost an efficacious tool. It is like butchers 
> banning knives because workers sometimes cut themselves. Programmers 
> must devise eIaborate workarounds, use extra flags, nest statements 
> excessively, or use gratuitous subroutines. The result is that 
> GOTOless programs are harder and costlier to create, test, and modify. 

The results of bowing to poorly designed or massively gotcha-prone languages
created piles and piles of unreliable, fragile code that were impossible to
reliably maintain, all while their supporters chanted it's not the language
fault, it's your fault.  Again, I will adapt from Fractal of Bad Design:

> Imagine you have a toolbox. 
> You pull out a screwdriver, and you see it’s one of those weird tri-headed
> things. Okay, well, that’s not very useful to you, but you guess it comes in
> handy sometimes.
>
> You pull out the hammer, but [...] it has the claw part on both sides. 
> Still serviceable though, I mean, you can hit nails with the middle of the 
> head holding it sideways.
>
> You pull out the pliers, but they don’t have those serrated surfaces; 
> it’s flat and smooth. That’s less useful, but it still turns bolts well enough, so whatever.
>
> And on you go. Everything in the box is kind of weird and quirky, but 
> maybe not enough to make it completely worthless. And there’s no clear 
> problem with the set as a whole; it still has all the tools.
>
> Now imagine you meet millions of carpenters using this toolbox who tell you 
> "well hey what’s the problem with these tools? They’re all I’ve ever used 
> and they work fine!" And the carpenters show you the houses they’ve built, 
> where every room is a pentagon and the roof is upside-down. And you knock 
> on the front door and it just collapses inwards and they all yell at you 
> for breaking their door.

R is just one more of the languages on the list above, and will meet the same
fate.

So, with all that said, let's get started.

### Inconsistent case style

R uses inconsistent case style in its base library all the time. Sometimes it
uses '.' as a separator (e.g. ``is.null``), sometimes it uses camelCase (e.g.
``modifyList``) sometimes snakecase (e.g. ``check_tzones``), sometimes all lowercase
(e.g. ``debugonce``, ``extendrange``). This pattern has already been observed in the 
famous essay [PHP, a fractal of bad
design](https://eev.ee/blog/2012/04/09/php-a-fractal-of-bad-design/) which I
quoted above.

### The interpreter is stateful by default

The interpreter preserves previous execution data across invocations. The
result is that you might receive bug reports from people who claim your package
is not working, but in reality there's nothing wrong with it, they just have
something that has messed up their environment, or they have stored variables
that they think hold something, but actually hold something else.

An interpreter should always be stateless (in other words, the vanilla option should
be enabled by default). This is the case with all interpreted languages except
R (as far as I know).

### It has four ways of doing object oriented programming

R has four ways of doing object oriented programming: S3, S4, R5 (apparently
now obsolete) and R6. They are:

- incompatible with each other
- have been "bolted on" on a language that has not been designed with object orientation in mind (kind of like Perl's ``bless``)
- each have massive shortcomings.

### Lists and environments are prone to typos

lists will return NULL if you use a name that has not been defined:
  
```
> a <- list()
> a$foo
NULL
```

The consequence of this is that if you accidentally mistype a name, it will not throw an error. It wil instead
continue with the NULL value until it will eventually fail, much later. Tracking down the incorrectly typed
name will be extremely hard.

### R6 objects return NULL on undefined variables

As a consequence of the above, R6 classes will suffer the same fate, both for member values and for methods:

```
> x <- R6::R6Class("x", list(foo = function() { print(self$notexistent) }))
> xx <- x$new()
> xx$foo()
NULL
```

This means that if I make a typo in one access e.g. results instead of result
it will use NULL instead of throwing an error.

When I inquired about this behavior, the proposed solution was, laughably, not
to mistype variables:

    if you're not willing to use get or another function then I propose you 
    doublecheck the code you're writing to avoid typos 

I wish to point out that this behavior is what created a massive amout of
problems in FORTRAN, because a mistyped variable would be accepted as real,
generally with a random value in it. It is the reason why [any FORTRAN course
recommends to use IMPLICIT
NONE](http://www.personal.psu.edu/jhm/f90/statements/implicit.html), no
exceptions. That's right, even FORTRAN 77 has at least a way to disable a
terrible feature (that made sense at the time of punchcards) that allows for
mistakes to pass silently.  R has no such luxury, you will not make mistakes by
not making mistakes.

### Exceptions are quit impractical

This is a minor annoyance, but R natively has only one way of throwing an
exception: ``stop()``.  Unfortunately, this is normally used to throw a string.
There's a way to describe a better protocol via [custom
conditions](http://adv-r.had.co.nz/Exceptions-Debugging.html) but it's rather
painful to use.  tryCatch also has different scope for the tried operation and
the handlers (which are functions, possibly closures).  Not a big deal to be
fair, but it's a bit annoying.

The result is that most libraries out there don't bother with a complex
protocol and just throw stop with an error message, making it impossible or
really hard to take appropriate corrective actions, as they depend on the type
of failure, and this is only expressed in fragile human readable form.

### Tracebacks are useless

Tracebacks are mostly useless in R, for many reasons. In addition to the above
two points (no exceptions and delayed evaluation) their parser is rather poor and can't provide meaningful
errors. Also, most often it seems that it keeps no information about the source file provenance, the routine
or the stack trace. Here are a few examples of outputs I've got:

```
Error in download_version_url(package, version, repos, type) :
  version '0.2.1' is invalid for package 'assertthat'
Calls: <Anonymous> -> <Anonymous> -> <Anonymous> -> download_version_url
```

No line numbers, no file provenance.

Here is a missing comma. Again, nothing that points out where the source of the error actually is.

```
> shiny::runApp('src', port=8888)
Loading required package: shiny
Error in dots_list(...) : attempt to apply non-function
Calls: <Anonymous> ... fluidRow -> div -> dots_list -> column -> div -> dots_list
Execution halted
make: *** [serve] Error 1
```

### nchar(NA) == 2 (fixed in >3.3)

nchar gives the number of characters in a string. Except when the argument is
NA, in which case it apparently converts NA to a string, then gives you the
length of that. The result is 2.

```
> nchar("hello")
[1] 5
> nchar(NA)
[1] 2
```

in R > 3.3 the same expression returns NA. One could argue it's a bug that has
been fixed. I suspect it was a design decision with unintended side effects.

### Extracting a regex subgroup forces you to pass the string twice

This is for vanilla R. Better packages exist but I am focusing on the core language.
Regular Expressions are such a fundamental tool that should be correctly implemented
out of the box

```
regmatches(
    "(sometext :: 0.1231313213)", 
    regexec(
        "\\((.*?) :: (0\\.[0-9]+)\\)", 
        "(sometext :: 0.1231313213)"
    )
)
[[1]]
[1] "(sometext :: 0.1231313213)" "sometext"                   "0.1231313213"
```

The [reason?](https://stackoverflow.com/questions/952275/regex-group-capture-in-r-with-multiple-capture-groups)

    regexec returns a list holding information regarding only the location of the matches, 
    hence regmatches requires the user to provide the string the match list belonged to.

### You can have NULL as an element of a list, _sometimes_

One of the many inconsistencies of the language. If you create a list with NULL, it will be a legitimate element
and it will be counted:

```
> l <-  list(1, NULL)
> l
[[1]]
[1] 1

[[2]]
NULL
> length(l)
[1] 2
```

Which of course has an effect on loops.

However, if you think about assigning NULL to an already existing list, it will not replace the position with NULL. It will
remove that entry. There's no way to have a list containing NULL after creation:

```
> l[[2]] <- NULL
> l
[[1]]
[1] 1
> length(l)
[1] 1
```

whoever thought of the semantics of this construct has winged it, and makes it
for an inconsistent behavior.

### %in% cannot tell you if there's a null value in a list

Related to the above, the ``%in%`` operator cannot tell you if you have a NULL
in a list. It can, however, tell you if you have any other element. 

```
> 1 %in% list(1,NULL,3)
[1] TRUE
> NULL %in% list(1,NULL,3)
logical(0)
```

Moreover, what it returns is not a ``TRUE`` or ``FALSE``, but an empty logical vector,
which breaks conditionals if you happen to have a variable that contains NULL:
```
> foo <- NULL
> foo %in$ list(1, 3, 4)
logical(0)
> if (foo %in% list(1, 2,3)) { print("hello") }
Error in if (foo %in% list(1, 2, 3)) { : argument is of length zero
> 
```

### is.integer(66) is FALSE (and is.\* routines are inconsistent)

Here we go in the realm of the ``is.`` functions. They are checking for type,
not value, and that is ok, provided that there's consistency. Unfortunately that's not the
case: ``is.na()`` and ``is.infinite()`` check for value, not type: NA is of
variable type, and Inf is a ``numeric``. Also, some of them behave on individual values,
other on the whole:

```
> is.infinite(c(1,2,3))
[1] FALSE FALSE FALSE
> is.numeric(c(1,2,3))
[1] TRUE
```

To go back to the ``is.integer(66)`` being false, it stems from the fact that 66
is not an integer type (a type that is never used implicitly), but a numeric
type, which is a type for floating point values. Integer math and the integer
type is as old as computer science, but R (and it's not the only one in this)
coerces all numerical literals (even those that are for all practical and
visual purposes integers) to floating point (type numeric). The broken design
of the data type hierarchy leads to these counterintuitive behaviors and poor
consistency.

### Everything is global with no namespaces

R does not support namespacing. There's no importing mechanism. All your code is brought in
by "sourcing" it and basically running the code in one single namespace. The result is that
if you have a large codebase that happens to define the same function name twice, you now
have a problem. Moreover, by not having namespaces, it's hard to organise routines in logical
modules. There is no hierarchy in organising individual R files (hence the R directory has 
only a bunch of R files which cannot be organised in subdirectories). When
these files are organised into a package, the sourcing of these files happen in 
alphabetical order. I have no idea what happens if the locale changes, and the
lack of control over the sourcing order means that you have to rely on stupid
names like ``aaa.R`` and ``zzz.R`` to ensure some code is sourced first or last.

### The library import strategy is very poor

The import strategy of the language, at least for external packages (as we saw
above, there's no import strategy for local code) and in all tutorials relies
heavily on ``library()``. The problem with library is that everything is
imported globally from the package, meaning that the chance of conflicts
between different libraries or between libraries and your routines is large.

But that's beside the point. The major problem is with code information: if I
see the routine ``foobar()`` called, I now have no idea where this routine comes from.
Is it core R? is it from one of the ten packages imported with library()? is it a
routine of this package? 

Fortunately, there's another notation, which is to qualify the routine
invocation with ``::``. So, instead of calling ``foobar()``, one can call
``thatlib::foobar()`` without using ``library()`` and at least ensure that the
provenance is established and there's no name conflict. Too bad one has to do
it everywhere, so one workaround is to do weird local assignments such as
``foobar <- thatlib::foobar``. And note: local as "inside each and every
function", because if you do it at the top level, you are basically polluting
the global namespace and solved nothing.

Additionally, the hierarchy is necessarily flat, so forget about being able to
organise libraries in subsystems and be able to invoke
``mylibrary::mysubsystem::myfunction``.

### The online documentation is poorly organised and deceiving

One day I get the following error (wow, a working stacktrace!):

```
Warning: Error in shinyWidgets::updateProgressBar: could not find function "startsWith"
Stack trace (innermost first):
    68: h
    67: .handleSimpleError
    66: shinyWidgets::updateProgressBar
    65: observeEventHandler
```

Sure enough in progressBar the startsWith is called

```
R/progressBars.R:    if (!startsWith(id, session$ns("")))
```

Uncertain about the nature of the error, I google startsWith, and get documentation
about [gdata startsWith](https://www.rdocumentation.org/packages/gdata/versions/2.18.0/topics/startsWith).
Try it, google "startsWith R". Only the second result is the correct function, which is startsWith from the
core R. If you go to Rdocumentation.org and search for "startsWith" you get Package entries in the following order

- translations
- tools 
- datasets 
- methods
- utils 
- stats4 
- tcltk
- compiler
- parallel
- splines
- grDevices
- grid
- graphics
- stats
- base 

Only *the last one* actually contains a function *startsWith*. In the function list, we get instead:

- startsWith (backports)
- startsWith (gdata)
- startsWith (base)
- startsWith (SparkR)
- startsWith (jmvcore)
- startsWith (Xmisc)
- other stuff unrelated to startsWith

Now, as you can see, in order to find out which ``startsWith`` is the one that
shinyWidgets is actually calling I must check shinyWidgets dependencies, plus
their subdependencies, plus their dependencies etc, because I have no idea
where that symbol comes from and which one is supposed to be called.
In practice, I need to find why my environment does not have a function that I
have no way of finding.

Of course this is a simple example (and yet pointed out that the authors of
shinyWidgets [did not check or agree on the appropriate minimum R compatibility
requirements on their DESCRIPTION
file](https://github.com/dreamRs/shinyWidgets/issues/234)) but in a real world
scenario with a large codebase it makes it extremely time consuming or even
impossible to trace the problem. This is time best spent on doing something
else. Like learning a better language.

### Delayed evaluation let problems pass silently and have errors occur away from where they originate

Imagine you have the following scenario (simplified to make the point):

```
baz <- function(x) {
    print("tons of code in baz")
    print(x)  # [2]
}
bar <- function(x) {
    print("tons of code in bar")
    baz(x)
    print("more tons of code in bar")
}
foo <- function(x) {
    print("tons of code in foo")
    bar(x)
    print("more tons of code in foo")
}

foo(3+"4") # [1]
```

Adding a number and a string is not possible, so an error should be produced. 
Where is the error going to happen? Not where the sum is actually performed in \[1\], 
but much, much later, at \[2\]

```
[1] "tons of code in foo"
[1] "tons of code in bar"
[1] "tons of code in baz"
Error in 3 + "4" : non-numeric argument to binary operator
```

because R does not evaluate the parameters passed to a function until they are
evaluated, which may be never. Comment out the line at \[2\] and the code will
execute without an error.

This is _horrifying_ because:

- errors will occur in locations much, much later in the execution, and tracing back their
  actual origin will be a nightmare, especially considering the poor or non-existent tracebacks.
- errors will be silenced until some conditions actually trigger the evaluations, meaning 
  that, for example, algorithms or UIs will keep hidden bug bombs that will only
  be triggered when specific circumstances occur, and not immediately when and
  where the expression is composed.

The justification for this behavior is performance (why calculate something you are not using).
I say if you are not using it, don't calculate it in the first place. Or at least devise something
that makes it _clear_ and _explicit_ the evaluation will be delayed, like a functor. Don't make it
the default of the language, because the default makes it much, much harder to debug. This design
is equivalent to [premature optimisation, the root of all evil](https://ubiquity.acm.org/article.cfm?id=1513451), 
and carries a heavy technical and human cost.

### Debugging information is inconsistent depending on invocation strategy

Invoking with Rscript provides some form of backtrace
```
$ Rscript x.R 
[1] "tons of code in foo"
[1] "tons of code in bar"
[1] "tons of code in baz"
Error in 3 + "4" : non-numeric argument to binary operator
Calls: foo -> bar -> baz -> print
Execution halted
```

Invoking from the prompt as source gives no information whatsoever about the call chain:

```
> source("x.R")
[1] "tons of code in foo"
[1] "tons of code in bar"
[1] "tons of code in baz"
Error in 3 + "4" : non-numeric argument to binary operator
```

same if you extract the broken evaluation 

```
x <- function() {
   foo(3+"4")
}
```

and invoke it as a function

```
> source("x.R")
> x()
[1] "tons of code in foo"
[1] "tons of code in bar"
[1] "tons of code in baz"
Error in 3 + "4" : non-numeric argument to binary operator
```

If it weren't for the prints, and in a large codebase, you would have no damn
idea where the error actually triggered, and as seen from the problem above,
where it actually originated.

### Non standard evaluation: workaround after workaround

In addition to what we saw above, in R the expression (and not the value) you
pass to a function is received in the called function, meaning that if you have
a dataframe with a column called ``Characteristic``, 
you can write it as a (non-existent) variable and exploit the mechanism to
refer to the column named ``Characteristic`` in ``data``:

```
sub <- subset(data, Characteristic == outcome)
```

Unfortunately, for linters and ``R CMD check`` now you have an undefined variable
"Characteristics". How do you work around it?  one way is to use rlang::.data,
but unfortunately then [you get an error](https://community.rstudio.com/t/using-rlang-data-with-dplyr-verbs-to-generate-queries/6074)
when your tests try to invoke your code. Not sure if it's a bug, but it
certainly does not help in understanding how this ["data
pronoun"](https://rlang.r-lib.org/reference/tidyeval-data.html) is supposed to
work. Some people use it with the rlang:: prefix, [some others say you
shouldn't](https://github.com/tidyverse/dplyr/issues/2930) but then you have to
add it to NAMESPACE. Yet it still does not work. 

What's the recommended solution? Shut up the check with "globalVariables" which 
declares a variable as global, but not for everything, [just for the
check](https://www.rdocumentation.org/packages/utils/versions/3.6.1/topics/globalVariables).
Can you restrict it at least in scope? No, of course not, because this is R, namespacing is not a thing,
the note states 

> The global variables list really belongs to a restricted scope (a function or
> group of method definitions, for example) rather than the package as a whole.
> However, implementing finer control would require changes in check and/or in
> codetools, so in this version the information is stored at the package level.

In practice, this whole ordeal works around (``globalVariables``) with a confusing
mechanism a workaround (``rlang::.data``) of a blunder of design of the language
(allowing to use undefined names from the caller in the callee) and of the
check system, which therefore does not even understand its own rules.

## Problems with its tools and environment

### Its package manager, packrat, is inadequate

Packrat is fundamentally flawed. It claims to be a package manager. It takes
too many freedoms and has some annoying non-orthogonality behaviors. It wants
to install a large, humongous set of initial requirements at bootstrap which
you are not going to use. Things like dplyr (to access sql databases), or yaml,
or Rcpp. These forced dependencies add complexity to your environment. It also
has no way to resolve a proper dependency tree. It just allows to reinstall
what you already installed using the deeply flawed resolution system that
``install.packages()`` provides. Your dependencies have no guarantee of being
consistent (and thus the environment you are developing on) because the
resolution of a given package might conflict with the dependencies you already
have. This is a well known problem, and it's especially dramatic in R where
dependencies in the DESCRIPTION file are so vicious that you end up with Shiny
(a web application framework) [installed when you install devtools](https://github.com/r-lib/devtools/issues/2133) 
(a library to perform build operations on packages, that has no justification
of being dependent on the former):

```
> install.packages("devtools")
Installing package into ‘/Users/xxx/tmp/xxx/packrat/lib/x86_64-apple-darwin15.6.0/3.5.3’
(as ‘lib’ is unspecified)
also installing the dependencies ‘zeallot’, ‘colorspace’, ‘utf8’, ‘vctrs’,
 ‘plyr’, ‘labeling’, ‘munsell’, ‘RColorBrewer’, ‘fansi’, ‘pillar’,
 ‘pkgconfig’, ‘httpuv’, ‘xtable’, ‘sourcetools’, ‘fastmap’, ‘gtable’,
 ‘reshape2’, ‘scales’, ‘tibble’, ‘viridisLite’, ‘sys’, ‘ini’, ‘backports’,
 ‘ps’, ‘lazyeval’, ‘shiny’, ‘ggplot2’, ‘later’, ‘askpass’, ‘clipr’,
 ‘clisymbols’, ‘curl’, ‘fs’, ‘gh’, ‘purrr’, ‘rprojroot’, ‘whisker’, ‘yaml’,
 ‘processx’, ‘R6’, ‘assertthat’, ‘rex’, ‘htmltools’, ‘htmlwidgets’,
 ‘magrittr’, ‘crosstalk’, ‘promises’, ‘mime’, ‘openssl’, ‘prettyunits’,
 ‘xopen’, ‘brew’, ‘commonmark’, ‘Rcpp’, ‘stringi’, ‘stringr’, ‘xml2’,
 ‘evaluate’, ‘praise’, ‘usethis’, ‘callr’, ‘cli’, ‘covr’, ‘crayon’, ‘desc’,
 ‘digest’, ‘DT’, ‘ellipsis’, ‘glue’, ‘git2r’, ‘httr’, ‘jsonlite’,
 ‘memoise’, ‘pkgbuild’, ‘pkgload’, ‘rcmdcheck’, ‘remotes’, ‘rlang’,
 ‘roxygen2’, ‘rstudioapi’, ‘rversions’, ‘sessioninfo’, ‘testthat’, ‘withr’
```

The R world has no equivalent of poetry or pipenv. Sadly, since I have to build reliable
environments, I am writing one myself, but I am not allowed to make it opensource yet.

## There is no consistent and reliable way to install old (archived) packages

Stock R has no way of specifying installation of a specific version of a
package.  You have to use ``devtools::install_version`` to do so. Unfortunately, I
verified that this function is unreliable in its behavior, and resolves
dependencies differently when the package that you are installing by version
also happens to be the most recent one. I did not file a bug because I just
gave up on it and starting writing my own tool to install packages.

### It is too focused on RStudio

Most people using R use RStudio. They don't go through the command prompt and are
therefore completely lost when you have to perform console operations. In a production
environment where you have to ensure runnability of a complex application that needs
to run on jenkins and three architectures, you have to bring out something a
bit more powerful. R has no executable commands. lintr must be invoked as an R function,
roxygen must be invoked as a R function, installing packages in the environment must be invoked
as a R function. This makes it really hard to trigger failures in CI.

### Its linter assumes you are CRAN and gives the all ok silently

On the topic of the linter, [it fails miserably at reporting an error](https://github.com/jimhester/lintr/issues/406)
because of completely broken assumption that [you are always running on
CRAN](https://github.com/jimhester/lintr/issues/407) unless told otherwise.

Lintr has a convenient function to lint a package (lint\_package), as well as a
convenient function to have linting as part of your tests (expect\_lint\_free).
Unfortunately, by default and with [no mention in the
documentation](https://www.rdocumentation.org/packages/lintr/versions/1.0.3/topics/expect_lint_free)
by default this function will assume it's running on CRAN, unless told
otherwise, and will say absolutely nothing about it. In practice, it makes you
believe your code has been linted, while it was not. See the documentation 

```
expect_lint_free

Test That The Package Is Lint Free
This function is a thin wrapper around lint_package that simply tests there are
no lints in the package. It can be used to ensure that your tests fail if the
package contains lints.
```

and the code:

```
> lintr::expect_lint_free
function (...)
{
    testthat::skip_on_cran()
    lints <- lint_package(...)
    has_lints <- length(lints) > 0
    lint_output <- NULL
    if (has_lints) {
        lint_output <- paste(collapse = "\n", capture.output(print(lints)))
    }   
    result <- testthat::expect(!has_lints, paste(sep = "\n",
        "Not lint free", lint_output))
    invisible(result)
}
> testthat::skip_on_cran
function () 
{
    if (identical(Sys.getenv("NOT_CRAN"), "true")) {
        return(invisible(TRUE))
    }
    skip("On CRAN")
}
```

In other words, its default assumes that you _are_ CRAN, unless you
specifically say otherwise with an environment variable. I say it again: **for
lintr any machine out there, your machine, my machine, the jenkins machine is
the CRAN build server by default**, and expect\_lint\_free will not do
absolutely anything and give the all clear. Massive least astonishment
violation, massive asymmetry in behavior between lint\_package() and
expect\_lint\_free(), and massive lack of documentation clarity.

### install.packages does not raise an error or return an identifying code if build fails

install.packages does not allow you to fail early.  If you install.packages,
and the installation is not successful for some reason, it will just give a
warning, but you have no way to stop the execution, (unless you use what boils
down to hacks)[https://stackoverflow.com/questions/26244530/how-do-i-make-install-packages-return-an-error-if-an-r-package-cannot-be-install].

In other words, CI will consider the execution a success, yet you might build a
broken environment and you will only know much later, when something will eventually fail
during tests and you will have to spend hours trying to figure out what happened.

### The whole environment is kept alive by one company and three major contributors

All the current development tooling in R, linters, development environment,
documentation, is kept alive by one company, RStudio, and three of their most
active developers. The results of this is that a lot of very questionable
design choices go in completely unopposed or unreviewed, and favor a single,
all-encompassing environment: RStudio. It's either our way or the highway,
even when their way is awfully broken and nonsensical.

### Getting a package approved on CRAN is an exercise in frustration

Getting your package on CRAN is one of the most frustrating, annoying,
uselessly complicated processes I've ever witnessed. They have [a complex set
of policies](https://cran.r-project.org/submit.html) you have to obey, and the
whole build system is extremely strict and extremely obtuse in what is accepted
and not accepted, giving you no hint of the space you are missing or the enter
you have in excess. Compared to python where you can register a package in pypi in
a few seconds, releasing [Tendril on CRAN has been a complete and utter waste
of a week of work](https://cran.r-project.org/web/packages/Tendril/index.html).

### RStudio is an extremely poor development environment 

RStudio is an extremely poor development environment. In truth, it's a data analysis platform that tries to be an IDE and fails miserably.

- Its configurability is absolutely limited. 
- It will not save files automatically on focus out, forcing you to perform saving every time
- Its file browser does not display a full tree, but only one directory at a time, making it impossible
  to easily switch to files that are far away in the hierarchy
- The code and the file displayed can get desynchronized if the code changes due to a git checkout, 
  but the editor will keep showing the wrong file. You might lose code if you accidentally save.

### Shiny requires a constant websocket open, transfers large chunks of HTML

Shiny allows for fast development of web interfaces to R code. Its design is extremely poor.
All the state of the session is kept on the server. Every time you click a button, every time
you modify a control content, it requires a round trip to the server to modify the state there.
The server will then respond with data to modify the page, potentially just a slab of HTML to 
replace the DOM tree.

This design has the following issues:

- it's awfully slow, as every user interaction requires network operations. This will give the user the impression
  of a poorly responding and slow application
- requires a constant and stable connection.
- If the connection is interrupted, willingly or unwillingly, the state will be lost and the user will 
  have to restart the whole interaction from scratch. There are some mitigating options but are palliative
  of a deeper issue.
- Dynamic interfaces flicker due to the delay in retrieving and replacing large parts of the HTML tree.

Moreover, the default implementation is single threaded, single task, meaning
that if one user starts a long running calculation, it will block _the_ _whole_
_application_ to anybody else. The calculation lasts 20 minutes?  No other user
will be able to even connect to the application for those 20 minutes. Yes, you
can use promises to mitigate this issue, but they are not part of Shiny itself.
A design that supports this natively should be a default, not an afterthought.
Even with futures, you still lock the session to the user, because the futures
must complete before other events are processed.

Finally, controls can only be either input or output. You can't use a control
both as an input and as an output. If you do, you will end up with potential
desynchronization problems and "ping-pongs" between the frontend state on the
browser and the server state, due to the intrinsic loop nature of the
transaction and the round trip time between the operations. This problem is
easy to handle when the state is all local to the browser, but pretty much
impossible to handle. Cases of controls that must be both input and output are
checkboxes, textfields, radio buttons, sliders, and selects.


# Licensing problems

The R interpreter is GPLv2, as are a relevant amount of CRAN libraries. This has deep, deep implications for
commercial suitability of R developed solutions, because with the interpreter being GPL, and most importantly
the interpreter core libraries being GPL, it means that any code that you develop must be released
under a GPL license and can only run in a GPL compliant system. This pretty much [destroys any chance 
for integration of R code in a commercial, closed source environment](https://www.r-bloggers.com/2019/01/how-gpl-makes-me-leave-r-for-python/).

# Summing up

R is a fundamentally broken language that is destined to a brief surge in
popularity pumped by the current data analysis trends, followed by an
inevitable crash once the same utilities are ported to python and its old
school proponents retire. It is deeply flawed technically, and deeply flawed
from a business perspective. It is a one-company environment defined by a
restricted group of developers who make very dubious and questionable design
choices.
