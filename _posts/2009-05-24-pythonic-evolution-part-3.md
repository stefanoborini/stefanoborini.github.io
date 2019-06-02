---
category: python
title: Pythonic Evolution - Part 3
---

In this third part of the \"silicon-based\" bacterial evolution, we move
to the real action. I developed a program 
which perform evolutive selection based on mathematical criteria. The
program has a set of rules to perform selection, but please note that
most (if not all) of these rules are totally arbitrary. In this sense,
it\'s nothing more than a toy, and I therefore warn against any
scientific analysis of what we obtain. It\'s just for fun. Also, the
code is pretty bad.

There are two classes in the program: Bacterium and Environment. A
Bacterium can be fed, and its genetic code can mutate.The Environment is
responsible for feeding the bacteria with the mathematical conditions,
assess if they are worthy for survival and reap the unworthy. At every
new generation, the Environment perform duplication for each bacterium
in the pool, and apply mutations to the new entries. We try to keep the
pool filled, so we always replenish it to 4000 bacteria at every
generation, out from the available mutated. 4000 is also the limit for
the number of bacteria simultaneously present. This is a very strong
limitation, as it hinders the normal behavior of conventional bacteria:
multiply exponentially. Unfortunately, we don\'t want to spend weeks in
calculations, and in any case the computer memory is limited, so we have
to find a proper and very harsh compromise.

Once the duplication/mutation step, the environment performs the
selection (reaping). For each of the mathematical conditions, each
bacterium is fed with the input value. The returned value is then
compared against what the environment expects. A score is obtained by
summing the relative errors for each condition, and then normalized on
the number of conditions. The closest this score is to zero, the better
is the response of the bacterium. Obtaining zero means that the
bacterium genetic code is able to respond to the conditions exactly. In
the more general situation, the error will be a positive floating point
number which will be compared against a tolerance. If the result exceed
the tolerance, then the bacterium is killed, otherwise it survives and
is allowed to reproduce in the next generation. An additional condition
tries to favor those bacteria having a more compact genome: a random
number between 0 and 50 is extracted, and if the value is greater than
the length of the genome of the bacterium, it will survive, otherwise it
will be killed. This will prevent genomes longer than 50, and strongly
favour short genomes, as it will be more probable that a random
extraction is greater than their length, granting it survival.

In order to improve our genetic pool, the Environment defines an
\"epoch\". An epoch is a number of generations where selection happens.
During each generation of the epoch, the tolerance on the conditions
will progressively decrease, meaning that, as time passes, the
environment becomes more and more selective.

Enough general chatting. Let\'s see an actual example. In the program
you can download, the following conditions are set for the environment

```python
e.setConditions([(0,7),(2,11),(4,15),(5,17)])
```

As you can see, the environment expects the bacteria to be able to solve
the equation 2x+7. The line

```python
e.epoch(1.0,0.0, 20)
```

Starts an epoch made of 20 generations. During these 20 generations, the
tolerance will decrease from 1.0 to 0.0. In other words, the environment
expects, at the end of the epoch, that the bacteria in the pool are able
to solve exactly 2x+7 for all the specified points (x=0,2,4,5).

Suppose we have a bacterium in the pool with the following genetic code:

```
IncX -3             # a = n | x = -3 | y = 0
AddYtoA             # a = n | x = -3 | y = 0
Return              # returns a = n
LoadX 1             # Never reached
BranchXNotZero 2    #
```

As you can see, this bacterium will return the input value unchanged.
This means that the result and relative error for each condition will be

```
Given  | Expected | Produced | abs(Relative Error)
0      | 7        | 0        | 7/7 = 1.0
2      | 11       | 2        | 9/11 = 0.81
4      | 15       | 4        | 11/15 = 0.73
5      | 17       | 5        | 12/17 = 0.70
---------------------------------------------------
                       Total = 3.24
                               / 4 (number of conditions
                             = 0.81
```

This bacterium (as it is, assuming no mutations) will therefore survive
in the first two generations (where the tolerance is 1.0 and 0.9) but it
will be killed in Generation 3, as the tolerance is now 0.8.

Let\'s see another example

```
MoveAtoY     # a = n   | x = 0 | y = n
IncA  3      # a = n+3 | x = 0 | y = n
MoveAtoY     # a = n+3 | x = 0 | y = n+3
Return       # returns a = n+3
LoadX 1      # Never reached
```

In this case, we get

```
Given  | Expected | Produced | abs(Relative Error)
0      | 7        | 3        | 4/7 = 0.57
2      | 11       | 5        | 6/11 = 0.54
4      | 15       | 7        | 8/15 = 0.53
5      | 17       | 8        | 9/17 = 0.53
---------------------------------------------------
                       Total = 2.17
                               / 4 (number of conditions
                             = 0.54
```

Much better. Of course, the best condition would be something like this
(chose a long one, just for illustrative purpose)

```
MoveAtoY    # a = n    | x = 0 | y = n
IncX 3      # a = n    | x = 3 | y = n
AddYtoA     # a = 2n   | x = 3 | y = n
IncA 2      # a = 2n+2 | x = 3 | y = n
IncA 4      # a = 2n+6 | x = 3 | y = n
MoveAtoY    # a = 2n+6 | x = 3 | y = 2n+6
IncA 1      # a = 2n+7 | x = 3 | y = 2n+6
LoadY -3    # a = 2n+7 | x = 3 | y = -3
IncX -2     # a = 2n+7 | x = 1 | y = -3
```

This bacterium returns exactly what the environment expects. This as
well

