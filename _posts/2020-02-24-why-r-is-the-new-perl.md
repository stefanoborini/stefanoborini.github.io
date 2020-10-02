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
for reliable development that needs to die and will be replaced by python
within 5 years. You have been warned. At the moment, R is kept alive only by
statisticians and the company behind its development, RStudio. As soon as the
python world decides to implement all R packages in python, R will be
abandoned.

Strong statement, and here comes the list why I think this is the case, it can
be recapped in different categories:

- problems with the design of the language and its libraries
- problems with its tools and environment
- problem with its licensing


## Problems with the design of the language and its libraries

Let's give a list of problems that R has as a language that makes it completely inadequate for professional,
reliable development.

### Inconsistent case style

R uses inconsistent case style in its base library all the time. Sometimes it
uses '.' as a separator (e.g. ``is.null``), sometimes it uses camelCase (e.g.
``modifyList``) sometimes snakecase (e.g. ``check_tzones``), sometimes all lowercase
(e.g. ``debugonce``, ``extendrange``). This pattern has already been observed in the 
famous essay [PHP, a fractal of bad design](https://eev.ee/blog/2012/04/09/php-a-fractal-of-bad-design/).

### The interpreter is stateful by default

The interpreter preserves previous execution data across invocations. The
result is that you might receive bug reports from people who claim your package
is not working, but in reality there's nothing wrong with it, they just have
something that has messed up their environment, or they have stored variables
that they think hold something, but actually hold something else.

An interpreter should always be stateless (in other words, the vanilla option should
be enabled by default). This is the case with all interpreted languages except
R (as far as I know).


## It has four ways of doing object oriented programming

R has four ways of doing object oriented programming: S3, S4, R5 (apparently
now obsolete) and R6. They are:

- incompatible with each other
- have been "bolted on" on a language that has not been designed with object orientation in mind (kind of like Perl's ``bless``)
- each have massive shortcomings.

# Lists and environments are prone to typos

lists will return NULL if you use a name that has not been defined:
  
```
> a <- list()
> a$foo
NULL
```

The consequence of this is that if you accidentally mistype a name, it will not throw an error. It wil instead
continue with the NULL value until it will eventually fail, much later. Tracking down the incorrectly typed
name will be extremely hard.

# R6 objects return NULL on undefined variables

As a consequence of the above, R6 classes will suffer the same fate, both for member values and for methods:

```
> x <- R6::R6Class("x", list(foo = function() { print(self$notexistent) }))
> xx <- x$new()
> xx$foo()
NULL
```

This means that if I make a typo in one access e.g. results instead of result it will use NULL instead of throwing an error.

When I inquired about this behavior, the proposed solution was, laughably, not to mistype variables:

    if you're not willing to use get or another function then I propose you doublecheck the code you're writing to avoid typos 

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

### Evaluation is delayed


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

> nchar("hello")
[1] 5
> nchar(NA)
[1] 2

in R > 3.3 the same expression returns NA. One could argue it's a bug that has
been fixed. I suspect it was a design decision with unintended side effects.


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
as a R function. This makes it really hard to spot failures in CI.

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



# Summing up

R is a fundamentally broken language that 























# Two ways to lookup namespaces

:: and $

# All global

# No clean way to handle zero length arrays in for loops

Suppose you want to iterate over each element of an array, but want to do it by index. You would assume that a loop 
such as  

    for (i in 1:length(array)) {
        print(array[[i]])
    }   

would work for an empty array. Not at all. It will actually run twice, one with i = 1 and again with i = 0.

https://stackoverflow.com/questions/44991925/why-do-variables-get-into-for-loops-with-zero-length

There's apparently nothing to handle this very common use case. Even seq_along does not do the right thing. 
The only suggestion I could find is to write a [workaround routine](https://www.r-bloggers.com/rs-range-and-loop-behaviour-zero-one-null/)

Edit: I then found that this is a working solution

    for (i in seq_len(length(array)))

The body of the loop will not be executed if array length is zero.

# Workaround after workaround

in R, the name of what you pass to a function is received in the called function, meaning that if you have a dataframe
with a column called "Characteristic", you can write this to extract data where the value of Characteristic is equal to  
a given value.

sub <- subset(data, Characteristic == outcome)

Unfortunately, now for linters and R check now you have an undefined variable
"Characteristics". How do you work around it?  one way is to use rlang::.data,
but unfortunately then [you get anerror](https://community.rstudio.com/t/using-rlang-data-with-dplyr-verbs-to-generate-queries/6074)
when your tests try to invoke your code. Not sure if it's a bug, but it
certainly does not help in understanding how this ["data
pronoun"](https://rlang.r-lib.org/reference/tidyeval-data.html) is supposed to
work. Some people use it with the rlang:: prefix, [some others say you
shouldn't](https://github.com/tidyverse/dplyr/issues/2930) but then you have to
add it to NAMESPACE. Yet it still does not work. What's the recommended
solution? Shut up the check with "globalVariables" which declares a variable as
global, but not for everything, [just for the
check](https://www.rdocumentation.org/packages/utils/versions/3.6.1/topics/globalVariables).
Can you restrict it at least in scope? No, of course, because in R, namespacing is not a thing,
the note states "The global variables list really belongs to a restricted scope (a function or
a group of method definitions, for example) rather than the package as a whole.
However, implementing finer control would require changes in check and/or in
codetools, so in this version the information is stored at the package level."

In practice, this whole ordeal works around (globalVariables) with a confusing
mechanism a workaround (rlang::.data) of a blunder of design of the language
(allowing to use undefined names from the caller in the callee) and of the
check system, which therefore does not even understand its own rules.

# is.integer(66) is FALSE

# %in% cannot tell you if there's a null value in a list

> 1 %in% list(1,NULL,3)
[1] TRUE
> NULL %in% list(1,NULL,3)
logical(0)


### You can have NULL as an element of a list, sometimes

```

(l = list(1, NULL))
[[1]]
[1] 1

[[2]]
NULL


l = list(1); l[[2]] = NULL; l
[[1]]
[1] 1


l = as.list(1:3); l[[2]] = NULL; l
[[1]]
[1] 1

[[2]]
[1] 2
```

you can have NULL as an element on a list, but assigning NULL to an
element of a list removes the element rather than makes it a NULL. 


# extracting a regex subgroup forces you to pass the string twice

regmatches("(sometext :: 0.1231313213)",regexec("\\((.*?) :: (0\\.[0-9]+)\\)","(sometext :: 0.1231313213)"))
[[1]]
[1] "(sometext :: 0.1231313213)" "sometext"                   "0.1231313213"

https://stackoverflow.com/questions/952275/regex-group-capture-in-r-with-multiple-capture-groups

# The standard library is ungooglable

say you want to know know to read a file. If you google that,
rdocumentation contains functions that are a separate package


# %in% operator is backwards

> x %in% "b"
[1] FALSE  TRUE  TRUE FALSE  TRUE
> x
[1] "a" "b" "b" "c" "b"
> x %in% "b"
[1] FALSE  TRUE  TRUE FALSE  TRUE
> "b" %in% x
[1] TRUE
>


# The import strategy does not allow you any information on how to debug

Warning: Error in shinyWidgets::updateProgressBar: could not find function "startsWith"
Stack trace (innermost first):
    68: h
    67: .handleSimpleError
    66: shinyWidgets::updateProgressBar
    65: observeEventHandler

Sure enough in progressBar the startsWith is called

R/progressBars.R:    if (!startsWith(id, session$ns("")))

Googling seems to point that startsWith is in gdata

https://www.rdocumentation.org/packages/gdata/versions/2.18.0/topics/startsWith

But gdata is not in the direct dependencies of shiny widgets

Imports:
    shiny (>= 0.14),
    htmltools,
    jsonlite,
    grDevices,
    scales

So now I need to find why my environment does not have a function that I have no way of finding.


# modifyList

This function merges two lists, and does not modify any of the passed arguments.
