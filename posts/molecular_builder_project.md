# Retrospective of an old project: the molecular builder project.
## or, how I discovered Agile before it went mainstream.

These are the notes of a project I was part of, which followed a strict waterfall process.
There was a specification phase (9 months), a design phase (3 months), an implementation phase (3 months) and a testing phase (3 months).
Specification and design phases produced Word documents. Implementation and testing produced code and bugs to be fixed.

The names of the guilty, as well as some details of the project will be redacted.

Pros:
- We did it!
- I did it!
- we learned a lot
- product is not that bad

Cons:
- no research/prototype
- specs complex, difficult, not exaustive
- blind creation
- prototyping yes or no?
- uneven partitioning of the workload
- worked on a non trivial task alone for quite some time
- contrasting constraints
- product is not that good

## plus points

### We did it!

The application came out and we almost met the deadline. I say almost
because yes, we met the internal deadline, but not the public beta as I
think is intended (released to the public on the website). I am happy
because we demonstrated to ourselves that we can act very efficiently when
needed.

### I did it!

The problem was not trivial, and it required me the best of my efforts to
solve problems quickly. I think this project increased my self-esteem
notably, because I was able to solve a task in the expected timeframe even
if I had to face a lot of expected and unexpected hurdles.

### We learned a lot

The project helped us in learning a lot. My personal findings, which should
act also as suggestions for future projects, are:

- the R&D department and the development department have reduced chance
of communication of the intents. The specs document is expected to be an
extract of all the attempts, mistakes, and good decision taken during
research and prototype development. However, most of the small knowledge (or even the
big, if the Research Guy think erroneously that a given fact is a known prerequisite)
is not transferred to the document. 

My opinion is that R&D and development should be more interwined, like
involving one of the developers during the research/prototype phase, maybe only
a couple of hours per week, and having the spec guys do a full lecture about
the specs to the team when the project starts.

- face-to-face discussion is fundamental. The absence of the Main Spec
Writer Guy, ASU, made understanding of the intents very complex. Also, nobody on
the team had the opportunity to see a molecular builder in true action, the
one that ASU implemented or one of the competitor's. In-house presence of
researcher TBP was fundamental to discuss and solve a lot of issues.

- Equalized partition of the task is very important. A big, non-atomizable
task should be given to two developers at the same time, with high priority
on discussing all the issues up to the minimal detail, both at the level of
design and implementation. This is also important when no previous codebase
and experience in that field is present.

- if a component design A depends on the design of other components B
and C, the assignee of A should review B and C to see if it fits the needs.

- sometimes the design depends on small details, like reading info from
a file instead of hardcoded info. Every time this decision is changed, the
design document has to be reworked. Every time it is reworked, there's a
high probability that a context switch to something else occurs, leaving the
design document in a meta-state. This makes the job of the team more difficult.

- it is very, very difficult to design for an algorithm whose expected
behavior is not well understood. This is true if the algorithm is not
understood to the developer, and it's even more true if it is not understood
(or may I better say, never seen it in action) to the spec guys.

- it is difficult, if not impossible, to give reliable time estimates 
when the above condition holds.

- we had to deliver the alpha one month earlier. A lot of time has been
wasted on use cases we never used, and a datamodel that was known to be
incorrect and overdesigned.

- the sign off of the specs should involve all the developers, not only
the project manager. The project manager sees the picture on a very high
level, but algorithmic details could have a dramatic effect on the design,
and the project manager could not have the competence and time to
pinpoint and understand all the subtle details of the domain of the application.
Please note that this is also already written in the guidelines for software
development strategy ("once the spec is finished it must be reviewed.
(...)at least one developer must be assigned to a review task.(...) the
responsability of the reviewer is to make sure that: a) all information
required for the implementation is available b) all issues associated with
the implementation are addressed". All my request of nailing down these
implementation details were said to be minor details to be addressed at a
later stage.

### Product is not that bad

