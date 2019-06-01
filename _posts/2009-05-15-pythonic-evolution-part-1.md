---
category: python
title: Pythonic Evolution - Part 1
---

This post is in different parts. The fact is that it requires quite a
lot of time investment, something I really don\'t have in this period.

A long time ago I wanted to play with the concept of genetic code, and
how it represents nothing but a language to code for molecular machines.
As the [Jacquard loom](http://en.wikipedia.org/wiki/Jacquard_loom),
it\'s nothing but a chemical punchcard who gets executed by the ribosome
loom, and loomed into a protein. The fact behind evolution at this level
is that if a small mutation happen in the punchcard by accident, and the
resulting protein turns out to provide a competitive advantage for
survival and reproduction, then this wrong punchcard will naturally
exploit this advantage by becoming the predominant form. Even a very
tiny advantage is sufficient, in the span of million of years, to reach
fixation (the old code is completely replaced by the new one).

The math is simple. Here is a program that does it

```python
normal = 500
mutated = 1

normal_survive_prob = 0.90
mutated_survive_prob = 0.91

for generation in xrange(1,1000):
    normal -= int(normal * (1-normal_survive_prob))
    mutated -= int(mutated*(1-mutated_survive_prob))

    normal *= 2
    mutated *= 2

    total = normal + mutated
    print "Generation %d -- normal : %d %%  mutated : %d %% " % \ 
          (generation, 100*normal/total, 100*mutated/total)
```

In this program (which has some simplifications, but the concept is
there), we have a population of bacteria. We start with 500 normal
bacteria, and only one mutant. This mutant has an advantage: its
mutation makes him more likely to survive (for example, to an
antibiotic, or to UV light from the Sun, or to oxygen). In this case the
probability that the standard bacterium can survive is 90 %. In other
words, if you have a large quantity of bacteria, some of these will die
due to UV light. If you divide the number of survived bacteria by the
number of bacteria you had, you will find out that 90 out of 100
survived, and the other 10 out of 100 died. The remaining 90 % do what
bacteria do all the time: reproduce by splitting in two, meaning that if
40 bacteria survived the UV light and they reproduce, you will get 80
bacteria. In turn, some of them will die, and other will survive, and
reproduce, and this goes on and on.The mutated bacteria has an
advantage: its mutation makes it more resistent to UV light, so it has a
slightly higher probability of surviving: 91 %

If you run the program, you will find out thatat generation 1, almost
everything is made out of normal bacteria

```
Generation 1 -- normal : 99 %  mutated : 0 %
```

At generation 100, you see that the mutated ones start to be visible

```
Generation 107 -- normal : 99 %  mutated : 1 %
```

At generation 365, the mutated ones can start a political party

```
Generation 365 -- normal : 85 %  mutated : 14 %
```

After 525 generations, they are fifty/fifty:

```
Generation 525 -- normal : 49 %  mutated : 50 %
```

At generation 700, the mutated ones are the large majority

```
Generation 700 -- normal : 12 %  mutated : 87 %
```

And finally, at generation 1000 the normal ones are basically
disappeared, and the mutated ones conquered their environmental niche:

```
Generation 1000 -- normal : 0 %  mutated : 99 %
```

Now, if you consider that a bacterial generation happens in days, or
even hours, you see how it does not take much for bacteria to evolve. If
our bacterium here divided every day, we would have a total fixation
after just three years. If you assume that the difference in probability
is 0.01 % (instead of 1% as in this example) you will get the same
result, it will just take more time (and even million of years is a
blink of an eye against the age of the Earth).

The best part about evolution is that it works for everything behaving
with the same modality. What you need is:

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
3.  **Variability of the replicator \"phenotype\"** (which means the
    \"final visible result\" of the replicator). Small modifications
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

A famous example of evolution at work is antibiotic resistance. The
selective pressure of a poisonous substance (an antibiotic) kills the
organisms not able to neutralize it, while those less sensitive to it
survive and reproduce, creating more copies of so-called antibiotic
resistant bacteria. Very soon, the antibiotic becomes ineffective
against this new breed, and a new one must be invented. This is also the
reason why antibiotics should be used sparingly, and always up to the
end of the treatment, so to be sure that even those bacteria that are
more resistant received a lethal dose and are therefore unable to start
a resistant strain.

But the funny part of the evolutive setup is that it works no matter
what the replicator and environment are\....

Continued!
