---
category: fortran
---
# Bad practices in legacy code

I have my fair experience with legacy Fortran code, and still I can't wrap my
head around some practices, in particular when it comes to understand the logic
behind some decision. Here I am giving you a list of the freak show I
personally witnessed, describing why it's bad, and how to do it in the correct
way.

## Useless names for variables

Quick! what do you think a variable called "izpxh" contains ? I'll tell you at the end of the section.

If you call a variable "a" it does not really transmit a lot about it. calling
it "hamiltonian" or "hamil" would have helped a bit at least to understand
what's going on. If it's too long to type, it means that you are using the
wrong editor. Vim, for example, has <a
href="http://www.mohdshakir.net/2007/12/27/enable-vim-code-python-auto-complete">a
nice autocompletion feature</a>. You may object that "back then" we wrote code
with cat redirected to file, and that's fine, but the time you save typing is
then wasted remembering what that variable contains. You are doing a dictionary
lookup in your brain every time you meet a symbol that is not directly
meaningful, mentally converting "a" into "hamiltonian" every time. This is
exhausting, and adds an additional layer of complexity to an already overloaded
brain which is trying to understand what's going on algorithmically. Remember,
<a
href="http://en.wikipedia.org/wiki/The_Magical_Number_Seven,_Plus_or_Minus_Two">a
brain can only deal with seven things at a time</a>. Finally, when you pass the
code to someone else, you

- waste time explaining him by mail what that variable contains
- make him slower at achieving his task
- teach him a bad practice, which will then be perpetrated to even more code.

Are you really saving time in the end ?

By the way, "izpxh" contains true if an atom is an hydrogen, false otherwise. What's wrong with "isHydrogen" ?

To conclude: *Use meaningful variable names*

## Recycling variables to contain something completely different

Another bad habit is to recycle variable names. If calling something "a" wasn't
bad enough, what's better to have "a" containing something in one part of the
code, and something of a completely different nature later on? Congratulations,
now not only you force yourself to do a dictionary lookup in your brain for the
symbol, you also have to remember in which part of the code you are. Double
trouble! This practice arises from the desire of recycling (thus saving)
allocated memory. You can't rename a symbol associated to a given memory space
unless you use pointers, which is a F90 feature, but you can achieve the same
in F77 with UNIONS.

In addition to this, often the same name is preserved in subroutines arguments,
where the name can be changed without any issue to a more proper meaning. Say
you have a variable "a" that contained the position, and after some operation
"a" contains the speed. Then you call a routine "kin(a,m)" which computes the
kinetic energy. The routine kin is defined as such

```
subroutine kin(a,m)
```

Why keep "a" as dummy argument just because the caller had "a" ? Why not take the chance of using a meaningful name within the routine, with

```
subroutine kin(speed, mass)
```

The worst case arises when a meaningful variable name (e.g. hamiltonian) is
used to contain the hamiltonian, and later on is used to contain something else
of similar structure (e.g. the overlap). This does not help in understanding
the algorithm.

To conclude: *Don't recycle variables. If you have to save memory, minimize the
damage, but the real question is "do you really have to save memory? today?"*

## Routines that do too much (and are misnamed)

If a routine is called "mulliken", it is expect it to compute the mulliken
charges, not the mulliken charges *and* the total charge *and* the dipole,
*and* the norm of the dipole, *and *write this information on a file. Such
routine not only cuts through the mathematical board, but also the computer
science board, doing computation and input/output at the same time.  This has
the following results

	- increase the number of arguments to pass to the routine
	- makes it harder or impossible to reuse
	- makes it harder to debug
	- makes it longer
	- increases the number of variables declared inside the routine
	- don't give any hint, while browsing the code, where the other things are calculated.

The objection at this point normally is "but calling a routine is expensive!"
No it's not. Calling a routine is not expensive, unless it's proven that it is.
Show me a profiler clearly indicating your code is slower due to excessive
routine calls, and we'll talk about it. Until then, you should not care.
Calling a small routine may even cost zero, because the compiler might be smart
enough to inline it automatically.

To conclude: *routines should do one thing and one thing only, and should be named clearly*

## A single routine, 1000 lines long

Connected to the above issue, you also have the case where a single routine
must do a lot of stuff in order to achieve a single result. Normally, this
routine is chunked into pieces using comments, like this

```
   ! doing foo
   lots of code
   ! doing bar
   more code
```

