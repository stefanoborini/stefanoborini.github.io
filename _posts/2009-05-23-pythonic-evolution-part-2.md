---
category: python
title: Pythonic Evolution - Part 2
---

This is the second part of a post relative to evolution. You can find
the first part of the post
[here](http://forthescience.org/blog/2009/05/15/pythonic-evolution-part-1/).

The last argument in the first post was relative to the requirements for
evolution to happen. To recall, you need

1.  **An imperfect replicator**, an entity able to produce a copy of
    itself, for example the DNA of our bacteria in the example above.
    The replication mechanism must have a certain degree of
    imperfection, so that some chance for occasional mutation must be
    possible, and consequently variability.
2.  **Action of the replicator on the environment**. For example, The
    DNA molecule, through a complex biological setup is able to produce
    proteins which, according to the laws of chemistry, influence the
    external world by digesting a metabolite and obtaining energy, or
    fighting an aggression to survive (to UV light, in our example) and
    reproduce.
3.  **Variability of the replicator "phenotype"** (which means the
    "final visible result" of the replicator). Small modifications
    (accidental or not) to the replicator will change its interaction
    with the external environment (for example, by granting him to
    survive better under UV light)
4.  **Environmental conditions**: the environment will propose
    conditions, for example availabe metabolites, temperature, pressure,
    UV light irradiation and these conditions could also change as time
    passes..
5.  **Selective pressure**: the interaction between the environmental
    conditions and the replicator phenotype will create a
    differentiation between replicators. Those better coping with the
    conditions will have higher reproductive chance than the others,
    producing a drift toward better replicators (in our case, the
    bacteria were under selective pressure because the UV light was
    killing them, but the mutated ones were more likely to survive)

We offered the example of bacteria where a slight mutation offered to a
single organism a very tiny additional chance to survive and produce
children. In this very simple model, the mutated (better fit)
characteristic became predominant in approx. one thousands generations,
not many when you consider bacteria having replication time in the order
of hours or days.

We closed the post by stating that this behavior works regardless of the
nature of the replicator and the environment. It works in nature with
the genetic code, compiled by ribosomes into proteins. It must works in
a digital environment with digital bacteria too.

Four years ago, I developed a simple python program to show how
\"software bacteria\" can evolve behavior to solve simple mathematical
equations with no active human programming. The idea is as follows: a
python program defines a \"Bacterium\" class, which represent our
byte-based life form. Also, I define an \"Environment\", where a bunch
of Bacterium instances will live, prosper and hopefully reproduce. The
environment will provide \"mathematical food\" to the bacteria, and the
better the bacteria elaborate this food, the better for them, and the
higher will be their chance to survive and reproduce.

In real bacteria, the genetic code is converted into protein, and the
proteins are responsible for processing metabolites (food) according to
the laws of chemistry. In our example, we will make a simplification,
skipping the protein step and having the mathematical food directly
processed by our genetic code.

The mathematical food will be a simple integer number and the genetic
code will be a very simple language able to do sums (of signed numbers)
and conditional branching. The result of the genetic code processing the
food will be another integer number, a metabolized mathematical result.
The environment will promote a condition so that those bacteria whose
metabolized product has a particular characteristic (in our case, a
particular resulting value) will have a higher chance of reproduction.
The condition the environment will propose is the expected result of a
simple mathematical equation. Ideally, at the end of this experiment,
the evolved bacteria will possess genetic code able to perform the
mathematical equation for any given input. In this sense, they evolved
to process the food in the best possible way.

Confused? Don\'t worry. It will be clearer soon.

Here comes The Bacterium
------------------------

Cellular systems are not that different from computer programs. There is
a programming language, a compiler, input and output parameters.
There\'s even memory.

In DNA, the genetic code is made out of four molecular letters, A G C T,
forming three letters words, named codons. DNA is first copied to RNA.
The RNA then is interpreted by an elaborate mechanism (the ribosome)
able to translate each group of three-letter words into a specific amino
acid (out of 20) as building block (think LEGO) to be put in a protein.
The protein so created is a molecular machine which performs a chemical
task, like digesting a metabolite, storing substances (eg. iron),
providing structural support and so on. How the system got started is
currently not yet known, but it takes one replicator molecule to start
the process, in particular if this molecule has self-catalytic
properties (meaning: it makes easier the creation of a copy of itself).
Likely candidates are vulcanic activity, electric discharges
(lightnings), or panspermia. I tend to favor the electric discharge,
coupled with catalysis by means of metals (found in the rocks). After
all, the [Miller-Urey
experiment](http://en.wikipedia.org/wiki/Miller-Urey_experiment)
demonstrated that if you mix and boil and discharge electricity long
enough, you will generate aminoacids out of simple gases like water,
methane, nitrogen and ammonia, something that it was present for sure
into the Earth primordial atmosphere. So, at the moment is not know
which was the replicator and how it got produced, but even if unlikely
as an event, once started it grows and is basically unstoppable,
provided proper conditions are met.

Once you have aminoacids, you have proteins. Biological systems evolved
to use proteins because they are more efficient and disposable, while
the genetic code is less efficient, and very important. After all,
programmers keep their source code in a backed up subversion repository,
while giving out compiled versions. Losing a compiled version is not a
big issue, you can always recreate it from the sources, but having your
subversion system go corrupt means that your asset is totally lost, and
could mean that your company is out of business. As already said, in our
in-silico setup, we skip the translation part for simplicity.

In our mathematical bacterium we have three variables that can be set:
A, X and Y. Each of them has a different role and particularity. A is
the import/export variable where the value representing the food is
first inserted, modified, and released to the environment. You can see
it as the unique input/output parameter of our \"genetic code
function\". X and Y are internal variables. You can make an analogy to
internal metabolites needed to support the food consumption. The main
difference between the two is that X is more of a counter: it can be
set, incremented (or decremented) and tested for being zero and decide
if branch (or not). Y is instead auxilliary in processing A. Our
bacterium has a genetic code which consist of 10 codons. Like amino
acids are able to perform various chemical operations on substrates by
their own chemical nature, these operations can perform different
mathematical or logical tasks. The codons are:

-   **LoadA**, **LoadX**, **LoadY**: each of them loads a specified
    value in the variable A, X or Y.
-   **IncA**, **IncX**: increments the value of the variable A or X of a
    given specified amount (can be negative)
-   **MoveAtoY**: copies the content of A into Y.
-   **AddYtoA**: performs the sum between the content of A and Y, and
    stores the result in A.
-   **BranchXZero**, **BranchXNotZero**: jumps a specified number of
    codons forward (or backwards) if the content of the variable X is
    zero or not-zero, respectively.
-   **Return**: terminates the execution of the genetic code.

Let\'s see some example of genetic code that does something to a
mathematical food.

This is the most trivial one

```
Return
```

A bacterium with this genetic code will take the metabolite (an input
number), and load it automatically in A. Then, it will finish
immediately with no processing. The content of A is the result of the
metabolic process. In this case, the bacterium returns what it eats. you
give him 5, it returns 5. You give him 13, it returns 13.

A more interesting case is the following:

```
IncA 5
Return
```

The bacterium with this genetic code in the first instruction will
increment 5 to the content of A. The second statement will return
whatever it is containted in A. This bacterium eats 4 and returns 9,
eats 13 and returns 18, etc. You get the idea.

So, now you can imagine a population of bacteria, and imagine that the
genetic code was created with a completely random process. For example,
say that we create a population of 3000 bacteria with the following
criteria:

1.  When you create each bacterium, you extract a random number of
    codons (from 2 to 50) which will be used to generate their genetic
    code.
2.  Given the number of codons for a specific bacterium, you extract
    that number of randomly chosen codons from the available pool
    (LoadA, LoadX, LoadY, IncA, IncX, MoveAtoY, AddYtoA, BranchXZero,
    BranchXNotZero, Return).
3.  For codons accepting a numeric value (LoadA, LoadX, LoadY, IncA,
    IncX, BranchXZero, BranchXNotZero), extract a random number from,
    say, -5 to +5 and use it as a numeric value.
4.  What you obtain is a bacterium whose genetic code is a random mess
    of a random number of random codons with random parameters.
5.  And of course you obtain a population of 3000 bacteria all with
    random genetic code.

If you feed a number (say 42) to each bacteria, you will expect many
different results. Each bacterium will be fed with the number 42 (which
will be placed in A) and then the randomly generated set of operations
will occur. Nice, but not particularly useful.

But here the cool stuff begins. Suppose you decide to say: if the
environment provides 42, those bacteria that produces a result close to
47 are more likely to survive. Those who produce a numeric value very
far from 47 are instead more likely to die. With this in mind, you start
killing bacteria. Those who return exactly 47 will survive. Those that
return 48 have a slight chance of dying, but not much. Those who return
0, or 500 will be probably killed immediately. Out of the starting 3000
bacteria, you will now have a troop of survivors (say 100) whose genetic
code produce, by pure random chance, something that is quite near to the
expected result (47) out of the food value 42.

Now you allow this bacteria to reproduce. Of course, if you take the 100
survivors and produce exact clones so to repopulate up to 3000, you will
obtain no improvement. Here the \"imperfect replication\" kicks in. You
allow a random number of mutations to occur to each bacterium before
duplicating. These mutations will change the genetic code, potentially
creating a new program that produces something lethal (too far from 47)
but also something with better fit (something quite near to 47).

After this event takes place, you allow the bacteria to replicate so
that you restore your pool of 3000, and you apply selection again. You
feed them 42 and you kill all those bacteria producing results too far
from the expectation (47). New survivors, new mutations, new generation,
and you go on and on.

As you can see, all the conditions for evolution are met:

1.  **An imperfect replicator** exists: it\'s our genetic code based on
    mathematical codons. Replication is imperfect because we have random
    mutation of the genetic code at every new generation.
2.  **Action of the replicator on the environment**. The genetic code
    takes a number and process it into another number.
3.  **Variability of the replicator "phenotype"**. Modifications on the
    genetic code produce modification in the final resulting value.
4.  **Environmental conditions**: The environment presents 42 and
    expects 47 as a good value indicative of a nice processing.
5.  **Selective pressure**: genetic code responding at best to the
    environmental conditions will have a higher chance to survive and
    produce a new generation. Genetic code that is slightly less
    accurate will have a lower chance to survive, and genetic code
    producing values too far from what the environment considers a
    proper response will be killed.

In the next post, we will see how this mechanism has been implemented
into a small python program, and we will see what happens for different
cases.