The product from the alpha to the beta improved a lot. some GUI issues have
been improved and fixed in almost no time. This is very good both in
recognizing our skills and providing a smarter product.


## the minus points, in chronological order

### no research/prototype

There has not been the development of an internal prototype. This hindered a
deployment of clear specifications. see the next point.

### specs complex, difficult, not exaustive

Specifications were not clear on how to achieve algorithmically the result
they wanted. Many ambiguities were present and in some cases phrases were
deceiving, confusing, or wrong.  This made very difficult to clearly
understand the specs and how the application was supposed to behave in the
various expected conditions. Also, specification did not cover many weird
cases and how to behave in those situations. The specs were overly long and
a lot of pertinent information was mixed with less important or optional
information. 

My suggestion is that specs should be divided into four different documents

- algorithmic specifications, where the algorithms and the internal behavior are detailed
- GUI specifications, where the behavior of the user interface is
detailed.
- domain-specific explanations, an appendix explaining technical terms,
and the basic concepts needed to grasp the fundamental informations needed
to understand the specs.
- nice-to-have features and planned extensions, containing the further
ideas the R\&D would like to see in the next releases.

The specs were written by three different people, which is good. However,
the overall style suffer from a scattered layout and a feel of
unfinishedness and inconsistency. 

Please note that this is not a fault from the spec guys. They did their best
and they were able to come out with something, which was far from trivial.
My opinion is that the main issue was that they were not sure on how the product
had to work in all conditions, and postponed some questions for an alpha to
nail down everything at a later stage, with something interactive at hand. I
agree with this position, because it is understandable. That's why they
needed a prototype.

They also had different opinions about the overall user workflow. and the
final result is a compromise between opinions, time constrains, programming
skills of the members of the project, and previously available codebase.

### blind creation

None of the team actually has seen a molecular builder in action. I think
that it would have helped a lot in finding out what the expected workflow
was, how to solve various problems, etc, otherwise a potential  
"elephant and the blind men" situation is likely to arise, followed by the
"square well" situation.

### prototyping: yes or no?

During the design phase, I clearly realised that without understanding the
algorithmic steps needed for the autoadjustment, the task was not feasible.

In order to clarify all the rough spots and requirements, i started
developing a prototype of the autoadjustment. The prototype was not meant to
work, it was a guideline for understanding, written mostly in
pseudolanguage-python.

Although the Development Strategy document clearly states that "In almost any
software design, prototyping could be used by the developer as an early
verification or a proof of concept. The prototyping of software design is
thus a natural part of the design phase and is the responsability of the
developer", i was discouraged by many people in doing prototyping.. 

As a result, my inexperience led to the situation of a quite complex task to
manage, being deprived of the only way I had to actually accomplish
something. Of course, the fact that I had to do it anyway led to a sense of
guiltiness of doing something I was not supposed to do, together with a
pressure of justifying what I was doing against others' people suggestions. 

Again, this is not a blame. It was just inexperience and my poor knowledge
of the development strategy document, and i'm pretty sure that it was
beneficial to understand how to handle future situations in a cool and smart
way.

### workload imponence and loneliness

The autoadjustment was clearly a consistent part of the application, in
particular because:

- as already stated, the behaviour was not clear at the spec level, and
some weird molecule could show up presenting some unusual characteristic
- there was no precedent codebase
- there was no precedent experience

The same point can be grasped by an approximate number of lines of live
code (non autogenerated) and test code.

- Visualization 1700+1000 (2700)
- ZMatrix 1400+1700 (3100)
- CommandInterface 1000+900 (1900)
- DataModel 1000+600 (1600)
- Other 1000+100 (1100)
- AutoAdjustment 5200+4000 (9200)

please note that this is not a complain about the amount of work. I'm not
aware of the level of involvement of the other members of the group in the
project, so it could be very well that the amount of work per hour is the
same, and i'm pretty sure it was. The above numbers are only for clarifying
that the AutoAdjustment was a complex task for all the points given above.