The major drawbacks of this behavior are

	- if a routine is too long, it might be doing too much. See above point
	- the comment splitting might not be kept up to date
    - it gives no hint at a glance of which entities are actually manipulated
      in that piece of code

If a part of the code is worth of a short comment explaining what it does, it
is also worth extracting into a separate routine with a meaningful name out of
a condensed form of the comment.  

To conclude: *Routines should not be more than two pages long. If you have more
than that, chunk them into properly named subroutines and call them.*

## The "if" soup

Excessive indentation of if conditions is detrimental to readability and
control. Most of the time you can rearrange the code

## Pages and pages of likely outdated comments

The more you comment, the more likely is that the code will not be up to date
with the comments. Comments don't run, code does. Be extremely wary of comments
containing lengthy explanations or ASCII art. They are the ones most likely to
become outdated, because they require a higher effort to keep up-to-date. The
fact that comments don't run implies there's no penalty for the programmer not
keeping them up-to-date.

To conclude: *keep your comments to a an essential minimum.*

## Be wise in commenting what is needed

Comments should detail things that are not evident from the code itself. If you
use a hack to work around an issue, write a comment. If you use a special
algorithm to solve a problem, comments with a reference to a proper external
resource (e.g. a book, google keyword or scientific paper) if a more throughout
explanation is needed. If you implement a specific equation from a methodology,
it may help to write a comment where this equation is (the paper, and the
equation number).

## Incorrect or lacking indentation, bad formatting

Proper code formatting is important. It hints at what's going on. Screwing up
indentation can lead to nasty bugs. Code without any indentation becomes
extremely hard to read because the visual cues of which parts of the code are
dependent on the conditions of other parts are lost. These visual clues are not
only important for understanding the code, but also for other, higher level
inspection tasks: heavily indented areas of the code hint at possible areas
that might be extracted, or a reformulation of the logic to reduce indentation.
Observing the code shape (for example, pasting it in a word processor and
reducing the font size to unreadable) gives you important clues about the
structure, organization and overall quality of the code.

Spaces and empty lines are another important clue

## Passing related information as independent entities to a routine

It does not make sense to pass a vector and the length of the vector as
independent parameters to a routine. If you need the vector, pass the vector.
If you need the length, pass just the length. If you need both, pass the vector
and have the length calculated internally. Having these two info passed
independently when they are, in fact, highly related, is asking for trouble.

## Using the wrong name for a given entity

## Collating arrays (and not marking the meaning of indexes)

## Routine comments about running info

## Comparing floats

## Changing the loop variable inside the loop

## Giving log messages semantic meaning

Making log messages meaningful for further parsing makes the output very fragile.

## Magic numbers

If you have magic integers that have a special meaning, give them a name as parameters. If I see this

```method = 2```

I get absolutely no information about it until I meet this

```
if (method == 1) then
    call doMethodTrivial()
else if (method == 2) then
    call doMethodLessTrivial()
else if (method == 3) then
    call doMethodComplex()
endif
```

This makes me angry for two reasons. The first reason is that I don't know what
that number means. The fact that the variable is called "method" may hint that
is a method selection, but it may be a plain integer that is used as such, like
in an exponent. The second reason is that it pretends I remember what each
number means every time I meet it around in the program, while at the moment
the only thing that hints at the meaning of each number is the logic of that
if. Suppose that earlier on I found this

```
if (method == 1) then
    mmParam=3.2
else if (method == 2) then
    mmParam=3.4
else if (method == 3) then
    mmParam=3.0
endif

now do you know what each number means?

Advanced languages such as C (yeah, advanced) has a nifty feature called enum.
Fortran does not, but you can sort of work around it, at the very minimum
declaring a bunch of parameters

```
integer, parameter :: METHOD_TYPE_TRIVIAL = 1
integer, parameter :: METHOD_TYPE_LESS_TRIVIAL = 2
integer, parameter :: METHOD_TYPE_COMPLEX = 3
```
so you can actually use these variables, making clear what you mean

```
if (method == METHOD_TYPE_TRIVIAL) then
    mmParam=3.2
else if (method == METHOD_TYPE_LESS_TRIVIAL) then
    mmParam=3.4
else if (method == METHOD_TYPE_COMPLEX) then
    mmParam=3.0
endif
```

## Overuse of OOP when a simple function would suffice
