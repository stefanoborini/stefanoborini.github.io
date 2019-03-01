---
category: other
---
The subtle art of writing a code example
========================================

One of the most frustrating experiences when learning a new technology
is finding useless examples. An example is the most precious thing that
comes with a new library, language, or technology. It must be a starting
point, a wise and unadulterated explanation on how to achieve a given
result. A perfect example must have the following characteristics:

-   **Self contained**: it should be small enough to be compiled or
    executed as a single program, without dependencies or complex
    makefiles. An example is also a strong functional test if you
    correctly installed the new technology. The more issues could arise,
    the more likely is that something goes wrong, and the more difficult
    is to debug and solve the situation.
-   **Pertinent**: it should demonstrate one, and only one, specific
    feature of your software/library, involving the minimal additional
    behavior from external libraries.
-   **Helpful**: the code should bring you forward, step by step, using
    comments or self-documenting code.
-   **Extensible**: the example code should be a small \"framework\" or
    blueprint for additional tinkering. A learner can start by adding
    features to this blueprint.
-   **Recyclable**: it should be possible to extract parts of the
    example to use in your own code
-   **Easy**: An example code is not the place to show your code-fu
    skillz. Keep it easy.

And here comes the helpful acronym: **SPHERE**. Yes, I looked for the
correct synonyms to make it, after the main concepts were in place.

Prototypical examples of violations of those rules:

**Violation of self-containedness**: an example spanning multiple files
without any real need for it. If your example is a python program, keep
everything into a single module file. Don\'t sub-modularize it. In Java,
try to keep everything into a single class, unless you really must
partition some entity into a meaningful object you need to pass around
(and java mandates one class per file, if I remember correctly).

**Violation of Pertinency**: When showing how many different shapes you
can draw, adding radio buttons and complex controls with all the
possible choices for point shapes is a bad idea. You de-focalize your
example code, introducing code for event handling, controls
initialization etc., and this is not part the feature you want to
demonstrate, they are unnecessary noise in the understanding of the
crucial mechanisms providing the feature.

**Violation of Helpfulness**: code containing dubious naming, wrong
comments, hacks, and functions longer than one page of code.

**Violation of Extensibility**: badly factored code that have everything
into a single function, with potentially swappable entities embedded
within the code. Example: if an example reads data from a file and
displays it, create a method getData() returning a useful entity,
instead of opening the file raw and plotting the stuff. This way, if the
user of the library needs to read data from a HTTP server instead, he
just has to modify the getData() module and use the example almost
as-is. Another violation of Extensibility comes if the example code is
not under a fully liberal (e.g. MIT or BSD) license.

**Violation of Recyclability**: when the code layout is so intermingled
that is difficult to easily copy and paste parts of it and recycle them
into another program. Again, licensing is also a factor.

**Violation of Easiness**: Yes, you are a functional-programming nerd
and want to show how cool you are by doing everything on a single line
of map, filter and so on, but that could not be helpful to someone else,
who is already under pressure to understand your library, and now has to
understand your code as well.

And in general, the final rule: if it takes more than 10 minutes to do
the following: compile the code, run it, read the source, and understand
it fully, it means that the example is not a good one.