The main issue arised during this project was to face these problems
alone, with also the idea that I had to write a design "according to the
specification" because it was what i was requested to do.

I'm not against research, I like research and solving problems, but doing
research when you are supposed to do software design can lead to some
discussion in the team, in particular for satisfying time constraints.

As a result, I was unable to provide what I was requested to do because I
was one step behind in the understanding, and it was not clear the level of
involvement and discussion I could have with ASU, since he was the main
point of reference for specs, but he wasn't in-house for a complete and
accurate disccussion of the many issues.

Many times I raised the flag pointing out that difficulties and obscure
points were present and i was not able to deal with them, but they were
classified as implementation details, and scheduled for a later stage. Fact
is that the understanding of these details was critical to provide the
design, and I had nobody to talk about these issues.

### contrasting constraints

The design of the autoadjustment was dependent on various factors

- the design choices of the datamodel and of the commands.
- how to load the central atom/dihedral templates, and which degree of expandability was
needed for the future.
- and of course, how to satisfy the specs

As a consequence, a quite large deal of uncertainty in the development of
the design (in particular routine signatures) arised.

Also, it was a request that commands must not return information to the
invoker. This request derived by the fact that the Design Patterns books do
not report a case where a command returns a status of execution. However,
the fact that the Command design pattern do not present this functionality
does not mean that it should not be provided. Indeed, some research on the
internet shows that returning the outcome of a command is a possible variant

http://www.theserverside.com/discussions/thread.tss?thread_id=28936

The autoadjustment required to return information about the success
of the operation, the abortion of the operation, or a occurred situation
that could lead to a partially optimized result. As of beta-public, this
requirement is still not satisfied, and the robustness of the code in
various error conditions is not 100 % assured. This also has led to some
degree of code duplication. Personally, i don't agree on this decision for
the design of the command pattern, also because we already have commands
(AddAtomCMD, f.ex.) returning information (the added identifier), but I can
live with it, since after all it works!

As a conclusion, the first design of the AutoAdjustment did not act as a
command, leading to a cascade of additional problems and needs from the
datamodel, the command queue manager and the commands. My inexperience here
played a quite large role, I'm sure, but summed up to the other issues
relative to autoadjustment, the result was quite difficult to handle.

Another constraint arised was relative to the loading of central atom
templates. In principle, they had to be hardcoded, then the focus changed to
file reading, then again to hardcoded. This had some implications in the
design, leading to additional delays and redoing.

### Product is not that good

The product is far from optimal, and in the public beta is still not
complying with the specifications in some points. My personal feeling is
that the spec guys had a different vision for the product. Also, the product
is far behind our direct competitor's product. 

The molecular builder is completely non standard in terms of human interface
guidelines, a bane that affects our software in general and in my opinion gives a
feeling of unfinished, unprofessional design to a product that is going to
become the flagship product. This has also be one of the
objections raised during the training course by some partecipants.

Moreover, many usability problems are present in the molecular builder, partially solved
through (again non standard) tricks that must be learned through the manual,
which is the opposite concept for a point-and-click interface.

For example, the z-matrix tool is not (and cannot be, for some unspecified
reason) always-on-top, leading to a frequent click and raise behavior
jumping between the 3D window and the z-matrix tool. This prevents the user
to put the 3d window fullscreen, otherwise the z-matrix tool will inevitably
go background when the 3D window is raised. The same happens with the
periodic table and the molecular cupboard. All three of them could be
practically embedded in a full-window sovereign application, although this
would require more time spent on widget design. 

Floating window paradigm is also difficult to use, and is particularly
annoying on all platforms. Floating windows impose the user to perform an
appropriate layout of the windows by hand, something that is not
task-oriented.

The Z-Matrix tool is not a z-matrix. Speaking as a chemist, the concept of z-matrix
is very clearly specified, and being presented with such tool with such name
would not put the product in a good light.

Many other problems are present, and they are here to stay for many other
releases, given the current priorities. This had an effect on the
personal satisfaction for the product developed.

