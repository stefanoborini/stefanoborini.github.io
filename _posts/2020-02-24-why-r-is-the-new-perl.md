---
category: graph theory
title: Why R is the new Perl (incomplete)
---

Why R is the new Perl

I have the unfortunate experience of having to use R.  

Perl was a language that started as a substitute for awk and sed, and grew as a hodgepodge of  
broken choices, unorganised decisions, and questionable design. Unfortunately it became the dear
little tool of bioinformaticians, and for a while, if you wanted to do bioinformatics, you were
in for the ride with that garbage dumpster fire. Hey, at least it was not PHP.

Then something happened, probably BioPython, and the bioinformaticians, pretty much the only ones
still keeping the language alive, left in droves.

Today R is in the same situation as Perl. It's a broken, inadequate language for reliable development
that needs to die and will be replaced by python within 5 years. You have been warned. At the moment,
R is kept alive only by statisticians and the company behind RStudio.

Let's give a list of problems that R has as a language that makes it completely inadequate for professional,
reliable development:

1. Its package manager, packrat, is broken

Packrat is fundamentally flawed. It claims to be a package manager. It takes too many liberties and 
has some annoying non-orthogonality behaviors. It wants to install a large, humongous set of initial
requirements at bootstrap which you are not going to use. Things like dplyr (to access sql databases),
or yaml, or Rcpp. These forced dependencies add 


# Inconsistent naming

# Two ways to lookup namespaces

:: and $

# All global

# install.packages does not raise an error or return an identifying code if build fails

install.packages does not allow you to fail early.  If you install.packages,
and the installation is not successful for some reason, it will just give a
warning, but you have no way to stop the execution, (unless you use what boils
down to hacks)[https://stackoverflow.com/questions/26244530/how-do-i-make-install-packages-return-an-error-if-an-r-package-cannot-be-install].

In other words, CI will consider the execution a success, yet you might build a
broken environment and you will only know much later, when something will fail
or you keep a massive lookout in the logs.

# four ways of going object oriented

R has four ways of doing object oriented programming: S3, S4, R5 and R6. 
All of them have either massive shortcomings, or extremely verbose. They are "bolted on" a language
that has not been designed with object orientation in mind.

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

# Its linter assumes you are CRAN and gives the all ok silently

If you want to check the quality of your code, you use a linter. In R, the linter
is called "lintr". It has a convenient function to lint a package (lint_package),
as well as a convenient function to have linting as part of your tests (expect_lint_free).
Unfortunately, by default and with [no mention in the documentation](https://www.rdocumentation.org/packages/lintr/versions/1.0.3/topics/expect_lint_free)
by default this function will assume it's running on CRAN, unless told otherwise, and will
say absolutely nothing about it. In practice, it makes you believe your code has been
linted, while it was not. See the code:

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
In other words, its default assumes that you _are_ CRAN, unless you specifically
say otherwise. Massive least astonishment violation, massive asymmetry in
behavior between lint_package() and expect_lint_free(), and massive lack of
documentation clarity.

# is.integer(66) is FALSE


# length("") is 1

# your interpreter is stateful

# lintr expect_lint_free() silently does nothing unless you are running on CRAN.

expect_lint_free
From lintr v1.0.3
by Jim Hester
16th
Percentile

Test That The Package Is Lint Free
This function is a thin wrapper around lint_package that simply tests there are no lints in the package. It can be used to ensure that your tests fail if the package contains lints.

https://github.com/jimhester/lintr/issues/407

# Lists are prone to typos
  
> a <- list()
> a$foo
NULL
>

# useless tracebacks

Error in download_version_url(package, version, repos, type) :
  version '0.2.1' is invalid for package 'assertthat'
Calls: <Anonymous> -> <Anonymous> -> <Anonymous> -> download_version_url

> shiny::runApp('src', port=8888)
Loading required package: shiny
Error in dots_list(...) : attempt to apply non-function
Calls: <Anonymous> ... fluidRow -> div -> dots_list -> column -> div -> dots_list
Execution halted
make: *** [serve] Error 1



# Their development tools (devtools) depend on a web UI framework (shiny) and a graph plotting library (ggplot2).

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

# extracting a regex subgroup forces you to pass the string twice

regmatches("(sometext :: 0.1231313213)",regexec("\\((.*?) :: (0\\.[0-9]+)\\)","(sometext :: 0.1231313213)"))
[[1]]
[1] "(sometext :: 0.1231313213)" "sometext"                   "0.1231313213"

https://stackoverflow.com/questions/952275/regex-group-capture-in-r-with-multiple-capture-groups

# The standard library is ungooglable

say you want to know know to read a file. If you google that,
rdocumentation contains functions that are a separate package

# RStudio is dangerous

- will not save stuff automatically
- can get desynchronized if the code changes due to a git switch, but the editor will keep showing the wrong file. You might lose code if you accidentally save.

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

shinyWidgets uses startsWith, but for some reason I get an error

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

# session is saved


# nchar(NA) == 2

Note: fixed in 3.3 and above.

nchar gives the number of characters in a string. Except when the argument is NA, in which case it apparently converts NA to a string, then gives you the length of that. The result is 2.

> nchar("hello")
[1] 5
> nchar(NA)
[1] 2

in R > 3.3 the same expression returns NA. One could argue it's a bug that has been fixed. I suspect it's a design decision with unintended side effects.


# R6 objects return NULL on undefined variables

> x <- R6::R6Class("x", list(foo = function() { print(self$notexistent) }))
> xx <- x$new()
> xx$foo()
NULL
This means that if I make a typo in one access e.g. results instead of result it will use NULL instead of throwing an error. Is there a way to force the latter?


if you're not willing to use get or another function then I propose you doublecheck the code you're writing to avoid typos 