```
BranchXNotZero 2   # a = n    | x = 0 | y = 0 | no branch
LoadY 1            # a = n    | x = 0 | y = 1
MoveAtoY           # a = n    | x = 0 | y = n
IncA 3             # a = n+3  | x = 0 | y = n
AddYtoA            # a = 2n+3 | x = 0 | y = n
IncA 4             # a = 2n+7 | x = 0 | y = n
```

At the end of the run of the program, you will obtain bacteria like
these. It is interesting to note that selection produced genetic code
able to solve the equation outside its defined space of conditions. We
never put the condition (10, 27), but these two bacteria are able to
satisfy it.

In the current setup, I purposely introduced \"noise\" codons in the
available genetic code. As you can see, the solution for 2n+7 can be
obtained with a proper combination of MoveAtoY, IncA and AddYtoA. The
remaining codons are not used, or if they are, their effect is neutral.
You have two contrasting effects here: the need for the genetic code to
be small (so to maximize its chance of survival against the length
selection) and the need to have buffer codons that can mutate without
particular trouble, in particular if they are after the Return codon.
This reduces the chance that a mutation will ruin the achieved
functionality, making the bacterium with a long genetic code less
sensitive to mutation.

Of course, you would be tempted to try similar cases. I can assure you
that simple equations will be properly satisfied. However, if you try to
do x\^2, your bacteria will always die. Why ? X\^2 is a rather
particular situation. First of all, there\'s an important codon which is
not present : MoveAtoX. Once you have this codon, the space of the
genetic code combinations allows you to potentially obtain the solution.
This is one I wrote by hand:

```
MoveAtoX
MoveAtoY
LoadA 0
BranchXZero 5
AddYtoA
IncX -1
BranchXNotZero -3
```

Obtaining this result from evolution is hard. In some sense, we face the
issue of the so called [Irreducible
Complexity](http://en.wikipedia.org/wiki/Irreducible_complexity), an
argument proposed to object evolution. Indeed this appears to be the
case. The genetic code able to produce the square is irreducible. Either
you take it as a whole, or you don\'t. From our toy program there\'s no
\"in-between\" that satisfies the constraints and allows the generation
of that code in steps. Although apparently a sound argument, there are
many considerations to do on this point, which have a substantial effect
against this position.

First, as I said the program shown here is a toy. You cannot put too
much reasoning for proofs into it. We are running on a very restricted
set of bacteria. Even if statistically improbable, the creation of the
above genetic code when million, or even billion of bacteria are
produced suddenly becomes more possible. Then, selection does its job by
granting it full survivability, and therefore takeover of the
population.

Second: the rules of chemistry are slightly more flexible than the rules
provided here. In this sense, this program represents a situation more
akin to a
[Ziggurat](http://upload.wikimedia.org/wikipedia/en/4/4d/Sacramento-river-bank-pyramid-20.4.jpg)
than an [Egyptian
pyramid](http://upload.wikimedia.org/wikipedia/commons/e/e3/Kheops-Pyramid.jpg).
Electronic interaction of molecules allow a very refined, smooth and
nuanced behavior, while our codons do not.

Third point is that we are assuming a single block of code to be able to
produce a complex mathematical result. Biological systems do not work
this way. Biological systems produce components, and make them interact.
For example, a complex (but still pretty simple) biological process like
the [Krebs
cycle](http://upload.wikimedia.org/wikipedia/commons/0/0b/Citric_acid_cycle_with_aconitate_2.svg)
is not performed by a single molecular übermachine. There are ten
different enzymes involved in carbohydrate consumption, interacting
together in the cell. Each enzyme is a small entity which performs a
simple operation. Together they network for a nice and refined
mechanism. In other words, selection and evolution moves to another
level in real biology: not only the evolution of single components
(enzymes) but also evolution of their mutual interaction. In our toy
program, we don\'t allow interaction of \"subroutines\", nor of
bacteria. The very fact that we are made of a system of interacting
cells and not a huge unicellular bacterium is a hint that our case is
very limited in possibilities.

Fourth point: there no chance for so called [\"lateral
transfer\"](http://en.wikipedia.org/wiki/Horizontal_gene_transfer) among
bacteria. In biological systems, the DNA can be exchanged among
bacteria, as it\'s universal and works in any case. Suppose that a very
powerful enzymatic system would be obtained by the concerted presence of
enzymes A,B,C and D. An organism happen to have enzymes A and B, but not
C and D, because they are normally not evolved in its conditions.
Another organism was able to evolve C and D to address its own
environment. These two bacteria can come in contact, and exchange their
genetic material. Suddenly, both organisms have the whole set of A,B,C,
and D. This would have not been possible without the universality of the
genetic code. It\'s also not possible in our program.

There are of course many other points and issues to consider. I think I
reached my goal to share a personal experiment, and I would like to
close with interesting links toward more evoluted (no pun intended)
software to simulate digital life forms

-   [Framsticks](http://en.wikipedia.org/wiki/Framsticks)
-   [Breve](http://en.wikipedia.org/wiki/Breve_%28software%29)
-   [Darwinbots](http://en.wikipedia.org/wiki/Darwinbots)
-   [Evolve](http://en.wikipedia.org/wiki/Evolve_4.0)
-   [Tierra](http://en.wikipedia.org/wiki/Tierra_%28computer_simulation%29)
-   [Avida (this I like the most)](http://en.wikipedia.org/wiki/Avida)
-   And finally, a [very interesting
    article](http://carlzimmer.com/articles/2005.php?subaction=showfull&id=1177184710&ucat=8)
    from Carl Zimmer about putting Darwin to the test in a simulated
    condition.

Thanks for reading.
