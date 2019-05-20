---
category: python
title: Current State of Python Packaging - 2019
---

# Current State of Python Packaging - 2019

In this post, I will try to put out the dumpster fire that is python packaging. I spent the best part of my evenings in 
the past two months to gather as much information as possible about the problem, the current solutions, what is legacy 
and what is not. 

The first source of confusion is the ambiguity surrounding terminology in python. In programming circles,
the meaning of the word "package" means an installable component (a library for example). Not so in python, where the term
for the same concept is "distribution". However, nobody really uses the term "distribution" except when they do (typically
in official documentation and Python Enhancement Proposals). Incidentally, the term is a bad choice because "distribution"
is generally used for a brand of Linux.

This is a warning that you should keep in mind, because python packaging is not really about python *packages*. 
It's about python *distributions* (python distributioning? whatever) but I'll keep calling it packaging.

**Explain me the problem please.**

The problems. Plural.

Suppose we want to create a python "thing": maybe it's a standalone program, maybe a library.
The development and usage of this thing involves the following "actors":

- **Developer**: the person or persons who write the thing.
- **CI**: an automated process that runs tests on the thing.
- **Build**: an automated or semi-automated process to go from the thing on our git to the thing someone else can install and use.
- **Enduser**: the final person or persons that use the thing. 
  They may be other developers, if the thing is a library, or they might be the general public, if it's an application.
  Or a cloud computing microservice, if the thing is a web service of some sort. You get the point.

The goal is to make all these people and machines happy, because each of them has different workflows and needs,
and these needs overlap somehow. To add to this, there is the problem that things change, new releases are made,
old releases are declared obsolete, and code is never written with no reliance on other code. There are always
dependencies, these dependencies change with time, may or may not be required, may
run quite deep and have to consider that code may be non portable between operating systems, or even inside the same
operating system. It's complicated. Bear with me.

To organise this mess somehow, every language in the world has to deal with how to package its code so that it can
be reused, installed, versioned and given some metainformation that describes, for example, "this has been compiled on
windows 64 bits" or "this will only work on macos". Python is no different, because although you may think it's an
"interpreted language" and "should run anywhere", it's not the case. Again, it's complicated, and your vision is 
incorrect. I'd love to explain you why, but I would take a digression I am unable to take here. So trust me.

**Ok, now I know the problem. What's the solution?**

A first step is to define a shippable entity that aggregates a given release of a given software. This shippable entity is what we
call package. You can ship it in two forms:

- **source**: you take the source code, put it in a zip or tar.gz, and who gets it has to compile it by himself.
- **binary**: you compile the code, publish the compiled stuff, and who gets it uses it directly with no additional fuss.

Of course with the need of packaging come the need for tools for it, specifically for the following tasks:

- create the shippable package (what I called **build** above)
- publish the shippable package somewhere so that it can be obtained by others
- download and install the shippable package
- handle dependencies. What if package A needs package B to run? What if
  package A may or may not need package B to run depending on what and how you
  are using A for. What if A needs package B only if installed on windows.
- define a runtime. In general an application needs a bunch of packages, and these packages
  need to be accessible and separated from the needs of another application. This is true
  both when you develop and when you run it.

**Can you be more specific? What do I have to do when I want to write some code?**

Sure. You want to write some code. So you generally follow these steps:

1. You create an isolated python so that you can work on multiple projects. 
   If you don't, the stuff for project A might mess up the stuff from project B.
2. You want to specify which dependencies you want, but keep into account that there are two ways of doing so: 
   **abstract** where you just say what you want in general terms (e.g. numpy) and **concrete**, where you say
   which specific version you want (e.g. numpy 1.1.0). Why the difference? I'll detail later.
   To create a real, working environment you need a concrete dependency.
3. Now you have what you need and you can start developing.

**Which tools do I have to use to do this?**

This is tricky, because there are many and they are changing. One option is
that you create the isolated python "virtual environment" with *virtualenv*,
which is part of python. Then, you use *pip* (also part of python) to install
the packages that you depend on. Typing them one by one is boring and not
really automatic, so people put the concrete dependencies (with hardcoded
versions) in a file and then tell pip: "go read that file and install what's in
there". And pip obliges.  This file is the famous requirements.txt you might 
have seen around.

**What is pip?**

A program that downloads packages and installs them. If they have dependencies, it installs the dependencies too.

**How?**

It goes to a remote service, pypi, finds the package by name and version, downloads it, and installs it.
But it does a little more than that, because this package may have additional dependencies itself, 
so it gets those too, and installs them.

**Why do you say that this approach "is an option"?**

Because it gets boring and complex quite quickly. You have to manage by hand
your direct dependencies versions for different platforms For example, on
windows you might need a package, and on linux another and you end up with
win-requirements.txt, linux-requirements.txt etc.  

You also have to consider that some of your dependencies are real dependencies
that you use and need for your software to work. Other dependencies are only
required to run tests, and so are really dependencies that as a developer, or a
CI machine, needs, but for someone that wants to use your software, they are not 
needed, so they are not dependencies. So now you have dev-requirement.txt as well.

Also, your final python environment is made of not only your direct
dependencies, but also its subdependencies.  What if you depend on A and B
directly, and they both depend on C. Which version of C should it be installed?
Is it even possible to do so, if, say, A wants C version 2 and B wants C
version 1?

It's a mess, and you don't want to deal with this mess.

In general, pip decides which version to install in a rather primitive way, and
can eventually paint itself into a corner and give you either a broken
environment or an error. So you need a more complex process, and basically 
leave pip with the plain task of downloading well defined versions, leaving the
task of deciding which versions to install to something else.

**For example?**

pipenv is one. It puts together virtualenv, pip and some magic so that you give a list of dependencies
and it tries its best to resolve the mess above and give you an environment that works.
poetry is another. People talk about the two and there's some feud going on because of political
and human reason. Most people seem to prefer poetry.

Some companies, such as Continuum and Enthought, have their own version (conda and edm) which are
generally one step above for some additional platform complexities. We don't go into that detail here.

**Which one is better? pipenv or poetry?**

I have no clue and take no stance. As I said, people seem to prefer poetry. 

**Ok so the bottom line is to use poetry, that creates an environment so that I can install my dependencies in an environment and then code.**

Well yes. But we haven't even started talking about building yet. That is, once you have your code, how do you create something
you can release?

**Right, is that what setup.py, setuptools and distutils are about?**

Yes and no. Originally, when you wanted to create source or binary distributions you used a standard lib module called distutils.
The idea was to have a python script, called setup.py, that did its magic to create something you could give to others. The
script could have been named anything else, but kind of became the standard and some tools (notably pip) specifically look for it. 
For example, if pip can't find a built version of the dependency you need, it will download the source and build it, basically running
setup.py and hoping for the best.

However... distutils stinks, so someone came up with alternatives that do a lot more stuff that distutils didn't do.
Big fight, big mess, long story short setuptools is better, everybody uses it. setuptools keeps using setup.py
to give the illusion that nothing has changed and the process to create your stuff is still the same.

**Why hoping for the best?**

Because there's no guarantee for pip that when it runs setup.py it can actually run. it's a python script
and may have some dependencies in itself that you have no way of specifying. It's a chicken and end problem.

**So setuptools and setup.py is the way to go when I need to build my stuff for release??**

It was. Not anymore, or maybe yes. It depends. See, the current situation is
that nobody wants setuptools to be the only one able to decide how packages are
made. The reason is deeper than that, and there are technicalities involved that
go too deep, but if you are curious take a look at PEP 518. The most egregious
is the following: Briefly said, if pip wants to build a dependency it
downloaded, how does it know what to download to even start executing the setup
script? Yes, it can assume it needs setuptools, but it's just an assumption.
And you don't have setuptools in your environment, so how does pip know that 
it's needed to build this package or that package?

In any case, they decided that anybody that want to write their own tool to
package should be able to do so, and therefore you need just another meta step
to define which package system you want to use in order to build your stuff.

**pyproject.toml?**

Exactly. More specifically, a subsection in it that defines the "backend" you
want to use. If you want to use a different build backend, you can say so. If
you don't, then the assumption is that you are using setuptools and therefore
whatever tool you need will look for setup.py, execute it, and hopefully build
something. 

setup.py is just going eventually to disappear, or not. setup.py is a way
**setuptools** (and before that, distutils) describes how to create a build.
Another tool might use some other approach. Possibly, they will use
pyproject.toml, adding some stuff in there in some tool specific keys.

Also, in pyproject.toml you can finally specify the dependencies needed to even
perform the build, removing the chicken egg problem given above.

**Couldn't they have included setuptools in the standard library instead?**

Maybe, but the problem is that the standard library has veeery slooow release
cycles.  The slowness of improvements over distutils is what triggered the
implementation of setuptools in the first place.

**Ok, so if I understand correctly: to create my working environment I need poetry. To create the built package, I need setup.py and setuptools. or pyproject.toml?**

If you want to use setuptools, you need a setup.py, but then you have the problem
that people will need setuptools installed to install your package.

**Which other tools can I use instead of setuptools?**

you can use flit, or poetry itself.

**Wasn't poetry something to install dependencies?**

Yes but it also does building. pipenv doesn't do that.

**By the way, if I use setup.py I have to write the dependencies, why? What is their relationship with the ones I installed with pipenv/poetry/requirements.txt?**

Those are the abstract dependencies that are needed for your package to run, and are the dependencies that
pip needs when it's time to decide what to download and install next. You should generally put loose (unversioned)
dependencies in there, because if you don't... remember when I told you about A and B having a common dependency C?
what if A says "I want to use C version 1.2.1" and B says "I want to use C version 1.2.2"? 

Pip has no choice when it's time to build a source distribution it downloaded. It doesn't know anything about
your requirements.txt. All it knows is that it needs to run setup.py, which in turns uses setuptools to then invoke pip
again to resolve the abstract dependencies written there into something concrete it can install.

**What about eggs? easy install? .egg-info directories**

Forget them. They are legacy. Always build wheels for your binary distributions.

**What about .pyz?**

Forget it. Unrelated to packaging, strictly speaking. It could be useful in some circumstances. See PEP-441 for more info.

**What about pyinstaller?**

It is also unrelated to packaging, strictly speaking. PyInstaller is a tool
that you involve when you want to create an executable.  It addresses this
need: get a final application on your user's desktop. Packaging is about
managing the network of dependencies, libraries and tools that you need to
create that application that you might, or might not, create with pyinstaller.

**What's with Wheels?**

Rememeber when I said that pip needs to know what to download from pypi to
download the right versions and the right operating system? a Wheel is a file
that contains the stuff to install, and has some special, well-codified  name
so that pip can make decisions as it installs dependencies and subdependencies.

Wheels file names (pep-0425) contain tags that act as metadata, so that when
something has been compiled for, say CPython, it knows the version, the ABI,
etc. There is a standard layout of this tags in the filename, and there are
particular keywords in that metadata that have specific meanings.

**Ok, but how do I install something I have the sources of? python setup.py?**

No. Use `pip install .` because it guarantees you can uninstall it afterwards.

**Can you give me a shorter version? What should I do as of today in 2019?**

To develop:
- Create your development environment with poetry, specifying the direct dependencies of your project with a strict version.
  This way you ensure your development (and testing) environment is always reproducible.
- Create a pyproject.toml and use poetry as a backend to create your source and binary distributions.

